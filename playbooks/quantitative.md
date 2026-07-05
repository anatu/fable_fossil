# Playbook: quantitative reasoning (probability, rates, capacity, estimation)

## Rules
- Every intermediate number gets written down. One operation per line. (T6)
- Prefer counts to percentages: work on a population of 10,000. (T2)
- Every probability lands in [0,1]; every rate carries units. (T11)
- If the problem resembles a classic, diff it against the classic first. (T1)

## Templates

### BAYES (posterior from test results)
1. Take 10,000 cases. Split by base rate: `D = 10,000 × prevalence`, `¬D = rest`.
2. Positives from D: `D × sensitivity^k` for k independent positive tests.
   Positives from ¬D: `¬D × FPR^k`.
3. Posterior = D-positives / (D-positives + ¬D-positives).
4. Sanity: posterior moves from the base rate toward the evidence; two positive
   tests move it far more than one; answer near the sensitivity number is trap T2.

### CAPACITY / BOTTLENECK
1. List every resource with its limit — with units.
2. For ONE unit of demand, count TOTAL load on each resource, INCLUDING indirect
   load (A calls B and B calls C ⇒ C receives B's calls too). (T3)
3. Max demand = min over resources of (limit / per-unit load).
4. Sanity: name the binding resource; confirm the others are under their limits
   at that rate.

### STOPPING / CONDITIONAL (repeat until one of several events)
1. List the stopping events and their per-trial probabilities p_i. Non-stopping
   outcomes are irrelevant.
2. P(stop on event i) = p_i / Σ p_j over stopping events only.
3. Sanity: these probabilities sum to 1.

### AT-LEAST-ONE / COLLISION
1. Compute the complement (all distinct / none occur) as a product of fractions.
2. Answer = 1 − complement.
3. Sanity: more trials/people ⇒ probability strictly increases.

## Verification
Recompute by a different route (complement, or counts if you used formulas).
Extreme-case probe: set one input to 0 or 1 — does the result behave sensibly?
