// All offsets use one session-relative monotonic clock. Background time is counted.
export class SequenceTimer {
  constructor() { this.instruction = null; this.closed = []; this.open = new Map(); this.result = null; }
  showInstructions(at) { if (this.instruction === null) this.instruction = at; }
  exclude(cause, at) { if (!this.open.has(cause)) this.open.set(cause, at); }
  include(cause, at) {
    if (this.open.has(cause)) { this.closed.push({ start_ms: this.open.get(cause), end_ms: at, cause }); this.open.delete(cause); }
  }
  finish(at) {
    if (this.result || this.instruction === null) return this.result;
    for (const cause of [...this.open.keys()]) this.include(cause, at);
    const intervals = this.closed.map(p => ({ ...p, start_ms: Math.max(this.instruction, p.start_ms), end_ms: Math.min(at, p.end_ms) })).filter(p => p.end_ms > p.start_ms);
    let edge = this.instruction, excluded = 0;
    for (const p of [...intervals].sort((a, b) => a.start_ms - b.start_ms)) {
      excluded += Math.max(0, p.end_ms - Math.max(edge, p.start_ms)); edge = Math.max(edge, p.end_ms);
    }
    const raw = at - this.instruction;
    return this.result = { raw_ms: raw, counted_ms: raw - excluded, excluded_ms: excluded, excluded_intervals: intervals, instruction_ms: this.instruction, finish_ms: at, entry_ms: this.instruction };
  }
}
