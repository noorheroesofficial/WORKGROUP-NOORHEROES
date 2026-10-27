# N-03 — Recommendation Explainability Viewer

## 1. Feature Context
NoorHeroes Admin Portal (NextJS). Read-only investigation tool letting Trust & Safety staff inspect exactly which signals drove a specific historical recommendation and confirm it passed the AI Safety Filter — critical for investigating parent complaints about inappropriate suggestions.

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization

## 3. Sub-feature
3.3 Recommendation Explainability Viewer (ID: N-03)

## 4. Objective
Build a search-by-masked-child-identifier + timestamp interface rendering a read-only breakdown of a historical recommendation decision: signals used, candidate set before/after the AI Safety Filter, and filter-pass confirmation, restricted to the `trust_safety` RBAC role with access itself logged as a sensitive-data-view event.

## 5. Business Requirements
Per PRD §8, §9 item 3, §12.5:
- Search by masked `child_id` + timestamp.
- Read-only breakdown: signals used (age band, mastery gap, recent skips, etc.), candidate set before/after AI Safety Filter, filter-pass confirmation.
- No edit/delete actions — pure investigation tool.
- Restricted to `trust_safety` role; access is itself logged as a sensitive-data-view audit event (since it surfaces masked per-child behavioral signal data).

## 6. Existing Architecture
Follow `NEXT-JS-INSTRUCTIONS.md` for admin RBAC-gated route conventions. Consumes B-02's `recommendation_decision_log` table via an admin read API.

## 7. Existing Code to Reuse
Existing Admin Portal RBAC route-guard pattern; existing audit-logging-on-sensitive-view convention if one exists elsewhere in the admin portal (e.g., from other "view masked user data" tools).

## 8. Files to Create
- `app/(admin)/recommendation-explainability/page.tsx`
- `components/recommendation-explainability/SearchForm.tsx`
- `components/recommendation-explainability/DecisionBreakdownView.tsx`
- `lib/api/recommendationExplainability.ts`
- `types/recommendationExplainability.ts`

## 9. Files to Modify
- Admin navigation/sidebar config (visible only to `trust_safety` role)

## 10. Backend Requirements
Consumes an admin read endpoint over B-02's `recommendation_decision_log` table (owned by B-02; if B-02's blueprint did not expose a dedicated admin-read endpoint, flag here that this sub-feature depends on one being added to B-02's scope — search by masked/hashed `child_id` requires the search input to be hashed identically to how B-02 stored it, per B-02 Task 05's documented hashing scheme).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Search form: masked/partial `child_id` identifier input + date/timestamp range picker.
- Results view: read-only breakdown showing signals used, before/after candidate sets (as a diff-style or two-column view), and a clear pass/fail indicator for the AI Safety Filter.
- No edit/delete/create UI affordances anywhere on this page — enforced by simply not building any mutation UI (not by disabling one).
- Page-level route guard restricted to `trust_safety` role.
- Every successful view of a decision-log record triggers a client-initiated (or server-side, preferably) audit-log write recording the sensitive-data-view event.

## 13. API Contract
**Admin API** (read-only):
- `GET /admin/v1/recommendations/explain?child_id_hash=...&from=...&to=...` — Auth: Admin Bearer, `trust_safety` role required — Response: matching decision-log records with signals/candidate-set/filter-pass detail.

