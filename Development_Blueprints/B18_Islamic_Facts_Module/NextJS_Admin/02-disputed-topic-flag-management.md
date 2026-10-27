# N-02 — Disputed-Topic Flag Management

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). A deliberately narrow, high-bar-gated admin surface enforcing FR-3's zero-exception rule: disputed/jurisprudentially-sensitive topics never get AI-auto-generated child-facing content.

## 2. Parent Feature
B.18 — Islamic Facts Module

## 3. Sub-feature
3.2 Disputed-Topic Flag Management (ID: N-02)

## 4. Objective
Add a "Jurisprudentially Sensitive" toggle on the Topic Registry management page, restricted to `trust_safety`/`scholar_lead` role, that hard-disables the Fact Editor's AI-assist drafting tool for any fact under a flagged topic.

## 5. Business Requirements
- FR-3: disputed/jurisprudentially-sensitive topics stay out of child-facing auto-generation — a hard, zero-exception rule.
- §8: Disputed-Topic Flag = Update-only behind `trust_safety`/`scholar_lead` role, deliberately a higher bar than standard content editing.
- §12.5: enforced server-side at the AI-assist endpoint itself (B-06), not just a hideable UI button — this UI is a convenience layer on top of that server-side guarantee, never the sole enforcement point.

## 6. Existing Architecture
Extends the Topic Registry's own management page (or a flag within it) per §9 Admin AI Code-Generation Prompt item 2. Reuses the Admin Portal's existing role-context for RBAC.

## 7. Existing Code to Reuse
- Existing Topic Registry management page/component (confirm exact existing location before assuming a new page is needed — likely shared across A.3/A.5/A.6/B.18's topic taxonomies).
- Existing role-gated toggle component pattern from elsewhere in the Admin Portal, if one exists.

## 8. Files to Create
- `components/islamic-facts/DisputedTopicToggle.tsx`.

## 9. Files to Modify
- Existing Topic Registry page — add the toggle, gated to `trust_safety`/`scholar_lead` role.
- `lib/api/islamicFacts.ts` (N-01) — add `patchTopicDisputedFlag()`.
- `components/islamic-facts/FactForm.tsx` (N-01) — read the topic's `is_jurisprudentially_sensitive` flag and hard-disable (not just hide) the AI-assist button for facts under that topic, if the CMS has an AI-assist tool.

## 10. Backend Requirements
Consumes B-06's `PATCH /v1/admin/topics/{id}/disputed-flag`. No backend code produced here.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- **Component:** `DisputedTopicToggle` rendered on the Topic Registry page — visible (read-only) to all admins, interactive only for `trust_safety`/`scholar_lead` roles.
- **Form/Validation:** toggling triggers a confirmation dialog (given the sensitivity/audit weight of this action) before submitting the PATCH.
- **Authorization/Permissions:** non-privileged roles see the control rendered disabled/read-only, never a live-but-hidden button.
- **Loading State:** toggle shows a brief loading spinner during the PATCH request.
- **Error State:** toast error on failure; toggle state reverts to last-confirmed server state (no optimistic-update drift).
- **Cross-cutting effect:** `FactForm.tsx` (N-01) reads the current topic's flag and disables its AI-assist control entirely when flagged — the client-side disable is a UX convenience; the actual enforcement is B-06's server-side check, and this UI must never claim otherwise (see §25 Security).
- **Accessibility:** toggle has a clear `aria-label` including current state ("Jurisprudentially Sensitive: On/Off"); confirmation dialog is keyboard-navigable and screen-reader-announced.

## 13. API Contract
**Required API:** `PATCH /v1/admin/topics/{id}/disputed-flag` (B-06).
**Authentication:** Bearer, admin.
**Authorization:** `trust_safety` or `scholar_lead` role.
**Request:** `{ "is_jurisprudentially_sensitive": true }`.
**Error Responses:** `403` for any other role, including `content_editor` attempting this action.

## 14. Database Requirements
N/A directly — consumes B-06's API (backed by B-06's `topic` table).

