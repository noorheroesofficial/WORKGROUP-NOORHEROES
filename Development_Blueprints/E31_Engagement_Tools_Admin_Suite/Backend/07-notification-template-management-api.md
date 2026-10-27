# B-07 — Notification Template Management API

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers the admin CRUD surface for the notification template library, split out from campaign scheduling (see **B-08 Notification Campaign Management API**) because the PRD treats the Template Library (Screen #18) and Template Editor (#19) as distinct authoring screens from the Campaign Scheduler/Segment Builder/Test-Device Send/Delivery Report (#20–23). Source: PRD §1.7 FR-6 (template portion), §1.18 Screens 18–19, §3.4.

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
1.7 Notification Template Management API (Backend ID: **B-07**)

## 4. Objective
Let content admins author and maintain the library of approved push/in-app notification templates that B-08's campaign scheduler and B.17's delivery engine consume, ensuring every template goes through the same content-safety review discipline B.17 already established — this layer authors templates, it does not deliver them.

## 5. Business Requirements
- FR-6 (PRD §1.7, template portion): notification template library (push + in-app). CRUD: create/read/update templates.
- **Hard rule (cross-cutting into B-08):** child-targeted campaigns are restricted to approved templates only — this sub-feature is the authoring surface that produces those approved templates.

## 6. Existing Architecture
Extends B.17's Notification Service. FastAPI/SQLAlchemy 2.0/PostgreSQL, Router → Service → Repository layering.

## 7. Existing Code to Reuse
- B.17's existing template content-safety review pipeline (not reimplemented here — this layer calls into it, not duplicates it).
- E.28's audit log + RBAC.

## 8. Files to Create
- `app/routers/admin/notification_templates_router.py`
- `app/schemas/admin/notification_template_schemas.py`
- `app/services/admin/notification_template_admin_service.py`
- `app/repositories/admin/notification_template_admin_repository.py`
- `tests/admin/test_notification_template_admin_api.py`

## 9. Files to Modify
- `app/routers/admin/__init__.py`
- `app/core/audit.py` (`notification_template.created`, `notification_template.updated`)

## 10. Backend Requirements
- **Database:** `notification_templates` (existing/extended from B.17), with `body_key` (localization key, not raw text), `channel` (`push`/`in_app`), `approved` flag, `translations` relationship.
- **Migration:** additive only.
- **Model:** `NotificationTemplate`.
- **Schema/DTO:** `NotificationTemplateCreate` (`name`, `channel`, `body_key`, `translations: {locale: text}`), `NotificationTemplateUpdate`, `NotificationTemplateRead`.
- **Repository:** `create()`, `list()`, `update()`, `get_translation_coverage(template_id)`.
- **Service:** `NotificationTemplateAdminService` — routes new/updated template copy through B.17's content-safety review pipeline before marking `approved=true`; audit logs.
- **Router:** `POST /v1/admin/notification-templates`, `GET /v1/admin/notification-templates`, `PATCH /v1/admin/notification-templates/{id}`.
- **Dependency Injection:** `require_role_any(["content_editor", "notification_manager"])`.
- **Validation:** `channel` ∈ {`push`, `in_app`}; at least a default-locale translation required before a template can be `approved`.
- **Business Rules:** a template only becomes eligible for use in a child-targeted campaign (B-08) once `approved=true`, which requires passing B.17's review pipeline — this sub-feature never sets `approved=true` without that pipeline's sign-off.
- **Exception Handling:** `404`, `422 VALIDATION_ERROR`, `422 CONTENT_REVIEW_REJECTED`.
- **Logging:** structured logs on create/update, including approval-status transitions.
- **Caching:** invalidate cached "approved templates by locale" list consumed by B-08 on write.
- **Transaction:** template write + audit log in one transaction.
- **Pagination/Filtering/Sorting:** list paginated, filterable by `channel`, `approved` status.

## 11. KMP Requirements
N/A — admin-only. Templates are consumed at delivery time by B.17's engine, unmodified by this layer.

## 12. NextJS Requirements
Consumed by **N-07 Notification Template Management UI**.

## 13. API Contract

### `POST /v1/admin/notification-templates`
- **Request:** `{ "name": "ramadan_announcement", "channel": "push", "body_key": "notif_ramadan_announcement", "translations": { "en": "Ramadan Mubarak! New stories are here.", "ar": "..." } }`
- **Response (201):** `NotificationTemplateRead` with `approved: false` until content-safety review completes
- **Errors:** `401`, `403`, `422 VALIDATION_ERROR`, `422 CONTENT_REVIEW_REJECTED`

### `GET /v1/admin/notification-templates`
- Query params: `channel`, `approved`, `page`, `page_size`

### `PATCH /v1/admin/notification-templates/{id}`
- **Request:** updated translations/body_key — re-triggers content-safety review, resets `approved=false` until re-approved.

## 14. Database Requirements
`notification_templates`: existing/extended B.17 table with `approved boolean default false`.

## 15. Validation
`channel` valid enum; default-locale translation required for approval eligibility.

## 16. Authentication
Admin JWT (E.28).

## 17. Authorization
`content_editor`+/`notification_manager`.

## 18. Error Handling
| Scenario | Response |
|---|---|
| Content-safety review rejects template copy | `422 CONTENT_REVIEW_REJECTED` |
| Missing default-locale translation | `422 VALIDATION_ERROR` |
| Unknown template id | `404 NOT_FOUND` |
| Unauthorized/forbidden | `401`/`403` |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Central to this sub-feature — templates are authored per-locale (English, Hindi, Arabic, Urdu), with translation-coverage tracked per template.

## 22. RTL
N/A at API layer.

## 23. Analytics
`notification_template_created` (PRD §1.19).

## 24. Performance
Cached "approved templates by locale" list, invalidated on write, read by B-08's campaign-creation validation path.

## 25. Security
Every template edit re-triggers B.17's content-safety review rather than silently retaining a stale approval — prevents a previously-approved template from being edited into unsafe copy without re-review.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2, pytest-asyncio.

## 27. Testing
- Unit: channel/translation validation.
- Integration: template edit resets `approved` to `false` and re-triggers review.
- Negative cases: content-review rejection, missing default-locale translation, unauthorized.

## 28. Documentation
OpenAPI docs explicitly noting that editing an approved template resets its approval status.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Database Model**
- Task ID: B-07-T01
- Files to Create/Modify: `app/models/notification_template.py` (extend if needed with `approved` flag).
- Tests: migration test.
- Dependencies: none.
- Definition of Done: migration applies cleanly.

**Task 02 — Repository & Service Layers**
- Task ID: B-07-T02
- Files to Create: `app/repositories/admin/notification_template_admin_repository.py`, `app/services/admin/notification_template_admin_service.py`.
- Implementation Details: calls B.17's existing content-safety review client; edit resets `approved=false`.
- Dependencies: Task 01.
- Definition of Done: unit tests green.

**Task 03 — API Endpoints**
- Task ID: B-07-T03
- Files to Create: `app/routers/admin/notification_templates_router.py`.
- Dependencies: Task 02.
- Definition of Done: integration tests green.

**Task 04 — Re-Review-On-Edit Signature Test**
- Task ID: B-07-T04
- Implementation Details: create and approve a template; edit its translation; assert `approved` resets to `false` until content-safety review re-runs.
- Tests: `tests/admin/test_notification_template_admin_api.py::test_edit_resets_approval_status`.
- Dependencies: Tasks 01–03.
- Definition of Done: test passes.

**Task 05 — Documentation & Final Review**
- Task ID: B-07-T05
- Dependencies: Tasks 01–04.
- Definition of Done: §31 checklist verified.

## 30. Definition of Done
Template CRUD implemented; content-safety re-review-on-edit proven; translation-coverage tracking functional; all endpoints audited and tested.

## 31. Final Verification Checklist
- [ ] `POST /v1/admin/notification-templates` creates a template, `approved=false` until reviewed
- [ ] `PATCH .../{id}` resets `approved` to `false` on any content edit
- [ ] Content-safety review rejection surfaced clearly
- [ ] Translation coverage trackable per template
- [ ] Audit log entries written for every mutation
- [ ] Unauthorized/forbidden paths tested
- [ ] No school/madrasa/institutional-tier logic introduced
- [ ] PostgreSQL/Redis credentials untouched
