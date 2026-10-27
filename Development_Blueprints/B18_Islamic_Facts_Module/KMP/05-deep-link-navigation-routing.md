# K-05 — Deep Link & Navigation Routing

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). Registers the deep-link surface connecting Home's card, spaced-repetition prompts, and any external deep link into `FactDetailScreen`.

## 2. Parent Feature
B.18 — Islamic Facts Module

## 3. Sub-feature
2.5 Deep Link & Navigation Routing (ID: K-05)

## 4. Objective
Register `noorheroes://facts/{fact_id}` and `noorheroes://facts/daily` deep links in `:core:navigation`, routing Home's Fact of the Day card tap and spaced-repetition resurfacing prompt taps into `FactDetailScreen`.

## 5. Business Requirements
- §6.3 Navigation Flow: `noorheroes://facts/{fact_id}` reachable from Home's card and from spaced-repetition resurfacing prompts.
- §6.8 Deep Linking: `noorheroes://facts/{fact_id}`, `noorheroes://facts/daily`.
- §1.18 Screen Inventory: Fact of the Day Card (Home, owned by A.2) → Fact Detail; Related Content Link → Story Detail/Surah Learning/Dua Card Detail; Spaced-Repetition Resurfacing Prompt → Fact Detail.

## 6. Existing Architecture
`:core:navigation`'s existing deep-link registry and route-resolution pattern (per `CORE_NAVIGATION_INSTRUCTIONS.md`) — this sub-feature adds new route entries, it does not introduce a new navigation framework.

## 7. Existing Code to Reuse
- `:core:navigation`'s existing deep-link parser/dispatcher.
- Existing pattern for resolving a content-id-bearing deep link into a typed navigation argument (mirrors how Story/Surah/Dua deep links already work).
- `:feature:story`'s existing Story Detail route (A.3), `:feature:quran`'s existing Surah Learning route (A.5), `:feature:dua`'s existing Dua Card Detail route (A.6) — Related Content routing consumes these three modules' existing destinations as-is; no new content-detail screens are built by B.18.

**Cross-reference dependency (PRD header: B.18 "Feeds into: A.3 Stories (related-content linkage)"):** this sub-feature is the concrete implementation of that cross-feature link — a fact's `related_content.content_type` of `story`/`surah`/`dua` must resolve to the corresponding feature module's real, existing route. Confirm each of the three route signatures (expected navigation args) with A.3/A.5/A.6 before wiring, rather than assuming a shared shape.

## 8. Files to Create
- `feature-facts/src/commonMain/kotlin/.../FactsNavGraph.kt` — route definitions for `FactDetail(factId)`.
- `feature-facts/src/commonTest/kotlin/.../FactDeepLinkRoutingTest.kt`.

## 9. Files to Modify
- `:core:navigation`'s central deep-link registry — register `noorheroes://facts/{fact_id}` and `noorheroes://facts/daily`.
- `:feature:home` (A.2) — confirm the Fact of the Day card's tap action already deep-links via this scheme, or update it to do so if it currently calls a different/legacy route (coordinate with B-08's backend cutover).

## 10. Backend Requirements
None — pure client-side routing; `noorheroes://facts/daily` resolves by first calling `FactsRepository.getDailyFact()` (B-02) to obtain a concrete `fact_id`, then navigating to the resolved `FactDetail(factId)` route.

## 11. KMP Requirements
- `noorheroes://facts/{fact_id}` → directly navigates to `FactDetailScreen(factId)`.
- `noorheroes://facts/daily` → resolves today's fact_id via `FactsRepository.getDailyFact()` first, then navigates to `FactDetailScreen(resolvedFactId)`; if resolution fails, show Fact Detail's own error/retry state rather than a broken deep link.
- Related Content link (within Fact Detail) routes to the appropriate existing destination: Story Detail, Surah Learning, or Dua Card Detail, based on `related_content.content_type` — reusing each destination's existing route, not a new unified content router.
- Malformed/unknown `fact_id` in the deep link → Fact Detail's existing not-found/error state (K-01), not a navigation crash.

## 12. NextJS Requirements
N/A.

## 13. API Contract
`noorheroes://facts/daily` indirectly triggers B-02; `noorheroes://facts/{fact_id}` indirectly triggers B-03 once `FactDetailScreen` mounts (per K-01).

## 14. Database Requirements
None new.

## 15. Validation
`fact_id` path segment validated as a well-formed UUID before attempting navigation; malformed → graceful error, not a crash or unhandled exception.

