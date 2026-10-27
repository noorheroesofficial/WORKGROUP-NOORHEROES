---
id: domain.story-player
kind: type
title: Story Player Domain State Machine & Entities
status: draft
owner_story: STORY-013
version: 1
created: 2026-09-29
---

# Contract: domain.story-player

- **Kind**: Domain Type & State Machine
- **Owner Story**: `STORY-013`
- **Status**: Draft

## Sealed Player State Model

```kotlin
sealed interface PlayerState {
    data object Loading : PlayerState
    
    data class Buffering(
        val positionMs: Long,
        val durationMs: Long,
    ) : PlayerState
    
    data class Playing(
        val positionMs: Long,
        val durationMs: Long,
        val selectedCaption: String? = null,
        val selectedAudioTrack: String? = null,
        val activeSubtitleText: String? = null,
    ) : PlayerState
    
    data class Paused(
        val positionMs: Long,
        val durationMs: Long,
        val selectedCaption: String? = null,
        val selectedAudioTrack: String? = null,
        val activeSubtitleText: String? = null,
    ) : PlayerState
    
    data class ChoiceActive(
        val choicePointId: String,
        val positionMs: Long,
    ) : PlayerState
    
    data object QuizActive : PlayerState
    
    data class Unavailable(
        val reasonResId: String,
        val fallbackStoryId: String? = null,
        val fallbackStoryTitle: String? = null,
    ) : PlayerState
    
    data class Completed(
        val episodeId: String,
        val starsEarned: Int = 10,
    ) : PlayerState
}
```

## Player Events & Effects

```kotlin
sealed interface PlayerEvent {
    data object OnPlay : PlayerEvent
    data object OnPause : PlayerEvent
    data class OnSeek(val targetPositionMs: Long) : PlayerEvent
    data object OnToggleCaptions : PlayerEvent
    data class OnSelectAudioTrack(val language: String) : PlayerEvent
    data object OnToggleControls : PlayerEvent
    data object OnBackClicked : PlayerEvent
    data object OnRetry : PlayerEvent
}

sealed interface PlayerEffect {
    data object NavigateBack : PlayerEffect
    data class ShowToast(val message: String) : PlayerEffect
    data class OpenChoiceOverlay(val choicePointId: String) : PlayerEffect
}
```

## Invariants
1. `PlayerState` is the SOLE source of truth for both `KMPPlayerController` operations and Compose overlay visibility. No UI element may show "Playing" controls while the state is `Buffering`.
2. `client_event_id` is generated once at session init via secure UUID and never regenerated mid-session.
3. Scrub-ahead clamp restricts seeking beyond `furthestReachedPositionMs + tolerance` if `scrubRestricted` is true.
4. On fatal player error, state transitions immediately to `PlayerState.Unavailable` with child-friendly message and zero technical error text.
