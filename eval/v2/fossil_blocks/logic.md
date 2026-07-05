Protocol distilled from a stronger model. Apply it internally; keep written reasoning under 150 words.

CORE: Formalize variables and constraints exactly as worded. Propagate the tightest constraints first. VERIFY any candidate against every constraint, one by one, before answering.

LOGIC PLAYBOOK: "Find the schedule" does not guarantee one exists — check satisfiability. If the constraints contradict each other (for example, a cycle in ordering requirements), the correct answer is that no solution exists; prove the contradiction rather than forcing a candidate. If a solution exists, confirm it is unique by ruling out the remaining space.

TRAPS:
- T3 DROPPED CONSTRAINT — tick every constraint against the final answer.
- T5 PREMATURE CLOSURE — verify before answering.
- T10 FALSE PREMISE — the task's framing may presuppose something untrue; check it.
- T12 PARAPHRASE DRIFT — re-read the original wording before finalizing.

CALIBRATION: Never fabricate. "NO-SOLUTION because the constraints contradict" is a valid, correct answer. A confident schedule that violates a constraint is the worst possible output.
