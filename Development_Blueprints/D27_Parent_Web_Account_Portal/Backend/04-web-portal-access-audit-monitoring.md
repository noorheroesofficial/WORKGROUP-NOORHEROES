# B-04 — Web Portal Access Audit & Security Monitoring

## 1. Feature Context
Part of Feature D.27 — Parent Web Account Portal. The observability layer that makes B-01's and B-02's structural exclusions verifiable in production, not just at test time — recording client-origin metadata on relevant events, surfacing rejected-request attempts, and alerting on the specific P0 conditions the PRD's Release & Rollback Plan (§15.2) names as rollback triggers.

## 2. Parent Feature
D.27 Parent Web Account Portal (`account.noorheroes.com`)

## 3. Sub-feature
**B-04 — Web Portal Access Audit & Security Monitoring**

## 4. Objective
Record client-origin/user-agent context on existing audit trails for actions taken via the web portal, persist a queryable log of gateway/middleware-rejected out-of-allowlist requests from this origin, and wire the three P0/alerting conditions the PRD specifies (successful out-of-allowlist request, login failure-rate spike, step-up failure-rate spike) into the platform's existing alerting pipeline.

## 5. Business Requirements
- §4.3 Audit Fields: "All actions taken via this web client are recorded in the same audit trails already specified by each underlying owning feature, with the client-origin/user-agent optionally recorded as contextual metadata."
- §10 DevOps Requirements: "Alert (P0) on any production-observed successful request from the `account.noorheroes.com` origin to an out-of-allowlist route. Alert on web portal login failure-rate spikes. Alert on step-up verification failure-rate spikes from this client."
- §8 Admin Requirements: this sub-feature is the data source consumed read-only by N-01's Admin Monitor page.
- §12.9 Security Checklist: "Gateway-level CORS/route allowlist verified to reject every out-of-scope route" — B-04 is what makes this an ongoing, observable guarantee in production, not just a one-time launch check.

## 6. Existing Architecture
Reuses the platform's existing structured logging (`StructuredLoggingMiddleware`, `infrastructure/`) and OpenTelemetry/Prometheus metrics infrastructure (`FAST-API-INSTRUCTIONS.md` §4) rather than introducing a new observability stack. B-02's middleware already logs rejections at the point of rejection (§16 of that blueprint); B-04's job is to ensure that log line is structured, queryable, and wired to alerting — not to reimplement rejection detection.

## 7. Existing Code to Reuse
- `src/noorheroes/infrastructure/` telemetry/metrics module (OpenTelemetry, Prometheus) — reused for alert-rule wiring, not a new monitoring stack.
- B-02's `WebPortalRouteAllowlistMiddleware` rejection log line (§16 of that blueprint) — B-04 consumes and enriches this, not a duplicate detection path.
- `core/deps.py` — wherever `ParentSessionContext`/`AdminSessionContext` are constructed, extended to optionally carry a `client_surface`/origin field sourced from the request, for propagation into audit events.
- Existing audit-log patterns already used by owning features (e.g. `modules/admin/repository.py::AdminAuditRepository`) — reused as the audit-record sink where applicable, not a parallel audit table.

## 8. Files to Create
- `src/noorheroes/infrastructure/monitoring/web_portal_access_log.py` — structured rejection-log writer/reader.
- `src/noorheroes/modules/admin/web_portal_monitor_schemas.py` — `WebPortalAllowlistSnapshotResponse`, `WebPortalRejectedRequestResponse` (read models for N-01).
- `src/noorheroes/modules/admin/web_portal_monitor_api.py` — `GET` endpoint(s) exposing the live allowlist snapshot and rejected-request log to N-01.
- `tests/infrastructure/test_web_portal_access_log.py`
- `tests/modules/admin/test_web_portal_monitor_api.py`

