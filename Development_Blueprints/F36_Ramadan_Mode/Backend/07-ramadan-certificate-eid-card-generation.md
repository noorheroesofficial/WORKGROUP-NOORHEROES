# B-07 — Ramadan Certificate & Eid Card Generation

## 1. Feature Context
Generates a shareable end-of-Ramadan certificate and a separate Eid celebration card, both behind Parent Gate verification and both reusing A.11's existing Share Card Service pattern end-to-end — including its PII-exclusion guarantee — rather than building a new generation/rendering pipeline.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
1.7 Ramadan Certificate & Eid Card Generation (ID: **B-07**)

## 4. Objective
Build `POST /v1/ramadan/certificates` and `POST /v1/ramadan/eid-cards`, both Parent-Gate-verified and both delegating rendering/storage to A.11's existing Share Card Service.

## 5. Business Requirements
- FR-6: certificate generation/share via the standard Parent Gate.
- §3.4: Auth = Parent Gate verification; generated artifact excludes child ID/DOB/location.
- §12.6: certificate/Eid-card generation reuses A.11's exact PII-exclusion guarantee.

## 6. Existing Architecture
`ramadan` bounded context, `app/ramadan/routers/certificate_router.py`, delegating to A.11's existing `app/rewards/services/share_card_service.py::ShareCardService` (exact class name to confirm against `rewards` context, §5.9) for actual rendering — this module supplies only the Ramadan-specific data payload (nights completed, child's display name if permitted, season badge).

## 7. Existing Code to Reuse
- A.11's `ShareCardService` (rendering/storage/PII-exclusion pattern — confirm exact class before implementation)
- `core/deps.py::require_elevated_session` (Parent Gate step-up)
- `app/shared/base_service.py::BaseService`

## 8. Files to Create
- `app/ramadan/routers/certificate_router.py`
- `app/ramadan/services/certificate_service.py`
- `app/ramadan/repositories/certificate_repository.py`
- `app/ramadan/schemas/certificate_schema.py`
- `app/ramadan/models/certificate.py`
- `alembic/versions/xxxx_create_ramadan_certificates_table.py`

## 9. Files to Modify
- `app/ramadan/routers/__init__.py` — register router

## 10. Backend Requirements
- `CertificateService.generate_certificate(child_id, requesting_parent)`: assembles the Ramadan-specific data payload (nights completed, badges earned within `season_id` scope) and calls A.11's `ShareCardService` to render/store it, persisting only `certificate_url`/`generated_at` in `ramadan_certificates` — no independent rendering logic in this module.
- `CertificateService.generate_eid_card(child_id, requesting_parent)`: same pattern for the Eid card, reusing A.11's service; Eid-card artifacts may or may not need their own table depending on whether A.11's `ShareCardService` already persists a generic share-artifact record (confirm before adding `ramadan_eid_cards` — avoid a redundant table if A.11 already tracks generated artifacts generically).
- PII exclusion enforced at the payload-assembly step — child ID, DOB, and location are never included in the data handed to `ShareCardService`.

## 11. Required API / API Contract
`POST /v1/ramadan/certificates`, `POST /v1/ramadan/eid-cards` → `200 { certificate_url }` / `{ card_url }`. **Auth:** Parent Gate (`require_elevated_session`). **Validation:** `child_id` must belong to the requesting parent's family. **Error Responses:** `403` if Parent Gate step-up is missing/expired; `422` if the child has no completed nights to certify (for the certificate specifically).

## 12. Database Requirements
`ramadan_certificates(certificate_id PK, child_id FK, certificate_url, generated_at)`; index `(child_id, generated_at DESC)`. PII-excluded artifact per §4.2.

## 13. Validation
`child_id` ownership check; certificate generation requires at least one completed night (business rule — a certificate for zero progress is not meaningful; confirm minimum threshold with product if not explicit elsewhere).

## 14. Authentication
`get_current_parent` plus `require_elevated_session` (Parent Gate step-up).

