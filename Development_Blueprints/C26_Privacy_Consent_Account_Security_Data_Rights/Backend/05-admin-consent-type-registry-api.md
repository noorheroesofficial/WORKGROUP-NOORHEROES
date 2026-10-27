# B-05 — Admin Consent Type Registry API

## 1. Feature Context
Part of Feature C.26's Admin Requirements (§8). Gives Legal/Compliance a managed registry of consent type definitions, replacing B-01's interim hardcoded `CONSENT_TYPE_REGISTRY` constant with a real, versioned, review-gated source of truth.

## 2. Parent Feature
C.26 Privacy, Consent, Account Security & Data Rights (Settings)

## 3. Sub-feature
**B-05 — Admin Consent Type Registry API**

## 4. Objective
Provide full CRUD for consent type definitions (type code, required/optional flag, display-text version reference), gated by legal/scholar review before a change becomes the active version shown to new registrants, restricted to `legal_compliance`/`content_editor` roles.

## 5. Business Requirements
- §8 Admin Requirements: "Consent Type Registry: Admin-managed definitions of consent types (name, required/optional flag, display text version) — changes here are scholar/legal-reviewed."
- CRUD permissions: full CRUD behind `legal_compliance`/`content_editor` role.
- Cross-ref: B-01's `list_consents()` currently derives its 6-item registry from a hardcoded code constant explicitly flagged as interim, pending this admin surface.

## 6. Existing Architecture
Extends `modules/admin/` (per `FAST-API-INSTRUCTIONS.md` §5.2, `AdminRouter` already requires `admin:write` RBAC scope) with a new resource, and reuses A.1's existing legal-content versioning system (referenced by A.1 B-05 §12/consent-record's `terms_version`/`privacy_version`/`child_data_version` fields) for the "display text version reference" rather than inventing a second document-versioning mechanism — confirm the exact existing versioning table/service location before implementing Task 03, per rule 30.

## 7. Existing Code to Reuse
- `modules/admin/models.py` conventions, `AdminRouter` (existing `admin:write` scope pattern).
- A.1's legal-content versioning system (location to be confirmed — likely `modules/identity` or a dedicated `modules/legal_content`, per A.1 B-05's `terms_version` etc. — do not assume its location without verifying).
- `common/base_repository.py::BaseRepository[ModelT]`.
- `common/outbox.py::OutboxWriter` (for `audit_logs` writes, per rule: "every mutating action writes an immutable audit_log row").

## 8. Files to Create
- `src/noorheroes/modules/identity/consent_type_models.py` — `ConsentTypeDefinitionOrm` (`type_code` PK, `required` boolean, `display_text_version_ref`, `review_status`, `active_version_id`)
- `src/noorheroes/modules/identity/consent_type_repository.py` — `ConsentTypeRepository`
- `src/noorheroes/modules/identity/consent_type_service.py` — `ConsentTypeRegistryService(BaseService)`
- `src/noorheroes/modules/identity/consent_type_schemas.py`
- `alembic/versions/xxxx_create_consent_type_definition.py`
- `tests/modules/identity/test_consent_type_registry.py`

## 9. Files to Modify
- `src/noorheroes/modules/admin/api.py` — add `GET/POST/PATCH /v1/admin/consent-types`, `POST /v1/admin/consent-types/{id}/approve` (review-gate action).
- `src/noorheroes/modules/identity/consent_log_service.py` (B-01) — once this registry exists, replace the interim hardcoded constant with a read from `ConsentTypeRepository`, coordinated as a follow-up task on B-01, not duplicated here.

