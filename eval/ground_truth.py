"""Verifies every ground truth in eval/tasks.md. Run: python3 ground_truth.py"""
import itertools
import math
import random
import subprocess
import sys

ok = True


def check(name, cond, detail=""):
    global ok
    status = "PASS" if cond else "FAIL"
    if not cond:
        ok = False
    print(f"[{status}] {name} {detail}")


# ---- T1: lower_bound infinite loop (run in subprocess with timeout) ----
T1_CODE = """
def lower_bound(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid
        else:
            hi = mid
    return lo
print(lower_bound([1, 3], 2))
"""
try:
    subprocess.run([sys.executable, "-c", T1_CODE], timeout=2, capture_output=True)
    check("T1 infinite loop on ([1,3], 2)", False, "terminated — expected hang")
except subprocess.TimeoutExpired:
    check("T1 infinite loop on ([1,3], 2)", True, "hangs as expected (lo=mid never advances)")

# T1 also: correct on inputs where lo never needs to advance past mid
T1_OK = """
def lower_bound(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid
        else:
            hi = mid
    return lo
print(lower_bound([3, 5, 7], 3))
"""
r = subprocess.run([sys.executable, "-c", T1_OK], timeout=2, capture_output=True, text=True)
check("T1 returns 0 for ([3,5,7], 3) (bug is input-dependent)", r.stdout.strip() == "0")


# ---- T2: dedupe_latest emits duplicate ids ----
def dedupe_latest(records):
    latest = {}
    order = []
    for rid, val in records:
        order.append(rid)
        latest[rid] = val
    return [(rid, latest[rid]) for rid in order]

out = dedupe_latest([("a", 1), ("b", 2), ("a", 3)])
check("T2 duplicate id in output", out == [("a", 3), ("b", 2), ("a", 3)], f"got {out}")


# ---- T3: make_config corrupts DEFAULT_CONFIG via shallow copy ----
DEFAULT_CONFIG = {"retries": 3, "timeouts": {"connect": 5, "read": 10}}

def make_config(overrides):
    config = dict(DEFAULT_CONFIG)
    for k, v in overrides.items():
        if isinstance(v, dict):
            config[k].update(v)
        else:
            config[k] = v
    return config

make_config({"timeouts": {"read": 1}})
second = make_config({})
check("T3 corruption leaks to later calls", second["timeouts"]["read"] == 1,
      f"second call read timeout = {second['timeouts']['read']}")
check("T3 DEFAULT_CONFIG mutated", DEFAULT_CONFIG["timeouts"]["read"] == 1)


# ---- T4: Bayes, two independent positive tests ----
p = 0.003 * 0.98**2 / (0.003 * 0.98**2 + 0.997 * 0.04**2)
check("T4 analytic", abs(p - 0.6436) < 0.001, f"p = {p:.4f}")
rng = random.Random(42)
hits = tot = 0
for _ in range(2_000_000):
    d = rng.random() < 0.003
    pos1 = rng.random() < (0.98 if d else 0.04)
    pos2 = rng.random() < (0.98 if d else 0.04)
    if pos1 and pos2:
        tot += 1
        hits += d
check("T4 Monte Carlo agrees", abs(hits / tot - p) < 0.01, f"MC = {hits/tot:.4f}")

# ---- T5: 8 people, shared birth month ----
p5 = 1 - math.perm(12, 8) / 12**8
check("T5 analytic", abs(p5 - 0.9536) < 0.001, f"p = {p5:.4f}")
share = 0
for _ in range(500_000):
    months = [rng.randrange(12) for _ in range(8)]
    share += len(set(months)) < 8
check("T5 Monte Carlo agrees", abs(share / 500_000 - p5) < 0.01, f"MC = {share/500_000:.4f}")

# ---- T6: bottleneck ----
# per request: B load 2, C load 3 direct + 2 indirect (one per B call) = 5
r_b = 500 / 2
r_c = 600 / 5
check("T6 answer 120 (C binds)", min(r_b, r_c) == 120, f"B cap {r_b}, C cap {r_c}")

# ---- T7: stop on 7 or 11 ----
p7, p11 = 6 / 36, 2 / 36
check("T7 analytic 0.25", abs(p11 / (p7 + p11) - 0.25) < 1e-12)
stops11 = 0
for _ in range(500_000):
    while True:
        s = rng.randint(1, 6) + rng.randint(1, 6)
        if s in (7, 11):
            stops11 += s == 11
            break
check("T7 Monte Carlo agrees", abs(stops11 / 500_000 - 0.25) < 0.005,
      f"MC = {stops11/500_000:.4f}")

# ---- T8: knights and knaves, unique solution ----
sols = []
for a, b, c, d in itertools.product([True, False], repeat=4):
    n_knights = a + b + c + d
    s_a = (not b) and (not d)
    s_b = c
    s_c = (not a) and b
    s_d = n_knights == 2
    if (a == s_a) and (b == s_b) and (c == s_c) and (d == s_d):
        sols.append((a, b, c, d))
check("T8 unique solution", sols == [(True, False, False, False)], f"solutions: {sols}")

# ---- T9: scheduling, unique order ----
sols9 = []
for perm in itertools.permutations("ABCDE"):
    pos = {t: i + 1 for i, t in enumerate(perm)}
    if not pos["C"] < pos["A"]:
        continue
    if abs(pos["B"] - pos["D"]) != 2:
        continue
    if pos["E"] != pos["A"] + 1:
        continue
    if not pos["D"] < pos["E"]:
        continue
    if pos["B"] == 5:
        continue
    if not pos["B"] < pos["D"]:
        continue
    sols9.append("".join(perm))
check("T9 unique solution BCDAE", sols9 == ["BCDAE"], f"solutions: {sols9}")

# ---- T10: reference implementation sanity for the rubric's expected outputs ----
def second_largest_distinct(xs):
    d = sorted(set(xs), reverse=True)
    if len(d) < 2:
        raise ValueError
    return d[1]

cases = [([5, 5, 3], 3), ([1, 2], 1), ([-1, -5], -5), ([5, 3, 3], 3), ([2, 9, 4, 9], 4)]
t10 = all(second_largest_distinct(i) == o for i, o in cases)
for bad in ([], [7], [4, 4, 4]):
    try:
        second_largest_distinct(bad)
        t10 = False
    except ValueError:
        pass
check("T10 rubric expected outputs consistent", t10)

print()
print("ALL GROUND TRUTHS VERIFIED" if ok else "GROUND TRUTH FAILURES — fix tasks.md")
sys.exit(0 if ok else 1)
