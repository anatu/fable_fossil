# I "fossilized" a frontier model's reasoning for a small model. The only thing that transferred was knowing when not to answer.

Setup: I had a frontier model (Claude Fable 5) write a "reasoning fossil" — a
small repo of markdown files meant to let a cheaper model (Haiku 4.5) borrow
its thought process: a 7-step reasoning loop, per-domain playbooks (debugging,
probability, constraint puzzles), 12 enumerated failure-mode traps, worked
traces, and calibration rules ("never fabricate; 'unsure, because X' is a
valid answer").

Then I tested it properly: 141 runs, 19 tasks with script-verified ground
truth, arms for Haiku alone, Haiku + generic "think step by step", Haiku +
fossil, and no-fossil Sonnet 5 / Fable 5 baselines.

Results:

1. **On every solvable task, plain Haiku scored 100%.** Multi-bug hunts,
   Mossel-style conditioned dice, a 4-door Monty variant, mixed-evidence
   Bayes, 5-person knights-and-knaves — tasks authored specifically to trip
   it. 64/64 unaided. The fossil added nothing because there was nothing to
   add. Small models are past needing reasoning templates for self-contained
   problems.
2. **The gap showed up somewhere else: broken questions.** Given a *correct*
   function plus a fake bug report ("this returns wrong results for negative
   x — find the bug and fix it"), plain Haiku invented a nonexistent bug in
   3 of 5 runs — it would trace the code, conclude it was fine, then fabricate
   a hypothetical "actual implementation" and report that as the bug.
3. **The fossil fixed exactly that.** With the traps + calibration files in
   context, Haiku rejected the false premise 5/5 times, explicitly citing the
   trap ("a bug report is a claim, not a fact — reproduce it before explaining
   it"). Score went 12/18 → 18/18 on the broken-task tier — identical to the
   Sonnet and Fable no-fossil baselines.

Takeaway: you can't transfer fluid intelligence through a markdown file, and
for modern small models you don't need to. What transfers is discipline at
the boundaries — premise checking, refusing to invent missing inputs,
treating "this doesn't reproduce" as a first-class answer. If you're writing
skills/CLAUDE.md files to make a cheap model behave like an expensive one,
spend the tokens on failure modes and refusal rules, not on how-to-reason
templates.

Caveats: small n (2–5 per cell), tasks and grades by the same model that
wrote the fossil, and the suite doesn't touch long-horizon agentic work —
which is presumably where the real weak/strong gap now lives.
