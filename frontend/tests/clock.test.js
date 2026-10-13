import test from 'node:test';
import assert from 'node:assert/strict';
import { DURATION_MS, phaseAt, PhaseClock } from '../src/clock.js';

const close = (actual, expected, tolerance = 1e-9) => assert.ok(Math.abs(actual - expected) <= tolerance, `${actual} should be within ${tolerance} of ${expected}`);

test('six cycles each contain exactly four seconds of inhale and six seconds of exhale', () => {
  assert.equal(DURATION_MS, 60_000);
  for (let cycle = 0; cycle < 6; cycle += 1) {
    const start = cycle * 10_000;
    assert.equal(phaseAt(start).phase, 'inhale');
    assert.equal(phaseAt(start + 3999.999).phase, 'inhale');
    assert.equal(phaseAt(start + 4000).phase, 'exhale');
    assert.equal(phaseAt(start + 9999.999).phase, 'exhale');
    assert.equal(phaseAt(start).cycle, cycle + 1);
    assert.equal(phaseAt(start + 9999.999).cycle, cycle + 1);
    assert.equal(phaseAt(start).done, false);
  }
  assert.deepEqual(phaseAt(60_000), { elapsed: 60_000, phase: 'exhale', inflation: 0, cycle: 6, done: true });
});

test('inflation is low/mid/full at meaningful pacing landmarks', () => {
  close(phaseAt(0).inflation, 0);
  close(phaseAt(2000).inflation, 0.5);
  close(phaseAt(4000).inflation, 1);
  close(phaseAt(7000).inflation, 0.5);
  close(phaseAt(10_000).inflation, 0);
});

test('visual inflation stays continuous across inhale/exhale and cycle boundaries', () => {
  const epsilon = 0.001;
  for (let cycle = 0; cycle < 6; cycle += 1) {
    const full = cycle * 10_000 + 4000;
    close(phaseAt(full - epsilon).inflation, phaseAt(full).inflation);
    close(phaseAt(full + epsilon).inflation, phaseAt(full).inflation);
    const boundary = (cycle + 1) * 10_000;
    close(phaseAt(boundary - epsilon).inflation, phaseAt(boundary).inflation);
    close(phaseAt(boundary + epsilon).inflation, phaseAt(boundary).inflation);
  }
});

test('clamped phase values remain within the sixty-second experiment', () => {
  assert.deepEqual(phaseAt(-500), phaseAt(0));
  assert.deepEqual(phaseAt(90_000), phaseAt(60_000));
  for (let elapsed = 0; elapsed <= 60_000; elapsed += 17) {
    const state = phaseAt(elapsed);
    assert.ok(state.inflation >= 0 && state.inflation <= 1);
    assert.ok(state.cycle >= 1 && state.cycle <= 6);
    assert.equal(state.done, false);
  }
});

test('one monotonic input clock drives phase, elapsed time, and completion despite irregular frames', () => {
  const clock = new PhaseClock();
  const anchor = 500_000;
  clock.start(anchor);
  let previous = 0;
  for (const offset of [0, 16, 33, 499, 2000, 3999, 4000, 11_379, 28_455, 59_999, 60_000, 120_000]) {
    const state = clock.sample(anchor + offset);
    assert.ok(state.elapsed >= previous);
    assert.deepEqual(state, phaseAt(offset));
    previous = state.elapsed;
  }
});

test('pause freezes the phase and resume continues from that exact point', () => {
  const clock = new PhaseClock();
  clock.start(1000);
  clock.pause(3500);
  const paused = clock.sample(3500);
  assert.equal(paused.elapsed, 2500);
  assert.deepEqual(clock.sample(90_000), paused);
  clock.pause(100_000); // Repeated pause is idempotent.
  assert.deepEqual(clock.sample(101_000), paused);
  clock.resume(110_000);
  assert.deepEqual(clock.sample(110_000), paused);
  assert.equal(clock.sample(111_500).elapsed, 4000);
  assert.equal(clock.sample(111_500).phase, 'exhale');
  clock.resume(112_000); // Repeated resume must not reanchor a running clock.
  assert.equal(clock.sample(112_000).elapsed, 4500);
});

test('background-pause contract excludes hidden time and does not flash missed cycles on return', () => {
  // The controller calls pause at visibility loss and requests deliberate resume.
  // This verifies the pure clock contract, not the browser visibility event wiring.
  const clock = new PhaseClock();
  clock.start(0);
  clock.pause(7500);
  const beforeBackground = clock.sample(7500);
  assert.equal(beforeBackground.phase, 'exhale');
  assert.equal(beforeBackground.cycle, 1);
  assert.deepEqual(clock.sample(607_500), beforeBackground);
  clock.resume(607_500);
  assert.deepEqual(clock.sample(607_500), beforeBackground);
  assert.equal(clock.sample(608_000).elapsed, 8000);
  assert.equal(clock.sample(608_000).cycle, 1);
  assert.equal(clock.sample(610_000).elapsed, 10_000);
  assert.equal(clock.sample(610_000).cycle, 2);
});

test('completion cannot resume beyond six cycles, and a new start resets only deliberately', () => {
  const clock = new PhaseClock();
  clock.start(0);
  clock.pause(75_000);
  assert.equal(clock.sample(75_000).done, true);
  clock.resume(80_000);
  assert.deepEqual(clock.sample(90_000), phaseAt(60_000));
  clock.start(100_000);
  assert.deepEqual(clock.sample(100_000), phaseAt(0));
  assert.equal(clock.sample(101_000).elapsed, 1000);
});
