// Mock test logic: marking, codes, calculator and paper generation.
// Run: node tests/test_mock.js [path/to/_site/mock/pool.json]   (generation tests need a built pool)
'use strict';
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const C = require('../site-static/mock-core.js');
let passed = 0;
const test = (name, fn) => { fn(); passed++; };

test('codes round-trip with options', () => {
  for (const seed of [0, 1, 123456789, 4294967295]) for (const opts of [{}, { borderline: true }, { officialOnly: true }, { borderline: true, officialOnly: true }]) {
    const code = C.encodeCode(seed, opts);
    assert.match(code, /^[2-9A-Z]{4}-[2-9A-Z]{4}$/);
    const d = C.decodeCode(code.toLowerCase());
    assert.strictEqual(d.seed, seed);
    assert.strictEqual(d.opts.borderline, !!opts.borderline);
    assert.strictEqual(d.opts.officialOnly, !!opts.officialOnly);
  }
  assert.strictEqual(C.decodeCode('nope'), null);
  assert.strictEqual(C.decodeCode('0000-0000'), null);
});

test('GATE marking', () => {
  const mcq1 = { ty: 'MCQ', m: 1, k: 'B' }, mcq2 = { ty: 'MCQ', m: 2, k: 'C|D' };
  assert.deepStrictEqual(C.mark(mcq1, 'B'), { status: 'correct', marks: 1 });
  assert.strictEqual(C.mark(mcq1, 'A').marks.toFixed(4), (-1 / 3).toFixed(4));
  assert.strictEqual(C.mark(mcq2, 'D').status, 'correct');
  assert.strictEqual(C.mark(mcq2, 'A').marks.toFixed(4), (-2 / 3).toFixed(4));
  assert.deepStrictEqual(C.mark(mcq1, undefined), { status: 'unanswered', marks: 0 });
  const msq = { ty: 'MSQ', m: 2, k: 'A;C' };
  assert.strictEqual(C.mark(msq, ['C', 'A']).marks, 2);
  assert.deepStrictEqual(C.mark(msq, ['A']), { status: 'wrong', marks: 0 });     // no partial, no negative
  assert.deepStrictEqual(C.mark(msq, []), { status: 'unanswered', marks: 0 });
  const nat = { ty: 'NAT', m: 2, k: '2.4..2.6' };
  assert.strictEqual(C.mark(nat, '2.5').marks, 2);
  assert.strictEqual(C.mark(nat, '2.6').marks, 2);
  assert.deepStrictEqual(C.mark(nat, '2.61'), { status: 'wrong', marks: 0 });
  assert.deepStrictEqual(C.mark(nat, '-'), { status: 'wrong', marks: 0 });
  assert.strictEqual(C.keyText(nat), '2.4 to 2.6');
  assert.strictEqual(C.keyText({ ty: 'NAT', k: '7..7' }), '7');
  assert.strictEqual(C.keyText(mcq2), 'C or D');
});

test('calculator', () => {
  const ev = (s, deg = true) => C.evaluate(s, { deg });
  const near = (a, b) => assert.ok(Math.abs(a - b) < 1e-9, `${a} vs ${b}`);
  near(ev('2+3*4'), 14);
  near(ev('(2+3)*4'), 20);
  near(ev('2^3^2'), 512);              // right-associative
  near(ev('-2^2'), -4);
  near(ev('2^-1'), 0.5);
  near(ev('(-2)^2'), 4);
  near(ev('10 mod 3'), 1);
  near(ev('-7 mod 3'), 2);
  near(ev('5!'), 120);
  near(ev('50%'), 0.5);
  near(ev('sin(30)'), 0.5);
  near(ev('sin(pi/6)', false), 0.5);
  near(ev('asin(1)'), 90);
  near(ev('log(1000)'), 3);
  near(ev('ln(e)'), 1);
  near(ev('log2(1024)'), 10);
  near(ev('logb(3,81)'), 4);
  near(ev('root(3,27)'), 3);
  near(ev('root(3,-8)'), -2);
  near(ev('sqrt(2)^2'), 2);
  near(ev('cbrt(64)'), 4);
  near(ev('abs(-3.5)'), 3.5);
  near(ev('exp(1)'), Math.E);
  near(ev('10^(2)'), 100);
  near(ev('1.5e3+1'), 1501);
  near(ev('1/(4)'), 0.25);
  assert.throws(() => ev('1/0'));
  assert.throws(() => ev('2+'));
  assert.throws(() => ev('(-3)!'));
  assert.throws(() => ev('tan(90)'));
  assert.strictEqual(C.formatResult(0.1 + 0.2), '0.3');
  assert.strictEqual(C.formatResult(1e-13), '0');
});

