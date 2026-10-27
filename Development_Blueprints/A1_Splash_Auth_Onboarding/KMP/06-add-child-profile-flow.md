# K-06 — Add Child Profile Flow

> **Status:** ✅ **Implemented & Verified** (Live simulator verified on Android `emulator-5554` with live FastAPI backend)

## 1. Feature Context
The final data-entry step of onboarding: nickname, DOB, avatar, language, learning level, plus optional interests/goal/AI-voice/accessibility fields, looped for multiple children. Sets the foundation for all downstream age-band-gated content.

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
2.6 Add Child Profile Flow (ID: **K-06**)

## 4. Objective
Build the Add Child screen (with embedded Avatar/Interests/Learning-Level sub-steps), the Add-Another-Child loop, and Learning-Level/Interests confirmation summary, against B-06, with client-generated idempotency keys reused across retries and zero raw-age input anywhere.

## 5. Business Requirements
- FR-13: Required fields nickname/DOB/avatar/language/learning-level; no raw "age" input field anywhere — DOB-only, server-derived age band.
- FR-14: Optional interests/daily-goal/AI-voice-toggle (default OFF)/accessibility prefs.
- FR-15: Duplicate nicknames allowed only with explicit avatar/color disambiguation and parent confirmation.
- FR-17: Idempotency key generated client-side once per creation attempt, reused across retries.
- Screen note: Avatar grid filtered live by resulting age band as DOB changes; empty state before DOB entry shows "enter birthdate to see avatars for this age," not a generic/empty grid.
- Screen note: Add-Another-Child prompt defaults focus to "No," not "Yes" (avoid pressure-driven over-adding).

## 6. Existing Architecture
`core-network`'s `SyncOperation.CreateChild` (existing sealed-class member per `core-network` docs) — this flow's submission goes through the existing offline-first `SyncQueue` pattern already established for child creation, not a new bespoke submission path.

## 7. Existing Code to Reuse
- `core-network`: `SyncOperation.CreateChild`, `Patchable<T>` (not needed here, this is a create not a patch)
- `core-data`: `SyncQueue.enqueue()`, `FamilyRepository` (existing — extend with the new field set)
- `core-common`: `Ulid.randomULID(clock)` — **resolved architecture decision:** `CORE_COMMON_INSTRUCTIONS.md`'s `id` package is explicitly documented as "sortable unique ID generation (ULID) **and idempotency keys**," and `Ulid.randomULID(clock)` is the standardized existing utility (preferred over UUID specifically because it's lexicographically sortable by time). This is the correct, existing call to use for the idempotency key — not `UUID.randomUUID()`. Note this deliberately diverges from the PRD's own Android AI-code-generation prompt (§7 of the PRD, which says `UUID.randomUUID()`), because existing architecture takes precedence over the PRD's generic wording per this project's own rule 2 ("do not invent a new architecture when the existing architecture already supports the requirement").
- `core-ui`: `NoorSegmentedControl`, `NoorSlider`, `NoorToggle`, `ExpandableCard` (for "Optional details" collapsible section)

## 8. Files to Create
- `feature/onboarding/ui/AddChildScreen.kt` (with embedded Avatar/Interests/LearningLevel sub-step composables)
- `feature/onboarding/ui/AddAnotherChildPromptScreen.kt`
- `feature/onboarding/ui/LearningLevelInterestsConfirmScreen.kt`
- `feature/onboarding/viewmodel/AddChildViewModel.kt` (+ State/Event)
- `core-network/api/ChildProfileDtos.kt` — extend existing `ChildProfileCreateRequestDto`/`ChildProfileResponseDto` with DOB/avatar/interests/etc.
- `feature/onboarding/data/AvatarCatalogRepository.kt` (age-band-filtered avatar catalog — bundled or remote-cached)
- `test/feature/onboarding/AddChildViewModelTest.kt`
- `androidTest/feature/onboarding/AddChildScreenTest.kt`

## 9. Files to Modify
- `core-network/api/AuthApiService.kt` or dedicated `FamilyApiService.kt` — extend `createChild()` request/response DTOs to match B-06's extended contract, add `Idempotency-Key` header injection
- `core-data/repository/FamilyRepositoryImpl.kt` — extend `checkInHabit()`-sibling `createChild()` method with new fields, idempotency-key generation-once-and-reuse
- `core-navigation/Route.kt` — add `AddChildRoute`, `AddAnotherChildPromptRoute`, `LearningLevelConfirmRoute`

