'use strict';
// Offline page: save or remove subject and paper packs. Works with sw.js, which serves whatever is in these caches.
(() => {
  const root = document.querySelector('#offline'); if (!root) return;
  const base = new URL(document.body.dataset.base, location.href);
  const packs = JSON.parse(document.querySelector('#offline-packs').textContent);
  const status = document.querySelector('#offline-status'), storage = document.querySelector('#offline-storage');
  const PACKS = 'gate-packs', savedKey = id => new URL('offline/saved/' + id, base).href;
  const mb = bytes => bytes >= 1048576 ? (bytes / 1048576).toFixed(bytes < 10485760 ? 1 : 0) + ' MB' : Math.max(1, Math.round(bytes / 1024)) + ' KB';
  if (!('caches' in window) || !('serviceWorker' in navigator) || !document.body.dataset.sw) {
    status.textContent = document.body.dataset.sw ? 'This browser cannot save pages for offline use. Private or incognito windows often block it.' : 'Offline saving is only available on the published site.';
    root.querySelectorAll('button').forEach(b => b.disabled = true); return;
  }
  let busy = false;
  const rows = new Map([...root.querySelectorAll('[data-pack]')].map(row => [row.dataset.pack, row]));

  async function savedManifests(cache) {
    const all = {};
    for (const pack of packs) { const hit = await cache.match(savedKey(pack.id)); if (hit) all[pack.id] = await hit.json(); }
    return all;
  }
  async function showStorage() {
    if (!navigator.storage?.estimate) return;
    const {usage = 0, quota = 0} = await navigator.storage.estimate();
    storage.textContent = 'Using ' + mb(usage) + ' on this device' + (quota ? ' · about ' + mb(quota - usage) + ' free for this site' : '') + '.';
  }
  async function render() {
    const saved = await savedManifests(await caches.open(PACKS)); let count = 0;
    for (const pack of packs) {
      const row = rows.get(pack.id), state = saved[pack.id], main = row.querySelector('.pack-save'), remove = row.querySelector('.pack-remove'), note = row.querySelector('.pack-state');
      row.querySelector('progress').hidden = true; remove.hidden = !state;
      if (!state) { main.hidden = false; main.textContent = 'Save offline'; note.textContent = ''; }
      else if (state.partial) { main.hidden = false; main.textContent = 'Resume'; note.textContent = 'Partly saved'; }
      else if (state.version !== pack.version) { main.hidden = false; main.textContent = 'Update'; note.textContent = 'Saved · newer version available'; count++; }
      else { main.hidden = true; note.textContent = '✓ Saved'; count++; }
    }
    document.querySelector('#offline-all').hidden = packs.filter(p => p.group === 'subject').every(p => saved[p.id] && !saved[p.id].partial && saved[p.id].version === p.version);
    await showStorage(); return count;
  }
  // Every URL another saved pack still needs, with the content hash that pack saved.
  function othersNeed(saved, id) {
    const need = {};
    for (const [other, manifest] of Object.entries(saved)) if (other !== id) Object.assign(need, manifest.files);
    return need;
  }
  async function save(pack) {
    const row = rows.get(pack.id), bar = row.querySelector('progress'), note = row.querySelector('.pack-state');
    const cache = await caches.open(PACKS);
    const response = await fetch(new URL('offline/' + pack.id + '.json', base), {cache: 'no-store'});
    if (!response.ok) throw Error('offline');
    const manifest = await response.json(), saved = await savedManifests(cache);
    const have = Object.assign(othersNeed(saved, pack.id), saved[pack.id]?.files), done = {};
    const todo = [];
    for (const [path, hash] of Object.entries(manifest.files)) {
      if (have[path] === hash && await cache.match(new URL(path, base))) done[path] = hash; else todo.push([path, hash]);
    }
    const total = Object.keys(manifest.files).length; let finished = total - todo.length, failed = null;
    bar.hidden = false; bar.max = total; bar.value = finished; row.querySelector('.pack-save').hidden = true;
    const next = async () => {
      while (todo.length && !failed) {
        const [path, hash] = todo.shift();
        try {
          const url = new URL(path, base), file = await fetch(url, {cache: 'no-cache'});
          if (!file.ok) throw Error('HTTP ' + file.status);
          await cache.put(url, file); done[path] = hash; bar.value = ++finished; note.textContent = 'Saving ' + finished + ' of ' + total;
        } catch (error) { failed = error; }
      }
    };
    await Promise.all(Array.from({length: 6}, next));
    const record = failed ? {version: manifest.version, partial: true, files: done} : {version: manifest.version, files: manifest.files};
    await cache.put(savedKey(pack.id), new Response(JSON.stringify(record), {headers: {'Content-Type': 'application/json'}}));
    if (failed) throw failed;
    // Files an older version of this pack had that nothing needs any more.
    const keep = Object.assign(othersNeed(saved, pack.id), manifest.files);
    for (const path of Object.keys(saved[pack.id]?.files || {})) if (!(path in keep)) await cache.delete(new URL(path, base));
  }
  async function remove(pack) {
    const cache = await caches.open(PACKS), saved = await savedManifests(cache), keep = othersNeed(saved, pack.id);
    for (const path of Object.keys(saved[pack.id]?.files || {})) if (!(path in keep)) await cache.delete(new URL(path, base));
    await cache.delete(savedKey(pack.id));
  }
  async function run(list, action) {
    if (busy) return; busy = true; root.classList.add('busy'); status.textContent = '';
    try {
      if (action === save) { await navigator.serviceWorker.ready; navigator.storage?.persist?.(); }
      for (const pack of list) await action(pack);
      status.textContent = action === save ? 'Saved. These pages and their question images now open without a connection.' : 'Removed from this device.';
    } catch (error) {
      status.textContent = error?.name === 'QuotaExceededError' ? 'This device is out of space for the site. Remove a saved subject or free up storage, then try again.'
        : 'Saving stopped — check your connection. What was downloaded is kept; press Resume to continue.';
    }
    busy = false; root.classList.remove('busy'); await render();
  }
  root.addEventListener('click', event => {
    const button = event.target.closest('button'); if (!button) return;
    const pack = packs.find(p => p.id === button.closest('[data-pack]')?.dataset.pack);
    if (button.id === 'offline-all') run(packs.filter(p => p.group === 'subject'), save);
    else if (pack && button.classList.contains('pack-save')) run([pack], save);
    else if (pack && button.classList.contains('pack-remove')) run([pack], remove);
  });
  render();
})();
