# B-03 — Fact Detail Retrieval API

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). Serves the full Fact Detail payload consumed by K-01's `FactDetailScreen` — the deeper "why" content behind the Home card's brief statement.

## 2. Parent Feature
B.18 — Islamic Facts Module

## 3. Sub-feature
1.3 Fact Detail Retrieval API (ID: B-03) — **User API**

## 4. Objective
Implement `GET /v1/facts/{id}` returning the complete fact payload with source citations, scholar-approval metadata, and a gracefully-resolved `related_content.available` flag, never producing a broken navigation reference.

## 5. Business Requirements
- FR-1, FR-6, FR-9 (§1.7).
- Acceptance Criteria: Fact Detail shows explanation, source references, scholar-approval indicator, related content/quiz link.
- Edge Case 6: related-content restructured (series renumbering) resolves to new canonical ID rather than breaking.
- Edge Case 9: offline cached fact, quiz needing connectivity shows a clear "needs internet" state.
- Error table: fetch failure → cached last-known data with staleness indicator, or friendly retry if no cache; withdrawn related-content link omitted gracefully; approval revoked mid-session does not abruptly alter an already-open view.
- NFR: Fact Detail load p95 < 400ms.

## 6. Existing Architecture
Extends `content` bounded context, `FactDetailService`, reusing B-01's approval-gated repository. Related-content availability resolved via a read-only call into the `content` module's existing content-eligibility check (same pattern as B.14 Favorites' `available` resolution).

## 7. Existing Code to Reuse
- B-01: `FactVersionRepository.get_published_version()`, `ScholarApprovalRepository`.
- `content` module's existing content-eligibility/availability check (confirm exact method name before assuming — likely `ContentRepository.is_available_for_child()` or equivalent per B.14's approach).
- `core/deps.py` → `get_current_child`.

## 8. Files to Create
- `src/noorheroes/modules/content/services/fact_detail_service.py` — `FactDetailService(BaseService)`.
- `src/noorheroes/modules/content/api/facts_router.py` (extend from B-02) — `GET /v1/facts/{id}`.
- `tests/modules/content/test_fact_detail_retrieval.py`.
- `tests/modules/content/test_fact_related_content_withdrawal.py`.

## 9. Files to Modify
- `src/noorheroes/modules/content/api/facts_router.py` (shared file with B-02, additive route).

## 10. Backend Requirements
- `GET /v1/facts/{id}`, auth `Depends(get_current_child)`.
- Returns full detail payload: `fact_id`, `text`, `explanation`, `topic`, `sources`, `scholar_approval` (with version/date), `jurisprudential_scope_note`, `related_content` (`content_id`, `content_type`, `available`), `linked_quiz_id`.
- `related_content.available` resolved by a live check against the referenced content's current eligibility/withdrawal state — `false` rather than a broken reference if stale/withdrawn (FR-9).
- If the related content was restructured (e.g., series renumbering), resolve to the new canonical content ID rather than failing (Edge Case 6) — delegate to the `content` module's existing restructuring-resolution mechanism (confirm exact mechanism per A.3 Edge Case 11 before assuming a new one is needed).
- `410 FACT_WITHDRAWN` if `fact.is_withdrawn = true`.
- Approval revocation mid-session must not retroactively alter a response the client already received — this endpoint simply serves the currently-valid published version at request time; no server-push invalidation is introduced.

## 11. KMP Requirements
Consumed by K-01 (`FactsRepository.getFactDetail()`). No KMP code produced here.

## 12. NextJS Requirements
N/A — child-facing endpoint.

## 13. API Contract
**Endpoint:** `GET /v1/facts/{id}`
**Auth:** Bearer, child-mode
**Response 200:**
```json
{
  "fact_id": "...",
  "text": "...",
  "explanation": "...",
  "topic": "...",
  "sources": [ { "type": "primary", "citation": "..." } ],
  "scholar_approval": { "approver_id": "...", "version": "v3", "approved_at": "..." },
  "jurisprudential_scope_note": "...",
  "related_content": { "content_id": "...", "content_type": "story", "available": true },
  "linked_quiz_id": "..."
}
```
**Error Codes:** `410 FACT_WITHDRAWN` (archived fact), `404` (unknown fact_id), `401` (invalid/missing session).

## 14. Database Requirements
Reads: `fact`, `fact_version`, `scholar_approval` (B-01 gated join). Read-only cross-module query into `content` module's content-eligibility tables for `related_content.available` resolution.

## 15. Validation
`fact_id` path param must be a valid UUID; malformed input → `422`.

## 16. Authentication
`Depends(get_current_child)`.

## 17. Authorization
Any authenticated child may fetch any published, non-withdrawn fact detail (no per-child restriction beyond age-band-appropriate text resolution already applied).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Fetch failure (DB/timeout) | Cached last-known data with staleness indicator; friendly retry if no cache |
| Related content withdrawn/stale | `related_content.available = false`, rest of payload unaffected |
| Fact withdrawn | `410 FACT_WITHDRAWN` |
| Unknown fact_id | `404` |
| Approval revoked mid-session | No retroactive alteration of already-served response; only future requests reflect exclusion (enforced naturally since this endpoint always re-queries `get_published_version()` fresh) |

## 19. Offline First
N/A — backend endpoint; offline caching is K-03's concern (client caches this response).

## 20. Local Data
N/A — backend.

## 21. Localization
Text/explanation/sources resolved per child's locale via `fact_version`.

## 22. RTL
N/A at API layer.

## 23. Analytics
None emitted server-side for this endpoint beyond standard request logging; client-side events (`fact_detail_viewed`, etc.) are K-01's concern.

## 24. Performance
p95 < 400ms target; single gated join plus one cross-module availability check per request; no N+1 risk since related-content resolution is a single lookup, not a collection.

## 25. Security
Approval-gate inherited from B-01; no new attack surface. `related_content.available` check prevents leaking existence of ineligible/withdrawn content via a resolvable reference.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async — existing platform dependencies.

## 27. Testing
- Unit: `related_content.available = false` for a withdrawn reference.
- Unit: restructured related-content resolves to new canonical ID (Edge Case 6).
- Unit: `410 FACT_WITHDRAWN` for archived fact.
- Integration: full detail payload shape matches §13 contract exactly.

## 28. Documentation
OpenAPI docstring documenting the `available` flag semantics and `410` error code.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `FactDetailService.get_detail()`**
Objective: Core detail-assembly logic including related-content availability resolution.
Files to Create: `services/fact_detail_service.py`.
Dependencies: B-01.
Expected Result: Assembles full payload per §13.
Definition of Done: Passes Task 03 tests.

**Task 02 — Implement Router Endpoint**
Objective: `GET /v1/facts/{id}` route.
Files to Modify: `api/facts_router.py`.
Dependencies: Task 01.
Definition of Done: Manual verification against dev DB.

**Task 03 — Tests**
Objective: Coverage per §27.
Dependencies: Tasks 01–02.
Definition of Done: All green.

**Task 04 — API Documentation**
Dependencies: Task 03.
Definition of Done: `/docs` accurate.

## 30. Definition of Done
- Full detail payload matches §13 contract.
- Withdrawn/restructured related-content handled without broken links.
- `410` for archived facts.
- Tests green, documentation updated.

## 31. Final Verification Checklist
- [ ] `related_content.available` correctly resolved for withdrawn/stale references
- [ ] Restructured content resolves to new canonical ID
- [ ] `410 FACT_WITHDRAWN` verified
- [ ] p95 < 400ms verified
- [ ] No broken links possible under any tested state
- [ ] Documentation updated
