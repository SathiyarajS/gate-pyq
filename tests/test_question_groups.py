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
                       lambda g:g['review']['sources'][0].update(sha256='missing'),
                       lambda g:g['review']['sources'][0].update(page=-1),
                       lambda g:g['review']['sources'][0].update(page=True),
                       lambda g:g['review'].update(reviewed_on='2026-99-99')]:
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

    def test_reviewed_repeat_requires_source_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'data').mkdir()
            (root/'data/repeats.json').write_text(json.dumps({'pairs':[
                dict(a='a',b='b',kind='same',status='reviewed')]}))
            with self.assertRaises(ValueError):site_features.load_repeats(root,questions())

    def test_other_topics_subject_is_normalized(self):
        self.assertEqual(question_groups.subject_of({'subject':'excluded'}),'13-other-topics')

    def test_source_review_removed_false_repeat_folds(self):
        qs=json.loads((ROOT/'data/questions.json').read_text())
        years={p['paper_id']:p['year'] for p in json.loads((ROOT/'data/papers.json').read_text())}
        for q in qs:q['year']=years[q['paper_id']]
        repeats=site_features.load_repeats(ROOT,qs)
        rejected=[p for p in json.loads((ROOT/'data/repeats.json').read_text())['pairs'] if p.get('status')=='rejected']
        self.assertGreaterEqual(len(rejected),9)
        for pair in rejected:
            self.assertNotIn(pair['b'],repeats.get(pair['a'],{}).get('group',[]))
        self.assertEqual(dict(repeats['CS-1992-Q20']['others'])['CS-1998-Q31'],'numbers')

    def test_repository_review_hashes_match_recorded_sources(self):
        crops=json.loads((ROOT/'data/crops.json').read_text())
        source_map=json.loads((ROOT/'audits/crop-source-map.json').read_text())['sources']
        reviews=[g['review'] for g in json.loads((ROOT/'data/problem-patterns.json').read_text())['groups']]
        reviews += [p['review'] for p in json.loads((ROOT/'data/repeats.json').read_text())['pairs']]
        for review in reviews:
            for source in review['sources']:
                known={c.get('source_sha256') or source_map[c['file']]['sha256'] for c in crops[source['question_id']] if c['file']==source['file']}
                self.assertLessEqual(source['page'],source_map[source['file']]['pages'])
                self.assertIn(source['sha256'],known,source['question_id'])

    def test_repository_patterns_valid(self):
        qs=json.loads((ROOT/'data/questions.json').read_text())
        self.assertTrue(question_groups.load_patterns(ROOT,qs))


if __name__=='__main__':unittest.main()
