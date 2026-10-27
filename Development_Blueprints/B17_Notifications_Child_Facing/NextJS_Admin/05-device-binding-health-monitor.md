# N-05 — Device Binding Health Monitor

## 1. Feature Context
Part of Feature B.17 — Notifications (Child-Facing). Read-only dashboard showing binding-switch latency and a count of "misdelivery-risk events correctly prevented" — framed positively as an integrity signal for the exclusive-binding architecture (B-01/B-03), mirroring B.15's duplicate-prevention monitor pattern (PRD §9 item 5).

## 2. Parent Feature
B.17 Notifications (Child-Facing) — NextJS Admin

## 3. Sub-feature
N-05 Device Binding Health Monitor

## 4. Objective
Build a read-only dashboard showing binding-switch latency and misdelivery-risk-prevented counts, restricted to `product_admin`/`trust_safety` roles, sourced from B-08's binding-health reporting API.

## 5. Business Requirements
- Visibility into binding-switch latency and any detected (and automatically prevented) misdelivery-risk events from the send-time re-check — a positive integrity signal (PRD §8, §9 item 5).
- Restricted to `product_admin`/`trust_safety` roles (PRD §8, §9 item 5).
- Framed positively (count of risks correctly prevented, not a raw failure count), mirroring B.15's duplicate-prevention monitor pattern (PRD §9 item 5).

## 6. Existing Architecture
- Extends the Admin Portal "Notification Management" module (PRD §8).
- Mirrors the structure of B.15's duplicate-prevention monitor (`Development_Blueprints/B13_Search_Discovery` or the relevant B.15 blueprint location, if present) — reuse its positive-framing dashboard pattern where applicable.
- Uses `recharts` consistent with N-04.

## 7. Existing Code to Reuse
- N-04's chart/dashboard shell patterns (date-range filter, loading/empty/error states) — reuse structurally for consistency across the two reporting dashboards.
- B.15's duplicate-prevention monitor pattern (if directly reusable component exists).

## 8. Files to Create
- `app/(admin)/notifications/reports/binding-health/page.tsx`.
- `components/notifications/BindingLatencyChart.tsx`.
- `components/notifications/MisdeliveryRiskPreventedCard.tsx`.
- `lib/api/notifications/binding-health.ts` — API client (may extend `lib/api/notifications/reports.ts` from N-04 if a shared reports client module is preferable).
- `lib/types/notifications.ts` — extend with `BindingHealthReport`.
- `tests/notifications/DeviceBindingHealthMonitor.test.tsx`.

## 9. Files to Modify
- Admin Portal navigation — add "Device Binding Health" entry under Notification Management → Reports.

## 10. Backend Requirements
Consumes B-08's `GET /v1/admin/notifications/reports/binding-health` exactly as documented.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Page: read-only dashboard with date-range filter.
- Component: binding-switch latency chart (p50/p95 over time).
- Component: "misdelivery-risk events correctly prevented" summary card, framed as a positive integrity signal.
- API Client: typed wrapper over B-08's binding-health endpoint.
- Type Definition: `BindingHealthReport` matching B-08's response shape.
- Authentication/Authorization: `product_admin`/`trust_safety` role required to view this page.
- Loading/Empty/Error States: per N-04's established pattern.
- Responsive UI: consistent with N-04.
- Testing: correct chart/card rendering from a known fixture API response.

## 13. API Contract
Consumes B-08 §13's `GET /v1/admin/notifications/reports/binding-health` exactly.

## 14. Database Requirements
N/A (frontend only).

## 15. Validation
Date-range picker enforces the same reasonable maximum window as B-08's server-side validation.

## 16. Authentication
Admin session via existing Admin Portal auth context.

## 17. Authorization
Page-level gate: `product_admin`/`trust_safety` only.

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| No data for selected range | Empty state, not a broken/blank chart |
| API failure | Error state with retry action |
| Unauthorized role | Page-level access-restricted state |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Standard portal locale conventions for UI copy.

## 22. RTL
Standard portal RTL conventions.

## 23. Analytics
Not applicable (consumes data, does not emit product analytics events).

## 24. Performance
Leverage B-08's Redis-cached response; debounce filter-driven re-fetches.

## 25. Security
This dashboard surfaces integrity metrics only (latency, prevented-risk counts) — no raw child-identifying data or specific misdelivery-incident detail is rendered (aggregate counts only), consistent with the privacy posture of B-08 §25.

## 26. Library Requirements
Next.js (App Router), TypeScript, React, `recharts`, existing Admin Portal component library.

## 27. Testing
- Unit: chart/card components render correctly from known fixture data.
- Integration: date-range filter changes correctly re-fetch and re-render.
- RBAC: non-`product_admin`/`trust_safety` roles cannot access this page.
- Edge case: empty-range response renders the correct empty state.

## 28. Documentation
Document the "positive framing" design decision (count of prevented risks, not raw incident detail) in code comments, cross-referencing PRD §9 item 5 and the B.15 pattern it mirrors.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Types & API Client**
- Files to Create: `lib/types/notifications.ts` extension, `lib/api/notifications/binding-health.ts`.

**Task 02 — Implement Dashboard Page Shell with Date-Range Filter**
- Files to Create: `reports/binding-health/page.tsx`.
- Existing Files to Reuse: N-04's date-range-picker/shell pattern.
- Authorization: page-level RBAC gate (`product_admin`/`trust_safety`).

**Task 03 — Implement Binding Latency Chart**
- Files to Create: `BindingLatencyChart.tsx`.
- Library: `recharts`.
- Tests: fixture-data rendering test.

**Task 04 — Implement Misdelivery-Risk-Prevented Summary Card**
- Files to Create: `MisdeliveryRiskPreventedCard.tsx`.
- Implementation Details: positive framing per PRD §9 item 5.
- Tests: fixture-data rendering test.

**Task 05 — Implement Loading/Empty/Error States**
- Files to Modify: dashboard page and chart/card components.
- Tests: state-rendering tests per §18.

**Task 06 — Write Full Test Suite & Documentation**
- Tests: per §27, including RBAC access test.
- Documentation: per §28.

## 30. Definition of Done
- Dashboard correctly visualizes binding-switch latency and misdelivery-risk-prevented counts from B-08's API.
- Page-level RBAC restricts access to `product_admin`/`trust_safety` only.
- Consistent with N-04's established dashboard patterns; correctly empty/error/loading-stated.

## 31. Final Verification Checklist
- [ ] Binding-switch latency chart (p50/p95) correctly renders from live/fixture data
- [ ] Misdelivery-risk-prevented summary card renders with correct positive framing
- [ ] Date-range filter correctly re-fetches and re-renders
- [ ] Page is inaccessible to roles other than `product_admin`/`trust_safety`
- [ ] Empty and error states render correctly
- [ ] No raw child-identifying or incident-level detail is exposed in this dashboard
- [ ] Full test suite passes

---

**All 18 sub-features of Feature B.17 — Notifications (Child-Facing) now have complete development blueprints:**
Backend B-01 → B-08, KMP K-01 → K-05, NextJS Admin N-01 → N-05 — saved under `Development_Blueprints/B17_Notifications_Child_Facing/`.