## 10. Backend Requirements
- Create/update writes land in a `pending_review` state; a distinct `approve` action (requiring the reviewing admin's identity, separate from the author) promotes a version to `active` — never auto-activate on save.
- Reject a type-code create/update that would leave the registry without exactly the 3 required + N optional structure B-01 depends on, unless the team explicitly signs off on changing that count (a defensive guard, not a hard business rule — confirm with product before enforcing strictly).
- Enforce `legal_compliance`/`content_editor` role on all mutations; read access broader (any authenticated admin) unless PRD specifies otherwise.
- Every mutation writes an immutable `audit_logs` row (actor, timestamp, before/after diff).

## 11. API Contract

### `GET /v1/admin/consent-types`
- **Response 200:** list of consent type definitions with current active version and any pending-review version.

### `POST /v1/admin/consent-types`
- **Auth:** `legal_compliance`/`content_editor`. Creates a new type definition in `pending_review`.

### `PATCH /v1/admin/consent-types/{id}`
- Updates a definition, creating a new pending-review version (append/version, not in-place mutation of the active version — consistent with the platform's consent-versioning discipline elsewhere).

### `POST /v1/admin/consent-types/{id}/approve`
- Promotes the pending-review version to active; reviewer must differ from the original author (four-eyes principle) — confirm this constraint against actual legal/compliance process requirements before hard-enforcing it.

## 12. Database Requirements
```sql
CREATE TABLE consent_type_definition (
    definition_id UUID PRIMARY KEY,
    type_code TEXT NOT NULL UNIQUE,
    required BOOLEAN NOT NULL,
    display_text_version_ref TEXT NOT NULL,
    review_status TEXT NOT NULL CHECK (review_status IN ('pending_review','active','superseded')),
    authored_by UUID NOT NULL,
    reviewed_by UUID,
    created_at TIMESTAMPTZ NOT NULL,
    activated_at TIMESTAMPTZ
);
CREATE UNIQUE INDEX ON consent_type_definition (type_code) WHERE review_status = 'active';
```

## 13. Validation
`type_code` unique among active definitions; `required` boolean; `display_text_version_ref` must resolve against the existing legal-content versioning system (§6 — location to be confirmed).

## 14. Authentication
Existing admin session mechanism (`get_current_admin`).

## 15. Authorization
`legal_compliance`/`content_editor` role required for all mutations; four-eyes on approval per §11 (pending process confirmation).

## 16. Error Handling
| Scenario | Response |
|---|---|
| Duplicate active `type_code` | `409 CONFLICT` |
| Unauthorized role attempting mutation | `403` |
| Approve attempted by the same author | `403 FOUR_EYES_VIOLATION` (pending confirmation this rule is desired) |
| Invalid `display_text_version_ref` | `422` |

## 17. Offline First
N/A — admin portal is not offline-first.

## 18. Local Data
N/A.

## 19. Localization
`display_text_version_ref` points to localized content managed by the existing legal-content versioning system; this API itself is locale-agnostic.

## 20. RTL
N/A backend.

## 21. Analytics
Not specified; standard admin audit logging suffices per §10.

## 22. Performance
Low-volume, admin-only, no special performance requirements.

## 23. Security
Review-gate (pending → active, ideally four-eyes) is the primary control preventing an unreviewed legal-text change from silently becoming user-facing; immutable audit trail on every mutation.

## 24. Library Requirements
No new libraries.

## 25. Testing
- Unit: create/update always lands in `pending_review`, never auto-activates.
- Unit: approve requires `legal_compliance`/`content_editor` role.
- Integration: full create → review → approve flow, active version correctly promoted, prior version marked `superseded`.
- Integration: unauthorized role rejected on all mutating endpoints.
- Integration: audit log row written on every mutation.

## 26. Documentation
Document the review-gate workflow explicitly in OpenAPI descriptions; note the flagged four-eyes constraint as pending process confirmation.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Confirm Legal-Content Versioning System Location**
- **Objective:** Locate A.1's existing versioning mechanism before wiring `display_text_version_ref` against a guessed table.
- **Definition of Done:** Location confirmed.

**Task 02 — `consent_type_definition` Model & Migration**
- **Files to Create:** model, migration.
- **Dependencies:** Task 01.

**Task 03 — Repository & Review-Gate Service**
- **Files to Create:** `consent_type_repository.py`, `consent_type_service.py`.
- **Definition of Done:** No path exists where a create/update directly activates without a separate approve call.

**Task 04 — Router Wiring with RBAC**
- **Files to Modify:** `admin/api.py`.
- **Definition of Done:** All mutations gated by role; audit log written on each.

**Task 05 — Full Test Suite & Documentation**

**Task 06 — Follow-Up Coordination Note for B-01**
- **Objective:** Flag (not implement here) that B-01's hardcoded registry constant should eventually read from this table.
- **Definition of Done:** Tracked as a follow-up, not silently left permanently hardcoded.

## 28. Definition of Done
Consent type definitions are fully CRUD-managed with a genuine review gate before activation, role-restricted, and fully audited — ready to eventually replace B-01's interim hardcoded registry.

## 29. Final Verification Checklist
- [ ] Legal-content versioning system location confirmed, not guessed
- [ ] Create/update never auto-activates without a separate approve step
- [ ] RBAC enforced on all mutations
- [ ] Immutable audit log row on every mutation
- [ ] Follow-up to migrate B-01 off its hardcoded registry explicitly tracked
- [ ] No PostgreSQL/Redis credential changes
