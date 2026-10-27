# N-04 — Parent Web Portal Account & Security Management

## 1. Feature Context
Part of Feature D.27 — Parent Web Account Portal. The Account & Security screen: profile edit, password/PIN reset, and language preference, reusing the same underlying credential infrastructure as the Mobile App's Parent PIN rather than duplicating it.

## 2. Parent Feature
D.27 Parent Web Account Portal (`account.noorheroes.com`)

## 3. Sub-feature
**N-04 — Parent Web Portal Account & Security Management**

## 4. Objective
Build the Account & Security screen allowing profile edit, password/PIN reset (step-up gated, same credential as A.1 B-04/C.19 B-03's `parent_pin`), and language preference update, with zero duplicated credential logic.

## 5. Business Requirements
- FR-6: "Account & Security screen: profile edit, password/PIN reset (the same underlying credential as the mobile app's Parent PIN, reused not duplicated), language preference."
- §1.18 Screens #3–4: Account & Security, Password/PIN Reset (step-up gated).
- §2.3 Tab Structure: sensitive actions require step-up (via N-02's `StepUpModal`).

## 6. Existing Architecture — Gap Flagged
A.1 B-04 ("Parent PIN & Biometric Security API") explicitly states the PIN "is never a standalone server credential... gates local app state only, never used for remote login," and its `POST /v1/identity/auth/pin` endpoint is documented as callable with `require_elevated_session` for **Settings-triggered resets** — this is the endpoint FR-6 refers to as reusable from the web. However, A.1 B-04's own framing assumes a Settings context inside the Mobile App; whether `POST /v1/identity/auth/pin` is already allowlisted/reachable for a web-originated, step-up-elevated request (per this document's B-01/B-02) has not been confirmed — flagged for Task 01, not assumed. Language preference reuses `noorheroes-admin`'s equivalent pattern (`updateLanguagePreference()`/`fetchLocalizationConfig()` per `NEXT-JS-INSTRUCTIONS.md` §7) if a parent-facing equivalent exists, or A.1's own locale-update path — confirm which is authoritative before wiring (Task 02).

## 7. Existing Code to Reuse
- A.1 B-04's `POST /v1/identity/auth/pin` (reset path, `require_elevated_session`-gated) — reused unmodified.
- N-02's `apiClient`, `StepUpModal`, `SessionContext`.
- Locale-update endpoint (owning feature to be confirmed, Task 02) — likely A.1's or C.26's language-preference path (C.26 Backend B-04 "Family Language Preference API" is a plausible owner, confirm before wiring).

## 8. Files to Create
- `noorheroes-account-portal/src/app/(portal)/account-security/page.tsx`
- `noorheroes-account-portal/src/features/account-security/api/account-security-client.ts`
- `noorheroes-account-portal/src/features/account-security/components/pin-reset-form.tsx`
- `noorheroes-account-portal/src/features/account-security/components/language-preference-selector.tsx`
- `noorheroes-account-portal/tests/features/account-security/pin-reset.test.tsx`

## 9. Files to Modify
- N-02's `allowed-endpoints.ts` — register the confirmed PIN-reset and language-preference endpoints.

## 10. Backend Requirements
Consumes A.1 B-04's `POST /v1/identity/auth/pin` (reset path) and the confirmed language-preference endpoint (Task 02) — no new backend logic, pending B-01/B-02 allowlist confirmation (Task 01).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Profile edit form (fields per A.1's existing parent profile schema — confirm exact editable fields before building, do not invent fields beyond what A.1 exposes).
- Password/PIN reset form, gated behind `StepUpModal` before submission is enabled.
- Language preference selector reusing the shared design-token/localization package's supported-language list (EN/HI/AR/UR).
- Success/confirmation state after reset; error state for reset failure (invalid format, step-up expired mid-form).
- Fire `web_account_security_viewed` on screen view, `web_password_pin_reset_initiated` on reset submission.

## 13. API Contract
Consumes A.1 B-04's contract (`POST /v1/identity/auth/pin`) and the confirmed language-preference contract, both as documented in their owning blueprints.

## 14. Database Requirements
Not applicable (frontend).

