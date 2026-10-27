# K-06 — Search Result Destination Routing

## 1. Feature Context
Part of Feature B.13 (Search & Discovery). The shared routing logic that sends a tapped search result to the correct existing destination screen, and exposes a deep link so other parts of the app can jump directly into Search.

## 2. Parent Feature
B.13 — Search & Discovery

## 3. Sub-feature
K-06 — Search Result Destination Routing

## 4. Objective
Provide a single, reusable, content-type-switched routing function used by both K-02 (online results) and K-05 (offline results), plus the `noorheroes://search?q=` deep link into Search itself, so routing logic is not duplicated across the two result-rendering paths.

## 5. Business Requirements
- FR-8: story result → Story Detail (A.3); surah result → Surah Learning (A.5); dua result → Dua Learning (A.6).
- §6.8: `noorheroes://search?q=` deep link (e.g., for a "search for more like this" suggestion elsewhere in the app).
- §2.3 Click mapping: result-card tap applies "Standard entitlement/unlock checks of the destination feature" and "Standard destination-feature error handling" — routing delegates, never reimplements, destination-level logic.

## 6. Existing Architecture
A small `SearchResultRouter` utility inside `feature-search`, built on `core-navigation`'s existing deep-link/destination registration mechanism (per `CORE_NAVIGATION_INSTRUCTIONS.md`), consumed by both K-02 and K-05 rather than each screen implementing its own `when(content_type)` switch independently.

## 7. Existing Code to Reuse
- `core-navigation`'s existing deep-link parsing/registration APIs.
- A.3's Story Detail, A.5's Surah Learning, A.6's Dua Learning existing navigation destinations/deep-link schemes — routed into as-is, no new destination screens created.

## 8. Files to Create
- `feature-search/src/commonMain/kotlin/.../search/routing/SearchResultRouter.kt`.
- `feature-search/src/commonTest/kotlin/.../SearchResultRoutingTest.kt` (parameterized over all three content types).

## 9. Files to Modify
- `SearchResultsScreen.kt` (K-02) — delegate result-card tap handling to `SearchResultRouter`.
- Offline results rendering path (K-05) — same delegation.
- `core-navigation`'s deep-link registration — add `noorheroes://search?q=` entry point into `SearchScreen`/pre-filled query submission.

## 10. Backend Requirements
None directly — consumes the `content_type`/`content_id` fields already present in B-01/B-03's response shapes.

## 11. KMP Requirements
- `SearchResultRouter.routeToDestination(contentId, contentType)` switches on `content_type`: `"story"` → Story Detail deep link, `"surah"` → Surah Learning deep link, `"dua"` → Dua Learning deep link.
- Unknown/unexpected `content_type` value → logged, non-crashing fallback (e.g., no-op with a subtle error toast) rather than an unhandled `when` branch.
- `noorheroes://search?q=` deep link opens `SearchScreen` with the query pre-filled and, per existing app deep-link conventions, either auto-submits or waits for confirmation (match whatever pattern other pre-filled-query deep links in the app already use, do not invent a new convention).
- Destination-level entitlement/unlock and error handling is fully delegated — this router performs navigation only, no duplicate business-rule checks.

## 12. NextJS Requirements
N/A.

## 13. API Contract
Consumes the `content_id`/`content_type` fields already defined in B-01 §13 and B-03 §13's response shapes — no additional contract introduced.

## 14. Database Requirements
None.

## 15. Validation
`content_type` validated against the known three-value set before routing; anything else handled per §11's non-crashing fallback.

## 16. Authentication
N/A (navigation-only utility).

## 17. Authorization
N/A — delegated entirely to the destination screen.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Unknown `content_type` | Non-crashing fallback, logged |
| Destination screen itself errors (e.g., content since withdrawn) | Standard destination-feature error handling (unchanged, not reimplemented here) |

## 19. Offline First
Routing itself has no offline dependency; K-05 already ensures offline results only surface content that's actually available offline before this router is ever invoked.

## 20. Local Data
None.

## 21. Localization
N/A (pure routing logic, no user-facing text).

## 22. RTL
N/A.

## 23. Analytics
`search_result_tapped` (with `content_type`) — fired at the point of invoking `SearchResultRouter`, shared by both K-02 and K-05's call sites so the event is not duplicated or missed on either path.

## 24. Performance
Trivial — a `when`-based dispatch, no measurable overhead.

## 25. Security
No new surface; routing performs no data access itself.

## 26. Library Requirements
`core-navigation` only.

## 27. Testing
- Parameterized test covering all three content types, asserting the correct destination deep link is invoked for each.
- Unknown-`content_type` fallback test (no crash).
- Deep-link test: `noorheroes://search?q=` opens Search with the query pre-filled.

## 28. Documentation
KDoc noting this is the single shared routing point for both K-02 and K-05, to prevent future duplication.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Implement SearchResultRouter**
Files to create: `SearchResultRouter.kt`.
Business rules: delegate all destination-level logic, route only.

**Task 02 — Wire Into K-02 and K-05**
Files to modify: `SearchResultsScreen.kt`, offline results rendering path.
Do not change: destination screens' own entitlement/error handling.

**Task 03 — Register Deep Link**
Files to modify: `core-navigation` deep-link registration.

**Task 04 — Add Parameterized Routing Test**
Files to create: `SearchResultRoutingTest.kt`.

**Task 05 — Final Review**
Objective: confirm K-02 and K-05 both call the same router (no duplicated `when(content_type)` logic remaining in either screen).

## 30. Definition of Done
- Single shared router used by both online and offline result paths.
- All three content types route correctly.
- Deep link functional.

## 31. Final Verification Checklist
- [ ] K-02 and K-05 both delegate to the same `SearchResultRouter` — no duplicated routing logic.
- [ ] All three content types verified by parameterized test.
- [ ] Unknown `content_type` does not crash the app.
- [ ] `noorheroes://search?q=` deep link functional.
- [ ] `search_result_tapped` fires exactly once per tap, from a single call site pattern.
