#!/usr/bin/env python3
"""Account for every corpus question during the systematic grouping review.

Candidate review is prior evidence, not completion of the full-corpus pass.
Subject reports are retained separately; this manifest never controls folding.
"""
import argparse
import collections
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE_STATUSES={'reviewed','blocked','pending'}
GROUPING_STATUSES={'reviewed_group','no_reviewed_match','ambiguous','pending'}


def progress(questions, reports, prior_reviewed=()):
    by_id={q['question_id']:q for q in questions}
    if len(by_id)!=len(questions):raise ValueError('Duplicate corpus question ID')
    prior=set(prior_reviewed)
    records={qid:dict(question_id=qid,subject='13-other-topics' if q['subject']=='excluded' else q['subject'],
                      source_status='pending',grouping_status='pending',prior_source_reviewed=qid in prior,independent_group_review='pending')
             for qid,q in by_id.items()}
    seen=set()
    for report in reports:
        entries=report.get('records',[])
        if isinstance(entries,dict):entries=[dict(v,question_id=k) for k,v in entries.items()]
        for entry in entries:
            qid=entry['question_id']
            if qid not in records or qid in seen:raise ValueError('Unknown or duplicate review ID: '+qid)
            seen.add(qid)
            if report.get('subject') not in (None,records[qid]['subject']):raise ValueError('Wrong review subject: '+qid)
            source_status=entry.get('source_status','pending');grouping_status=entry.get('grouping_status','pending')
            if source_status not in SOURCE_STATUSES or grouping_status not in GROUPING_STATUSES:raise ValueError('Invalid review status: '+qid)
            if source_status=='reviewed' and not (entry.get('source_evidence') or entry.get('sources') or entry.get('evidence_refs')):
                raise ValueError('Reviewed source needs auditable evidence: '+qid)
            if grouping_status!='pending' and not entry.get('fingerprint'):
                raise ValueError('Grouping decision needs method fingerprint: '+qid)
            if source_status=='blocked' and not (entry.get('blocker') or entry.get('notes')):
                raise ValueError('Source blocker needs explanation: '+qid)
            records[qid].update(source_status=source_status,grouping_status=grouping_status,
                                report=report.get('report_path',''),notes=entry.get('notes',''),
                                independent_group_review=report.get('independent_group_review',{}).get('status','pending'))
    counts=collections.Counter(r['subject'] for r in records.values())
    completed=lambda r:r['source_status']=='reviewed' and r['grouping_status']!='pending' and r['independent_group_review']=='passed'
    subjects=[dict(subject=s,total=n,complete=sum(completed(r) for r in records.values() if r['subject']==s),
                   source_reviewed=sum(r['source_status']=='reviewed' for r in records.values() if r['subject']==s),
                   source_blocked=sum(r['source_status']=='blocked' for r in records.values() if r['subject']==s))
              for s,n in sorted(counts.items())]
    return dict(scope='Systematic full-corpus repeat and pattern review. Candidate-only source review is not full-corpus completion.',
                total=len(records),complete=sum(completed(r) for r in records.values()),
                source_reviewed=sum(r['source_status']=='reviewed' for r in records.values()),
                source_blocked=sum(r['source_status']=='blocked' for r in records.values()),
                subjects=subjects,records=[records[qid] for qid in sorted(records)],
                caveat='A completed question review can retain an ambiguous grouping decision. It is not a guarantee that every semantic relationship has been found. No uncertain match is folded automatically.')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--report-dir',type=Path,default=ROOT/'audits/grouping/full-corpus')
    ap.add_argument('--write',action='store_true')
    args=ap.parse_args()
    questions=json.loads((ROOT/'data/questions.json').read_text())
    prior=json.loads((ROOT/'audits/grouping/coverage.json').read_text())['source_reviewed_question_ids']
    reports=[]
    for path in sorted(args.report_dir.glob('*.json')):
        if path.name=='manifest.json':continue
        report=json.loads(path.read_text());report['report_path']=str(path.relative_to(ROOT));reports.append(report)
    result=progress(questions,reports,prior)
    if args.write:
        args.report_dir.mkdir(parents=True,exist_ok=True)
        (args.report_dir/'manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))


if __name__=='__main__':main()
