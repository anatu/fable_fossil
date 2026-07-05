# Fable Fossil — Design

Built 2026-07-05 by Claude Fable 5 (claude-fable-5). Owner: natu.anand@gmail.com.

## Goal

Persist the transferable part of a strong model's reasoning so a weaker, cheaper
model can consult it at task time and close part of the capability gap.

## What can and cannot fossilize

Model capability splits roughly like human intelligence:

- **Fluid** — raw depth on novel problems, long-horizon coherence, taste. Lives in
  the weights. A file cannot transfer it. Any design pretending otherwise fails.
- **Crystallized** — procedures, decision templates, verification methods, known
  traps, the *form* of good reasoning. This transfers well through text, because
  the weak model only has to *follow and check*, not *invent*.

The fossil therefore stores five artifact types, in descending order of leverage:

1. **Verification catalogs** — checking an answer is easier than producing one
   (the generator–verifier gap). Shifting the weak model's effort from generation
   to independent verification is the single highest-value transfer.
2. **Traps** — enumerated failure modes with recognition signatures and
   countermeasures. Negative knowledge is cheap to store and weak models hit the
   same traps repeatedly (base-rate neglect, off-by-one, pattern-match
   substitution, dropped constraints).
3. **Procedures/playbooks** — step-by-step decision procedures per task family.
   They externalize working memory, which is exactly what weaker models lack.
4. **Templates** — recurring computations reduced to fill-in forms (Bayes by
   counts, bottleneck analysis, complement-of-collision).
5. **Exemplar traces** — full worked examples showing the *shape* of the
   reasoning. Few-shot form transfer beats abstract advice for weak models.

Plus one meta-artifact: **calibration rules** — explicit triggers for when the
weak model should stop and escalate rather than answer. A fossil that teaches a
weak model when not to trust itself is safer than one that only makes it bolder.

## Architecture

```
fable_fossil/
  CLAUDE.md                  # auto-loads for any Claude Code session here; routing hook
  FOSSIL.md                  # index + loading protocol (the only always-read file)
  DESIGN.md                  # this file
  protocols/
    core-loop.md             # universal 7-step reasoning loop
    verification.md          # independent-check catalog by answer type
    calibration.md           # confidence language + escalation triggers
  playbooks/                 # one per task family; load exactly one
    debugging.md
    quantitative.md
    logic-constraints.md
    code-review-edges.md
    software-design.md
  traps/
    failure-modes.md         # T1–T12 with signatures and countermeasures
  exemplars/                 # worked traces; load one when task FORM is unfamiliar
    trace-debugging.md
    trace-bayes.md
    trace-constraints.md
  eval/
    tasks.md                 # 10 benchmark tasks + ground truth + scoring rubric
    ground_truth.py          # script that verifies every ground truth
    README.md                # methodology, how to rerun
    results/                 # experiment results per date/model
```

## Design principles

1. **Selective retrieval.** The consumer reads FOSSIL.md, then loads ≤ ~4k tokens
   (core loop + one playbook + traps). Weak models degrade with long irrelevant
   context; loading everything would hurt.
2. **Verification-heavy.** Every playbook ends in an independent check that does
   not share the failure mode of the generation path.
3. **Exemplars carry form.** Traces are written to be copied structurally, not
   read as prose.
4. **Negative knowledge is first-class.** Traps are numbered and cross-referenced
   from playbooks.
5. **Calibration over confidence.** "Unsure, because X" is a valid fossil output;
   a fluent wrong answer is the worst one.
6. **Honest scope.** FOSSIL.md states what does not transfer. Consumers should
   not expect Fable-level performance on novel deep problems.
7. **Maintenance loop.** When a strong model runs a session, it appends new traps,
   templates, and traces, and re-runs `eval/` as a regression suite. The fossil
   is an accreting artifact, not a snapshot.

## Evidence plan

Two legs:

**Prior literature (from model knowledge, cutoff Jan 2026):**
- Chain-of-thought and zero-shot CoT prompting (Wei et al. 2022; Kojima et al.
  2022): explicit intermediate steps disproportionately help smaller models on
  multi-step problems.
- Distilling step-by-step (Hsieh et al. 2023) and related rationale-distillation
  work: rationales authored by a larger model improve smaller-model task
  performance beyond label-only supervision.
- Self-consistency and verify-then-answer results (Wang et al. 2022 onward):
  independent checking recovers errors generation alone does not.
- Checklist effects on expert error rates (medicine/aviation), mirrored in LLM
  structured-prompting results: externalized procedure reduces omission errors.
- The Claude Skills paradigm itself: procedural files measurably improve agent
  task completion. The fossil is that paradigm applied to reasoning rather than
  tool operation.

**Local controlled experiment (direct evidence, in `eval/`):**
- 10 tasks across 4 families (debugging ×3, quantitative ×4, logic ×2, test-case
  design ×1), all with script-verified ground truth, authored to be novel
  variants rather than memorized classics.
- 3 arms on the weaker model (Haiku 4.5): **A** task only; **B** task + generic
  "think step by step, double-check" (isolates fossil content from mere effort
  elicitation); **C** task + fossil material (core loop + matching playbook +
  traps), exactly as the routing table would load it.
- 2 independent runs per cell; 0–2 rubric points per task; author-graded against
  the verified ground truth.
- Threats to validity, acknowledged: small n; grader = task author = fossil
  author; tool use forbidden by instruction only; single weak model; exemplar
  traces excluded from arm C prompts to avoid answer leakage (so C tests the
  fossil *minus* its exemplar leg).

Results live in `eval/results/` and are summarized in FOSSIL.md.

**Findings (2026-07-05, Haiku 4.5, 123 runs):** three tiers were needed
because the first two hit ceiling — Haiku solved all 16 solvable tasks in all
arms (64/64 unaided), including hard variants authored to trip it. The fossil
caused no harm anywhere. Separation appeared only on the calibration tier:
given a correct function plus a fabricated bug report, control invented a
nonexistent bug in 3/5 final answers, generic step-by-step in 1/5 (+1 hedge),
and the fossil arm rejected the false premise in 5/5, citing trap T10. Small
n (Fisher p ≈ 0.08), but direction is consistent and the mechanism is visible
in the transcripts. Design consequence: for Haiku-class consumers, invest in
the calibration/traps legs and messy-domain playbooks rather than more
puzzle templates; the playbook/template legs remain the bet for genuinely
weaker consumers (untestable in this harness — Haiku is the weakest model
available to it).

## Usage

- Any Claude Code session started in this directory auto-loads CLAUDE.md, which
  points to FOSSIL.md.
- From other projects: reference the fossil in that project's CLAUDE.md
  ("For nontrivial reasoning tasks, consult /Users/natuanand/fable_fossil/FOSSIL.md
  and follow its loading protocol"), or symlink the directory in.
- Non-Claude models: any model that can read files can consume it; the files are
  plain markdown with no harness dependencies.

## Limitations / future work

- Coverage: five playbooks. Writing, research synthesis, and data analysis
  families are unwritten.
- Exemplar bank is thin (3 traces); the form-transfer leg is under-exploited.
- Eval should be re-run per new candidate weak model; effects will differ.
- No automated retrieval; routing is manual via the table. Fine at this size.
