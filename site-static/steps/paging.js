'use strict';
// "Step through it" renderer: page replacement (frame grid).
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/ (checked against the answer at build time).
window.gateStepsRegister(({h}) => {
  function frames(s, data, step) {
    const now = step.final ? data.refs.length - 1 : step.i, t = h('table', 'steps-table steps-grid');
    const head = t.createTHead().insertRow(), body = t.createTBody();
    head.append(h('th', null, 'Reference'));
    data.refs.forEach((r, j) => { const c = h('th', j === now && !step.final ? 'is-now' : null, r); head.append(c); });
    for (let k = 0; k < data.frames; k++) {
      const row = body.insertRow(); row.insertCell().textContent = 'Frame ' + (k + 1);
      data.refs.forEach((_, j) => { const td = row.insertCell(), at = s.steps[j + 1];
        if (j <= now) { const v = at.frames[k]; td.textContent = v == null ? '' : v; if (at.fault && at.slot === k) td.className = 'is-new'; }
        if (j === now && !step.final) td.classList.add('is-now'); });
    }
    const f = body.insertRow(); f.className = 'fault-row'; f.insertCell().textContent = 'Fault';
    data.refs.forEach((_, j) => { const td = f.insertCell(); if (j <= now) td.textContent = s.steps[j + 1].fault ? 'F' : ''; if (j === now && !step.final) td.classList.add('is-now'); });
    return t;
  }

  // Disk scheduling: cylinders across, one row per head movement, drawn up to the current step.
  return {
    'page-replace': (s, data, step) => {
      const w = h('div', 'steps-table-wrap'); w.append(frames(s, data, step));
      const out = [h('p', 'steps-time', step.final ? 'Finished' : step.i < 0 ? 'Start' : `Reference ${step.i + 1} of ${data.refs.length}: page ${data.refs[step.i]}`), w];
      if (step.order) out.push(h('p', 'steps-ready', step.order));
      return out;
    },
  };
});
