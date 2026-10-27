# Contract: domain.story-detail

- **Kind**: Domain Interface
- **Owner Story**: `STORY-007`, `STORY-008`
- **Status**: Stable

## StoryCatalogRepository Interface Extension
```kotlin
interface StoryCatalogRepository {
    // K-01
    suspend fun getStoriesLibrary(filter: StoryFilter): NoorResult<StoryLibraryResult>
    suspend fun getDownloadedStories(): List<StoryItem>
    
    // K-02
    suspend fun getStoryDetail(id: String): NoorResult<StoryDetail>
}
```

## Domain Entity Model
```kotlin
data class StoryDetail(
    val id: String,
    val seriesId: String,
    val title: String,
    val synopsis: String,
    val description: String?,
    val category: String,
    val ageBands: List<String>,
    val coverUrl: String?,
    val scholarApprovalStatus: String,
    val scholarApprovalTags: List<String>,
    val sourceReferences: List<String>,
    val episodes: List<EpisodeItem>,
    val relatedStories: List<StorySummaryItem>,
    val totalDurationSeconds: Int,
    val isBedtimeEligible: Boolean,
    val freeOrPremium: String,
    val isOffline: Boolean = false,
    val isWithdrawn: Boolean = false,
)

data class EpisodeItem(
    val id: String,
    val seriesId: String,
    val episodeNumber: Int,
    val title: String,
    val synopsis: String?,
    val format: String,
    val durationSeconds: Int,
    val isLocked: Boolean,
    val unlockCondition: String?,
    val isCompleted: Boolean,
    val progressSeconds: Int,
    val progressPercent: Float,
    val isBedtimeEligible: Boolean,
    val isPaywalled: Boolean = false,
    val thumbnailUrl: String? = null,
)
```

## Invariants
1. `isLocked` and `unlockCondition` are server-authoritative; the client NEVER re-computes or overrides them.
2. Lightweight refresh triggered `onResume` ensures episode unlocks reflect in real-time without screen reloads.
3. HTTP 410 maps to `isWithdrawn = true` and shows a graceful "no longer available" view.
