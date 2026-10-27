# K-06 — Bedtime Notification Deep Link & Continue Listening

## 1. Feature Context
Owns the two navigation entry points into K-01's player triggered from outside the app: the "Tonight's bedtime story is ready 🌙" push notification (scheduled/sent by A.12, this feature owns only the landing destination) and a "continue listening" shortcut resuming the most recent in-progress bedtime content.

## 2. Parent Feature
Feature A.4 — Audio Bedtime Player & Bedtime Mode

## 3. Sub-feature
2.6 Bedtime Notification Deep Link & Continue Listening (ID: **K-06**)

## 4. Objective
Register `noorheroes://bedtime/{content_id}` and `noorheroes://bedtime/continue` deep links in `core-navigation`, routing correctly into K-01's `BedtimeAudioPlayerRoute` whether the app is cold-started or already running, and handling not-entitled/withdrawn-content edge cases gracefully.

## 5. Business Requirements
- §6.8: `noorheroes://bedtime/{content_id}` for "bedtime story ready" notification entry; `noorheroes://bedtime/continue` resumes the most recent in-progress bedtime content.
- §6.9: landing target for the "Tonight's bedtime story is ready 🌙" notification (sent ~30 min before the configured window start) — implemented by A.12, this feature only owns the deep-link destination.
- FR-14: deep link arriving outside the bedtime window does not force Bedtime Mode visuals unless explicitly toggled (consistent with K-03's resolution logic, which already accounts for entry point as one of its inputs).

## 6. Existing Architecture
`core-navigation`'s existing deep-link registry (the same mechanism A.3/K-03 uses for `noorheroes://stories/{episode_id}`) — this sub-feature registers two additional patterns following the identical convention, no new deep-link infrastructure.

## 7. Existing Code to Reuse
- `core-navigation`'s deep-link registration/dispatch mechanism (mirror A.3/K-03's `noorheroes://stories/{episode_id}` registration exactly)
- K-01's `BedtimeAudioPlayerRoute` (navigation target)
- K-07's `BedtimeRepository` (for resolving "most recent in-progress bedtime content" — confirm whether this data already exists via `PlaybackSessionManager`'s resume-position tracking, shared with A.3/K-03, or whether a small additive query is needed)

## 8. Files to Create
- `feature/bedtime-audio/navigation/BedtimeDeepLinkHandler.kt`
- `test/feature/bedtime-audio/BedtimeDeepLinkHandlerTest.kt`

## 9. Files to Modify
- `core-navigation/Route.kt` — register `noorheroes://bedtime/{content_id}` and `noorheroes://bedtime/continue` patterns, both resolving to `BedtimeAudioPlayerRoute`

## 10. KMP Requirements
- `noorheroes://bedtime/{content_id}`: resolves directly to `BedtimeAudioPlayerRoute(contentId)` — identical handling whether the app is cold-started (deep link resolved after app init) or already running (immediate navigation).
- `noorheroes://bedtime/continue`: resolves the most recent in-progress bedtime content via `PlaybackSessionManager`'s existing resume-position tracking (reused, not duplicated) filtered to Bedtime-category content, then navigates to `BedtimeAudioPlayerRoute` with that resolved `contentId`; if no in-progress bedtime content exists, falls back to the Bedtime Corner/Stories Bedtime category screen rather than a dead end.
- Not-entitled/withdrawn content via deep link: routes into K-01's existing safe-stop + alternative pattern (reuses K-01's `Unavailable` state handling, no separate error path for the deep-link case).
- Outside-window entry: `forceCalmMode` resolution (K-03) treats deep-link entry the same as any other entry point — no special-casing that would force calm mode simply because the entry came from a notification (the window/toggle inputs alone determine the result, consistent with FR-14).

## 11. Required API
**User API** — B-02 `GET /v1/content/{id}/manifest?format=audio` (via K-01, triggered after navigation resolves).

## 12. Offline First
Deep-link resolution itself requires no network call; the subsequent manifest fetch (K-01) follows K-01's existing offline-first behavior.

## 13. Local Data
Reuses `PlaybackSessionManager`'s existing resume-position store — no new local persistence.