## 9. Files to Modify
- `src/noorheroes/core/deps.py` — propagate `client_surface`/origin context into `ParentSessionContext` where relevant, so downstream audit events (e.g. C.24's cancellation audit, C.26's consent-withdrawal audit) can optionally record it per §4.3.
- Alerting/metrics configuration (exact mechanism to be confirmed against the platform's actual deployed alerting tool — Prometheus Alertmanager, or equivalent; not documented in `FAST-API-INSTRUCTIONS.md`, confirm before implementation per rule 30) — add the three P0/alert rules from §10.
- `src/noorheroes/modules/admin/api.py` — mount `web_portal_monitor_api.py`'s router, `product_admin`/`trust_safety`/`security`-gated.

## 10. Backend Requirements
- On every rejection B-02's middleware logs (§16 of that blueprint), write a structured `WebPortalRejectedRequestEvent` (route, timestamp, origin, a truncated/redacted request identifier — never full request bodies, per `redact()`-equivalent server-side discipline) to a queryable store (reuse existing structured-logging pipeline's query surface, e.g. the platform's log aggregation tool, rather than a new PostgreSQL table, unless the platform's existing pattern is DB-backed audit logs — confirm against `AdminAuditRepository`'s actual backing store before deciding).
- Expose `GET /v1/admin/web-portal-monitor/allowlist` returning the live B-01/B-02 allowlist configuration (sourced directly from the same registry B-02 enforces against — never a separately hand-maintained copy, per PRD §8: "sourced directly from the live gateway configuration, not a separately-maintained admin-entered copy").
- Expose `GET /v1/admin/web-portal-monitor/rejected-requests` returning a paginated log of rejected attempts.
- Wire alert rules:
  1. **P0** — any successful (non-rejected) request from `account.noorheroes.com` to a route not on the B-01/B-02 allowlist. This condition should be structurally unreachable given B-01+B-02; the alert exists as a defense-in-depth tripwire, not an expected occurrence.
  2. Alert on web portal login failure-rate spike (sourced from N-03's `web_portal_login_failed_unrecognized_device` and standard OTP-failure events, aggregated server-side).
  3. Alert on step-up verification failure-rate spike from `client_surface: web_portal` (sourced from B-03's step-up verify failures).

## 11. API Contract

### `GET /v1/admin/web-portal-monitor/allowlist`
- **Auth:** `Depends(get_current_admin)` + `require_admin_scope("web_portal_monitor:read")` (or equivalent RBAC scope, confirm against the admin permission catalog)
- **Response 200:** `{ "allowlist": [ { "method": "...", "path": "...", "owning_feature": "..." } ] }`

### `GET /v1/admin/web-portal-monitor/rejected-requests`
- **Auth:** Same as above
- **Response 200:** `{ "items": [ { "route": "...", "origin": "...", "occurred_at": "..." } ], "total": N, "page": N }`
- **Error Responses:** `403 FORBIDDEN` for non-`product_admin`/`trust_safety`/`security` roles

## 12. Database Requirements
If audit events are DB-backed (pending confirmation per §10), a new append-only table analogous to `AdminAuditLog` (per `FAST-API-INSTRUCTIONS.md` §5.2) scoped to web-portal rejection events; otherwise, reuses the existing log-aggregation query surface with no new schema. This decision must be confirmed, not assumed, before Task 02.

## 13. Validation
Pagination parameters (`page`, `limit`) on the rejected-requests endpoint follow the platform's existing pagination convention (`BaseRepository.list_paginated` / `PageResult` pattern).

## 14. Authentication
`Depends(get_current_admin)` on both monitor endpoints.

## 15. Authorization
Restricted to `product_admin` / `trust_safety` / `security` roles per PRD §8 — no broader admin role may read this data.

## 16. Error Handling
| Scenario | Response |
|---|---|
| Non-privileged admin role queries monitor endpoints | `403 FORBIDDEN` |
| No rejected requests in range | `200`, empty `items` array (feeds N-01's empty state) |
| Allowlist snapshot source unavailable | `503`, never a silently stale/cached fallback presented as current |

## 17. Offline First
Not applicable (backend).

## 18. Local Data
Not applicable (backend).

## 19. Localization
Not applicable (backend) — response field values are structural/technical (route paths, timestamps), not user-facing localized text.

## 20. RTL
Not applicable (backend).

## 21. Analytics
This sub-feature is itself an internal analytics/observability surface, not a producer of product analytics events.

## 22. Performance
Rejected-request log writes must not add meaningful latency to the already-rejected request path (fire-and-forget/async write where the platform's existing logging infrastructure supports it); monitor read endpoints are low-traffic, admin-only, and may use standard pagination without special optimization.

## 23. Security
- The allowlist snapshot endpoint must read the *live* configuration, never a cached or admin-editable copy — this is the specific guarantee PRD §8/§12.5 require ("not admin-runtime-editable").
- Rejected-request log entries must never include full request bodies or credentials — route, origin, and timestamp only, consistent with `redact()`'s existing sensitive-key discipline used elsewhere in the codebase.
- This sub-feature's P0 alert (successful out-of-allowlist request) is the production-facing tripwire for B-01/B-02's entire security guarantee — its correct wiring is as important as the allowlist logic itself.

## 24. Library Requirements
Reuses existing OpenTelemetry/Prometheus infrastructure already present per `FAST-API-INSTRUCTIONS.md` §4 — no new monitoring library introduced without first confirming the platform's actual deployed alerting tool.

## 25. Testing
- Unit: rejected-request events are correctly structured and redacted (no request body/credential leakage).
- Integration: `GET /v1/admin/web-portal-monitor/allowlist` returns a snapshot provably sourced from the same registry B-02 enforces against (not a stale/hand-maintained copy).
- Integration: `GET /v1/admin/web-portal-monitor/rejected-requests` correctly paginated, empty-state-safe.
- Integration: RBAC — non-privileged admin roles receive `403`.
- Alert-rule test (where the platform's alerting tool supports rule-testing): simulated successful out-of-allowlist request triggers the P0 alert condition.

## 26. Documentation
Document the alert-rule definitions and their PRD §10 rationale directly alongside the alerting configuration, so a future on-call engineer understands why each alert exists (e.g. "this alert should never fire; if it does, B-01/B-02's guarantee has failed").

## 27. AI Coding Agent Implementation Steps

**Task 01 — Confirm Audit-Event Backing Store**
- **Objective:** Determine whether rejected-request events are DB-backed (mirroring `AdminAuditLog`) or log-aggregation-backed, per §12.
- **Definition of Done:** Confirmed storage mechanism, documented.

**Task 02 — Implement Structured Rejection-Log Writer**
- **Files to Create:** `web_portal_access_log.py`.
- **Dependencies:** Task 01; consumes B-02's rejection event.

**Task 03 — Propagate `client_surface` Context**
- **Files to Modify:** `core/deps.py`.
- **Objective:** Optional origin/client-surface metadata available to downstream audit events per §4.3.

**Task 04 — Implement Admin Monitor Read Endpoints**
- **Files to Create:** `web_portal_monitor_schemas.py`, `web_portal_monitor_api.py`.
- **Dependencies:** Tasks 01–02.

**Task 05 — Wire the Three P0/Alert Conditions**
- **Objective:** Per §10's three named conditions.
- **Dependencies:** Confirm actual alerting tool before implementation (per rule 30).

**Task 06 — RBAC Wiring**
- **Definition of Done:** `product_admin`/`trust_safety`/`security` only; verified by test.

**Task 07 — Full Test Suite**
- **Definition of Done:** All §25 tests green.

**Task 08 — Documentation**
- **Definition of Done:** Alert rules documented with rationale.

## 28. Definition of Done
Every web-portal-originated sensitive action carries optional client-origin audit context, rejected out-of-allowlist attempts are queryable by privileged admins via a live (never stale) source, and the three named P0/alert conditions are correctly wired to the platform's existing alerting infrastructure.

## 29. Final Verification Checklist
- [ ] Audit-event backing store decision confirmed (Task 01) before implementation
- [ ] Allowlist snapshot endpoint reads the live B-01/B-02 configuration, never a stale copy
- [ ] Rejected-request log entries contain no request bodies or credentials
- [ ] RBAC restricts monitor endpoints to `product_admin`/`trust_safety`/`security`
- [ ] All three P0/alert conditions wired and testable
- [ ] No PostgreSQL/Redis credential changes
