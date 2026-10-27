# N-06 — Avatar Item Management UI

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers the Admin Portal screens for the avatar base library, item catalog, and unlock-rule editor, consuming **B-06**. Source: PRD §1.18 Screens 14–17, §6, §7 item 2.

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
3.6 Avatar Item Management UI (Admin ID: **N-06**)

## 4. Objective
Give content admins a catalog-management experience for avatar items whose editor form structurally contains **no real-money price input field anywhere** — mirroring the backend's structural schema absence — and whose unlock-rule editor reuses the shared Rule-Builder component from N-05.

## 5. Business Requirements
- Screen Inventory (PRD §1.18): #14 Avatar Base Library, #15 Avatar Item Catalog, #16 Avatar Item Editor (unlock-rule mapping), #17 Avatar Ownership Distribution (read-only).
- Frontend AI Code-Gen Prompt item 2 (PRD §7): Avatar Item Editor's form schema has NO real-money price input field anywhere — UI test confirming no such input exists, mirroring the backend's structural schema-absence guarantee.

## 6. Existing Architecture
React + TypeScript, Admin Portal shell from E.28.

## 7. Existing Code to Reuse
- Shared `RuleBuilder` component (built/extracted in N-05) for the unlock-rule mapping (badge/level/habit-milestone).
- E.29's `ContentUploadRepository` for item artwork.

## 8. Files to Create
- `app/(admin)/engagement/avatar/base-library/page.tsx`
- `app/(admin)/engagement/avatar/items/page.tsx`
- `app/(admin)/engagement/avatar/items/[id]/page.tsx`
- `app/(admin)/engagement/avatar/items/ownership/page.tsx`
- `components/engagement/avatar/AvatarItemCatalogTable.tsx`
- `components/engagement/avatar/AvatarItemEditorForm.tsx`
- `components/engagement/avatar/OwnershipDistributionView.tsx`
- `repositories/admin/AvatarAdminRepository.ts`
- `types/admin/avatarItem.ts`
- `__tests__/engagement/avatar/AvatarItemEditorForm.test.tsx`

## 9. Files to Modify
- `components/shell/EngagementNavGroup.tsx`
- `lib/analytics/EngagementAdminAnalytics.ts`

## 10. Backend Requirements
Consumes **B-06** endpoints: `POST/GET /v1/admin/avatar-items`, `PATCH /v1/admin/avatar-items/{id}`, `POST /v1/admin/avatar-items/{id}/retire`.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- **Page:** Avatar Base Library, Avatar Item Catalog, Avatar Item Editor, Ownership Distribution.
- **Route:** `/engagement/avatar/base-library`, `/engagement/avatar/items`, `/engagement/avatar/items/[id]`, `/engagement/avatar/items/ownership`.
- **Component:** `AvatarItemCatalogTable`, `AvatarItemEditorForm` (name, category, art upload, unlock-rule mapping via shared `RuleBuilder` configured for badge/level/milestone reference types — **and structurally no price field defined anywhere in the form schema/TypeScript type**), `OwnershipDistributionView` (read-only chart/stat).
- **API Client:** `AvatarAdminRepository`.
- **Type Definition:** `AvatarItem`, `AvatarItemCreateInput` — this TypeScript interface must not declare any `price`/`cost`/`amount_usd`-style field, enforced by the signature test in §27.
- **Form:** React Hook Form + Zod; `AvatarItemCreateInput` Zod schema uses `.strict()` so any unexpected field (including an accidentally-added price field in a future PR) fails validation.
- **Validation:** unlock-rule reference validated via the shared `RuleBuilder`'s live-validation pattern (reused from N-05).
- **Authentication/Authorization:** `content_editor`+.
- **Loading/Empty/Error States:** standard.
- **Pagination/Filtering/Sorting:** catalog by category/retired status.
- **Responsive/Accessibility/RTL:** standard.
- **Analytics:** `avatar_item_created`, `avatar_item_unlock_rule_updated`.
- **Performance:** ownership distribution computed server-side, rendered as a lightweight read-only view.
- **Testing:** signature UI test confirming zero price input exists in the rendered form (PRD §7 item 2).

## 13. API Contract
Reuses B-06's contract verbatim (see `Backend/06-avatar-item-management-api.md` §13).

## 14. Database Requirements
N/A.

## 15. Validation
`AvatarItemCreateInput` Zod schema is `.strict()`; unlock-rule type/reference required and validated against the live registry.

## 16. Authentication
Inherits E.28 session.

