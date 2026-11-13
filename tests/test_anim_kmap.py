import sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from animations import kmap


def spec(**kw):
    return dict(kind='kmap', **kw)


class KMapTest(unittest.TestCase):
    def test_prime_and_essential_implicants_match_the_worked_solution(self):
        # CS-2018-Q59: five primes 01-1, 0-11, 10--, -01-, -0-0; three are essential.
        km, sol = kmap.kmap_solve('Q', spec(vars=list('PQRS'), minterms=[0, 2, 5, 7, 9, 11], dontcares=[3, 8, 10, 12, 14], expect={}))
        self.assertEqual(sorted(p['text'] for p in sol['pis']), sorted(['P′QS', 'P′RS', 'PQ′', 'Q′R', 'Q′S′']))
        self.assertEqual(sorted(sol['pis'][k]['text'] for k in sol['essential']), sorted(['P′QS', 'PQ′', 'Q′S′']))

    def test_a_map_is_read_in_gray_code_order(self):
        # CS-2012-Q40: columns ab, rows cd; the corners and the outer columns of rows 00/01.
        s = spec(vars=list('abcd'), map=dict(rows=['c', 'd'], cols=['a', 'b'], cells=[[1, 'X', 'X', 1], ['X', 0, 0, 1], [0, 0, 0, 0], [1, 0, 0, 'X']]), expect={})
        km, sol = kmap.kmap_solve('Q', s)
        self.assertEqual(km.grid[0], [0, 4, 12, 8])
        self.assertEqual(sorted(km.on), [0, 2, 8, 9])
        self.assertEqual(sorted(km.dc), [1, 4, 10, 12])
        self.assertEqual(sol['cost'], (2, 4))

    def test_non_unique_minimal_covers_are_all_accepted(self):
        # CS-2026-S1-Q48: options B and D are both minimal; A and C miss a 1.
        on = [1, 2, 3, 4, 5, 7, 10, 12, 13, 14]
        claims = [dict(type='minimal', value=v, holds=h) for v, h in (("P'S+QR'+P'Q'R+Q'RS'", False), ("P'S+QR'+P'Q'R+PRS'", True),
                                                                      ("P'S+QR'+PQS'+PRS'", False), ("P'S+QR'+PQS'+Q'RS'", True))]
        data = kmap.kmap_animation('Q', spec(vars=list('PQRS'), minterms=on, expect=dict(claims=claims)))
        self.assertIn('Other choices with the same cost', data['schedules'][0]['steps'][-len(claims) - 2]['note'])
        claims[0]['holds'] = True
        with self.assertRaises(SystemExit):
            kmap.kmap_animation('Q', spec(vars=list('PQRS'), minterms=on, expect=dict(claims=claims)))

    def test_product_of_sums_groups_the_zeros(self):
        # CS-2017-S2-Q38: f = (w'+z')(x'+z).
        s = spec(vars=list('wxyz'), form='pos', minterms=[0, 1, 2, 3, 7, 8, 10], dontcares=[5, 6, 11, 15], expect=dict(minimal="(w'+z')(x'+z)"))
        self.assertIn('(w′ + z′)(x′ + z)', kmap.kmap_animation('Q', s)['schedules'][0]['steps'][-1]['note'])
        s['expect']['minimal'] = "(w+z)(x'+z)"
        with self.assertRaises(SystemExit):
            kmap.kmap_animation('Q', s)

    def test_an_equivalent_but_larger_expression_is_not_minimal(self):
        # CS-2012-Q40 option D adds c'd', which only covers ones already covered.
        s = spec(vars=list('abcd'), map=dict(rows=['c', 'd'], cols=['a', 'b'], cells=[[1, 'X', 'X', 1], ['X', 0, 0, 1], [0, 0, 0, 0], [1, 0, 0, 'X']]),
                 expect=dict(minimal="b'd'+b'c'+c'd'"))
        with self.assertRaises(SystemExit):
            kmap.kmap_animation('Q', s)
        s['expect'] = dict(minimal="b'd'+b'c'", rejects=["b'd'+b'c'"])
        with self.assertRaises(SystemExit):
            kmap.kmap_animation('Q', s)

    def test_expressions_fill_the_map(self):
        # CS-2015-S2-Q55: the complement of the bracket is ABCD alone.
        km, sol = kmap.kmap_solve('Q', spec(vars=list('ABCD'), expr="~(D'+AB'+A'C+AC'D+A'C'D)", expect={}))
        self.assertEqual(sorted(km.on), [15])
        # CS-2011-Q24: a product of sums sets the 0s one factor at a time.
        km, sol = kmap.kmap_solve('Q', spec(vars=list('PQR'), expr="(P+Q'+R')(P+Q'+R)(P+Q+R')", expect={}))
        self.assertEqual(sorted(km.off), [1, 2, 3])
        self.assertEqual([s['hi'] for s in sol['steps'][1:4]], [[3], [2], [1]])

    def test_claims_about_terms(self):
        # CS-1997-Q36: xz is an implicant, not a minterm; y'x is not prime.
        claims = [dict(type='prime', value="y'x", holds=False), dict(type='minterm', value='xz', holds=False), dict(type='implicant', value='xz', holds=True)]
        kmap.kmap_animation('Q', spec(vars=list('xyz'), expr="x'+y'x+xz", expect=dict(claims=claims)))
        claims[0]['holds'] = True
        with self.assertRaises(SystemExit):
            kmap.kmap_animation('Q', spec(vars=list('xyz'), expr="x'+y'x+xz", expect=dict(claims=claims)))

    def test_parser(self):
        node = kmap.parse("~(b1b0)+b3'", ['b3', 'b2', 'b1', 'b0'])
        self.assertEqual(sorted(kmap.ones(node, 4)), [m for m in range(16) if m & 3 != 3 or not m & 8])
        with self.assertRaises(SystemExit):
            kmap.parse('A+q', ['A', 'B'])


if __name__ == '__main__':
    unittest.main()
