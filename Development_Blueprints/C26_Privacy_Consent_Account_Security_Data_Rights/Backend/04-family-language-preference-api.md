# B-04 — Family Language Preference API

## 1. Feature Context
Part of Feature C.26 — Privacy, Consent, Account Security & Data Rights (Settings). Sets the family/parent-level default display language, distinct from B.16 B-02's per-child override.

## 2. Parent Feature
C.26 Privacy, Consent, Account Security & Data Rights (Settings)

## 3. Sub-feature
**B-04 — Family Language Preference API**

## 4. Objective
Implement a family-level default display-locale setting, mirroring B.16 B-02's per-child pattern exactly (upsert, `LanguageRepository` validation, immediate-apply semantics), stored on the family account rather than duplicating a new preferences concept.

## 5. Business Requirements
- FR-10: language picker sets the app's display language; same mechanism as B.16's per-child toggle, but at the family/default level.
- Edge Case 6: changing the family-level default does not affect a child's own individually-overridden language, if any.

## 6. Existing Architecture — Flagged Gap (confirm before implementing)
**The C.26 PRD's §3.4 API List does not enumerate an explicit endpoint for this setting** — only FR-10 and the screen inventory reference it narratively. Per rule 30 (do not guess/invent an API contract), this blueprint proposes the most architecturally consistent contract, grounded in B.16 B-02's already-implemented and directly analogous pattern, but it must be confirmed against the actual API contract when the team provides one, before final implementation.

**Proposed placement:** extend `modules/identity`'s existing `FamilyAccount` model (per `FAST-API-INSTRUCTIONS.md` §5.1, already one of `identity`'s core models) with a single `default_display_locale` column — mirroring B.16 B-02's `child_preferences.display_locale` pattern but at the family-account level, rather than introducing a new `family_preferences` table for a single column.

## 7. Existing Code to Reuse
- `modules/identity/models.py::FamilyAccount` — extend with one new column.
- `modules/localization/repository.py::LanguageRepository` — same validation source B.16 B-02 already uses; do not duplicate the supported-language list.
- `core/deps.py::get_current_parent`.

## 8. Files to Create
- `alembic/versions/xxxx_add_default_display_locale_to_family_account.py`
- `tests/modules/identity/test_family_language_preference.py`

## 9. Files to Modify
- `src/noorheroes/modules/identity/models.py` — add `default_display_locale VARCHAR NOT NULL DEFAULT 'en'` to `FamilyAccount`.
- `src/noorheroes/modules/identity/schemas.py` — add `FamilyLanguagePreferenceResponse`, `FamilyLanguagePreferenceUpdateRequest`.
- `src/noorheroes/modules/identity/api.py` — add `GET /v1/family/language`, `PATCH /v1/family/language` (paths proposed — confirm against actual API contract per §6).

## 10. Backend Requirements
- `GET` returns the family's current `default_display_locale`.
- `PATCH` validates the submitted locale against `LanguageRepository`'s active supported-language list (`422 UNSUPPORTED_LOCALE` otherwise), then updates `FamilyAccount.default_display_locale` directly (single-row update by `family_id`, not an upsert — the column always exists with a default, unlike B.16's one-row-per-child table which may not exist yet for a new child).
- This setting is read by any downstream consumer resolving a "no child-level override present" default locale — coordinate with B.16 B-02's owner on the exact precedence read order (child override first, family default fallback) without modifying B.16 B-02's own endpoint.

## 11. API Contract (proposed, pending confirmation per §6)

### `GET /v1/family/language`
- **Auth:** Bearer (parent)
- **Response 200:** `{ "default_display_locale": "en" }`

### `PATCH /v1/family/language`
- **Auth:** Bearer (parent) — no step-up required (language is not a sensitive action per §1.15 Permission States)
- **Request:** `{ "default_display_locale": "ar" }`
- **Response 200:** `{ "updated": true }`
- **Errors:** `401`, `422 UNSUPPORTED_LOCALE`

## 12. Database Requirements
Single new nullable-with-default column on the existing `family_account` table — no new table.

## 13. Validation
`default_display_locale` required, must exist in `LanguageRepository`'s active supported-language set.

## 14. Authentication
`Depends(get_current_parent)`.

## 15. Authorization
Family-ownership implicit — `family_id` derived from bearer token.

## 16. Error Handling
| Scenario | Response |
|---|---|
| Unsupported locale code | `422 UNSUPPORTED_LOCALE` |
| Missing/malformed body | `422` |
| Database failure | `503`, retryable |

## 17. Offline First
N/A backend.

## 18. Local Data
N/A backend; consumed by K-05.

## 19. Localization
This endpoint stores a locale code, not display text.

## 20. RTL
N/A backend.

## 21. Analytics
Backing source for `language_changed` (K-05).

## 22. Performance
Single-row read/update on an already-indexed primary key (`family_id`).

## 23. Security
Non-sensitive setting — no step-up required, consistent with §1.15's stated Permission States.

## 24. Library Requirements
No new dependencies.

## 25. Testing
- Unit: unsupported locale rejected.
- Integration: update persists and is immediately readable via `GET`.
- Integration: changing the family default does not alter any existing `child_preferences` row (Edge Case 6, cross-feature test with B.16 B-02's table).

## 26. Documentation
OpenAPI must state this is a proposed contract pending confirmation (per §6) until the team provides the authoritative API contract; flag clearly so it is not mistaken for an already-agreed spec.

## 27. AI Coding Agent Implementation Steps

**Task 00 — Confirm Actual API Contract (blocking)**
- **Objective:** Obtain the authoritative endpoint path/method from the team before implementing the proposed contract in §11 as final.
- **Definition of Done:** Contract confirmed or this blueprint's proposal explicitly approved as-is.

**Task 01 — Add `default_display_locale` Column**
- **Files to Modify:** `models.py`; **Files to Create:** migration.
- **Definition of Done:** Column added with sensible default (`'en'`), migration applies cleanly.

**Task 02 — Implement Read/Update Endpoints**
- **Files to Modify:** `schemas.py`, `api.py`.
- **Dependencies:** Task 00, Task 01.
- **Definition of Done:** Both endpoints live, validated against `LanguageRepository`.

**Task 03 — Cross-Feature Non-Interference Test with B.16 B-02**
- **Objective:** Confirm family-level change never mutates `child_preferences` rows.
- **Definition of Done:** Edge Case 6 test passes.

**Task 04 — Full Test Suite & Documentation**
- **Definition of Done:** All §25 tests green.

## 28. Definition of Done
Family-level default language is settable and readable, validated against the platform's real supported-language registry, provably independent of any child's individual override — with the proposed contract explicitly flagged pending confirmation rather than presented as already-agreed.

## 29. Final Verification Checklist
- [ ] API contract confirmed with the team or explicitly approved as proposed (Task 00)
- [ ] Locale validated against live `LanguageRepository` data, not a hardcoded list
- [ ] Family-level change does not affect any child's individual override
- [ ] No new table created — single column added to existing `family_account`
- [ ] No PostgreSQL/Redis credential changes
