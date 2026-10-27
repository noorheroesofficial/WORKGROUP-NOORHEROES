# N-05 — Badge Management UI

> **Reconciliation note (2026-08-18):** supersedes the badge-CRUD portion of `A11_Rewards_System/NextJS_Admin/02-badge-achievement-definition-manager.md` (now partially deprecated). That file's achievement-level (cumulative) CRUD and Simulate-tool sections are not covered here — see its note for the flagged scope decision.

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers the Admin Portal screens for the badge library and criteria builder, consuming **B-05**. Source: PRD §1.18 Screens 11–13, §2.1 (Rule-Builder Visual Language), §2.2 (Badge Criteria Builder screen spec), §6, §7 items 1, 2.5.

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
3.5 Badge Management UI (Admin ID: **N-05**)

## 4. Objective
Give content admins a safe, structured rule-builder for badge criteria (dropdown-driven, never free-form text), with live validation of the referenced event type, while clearly distinguishing icon-only updates (permitted retroactively) from criteria updates (never retroactive).

## 5. Business Requirements
- Screen Inventory (PRD §1.18): #11 Badge Library, #12 Badge Criteria Builder, #13 Badge Icon/Asset Upload.
- Rule-Builder Visual Language (PRD §2.1): structured rule-builder reused across Badge Criteria, Avatar Unlock Rules, and Challenge Goal Types — not three separate implementations.
- Screen spec (PRD §2.2): event-type dropdown + threshold/condition fields, live validation indicator, icon upload, award-count preview.
- States: Default, Validating, Saved, Error (invalid event-type reference).

## 6. Existing Architecture
React + TypeScript, Admin Portal shell from E.28.

## 7. Existing Code to Reuse
- The shared structured Rule-Builder component (PRD §2.1) — this sub-feature should build it if it doesn't yet exist, since Badge Criteria (N-05), Avatar Unlock Rules (N-06), and Challenge Goal Types (N-02) all consume the same component. If N-02 was implemented first without extracting this component, refactor at this point to share it, per the PRD's explicit non-duplication requirement.
- E.29's `ContentUploadRepository` for icon upload.

## 8. Files to Create
- `app/(admin)/engagement/badges/page.tsx`
- `app/(admin)/engagement/badges/[id]/page.tsx`
- `components/engagement/badges/BadgeLibraryTable.tsx`
- `components/engagement/badges/BadgeCriteriaBuilder.tsx`
- `components/shared/RuleBuilder.tsx` (shared component, if not already extracted)
- `repositories/admin/BadgeAdminRepository.ts`
- `types/admin/badge.ts`
- `__tests__/engagement/badges/BadgeCriteriaBuilder.test.tsx`

