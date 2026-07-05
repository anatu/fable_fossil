# Verification catalog

Rule: the check must not share the failure mode of the generation path.
If you computed forward, verify backward. If you reasoned abstractly, verify on
a concrete instance.

## Numeric answers
- Recompute by a different route: complement, ratio, different operation order.
- Magnitude sanity: probability ∈ [0,1]; rate has units; compare to a known anchor.
- Extreme-case probe: push one input to 0 or ∞ — does the formula still behave?
- Prefer counts over percentages (population of 10,000) — errors become visible.

## Code / bug answers
- Hand-trace ONE concrete input line by line, tracking each variable in a table.
  Read what the code DOES, not what its names suggest.
- Boundary sweep: empty, one element, two equal, all equal, negative, max/min,
  duplicates, already-seen value.
- Every loop: run the first and last iteration explicitly. Can the loop variable
  fail to advance? (infinite loop). Every `<` vs `<=`: test the equality case.
- State lifetime: what persists across calls? Defaults, module globals,
  closures, caches, shallow copies.
- After proposing a fix: re-run the nominal case against the fix too.

## Logic / constraint answers
- Verify the candidate against EVERY constraint individually; tick each off.
- Uniqueness: try to construct a second solution. If you cannot rule out all
  alternatives by argument, enumerate the remaining space explicitly.

## Claims / facts
- Separate what a source states from what you inferred. Mark inferences as such.
- If a claim is load-bearing and unverifiable here, say so.
