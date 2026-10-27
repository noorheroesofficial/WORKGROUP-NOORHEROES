---
id: EPIC-004
title: Interactive Choice & Quiz Moment Overlays
status: planned
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
prd_sections: ["1.7", "1.18", "2.1", "7.4", "7.9"]
depends_on: [EPIC-003]
created: 2026-09-29
---

## Description
Implements the in-player interactive choice and pause-and-quiz moment overlays (K-04) layered conditionally on top of K-03's `PlayerState.ChoiceActive` and `PlayerState.QuizActive`. Features:
1. **Deterministic Pure-Domain Branching**: `BranchResolver` evaluates next branch segment immediately using the manifest's `interactive_script`, ensuring playback is never blocked or stalled waiting for a network response.
2. **Defensive 3-Option Cap**: Hard-enforces maximum of 3 option cards per choice point. In debug builds, `require(options.size <= 3)` fails loudly; in release builds, it gracefully truncates to the first 3 options and logs an error to avoid crashing.
3. **No Countdown Pressure**: Reflects the Islamic moral ethos ("Take your time — there is no rush ✨") without countdown timers.
4. **Input Debouncing**: Rapid repeated taps are debounced so exactly one selection registers.
5. **Offline-Safe Outbox**: B-05 (`POST /v1/content/{id}/choice`) client is strictly fire-and-forget, writing to a persistent local outbox with UUID v4 idempotency keys, synced on reconnect.
6. **Shared Quiz Component Delegation**: `QuizMomentOverlay` delegates quiz rendering directly to a modular quiz engine delegate to eliminate duplicated UI logic.
7. **Visual Parity**: 1:1 match with `Screens/Mobile App/Stories/Choice.png` including dark scrim, `"💡 What would you do?"` badge, rounded cards, emoji badges, and full RTL layout mirroring.

## Stories
- STORY-018 — Implement Pure-Domain Deterministic BranchResolver
- STORY-019 — Implement ChoiceEventRepository with Offline Outbox & Sync
- STORY-020 — Implement ChoiceOverlay Composable with 3-Option Cap & Tap Debounce
- STORY-021 — Implement QuizMomentOverlay Delegating to Shared Quiz Delegate
- STORY-022 — Wire Choice and Quiz State Transitions into StoryPlayerViewModel
- STORY-023 — Full Integration Verification, RTL Mirroring, and Zero-Missing Scenarios

## Out of Scope
- Bedtime Mode ambient night sky, dimmed theme tokens, and sleep timer (deferred to K-05 / EPIC-005)
- Post-playback completion reward reveal, XP/points calculation, and streak triggers (deferred to K-06 / EPIC-006)
- Offline download manager integration and storage quota management (deferred to K-07 / EPIC-007)
