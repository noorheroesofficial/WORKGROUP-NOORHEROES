# B-04 — Child-Safe Template Governance & Rendering

## 1. Feature Context
Part of Feature B.17 — Notifications (Child-Facing). Child notification copy contains no billing or sensitive analytics — this is a template-authoring-time constraint enforced by content governance, not merely a runtime filter (FR-6), with zero exceptions including reward/milestone notifications.

## 2. Parent Feature
B.17 Notifications (Child-Facing) — Backend (FastAPI)

## 3. Sub-feature
B-04 Child-Safe Template Governance & Rendering

## 4. Objective
Implement `NotificationTemplate` CRUD with a hard, non-bypassable billing/analytics-term blocklist validator for every child-facing template, plus a `TemplateRenderer` that produces locale-appropriate, tone-consistent copy from governed templates at send time.

## 5. Business Requirements
- Child notification copy contains no billing or sensitive analytics language, enforced at template-authoring time via content governance (FR-6) — applies even to milestone/reward notifications that might otherwise reference subscription tier.
- Notification copy tone is warm, non-shaming, non-pressuring, consistent with A.7/A.11's established tone (PRD §2.1) — e.g. streak-risk copy is urgency-aware but not alarming; bedtime copy is calm and inviting.
- This mirrors the platform's established pattern from A.5/A.7's feedback-template and mercy-copy review gates (PRD §3.5) — reuse that pattern's structure where applicable.

## 6. Existing Architecture
- Extends `src/noorheroes/modules/notifications/` (`FAST-API-INSTRUCTIONS.md` §5.8).
- Mirror the blocklist-validation pattern already established for A.7's mercy-toned-copy review workflow (`Development_Blueprints/A7_Habit_Tracker/Backend/11-admin-mercy-toned-copy-localization-review-workflow.md`) — reuse its validator architecture rather than inventing a new one, adapting the term list to billing/analytics terms per this feature's scope.

## 7. Existing Code to Reuse
- `BaseService`, `BaseRepository[ModelT]`.
- A.7's content-governance/blocklist validator pattern (structure, not the term list itself).

## 8. Files to Create
- `src/noorheroes/modules/notifications/template_service.py` — `TemplateService(BaseService)`.
- `src/noorheroes/modules/notifications/template_repository.py` — `TemplateRepository(BaseRepository[NotificationTemplate])`.
- `src/noorheroes/modules/notifications/content_safety_validator.py` — `ChildSafetyBlocklistValidator` with the term list (`subscribe`, `price`, `billing`, `renew`, `trial`, `engagement score`, `retention`, etc.).
- `src/noorheroes/modules/notifications/template_renderer.py` — `TemplateRenderer.render(template, locale, context) -> str`.
- Extend `models.py`: `NotificationTemplate`.
- `alembic/versions/<rev>_create_notification_template_table.py`.
- Extend `schemas.py`: `TemplateCreateRequest`, `TemplateUpdateRequest`, `TemplateResponse`.
- Extend `api.py`: `POST/GET/PATCH /v1/admin/notifications/templates`.
- `tests/modules/notifications/test_template_service.py`.
- `tests/modules/notifications/test_content_safety_validator.py`.

## 9. Files to Modify
None outside this module.

## 10. Backend Requirements
- `TemplateService.create()`/`update()` run every child-facing template body through `ChildSafetyBlocklistValidator` **before** save; on any match, reject with the matched term surfaced in the error response, for every admin role, with no override parameter accepted anywhere in the API.
- `TemplateRenderer.render()` substitutes placeholders (child name, streak count, content title, etc.) into the governed template body for the requested locale.
- Prevent duplicate active template for the same `(type, locale, class)` combination.
- Parent-facing templates are exempt from the blocklist (they may legitimately reference billing) but still pass through the same CRUD/versioning path for consistency.

## 11. KMP Requirements
Not applicable — templates are server-rendered; client only receives final copy via delivery.

## 12. NextJS Requirements
Template CRUD UI is N-01 Notification Template Library, which calls this API.

## 13. API Contract

**Required API — Admin API**
- **HTTP Method:** POST
- **Endpoint:** `/v1/admin/notifications/templates`
- **Request:** `{ "type": "streak_risk", "class": "child_facing", "locale": "en", "body": "Don't lose your {{streak_count}}-day streak! {{minutes_left}} minutes left" }`
- **Response 201:** `{ "template_id": "uuid", "status": "active" }`
- **Response 422 (blocklist violation):** `{ "error": "blocklist_violation", "matched_term": "trial" }`
- **Authentication:** Bearer (admin session)
- **Authorization:** `content_editor` role
- **Validation:** required placeholders present per type; blocklist check for `class=child_facing`
- **Error Responses:** `401`, `403`, `409` (duplicate active template), `422` (blocklist violation or malformed placeholders)

- **HTTP Method:** GET / PATCH — standard CRUD variants of the above, same auth/authorization.

