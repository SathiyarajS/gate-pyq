import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from reader_text import reader, answer


class ReaderTextTest(unittest.TestCase):
    def test_checking_notes_and_other_copy_are_dropped(self):
        text = 'Substitute B=A.\n\nSource discrepancies and qualifications:\n- Complement bars verified visually on GateForum p7; plain OCR loses them.'
        self.assertEqual(reader(text), 'Substitute B=A.')
        self.assertEqual(reader('In GateForum, C is false. In GFG, C compares g2 with itself.'), 'C compares g2 with itself.')

    def test_labels_and_headings_are_simplified(self):
        self.assertEqual(reader('Baseline derivation and retained qualifications: Count the pairs.'), 'Solution: Count the pairs.')
        self.assertEqual(reader('Both reproductions print 6K×8 RAM.'), 'The paper prints 6K×8 RAM.')
        self.assertEqual(reader('Teaching detail: Use induction.'), 'Use induction.')

    def test_plain_text_is_unchanged(self):
        text = '1. Scan the edges in order.\n- Each find is O(log n).'
        self.assertEqual(reader(text), text)

    def test_answer_formats(self):
        self.assertEqual(answer('6 to 6'), '6')
        self.assertEqual(answer('3.7 to 3.8'), '3.7 to 3.8')
        self.assertEqual(answer('B;C'), 'B, C')


if __name__ == '__main__':
    unittest.main()


class SolutionFormattingTest(unittest.TestCase):
    def setUp(self):
        import build_site
        self.render = lambda t: str(build_site.solution(t))

    def test_bold_headings_and_exponents(self):
        self.assertIn('<strong>Common error:</strong>', self.render('**Common error:** The empty set counts.'))
        self.assertIn('<h4 class="sol-h">Method</h4>', self.render('Method:\n\nStart here.'))
        self.assertIn('a<sup>n</sup> b<sup>n</sup>', self.render('L={a^n b^n: n≥0} and 2^(n−1).'))
        self.assertIn('2<sup>n−1</sup>', self.render('L={a^n b^n: n≥0} and 2^(n−1).'))
        self.assertIn('a<sub>n−1</sub>', self.render('a_(n−1)+a_n'))

    def test_code_and_diagrams_keep_spacing(self):
        self.assertIn('n^2', self.render('int f(int n){ return n^2; }'))
        out = self.render('DELETE(x):\n  k:=pos[x];\n  pos[x]:=0.\nThe position array directly locates x, avoiding a search entirely.')
        self.assertIn('<pre class="figure-text">DELETE(x):', out)
        self.assertIn('<p>The position array', out)
