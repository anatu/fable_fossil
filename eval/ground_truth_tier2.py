"""Verifies Tier-2 ground truths. Run: python3 ground_truth_tier2.py"""
import itertools
import random
import sys

ok = True


def check(name, cond, detail=""):
    global ok
    status = "PASS" if cond else "FAIL"
    if not cond:
        ok = False
    print(f"[{status}] {name} {detail}")


# ---- H1: moving_average with three planted bugs ----
def moving_average(xs, k):
    if k < 0:
        raise ValueError("k must be positive")
    out = []
    s = sum(xs[:k])
    out.append(s / k)
    for i in range(k, len(xs) - 1):
        s += xs[i] - xs[i - k]
        out.append(s / k)
    return out

# B1: k == 0 -> ZeroDivisionError instead of ValueError
try:
    moving_average([1, 2, 3], 0)
    check("H1.B1 k=0 crashes", False, "no exception")
except ZeroDivisionError:
    check("H1.B1 k=0 raises ZeroDivisionError (should be ValueError)", True)
except ValueError:
    check("H1.B1 k=0 crashes", False, "raised ValueError - bug absent")

# B2: k > len(xs) -> silent wrong result instead of ValueError
r = moving_average([1, 2], 5)
check("H1.B2 k>len returns wrong value silently", r == [0.6], f"got {r}")

# B3: last window missing
r = moving_average([1, 2, 3, 4], 2)
check("H1.B3 last window missing", r == [1.5, 2.5], f"got {r} (correct would be [1.5,2.5,3.5])")
# sanity: n == k case is NOT affected by B3
r = moving_average([2, 4], 2)
check("H1 n==k window count correct (B3 needs n>k)", r == [3.0], f"got {r}")


# ---- H2: die until first 4, conditioned on all rolls even -> E[length] = 1.5 ----
rng = random.Random(7)
total = n = 0
for _ in range(3_000_000):
    seq = []
    while True:
        roll = rng.randint(1, 6)
        seq.append(roll)
        if roll == 4:
            break
    if all(r % 2 == 0 for r in seq):
        total += len(seq)
        n += 1
mc = total / n
check("H2 Monte Carlo E[len | all even] ~= 1.5", abs(mc - 1.5) < 0.01, f"MC = {mc:.4f} over {n} kept runs")

# ---- H3: 4-door Monty, host opens one random goat door, switch uniformly at random ----
wins = 0
N = 1_000_000
for _ in range(N):
    car = rng.randrange(4)
    pick = 0
    goats = [d for d in range(4) if d != pick and d != car]
    opened = rng.choice(goats)
    closed_others = [d for d in range(4) if d != pick and d != opened]
    final = rng.choice(closed_others)
    wins += final == car
mc3 = wins / N
check("H3 Monte Carlo P(win | random switch) ~= 0.375", abs(mc3 - 0.375) < 0.005, f"MC = {mc3:.4f}")

# ---- H4: 5-person knights/knaves, unique solution ----
sols = []
for a, b, c, d, e in itertools.product([True, False], repeat=5):
    cnt = a + b + c + d + e
    s_a = (b != c)                 # exactly one of B and C is a knight
    s_b = (not d) or (not e)       # D is a knave or E is a knave (inclusive)
    s_c = (a == d)                 # A and D are the same type
    s_d = (cnt % 2 == 1)           # number of knights is odd
    s_e = (b != c)                 # B and C are of different types
    if a == s_a and b == s_b and c == s_c and d == s_d and e == s_e:
        sols.append(tuple("K" if x else "V" for x in (a, b, c, d, e)))
print(f"  H4 solutions: {sols}")
check("H4 unique solution", len(sols) == 1)

# ---- H5: 6-task scheduling, unique order ----
sols5 = []
for perm in itertools.permutations("ABCDEF"):
    p = {t: i + 1 for i, t in enumerate(perm)}
    if p["F"] != p["A"] - 1:
        continue
    if not p["C"] > p["A"]:
        continue
    if abs(p["B"] - p["E"]) != 2:
        continue
    if not p["D"] < p["F"]:
        continue
    if not p["B"] < p["D"]:
        continue
    if p["E"] == 6:
        continue
    if p["C"] == p["E"] + 1:
        continue
    sols5.append("".join(perm))
print(f"  H5 solutions: {sols5}")
check("H5 unique solution", len(sols5) == 1)

# ---- H6: sequential mixed evidence Bayes ----
p = (0.005 * 0.90 * 0.15) / (0.005 * 0.90 * 0.15 + 0.995 * 0.05 * 0.98)
check("H6 analytic ~= 0.01366", abs(p - 0.01366) < 0.0005, f"p = {p:.5f}")
hits = tot = 0
for _ in range(4_000_000):
    dis = rng.random() < 0.005
    t1 = rng.random() < (0.90 if dis else 0.05)
    t2 = rng.random() < (0.85 if dis else 0.02)
    if t1 and not t2:
        tot += 1
        hits += dis
check("H6 Monte Carlo agrees", abs(hits / tot - p) < 0.003, f"MC = {hits/tot:.5f}")

print()
print("ALL TIER-2 GROUND TRUTHS VERIFIED" if ok else "FAILURES - adjust tasks")
sys.exit(0 if ok else 1)
