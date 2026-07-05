# Exemplar trace: constraint puzzle

Copy the STRUCTURE of this trace, not its content.

## Task
Four runners W, X, Y, Z finish a race, no ties. X finishes before W. Exactly one
runner finishes between X and Z. Y does not finish last. Z finishes before Y.
Find the finishing order.

## Trace

1. RESTATE / FORMALIZE. Positions 1–4, one runner each.
   C1: pos(X) < pos(W). C2: |pos(X) − pos(Z)| = 2. C3: pos(Y) ≠ 4.
   C4: pos(Z) < pos(Y).
2. PROPAGATE. C2 is tightest — enumerate (X,Z) pairs: (1,3), (2,4), (3,1), (4,2).
   C1 needs a W after X, so X ≠ 4 → drop (4,2).
3. CASE TREE.
   - X=1, Z=3: C4 → Y=4. Violates C3. ✗
   - X=2, Z=4: C4 → Y>4 impossible. ✗
   - X=3, Z=1: C1 → W=4. Remaining Y=2. C3: 2≠4 ✓. C4: 1<2 ✓. Candidate:
     Z, Y, X, W.
4. ANSWER. 1st Z, 2nd Y, 3rd X, 4th W.
5. VERIFY — tick pass. C1: X(3)<W(4) ✓. C2: |3−1|=2, exactly one runner (Y)
   between ✓. C3: Y=2 ✓. C4: Z(1)<Y(2) ✓. Uniqueness: the case tree covered
   every (X,Z) pair allowed by C2, and the other branches died — unique ✓.
6. CALIBRATE. High — full enumeration of the branching variable, all constraints
   ticked.

## Why this form works
The tightest constraint chose the branching variable; each dead branch cites its
killer; the tick pass caught nothing this time, but it is what usually catches
the dropped constraint (trap T3).
