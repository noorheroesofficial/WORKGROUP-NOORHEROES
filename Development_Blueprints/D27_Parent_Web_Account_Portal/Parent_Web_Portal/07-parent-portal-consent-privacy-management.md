# N-07 — Parent Web Portal Consent & Privacy Management

## 1. Feature Context
Part of Feature D.27 — Parent Web Account Portal. The Consent & Privacy screen: the same synthesized 6-item Consent Log C.26 B-01 already exposes to the Mobile App, rendered as a second client against the identical backend contract.

## 2. Parent Feature
D.27 Parent Web Account Portal (`account.noorheroes.com`)

## 3. Sub-feature
**N-07 — Parent Web Portal Consent & Privacy Management**

## 4. Objective
Build the Consent & Privacy and Consent Detail screens against C.26 B-01's existing consent-log/withdrawal contract, correctly handling required-vs-optional consent semantics and the endpoint-shape correction found during investigation.

## 5. Business Requirements
- FR-9: "Consent & Privacy screen: the same Consent Log content and withdraw/re-grant actions specified in C.26, rendered as a second client against the identical backend contract."
- C.26 FR-8 (inherited): required consents (terms, privacy, child_data) cannot be withdrawn — attempting to do so routes to the account-deletion path, not a toggle.
- C.26 Edge Case 1 (inherited): re-granting a withdrawn optional consent creates a new ledger entry, never an "undelete."

## 6. Existing Architecture — Path Correction Flagged
PRD §3.4 lists `GET/PATCH /v1/parent/consents`. Investigation of C.26 B-01 ("Consent Log & Withdrawal API") shows the actual, implemented contract is `GET /v1/parent/consents` (synthesized 6-item list from A.1's append-only consent snapshot) and `POST /v1/parent/consents/{id}/withdraw` — **there is no `PATCH /v1/parent/consents` endpoint**; withdrawal is a dedicated `POST .../withdraw` action, and re-granting an optional consent (per C.26 Edge Case 1) is a separate concern not yet confirmed to have its own endpoint distinct from withdrawal (C.26 B-01's own text describes withdrawal only — "re-granting... creates a new ledger entry" is stated as the *effect* but the exact re-grant endpoint/mechanism is not fully specified in the excerpt reviewed). This screen's `apiClient` must be built against the confirmed `GET`/`POST .../withdraw` shape, and Task 01 must confirm the re-grant mechanism before that action is exposed in the UI.

## 7. Existing Code to Reuse
- C.26 B-01's `GET /v1/parent/consents`, `POST /v1/parent/consents/{id}/withdraw` — consumed unmodified.
- The `id` values are the fixed, code-defined strings C.26 B-01 established (`"terms"`, `"privacy"`, `"child_data"`, `"personalization"`, `"voice_ai"`, `"marketing"`) — this screen must use these exact identifiers, not invent its own.
- N-02's `apiClient`, `StepUpModal`.

## 8. Files to Create
- `noorheroes-account-portal/src/app/(portal)/consent/page.tsx`
- `noorheroes-account-portal/src/app/(portal)/consent/[consentId]/page.tsx`
- `noorheroes-account-portal/src/features/consent/api/consent-client.ts`
- `noorheroes-account-portal/src/features/consent/components/withdraw-confirmation-modal.tsx`
- `noorheroes-account-portal/tests/features/consent/required-consent-guard.test.tsx`

## 9. Files to Modify
- N-02's `allowed-endpoints.ts` — register the corrected `GET /v1/parent/consents`, `POST /v1/parent/consents/{id}/withdraw` paths (not the PRD's `PATCH` shorthand).

