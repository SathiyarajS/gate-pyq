# Import and review a new GATE CS year

Run **Prepare a new GATE CS year** from Actions on `main` once the organizing institute publishes the question papers and final answer keys. Enter the next year after the latest year in `data/papers.json` and one official HTTPS paper/key pair per set, for example:

```json
[
  {"set": 1, "paper_url": "https://example.ac.in/paper-cs1.pdf", "key_url": "https://example.ac.in/final-key-cs1.pdf"},
  {"set": 2, "paper_url": "https://example.ac.in/paper-cs2.pdf", "key_url": "https://example.ac.in/final-key-cs2.pdf"}
]
```

Use set 1 for a single paper. The importer supports the modern digital format with continuous question numbering and a text-extractable key table. It saves both PDFs under `sources/web/<host>/<path>`, as for earlier years, and records their paths and hashes, physical pages, exam sessions, marks, types, and key text. A mismatched numbering scheme, missing rows, or unsupported key format stops the import for investigation. Source and final-key provenance still require independent verification.

The workflow pushes `import/gate-cs-<year>` and opens a draft PR targeting `main`. Its files under `data/imports/<year>/` are review inputs. The site only reads the canonical inventory and question records.

The workflow uses the repository token to push the branch. For draft PR creation, enable **Allow GitHub Actions to create and approve pull requests** under **Settings → Actions → General**, or configure the repository secret `GATE_IMPORT_PR_TOKEN` with a token that can create pull requests in this repository. If the branch was pushed but PR creation failed, open a draft PR from that branch. If a workflow-created PR has no Pages check, dispatch **Build and deploy site** on the PR branch for a build and browser check. A branch dispatch cannot deploy.

## Instructions for Codex on the draft PR

1. Read `AGENTS.md`, `HANDOFF.md` and `data/README.md`. Verify each official PDF and its recorded SHA-256, the final-key designation, session completeness, and the printed numbering, marks, types, option order, and key ranges. Inspect the full source pages for diagrams, tables, and questions continuing onto another page. Record any unresolved discrepancies.
2. Classify each question by subject and topic. Write an accurate, self-contained paraphrase and a worked solution from the paper before comparing the result with the official key. Preserve the official key and document differences. Keep the corresponding subject notes and source records in sync. Use official page links where a source crop has yet to be registered under the repository’s crop rules.
3. Add step-throughs where all simulator inputs are explicit in the question and the computed result matches the keyed answer content. Reuse the existing animation family, renderer, controls, and styling when applicable. Add focused worked-example tests and check representative players at 390×900 in Chromium. See HANDOFF §3.6 and §3.7 for the animation contract and exclusions.
4. Use a fresh Codex session to independently verify the source, solutions and animation inputs/results. If adding exact redrawn text or figures, follow the separate transcription and screenshot review in HANDOFF §3.3. Mark checks as passed only when they were performed.
5. Move reviewed records into `data/papers.json` and `data/questions.json` in repository format. Refresh coverage and checklist, run `python scripts/validate.py`, full pytest, `node tests/test_transcription_math.js`, the release build, and the Chromium study-view checks. Confirm the new year appears on the home page, paper and subject views, search filters, and heatmap. Summarize per-session counts, key and source status, and animation coverage in the PR. Merging the reviewed PR into `main` triggers the public deployment.
