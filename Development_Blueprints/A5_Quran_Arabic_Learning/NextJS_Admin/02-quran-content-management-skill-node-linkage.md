# N-02 — Quran Content Management Extension (Skill-Node Linkage)

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). Extends the existing Admin Quran Management module (Surahs/Ayahs/Translations/Tafseer) with skill-node linkage fields, per B-09.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
N-02 — Quran Content Management Extension (Skill-Node Linkage)

## 4. Objective
Add a skill-node linkage field to the existing Quran Management admin views, while preserving ayah-text immutability in the UI (no edit affordance ever rendered for it) and the existing scholar-sign-off workflow for translations/tafseer.

## 5. Business Requirements
- Admin Requirements §8: this feature's admin surface extends the existing Quran Management module with skill-node linkage fields, not a separate Quran data model. Ayah text is seed-once/immutable; translations/tafseer/recitation tracks are versioned, editable, scholar-sign-off gated.
- FR-21: ayah text never editable post-seed.

## 6. Existing Architecture
This is explicitly an **extension** of the existing Admin Quran Management module (already built as part of the Content CMS/`content` context's admin surface, per the PRD's own framing: "extends that module... not a separate Quran data model"). Per Rule 30, this blueprint must locate and extend the existing module rather than rebuilding it.

## 7. Existing Code to Reuse
- The existing Quran Management module's `BaseResourceClient`-derived resource client, list/detail pages, and translation/tafseer editing forms (confirm exact file locations before extending).
- Existing scholar-sign-off workflow UI (approval status badges, versioning display) — reused as-is, this blueprint only adds a linkage field to the existing forms.

## 8. Files to Create
- `src/features/quran-content/components/skill-node-linkage-field.tsx` (a form field/section added to the existing Ayah edit view)
- `src/features/quran-content/hooks/use-skill-nodes-for-ayah.ts` (fetches linked `skill_node` entries for a given ayah)
- `src/features/quran-content/__tests__/skill-node-linkage-field.test.tsx`

## 9. Files to Modify
- Existing Ayah detail/edit page/component (locate via Task 01) — embed `SkillNodeLinkageField`.
- Existing Ayah resource client — extend read model to include linked `skill_node_id`s if not already present in the response (or fetch separately via N-02's own hook if the existing Ayah API doesn't include this).

## 10. Backend Requirements
Consumes B-09's `skill_node` read endpoints (for the linkage picker/display) plus the existing Quran Management module's own translation/tafseer CRUD endpoints (unmodified by this blueprint).

## 11. KMP Requirements
N/A (admin-only).

## 12. NextJS Requirements
- **Skill-node linkage field**: added to the existing Ayah edit view, showing which `skill_node`(s) reference this ayah (read-only display, or a light picker if curriculum editors need to adjust linkage from this side — confirm against N-01's ownership: node-to-ayah linkage is primarily edited via N-01's `AyahSearchPicker` when creating/editing a `skill_node`; this field here is likely read-only/informational to avoid two conflicting edit surfaces for the same relationship).
- **Ayah-text immutability in UI**: the ayah text field itself must render as read-only/display-only in every view this extension touches — no textbox, no save affordance, ever, for `arabic_text_immutable`.
- **Scholar-sign-off preserved**: this blueprint does not alter the existing translation/tafseer versioning/sign-off UI — it only adds the linkage field alongside it.

## 13. API Contract
Read-only consumption of B-09's `skill_node` list/detail (filtered by `related_ayah_id`); no new write endpoint introduced by this blueprint.

## 14. Database Requirements
N/A (client consumes API only).

## 15. Validation
N/A (read-only field; if a light edit affordance is added per §12's open question, it would reuse N-01's existing cycle-detection/validation flow rather than duplicating it).

## 16. Authentication
Reuses existing Admin Portal session.

## 17. Authorization
Reuses the existing Quran Management module's role scoping (per PRD: "scoped per the existing module's role") — this blueprint does not introduce a new role, and explicitly must never introduce any UPDATE affordance for ayah text regardless of role, since no such role exists by design.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Linked skill-node fetch failure | Graceful "unable to load linked skills" inline message, does not block the rest of the Ayah edit view |
| Ayah text field | No error state possible since it is never editable — display-only |

## 19. Offline First
N/A (admin web app).

## 20. Local Data
N/A (TanStack Query cache only).

## 21. Localization
Reuses existing Quran Management module's localization handling.

## 22. RTL
Reuses existing Quran Management module's RTL/Arabic-script editing support.

## 23. Analytics
N/A (internal admin tooling).

## 24. Performance
Lightweight addition to an existing page; no special concerns.

## 25. Security
Ayah-text immutability is enforced at the database layer by B-09's trigger — this UI-layer read-only rendering is a defense-in-depth UX measure, not the primary control, and must never regress into accidentally exposing an edit path (e.g., via a generic "edit all fields" form component that doesn't explicitly exclude this field).

## 26. Library Requirements
Next.js 15, TypeScript, TanStack Query v5. No new dependencies.

## 27. Testing
- Component test: ayah-text field renders as read-only in every state (no edit mode ever available for it, even if a "quick edit" generic form pattern exists elsewhere in the module).
- Component test: linked skill-node display renders correctly for an ayah with multiple linked nodes.
- Integration test: linked skill-node fetch failure doesn't block the rest of the page.

## 28. Documentation
Inline note on the ayah-text field component explaining why it's permanently read-only, referencing B-09's database-level enforcement as the authoritative control.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Locate Existing Quran Management Module**
- Task ID: N-02-T01
- Objective: Find the existing Ayah edit view, resource client, and translation/tafseer editing components before extending them.
- Dependencies: None (verification task, per Rule 30 — do not rebuild what already exists).
- Definition of Done: File locations confirmed and documented in §6/§9.

**Task 02 — Implement `use-skill-nodes-for-ayah` Hook**
- Task ID: N-02-T02
- Dependencies: N-02-T01, B-09.
- Definition of Done: Hook returns correctly filtered `skill_node` list for a given ayah.

**Task 03 — Build `SkillNodeLinkageField` and Embed in Existing Ayah View**
- Task ID: N-02-T03
- Files to Modify: existing Ayah edit page (per Task 01).
- Dependencies: N-02-T02.
- Definition of Done: Field renders correctly within the existing page without disrupting existing translation/tafseer editing UI.

**Task 04 — Verify Ayah-Text Field Remains Read-Only**
- Task ID: N-02-T04
- Objective: Explicit regression check that no edit path exists for `arabic_text_immutable` anywhere this extension touches.
- Dependencies: N-02-T01, N-02-T03.
- Definition of Done: Component test (Task 05) confirms read-only rendering in all states.

**Task 05 — Tests**
- Task ID: N-02-T05
- Dependencies: N-02-T01–T04.
- Definition of Done: All green in CI.

## 30. Definition of Done
Skill-node linkage visible on the existing Ayah edit view, ayah-text field remains permanently read-only, existing scholar-sign-off workflow untouched, fully tested.

## 31. Final Verification Checklist
- [ ] Ayah text field is read-only in every state, no edit affordance introduced anywhere
- [ ] Linked skill-node display correctly reflects B-09's data
- [ ] Existing translation/tafseer scholar-sign-off workflow unmodified and unregressed
- [ ] No duplicate/conflicting linkage-edit surface introduced (linkage editing remains owned by N-01)
- [ ] Full test suite green in CI
