# Blueprint: Contact Support Form & Ticket History/Status Tracking

## 1. Feature Context
Platform: NoorHeroes KMP App. Same module: `:feature:parent-notifications-support`. This blueprint delivers the escalation half of the Support Center — ticket submission, history, and status tracking — including the Account Deletion Cancellation entry point, and closes out the module's KMP scope.

## 2. Parent Feature
C.25 — Notifications (Parent) & Support.

## 3. Sub-feature
K-04 — Contact Support Form & Ticket History/Status Tracking.

## 4. Objective
Build `ContactSupportFormScreen`, `TicketSubmittedConfirmation`, `TicketHistoryScreen`, and `TicketDetailScreen`, wired to B-04, with an explicit "Account Deletion Cancellation" category option and a structural guarantee that submission touches **only** ticket-creation endpoints — never any deletion-status-mutation code path.

## 5. Business Requirements
Source: PRD §1.7 FR-8; §1.10 Edge Case 3; §1.11; §6.2, §6.6, §6.8, §6.10; §7 Android AI Code-Generation Prompt items 3–5.
- Ticket Category Selector includes an explicit, clearly-labeled "Account Deletion Cancellation" option with helper text explaining it routes to an expedited human-reviewed queue (§7 item 4).
- `SupportRepository.submitTicket()` must have **no** code path touching any deletion-status-mutation endpoint — a structural guarantee confirming this module's API surface for this action is limited to ticket creation only (§7 item 4, mirrors B-04's server-side guarantee).
- Local draft preservation and retry on network failure — never silently lost (§1.11).
- `TicketDetailScreen` displays status (submitted/in_progress/resolved) prominently via a clear stage-indicator, not free-text alone (§7 item 5).
- Deep-link entry points: `noorheroes://parent/notifications`, `noorheroes://parent/support`, `noorheroes://parent/support/tickets/{id}` (§6.8).
- Deletion-Pending Countdown Banner (cross-ref C.21) is an entry point that pre-tags the ticket category as Account Deletion Cancellation.

## 6. Existing Architecture
Same module/DI root as K-01 through K-03. Extends the `SupportRepository` interface K-03 established with ticket-related methods, rather than creating a second repository for the same `support` concept.

## 7. Existing Code to Reuse
- `SupportRepository` interface (K-03) — extend with `submitTicket()`, `getTickets()`, `getTicketDetail()`, `addFollowUpMessage()`.
- `AuthStateProvider`, `NoorResult<T>`, `BaseViewModel`, `Route` pattern.
- K-01's offline-draft-preservation pattern (the mark-read outbox/queue mechanism) as a structural reference for this blueprint's own local-draft-preservation requirement, though the specific persistence need differs (a single in-flight ticket draft vs. a queue of actions).
- C.21's Deletion-Pending Countdown Banner component (referenced entry point — confirm its exact location/API in C.21's own KMP blueprints before wiring; do not invent this component if it doesn't yet exist, in which case this blueprint's entry-point wiring is deferred until C.21 delivers it).

## 8. Files to Create
- `feature/parent-notifications-support/src/commonMain/kotlin/.../ContactSupportFormRoute.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../ContactSupportFormScreen.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../ContactSupportFormViewModel.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../TicketSubmittedConfirmationScreen.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../TicketHistoryRoute.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../TicketHistoryScreen.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../TicketHistoryViewModel.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../TicketDetailRoute.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../TicketDetailScreen.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../TicketDetailViewModel.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../components/TicketCategorySelector.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../components/TicketStageIndicator.kt`
- `feature/parent-notifications-support/src/commonTest/kotlin/.../ContactSupportFormViewModelTest.kt`
- `feature/parent-notifications-support/src/commonTest/kotlin/.../SupportRepositoryTicketOnlyStructuralTest.kt`

## 9. Files to Modify
- `SupportRepository.kt` (K-03) — add ticket method signatures.
- `di/ParentNotificationsSupportModule.kt` — register this blueprint's ViewModels.
- Navigation graph — register all 4 routes and the 3 deep-link URI mappings (§6.8).
- C.21's Deletion-Pending Countdown Banner (if it exists) — wire its "Cancel" affordance to launch `ContactSupportFormRoute` pre-tagged with `category = account_deletion_cancellation`.

