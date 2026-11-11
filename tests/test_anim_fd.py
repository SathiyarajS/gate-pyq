import sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from animations import fd


def rel(attrs, fds):
    names = list(attrs)
    return fd.Rel('R', names, [fd._parse_fd(x, names) for x in fds])


class FDTest(unittest.TestCase):
    def test_closure_fires_in_order_and_stops(self):
        # CS-2006-Q70: (AF)+ = {A, D, E, F}; C and G never appear.
        r = rel('ABCDEFG', ['AB->CD', 'AF->D', 'DE->F', 'C->G', 'F->E', 'G->A'])
        full, fired = r.close(frozenset('AF'))
        self.assertEqual(full, frozenset('ADEF'))
        self.assertEqual([i for i, _ in fired], [1, 4])

    def test_candidate_keys(self):
        # CS-2013-Q64: four keys, each D with one of A, B, E, F.
        r = rel('ABCDEFGH', ['CH->G', 'A->BC', 'B->CFH', 'E->A', 'F->EG'])
        keys = fd.candidate_keys(r)[0]
        self.assertEqual({''.join(sorted(k)) for k in keys}, {'AD', 'BD', 'DE', 'DF'})

    def test_normal_forms(self):
        # 3NF but not BCNF (AB -> C, C -> A); 1NF only (a -> c, b -> d); 2NF only (marks -> grade).
        cases = [('ABC', ['AB->C', 'C->A'], '3NF'), ('abcd', ['a->c', 'b->d'], '1NF'),
                 ('RCMG', ['RC->MG', 'M->G'], '2NF'), ('ABC', ['A->BC'], 'BCNF')]
        for attrs, fds, want in cases:
            r = rel(attrs, fds)
            out = {}
            fd.do_nf(r, fd.candidate_keys(r)[0], None, [], out)
            self.assertEqual(out['nf'], want, attrs)

    def test_projection(self):
        # CS-2002-Q84: R1(L, M, N, P) gets MN -> P through M -> O and NO -> P.
        full = rel('LMNOP', ['M->O', 'NO->P', 'P->L', 'L->MN'])
        r1 = fd.project(full, list('LMNP'), 'R1')
        self.assertTrue(frozenset('P') <= r1.close(frozenset('MN'))[0])
        self.assertNotIn('O', r1.close(frozenset('M'))[0])

    def test_chase(self):
        # CS-2021-S1-Q43: D1 lossless, D2 lossy.
        r = rel('PQSTXYZW', ['PQ->X', 'P->YX', 'Q->Y', 'Y->ZW'])
        d1 = [(n, frozenset(n)) for n in ['PQST', 'PTX', 'QY', 'YZW']]
        d2 = [(n, frozenset(n)) for n in ['PQS', 'TX', 'QY', 'YZW']]
        self.assertTrue(fd.chase(r, d1)[0])
        self.assertFalse(fd.chase(r, d2)[0])

    def test_minimal_cover(self):
        spec = dict(kind='fd', attrs='VWXYZ', fds=['V->W', 'VW->X', 'Y->VX', 'Y->Z'], do=['cover'],
                    expect=dict(cover=['V->W', 'V->X', 'Y->V', 'Y->Z']))
        self.assertTrue(fd.fd_animation('Q', spec)['schedules'][0]['steps'][-1]['final'])
        spec['expect']['cover'] = ['V->W', 'W->X', 'Y->V', 'Y->Z']
        with self.assertRaises(SystemExit):
            fd.fd_animation('Q', spec)

    def test_wrong_expectations_stop_the_build(self):
        base = dict(kind='fd', attrs='ABC', fds=['AB->C', 'C->A'])
        for do, expect in [(['keys'], dict(keys=['AB'])), (['keys', 'nf'], dict(nf='BCNF')),
                           ([dict(implies='C->B')], dict(implied={'C->B': True})),
                           (['preserve'], dict(preserved=True))]:
            spec = dict(base, do=do, expect=expect, components={'R1': 'AC', 'R2': 'BC'})
            with self.assertRaises(SystemExit):
                fd.fd_animation('Q', spec)


if __name__ == '__main__':
    unittest.main()
