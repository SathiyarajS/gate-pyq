"""Build-level regression: one newest-first list per subject and topic, plus similar-question pages."""
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = re.compile(r'<article class="question" id="([^"]+)"[^>]*data-year="(\d+)"([^>]*)>')


def subject_of(q):
    return q['subject'] if q['subject'] != 'excluded' else '13-other-topics'


class StudyViewRenderingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output = tempfile.TemporaryDirectory(dir=ROOT, prefix='_test-study-')
        cls.addClassCleanup(cls.output.cleanup)
        cls.site = Path(cls.output.name)
        subprocess.run([sys.executable, str(ROOT/'scripts/build_site.py'), '--preview',
                        '--output', cls.site.name], check=True, capture_output=True, text=True)
        cls.questions = json.loads((ROOT/'data/questions.json').read_text())

    def test_each_subject_is_one_newest_first_page_with_every_question(self):
        for subject in {subject_of(q) for q in self.questions}:
            with self.subTest(subject=subject):
                expected = Counter(q['question_id'] for q in self.questions if subject_of(q) == subject)
                html = (self.site/subject/'index.html').read_text()
                cards = ARTICLE.findall(html)
                self.assertEqual(Counter(c[0] for c in cards), expected)
                years = [int(c[1]) for c in cards]
                self.assertEqual(years, sorted(years, reverse=True))
                self.assertIn('class="year-jump"', html)
                self.assertNotIn(f'{subject}/page/2/', html)
                records = json.loads((self.site/subject/'index.json').read_text())
                self.assertEqual(Counter(r['id'] for r in records), expected)

    def test_topic_pages_are_single_and_complete(self):
        topics = json.loads((ROOT/'data/topics.json').read_text())
        subject = '08-operating-systems'
        for topic in topics[subject]['topics']:
            ids = [q for q, t in topics[subject]['assign'].items() if t == topic['id']]
            html = (self.site/subject/'topic'/topic['id']/'index.html').read_text()
            self.assertEqual(Counter(c[0] for c in ARTICLE.findall(html)), Counter(ids))

    def test_similar_pages_and_one_per_method_marks(self):
        subject = '08-operating-systems'
        srtf = next(g for g in json.loads((ROOT/'data/problem-patterns.json').read_text())['groups'] if g['id'] == 'srtf-schedule-metrics')
        page = (self.site/subject/'similar/srtf-schedule-metrics/index.html').read_text()
        cards = ARTICLE.findall(page)
        self.assertEqual(Counter(c[0] for c in cards), Counter(srtf['members']))
        self.assertEqual([int(c[1]) for c in cards], sorted((int(c[1]) for c in cards), reverse=True))
        self.assertIn('How these are solved', page)
        listing = (self.site/subject/'index.html').read_text()
        marks = {c[0]: 'data-alt="1"' in c[2] for c in ARTICLE.findall(listing) if c[0] in srtf['members']}
        self.assertEqual(sum(not alt for alt in marks.values()), 1)  # only the newest stays under "One per method"
        newest = cards[0][0]
        self.assertFalse(marks[newest])
        self.assertIn(f'similar/srtf-schedule-metrics/#{newest}', listing)
        self.assertIn('One per method', listing)

    def test_old_addresses_redirect_to_the_subject(self):
        subject = '08-operating-systems'
        for path in ('page/2', 'unique', 'patterns', 'patterns/page/3'):
            html = (self.site/subject/path/'index.html').read_text()
            self.assertRegex(html, r'http-equiv="refresh" content="0;url=[./]*' + subject + '/"')
        redirect = (self.site/'q/CS-2024-S2-Q37/index.html').read_text()
        self.assertIn(subject + '/#CS-2024-S2-Q37', redirect)


if __name__ == '__main__': unittest.main()
