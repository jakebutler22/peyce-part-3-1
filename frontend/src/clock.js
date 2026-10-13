export const DURATION_MS = 60000;
export function phaseAt(elapsed) {
  const time = Math.max(0, Math.min(DURATION_MS, elapsed));
  const local = time === DURATION_MS ? 10000 : time % 10000;
  const inhale = local < 4000;
  const linear = inhale ? local / 4000 : 1 - (local - 4000) / 6000;
  return { elapsed: time, phase: inhale ? 'inhale' : 'exhale', inflation: (1 - Math.cos(Math.PI * linear)) / 2, cycle: Math.min(6, Math.floor(time / 10000) + 1), done: time >= DURATION_MS };
}
export class PhaseClock {
  constructor() { this.elapsed = 0; this.anchor = null; }
  start(now) { this.elapsed = 0; this.anchor = now; }
  sample(now) { return phaseAt(this.elapsed + (this.anchor === null ? 0 : Math.max(0, now - this.anchor))); }
  pause(now) { this.elapsed = this.sample(now).elapsed; this.anchor = null; }
  resume(now) { if (this.anchor === null && this.elapsed < DURATION_MS) this.anchor = now; }
}
