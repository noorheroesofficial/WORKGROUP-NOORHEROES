---
id: repo.choice-event
kind: repo
title: Choice Event Repository & Offline Outbox Interface
status: draft
owner_story: STORY-019
version: 1
created: 2026-09-29
---

# Contract: repo.choice-event

- **Kind**: Repository
- **Package**: `com.noorheroes.feature.stories.data`
- **Owner Story**: `STORY-019`
- **Status**: Draft

## Data Entities

### `PendingChoiceEvent`
```kotlin
data class PendingChoiceEvent(
    val clientEventId: String, // UUID v4 idempotency key
    val contentId: String,
    val choicePointId: String,
    val selectedOptionId: String,
    val timestampEpochMs: Long,
    val syncStatus: SyncStatus = SyncStatus.PENDING
) {
    enum class SyncStatus {
        PENDING,
        SYNCING,
        SYNCED,
        FAILED
    }
}
```

## Repository Interface: `ChoiceEventRepository`

```kotlin
interface ChoiceEventRepository {
    /**
     * Enqueues an interactive choice event into the local offline outbox and triggers
     * a fire-and-forget background synchronization attempt to POST /v1/content/{id}/choice.
     * MUST NEVER block the caller or delay player playback.
     */
    suspend fun recordChoice(
        contentId: String,
        choicePointId: String,
        selectedOptionId: String
    ): Result<Unit>

    /**
     * Synchronizes all pending choice events with the backend B-05 API.
     * Retries failed events with exponential backoff on reconnection.
     */
    suspend fun syncPendingEvents(): Result<Int>

    /**
     * Returns count of unsynced events in the local outbox.
     */
    suspend fun getPendingEventCount(): Int
}
```

## Invariants
1. **Fire-and-Forget**: Calling `recordChoice` must return immediately after writing to the local persistent store (or launching asynchronous sync job). It must never throw an uncaught network exception to the player.
2. **Idempotency**: Every recorded choice generates a persistent `clientEventId` (UUID v4) that is retained across retries to prevent duplicate server tallies per B-05 spec.
3. **Offline Resilience**: If the device is offline or the server returns 5xx/network timeout, the event remains in `PENDING` status in local storage and is flushed when network connectivity is restored.