## 17. Authorization
`content_editor`+.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Server `422 INVALID_UNLOCK_REFERENCE` | Rule-Builder shows Error state |
| Server `422 UNKNOWN_FIELD` (should never occur given `.strict()` client schema, but handled defensively) | Generic form error surfaced |
| Art fails upload-safety pipeline | Upload area shows E.29 rejection reason |
| `404` unknown item | Redirect to catalog with toast |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Item name via localization-key editor.

## 22. RTL
Full RTL support.

## 23. Analytics
`avatar_item_created`, `avatar_item_unlock_rule_updated`.

## 24. Performance
Ownership distribution view lazy-loaded (not part of the initial catalog list render).

## 25. Security
The signature UI test asserting zero real-money input exists anywhere in the rendered `AvatarItemEditorForm` is treated as a security-relevant regression test, mirroring the backend's structural schema-absence guarantee (PRD §7 item 2) — this test must be part of the CI-blocking suite for this sub-feature, not merely a nice-to-have.

## 26. Library Requirements
React, TypeScript, React Hook Form, Zod (`.strict()`), React Query, Jest/RTL.

## 27. Testing
- **UI test (signature):** render `AvatarItemEditorForm` and assert, via DOM query, that no input element with a name/label/placeholder matching price-related patterns (`price`, `cost`, `usd`, `amount`) exists anywhere in the rendered output (PRD §7 item 2).
- **Integration:** full create-with-unlock-rule-mapping flow.
- **Unit:** Zod `.strict()` schema rejects an injected extra field in a test payload.

## 28. Documentation
Document the structural no-price-field guarantee prominently at the top of `AvatarItemEditorForm.tsx` and `types/admin/avatarItem.ts` to prevent future accidental reintroduction.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Types & API Client (No-Price-Field Guarantee)**
- Task ID: N-06-T01
- Objective: Define `AvatarItem`/`AvatarItemCreateInput` TypeScript types and Zod `.strict()` schema with zero price-related fields.
- Files to Create: `types/admin/avatarItem.ts`, `repositories/admin/AvatarAdminRepository.ts`.
- Tests: unit test asserting the Zod schema rejects an injected `price_usd` field.
- Dependencies: B-06.
- Definition of Done: schema test green.

**Task 02 — Avatar Base Library & Item Catalog Screens**
- Task ID: N-06-T02
- Files to Create: `app/(admin)/engagement/avatar/base-library/page.tsx`, `app/(admin)/engagement/avatar/items/page.tsx`, `components/engagement/avatar/AvatarItemCatalogTable.tsx`.
- Dependencies: Task 01.
- Definition of Done: list screens render with all states.

**Task 03 — Avatar Item Editor with Unlock-Rule Mapping**
- Task ID: N-06-T03
- Files to Create: `app/(admin)/engagement/avatar/items/[id]/page.tsx`, `components/engagement/avatar/AvatarItemEditorForm.tsx`.
- Implementation Details: composes shared `RuleBuilder` (from N-05) configured for badge/level/milestone reference types.
- Dependencies: Task 01, N-05 Task 01 (shared `RuleBuilder`).
- Definition of Done: signature no-price-field UI test passes.

**Task 04 — Ownership Distribution View**
- Task ID: N-06-T04
- Files to Create: `app/(admin)/engagement/avatar/items/ownership/page.tsx`, `components/engagement/avatar/OwnershipDistributionView.tsx`.
- Dependencies: Task 01.
- Definition of Done: read-only view renders correctly.

**Task 05 — Permission Gating & Accessibility**
- Task ID: N-06-T05
- Dependencies: Tasks 02–04.
- Definition of Done: accessibility audit passes.

**Task 06 — Tests & Documentation**
- Task ID: N-06-T06
- Dependencies: Tasks 01–05.
- Definition of Done: §31 checklist verified.

## 30. Definition of Done
Avatar catalog/library/editor/ownership screens functional against B-06; signature no-real-money-field UI test green; unlock-rule mapping reuses shared Rule-Builder component.

## 31. Final Verification Checklist
- [ ] `AvatarItemEditorForm` renders with zero price/cost/amount input fields (signature test green)
- [ ] `AvatarItemCreateInput` Zod schema is `.strict()`, rejects injected extra fields
- [ ] Unlock-rule mapping uses shared `RuleBuilder` component
- [ ] Ownership Distribution view is read-only
- [ ] Retire action does not affect owned-item equippability messaging
- [ ] `content_editor`+ gating enforced
- [ ] Loading/empty/error states implemented
- [ ] Responsive, accessible, RTL-supported
- [ ] Analytics events fire correctly
- [ ] No school/madrasa/institutional-tier logic introduced
