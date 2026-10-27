# K-05 — Family Language Picker

## 1. Feature Context
Part of Feature C.26. Sets the family/parent-level default display language, distinct from B.16 K-03's per-child override.

## 2. Parent Feature
C.26 Privacy, Consent, Account Security & Data Rights (Settings)

## 3. Sub-feature
**K-05 — Family Language Picker**

## 4. Objective
Render `LanguagePickerScreen`, applying the selected family-level default language immediately, consistent in mechanism with (but independent of) B.16 K-03's per-child language toggle.

## 5. Business Requirements
- FR-10: family/default-level language picker, applied immediately, distinct from a child's own B.16 override.
- Edge Case 6: changing the family default does not affect a child with their own override.
- §1.18 Screen Inventory #14: Language Picker.

## 6. Existing Architecture
Within `:feature:parent-settings`, consumes B-04's proposed (pending confirmation) family-language endpoint. Mirrors B.16 K-03's `LanguageToggle`/`DisplayLanguagePickerScreen` Composable pattern structurally, but writes to the family-level setting, not `child_preferences`.

## 7. Existing Code to Reuse
- B.16 K-03's language-picker Composable structure/visual pattern (reuse the list-of-languages UI, not the per-child write call).
- `:core:datastore`'s locale-application mechanism (however B.16 K-03 applies a language change immediately without app restart — reuse that exact mechanism, do not build a second one).

## 8. Files to Create
- `feature/parent-settings/src/commonMain/kotlin/.../FamilyLanguagePickerScreen.kt`
- `core-data/.../FamilyLanguageRepository.kt` (interface) + impl

## 9. Files to Modify
- `ParentSettingsNavGraph.kt` (K-01) — wire the route.

## 10. Backend Requirements
Consumes B-04's proposed `GET/PATCH /v1/family/language` — **flagged pending confirmation of the actual contract**, per B-04 §6; do not hardcode the proposed path as final without checking B-04's resolution status first.

## 11. KMP Requirements
- Render the same supported-language list B.16 K-03 uses (reuse the existing language-registry client, do not duplicate the list).
- On selection, call `FamilyLanguageRepository.updateDefaultLocale()`, apply immediately via the existing locale-application mechanism (§7), consistent with B.16's "no app restart required" behavior.
- Confirm (via a cross-feature test) that changing this setting does not touch any `child_preferences` local cache entry (Edge Case 6).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Consumes B-04's proposed contract, pending confirmation.

## 14. Database Requirements
Local datastore entry for the family-level default locale, separate from B.16's per-child preference cache.

## 15. Validation
None client-side beyond the language list being closed (no free-text entry).

## 16. Authentication
Parent session; no step-up required (non-sensitive setting, per C.26 §1.15).

## 17. Authorization
None beyond standard parent-session access.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| API failure on update | Inline error, selection reverts to prior value |
| Offline | Selection blocked with a clear "requires connectivity" indicator |

## 19. Offline First
Read (current setting) available from cache; update requires connectivity.

## 20. Local Data
Family-level default locale cached separately from any child's individual override — never merged into the same cache key.

## 21. Localization
Language names displayed in their own native script (existing platform convention, reused from B.16 K-03).

## 22. RTL
Selecting Arabic/Urdu triggers immediate RTL layout switch, consistent with B.16's established behavior.

## 23. Analytics
`language_changed`.

## 24. Performance
Trivial, single-selection screen.

## 25. Security
None beyond standard parent-session access — non-sensitive setting.

## 26. Library Requirements
No new libraries.

## 27. Testing
- Integration test: selecting a language applies immediately without app restart (reused test pattern from B.16 K-03).
- Integration test: family-level change does not mutate any child's individual `child_preferences` cache entry (Edge Case 6).
- UI test: RTL layout switch verified on Arabic/Urdu selection.

## 28. Documentation
KDoc explicitly distinguishing this family-level setting from B.16 K-03's per-child override, cross-referencing both.

## 29. AI Coding Agent Implementation Steps

**Task 00 — Confirm B-04's Contract Status**
- **Objective:** Verify B-04's proposed endpoint has been confirmed before hardcoding it as final.

**Task 01 — `FamilyLanguageRepository`**
- **Files to Create:** interface + impl.
- **Dependencies:** Task 00.

**Task 02 — `FamilyLanguagePickerScreen`**
- **Files to Create:** screen composable, reusing B.16 K-03's list UI pattern.

**Task 03 — Immediate-Apply Integration**
- **Definition of Done:** Reuses the exact same locale-application mechanism B.16 K-03 uses, no app restart required.

**Task 04 — Cross-Feature Non-Interference Test**
- **Definition of Done:** Edge Case 6 verified against B.16's cache.

**Task 05 — Localization, RTL, Analytics, Full Test Suite**

## 30. Definition of Done
Family-level language picker applies immediately, is provably independent of any child's individual override, and reuses B.16's existing immediate-apply mechanism rather than a second implementation.

## 31. Final Verification Checklist
- [ ] B-04's contract confirmed before hardcoding as final
- [ ] Immediate-apply behavior verified, no app restart
- [ ] Family-level change proven independent of child-level overrides (Edge Case 6)
- [ ] RTL switch verified on Arabic/Urdu selection
- [ ] Reuses B.16 K-03's language list/locale-application mechanism, not a duplicate
