# N-07 — Reward/XP-Rule Version Editor

## 1. Feature Context
The authoring surface for new XP/badge-criteria rule versions, with explicit "future events only" framing so no editor is ever confused into thinking a new rule retroactively touches historical ledger entries.

## 2. Parent Feature
E.29 — Content CMS & Scholar Review Workflow

## 3. Sub-feature
2.7 Reward/XP-Rule Version Editor (ID: **N-07**)

## 4. Objective
Build a new-rule-version form against B-09, referencing a valid event type, with the old version shown as still-active-until-cutover and explicit non-retroactivity messaging on submit.

## 5. Business Requirements
- FR-11: new XP rule/badge-criteria version validated (references a valid event type), saved as a new version, old version stays active until cutover; Reward Engine picks up the new rule for future events only.
- §1.18 screen 27: Reward/XP-Rule Version Editor.

## 6. Existing Architecture
`src/features/reward-rules/` module, reached from Content List/Engagement navigation cross-reference.

## 7. Existing Code to Reuse
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/components/confirmation-dialog.tsx::ConfirmationDialog` (for the publish/cutover confirmation, carrying the non-retroactivity messaging)

## 8. Files to Create
- `src/app/(dashboard)/reward-rules/page.tsx` — list of rule versions by event type
- `src/app/(dashboard)/reward-rules/new/page.tsx` — new version form
- `src/features/reward-rules/api/reward-rule-repository.ts`
- `src/features/reward-rules/hooks/use-reward-rules.ts`, `use-event-types.ts`, `use-create-rule-version.ts`
- `src/features/reward-rules/components/rule-version-form.tsx`
- `src/features/reward-rules/components/non-retroactivity-notice.tsx`
- `src/features/reward-rules/types/reward-rule.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `REWARD_RULES.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav item, cross-referenced from Engagement navigation

## 10. NextJS Requirements
- `RuleVersionForm`: `event_type` selector populated from a live event-type registry endpoint (never a hardcoded list); `xp_value`/`badge_criteria` fields.
- `NonRetroactivityNotice`: explicit, always-visible messaging that submitting this form creates a new version applied to future events only — existing ledger entries are never affected — shown both inline on the form and in the submit confirmation dialog.
- List view shows current active version and any prior versions per event type, read-only history.

## 11. Required API
**Admin API** — B-09: `POST /v1/admin/rewards`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="content_editor"`.

## 13. Loading / Empty / Error States
Event-type-list loading state; invalid-event-type inline validation error; submission-failure error state.

## 14. Responsive UI / Accessibility
Standard form accessibility — labeled fields, error messages programmatically associated with their inputs.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`.

## 16. Security
No update/edit action exists anywhere in this module's UI for an existing rule version — only "create new version," mirroring B-09's insert-only repository guarantee.

## 17. Testing
Unit: `event_type` selector sourced from live registry, non-retroactivity notice always rendered. UI: confirm no edit affordance exists for an existing rule version row in the list view. Integration: full create-new-version → old-version-still-shown-as-active-until-cutover flow.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `reward-rule.ts` schema. Files: `types/reward-rule.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `RewardRuleRepositoryImpl`**
Objective: Repository for B-09's endpoint plus event-type registry read. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `RuleVersionForm` and `NonRetroactivityNotice`**
Objective: Event-type-driven form with always-visible non-retroactivity messaging. Dependencies: Task 02. Tests: notice-always-rendered test. Definition of Done: test passes.

**Task 04 — Implement the List and New-Version Pages**
Objective: Version history list + new-version form composition. Dependencies: Task 03. Tests: **mandatory** — no edit affordance exists on any existing rule-version row. Definition of Done: test passes.

**Task 05 — Add Full Test Suite**
Objective: Complete coverage per §17. Definition of Done: all green in CI.

**Task 06 — Final Code Review**
Objective: Confirm zero edit/update UI path exists for an existing rule version. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] `event_type` selector sourced from a live registry, never hardcoded
- [ ] Non-retroactivity messaging always visible on both the form and the submit confirmation
- [ ] Zero edit/update affordance exists for an existing rule-version row anywhere in the UI
- [ ] Old version correctly shown as still-active until cutover

## 20. Definition of Done
Reward/XP-rule authoring correctly communicates and enforces (at the UI level) B-09's append-only, non-retroactive guarantee, giving editors zero path to accidentally believe a new rule touches historical rewards.