## 10. KMP Requirements
- `SupportRepository` (extended): `suspend fun submitTicket(category: TicketCategory, message: String, relatedDeletionRequestId: String?): NoorResult<TicketSubmissionResult>`, `suspend fun getTickets(): NoorResult<List<TicketSummary>>`, `suspend fun getTicketDetail(id: String): NoorResult<TicketDetail>`, `suspend fun addFollowUpMessage(ticketId: String, body: String): NoorResult<TicketMessage>`. **No method on this interface may call, reference, or import any deletion-cancellation-mutation API** — this is the structural guarantee verified in Task 05.
- `TicketCategory` enum: `AccountDeletionCancellation`, `Billing`, `Technical`, `ContentConcern`, `SafetyConcern`, `General` (mirrors B-04's exact FR-9 taxonomy — confirm exact wire values match the backend's string codes rather than diverging).
- `ContactSupportFormViewModel`: holds an in-progress draft (`category`, `message`, optional pre-tagged `relatedDeletionRequestId`) in memory, persisted to a lightweight local store (e.g., a single-row local cache, not a full outbox queue) so an app kill/network failure doesn't lose in-progress text; on submit failure, retries with the preserved draft rather than clearing it.
- `TicketCategorySelector`: includes "Account Deletion Cancellation" as an explicit, clearly-labeled option with helper text ("This routes to a priority-reviewed queue and helps you cancel a pending deletion request") — never buried among generic categories.
- `TicketDetailViewModel`: exposes `TicketStageIndicator` state (`Submitted`/`InProgress`/`Resolved`) derived directly from the server's `status` field, plus the message thread for follow-ups.
- Deep-link handling for `noorheroes://parent/support/tickets/{id}` routes directly to `TicketDetailRoute(id)`, consistent with reusing `:core:notifications`'s `DeepLinkResolutionHandler` for any notification-originated navigation (K-01), while direct app-link taps (not notification-originated) may use a simpler direct-route resolution — confirm this distinction against the platform's actual deep-link architecture before assuming two separate resolution paths are correct.

## 11. Files to Create — Screen Composables
- `ContactSupportFormScreen`: category selector (with the Account Deletion Cancellation option and helper text), message text field, submit button; shows local-draft-preserved state clearly if a previous submission attempt failed.
- `TicketSubmittedConfirmationScreen`: confirmation + `queue_priority` context ("Your request is in our priority queue" for expedited categories) + link to Ticket History.
- `TicketHistoryScreen`: list of the parent's tickets (category, status badge, created date).
- `TicketDetailScreen`: `TicketStageIndicator` prominently at top, message thread below, follow-up message input at bottom.

## 12. NextJS Requirements
N/A.

## 13. API Contract
Consumes `POST /v1/support/tickets`, `GET /v1/support/tickets`, `GET /v1/support/tickets/{id}`, `POST /v1/support/tickets/{id}/messages` (B-04).

## 14. Database Requirements
Lightweight local single-draft persistence for the in-progress Contact Support form (survive app kill before submission); no full ticket-history caching required per PRD's connectivity requirement for this surface (§1.14) — history/detail views require connectivity, unlike K-01's inbox.

## 15. Validation
Client-side: `category` required, `message` non-empty before enabling Submit — mirrors, does not replace, B-04's server-side validation.

## 16. Authentication
Reachable only via an authenticated parent session.

## 17. Authorization
Own-tickets-only access, enforced server-side (B-04); this client simply renders whatever the session-scoped API returns.

## 18. Error Handling
- Submission network failure → local draft preserved, retry offered, never silently lost (§1.11) — this is the primary error-handling deliverable of this blueprint.
- Ticket history/detail fetch failure → standard error state with retry (requires connectivity, no offline fallback per §1.14).
- Follow-up message failure → local retry, message not lost from the input field.

## 19. Offline First
Explicitly N/A for this sub-feature's core actions (submission, history, detail all require connectivity, §1.14) — only the in-progress draft's local preservation is a "survive interruption" concern, not full offline-first support.

## 20. Local Data
Single-draft local persistence only (see §14) — not a general offline cache.

## 21. Localization
All UI copy, category labels/helper text, and stage-indicator labels via localization keys; support English/Hindi/Arabic/Urdu.

## 22. RTL
Category selector, stage indicator, and message-thread layout must mirror correctly in RTL.

## 23. Analytics
`support_ticket_submitted` (with `category`), `support_ticket_status_viewed`, `support_ticket_follow_up_added`, `account_deletion_cancellation_ticket_submitted` (§1.19) — the last fires specifically (in addition to the generic `support_ticket_submitted`) whenever `category == AccountDeletionCancellation`, giving product/trust-safety visibility into this specific high-stakes flow.

## 24. Performance
Standard list/detail rendering; no special performance concerns beyond `@Stable` state modeling consistent with the rest of the module.

