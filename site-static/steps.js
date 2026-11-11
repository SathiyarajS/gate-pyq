'use strict';
// "Step through it" players for CPU-scheduling questions. Loaded only when a reader opens one.
// Data comes from the build (scripts/animations.py), which checks every result against the answer.
(() => {
  const SVG = 'http://www.w3.org/2000/svg';
  const el = (tag, attrs = {}, text) => { const n = document.createElementNS(SVG, tag); for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v); if (text != null) n.textContent = text; return n; };
  const h = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; };

  let view = null;
  function gantt(s, data, step) {
    const names = data.processes, colour = name => data.colors[names.indexOf(name)];
    // Drawn at the player's actual width so labels stay readable on phones.
    const W = Math.max(300, Math.min(720, Math.round(view.clientWidth || 640))), left = 4, right = 12, top = 6, barH = 30, axisY = top + barH + 16, x = t => left + (W - left - right) * t / s.end;
    const svg = el('svg', {viewBox: `0 0 ${W} ${axisY + 10}`, class: 'gantt', role: 'img', 'aria-label': `Timeline up to time ${step.t}`});
    svg.append(el('rect', {x: left, y: top, width: W - left - right, height: barH, class: 'gantt-track', rx: 4}));
    const ticks = new Set([0, s.end]);
    for (const [name, a, b] of s.segs) {
      if (a >= step.t && !step.final) continue;
      const end = step.final ? b : Math.min(b, step.t);
      ticks.add(a); ticks.add(end);
      const g = el('g', {class: 'seg p' + colour(name)});
      g.append(el('rect', {x: x(a) + 1, y: top, width: Math.max(0, x(end) - x(a) - 2), height: barH, rx: 3}));
      if (x(end) - x(a) > 22) g.append(el('text', {x: (x(a) + x(end)) / 2, y: top + barH / 2 + 5, 'text-anchor': 'middle'}, name));
      svg.append(g);
    }
    // The process chosen at this step, shown as a dashed outline up to its next decision point.
    if (!step.final && step.run) {
      const seg = s.segs.find(([n, a, b]) => n === step.run && a <= step.t && step.t < b);
      if (seg) { const next = s.steps.find(x => x.t > step.t); const end = next ? Math.min(seg[2], next.t) : seg[2];
        svg.append(el('rect', {x: x(step.t) + 1, y: top + 1, width: Math.max(0, x(end) - x(step.t) - 2), height: barH - 2, rx: 3, class: 'seg-next p' + colour(step.run)}));
        if (x(end) - x(step.t) > 22) svg.append(el('text', {x: (x(step.t) + x(end)) / 2, y: top + barH / 2 + 5, 'text-anchor': 'middle', class: 'seg-next-label'}, step.run)); ticks.add(end); }
    }
    // Every boundary gets a tick; a label is skipped where it would collide with the previous one.
    let lastLabel = -Infinity;
    [...ticks].sort((a, b) => a - b).forEach(t => { svg.append(el('line', {x1: x(t), x2: x(t), y1: top + barH, y2: top + barH + 4, class: 'tick'}));
      if (x(t) - lastLabel >= 7 * String(t).length + 8 || t === s.end) { svg.append(el('text', {x: x(t), y: axisY + 4, 'text-anchor': 'middle', class: 'tick-label'}, t)); lastLabel = x(t); } });
    if (!step.final) svg.append(el('line', {x1: x(step.t), x2: x(step.t), y1: top - 4, y2: top + barH + 4, class: 'now'}));
    return svg;
  }

  function table(s, data, step) {
    const t = h('table', 'steps-table'), head = t.createTHead().insertRow(), body = t.createTBody();
    const names = data.processes, prio = data.priority;
    // The finished table shows the completion times and only the measure the question asks about.
    const cols = step.final ? s.final.cols : ['Process', 'Arrival', 'Burst'].concat(prio ? ['Priority'] : [], ['Left', 'State']);
    cols.forEach(c => head.append(h('th', null, c)));
    names.forEach((name, i) => {
      const row = body.insertRow();
      const cells = step.final ? s.final.rows[i] : [name, data.arrival[i], data.burst[i]].concat(prio ? [prio[i]] : [], [step.rem[i],
        step.run === name ? 'running' : step.rem[i] === 0 ? 'done' : data.arrival[i] > step.t ? 'not arrived' : 'waiting']);
      cells.forEach((v, j) => { const td = row.insertCell(); td.textContent = v; if (j === 0) td.className = 'p' + data.colors[i]; });
      if (step.final ? s.final.highlight === name : step.run === name) row.className = 'is-running';
      if (step.final && s.final.metric) row.cells[cells.length - 1].className = 'is-metric';
    });
    return t;
  }

  function player(root) {
    const data = JSON.parse(root.dataset.steps);
    let which = 0, i = 0;
    const tabs = h('div', 'steps-tabs');
    view = h('div', 'steps-view');
    const note = h('p', 'steps-note'), bar = h('div', 'steps-bar'), policy = h('p', 'steps-policy');
    const prev = h('button', null, 'Previous'), next = h('button', null, 'Next'), count = h('span', 'steps-count');
    prev.type = next.type = 'button'; note.setAttribute('aria-live', 'polite');
    bar.append(prev, count, next);
    if (data.schedules.length > 1) data.schedules.forEach((s, k) => { const b = h('button', null, s.short); b.type = 'button'; b.onclick = () => { which = k; i = 0; draw(); }; tabs.append(b); });
    function draw() {
      const s = data.schedules[which], step = s.steps[i];
      [...tabs.children].forEach((b, k) => b.setAttribute('aria-pressed', String(k === which)));
      const wrap = h('div', 'steps-table-wrap'); wrap.append(table(s, data, step));
      policy.textContent = s.title;
      view.replaceChildren(h('p', 'steps-time', step.final ? 'Finished' : 'Time ' + step.t));
      view.append(gantt(s, data, step), wrap);
      if (!step.final && step.ready.length) view.append(h('p', 'steps-ready', s.queue_label + ': ' + step.ready.join(', ')));
      note.textContent = step.note;
      count.textContent = `Step ${i + 1} of ${s.steps.length}`;
      prev.disabled = i === 0; next.disabled = i === s.steps.length - 1;
    }
    prev.onclick = () => { if (i > 0) { i--; draw(); } };
    next.onclick = () => { const s = data.schedules[which]; if (i < s.steps.length - 1) { i++; draw(); } };
    root.tabIndex = 0;
    root.addEventListener('keydown', e => { if (e.key === 'ArrowRight') { next.click(); e.preventDefault(); } if (e.key === 'ArrowLeft') { prev.click(); e.preventDefault(); } });
    root.replaceChildren(tabs, policy, view, note, bar);
    draw();
  }

  window.gateSteps = root => { if (!root.dataset.ready) { root.dataset.ready = '1'; player(root); } };
  document.querySelectorAll('details.steps[open] .steps-player').forEach(window.gateSteps);
})();
