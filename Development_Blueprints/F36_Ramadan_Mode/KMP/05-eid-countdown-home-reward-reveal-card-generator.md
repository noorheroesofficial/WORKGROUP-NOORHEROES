# K-05 — Eid Countdown, Home & Reward Reveal Card Generator

## 1. Feature Context
The joyful transition out of the 30-night journey — Eid Countdown, the celebratory Eid Home re-theme, a Reward Reveal moment, and the Eid Card Generator — all of which must correctly re-sync to a moon-sighting-corrected date on next app open without any special client handling beyond simply re-reading server state.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
2.5 Eid Countdown, Home & Reward Reveal Card Generator (ID: **K-05**)

## 4. Objective
Build the Eid Countdown, Eid Home (themed), Eid Reward Reveal, and Eid Card Generator screens, sourcing all timing from B-01 and card generation from B-07.

## 5. Business Requirements
- §1.18 Screens 9-12: Eid Countdown, Eid Home (themed), Eid Reward Reveal, Eid Card Generator.
- FR-3: moon-sighting-disputed Eid date re-syncs the in-progress UI on next app open.
- §2.1: Eid Celebration Visual Language — joyful, bright, celebratory shift, child-safe non-startling flourishes.
- §2.5: full image-generation prompt provided for Eid Home (En + Ar RTL).

