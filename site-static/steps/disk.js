'use strict';
// "Step through it" renderer: disk scheduling (head path and moves).
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/ (checked against the answer at build time).
window.gateStepsRegister(({el, h}) => {
  function head(s, data, step, k, width) {
    const W = Math.max(300, Math.min(720, Math.round(width || 640))), pad = 16, top = 22, rowH = 20;
    const x = c => pad + (W - 2 * pad) * (c - data.lo) / Math.max(1, data.hi - data.lo);
    const H = top + rowH * (s.moves.length + 1);
    const svg = el('svg', {viewBox: `0 0 ${W} ${H}`, class: 'head-path', role: 'img', 'aria-label': `Head at cylinder ${step.pos}`});
    svg.append(el('line', {x1: x(data.lo), x2: x(data.hi), y1: top - 8, y2: top - 8, class: 'tick'}));
    // Axis labels: the ends and every requested cylinder, skipping any that would collide.
    let last = -Infinity;
    [...new Set([data.lo, data.hi, data.start, ...data.requests])].sort((a, b) => a - b).forEach(c => {
      const done = !data.requests.includes(c) || !step.pending.includes(c);
      svg.append(el('circle', {cx: x(c), cy: top - 8, r: 2.5, class: data.requests.includes(c) ? (done ? 'req done' : 'req') : 'end'}));
      const room = n => 7 * String(n).length + 6;
      if (c === data.hi || (x(c) - last >= room(c) && x(data.hi) - x(c) >= room(data.hi))) { svg.append(el('text', {x: x(c), y: top - 13, 'text-anchor': 'middle', class: 'tick-label'}, c)); last = x(c); } });
    const shown = step.final ? s.moves.length : k;
    const y = r => top + rowH * r + 6;
    for (let r = 0; r < shown; r++) {
      const [a, b, served] = s.moves[r];
      svg.append(el('line', {x1: x(a), y1: y(r), x2: x(b), y2: y(r + 1), class: 'path' + (served ? '' : ' unserved') + (r === shown - 1 && !step.final ? ' latest' : '')}));
    }
    for (let r = 0; r <= shown; r++) {
      const c = r === 0 ? data.start : s.moves[r - 1][1];
      // Label on the side away from the line that reaches this point (or leaves the start), kept inside the chart.
      const other = r === 0 ? (s.moves[0] ? s.moves[0][1] : c) : s.moves[r - 1][0];
      let right = other === c ? x(c) < W / 2 : other < c;
      if (!right && x(c) < 34) right = true; else if (right && x(c) > W - 34) right = false;
      svg.append(el('circle', {cx: x(c), cy: y(r), r: r === shown && !step.final ? 5 : 3.5, class: 'stop' + (r === shown && !step.final ? ' now' : '')}));
      const gap = r === shown && !step.final ? 10 : 8;
      svg.append(el('text', {x: x(c) + (right ? gap : -gap), y: y(r) + 4, 'text-anchor': right ? 'start' : 'end', class: 'stop-label'}, c));
    }
    return svg;
  }

  function moveTable(s, step, k) {
    const shown = step.final ? s.moves.length : k, t = h('table', 'steps-table'), head = t.createTHead().insertRow(), body = t.createTBody();
    ['Move', 'From', 'To', 'Distance', 'Total'].forEach(c => head.append(h('th', null, c)));
    let total = 0;
    s.moves.slice(0, shown).forEach(([a, b], r) => { total += Math.abs(b - a); const row = body.insertRow();
      [r + 1, a, b, Math.abs(b - a), total].forEach(v => { row.insertCell().textContent = v; });
      if (r === shown - 1 && !step.final) row.className = 'is-running'; });
    return t;
  }

  // Hashing: one row per slot; this step's collisions and placement are labelled.
  return {
    'disk-schedule': (s, data, step, i, width) => {
      const w = h('div', 'steps-table-wrap'); w.append(moveTable(s, step, i));
      const out = [h('p', 'steps-time', step.final ? 'Finished' : 'Head at ' + step.pos), head(s, data, step, i, width), w];
      if (!step.final && step.pending.length) out.push(h('p', 'steps-ready', 'Pending: ' + step.pending.join(', ')));
      return out;
    },
  };
});
