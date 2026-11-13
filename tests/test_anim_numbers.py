import sys, unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from animations import numbers


def run(kind, spec, qid='Q'):
    return numbers.KINDS[kind](qid, dict(spec, kind=kind))


class RadixTest(unittest.TestCase):
    def test_expansion_and_division(self):
        # CS-2023-Q32: 132 in base 4 is 30, which is 110 in base 5.
        steps, total, _ = numbers.expand_steps('132', 4)
        self.assertEqual(total, 30)
        _, digits, rows = numbers.divide_steps(30, 5)
        self.assertEqual(digits, '110')
        self.assertEqual([r[0] for r in rows], [30, 6, 1])

    def test_binary_fraction_and_pattern(self):
        # CS-2021-S2-Q28: 0.1101 in binary is 0.8125 = 0.8xy5, so x + y = 3.
        out = run('radix-convert', {'numeral': '0.1101', 'from': 2, 'to': 10, 'pattern': '0.8xy5', 'expect': {'result': '0.8125', 'sum': 3}})
        self.assertIn('x + y = 3', out['schedules'][0]['steps'][-1]['note'])
        with self.assertRaises(SystemExit):
            run('radix-convert', {'numeral': '0.1101', 'from': 2, 'to': 10, 'pattern': '0.8xy5', 'expect': {'sum': 4}})

    def test_regroup_power_of_two_bases(self):
        # CS-2017-S2-Q11: BCA9 hexadecimal is 136251 octal.
        steps, result = numbers.regroup_steps('BCA9', 16, 8)
        self.assertEqual(result, '136251')
        # CS-2009-Q5: the option is printed with a leading zero, 028F.
        run('radix-convert', {'numeral': '1217', 'from': 8, 'to': 16, 'method': 'regroup', 'expect': {'result': '028F'}})
        with self.assertRaises(SystemExit):
            run('radix-convert', {'numeral': '1217', 'from': 8, 'to': 16, 'method': 'regroup', 'expect': {'result': '0B17'}})

    def test_a_digit_too_big_for_its_base_stops(self):
        with self.assertRaises(SystemExit):
            numbers.value_of('129', 8)


class EquationTest(unittest.TestCase):
    def test_counts_only_valid_digits(self):
        # CS-2014-S2-Q18: 123 in base 5 = x8 in base y has three valid (x, y).
        out = run('radix-equation', {'equations': ['123_5 = x8_y'], 'expect': {'count': 3}})
        rows = out['schedules'][0]['steps'][-1]['blocks'][0]['rows']
        self.assertEqual(len(rows), 7)  # every factor pair of 30, four of them invalid
        with self.assertRaises(SystemExit):
            run('radix-equation', {'equations': ['123_5 = x8_y'], 'expect': {'count': 4}})

    def test_square_root_and_options(self):
        # CS-1997-Q39: sqrt(224_r) = 13_r only for r = 5.
        run('radix-equation', {'equations': ['sqrt(224_r) = 13_r'], 'options': [{'r': 10}, {'r': 8}, {'r': 5}, {'r': 6}], 'expect': {'solutions': [{'r': 5}]}})

    def test_find_base_then_add_in_it(self):
        # CS-2010-Q6: 137 + 276 = 435 holds in base 8, where 731 + 672 = 1623.
        out = run('radix-equation', {'equations': ['137_b + 276_b = 435_b'], 'then': '731_b + 672_b', 'expect': {'solutions': [{'b': 8}], 'then': '1623'}})
        self.assertEqual(len(out['schedules']), 2)

    def test_expression_parser(self):
        e = numbers.parse_expr('4(X+Y)+Z=0')
        self.assertTrue(numbers.evaluate(e, {'X': Fraction(-9), 'Y': Fraction(6), 'Z': Fraction(12)}))
        self.assertEqual(numbers.evaluate(numbers.parse_expr('312_b / 20_b'), {'b': 5}), Fraction(41, 5))


class SignedTest(unittest.TestCase):
    def test_column_subtraction_with_borrow(self):
        # CS-2014-S3-Q10: 7526 - 4364 = 3142 in octal.
        _, result = numbers.column_steps('7526', '4364', 8, '-')
        self.assertEqual(result, '3142')

    def test_encode_and_decode(self):
        run('signed-encode', {'value': -539, 'bits': 12, 'expect': {'hex': 'DE5'}})  # CS-2001-Q35
        self.assertEqual(numbers.twos('1111111111110101'), -11)  # CS-2016-S1-Q17
        run('signed-decode', {'patterns': ['11100111', '11100100'], 'test': {'divisible_by': '11111011'}, 'expect': {'match': ['11100111']}})

    def test_overflow_by_carries(self):
        # CS-2024-S1-Q13: with A = 01010 and B = 11010, only A - B overflows 5 bits.
        spec = {'bits': 5, 'operands': {'A': '01010', 'B': '11010'}, 'ops': ['A+B', 'A−B', 'B−A', '2B'], 'expect': {'overflow': ['A−B']}}
        out = run('signed-ops', spec)
        self.assertEqual([s['short'] for s in out['schedules']], ['A+B', 'A−B', 'B−A', '2B'])
        spec['expect'] = {'overflow': ['B−A']}
        with self.assertRaises(SystemExit):
            run('signed-ops', spec)

    def test_shift_and_sign_magnitude(self):
        run('signed-ops', {'bits': 16, 'operands': {'P': '1111100001111011'}, 'ops': ['8P'], 'expect': {'results': {'8P': 'C3D8'}}})  # CS-2010-Q18
        run('signed-ops', {'bits': 8, 'repr': 'sign-magnitude', 'operands': {'X': '10110100', 'Y': '01001100'},
                           'ops': ['X+Y', 'X−Y', '−X+Y', '−X−Y'], 'expect': {'overflow': ['X−Y', '−X+Y']}})  # CS-2026-S1-Q22


class FloatTest(unittest.TestCase):
    def test_encode_decode_round_trip(self):
        bits, e, _ = numbers.f32_encode(Fraction('-14.25'))
        self.assertEqual(numbers._hex(bits), 'C1640000')  # CS-2014-S2-Q55
        self.assertEqual(numbers.f32_decode(format(0xC2710000, '032b')), ('normal', Fraction('-60.25')))  # CS-2026-S2-Q34
        self.assertEqual(numbers.f32_decode('0' * 32)[0], 'zero')
        self.assertEqual(numbers.f32_decode('0' + '1' * 31)[0], 'NaN')
        with self.assertRaises(SystemExit):
            numbers.f32_encode(Fraction(1, 10))  # 0.1 needs rounding

    def test_register_arithmetic(self):
        # CS-2026-S1-Q36: 35C00000 + 34A00000 = 35E80000.
        run('ieee754', {'registers': {'X': '35C00000', 'Y': '34A00000'}, 'compute': 'X+Y', 'expect': {'hex': '35E80000'}})
        with self.assertRaises(SystemExit):
            run('ieee754', {'registers': {'X': '35C00000', 'Y': '34A00000'}, 'compute': 'X+Y', 'expect': {'hex': '35EC0000'}})


class BoothTest(unittest.TestCase):
    def test_counts_bit_changes(self):
        # CS-2025-S2-Q32: 13 additions and subtractions.
        run('booth', {'multiplier': '1010 0100 1010 1010', 'multiplicand': '1100 1101 1110 1101', 'expect': {'count': 13}})
        with self.assertRaises(SystemExit):
            run('booth', {'multiplier': '1010 0100 1010 1010', 'multiplicand': '0', 'expect': {'count': 16}})
