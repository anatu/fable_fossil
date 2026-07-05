# Fossil eval — methodology

Question: does fossil material measurably improve a weaker model's accuracy on
tasks it would otherwise get wrong — beyond what generic "think step by step"
prompting already buys?

## Setup
- Weak model: Haiku 4.5 (`claude-haiku-4-5`), spawned as subagents.
- Tasks: 10, in `tasks.md`. 4 families: debugging (T1–T3), quantitative
  (T4–T7), logic (T8–T9), test-case design (T10). All ground truths verified by
  `ground_truth.py`. Tasks are authored variants, not verbatim classics.
- Arms (identical task text; identical "no tools, plain text, end with
  FINAL ANSWER" wrapper):
  - **A — control:** task only.
  - **B — generic CoT:** + "think step by step carefully, double-check your
    work". Controls for effort elicitation.
  - **C — fossil:** + core-loop.md + the routing-table playbook for the task's
    family + failure-modes.md, verbatim. No exemplar traces (they could leak
    structurally similar content; C therefore under-tests the fossil).
- 2 independent runs per (task, arm) = 60 samples.
- Scoring: rubric in tasks.md, 0–2 per task, graded against verified ground
  truth.

## Threats to validity
- Small n (2 runs/cell); single weak model; grader = task author = fossil author.
- Tool use forbidden by instruction, not enforcement.
- Arm labels visible to the grader.
- Results generalize to *these task families*, not to open-ended work.

## Rerun protocol
1. `python3 ground_truth.py` — must print ALL GROUND TRUTHS VERIFIED.
2. Spawn the weak model once per (task, arm, run) with the wrappers above.
3. Grade against rubrics; write `results/<date>-<model>.md` with the per-cell
   table and honest caveats.