## 14. Database Requirements
Reads `recommendation_decision_log` (owned by B-02's migration). No writes from this sub-feature except the audit-log-on-view event (if implemented server-side, this may be a backend responsibility triggered by the admin API call itself rather than a separate client-side write — confirm ownership with B-02/platform audit-logging conventions before implementing a duplicate client-side audit call).

## 15. Validation
Search input must be hashed using the exact same hash function B-02 used to store `child_id_hash` in `recommendation_decision_log` (per B-02 Task 05) — mismatched hashing would silently return zero results rather than erroring, so this must be verified explicitly in integration testing, not assumed correct.

## 16. Authentication
Existing Admin Portal Bearer-session auth.

## 17. Authorization
Strictly restricted to `trust_safety` RBAC role (route-level guard, not just a hidden nav entry — direct URL access must also be blocked for non-`trust_safety` admins).

## 18. Error Handling
No-results state (clear "no matching records" message, distinct from an error); API/auth error states handled gracefully; malformed search input rejected with inline validation before submission.

## 19. Offline First
Not applicable (admin web portal).

## 20. Local Data
Not applicable.

## 21. Localization
Admin Portal UI chrome localized per existing convention; underlying signal/candidate data displayed as-is (raw investigative data, not typically translated).

## 22. RTL
Per existing Admin Portal RTL support convention.

## 23. Analytics
Not specified as required beyond the mandatory sensitive-data-view audit logging (§12), which is a security/compliance requirement, not a product-analytics one — treat distinctly.

## 24. Performance
Search should be reasonably fast even as `recommendation_decision_log` grows — relies on B-02's indexing (hashed child_id + timestamp) being adequate; flag to B-02 if query performance becomes an issue at scale.

## 25. Security
This is the most security-sensitive admin surface in the A.2 feature set: strict RBAC (`trust_safety` only), no mutation capability whatsoever, and mandatory audit-logging on every view (viewing masked behavioral data about a specific child is itself a sensitive action that must be traceable).

## 26. Library Requirements
Next.js, existing Admin Portal RBAC/route-guard library, existing admin API-client conventions.

## 27. Testing
- Component test: search form validation and submission.
- Component test: read-only breakdown view renders correctly with fixture decision-log data, confirming no edit/delete controls are present anywhere in the DOM.
- Integration test: non-`trust_safety` admin attempting direct URL access is blocked (not just hidden from nav).
- Integration test: viewing a record triggers the sensitive-data-view audit-log write.
- Integration test: search-hash correctness verified end-to-end against B-02's actual hashing scheme (not just unit-mocked).

## 28. Documentation
Page-level documentation emphasizing this is a read-only, `trust_safety`-restricted, audit-logged investigation tool — explicitly warn future contributors against adding any mutation capability to this page.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Types & API Client (Read-Only)**
- Objective: Typed contract for the explainability read API.
- Why Required: Foundation for search/results components.
- Existing Architecture to Follow: Existing admin-portal API-client conventions.
- Existing Files to Reuse: Existing typed-fetch wrapper.
- Files to Create: `types/recommendationExplainability.ts`, `lib/api/recommendationExplainability.ts`
- Files to Modify: none
- Implementation Details: `DecisionLogRecord { childIdHash, generatedAt, signals, candidateSetBefore, candidateSetAfter, filterPass }`; `searchDecisionLogs(childIdHashOrQuery, from, to)` — client submits a search value that the API hashes server-side (preferred, to avoid client-side hashing-scheme drift) or, if client-side hashing is required, uses a shared/exported hashing utility matching B-02's exact implementation, not a reimplementation.
- Business Rules: Read-only client — no create/update/delete methods defined in this API client at all.
- Validation: N/A.
- Error Handling: Typed error results, explicit "no results" vs. "error" distinction.
- Security: No mutation methods exist in this client by design.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Unit tests for the API client (mocked fetch), including a no-results-vs-error distinction test.
- Documentation: TSDoc explicitly noting read-only design.
- Dependencies: B-02's admin read endpoint (coordinate before finalizing).
- Do Not Change: N/A.
- Expected Result: Read-only typed client.
- Definition of Done: Unit tests pass.

**Task 02 — Build `SearchForm` Component**
- Objective: Masked-identifier + date-range search input.
- Why Required: Primary entry point for investigation.
- Existing Architecture to Follow: Existing admin form conventions.
- Existing Files to Reuse: Existing date-range-picker component if present.
- Files to Create: `components/recommendation-explainability/SearchForm.tsx`
- Files to Modify: none
- Implementation Details: Search input + date-range picker, client-side validation before submission.
- Business Rules: N/A.
- Validation: Malformed input rejected before API call.
- Error Handling: Inline validation errors.
- Security: N/A.
- Performance: N/A.
- Localization: Labels localized.
- RTL: Per §22.
- Analytics: N/A.
- Tests: Component tests for validation and submission.
- Documentation: TSDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working search form.
- Definition of Done: Component tests pass.

**Task 03 — Build `DecisionBreakdownView` (Read-Only) + Page Assembly with RBAC Guard**
- Objective: Read-only results view and full page with strict role gating and audit logging.
- Why Required: Core deliverable; PRD §12.5's mandatory audit-on-view requirement.
- Existing Architecture to Follow: Existing Admin Portal RBAC route-guard and audit-logging conventions.
- Existing Files to Reuse: Existing RBAC guard component/HOC, existing audit-logging utility if present.
- Files to Create: `components/recommendation-explainability/DecisionBreakdownView.tsx`, `app/(admin)/recommendation-explainability/page.tsx`
- Files to Modify: Admin navigation config (visible to `trust_safety` only), route-level RBAC guard registration
- Implementation Details: Renders signals list, before/after candidate-set comparison, filter-pass badge — purely presentational, zero interactive mutation elements; page wrapped in a `trust_safety`-only route guard blocking even direct URL access for other roles; view triggers an audit-log write (prefer having the backend admin API log the view server-side on each successful `GET`, since that's more tamper-resistant than a client-initiated log call — confirm this is how B-02/the platform's audit convention works before implementing a client-side log call as a fallback).
- Business Rules: No edit/delete/create controls anywhere on this page, verified explicitly in tests.
- Validation: N/A.
- Error Handling: No-results and error states distinct.
- Security: `trust_safety`-only RBAC gate; audit-logged views; this is the core security requirement of the whole sub-feature.
- Performance: N/A.
- Localization: Labels localized.
- RTL: Per §22.
- Analytics: N/A (audit logging is a security/compliance mechanism, tracked separately from product analytics).
- Tests: Component test confirming absence of any mutation UI; integration test for RBAC route-guard blocking non-`trust_safety` roles even via direct URL; integration test confirming audit-log write occurs on view.
- Documentation: Page comment per §28.
- Dependencies: Tasks 01, 02.
- Do Not Change: Never add mutation capability to this page.
- Expected Result: Complete, strictly read-only, audit-logged investigation tool.
- Definition of Done: All tests pass, including the RBAC-bypass-attempt test.

## 30. Definition of Done
Trust & Safety staff can search and inspect historical recommendation decisions read-only, with strict `trust_safety`-only access and mandatory audit logging on every view; all tests green.

## 31. Final Verification Checklist
- [ ] Search by masked identifier + date range returns correct results
- [ ] Zero mutation UI elements exist anywhere on this page (verified by test, not just review)
- [ ] Direct URL access blocked for non-`trust_safety` roles
- [ ] Every successful view writes a sensitive-data-view audit-log entry
- [ ] Search-hash correctness verified against B-02's actual hashing scheme end-to-end
- [ ] No-results state distinct from error state
- [ ] All tests pass
