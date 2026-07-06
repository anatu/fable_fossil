# I "fossilized" a frontier model's reasoning for a small model, then spent 341 eval runs finding out what actually transferred

Setup: I had a frontier model (Claude Fable 5) write a "reasoning fossil" — a
small repo of markdown files meant to let a cheaper model (Haiku 4.5) borrow
its thought process: a 7-step reasoning loop, per-domain playbooks, 12
enumerated failure-mode traps, worked traces, and calibration rules ("never
fabricate; 'cannot be determined' is a valid answer").

Then I benchmarked it twice, because the first eval had a flaw worth sharing.

**Eval v1** (141 runs, 3 arms + Sonnet/Fable baselines): on every *solvable*
task — multi-bug hunts, conditioned-probability traps, Monty Hall variants,
knights-and-knaves — plain Haiku scored 100% unaided. Zero headroom. The only
separation came from broken tasks (fake bug reports on correct code): plain
Haiku fabricated a nonexistent bug in 3/5 runs; fossil-Haiku rejected the
premise 5/5, matching Sonnet and Fable exactly. But v1 had a hole: every
calibration task was broken, so a model that just rejects *everything* would
have scored perfectly, and I never measured false alarms.

**Eval v2** fixed that (200 runs, preregistered before any data, 20
broken/healthy task pairs, forced verdict lines, 100% script-graded — no
human judgment in scoring):

| | Plain Haiku | Fossil-Haiku | Sonnet |
|---|---|---|---|
| Overall | 94% | **100%** | 100% |
| Broken-task hit rate | 88% | **100%** | 100% |
| False alarms on healthy twins | 0 | **0** | 0 |
| Tokens/run | 13.8k | 15.6k | 25.7k |

Three things I didn't expect:

1. **Prompt framing was half of v1's effect.** When the verdict menu
   explicitly legitimized "NO-BUG" as an answer, plain Haiku stopped
   fabricating on ordinary fake bug reports (10/10, vs 2/5 under v1's
   presupposing "identify the bug and fix it" framing). A lot of weak-model
   "sycophancy" is really the prompt refusing to offer an exit.
2. **What still breaks the unaided model is social pressure and false
   anchors.** Its only v2 failures: "our staff engineer already confirmed
   this bug — don't relitigate" (sided with the authority against the
   docstring, twice), and "a colleague computed the posterior is 96%"
   (updated from the wrong anchor instead of recomputing, twice). The
   fossil's calibration language — "a bug report is a claim, not a fact;
   authority changes nothing about the evidence" — fixed all of it, 40/40,
   with zero induced paranoia on the healthy twins.
3. **The result is strong-model parity at a discount.** Fossil-Haiku matched
   Sonnet exactly on this benchmark at 61% of its per-run token cost, paying
   a 13% overhead over plain Haiku.

Takeaway for anyone writing skills / system prompts / CLAUDE.md files for
cheap models: reasoning templates for self-contained problems are dead
weight — modern small models don't need them. Spend the tokens on (a) verdict
menus that make "no" a legitimate answer, and (b) explicit
pressure-and-anchor resistance rules. That's where the measured value is.

Caveats, honestly: same author wrote the tasks, the fossil, and the grader
(grader is deterministic and public; ground truths are executable-verified);
one weak model; single-turn tasks only — long-horizon agentic work is the
untested axis. Repo with the full prereg, raw per-run logs, and grading
scripts: https://github.com/anatu/fable_fossil

