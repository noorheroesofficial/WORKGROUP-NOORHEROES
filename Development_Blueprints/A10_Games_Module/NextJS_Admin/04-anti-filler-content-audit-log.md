# N-04 — Anti-Filler Content Audit Log

## 1. Feature Context
Part of **A.10 Games Module**. Covers the read-only, append-only audit log view showing every game's publish-time skill-mapping-gate validation result — the inspectable artifact backing the platform's "100% zero-filler-content audit pass rate" success metric (PRD §1.4, §8, §9 item 4).

## 2. Parent Feature
A.10 Games Module — NextJS Admin

## 3. Sub-feature
**3.4 Anti-Filler Content Audit Log** `[N-04]`

## 4. Objective
Render a read-only, append-only log view (`game_id`, `validated_skill_node_ids`, `validating_admin_id`, `timestamp`) sourced from `GET /admin/v1/games/audit-log` (B-06), restricted to `product_admin`/`trust_safety` roles, supporting periodic compliance reporting (PRD §9 item 4).

## 5. Business Requirements
- §8: Anti-Filler Content Audit Log — read-only, restricted to `product_admin`/`trust_safety` roles.
- §1.4: supports the "Zero-filler-content audit pass rate: 100%" success metric with a concrete, inspectable artifact.
- §12.9 Security Checklist: audit trail is a pre-launch verification item.

## 6. Existing Architecture
Read-only feature module `src/features/games-catalog/` extended with an audit-log sub-feature, restricted via a narrower `RequirePermission` scope than N-02's compliance dashboard, following the existing tiered-permission pattern (`games:read` vs. a new `games:audit`).

## 7. Existing Code to Reuse
- `DataTable`, `FilterPanel`, `SearchBar` (date-range filter variant), `EmptyState`, `QueryErrorState`.
- `RequirePermission` — gated to `product_admin`/`trust_safety` roles specifically (new permission string `games:audit`, following the existing convention).
- `formatDate` / `useFormatters()` — timestamp display.
- `usePaginationState` — standard table pagination.

## 8. Files to Create
```
src/features/games-catalog/api/games-audit-log-client.ts
src/features/games-catalog/api/games-audit-log-schema.ts
src/features/games-catalog/hooks/use-games-audit-log.ts
src/features/games-catalog/components/games-audit-log-table.tsx
src/app/(dashboard)/games-catalog/audit-log/page.tsx
src/features/games-catalog/__tests__/games-audit-log-table.test.tsx
```

## 9. Files to Modify
```
src/shared/constants/api-endpoints.ts       # API_ENDPOINTS.GAMES.AUDIT_LOG
src/shared/constants/permissions.ts         # add "games:audit" permission string
src/shared/components/dashboard-shell.tsx   # add Audit Log nav entry, visible only to product_admin/trust_safety
```
**Do Not Change:** N-01/N-02 components — this is a separate, more restricted read surface.

