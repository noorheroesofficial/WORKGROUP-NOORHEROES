# N-03 — Coaching Feedback Template Library Manager

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). Admin CRUD editor for AI Pronunciation coaching-feedback templates, with mandatory, non-bypassable blocklist validation, backed by B-10.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
N-03 — Coaching Feedback Template Library Manager (Admin API consumer)

## 4. Objective
Provide a CRUD table/editor for feedback templates where every save is run through B-10's blocklist validator, blocking the save entirely with the matched term highlighted for every admin role — no override/bypass path anywhere in the UI.

## 5. Business Requirements
- Admin Requirements §8: full CRUD behind `content_editor` role + mandatory blocklist validation, non-bypassable — a template containing a blocked term cannot be saved as active, regardless of admin role.
- §9 Admin AI Code-Generation Prompt: save action runs text through a blocklist validator fetched from `GET /admin/v1/config/feedback-blocklist`; on match, block save entirely with the matched term highlighted, for every admin role, no override option in the UI.

## 6. Existing Architecture
Next.js 15 App Router Admin Portal per N-01/N-02's grounding: TanStack Query v5, Zod, `BaseResourceClient`, `RequirePermission`, `DataTable`.

## 7. Existing Code to Reuse
- `BaseResourceClient` — extend for `FeedbackTemplateResourceClient`.
- `DataTable` for the template list/table view.
- `RequirePermission` gating for `content_editor` role.
- `useTranslation`/`useLocalization` for locale-aware content preview.

## 8. Files to Create
- `src/features/coaching-templates/api/feedback-template-resource-client.ts`
- `src/features/coaching-templates/api/feedback-blocklist-client.ts` (`GET /admin/v1/config/feedback-blocklist`)
- `src/features/coaching-templates/hooks/use-feedback-templates.ts`
- `src/features/coaching-templates/hooks/use-save-feedback-template.ts` (includes blocklist pre-check + server-authoritative validation)
- `src/features/coaching-templates/components/feedback-template-table.tsx`
- `src/features/coaching-templates/components/feedback-template-editor.tsx`
- `src/features/coaching-templates/components/blocklist-match-highlighter.tsx`
- `src/features/coaching-templates/schemas/feedback-template.schema.ts`
- `src/app/(dashboard)/learning/feedback-templates/page.tsx`
- `src/features/coaching-templates/__tests__/feedback-template-editor.test.tsx`

## 9. Files to Modify
- Dashboard sidebar navigation — add "Coaching Feedback Templates" entry, gated by `content_editor`.

## 10. Backend Requirements
Consumes B-10 (`POST/PUT /v1/admin/learning/feedback-templates`, `GET /admin/v1/config/feedback-blocklist`).

## 11. KMP Requirements
N/A (admin-only).

## 12. NextJS Requirements
- **Template table**: `DataTable`-based list, filterable by `confidence_band`/`locale`, per `usePaginationState`/`useDebouncedValue` conventions.
- **Editor**: form for `confidence_band`, `locale`, `text`. On save attempt, first runs a **client-side pre-check** against the fetched blocklist (for immediate feedback), then submits to B-10, which is the **authoritative** check — if the server rejects with a blocklist match, render `BlocklistMatchHighlighter` showing the exact matched term(s) inline in the text field (e.g., highlighted span), not a generic error toast.
- **No override path**: there is no admin-role-conditional "force save" button anywhere in this UI — the save action's only two outcomes are success or a blocked-with-highlighted-term state, for every role including any future elevated/super-admin role.
- **RBAC**: entire page gated behind `content_editor` via `RequirePermission`.
- **Locale-aware preview**: template text previewed with correct RTL rendering for Arabic/Urdu locale templates, via `useLocalization`.

## 13. API Contract
Per B-10 §13: `POST/PUT /v1/admin/learning/feedback-templates`, `GET /admin/v1/config/feedback-blocklist`.

## 14. Database Requirements
N/A (client consumes API only).

## 15. Validation
Zod schema mirrors B-10's request contract; client-side blocklist pre-check (fetched list) is a UX convenience only — the server-side check in B-10 is authoritative and this UI must never assume the client-side pre-check alone is sufficient (e.g., if the blocklist-fetch fails, the client must still submit to the server and honor its authoritative rejection, never silently allow a save because the local pre-check couldn't run).

## 16. Authentication
Reuses existing Admin Portal session.