## 6. Existing Architecture
`:feature:ramadan` module; Eid Card Generator delegates entirely to B-07 (which itself delegates to A.11's `ShareCardService`) — no local rendering logic.

## 7. Existing Code to Reuse
- K-01's `RamadanCampaignViewModel` (phase-derived Eid-mode entry, re-sync behavior)
- A.11's Share Card generation UI pattern (Parent Gate → generate → share flow, structural reference)
- `:core:security`'s Parent Gate/step-up UI component (per `CORE_SECURITY_INSTRUCTIONS.md`)

## 8. Files to Create
- `feature/ramadan/presentation/eid/EidCountdownScreen.kt`
- `feature/ramadan/presentation/eid/EidHomeScreen.kt`
- `feature/ramadan/presentation/eid/EidRewardRevealScreen.kt`
- `feature/ramadan/presentation/eid/EidCardGeneratorScreen.kt`
- `feature/ramadan/presentation/eid/EidCardViewModel.kt`
- `feature/ramadan/domain/usecase/GenerateEidCardUseCase.kt`

## 9. Files to Modify
- `:core:navigation`'s nav-graph — register Eid screens and `noorheroes://ramadan/eid` deep link

## 10. KMP Requirements
- **UI/Screen:** Eid Countdown (last 2 days), Eid Home (bright/celebratory theme overlay per §2.5's provided prompt), Eid Reward Reveal interaction, Eid Card Generator gated behind Parent Gate → Share.
- **State/ViewModel:** phase transition into `eid_transition`/`eid_celebration` sourced from K-01's shared `RamadanCampaignViewModel` — no independent Eid-date tracking.
- **Re-sync behavior:** on every app open, the phase/Eid-date is re-fetched from B-01; if an admin override (B-08) has corrected the date since last open, the UI reflects it automatically — this requires no special-case code, only that K-01's existing "always fetch fresh on open, cache as fallback" pattern is followed faithfully (never a locally-persisted "final" Eid date that resists refresh).
- **Card generation:** `GenerateEidCardUseCase` calls B-07's `POST /v1/ramadan/eid-cards`, gated by the Parent Gate step-up flow.
- **Deep Linking:** `noorheroes://ramadan/eid`.
- **Loading/Empty/Error:** loading state during card generation (potentially a longer server-side rendering call); error state with retry for generation failure.

## 11. NextJS Requirements
N/A.

## 12. API Contract
`GET /v1/ramadan/campaign-status` (B-01, re-sync source), `POST /v1/ramadan/eid-cards` (B-07).

## 13. Database Requirements
No new local table — reuses K-01's campaign-status cache entity for phase/date state.

## 14. Validation
N/A beyond standard response validation.

## 15. Authentication
Standard session for Countdown/Home/Reveal; Parent Gate step-up (`:core:security`) specifically for Card Generator.

## 16. Authorization
Card generation requires the Parent Gate step-up — a child alone cannot trigger it.

## 17. Error Handling
Card-generation failure → clear retry prompt, never a silently-broken share action.

## 18. Offline First
Countdown/Home render from K-01's cached phase state when offline; Card Generator requires connectivity (generation is a live server call, consistent with B-07's §17 "N/A — requires a live connection").

## 19. Local Data
Reuses K-01's `RamadanCampaignCacheEntity`.

## 20. Localization
"Eid Mubarak" and all Eid-mode copy fully localized across En/Hi/Ar/Ur per the provided §2.5 image-generation prompt's bilingual specification.

## 21. RTL
Full RTL mirroring for Arabic/Urdu, per the §2.5 Arabic prompt's explicit layout description.

## 22. Analytics
`ramadan_eid_countdown_viewed`, `ramadan_eid_mode_entered`, `ramadan_eid_reward_revealed`, `ramadan_eid_card_generated` per §1.19.

## 23. Performance
Celebratory animation/particle effects (per §2.1's "non-startling celebratory flourishes") must be GPU-efficient and not cause jank/ANR on lower-end devices — profile against `CORE_CRASH_INSTRUCTIONS.md`'s ANR-prevention guidance; card-generation loading state must not block the UI thread.

## 24. Security
Card Generator's Parent Gate requirement is enforced client-side as UX gating but is not the actual security boundary — B-07 independently requires the elevated session server-side regardless of client state.

## 26. Library Requirements
Kotlin, Jetpack Compose, Hilt, Retrofit + OkHttp. Reuses `:core:security`'s existing Parent Gate component. No new libraries.

## 27. Testing
Unit: phase-transition-to-Eid-mode derivation from K-01's shared state. **Mandatory** integration test: simulate an admin override between two app-open cycles and confirm the UI reflects the corrected date on the second open without any special-case code path. UI test: Parent Gate correctly blocks Card Generator access without step-up.

## 28. Documentation
KDoc on `EidCardViewModel` noting the re-sync behavior depends entirely on K-01's always-fetch-fresh pattern.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Build Eid Countdown and Eid Home Screens**
Objective: Phase-driven rendering from K-01's shared ViewModel. Files to Create: `presentation/eid/EidCountdownScreen.kt`, `presentation/eid/EidHomeScreen.kt`. Dependencies: K-01. Tests: phase-transition UI tests. Definition of Done: tests pass.

**Task 02 — Build Eid Reward Reveal Screen**
Objective: Reveal interaction with accessibility-equivalent non-visual path. Files to Create: `presentation/eid/EidRewardRevealScreen.kt`. Dependencies: Task 01. Tests: accessibility test. Definition of Done: test passes.

**Task 03 — Implement `GenerateEidCardUseCase`**
Objective: Calls B-07, Parent-Gate-gated. Files to Create: `domain/usecase/GenerateEidCardUseCase.kt`. Tests: Parent-Gate-enforcement UI test. Definition of Done: test passes.

**Task 04 — Build `EidCardGeneratorScreen` and `EidCardViewModel`**
Objective: Generation flow with loading/error states. Files to Create: `presentation/eid/EidCardGeneratorScreen.kt`, `presentation/eid/EidCardViewModel.kt`. Dependencies: Task 03. Tests: generation-flow integration test. Definition of Done: test passes.

**Task 05 — Verify Admin-Override Re-Sync Behavior**
Objective: Confirm no locally-persisted "final" Eid date resists refresh. Dependencies: K-01. Tests: **mandatory** — simulated-override re-sync test. Definition of Done: test passes.

**Task 06 — Wire Navigation and Deep Link**
Objective: `noorheroes://ramadan/eid`. Files to Modify: nav-graph. Dependencies: Task 01. Tests: deep-link test. Definition of Done: test passes.

**Task 07 — Add Localization, Analytics, Performance Pass, and Full Test Suite**
Objective: Complete §20/§22/§23/§27 coverage. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm zero locally-cached "final" Eid date logic exists that could resist a server-side correction. Definition of Done: checklist in §30 checked.

## 30. Final Verification Checklist
- [ ] Admin-override re-sync verified across two simulated app-open cycles — mandatory test passing
- [ ] Card Generator blocked without Parent Gate step-up
- [ ] Celebratory animations profiled for jank/ANR-free performance
- [ ] Full En/Hi/Ar/Ur localization and RTL mirroring per the provided image prompt

## 31. Definition of Done
Eid's transition, celebration, and card-sharing moment render joyfully and correctly re-sync to any last-minute moon-sighting correction, entirely through the same server-driven state pattern established at K-01.
