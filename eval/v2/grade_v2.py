"""Mechanical grader for eval v2. No human judgment touches scoring.

Input: results JSONL, one row per run:
  {"id": "CB1-B", "arm": "control|fossil|sonnet", "run": 1,
   "verdict": "<verbatim final VERDICT line>", "tokens": 12345}

Usage: python3 grade_v2.py results.jsonl
"""
import json
import re
import sys
from collections import defaultdict

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from tasks import TASKS  # noqa: E402

BY_ID = {t["id"]: t for t in TASKS}


def parse_verdict(raw):
    """Return (kind, value). kind in {BUG, NO-BUG, CANNOT-DETERMINE, IMPOSSIBLE,
    NO-SOLUTION, SOLUTION, ANSWER, UNPARSEABLE}."""
    m = re.search(r"VERDICT\s*:\s*(.+)", raw, re.IGNORECASE)
    if not m:
        return ("UNPARSEABLE", None)
    v = m.group(1).strip().strip("*`_ .").upper()
    if re.match(r"NO[\s\-_]?BUG", v):
        return ("NO-BUG", None)
    if v.startswith("BUG"):
        return ("BUG", None)
    if v.startswith("CANNOT") or "CANNOT-DETERMINE" in v or "INDETERMIN" in v:
        return ("CANNOT-DETERMINE", None)
    if v.startswith("IMPOSSIBLE"):
        return ("IMPOSSIBLE", None)
    if re.match(r"NO[\s\-_]?SOLUTION", v):
        return ("NO-SOLUTION", None)
    m2 = re.match(r"SOLUTION\s*=?\s*([A-D](?:\s*,?\s*[A-D]){3})", v)
    if m2:
        return ("SOLUTION", re.sub(r"[^A-D]", "", m2.group(1)))
    m3 = re.match(r"ANSWER\s*=?\s*(.+)", v)
    if m3:
        num = m3.group(1)
        num = num.replace("$", "").replace(",", "").replace(":1", "").strip()
        pct = num.endswith("%")
        num = num.rstrip("%").strip()
        m4 = re.match(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", num)
        if not m4:
            return ("UNPARSEABLE", None)
        x = float(m4.group(0))
        if pct:
            x /= 100.0
        return ("ANSWER", x)
    return ("UNPARSEABLE", None)


def is_correct(task, kind, value):
    exp = task["expected"]
    if exp in ("NO-BUG", "BUG", "CANNOT-DETERMINE", "IMPOSSIBLE", "NO-SOLUTION"):
        return kind == exp
    if exp.startswith("SOLUTION="):
        return kind == "SOLUTION" and value == exp.split("=")[1]
    if exp == "ANSWER":
        if kind != "ANSWER":
            return False
        lo, hi = task["range"]
        if lo <= value <= hi:
            return True
        # scale forgiveness: probability given as percent, or percent as fraction
        if hi <= 1.5 and lo <= value / 100.0 <= hi:
            return True
        if lo >= 1 and lo <= value * 100.0 <= hi:
            return True
        return False
    raise ValueError(exp)


def main(path):
    rows = [json.loads(l) for l in open(path) if l.strip()]
    cells = defaultdict(lambda: [0, 0, 0])  # key -> [correct, total, tokens]

    def add(key, ok, tok):
        cells[key][0] += ok
        cells[key][1] += 1
        cells[key][2] += tok

    unparseable = []
    for r in rows:
        t = BY_ID[r["id"]]
        kind, value = parse_verdict(r["verdict"])
        if kind == "UNPARSEABLE":
            unparseable.append((r["id"], r["arm"], r["run"], r["verdict"]))
        ok = int(is_correct(t, kind, value))
        tok = r.get("tokens", 0)
        arm = r["arm"]
        add((arm, "overall"), ok, tok)
        add((arm, t["variant"]), ok, tok)
        add((arm, t["family"]), ok, tok)
        add((arm, t["family"], t["variant"]), ok, tok)

    arms = sorted({k[0] for k in cells})

    def line(label, key_suffix):
        parts = [f"{label:<22}"]
        for a in arms:
            c, n, _ = cells.get((a,) + key_suffix, [0, 0, 0])
            parts.append(f"{a}: {c}/{n}" + (f" ({c/n:.0%})" if n else ""))
        print("  ".join(parts))

    print(f"runs: {len(rows)}   arms: {', '.join(arms)}\n")
    line("OVERALL", ("overall",))
    line("broken (hit rate)", ("broken",))
    line("healthy (1-FA rate)", ("healthy",))
    print()
    for fam in ["CB", "QM", "HO", "PR"]:
        line(f"{fam} all", (fam,))
        line(f"{fam} broken", (fam, "broken"))
        line(f"{fam} healthy", (fam, "healthy"))
    print()
    for a in arms:
        c, n, tok = cells[(a, "overall")]
        print(f"{a}: mean subagent tokens/run = {tok//max(n,1):,}")
    if unparseable:
        print(f"\nUNPARSEABLE ({len(unparseable)}):")
        for u in unparseable:
            print("  ", u)


if __name__ == "__main__":
    main(sys.argv[1])
