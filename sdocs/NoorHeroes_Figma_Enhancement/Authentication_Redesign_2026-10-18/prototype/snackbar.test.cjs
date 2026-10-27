const { test } = require('node:test');
const assert = require('node:assert/strict');
const { createSnackbar } = require('./snackbar-core.cjs');

function setup(maxPending = 2) {
  const renders = [], tasks = new Map(); let id = 0;
  const snackbar = createSnackbar({ maxPending, render: (item, busy) => renders.push({ item, busy }),
    schedule: (fn, ms) => { tasks.set(++id, { fn, ms }); return id; },
    cancel: token => tasks.delete(token) });
  return { snackbar, renders, tasks, current: () => renders.at(-1)?.item };
}

test('one active message, deduplication, bounded FIFO, and no blank feedback', () => {
  const { snackbar, current } = setup();
  assert.equal(snackbar.show({ message: '   ' }), false);
  assert.equal(snackbar.show({ message: 'Offline', tone: 'error' }), true);
  assert.equal(snackbar.show({ message: 'Offline', tone: 'error' }), false);
  assert.equal(snackbar.show({ message: 'Saved', tone: 'success' }), true);
  assert.equal(snackbar.show({ message: 'Notice', tone: 'info' }), true);
  assert.equal(snackbar.show({ message: 'Overflow', tone: 'warning' }), false);
  assert.equal(current().message, 'Offline');
  snackbar.dismiss(); assert.equal(current().tone, 'success');
  snackbar.dismiss(); assert.equal(current().tone, 'info');
  snackbar.clear(); assert.equal(current(), null);
});

test('persistent actionable errors and timed non-action statuses', () => {
  const { snackbar, tasks, current } = setup();
  snackbar.show({ message: 'Offline', tone: 'error', actionLabel: 'Retry', action() {} });
  assert.equal(tasks.size, 0);
  snackbar.dismiss(); snackbar.show({ message: 'Saved', tone: 'success' });
  assert.equal([...tasks.values()][0].ms, 6000);
  [...tasks.values()][0].fn(); assert.equal(current(), null);
});

test('an action executes once and queued feedback waits for its result', async () => {
  const { snackbar, current } = setup(); let calls = 0, complete;
  snackbar.show({ message: 'Retry', actionLabel: 'Retry', action: () => { calls++; return new Promise(r => complete = r); } });
  snackbar.show({ message: 'Next', tone: 'info' });
  const work = snackbar.activate(); snackbar.activate();
  assert.equal(calls, 1); assert.equal(current(), null);
  complete(); await work; assert.equal(current().message, 'Next');
});

test('clear cancels stale timers, keeps semantics and operation-specific retry callbacks', async () => {
  const { snackbar, tasks, current } = setup(); let operation;
  snackbar.show({ message: 'Offline', key: 'identifier', actionLabel: 'Retry', action: () => operation = 'identifier' });
  snackbar.show({ message: 'Offline', key: 'google', actionLabel: 'Retry', action: () => operation = 'google' });
  await snackbar.activate(); assert.equal(operation, 'identifier');
  await snackbar.activate(); assert.equal(operation, 'google');
  snackbar.show({ message: 'Warning', tone: 'warning' });
  snackbar.refresh(); assert.equal(current().tone, 'warning');
  snackbar.clear(); assert.equal(tasks.size, 0); assert.equal(current(), null);
});
