# fable_fossil

A reasoning fossil: procedures, verification methods, failure-mode traps, and
worked traces distilled from Claude Fable 5, for weaker models to consult at
task time. Built 2026-07-05.

- **FOSSIL.md** — index and routing table. Start here.
- **DESIGN.md** — what transfers and what doesn't, architecture, evidence.
- **protocols/ · playbooks/ · traps/ · exemplars/** — the fossil content.
- **eval/** — 141-run benchmark (19 tasks, script-verified ground truth) used
  as a regression suite. Results: `eval/results/2026-07-05-haiku.md`.

Measured result: Haiku 4.5 needs no help on solvable self-contained reasoning
tasks (64/64 unaided), but the fossil's calibration leg took it from 12/18 to
18/18 on false-premise/missing-input tasks — matching no-fossil Sonnet 5 and
Fable 5 baselines exactly. The fossil's proven value is discipline at the
boundaries, not raw problem-solving.

Any Claude Code session in this directory auto-loads CLAUDE.md and routes
through FOSSIL.md. From other projects, reference
`/Users/natuanand/fable_fossil/FOSSIL.md` in that project's CLAUDE.md.
