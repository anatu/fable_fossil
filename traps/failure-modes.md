# Known failure modes (traps)

Distilled from observed weaker-model errors. Scan the ones matching your task
family before answering. Format: signature → countermeasure.

**T1 PATTERN-MATCH SUBSTITUTION** — you answer the classic textbook version, not
the variant actually asked. Signature: the problem "feels familiar".
→ Quote the exact numbers/conditions back; list the differences from the
classic; solve THIS one.

**T2 BASE-RATE NEGLECT** — posterior driven by test accuracy, ignoring
prevalence. Signature: answer near the sensitivity number.
→ Use counts on a population of 10,000; the base rate enters at step 1.

**T3 DROPPED CONSTRAINT** — one requirement silently disappears mid-solution
(especially indirect/derived load, self-referential clauses, "not first/last").
→ Number constraints at the start; tick every one against the final answer.

**T4 OFF-BY-ONE / BOUNDARY BLINDNESS** — `<` vs `<=`, first/last iteration,
empty input. → Explicitly run the equality case, the first iteration, the last
iteration, and the empty input.

**T5 PREMATURE CLOSURE** — first plausible answer accepted, verification
skipped. → Core-loop step 6 is mandatory; verify by an independent method.

**T6 MENTAL ARITHMETIC CHAINS** — multi-op arithmetic done in one breath.
→ One operation per written line. Prefer integer counts to decimals.

**T7 NAME TRUST** — believing what a function/variable name says over what the
code does. → Read as-executed; trace values, ignore names.

**T8 SHARED STATE / ALIASING** — mutable defaults, module globals, caches,
shallow copies of nested structures. → Ask "what persists across calls?" and
"who else holds a reference to this object?"

**T9 HAPPY-PATH ONLY** — empty input, error branches, concurrent interleavings
unexamined. → Boundary sweep + "what if two callers interleave here?"

**T10 FALSE PREMISE SWALLOWED** — the question asserts something untrue and the
answer inherits it. Signature: the answer feels forced. → Check the premise.

**T11 UNIT & CALENDAR ASSUMPTIONS** — seconds vs ms, timezones, DST, months ≠
30 days, leap years. → Carry units through every line.

**T12 PARAPHRASE DRIFT** — your restatement of the task quietly changes it.
→ Re-read the ORIGINAL wording once, immediately before finalizing.
