# N-03 — Age-Band Difficulty Tuning Panel

## 1. Feature Context
Part of **A.10 Games Module**. Covers the Learning-Science-sign-off-gated panel for adjusting per-age-band difficulty parameters on a **published** game, embedded within N-01's editor rather than as a standalone page (PRD §8, §9 item 3).

## 2. Parent Feature
A.10 Games Module — NextJS Admin

## 3. Sub-feature
**3.3 Age-Band Difficulty Tuning Panel** `[N-03]`

## 4. Objective
Provide an in-editor panel for adjusting `age_band_difficulty_config` on a published game, requiring an additional `learning_science` sign-off field/checkbox before changes can be saved — enforced client-side as a required field and server-side as a hard `422 SIGNOFF_REQUIRED` check (B-06 §17/§18).

## 5. Business Requirements
- §8: Age-Band Difficulty Tuning — accessible from within the Games Catalog Editor (not a separate page), requiring an additional `learning_science` role sign-off before changes to a published game are saved.
- §1.8 NFR: difficulty-tier parameters must be genuinely calibrated per age band, reviewed by Learning Science, not just arbitrarily scaled numbers.
- Permissions: Update-only, behind `content_editor` + `learning_science` sign-off (§8 CRUD permissions table).

## 6. Existing Architecture
Embedded panel within N-01's `GameEditorForm` / `AgeBandDifficultySubform` (already scaffolded in N-01 Task 06), extended here with the sign-off requirement specific to **published** games. Not a new route — a conditional UI section within the existing editor.

## 7. Existing Code to Reuse
- `AgeBandDifficultySubform` (N-01) — extended, not duplicated, with a sign-off gate specifically for the published-game case.
- `useAdminSession()` — to check whether the current admin holds the `learning_science` role/scope for the sign-off checkbox's own validity (an admin without that scope cannot self-sign-off; the field must reflect an actual `learning_science`-scoped session, not just a checkbox anyone can tick).
- `ConfirmationDialog` — optional confirmation step before saving a published game's difficulty change, consistent with other consequential-action patterns in the portal.

## 8. Files to Create
```
src/features/games-catalog/components/learning-science-signoff-field.tsx
src/features/games-catalog/__tests__/learning-science-signoff-field.test.tsx
```

## 9. Files to Modify
```
src/features/games-catalog/components/age-band-difficulty-subform.tsx   # add signoff-required conditional logic for published games
src/features/games-catalog/hooks/use-update-game.ts                     # pass learning_science_signoff field through to PATCH request
src/features/games-catalog/api/games-schema.ts                          # add learningScienceSignoff to gameUpdateInputSchema (conditionally required)
```
**Do Not Change:** N-01's core CRUD flow for draft games — this sign-off requirement applies specifically to difficulty changes on already-published games (per B-06 §10).

## 10. Backend Requirements
Consumes B-06's `PATCH /admin/v1/games/{id}` with the `learning_science_signoff` field, and its `422 SIGNOFF_REQUIRED` error response, exactly as documented.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- `LearningScienceSignoffField`: renders only when (a) the game being edited is `published`, and (b) the `age_band_difficulty_config` has been modified from its last-saved value.
- Field is only interactable/checkable if `useAdminSession().admin` has the `learning_science` scope; otherwise renders as a disabled/informational note ("Requires Learning Science sign-off — you do not currently hold this role") rather than a fake-checkable checkbox.
- Save button for difficulty changes on a published game remains disabled until sign-off is provided by a `learning_science`-scoped session — mirroring N-01's Publish-button-disabled UX-courtesy pattern (client-side convenience, B-06's server-side `422` is the real boundary).

## 13. API Contract
Extends B-06 §13 `PATCH /admin/v1/games/{id}` — request body gains an optional `learning_science_signoff: { admin_id, timestamp }` field, required by the server when `age_band_difficulty_config` changes on a published game.

## 14. Database Requirements
N/A (frontend only).

## 15. Validation
Client-side: sign-off field required (and only enterable by a correctly-scoped session) before the Save button activates for this specific change type. Server-side (B-06) remains the authoritative check.

## 16. Authentication
Relies on `useAdminSession()` for role/scope introspection.

