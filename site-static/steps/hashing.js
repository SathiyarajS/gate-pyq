'use strict';
// "Step through it" renderer: hashing (one row per slot).
// Loaded on demand by assets/steps.js; the data comes from scripts/animations/ (checked against the answer at build time).
window.gateStepsRegister(({h}) => {
  function slots(s, data, step) {
    const t = h('table', 'steps-table hash-table'), head = t.createTHead().insertRow(), body = t.createTBody();
    ['Slot', data.chaining ? 'Chain' : 'Key', ''].forEach(c => head.append(h('th', null, c)));
    step.table.forEach((v, i) => {
      const row = body.insertRow(), placed = step.slot === i, hit = step.probed.includes(i);
      [i, Array.isArray(v) ? v.join(' → ') : v == null ? '' : v, placed ? (data.chaining ? 'added' : 'placed') : hit ? 'collision' : ''].forEach(x => { row.insertCell().textContent = x; });
      if (placed) row.className = 'is-running'; else if (hit) row.className = 'is-probed';
    });
    return t;
  }

  // Trees: circles with keys, edges to parents, highlighted nodes for this step.
  return {
    'hash-insert': (s, data, step, i) => {
      const w = h('div', 'steps-table-wrap'); w.append(slots(s, data, step));
      const out = [h('p', 'steps-time', step.final ? 'Finished' : step.key == null ? 'Start' : 'Insert ' + step.key), w];
      const left = data.keys.slice(step.final ? data.keys.length : i);
      if (left.length) out.push(h('p', 'steps-ready', 'Still to insert: ' + left.join(', ')));
      return out;
    },
  };
});
