# K-08 — Family Ramadan Report, Conversion Card & Family Member Invite

## 1. Feature Context
The family-wide closing experience: an aggregate-only progress view that structurally cannot become a sibling leaderboard, a printable end-of-Ramadan report, a soft never-blocking Day 28-30 conversion moment, and a read-only report link parents can share with extended family — four distinct screens unified by one rule: nothing here may ever pressure, compare, or interrupt.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
2.8 Family Ramadan Report, Conversion Card & Family Member Invite (ID: **K-08**)

## 4. Objective
Build the Family Ramadan Aggregate view, the printable Family Ramadan Report, the Day 28-30 Conversion Moment Card, and the Family Member Invite screen.

## 5. Business Requirements
- §1.18 Screens 17-20: Family Ramadan Aggregate, Family Ramadan Report (printable), Conversion Moment Card (Day 28-30), Family Member Invite.
- FR-13: Day 28-30 conversion moment shows a soft, never-blocking card, standard purchase-flow terms shown first.
- FR-14: Family member invites support a read-only Family Ramadan Report link.
- Edge Case 4: divergent fasting approaches across children → Aggregate reflects each child's own scope without implying comparison.
- Edge Case 7: trial lapses before day 28 → card simply doesn't apply, C.24's standard messaging takes over.
- Edge Case 8: invite link opened without the app installed → graceful install/account-context prompt, never a broken page.
- §2.2: Family Ramadan Aggregate — "warm family-wide view without ranking siblings," aggregate-only visualization.
- §7 Android AI prompt item 4 (mandatory): Aggregate renders from a DTO with no per-child-array field.

## 6. Existing Architecture
`:feature:ramadan` module; Conversion Card reuses C.24's existing purchase-flow entry point entirely — this sub-feature supplies only the trigger condition and card copy, never its own checkout logic.

## 7. Existing Code to Reuse
- C.24's existing purchase-flow screen/endpoint (Conversion Card's "Continue with [plan]" target)
- C.20's card pattern (Aggregate visualization)
- B.15's/A.1's existing invite-link handling pattern (if one exists for other read-only share links — confirm before building a new deep-link-resolution flow)

## 8. Files to Create
- `feature/ramadan/presentation/familyaggregate/FamilyRamadanAggregateScreen.kt`
- `feature/ramadan/presentation/familyaggregate/FamilyAggregateViewModel.kt`
- `feature/ramadan/presentation/familyreport/FamilyRamadanReportScreen.kt`
- `feature/ramadan/presentation/conversion/RamadanConversionCard.kt`
- `feature/ramadan/presentation/invite/FamilyMemberInviteScreen.kt`
- `feature/ramadan/domain/usecase/GetFamilyAggregateUseCase.kt`

## 9. Files to Modify
- `:core:navigation`'s nav-graph — register these four screens/components and the invite-link deep-link handler

## 10. KMP Requirements
- **UI/Screen:** Aggregate view (no per-child breakdown UI element of any kind — not just no array field, no comparative visualization at all); printable Report; Conversion Card as a dismissible, non-blocking component on Home/Dashboard; Invite screen generating a read-only link.
- **State/ViewModel:** `FamilyAggregateViewModel`'s state class **structurally excludes** a per-child list/array field — enforced via a reflection-style test (mandatory, mirrors B-06's server-side guarantee).
- **Conversion Card trigger logic:** shown only when both the Day 28-30 window (from K-01's phase state) AND an active trial (from C.24's existing trial-state check) are true; if the trial has already lapsed or converted, the card simply does not render — C.24's standard messaging takes over, with zero Ramadan-specific fallback UI (Edge Case 7).
- **Conversion Card non-blocking guarantee:** dismissible, never a modal that blocks navigation; standard purchase-flow terms shown before any Ramadan-specific framing, per FR-13.
- **Invite handling:** generates a read-only link; the link-open handler (for a recipient without the app) shows an install/account-context prompt rather than a 404/broken page (Edge Case 8) — coordinate with the platform's existing deferred-deep-link infrastructure if one exists rather than building a parallel one.
- **Offline First:** Aggregate/Report render from K-07's/B-06's cached family-aggregate data when offline.

## 11. NextJS Requirements
N/A.

## 12. API Contract
`GET /v1/ramadan/family-aggregate` (B-06). Conversion Card reuses C.24's existing endpoints entirely (no Ramadan-specific purchase endpoint). Invite-link generation — **flagged, do not guess:** no dedicated endpoint enumerated in PRD §3.4; confirm against the platform's existing family-invite mechanism (if A.1/C.21 already has one) before building a new one.

## 13. Database Requirements
No new local table — reuses B-06's aggregate response, cached transiently.

## 14. Validation
N/A beyond standard response validation.

## 15. Authentication
Standard authenticated parent session for all four screens.

## 16. Authorization
Aggregate/Report/Invite scoped to the requesting parent's own family; invite link itself is read-only for its external recipient (no write access granted).

## 17. Error Handling
Aggregate-fetch failure → fall back to last-cached aggregate; invite-link-open-without-app → graceful install prompt (Edge Case 8), never a broken/blank page.

