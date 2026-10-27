# B-01 — Fact Content, Versioning & Scholar-Approval Data Model

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). This is the foundational data layer — every other B.18 backend sub-feature (B-02 through B-08) depends on the tables and approval-gate invariant defined here. No other sub-feature may create its own copy of these tables.

## 2. Parent Feature
B.18 — Islamic Facts Module

## 3. Sub-feature
1.1 Fact Content, Versioning & Scholar-Approval Data Model (ID: B-01)

## 4. Objective
Extend the existing `content` bounded context with a `fact`, `fact_version`, `scholar_approval`, and `fact_seen_log` table set, implementing scholar-approval enforcement as a hard, structural, query-layer invariant — never a workflow convention that a buggy or bypassed admin path could violate.

## 5. Business Requirements
- FR-1: each fact stores fact text by locale/age-band, topic and related-content linkage, primary/secondary source references, scholar approval and version, an explanation, a linked quiz item, and jurisprudential-scope/exclusion notes (source §21.9, restated as canonical field list).
- FR-11: scholar-approval records are versioned; editing text/explanation/sources creates a new version requiring fresh sign-off before it can replace the currently-published version; children always see the latest *published* (approved) version, never a draft.
- NFR (Content Integrity): 100% of published facts must have a valid, current scholar-approval record at all times; a fact whose approval has been revoked/superseded is automatically excluded from selection until a re-approved version replaces it.
- §4.4 Soft Delete Rules: `fact.is_withdrawn = true` used instead of deletion, preserving `fact_seen_log` history.
- §4.5 Retention: `fact_seen_log` retained indefinitely (feeds dedup and spaced-repetition evidence).
- Acceptance Criteria: a revoked/superseded fact version is excluded from "today's fact" eligibility until a re-approved version exists.
- Edge Case 5: a scholar revokes approval on a version a child already engaged with → the child's historical engagement/mastery-evidence record is preserved; only future selection eligibility is affected.
- Edge Case 8: an admin attempts to mark a fact approved without an actual scholar-review record → rejected by validation.

## 6. Existing Architecture
Extends the existing `content` bounded context (`src/noorheroes/modules/content/`) per `FAST-API-INSTRUCTIONS.md` §5.4, following the identical Router → Service → Repository → `BaseRepository[ModelT]` layering used by all 10 existing contexts. No new bounded context is created — `fact` is a new content type sibling to `ContentItem`/`Series`, not a parallel content system. PostgreSQL + Alembic per existing infrastructure; no new database technology introduced.

## 7. Existing Code to Reuse
- `common/base_repository.py` → `BaseRepository[ModelT]` for `FactRepository`, `FactVersionRepository`, `ScholarApprovalRepository`.
- `common/base_service.py` → `BaseService` as base for `FactContentService`.
- `common/schemas.py` → `NoorHeroesBaseModel` as the Pydantic v2 camelCase base for all new DTOs.
- `content` module's existing `ContentItem`/`Series` models — reference pattern for `is_withdrawn`, `created_at` conventions (do not duplicate columns inconsistently).
- Existing scholar-approval workflow pattern already established in A.3/A.5/A.6 content types — reuse the `scholar_approval`-style table shape rather than inventing a new approval schema.
- `infrastructure/database.py` → `AsyncSessionLocal`, existing Alembic migration chain.

## 8. Files to Create
- `src/noorheroes/modules/content/models/fact.py` — `FactOrm`, `FactVersionOrm`, `ScholarApprovalOrm`, `FactSeenLogOrm`.
- `src/noorheroes/modules/content/schemas/fact.py` — `FactVersionCreateRequest`, `FactResponse`, `FactDetailResponse`, `ScholarApprovalResponse`.
- `src/noorheroes/modules/content/repositories/fact_repository.py` — `FactRepository(BaseRepository[FactOrm])`, `FactVersionRepository(BaseRepository[FactVersionOrm])` with `get_published_version(fact_id, locale, age_band) -> FactVersionOrm | None` enforcing the approval join.
- `src/noorheroes/modules/content/repositories/scholar_approval_repository.py` — `ScholarApprovalRepository(BaseRepository[ScholarApprovalOrm])`.
- `src/noorheroes/modules/content/repositories/fact_seen_log_repository.py` — `FactSeenLogRepository` with `record_seen(child_id, fact_id)`, `get_recent_seen_ids(child_id, window_days)`.
- `alembic/versions/xxxx_create_fact_tables.py` — creates `fact`, `fact_version`, `scholar_approval`, `fact_seen_log`.
- `tests/modules/content/test_fact_approval_gate.py`.
- `tests/modules/content/test_fact_versioning_immutability.py`.

