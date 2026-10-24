"""SQLite transactions, immutable revisions, structured turns and safe provenance."""
from contextlib import contextmanager
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from .domain import CONTENT_VERSION, POLICY_VERSION, PROMPT_VERSION, QUESTION_VERSION, QUESTIONS, match_exercise


def stamp():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


class Conflict(Exception):
    pass


class Missing(Exception):
    pass


class Repository:
    def __init__(self, db_path):
        self.db_path = str(db_path)

    @contextmanager
    def connection(self):
        connection = sqlite3.connect(self.db_path, timeout=2)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def initialize(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            version = db.execute("PRAGMA user_version").fetchone()[0]
            if version not in (0, 1):
                raise RuntimeError("Unsupported schema version; database was not reset")
            db.execute("PRAGMA journal_mode=WAL")
            db.executescript("""
                CREATE TABLE IF NOT EXISTS sessions (
                  id TEXT PRIMARY KEY, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
                  ended_at TEXT, revision INTEGER NOT NULL, status TEXT NOT NULL,
                  exercise TEXT, color TEXT NOT NULL, color_explicit INTEGER NOT NULL,
                  schema_version INTEGER NOT NULL DEFAULT 1, question_version TEXT NOT NULL,
                  policy_version TEXT NOT NULL, content_version TEXT NOT NULL,
                  context TEXT NOT NULL DEFAULT 'fictional-local-coursework',
                  snapshot_json TEXT NOT NULL, result_json TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS revisions (
                  session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
                  revision INTEGER NOT NULL, snapshot_json TEXT NOT NULL,
                  result_json TEXT NOT NULL, created_at TEXT NOT NULL,
                  PRIMARY KEY(session_id,revision));
                CREATE TABLE IF NOT EXISTS operations (
                  operation_id TEXT PRIMARY KEY,
                  session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
                  revision INTEGER NOT NULL, kind TEXT NOT NULL, payload_json TEXT NOT NULL,
                  response_json TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS turns (
                  id INTEGER PRIMARY KEY, session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
                  revision INTEGER NOT NULL, sequence INTEGER NOT NULL, role TEXT NOT NULL,
                  question_id TEXT, answer_id INTEGER, skipped INTEGER NOT NULL DEFAULT 0,
                  text TEXT NOT NULL, question_version TEXT NOT NULL, source TEXT NOT NULL,
                  created_at TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS lifecycle (
                  event_id TEXT PRIMARY KEY, session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
                  revision INTEGER NOT NULL, kind TEXT NOT NULL, at_ms REAL NOT NULL,
                  active_ms REAL NOT NULL, cause TEXT NOT NULL, created_at TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS explanations (
                  request_id TEXT PRIMARY KEY, session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
                  revision INTEGER NOT NULL, mode TEXT NOT NULL, model_id TEXT NOT NULL,
                  prompt_version TEXT NOT NULL, question_version TEXT NOT NULL, policy_version TEXT NOT NULL,
                  reason_code TEXT NOT NULL, outcome TEXT NOT NULL, validation TEXT NOT NULL,
                  fragments_json TEXT, references_json TEXT NOT NULL DEFAULT '[]',
                  text TEXT NOT NULL, stale INTEGER NOT NULL DEFAULT 0,
                  created_at TEXT NOT NULL, updated_at TEXT NOT NULL, response_json TEXT);
                CREATE TABLE IF NOT EXISTS live_budget (
                  id INTEGER PRIMARY KEY CHECK(id=1), attempts INTEGER NOT NULL,
                  reserved_usd REAL NOT NULL);
                INSERT OR IGNORE INTO live_budget(id,attempts,reserved_usd) VALUES(1,0,0);
                PRAGMA user_version=1;
            """)
            # A restart cannot assert that previously active pacing was completed.
            for row in db.execute("SELECT id,snapshot_json FROM sessions WHERE status IN ('active','paused')").fetchall():
                snapshot = json.loads(row["snapshot_json"])
                snapshot["status"] = "interrupted"
                db.execute("UPDATE sessions SET status='interrupted',snapshot_json=?,updated_at=? WHERE id=?", (encoded(snapshot), stamp(), row["id"]))
            db.execute("UPDATE explanations SET outcome='obsolete',validation='interrupted-request',stale=1,updated_at=? WHERE outcome='pending'", (stamp(),))

    def save(self, session_id, snapshot):
        value = snapshot.model_dump(mode="json") if hasattr(snapshot, "model_dump") else snapshot
        payload = encoded(value)
        revision, operation_id = value["revision"], value["operation_id"]
        result = match_exercise(value["answers"], value["direct_choice"])
        response = dict(session_id=session_id, revision=revision, saved=True, result=result, status=value["status"])
        now = stamp()
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            replay = db.execute("SELECT * FROM operations WHERE operation_id=?", (operation_id,)).fetchone()
            if replay:
                if replay["session_id"] != session_id or replay["kind"] != "snapshot" or replay["payload_json"] != payload:
                    raise Conflict("Operation identifier was already used for a different action")
                return json.loads(replay["response_json"])
            current = db.execute("SELECT revision,snapshot_json FROM sessions WHERE id=?", (session_id,)).fetchone()
            if current and revision <= current["revision"]:
                raise Conflict("Snapshot revision must be newer than the saved revision")
            if not current and revision != 1:
                raise Conflict("A new session starts at revision 1")
            if current:
                previous_events = json.loads(current["snapshot_json"])["events"]
                if value["events"][:len(previous_events)] != previous_events:
                    raise Conflict("Previously saved lifecycle events must remain an unchanged prefix")
            values = (now, now if value["status"] in ("finished", "stopped", "completed") else None,
                      revision, value["status"], value["exercise"], value["color"], int(value["color_explicit"]), payload, encoded(result))
            if current:
                db.execute("UPDATE sessions SET updated_at=?,ended_at=?,revision=?,status=?,exercise=?,color=?,color_explicit=?,snapshot_json=?,result_json=? WHERE id=?", (*values, session_id))
            else:
                db.execute("INSERT INTO sessions(id,created_at,updated_at,ended_at,revision,status,exercise,color,color_explicit,snapshot_json,result_json,question_version,policy_version,content_version) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (session_id, now, *values, QUESTION_VERSION, POLICY_VERSION, CONTENT_VERSION))
            db.execute("INSERT INTO revisions VALUES(?,?,?,?,?)", (session_id, revision, payload, encoded(result), now))
            for index, received in enumerate(value["answered"]):
                if not received:
                    continue
                qid, question, labels = QUESTIONS[index]
                answer = value["answers"][index]
                for role, text, sequence, answer_id, skipped in (("assistant", question, index * 2, None, 0), ("user", "Skipped this question" if answer is None else labels[answer], index * 2 + 1, answer, int(answer is None))):
                    db.execute("INSERT INTO turns(session_id,revision,sequence,role,question_id,answer_id,skipped,text,question_version,source,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)", (session_id, revision, sequence, role, qid, answer_id, skipped, text, QUESTION_VERSION, "structured-turn", now))
            for event in value["events"]:
                old = db.execute("SELECT * FROM lifecycle WHERE event_id=?", (event["id"],)).fetchone()
                if old and (old["session_id"] != session_id or any(old[k] != event[k] for k in ("kind", "at_ms", "active_ms", "cause"))):
                    raise Conflict("An existing lifecycle event cannot be changed")
                db.execute("INSERT OR IGNORE INTO lifecycle VALUES(?,?,?,?,?,?,?,?)", (event["id"], session_id, revision, event["kind"], event["at_ms"], event["active_ms"], event["cause"], now))
            db.execute("INSERT INTO operations VALUES(?,?,?,?,?,?)", (operation_id, session_id, revision, "snapshot", payload, encoded(response)))
        return response

    def get(self, session_id):
        with self.connection() as db:
            row = db.execute("SELECT * FROM sessions WHERE id=?", (session_id,)).fetchone()
            if not row:
                raise Missing("Saved session not found")
            result = dict(row)
            result.update(json.loads(result.pop("snapshot_json")))
            result["result"] = json.loads(result.pop("result_json"))
            result["turns"] = [dict(t) | {"superseded": t["revision"] != result["revision"]} for t in db.execute("SELECT * FROM turns WHERE session_id=? ORDER BY revision,sequence,id", (session_id,))]
            result["lifecycle"] = [dict(t) | {"id": t["event_id"]} for t in db.execute("SELECT * FROM lifecycle WHERE session_id=? ORDER BY at_ms,rowid", (session_id,))]
            result["explanations"] = []
            for t in db.execute("SELECT * FROM explanations WHERE session_id=? ORDER BY created_at,rowid", (session_id,)):
                attempt = dict(t)
                attempt["fragments"] = json.loads(attempt.pop("fragments_json")) if attempt["fragments_json"] else None
                attempt["references"] = json.loads(attempt.pop("references_json"))
                attempt.pop("response_json")
                attempt["superseded"] = attempt["revision"] != result["revision"]
                result["explanations"].append(attempt)
            return result

    def list(self):
        with self.connection() as db:
            rows = db.execute("SELECT id,created_at,updated_at,exercise,status,color,result_json,snapshot_json FROM sessions ORDER BY updated_at DESC,id DESC").fetchall()
            result = []
            for row in rows:
                value = dict(row)
                snapshot = json.loads(value.pop("snapshot_json"))
                value["result"] = json.loads(value.pop("result_json"))
                value["timing"] = snapshot["timing"]
                attempt = db.execute("SELECT mode,model_id,outcome,text,revision,stale FROM explanations WHERE session_id=? ORDER BY created_at DESC,rowid DESC LIMIT 1", (value["id"],)).fetchone()
                value["explanation"] = dict(attempt) if attempt else None
                result.append(value)
            return result

    def clear(self):
        with self.connection() as db:
            db.execute("DELETE FROM sessions")
            # Do not clear the global live-attempt guard with the history UI.
        return {"deleted": True}

    def interrupt(self, session_id, request):
        payload = encoded(request.model_dump(mode="json"))
        operation_id = str(request.operation_id)
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            old = db.execute("SELECT * FROM operations WHERE operation_id=?", (operation_id,)).fetchone()
            if old:
                if old["kind"] != "interrupt" or old["session_id"] != session_id or old["payload_json"] != payload:
                    raise Conflict("Operation identifier belongs to another action")
                return json.loads(old["response_json"])
            row = db.execute("SELECT status,revision,snapshot_json FROM sessions WHERE id=?", (session_id,)).fetchone()
            if not row:
                raise Missing("Saved session not found")
            if row["revision"] != request.revision:
                raise Conflict("Interruption belongs to an older revision")
            status = row["status"]
            if status in ("active", "paused"):
                status = "interrupted"
                value = json.loads(row["snapshot_json"])
                value["status"] = status
                db.execute("UPDATE sessions SET status=?,snapshot_json=?,updated_at=? WHERE id=?", (status, encoded(value), stamp(), session_id))
            response = dict(session_id=session_id, revision=request.revision, status=status, saved=True)
            db.execute("INSERT INTO operations VALUES(?,?,?,?,?,?)", (operation_id, session_id, request.revision, "interrupt", payload, encoded(response)))
            return response

    def begin_explanation(self, session_id, request, mode, model_id):
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            old = db.execute("SELECT * FROM explanations WHERE request_id=?", (str(request.request_id),)).fetchone()
            if old:
                if old["session_id"] != session_id or old["revision"] != request.revision:
                    raise Conflict("Explanation request identifier belongs to another revision")
                current = db.execute("SELECT revision,status FROM sessions WHERE id=?", (session_id,)).fetchone()
                stale = bool(old["stale"]) or not current or current["revision"] != request.revision or current["status"] != "ready"
                if old["response_json"]:
                    response = json.loads(old["response_json"])
                    if stale:
                        response.update(stale=True, status="obsolete")
                    return None, response
                return None, dict(session_id=session_id, revision=request.revision, request_id=str(request.request_id), mode=old["mode"], model_id=old["model_id"], status="obsolete" if stale else "fallback", text=old["text"], fragments=None, references=[], stale=stale)
            row = db.execute("SELECT * FROM sessions WHERE id=?", (session_id,)).fetchone()
            if not row:
                raise Missing("Saved session not found")
            if row["revision"] != request.revision or row["status"] != "ready":
                raise Conflict("Explanation requires the current ready revision")
            snapshot, result = json.loads(row["snapshot_json"]), json.loads(row["result_json"])
            now = stamp()
            db.execute("INSERT INTO explanations(request_id,session_id,revision,mode,model_id,prompt_version,question_version,policy_version,reason_code,outcome,validation,text,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (str(request.request_id), session_id, request.revision, mode, model_id, PROMPT_VERSION, QUESTION_VERSION, POLICY_VERSION, result["code"], "pending", "pending", result["reason"], now, now))
            return (snapshot, result), None

    def reserve_live_attempt(self, settings):
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT attempts,reserved_usd FROM live_budget WHERE id=1").fetchone()
            if not settings.live_configured or row["attempts"] >= settings.live_max_attempts or row["reserved_usd"] + settings.attempt_reservation_usd > settings.approved_budget_usd:
                return False
            db.execute("UPDATE live_budget SET attempts=attempts+1,reserved_usd=reserved_usd+? WHERE id=1", (settings.attempt_reservation_usd,))
            return True

    def finish_explanation(self, session_id, request, response, outcome):
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            current = db.execute("SELECT revision,status FROM sessions WHERE id=?", (session_id,)).fetchone()
            stale = not current or current["revision"] != request.revision or current["status"] != "ready"
            response["stale"] = stale
            if stale:
                response["status"] = "obsolete"
            if current:
                db.execute("UPDATE explanations SET outcome=?,validation=?,model_id=?,fragments_json=?,references_json=?,text=?,stale=?,updated_at=?,response_json=? WHERE request_id=?", (response["status"], outcome, response["model_id"], encoded(response["fragments"]) if response["fragments"] else None, encoded(response["references"]), response["text"], int(stale), stamp(), encoded(response), str(request.request_id)))
                if response["status"] == "validated":
                    db.execute("INSERT INTO turns(session_id,revision,sequence,role,text,question_version,source,created_at) VALUES(?,?,99,'assistant',?,?,?,?)", (session_id, request.revision, response["text"], QUESTION_VERSION, "validated-" + response["mode"] + "-acknowledgment", stamp()))
            return response
