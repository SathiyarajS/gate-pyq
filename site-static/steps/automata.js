'use strict';
// Finite-state machines: states, active transitions, and computed trace tables.
window.gateStepsRegister(({h, css}) => {
  css(`
    .fa-view {min-width:0;overflow-wrap:anywhere}
    .fa-view .fa-states {display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 8px}
    .fa-view .fa-state {border:1px solid var(--line);border-radius:4px;padding:2px 8px;background:var(--panel);font-size:.85rem;font-variant-numeric:tabular-nums}
    .fa-view .fa-accept {border:3px double currentColor}
    .fa-view .fa-now {border-color:var(--accent);background:color-mix(in oklab,var(--accent) 24%,var(--panel));color:var(--ink);font-weight:700}
    .fa-view .fa-off {opacity:.5}
    .fa-view .steps-table th,.fa-view .steps-table td {white-space:normal;overflow-wrap:anywhere}
    .fa-view .steps-table th:first-child {min-width:0}
    .fa-view .fa-transitions {margin:6px 0;padding-left:20px}
    .fa-view .fa-tape {font-family:monospace;white-space:normal;overflow-wrap:anywhere}
    .fa-view .fa-tape span {display:inline-block;padding:3px}
    .fa-view .fa-g0 {border-color:var(--s0)} .fa-view .fa-g1 {border-color:var(--s1)}
    .fa-view .fa-g2 {border-color:var(--s2)} .fa-view .fa-g3 {border-color:var(--s3)}
    .fa-view .fa-g4 {border-color:var(--s4)} .fa-view .fa-g5 {border-color:var(--s5)}
  `);
  function table(t) {
    const wrap=h('div','steps-table-wrap'), node=h('table','steps-table');
    const head=h('thead'), row=h('tr');
    t.head.forEach(v=>row.append(h('th',null,v)));head.append(row);node.append(head);
    const body=h('tbody');
    t.rows.forEach((values,i)=>{const r=h('tr',(t.now||[]).includes(i)?'is-running':null);
      values.forEach(v=>r.append(h('td',null,v)));body.append(r);});
    node.append(body);wrap.append(node);return wrap;
  }
  function render(s,data,step) {
    const root=h('div','fa-view'), fa=s.fa;
    root.append(h('p','steps-time',step.final?'Finished':step.head));
    if(fa){
      const states=h('div','fa-states');
      fa.states.forEach(name=>{const cls=(step.n||{})[name];
        const text=(name===fa.start?'Start → ':'')+name+(fa.final.includes(name)?' (accept)':'')+((step.tag||{})[name]!==undefined?' · '+step.tag[name]:'');
        states.append(h('span','fa-state'+(fa.final.includes(name)?' fa-accept':'')+(cls?' fa-'+cls:''),text));});
      root.append(states);
      const active=Object.entries(step.e||{});
      if(active.length){const list=h('ul','fa-transitions');
        active.forEach(([i])=>{const [u,v,label]=fa.edges[Number(i)];list.append(h('li',null,`${u} → ${v} on ${label}`));});root.append(list);}
    }
    if(step.tape){
      const tape=h('p','fa-tape');tape.append(h('span',null,'Input:'));
      step.tape.sym.forEach((c,i)=>tape.append(h('span',i===step.tape.pos?'fa-now':null,c)));
      if(!step.tape.sym.length)tape.append(h('span',null,'ε'));root.append(tape);
      if(step.tape.out)root.append(h('p','fa-tape','Output: '+step.tape.out.join(' ')));
    }
    if(step.table)root.append(table(step.table));
    if(step.table2)root.append(table(step.table2));
    (step.line||[]).forEach(line=>root.append(h('p','steps-ready',line)));
    return [root];
  }
  return Object.fromEntries(['fa-run','fa-count','fa-subset','fa-refine','fa-language','fa-claims','fa-mealy'].map(k=>[k,render]));
});
