# B-02 — Media Upload & Safety Pipeline Service

## 1. Feature Context
The fail-closed gate standing between any uploaded media file and a human reviewer's eyes: MIME validation, AV scanning, and safety classification must all pass before a media item is even visible to a review queue. This is one of the two highest-priority guarantees in the entire E.29 service per the PRD's own backend AI-prompt.

## 2. Parent Feature
E.29 — Content CMS & Scholar Review Workflow

## 3. Sub-feature
1.2 Media Upload & Safety Pipeline Service (ID: **B-02**)

## 4. Objective
Implement multipart media upload routing asynchronously through an MIME→AV-scan→safety-classifier pipeline via Kafka/Celery, with `media_asset`/`safety_pipeline_result` excluded from every review-queue query until `status='pass'`, and a terminal `quarantined` state on any failure.

## 5. Business Requirements
- FR-4: multipart upload, virus scanning, transcoding/thumbnail jobs, loudness normalization, caption validation, audio-track mapping, rights/license fields, CDN purge, emergency disable.
- FR-5: only an approved immutable version can publish; every upload passes MIME validation, AV scan, and safety classifiers before entering the review queue — failed media is quarantined and never reaches the review queue at all.
- Edge Case 3: automated pipeline pass doesn't preclude a human reviewer later catching a subtle issue — this is the intended, expected function of downstream human review stages.

## 6. Existing Architecture
New `modules/content_cms/media/` sub-package. Async processing via the platform's existing Celery infrastructure (per `LocalizationRouter`'s established Celery-task pattern in `modules/localization/tasks.py` — mirror that pattern here, not a new job-queue mechanism).

## 7. Existing Code to Reuse
- `modules/localization/tasks.py` (Celery background-task pattern to mirror)
- `infrastructure/` storage/CDN integration (reuse existing object-storage client if one is already established, e.g., the R2 pattern referenced in `MediaService.initiate_upload()` from the child-facing `media` module)
- `common/base_service.py`, `common/base_repository.py`

## 8. Files to Create
- `src/noorheroes/modules/content_cms/media/models.py` — `MediaAssetOrm`, `SafetyPipelineResultOrm`
- `alembic/versions/xxxx_create_media_asset_safety_pipeline_result.py`
- `src/noorheroes/modules/content_cms/media/schemas.py` — `MediaUploadResponse`, `MediaStatusResponse`
- `src/noorheroes/modules/content_cms/media/repository.py` — `MediaAssetRepository`
- `src/noorheroes/modules/content_cms/media/service.py` — `MediaProcessingService(BaseService)`
- `src/noorheroes/modules/content_cms/media/tasks.py` — `run_safety_pipeline_task(media_id)` (Celery)
- `src/noorheroes/infrastructure/media_safety/mime_validator.py`, `av_scanner.py` (ClamAV or cloud-equivalent adapter), `safety_classifier.py`
- `src/noorheroes/modules/content_cms/media/api.py` — `MediaRouter`
- `tests/modules/content_cms/media/test_media_processing_service.py`
- `tests/modules/content_cms/media/test_safety_gate_exclusion.py`

## 9. Files to Modify
- `src/noorheroes/main.py` — register `MediaRouter` under `/v1/admin/media`
- `src/noorheroes/modules/content_cms/api.py` (B-01/B-04) — review-queue query joins must explicitly filter `safety_pipeline_result.status = 'pass'`

## 10. Backend Requirements
- `MediaProcessingService.initiate_upload(file, actor_id)`: MIME-validates synchronously (reject obviously-wrong types immediately, `422`), persists `media_asset` with `safety_pipeline_result.status='pending'`, enqueues `run_safety_pipeline_task` asynchronously.
- `run_safety_pipeline_task`: runs AV scan → safety classifiers → (if applicable) transcoding/thumbnailing/loudness-normalization/caption-validation; on any stage failure, sets `status='quarantined'` (terminal — re-upload required, never a retryable "fix in place" state for the same `media_id`); on full pass, sets `status='pass'`.
- Any query that lists review-queue-eligible content (owned by B-04) must join against `safety_pipeline_result` and filter `status='pass'` — this filter lives in this module's repository helper, reused by B-04 rather than duplicated.
- CDN purge / emergency media disable: immediate cache invalidation + `media_asset` flag, independent of the content-item-level suspend (B-07) but callable from it.

## 11. API Contract

### `POST /v1/admin/media`
- Auth: `content_editor`+ role. Response 202: `{ media_id, status: "pending" }` (async — pipeline runs in background).

### `GET /v1/admin/media/{id}/status`
- Auth: `content_editor`+ role. Response 200: `{ status: "pending"|"pass"|"quarantined", classifier_results?: {...}, quarantine_reason?: "..." }`.

### `POST /v1/admin/media/{id}/purge-cdn`
- Auth: `content_editor`+ role or safety role. Response 200: `{ purged: true }`.

## 12. Database Requirements
- `media_asset`: FK `content_version_id`; index `(content_version_id)`.
- `safety_pipeline_result`: PK = FK `media_id`; CHECK `status IN ('pending','pass','quarantined')`.

## 13. Validation
- MIME type checked against an explicit allow-list before any storage write occurs.
- File-size limits enforced per content-type/format policy.

## 14. Authentication
Admin Bearer via `get_current_admin`.

