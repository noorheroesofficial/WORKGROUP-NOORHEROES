# K-04 — Auto-Unlock Detection & Celebration Notification

## 1. Feature Context
NoorHeroes KMP app (Android/iOS). Part of Feature A.12 — Avatar System. Detects server-side criteria-based unlocks (granted by B-02's Unlock Evaluation Engine) via response diffing, surfaces an in-app celebration when appropriate, and handles push-notification deep-link landing on the newly-unlocked item.

## 2. Parent Feature
A.12 Avatar System — KMP App (Android/iOS)

## 3. Sub-feature
K-04 Auto-Unlock Detection & Celebration Notification

## 4. Objective
Implement diffing-based auto-unlock detection against successive `GET /v1/children/{id}/inventory` responses, firing `avatar_item_auto_unlocked` and an in-app celebration when the app is foregrounded, plus notification deep-link handling — backing FR-8 and PRD §6.6/§7 item 5.

## 5. Business Requirements
- The child is never required to manually "claim" an avatar-item unlock — auto-unlock is detected and surfaced automatically (FR-8).
- Detection is diffing-based: since the unlock itself happens server-side asynchronously (B-02), the client compares each fresh inventory response's owned-items list against the previously-cached list to identify newly-owned items.
- If the app is foregrounded when a new item is detected, an in-app celebration surfaces; otherwise the item is simply discoverable next time the Avatar screen opens.
- A missed/failed notification never affects the underlying unlock — the grant itself (server-side `child_inventory` row, B-02) is authoritative regardless of notification delivery (PRD §1.11 Error Handling).
- Notification deep link lands directly on the newly-unlocked item's detail (`noorheroes://avatar/item/{itemId}`).

## 6. Existing Architecture
Extends `feature-avatar`/`feature-avatar-domain` established in K-01–K-03. The diffing pattern mirrors the platform's general "client detects server-side async state change via response comparison" approach; the celebration-modal presentation style follows the same non-alarming, joyful, growth-themed visual language established for badge/streak celebrations in A.6/A.7 (Dua Master badge celebration, Noor Garden milestone reveal). Push notification delivery itself is owned by the existing `notifications` feature module (not re-implemented here) — this sub-feature only owns the landing-target behavior and the client-side diffing detection that can independently surface a celebration even without a successfully-delivered push.

## 7. Existing Code to Reuse
- `AvatarViewModel`/`InventoryRepository`/`avatar_inventory_cache` (K-01)
- `core-navigation` deep-link dispatch pattern (`noorheroes://` scheme handler)
- `core-analytics` `AnalyticsTracker`
- Existing `notifications` feature module's landing-target registration mechanism (used elsewhere for other feature deep links)

## 8. Files to Create
- `feature-avatar/src/commonMain/kotlin/.../unlock/AutoUnlockDiffDetector.kt`
- `feature-avatar/src/commonMain/kotlin/.../unlock/AutoUnlockCelebrationModal.kt` (Composable)
- `feature-avatar-domain/src/commonMain/kotlin/.../DetectNewlyOwnedItemsUseCase.kt`
- `feature-avatar/src/commonTest/kotlin/.../AutoUnlockDiffDetectorTest.kt`

## 9. Files to Modify
- `feature-avatar/src/commonMain/kotlin/.../data/InventoryRepository.kt` (K-01) — invoke `AutoUnlockDiffDetector` after each successful `getInventory()` fetch, comparing against the previously-cached `avatar_inventory_cache` state before overwriting it
- Existing `notifications` feature module's deep-link landing-target registry — register `noorheroes://avatar/item/{itemId}`

## 10. KMP Requirements
- `AutoUnlockDiffDetector.detectNewlyOwned(previous: List<OwnedItem>, current: List<OwnedItem>): List<OwnedItem>` — pure function comparing item ID sets, returning items present in `current` but absent from `previous`.
- Invoked by `InventoryRepository` immediately after each successful inventory fetch and immediately before the fetched response overwrites the cached previous state (ordering is critical — diffing must always compare against the *prior* cache, never against itself).
- For each newly-detected item, fire `avatar_item_auto_unlocked` via `AnalyticsTracker.logEvent()` regardless of foreground state.
- If the app is foregrounded at detection time, present `AutoUnlockCelebrationModal` (gentle, non-jarring reveal, consistent with the platform's Character Evolution/badge-celebration visual language, not an aggressive flash/strobe effect).
- If the app is backgrounded, rely on the existing `notifications` module's push delivery for the primary discovery path; the diffing detector still runs on next foreground/fetch and will simply find the item already reflected as owned (no duplicate celebration if the child already saw the item via the notification).
- Notification deep-link landing target `noorheroes://avatar/item/{itemId}` navigates directly to the item's (now-owned) detail view within the Avatar Screen.

## 11. Backend Requirements
Consumes `GET /v1/children/{id}/inventory` (B-01); the underlying grant is produced asynchronously by B-02's Unlock Evaluation Engine — this sub-feature has no direct dependency on B-02's internals beyond the eventual reflection in B-01's response.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
No new endpoint; consumes the same `GET /v1/children/{id}/inventory` (B-01) already used by K-01, applying diff detection as a side effect of each fetch.

## 14. Database Requirements (Local)
Reuses `avatar_inventory_cache` (K-01) as the "previous state" comparison baseline — no new local table, but the write-ordering requirement (diff-before-overwrite) is a critical implementation detail documented explicitly in this task.

## 15. Validation
Unit test (P0, mandatory per PRD §7 Android prompt item 5): feed two sequential mocked inventory responses, the second containing exactly one additional owned item, and assert `AutoUnlockDiffDetector` correctly identifies exactly that one new item — no false positives from re-ordering, no false negatives from a changed-but-not-new item (e.g., an equip-state change on an already-owned item must not be misidentified as a new unlock).

## 16. Authentication
Reuses shared `core-network` Bearer token attachment (inherited from K-01's inventory fetch).

## 17. Authorization
N/A at UI layer.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Notification delivery fails/is missed | Item still discoverable via diffing on next Avatar screen open/fetch; grant itself unaffected (§1.11) |
| App backgrounded at unlock-detection time | No in-app celebration shown; push notification (if delivered) is the primary discovery path; diffing still logs `avatar_item_auto_unlocked` |
| Two items unlocked between fetches | Both correctly identified by the diff (not just the first); celebration handles a multi-item unlock gracefully (queued or combined presentation, not a dropped second item) |
| Diff baseline missing (first-ever fetch, fresh install) | No false "newly unlocked" celebration fires for a brand-new child's initial owned-items set — the detector must treat an empty/absent previous state as "no diff to report," not "everything is new" |

## 19. Offline First
Diff detection only runs on a successful network fetch (it requires two real response snapshots to compare); it does not run against purely-cached/offline reads, consistent with the PRD's "auto-unlock evaluation requires connectivity" principle (§1.14).

## 20. Local Data
```
GET /v1/children/{id}/inventory (fresh fetch)
   ↓
AutoUnlockDiffDetector.detectNewlyOwned(cached avatar_inventory_cache, fresh response)
   ↓
[if new items found] → fire analytics + celebration (if foregrounded)
   ↓
Overwrite avatar_inventory_cache with fresh response
```

## 21. Localization
Celebration modal copy ("You unlocked a new outfit! 🎉"-style text) resolved via string resources (English, Hindi, Arabic, Urdu).

## 22. RTL
Celebration modal layout mirrors correctly for RTL locales; verified via a dedicated RTL layout test.

## 23. Analytics
`avatar_item_auto_unlocked` (fired on diff detection, regardless of foreground state), `avatar_unlock_notification_shown` (fired when the celebration modal is actually presented) via `AnalyticsTracker.logEvent()`.

## 24. Performance
Diffing is a simple set-comparison over a typically-small owned-items list (no meaningful performance risk); must not block the inventory-fetch response path from updating the UI (run diff detection as a non-blocking side effect, not a gate on rendering the fresh state).

## 25. Security
No new sensitive data handling.

## 26. Library Requirements
Compose Multiplatform, Koin, kotlinx-coroutines, existing `notifications` module's deep-link registration API.

## 27. Testing
- Unit (P0): two-sequential-mocked-responses diff test, asserting exactly the correct new item is identified (per PRD §7 item 5).
- Unit: empty/absent-baseline case does not produce false "everything is new" celebration.
- Unit: equip-state-only change on an already-owned item is not misidentified as a new unlock.
- Integration: multi-item simultaneous unlock correctly identifies all new items, not just the first.
- Integration: notification deep link `noorheroes://avatar/item/{itemId}` navigates to the correct item detail.

## 28. Documentation
KDoc on `AutoUnlockDiffDetector` explicitly explaining the diff-before-overwrite ordering requirement and why it is safety-critical for correct detection.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `AutoUnlockDiffDetector`**
- Objective: pure diffing function comparing two owned-items snapshots.
- Files to Create: `AutoUnlockDiffDetector.kt`
- Implementation Details: set-difference on item IDs; explicit handling of empty/absent baseline.
- Tests (P0): mandatory two-response diff test.
- Definition of Done: P0 test passes; empty-baseline edge case verified.

**Task 02 — Implement `DetectNewlyOwnedItemsUseCase`**
- Objective: domain-layer wrapper invoking the detector with the correct before/after snapshots sourced from the repository layer.
- Files to Create: `DetectNewlyOwnedItemsUseCase.kt`
- Definition of Done: use case correctly orchestrates detector invocation with proper diff-before-overwrite ordering.

**Task 03 — Wire Diff Detection into `InventoryRepository`**
- Objective: invoke the use case as a side effect of every successful `getInventory()` fetch, before cache overwrite.
- Files to Modify: `InventoryRepository.kt` (K-01)
- Do Not Change: do not reorder the diff-then-overwrite sequence — reversing it silently breaks detection.
- Tests: integration test confirming correct ordering via a fixture sequence.
- Definition of Done: repository correctly triggers detection on every fetch without altering K-01's existing fetch/cache contract.

**Task 04 — Build `AutoUnlockCelebrationModal` Composable**
- Objective: gentle, non-jarring celebration reveal for foregrounded detection.
- Files to Create: `AutoUnlockCelebrationModal.kt`
- Localization/RTL: per §21/§22.
- Analytics: `avatar_unlock_notification_shown` on presentation.
- Tests: UI test for correct rendering, including multi-item unlock presentation.
- Definition of Done: modal renders correctly and matches the platform's established celebration visual language.

**Task 05 — Register Notification Deep-Link Landing Target**
- Objective: `noorheroes://avatar/item/{itemId}` routes to item detail.
- Files to Modify: existing `notifications` module's deep-link landing-target registry.
- Definition of Done: notification tap correctly lands on the specified item's detail view.

**Task 06 — Final Code Review**
- Do Not Change: existing `notifications` module's core push-delivery mechanism (only register a new landing target).
- Expected Result: PR merge-ready.

## 30. Definition of Done
Auto-unlock detection reliably identifies newly-owned items via response diffing, fires correct analytics regardless of foreground state, presents a gentle celebration when foregrounded, and correctly routes notification deep links — with the underlying grant remaining authoritative regardless of notification delivery success.

## 31. Final Verification Checklist
- [ ] Diff detector correctly identifies newly-owned items across two sequential mocked responses (P0 test passing)
- [ ] Empty/absent baseline does not produce a false "everything is new" celebration
- [ ] Equip-state-only changes are not misidentified as new unlocks
- [ ] Multi-item simultaneous unlock correctly identifies all new items
- [ ] Diff-before-overwrite ordering verified and documented
- [ ] Celebration modal renders gently, non-jarringly, matching platform visual language
- [ ] Notification deep link lands on correct item detail
- [ ] Localization (EN/HI/AR/UR) and RTL verified
- [ ] Analytics events wired via `AnalyticsTracker`
