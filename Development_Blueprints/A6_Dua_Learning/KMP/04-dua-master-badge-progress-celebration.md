# K-04 — Dua Master Badge Progress Celebration

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. **Scope correction:** `A11_Rewards_System/KMP/09-reward-unlock-animation-badge-unlock-modal.md` already builds a shared, reusable `BadgeUnlockModal(badge: BadgeUiModel, onDismiss)` in `core/design-system/.../reward/`, and documents that `A3_Stories_Module`'s equivalent K-06 was *updated* to consume it directly rather than build a local modal, with the explicit note "no outstanding coordination item remains for A.3." **This file should follow the identical pattern A.3 already set: reuse only, no local build.**

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
K-04 — Dua Master Badge Progress Celebration (reuse of `core/design-system`'s `BadgeUnlockModal`)

## 4. Objective
Trigger `core/design-system`'s existing `BadgeUnlockModal` when the child's Dua Master badge is awarded (per B-05's real, A11-driven award flow), with `onDismiss` navigating back to the Dua Card/Catalog screen the child was on, per the modal's own documented dismiss contract ("dismiss always navigates the calling screen back to its own 'next step'").

## 5. Business Requirements
FR-10; Edge Case 2 (stickiness — already guaranteed by A11's `child_badges` table, nothing to implement here).

## 6. Existing Architecture
`core/design-system/src/commonMain/kotlin/.../reward/BadgeUnlockModal.kt` (A11-K09) — reused, not rebuilt. Badge-award detection mechanism (how the client learns a new badge was awarded — polling `GET /v1/rewards/balance`, a push signal, or a result embedded in `QuizResult` from K-03/`:core:quiz-engine`) needs confirming against A11's actual shared rewards client module (`A11_Rewards_System/KMP/01-shared-rewards-client-module.md`) before this file assumes a specific mechanism.

## 7. Existing Code to Reuse
- `core/design-system`'s `BadgeUnlockModal`, `BadgeUiModel` (A11-K09) — the entire celebration UI, not rebuilt
- A11's shared rewards client module (K-01) — badge-award detection

## 8. Files to Create
- `feature/dua/src/commonMain/kotlin/.../badge/DuaMasterBadgeTrigger.kt` — thin trigger logic only, no modal UI
- `feature/dua/src/commonTest/kotlin/.../DuaMasterBadgeTriggerTest.kt`

## 9. Files to Modify
- `DuaCardDetailScreen.kt` / `DuaCatalogScreen.kt` (K-01/K-02) — mount `BadgeUnlockModal` when triggered, per A3-K06's established integration pattern

## 10. Backend Requirements
Consumes A11's existing reward/badge read surface (via B-05's `dua_learned` award wiring) — no new backend endpoint.

## 11. KMP Requirements
- Detect a new "Dua Master" badge award via A11's shared rewards client (confirm exact mechanism per §6, do not assume)
- Call `BadgeUnlockModal(badge = BadgeUiModel(...), onDismiss = { /* navigate per the modal's documented contract */ })`
- Deferred/queued trigger if the award happens while the child is on an unrelated screen — confirm whether A11's shared rewards client already handles this queuing generically (likely, given 4+ consumers) before building dua-specific queuing logic

## 12. NextJS Requirements
N/A.

## 13. API Contract
No new endpoint — reads A11's existing reward/badge state.

## 14. Database Requirements
N/A directly.

## 15. Validation
N/A beyond confirming the badge code/type matches "Dua Master" as configured in B-05/B-10's A11 admin setup.

## 16. Authentication / 17. Authorization
Inherited from A11's shared rewards client's existing session handling.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Badge-progress signal arrives off-screen | Deferred per A11's shared client behavior (confirm, don't reinvent) |
| Rewards read API unavailable | Celebration simply doesn't trigger this session — non-critical, non-blocking |

## 19. Offline First
N/A — live-state signal; deferred until online per A11's existing pattern.

## 20. Local Data
None dua-specific — any "pending celebration" queuing is A11's shared client's responsibility if it exists.

## 21. Localization / 22. RTL
Inherited from `BadgeUnlockModal`'s existing localization.

## 23. Analytics
`dua_master_badge_progress_updated` — confirm whether A11's shared client already fires a generic `badge_unlocked` event that supersedes a dua-specific one, to avoid double-counting.

## 24. Performance / 25. Security
N/A directly — inherited from A11's already-hardened shared components.

## 26. Library Requirements
`core/design-system`'s reward package, A11's shared rewards client module — no new dependencies.

## 27. Testing
- Unit: trigger-detection logic for a Dua Master award specifically (filtering A11's generic badge-award stream for this one badge code)
- Integration: `BadgeUnlockModal` renders correctly with dua-specific `BadgeUiModel` content, dismiss navigates correctly

## 28. Documentation
Record (mirroring A3-K06's own note) that no local modal was built and why — reuse only.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm A11's Badge-Award Detection Mechanism**
Task ID: K-04-T01. Objective: read `A11_Rewards_System/KMP/01-shared-rewards-client-module.md` to determine the real mechanism (polling/push/result-embedded) before building trigger logic. Definition of Done: documented finding.

**Task 02 — Implement Dua-Specific Filter/Trigger**
Task ID: K-04-T02. Files to Create: `DuaMasterBadgeTrigger.kt`. Dependencies: Task 01. Definition of Done: correctly filters A11's generic award stream for the "Dua Master" badge code.

**Task 03 — Wire `BadgeUnlockModal`**
Task ID: K-04-T03. Files to Modify: relevant K-01/K-02 screens. Existing Files to Reuse: `BadgeUnlockModal` (A11-K09) — reuse only, no local build, per A3-K06's precedent. Definition of Done: modal renders correctly with dua-specific content on trigger.

**Task 04 — Add Tests**
Task ID: K-04-T04. Definition of Done: all §27 scenarios green.

**Task 05 — Add Documentation**
Task ID: K-04-T05. Definition of Done: reuse-only note recorded.

**Task 06 — Final Code Review**
Task ID: K-04-T06. Definition of Done: §31 checklist fully checked; confirm no local modal exists in `feature/dua/`.

## 30. Definition of Done
Dua Master badge celebration triggers correctly using A11's existing shared `BadgeUnlockModal`, with no local modal implementation, mirroring A3's own confirmed reuse pattern.

## 31. Final Verification Checklist
- [ ] No local badge celebration modal built — `BadgeUnlockModal` (A11-K09) reused directly
- [ ] Badge-award detection mechanism confirmed against A11's real shared client, not assumed
- [ ] Filter correctly isolates the "Dua Master" badge from A11's generic award stream
- [ ] Dismiss behavior matches the modal's documented contract

## 32. Addendum — What Changed From the Original Draft
The original draft built a bespoke celebration modal and trigger mechanism. The real, already-existing `A11_Rewards_System/KMP/09` blueprint provides a shared `BadgeUnlockModal` in `core/design-system`, and documents that Stories (A.3) already updated its own equivalent file to consume it directly rather than build locally, with the explicit note that no coordination item remains outstanding for that feature. This file now follows the identical, already-proven reuse pattern.