## 10. Backend Requirements
Consumes C.26 B-01 exclusively, at its actual (corrected) contract shape.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Consent & Privacy screen: 6-item list (3 required, 3 optional), each showing current status and `last_changed_at`.
- Consent Detail screen per item.
- Withdraw action available only on the 3 optional items — required-consent items must not render a withdraw control at all (not merely a disabled one), matching C.26 B-01's server-side hard rejection with a consistent frontend affordance.
- Withdraw Confirmation modal, `StepUpModal`-gated.
- "Required-consent redirect" (shared logic per §2.3 Tab Structure): if a required-consent withdrawal is somehow attempted (defensive coding only, since the UI shouldn't offer it), redirect to the account-deletion entry point (N-09) rather than showing a generic error, mirroring C.26's own stated behavior.
- Fire `web_consent_viewed`, `web_consent_withdrawn`.

## 13. API Contract
Consumes C.26 B-01's contract exactly as documented in that blueprint, at the corrected paths per §6.

## 14. Database Requirements
Not applicable (frontend).

## 15. Validation
`consentId` route param must be one of the 6 fixed, code-defined identifiers — any other value is a client-side routing error (404), never forwarded to the API as an arbitrary string.

## 16. Authentication
Requires active `SessionContext`.

## 17. Authorization
Withdrawal requires fresh `StepUpModal` elevation (FR-3).

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Attempted withdrawal of a required consent (defensive path) | Redirect to account-deletion entry point (N-09), not a generic error |
| Withdrawal succeeds | List updates to reflect new status |
| Consent snapshot fetch fails | `ErrorView`-equivalent with retry |

## 19. Offline First
Not applicable — mutating actions require connectivity.

## 20. Local Data
Not applicable beyond N-02's in-memory session state.

## 21. Localization
Full EN/HI/AR/UR localization of all 6 consent items' display names and descriptions, sourced from the same localization keys the Mobile App uses (never a second, independently-maintained copy of consent display text).

## 22. RTL
Full RTL layout.

## 23. Analytics
`web_consent_viewed`, `web_consent_withdrawn` (§1.19).

## 24. Performance
Trivial — single small list fetch, no pagination needed for a fixed 6-item list.

## 25. Security
- Required-consent items must never expose a withdraw control in the UI, matching C.26 B-01's server-side hard rejection — defense-in-depth between UI affordance and server enforcement.
- The fixed, shared `id` string set (not database primary keys) must be used exactly as C.26 B-01 defines them — inventing new identifiers here would break cross-surface consistency with the Mobile App's identical screen.

## 26. Library Requirements
No new libraries beyond N-02's established stack.

## 27. Testing
- Integration: 6-item list renders correctly with required/optional distinction visible.
- Integration: required-consent items render no withdraw control.
- Integration: withdrawal requires `StepUpModal` elevation before the call fires.
- Integration: withdrawal success updates the displayed status.
- Regression: this screen's data matches the Mobile App's equivalent screen when queried against the same family (cross-surface consistency, mirroring D.27's core architectural promise).

## 28. Documentation
Document the path-correction finding (§6) so a future maintainer building against the PRD's literal `PATCH` reference doesn't introduce a nonexistent endpoint call.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm the Re-Grant Mechanism**
- **Objective:** Determine whether re-granting a withdrawn optional consent uses a dedicated endpoint or reuses `POST .../withdraw`-equivalent semantics in reverse, per C.26 B-01 Edge Case 1.
- **Definition of Done:** Confirmed mechanism, documented before Task 04.

**Task 02 — Build `consent-client.ts` at the Corrected Contract Shape**
- **Files to Create:** `consent-client.ts`.

**Task 03 — Build Consent & Privacy List and Detail Screens**
- **Files to Create:** `page.tsx`, `[consentId]/page.tsx`.

**Task 04 — Build Withdraw (and, if confirmed, Re-Grant) Flow with Step-Up Gate**
- **Files to Create:** `withdraw-confirmation-modal.tsx`.
- **Dependencies:** Task 01.

**Task 05 — Required-Consent Guard Test**
- **Files to Create:** `required-consent-guard.test.tsx`.

**Task 06 — Localization, RTL, Analytics, Full Test Suite**

## 30. Definition of Done
A parent can review all 6 consent items and withdraw any optional one from the web portal, reading and writing through C.26 B-01's exact existing contract — with the PRD's `PATCH` reference corrected to the actual `GET`/`POST .../withdraw` shape, and the required-consent-cannot-withdraw rule enforced at both the UI-affordance and server level.

## 31. Final Verification Checklist
- [ ] Corrected `GET`/`POST .../withdraw` paths used (not the PRD's `PATCH` shorthand)
- [ ] Required-consent items render no withdraw control
- [ ] Re-grant mechanism confirmed (Task 01) before implementation
- [ ] Withdrawal gated behind fresh step-up elevation
- [ ] Fixed, shared `id` identifiers used exactly as C.26 B-01 defines them
- [ ] Full localization and RTL verified