## 25. Security
**This blueprint's core guarantee**, alongside B-04's server-side equivalent: `SupportRepository`'s ticket-related methods have zero code path touching any deletion-status-mutation API. This is verified structurally in Task 05 and must remain true even as the module evolves — any future contributor adding a "quick cancel" shortcut to this screen would violate FR-8's mandated separation.

## 26. Library Requirements
No new third-party libraries.

## 27. Testing
1. **UI test (mandatory, highest priority):** selecting "Account Deletion Cancellation" and submitting calls `SupportRepository.submitTicket()` with the correct category value, and this repository method has zero code path touching any deletion-status-mutation endpoint — a structural test confirming this module's entire API surface for this action is limited to ticket creation only (§7 item 4).
2. UI test: `TicketDetailScreen` displays the stage-indicator prominently, correctly reflecting `submitted`/`in_progress`/`resolved` (§7 item 5).
3. UI test: submission network failure preserves the local draft (category + message text) and offers retry, never silently discarding it.
4. UI test: successful submission for an expedited category shows the priority-queue confirmation context.
5. Integration test: full FAQ-search → ticket-submission → status-tracking flow (cross-references K-03).
6. Integration test: full Account-Deletion-Cancellation ticket flow confirming zero client-side deletion-status mutation anywhere in the call chain.
7. UI test: RTL layout for category selector and stage indicator.

## 28. Documentation
KDoc on `SupportRepository`'s ticket methods and `ContactSupportFormViewModel` explicitly stating: "This module creates and tracks tickets only — it must never call or reference any deletion-cancellation-mutation API," citing FR-8 and B-04 §3.5.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Routes and Extend SupportRepository with Ticket Methods**
- Task ID: K04-T01
- Objective: Navigation destinations and the ticket half of the shared repository contract.
- Why This Is Required: Foundation, and the exact point where the structural API-surface guarantee is established.
- Existing Architecture to Follow: `Route` pattern; K-03's `SupportRepository` interface (extend, don't fork).
- Existing Files to Reuse: `SupportRepository.kt` (K-03), `Route`, `NoorResult<T>`.
- Files to Create: `ContactSupportFormRoute.kt`, `TicketHistoryRoute.kt`, `TicketDetailRoute.kt`.
- Files to Modify: `SupportRepository.kt` (add ticket method signatures per §10).
- Implementation Details: `TicketCategory` enum matching B-04's exact FR-9 wire values.
- Business Rules: FR-8, FR-9.
- Validation: N/A.
- Error Handling: N/A.
- Security: Interface surface deliberately excludes any deletion-mutation method.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: `analyticsName` per route.
- Tests: Covered in Task 05.
- Documentation: KDoc per §28.
- Dependencies: K-03's `SupportRepository`.
- Do Not Change: Do not modify K-03's FAQ methods on the same interface.
- Expected Result: Extended interface compiles.
- Definition of Done: `TicketCategory` values match B-04 exactly.

