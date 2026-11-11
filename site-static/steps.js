'use strict';
// "Step through it" players for scheduling questions. Loaded only when a reader opens one.
// Data comes from the build (scripts/animations.py), which checks every result against the answer.
(() => {
  const SVG = 'http://www.w3.org/2000/svg';
  const el = (tag, attrs = {}, text) => { const n = document.createElementNS(SVG, tag); for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v); if (text != null) n.textContent = text; return n; };
  const h = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; };

  let view = null;
  function gantt(s, names, step) {
    // Drawn at the player's actual width so labels stay readable on phones.
    const W = Math.max(300, Math.min(720, Math.round(view.clientWidth || 640))), left = 4, right = 12, top = 6, barH = 30, axisY = top + barH + 16, x = t => left + (W - left - right) * t / s.end;
    const svg = el('svg', {viewBox: `0 0 ${W} ${axisY + 10}`, class: 'gantt', role: 'img', 'aria-label': `Timeline up to time ${step.t}`});
    svg.append(el('rect', {x: left, y: top, width: W - left - right, height: barH, class: 'gantt-track', rx: 4}));
    const ticks = new Set([0, s.end]);
    for (const [name, a, b] of s.segs) {
      if (a >= step.t && !step.final) continue;
      const end = step.final ? b : Math.min(b, step.t);
      ticks.add(a); ticks.add(end);
      const g = el('g', {class: 'seg p' + (names.indexOf(name) % 6)});
      g.append(el('rect', {x: x(a) + 1, y: top, width: Math.max(0, x(end) - x(a) - 2), height: barH, rx: 3}));
      if (x(end) - x(a) > 22) g.append(el('text', {x: (x(a) + x(end)) / 2, y: top + barH / 2 + 5, 'text-anchor': 'middle'}, name));
      svg.append(g);
    }
    // The process chosen at this step, shown as a dashed outline up to its next decision point.
    if (!step.final && step.run) {
      const seg = s.segs.find(([n, a, b]) => n === step.run && a <= step.t && step.t < b);
      if (seg) { const next = s.steps.find(x => x.t > step.t); const end = next ? Math.min(seg[2], next.t) : seg[2];
        svg.append(el('rect', {x: x(step.t) + 1, y: top + 1, width: Math.max(0, x(end) - x(step.t) - 2), height: barH - 2, rx: 3, class: 'seg-next p' + (names.indexOf(step.run) % 6)}));
        if (x(end) - x(step.t) > 22) svg.append(el('text', {x: (x(step.t) + x(end)) / 2, y: top + barH / 2 + 5, 'text-anchor': 'middle', class: 'seg-next-label'}, step.run)); ticks.add(end); }
    }
    [...ticks].sort((a, b) => a - b).forEach(t => { svg.append(el('line', {x1: x(t), x2: x(t), y1: top + barH, y2: top + barH + 4, class: 'tick'})); svg.append(el('text', {x: x(t), y: axisY + 4, 'text-anchor': 'middle', class: 'tick-label'}, t)); });
    if (!step.final) svg.append(el('line', {x1: x(step.t), x2: x(step.t), y1: top - 4, y2: top + barH + 4, class: 'now'}));
    return svg;
  }

  function table(s, names, step) {
    const t = h('table', 'steps-table'), head = t.createTHead().insertRow(), body = t.createTBody();
    // The finished table shows only the time the question asks about.
    const k = s.metric === 'turnaround' ? 4 : 5;
    const cols = step.final ? ['Process', 'Arrival', 'Burst', 'Done at', k === 4 ? 'Turnaround' : 'Waiting'] : ['Process', 'Arrival', 'Burst', 'Left', 'State'];
    cols.forEach(c => head.append(h('th', null, c)));
    s.rows.forEach((r, i) => {
      const row = body.insertRow();
      const cells = step.final ? [r[0], r[1], r[2], r[3], r[k]] : [r[0], r[1], r[2], step.rem[i],
        step.run === r[0] ? 'running' : step.rem[i] === 0 ? 'done' : r[1] > step.t ? 'not arrived' : 'waiting'];
      cells.forEach((v, j) => { const td = row.insertCell(); td.textContent = v; if (j === 0) td.className = 'p' + (i % 6); });
      if (!step.final && step.run === r[0]) row.className = 'is-running';
      if (step.final) row.cells[4].className = 'is-metric';
    });
    return t;
  }

  function player(root) {
    const data = JSON.parse(root.dataset.steps), names = data.processes;
    let which = 0, i = 0;
    const tabs = h('div', 'steps-tabs');
    view = h('div', 'steps-view');
    const note = h('p', 'steps-note'), bar = h('div', 'steps-bar');
    const prev = h('button', null, 'Previous'), next = h('button', null, 'Next'), count = h('span', 'steps-count');
    prev.type = next.type = 'button'; note.setAttribute('aria-live', 'polite');
    bar.append(prev, count, next);
    if (data.schedules.length > 1) data.schedules.forEach((s, k) => { const b = h('button', null, s.title); b.type = 'button'; b.onclick = () => { which = k; i = 0; draw(); }; tabs.append(b); });
    function draw() {
      const s = data.schedules[which], step = s.steps[i];
      [...tabs.children].forEach((b, k) => b.setAttribute('aria-pressed', String(k === which)));
      const wrap = h('div', 'steps-table-wrap'); wrap.append(table(s, names, step));
      view.replaceChildren(h('p', 'steps-time', step.final ? 'Finished' : 'Time ' + step.t));
      view.append(gantt(s, names, step), wrap);
      if (!step.final && step.ready.length) view.append(h('p', 'steps-ready', 'Ready queue: ' + step.ready.join(', ')));
      note.textContent = step.note;
      count.textContent = `Step ${i + 1} of ${s.steps.length}`;
      prev.disabled = i === 0; next.disabled = i === s.steps.length - 1;
    }
    prev.onclick = () => { if (i > 0) { i--; draw(); } };
    next.onclick = () => { const s = data.schedules[which]; if (i < s.steps.length - 1) { i++; draw(); } };
    root.tabIndex = 0;
    root.addEventListener('keydown', e => { if (e.key === 'ArrowRight') { next.click(); e.preventDefault(); } if (e.key === 'ArrowLeft') { prev.click(); e.preventDefault(); } });
    if (data.schedules.length === 1) tabs.append(h('p', 'steps-policy', data.schedules[0].title));
    root.replaceChildren(tabs, view, note, bar);
    draw();
  }

  window.gateSteps = root => { if (!root.dataset.ready) { root.dataset.ready = '1'; player(root); } };
  document.querySelectorAll('details.steps[open] .steps-player').forEach(window.gateSteps);
})();
