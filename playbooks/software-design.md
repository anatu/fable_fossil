# Playbook: design decisions

1. **Requirements as testable statements.** Separate must-have from nice-to-have.
   A requirement you can't test is an opinion.
2. **Invariants before features.** What must the system never violate (data
   integrity, idempotency, auth boundaries)? Invariants outrank features in
   every trade-off.
3. **Enumerate ≥ 2 designs.** For each: what breaks first at 10× load/scope;
   blast radius when it fails; how reversible is adopting it.
4. **Pick simplest-and-reversible.** When two designs tie on requirements, the
   one that is easier to delete wins. State what evidence would change the
   decision.
5. **Failure modes and observers.** For the chosen design: how does it fail, who
   notices, and how fast? A failure nobody observes is the design's real cost.
6. **Calibrate.** Flag decisions that are irreversible or security-relevant for
   human/stronger-model review rather than deciding unilaterally.
