# GATE CS Previous Year Questions (1991–2026)

**Website: https://sathiyarajs.github.io/gate-pyq/**

Every GATE Computer Science question from 1991 to 2026, all 3,406 of them from 46 papers, with answers and worked solutions. Free, no sign-up.

- **Organised for study.** 13 subjects, grouped by topic, 10 questions per page. Each question shows the original from the exam paper, with its year and paper in brackets.
- **Answers you open when ready.** A collapsible **Answer** shows the official key (or says none was found), a step-by-step solution, and any discrepancy between the key and the working.
- **Step-throughs.** Many questions have an animated walk-through of the solution: sorting, graphs, DP, recursion, automata, parsing, K-maps, pipelines, CPU and disk scheduling, paging, deadlock, subnetting, C traces and more.
- **Practice tools.** Search, filters (year, marks, type), A–D practice buttons, bookmarks and progress, full-paper mock tests with a timer, a topic-by-year chart and dark mode. It can be installed as an app.
- **PDFs.** Every subject has two downloads: one with answers and solutions, and one with questions only plus an answer index.

## Found a mistake?

Use **Report issue** under the question, or the site's **Feedback** page. Every discrepancy we know of is listed in [DISCREPANCIES.md](DISCREPANCIES.md) and shown next to its question.

## How it is built

- `data/questions.json` holds the questions, answers, official keys and solutions. Each question's crop box is in `data/crops.json`, and its rendered image is in `site-assets/q/`.
- `scripts/build_site.py` generates the static site, and `scripts/build_pdfs.py` the PDFs. Every push to `main` rebuilds and redeploys the site through GitHub Actions (`.github/workflows/pages.yml`).
- The source question papers are not stored here; only each paper's link and sha256 fingerprint are kept. See [sources/README.md](sources/README.md).
- **New exam years** are added in one agent run. See [Adding a new year](#adding-a-new-year).

To build locally:

```sh
python3.12 -m venv .venv && . .venv/bin/activate
pip install -r requirements-site.txt && python -m playwright install chromium && npm ci --ignore-scripts
python scripts/build_site.py --release
python -m http.server -d _site 8000          # open http://localhost:8000
```

## Adding a new year

When GATE publishes a new year's papers and final answer keys, run one command in this folder and leave it. It works with either Codex or Claude Code:

```sh
git pull
codex exec --full-auto -c sandbox_workspace_write.network_access=true "Read docs/NEW_YEAR_IMPORT.md and add the next GATE CS year to the site, start to finish, without asking me anything."
# or: claude -p "Read docs/NEW_YEAR_IMPORT.md and add the next GATE CS year to the site, start to finish, without asking me anything." --dangerously-skip-permissions
```

The agent:
1. finds the official papers and keys and checks them
2. cuts the question images
3. writes the solutions and step-throughs
4. has a separate session review everything
5. merges into `main`, which publishes the new year

The full procedure is in [docs/NEW_YEAR_IMPORT.md](docs/NEW_YEAR_IMPORT.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Coding agents start from [AGENTS.md](AGENTS.md) and [HANDOFF.md](HANDOFF.md), which hold the remaining work and the rules. Background notes (coverage, quality, review status, source access, history) are in [docs/](docs/).

## License

- **Code** (scripts, templates, site code): [MIT](LICENSE).
- **Our solutions, explanations, step-throughs and data** (everything we wrote): [CC BY-NC-SA 4.0](LICENSE-CONTENT.md). You may share and adapt them for non-commercial use, with credit and under the same license.
- **The GATE question papers themselves** (and the question images cropped from them) belong to their original setters, the IITs and IISc that organise GATE. This project claims no rights in them and they are not covered by either license. They are reproduced for students' study.