## 10. Backend Requirements
Consumes B-06's `GET /admin/v1/games/audit-log` exactly as documented, including its `product_admin`/`trust_safety`-only authorization.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- `GamesAuditLogTable`: columns = game title/ID, validated skill node IDs (expandable/truncated list), validating admin (ID or resolved name if available), timestamp (formatted via `useFormatters()`).
- Filter by date range and/or game ID via `FilterPanel`/`SearchBar`.
- Strictly read-only — no action buttons on rows (append-only log, no edit/delete affordance anywhere in the UI, matching the backend's immutable audit table).
- Export/reporting affordance (CSV or similar) may be considered for "supports periodic compliance reporting" (§8) — if implemented, uses existing export patterns from the portal if any exist; otherwise flagged as a nice-to-have, not a hard requirement per the PRD's minimum spec.

## 13. API Contract
Consumes B-06 §13 `GET /admin/v1/games/audit-log`:
```json
{ "entries": [ { "game_id": "uuid", "validated_skill_node_ids": ["uuid"], "validating_admin_id": "uuid", "timestamp": "iso8601" } ] }
```

## 14. Database Requirements
N/A (frontend only).

## 15. Validation
N/A — read-only, no form input beyond filter/search parameters.

## 16. Authentication
Relies on existing session flow.

## 17. Authorization
`RequirePermission permission="games:audit"` — restricted specifically to `product_admin`/`trust_safety` roles (narrower than N-02's `games:read`), matching B-06 §17's backend restriction exactly. Nav entry itself hidden (not merely disabled) for non-qualifying admins, consistent with `RequirePermission`'s conditional-render pattern.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Audit log fetch failure | `QueryErrorState` with retry |
| Insufficient permission (non-product_admin/trust_safety) | `RequirePermission` fallback — page/nav entry not shown at all |
| Empty log (no games ever published yet) | `EmptyState` |

## 19. Offline First
N/A.

## 20. Local Data
N/A (React Query cache only).

## 21. Localization
Column headers and any UI copy localized via `useTranslation()`; timestamps formatted per active locale via `useFormatters()`.

## 22. RTL
Table renders correctly for Arabic/Urdu admin locales.

## 23. Analytics
No dedicated client analytics event specified; this view is itself the audit/compliance-reporting surface.

## 24. Performance
Paginated, indexed backend query (per B-06 §24 precedent) keeps this responsive even as the audit log grows unbounded over the catalog's lifetime — frontend must never attempt to load the full log at once.

## 25. Security
- Strictly read-only and append-only-sourced — no mutation path exists anywhere in this UI.
- Access restricted to `product_admin`/`trust_safety` only, both client-side (nav/route gating) and server-side (B-06's authoritative `403` enforcement) — this is the platform's forensic record for content-governance questions and must not be exposed more broadly.

## 26. Library Requirements
Next.js 15, TanStack Query v5, Zod. No new dependencies.

## 27. Testing
- Unit: table renders all four documented fields correctly (`game_id`, `validated_skill_node_ids`, `validating_admin_id`, `timestamp`).
- Unit: no action/mutation buttons present anywhere in this component tree (structural/snapshot test guarding the append-only nature).
- Integration: `RequirePermission` correctly hides the nav entry and blocks the route for non-`product_admin`/`trust_safety` sessions.
- Integration: date-range/game-ID filtering narrows results correctly.
- Integration: empty-log state renders `EmptyState`, not an error.

## 28. Documentation
Code comments noting this view's role as the concrete, inspectable artifact supporting the platform's 100% anti-filler audit metric (§1.4) — any future feature request to add mutation capability here should be treated as a governance-relevant design change requiring explicit review, not a routine feature addition.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Audit Log Zod Schema**
- Objective: `gamesAuditLogEntrySchema` matching B-06 §13 response shape.

**Task 02 — Implement GamesAuditLogClient**
- Objective: Thin read-only client wrapping `GET /admin/v1/games/audit-log`.

**Task 03 — Implement useGamesAuditLog Hook**
- Objective: React Query hook with pagination + date-range/game-ID filter params.

**Task 04 — Build GamesAuditLogTable**
- Objective: `DataTable` rendering all four fields, no action columns.
- Definition of Done: structural test confirms zero mutation affordances present.

**Task 05 — Register Route & Restricted Navigation**
- Objective: `src/app/(dashboard)/games-catalog/audit-log/page.tsx`; nav entry visible only to qualifying roles.

**Task 06 — Add "games:audit" Permission**
- Objective: New permission string, wired into `RequirePermission` for both nav and route.
- Files to Modify: `permissions.ts`.

**Task 07 — Add Tests**
- Objective: Full suite per §27, including the structural no-mutation-affordance test.

**Task 08 — Add Documentation**
- Objective: Governance-significance comment per §28.

**Task 09 — Final Code Review**
- Objective: Confirm strict read-only/append-only nature preserved; confirm `product_admin`/`trust_safety`-only access enforced both client- and server-side.
- Definition of Done: review checklist (§31) fully checked.

## 30. Definition of Done
- Audit log correctly displays all documented fields, paginated, filterable.
- Strictly read-only — verified via structural test that no mutation affordance exists.
- Access restricted to `product_admin`/`trust_safety` only, both client- and server-side.
- Supports the platform's 100% anti-filler audit metric as a concrete, inspectable artifact.

## 31. Final Verification Checklist
- [ ] All four documented fields (`game_id`, `validated_skill_node_ids`, `validating_admin_id`, `timestamp`) correctly displayed
- [ ] Structural test confirms zero mutation/action affordances present anywhere in this view
- [ ] `RequirePermission` (`games:audit`) restricts both nav visibility and route access to `product_admin`/`trust_safety`
- [ ] Pagination and date-range/game-ID filtering functioning correctly
- [ ] Empty-log state renders `EmptyState`, not an error
- [ ] Localization/RTL verified
- [ ] No files outside declared scope modified

---

## 32. Cross-Platform Dependencies
- Backend Dependency: B-06 (`GET /admin/v1/games/audit-log`), B-04 (source of every logged validation row).
- KMP Dependency: None.
- Admin Dependency: N-01/N-02 referenced conceptually (as the actions being audited) but not linked to, preserving this view's read-only isolation.
- Database Dependency: None (frontend only); backend `admin_audit_log` is the source of truth.
- External Service Dependency: None.
- Figma Dependency: Anti-Filler Content Audit Log screen — Figma Required.
