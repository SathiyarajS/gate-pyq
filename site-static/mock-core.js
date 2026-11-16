/* GATE-style mock test: pure logic (no DOM). Used by mock.js in the browser and by
   tests/test_mock.js in Node. Paper generation, marking and the calculator engine. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.MockCore = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /* ---------- deterministic random numbers and mock codes ---------- */
  function mulberry32(seed) {
    let a = seed >>> 0;
    return function () {
      a = (a + 0x6d2b79f5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const CODE_ALPHABET = '23456789ABCDEFGHJKMNPQRSTUVWXYZ'; // no 0/O/1/I/L
  // Code = 7 characters of seed + 1 option character (bit0 borderline, bit1 official only).
  function encodeCode(seed, opts) {
    let n = seed >>> 0, s = '';
    for (let i = 0; i < 7; i++) { s = CODE_ALPHABET[n % 31] + s; n = Math.floor(n / 31); }
    const flags = (opts.borderline ? 1 : 0) | (opts.officialOnly ? 2 : 0);
    return s.slice(0, 4) + '-' + s.slice(4) + CODE_ALPHABET[flags];
  }
  function decodeCode(code) {
    const c = String(code || '').toUpperCase().replace(/[^0-9A-Z]/g, '');
    if (c.length !== 8 || [...c].some(ch => !CODE_ALPHABET.includes(ch))) return null;
    let n = 0;
    for (const ch of c.slice(0, 7)) n = n * 31 + CODE_ALPHABET.indexOf(ch);
    const flags = CODE_ALPHABET.indexOf(c[7]);
    if (flags > 3 || n > 0xffffffff) return null;
    return { seed: n >>> 0, opts: { borderline: !!(flags & 1), officialOnly: !!(flags & 2) } };
  }

  /* ---------- answer keys and GATE marking ---------- */
  // Keys arrive normalised by scripts/mock_pool.py: MCQ 'B' or 'C|D'; MSQ 'A;C'; NAT 'lo..hi'.
  function parseKey(type, key) {
    if (type === 'MCQ') return { accept: key.split('|') };
    if (type === 'MSQ') return { set: key.split(';').sort().join(';') };
    const [lo, hi] = key.split('..').map(Number);
    return { lo, hi };
  }
  function negative(q) { return q.ty === 'MCQ' ? (q.m === 1 ? 1 / 3 : 2 / 3) : 0; }
  // response: MCQ 'B'; MSQ ['A','C']; NAT '12.5'. Returns {status, marks}.
  function mark(q, response) {
    if (response === undefined || response === null || response === '' || (Array.isArray(response) && !response.length))
      return { status: 'unanswered', marks: 0 };
    const k = parseKey(q.ty, q.k);
    let ok;
    if (q.ty === 'MCQ') ok = k.accept.includes(response);
    else if (q.ty === 'MSQ') ok = [...response].sort().join(';') === k.set;
    else {
      const v = Number(String(response).trim());
      ok = String(response).trim() !== '' && isFinite(v) && v >= k.lo - 1e-9 && v <= k.hi + 1e-9;
    }
    return ok ? { status: 'correct', marks: q.m } : { status: 'wrong', marks: negative(q) ? -negative(q) : 0 };
  }
  function keyText(q) {
    if (q.ty === 'MCQ') return q.k.split('|').join(' or ');
    if (q.ty === 'MSQ') return q.k.split(';').join(', ');
    const [lo, hi] = q.k.split('..');
    return lo === hi ? lo : lo + ' to ' + hi;
  }

  /* ---------- paper generation ---------- */
  // Pattern of every paper since 2017: GA 10 questions (5 x 1 + 5 x 2 marks), core 55 (25 x 1 + 30 x 2).
  const PATTERN = { GA: { 1: 5, 2: 5 }, CS: { 1: 25, 2: 30 } };

  function largestRemainder(weights, total, rnd) {
    const keys = Object.keys(weights), sum = keys.reduce((a, k) => a + weights[k], 0) || 1;
    const raw = keys.map(k => ({ k, v: (weights[k] / sum) * total }));
    const out = {};
    let used = 0;
    raw.forEach(r => { out[r.k] = Math.floor(r.v); used += out[r.k]; });
    raw.sort((a, b) => (b.v - Math.floor(b.v)) - (a.v - Math.floor(a.v)) || rnd() - 0.5);
    for (let i = 0; used < total && raw.length; i = (i + 1) % raw.length) { out[raw[i].k]++; used++; }
    return out;
  }
  function weightedPick(items, weightOf, rnd) {
    let total = 0;
    const w = items.map(it => { const v = Math.max(0, weightOf(it)); total += v; return v; });
    if (!total) return null;
    let r = rnd() * total;
    for (let i = 0; i < items.length; i++) { r -= w[i]; if (r <= 0) return items[i]; }
    return items[items.length - 1];
  }

  /* Generate one paper. data = pool.json; opts = {borderline, officialOnly};
     seen = {question_id: times} (lowers the chance of repeats). Deterministic for a seed
     when seen is empty. Returns {questions:[pool rows in exam order], plan}. */
  function generate(data, seed, opts, seen) {
    seen = seen || {};
    const rnd = mulberry32(seed);
    const latest = data.latest, first = 1991;
    const usable = data.pool.filter(q => (opts.borderline || !q.b) && (!opts.officialOnly || q.ks === 'o'));
    const ga = data.ga, W = data.weights;
    // Per-mock variation like real papers: each subject's share moves by up to ±25%.
    const subjW = {};
    for (const [s, v] of Object.entries(W.subjects)) if (v > 0) subjW[s] = v * (0.75 + 0.5 * rnd());
    const picked = [], used = new Set();
    const recency = y => 0.5 + (y - first) / (latest - first);       // 0.5 (1991) .. 1.5 (latest)
    const fresh = q => 1 / (1 + 3 * (seen[q.i] || 0));               // seen once: 1/4 the chance
    const topicCount = {};
    for (const q of usable) { const k = q.s + '|' + q.t; topicCount[k] = (topicCount[k] || 0) + 1; }
    const topicW = q => {
      const tw = (W.topics[q.s] || {})[q.t];
      // Topics not asked in the last ten years still appear, rarely.
      const share = tw && tw > 0 ? tw : 0.02;
      return share / topicCount[q.s + '|' + q.t];
    };

    function fill(section, subjects, quotas) {
      for (const marks of [1, 2]) {
        const n = PATTERN[section][marks];
        const perSubject = section === 'GA' ? { [ga]: n } : largestRemainder(quotas, n, rnd);
        const mix = W.type_mix[section + marks];
        // Type quotas for this section and marks, from the recent papers' mix.
        const typeQuota = largestRemainder(mix, n, rnd);
        const slots = [];
        for (const [s, c] of Object.entries(perSubject)) for (let i = 0; i < c; i++) slots.push(s);
        // Shuffle slots so type quotas are shared fairly between subjects.
        for (let i = slots.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [slots[i], slots[j]] = [slots[j], slots[i]]; }
        for (let si = 0; si < slots.length; si++) {
          const s = slots[si];
          let cands = usable.filter(q => q.s === s && q.m === marks && !used.has(q.i));
          if (!cands.length) cands = usable.filter(q => (section === 'GA' ? q.s === ga : q.s !== ga) && q.m === marks && !used.has(q.i));
          const wantType = weightedPick(Object.keys(typeQuota), t => typeQuota[t], rnd);
          const typed = cands.filter(q => q.ty === wantType);
          const pool = typed.length ? typed : cands;
          // Linked questions need room for the whole group in this subject's remaining slots.
          const room = slots.slice(si).filter(x => x === s).length;
          const fits = pool.filter(q => !q.g || usable.filter(o => o.g === q.g && o.m === marks).length <= room);
          const q = weightedPick(fits.length ? fits : pool.filter(q => !q.g), q => topicW(q) * recency(q.y) * fresh(q), rnd);
          if (!q) continue;
          const group = q.g ? usable.filter(o => o.g === q.g && o.m === marks).sort((a, b) => a.i.localeCompare(b.i, 'en', { numeric: true })) : [q];
          for (const g of group) {
            used.add(g.i); picked.push(Object.assign({ section, marks }, g));
            if (typeQuota[g.ty] > 0) typeQuota[g.ty]--;
            if (g !== q) { const idx = slots.indexOf(s, si + 1); if (idx > si) slots.splice(idx, 1); }
          }
        }
      }
    }
    fill('GA', [ga], null);
    fill('CS', Object.keys(subjW), subjW);
    // Exam order: GA then CS; 1-mark before 2-mark; linked questions stay adjacent.
    const order = [];
    for (const section of ['GA', 'CS']) for (const marks of [1, 2]) {
      const block = picked.filter(q => q.section === section && q.marks === marks);
      const units = [];
      for (const q of block) {
        const u = q.g && units.find(u => u[0].g === q.g);
        u ? u.push(q) : units.push([q]);
      }
      for (let i = units.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [units[i], units[j]] = [units[j], units[i]]; }
      units.forEach(u => order.push(...u));
    }
    return { questions: order };
  }

  // Try several seeds and keep the one with the fewest already-seen questions; the code
  // then reproduces this exact paper for anyone (generation itself ignores history).
  function freshestSeed(data, opts, seen, tries, seedSource) {
    let best = null;
    for (let t = 0; t < tries; t++) {
      const seed = seedSource();
      const paper = generate(data, seed, opts, {});
      const repeats = paper.questions.filter(q => seen[q.i]).length;
      if (!best || repeats < best.repeats) best = { seed, repeats, paper };
      if (!repeats) break;
    }
    return best;
  }

  function summarise(data, paper, responses) {
    const rows = paper.questions.map((q, n) => Object.assign({ n: n + 1, response: responses[q.i] }, q, mark(q, responses[q.i])));
    const total = rows.reduce((a, r) => a + r.marks, 0);
    const by = (keyOf) => {
      const m = new Map();
      for (const r of rows) {
        const k = keyOf(r);
        const e = m.get(k) || { key: k, questions: 0, max: 0, attempted: 0, correct: 0, wrong: 0, marks: 0 };
        e.questions++; e.max += r.m; e.marks += r.marks;
        if (r.status !== 'unanswered') e.attempted++;
        if (r.status === 'correct') e.correct++;
        if (r.status === 'wrong') e.wrong++;
        m.set(k, e);
      }
      return [...m.values()];
    };
    const sections = by(r => r.section);
    const subjects = by(r => r.s).sort((a, b) => b.max - a.max);
    const topics = by(r => r.s + '|' + r.t);
    // Weak topics: lost marks (wrong or skipped) weighted by how much the topic carries.
    const weak = topics.map(t => Object.assign(t, { lost: t.max - Math.max(0, t.marks) }))
      .filter(t => t.lost > 0).sort((a, b) => b.lost - a.lost).slice(0, 6);
    return { rows, total: Math.round(total * 100) / 100, sections, subjects, weak };
  }

  /* ---------- calculator engine ---------- */
  // Expression grammar (what the on-screen keys produce):
  //   expr := term (('+'|'-') term)* ; term := unary (('*'|'/'|'mod') unary)*
  //   unary := ('-'|'+') unary | power ; power := postfix ('^' unary)?
  //   postfix := primary ('!' | '%')* ; primary := number | const | func '(' expr (',' expr)? ')' | '(' expr ')'
  const FUNCS = {
    sin: 1, cos: 1, tan: 1, asin: 1, acos: 1, atan: 1, sinh: 1, cosh: 1, tanh: 1, asinh: 1, acosh: 1, atanh: 1,
    log: 1, ln: 1, log2: 1, sqrt: 1, cbrt: 1, abs: 1, exp: 1, root: 2, logb: 2,
  };
  function evaluate(src, opts) {
    const deg = !opts || opts.deg !== false;
    const toRad = x => (deg ? (x * Math.PI) / 180 : x);
    const fromRad = x => (deg ? (x * 180) / Math.PI : x);
    const s = String(src).replace(/\s+/g, '').replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-').replace(/π/g, 'pi');
    let i = 0;
    const peek = () => s[i], eat = (c) => { if (s.startsWith(c, i)) { i += c.length; return true; } return false; };
    function fail(msg) { throw new Error(msg || 'Syntax error'); }
    function number() {
      const m = /^(\d+\.?\d*|\.\d+)(e[+-]?\d+)?/i.exec(s.slice(i));
      if (!m) return null;
      i += m[0].length; return parseFloat(m[0]);
    }
    function primary() {
      const n = number();
      if (n !== null) return n;
      if (eat('(')) { const v = expr(); if (!eat(')')) fail('Missing )'); return v; }
      const m = /^[a-z][a-z0-9]*/.exec(s.slice(i));
      if (!m) fail();
      const name = m[0]; i += name.length;
      if (name === 'pi') return Math.PI;
      if (name === 'e') return Math.E;
      if (!FUNCS[name]) fail('Unknown ' + name);
      if (!eat('(')) fail('Missing (');
      const a = expr(); let b;
      if (FUNCS[name] === 2) { if (!eat(',')) fail('Missing ,'); b = expr(); }
      if (!eat(')')) fail('Missing )');
      switch (name) {
        case 'sin': return Math.sin(toRad(a));
        case 'cos': return Math.cos(toRad(a));
        case 'tan': { const c = Math.cos(toRad(a)); if (Math.abs(c) < 1e-15) fail('Math error'); return Math.sin(toRad(a)) / c; }
        case 'asin': return fromRad(Math.asin(a));
        case 'acos': return fromRad(Math.acos(a));
        case 'atan': return fromRad(Math.atan(a));
        case 'sinh': return Math.sinh(a); case 'cosh': return Math.cosh(a); case 'tanh': return Math.tanh(a);
        case 'asinh': return Math.asinh(a); case 'acosh': return Math.acosh(a); case 'atanh': return Math.atanh(a);
        case 'log': return Math.log10(a); case 'ln': return Math.log(a); case 'log2': return Math.log2(a);
        case 'sqrt': return Math.sqrt(a); case 'cbrt': return Math.cbrt(a); case 'abs': return Math.abs(a);
        case 'exp': return Math.exp(a);
        case 'root': return b < 0 && a % 2 === 1 ? -Math.pow(-b, 1 / a) : Math.pow(b, 1 / a); // root(n, x) = x^(1/n)
        case 'logb': return Math.log(b) / Math.log(a);                                     // logb(base, x)
      }
    }
    function factorial(n) {
      if (n < 0 || !Number.isInteger(n)) fail('Math error');
      if (n > 170) return Infinity;
      let r = 1; for (let k = 2; k <= n; k++) r *= k; return r;
    }
    function postfix() {
      let v = primary();
      for (;;) {
        if (eat('!')) v = factorial(v);
        else if (peek() === '%' ) { i++; v = v / 100; }
        else return v;
      }
    }
    // Negation binds looser than ^ (so -2^2 = -4); the exponent may itself be negative (2^-1).
    function power() { const b = postfix(); if (eat('^')) return Math.pow(b, unary()); return b; }
    function unary() { if (eat('-')) return -unary(); if (eat('+')) return unary(); return power(); }
    function term() {
      let v = unary();
      for (;;) {
        if (eat('*')) v *= unary();
        else if (eat('/')) { const d = unary(); if (d === 0) fail('Cannot divide by zero'); v /= d; }
        else if (eat('mod')) { const d = unary(); v = d === 0 ? NaN : v - d * Math.floor(v / d); }
        else return v;
      }
    }
    function expr() {
      let v = term();
      for (;;) { if (eat('+')) v += term(); else if (eat('-')) v -= term(); else return v; }
    }
    if (!s) return 0;
    const v = expr();
    if (i < s.length) fail();
    if (Number.isNaN(v)) fail('Math error');
    return v;
  }
  function formatResult(v) {
    if (!isFinite(v)) return v > 0 ? 'Infinity' : v < 0 ? '-Infinity' : 'Math error';
    if (Math.abs(v) < 1e-12) return '0';
    const r = parseFloat(v.toPrecision(12));
    return Math.abs(r) >= 1e15 || Math.abs(r) < 1e-9 ? r.toExponential(9).replace(/\.?0+e/, 'e') : String(r);
  }

  return { mulberry32, encodeCode, decodeCode, parseKey, mark, negative, keyText, generate, freshestSeed, summarise, evaluate, formatResult, PATTERN };
});