// Key sequences as the exam's calculator takes them: the number first, then the function key.
test('calculator keys work number first, like the exam', () => {
  const run = (keys, deg = true, mem) => {
    let st = Object.assign(C.calcInit(), { mem });
    for (const k of keys.split(' ')) st = Object.assign(C.calcPress(st, k, { deg }), { mem });
    return st;
  };
  // Results are the raw floating-point value, as the exam shows them; compare numbers with a tolerance.
  const is = (keys, want, deg) => {
    const got = run(keys, deg).val, w = Number(want);
    if (!isFinite(w) || want === '') return assert.strictEqual(got, want, keys);
    assert.ok(Math.abs(Number(got) - w) <= 1e-9 * Math.max(1, Math.abs(w)), `${keys}: ${got} vs ${want}`);
  };
  is('3 0 sin', '0.5');                 // 30 sin
  is('3 0 sin', C.formatResult(Math.sin(30)), false);
  is('1 sinh', C.formatResult(Math.sinh(1)));
  is('1 0 0 0 log', '3');
  is('e ln', '1');
  is('2 5 6 log2', '8');
  is('8 1 logy 3 =', '4');              // 81 logᵧx 3 = : log base 3 of 81
  is('2 ^ 1 0 =', '1024');
  is('6 2 5 yroot 4 =', '5');           // 625 ʸ√x 4 = : 4th root of 625
  is('8 yroot 3 =', '2');
  is('5 sqr', '25');
  is('4 cube', '64');
  is('1 4 4 sqrt', '12');
  is('2 7 cbrt', '3');
  is('5 fact', '120');
  is('4 recip', '0.25');
  is('2 exp', C.formatResult(Math.exp(2)));
  is('3 pow10', '1000');
  is('3 EXP 5 =', '300000');
  is('3 EXP 5 NEG =', '0.00003');
  is('5 NEG', '-5');
  is('7 NEG abs', '7');
  is('2 0 log * 3 - 7 =', String(C.formatResult(Math.log10(20) * 3 - 7)));
  is('7 3 * ( 2 + 3 ) =', '365');
  is('8 * pi =', String(C.formatResult(8 * Math.PI)));
  is('2 + 3 sqr =', '11');              // the one-number key applies to the 3 only
  is('( 2 + 3 ) sqr =', '25');
  is('5 sqr sqr', '625');
  is('2 * 3 = * 2 =', '12');            // a result carries on into the next operation
  is('2 * 3 = 4', '4');                 // a new number after = starts over
  is('1 0 mod 3 =', '1');
  is('2 * - 3 =', '-6');
  is('2 + * 3 =', '6');                 // a second operator replaces the first
  is('( 2 + 3 =', '5');                 // open brackets are closed on =
  is('1 2 BS 3 =', '13');
  is('3 0 sin BS', '30');               // backspace unwraps the last function
  is('1 . . 5 =', '1.5');
  is('0 0 7', '7');
  is('5 0 %', '0.5');
  is('5 NEG 3', '-53');
  is('1 / 0 =', 'Cannot divide by zero');
  is('9 0 tan', 'Math error');
  assert.strictEqual(run('2 + MR =', true, 5).val, '7');
  // What the official mock shows (checked against screenshots of it):
  assert.strictEqual(run('3 0 sin').val, '0.49999999999999994');            // unrounded
  assert.strictEqual(C.calcTop(run('3 0 sin'), true), 'sind(30)');
  assert.strictEqual(C.calcTop(run('3 0'), true), '');                      // 30 is still being typed
  assert.strictEqual(C.calcTop(run('6 2 5 yroot'), true), '625yroot');
  assert.strictEqual(run('6 2 5 yroot').val, '625');
  assert.strictEqual(C.calcTop(run('6 2 5 yroot 4'), true), '625yroot');
  assert.strictEqual(run('6 2 5 yroot 4').val, '4');
  assert.strictEqual(C.calcTop(run('6 2 5 yroot 4 ='), true), '625yroot4');
  assert.strictEqual(run('6 2 5 yroot 4 =').val, '5');
  assert.strictEqual(C.calcTop(run('mod'), true), '0mod');                  // operator on an empty display
  assert.strictEqual(C.calcTop(run('logy'), true), '0logxBasey');
  assert.strictEqual(C.calcTop(run('8 1 logy 3 ='), true), '81logxBasey3');
  assert.strictEqual(run('CLR').val, '0');
});

