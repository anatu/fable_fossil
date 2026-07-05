# Playbook: debugging / bug-finding

Goal: find what the code DOES wrong — not what looks untidy.

## Procedure
1. **Contract first.** Read docstring/spec/caller expectations. Write the
   contract as invariants before reading the body.
2. **Read as-executed.** Ignore names; track types and values. (Trap T7)
3. **Trace three concrete inputs by hand**, variables in a table:
   nominal · boundary (empty / one element / equal values) · hostile
   (duplicates, negatives, containment, huge). (Traps T4, T9)
4. **Loop audit.** For every loop: first iteration, last iteration, termination.
   Can the update fail to advance the loop variable? → infinite loop. (T4)
5. **State lifetime.** Mutable defaults, module globals, closures, caches,
   shallow vs deep copies — what leaks across calls? Who else holds a reference?
   (T8)
6. **Concurrency/async.** Any check-then-act window? Any await inside a
   non-awaiting iteration?
7. **Report:** the bug, its mechanism, ONE concrete trigger input, expected vs
   actual output.

## Bug taxonomy (sweep in this order — ordered by frequency)
- boundaries: off-by-one, empty, single element, equal elements
- aliasing / shared mutable state / shallow copy of nested structure
- wrong comparison: `<` vs `<=`, `is` vs `==`, string vs number
- loop termination / non-advancing update
- overwrite instead of merge (assignment where max/min/accumulate needed)
- swallowed error paths
- units, encoding, timezone
- async ordering / races

## Verification
Run the trigger input through your FIXED version mentally. Then re-run the
nominal case against the fix — a fix that breaks the happy path is not a fix.
Multiple bugs are common: finding one does not end the sweep.
