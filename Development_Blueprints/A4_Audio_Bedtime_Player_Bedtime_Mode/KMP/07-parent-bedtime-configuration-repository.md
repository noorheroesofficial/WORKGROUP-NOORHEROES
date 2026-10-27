# K-07 — Parent Bedtime Configuration Repository & Fail-Safe Caching

## 1. Feature Context
The single client-side data-access point for B-01's bedtime configuration, consumed by K-02 (sleep-timer ceiling), K-03 (window state for calm-mode resolution), and indirectly by A.3/K-05's overlay if it shares this same config source. Its most important property is failing safe: if the config can't be fetched, the app must default to NOT auto-forcing Bedtime Mode, never crash, and never block the Calm Mode toggle.

## 2. Parent Feature
Feature A.4 — Audio Bedtime Player & Bedtime Mode

## 3. Sub-feature
2.7 Parent Bedtime Configuration Repository & Fail-Safe Caching (ID: **K-07**)

## 4. Objective
Implement `BedtimeRepository.getConfig()` as a cached client for B-01's `GET /v1/parent-controls/{child_id}/bedtime`, applying the "changes apply at next session" caching rule, and a documented fail-safe default when the fetch fails.

## 5. Business Requirements
- §3.4: client caches aggressively (5–15 min); config changes apply at next session, not mid-session.
- §1.11 Error Handling: parent bedtime-window config fetch failure → player defaults to NOT forcing Bedtime Mode automatically (fails safe), but the explicit Calm Mode toggle remains available regardless.
- §1.10 Edge Case 4: parent narrows the bedtime window while a session is already in Bedtime Mode within the now-excluded time — current session remains in Bedtime Mode until exited; new window applies next session (this is a direct consequence of this repository's caching contract, not re-fetching mid-session).
- §12: Bedtime config tampering by a child is a write-side (B-01) concern; this repository only reads.

## 6. Existing Architecture
Reuses the existing parent-settings local cache mechanism already established for C.23 Parental Controls (confirmed pattern: DataStore or Room-backed local cache per `CORE_DATASTORE_INSTRUCTIONS.md`/`CORE_DATA_INSTRUCTIONS.md`) — this sub-feature adds a `BedtimeRepository` that follows the exact same local-cache-plus-remote-fetch pattern already used for other parent-controls data, rather than introducing a second caching mechanism.

## 7. Existing Code to Reuse
- Existing parent-settings local cache infrastructure (confirm exact class, e.g., a `ParentControlsLocalDataSource` or `DataStore`-backed cache used by C.23) — reuse directly
- `core-network`'s API client conventions (mirror A.3's `ManifestRepository`/`PlaybackHeartbeatRepository` client-construction pattern)
- `core/deps`-equivalent DI wiring (Hilt module registration, consistent with the rest of the KMP app)

## 8. Files to Create
- `feature/bedtime-audio/data/BedtimeRepository.kt` — `getConfig(childId): BedtimeConfig` (cached), exposing `windowStart`, `windowEnd`, `sleepTimerCeilingMinutes`, `allowUntilEpisodeEndsOption`, `autoSuggestDownload`
- `test/feature/bedtime-audio/BedtimeRepositoryTest.kt`

## 9. Files to Modify
None expected beyond DI registration (Hilt module) — this is new, additive infrastructure with no existing file requiring behavioral change.

## 10. KMP Requirements
- `getConfig(childId)`: cache-first read (5–15 min TTL) against B-01's endpoint; on cache miss, fetches remotely and updates the local cache.
- **Fail-safe default:** if the remote fetch fails (network error, `5xx`, timeout) and no valid cached value exists, `getConfig()` returns a safe-default `BedtimeConfig` with `windowStart = null`, `windowEnd = null` (i.e., "no auto-applied window") rather than throwing — callers (K-03) must never crash or block on this failure, and the Calm Mode manual toggle must remain available regardless of this fallback.
- Config-changes-apply-at-next-session rule: this repository does **not** poll or re-fetch mid-session; a cached value read at session start remains authoritative for that session's `forceCalmMode` resolution (K-03), even if the parent changes the config on another device mid-session (Edge Case 4).
- Reuses the existing parent-settings local cache store (no new local database/table) — if the existing cache infrastructure is keyed generically (e.g., a generic key-value parent-settings cache), this repository's config is stored under a namespaced key rather than introducing a dedicated new local table.

## 11. Required API
**User API** — B-01 `GET /v1/parent-controls/{child_id}/bedtime`.

