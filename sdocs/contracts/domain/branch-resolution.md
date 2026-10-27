---
id: domain.branch-resolution
kind: type
title: Deterministic Story Branch Resolution Domain Model & Engine
status: draft
owner_story: STORY-018
version: 1
created: 2026-09-29
---

# Contract: domain.branch-resolution

- **Kind**: Domain / Type
- **Package**: `com.noorheroes.feature.stories.domain`
- **Owner Story**: `STORY-018`
- **Status**: Draft

## Domain Models

### `ChoiceOption`
```kotlin
data class ChoiceOption(
    val id: String,
    val text: String,
    val iconName: String? = null,
    val nextSegmentRef: String
)
```

### `ChoicePoint`
```kotlin
data class ChoicePoint(
    val id: String,
    val timestampMs: Long,
    val prompt: String,
    val options: List<ChoiceOption>
)
```

### `QuizMoment`
```kotlin
data class QuizMoment(
    val id: String,
    val timestampMs: Long,
    val questionId: String,
    val resumeTimestampMs: Long
)
```

### `BranchResolutionResult`
```kotlin
sealed interface BranchResolutionResult {
    data class Resolved(
        val choicePointId: String,
        val selectedOptionId: String,
        val nextSegmentRef: String
    ) : BranchResolutionResult

    data class Error(
        val reason: Reason
    ) : BranchResolutionResult {
        enum class Reason {
            OPTION_NOT_FOUND,
            EMPTY_OPTIONS,
            MALFORMED_CHOICE_POINT
        }
    }
}
```

## Service Interface: `BranchResolver`

```kotlin
interface BranchResolver {
    /**
     * Deterministically resolves the next story segment based on learner selection.
     * Must be 100% client-side, pure-function evaluation with zero network dependencies.
     * Enforces the max-3-options invariant:
     * - In debug: assertion fails loudly if options.size > 3
     * - In release: gracefully clamps to the first 3 options and resolves
     */
    fun resolve(
        choicePoint: ChoicePoint,
        selectedOptionId: String,
        isDebug: Boolean = false
    ): BranchResolutionResult
}
```

## Invariants
1. **Determinism**: Given the identical `(ChoicePoint, selectedOptionId)` pair, `resolve()` must always return the exact same `Resolved(nextSegmentRef)`.
2. **Defensive Option Cap**: In debug builds (`isDebug == true`), if `choicePoint.options.size > 3`, `resolve()` must throw an `IllegalArgumentException`. In release builds (`isDebug == false`), it must truncate to `choicePoint.options.take(3)` and log an error.
3. **Pure Execution**: No I/O, no network calls, no coroutine suspension required for branch computation.
