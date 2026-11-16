/* GATE-style mock test: exam screen, calculator, results. Logic lives in mock-core.js. */
(function () {
  'use strict';
  const app = document.getElementById('mock-app');
  if (!app || !window.MockCore) return;
  const C = window.MockCore;
  const BASE = app.dataset.base || '../';
  const DURATION = 180 * 60 * 1000;
  const K = { active: 'gpyq.mock.active.v1', history: 'gpyq.mock.history.v1', seen: 'gpyq.mock.seen.v1', prefs: 'gpyq.mock.prefs.v1' };
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* storage unavailable: the exam still runs */ } },
    del(k) { try { localStorage.removeItem(k); } catch (e) { /* ignore */ } },
  };
  const $ = (sel, el) => (el || document).querySelector(sel);
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const fmtTime = ms => { const s = Math.max(0, Math.round(ms / 1000)); return [Math.floor(s / 3600), Math.floor(s / 60) % 60, s % 60].map(n => String(n).padStart(2, '0')).join(':'); };
  const fmtMarks = v => (Math.round(v * 100) / 100).toString();
  let data = null;

  fetch(BASE + 'mock/pool.json').then(r => { if (!r.ok) throw new Error(r.status); return r.json(); }).then(d => {
    data = d;
    setup();
  }).catch(() => { $('#mock-status', app).textContent = 'The question pool could not be loaded. Check your connection and reload.'; });

  /* ------------------------------------------------------------ setup screen */
  function setup() {
    const prefs = store.get(K.prefs, { borderline: false, officialOnly: false });
    const form = $('#mock-form', app);
    form.borderline.checked = !!prefs.borderline;
    form.officialOnly.checked = !!prefs.officialOnly;
    const url = new URL(location.href), codeParam = url.searchParams.get('code');
    if (codeParam && C.decodeCode(codeParam)) form.code.value = C.decodeCode(codeParam) && codeParam.toUpperCase();
    $('#mock-status', app).textContent = '';
    app.classList.add('ready');
    form.addEventListener('submit', e => {
      e.preventDefault();
      const opts = { borderline: form.borderline.checked, officialOnly: form.officialOnly.checked };
      store.set(K.prefs, opts);
      const typed = form.code.value.trim();
      if (typed) {
        const decoded = C.decodeCode(typed);
        if (!decoded) { $('#mock-status', app).textContent = 'That mock code is not valid. Codes look like 7KQ2-M9FC.'; form.code.focus(); return; }
        return start(decoded.seed, decoded.opts);
      }
      const seen = store.get(K.seen, {});
      const best = C.freshestSeed(data, opts, seen, 12, () => (crypto.getRandomValues(new Uint32Array(1))[0]));
      start(best.seed, opts);
    });
    const active = store.get(K.active, null);
    if (active && !active.submitted) {
      const left = active.endsAt - Date.now();
      if (left <= 0) { finish(active, true); return; }
      const box = $('#mock-resume', app);
      box.hidden = false;
      $('#mock-resume-text', app).textContent = `You have a mock in progress (code ${active.code}, ${fmtTime(left)} left).`;
      $('#mock-resume-go', app).onclick = () => exam(active);
      $('#mock-resume-drop', app).onclick = () => { if (confirmInline(box, 'Discard the mock in progress? Its answers will be lost.')) { store.del(K.active); box.hidden = true; } };
    }
    renderHistory();
  }
  function confirmInline(_box, msg) { return window.confirm(msg); } // only outside the exam screen

  function start(seed, opts) {
    const paper = C.generate(data, seed, opts, {});
    const code = C.encodeCode(seed, opts);
    const now = Date.now();
    const active = {
      v: 1, code, ids: paper.questions.map(q => q.i), meta: paper.questions.map(q => ({ section: q.section })),
      startedAt: now, endsAt: now + DURATION, cur: 0, states: {}, saved: {}, time: {}, submitted: false,
    };
    store.set(K.active, active);
    history.replaceState(null, '', location.pathname + '?code=' + code);
    exam(active);
  }
  function paperFrom(active) {
    const byId = new Map(data.pool.map(q => [q.i, q]));
    return { questions: active.ids.map((id, n) => Object.assign({ section: active.meta[n].section }, byId.get(id))).filter(q => q.i) };
  }

  /* ------------------------------------------------------------ exam screen */
  function exam(active) {
    const paper = paperFrom(active);
    const qs = paper.questions;
    let cur = Math.min(active.cur || 0, qs.length - 1), draft, shownAt = Date.now(), timer;
    const root = document.createElement('div');
    root.className = 'exam';
    root.setAttribute('role', 'application');
    root.setAttribute('aria-label', 'GATE CS mock test');
    root.innerHTML = `
      <div class="exam-top">
        <div class="exam-title"><strong>GATE CS · Mock Test</strong><span>Mock code ${esc(active.code)}</span></div>
        <div class="exam-tools"><button type="button" data-act="calc">Calculator</button><button type="button" data-act="help">Instructions</button></div>
        <div class="exam-timer" aria-live="off">Time Left : <b id="exam-time">--:--:--</b></div>
      </div>
      <div class="exam-sections" role="tablist" aria-label="Sections">
        <button type="button" role="tab" data-sec="GA"><span class="long">General Aptitude</span><span class="short">GA</span></button>
        <button type="button" role="tab" data-sec="CS"><span class="long">Computer Science and Information Technology</span><span class="short">CS &amp; IT</span></button>
        <button type="button" class="palette-toggle" data-act="palette" aria-expanded="false">Question palette</button>
      </div>
      <div class="exam-body">
        <section class="exam-q" aria-live="polite">
          <div class="q-meta"><span id="q-type"></span><span id="q-marks"></span></div>
          <h2 class="q-no" id="q-no"></h2>
          <div class="q-img" id="q-img"></div>
          <div class="q-resp" id="q-resp"></div>
        </section>
        <div class="exam-palette" id="exam-palette" role="region" aria-label="Question palette">
          <div class="candidate"><span class="avatar" aria-hidden="true">👤</span><span>Candidate</span><button type="button" class="palette-close" data-act="palette" aria-label="Close question palette">Close</button></div>
          <ul class="legend" id="legend"></ul>
          <h3 id="pal-title"></h3>
          <div class="pal-grid" id="pal-grid"></div>
          <button type="button" class="submit" data-act="submit">Submit</button>
        </div>
      </div>
      <div class="exam-actions">
        <div><button type="button" data-act="review">Mark for Review &amp; Next</button><button type="button" data-act="clear">Clear Response</button></div>
        <div><button type="button" data-act="back">Back</button><button type="button" class="primary" data-act="save">Save &amp; Next</button></div>
      </div>
      <div class="exam-modal" id="exam-modal" hidden role="dialog" aria-modal="true" aria-labelledby="modal-title"><div class="modal-box" id="modal-box"></div></div>`;
    document.body.appendChild(root);
    document.body.classList.add('exam-open');
    const calc = Calculator(root);

    function persist() { active.cur = cur; store.set(K.active, active); }
    function state(q) { return active.states[q.i] || 'nv'; }
    function addTime() { const q = qs[cur]; const now = Date.now(); active.time[q.i] = (active.time[q.i] || 0) + (now - shownAt); shownAt = now; }
    function hasValue(v) { return !(v === undefined || v === null || v === '' || (Array.isArray(v) && !v.length)); }

    function show(n) {
      addTime();
      cur = Math.max(0, Math.min(qs.length - 1, n));
      const q = qs[cur];
      if (state(q) === 'nv') active.states[q.i] = 'na';
      draft = Array.isArray(active.saved[q.i]) ? active.saved[q.i].slice() : active.saved[q.i];
      $('#q-type', root).textContent = 'Question Type: ' + q.ty;
      $('#q-marks', root).textContent = `Marks for correct answer: ${q.m} | Negative Marks: ${q.ty === 'MCQ' ? (q.m === 1 ? '1/3' : '2/3') : '0'}`;
      $('#q-no', root).textContent = 'Question No. ' + (cur + 1);
      $('#q-img', root).innerHTML = q.img.map(([f, w, h]) => `<img src="${BASE}assets/questions/${esc(f)}" width="${w}" height="${h}" alt="Question ${cur + 1}">`).join('');
      renderResponse(q);
      root.querySelectorAll('.exam-sections [data-sec]').forEach(b => { const on = b.dataset.sec === q.section; b.classList.toggle('on', on); b.setAttribute('aria-selected', on); });
      renderPalette();
      persist();
      $('.exam-q', root).scrollTop = 0;
    }
    function renderResponse(q) {
      const box = $('#q-resp', root);
      if (q.ty === 'NAT') {
        box.innerHTML = `<label class="nat"><span>Your answer</span><input id="nat" type="text" readonly inputmode="none" autocomplete="off" aria-describedby="nat-help"></label>
          <p id="nat-help" class="nat-help">Use the on-screen keypad. Physical keyboard input is disabled, as in the exam.</p>
          <div class="keypad" role="group" aria-label="Number keypad">${['Backspace', '7', '8', '9', '4', '5', '6', '1', '2', '3', '0', '.', '-', 'Clear All'].map(k => `<button type="button" data-key="${k}" class="${k.length > 1 ? 'wide' : ''}">${k}</button>`).join('')}</div>`;
        const input = $('#nat', box);
        input.value = draft || '';
        box.querySelectorAll('[data-key]').forEach(b => b.addEventListener('click', () => {
          let v = input.value; const k = b.dataset.key;
          if (k === 'Backspace') v = v.slice(0, -1);
          else if (k === 'Clear All') v = '';
          else if (k === '-') v = v.startsWith('-') ? v.slice(1) : '-' + v;
          else if (k === '.') { if (!v.includes('.')) v += v === '' || v === '-' ? '0.' : '.'; }
          else if (v.replace(/[-.]/g, '').length < 12) v += k;
          input.value = v; draft = v;
        }));
        return;
      }
      const multi = q.ty === 'MSQ';
      const letters = Array.from({ length: Math.max(4, q.n || 4) }, (_, i) => String.fromCharCode(65 + i));
      const sel = multi ? new Set(draft || []) : draft;
      box.innerHTML = `<fieldset class="choices-exam"><legend>${multi ? 'Select one or more options' : 'Select one option'}</legend>${letters.map(L =>
        `<label><input type="${multi ? 'checkbox' : 'radio'}" name="opt" value="${L}" ${multi ? (sel.has(L) ? 'checked' : '') : (sel === L ? 'checked' : '')}> (${L})</label>`).join('')}</fieldset>
        <p class="nat-help">Options (A)–(${letters[letters.length - 1]}) are as printed in the question above.</p>`;
      box.querySelectorAll('input').forEach(inp => inp.addEventListener('change', () => {
        draft = multi ? [...box.querySelectorAll('input:checked')].map(x => x.value) : (box.querySelector('input:checked') || {}).value;
      }));
    }
    const LEGEND = [['a', 'Answered'], ['na', 'Not Answered'], ['nv', 'Not Visited'], ['mr', 'Marked for Review'], ['amr', 'Answered & Marked for Review (will be considered for evaluation)']];
    function renderPalette() {
      const q = qs[cur], sec = q.section;
      const counts = {};
      qs.filter(x => x.section === sec).forEach(x => { counts[state(x)] = (counts[state(x)] || 0) + 1; });
      $('#legend', root).innerHTML = LEGEND.map(([s, label]) => `<li><span class="st st-${s}">${counts[s] || 0}</span>${label}</li>`).join('');
      $('#pal-title', root).textContent = sec === 'GA' ? 'General Aptitude' : 'Computer Science and Information Technology';
      $('#pal-grid', root).innerHTML = qs.map((x, n) => x.section === sec ? `<button type="button" class="st st-${state(x)}${n === cur ? ' cur' : ''}" data-go="${n}" aria-label="Question ${n + 1}, ${LEGEND.find(l => l[0] === state(x))[1]}">${n + 1}</button>` : '').join('');
    }
    function saveDraft(markReview) {
      const q = qs[cur];
      if (hasValue(draft)) { active.saved[q.i] = draft; active.states[q.i] = markReview ? 'amr' : 'a'; }
      else { delete active.saved[q.i]; active.states[q.i] = markReview ? 'mr' : 'na'; }
    }
    function next() { if (cur < qs.length - 1) show(cur + 1); else { renderPalette(); persist(); } }

    root.addEventListener('click', e => {
      const b = e.target.closest('button');
      if (!b || !root.contains(b)) return;
      const go = b.dataset.go, sec = b.dataset.sec, act = b.dataset.act;
      if (go !== undefined) { show(+go); closePalette(); return; }   // moving away discards an unsaved selection, as in the exam
      if (sec) { const first = qs.findIndex(x => x.section === sec); if (first >= 0) show(first); return; }
      if (act === 'save') { saveDraft(false); next(); }
      else if (act === 'review') { saveDraft(true); next(); }
      else if (act === 'clear') { draft = undefined; const q = qs[cur]; delete active.saved[q.i]; active.states[q.i] = 'na'; renderResponse(q); renderPalette(); persist(); }
      else if (act === 'back') { if (cur > 0) show(cur - 1); }
      else if (act === 'submit') confirmSubmit();
      else if (act === 'calc') calc.toggle();
      else if (act === 'help') helpModal();
      else if (act === 'palette') { const p = $('#exam-palette', root); const open = !p.classList.contains('open'); p.classList.toggle('open', open); $('.palette-toggle', root).setAttribute('aria-expanded', open); }
    });
    function closePalette() { $('#exam-palette', root).classList.remove('open'); }

    function modal(html, onBind) {
      const m = $('#exam-modal', root), box = $('#modal-box', root);
      box.innerHTML = html; m.hidden = false;
      const close = () => { m.hidden = true; box.innerHTML = ''; };
      box.querySelectorAll('[data-close]').forEach(b => b.addEventListener('click', close));
      onBind && onBind(box, close);
      (box.querySelector('[data-focus]') || box.querySelector('button')).focus();
    }
    function helpModal() {
      modal(`<h2 id="modal-title">Instructions</h2>
        <ul><li>65 questions, 100 marks, 3 hours. General Aptitude: 10 questions (15 marks). Computer Science: 55 questions (85 marks).</li>
        <li>MCQ: one correct option. A wrong answer loses 1/3 mark (1-mark questions) or 2/3 mark (2-mark questions).</li>
        <li>MSQ: one or more correct options. Marks only if exactly the correct options are chosen. No negative marks.</li>
        <li>NAT: type a number with the on-screen keypad. No negative marks.</li>
        <li>An answer counts only after <b>Save &amp; Next</b> or <b>Mark for Review &amp; Next</b>. Moving to another question without saving discards the selection.</li>
        <li>Answered questions that are also marked for review are evaluated.</li>
        <li>The test submits itself when the timer reaches zero.</li></ul>
        <div class="modal-actions"><button type="button" class="primary" data-close data-focus>Back to the test</button></div>`);
    }
    function confirmSubmit() {
      addTime(); persist();
      const rows = ['GA', 'CS'].map(sec => {
        const list = qs.filter(q => q.section === sec), c = s => list.filter(q => state(q) === s).length;
        return `<tr><th>${sec === 'GA' ? 'General Aptitude' : 'Computer Science'}</th><td>${list.length}</td><td>${c('a') + c('amr')}</td><td>${c('na')}</td><td>${c('mr') + c('amr')}</td><td>${c('nv')}</td></tr>`;
      }).join('');
      modal(`<h2 id="modal-title">Submit the test?</h2>
        <table class="submit-table"><thead><tr><th>Section</th><th>Questions</th><th>Answered</th><th>Not answered</th><th>Marked for review</th><th>Not visited</th></tr></thead><tbody>${rows}</tbody></table>
        <p>Time left: ${fmtTime(active.endsAt - Date.now())}. After submitting you cannot change any answer.</p>
        <div class="modal-actions"><button type="button" data-close data-focus>No, go back</button><button type="button" class="primary" id="do-submit">Yes, submit</button></div>`,
        (box, close) => { $('#do-submit', box).addEventListener('click', () => { close(); end(false); }); });
    }
    function end(auto) {
      clearInterval(timer);
      addTime();
      calc.hide();
      root.remove();
      document.body.classList.remove('exam-open');
      finish(active, auto);
    }
    function tick() {
      const left = active.endsAt - Date.now();
      $('#exam-time', root).textContent = fmtTime(left);
      $('.exam-timer', root).classList.toggle('low', left < 5 * 60 * 1000);
      if (left <= 0) end(true);
    }
    // NAT answers come only from the keypad; keep stray typing from reaching the page.
    root.addEventListener('keydown', e => { if (e.target.id === 'nat') e.preventDefault(); });
    timer = setInterval(tick, 1000); tick();
    shownAt = Date.now();
    show(cur);
  }

  /* ------------------------------------------------------------ results */
  function finish(active, auto) {
    active.submitted = true;
    const paper = paperFrom(active);
    const sum = C.summarise(data, paper, active.saved);
    const usedMs = Math.min(DURATION, Date.now() - active.startedAt);
    const seen = store.get(K.seen, {});
    paper.questions.forEach(q => { seen[q.i] = (seen[q.i] || 0) + 1; });
    store.set(K.seen, seen);
    const hist = store.get(K.history, []);
    hist.unshift({ code: active.code, at: Date.now(), total: sum.total, sections: sum.sections.map(s => [s.key, s.marks]), ids: active.ids, meta: active.meta, saved: active.saved, time: active.time, used: usedMs, auto: !!auto });
    store.set(K.history, hist.slice(0, 20));
    store.del(K.active);
    renderResult(active, sum, usedMs, auto);
  }
  function renderResult(active, sum, usedMs, auto) {
    const names = data.names;
    const sec = k => sum.sections.find(s => s.key === k) || { marks: 0, max: 0, attempted: 0, correct: 0, wrong: 0 };
    const ga = sec('GA'), cs = sec('CS');
    const counts = sum.rows.reduce((a, r) => (a[r.status]++, a), { correct: 0, wrong: 0, unanswered: 0 });
    const ans = r => r.response === undefined ? '—' : Array.isArray(r.response) ? r.response.join(', ') : String(r.response);
    const out = $('#mock-result', app);
    out.hidden = false;
    $('#mock-setup', app).hidden = true;
    out.innerHTML = `
      <section class="result-head">
        <p class="eyebrow">MOCK ${esc(active.code)} · ${auto ? 'SUBMITTED WHEN TIME RAN OUT' : 'SUBMITTED'}</p>
        <h2><span class="score">${fmtMarks(sum.total)}</span> / 100</h2>
        <p>General Aptitude ${fmtMarks(ga.marks)} / ${ga.max} · Computer Science ${fmtMarks(cs.marks)} / ${cs.max} · ${counts.correct} correct, ${counts.wrong} wrong, ${counts.unanswered} not answered · time used ${fmtTime(usedMs)}</p>
        <p class="result-actions"><a class="button" href="?code=${esc(active.code)}" data-retake>Retake this mock</a> <a class="button" href="./" data-new>New mock</a> <button type="button" class="button" data-copy="${esc(active.code)}">Copy mock code</button></p>
      </section>
      ${sum.weak.length ? `<section><h2>Where you lost marks</h2><p class="source-note">Topics in this mock where marks were lost (wrong or not answered), largest first.</p><ul class="weak">${sum.weak.map(t => { const [s, tp] = t.key.split('|'); const row = sum.rows.find(r => r.s === s && r.t === tp); return `<li><b>${esc(names[s] || s)}</b> · ${esc(row ? row.tt : tp)}: lost ${fmtMarks(t.lost)} of ${t.max}</li>`; }).join('')}</ul></section>` : ''}
      <section><h2>By subject</h2><div class="table-wrap"><table class="result-table"><thead><tr><th>Subject</th><th>Questions</th><th>Attempted</th><th>Correct</th><th>Wrong</th><th>Marks</th></tr></thead><tbody>
      ${sum.subjects.map(s => `<tr><th>${esc(names[s.key] || s.key)}</th><td>${s.questions}</td><td>${s.attempted}</td><td>${s.correct}</td><td>${s.wrong}</td><td>${fmtMarks(s.marks)} / ${s.max}</td></tr>`).join('')}
      </tbody></table></div></section>
      <section><h2>Every question</h2><p class="source-note">“Our answer” marks questions with no official key, scored against our worked solution.</p><div class="table-wrap"><table class="result-table q-table"><thead><tr><th>#</th><th>Question</th><th>Your answer</th><th>Correct answer</th><th>Result</th><th>Marks</th><th>Time</th></tr></thead><tbody>
      ${sum.rows.map(r => `<tr class="r-${r.status}"><td>${r.n}</td><td><a href="${BASE}q/${esc(r.i)}/">${esc(r.l)}</a><br><small>${esc(names[r.s] || r.s)} · ${esc(r.tt)} · ${r.ty}</small></td><td>${esc(ans(r))}</td><td>${esc(C.keyText(r))}${r.ks === 'd' ? ' <small>(our answer)</small>' : ''}</td><td>${r.status === 'correct' ? '✓ Correct' : r.status === 'wrong' ? '✗ Wrong' : '— Not answered'}</td><td>${fmtMarks(r.marks)}</td><td>${fmtTime(active.time[r.i] || 0).replace(/^00:/, '')}</td></tr>`).join('')}
      </tbody></table></div></section>`;
    out.querySelector('[data-copy]').addEventListener('click', e => { try { navigator.clipboard.writeText(e.target.dataset.copy); e.target.textContent = 'Copied'; } catch (err) { e.target.textContent = e.target.dataset.copy; } });
    out.scrollIntoView();
  }
  function renderHistory() {
    const hist = store.get(K.history, []);
    const box = $('#mock-history', app);
    if (!hist.length) { box.hidden = true; return; }
    box.hidden = false;
    $('#mock-history-list', app).innerHTML = hist.map((h, n) => `<tr><td>${new Date(h.at).toLocaleString()}</td><td><code>${esc(h.code)}</code></td><td>${fmtMarks(h.total)} / 100</td><td>${h.sections.map(([k, v]) => `${k} ${fmtMarks(v)}`).join(' · ')}</td><td><button type="button" class="linklike" data-view="${n}">View</button></td></tr>`).join('');
    box.addEventListener('click', e => {
      const b = e.target.closest('[data-view]'); if (!b) return;
      const h = hist[+b.dataset.view];
      const active = { code: h.code, ids: h.ids, meta: h.meta, saved: h.saved, time: h.time || {} };
      renderResult(active, C.summarise(data, paperFrom(active), h.saved), h.used || 0, h.auto);
    });
  }

  /* ------------------------------------------------------------ calculator */
  function Calculator(host) {
    const KEYS = [
      ['mod', ' mod ', 'op'], ['sinh', 'sinh(', 'fn'], ['cosh', 'cosh(', 'fn'], ['tanh', 'tanh(', 'fn'], ['Exp', 'EXP', 'fn'], ['(', '(', ''], [')', ')', ''], ['←', 'BS', 'ctl'], ['C', 'CLR', 'ctl'], ['+/−', 'NEG', 'op'], ['√', 'sqrt(', 'fn'],
      ['sinh⁻¹', 'asinh(', 'fn'], ['cosh⁻¹', 'acosh(', 'fn'], ['tanh⁻¹', 'atanh(', 'fn'], ['log₂x', 'log2(', 'fn'], ['ln', 'ln(', 'fn'], ['log', 'log(', 'fn'], ['7', '7', 'num'], ['8', '8', 'num'], ['9', '9', 'num'], ['/', '/', 'op'], ['%', '%', 'op'],
      ['π', 'pi', 'fn'], ['e', 'e', 'fn'], ['n!', '!', 'fn'], ['logᵧx', 'logb(', 'fn'], ['eˣ', 'exp(', 'fn'], ['10ˣ', '10^(', 'fn'], ['4', '4', 'num'], ['5', '5', 'num'], ['6', '6', 'num'], ['*', '*', 'op'], ['1/x', 'INV', 'fn'],
      ['sin', 'sin(', 'fn'], ['cos', 'cos(', 'fn'], ['tan', 'tan(', 'fn'], ['xʸ', '^', 'fn'], ['x³', '^3', 'fn'], ['x²', '^2', 'fn'], ['1', '1', 'num'], ['2', '2', 'num'], ['3', '3', 'num'], ['−', '-', 'op'], ['=', 'EQ', 'eq'],
      ['sin⁻¹', 'asin(', 'fn'], ['cos⁻¹', 'acos(', 'fn'], ['tan⁻¹', 'atan(', 'fn'], ['ʸ√x', 'root(', 'fn'], ['∛', 'cbrt(', 'fn'], ['|x|', 'abs(', 'fn'], ['0', '0', 'num'], [',', ',', 'num'], ['.', '.', 'num'], ['+', '+', 'op'],
    ];
    const el = document.createElement('div');
    el.className = 'calc'; el.hidden = true;
    el.setAttribute('role', 'dialog'); el.setAttribute('aria-label', 'Scientific calculator');
    el.innerHTML = `<div class="calc-bar"><b>Scientific Calculator</b><button type="button" data-calc-close aria-label="Close calculator">×</button></div>
      <div class="calc-screen"><div class="calc-expr" aria-label="Expression"></div><div class="calc-val" aria-live="polite">0</div></div>
      <div class="calc-modes"><label><input type="radio" name="angle" value="deg" checked> Deg</label><label><input type="radio" name="angle" value="rad"> Rad</label>
        <span class="calc-mem"><button type="button" data-mem="MC">MC</button><button type="button" data-mem="MR">MR</button><button type="button" data-mem="MS">MS</button><button type="button" data-mem="M+">M+</button><button type="button" data-mem="M-">M−</button><span class="mflag" hidden>M</span></span></div>
      <div class="calc-keys">${KEYS.map(([label, v, cls]) => `<button type="button" class="${cls}" data-v="${esc(v)}">${label}</button>`).join('')}</div>
      <p class="calc-hint">ʸ√x: root(y, x) · logᵧx: logb(y, x) · use “,” between the two numbers.</p>`;
    host.appendChild(el);
    let expr = '', mem = null, justEvaluated = false;
    const exprEl = el.querySelector('.calc-expr'), valEl = el.querySelector('.calc-val');
    const deg = () => el.querySelector('input[name=angle]:checked').value === 'deg';
    const pretty = s => s.replace(/\*/g, '×').replace(/\//g, '÷').replace(/pi/g, 'π').replace(/sqrt\(/g, '√(').replace(/cbrt\(/g, '∛(');
    function draw() { exprEl.textContent = pretty(expr); }
    function value() { try { return C.evaluate(expr || '0', { deg: deg() }); } catch (e) { return null; } }
    function press(v) {
      if (v === 'CLR') { expr = ''; valEl.textContent = '0'; justEvaluated = false; return draw(); }
      if (v === 'BS') { expr = expr.replace(/(asinh|acosh|atanh|sinh|cosh|tanh|asin|acos|atan|sin|cos|tan|log2|logb|log|ln|sqrt|cbrt|abs|exp|root)\($|10\^\($| mod $|pi$|.$/, ''); return draw(); }
      if (v === 'EQ') {
        try { const r = C.evaluate(expr || '0', { deg: deg() }); valEl.textContent = C.formatResult(r); expr = C.formatResult(r).replace('Infinity', ''); justEvaluated = true; }
        catch (e) { valEl.textContent = e.message || 'Error'; }
        return;
      }
      if (v === 'NEG') { const m = /(\(-)?(\d+\.?\d*)\)?$/.exec(expr); if (m && m[1]) expr = expr.slice(0, m.index) + m[2]; else if (m) expr = expr.slice(0, m.index) + '(-' + m[2] + ')'; else expr += '-'; return draw(); }
      if (v === 'INV') { expr = '1/(' + (expr || '0') + ')'; return draw(); }
      if (v === 'EXP') { if (/\d$/.test(expr)) expr += 'e'; return draw(); }
      if (justEvaluated && /^[0-9.(]|^[a-z]/.test(v) && !/^(mod|\^)/.test(v.trim())) expr = '';
      justEvaluated = false;
      expr += v; draw();
    }
    el.addEventListener('click', e => {
      const b = e.target.closest('button'); if (!b) return;
      if (b.hasAttribute('data-calc-close')) return hide();
      const memOp = b.dataset.mem;
      if (memOp) {
        const cur = value();
        if (memOp === 'MC') mem = null;
        else if (memOp === 'MR') { if (mem !== null) { if (justEvaluated) expr = ''; expr += C.formatResult(mem); justEvaluated = false; draw(); } }
        else if (cur !== null) mem = memOp === 'MS' ? cur : (mem || 0) + (memOp === 'M+' ? cur : -cur);
        el.querySelector('.mflag').hidden = mem === null;
        return;
      }
      if (b.dataset.v !== undefined) press(b.dataset.v);
    });
    el.addEventListener('keydown', e => {
      const map = { Enter: 'EQ', '=': 'EQ', Backspace: 'BS', Escape: 'CLR' };
      if (map[e.key]) { e.preventDefault(); press(map[e.key]); }
      else if (/^[0-9.+\-*/^()%!,]$/.test(e.key)) { e.preventDefault(); press(e.key); }
    });
    // Drag by the title bar (pointer events: mouse, pen and touch).
    const bar = el.querySelector('.calc-bar');
    bar.addEventListener('pointerdown', e => {
      if (e.target.closest('button')) return;
      const r = el.getBoundingClientRect(), dx = e.clientX - r.left, dy = e.clientY - r.top;
      bar.setPointerCapture(e.pointerId);
      const move = ev => { el.style.left = Math.max(0, Math.min(innerWidth - 80, ev.clientX - dx)) + 'px'; el.style.top = Math.max(0, Math.min(innerHeight - 40, ev.clientY - dy)) + 'px'; el.style.right = 'auto'; };
      const up = () => { bar.removeEventListener('pointermove', move); bar.removeEventListener('pointerup', up); };
      bar.addEventListener('pointermove', move); bar.addEventListener('pointerup', up);
    });
    function show() { el.tabIndex = -1; el.hidden = false; el.focus(); }
    function hide() { el.hidden = true; }
    return { toggle() { el.hidden ? show() : hide(); }, hide };
  }
})();
