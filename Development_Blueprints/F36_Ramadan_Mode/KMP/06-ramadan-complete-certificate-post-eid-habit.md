# K-06 — Ramadan Complete Certificate & Post-Eid Habit Transition

## 1. Feature Context
Closes out the season with a shareable completion certificate and a gentle, 14-day-window transition into A.7's existing Habit Builder — turning Ramadan's momentum into a lasting habit rather than a hard stop, without building any parallel habit-setup flow.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
2.6 Ramadan Complete Certificate & Post-Eid Habit Transition (ID: **K-06**)

## 4. Objective
Build the Ramadan Complete Certificate screen (calling B-07) and the Post-Eid "Keep the Habit" screen that hands off into A.7's existing Habit Builder.

## 5. Business Requirements
- §1.18 Screens 13-14: Ramadan Complete Certificate, Post-Eid "Keep the Habit."
- §3.3/§9: certificate generation reuses A.11's Share Card Service pattern (via B-07) — no parallel pipeline.
- §1.4: post-Eid habit-continuation rate (active 14 days post-Eid) ≥ 50% target — this screen is the primary lever for that metric.
- §12.6: certificate reuses A.11's exact PII-exclusion guarantee.

## 6. Existing Architecture
`:feature:ramadan` module; Post-Eid transition hands off directly into A.7's existing Habit Builder screen/flow — this sub-feature owns only the transition prompt, not any habit-configuration logic.

## 7. Existing Code to Reuse
- A.7's Habit Builder screen/ViewModel (navigation target, not reimplemented)
- K-05's `GenerateEidCardUseCase` pattern (structural reference for certificate generation, distinct endpoint)
- `:core:security`'s Parent Gate component

## 8. Files to Create
- `feature/ramadan/presentation/certificate/RamadanCertificateScreen.kt`
- `feature/ramadan/presentation/certificate/RamadanCertificateViewModel.kt`
- `feature/ramadan/domain/usecase/GenerateCertificateUseCase.kt`
- `feature/ramadan/presentation/posteid/PostEidHabitTransitionScreen.kt`

## 9. Files to Modify
- `:core:navigation`'s nav-graph — register Certificate screen (reachable from Eid Home and Journey Map) and Post-Eid screen (reachable from Home during the 14-day post-Eid tail), with the Post-Eid screen's primary CTA navigating into A.7's existing Habit Builder route

## 10. KMP Requirements
- **UI/Screen:** Certificate preview/share screen, Parent-Gate-gated; Post-Eid transition screen shown on Home during the `post_eid_tail` phase (sourced from K-01's shared campaign state).
- **State/ViewModel:** `RamadanCertificateViewModel` calls `GenerateCertificateUseCase` → B-07; no local rendering of certificate content beyond displaying the returned `certificate_url`.
- **Use Case/Repository:** `GenerateCertificateUseCase` → `RamadanRepository.generateCertificate()` → B-07.
- **Navigation:** Post-Eid screen's CTA navigates directly into A.7's existing Habit Builder entry route — no intermediate Ramadan-specific habit-setup screen.
- **Loading/Empty/Error:** loading state during certificate generation; error state with retry.

## 11. NextJS Requirements
N/A.

## 12. API Contract
`POST /v1/ramadan/certificates` (B-07).

## 13. Database Requirements
No new local table required — certificate URL displayed transiently from the API response; not persisted client-side beyond the current screen session.

## 14. Validation
N/A beyond standard response validation.

## 15. Authentication
Parent Gate step-up (`:core:security`) required before certificate generation, mirroring B-07's server-side requirement.

## 16. Authorization
Certificate generation scoped to the requesting parent's own family's children.

## 17. Error Handling
Generation failure (e.g., zero completed nights) → clear, encouraging message (never framed as a shortfall/failure on the child's part) with guidance rather than a raw error.

## 18. Offline First
N/A — generation requires connectivity, consistent with B-07.

## 19. Local Data
N/A.

## 20. Localization
Certificate preview labels and Post-Eid transition copy fully localized across En/Hi/Ar/Ur.

## 21. RTL
Full RTL layout for both screens.

## 22. Analytics
`ramadan_certificate_generated`, `ramadan_certificate_shared`, `ramadan_post_eid_habit_transition_shown` per §1.19.

## 23. Performance
Certificate image/PDF preview loads asynchronously off the main thread; no blocking network call on screen composition.

## 24. Security
Client-side mirrors B-07's PII-exclusion guarantee only by displaying exactly what the server returns — never composing any additional child-identifying overlay text client-side.

## 26. Library Requirements
Kotlin, Jetpack Compose, Hilt, Retrofit + OkHttp, Coil (or existing image-loading library) for certificate preview. No new libraries.

## 27. Testing
Unit: `GenerateCertificateUseCase` request/response handling. UI test: certificate preview displays only server-supplied fields, no client-composed PII overlay (mirrors B-07's guarantee). Integration: full Post-Eid → A.7 Habit Builder hand-off navigates correctly and only during the `post_eid_tail` phase window.

## 28. Documentation
KDoc noting the Post-Eid screen must never contain its own habit-configuration logic — it is a pure navigation hand-off.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `GenerateCertificateUseCase`**
Objective: Calls B-07, Parent-Gate-gated. Files to Create: `domain/usecase/GenerateCertificateUseCase.kt`. Tests: use-case unit tests. Definition of Done: tests pass.

**Task 02 — Build `RamadanCertificateScreen` and ViewModel**
Objective: Preview/share flow with loading/error states. Files to Create: `presentation/certificate/RamadanCertificateScreen.kt`, `presentation/certificate/RamadanCertificateViewModel.kt`. Dependencies: Task 01. Tests: UI tests for loading/error/success states. Definition of Done: tests pass.

**Task 03 — Build `PostEidHabitTransitionScreen`**
Objective: Pure navigation hand-off into A.7's Habit Builder, phase-gated to `post_eid_tail`. Files to Create: `presentation/posteid/PostEidHabitTransitionScreen.kt`. Dependencies: K-01's shared campaign state. Tests: phase-gating test. Definition of Done: test passes.

**Task 04 — Wire Navigation into A.7's Habit Builder**
Objective: Confirm exact route/entry point, wire hand-off. Files to Modify: nav-graph. Dependencies: Task 03. Tests: navigation integration test. Definition of Done: test passes.

**Task 05 — Add Localization, Analytics, and Full Test Suite**
Objective: Complete §20/§22/§27 coverage. Definition of Done: all green in CI.

**Task 06 — Final Code Review**
Objective: Confirm zero habit-configuration logic exists in this module — purely a hand-off. Definition of Done: checklist in §30 checked.

## 30. Final Verification Checklist
- [ ] Certificate preview displays only server-supplied fields, no client-composed PII
- [ ] Post-Eid transition shown only during the `post_eid_tail` phase window
- [ ] Hand-off navigates correctly into A.7's existing Habit Builder with zero duplicated logic
- [ ] Generation-failure state is encouraging, never shame-framed

## 31. Definition of Done
The season closes with a shareable, PII-safe certificate and a frictionless, non-duplicative path into the platform's permanent habit-tracking experience.
