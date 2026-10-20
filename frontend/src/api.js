export async function api(path, { method = 'GET', body, fault, signal } = {}) {
  const timeoutController = signal ? null : new AbortController();
  const timeout = timeoutController ? setTimeout(() => timeoutController.abort(), 6000) : null;
  try {
  const response = await fetch(`/api${path}`, {
    method, signal: signal || timeoutController.signal, headers: { 'Content-Type': 'application/json', ...(fault ? { 'X-Peyce-Test-Fault': fault } : {}) },
    ...(body === undefined ? {} : { body: JSON.stringify(body) }),
  });
  if (!response.ok) throw new Error(`Local service returned ${response.status}`);
  return await response.json();
  } finally { if (timeout) clearTimeout(timeout); }
}

// A failed write does not poison later saves. Retrying the same operation is idempotent.
export class SaveQueue {
  constructor(write) { this.write = write; this.tail = Promise.resolve(); }
  enqueue(payload) {
    const captured = structuredClone(payload);
    const job = this.tail.catch(() => {}).then(() => this.write(captured));
    this.tail = job;
    return job;
  }
}
