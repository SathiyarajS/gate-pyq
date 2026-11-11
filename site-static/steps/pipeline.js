'use strict';
// "Step through it" renderer: instruction pipelines (one row per instruction, one column per cycle).
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/pipeline.py (checked against the answer at build time).
// Each step adds one instruction's row; a cell holds the stage it is working in, or the stage it waits in.
window.gateStepsRegister(({h, css}) => {
  css(`
.pipe-grid th,.pipe-grid td{padding:3px 2px;min-width:1.9em;font-size:.74rem;text-align:center;border-left:1px solid color-mix(in oklab,var(--line) 60%,transparent)}
.pipe-grid th:first-child,.pipe-grid td:first-child{min-width:0;padding:3px 6px 3px 2px;border-left:0}
.pipe-grid td.st{font-weight:650;color:var(--ink)}
.pipe-grid td.s0{background:color-mix(in oklab,var(--s0) 22%,transparent)}.pipe-grid td.s1{background:color-mix(in oklab,var(--s1) 22%,transparent)}
.pipe-grid td.s2{background:color-mix(in oklab,var(--s2) 22%,transparent)}.pipe-grid td.s3{background:color-mix(in oklab,var(--s3) 26%,transparent)}
.pipe-grid td.s4{background:color-mix(in oklab,var(--s4) 22%,transparent)}.pipe-grid td.s5{background:color-mix(in oklab,var(--s5) 22%,transparent)}
.pipe-grid td.wait{font-weight:400;color:var(--muted);background:repeating-linear-gradient(135deg,transparent 0 4px,color-mix(in oklab,var(--muted) 18%,transparent) 4px 6px)}
.pipe-grid tr.is-now td:first-child{color:var(--accent)}
.pipe-grid tr.is-now td{box-shadow:inset 0 2px 0 var(--accent),inset 0 -2px 0 var(--accent)}
.pipe-grid tr.is-now td:first-child{box-shadow:inset 0 2px 0 var(--accent),inset 0 -2px 0 var(--accent),inset -1px 0 0 var(--line)}
.pipe-grid td.last{outline:2px solid var(--accent);outline-offset:-2px}
.pipe-key{display:flex;flex-wrap:wrap;gap:2px 12px;margin:0 0 4px;font-size:.78rem;color:var(--muted)}
.pipe-key i{display:inline-block;width:1.1em;height:.8em;vertical-align:-.05em;margin-right:.35em;border-radius:2px;background:repeating-linear-gradient(135deg,transparent 0 3px,color-mix(in oklab,var(--muted) 35%,transparent) 3px 5px)}
`);

  function grid(data, step) {
    const t = h('table', 'steps-table steps-grid pipe-grid'), head = t.createTHead().insertRow(), body = t.createTBody();
    head.append(h('th', null, 'Cycle'));
    for (let c = 1; c <= data.cycles; c++) head.append(h('th', null, c));
    data.names.forEach((name, i) => {
      const row = body.insertRow(), cells = step.rows[i];
      row.insertCell().textContent = name;
      const at = {};
      (cells || []).forEach(([c, s, kind]) => { at[c] = [s, kind]; });
      for (let c = 1; c <= data.cycles; c++) {
        const td = row.insertCell(), x = at[c];
        if (x) {
          td.textContent = x[0];
          td.className = x[1] === 'work' ? 'st s' + (data.stages.indexOf(x[0]) % 6) : 'wait';
          if (step.final && i === data.names.length - 1 && c === data.cycles) td.classList.add('last');
        }
      }
      if (i === step.row) row.className = 'is-now';
    });
    return t;
  }

  return {
    pipeline: (s, data, step) => {
      const w = h('div', 'steps-table-wrap'); w.append(grid(data, step));
      const out = [h('p', 'steps-time', step.final ? 'Finished' : step.row < 0 ? 'Start' : `${data.names[step.row]}` + (data.texts[step.row] !== data.names[step.row] ? `: ${data.texts[step.row]}` : '')), w];
      if (step.rows.some(r => r.some(c => c[2] === 'stall'))) { const k = h('p', 'pipe-key'), sp = h('span'); sp.append(h('i'), 'waiting in that stage'); k.append(sp); out.push(k); }
      return out;
    },
  };
});
