---
id: STORY-019
epic: EPIC-004
kind: feature
title: Implement ChoiceEventRepository with Offline Outbox & Sync
status: ready
priority: P0
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
depends_on: [STORY-018]
produces: [repo.choice-event]
consumes: [api.choice-event]
created: 2026-09-29
---

## User Story
As the story platform, I want choice selections recorded durably via a fire-and-forget repository with a local offline outbox, so that editorial analytics are reliably delivered to the backend (B-05) without ever blocking player playback or losing data during offline use.

## Acceptance Criteria
- [ ] AC1: Given a call to `ChoiceEventRepository.recordChoice(...)`, the method enqueues the event into the local persistent outbox and launches a background sync job, returning immediately to the caller (`< 10ms`).
- [ ] AC2: Given every choice event, a persistent cryptographically random UUID v4 `clientEventId` is created and stored, preventing duplicate tallying on retry or resubmission.
- [ ] AC3: Given an online network connection, `POST /v1/content/{id}/choice` is invoked with `clientEventId`, `choicePointId`, and `selectedOptionId`. Upon HTTP 200, the outbox record is marked synced or purged.
- [ ] AC4: Given an offline or intermittent connection (HTTP 5xx, timeout, socket error), the event remains persisted in `PendingChoiceEvent` storage with status `PENDING`.
- [ ] AC5: Given `syncPendingEvents()` triggered on network reconnect, all queued events are dispatched in FIFO order with exponential backoff and jitter.
- [ ] AC6: Given any network failure during `recordChoice`, no exception is bubbled up to the player viewmodel or UI layer.

## Technical Notes
- Files in scope:
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/data/remote/ChoiceEventApi.kt`
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/data/repository/ChoiceEventRepositoryImpl.kt`
  - `feature/feature-stories/src/commonTest/kotlin/com/noorheroes/feature/stories/data/ChoiceEventRepositoryTest.kt`
- Conforms to contracts `api.choice-event` and `repo.choice-event`.
- Uses Ktor client and `core-datastore` outbox persistence pattern (mirroring K-07).

## Test Approach
- Unit: Verify `recordChoice` returns immediately and writes to local store.
- Unit: Verify `clientEventId` UUID v4 generation and reuse across sync attempts.
- Integration: Simulate offline recording followed by reconnect, verifying exact single network dispatch per queued event.

## Out of Scope
- Branch segment resolution (STORY-018).
- Overlay UI display (STORY-020).