## 16. Authentication
N/A — routing layer; the destination screen (K-01) enforces authenticated access as usual.

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Malformed `fact_id` in deep link | Fact Detail's not-found/error state |
| `noorheroes://facts/daily` resolution fails (network error) | Fact Detail's error/retry state, not a silent no-op |
| Unknown deep-link scheme variant | Falls through to the app's existing default deep-link-not-recognized handling |

## 19. Offline First
`noorheroes://facts/daily` resolution respects K-03's offline-first `getDailyFact()` behavior (cached fallback if offline).

## 20. Local Data
None new.

## 21. Localization
N/A — deep-link scheme itself is not localized; downstream screen content is (K-01).

## 22. RTL
N/A — routing layer.

## 23. Analytics
None new directly; standard deep-link-open analytics (if the platform tracks deep-link entry generally) apply unmodified.

## 24. Performance
Negligible; route resolution is O(1) dictionary lookup plus, for `/daily`, one repository call already covered by K-03's caching.

## 25. Security
Deep link does not bypass authentication — `FactDetailScreen` still requires an authenticated child session to actually load content, per K-01.

## 26. Library Requirements
None new — uses `:core:navigation`'s existing deep-link framework (Compose Navigation or platform equivalent).

## 27. Testing
- Unit: `noorheroes://facts/{valid-uuid}` routes to `FactDetailScreen` with correct argument.
- Unit: `noorheroes://facts/{malformed}` routes to an error state, no crash.
- Unit: `noorheroes://facts/daily` resolves via `getDailyFact()` then routes correctly.
- Integration: Home card tap and resurfacing-prompt tap both correctly reach `FactDetailScreen`.

## 28. Documentation
Update `:core:navigation`'s deep-link registry documentation with the two new routes.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Register Deep-Link Routes**
Objective: Add `noorheroes://facts/{fact_id}` and `noorheroes://facts/daily` to `:core:navigation`'s registry.
Files to Modify: `:core:navigation`'s central deep-link registry.
Dependencies: K-01 complete (destination screen must exist).
Definition of Done: Both routes resolve correctly in isolation.

**Task 02 — `/daily` Resolution Logic**
Objective: Resolve `noorheroes://facts/daily` via `FactsRepository.getDailyFact()` before navigating.
Files to Create: `FactsNavGraph.kt`.
Dependencies: Task 01, K-03 (offline-first repository).
Definition of Done: Correct fact_id resolved and navigated to, offline fallback respected.

**Task 03 — Confirm/Update Home Card Wiring**
Objective: Ensure `:feature:home`'s Fact of the Day card uses this deep-link scheme (or direct navigation equivalent), coordinated with B-08's backend cutover.
Files to Modify: `:feature:home`'s card tap handler (confirm exact current implementation before assuming it needs a change).
Dependencies: Task 02.
Definition of Done: Card tap reaches `FactDetailScreen` via the confirmed route.

**Task 04 — Confirm Story/Surah/Dua Route Contracts**
Objective: Confirm exact navigation-argument signatures for `:feature:story`'s Story Detail, `:feature:quran`'s Surah Learning, and `:feature:dua`'s Dua Card Detail routes with A.3/A.5/A.6 before wiring Related Content routing.
Why Required: Rule 30 — do not guess at another feature's route shape.
Dependencies: Task 02.
Definition of Done: Three confirmed route signatures documented; Related Content routing (within K-01) uses them exactly.

**Task 05 — Tests**
Objective: Coverage per §27.
Dependencies: Tasks 01–04.
Definition of Done: All green.

**Task 06 — Documentation**
Dependencies: Task 05.
Definition of Done: `:core:navigation` docs updated.

## 30. Definition of Done
- Both deep-link routes registered and functioning.
- `/daily` correctly resolves via the repository before navigating, respecting offline-first behavior.
- Home card and resurfacing prompts both verified to reach Fact Detail correctly.
- Malformed input handled gracefully, no crashes.

## 31. Final Verification Checklist
- [ ] `noorheroes://facts/{fact_id}` and `noorheroes://facts/daily` both registered and tested
- [ ] Malformed `fact_id` handled gracefully, no crash
- [ ] `/daily` resolution respects offline-first caching (K-03)
- [ ] Home card and resurfacing prompt entry points verified end-to-end
- [ ] Related Content routing reuses existing Story/Surah/Dua destinations, no new unified router
- [ ] Documentation updated
