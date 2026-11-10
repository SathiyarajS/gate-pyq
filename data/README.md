# Audit records

`papers.json` is a provisional paper/session inventory, not evidence of source completeness. Source-index links are discovery starting points, not paper or key citations. Null counts and URLs mean unverified, not absent. Do not invent final-key provenance for historical papers.

`questions.json` contains one record per original numbered item. Required fields: `question_id`, `paper_id`, `source_question_number`, `subject`, `question_text`, `source_page`, `solution`, `derived_answer`, `official_answer`, `verification_status`, `discrepancy_ids`. For an out-of-scope item use subject `excluded` and a nonempty `exclusion_reason`; retain the question identifier so paper totals still reconcile. For included items use the exact subject directory name. Store figures and code faithfully and cite source pages. Compound historical questions need an explicit numbering convention and count reconciliation before marking the paper verified.

Verification states: `pending`, `independently_solved`, `official_key_matched`, `reviewed`, `discrepancy_open`. `reviewed` requires independent mathematical checking and a comparison to the final official key. If an official key is unavailable, keep that limitation visible rather than using `reviewed`. A program cannot certify a solution's mathematical correctness.

Before release: verify the inventory, locate original papers and final keys, reconcile every question number, check subject classification, independently derive solutions, review figures and options, compare exact accepted answers/ranges, and resolve or explicitly disclose discrepancies. All papers currently remain pending.