## 14. Localization
No new localized strings (notification copy itself is owned by A.12).

## 15. RTL
Not applicable — this sub-feature is navigation-only, no new UI surface.

## 16. Analytics
`BedtimeAnalytics`: `bedtime_player_opened` with `entry_source="notification"` or `entry_source="continue_listening"` (extending K-01's existing event with the correct source value for these two entry points, not a new event).

## 17. Performance
Deep-link resolution must not block app cold-start beyond the existing navigation-graph resolution time already budgeted elsewhere in the app.

## 18. Security
Deep-link `content_id` is validated against the same entitlement checks K-01's manifest fetch already performs — a malformed or unauthorized `content_id` in the deep link cannot bypass entitlement, it simply surfaces K-01's existing `Unavailable`/error handling.

## 19. Testing
- Unit: deep-link pattern matching for both `noorheroes://bedtime/{content_id}` and `noorheroes://bedtime/continue`.
- Unit: "continue" resolution correctly filters to Bedtime-category in-progress content, falls back to the Bedtime Corner when none exists.
- Integration: cold-start deep-link resolution vs. already-running-app resolution both navigate correctly.
- Integration: deep link to withdrawn/not-entitled content routes into K-01's existing safe-stop pattern, not a raw crash or unhandled route.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Register the Two Deep-Link Patterns**
Objective: `noorheroes://bedtime/{content_id}` and `noorheroes://bedtime/continue` in `core-navigation`, both resolving to `BedtimeAudioPlayerRoute`. Files to modify: `core-navigation/Route.kt`. Follow: A.3/K-03's exact registration pattern. Tests: pattern-matching unit tests. Definition of Done: tests pass.

**Task 02 — Implement `BedtimeDeepLinkHandler` for "Continue" Resolution**
Objective: Resolve most recent in-progress bedtime content via `PlaybackSessionManager`, filtered to Bedtime category; fallback to Bedtime Corner if none. Files to create: `BedtimeDeepLinkHandler.kt`. Dependencies: Task 01, `PlaybackSessionManager`. Tests: resolution-with-data and no-data-fallback tests. Definition of Done: tests pass.

**Task 03 — Verify Cold-Start vs. Running-App Resolution Parity**
Objective: Both app states navigate identically. Dependencies: Task 01–02. Tests: integration tests for both states. Definition of Done: tests pass.

**Task 04 — Verify Not-Entitled/Withdrawn Deep-Link Handling**
Objective: Confirm routing into K-01's existing safe-stop pattern, no separate/duplicate error path. Dependencies: Task 01, K-01. Tests: withdrawn-content-via-deep-link integration test. Definition of Done: test passes.

**Task 05 — Extend `bedtime_player_opened`'s `entry_source` Values**
Objective: Correct `entry_source` value for notification and continue-listening entries. Dependencies: Task 01–02. Tests: fake-tracker assertion per entry point. Definition of Done: test passes.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §19. Definition of Done: all green.

**Task 07 — Final Code Review**
Objective: Confirm zero duplicated error-handling path for the deep-link case (reuses K-01's existing `Unavailable` state); confirm no entitlement bypass is possible via a crafted deep link. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [ ] Both deep-link patterns registered and correctly route to `BedtimeAudioPlayerRoute`
- [ ] "Continue" correctly resolves the most recent in-progress Bedtime-category content, with a sane fallback when none exists
- [ ] Cold-start and already-running-app resolution both work identically
- [ ] Not-entitled/withdrawn content via deep link reuses K-01's existing safe-stop pattern, no separate crash-prone path
- [ ] Deep-link entry does not bypass K-03's `forceCalmMode` resolution logic or force calm mode inappropriately
- [ ] `entry_source` correctly reflects `notification` vs. `continue_listening` on `bedtime_player_opened`

## 22. Definition of Done
The "bedtime story ready" notification and continue-listening shortcut both reliably land the child in K-01's player with correct content resolution, safe handling of withdrawn/not-entitled edge cases, and no entitlement bypass — using entirely the app's existing deep-link infrastructure.
