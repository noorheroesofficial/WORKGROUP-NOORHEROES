# Blueprint: Support Center & FAQ Search

## 1. Feature Context
Platform: NoorHeroes KMP App. Same module: `:feature:parent-notifications-support`. This blueprint delivers the self-serve half of the Support Center — the calm, search-first landing hub and FAQ search/detail flow that K-04's ticket flow sits behind as the escalation path.

## 2. Parent Feature
C.25 — Notifications (Parent) & Support.

## 3. Sub-feature
K-03 — Support Center & FAQ Search.

## 4. Objective
Build `SupportCenterScreen`, `FaqSearchScreen`, and the FAQ Article Detail screen, wired to B-03, with a zero-results state that prominently surfaces a "Contact Support" call-to-action rather than a dead end.

## 5. Business Requirements
Source: PRD §2.2 Screen-Level Design (Support Center); §1.10 Edge Case 4; §1.14 Offline States; §1.19 Events; §6.2, §6.10.
- `SupportCenterScreen`: FAQ search bar, popular-topics quick links, "Contact Support" entry, "My Tickets" entry (§2.2 Components) — "a calm, effective self-serve-first help hub."
- FAQ search and ticket submission require connectivity; clearly indicated if attempted offline (§1.14) — this is a genuine exception to the inbox's offline-first model (K-01), not an inconsistency to "fix."
- Zero-results FAQ search → clear "no results, contact Support" fallback, never a dead-end blank result (Edge Case 4).
- Deliberately conventional search-first, help-center wireframe pattern — parents benefit from recognizable patterns over novel interaction models (§2.4).

## 6. Existing Architecture
Same module/DI root as K-01/K-02 (`ParentNotificationsSupportModule`). Reuses `Route`/`BaseViewModel`/`AuthStateProvider` patterns established in those blueprints.