## 15. Validation
Confirmation dialog required before submit (double-confirmation for this high-sensitivity toggle, beyond standard form submission).

## 16. Authentication
Standard Admin Portal auth.

## 17. Authorization
`trust_safety`/`scholar_lead` role strictly required for the toggle interaction; other roles see it as read-only, disabled.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Non-privileged role attempts toggle | Control rendered disabled/read-only in UI; if somehow triggered, `403` from B-06 shown as a toast |
| Network/API failure | Toast error, toggle state reverts to last-confirmed server state |

## 19. Offline First
N/A — online-only admin surface.

## 20. Local Data
N/A.

## 21. Localization
Admin chrome standard localization; topic name label rendered as stored (may include non-English text).

## 22. RTL
N/A beyond standard admin chrome handling; topic labels render correctly regardless of script direction.

## 23. Analytics
N/A — internal admin tool; audit logging (high-sensitivity flag) is B-06's server-side responsibility.

## 24. Performance
Negligible — single PATCH request, no heavy computation.

## 25. Security
This UI must never be treated as the enforcement boundary — code review must confirm the AI-assist hard-disable in `FactForm.tsx` is a UX convenience layered on top of B-06's server-side check, not a replacement for it, and that the disable state cannot be defeated by direct DOM manipulation bypassing an otherwise-live button (i.e., confirm the underlying AI-assist API call, if attempted directly, is rejected by B-06 regardless of this UI's state).

## 26. Library Requirements
Existing Admin Portal toggle/dialog component library — no new libraries.

## 27. Testing
- Unit: toggle only interactive for correct roles.
- Unit: confirmation dialog required before submit.
- Integration: toggling flag correctly disables AI-assist in `FactForm.tsx` for facts under that topic.
- Security test (cross-reference B-06's own test): confirm a direct API call to AI-assist bypassing this UI is still rejected — this UI's test suite should not claim security coverage that only B-06's test actually provides.

## 28. Documentation
Component documentation noting this control is UX-convenience only; the true enforcement boundary is documented in B-06.

## 29. AI Coding Agent Implementation Steps

**Task 01 — API Client Extension**
Objective: `patchTopicDisputedFlag()` in `lib/api/islamicFacts.ts`.
Dependencies: B-06 deployed or contract-mocked, N-01's API client file existing.
Definition of Done: Typed client function available.

**Task 02 — Toggle Component**
Objective: `DisputedTopicToggle.tsx` with role-gating and confirmation dialog.
Dependencies: Task 01.
Definition of Done: Component renders correctly per role, requires confirmation.

**Task 03 — Wire into Topic Registry Page**
Objective: Add toggle to existing Topic Registry page.
Files to Modify: existing Topic Registry page.
Dependencies: Task 02.
Definition of Done: Toggle visible and functional in context.

**Task 04 — Wire AI-Assist Hard-Disable in Fact Editor**
Objective: `FactForm.tsx` reads flag, disables AI-assist button.
Files to Modify: `FactForm.tsx` (N-01).
Dependencies: Task 01, N-01 complete.
Definition of Done: AI-assist control fully disabled (not hidden-but-clickable) for flagged topics.

**Task 05 — Tests**
Dependencies: Tasks 01–04.
Definition of Done: All green, including confirmation of B-06's server-side enforcement as the true security boundary.

## 30. Definition of Done
- Toggle functioning, role-gated, confirmation-required.
- Fact Editor's AI-assist control hard-disabled for flagged topics.
- Explicit acknowledgment (in code comments/tests) that server-side enforcement (B-06) is the true security boundary, this UI is convenience only.

## 31. Final Verification Checklist
- [ ] Toggle interactive only for `trust_safety`/`scholar_lead` roles
- [ ] Confirmation dialog required before submit
- [ ] AI-assist control genuinely disabled (not just visually) for flagged-topic facts
- [ ] Test suite does not overstate this UI's security guarantee — B-06's server-side test remains the actual security proof
- [ ] Accessibility verified for toggle and confirmation dialog
