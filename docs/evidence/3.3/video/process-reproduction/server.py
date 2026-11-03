"""Local development evidence viewer: two fixed controls, no arbitrary commands."""
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = ROOT / "docs/evidence/3.3/video/process-reproduction"
PYTHON = ROOT / "backend/.venv/bin/python"
OLD = "2cc923846654e1492cea4f82494c4f4874674532"
CURRENT = "2f00ffb0c72826a0a2b8a8fa000eb04971e2ff53"
lock = threading.Lock()

def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])

DIFF = git("diff", OLD, CURRENT, "--", "backend/app/explanations.py", "backend/app/repository.py").decode()
def excerpt(file, first, last):
    lines = git("show", f"{CURRENT}:{file}").decode().splitlines()
    return {"file": file, "source_commit": CURRENT, "first_line": first, "last_line": last,
            "code": "\n".join(f"{number:3}  {lines[number - 1]}" for number in range(first, last + 1))}
SNIPPETS = {"adapter": excerpt("backend/app/explanations.py", 201, 210),
            "repository": excerpt("backend/app/repository.py", 242, 250),
            "persistence": excerpt("backend/app/repository.py", 250, 254)}

def run(label):
    commit = OLD if label == "before" else CURRENT
    with lock, tempfile.TemporaryDirectory(prefix="peyce-process-s17-") as directory:
        target = Path(directory)
        for file in git("ls-tree", "-r", "--name-only", commit, "backend/app").decode().splitlines():
            if file.endswith(".py"):
                output = target / file
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(git("show", f"{commit}:{file}"))
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "PYTHON_DOTENV_DISABLED": "1",
               "PYTHONNOUSERSITE": "1", "PEYCE_MODEL_MODE": "mock",
               "PEYCE_DB_PATH": str(target / "fixture.sqlite3")}
        command = [str(PYTHON), str(HERE / "run_case.py"), str(target / "backend"),
                   str(target / "fixture.sqlite3"), commit, label.upper()]
        result = subprocess.run(command, cwd=target, env=env, capture_output=True, text=True, timeout=20)
        if result.returncode:
            return {"result": "RUNNER ERROR", "exit_code": result.returncode,
                    "stdout": result.stdout[-5000:], "stderr": result.stderr[-5000:]}
        value = json.loads(result.stdout)
        value["executed_at_utc"] = datetime.now(timezone.utc).isoformat()
        value["runner_command"] = "backend/.venv/bin/python .verification/process-recording-viewer/run_case.py <extracted pinned backend> <new temporary fixture DB> <commit> " + label.upper()
        (OUT / (label + ".json")).write_text(json.dumps(value, indent=2) + "\n")
        return value

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass
    def send(self, body, status=200, kind="application/json"):
        data = body.encode()
        self.send_response(status)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)
    def do_GET(self):
        if self.path == "/":
            self.send((HERE / "index.html").read_text(), kind="text/html; charset=utf-8")
        elif self.path == "/diff":
            self.send(DIFF, kind="text/plain; charset=utf-8")
        elif self.path in ("/code/adapter", "/code/repository", "/code/persistence"):
            self.send(json.dumps(SNIPPETS[self.path.rsplit("/", 1)[-1]]))
        elif self.path in ("/result/before", "/result/retest"):
            file = OUT / (self.path.rsplit("/", 1)[-1] + ".json")
            self.send(file.read_text() if file.exists() else "{}")
        else:
            self.send("{}", 404)
    def do_POST(self):
        if self.path not in ("/run/before", "/run/retest"):
            return self.send("{}", 404)
        if self.headers.get("Origin") not in (None, "http://127.0.0.1:5182"):
            return self.send("{}", 403)
        result = run(self.path.rsplit("/", 1)[-1])
        self.send(json.dumps(result))

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "source-change.diff").write_text(DIFF)
    print("Peyce development evidence viewer: http://127.0.0.1:5182/", flush=True)
    ThreadingHTTPServer(("127.0.0.1", 5182), Handler).serve_forever()
