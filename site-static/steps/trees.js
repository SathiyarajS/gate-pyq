'use strict';
// "Step through it" renderer: heaps and binary search trees.
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/ (checked against the answer at build time).
window.gateStepsRegister(({el, h}) => {
  function treeSvg(points, W, H, label) {
    const svg = el('svg', {viewBox: `0 0 ${W} ${H}`, class: 'tree', role: 'img', 'aria-label': label});
    const at = new Map(points.map(p => [p.id, p]));
    points.forEach(p => { const q = at.get(p.parent); if (q) svg.append(el('line', {x1: q.x, y1: q.y, x2: p.x, y2: p.y, class: 'edge' + (p.onPath && q.onPath ? ' on' : '')})); });
    points.forEach(p => { const g = el('g', {class: 'node' + (p.cls ? ' ' + p.cls : '')});
      g.append(el('circle', {cx: p.x, cy: p.y, r: 14})); g.append(el('text', {x: p.x, y: p.y + 4, 'text-anchor': 'middle'}, p.text)); svg.append(g); });
    return svg;
  }

  function heapView(s, data, step, width) {
    const d = data.arity, W = Math.max(300, Math.min(560, Math.round(width || 560))), pad = 16, rowH = 50, top = 20;
    const max = Math.max(...s.steps.map(x => x.arr.length), 1);
    const level = i => { let L = 0, start = 0, width = 1; while (i >= start + width) { start += width; width *= d; L++; } return [L, i - start, width]; };
    const levels = level(max - 1)[0] + 1;
    const pts = step.arr.map((v, i) => { const [L, pos, width] = level(i);
      return {id: i, parent: i ? Math.floor((i - 1) / d) : null, x: pad + (pos + 0.5) * (W - 2 * pad) / width, y: top + L * rowH, text: v,
        cls: step.hi.includes(i) ? 'hi' : '', onPath: step.hi.includes(i)}; });
    const t = h('table', 'steps-table steps-grid heap-array'), r1 = t.insertRow(), r2 = t.insertRow();
    r1.append(h('th', null, 'Index')); r2.append(h('th', null, 'Key'));
    step.arr.forEach((v, i) => { r1.append(h('th', null, i)); const c = r2.insertCell(); c.textContent = v; if (step.hi.includes(i)) c.className = 'is-now'; });
    const wrap = h('div', 'steps-table-wrap'); wrap.append(t);
    return [treeSvg(pts, W, top + (levels - 1) * rowH + 20, 'Heap'), wrap];
  }

  function bstView(s, data, step, width) {
    const n = data.nodes.length, W = Math.max(300, Math.min(640, Math.round(width || 640))), pad = 16, rowH = 46, top = 20;
    const depth = Math.max(...data.nodes.map(x => x[2]));
    const shown = new Set(step.shown), path = new Set(step.path);
    const pts = data.nodes.filter(([k]) => shown.has(k)).map(([k, rank, dep, parent]) => ({id: k, parent, x: pad + (rank + 0.5) * (W - 2 * pad) / n, y: top + dep * rowH, text: k,
      cls: k === step.key && !step.final ? 'now' : path.has(k) ? 'hi' : '', onPath: path.has(k)}));
    const out = [treeSvg(pts, W, top + depth * rowH + 20, 'Binary search tree')];
    if (step.out && step.out.length) out.push(h('p', 'steps-ready', 'Visited so far: ' + step.out.join(', ')));
    return out;
  }

  // Address fields: the address as a bar split into fields, and the derivation so far.
  const finished = step => step.final ? [h('p', 'steps-time', 'Finished')] : [];
  return {
    heap: (s, data, step, i, width) => [...finished(step), ...heapView(s, data, step, width)],
    bst: (s, data, step, i, width) => [...finished(step), ...bstView(s, data, step, width)],
  };
});
