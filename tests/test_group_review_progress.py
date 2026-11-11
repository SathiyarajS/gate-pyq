import sys
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from group_review_progress import progress


class FullCorpusProgressTest(unittest.TestCase):
    def setUp(self):
        self.questions=[{'question_id':'a','subject':'s'}, {'question_id':'b','subject':'s'},
                        {'question_id':'c','subject':'excluded'}]
        self.record={'question_id':'a','source_status':'reviewed','grouping_status':'no_reviewed_match',
                     'source_evidence':[{'file':'source.pdf','page':1,'sha256':'a'*64}],
                     'fingerprint':{'procedure':'A specific method'},'notes':'No accepted counterpart found, not proof of uniqueness.'}

    def test_prior_candidate_evidence_is_not_full_corpus_completion(self):
        result=progress(self.questions,[],['a','b'])
        self.assertEqual(result['total'],3)
        self.assertEqual(result['complete'],0)
        self.assertEqual(len(result['records']),3)
        self.assertEqual(result['records'][2]['subject'],'13-other-topics')

    def test_partial_report_cannot_drop_pending_questions(self):
        result=progress(self.questions,[{'subject':'s','records':[self.record],'independent_group_review':{'status':'passed'}}])
        self.assertEqual(result['complete'],1)
        self.assertEqual(result['source_reviewed'],1)
        self.assertEqual([r['question_id'] for r in result['records']],['a','b','c'])
        self.assertEqual(result['records'][1]['source_status'],'pending')

    def test_primary_review_alone_is_not_complete(self):
        result=progress(self.questions,[{'records':[self.record]}])
        self.assertEqual(result['complete'],0)
        self.assertEqual(result['source_reviewed'],1)

    def test_invalid_review_is_rejected(self):
        for change in [{'question_id':'unknown'},{'source_evidence':[]},{'fingerprint':{}},
                       {'source_status':'verified'},{'grouping_status':'unique'}]:
            record=dict(self.record,**change)
            with self.assertRaises(ValueError):progress(self.questions,[{'records':[record]}])
        with self.assertRaises(ValueError):progress(self.questions,[{'records':[self.record,self.record]}])

    def test_blockers_and_ambiguity_are_not_hidden(self):
        blocked=dict(self.record,source_status='blocked',grouping_status='ambiguous',notes='Essential figure illegible.')
        result=progress(self.questions,[{'records':[blocked]}])
        self.assertEqual(result['complete'],0)
        self.assertEqual(result['source_blocked'],1)
        self.assertIn('illegible',result['records'][0]['notes'])


if __name__=='__main__':unittest.main()
