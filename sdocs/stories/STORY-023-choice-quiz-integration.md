---
id: STORY-023
epic: EPIC-004
kind: feature
title: Full Integration Verification, RTL Mirroring, and Zero-Missing Scenarios
status: ready
priority: P0
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
depends_on: [STORY-018, STORY-019, STORY-020, STORY-021, STORY-022]
produces: []
consumes: [domain.branch-resolution, repo.choice-event, domain.story-player]
created: 2026-09-29
---

## User Story
As an engineering team, we want end-to-end integration tests, RTL layout audits, and a zero-missing scenario matrix across all interactive choice and quiz flows, so that K-04 is completely verified, robust, and compliant with all project invariants.

## Acceptance Criteria
- [ ] AC1: Given the end-to-end interactive choice flow, when a scripted choice point arrives:
  - Video pauses cleanly without frame drops or black frames on the underlying surface.
  - `ChoiceOverlay` renders matching `Choice.png`.
  - Selecting an option branches playback immediately without waiting for B-05 network completion.
  - Choice event is queued in local outbox and synced to `POST /v1/content/{id}/choice`.
- [ ] AC2: Given RTL locales (Arabic `ar`, Urdu `ur`), choice cards, option icons, text layout, and RTL flow mirror correctly without clipped glyphs or inverted punctuation.
- [ ] AC3: Given the defensive 3-option cap requirement:
  - Debug builds throw an assertion error if content ever defines >3 options.
  - Release builds truncate to the first 3 options and log an error without crashing.
- [ ] AC4: Given rapid repeated taps on an option card, exactly one selection event is recorded and dispatched.
- [ ] AC5: Given network offline status, choices are made seamlessly offline, queued in the datastore outbox, and flushed upon simulated reconnect.
- [ ] AC6: Given Design System rules (`NoorHeroes/docs/rule.md`), an automated lint audit verifies:
  - 0 raw color values (`#hex`, `Color(0x...)`).
  - 0 raw dimensions (`.dp`, `.sp`).
  - 0 raw shapes (`RoundedCornerShape(...)`).
  - 0 raw Material 3 components (`androidx.compose.material3.*`).
  - All source files are strictly `< 500 lines`.
  - 100% 4-locale parity across EN, AR, HI, UR strings.

## Technical Notes
- Files in scope:
  - `feature/feature-stories/src/commonTest/kotlin/com/noorheroes/feature/stories/integration/ChoiceQuizIntegrationTest.kt`
  - `feature/feature-stories/src/androidInstrumentedTest/kotlin/com/noorheroes/feature/stories/presentation/ChoiceOverlayRtlTest.kt`
- Validates all 8 items in the Blueprint K-04 verification checklist.

## Test Approach
- Integration: Full playback simulation with offline outbox queuing and reconnect sync.
- Snapshot / UI: RTL rendering in Arabic and Urdu.
- Audit Script: Automated script verifying zero raw tokens and file length compliance.

## Out of Scope
- Post-story completion screen (EPIC-006).
