# Exemplar trace: Bayes by counts

Copy the STRUCTURE of this trace, not its content.

## Task
2% of widgets are defective. A detector flags 95% of defective widgets and 3%
of good ones. A widget is flagged. Probability it is defective?

## Trace

1. RESTATE. Asked: P(defective | flagged). Given: prevalence 2%, sensitivity
   95%, false-positive rate 3%. Not the classic "99% accurate test" — numbers
   differ, one flag only.
2. INVENTORY. C1 prevalence 0.02. C2 P(flag|def)=0.95. C3 P(flag|good)=0.03.
   Unknown: P(def|flag).
3. PLAN. Bayes-by-counts template, population 10,000.
4. EXECUTE.
   - defective: 10,000 × 0.02 = 200. good: 9,800.
   - flagged defective: 200 × 0.95 = 190.
   - flagged good: 9,800 × 0.03 = 294.
   - total flagged: 190 + 294 = 484.
   - posterior: 190 / 484 = 0.3926.
5. ANSWER. ≈ 39.3%.
6. VERIFY. Independent route — odds form: prior odds 2:98 = 1:49; likelihood
   ratio 0.95/0.03 = 31.67; posterior odds 31.67:49 = 0.646 → p = 0.646/1.646 =
   0.393 ✓. Sanity: below 50% despite a "95% accurate" detector, because good
   widgets outnumber defective 49:1 — the false positives (294) outnumber the
   true positives (190). In [0,1] ✓.
7. CALIBRATE. High — two routes agree.

## Why this form works
Counts made the false-positive pile visible (trap T2); a second, structurally
different computation confirmed the number; the "surprising" answer was
explained, not just asserted.
