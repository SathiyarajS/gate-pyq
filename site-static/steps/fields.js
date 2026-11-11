'use strict';
// "Step through it" renderer: address fields (bit bar and derivation table).
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/ (checked against the answer at build time).
window.gateStepsRegister(({el, h}) => {
  function fieldsView(s, data, step, width) {
    const W = Math.max(300, Math.min(640, Math.round(width || 640))), pad = 2, barH = 34, top = 4;
    const colour = {Tag: 0, Index: 1, 'Index + offset': 1, Offset: 2, 'Page number': 0};
    const known = step.fields.reduce((a, f) => a + f[1], 0), total = data.bits || known || 1;
    const svg = el('svg', {viewBox: `0 0 ${W} ${barH + top + 22}`, class: 'gantt fields-bar', role: 'img', 'aria-label': 'Address fields'});
    svg.append(el('rect', {x: pad, y: top, width: W - 2 * pad, height: barH, rx: 4, class: 'gantt-track'}));
    let x = W - pad;
    for (let k = step.fields.length - 1; k >= 0; k--) {
      const [name, bits] = step.fields[k], w = (W - 2 * pad) * bits / total;
      x -= w; if (!bits) continue;
      const g = el('g', {class: 'seg p' + (colour[name] ?? 3)});
      g.append(el('rect', {x: x + 1, y: top, width: Math.max(0, w - 2), height: barH, rx: 3}));
      const label = w > 9 * (name.length + String(bits).length + 1) ? `${name} ${bits}` : w > 22 ? String(bits) : '';
      if (label) g.append(el('text', {x: x + w / 2, y: top + barH / 2 + 5, 'text-anchor': 'middle'}, label));
      svg.append(g);
    }
    if (data.bits) svg.append(el('text', {x: pad, y: top + barH + 16, class: 'tick-label'}, `${data.bits}-bit address` + (known < data.bits ? ` · ${data.bits - known} bits still to assign` : '')));
    const t = h('table', 'steps-table'), head = t.createTHead().insertRow(), body = t.createTBody();
    ['Quantity', 'Value', 'How'].forEach(c => head.append(h('th', null, c)));
    step.rows.forEach((r, k) => { const row = body.insertRow(); r.forEach(v => { row.insertCell().textContent = v; }); if (k === step.rows.length - 1 && !step.final) row.className = 'is-running'; });
    const wrap = h('div', 'steps-table-wrap'); wrap.append(t);
    const names = step.fields.map(f => f[0]), legend = h('p', 'steps-ready', step.fields.length ? 'Fields, left to right: ' + step.fields.map(f => `${f[0]} (${f[1]})`).join(', ') : '');
    return data.bits || step.fields.length ? [svg, legend, wrap] : [wrap];
  }

  return {
    'address-fields': (s, data, step, i, width) => fieldsView(s, data, step, width),
  };
});
