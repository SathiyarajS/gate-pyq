"""Build-level regression: all original questions remain reachable in every view."""
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class StudyViewRenderingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output = tempfile.TemporaryDirectory(dir=ROOT, prefix='_test-study-')
        cls.addClassCleanup(cls.output.cleanup)
        cls.site = Path(cls.output.name)
        subprocess.run([sys.executable, str(ROOT/'scripts/build_site.py'), '--preview',
                        '--output', cls.site.name], check=True, capture_output=True, text=True)
        cls.questions = json.loads((ROOT/'data/questions.json').read_text())

    def test_every_question_once_in_each_view_across_pagination(self):
        subjects = {q['subject'] if q['subject'] != 'excluded' else '13-other-topics' for q in self.questions}
        for subject in subjects:
            expected = Counter(q['question_id'] for q in self.questions
                               if (q['subject'] if q['subject'] != 'excluded' else '13-other-topics') == subject)
            for view in ['', 'unique', 'patterns']:
                with self.subTest(subject=subject, view=view):
                    base = self.site/subject/view
                    pages = [base/'index.html'] + list((base/'page').glob('*/index.html'))
                    actual = Counter(qid for page in pages for qid in
                                     re.findall(r'<article class="question" id="([^"]+)"', page.read_text()))
                    self.assertEqual(actual, expected)
            records = json.loads((self.site/subject/'index.json').read_text())
            self.assertEqual(Counter(r['id'] for r in records), expected)

    def test_all_view_stays_filterable_and_canonical(self):
        subject = '08-operating-systems'
        all_html = (self.site/subject/'index.html').read_text()
        self.assertIn('id="filters"', all_html)
        self.assertIn('>All questions</a>', all_html)
        self.assertIn('>Known repeats folded</a>', all_html)
        self.assertIn('>Problem patterns</a>', all_html)
        redirect = (self.site/'q/CS-2024-S2-Q37/index.html').read_text()
        self.assertNotIn('/patterns/', redirect)
        self.assertNotIn('/unique/', redirect)

    def test_pattern_alternatives_and_coverage(self):
        html = (self.site/'08-operating-systems/patterns/index.html').read_text()
        self.assertRegex(html, r'\d+ in \d+ reviewed problem patterns')
        self.assertIn('Browse reviewed patterns', html)
        html = next(p.read_text() for p in (self.site/'08-operating-systems/patterns').rglob('index.html') if 'id="group-srtf-schedule-metrics"' in p.read_text())
        self.assertIn('id="group-srtf-schedule-metrics"', html)
        self.assertIn('class="group-alternatives"', html)
        self.assertIn('Show 4 alternative questions', html)
        self.assertIn('id="CS-2024-S2-Q37"', html)
        self.assertIn('id="CS-2004-Q46"', html)
        self.assertIn('Source page 7', html)
        self.assertIn('not a transcription or answer certification', html)
        self.assertNotIn('id="filters"', html)
        for view in ['unique','patterns']:
            html = (self.site/'08-operating-systems'/view/'index.html').read_text()
            self.assertIn('Coverage is incomplete', html)
            self.assertNotIn('unique questions', html.lower())


if __name__ == '__main__': unittest.main()