## 9. Files to Modify
- `src/noorheroes/modules/content/__init__.py` — export new models/repositories.
- None to `main.py` or router aggregator (no endpoints in this sub-feature — pure data layer, consumed by B-02/B-03/B-06).

## 10. Backend Requirements
- `fact` table: `fact_id` (PK, uuid), `topic` (string, CHECK against registered topic values), `linked_quiz_question_id` (uuid, nullable FK into A.8's question bank), `is_withdrawn` (bool, default false), `created_at`.
- `fact_version` table: `version_id` (PK), `fact_id` (FK), `locale`, `age_band`, `text`, `explanation`, `sources` (jsonb), `jurisprudential_scope_note` (nullable text), `status` (CHECK `IN ('draft','pending_review','published','archived')`), `created_at`. Index `(fact_id, locale, age_band, status)`.
- `scholar_approval` table: `approval_id` (PK), `version_id` (FK), `approver_id`, `approved` (bool), `approved_at`, `revoked_at` (nullable). Index `(version_id)`.
- **Approval gate (hard invariant):** `FactVersionRepository.get_published_version()` performs a SQL join requiring `fact_version.status = 'published' AND scholar_approval.approved = true AND scholar_approval.revoked_at IS NULL` — this is the ONLY code path any other sub-feature may use to resolve a "current" fact version. No other query path may bypass this join.
- `fact_seen_log` table: append-only, `(child_id FK, fact_id FK, seen_at)`, index `(child_id, seen_at DESC)`.
- A `fact_version` cannot transition to `status='published'` via the repository layer unless a corresponding `scholar_approval` row with `approved=true` exists at the moment of the transition (checked in `FactContentService.publish_version()`, not merely at read time — defense in depth).
- Editing a published fact's text/explanation/sources always creates a **new row** in `fact_version` with `status='draft'` — never an UPDATE on a `published` row's content columns.

## 11. KMP Requirements
None — pure backend data layer. Consumed indirectly via B-02/B-03's APIs by K-01.

## 12. NextJS Requirements
None directly — consumed via B-06's admin API by N-01/N-03.

## 13. API Contract
No public endpoints in this sub-feature. Internal repository contract only:
- `FactVersionRepository.get_published_version(fact_id, locale, age_band) -> FactVersionOrm | None`
- `FactContentService.publish_version(version_id, approver_id) -> FactVersionOrm` — raises `ValidationError` if no valid `scholar_approval` exists.
- `FactContentService.revoke_approval(version_id, reason) -> None` — sets `revoked_at`, never deletes the approval row (audit trail).

## 14. Database Requirements
Per PRD §4.1/§4.2 ER diagram: `fact`, `fact_version`, `scholar_approval`, `fact_seen_log` exactly as specified. Migration must run before any B-02/B-03/B-06 code depends on these tables. `fact_seen_log` is append-only — no UPDATE/DELETE code path should ever be written against it beyond retention-policy pruning if introduced later.

## 15. Validation
- `topic` must be a registered topic value (CHECK constraint + service-layer validation against the Topic Registry).
- `fact_version.status` must be one of the four enumerated values.
- `sources` jsonb must contain at least one primary source reference (service-layer validation, not DB constraint, to allow future schema evolution).
- `scholar_approval.approved_at` required when `approved=true`.

## 16. Authentication
N/A — no endpoints. Repository/service layer only, invoked by authenticated endpoints in B-02/B-03/B-06.

## 17. Authorization
N/A at this layer — enforced by the calling endpoints (child-mode in B-02/B-03, `content_editor`/`scholar_reviewer` in B-06).

## 18. Error Handling
- `FactContentService.publish_version()` raises `ValidationError` (not a silent no-op) if called without a valid, non-revoked `scholar_approval` row — this is the structural enforcement point referenced throughout B.18.
- Revoking an already-revoked approval is idempotent (no error), consistent with defensive API design.
- Database failure during a version-create transaction rolls back atomically (no partial `fact_version` row without its intended `scholar_approval` linkage state).

## 19. Offline First
N/A — backend-only.

## 20. Local Data
N/A — backend-only.

## 21. Localization
`fact_version.locale` and `age_band` are the localization/age-targeting keys; no hardcoded locale logic — locale set is read from the platform's existing supported-locale registry (English, Hindi, Arabic, Urdu).

## 22. RTL
N/A at the data layer; `sources`/`text`/`explanation` stored as plain Unicode text, RTL rendering is a KMP/NextJS concern (K-01, N-01).

## 23. Analytics
None directly emitted here; `fact_scholar_approval_revoked_excluded` (internal/content-integrity signal) is emitted by B-02's selection service when it excludes a revoked fact, not by this layer.

## 24. Performance
- Indexes on `(fact_id, locale, age_band, status)` and `(child_id, seen_at DESC)` sized for the expected query patterns of B-02 (daily selection) and B-03 (detail fetch).
- `fact_seen_log` append-only pattern avoids UPDATE contention under concurrent child sessions.

## 25. Security
- Approval-gate enforcement at the query/service layer (not just admin UI) is this sub-feature's defining security control — a compromised or misconfigured admin form cannot result in an unapproved fact becoming selectable.
- No PII in these tables; `fact_seen_log.child_id` is a standard FK, no additional encryption beyond platform baseline.

## 26. Library Requirements
SQLAlchemy 2.0 (async), Alembic, Pydantic v2 — all already in the platform's dependency set; no new libraries introduced.

## 27. Testing
- Unit: approve → publish → confirm selectable via `get_published_version()`.
- Unit: revoke approval on a published version → confirm immediately unselectable via `get_published_version()`; confirm `fact_seen_log` rows for children who already saw it remain untouched.
- Unit: attempt `publish_version()` without a valid approval row → `ValidationError` raised, no state change.
- Unit: edit a published version's text → confirm a NEW `fact_version` row is created with `status='draft'`, the original published row is untouched.
- Integration: full create → approve → publish → revoke → re-approve → re-publish lifecycle against a real test database.

## 28. Documentation
Update `FAST-API-INSTRUCTIONS.md` §5.4 (`content` Context) to document the new `fact`/`fact_version`/`scholar_approval`/`fact_seen_log` models and the approval-gate invariant as a documented architectural rule, not just inline code comments.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create SQLAlchemy Models**
Objective: Define `FactOrm`, `FactVersionOrm`, `ScholarApprovalOrm`, `FactSeenLogOrm` in `src/noorheroes/modules/content/models/fact.py`.
Why This Is Required: Foundation for every other B.18 backend sub-feature.
Existing Architecture to Follow: `content` module's existing `ContentItem`/`Series` model conventions (declarative base, `created_at` server-default pattern).
Existing Files to Reuse: `src/noorheroes/modules/content/models/__init__.py` base declarative class.
Files to Create: `src/noorheroes/modules/content/models/fact.py`.
Files to Modify: `src/noorheroes/modules/content/models/__init__.py`.
Implementation Details: Four ORM classes matching §4.1 ER diagram exactly; FK relationships with `lazy="raise"` per existing N+1-prevention convention if used elsewhere in `content` module (confirm convention before assuming).
Business Rules: `fact_version.status` CHECK constraint at DB level as a defense-in-depth backstop to service-layer validation.
Validation: N/A (model layer).
Error Handling: N/A (model layer).
Security: N/A.
Performance: Composite indexes per §14.
Localization: `locale`/`age_band` columns present.
RTL: N/A.
Analytics: N/A.
Tests: Deferred to Task 06.
Documentation: Docstrings on each ORM class referencing PRD §4.1.
Dependencies: None (first task).
Do Not Change: Existing `ContentItem`/`Series` models.
Expected Result: Four new ORM classes importable from `src.noorheroes.modules.content.models.fact`.
Definition of Done: Models compile, relationships resolve, no circular imports.

**Task 02 — Write Alembic Migration**
Objective: Create `xxxx_create_fact_tables.py` migration.
Why This Is Required: Tables must exist before any repository/service code can run against them.
Existing Architecture to Follow: Existing Alembic migration chain/naming convention in `alembic/versions/`.
Files to Create: `alembic/versions/xxxx_create_fact_tables.py`.
Implementation Details: `upgrade()` creates all four tables with exact column/constraint/index definitions from §10/§14; `downgrade()` drops them in FK-safe order.
Business Rules: CHECK constraints for `fact_version.status`.
Dependencies: Task 01.
Do Not Change: Any existing migration file or PostgreSQL/Redis credentials.
Expected Result: `alembic upgrade head` succeeds against a clean test database.
Definition of Done: Migration applies and rolls back cleanly in CI.

**Task 03 — Implement Repositories**
Objective: `FactRepository`, `FactVersionRepository`, `ScholarApprovalRepository`, `FactSeenLogRepository`.
Existing Architecture to Follow: `BaseRepository[ModelT]` generic pattern.
Implementation Details: `FactVersionRepository.get_published_version()` implements the approval-gate join described in §10.
Dependencies: Task 01, Task 02.
Expected Result: Repository methods callable and correctly enforce the approval gate.
Definition of Done: Passes Task 06's approval-gate unit tests.

**Task 04 — Implement `FactContentService`**
Objective: `publish_version()`, `revoke_approval()`, `create_draft_version()` business logic.
Implementation Details: `publish_version()` re-validates the approval row exists at transition time (service-layer defense in depth beyond the repository join).
Error Handling: `ValidationError` on missing/revoked approval per §18.
Dependencies: Task 03.
Expected Result: Service methods enforce all business rules from §5/§10.
Definition of Done: Passes Task 06 tests.

**Task 05 — Pydantic Schemas**
Objective: `FactVersionCreateRequest`, `FactResponse`, `FactDetailResponse`, `ScholarApprovalResponse` in `schemas/fact.py`.
Existing Architecture to Follow: `NoorHeroesBaseModel` camelCase convention.
Dependencies: Task 01.
Expected Result: Schemas ready for consumption by B-02/B-03/B-06 endpoint layers.
Definition of Done: Schema validation round-trips correctly against ORM data.

**Task 06 — Tests**
Objective: Full unit + integration coverage per §27.
Files to Create: `tests/modules/content/test_fact_approval_gate.py`, `tests/modules/content/test_fact_versioning_immutability.py`.
Dependencies: Tasks 01–05.
Expected Result: All tests green.
Definition of Done: CI-blocking approval-gate test passes; versioning-immutability test passes.

**Task 07 — Documentation Update**
Objective: Update `FAST-API-INSTRUCTIONS.md` §5.4.
Dependencies: Tasks 01–06 complete and verified.
Expected Result: Architecture doc reflects new models and the approval-gate invariant.
Definition of Done: Documentation reviewed for accuracy against final implementation.

## 30. Definition of Done
- All four tables created via migration, matching §4.1 ER diagram exactly.
- Approval-gate invariant enforced at both repository-query and service-transition layers (double enforcement, not single point of failure).
- Editing a published version always produces a new row, never an in-place content mutation.
- `fact_seen_log` append-only, no update/delete code path introduced.
- All unit and integration tests green, including the signature revoke → immediately-unselectable test.
- `FAST-API-INSTRUCTIONS.md` updated.

## 31. Final Verification Checklist
- [ ] `fact`, `fact_version`, `scholar_approval`, `fact_seen_log` tables match §4.1/§4.2 exactly
- [ ] Approval-gate join verified: revoke → immediately unselectable via `get_published_version()`
- [ ] `fact_seen_log` history for prior viewers untouched by a later revocation
- [ ] Editing a published version creates a new `fact_version` row, never mutates the published row's content columns
- [ ] `publish_version()` raises `ValidationError` when called without a valid approval row (tooling-bypass prevention, Edge Case 8)
- [ ] Migration applies/rolls back cleanly
- [ ] No new bounded context created — extends existing `content` module only
- [ ] No PostgreSQL/Redis credentials modified
- [ ] Documentation updated
