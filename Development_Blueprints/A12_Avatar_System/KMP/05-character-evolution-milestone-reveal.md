# K-05 — Character Evolution Milestone Reveal

## 1. Feature Context
NoorHeroes KMP app (Android/iOS). Part of Feature A.12 — Avatar System. Implements the Character Evolution milestone reveal: the Noor companion/avatar visibly evolving through learning-based progression, presented with a gentle, growth-themed transition rather than an abrupt power-up effect.

## 2. Parent Feature
A.12 Avatar System — KMP App (Android/iOS)

## 3. Sub-feature
K-05 Character Evolution Milestone Reveal

## 4. Objective
Build the Character Evolution Milestone Reveal modal and its graceful in-place/next-load application logic, backing FR-9 and Edge Case 8.

## 5. Business Requirements
- Avatars and Noor companions evolve through learning-based progression — Quran skills, story morals, kindness actions, and habit consistency unlock new outfits, glow states, and story-world abilities (FR-9).
- If a child is actively viewing the companion (e.g., on Home) when an evolution milestone is crossed, the visual update applies gracefully — on next Home load or via a graceful in-place transition — never an abrupt, jarring change mid-interaction that could startle a young child (Edge Case 8).
- Evolution milestones use a gentle, growth-themed transition (a soft glow bloom, consistent with A.7's Noor Garden growth metaphor) rather than an abrupt "transform" effect, reinforcing "gradual real progress" over a sudden game-like power-up (PRD §2.1).
- Success metric target: Character Evolution milestone view-through rate ≥ 70% (PRD §1.4) — the reveal must be genuinely engaging, not skippable-by-default in a way that undermines this metric.

## 6. Existing Architecture
Extends `feature-avatar`/`feature-avatar-domain` established in K-01–K-04. The Noor companion itself is presented on the Home screen, owned by A.2 Home Dashboard (per A.12 PRD's "Feeds into: A.2 Home — Noor companion presentation" scope note). This sub-feature owns the *evolution reveal moment and transition logic* as part of the Avatar System; the baseline companion-rendering surface on Home is A.2's existing `HomeScreen`/companion-widget composable, which this sub-feature integrates with via a shared evolution-state signal rather than duplicating Home's rendering logic. The gentle-transition visual language is shared with A.7's Noor Garden growth metaphor (glow-bloom, not abrupt transform) — reuse `core-design-system` tokens established there where applicable, extending with Character-Evolution-specific tokens only where genuinely new.

## 7. Existing Code to Reuse
- `AvatarViewModel`/`Avatar3DRenderer` (K-01)
- A.2 Home's Noor companion presentation composable (integration point, not duplicated)
- `core-design-system` growth/glow-bloom tokens (A.7 Noor Garden precedent)
- `core-analytics` `AnalyticsTracker`

## 8. Files to Create
- `feature-avatar/src/commonMain/kotlin/.../evolution/CharacterEvolutionRevealModal.kt` (Composable)
- `feature-avatar/src/commonMain/kotlin/.../evolution/CharacterEvolutionDetector.kt`
- `feature-avatar-domain/src/commonMain/kotlin/.../GetCompanionEvolutionUseCase.kt` (calls B-07's standalone endpoint, for Home's lightweight companion-tier read)
- `feature-avatar-domain/src/commonMain/kotlin/.../DetectEvolutionMilestoneUseCase.kt`
- `feature-avatar/src/commonTest/kotlin/.../CharacterEvolutionGracefulApplicationTest.kt`

## 9. Files to Modify
- A.2 Home's companion-presentation composable — integrate a hook to check for a pending evolution reveal and, if the child is actively viewing the companion, apply the graceful in-place transition instead of an abrupt state swap (coordination point flagged explicitly, not silently duplicated)

## 10. KMP Requirements
- `CharacterEvolutionDetector` reuses the same diffing principle as K-04's `AutoUnlockDiffDetector`, but scoped to companion-evolution-tier fields within the inventory/companion-state response (e.g., a `companion_tier`/`evolution_stage` field) rather than owned-items — detects a tier/stage increase between successive fetches.
- If the child is **not** actively viewing the companion at detection time, the new tier is simply reflected on next Home load (no special transition needed — the companion just renders at its new tier).
- If the child **is** actively viewing the companion (Home screen foregrounded) when the detector identifies a crossed milestone, `CharacterEvolutionRevealModal` presents with a soft glow-bloom transition, then dismisses back to the current screen (e.g., Home) — never an abrupt swap of the rendered companion mid-frame.
- Modal presentation must be interruptible/dismissible without causing any inconsistency in the underlying companion-tier state (dismissing the modal is purely a UI action, not a state mutation).

## 11. Backend Requirements
Consumes companion-evolution-tier data from B-07 (Companion Evolution Tier API), which formalizes the `companion_tier`/`evolution_stage` signal this sub-feature originally needed to assume — B-07 both extends B-01's `GET /v1/children/{id}/inventory` response with a `companion_evolution` object (used by K-01's existing single inventory fetch) and exposes a standalone `GET /v1/children/{id}/companion-evolution` endpoint (preferred here on Home, avoiding a full inventory fetch just to render tier). Tier advancement is monotonic (never decreases) and driven by the same `UnlockEvaluationConsumer` event stream B-02 already consumes.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`GET /v1/children/{id}/companion-evolution` (B-07) — `{ "tier": 3, "tier_name": "Radiant Explorer", "last_advanced_at": "..." }`. The same data is also available as the `companion_evolution` field on `GET /v1/children/{id}/inventory` (B-01, extended by B-07) for surfaces that already fetch the full inventory (K-01).

## 14. Database Requirements (Local)
Reuses `avatar_inventory_cache` (K-01) as the diff baseline for companion-tier detection, mirroring K-04's pattern.

## 15. Validation
Unit test asserting that when the companion is actively being viewed at milestone-crossing detection time, the transition is applied gracefully (via the documented glow-bloom path) rather than an abrupt state swap — verified by asserting the transition-state flag sequence, not a visual/pixel comparison (Edge Case 8, mandatory).

## 16. Authentication
Reuses shared `core-network` Bearer token attachment (inherited from K-01's inventory fetch).

## 17. Authorization
N/A at UI layer.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Evolution milestone crossed while child is off Home/not viewing companion | New tier simply reflected on next Home load, no special transition needed |
| Evolution milestone crossed while child is actively viewing companion | Graceful glow-bloom transition applied in-place, never an abrupt swap |
| Modal dismissed mid-transition | Underlying companion-tier state is unaffected by the dismissal action; companion settles at its correct new tier regardless |
| Detector runs with no prior baseline (fresh install) | No false "evolution" reveal fires for a brand-new child's initial tier |

## 19. Offline First
Companion-tier detection only runs on a successful network fetch, mirroring K-04's connectivity-dependent diffing principle; offline sessions simply render the last-known tier from cache without triggering a reveal.

## 20. Local Data
```
GET /v1/children/{id}/inventory (fresh fetch, includes companion-tier signal)
   ↓
CharacterEvolutionDetector.detectMilestoneCrossed(cached tier, fresh tier)
   ↓
[if crossed AND companion actively viewed] → graceful in-place transition / reveal modal
[if crossed AND not actively viewed] → silently reflected on next Home load
   ↓
Overwrite avatar_inventory_cache with fresh response
```

## 21. Localization
Milestone reveal celebratory copy resolved via string resources (English, Hindi, Arabic, Urdu).

## 22. RTL
Reveal modal layout mirrors correctly for RTL locales; verified via a dedicated RTL layout test.

## 23. Analytics
`character_evolution_milestone_reached` (fired on detection, regardless of viewing state), `character_evolution_reveal_viewed` (fired only when the modal is actually presented and viewed) via `AnalyticsTracker.logEvent()`.

## 24. Performance
Diffing is a lightweight single-field comparison; transition animation must remain smooth on low-end Android (reuse `core-design-system`'s already-performance-tuned glow-bloom animation primitives from A.7's Noor Garden rather than introducing a new animation system).

## 25. Security
No new sensitive data handling.

## 26. Library Requirements
Compose Multiplatform, Koin, kotlinx-coroutines, `core-design-system` animation primitives.

## 27. Testing
- Unit (P0): graceful in-place transition applied when companion is actively viewed at detection time (Edge Case 8).
- Unit: no false reveal on fresh-install/no-baseline case.
- Unit: dismissing the modal mid-transition does not corrupt the underlying tier state.
- UI: reveal modal renders the correct gentle glow-bloom transition, not an abrupt swap (visual-language conformance test against design tokens).
- Integration: milestone crossed while off Home → new tier correctly reflected on next Home load without a modal ever firing outside the viewing context.

## 28. Documentation
KDoc on `CharacterEvolutionDetector` explaining its relationship to K-04's diffing pattern and the specific "never abrupt while actively viewed" business rule driving the graceful-transition branch.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `CharacterEvolutionDetector`**
- Objective: diff-based detection of a companion-tier increase between successive fetches.
- Files to Create: `CharacterEvolutionDetector.kt`
- Existing Architecture to Follow: mirrors `AutoUnlockDiffDetector`'s (K-04) pattern, scoped to the tier field.
- Tests: unit tests for tier-increase detection, no-baseline case, no-false-positive on unrelated field changes.
- Definition of Done: detector correctly identifies genuine tier crossings only.

**Task 02 — Implement `DetectEvolutionMilestoneUseCase`**
- Objective: domain-layer orchestration invoking the detector with correct before/after snapshots.
- Files to Create: `DetectEvolutionMilestoneUseCase.kt`
- Definition of Done: use case correctly wired with proper diff-before-overwrite ordering (shared discipline with K-04 Task 03).

**Task 03 — Build `CharacterEvolutionRevealModal` Composable**
- Objective: gentle glow-bloom transition reveal, reusing A.7 Noor Garden's animation tokens.
- Files to Create: `CharacterEvolutionRevealModal.kt`
- Localization/RTL: per §21/§22.
- Analytics: `character_evolution_reveal_viewed` on presentation.
- Tests: visual-language conformance UI test.
- Definition of Done: modal matches the platform's established gentle-transition visual language, verified against design tokens.

**Task 04 — Integrate Graceful In-Place Application with A.2 Home**
- Objective: coordination hook so an actively-viewed companion transitions gracefully rather than being abruptly swapped.
- Files to Modify: A.2 Home's companion-presentation composable (flagged coordination point, not a silent duplication)
- Tests (P0): Edge Case 8 graceful-transition test.
- Do Not Change: do not rewrite A.2 Home's existing companion-rendering logic beyond adding this integration hook.
- Definition of Done: P0 test passes; A.2 Home's existing behavior otherwise unaffected.

**Task 05 — Final Code Review**
- Do Not Change: A.2 Home's unrelated dashboard logic; K-04's `AutoUnlockDiffDetector` (separate concern, not to be merged).
- Expected Result: PR merge-ready.

## 30. Definition of Done
Character Evolution milestones are correctly detected via diffing, applied gracefully (never abruptly) when the companion is actively being viewed, and presented via a gentle glow-bloom reveal matching the platform's established growth-metaphor visual language.

## 31. Final Verification Checklist
- [ ] Tier-crossing detection correctly identifies genuine milestones only (no false positives on unrelated field changes)
- [ ] Graceful in-place transition verified when companion is actively viewed at detection time (P0 test passing)
- [ ] No abrupt/jarring swap ever occurs while the child is actively viewing the companion
- [ ] Reveal modal matches the established gentle glow-bloom visual language, not a sudden "transform" effect
- [ ] A.2 Home integration hook added without disrupting existing Home dashboard behavior
- [ ] Localization (EN/HI/AR/UR) and RTL verified
- [ ] Analytics events wired via `AnalyticsTracker`
- [ ] Animation performance smooth on low-end Android target
