(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.NHFeedback = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  function createSnackbar({ render = () => {}, schedule = setTimeout, cancel = clearTimeout, maxPending = 8 } = {}) {
    const queue = [], keys = new Set();
    let current = null, timer, generation = 0, processing = false;
    const limit = Number.isFinite(maxPending) ? Math.max(0, Math.floor(maxPending)) : 8;
    function stopTimer() { generation++; if (timer !== undefined) cancel(timer); timer = undefined; }
    function next() {
      if (processing || current || !queue.length) { render(current, processing); return; }
      current = queue.shift(); render(current, false);
      if (current.duration > 0) {
        const token = ++generation;
        timer = schedule(() => { if (token === generation) dismiss(); }, current.duration);
      }
    }
    function dismiss() {
      stopTimer(); if (current) keys.delete(current.key); current = null; next();
    }
    function clear() { stopTimer(); queue.length = 0; keys.clear(); current = null; render(null, processing); }
    function show(value) {
      const message = typeof value?.message === 'string' ? value.message.trim() : '';
      if (!message) return false;
      const tone = ['error', 'success', 'warning', 'info'].includes(value.tone) ? value.tone : 'info';
      const action = typeof value.action === 'function' && value.actionLabel ? value.action : null;
      const key = value.key || [tone, message, action ? value.actionLabel : ''].join('|');
      if (keys.has(key) || ((current || processing) && queue.length >= limit)) return false;
      const duration = Number.isFinite(value.duration) ? Math.max(0, value.duration) : action ? 0 : 6000;
      keys.add(key); queue.push({ message, tone, key, action, actionLabel: action ? value.actionLabel : '', duration });
      next(); return true;
    }
    async function activate() {
      if (processing || !current?.action) return;
      const item = current; processing = true; stopTimer(); keys.delete(item.key); current = null; render(null, true);
      try { return await item.action(); }
      finally { processing = false; next(); }
    }
    return { show, dismiss, clear, activate, refresh: () => render(current, processing) };
  }
  return { createSnackbar };
});
