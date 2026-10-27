# Blueprint: AI Insight Report Screen (Premium)

## 1. Feature Context
Platform: NoorHeroes KMP App. Module: `:feature:reports`, integrating `:core:auth`/subscription entitlement state and `:feature:subscription` (C.24) for the upsell path. Delivers the premium AI Insight Report screen.

## 2. Parent Feature
C.22 — Per-Child Reports.

## 3. Sub-feature
K-06 — AI Insight Report Screen (Premium).

## 4. Objective
Render the AI Insight Report (strengths, weak areas, suggested next content, healthy-usage notes) for entitled families, and a locked/upsell state for non-premium families, always respecting the serve-time entitlement check enforced by Backend B-06.

## 5. Business Requirements
Source: PRD §1.7 FR-6, FR-8, §1.10 Edge Case #4, §1.18 Screen Inventory #12.
- Content: strengths, weak areas, suggested next stories/duas/Quran practice, healthy-usage notes.
- Locked/upsell state for non-premium families, routing to C.24.
- Entitlement lapsing mid-generation/mid-view must be respected at serve time — the client always trusts the server's current response over any previously cached "entitled" state.

## 6. Existing Architecture
Consumes Backend B-06's extended `GET /v1/parent/reports/{child_id}/ai-insight`. Reuses C.24's existing upsell/paywall UI pattern rather than building a new one.

## 7. Existing Code to Reuse
- C.24's `PremiumUpsellTapHandler` (`feature/subscription/navigation/PremiumUpsellTapHandler.kt`, C.24 K-12) — the confirmed, existing shared tap-through-to-Subscription-landing handler, navigating to the Subscription landing screen (C.24 K-01) with an upsell context flag. This screen's `Locked` state CTA should invoke this handler rather than a bespoke navigation call.
- `Navigator` for routing to C.24's subscription flow.
- `BaseViewModel`, `NoorResult<T>`.

## 8. Files to Create
- `feature/reports/src/commonMain/kotlin/.../AiInsightReportRoute.kt`
- `feature/reports/src/commonMain/kotlin/.../AiInsightReportScreen.kt`
- `feature/reports/src/commonMain/kotlin/.../AiInsightReportViewModel.kt`
- `feature/reports/src/commonMain/kotlin/.../AiInsightReportUiState.kt`
- `feature/reports/src/commonTest/kotlin/.../AiInsightReportViewModelTest.kt`

## 9. Files to Modify
- `ReportRepository.kt` — add `getAiInsightReport(childId): NoorResult<AiInsightReportResult>`

