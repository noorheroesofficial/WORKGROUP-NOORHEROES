# B-08 — Quran Content Proposal & Elevated Review API

## 1. Feature Context
A deliberately stricter, distinct authoring path for Quran-adjacent content: ayah text itself is immutable, only translations/tafseer/recitations version, and review runs at an elevated confidence threshold — never sharing or being weakened by the general content-editing tooling.

## 2. Parent Feature
E.29 — Content CMS & Scholar Review Workflow

## 3. Sub-feature
1.8 Quran Content Proposal & Elevated Review API (ID: **B-08**)

## 4. Objective
Implement `POST /v1/admin/quran-proposals`/`PATCH /v1/admin/quran-proposals/{id}` requiring a valid FK to an existing immutable `ayah_id` and applying a review confidence-threshold configuration distinct from and stricter than general content review.

## 5. Business Requirements
- FR-10: ayah text immutable; only translations/tafseer/recitations version; proposed changes link to an existing immutable ayah record; scholar review at an elevated confidence threshold; on approval publish with locale + age tags.
- NFR: the elevated-threshold, ayah-immutable design must never be weakened or bypassed by any general content-editing tooling shared with other content types.

## 6. Existing Architecture
`modules/content_cms/quran/` sub-package, deliberately separate from B-01's general `content_item`/`content_version` model — a `quran_proposal` table with its own review path, reusing B-03's `ReviewWorkflowService` machinery but configured with a distinct, elevated threshold parameter.

## 7. Existing Code to Reuse
- `modules/content_cms/review/workflow_engine.py::ReviewWorkflowService` (B-03, reused with a stricter threshold config)
- A.5's existing `ayah` table/model (read-only reference — cross-ref A.5's immutability guarantee, this document's authoring-side enforcement point)
- `modules/admin/audit/service.py::AuditLogService.log_action()` (E.28)

## 8. Files to Create
- `src/noorheroes/modules/content_cms/quran/models.py` — `QuranProposalOrm`
- `alembic/versions/xxxx_create_quran_proposal.py`
- `src/noorheroes/modules/content_cms/quran/schemas.py` — `QuranProposalCreateRequest`, `QuranProposalResponse`
- `src/noorheroes/modules/content_cms/quran/repository.py` — `QuranProposalRepository`
- `src/noorheroes/modules/content_cms/quran/service.py` — `QuranProposalService(BaseService)`
- `src/noorheroes/modules/content_cms/quran/api.py` — `QuranProposalRouter`
- `tests/modules/content_cms/quran/test_quran_proposal_service.py`
- `tests/modules/content_cms/quran/test_elevated_threshold.py`

## 9. Files to Modify
- `src/noorheroes/main.py` — register `QuranProposalRouter` under `/v1/admin/quran-proposals`
- `src/noorheroes/core/settings.py` — add a distinct `QURAN_REVIEW_CONFIDENCE_THRESHOLD` config key, separate from and stricter than the general content-review threshold

## 10. Backend Requirements
- `QuranProposalService.create(payload)`: requires `ayah_id` to reference an existing row in A.5's `ayah` table (read-only FK validation — this service never writes to `ayah` itself); proposal type restricted to `translation|tafseer|recitation`.
- Review decisions on a `quran_proposal` route through B-03's `ReviewWorkflowService`, but with the threshold parameter explicitly sourced from `QURAN_REVIEW_CONFIDENCE_THRESHOLD`, never the general default — this distinction must be observable/testable (e.g., surfaced in the review-detail response so a scholar sees which threshold applies).
- On approval, publishes with `locale` + `age_band` tags attached to the new translation/tafseer/recitation version — never mutates the referenced `ayah` row.

## 11. API Contract

### `POST /v1/admin/quran-proposals`
- Auth: `content_editor`+ role. Request: `{ ayah_id, proposal_type: "translation"|"tafseer"|"recitation", content, locale }`. Response 201: created proposal. Errors: `404 AYAH_NOT_FOUND`.

### `PATCH /v1/admin/quran-proposals/{id}`
- Auth: `scholar_reviewer` role, at the elevated threshold. Request: standard review-decision shape (delegates to B-03). Response 200: updated proposal.

