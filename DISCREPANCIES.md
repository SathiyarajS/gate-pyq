# Discrepancy and interpretation log

This partial review does not establish that other questions are discrepancy-free. Original master-paper numbering applies.

| ID | Subject | Year/Set | Q# | Type | Summary | Official key | Derivation / interpretation | Status |
|----|---------|----------|----|------|---------|--------------|-----------------------------|--------|
| CS-2026-S1-Q28-LL1 | Compiler Design | 2026 CS1 | 28 | Overbroad statement / ambiguity | A literal claim that every LL(1) grammar must be syntactically left-factored has a nullable-prefix counterexample. | C | S→Aa\|Ab, A→ε is productive/reduced and LL(1), with a shared syntactic prefix A. See solution for FIRST/FOLLOW details. | Open; official scoring answer retained |
| CS-2026-S1-Q19-PROXY | Computer Networks | 2026 CS1 | 19 | Interpretation qualification | Direct browser-origin connections differ from browser-forward-proxy connections that can carry multiple origins. | A;C;D | Published answer follows direct-origin interpretation. | Explained; no key disagreement asserted |
| CS-2026-S1-Q44-IW | Computer Networks | 2026 CS1 | 44 | Missing assumption | Initial congestion window and exact starting time convention are not explicit. | B | The simplified one-segment initial window gives [10,11) ms; different initial windows give different rounds. | Open; official scoring answer retained |

Sources: [Official 2026 CS1 paper](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS1.pdf), pages 15, 21 and 33; [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf), page 1. The key's final/revised status has not been independently confirmed. The Q28 and Q44 issues are wording/assumption qualifications, not claims that the scoring key was changed.