## 17. Authorization
`RequirePermission` + `content_editor` role; page not rendered for unauthorized roles.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Blocklist match on save (server-authoritative) | Block save, highlight matched term(s) inline, for every role, no override |
| Blocklist-fetch failure (client pre-check) | Client-side pre-check simply skipped; submission still proceeds to the server, whose rejection remains authoritative — never silently bypass server-side enforcement due to a client-side fetch failure |
| Validation failure (missing fields) | Inline Zod error display |
| API failure during save | Toast/inline error with retry, form state preserved |

## 19. Offline First
N/A (admin web app).

## 20. Local Data
N/A (TanStack Query cache only).

## 21. Localization
Template `locale` field drives content-preview language; UI chrome localized via `useTranslation`.

## 22. RTL
Full RTL preview for Arabic/Urdu-locale template text, plus standard Admin Portal RTL layout via `useLocalization`.

## 23. Analytics
N/A (internal admin tooling; B-10's audit_log, including rejected-attempt entries, provides the necessary content-safety monitoring trail).

## 24. Performance
Lightweight CRUD UI; no special performance concerns given the template library's small expected size.

## 25. Security
This is the UI-layer front door to one of the feature's two most safety-critical controls (alongside K-04/B-04's zero-retention guarantee) — the blocklist enforcement must be visibly and functionally impossible to bypass from this UI for any role, verified via component tests attempting to construct a bypass path (e.g., checking no hidden/disabled-but-present "force save" element exists in the DOM for any role).

## 26. Library Requirements
Next.js 15, TypeScript, TanStack Query v5, Zod. No new dependencies.

## 27. Testing
- Component test: save with a blocklisted phrase is blocked, matched term highlighted correctly.
- Component test: no "force save"/override element exists in the rendered DOM for any simulated role, including a hypothetical super-admin role.
- Component test: blocklist-fetch failure does not silently allow a save to succeed without server-side validation (mock a failed pre-check fetch, confirm the save call still goes to the server and honors its rejection).
- Integration test: `content_editor`-gated page renders nothing for unauthorized roles.

## 28. Documentation
Inline note explicitly stating there is no bypass path by design, cross-referencing B-10's CI-blocking backend test as the ultimate enforcement mechanism.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `FeedbackTemplateResourceClient` and `FeedbackBlocklistClient`**
- Task ID: N-03-T01
- Existing Files to Reuse: `BaseResourceClient`.
- Dependencies: B-10.
- Definition of Done: CRUD + blocklist-fetch calls succeed against staging.

**Task 02 — Implement Zod Schema and Query/Mutation Hooks**
- Task ID: N-03-T02
- Dependencies: N-03-T01.
- Definition of Done: Hooks unit-tested, including the server-authoritative-rejection-on-client-fetch-failure path.

**Task 03 — Build `FeedbackTemplateTable`**
- Task ID: N-03-T03
- Existing Files to Reuse: `DataTable`.
- Dependencies: N-03-T02.
- Definition of Done: Table renders with filtering/pagination.

**Task 04 — Build `FeedbackTemplateEditor` and `BlocklistMatchHighlighter`**
- Task ID: N-03-T04
- Implementation Details: Client-side pre-check + server-authoritative submission; matched-term highlighting on rejection; RTL-aware preview.
- Dependencies: N-03-T02.
- Definition of Done: Editor correctly blocks and highlights on a known-bad phrase in component testing.

**Task 05 — Wire Page, RBAC, and Navigation**
- Task ID: N-03-T05
- Dependencies: N-03-T03, N-03-T04.
- Definition of Done: Page reachable only for `content_editor` role.

**Task 06 — Tests**
- Task ID: N-03-T06
- Objective: Full coverage per §27, including the no-bypass-path DOM-inspection test.
- Dependencies: N-03-T01–T05.
- Definition of Done: All green in CI.

## 30. Definition of Done
Feedback Template Library Manager live, blocklist enforcement visibly and functionally non-bypassable for any role, `content_editor` RBAC strictly enforced, full RTL/localization, fully tested.

## 31. Final Verification Checklist
- [ ] Blocklisted phrase save is blocked with the matched term clearly highlighted
- [ ] No override/force-save element exists in the DOM for any role
- [ ] Blocklist-fetch failure never causes a silent bypass of server-side enforcement
- [ ] Page not rendered at all for non-`content_editor` roles
- [ ] RTL-aware content preview verified for Arabic/Urdu templates
- [ ] Full test suite green in CI