## 15. Authorization
Parent Gate verification required for both endpoints given they produce shareable, potentially externally-distributed artifacts.

## 16. Error Handling
Rendering/storage failure in A.11's `ShareCardService` → propagate a clear retry-eligible error, do not silently succeed with a broken URL.

## 17. Offline First
N/A — generation requires a live connection; not a cached/offline operation.

## 18. Local Data
N/A server-side.

## 19. Localization
Certificate/card text localized per the child's/family's active locale (En/Hi/Ar/Ur) — delegated to A.11's existing localized-rendering support if present; confirm A.11's `ShareCardService` already handles this before assuming it does.

## 20. RTL
Delegated to A.11's existing rendering pipeline for Ar/Ur artifacts.

## 21. Analytics
`ramadan_certificate_generated`, `ramadan_certificate_shared`, `ramadan_eid_card_generated` per §1.19.

## 22. Performance
Rendering is inherently a heavier, less-frequent operation — reuse A.11's existing async/queued rendering pattern if one exists rather than a synchronous blocking call.

## 23. Security
PII exclusion (no child ID/DOB/location in the generated artifact) is this sub-feature's core guarantee, mandatory-tested; Parent Gate step-up required before any generation call proceeds.

## 26. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async. Reuses A.11's existing rendering library/dependency — no new rendering library added here.

## 27. Testing
Unit: PII-exclusion at the payload-assembly step. Integration: **mandatory** — generated artifact contains zero PII fields; Parent-Gate-missing request is rejected; full Parent-Gate → generate → persist flow succeeds end-to-end for both certificate and Eid card.

## 28. Documentation
OpenAPI docstring for both endpoints noting the Parent Gate requirement and the PII-exclusion guarantee.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm A.11's `ShareCardService` Contract**
Objective: Identify exact method signature, PII-exclusion mechanism, and whether it already persists generated-artifact records generically. Files to Read: A.11's rewards-context service files. Definition of Done: findings documented before Task 02.

**Task 02 — Write Migration for `ramadan_certificates`**
Objective: Certificate-URL tracking table (Eid-card table only if Task 01 confirms A.11 doesn't already track it). Files to Create: `alembic/versions/xxxx_create_ramadan_certificates_table.py`, `models/certificate.py`. Dependencies: Task 01. Tests: migration test. Definition of Done: schema created.

**Task 03 — Implement `CertificateRepository`**
Objective: `(child_id, generated_at DESC)`-indexed reads/writes. Files to Create: `repositories/certificate_repository.py`. Dependencies: Task 02. Tests: repository tests. Definition of Done: tests pass.

**Task 04 — Implement `CertificateService` with PII-Excluded Payload Assembly**
Objective: Assemble Ramadan data, delegate rendering to A.11's `ShareCardService`. Files to Create: `services/certificate_service.py`. Dependencies: Task 01, Task 03. Tests: **mandatory** — zero-PII-in-payload test. Definition of Done: test passes.

**Task 05 — Implement the Router Endpoints with Parent Gate**
Objective: `POST /v1/ramadan/certificates`, `POST /v1/ramadan/eid-cards`. Files to Create: `routers/certificate_router.py`. Files to Modify: `routers/__init__.py`. Dependencies: Task 04. Tests: **mandatory** — Parent-Gate-missing rejection test; end-to-end generation test. Definition of Done: tests pass.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §27, both mandatory tests included. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm zero independent rendering logic exists outside the A.11 delegation call. Definition of Done: checklist in §30 checked.

## 30. Final Verification Checklist
- [ ] Generated artifact contains zero PII fields (child ID/DOB/location) — mandatory test passing
- [ ] Parent Gate step-up required and enforced for both endpoints
- [ ] Rendering fully delegated to A.11's existing `ShareCardService`, no parallel pipeline
- [ ] Certificate/Eid-card URLs persisted correctly

## 31. Definition of Done
Families can generate and share a PII-safe, Parent-Gate-protected Ramadan certificate and Eid card, entirely through the platform's one existing share-card rendering engine.
