# FABLE FOSSIL — index

Distilled from Claude Fable 5 (claude-fable-5), 2026-07-05. Design rationale: DESIGN.md.

## Scope — read this first

- This transfers **crystallized** skill: procedures, verification methods, known
  traps, computation templates, and the form of good reasoning traces.
- It does **not** transfer raw capability. On novel, deep problems you will still
  be out of your depth — the fossil's job there is to make you *notice* that
  (protocols/calibration.md) rather than produce a fluent wrong answer.

## Loading protocol

1. Classify the task with the routing table.
2. Load `protocols/core-loop.md` + the ONE matching playbook + `traps/failure-modes.md`.
3. If the task's FORM is unfamiliar, also load the matching exemplar trace and
   copy its structure.
4. Budget: ≤ ~4k tokens of fossil material in context. Never load everything.
5. Before finalizing any answer, run `protocols/calibration.md`.

## Routing table

| Task looks like | Load |
|---|---|
| find/fix a bug, "why is this wrong", trace behavior | playbooks/debugging.md (+ exemplars/trace-debugging.md) |
| probability, rates, capacity, estimation, "give a number" | playbooks/quantitative.md (+ exemplars/trace-bayes.md) |
| puzzle, scheduling, constraints, who-lies | playbooks/logic-constraints.md (+ exemplars/trace-constraints.md) |
| review code, design test cases, edge-case hunting | playbooks/code-review-edges.md |
| architecture / design decision | playbooks/software-design.md |
| anything else nontrivial | protocols/core-loop.md + traps/failure-modes.md only |

## Maintenance protocol (for strong models)

When a strong model runs a session here:
- Append newly observed weak-model failures to traps/failure-modes.md (signature
  + countermeasure, keep numbering).
- Add playbooks for uncovered task families; add exemplar traces (one per family
  minimum).
- Re-run the regression suite: see eval/README.md. Do not weaken ground truths.
- Keep every file small. If a playbook exceeds ~150 lines, split it.

## Evidence

Controlled experiment (2026-07-05, 123 runs, Haiku 4.5, 3 arms): full method
in eval/README.md, results in eval/results/2026-07-05-haiku.md.

- No harm: fossil arm ≥ control in every cell.
- On solvable self-contained tasks (debugging, probability, logic, test
  design — including deliberately trap-laden ones), Haiku 4.5 scored 64/64
  WITHOUT the fossil. Do not expect accuracy gains there for Haiku-class
  consumers.
- Measured value concentrates in **calibration**: on a false-premise bug
  report, control fabricated a bug in 3/5 runs; the fossil arm rejected the
  premise in 5/5, citing trap T10. Protocols/calibration.md and
  traps/failure-modes.md are the highest-leverage files for strong-ish weak
  models; playbooks/templates matter more the weaker the consumer.
- Gap-closure: Sonnet 5 and Fable 5 baselines (no fossil) scored 18/18 on the
  calibration tier. Haiku+fossil also scored 18/18 vs plain Haiku's 12/18 —
  the fossil closed the full measured gap to the strong models on this suite.
  The unmeasured residual gap (long-horizon agentic work, ambiguity, domain
  knowledge) is where strong models should still be preferred.
