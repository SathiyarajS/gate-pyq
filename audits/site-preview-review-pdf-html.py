#!/usr/bin/env python3
"""Verify print HTML structure; does not render or validate PDF files."""
import importlib.util,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('pdf',ROOT/'scripts/build_pdfs.py')
pdf=importlib.util.module_from_spec(spec);spec.loader.exec_module(pdf)
count=0
for subject in json.loads((ROOT/'_site/build-report.json').read_text())['subject_counts']:
 records=json.loads((ROOT/'_site'/subject/'index.json').read_text())
 question_only=pdf.document(subject,records,True)
 assert 'class="answer"' not in question_only
 assert '<h3>Detailed solution</h3>' not in question_only
 assert len(re.findall('<li>',question_only))==len(records)
 assert pdf.document(subject,records,False).count('<h3>Detailed solution</h3>')==len(records)
 count+=len(records)
print(f'13 subjects / {count} entries: questions-only removal, answer-index counts and full solutions pass. Actual PDF rendering NOT tested.')
