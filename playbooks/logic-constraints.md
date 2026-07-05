# Playbook: logic & constraint puzzles

## Procedure
1. **Formalize.** Variables, domains, constraints numbered C1..Cn — quoting the
   puzzle's exact wording per constraint. Paraphrase drift here poisons
   everything downstream. (T12)
2. **Propagate.** Apply the tightest constraints first (immediately-after,
   exactly-N-between, fixed positions). Record what each rules out.
3. **Case-split only when propagation stalls.** Pick the variable with fewest
   remaining options. Explore branches in a written tree; kill a branch at its
   first contradiction and cite which constraint killed it.
4. **Truth-teller/liar puzzles.** A knight's statement is true; a knave's is
   false — as a biconditional: `speaker_is_knight ⇔ statement_true`. Check each
   speaker against their OWN statement, including statements about counts
   ("exactly two of us…"), which are evaluated against the candidate assignment
   itself. Self-referential clauses bite last. (T3)
5. **Verify.** Candidate against EVERY constraint, tick each. Then attempt a
   second solution: if you cannot rule out every alternative by argument,
   enumerate the remaining space (4 binary people = 16 rows — just do it).
6. If asked for "the unique X", uniqueness is part of the answer — show it.

## Verification
The tick-pass (step 5) is not optional. Most puzzle errors are one forgotten
constraint, not bad deduction. (T3, T5)
