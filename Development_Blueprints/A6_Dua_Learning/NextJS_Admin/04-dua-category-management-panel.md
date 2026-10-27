# N-04 — Dua Category Management Panel

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. Companion to B-11. Re-derived against the real admin portal architecture — see §32.

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
N-04 — Dua Category Management Panel

## 4. Objective
Let scope-appropriate admins add, relabel, reorder, and deactivate dua categories through a settings panel built on the real `BaseResourceClient`/`DataTable`/`RequirePermission` stack, immediately reflected in the child-facing catalog without a deploy.

## 5. Business Requirements
PRD §4.2, §2.1.

## 6. Existing Architecture
Sibling settings page to N-01, following the same real component stack (`NEXT-JS-INSTRUCTIONS.md` §5–§9): `BaseResourceClient`-extending `DuaCategoryResourceClient`, `useDuaCategoryList()`/`useCreateDuaCategory()`/etc. hooks, `DataTable`, `RequirePermission`, `ConfirmationDialog`.

## 7. Existing Code to Reuse
- `BaseResourceClient` (extend for `DuaCategoryResourceClient`)
- `DataTable`, `RequirePermission`, `ConfirmationDialog`
- `useTranslation()`, `useFormatters()`

## 8. Files to Create
- `src/features/dua/api/DuaCategoryResourceClient.ts`
- `src/features/dua/hooks/useDuaCategoryList.ts`, `useCreateDuaCategory.ts`, `useUpdateDuaCategory.ts`, `useDeactivateDuaCategory.ts`
- `src/features/dua/pages/DuaCategoryManagementPage.tsx`
- `src/features/dua/components/CategoryEditorForm.tsx`
- `src/features/dua/components/CategoryReorderList.tsx`
- `src/features/dua/__tests__/CategoryManagementPanel.test.tsx`

## 9. Files to Modify
- Admin navigation/sidebar config — add "Dua Categories" entry under Dua Management, wrapped in `<RequirePermission>`

## 10. Backend Requirements
Consumes B-11 (`GET/POST/PATCH /v1/admin/dua/categories`, `POST .../deactivate`).

## 11. KMP Requirements
N/A directly — consumed indirectly via B-11's public endpoint, rendered by K-09.

## 12. NextJS Requirements
- List of categories (active + inactive) with icon preview, label (default locale), sort order — via `DataTable`
- `CategoryEditorForm`: `category_key` (immutable after creation), icon selector, per-locale label inputs, sort order
- `CategoryReorderList`: persists `sort_order` on save
- Deactivate via `ConfirmationDialog`, surfacing B-11's finalized deactivation rule (block vs. force-confirm)
- Restricted visibility via `RequirePermission`, same scope as N-01 (category taxonomy is content-adjacent, per B-11's correction — not a separate undefined higher-privilege scope)

## 13. API Contract
Per B-11 §13.

## 14. Database Requirements
N/A (frontend).

## 15. Validation
`category_key`: lowercase snake_case, unique, immutable post-creation; English label required minimum.

## 16. Authentication
Existing admin session.

## 17. Authorization
Same permission scope as N-01 (confirmed via B-11's real scope correction — `content_editor`-equivalent, not an undefined `product_admin` string).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Duplicate `category_key` | Inline field error via `parseApiError`, using the backend's `409` message |
| Deactivate with existing published duas | `ConfirmationDialog` reflecting B-11's finalized rule |
| Wrong permission, direct navigation | Graceful permission-denied state via `RequirePermission` |
| API failure | `ErrorView`, form data preserved |

## 19. Offline First / 20. Local Data
N/A (admin web).

## 21. Localization
Authoring surface for per-locale category labels.

## 22. RTL
Admin UI RTL support; Arabic label input needs correct RTL text entry.

## 23. Analytics
N/A (internal admin tool).

## 24. Performance
Trivial — small, infrequently-changed list.

## 25. Security
Permission-gated mutation, same rationale as N-01/B-11.

## 26. Library Requirements
Existing stack only.

## 27. Testing
- Unit: `category_key` validation (immutable, unique, snake_case)
- Integration: create category → immediately visible → immediately usable in N-01's dua editor category picker without a reload/deploy
- Integration: reorder persists correctly
- Security: wrong-permission direct navigation → graceful permission-denied state

## 28. Documentation
Note `category_key` immutability rationale (referenced by `dua.category` FK per B-11).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `DuaCategoryResourceClient`**
Task ID: N-04-T01. Files to Create: `DuaCategoryResourceClient.ts`. Existing Architecture to Follow: `BaseResourceClient` extension pattern. Definition of Done: matches B-11's contract.

**Task 02 — Implement Hooks**
Task ID: N-04-T02. Definition of Done: hooks correctly wrap the resource client.

**Task 03 — Implement List Page**
Task ID: N-04-T03. Files to Create: `DuaCategoryManagementPage.tsx`. Existing Files to Reuse: `DataTable`. Definition of Done: renders active/inactive categories correctly.

**Task 04 — Implement Editor Form**
Task ID: N-04-T04. Files to Create: `CategoryEditorForm.tsx`. Definition of Done: create/edit flows validate and save correctly.

**Task 05 — Implement Reorder Control**
Task ID: N-04-T05. Files to Create: `CategoryReorderList.tsx`. Definition of Done: reorder persists.

**Task 06 — Implement Deactivation Flow**
Task ID: N-04-T06. Existing Files to Reuse: `ConfirmationDialog`. Definition of Done: matches B-11's finalized rule.

**Task 07 — Implement RBAC**
Task ID: N-04-T07. Existing Files to Reuse: `RequirePermission`. Definition of Done: correct permission scope enforced (same as N-01).

**Task 08 — Register Navigation**
Task ID: N-04-T08. Definition of Done: entry visible only to permitted admins.

**Task 09 — Add Tests**
Task ID: N-04-T09. Definition of Done: all §27 scenarios green.

**Task 10 — Add Documentation**
Task ID: N-04-T10. Definition of Done: immutability rationale written.

**Task 11 — Final Code Review**
Task ID: N-04-T11. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
Categories fully manageable via the real `BaseResourceClient`/`DataTable`/`RequirePermission` stack, changes immediately live in the child-facing catalog and N-01's picker, no deploy required.

## 31. Final Verification Checklist
- [ ] `DuaCategoryResourceClient extends BaseResourceClient`
- [ ] Create/edit/reorder/deactivate all function correctly against B-11
- [ ] `category_key` immutable after creation
- [ ] New category immediately usable in N-01 without a deploy
- [ ] Same permission scope as N-01, confirmed not an undefined separate scope
- [ ] Accessibility and responsive layout verified

## 32. Addendum — What Changed From the Original Draft
Corrected from generic Next.js placeholders to the real `BaseResourceClient`-extension pattern, real hook naming, and real shared components (`DataTable`, `RequirePermission`, `ConfirmationDialog`). Also corrected the assumed `product_admin`-only restriction to match B-11's real-scope correction — category management uses the same `content_editor`-equivalent permission as dua content authoring (N-01), not an unconfirmed separate higher-privilege scope.