## 10. KMP Requirements
- `AiInsightReportUiState`: `sealed interface { object Loading; data class Content(val data: AiInsightReportData); data class Locked(val upsellContext: UpsellContext); data class Error(val error: AppError) }`.
- `AiInsightReportViewModel` fetches fresh on every screen entry (never serves a locally cached "entitled" response without a fresh server round-trip, given Backend B-06's serve-time entitlement guarantee — the client must not short-circuit this with stale local state).
- `Locked` state's CTA invokes `PremiumUpsellTapHandler` (C.24 K-12), which navigates to C.24's Subscription landing screen (K-01) with an upsell context flag.
- If a previously entitled session's cached data exists locally but the fresh fetch returns `Locked`, the UI immediately reflects `Locked` — never shows stale premium content.

## 11. Files to Create — continued
`AiInsightReportScreen`: strengths/weak-areas/suggested-content/healthy-usage-notes sections when `Content`; upsell card when `Locked`.

## 12. NextJS Requirements
N/A.

## 13. API Mapping
`ReportRepository.getAiInsightReport(childId)` → `GET /v1/parent/reports/{child_id}/ai-insight` (Backend B-06).

## 14. Database Requirements (Local)
Cached via `:core:offline-cache` for offline read-only viewing of previously fetched **entitled** content only; a `Locked` response is never cached as viewable content (nothing to cache for a locked state beyond the upsell context itself).

## 15. Validation
`childId` required nav arg.

## 16. Authentication
Inherits Parent Gate requirement.

## 17. Authorization
Server-enforced (family-ownership + entitlement, Backend B-06); client always trusts the fresh response.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Non-premium family | `Locked` state with upsell CTA |
| Entitlement lapses since last successful view | Fresh fetch returns `Locked`; UI reflects it immediately, discarding any stale cached premium content from display |
| Network failure | `Error` with retry |

## 19. Offline First
Only previously fetched **entitled** content is cached for offline read; a fresh online fetch is required to re-confirm entitlement before trusting cached content is still valid to display as "current" (display cached content with an "as of" freshness label if offline, consistent with the platform's general offline-cache pattern, but do not claim it reflects current entitlement).

## 20. Local Data
Cached `AiInsightReportData` per `childId`, entitlement-state-aware (not served if a fresh check would deny it).

## 21. Localization
All content sections locale-resolved server-side (Backend B-06/C.20's `AIReportGenerationService`); upsell copy reused from C.24.

## 22. RTL
Content sections and upsell card mirror correctly for Arabic/Urdu.

## 23. Analytics
`ai_insight_report_viewed` on successful `Content` load; `ai_insight_locked_state_shown` on `Locked` state render.

## 24. Performance
Standard screen-level performance; no special concerns beyond the entitlement-freshness requirement (always a live fetch, no stale-serving optimization that would violate Edge Case #4).

## 25. Security
Client never serves previously cached premium content without deferring to the current server response — this prevents a client-side entitlement-bypass pattern where a family could view stale premium content indefinitely after cancellation while offline-then-online without a fresh check.

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. Unit test: entitled family renders `Content` with all sections.
2. Unit test: non-premium family renders `Locked` with correct upsell context.
3. **Race-awareness test:** simulate a fresh fetch returning `Locked` despite locally cached `Content` data existing — assert UI reflects `Locked`, never the stale cached content.
4. UI test: `Locked` state CTA correctly routes to C.24's subscription flow.
5. Integration test: full fetch-and-render flow for both entitled and non-entitled cases.

## 28. Documentation
KDoc explicitly citing Edge Case #4 and the "always trust fresh server response" contract.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define AiInsightReportUiState and Repository Method**
- Task ID: K06-T01
- Objective: Data model with distinct `Content`/`Locked`/`Error` states.
- Why This Is Required: Foundation mirroring Backend B-06's serve-time entitlement contract.
- Existing Architecture to Follow: `NoorResult<T>` pattern.
- Existing Files to Reuse: `ReportRepository` (extend).
- Files to Create: `AiInsightReportUiState.kt`.
- Files to Modify: `ReportRepository.kt`.
- Implementation Details: Per §10.
- Business Rules: Edge Case #4.
- Validation: N/A.
- Error Handling: `Locked`/`Error` distinct.
- Security: N/A at this layer.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 03.
- Documentation: KDoc.
- Dependencies: Backend B-06 live.
- Do Not Change: N/A.
- Expected Result: State model compiles.
- Definition of Done: Matches Backend B-06's contract.

**Task 02 — Implement AiInsightReportViewModel and Screen**
- Task ID: K06-T02
- Objective: Always-fresh fetch, render content or locked/upsell state.
- Why This Is Required: Delivers the sub-feature while honoring the entitlement race fix.
- Existing Architecture to Follow: `BaseViewModel`, `PremiumUpsellTapHandler` (C.24 K-12).
- Existing Files to Reuse: `feature/subscription/navigation/PremiumUpsellTapHandler.kt`.
- Files to Create: `AiInsightReportViewModel.kt`, `AiInsightReportScreen.kt`, `AiInsightReportRoute.kt`.
- Files to Modify: Navigation graph.
- Implementation Details: Per §10, §18.
- Business Rules: Edge Case #4.
- Validation: N/A.
- Error Handling: Per §18.
- Security: Never serves stale cached premium content over a fresh `Locked` response.
- Performance: N/A.
- Localization: Full string-resource coverage.
- RTL: Verified mirroring.
- Analytics: `ai_insight_report_viewed`/`ai_insight_locked_state_shown`.
- Tests: Covered in Task 03.
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: `PremiumUpsellTapHandler`'s internals.
- Expected Result: Screen renders correctly across all states.
- Definition of Done: Race-awareness verified.

**Task 03 — Write Test Suite**
- Task ID: K06-T03
- Objective: Cover §27, with the race-awareness test as the defining verification.
- Why This Is Required: Edge Case #4 client-side verification.
- Existing Architecture to Follow: Kotlin test + Compose UI test.
- Existing Files to Reuse: Entitlement-state fixtures.
- Files to Create: `AiInsightReportViewModelTest.kt`.
- Files to Modify: none.
- Implementation Details: 5 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact states.
- Security: Race-awareness test is critical.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test KDoc.
- Dependencies: Tasks 01–02.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green.

## 30. Definition of Done
`AiInsightReportScreen` live, entitled content and locked/upsell states both correctly rendered, fresh server response always trusted over stale cached content, all tests green.

## 31. Final Verification Checklist
- [ ] Locked state correctly routes to C.24's subscription flow
- [ ] Race-awareness test confirms UI never displays stale cached premium content over a fresh `Locked` response
- [ ] Content sections correctly render for entitled families
- [ ] Localization and RTL mirroring verified