## 17. Authorization
Sign-off field's interactability is itself gated by the `learning_science` scope check — an admin without it cannot fabricate a valid sign-off client-side (though, per the UX-courtesy principle, the server re-validates this independently).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Save attempted without sign-off on a published-game difficulty change | Save button remains disabled; if somehow submitted (stale state), server `422 SIGNOFF_REQUIRED` displayed via `QueryErrorState` |
| Admin without `learning_science` scope attempts to view the panel | Field shown as informational/disabled, not a fake-interactive control |
| Sign-off submitted by a session that server determines lacks the scope (race condition) | Server `422`/`403` displayed, client state corrected on next fetch |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Sign-off field label, informational note, and any validation messages localized via `useTranslation()`.

## 22. RTL
Panel layout renders correctly for Arabic/Urdu.

## 23. Analytics
No dedicated client analytics event specified; the change itself is captured in B-06's admin audit log (§10 of B-06).

## 24. Performance
Negligible — a small conditional form section, no additional data-fetching overhead beyond what N-01's editor already performs.

## 25. Security
Client-side role check is a UX courtesy; server-side scope validation (B-06 §17) is the actual authorization boundary — this distinction is preserved and documented, consistent with N-01's Publish-button precedent.

## 26. Library Requirements
Next.js 15, TanStack Query v5, Zod. No new dependencies.

## 27. Testing
- Unit: sign-off field only renders for published games with modified difficulty config.
- Unit: field is disabled/informational for admins lacking `learning_science` scope.
- Unit: Save button remains disabled until valid sign-off provided.
- Integration: server `422 SIGNOFF_REQUIRED` correctly surfaces if a stale client state bypasses the disabled button (defensive test).

## 28. Documentation
Code comments documenting the client-courtesy-vs-server-boundary distinction, consistent with N-01's established pattern.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Extend gameUpdateInputSchema**
- Objective: Add optional `learningScienceSignoff` field, Zod-validated shape.
- Files to Modify: `games-schema.ts`.

**Task 02 — Build LearningScienceSignoffField Component**
- Objective: Conditional rendering per §12; scope-check via `useAdminSession()`.
- Definition of Done: renders correctly across all three states (not applicable / informational-disabled / interactive).

**Task 03 — Wire Into AgeBandDifficultySubform**
- Objective: Show sign-off field specifically when editing a published game's difficulty config.
- Files to Modify: `age-band-difficulty-subform.tsx`.

**Task 04 — Gate Save Button**
- Objective: Save disabled until valid sign-off present (for this specific change type only).
- Definition of Done: unit test confirms gating logic.

**Task 05 — Wire Signoff Into Update Mutation**
- Objective: `useUpdateGame` passes `learning_science_signoff` through to the PATCH request.
- Files to Modify: `use-update-game.ts`.

**Task 06 — Add Error Handling for Server 422**
- Objective: `QueryErrorState` displays `SIGNOFF_REQUIRED` clearly if triggered.

**Task 07 — Add Tests**
- Objective: Full suite per §27.

**Task 08 — Add Documentation**
- Objective: Client-courtesy-vs-server-boundary comment per §28.

**Task 09 — Final Code Review**
- Objective: Confirm the sign-off requirement applies only to published-game difficulty changes, not general draft editing (avoid over-broad gating).
- Definition of Done: review checklist (§31) fully checked.

## 30. Definition of Done
- Sign-off field correctly gated to published-game difficulty changes only.
- Field interactability correctly reflects the current admin's `learning_science` scope.
- Save button gating and server-error fallback both tested.
- Client-courtesy-vs-server-boundary distinction documented.

## 31. Final Verification Checklist
- [ ] Sign-off field renders only for published games with modified difficulty config
- [ ] Field correctly reflects `learning_science` scope possession (interactive vs. informational)
- [ ] Save button gated correctly until valid sign-off provided
- [ ] Server `422 SIGNOFF_REQUIRED` handled gracefully as a defensive fallback
- [ ] Draft-game editing unaffected by this gating (scope correctly limited)
- [ ] Localization/RTL verified
- [ ] No files outside declared scope modified

---

## 32. Cross-Platform Dependencies
- Backend Dependency: B-06 (`learning_science_signoff` field on `PATCH /admin/v1/games/{id}`).
- KMP Dependency: None.
- Admin Dependency: N-01 (this panel is embedded within, not a standalone page).
- Database Dependency: None (frontend only).
- External Service Dependency: None.
- Figma Dependency: Part of N-01's Games Catalog Editor screen — no separate Figma screen expected.
