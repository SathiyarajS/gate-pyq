'use strict';
// "Step through it" player core: tabs, Previous/Next, the note and keyboard control.
// Each family's drawing code lives in assets/steps/<player>.js and is loaded the first
// time a question of that family is opened. The data comes from scripts/animations/,
// which checks every result against the answer at build time.
(() => {
  const SVG = 'http://www.w3.org/2000/svg';
  const el = (tag, attrs = {}, text) => { const n = document.createElementNS(SVG, tag); for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v); if (text != null) n.textContent = text; return n; };
  const h = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; };
  const here = document.currentScript ? document.currentScript.src : new URL('assets/steps.js', document.baseURI).href;
  const renderers = {}, loading = {};

  // A family file calls this with a function that receives the helpers {el, h, css} and returns {kind: render}.
  // render(schedule, data, step, index, width) returns the nodes to show for that step.
  // css(text) adds a family's own styles once; the series colours --s0 to --s5 are set on .steps-player.
  const css = text => { const st = document.createElement('style'); st.textContent = text; document.head.append(st); };
  window.gateStepsRegister = make => Object.assign(renderers, make({el, h, css}));

  const load = name => loading[name] || (loading[name] = new Promise((ok, fail) => {
    const s = document.createElement('script'); s.src = new URL('steps/' + name + '.js', here).href; s.onload = ok; s.onerror = fail; document.head.append(s);
  }));

  function player(root, data) {
    const render = renderers[data.kind];
    let which = 0, i = 0;
    const tabs = h('div', 'steps-tabs'), view = h('div', 'steps-view');
    const note = h('p', 'steps-note'), bar = h('div', 'steps-bar'), policy = h('p', 'steps-policy');
    const prev = h('button', null, 'Previous'), next = h('button', null, 'Next'), count = h('span', 'steps-count');
    prev.type = next.type = 'button'; note.setAttribute('aria-live', 'polite');
    bar.append(prev, count, next);
    if (data.schedules.length > 1) data.schedules.forEach((s, k) => { const b = h('button', null, s.short); b.type = 'button'; b.onclick = () => { which = k; i = 0; draw(); }; tabs.append(b); });
    function draw() {
      const s = data.schedules[which], step = s.steps[i];
      [...tabs.children].forEach((b, k) => b.setAttribute('aria-pressed', String(k === which)));
      policy.textContent = s.title;
      view.replaceChildren(...render(s, data, step, i, view.clientWidth));
      note.textContent = step.note;
      count.textContent = `Step ${i + 1} of ${s.steps.length}`;
      prev.disabled = i === 0; next.disabled = i === s.steps.length - 1;
      // Keep the current column in view when a wide table scrolls sideways.
      view.querySelectorAll('.steps-table-wrap').forEach(w => { const cur = w.querySelector('.is-now');
        if (cur && w.scrollWidth > w.clientWidth) w.scrollLeft = Math.max(0, cur.offsetLeft - w.clientWidth / 2); });
    }
    prev.onclick = () => { if (i > 0) { i--; draw(); } };
    next.onclick = () => { const s = data.schedules[which]; if (i < s.steps.length - 1) { i++; draw(); } };
    root.tabIndex = 0;
    root.addEventListener('keydown', e => { if (e.key === 'ArrowRight') { next.click(); e.preventDefault(); } if (e.key === 'ArrowLeft') { prev.click(); e.preventDefault(); } });
    root.replaceChildren(tabs, policy, view, note, bar);
    draw();
  }

  // Returns a promise, so the caller can report a failed load.
  window.gateSteps = root => {
    if (root.dataset.ready) return Promise.resolve();
    root.dataset.ready = '1';
    const data = JSON.parse(root.dataset.steps);
    return load(data.player).then(() => player(root, data), e => { delete root.dataset.ready; throw e; });
  };
  document.querySelectorAll('details.steps[open] .steps-player').forEach(r => window.gateSteps(r));
})();