const poolPath = process.argv[2] || path.join(__dirname, '..', '_site', 'mock', 'pool.json');
if (fs.existsSync(poolPath)) {
  const data = JSON.parse(fs.readFileSync(poolPath, 'utf8'));
  test('every generated paper follows the GATE pattern', () => {
    for (let seed = 1; seed <= 300; seed++) {
      const opts = { borderline: seed % 3 === 0, officialOnly: seed % 5 === 0 };
      const paper = C.generate(data, seed * 2654435761 >>> 0, opts, {}).questions;
      const ids = new Set(paper.map(q => q.i));
      assert.strictEqual(paper.length, 65, `seed ${seed}: ${paper.length} questions`);
      assert.strictEqual(ids.size, 65, `seed ${seed}: duplicate question`);
      const ga = paper.filter(q => q.section === 'GA'), cs = paper.filter(q => q.section === 'CS');
      assert.strictEqual(ga.length, 10); assert.strictEqual(cs.length, 55);
      assert.ok(ga.every(q => q.s === data.ga)); assert.ok(cs.every(q => q.s !== data.ga));
      assert.strictEqual(ga.reduce((a, q) => a + q.m, 0), 15);
      assert.strictEqual(cs.reduce((a, q) => a + q.m, 0), 85);
      if (!opts.borderline) assert.ok(paper.every(q => !q.b));
      if (opts.officialOnly) assert.ok(paper.every(q => q.ks === 'o'));
      // exam order: GA first, 1-mark before 2-mark within a section
      const order = paper.map(q => (q.section === 'GA' ? 0 : 2) + (q.m - 1));
      assert.deepStrictEqual(order, [...order].sort((a, b) => a - b));
    }
  });
  test('same seed, same paper; different seeds differ', () => {
    const a = C.generate(data, 42, {}, {}).questions.map(q => q.i);
    const b = C.generate(data, 42, {}, {}).questions.map(q => q.i);
    const c = C.generate(data, 43, {}, {}).questions.map(q => q.i);
    assert.deepStrictEqual(a, b);
    assert.ok(c.filter(id => a.includes(id)).length < 20);
  });
  test('subject mix tracks recent weightage', () => {
    const marks = {}; let n = 0;
    for (let seed = 1; seed <= 400; seed++) {
      for (const q of C.generate(data, seed * 7919, {}, {}).questions) if (q.section === 'CS') marks[q.s] = (marks[q.s] || 0) + q.m;
      n++;
    }
    const w = data.weights.subjects, total = Object.values(w).reduce((a, b) => a + b, 0);
    for (const [s, v] of Object.entries(w)) {
      const expected = (85 * v) / total, got = marks[s] / n;
      assert.ok(Math.abs(got - expected) < 1.6, `${s}: ${got.toFixed(2)} marks per paper vs ${expected.toFixed(2)} expected`);
    }
  });
  test('linked (common-data) pairs come together and in order', () => {
    const groups = {};
    for (const q of data.pool) if (q.g) (groups[q.g] = groups[q.g] || []).push(q.i);
    assert.ok(Object.keys(groups).length >= 30, 'linked groups found: ' + Object.keys(groups).length);
    let seenGroups = 0;
    for (let seed = 1; seed <= 600; seed++) {
      const ids = C.generate(data, seed * 31337, { officialOnly: seed % 2 === 0 }, {}).questions.map(q => q.i);
      for (const [g, members] of Object.entries(groups)) {
        const at = members.map(i => ids.indexOf(i)).filter(n => n >= 0);
        if (!at.length) continue;
        const usable = data.pool.filter(q => q.g === g && (seed % 2 !== 0 || q.ks === 'o')).length;
        if (usable < members.length) continue;
        seenGroups++;
        assert.strictEqual(at.length, members.length, `seed ${seed}: only part of ${members}`);
        at.forEach((n, k) => assert.strictEqual(n, at[0] + k, `seed ${seed}: ${members} not adjacent and in order`));
      }
    }
    assert.ok(seenGroups > 20, 'groups drawn: ' + seenGroups);
  });
  test('modern question-type mix', () => {
    const t = { MCQ: 0, MSQ: 0, NAT: 0 };
    for (let seed = 1; seed <= 200; seed++) for (const q of C.generate(data, seed * 104729, {}, {}).questions) if (q.section === 'CS') t[q.ty]++;
    const per = k => t[k] / 200;
    assert.ok(per('NAT') > 12 && per('MSQ') > 8, JSON.stringify({ MCQ: per('MCQ'), MSQ: per('MSQ'), NAT: per('NAT') }));
  });
  test('seen questions are avoided', () => {
    const seen = {};
    for (const q of C.generate(data, 7, {}, {}).questions) seen[q.i] = 1;
    let s = 1000;
    const best = C.freshestSeed(data, {}, seen, 12, () => s++);
    assert.ok(best.repeats <= 3, 'repeats ' + best.repeats);
  });
  test('summary totals', () => {
    const paper = C.generate(data, 99, {}, {});
    const resp = {};
    paper.questions.forEach((q, n) => { if (n % 2 === 0) resp[q.i] = q.ty === 'MSQ' ? q.k.split(';') : q.ty === 'NAT' ? q.k.split('..')[0] : q.k.split('|')[0]; });
    const sum = C.summarise(data, paper, resp);
    const expected = paper.questions.reduce((a, q, n) => a + (n % 2 === 0 ? q.m : 0), 0);
    assert.strictEqual(sum.total, expected);
    assert.strictEqual(sum.sections.length, 2);
    assert.deepStrictEqual(sum.rows.map(r => r.n), paper.questions.map((q, k) => k + 1));   // numbered 1..65, not by choice count
  });
} else {
  console.log('(pool not built: generation tests skipped; run scripts/build_site.py --release first)');
}
console.log(`Mock test logic passed: ${passed} checks.`);
