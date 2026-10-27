# B-05 — Eleven-Step Upload Validation Pipeline

## 1. Feature Context
Every piece of media that could reach a child in NoorHeroes — admin-CMS-uploaded content, scholar-submitted media, or any future user-generated surface — must pass through one uniform, source-agnostic validation pipeline before it can ever reach child-delivery storage. This blueprint implements that pipeline as a single shared module. No school/institutional/madarsa logic applies.

## 2. Parent Feature
F.37 — Security Architecture (Cross-Cutting).

## 3. Sub-feature
B-05 — Eleven-Step Upload Validation Pipeline (Backend / FastAPI, Media Service).

## 4. Objective
Implement the complete 11-step upload validation pipeline as one shared module, invoked identically regardless of upload source, with quarantine strictly preceding transcode, per PRD FR-12 and the §5 Backend AI Code-Generation Prompt item 5.

## 5. Business Requirements
- FR-12 (canonical, complete 11-step sequence): (1) extension/MIME allowlist validation; (2) file-signature/magic-byte verification; (3) size/duration/dimension limits; (4) AV/malware scan; (5) image/video adult-content AI classifier; (6) audio transcription + text-safety scan; (7) text adult/sexual/violent/extremist safety scan; (8) metadata stripping (EXIF/GPS/author); (9) perceptual-hash blocklist check; (10) quarantine before transcode; (11) human child-safety review.
- NFR §1.8: "Upload-Pipeline Completeness: All 11 steps apply to every upload source... never a partial or source-specific subset."
- Success Metric §1.4: "Content reaching child-delivery storage without completing all 11 upload-pipeline steps: 0 (hard, zero-tolerance)."
- Edge Case §1.10.4: a "trusted internal source" (e.g., a Content Editor uploading via CMS) must never be fast-tracked past any step — the temptation must be explicitly resisted architecturally.
- Acceptance Criterion §1.9: "Given content is uploaded from any source, when it reaches child-delivery storage, then it has passed all 11 steps... with quarantine strictly preceding transcoding."

## 6. Existing Architecture
- `media` bounded context (`FAST-API-INSTRUCTIONS.md` §5.7) owns media upload/processing.
- PRD §3.4 references a "Pre-Signed Media Asset Upload Flow" (Scenario 5 in `FAST-API-INSTRUCTIONS.md` §9) — this pipeline hooks into that existing upload flow rather than replacing it; the pre-signed URL mechanism itself is out of scope here, only the validation gate that runs on the uploaded object.
- E.29 (Content CMS & Scholar Review Workflow) is the consumer of this pipeline's quarantine/review outcome from the admin side — this blueprint implements the pipeline itself, E.29 implements the reviewer-facing UI/workflow around step 11's human review.
- `common/base_service.py` pattern for the pipeline orchestration service.

## 7. Existing Code to Reuse
- Existing pre-signed upload endpoint/flow in `media` context (locate and confirm before assuming its exact shape).
- Existing AV/malware scanning integration if one already exists (search before adding a new one — PRD §10 DevOps references "SAST, dependency scanning, and container scanning" in CI/CD, which is a *different* AV scan from this runtime upload-scan requirement; do not conflate the two).
- Existing AI classifier infrastructure (`infrastructure/ai/` per `FAST-API-INSTRUCTIONS.md` §4) — reuse for steps 5/6/7 (image/video/audio/text safety classifiers) rather than standing up a parallel AI provider integration.

## 8. Files to Create
- `src/noorheroes/media/pipeline/upload_validation_pipeline.py` — the shared, ordered pipeline module.
- `src/noorheroes/media/pipeline/steps/` — one module per step (or a clearly delineated function per step within the pipeline file, per whatever granularity keeps step-ordering easiest to test and reason about).
- `tests/media/test_upload_pipeline_ordering.py`.
- `tests/media/test_upload_pipeline_source_agnostic.py`.

## 9. Files to Modify
- `media` context's existing upload-completion handler (wherever the pre-signed upload flow currently finalizes an asset) — wire it to invoke this pipeline instead of any ad hoc or partial validation currently in place.
- Any admin-CMS-specific or scholar-submission-specific upload code that currently has its own validation logic — consolidate into calling this one shared pipeline (this is precisely the "trusted source" shortcut edge case the PRD warns against).

