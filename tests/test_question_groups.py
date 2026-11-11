import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import question_groups
import site_features


def questions():
    return [dict(question_id=qid, subject='s', year=year, paper_id='P'+qid,
                 source_question_number='1') for qid, year in [('a',2000),('b',2020),('c',2010)]]


def pattern():
    return dict(id='pattern', title='A method', subject='s', status='reviewed',
                representative='a', members=['a','b'], rationale='Same reasoning, different metric.',
                review=dict(method='source-page-comparison', reviewer='reviewer', reviewed_on='2026-11-11',
                            sources=[dict(question_id=qid,file='source.pdf',page=1,sha256='a'*64,
                                          notes='Constraints and requested metric checked.') for qid in ['a','b']]))


class StudyGroupsTest(unittest.TestCase):
    def load(self, group):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'data').mkdir()
            (root/'data/problem-patterns.json').write_text(json.dumps({'groups':[group]}))
            return question_groups.load_patterns(root, questions())

    def test_reviewed_pattern_retains_all_variants_and_ungrouped(self):
        units=question_groups.study_units(questions(), self.load(pattern()), lambda q:-q['year'])
        self.assertEqual(len(units),2)
        ids=[q['question_id'] for u in units for q in [u['representative']]+u['alternatives']]
        self.assertCountEqual(ids,['a','b','c'])
        self.assertEqual(next(u for u in units if u['group'])['representative']['question_id'],'a')

    def test_candidate_or_rejected_never_folds_even_identical_text(self):
        for status in ['candidate','rejected']:
            g=pattern();g['status']=status;g.pop('review')
            units=question_groups.study_units(questions(),self.load(g),lambda q:-q['year'])
            self.assertEqual(len(units),3)
            self.assertTrue(all(not u['alternatives'] for u in units))

    def test_review_requires_all_source_evidence(self):
        for mutate in [lambda g:g.pop('review'), lambda g:g['review']['sources'].pop(),
                       lambda g:g['review'].update(method='text-similarity'),
                       lambda g:g['review']['sources'][0].update(sha256='missing')]:
            g=pattern();mutate(g)
            with self.assertRaises(ValueError):self.load(g)

    def test_invalid_members_and_subject_rejected(self):
        for change in [dict(members=['a','a']),dict(members=['a','unknown']),dict(subject='other'),
                       dict(representative='c'),dict(status='automatic')]:
            g=pattern();g.update(change)
            with self.assertRaises(ValueError):self.load(g)

    def test_overlap_does_not_silently_drop_questions(self):
        with self.assertRaises(ValueError):
            question_groups.study_units(questions(),[pattern(),pattern()],lambda q:-q['year'])

    def test_cross_subject_repeat_only_retains_local_members(self):
        units=question_groups.study_units(questions(),[dict(members=['a','elsewhere'])],lambda q:-q['year'])
        self.assertEqual(len(units),3)
        self.assertTrue(all(not u['alternatives'] for u in units))

    def test_repeat_candidate_cannot_bridge_reviewed_groups(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'data').mkdir()
            (root/'data/repeats.json').write_text(json.dumps({'pairs':[
                dict(a='a',b='b',kind='same'),dict(a='b',b='c',kind='numbers',status='candidate')]}))
            repeats=site_features.load_repeats(root,questions())
            self.assertNotIn('c',repeats)
            self.assertEqual(set(repeats['a']['group']),{'a','b'})

    def test_repository_patterns_valid(self):
        qs=json.loads((ROOT/'data/questions.json').read_text())
        self.assertTrue(question_groups.load_patterns(ROOT,qs))


if __name__=='__main__':unittest.main()