## 10. KMP Requirements
- Idempotency key: generate once via the shared ID utility at the start of the Add Child step (first field interaction or screen entry, per K-07's draft-persistence timing), persist it alongside the draft (K-07), reuse on every retry — never regenerate on resubmission, even across process death.
- DOB picker: Material3 `DatePicker` only, never a free-text field; on change, immediately re-filter the Avatar grid using a *client-side estimate* of age band purely for UI filtering responsiveness — but the `age_band` actually persisted/displayed anywhere authoritative always comes from the server's `201` response, never the client estimate (avoid the two silently diverging — label the client-side filter logic clearly as "display-filter only, not authoritative" in code comments).
- Avatar/Interest/Learning-Level are sub-steps embedded within the Add Child step's own navigation (a stepper/pager within one screen's ViewModel state), not separate full back-stack nav entries — matches §6.3's requirement.
- Duplicate-nickname conflict: on `409 DUPLICATE_NICKNAME`, show the modal with the existing child's summary (name, avatar) side-by-side; require the parent to alter the avatar/color or confirm intentional duplication before resubmitting with `confirmed_duplicate: true`.
- Add-Another-Child prompt: focus defaults to "No" — verify via Compose `FocusRequester` default state, not just visual styling.
- Offline: all fields fillable, Save disabled with "Connect to the internet to continue" until connectivity returns; submission enqueued via `SyncQueue.enqueue(SyncOperation.CreateChild(...))` which handles the actual retry/reconnect logic (do not build a parallel retry mechanism — this is exactly what `SyncQueue`/`WorkManager` integration already exists for).

## 11. Required API
- `POST /v1/identity/family/children` (B-06) — via the existing `SyncOperation.CreateChild` handler
- `GET /v1/identity/family/children` (B-06) — for the family-level summary used in the confirmation screen

## 12. Offline First
Full offline-fillable form; submission goes through `SyncQueue` for automatic reconnect-triggered retry, respecting the idempotency key established at step-start.

## 13. Local Data
Draft state (all Add Child fields across the multi-child loop) persisted via K-07's shared `OnboardingViewModel`-scoped DataStore mechanism — this sub-feature is a *consumer* of K-07's persistence layer, not a separate draft store.

## 14. Localization
Learning-level cards use plain-language descriptions (Beginner/Intermediate/Advanced-equivalent), fully localized, not numeric levels — avoid any hardcoded English fallback for these labels.

## 15. RTL
Avatar grid: 3 columns mobile / 5 columns tablet, mirrors correctly in RTL (grid flow direction, not just individual item mirroring). Interest chips wrap correctly in RTL reading order.

## 16. Analytics
Emit `add_child_started` (family_existing_child_count), `avatar_selected`/`interest_selected`/`learning_level_selected` (selection_id), `add_child_submitted` (has_optional_fields_filled), `add_child_succeeded` (age_band, latency_ms), `add_child_failed` (error_code), `add_another_child_prompted` (response).

## 17. Performance
Avatar grid re-filtering on DOB change must not cause visible jank — precompute/cache the age-band-to-avatar-set mapping rather than filtering a large catalog on every keystroke-equivalent DOB-picker interaction.

## 18. Security
`accessibility_prefs`/`interests` sent as structured, validated client-side objects (not free-text blobs) matching B-06's expected jsonb shape.

## 19. Testing
- Unit: idempotency key generated once, reused across simulated retries and a simulated process-death/restore (integration with K-07); duplicate-nickname modal only appears on `409`, never speculatively; Add-Another default-focus-is-No assertion; DOB-change re-filters the avatar grid using client-estimate only, never overwrites a server-confirmed `age_band`.
- UI: empty/partial/valid/saving/error states (Compose Test); duplicate-nickname modal with side-by-side comparison rendering.
- Integration (Robolectric): process-death mid-Add-Child, full state restoration including the reused idempotency key (shared test suite with K-07).

## 20. AI Coding Agent Implementation Steps