**Task 02 — Implement ContactSupportFormViewModel with Draft Preservation**
- Task ID: K04-T02
- Objective: Form state management with local-draft survival on failure/interruption.
- Why This Is Required: PRD §1.11 mandates never silently losing an in-progress submission.
- Existing Architecture to Follow: `BaseViewModel`, `DispatcherProvider`; lightweight local persistence pattern (single-row cache, not a full Room table unless the platform's convention prefers Room for all persistence — confirm before choosing a simpler mechanism like a DataStore/Preferences-equivalent per `CORE_DATASTORE_INSTRUCTIONS.md`, not read this pass).
- Existing Files to Reuse: `BaseViewModel`, `DispatcherProvider`, extended `SupportRepository` (Task 01).
- Files to Create: `ContactSupportFormViewModel.kt`.
- Files to Modify: none.
- Implementation Details: Draft state persisted locally on every field change (debounced); cleared only on confirmed successful submission; retry re-uses the preserved draft.
- Business Rules: §1.11.
- Validation: `category`/`message` required before submit enabled.
- Error Handling: Preserve-and-retry on network failure.
- Security: N/A.
- Performance: Debounced local persistence writes.
- Localization: N/A (ViewModel has no strings).
- RTL: N/A.
- Analytics: Fire `support_ticket_submitted`, `account_deletion_cancellation_ticket_submitted` (conditionally).
- Tests: Covered in Task 05.
- Documentation: KDoc, author tag.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Draft survives simulated app-kill/network-failure scenarios in tests.
- Definition of Done: All Task 05 tests pass.

**Task 03 — Implement TicketHistoryViewModel and TicketDetailViewModel**
- Task ID: K04-T03
- Objective: History list and detail/status-tracking state management.
- Why This Is Required: Core deliverable for ticket visibility.
- Existing Architecture to Follow: `BaseViewModel`, `DispatcherProvider`.
- Existing Files to Reuse: extended `SupportRepository`.
- Files to Create: `TicketHistoryViewModel.kt`, `TicketDetailViewModel.kt`.
- Files to Modify: none.
- Implementation Details: `TicketDetailViewModel` derives `TicketStageIndicator` state directly from server `status`; follow-up message submission with retry-on-failure (not silently lost, consistent with §1.11's spirit).
- Business Rules: §6.6, §7 item 5.
- Validation: Follow-up message non-empty.
- Error Handling: Standard retry.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: Fire `support_ticket_status_viewed`, `support_ticket_follow_up_added`.
- Tests: Covered in Task 05.
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: ViewModels functional against fake repository data.
- Definition of Done: Stage indicator correctly reflects all 3 status values.

**Task 04 — Implement Screen Composables and Deep-Link Wiring**
- Task ID: K04-T04
- Objective: Full visual delivery of all 4 screens plus the 3 deep-link URI mappings and the Deletion-Pending Countdown Banner entry point.
- Why This Is Required: Core deliverable, and the completion of C.25's KMP navigation surface.
- Existing Architecture to Follow: `:core:design-system` tokens; platform's deep-link registration mechanism (confirm exact pattern before implementation).
- Existing Files to Reuse: Design-system category-selector/stage-indicator primitives if they exist; C.21's Deletion-Pending Countdown Banner component if it already exists (do not invent it here if it doesn't — flag as a follow-up dependency instead).
- Files to Create: `ContactSupportFormScreen.kt`, `TicketSubmittedConfirmationScreen.kt`, `TicketHistoryScreen.kt`, `TicketDetailScreen.kt`, `components/TicketCategorySelector.kt`, `components/TicketStageIndicator.kt`.
- Files to Modify: `di/ParentNotificationsSupportModule.kt`, navigation graph, C.21's countdown banner (if present).
- Implementation Details: Per §11; `noorheroes://parent/support`, `noorheroes://parent/support/tickets/{id}` deep-link registration.
- Business Rules: §6.8, §7 item 4.
- Validation: N/A.
- Error Handling: Per §18.
- Security: N/A.
- Performance: N/A.
- Localization: All strings via localization package.
- RTL: Layout mirrors correctly.
- Analytics: N/A (fired from ViewModels).
- Tests: Covered in Task 05.
- Documentation: KDoc.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All 4 screens render correctly; deep links resolve correctly.
- Definition of Done: Matches §11, §6.8.

**Task 05 — Write Test Suite Including the Structural Ticket-Only Test**
- Task ID: K04-T05
- Objective: Cover §27, with case 1 as the mandatory centerpiece.
- Why This Is Required: PRD §7 item 4 — the top-priority guarantee for this sub-feature.
- Existing Architecture to Follow: Kotlin test + Compose UI testing conventions; static import-graph/reflection inspection for the structural test.
- Existing Files to Reuse: none new.
- Files to Create: `ContactSupportFormViewModelTest.kt`, `SupportRepositoryTicketOnlyStructuralTest.kt`.
- Files to Modify: none.
- Implementation Details: All 7 cases from §27; the structural test inspects `SupportRepository`'s implementation and `ContactSupportFormViewModel`'s call graph for any reference to a deletion-mutation API/class.
- Business Rules: FR-8.
- Validation: N/A.
- Error Handling: N/A.
- Security: Test 1 and 6 are the security/trust-critical tests for this entire blueprint.
- Performance: N/A.
- Localization: N/A.
- RTL: RTL layout test.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings citing FR-8.
- Dependencies: Tasks 01–04.
- Do Not Change: N/A.
- Expected Result: All pass.
- Definition of Done: 100% of §27 green, including the structural/behavioral guarantee.

## 30. Definition of Done
`ContactSupportFormScreen`, `TicketSubmittedConfirmationScreen`, `TicketHistoryScreen`, `TicketDetailScreen` live and functional against B-04, Account Deletion Cancellation entry point wired, draft preservation on failure implemented, structurally proven to touch only ticket-creation endpoints, all tests green — this completes C.25's full KMP scope (K-01 through K-04).

## 31. Final Verification Checklist
- [ ] "Account Deletion Cancellation" is an explicit, clearly-labeled category option with helper text
- [ ] `SupportRepository`'s ticket methods have zero reference to any deletion-mutation API (tested)
- [ ] In-progress draft survives network failure and is never silently lost
- [ ] Stage indicator prominently reflects submitted/in_progress/resolved
- [ ] All 3 deep-link URIs resolve correctly
- [ ] RTL layout verified for category selector and stage indicator
- [ ] No hardcoded strings
