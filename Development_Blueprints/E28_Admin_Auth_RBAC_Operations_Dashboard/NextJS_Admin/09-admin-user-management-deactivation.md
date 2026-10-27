# N-09 — Admin User Management & Deactivation

## 1. Feature Context
Part of E.28. Component #20 in PRD §1.18 (within Role List / Admin User List). Extends the existing `useUsers`/`DataTable` pattern into an admin-scoped variant, plus the deactivation confirmation flow backed by B-09.

## 2. Parent Feature
E.28 — Admin Portal: Authentication, RBAC & Operations Dashboard

## 3. Sub-feature
N-09 — Admin User Management & Deactivation

## 4. Objective
Build the Admin User List/Detail and Deactivation confirmation flow, correctly surfacing the last-super-admin-protection error from B-09.

## 5. Business Requirements
- §4.4: deactivation is soft (`active=false`), never a delete affordance in the UI.
- Implicit: last-active-super-admin cannot be deactivated (B-09's `409 LAST_SUPER_ADMIN_CANNOT_DEACTIVATE`).
- §1.19: `admin_user_deactivated` analytics event.

## 6. Existing Architecture
Extends the existing `useUsers()`/`UserRepositoryImpl`/`DataTable` pattern (currently modeling the parent/family-facing `Users` domain) with an admin-scoped variant reading from B-09's `/v1/admin/users` endpoints — a distinct resource from the existing consumer-facing Users feature, not a reuse of the same repository/schema (different backend table, different fields: role, 2FA status, etc.).

## 7. Existing Code to Reuse
| Component | Location | Reuse For |
|---|---|---|
| `DataTable` pattern (structure only) | `src/features/users/` | Template for Admin User List |
| `ConfirmationDialog` | `src/shared/components/` | Deactivation confirmation |
| `useElevatedSession()` (pattern reference) | `src/features/auth/` | Consider whether deactivation should require step-up elevation, consistent with the existing "High Risk" deletion pattern documented for `useDeleteFamily()` — **decision: yes, deactivation of an admin account is a high-risk action and should require `useElevatedSession()`'s step-up OTP flow, mirroring the existing `DeleteFamilyButton` example in the NextJS instructions manual §15.** |

## 8. Files to Create
- `src/app/(dashboard)/platform/admin-users/page.tsx`
- `src/app/(dashboard)/platform/admin-users/[adminId]/page.tsx`
- `src/features/admin-users/components/admin-user-list.tsx`
- `src/features/admin-users/components/admin-user-detail.tsx`
- `src/features/admin-users/components/deactivate-admin-user-button.tsx`
- `src/features/admin-users/hooks/use-admin-users.ts`
- `src/features/admin-users/hooks/use-deactivate-admin-user.ts`
- `src/features/admin-users/api/admin-users.repository.ts`
- `tests/features/admin-users/deactivation-flow.test.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `ADMIN_USERS.BASE`, `ADMIN_USERS.DEACTIVATE(id)`

## 10. NextJS Requirements
- Admin User List: `DataTable` (email, role, active status), filterable by role/status.
- Admin User Detail: full detail including role assignment.
- Deactivation: `useElevatedSession()`-gated (step-up OTP required, mirroring the existing `DeleteFamilyButton` high-risk-action pattern) + `ConfirmationDialog` with a reason field.
- Last-super-admin protection: `409 LAST_SUPER_ADMIN_CANNOT_DEACTIVATE` surfaced as a clear, specific message, not a generic error.

## 11. API Contract (Consumed)
`GET /v1/admin/users`, `GET /v1/admin/users/{id}`, `POST /v1/admin/users/{id}/deactivate` (B-09).

## 12. Database Requirements
N/A.

## 13. Validation
Deactivation `reason` field required before submission.

## 14. Authentication
Assumes established session; deactivation additionally requires a fresh elevated (step-up 2FA) token.

## 15. Authorization
`super_admin` for list/detail/deactivate.

## 16. Error Handling
`409 LAST_SUPER_ADMIN_CANNOT_DEACTIVATE` → specific, clear message explaining why the action is blocked; `404 ADMIN_USER_NOT_FOUND` standard handling.

## 17. Offline First
N/A.

## 18. Local Data
None persisted (elevated token held in React state only, per `useElevatedSession()`'s existing memory-only pattern).

## 19. Localization
All labels localized.

## 20. RTL
Standard table/form RTL verification.

## 21. Analytics
Fire `admin_user_deactivated` on success.

## 22. Performance
Standard pagination on the Admin User List.

## 23. Security
Deactivation requires step-up elevation (fresh OTP), consistent with the platform's existing high-risk-action pattern — never a single-click destructive action without re-authentication.

## 24. Library Requirements
No new libraries.

## 25. Testing
- Unit: deactivation requires elevated token before submission.
- Unit: last-super-admin-protection error surfaced clearly.
- Integration: full list → detail → deactivate flow.

## 26. Documentation
None beyond standard.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Build Admin User List**
- Task ID: N-09-T01
- Files to Create: `admin-user-list.tsx`, `use-admin-users.ts`, `admin-users/page.tsx`.
- Dependencies: B-09 GET list endpoint.
- Definition of Done: List renders, filterable by role/status.

**Task 02 — Build Admin User Detail**
- Task ID: N-09-T02
- Files to Create: `admin-user-detail.tsx`, `[adminId]/page.tsx`.
- Dependencies: Task 01, B-09 GET detail endpoint.
- Definition of Done: Detail view renders role assignment correctly.

**Task 03 — Implement Elevated Deactivation Flow**
- Task ID: N-09-T03
- Files to Create: `deactivate-admin-user-button.tsx`, `use-deactivate-admin-user.ts`.
- Implementation Details: `useElevatedSession()` step-up → `ConfirmationDialog` with reason field → `POST /v1/admin/users/{id}/deactivate`.
- Security: Mirrors the existing `DeleteFamilyButton` high-risk-action pattern exactly.
- Analytics: `admin_user_deactivated`.
- Dependencies: Task 02, B-09 deactivate endpoint.
- Definition of Done: Deactivation requires fresh OTP elevation before submission succeeds.

**Task 04 — Last-Super-Admin Error Handling**
- Task ID: N-09-T04
- Objective: Clear, specific messaging for the `409 LAST_SUPER_ADMIN_CANNOT_DEACTIVATE` response.
- Files to Modify: `use-deactivate-admin-user.ts`.
- Dependencies: Task 03.
- Definition of Done: Distinct message verified in a dedicated test.

**Task 05 — Localization, RTL Pass**
- Task ID: N-09-T05
- Dependencies: Tasks 01–03.
- Definition of Done: All labels localized; RTL verified.

**Task 06 — Full Test Suite**
- Task ID: N-09-T06
- Files to Create: `tests/features/admin-users/deactivation-flow.test.tsx`.
- Dependencies: Tasks 01–05.
- Definition of Done: All §25 scenarios green.

## 28. Definition of Done
- Admin User List/Detail live, `super_admin`-gated.
- Deactivation requires step-up elevation and a reason, never a single-click action.
- Last-super-admin protection surfaced clearly.

## 29. Final Verification Checklist
- [ ] Deactivation requires fresh OTP elevation before submission
- [ ] Deactivation requires a reason field
- [ ] `409 LAST_SUPER_ADMIN_CANNOT_DEACTIVATE` surfaced with a specific, clear message
- [ ] `admin_user_deactivated` analytics fires on success
- [ ] No hard-delete affordance exists anywhere in this UI
- [ ] RTL layout verified

---

## Blueprint Set Complete

All 18 development blueprints for Feature E.28 (Admin Portal: Authentication, RBAC & Operations Dashboard) have been generated:

**Backend (FastAPI):** B-01 through B-09
**KMP:** Not applicable (web-only feature)
**NextJS Admin:** N-01 through N-09

Files are saved under `Development_Blueprints/E28_Admin_Auth_RBAC_Operations_Dashboard/{Backend,NextJS_Admin}/`.