## 12. Offline First
Bedtime-window configuration is cached locally so bedtime-mode resolution (K-03) and sleep-timer ceiling lookup (K-02) both work fully offline once an initial fetch has succeeded at least once; a fully offline first-ever session (never previously fetched) uses the fail-safe default.

## 13. Local Data
Reuses the existing parent-settings local cache — explicitly no new local store, table, or DataStore file introduced by this sub-feature.

## 14. Localization
Not applicable — data-layer only, no user-facing strings.

## 15. RTL
Not applicable.

## 16. Analytics
No new analytics events (this is a pure data-access layer; consuming screens emit their own events).

## 17. Performance
Cache-first reads avoid a network round-trip on every player launch; TTL (5–15 min) balances freshness against request volume for a value that changes infrequently.

## 18. Security
No new security surface — this repository only reads; B-01 enforces all write-side authorization. No sensitive data beyond the child's own bedtime schedule is cached (not treated as high-sensitivity PII, consistent with B-01's own data-classification).

## 19. Testing
- Unit: cache-hit path returns the cached value without a network call.
- Unit: cache-miss path fetches remotely and populates the cache.
- **Unit: fetch-failure fail-safe test** — simulate a network error with no valid cache present, assert `getConfig()` returns the safe-default (`null` window fields) rather than throwing.
- Unit: fetch-failure with a valid (possibly stale) cache present — assert the stale cached value is used rather than the fail-safe default (stale-but-valid data preferred over no data, consistent with the "apply at next session" rule not requiring real-time freshness).
- Integration: confirms no duplicate local storage mechanism is introduced — assert the underlying storage call sites match the existing parent-settings cache infrastructure's API, not a newly introduced one.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Confirm the Existing Parent-Settings Local Cache Infrastructure**
Objective: Identify the exact existing class/mechanism used for C.23 Parental Controls' local caching. Why: this sub-feature must reuse it, not duplicate it, per FR/architecture-reuse rules. Follow: `CORE_DATASTORE_INSTRUCTIONS.md`/`CORE_DATA_INSTRUCTIONS.md`. Definition of Done: exact reuse target identified and documented in code comments/PR description.

**Task 02 — Implement `BedtimeRepository.getConfig()` with Cache-First Read**
Objective: Cache-hit/cache-miss handling against B-01's endpoint, TTL 5–15 min. Files to create: `BedtimeRepository.kt`. Dependencies: Task 01. Tests: cache-hit and cache-miss unit tests. Definition of Done: tests pass.

**Task 03 — Implement the Fail-Safe Default Path**
Objective: Fetch failure with no valid cache returns a safe-default config, never throws. Dependencies: Task 02. Tests: **the fetch-failure fail-safe test** (signature test for this sub-feature). Definition of Done: test passes; confirm downstream (K-03) does not crash when consuming this fallback.

**Task 04 — Implement Stale-Cache-Preferred-Over-Fail-Safe Behavior**
Objective: A fetch failure with a valid (even if TTL-expired) cached value uses that cached value, not the null-window fail-safe. Dependencies: Task 02–03. Tests: stale-cache-preferred unit test. Definition of Done: test passes.

**Task 05 — Register DI Wiring**
Objective: Hilt module registration consistent with the rest of the app's repository DI pattern. Definition of Done: `BedtimeRepository` injectable into K-02/K-03.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §19, including the no-duplicate-storage-mechanism integration test. Definition of Done: all green.

**Task 07 — Final Code Review**
Objective: Confirm zero new local storage mechanism was introduced; confirm the fail-safe default is genuinely safe (never forces Bedtime Mode) and never throws. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [ ] `getConfig()` is cache-first with a 5–15 minute TTL
- [ ] Fetch failure with no valid cache returns a safe null-window default, never throws
- [ ] Fetch failure with a valid (possibly stale) cache uses the cached value in preference to the fail-safe default
- [ ] No new local storage mechanism introduced — reuses the existing parent-settings cache infrastructure
- [ ] Config read at session start remains authoritative for that session (no mid-session re-fetch), consistent with Edge Case 4
- [ ] `BedtimeRepository` correctly injectable into K-02 and K-03 via existing DI conventions

## 22. Definition of Done
K-02 and K-03 can reliably read the parent's bedtime configuration through a single, cache-first, fail-safe repository that never crashes, never forces Bedtime Mode on failure, and introduces no duplicate local storage — reusing the app's existing parent-settings cache infrastructure entirely.