**Task 01 — Extend `ChildProfileCreateRequestDto`/Response and API Client**
Objective: Match B-06's extended contract, add `Idempotency-Key` header support. Follow: existing DTO/API-client conventions. Tests: DTO round-trip against B-06's documented shape. Definition of Done: typed, tested client contract.

**Task 02 — Confirm/Extend `SyncOperation.CreateChild` Handler**
Objective: Wire the new field set into the existing offline-first sync operation (per `core-network`'s documented `SyncOperation` sealed hierarchy). Follow: existing `SyncHandler<T>` interface (`handle`, `reconcile`, `onFailed`). Files to Modify: the existing `CreateChild` handler implementation. Tests: reconnect-triggered retry reuses the same idempotency key. Definition of Done: no parallel/duplicate retry mechanism exists alongside `SyncQueue`.

**Task 03 — Implement `AvatarCatalogRepository` with Age-Band Filtering**
Objective: Provide the avatar/interest catalog filtered by a client-side DOB-derived estimate. Follow: bundled-first pattern similar to K-02's intro content. Business Rules: clearly documented as display-filter-only, not authoritative. Tests: filter-correctness for each age band. Definition of Done: catalog available offline.

**Task 04 — Implement `AddChildViewModel`**
Objective: Orchestrate the multi-sub-step Add Child flow, idempotency-key lifecycle, duplicate-nickname handling. Follow: `BaseViewModel`, integrates with K-07's shared draft persistence. Business Rules: idempotency key generated once at step start, reused always. Tests: full matrix per §19. Dependencies: Tasks 01–03, K-07. Definition of Done: idempotency-key-reuse-across-process-death test passes (joint with K-07).

**Task 05 — Implement `AddChildScreen` with Embedded Sub-Steps**
Objective: Nickname/DOB/Avatar/Language/Learning-Level as one screen's internal stepper, not separate nav entries. Follow: `NoorHeroesTheme`, `core-ui` form components. Tests: covered by Task 08. Dependencies: Task 04. Definition of Done: back-stack shows one entry for the entire Add Child step, not one per sub-step.

**Task 06 — Implement Duplicate-Nickname Modal**
Objective: `409`-triggered modal with side-by-side comparison and `confirmed_duplicate` resubmission. Follow: `NoorDialog`. Tests: 409-only-trigger assertion. Dependencies: Task 04. Definition of Done: modal never appears speculatively.

**Task 07 — Implement Add-Another-Child Prompt & Confirmation Screens**
Objective: Default-focus-No prompt; per-child editable summary confirmation. Follow: `FocusRequester`, `ExpandableCard`. Tests: default-focus assertion. Dependencies: Task 04. Definition of Done: focus verified via instrumented test, not just visual inspection.

**Task 08 — Add Analytics Instrumentation**
Objective: All events in §16. Follow: `AnalyticsTracker`, ViewModel-only. Definition of Done: one call site per event.

**Task 09 — Add Full Test Suite**
Objective: Complete coverage per §19, including the joint Robolectric integration test with K-07. Definition of Done: all green in CI.

**Task 10 — Final Code Review**
Objective: Confirm zero raw-age input anywhere, idempotency-key lifecycle correctness, no parallel retry mechanism bypassing `SyncQueue`. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [x] No raw "age" input field anywhere in the UI or DTOs
- [x] Idempotency key generated once per Add-Child attempt, reused across retries and process death
- [x] Duplicate-nickname modal appears only on server `409`, never speculatively
- [x] Add-Another-Child prompt defaults focus to "No"
- [x] Avatar-grid DOB-based filtering is clearly client-estimate-only, never overwrites server-confirmed `age_band`
- [x] Submission goes through the existing `SyncQueue`/`SyncOperation.CreateChild`, no parallel retry logic
- [x] Full offline-fillable behavior verified
- [x] All analytics events in §16 emitted correctly

## 22. Definition of Done
Add Child (with all sub-steps and the multi-child loop) is live against B-06, fully offline-first via the existing `SyncQueue`, idempotency-safe across retries and process death, and hands off to the Screen Time/Notification primer and K-08 (Profile Picker). **(STATUS: IMPLEMENTED & VERIFIED)**
