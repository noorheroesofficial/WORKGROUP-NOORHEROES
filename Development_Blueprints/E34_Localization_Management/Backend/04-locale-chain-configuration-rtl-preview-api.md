# B-04 — Locale Chain Configuration & RTL Preview API

## 1. Feature Context
The configuration surface for per-locale fallback ordering, and the data endpoint feeding the RTL Preview tool that lets a localization manager actually see mirrored layout fidelity before a locale-affecting change ships.

## 2. Parent Feature
E.34 — Localization Management

## 3. Sub-feature
1.4 Locale Chain Configuration & RTL Preview API (ID: **B-04**)

## 4. Objective
Build CRUD for `locale_chain_config` (with a no-self-reference constraint) and `GET /v1/admin/locales/{code}/rtl-preview`.

## 5. Business Requirements
- FR-9: locale-chain fallback is explicit and ordered per locale, not a single global default.
- FR-7: full RTL mirroring for Arabic and Urdu, validated via the RTL Preview screen before a locale-affecting change ships.
- §4.2: `locale_chain_config` `CHECK fallback_locale_code != locale_code` (no self-referential loop).

## 6. Existing Architecture
`localization` bounded context, `app/localization/routers/locale_chain_router.py`.

## 7. Existing Code to Reuse
- `app/shared/base_service.py::BaseService`
- E.28's `AuditLogService.log_action()`

## 8. Files to Create
- `app/localization/routers/locale_chain_router.py`
- `app/localization/services/locale_chain_config_service.py`
- `app/localization/repositories/locale_chain_repository.py`
- `app/localization/services/rtl_preview_service.py`
- `app/localization/schemas/locale_chain_schema.py`, `rtl_preview_schema.py`
- `alembic/versions/xxxx_create_locale_chain_config_table.py`

## 9. Files to Modify
- `app/localization/routers/__init__.py` — register router

## 10. Backend Requirements
- `LocaleChainConfigService.set_chain()`: validates `fallback_locale_code != locale_code` at both the application layer and via the DB `CHECK` constraint (defense-in-depth, consistent with the platform's established pattern); rejects a configuration that would create a longer cycle across multiple hops (application-layer graph-cycle check, since the DB constraint alone only catches direct self-reference).
- `RtlPreviewService.get_preview()`: assembles rendered preview data (resolved strings for a given screen/locale via B-02's delivery logic) plus `is_rtl` metadata from the `locale` table, for the frontend's side-by-side comparison rendering.

## 11. Required API / API Contract
`GET /v1/admin/locales/{code}/chain` → current config.
`PUT /v1/admin/locales/{code}/chain` `{fallback_locale_code, priority_order}` → `200`.
`GET /v1/admin/locales/{code}/rtl-preview?screen=` → `200` preview data.

## 12. Database Requirements
`locale_chain_config(locale_code PK/FK, fallback_locale_code FK, priority_order)`, `CHECK fallback_locale_code != locale_code`. Index `(locale_code, priority_order)`.

## 13. Validation
No self-reference (app + DB); no multi-hop cycle (app-layer graph check); `screen` parameter validated against a known screen registry for RTL preview.

## 14. Authentication
`get_current_admin`.

## 15. Authorization
`require_admin_scope("localization_manager")`.

## 16. Error Handling
`422 SELF_REFERENTIAL_CHAIN` or `422 CYCLIC_CHAIN` for invalid configurations; `404` for unknown locale/screen.

## 17. Security
Cycle-prevention (both direct self-reference via DB `CHECK` and multi-hop cycles via application logic) is this sub-feature's core guarantee — mandatory test confirms both a direct self-reference and a 3-locale cycle (A→B→C→A) are rejected.

## 18. Analytics
`rtl_preview_viewed` per §1.19.

## 19. Performance
Small config table, negligible query cost; RTL preview assembly reuses B-02's already-cached delivery data where possible.

## 20. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async, Alembic. No new libraries.

## 21. Testing
Unit: cycle-detection graph logic. Integration: **mandatory** — direct self-reference rejected by DB `CHECK`; **mandatory** — multi-hop cycle rejected by application-layer check; RTL preview correctly returns `is_rtl=true` and resolved strings for Arabic/Urdu fixtures.

## 22. Documentation
OpenAPI docstrings; note on the chain config endpoint that cycles are rejected at both layers.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Write Migration for `locale_chain_config`**
Objective: Table with self-reference `CHECK`. Files: `alembic/versions/xxxx_create_locale_chain_config_table.py`. Tests: migration test + direct-self-reference-rejected test. Definition of Done: tests pass.

**Task 02 — Implement Cycle-Detection Logic**
Objective: Multi-hop graph-cycle check. Files: `services/locale_chain_config_service.py`. Dependencies: Task 01. Tests: **mandatory** — 3-locale-cycle-rejected test. Definition of Done: test passes.

**Task 03 — Implement Router Endpoints for Chain Config**
Objective: `GET`/`PUT` chain config. Files: `routers/locale_chain_router.py`. Dependencies: Task 02. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 04 — Implement `RtlPreviewService`**
Objective: Assemble preview data using B-02's delivery logic + `is_rtl` metadata. Files: `services/rtl_preview_service.py`. Dependencies: B-02. Tests: RTL-fixture-resolution test. Definition of Done: test passes.

**Task 05 — Implement the RTL Preview Endpoint**
Objective: `GET .../rtl-preview`. Dependencies: Task 04. Tests: endpoint integration test. Definition of Done: test passes.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §21, both mandatory tests included. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm cycle prevention covers both direct and multi-hop cases. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] Direct self-reference rejected by DB `CHECK` — mandatory test passing
- [ ] Multi-hop cycles rejected by application logic — mandatory test passing
- [ ] RTL preview correctly resolves strings and `is_rtl` metadata for Arabic/Urdu
- [ ] `localization_manager` scope enforced

## 25. Definition of Done
Locale fallback chains are configured with cycle-safety enforced at two layers, and the RTL Preview tool has the correctly-resolved data it needs for genuine mirrored-layout verification.
