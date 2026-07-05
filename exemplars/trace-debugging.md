# Exemplar trace: debugging

Copy the STRUCTURE of this trace, not its content.

## Task
Find any bugs:

```python
def merge_intervals(intervals):
    """Merge overlapping [start, end] intervals. Input may be unsorted.
    Returns merged intervals sorted by start."""
    intervals.sort()
    out = [intervals[0]]
    for s, e in intervals[1:]:
        if s <= out[-1][1]:
            out[-1][1] = e
        else:
            out.append([s, e])
    return out
```

## Trace

1. RESTATE. Contract: merge overlapping intervals; unsorted input allowed;
   output sorted by start. Suspicious spots by taxonomy: the merge assignment,
   the empty-input case, the in-place sort.
2. INVENTORY. C1 overlaps merged. C2 result sorted. C3 unsorted input handled.
   C4 (implicit) edge inputs don't crash.
3. PLAN. Debugging playbook: trace nominal, boundary, hostile.
4. EXECUTE.
   - Nominal `[[1,3],[2,4]]`: sorted same. out=[[1,3]]. (2,4): 2≤3 →
     out[-1][1]=4 → `[[1,4]]`. ✓
   - Hostile — containment `[[1,10],[2,3]]`: out=[[1,10]]. (2,3): 2≤10 →
     out[-1][1]=**3** → `[[1,3]]`. ✗ Coverage of 4..10 lost. Mechanism:
     assignment overwrites the merged end instead of taking the max.
   - Boundary — `[]`: `intervals[0]` raises IndexError. ✗
   - Side effect: `intervals.sort()` mutates the caller's list. Worth flagging.
5. ANSWER. Bug 1: `out[-1][1] = e` must be `max(out[-1][1], e)`; trigger
   `[[1,10],[2,3]]` → returns `[[1,3]]`, expected `[[1,10]]`. Bug 2: empty input
   crashes; contract should return `[]`.
6. VERIFY. Fix vs nominal: max(3,4)=4 — unchanged ✓. Fix vs containment:
   max(10,3)=10 ✓. Empty guard doesn't affect either ✓.
7. CALIBRATE. High — each bug demonstrated on a concrete input.

## Why this form works
Contract stated before reading the body; concrete inputs traced with values, not
vibes; the sweep continued after the first bug; the fix was re-checked against
the happy path.
