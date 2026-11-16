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
  });
} else {
  console.log('(pool not built: generation tests skipped; run scripts/build_site.py --release first)');
}
console.log(`Mock test logic passed: ${passed} checks.`);
