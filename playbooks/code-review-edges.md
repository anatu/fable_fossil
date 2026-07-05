# Playbook: code review & test-case design

## Spec-diff method
1. Write the spec as invariants: input domain, output contract, error behavior.
2. Diff the implementation (or proposed tests) against each invariant, one by one.
3. Anything the spec says that no test exercises is a hole. Anything the code
   does that the spec doesn't mention is a question.

## Edge-case master list
Walk this list against the spec; name every applicable case, skip none silently:
- empty input; single element; exactly two elements
- all elements equal; duplicates of the extreme value; ties just below the extreme
- negative, zero, max-size values; mixed sign
- unsorted / reverse-sorted input when order could matter
- empty string, whitespace, unicode (for text)
- the boundary of every explicit conditional in the spec: n−1, n, n+1
- specified error behavior: does invalid input raise/return exactly what the
  spec says? (error paths are part of the contract)
- state carried between calls; concurrent callers (T8, T9)

## For "list the test cases" tasks
Enumerate by walking the master list against the spec. The score is coverage of
the failure-prone cases (all-equal, duplicate-max, empty), not the count of
happy-path variations.
