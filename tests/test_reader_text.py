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
