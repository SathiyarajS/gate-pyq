'use strict';
// "Step through it" renderer: fork() process trees.
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/fork.py (checked against the answer at build time).
window.gateStepsRegister(({el, h, css}) => {
  css(`
.fork-tally{display:flex;flex-wrap:wrap;gap:6px 14px;margin:4px 0 6px;font-size:.85rem}
.fork-tally span{color:var(--muted)}.fork-tally b{color:var(--ink);font-variant-numeric:tabular-nums;margin-left:.3em}
.fork-main{display:flex;gap:14px;align-items:flex-start}.fork-main.stacked{flex-direction:column;gap:4px}
.fork-code{margin:2px 0 4px;padding:6px 0;font-size:.78rem;line-height:1.45;background:var(--panel);border-radius:6px;overflow-x:auto;flex:0 0 auto;max-width:100%}
.fork-code span{display:block;padding:0 10px;white-space:pre}.fork-code span.is-now{background:color-mix(in oklab,var(--accent) 18%,transparent);box-shadow:inset 3px 0 0 var(--accent)}
.fork-tree{display:block;height:auto;font-family:inherit;max-width:100%}
.fork-tree .edge{stroke-width:2.5;stroke-linecap:round}.fork-tree .edge.c0{stroke:var(--s0)}.fork-tree .edge.c1{stroke:var(--s1)}.fork-tree .edge.c2{stroke:var(--s2)}.fork-tree .edge.c3{stroke:var(--s3)}.fork-tree .edge.c4{stroke:var(--s4)}.fork-tree .edge.c5{stroke:var(--s5)}
.fork-tree .node circle{fill:var(--panel);stroke:var(--muted);stroke-width:1.5}.fork-tree .node text{font-weight:650;fill:var(--ink);font-variant-numeric:tabular-nums}
.fork-tree .node.new circle{stroke:var(--accent);stroke-width:3}.fork-tree .node.now circle{fill:var(--accent);stroke:var(--accent)}.fork-tree .node.now text{fill:var(--bg)}
.fork-tree .node.wait circle{stroke-dasharray:3 2.5;stroke-width:2}.fork-tree .node.done circle{stroke:var(--line);stroke-dasharray:none}.fork-tree .node.done text{fill:var(--muted);font-weight:500}
.fork-calls{display:flex;flex-wrap:wrap;align-items:center;gap:4px 10px;margin:2px 0;font-size:.8rem;color:var(--muted)}
.fork-calls i{font-style:normal;white-space:nowrap;color:var(--ink)}.fork-calls i::before{content:"";display:inline-block;width:1em;height:3px;border-radius:2px;margin-right:.35em;vertical-align:.2em;background:var(--s0)}
.fork-calls i.c1::before{background:var(--s1)}.fork-calls i.c2::before{background:var(--s2)}.fork-calls i.c3::before{background:var(--s3)}.fork-calls i.c4::before{background:var(--s4)}.fork-calls i.c5::before{background:var(--s5)}
.fork-calls i.is-now{font-weight:750;text-decoration:underline;text-decoration-color:var(--accent);text-underline-offset:3px}
.fork-key{font-size:.75rem;color:var(--muted);margin:2px 0}
`);

  // Fixed positions from the final tree, so nodes never move: leaves in depth-first order, parents centred over their children.
  function layout(nodes) {
    const kids = nodes.map(() => []);
    nodes.forEach(([p], k) => { if (p != null) kids[p].push(k); });
    const pos = [];
    let leaf = 0;
    const walk = k => { if (!kids[k].length) { pos[k] = leaf++; return; } kids[k].forEach(walk); pos[k] = (pos[kids[k][0]] + pos[kids[k][kids[k].length - 1]]) / 2; };
    walk(0);
    return {pos, leaves: leaf, depth: Math.max(...nodes.map(n => n[2]))};
  }

  function tree(s, step, W) {
    const {pos, leaves, depth} = layout(s.nodes), pad = 4;
    // Top-down when every leaf gets room for a full label; otherwise the tree lies on its side and the leaves stack downwards.
    const down = (W - 2 * pad) / leaves >= 34;
    let r, at, Wt, H, fs;
    if (down) {
      const gap = (W - 2 * pad) / leaves, rowH = 48; r = 13; fs = 11;
      at = k => [pad + (pos[k] + 0.5) * gap, pad + r + 2 + s.nodes[k][2] * rowH];
      Wt = W; H = 2 * pad + 2 * r + 4 + depth * rowH;
    } else {
      const rowH = 23, colW = Math.min(80, (W - 2 * pad - 24) / Math.max(1, depth)); r = 10.5; fs = 9.5;
      at = k => [pad + 12 + s.nodes[k][2] * colW, pad + r + 1 + pos[k] * rowH];
      Wt = Math.min(W, 2 * pad + 24 + depth * colW); H = 2 * pad + 2 * r + 2 + (leaves - 1) * rowH;
    }
    const svg = el('svg', {viewBox: `0 0 ${Wt} ${H}`, width: Wt, class: 'fork-tree', role: 'img', 'aria-label': `Process tree with ${step.n} process${step.n > 1 ? 'es' : ''}`});
    for (let k = 1; k < step.n; k++) {
      const [p, call] = s.nodes[k], [x1, y1] = at(p), [x2, y2] = at(k);
      // Edges leave the parent towards the next level and bend into the child, so an edge to a far sibling never passes through a nearer one.
      const d = down ? `M${x1} ${y1}C${x1} ${y1 + 0.55 * (y2 - y1)} ${x2} ${y1 + 0.15 * (y2 - y1)} ${x2} ${y2}` : `M${x1} ${y1}C${(x1 + x2) / 2} ${y1} ${(x1 + x2) / 2} ${y2} ${x2} ${y2}`;
      const e = el('path', {d, fill: 'none', class: 'edge c' + (call % 6)});
      e.append(el('title', {}, `P${k} made by P${p} (${s.calls[call].label})`));
      svg.append(e);
    }
    for (let k = 0; k < step.n; k++) {
      const [x, y] = at(k), st = step.status[k];
      const cls = 'node' + (k === step.actor ? ' now' : '') + (k === step.new ? ' new' : '') + (step.final ? '' : st === 'w' ? ' wait' : st === 'd' && k !== step.actor ? ' done' : '');
      const g = el('g', {class: cls});
      g.append(el('circle', {cx: x, cy: y, r}));
      g.append(el('text', {x, y: y + fs * 0.36, 'text-anchor': 'middle', 'font-size': fs}, 'P' + k));
      svg.append(g);
    }
    return svg;
  }

  function code(data, step) {
    const pre = h('pre', 'fork-code');
    data.code.forEach((line, k) => pre.append(h('span', k === step.line ? 'is-now' : null, line)));
    return pre;
  }

  function view(s, data, step, width) {
    const W = Math.max(280, Math.round(width || 560));
    const out = [h('p', 'steps-time', step.final ? 'Finished' : step.actor == null ? 'Start' : 'P' + step.actor + ' runs')];
    const tally = h('p', 'fork-tally');
    const stat = (label, v) => { const sp = h('span', null, label); sp.append(h('b', null, v)); tally.append(sp); };
    stat('Processes', step.n); stat('Children created', step.children);
    if (data.prints) stat('printf calls', step.prints);
    out.push(tally);
    // The listing sits beside the tree when both fit, and above it on a phone.
    const longest = Math.max(...data.code.map(x => x.length)), codeW = longest * 7.1 + 24, side = W - codeW - 14 >= 300;
    const main = h('div', 'fork-main' + (side ? '' : ' stacked'));
    main.append(code(data, step));
    const right = h('div');
    right.append(tree(s, step, side ? W - codeW - 14 : W));
    const used = new Set(s.nodes.slice(1, step.n).map(n => n[1]));
    if (used.size) {
      const calls = h('p', 'fork-calls', 'Edge colours:');
      s.calls.forEach((c, k) => { if (used.has(k)) calls.append(h('i', 'c' + (k % 6) + (k === step.call ? ' is-now' : ''), c.label)); });
      right.append(calls);
    }
    const key = ['filled: running now'];
    if (step.new != null) key.push('ringed: new child');
    if (step.status.includes('w')) key.push('dashed: waiting');
    if (step.status.includes('d')) key.push('grey: ended');
    if (!step.final && step.actor != null) right.append(h('p', 'fork-key', key.join(' · ')));
    main.append(right);
    out.push(main);
    return out;
  }

  return {'fork-tree': (s, data, step, i, width) => view(s, data, step, width)};
});