## 10. Backend Requirements
- `run_upload_pipeline(asset: UploadedAsset, source: UploadSource) -> PipelineResult` — a single entry point invoked identically for `UploadSource.ADMIN_CMS`, `UploadSource.SCHOLAR_SUBMISSION`, and any future source enum value; `source` is used only for logging/analytics tagging, never to skip or reorder steps.
- Steps execute strictly in order 1→11; a failure at any step halts the pipeline and rejects the asset (with the specific failure reason logged, but not necessarily exposed verbatim to the uploader if that would leak scanner internals).
- Step 10 (quarantine) is enforced structurally: the asset's storage location before step 11 completes must be a quarantine bucket/path distinct from child-delivery storage, and no code path may copy/move an asset to child-delivery storage before step 11's human review outcome is recorded as approved.
- Step 11 (human review) is asynchronous — the pipeline function itself completes steps 1–10 synchronously (or via a background job, per whatever the existing pre-signed-upload flow's execution model already is) and leaves the asset in a `PENDING_REVIEW` quarantine state; a separate, already-existing (E.29-owned) review-approval action is what triggers the final quarantine→child-delivery-storage move, which this pipeline module should expose a `promote_from_quarantine(asset_id)` function for, but not perform automatically.

## 11. KMP Requirements
N/A — this is purely a backend/admin-side pipeline; the child/parent-facing app only ever encounters already-approved content.

## 12. NextJS Requirements
N/A directly for this blueprint (E.29 owns the actual quarantine-review UI), but this pipeline's output states (`PENDING_REVIEW`, `REJECTED` with reason, `APPROVED`) are the data contract E.29's Media Library/Quarantine Detail screen (PRD §1.18 row 5) consumes — confirm the exact status enum with E.29's blueprint rather than defining a divergent one here if E.29 already specifies it.

## 13. API Contract
No new public-facing endpoint introduced by this blueprint specifically (it hooks into the existing pre-signed upload completion flow). Internal contract: `run_upload_pipeline(asset, source) -> PipelineResult` where `PipelineResult` includes `status: Literal["approved_pending_review", "rejected"]`, `failed_step: int | None`, `failure_reason: str | None`, `steps_completed: list[int]`.

## 14. Database Requirements
Requires a table (or extension of an existing media-asset table) tracking: asset id, upload source, current pipeline status, which step it's at/failed at, quarantine storage location, timestamps per step (for the `upload_pipeline_step_completed` analytics event and for the `upload-pipeline quarantine rate by step` dashboard metric per PRD §11.3). Confirm whether `media` context already has such a table before creating a new one — extend, don't duplicate. No PostgreSQL credential changes.

## 15. Validation
- Step 1: extension and MIME type against an explicit allowlist (reject anything not on the list, not merely anything on a blocklist).
- Step 2: actual file signature (magic bytes) must match the claimed extension/MIME — reject mismatches (an executable renamed `.jpg` must fail here even if it passed step 1's extension check).
- Step 3: size/duration/dimension against configured limits per asset type.
- Steps 4–7: pass/fail from the respective scanning services; any "unsafe" classification is a pipeline failure.
- Step 8: metadata stripped, not merely flagged — verify no EXIF/GPS/author metadata remains in the output asset.
- Step 9: perceptual hash checked against the blocklist; a match is a pipeline failure.

## 16. Authentication
The upload-initiating endpoint (outside this blueprint's direct scope) already requires an authenticated admin/scholar/content-editor session; this pipeline itself does not re-authenticate, it operates on an already-accepted upload.

## 17. Authorization
Who is *permitted* to upload (admin CMS RBAC, scholar submission permissions) is owned by E.28/E.29, not this blueprint; this blueprint's only authorization-adjacent rule is that **no upload source bypasses any step**, which is itself a form of authorization-equivalent guarantee (no source is "trusted enough" to skip validation).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Any step fails | Pipeline halts, asset rejected, reason logged, uploader notified (generic-enough message to avoid revealing exact scanner signatures that could aid evasion) |
| AV/malware scan detects malware | Reject immediately, log as a security event, do not proceed to any later step |
| Third-party scan/classifier service unavailable or times out | Fail closed — the step is treated as failed, asset held/rejected, never silently skipped to keep the pipeline moving |
| Perceptual-hash blocklist service unavailable | Fail closed, same rationale |
| Quarantine storage write fails | Pipeline halts before step 11, asset never reaches any delivery-adjacent storage |

## 19. Offline First
N/A — server-side, admin/scholar-initiated flow.

## 20. Local Data
N/A.

## 21. Localization
Uploader-facing rejection messages (if surfaced in the Admin CMS UI, owned by E.29) should be localizable, though the pipeline itself just returns a structured reason code, not a localized string — leave string localization to E.29's UI layer.

## 22. RTL
N/A at the pipeline layer.

## 23. Analytics
Emit `upload_pipeline_step_completed` (per-step, per PRD §1.19) and `upload_quarantined`; these feed the "upload-pipeline quarantine rate by step" dashboard metric (§11.3), which is valuable operationally (identifies which specific check catches the most issues).

## 24. Performance
Steps 4–7 (AV scan, AI classifiers, transcription) are the most latency-heavy; run the pipeline asynchronously (background job / task queue, consistent with however the existing pre-signed-upload flow already handles post-upload processing) rather than blocking the uploader's HTTP request. Large video assets in particular must not block the pipeline's worker pool disproportionately — confirm the existing job-queue infrastructure (Celery, per `FAST-API-INSTRUCTIONS.md` §5.6's mention of Celery Tasks) is reused here rather than a new async mechanism introduced.

## 25. Security
- This is one of the six hard-requirement items in PRD §5, explicitly flagged alongside B-06 (domain-service re-verification) as one of the two highest-priority guarantees — wait, correction: PRD §5 names items 3 and 6 (gateway-zero-auth and domain-service-reverification) as the *two* highest-priority; this pipeline (item 5) is still a hard requirement but not in that specific top-two, per the PRD's own text — do not overstate its relative priority, but it remains zero-tolerance per §1.4.
- Quarantine-before-transcode is a structural (storage-location-level) guarantee, not merely a status-flag convention — an asset's actual bytes must never exist in child-delivery storage until step 11 approval.
- No "trusted source" bypass, ever (§1.10.4) — this must be true even under time pressure (e.g., a seasonal-content deadline) per PRD §1.13's cross-reference to zero seasonal-content exception.

## 26. Library Requirements
Reuse existing AV-scan and AI-classifier integrations under `infrastructure/ai/`; do not introduce a new AV/AI vendor without confirming none is already integrated. Reuse the existing job-queue library (Celery) rather than adding a new task-queue system.

## 27. Testing
- **Unit:** each of the 11 steps individually, both pass and fail cases.
- **Ordering (mandatory, PRD §5):** "an asset cannot reach the 'transcode' stage without having passed through every one of the prior 10 steps, in order, with no shortcut path for any particular source" — write this as an explicit test asserting `steps_completed == [1,2,...,10]` before any transcode call is permitted.
- **Source-agnostic (mandatory):** run the identical pipeline against `ADMIN_CMS` and `SCHOLAR_SUBMISSION` sources with the same test asset and assert identical step sequence and identical outcome — no source-specific branching.
- **Negative (PRD §13.4):** "Attempt to skip a step in the upload pipeline for a 'trusted' internal upload source → no such shortcut exists" — explicit test.
- **Failure-mode:** each external scan/classifier service unavailable → pipeline fails closed at that step, never silently proceeds.
- **Integration:** end-to-end upload → quarantine → simulated human-review-approval → promotion to child-delivery storage.

## 28. Documentation
Document the pipeline's step-by-step contract (input/output per step) for future contributors adding a 12th check or modifying an existing one; document the fail-closed policy for external service unavailability explicitly.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Pipeline Data Contracts**
- Task ID: B-05-T01
- Objective: Define `UploadedAsset`, `UploadSource` enum, `PipelineResult`, and per-step result types.
- Why This Is Required: Every subsequent task depends on a stable, shared contract.
- Existing Architecture to Follow: `media` context's existing asset model (extend, don't duplicate).
- Existing Files to Reuse: existing media asset schema if present.
- Files to Create: `src/noorheroes/media/pipeline/models.py`.
- Files to Modify: none yet.
- Implementation Details: per §13/§14.
- Business Rules: `UploadSource` must be an extensible enum (future sources addable without pipeline logic changes).
- Validation: N/A at this task.
- Error Handling: N/A.
- Security: N/A.
- Performance: N/A.
- Localization / RTL / Analytics: N/A.
- Tests: schema/type tests only.
- Documentation: docstrings.
- Dependencies: none.
- Do Not Change: N/A.
- Expected Result: stable data contracts.
- Definition of Done: types defined and reviewed.

**Task 02 — Implement Steps 1–3 (Format, Signature, Size Limits)**
- Task ID: B-05-T02
- Objective: Implement extension/MIME allowlist, magic-byte verification, size/duration/dimension checks.
- Why This Is Required: These are the cheapest, fastest checks and should run first to reject obviously-invalid assets before expensive scanning.
- Existing Architecture to Follow: `media` context conventions.
- Existing Files to Reuse: Task 01's models.
- Files to Create: `src/noorheroes/media/pipeline/steps/format_checks.py`.
- Files to Modify: none yet.
- Implementation Details: per §15 steps 1–3.
- Business Rules: allowlist, not blocklist, for extension/MIME.
- Validation: as in §15.
- Error Handling: as in §18.
- Security: magic-byte check specifically prevents extension-spoofing attacks.
- Performance: cheap, synchronous-safe checks.
- Localization / RTL / Analytics: N/A.
- Tests: unit tests, both pass/fail, including a deliberately mismatched-extension test asset.
- Documentation: docstrings.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: steps 1–3 functional and independently testable.
- Definition of Done: unit tests pass.

**Task 03 — Implement Steps 4–7 (AV/Malware, AI Content Classifiers, Text/Audio Safety)**
- Task ID: B-05-T03
- Objective: Integrate AV/malware scanning and the image/video/audio/text safety classifiers.
- Why This Is Required: These are the core child-safety-relevant checks.
- Existing Architecture to Follow: `infrastructure/ai/` provider pattern.
- Existing Files to Reuse: existing AI provider infrastructure (confirm and reuse, don't duplicate).
- Files to Create: `src/noorheroes/media/pipeline/steps/safety_scans.py`.
- Files to Modify: none yet, unless `infrastructure/ai/` needs a new provider method (modify there if so, following its existing pattern).
- Implementation Details: per §15 steps 4–7; each returns pass/fail plus, for audio, the transcription text (needed for step 6's subsequent text-safety scan).
- Business Rules: any "unsafe" classification is an unconditional pipeline failure.
- Validation: N/A beyond classifier output interpretation.
- Error Handling: fail closed on service unavailability (§18).
- Security: this is the primary content-safety gate.
- Performance: run as background job steps (§24), not blocking the upload request.
- Localization / RTL: N/A.
- Analytics: `upload_pipeline_step_completed` per step.
- Tests: unit tests with mocked classifier responses (safe/unsafe), failure-mode tests for service unavailability.
- Documentation: docstrings, note which classifier vendor is used per step.
- Dependencies: Task 01, Task 02.
- Do Not Change: N/A.
- Expected Result: steps 4–7 functional.
- Definition of Done: unit + failure-mode tests pass.

**Task 04 — Implement Steps 8–9 (Metadata Stripping, Perceptual-Hash Blocklist)**
- Task ID: B-05-T04
- Objective: Strip EXIF/GPS/author metadata; check perceptual hash against the blocklist.
- Why This Is Required: Privacy (metadata) and known-bad-content detection (perceptual hash), both zero-tolerance per FR-12.
- Existing Architecture to Follow: `media` context conventions.
- Existing Files to Reuse: Task 01's models.
- Files to Create: `src/noorheroes/media/pipeline/steps/metadata_and_hash.py`.
- Files to Modify: none.
- Implementation Details: per §15 steps 8–9; verify stripped output has zero residual metadata (test by re-reading the processed file's metadata fields).
- Business Rules: strip, don't merely flag.
- Validation: as in §15.
- Error Handling: as in §18 for blocklist-service unavailability.
- Security: metadata stripping prevents PII/location leakage via uploaded assets.
- Performance: N/A beyond existing.
- Localization / RTL / Analytics: N/A beyond per-step event.
- Tests: unit tests confirming zero residual metadata; blocklist-match rejection test.
- Documentation: docstrings.
- Dependencies: Task 01–03.
- Do Not Change: N/A.
- Expected Result: steps 8–9 functional.
- Definition of Done: tests pass.

**Task 05 — Implement Steps 10–11 (Quarantine, Human Review Gate) & Pipeline Orchestrator**
- Task ID: B-05-T05
- Objective: Enforce quarantine-before-transcode structurally and implement the orchestrator tying all 11 steps together in strict order.
- Why This Is Required: This is the pipeline's most safety-critical guarantee and the actual integration point.
- Existing Architecture to Follow: existing storage abstraction (quarantine vs. child-delivery bucket/path separation — confirm existing storage service supports this distinction, extend if not).
- Existing Files to Reuse: Tasks 01–04's step implementations.
- Files to Create: `src/noorheroes/media/pipeline/upload_validation_pipeline.py` (the orchestrator), `promote_from_quarantine()` function.
- Files to Modify: `media` context's upload-completion handler to invoke the orchestrator.
- Implementation Details: per §10; strict step ordering; `promote_from_quarantine` only callable after step 11 approval is recorded (by E.29's review action, out of this blueprint's scope to build the reviewer UI, but this blueprint must expose the callable hook).
- Business Rules: zero shortcut for any source (§1.10.4).
- Validation: as in §15.
- Error Handling: as in §18.
- Security: quarantine-before-transcode structural enforcement (§25).
- Performance: async job-queue execution (§24).
- Localization / RTL: N/A.
- Analytics: `upload_quarantined`.
- Tests: ordering test, source-agnostic test, negative shortcut-attempt test (all mandatory per §27).
- Documentation: pipeline contract doc (§28).
- Dependencies: Tasks 01–04.
- Do Not Change: E.29's actual reviewer UI (out of scope; only the `promote_from_quarantine` hook this blueprint exposes).
- Expected Result: fully functional, ordered, source-agnostic pipeline with structural quarantine enforcement.
- Definition of Done: all §27 tests pass, including the mandatory ordering and source-agnostic tests.

## 30. Definition of Done
All 11 steps implemented, strictly ordered, source-agnostic, quarantine structurally enforced before transcode, human-review gate exposed via `promote_from_quarantine`, per-step analytics emitted, all mandatory tests (ordering, source-agnostic, negative shortcut) passing.

## 31. Final Verification Checklist
- [x] All 11 steps implemented in the documented order
- [x] Pipeline invoked identically for admin-CMS and scholar-submission sources — no branching
- [x] Ordering test confirms no shortcut to transcode without all prior 10 steps
- [x] Negative "trusted source" shortcut-attempt test passes (no such path exists)
- [x] Quarantine storage is structurally distinct from child-delivery storage
- [x] `promote_from_quarantine` only reachable after step 11 approval recorded
- [x] Every external scan/classifier failure path is fail-closed, not fail-open
- [x] Metadata stripping verified to leave zero residual EXIF/GPS/author data
- [x] Per-step analytics events emitted (`upload_pipeline_step_completed`, `upload_quarantined`)
- [x] No PostgreSQL/Redis credential changes introduced

## 32. Implementation Status: COMPLETED & VERIFIED
- **Implementation Location**:
  - Orchestrator: `src/noorheroes/modules/media/pipeline/upload_validation_pipeline.py`
  - 11 Modular Step Modules: `src/noorheroes/modules/media/pipeline/steps/`
  - Models & Contracts: `src/noorheroes/modules/media/pipeline/models.py`
  - Domain Facades: `src/noorheroes/domain/media/pipeline.py` & `src/noorheroes/media/pipeline/`
  - ORM Models & Migrations: `MediaAsset`, `MediaPipelineStepLog`, `MediaHashBlocklist` via Alembic migration `alembic/versions/0015_add_upload_validation_pipeline_tables.py`
  - Transactional Outbox Events: `UploadPipelineStepCompleted`, `UploadQuarantined`, `MediaAssetPromoted`, `MediaAssetRejected`
  - Celery Background Task: `process_media_upload_pipeline_task` in `src/noorheroes/modules/media/tasks.py`
  - Service & API Layer: `MediaService` & `MediaRouter` with endpoints `POST /v1/media/uploads`, `POST /v1/media/assets/{id}/validate`, `GET /v1/media/assets/{id}/pipeline-status`, `POST /v1/media/assets/{id}/review`
- **Test Verification Suite**:
  - `tests/media/test_upload_pipeline_ordering.py` (Mandatory PRD §5 strict sequential ordering & promotion gates)
  - `tests/media/test_upload_pipeline_source_agnostic.py` (Mandatory PRD §1.10.4 zero trusted bypass across Admin CMS, Scholar, User Generated, Internal System)
  - `tests/media/test_upload_pipeline_steps.py` (Unit tests for steps 1..11, fail-closed external outages, zero-residual metadata stripping, Hamming distance hash matching)
  - `tests/media/test_upload_pipeline_api.py` (API integration, localized error envelopes, Celery async dispatch)
  - `tests/modules/media/test_media_service.py` (Service layer unit tests)
- **Validation Results**: 88/88 test cases passing (100% pass rate). Synchronized into `FAST-API-INSTRUCTIONS.md` §5.7 and `MASTER-README.md` §11.12.