## 7. Existing Code to Reuse
- `AuthStateProvider` (support works for any parent, even pre-subscription per B-03 §16 — confirm whether this screen is reachable pre-subscription at the navigation-guard level, i.e., `requiredAuthState` may need to be a broader "any authenticated parent" state rather than a subscription-gated one; do not assume subscription-gating without confirming against the platform's actual auth-state hierarchy).
- `NoorResult<T>`, `BaseViewModel`, `Route` pattern.
- K-01/K-02's Koin module (`ParentNotificationsSupportModule`) — extend rather than duplicate.
- Design tokens, Parent-Mode formal visual register (`:core:design-system`).

## 8. Files to Create
- `feature/parent-notifications-support/src/commonMain/kotlin/.../SupportCenterRoute.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../SupportCenterScreen.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../SupportCenterViewModel.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../FaqSearchRoute.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../FaqSearchScreen.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../FaqSearchViewModel.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../FaqArticleDetailRoute.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../FaqArticleDetailScreen.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../SupportRepository.kt` (interface — also consumed by K-04)
- `feature/parent-notifications-support/src/commonTest/kotlin/.../FaqSearchViewModelTest.kt`
- `feature/parent-notifications-support/src/commonTest/kotlin/.../FaqZeroResultsFallbackTest.kt`

## 9. Files to Modify
- `di/ParentNotificationsSupportModule.kt` — register `SupportRepository` (shared with K-04) and this blueprint's ViewModels.
- Navigation graph — register `SupportCenterRoute`, `FaqSearchRoute`, `FaqArticleDetailRoute`; wire from Parent Dashboard/Settings entry points and from `NotificationsInboxScreen`'s (K-01) navigation surface if applicable.

## 10. KMP Requirements
- `SupportCenterRoute`/`FaqSearchRoute`/`FaqArticleDetailRoute`: `Route` implementations with appropriate `requiredAuthState` (per §7's caveat) and `analyticsName` (`"support_center"`, `"faq_search"`, `"faq_article_detail"`).
- `SupportRepository` interface (shared with K-04): `suspend fun searchFaq(query: String, locale: String?): NoorResult<List<FaqArticleSummary>>`, `suspend fun getFaqArticle(id: String): NoorResult<FaqArticleDetail>`, `suspend fun submitFaqFeedback(id: String, helpful: Boolean): NoorResult<Unit>` (ticket methods added by K-04 to the same interface).
- `SupportCenterViewModel`: exposes popular-topics quick links (a small curated/static or server-driven list — confirm source before hardcoding a topic list; if no dedicated "popular topics" endpoint exists in B-03, this may need to be a client-side curated set pending a future backend enhancement, and should be flagged as such rather than silently invented as if server-driven).
- `FaqSearchViewModel`: debounced search-as-you-type (e.g., 300ms, mirroring the Admin Portal's `useDebouncedValue` pattern conceptually) against `SupportRepository.searchFaq()`; states: `Default`, `SearchActive`, `SearchZeroResults`.
- `FaqArticleDetailViewModel` (or folded into the screen if state is trivial — confirm complexity before adding a separate ViewModel class): loads full article, exposes "Was this helpful?" submission calling `submitFaqFeedback()`.
- Require connectivity for search: if the network call fails due to no connectivity, show a distinct "You're offline — search requires an internet connection" message, not a generic error or an empty-results state (these must be visually/textually distinct per §1.14).

## 11. Files to Create — Screen Composables
- `SupportCenterScreen`: search bar (routes to `FaqSearchScreen` on submit or live-search inline — confirm exact UX pattern, default to inline search-as-you-type within `SupportCenterScreen` itself transitioning to `FaqSearchScreen`'s result-list rendering, consistent with §2.2's Default/Search-active/Search-zero-results state model belonging to one cohesive search experience), popular-topics quick links, "Contact Support" entry (→ K-04), "My Tickets" entry (→ K-04).
- `FaqSearchScreen`: result list (title + summary); zero-results state prominently surfaces a "Contact Support" CTA (→ K-04's `ContactSupportFormScreen`).
- `FaqArticleDetailScreen`: full article body (RTL-aware text rendering for Arabic/Urdu content), "Was this helpful?" yes/no capture, with a "no" response optionally prompting a Contact Support suggestion (natural extension of Edge Case 4's spirit, though not explicitly mandated for the "unhelpful" case — confirm against Figma before adding this specific behavior beyond the explicit zero-results requirement).

## 12. NextJS Requirements
N/A.

## 13. API Contract
Consumes `GET /v1/support/faq?q=`, `GET /v1/support/faq/{id}`, `POST /v1/support/faq/{id}/feedback` (B-03) via `SupportRepository`.

## 14. Database Requirements
No local persistence required — FAQ search/detail requires connectivity per §1.14; no offline-cache obligation for this specific sub-feature (unlike K-01's inbox).

## 15. Validation
Search query length-bounded client-side (mirroring B-03's server-side bound) to avoid pathological input; `helpful` feedback is a simple boolean, no complex validation.

## 16. Authentication
Per §7's caveat — confirm whether this is reachable without a full parent session (public/pre-subscription per B-03) or requires standard parent authentication; default to requiring at least basic app authentication (not necessarily subscription) unless confirmed otherwise.

## 17. Authorization
No family-scoped data involved (FAQ content is universal, not per-family) — no cross-family authorization concern for search/detail; feedback submission is anonymous-safe (no PII beyond the boolean + article ID).

## 18. Error Handling
- Zero-results search → "Contact Support" CTA fallback (Edge Case 4), never blank.
- Offline attempt → distinct "requires connectivity" messaging, not a generic error (§1.14).
- Article-detail fetch failure → standard error state with retry.
- Feedback-submission failure → silently retried or fire-and-forget with a best-effort local swallow (feedback is a nice-to-have signal, not a critical user-facing action — do not block the UI on its success, but do not silently pretend it succeeded if surfaced explicitly to the user as a "Thanks!" confirmation; ensure the confirmation only shows on actual success).

## 19. Offline First
Explicitly N/A for search/submission per §1.14 — this is the one KMP sub-feature in C.25 that is deliberately not offline-first, and that distinction should be preserved, not "fixed" into an inconsistency with K-01.

## 20. Local Data
N/A.

## 21. Localization
All UI copy via localization keys; FAQ article `body` content itself is served pre-localized by `locale` from B-03 (server-side content governance, not client-side translation) — the client requests the user's active locale and renders whatever `body` comes back as-is, including RTL text shaping for Arabic/Urdu content.

## 22. RTL
Search bar, result list, and article-detail body text must all render correctly in RTL layout and RTL text direction for Arabic/Urdu article content specifically (distinct from RTL *layout* mirroring, which applies to all locales' UI chrome — article body text direction depends on the article's own `locale`, independent of the app's overall UI locale in an edge case where they differ, though typically they'd match).

## 23. Analytics
`support_center_viewed`, `faq_search_performed`, `faq_article_viewed`, `faq_zero_results_shown`, `faq_marked_unhelpful` (§1.19).

## 24. Performance
- Debounced search input (avoid firing a network request per keystroke).
- Cancel in-flight search requests when a newer query supersedes them (avoid stale-result race conditions where an older, slower response overwrites a newer one).

## 25. Security
No sensitive data; standard input validation on the search query to avoid any injection-style abuse being forwarded verbatim (though the actual query-sanitization boundary is server-side, B-03).

## 26. Library Requirements
No new third-party libraries.

## 27. Testing
1. **UI test (mandatory):** zero-results search state transitions to prominently show the "Contact Support" CTA (§7 item 3 of the PRD's Android AI Code-Gen Prompt, cross-referenced from K-04's own prompt since this is where the zero-results state itself lives).
2. Unit test: search debounce correctly limits network calls during rapid typing.
3. Unit test: an in-flight search request is cancelled/ignored when a newer query supersedes it.
4. Unit test: offline search attempt shows the distinct "requires connectivity" message, not a generic error or empty-results state.
5. UI test: "Was this helpful?" feedback submission shows a confirmation only on actual success.
6. UI test: RTL rendering of Arabic/Urdu article body content.
7. Integration test: full search → article detail → feedback flow.

## 28. Documentation
KDoc citing PRD §2.2, §1.14, Edge Case 4.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Routes and Shared SupportRepository Interface**
- Task ID: K03-T01
- Objective: Navigation destinations and the data-access contract shared with K-04.
- Why This Is Required: Foundation for this blueprint and a dependency of K-04.
- Existing Architecture to Follow: `Route` pattern; `core-data` repository interface pattern.
- Existing Files to Reuse: `Route`, `NoorResult<T>`.
- Files to Create: `SupportCenterRoute.kt`, `FaqSearchRoute.kt`, `FaqArticleDetailRoute.kt`, `SupportRepository.kt` (interface, FAQ methods only — K-04 extends with ticket methods).
- Files to Modify: none.
- Implementation Details: Per §10.
- Business Rules: §6.2.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: `analyticsName` per route.
- Tests: Covered in Task 04.
- Documentation: KDoc.
- Dependencies: None.
- Do Not Change: N/A.
- Expected Result: Types compile.
- Definition of Done: `SupportRepository` interface is extensible for K-04 without breaking changes.

**Task 02 — Implement SupportCenterViewModel and FaqSearchViewModel**
- Task ID: K03-T02
- Objective: Core state management for the search flow.
- Why This Is Required: Central orchestrators.
- Existing Architecture to Follow: `BaseViewModel`, `DispatcherProvider`.
- Existing Files to Reuse: `BaseViewModel`, `DispatcherProvider`, `SupportRepository` (Task 01).
- Files to Create: `SupportCenterViewModel.kt`, `FaqSearchViewModel.kt`.
- Files to Modify: none.
- Implementation Details: Debounced search, cancellation of superseded requests, connectivity-aware error states, `SearchZeroResults` state per §10.
- Business Rules: Edge Case 4, §1.14.
- Validation: N/A.
- Error Handling: Per §18.
- Security: N/A.
- Performance: Debounce + cancellation.
- Localization: N/A (ViewModel has no strings).
- RTL: N/A.
- Analytics: Fire `support_center_viewed`, `faq_search_performed`, `faq_zero_results_shown`.
- Tests: Covered in Task 04.
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: ViewModels functional against a fake repository.
- Definition of Done: All Task 04 tests pass.

**Task 03 — Implement FaqArticleDetailScreen/ViewModel and Screen Composables**
- Task ID: K03-T03
- Objective: Article detail rendering, feedback capture, and full screen assembly for all three screens.
- Why This Is Required: Core visual deliverable.
- Existing Architecture to Follow: `:core:design-system` tokens; RTL-aware text rendering conventions.
- Existing Files to Reuse: Design-system search-bar, list-item, and article-body components — confirm exact names before use.
- Files to Create: `SupportCenterScreen.kt`, `FaqSearchScreen.kt`, `FaqArticleDetailRoute.kt`, `FaqArticleDetailScreen.kt`.
- Files to Modify: `di/ParentNotificationsSupportModule.kt`, navigation graph.
- Implementation Details: Per §11.
- Business Rules: §2.2, §2.4.
- Validation: N/A.
- Error Handling: Per §18, including the zero-results CTA and offline-distinct messaging.
- Security: N/A.
- Performance: N/A.
- Localization: All strings via localization package; article body rendered as-is from server locale.
- RTL: Layout and article-body text direction both verified.
- Analytics: Fire `faq_article_viewed`, `faq_marked_unhelpful`.
- Tests: Covered in Task 04.
- Documentation: KDoc.
- Dependencies: Task 02.
- Do Not Change: N/A.
- Expected Result: All three screens render correctly across states.
- Definition of Done: Matches §11 exactly.

**Task 04 — Write Test Suite**
- Task ID: K03-T04
- Objective: Cover §27.
- Why This Is Required: PRD-mandated coverage, notably the zero-results CTA test.
- Existing Architecture to Follow: Kotlin test + Compose UI testing conventions.
- Existing Files to Reuse: none new.
- Files to Create: `FaqSearchViewModelTest.kt`, `FaqZeroResultsFallbackTest.kt`.
- Files to Modify: none.
- Implementation Details: All 7 cases from §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: Debounce/cancellation tests.
- Localization: N/A.
- RTL: RTL rendering test.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All pass.
- Definition of Done: 100% of §27 green.

## 30. Definition of Done
`SupportCenterScreen`, `FaqSearchScreen`, `FaqArticleDetailScreen` live and functional against B-03, zero-results state correctly surfaces the Contact Support CTA, offline attempts show distinct messaging, all tests green.

## 31. Final Verification Checklist
- [ ] Zero-results search shows Contact Support CTA, never a dead end (tested)
- [ ] Offline search attempt shows distinct connectivity messaging, not a generic error
- [ ] Search debounced and superseded requests cancelled correctly
- [ ] Feedback confirmation shown only on actual submission success
- [ ] RTL layout and article-body text direction verified
- [ ] `SupportRepository` interface left extensible for K-04's ticket methods
- [ ] No hardcoded strings
