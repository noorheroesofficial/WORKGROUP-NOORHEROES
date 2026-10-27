# Blueprint: Report PDF Export Service

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI). Module: `src/noorheroes/modules/dashboard/`. Delivers `POST /v1/parent/reports/{child_id}/export`, rendering the same governed report data as the in-app view as a downloadable PDF.

## 2. Parent Feature
C.22 — Per-Child Reports.

## 3. Sub-feature
B-07 — Report PDF Export Service.

## 4. Objective
Render a parent-facing PDF using the exact same aggregation function/service as the in-app JSON API, guaranteeing the export is never a separate, less-governed data path, and honoring the content-safety fallback and offline-block rules.

## 5. Business Requirements
Source: PRD §1.7 FR-11, §1.9 Acceptance Criteria, §1.10 Edge Case #7, #9, §3.4, §5 item 4.
- Export PDF produces content identical in governance (no raw transcript, no diagnosis, no sibling comparison) to the in-app view — not a separate export-specific data path (FR-11).
- p95 < 3s generation time (PRD NFR).
- Export requested against a `content_safety_passed = false` report falls back to the last passing report (Edge Case #7).
- Export requested offline is blocked with a clear "needs internet" message (Edge Case #9).

## 6. Existing Architecture
Depends on B-01's `get_per_child_report()` (or the relevant underlying report's aggregation function for the specific report type being exported) as its sole data source — the PDF Export Service is a rendering layer over already-aggregated, already-validated data, never an independent query path.

## 7. Existing Code to Reuse
- `DashboardAggregationService.get_per_child_report()` (B-01) — the single call this service must invoke for data.
- `ContentSafetyValidator` fallback pattern (C.20) — reused for the content-safety-failed-report fallback.
- `require_parent_session_only` (C.20 B-01).
- Confirmed via codebase-wide search: **no PDF rendering library exists anywhere in the platform today** (no invoice/receipt/certificate export precedent found) — this is a genuinely new dependency decision, not a name to recover from an existing pattern. Recommend **WeasyPrint** (HTML/CSS-to-PDF, native RTL/bidi text support via its Pango/Cairo backend, no headless-browser overhead) as the default choice given the RTL requirement in §22, but this selection requires architecture sign-off before adding to `pyproject.toml`, per project instruction #30 — do not silently install it without that confirmation.
- `MediaService`'s existing R2 pre-signed URL / CDN signing infrastructure (established in A.3 B-07, `infrastructure/` CDN signing integration) — reused for this endpoint's signed `pdf_url`, not a new signing mechanism.

## 8. Files to Create
- `src/noorheroes/modules/dashboard/pdf_export.py` — `ReportPdfExportService`
- `tests/modules/dashboard/test_report_pdf_export_service.py`

## 9. Files to Modify
- `src/noorheroes/modules/dashboard/schemas.py` — add `PdfExportResponse`
- `src/noorheroes/modules/dashboard/api.py` — add `POST /v1/parent/reports/{child_id}/export`
- `pyproject.toml` — add `weasyprint` (pending architecture sign-off per §7)

## 10. Backend Requirements
- Route: `POST /v1/parent/reports/{child_id}/export`, gated by `require_parent_session_only` + family-ownership.
- `ReportPdfExportService.export(parent_ctx, child_id)`:
  1. Check the requesting parent is online-authenticated (this is inherently true for any live request; the "offline block" per Edge Case #9 is enforced client-side by K-07 checking connectivity before ever calling this endpoint — this service does not need a server-side offline concept, but must document that it assumes a live request).
  2. Call the **same** `DashboardAggregationService.get_per_child_report()` (B-01) used by the JSON API — never a parallel query path.
  3. If the underlying report's `content_safety_passed = false`, fall back to the most recent `content_safety_passed = true` report (Edge Case #7).
  4. Render the aggregated data to PDF via the platform's PDF rendering library.
  5. Upload the rendered PDF to storage; generate a signed, short-TTL `pdf_url` + `expires_at`.
- No caching of rendered PDFs beyond the signed URL's TTL — each export call re-renders from current data (reports are living data, not fixed artifacts, until the point of export).

## 11. KMP Requirements
Consumed by K-07 (`PdfExportFlow`), which shows the "Generating your report..." progress state during the call and hands off to the OS share/save sheet on success.

## 12. NextJS Requirements
N/A.

## 13. API Contract
- **HTTP Method:** POST
- **Endpoint:** `/v1/parent/reports/{child_id}/export`
- **Auth:** Bearer, parent session only
- **Request:** path `child_id: str`; body: none (or optional `report_type` if exporting a specific report type beyond the default per-child report — confirm scope with product before adding)
- **Response 200:**
```json
{ "pdf_url": "string (signed, short-TTL)", "expires_at": "ISO-8601" }
```
- **Authentication:** Bearer parent session
- **Authorization:** Family-ownership on `child_id`
- **Validation:** `child_id` required
- **Error Responses:** `403`/`404` `ChildScopeViolationError`, `401` invalid session, `500`/`503` PDF generation failure

## 14. Database Requirements
No new tables; reads from the same sources as B-01, writes only to object storage (PDF file), not to a new DB table.

## 15. Validation
`child_id` required, family-owned.

## 16. Authentication
Bearer parent session.

## 17. Authorization
Family-ownership check, additive to the parent-session gate.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Cross-family `child_id` | `403`/`404` `ChildScopeViolationError` |
| Underlying report `content_safety_passed = false` | Falls back to last passing report (Edge Case #7) |
| PDF rendering failure | `500`/`503`, retryable |
| Client offline | Blocked client-side before this endpoint is ever called (Edge Case #9, enforced by K-07) |

## 19. Offline First
N/A server-side by design — this write action requires a live, server-validated payload; the offline block is a client-side (K-07) responsibility per Edge Case #9.

## 20. Local Data
N/A (backend).

## 21. Localization
PDF content uses the same locale-resolved copy as the in-app view, respecting the parent's selected locale (English/Hindi/Arabic/Urdu) including RTL text layout in the rendered PDF for Arabic/Urdu.

## 22. RTL
WeasyPrint (recommended in §7) supports `dir: rtl` CSS and Arabic/Urdu shaping via its Pango text backend, satisfying this requirement out of the box — if a different library is chosen during architecture sign-off, re-verify RTL capability before implementation, and flag as an architecture gap requiring escalation (project instruction #24) rather than silently shipping LTR-only PDFs for RTL locales.

## 23. Analytics
`report_pdf_export_initiated` / `report_pdf_export_completed` fired client-side (K-07).

## 24. Performance
p95 < 3s generation time (PRD NFR) — profile the rendering step specifically; if the aggregation call itself is slow, rely on B-01's existing cache rather than optimizing rendering at the expense of data freshness.

## 25. Security
Signed, short-TTL download URL prevents indefinite public access to a generated PDF; PDF content inherits every governance guarantee of the underlying aggregated data (no raw transcript, no raw score, no sibling comparison, no diagnosis).

## 26. Library Requirements
`weasyprint` — new dependency, none exists on the platform today (verified by codebase search); requires architecture sign-off before addition per §7.

## 27. Testing
1. Unit test: PDF export calls the identical aggregation function as the JSON API (mocked to assert same call signature/service instance).
2. Unit test: content-safety-failed report triggers fallback to last passing report.
3. Unit test: cross-family `child_id` rejected.
4. Unit test: signed URL has correct short TTL and `expires_at`.
5. Performance test: p95 < 3s under representative load.
6. Integration test: full export request through the gate, PDF successfully generated and retrievable via the signed URL.

## 28. Documentation
OpenAPI docstring explicitly stating the "same aggregation path as the JSON API" guarantee.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement ReportPdfExportService Using Shared Aggregation Call**
- Task ID: B07-T01
- Objective: Build the export service, sourcing data exclusively from B-01's aggregation function.
- Why This Is Required: FR-11's core guarantee — no parallel data-fetch path.
- Existing Architecture to Follow: `BaseService` pattern.
- Existing Files to Reuse: `DashboardAggregationService.get_per_child_report()`.
- Files to Create: `pdf_export.py`.
- Files to Modify: none.
- Implementation Details: Per §10 steps 2–5.
- Business Rules: FR-11, Edge Case #7.
- Validation: Family-ownership.
- Error Handling: Per §18.
- Security: Signed URL generation.
- Performance: p95 < 3s target.
- Localization: RTL-aware rendering.
- RTL: Verify library support.
- Analytics: N/A (client-side).
- Tests: Covered in Task 03.
- Documentation: Docstring citing FR-11.
- Dependencies: B-01.
- Do Not Change: `DashboardAggregationService.get_per_child_report()` signature.
- Expected Result: Service renders and uploads PDF correctly.
- Definition of Done: Task 03's "same call" test passes.

**Task 02 — Implement Route**
- Task ID: B07-T02
- Objective: Expose `POST /v1/parent/reports/{child_id}/export`.
- Why This Is Required: Public contract delivery.
- Existing Architecture to Follow: Router `Depends()` pattern.
- Existing Files to Reuse: `api.py`.
- Files to Create: none.
- Files to Modify: `api.py`.
- Implementation Details: `@router.post("/reports/{child_id}/export", response_model=PdfExportResponse)`.
- Business Rules: FR-11.
- Validation: Per §15.
- Error Handling: Per §18.
- Security: Inherits gate.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 03.
- Documentation: OpenAPI summary.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Endpoint live.
- Definition of Done: Matches §13.

**Task 03 — Write Test Suite**
- Task ID: B07-T03
- Objective: Cover §27, with the "same aggregation call" test as the highest-priority guarantee.
- Why This Is Required: FR-11 verification.
- Existing Architecture to Follow: pytest + fixtures, mocking to assert call-path identity.
- Existing Files to Reuse: Family/child/session fixtures.
- Files to Create: `test_report_pdf_export_service.py`.
- Files to Modify: none.
- Implementation Details: 6 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact responses.
- Security: Fallback test is critical.
- Performance: p95 assertion.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings.
- Dependencies: Tasks 01–02.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green.

## 30. Definition of Done
`POST /v1/parent/reports/{child_id}/export` live, gated, sources data exclusively via B-01's aggregation call, falls back correctly for content-safety-failed reports, p95 < 3s achieved, all tests green.

## 31. Final Verification Checklist
- [ ] PDF generation pipeline verified to call the identical aggregation function as the JSON API (no parallel data-fetch)
- [ ] Content-safety-failed-report fallback verified
- [ ] Signed, short-TTL URL verified
- [ ] p95 < 3s generation time verified under load test
- [ ] RTL PDF rendering capability verified or gap escalated
- [ ] OpenAPI docs state the shared-aggregation guarantee