## 14. Database Requirements
- `notification_templates`: `template_id UUID PK`, `type VARCHAR`, `class VARCHAR CHECK IN ('child_facing','parent_facing')`, `locale VARCHAR`, `body TEXT`, `status VARCHAR CHECK IN ('active','archived')`, `created_by UUID`, `created_at TIMESTAMPTZ`; UNIQUE `(type, class, locale)` where `status='active'`.

## 15. Validation
- Blocklist validator runs on every save of a `class=child_facing` template — hard-blocking, no admin-role override (FR-6, non-negotiable per PRD).
- Placeholder syntax validated against the known placeholder set for the template's `type`.

## 16. Authentication
Bearer JWT via admin session dependency.

## 17. Authorization
`content_editor` role required for create/update; read access broader per existing admin RBAC.

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| Blocklist term present in child-facing template | `422` with matched term, save rejected for every role, no override |
| Duplicate active template for same type/class/locale | `409 Conflict` |
| Missing required placeholder | `422` with the missing placeholder named |
| Database failure on save | `500`, transaction rolled back, no partial template persisted |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Templates are authored per-locale (`en`, `hi`, `ar`, `ur`); `TemplateRenderer` selects the template matching the recipient child's current locale, falling back to `en` if no localized template exists for that type — log the fallback occurrence for content-ops visibility.

## 22. RTL
Rendered Arabic/Urdu copy relies on the client's RTL rendering (K-03/notification OS chrome); this backend sub-feature only produces the correctly-directioned text string.

## 23. Analytics
None directly emitted by this sub-feature (template authoring is an admin action, not a child-facing event); template usage is implicitly reflected in `notification_sent` volume per type.

## 24. Performance
Template lookups are cache-friendly (Redis cache keyed by `(type, class, locale)`, invalidated on update) since the same active template is read on every matching send.

## 25. Security
The blocklist gate is a hard content-safety control with zero exceptions — verify in tests that no admin role, including the most privileged, can bypass it via any request parameter (PRD §12.1, §12.5).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Redis (template cache), Pydantic v2, pytest.

## 27. Testing
- Unit: blocklist validator against the full known-bad-phrase list (PRD §5 backend prompt item 6) — asserting rejection for every listed term, for every admin role.
- Unit: template rendering with placeholder substitution across all four locales.
- Integration: full create → validate → publish → render flow.
- Regression: any addition to the blocklist term list re-runs the full rejection-coverage test.

## 28. Documentation
Document the full blocklist term list and the "no override, any role" policy prominently in `content_safety_validator.py`; OpenAPI docs for CRUD endpoints.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create NotificationTemplate Model & Migration**
- Files to Create: `models.py` extension, migration.
- Validation: UNIQUE constraint on `(type, class, locale)` for active templates.

**Task 02 — Implement ChildSafetyBlocklistValidator**
- Objective: Hard-blocking term validator.
- Why Required: PRD's non-negotiable content-safety gate (§5 backend prompt item 6).
- Files to Create: `content_safety_validator.py`.
- Business Rules: FR-6.
- Tests: rejection-coverage test for every known-bad term, for every role — mandatory.
- Do Not Change: do not add a bypass/override parameter for any role.

**Task 03 — Implement TemplateRepository & TemplateService CRUD**
- Files to Create: `template_repository.py`, `template_service.py`.
- Implementation Details: `create()`/`update()` invoke the blocklist validator for `class=child_facing` before persisting.
- Tests: unit tests for CRUD + validator integration.

**Task 04 — Implement TemplateRenderer**
- Files to Create: `template_renderer.py`.
- Implementation Details: placeholder substitution, locale fallback-to-`en` with logged fallback.
- Localization: EN/HI/AR/UR.
- Tests: rendering test per locale, fallback test.

**Task 05 — Implement Admin CRUD API Endpoints**
- Files to Modify: `api.py`.
- Authentication/Authorization: admin session, `content_editor` role.
- Error Handling: per §18.
- Tests: endpoint integration tests including the `422` blocklist-violation response shape.

**Task 06 — Add Template Cache Layer**
- Files to Modify: `template_service.py`.
- Performance: Redis cache keyed by `(type, class, locale)`, invalidated on update.
- Tests: cache-hit/invalidation test.

**Task 07 — Write Full Test Suite & Documentation**
- Tests: per §27.
- Documentation: per §28.

## 30. Definition of Done
- Blocklist validator rejects every known-bad term for every admin role with no override path.
- Full CRUD + rendering implemented and tested across all four locales.
- Template cache correctly invalidates on update.

## 31. Final Verification Checklist
- [ ] Blocklist validator rejects 100% of known-bad terms for every admin role, no exceptions
- [ ] No override/bypass parameter exists anywhere in the API for the blocklist
- [ ] Duplicate active template for same type/class/locale rejected (409)
- [ ] Renderer correctly substitutes placeholders across EN/HI/AR/UR
- [ ] Locale fallback to `en` logged when a localized template is missing
- [ ] Template cache invalidates correctly on update
- [ ] Full test suite passes; OpenAPI documentation matches implemented contract
