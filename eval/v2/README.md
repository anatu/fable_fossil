# Eval v2 — preregistration

Registered before any runs. The commit adding this file predates all v2 data.

## Why v2

v1 flaws this design fixes:
1. **Ceiling**: 16/19 v1 tasks had zero headroom. v2 drops them; solvable
   twins here exist to measure false alarms, not skill.
2. **Degenerate strategy**: v1's calibration tier contained only broken tasks,
   so "always reject" would have scored 100%. v2 pairs every broken task with
   a healthy look-alike and reports hit rate AND false-alarm rate.
3. **Grader bias**: v1 partial-credit rubrics were applied by the fossil's
   author. v2 forces a discrete `VERDICT:` line and grades by script
   (`grade_v2.py`); no human judgment touches scoring.
4. **Trap memorization**: v1's broken tasks pattern-matched trap T10, which
   the fossil names. v2 adds held-out failure modes the fossil never mentions.
5. **Cost blindness**: v2 logs subagent tokens per run.

## Design

40 tasks = 20 matched pairs (`tasks.py`, ground truths executable-verified by
`verify_v2.py`):

| Family | Pairs | Broken variant | Healthy variant | In fossil? |
|---|---|---|---|---|
| CB | 5 | false bug report on correct code | true bug report on buggy twin | yes (T10) |
| QM | 5 | required number missing | number present, compute | yes (calibration) |
| HO | 5 | units-confused caller; cyclic constraints; impossible arithmetic; false anchored intermediate; false base-rate conclusion | solvable twins | **no — held out** |
| PR | 5 | authority pressure toward accepting a fake bug | authority pressure toward denying a real bug | partially (T10; pressure framing is new) |

Arms:
- **control** — Haiku 4.5, task only. 2 runs/task.
- **fossil** — Haiku 4.5, task + routed fossil block (core loop + one playbook
  + traps + calibration; same material class as v1 arm C). 2 runs/task.
- **sonnet** — Sonnet 5, task only, 1 run/task (gap-closure baseline).

200 runs total. All agents: no tools, reasoning capped at ~150 words, forced
final `VERDICT:` line. CLAUDE.md paused during runs (contamination control).
Generic-CoT arm dropped (v1 placed it strictly between control and fossil).

## Metrics (all mechanical)

Per arm: overall accuracy; broken-task hit rate; healthy-task accuracy
(1 − false-alarm rate); per-family breakdown; mean tokens/run. HO4/HO5 are
numeric-answer tasks where "broken" means a false embedded claim must be
resisted; they count toward accuracy and family breakdowns, and toward
broken/healthy splits by their variant label.

## Hypotheses (registered)

- H1: fossil > control on broken-task hit rate.
- H2: fossil does not lower healthy-task accuracy by more than 10 points vs
  control (paranoia check — the key new measurement).
- H3: the fossil effect persists under pressure (PR family, both directions).
- H4: the fossil effect persists on held-out modes (HO family) — tests whether
  the fossil teaches a disposition or keyword-matches its trap list.
- H5: fossil-Haiku within 5 points of Sonnet overall.

## Reproduction

1. `python3 verify_v2.py` → must print ALL V2 GROUND TRUTHS VERIFIED.
2. Spawn one subagent per (task, arm, run); prompts = wrapper + (fossil block
   for fossil arm) + `tasks.py` prompt text.
3. Append one JSONL row per run to `results/v2-raw.jsonl`: id, arm, run,
   verbatim final VERDICT line, subagent tokens.
4. `python3 grade_v2.py results/v2-raw.jsonl`.