## 15. Authorization
`require_admin_scope("content_editor")` for upload; CDN-purge/emergency-disable additionally permitted for safety roles.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| MIME validation fails | Immediate `422`, no storage write, no pipeline job enqueued |
| AV scan or safety classifier fails | `status='quarantined'`, terminal, re-upload required |
| AV-scan/classifier service itself unavailable | Fail closed to `quarantined` (or held at `pending` with a retry policy — never advanced to `pass` on an inconclusive result) |
| Review-queue query encountering a non-`pass` media reference | Excluded entirely from the result set, never partially shown |
| Database/storage failure | `503`, logged |

## 17. Security
- Fail-closed design is this service's core security property: any uncertain, failed, or pending safety-pipeline result excludes the media from review-queue visibility — verified by a dedicated exclusion test, not just a happy-path pass test.
- No media reaches CDN-public availability before a content item referencing it completes the full publish pipeline (B-06) — upload alone never makes media publicly servable.

## 18. Analytics
Internal admin/pipeline event, audited via `AuditLogService` for upload/quarantine transitions; `content_media_uploaded`/`content_media_quarantined` recorded as audit-log entries.

## 19. Performance
AV scanning/transcoding is potentially heavy-compute — dispatched to dedicated async worker infrastructure (Celery), never run synchronously in the request path; upload endpoint returns `202 Accepted` immediately.

## 20. Library Requirements
- ClamAV (or equivalent cloud AV-scanning API) adapter.
- Content-safety classifier integration (per existing `infrastructure/ai/` provider pattern if a similar classifier is already integrated elsewhere, e.g., B-06 of A.3's moral-summary safety validator — reuse that provider abstraction pattern, not a parallel one).
- Celery (already used by `modules/localization/tasks.py`).

## 21. Testing
- Unit: MIME allow-list rejection, quarantine-on-any-stage-failure logic.
- **Mandatory fail-closed exclusion test**: confirm a media item with `status='pending'` or `'quarantined'` is excluded from any review-queue listing query, never returned even partially (per PRD backend AI-prompt requirement #2).
- Integration: full upload → async pipeline → pass/quarantine flow using a mocked AV-scanner/classifier for reliable CI execution.

## 22. Documentation
Update OpenAPI schema; document the AV-scanning/classifier provider configuration by env var name only (never secret values).

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `MediaAssetOrm`/`SafetyPipelineResultOrm` Models & Migration**
Objective: Base tables per the PRD ER diagram. Follow: existing SQLAlchemy/Alembic conventions. Business Rules: CHECK `status IN ('pending','pass','quarantined')`. Tests: migration smoke test. Definition of Done: clean migration.

**Task 02 — Implement MIME Validator and Upload Entry Point**
Objective: Synchronous MIME allow-list check, storage write, `media_asset`/`safety_pipeline_result(pending)` row creation. Follow: existing storage-client pattern. Tests: MIME rejection test. Definition of Done: test passes.

**Task 03 — Implement AV Scanner and Safety Classifier Adapters**
Objective: `av_scanner.py`, `safety_classifier.py` behind a common interface. Follow: existing `infrastructure/ai/` provider-abstraction pattern if applicable. Tests: mocked pass/fail scenarios. Definition of Done: tests pass.

**Task 04 — Implement `run_safety_pipeline_task` Celery Task**
Objective: Orchestrate MIME (already done) → AV → classifier → optional transcoding/normalization → final status write. Dependencies: Task 02–03. Business Rules: any stage failure → `quarantined`, terminal. Tests: full-pipeline pass and quarantine paths. Definition of Done: tests pass.

**Task 05 — Implement Mandatory Fail-Closed Exclusion Filter**
Objective: A reusable repository helper (`filter_pass_only()`) that B-04's review-queue query must use. Dependencies: Task 01. Tests: **mandatory** — pending/quarantined media never appears in a review-queue-shaped query result. Definition of Done: exclusion test passes.

**Task 06 — Add Router Endpoints**
Objective: Wire upload, status, and CDN-purge endpoints. Tests: covered by Task 08. Definition of Done: endpoints live, documented, upload returns `202`.

**Task 07 — Wire Audit Logging**
Objective: `AuditLogService.log_action()` on upload and on quarantine transition. Dependencies: E.28 B-05. Tests: audit rows present. Definition of Done: test passes.

**Task 08 — Add Unit & Integration Tests**
Objective: Full coverage per §21, including the mandatory exclusion test. Definition of Done: all green in CI.

**Task 09 — Update OpenAPI Documentation**
Objective: Regenerate/diff-classify; document AV-scanner config env vars. Definition of Done: non-breaking diff confirmed, no secrets present.

**Task 10 — Final Code Review**
Objective: Confirm zero code path can mark media `pass` without a genuinely completed pipeline run; confirm the exclusion filter is the one B-04 actually consumes, not a duplicated/divergent copy. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] Upload endpoint returns `202` immediately; pipeline runs asynchronously
- [ ] Any pipeline-stage failure results in a terminal `quarantined` status, never a retryable-in-place state
- [ ] Media with `status != 'pass'` is excluded from every review-queue query (mandatory exclusion test passing)
- [ ] AV-scanner/classifier outage fails closed, never advances a media item to `pass` on an inconclusive result
- [ ] CDN purge / emergency disable functions independent of content-item-level suspend
- [ ] Upload/quarantine transitions audited via `AuditLogService`
- [ ] No PostgreSQL/Redis credentials modified

## 25. Definition of Done
Media uploads are fail-closed gated through a genuine MIME/AV/safety-classifier pipeline before ever becoming visible to a human reviewer — the single most important trust guarantee behind the platform's "every piece of content is scholar-reviewed and safety-vetted" claim, alongside B-01's provenance immutability.