## 18. Offline First
Aggregate/Report support offline read from cache; Conversion Card and Invite generation require connectivity (live trial-state and link-generation checks).

## 19. Local Data
Cached family-aggregate response (shared with K-07's Dashboard Tab summary card, single source, not duplicated).

## 20. Localization
Report, Conversion Card copy (with standard purchase terms shown first per FR-13), and Invite screen fully localized across En/Hi/Ar/Ur.

## 21. RTL
Full RTL layout for all four screens, including the printable Report's layout direction.

## 22. Analytics
`ramadan_family_report_viewed`, `ramadan_family_member_invited`, `ramadan_conversion_card_shown`, `ramadan_conversion_card_converted` per §1.19.

## 23. Performance
Reflection-style structural check for the no-per-child-array guarantee should run as a cheap unit test, not a runtime cost; Report's printable layout renders without blocking the UI thread.

## 24. Security
Invite link is read-only by construction — no token/permission escalation path exists for the external recipient; Conversion Card never bypasses C.24's existing purchase-flow security (payment terms, entitlement checks) since it reuses that flow entirely rather than reimplementing any part of it.

## 26. Library Requirements
Kotlin, Jetpack Compose, Hilt, Retrofit + OkHttp. Reuses C.24's existing purchase-flow SDK/library. No new libraries.

## 27. Testing
Unit: **mandatory** — reflection-style test confirming `FamilyAggregateViewModel`'s state has no per-child-array field (§7 item 4). UI test: Conversion Card renders only within the correct trial+window intersection and is fully dismissible/non-blocking; Aggregate view renders no comparative visualization for divergent-approach siblings (Edge Case 4). Integration: trial-lapsed-before-day-28 correctly suppresses the card with zero fallback UI (Edge Case 7); invite-link-without-app shows the graceful prompt (Edge Case 8).

## 28. Documentation
KDoc on `FamilyAggregateViewModel` stating the no-per-child-array contract explicitly, mirroring B-06's server-side documentation.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `GetFamilyAggregateUseCase`**
Objective: Fetch B-06's aggregate with offline-cache fallback. Files to Create: `domain/usecase/GetFamilyAggregateUseCase.kt`. Tests: use-case unit tests. Definition of Done: tests pass.

**Task 02 — Implement `FamilyAggregateViewModel` with No Per-Child State**
Objective: Structurally exclude any per-child array. Files to Create: `presentation/familyaggregate/FamilyAggregateViewModel.kt`. Dependencies: Task 01. Tests: **mandatory** — reflection-style no-per-child-array test. Definition of Done: test passes.

**Task 03 — Build `FamilyRamadanAggregateScreen` and `FamilyRamadanReportScreen`**
Objective: Aggregate-only visualization; printable report layout. Files to Create: `presentation/familyaggregate/FamilyRamadanAggregateScreen.kt`, `presentation/familyreport/FamilyRamadanReportScreen.kt`. Dependencies: Task 02. Tests: no-comparison-rendering UI test. Definition of Done: test passes.

**Task 04 — Build `RamadanConversionCard` with Trial+Window Gating**
Objective: Dismissible, non-blocking, correctly gated. Files to Create: `presentation/conversion/RamadanConversionCard.kt`. Existing Files to Reuse: C.24's purchase-flow entry point. Dependencies: K-01, C.24's trial-state check. Tests: **mandatory** — trial-lapsed-suppression test; non-blocking/dismissible test. Definition of Done: both pass.

**Task 05 — Confirm and Implement Invite-Link Generation/Handling**
Objective: Reuse existing family-invite infrastructure if present; graceful install prompt for no-app case. Files to Create: `presentation/invite/FamilyMemberInviteScreen.kt`. Dependencies: confirmed API contract. Tests: **mandatory** — Edge Case 8 graceful-prompt test. Definition of Done: test passes.

**Task 06 — Wire Navigation and Deep-Link Handling**
Objective: Register all four screens plus the invite deep link. Files to Modify: nav-graph. Dependencies: Task 03, Task 05. Tests: navigation/deep-link tests. Definition of Done: tests pass.

**Task 07 — Add Localization, Analytics, and Full Test Suite**
Objective: Complete §20/§22/§27 coverage, all mandatory tests included. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm zero comparative/ranking UI exists anywhere across the four screens, and zero Ramadan-specific purchase logic exists outside C.24's reused flow. Definition of Done: checklist in §30 checked.

## 30. Final Verification Checklist
- [ ] No per-child-array field in `FamilyAggregateViewModel`'s state — mandatory test passing
- [ ] Conversion Card correctly suppressed when trial has lapsed before day 28 — mandatory test passing
- [ ] Conversion Card is dismissible and never blocking, standard terms shown first
- [ ] Invite link opened without the app shows a graceful prompt, never a broken page — mandatory test passing
- [ ] Zero comparative/ranking visualization anywhere across all four screens

## 31. Definition of Done
Families close the season with a warm, comparison-free rollup and a genuinely optional, never-pressuring path to continue their subscription — both built entirely on existing, hardened platform mechanics.