## 15. Validation
Client-side PIN format check (4–6 digits) mirroring A.1 B-04's server-side rule, as a UX convenience only — server remains authoritative.

## 16. Authentication
Requires active `SessionContext`; PIN reset additionally requires fresh `StepUpModal` elevation per FR-3.

## 17. Authorization
Self-only, enforced server-side by A.1 B-04 (`parent_id` from bearer token).

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Invalid PIN format | Inline `422 INVALID_PIN_FORMAT` error |
| Step-up expired mid-form | Prompt re-elevation via `StepUpModal` before allowing resubmission |
| Reset succeeds | Confirmation state, no automatic navigation away (parent may want to review Account & Security further) |

## 19. Offline First
Not applicable — mutating actions require connectivity.

## 20. Local Data
No PIN value ever persisted client-side beyond the active form submission; discarded from memory immediately after the request completes, mirroring A.1 B-04's own server-side discipline.

## 21. Localization
Full EN/HI/AR/UR localization; language preference selector itself is the localization control for the rest of the portal.

## 22. RTL
Full RTL layout for forms and selector.

## 23. Analytics
`web_account_security_viewed`, `web_password_pin_reset_initiated` (§1.19), tagged `client_surface: web_portal`.

## 24. Performance
Standard form-interaction performance; no special optimization required for this low-traffic screen.

## 25. Security
- PIN value never logged client-side (mirrors A.1 B-04's server-side "never logged in plaintext" discipline) — enforced by code review, no `console.log`/analytics call anywhere near the raw PIN field value.
- Step-up gate is mandatory before reset submission is even enabled in the UI (defense-in-depth alongside the server's own `require_elevated_session` enforcement).

## 26. Library Requirements
No new libraries beyond N-02's established stack.

## 27. Testing
- Integration: PIN reset blocked until `StepUpModal` elevation succeeds.
- Integration: invalid PIN format shows inline error, does not submit.
- Integration: successful reset shows confirmation state.
- Unit: no raw PIN value appears in any logged output (log-inspection test, mirroring A.1 B-04's own equivalent test).
- Integration: language preference change updates the portal's active locale immediately.

## 28. Documentation
Document the confirmed PIN-reset and language-preference endpoint ownership (Task 01/02 outcomes) so future maintainers don't re-derive this investigation.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm `POST /v1/identity/auth/pin` Is Reachable From This Origin (blocking)**
- **Objective:** Verify this endpoint is (or will be) included in B-01/B-02's allowlist for `account.noorheroes.com`.
- **Definition of Done:** Confirmed and added to the allowlist if missing.

**Task 02 — Confirm Language-Preference Endpoint Ownership**
- **Objective:** Identify the authoritative parent-facing language-preference endpoint (A.1 vs. C.26 B-04 vs. another owner).
- **Definition of Done:** Confirmed endpoint documented and allowlisted.

**Task 03 — Build `account-security-client.ts`**
- **Dependencies:** Tasks 01–02.

**Task 04 — Build Profile Edit, PIN Reset, and Language Selector Components**
- **Files to Create:** `page.tsx`, `pin-reset-form.tsx`, `language-preference-selector.tsx`.

**Task 05 — Wire `StepUpModal` Gate on Reset**

**Task 06 — Error/Success States, Localization, RTL, Analytics**

**Task 07 — Full Test Suite**

## 30. Definition of Done
A parent can review and edit their account profile, reset their password/PIN (reusing A.1 B-04's exact credential, step-up gated), and change their language preference from the web portal — with both endpoint-ownership questions resolved in writing before implementation.

## 31. Final Verification Checklist
- [ ] `POST /v1/identity/auth/pin` confirmed reachable from this origin (Task 01)
- [ ] Language-preference endpoint ownership confirmed (Task 02)
- [ ] PIN reset gated behind `StepUpModal` before submission is enabled
- [ ] No raw PIN value ever logged client-side
- [ ] Full localization and RTL verified

---
**Figma flagged, not guessed:** No dedicated Figma screen prompt is provided in PRD §2.5 for Account & Security — only Subscription & Invoices and Deletion Status/Countdown have explicit image-generation prompts. Request an Account & Security mockup from design before finalizing this screen's visual implementation; do not invent layout details beyond the composite wireframe description in §2.4.
