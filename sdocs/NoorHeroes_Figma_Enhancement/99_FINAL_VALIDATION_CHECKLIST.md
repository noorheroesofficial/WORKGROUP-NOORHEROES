# Final documentation validation and execution checklist

Prepared 13 October 2026. This is a review package, not authorization to design all screens.

## Documentation checks performed

- [x] 237 individually numbered prompts across 27 visible feature groups; screens, overlays and alternate states are identified.
- [x] Every prompt has all 11 requested sections, source references, content audit, action/state contracts, motion, acceptance checks and a single-screen approval stop.
- [x] 17 shared-surface aliases resolve to owning prompts.
- [x] Both actual Figma reference containers inspected: Frame1 `1095:2`, Frame2 `1085:13003`, page `928:2`.
- [x] Exact text and compact structural records retained for 104 Figma child surfaces; desktop hub excluded.
- [x] Current mobile catalogue captured, including 20 seasonal previews. Web/admin previews excluded.
- [x] All 412 numbered functional requirements from 29 applicable feature/architecture PRDs retained in the requirement register. Derived owning-screen candidates are labeled as candidates.
- [x] All 936 observed controls have an owning prompt and a behavior or explicit unresolved-binding entry. Presence extraction does not establish click destinations.
- [x] PRD hashes match the audit manifest. No protected sources or Figma designs were written by this task.
- [x] Global navigation, motion, accessibility, responsive layout and decision registers are linked from the master index.

See [machine-readable structural validation](Evidence/document-validation.json), [source access qualifications](01_SOURCE_AUDIT_AND_ACCESSIBILITY.md) and [control reconciliation](11_CURRENT_CONTROL_RECONCILIATION.md).

## Execution blockers and limits

- [ ] Resolve the global and screen-specific content/flow conflicts in [open decisions](09_OPEN_QUESTIONS_AND_APPROVALS.md). Source strings remain separate; no religious, legal or localized copy was invented.
- [ ] Confirm 576 label-to-action bindings in the hosted preview ledger before wiring those controls. Their owning action contracts are documented; exact source click destinations were not comprehensively exercised.
- [ ] Approve one coherent copy ledger per screen, including verified Arabic/translation/content IDs and fixture provenance.
- [ ] Resolve missing independent destinations, notably full activity history and family account deletion/cancellation; proposed surfaces remain explicitly blocked.
- [ ] Approve tokens, component contracts and the enhanced-design working area. Existing instances/reactions were not found in inspected Figma descendants; proposed reusable components are recommendations.
- [ ] Review source paragraphs and visual details not covered by representative visual inspection. Extraction and requirement retention do not constitute exhaustive paragraph-by-paragraph or pixel-by-pixel certification.
- [ ] Verify runtime OpenAPI, actual persistence, permission, billing, security and synchronization contracts during implementation. No production integration was tested here.

## Before executing each individual prompt

1. Open its source PRD, corresponding blueprint and exact design references. Resolve missing or conflicting references.
2. Approve exact copy and required states; retain conditional entry/exit behavior rather than treating review numbering as a linear journey.
3. Duplicate only the approved source into the approved enhancement area; preserve originals.
4. Execute only that prompt and necessary approved shared dependencies.
5. Check all listed acceptance criteria, logical widths 320/360/390/420, 200% text, contrast, targets, safe areas, RTL where required, reduced motion and relevant interruptions.
6. Test forward/back/cancel and failure paths in the prototype. Do not claim simulated Figma behavior enforces production business rules.
7. Capture differences and evidence, report unresolved items, obtain review and approval before the next screen.

## Handover decision

The documentation is available for staged review. It is not fully cleared for prototype execution: content decisions, exact control bindings and missing destination policies must be settled for affected screens. No Figma design execution began.
