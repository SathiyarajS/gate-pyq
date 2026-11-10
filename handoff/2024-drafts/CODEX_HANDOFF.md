# Continue the GATE question project

Repository: https://github.com/SathiyarajS/gate-pyq
Working branch: site. Last verified remote head: 76eea72209c75ea5cd23ae05a0cef73cd6971e99.

Please complete the remaining question work following CODEX_INSTRUCTIONS.md and the repository's applicable instructions. Read docs/TRANSCRIPTIONS.md, docs/MANUAL_VISUAL_REVIEW.md, PRIVATE_SITE.md, audits/crop-review-completion.json, audits/topics-review.md and the per-paper draft audits before changing anything.

## Scope and permission

Keep all work on site. Push meaningful reviewed batches, using one paper per transcription commit and the repository's requested commit message. Do not change repository visibility, permissions, Pages settings, main, or deploy publicly. Do not overwrite unrelated work or force-push. Respect your environment's access restrictions. The user will manually validate visual rendering; never assume that review has happened.

## Verified state

- 3,406 questions across 46 papers. All questions remain in scope, including the 238 excluded-subject records retained under Other Topics.
- Crop review is complete: 3,406 questions, 4,351 reviewed parts, zero pending crop boundaries. This does not mean transcription, browser/PDF validation or official-original fidelity is complete.
- Topic assignment audit says all 3,406 individually reviewed, zero candidates. Some older prose may still describe earlier pending gates.
- Remote site contains 195 source-reviewed draft transcriptions: CS-2026-S2, CS-2026-S1 and CS-2025-S1, 65 each. All remain status draft; zero verified redraws.
- Transcription infrastructure is present, independently reviewed and covered by 31 Python tests plus KaTeX checks. Verified display requires separate reviewer metadata, solution checking and rendered_comparison_checked. Drafts retain crop/paraphrase fallback. Do not manufacture approval metadata.
- No exact-head CI runs/statuses were present at the verified checkpoint. Empty CI is not a pass. No browser or finished-PDF visual acceptance has been claimed.

## Preserve the attached unpushed work

The handoff bundle contains:

1. pending-site-changes/: a complete frozen CS-2025-S2 checkpoint, 14 files. Its 65 drafts and eight SVGs have independent source/figure review. All remain draft. Q12 option D is e−1, not e^(−1); question and solution are corrected, answer A unchanged. Apply these files only after checking current site still includes the stated baseline. data/questions.json differs from the baseline only at CS-2025-S2-Q12; verify before replacing the large file. Commit as `transcribe: CS-2025-S2 (0/65 verified)`.
2. drafts/: 130 further draft questions for CS-2024-S1 and CS-2024-S2, split into first/second halves, with editable figure sources. These are NOT ready to mark verified or blindly copy over repository figures. Rename generic generator filenames uniquely when integrating, adjust only their output paths, and prove their regenerated SVG bytes/content match the reviewed artifacts.
3. review-fixes/: exact source/formatting corrections and proposed solution/discrepancy patches for the 2024 drafts. These proposals are not all applied.
4. BUNDLE_MANIFEST.json: hashes of the preserved files. Original PDFs, crop assets, dependencies and large raster evidence are not included.

Already-dispatched GitHub object uploads may have left unreferenced blobs. They are not commits or branch updates. Re-read the branch before any write; do not infer a push from an uploaded blob.

## 2024 draft readiness and fixes

CS-2024-S1 Q1–35: independent source/figure review complete. Four SVGs reviewed. Restore listed emphasis in Q22, Q30, Q34. Q18/Q19 source uses typographic C quotes; retain [sic] and add narrowly framed intended-ASCII solution qualifications/discrepancy entries without changing answers.

CS-2024-S1 Q36–65: independent source/figure review complete, two SVGs reviewed. Q42 prints the conflicting n≥1 recursive boundary and n=1 base case. Preserve [sic] and qualified solution; reclassify its existing BASE-CASE discrepancy as question-error rather than duplicate it. Minor emphasis recommendations are preserved separately.

CS-2024-S2 Q1–35: independent source/figure review complete, but fixes remain. Q33 options B/D need spaces before “will”; restore listed emphasis/paragraphs. Q2/Q29 grammar notes are supported. Q33 typography note must not falsely imply the function definition itself fails to compile. Q8's second pie-chart title clips in Inkscape but not MuPDF, so check production rendering. Q22 DFA topology is correct, but its SVG was hand-generated; regenerate through the pinned Graphviz DOT route required by CODEX instructions and review again.

CS-2024-S2 Q36–65: draft text and six SVGs are saved. Source pages were inspected and safe_svg passed, but actual SVG raster inspection and separate independent review were NOT completed before pause. Q36 needs a qualification for printed typographic quotes/en-dash subtraction. Treat these as unfinished drafts and inspect every figure.

## Next work

- Reconcile/apply the pending CS-2025-S2 checkpoint without losing other changes.
- Finish and independently review both 2024 papers, then continue newest-first from 2023 through 1991. There are 3,016 questions without any prepared draft beyond the preserved 390 drafted questions. Every draft still needs its required production visual acceptance.
- Use exact source wording/options/code, explicit source-typo notes, safe accessible vector figures, and shared contexts stored once. Check every existing solution against the exact source. Preserve uncertainty and official-key strings; do not invent source originals or keys.
- Keep per-paper provenance, hashes and separate review evidence. Use source files matching audits/crop-source-map.json. Downloaded/generated sources and images are not necessarily in a fresh clone. Restore exact listed PDFs/archive members, never change hashes to accept a different file. Do not run locate_crops.py merely to restore sources: it rewrites reviewed crop metadata.
- Run structural/unit/math tests and full preview checks. Review comparison pages for every question. The user will inspect responsive light/dark layouts, figures/math, interactions and PDFs; request precise per-question evidence and fix findings before setting verified status.
- Actual 26 PDFs, browser screenshots at360px/1280px, interactive QA, source/reuse uncertainty, and authorized publication/merge gates remain separate. Do not call the whole project complete while any required gate remains.

## Commands and practical notes

Use a normal writable clone. Python3.12 virtual environment: `python -m pip install -r requirements-site.txt`; Node20+: `npm ci --ignore-scripts`.

Run `python scripts/validate.py`, `python -m unittest discover -s tests`, `node tests/test_transcription_math.js`, `python scripts/compare_transcription.py PAPER_ID`, and private preview builds per the manual guide. No release build should silently bypass the fail-closed gate.

The prior workspace had no .git metadata; do not assume its paths exist on your computer. This bundle transfers source work, not environment state. If using GitHub APIs rather than a normal Git push, create per-file blobs then a SHA-only tree and compare-and-swap ref update; never force. data/questions.json is about15MB. Base64 exceeds a16MiB transport limit; UTF-8 succeeded. Verify remote commit, exact paths and hashes before reporting a push.

Report real blockers promptly and preserve unfinished work. Notify the user only when all requested questions and the required checks are genuinely done, or when their input is needed.
