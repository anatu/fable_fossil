# Fable Fossil

This directory is a reasoning fossil: procedures, verification methods, traps,
and worked traces distilled from Claude Fable 5, for weaker models to consult.

For any nontrivial task in this session:

1. Read `FOSSIL.md` (the index).
2. Load ONLY what its routing table names for the task type (≤ ~4k tokens).
3. Follow `protocols/core-loop.md`. Do not skip the verification step.
4. Apply `protocols/calibration.md` before finalizing — escalate instead of
   guessing when a trigger fires.

Do not load the whole fossil at once. Do not edit `eval/tasks.md` ground truths
unless you are a strong model updating the benchmark deliberately.

When running eval subagents in this directory, temporarily rename this file
(`mv CLAUDE.md .claude-md.paused`) so control arms don't inherit fossil
pointers; restore it afterwards. Eval design rule: include both a weak-model
control arm (attributes the effect) and a strong-model no-fossil baseline
(measures gap closure).
