# N-08 — Parent Web Portal Data Export Request & Tracking

## 1. Feature Context
Part of Feature D.27 — Parent Web Account Portal. This is D.27's cleanest cross-surface-consistency showcase: the Data Export screen calls the exact same `data_request` record C.26 B-03 already built to be surface-agnostic by design — its `get_status()` method has zero branching logic of any kind, verified by that blueprint's own test suite.

## 2. Parent Feature
D.27 Parent Web Account Portal (`account.noorheroes.com`)

## 3. Sub-feature
**N-08 — Parent Web Portal Data Export Request & Tracking**

## 4. Objective
Build the Data Export Request and Export Status Tracking screens against C.26 B-03's existing, already-surface-agnostic export contract, requiring zero new backend accommodation.

## 5. Business Requirements
- FR-10: "Data Export screen: request and track status identically to C.26's mobile flow — the exact same `data_requests` record, queryable consistently from both surfaces."
- §1.9 Acceptance Criteria: "Given a parent requests a data export from the web portal, when they later check status from the Mobile App, then both surfaces show the identical current state."
- C.26 B-03 (inherited): idempotent dedup — a duplicate request while one is `preparing` returns the existing `request_id`, never a second job.

## 6. Existing Architecture
Fully confirmed, no gaps. C.26 B-03 ("Data Export Request & Status API") is purpose-built for exactly this cross-surface use case — its own Definition of Done states it is "ready to be consumed identically by D.27's web portal once built," and its `get_status()` method is explicitly documented and tested to have "no surface-specific branching of any kind." This sub-feature is the most direct, lowest-risk consumer in the entire D.27 document.

## 7. Existing Code to Reuse
- C.26 B-03's `POST /v1/data-requests/exports`, `GET /v1/data-requests/{id}` — consumed unmodified.
- N-02's `apiClient`, `StepUpModal`.

## 8. Files to Create
- `noorheroes-account-portal/src/app/(portal)/data-export/page.tsx`
- `noorheroes-account-portal/src/app/(portal)/data-export/status/[requestId]/page.tsx`
- `noorheroes-account-portal/src/features/data-export/api/data-export-client.ts`
- `noorheroes-account-portal/tests/features/data-export/cross-surface-consistency.test.ts`

## 9. Files to Modify
- N-02's `allowed-endpoints.ts` — register `POST /v1/data-requests/exports`, `GET /v1/data-requests/{id}`.

## 10. Backend Requirements
Consumes C.26 B-03 exclusively, zero new backend work required — the cleanest reuse case in this document.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Data Export Request screen: single "Request Export" action, `StepUpModal`-gated, calling `POST /v1/data-requests/exports`.
- On response (whether `200` existing-in-progress or `201` new — note C.26 B-03 §11 flags the PRD's own `222` status code as a likely documentation typo requiring confirmation; this screen must not special-case a `222` response), navigate to Export Status Tracking with the returned `request_id`.
- Export Status Tracking screen: polls or displays `GET /v1/data-requests/{id}`, showing `preparing|ready|failed`; download link shown when `ready` with a `download_url`.
- Loading/error states.
- Fire `web_data_export_requested`, `web_data_export_status_viewed`.

## 13. API Contract
Consumes C.26 B-03's contract exactly as documented in that blueprint. If the PRD's `222` status code reference is confirmed to be a typo (per that blueprint's own flag), this screen must handle `200`/`201` only.

## 14. Database Requirements
Not applicable (frontend).

## 15. Validation
`requestId` route param passed through; ownership enforced server-side (C.26 B-03 §15, family-ownership check).

## 16. Authentication
Requires active `SessionContext`.

## 17. Authorization
Export request requires fresh `StepUpModal` elevation (FR-3); status polling requires only an active session.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Duplicate request while `preparing` | Server returns the existing `request_id` unchanged (C.26 B-03's idempotent dedup) — this screen simply displays that status, no special duplicate-request UI needed |
| Export job fails (`status: failed`) | Status screen shows failure state, no download link |
| Status query for a request not owned by the family | `403`/`404`, standard error handling |

## 19. Offline First
Not applicable for the request action; status polling could degrade to "last known state shown, retry when back online" if the parent's connection drops mid-poll, consistent with N-02's offline banner.

## 20. Local Data
Not applicable beyond N-02's in-memory session state; no export content itself is cached client-side.

## 21. Localization
Full EN/HI/AR/UR localization of status labels and copy.

## 22. RTL
Full RTL layout.

## 23. Analytics
`web_data_export_requested`, `web_data_export_status_viewed` (§1.19).

## 24. Performance
Trivial request/poll pattern; export generation itself is async server-side (C.26 B-03), this screen only displays state.

## 25. Security
- Relies entirely on C.26 B-03's existing family-scoping and signed, time-limited download URLs — this sub-feature introduces no new security logic.
- Requesting an export is step-up gated per FR-3, consistent with every other sensitive action in this portal.

## 26. Library Requirements
No new libraries beyond N-02's established stack.

## 27. Testing
- Integration: request flow requires `StepUpModal` elevation before the call fires.
- Integration: duplicate request while `preparing` correctly displays the existing request's status rather than erroring.
- Integration: status screen correctly renders `preparing`/`ready`/`failed` states.
- **Cross-surface consistency test (highest priority, per Acceptance Criteria):** a request initiated via this screen's fixture is confirmed queryable and shows identical status/fields as the same request would via a simulated Mobile App call — proving no surface-specific branching was accidentally introduced on the frontend side either.

## 28. Documentation
Cross-reference C.26 B-03's own Definition of Done, which already anticipated and named this exact sub-feature as its intended second consumer.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm the `222` Status Code Discrepancy**
- **Objective:** Confirm with C.26 B-03's owning team whether `222` is a documentation typo (as flagged in that blueprint) before this screen's response-handling code is finalized.

**Task 02 — Build `data-export-client.ts`**
- **Files to Create:** `data-export-client.ts`.

**Task 03 — Build Request and Status Tracking Screens**
- **Files to Create:** `page.tsx`, `status/[requestId]/page.tsx`.

**Task 04 — Write the Cross-Surface Consistency Test**
- **Files to Create:** `cross-surface-consistency.test.ts`.

**Task 05 — Localization, RTL, Analytics, Full Test Suite**

## 30. Definition of Done
A parent can request and track a data export from the web portal, reading and writing the exact same `data_request` record as the Mobile App, with a passing cross-surface consistency test and the `222`-status-code ambiguity resolved before shipping.

## 31. Final Verification Checklist
- [ ] `222` status code discrepancy resolved (Task 01)
- [ ] Export request gated behind fresh step-up elevation
- [ ] Duplicate-request-while-preparing correctly displays existing status, no error
- [ ] Cross-surface consistency test passes
- [ ] Full localization and RTL verified