## 9. Files to Modify
- `components/shell/EngagementNavGroup.tsx`
- `lib/analytics/EngagementAdminAnalytics.ts`
- `components/engagement/challenges/ChallengeBuilderForm.tsx` (refactor to use shared `RuleBuilder` if N-02 didn't already extract it)

## 10. Backend Requirements
Consumes **B-05** endpoints: `POST/GET /v1/admin/badges`, `PATCH /v1/admin/badges/{id}/criteria`, `PATCH /v1/admin/badges/{id}/icon`, `POST /v1/admin/badges/{id}/retire`.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- **Page:** Badge Library, Badge Criteria Builder (icon upload nested within).
- **Route:** `/engagement/badges`, `/engagement/badges/[id]`.
- **Component:** `BadgeLibraryTable`, `BadgeCriteriaBuilder` (uses shared `RuleBuilder`), live validation indicator (green check / red error based on event-type resolution), award-count preview (read-only stat card).
- **API Client:** `BadgeAdminRepository`.
- **Type Definition:** `Badge`, `BadgeCriteriaVersion`, `BadgeCreateInput`.
- **Form:** React Hook Form + Zod; criteria builder emits `{event_type, condition, threshold}` structured object, never free text.
- **Validation:** live client-side call to a lightweight "validate event type" endpoint or local registry cache as the admin selects a type, showing the Validating → Saved/Error states per PRD §2.2.
- **Authentication/Authorization:** `content_editor`+.
- **States:** Default, Validating, Saved, Error (invalid event-type reference) — implemented explicitly as a state machine on the criteria builder form.
- **Loading/Empty/Error States:** standard, plus the criteria-specific states above.
- **Pagination/Filtering/Sorting:** badge library by active/retired status.
- **Responsive/Accessibility/RTL:** standard.
- **Analytics:** `badge_created`, `badge_criteria_updated`.
- **Performance:** debounce live validation calls.
- **Testing:** UI test confirming the invalid-event-type error state renders correctly; UI test confirming icon-only update path is distinct from criteria-update path in the UI (separate actions/buttons, not conflated).

## 13. API Contract
Reuses B-05's contract verbatim (see `Backend/05-badge-management-api.md` §13).

## 14. Database Requirements
N/A.

## 15. Validation
Criteria builder only allows selecting `event_type` from a fetched registry list (dropdown-constrained, never a free-text field) — this structurally prevents most invalid-event-type submissions client-side, with the server as final authority.

## 16. Authentication
Inherits E.28 session.

## 17. Authorization
`content_editor`+.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Server returns `422 INVALID_EVENT_TYPE` | Criteria Builder enters Error state with red indicator and explanatory message |
| Icon fails upload-safety pipeline | Icon upload area shows E.29 rejection reason |
| `404` unknown badge | Redirect to library with toast |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Badge name/description via localization-key editor.

## 22. RTL
Full RTL support, per PRD §2.5's explicit Arabic RTL wireframe prompt for this exact screen.

## 23. Analytics
`badge_created`, `badge_criteria_updated`.

## 24. Performance
Debounced live event-type validation; award-count preview fetched lazily (not blocking initial form render).

## 25. Security
No security-sensitive client logic beyond standard role-gating; the dropdown-constrained event-type selector reduces (but does not replace) server-side validation.

## 26. Library Requirements
React, TypeScript, React Hook Form, Zod, React Query, Jest/RTL.

## 27. Testing
- **UI test:** Badge Criteria Builder shows Error state with clear messaging for an invalid/unresolvable event type.
- **UI test:** award-count preview renders as read-only (no accidental editable field).
- **Integration:** full badge-create → criteria-update flow, confirming UI never implies retroactive badge revocation.

## 28. Documentation
Document the shared `RuleBuilder` component's API/props clearly, since N-05 (Badge), N-06 (Avatar), and N-02 (Challenge goal type) all depend on it — a breaking change here affects three sub-features.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Shared Rule-Builder Component**
- Task ID: N-05-T01
- Objective: Build (or refactor into) the shared, reusable `RuleBuilder` component per PRD §2.1's explicit reuse requirement.
- Files to Create: `components/shared/RuleBuilder.tsx`.
- Files to Modify: `components/engagement/challenges/ChallengeBuilderForm.tsx` if N-02 built a non-shared version.
- Dependencies: none (or N-02 if refactoring).
- Definition of Done: component is generic enough to configure event-type + condition + threshold for badges, avatar unlock rules, and challenge goal types via props/config.

**Task 02 — Types & API Client**
- Task ID: N-05-T02
- Files to Create: `types/admin/badge.ts`, `repositories/admin/BadgeAdminRepository.ts`.
- Dependencies: B-05.
- Definition of Done: typed repository unit-tested.

**Task 03 — Badge Library & Criteria Builder Screens**
- Task ID: N-05-T03
- Files to Create: `app/(admin)/engagement/badges/page.tsx`, `[id]/page.tsx`, `components/engagement/badges/BadgeLibraryTable.tsx`, `BadgeCriteriaBuilder.tsx`.
- Implementation Details: `BadgeCriteriaBuilder` composes the shared `RuleBuilder`; live-validation state machine (Default/Validating/Saved/Error).
- Dependencies: Tasks 01–02.
- Definition of Done: signature Error-state UI test passes.

**Task 04 — Icon Upload Integration**
- Task ID: N-05-T04
- Implementation Details: icon upload via shared `ContentUploadRepository`, distinct action from criteria update.
- Dependencies: Task 03.
- Definition of Done: icon-only-update-path test passes.

**Task 05 — Permission Gating & Accessibility**
- Task ID: N-05-T05
- Dependencies: Task 03.
- Definition of Done: accessibility audit passes.

**Task 06 — Tests & Documentation**
- Task ID: N-05-T06
- Dependencies: Tasks 01–05.
- Definition of Done: §31 checklist verified.

## 30. Definition of Done
Shared Rule-Builder component built/reused; Badge Library and Criteria Builder functional against B-05; live validation states implemented; icon vs. criteria update paths clearly distinct in the UI.

## 31. Final Verification Checklist
- [ ] Badge Criteria Builder uses the shared `RuleBuilder` component (not a bespoke implementation)
- [ ] Event-type field is dropdown-constrained, never free text
- [ ] Live validation states (Default/Validating/Saved/Error) implemented
- [ ] Invalid event-type reference shows clear Error state
- [ ] Award-count preview renders read-only
- [ ] Icon upload is a distinct action from criteria update
- [ ] `content_editor`+ gating enforced
- [ ] Loading/empty/error states implemented
- [ ] Responsive, accessible, RTL-supported
- [ ] Analytics events fire correctly
- [ ] No school/madrasa/institutional-tier logic introduced