## 12. Database Requirements
- `quran_proposal`: FK `ayah_id` (references A.5's `ayah` table, read-only relationship — no ON DELETE/UPDATE CASCADE that could ripple into `ayah` mutation); `proposal_type` CHECK constraint.

## 13. Validation
`ayah_id` FK existence-checked before insert; `proposal_type` restricted to the three canonical values.

## 14. Authentication
Admin Bearer via `get_current_admin`.

## 15. Authorization
`require_admin_scope("content_editor")` for proposal creation; `require_admin_scope("scholar_reviewer")` for review decisions.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Non-existent `ayah_id` | `404 AYAH_NOT_FOUND` |
| Invalid `proposal_type` | `422` |
| Review decision at the wrong (general, not elevated) threshold | Structurally impossible — threshold is read from `QURAN_REVIEW_CONFIDENCE_THRESHOLD`, never the general config key, for any call through this module |
| Database failure | `503`, logged |

## 17. Security
Ayah-text immutability is enforced by construction: this service has no write path to the `ayah` table at all — only a read-only FK reference — making it architecturally impossible for this module's tooling to ever mutate immutable Quran text.

## 18. Analytics
`quran_proposal_submitted`, `quran_scholar_review_decision` audited via `AuditLogService`.

## 19. Performance
Standard low-volume admin-write performance profile; no special considerations.

## 20. Library Requirements
No new libraries.

## 21. Testing
- Unit: `ayah_id` FK-existence validation, `proposal_type` enum validation.
- **Mandatory test**: confirm the threshold value used for Quran-category review differs from (is stricter than) the general content-review default (per PRD backend AI-prompt requirement #7).
- Integration: full propose → elevated-threshold-review → approve → publish-with-locale-age-tags flow.

## 22. Documentation
Update OpenAPI schema; document the two distinct threshold config keys and their intended values.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `QuranProposalOrm` Model & Migration**
Objective: Base table with read-only FK to A.5's `ayah` table. Follow: existing SQLAlchemy/Alembic conventions. Do Not Change: A.5's `ayah` table/model in any way. Tests: migration smoke test, FK-existence test. Definition of Done: clean migration.

**Task 02 — Implement `QuranProposalRepository`/`QuranProposalService`**
Objective: CRUD with ayah-existence validation. Dependencies: Task 01, A.5's `ayah` model (read-only import). Tests: non-existent-ayah rejection. Definition of Done: test passes.

**Task 03 — Wire Elevated-Threshold Review via B-03**
Objective: Review decisions on `quran_proposal` route through `ReviewWorkflowService` configured with `QURAN_REVIEW_CONFIDENCE_THRESHOLD`. Dependencies: B-03. Tests: **mandatory** — threshold-differs-from-general-default test. Definition of Done: test passes.

**Task 04 — Add Router Endpoints**
Objective: Wire create/review routes. Tests: covered by Task 05. Definition of Done: endpoints live, documented.

**Task 05 — Add Unit & Integration Tests**
Objective: Full coverage per §21. Definition of Done: all green in CI.

**Task 06 — Update OpenAPI Documentation**
Objective: Regenerate/diff-classify; document the two threshold config keys. Definition of Done: non-breaking diff confirmed.

**Task 07 — Final Code Review**
Objective: Confirm zero write path exists from this module into A.5's `ayah` table; confirm the elevated threshold is genuinely distinct from and stricter than the general default. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] `ayah_id` FK existence-validated before every proposal creation
- [ ] Zero write path from this module into A.5's `ayah` table under any code path
- [ ] Review threshold for Quran proposals is configured distinctly from and stricter than the general content-review threshold — verified by a mandatory test
- [ ] Approved proposals publish with locale + age tags attached to the new version, not the `ayah` row
- [ ] Quran proposal review still routes through B-03's shared segregation-of-duties engine

## 25. Definition of Done
Quran-adjacent content authoring is structurally isolated from any risk of mutating immutable ayah text, reviewed at a genuinely elevated rigor threshold, and cleanly reuses B-03's segregation-of-duties machinery rather than forking a weaker parallel review path.
