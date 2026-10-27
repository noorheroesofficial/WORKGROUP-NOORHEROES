# N-05 — Parent Web Portal Devices & Sessions Management

## 1. Feature Context
Part of Feature D.27 — Parent Web Account Portal. The Devices and Sessions screen: lists active devices and lets a parent revoke any of them, force-logging out that session. This sub-feature carries the most significant open architecture question in the entire D.27 breakdown — flagged here, not silently resolved.

## 2. Parent Feature
D.27 Parent Web Account Portal (`account.noorheroes.com`)

## 3. Sub-feature
**N-05 — Parent Web Portal Devices & Sessions Management**

## 4. Objective
Build the Devices & Sessions screen against a confirmed, correctly-scoped backend session-list/revocation contract — resolving, before implementation, whether that contract is C.23 B-06's existing child-mode-session mechanism or a distinct, not-yet-built parent-account-session mechanism.

## 5. Business Requirements
- FR-7: "Devices and Sessions screen: lists active sessions/devices (reusing C.19's exact session-list/revocation contract), supports revocation with the same immediate force-logout effect specified there."
- §1.18 Screens #5–6: Devices and Sessions, Device Revocation Confirmation (step-up gated modal).
- Edge Case 2: "A parent revokes a mobile device from the web portal's Devices screen while actively using that exact device → the mobile session is force-logged-out immediately... a deliberate, expected consequence, not a bug."
- §1.12 Empty States: "Zero devices listed → friendly 'No devices found yet' framing."

## 6. Existing Architecture — Blocking Gap, Flagged Not Guessed
This is the single most consequential open question carried from B-01 into this screen. Investigation of the reviewed backend blueprints shows:

1. `GET /v1/sessions` / `DELETE /v1/sessions/{id}` is implemented by **C.23 B-06** ("Active Device Sessions & Revocation API"), explicitly scoped to **child-mode device sessions** — "return all active (non-revoked) sessions across all children in the family," issued at the moment C.19 B-04's `SessionActivationService.activate()` mints a **child-mode** `session_token` via `POST /v1/sessions/child-mode`. Its response shape is `{ sessions: [{ session_id, child_id, device_name, last_active_at }] }` — every listed session is explicitly tied to a `child_id`.
2. FR-7's premise — a parent reviewing and revoking their **own** browser/login sessions/devices for account-security purposes (the standard "manage your logged-in devices" pattern found in most account-security UIs, and the only sensible reading of a **web portal's** own "Devices and Sessions" screen, since a parent is not going to browse the web portal *as* a child-mode session) — does not correspond to any endpoint found in the reviewed backend. There is no `parent_session`/`ParentSessionOrm` equivalent to C.23 B-06's `DeviceSessionOrm`; `ParentSessionContext` (`core/deps.py`) is a per-request JWT-derived DTO, not a persisted, listable record.

**This is a genuine backend gap, not a frontend implementation detail.** Building N-05 against `GET/DELETE /v1/sessions` as literally specified would render **child-mode device sessions** on a screen the PRD, its own Edge Case 2, and ordinary product sense all describe as the *parent's own* login-session list — a potentially serious, user-facing correctness bug (and arguably a privacy/trust issue: a "your devices" screen showing someone else's — the children's — session data). This must be resolved before any frontend code is written against this screen.

```
Existing Architecture
   → GET/DELETE /v1/sessions (C.23 B-06) lists/revokes child-mode device
     sessions only, keyed by child_id
        ↓
Problem
   → FR-7 assumes a parent-own-session list/revoke contract that does not
     exist; reusing C.23 B-06 literally would show child sessions on a
     parent "Devices and Sessions" screen
        ↓
Proposed Improvement (requires product/architecture decision — Task 01)
   Option A: Build a net-new `parent_session` listing/revocation
     mechanism, structurally parallel to C.23 B-06 but scoped to the
     parent's own authenticated sessions (mobile app logins + web portal
     logins), reusing C.23 B-06's Redis revocation-denylist pattern and
     `jti`-claim approach rather than inventing a second one.
   Option B: If "Devices and Sessions" in the PRD's intent is actually
     about reviewing/revoking children's active devices (a parental-
     controls concern, not an account-security one), then C.23 B-06 is
     the correct contract after all, and this screen's framing/copy
     should be corrected to say so explicitly rather than implying
     parent-own-session management.
        ↓
Impact
   → Option A is materially new backend scope (a B-05-equivalent sub-
     feature, not yet in this document's Backend section); Option B
     requires no new backend work but changes this screen's product
     framing and its Figma requirements.
        ↓
Implementation
   → Blocked on Task 01's resolution; this file's remaining sections
     assume Option A (parent-own-session, the PRD's evident intent) as
     the working hypothesis, but implementation must not proceed past
     Task 01 without written confirmation.
        ↓
Documentation Update
   → B-01's allowlist entry for "GET/DELETE /v1/sessions" must be
     corrected once resolved — either pointing at a new parent-session
     endpoint path, or explicitly re-confirmed as C.23 B-06's existing
     path with this screen's framing corrected instead.
```

## 7. Existing Code to Reuse
- **If Option A:** C.23 B-06's Redis revocation-denylist pattern (`session_revocation.py`'s `add_to_denylist()`/`is_revoked()`), `jti`-claim approach, and `device_sessions`-equivalent table structure — reused as an architectural pattern for a new, parallel `parent_session` mechanism, not duplicated logic inside the same table (parent and child sessions should not share one ambiguous table).
- **If Option B:** C.23 B-06's contract directly, unmodified.
- N-02's `apiClient`, `StepUpModal`, `PortalShell`.

## 8. Files to Create
- `noorheroes-account-portal/src/app/(portal)/devices/page.tsx`
- `noorheroes-account-portal/src/features/devices/api/devices-client.ts`
- `noorheroes-account-portal/src/features/devices/components/device-revocation-confirmation-modal.tsx`
- `noorheroes-account-portal/tests/features/devices/device-revocation.test.tsx`

## 9. Files to Modify
- N-02's `allowed-endpoints.ts` — register the confirmed (Option A or B) session-list/revoke endpoint.

## 10. Backend Requirements
Pending Task 01's resolution: either a new parent-session backend sub-feature (Option A, not yet specified in this document and requiring its own blueprint before N-05 can be fully implemented) or C.23 B-06 directly (Option B). This file does not fabricate a backend contract for Option A beyond noting its likely shape (mirroring C.23 B-06's, scoped to `parent_id` instead of `child_id`).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Devices & Sessions screen: table/list of active sessions (`device_name`, `last_active_at`), Revoke action per row.
- Device Revocation Confirmation modal, `StepUpModal`-gated before the revoke call fires.
- Empty state: "No devices found yet" (§1.12).
- Loading/error states.
- Fire `web_devices_viewed` on screen view, `web_device_revoked` on successful revocation.
- **This screen must not render any `child_id`-associated data under any circumstance** — if Task 01 resolves to Option B (C.23 B-06's actual contract), this screen's entire premise needs product re-scoping before any UI is built, per FR-4's structural exclusion of child-scoped data from this portal entirely; rendering child-mode session data here would itself be a violation of D.27's core architectural guarantee.

## 13. API Contract
Pending Task 01. If Option A, mirrors C.23 B-06's shape scoped to `parent_id`: `GET /v1/parent/sessions` → `{ sessions: [{ session_id, device_name, last_active_at, client_surface }] }`; `DELETE /v1/parent/sessions/{id}`.

## 14. Database Requirements
Not applicable (frontend) — backend schema questions belong to the eventual Option A backend sub-feature.

## 15. Validation
Not applicable beyond standard revoke-confirmation UX.

## 16. Authentication
Requires active `SessionContext`.

## 17. Authorization
Revocation requires fresh `StepUpModal` elevation (FR-3, per §2.3 Tab Structure).

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Zero devices | "No devices found yet" empty state |
| Revoke fails (network/server error) | Inline error, list unchanged |
| Revoke succeeds | List updates immediately, revoked device removed |
| Parent revokes the session they're currently using | Expected — that session force-logs-out on its next request (Edge Case 2); this screen does not need special handling for "don't let me revoke myself," since immediate self-revocation is explicitly the intended, deliberate behavior |

## 19. Offline First
Not applicable — mutating actions require connectivity.

## 20. Local Data
Not applicable beyond N-02's in-memory session state.

## 21. Localization
Full EN/HI/AR/UR localization; `last_active_at` formatted client-side per active locale.

## 22. RTL
Full RTL layout for the device list and confirmation modal.

## 23. Analytics
`web_devices_viewed`, `web_device_revoked` (§1.19).

## 24. Performance
Low-volume, parent-initiated list; no special optimization required.

## 25. Security
- This screen's single most important property is that it never, under any resolution of Task 01, renders child-scoped session data — a direct instance of D.27's core structural exclusion (FR-4), independent of and in addition to the backend gateway/middleware guarantees (B-01/B-02).
- Revocation gated behind fresh step-up, consistent with every other sensitive action in this portal.

## 26. Library Requirements
No new libraries beyond N-02's established stack.

## 27. Testing
- Integration: empty state renders correctly with zero devices.
- Integration: revoke flow requires `StepUpModal` elevation before the DELETE call fires.
- Integration: revoked device disappears from the list on success.
- **Negative test (highest priority):** no rendered device row or underlying API response ever includes a `child_id` field — if Task 01 resolves to Option B, this test should fail loudly, forcing the scope question to be re-raised rather than silently shipping child-session data on this screen.

## 28. Documentation
Document Task 01's resolution prominently — this is the single most important open decision in the entire D.27 feature, more consequential than any other flagged gap in this document set, because an incorrect resolution risks exposing child-associated data on a parent-facing web surface.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Resolve the Parent-vs-Child Session Contract Question (blocking, highest priority in this entire feature)**
- **Objective:** Obtain written product/architecture confirmation of Option A (new parent-session mechanism) vs. Option B (C.23 B-06 directly, with corrected screen framing) per §6.
- **Why This Is Required:** FR-7's assumption does not match any existing backend contract; the wrong resolution risks child-data exposure on this portal, a zero-tolerance violation per FR-4/NFR Structural Scope Exclusion.
- **Definition of Done:** Written confirmation obtained; this blocks every subsequent task in this file.

**Task 02 — (If Option A) Specify and Build the Parent-Session Backend Sub-Feature**
- **Objective:** A new backend blueprint, structurally parallel to C.23 B-06, scoped to `parent_id`.
- **Dependencies:** Task 01.
- **Note:** This is out of this file's own scope to fully specify; it becomes a new Backend sub-feature (e.g., B-05) once Task 01 resolves to Option A.

**Task 03 — Build `devices-client.ts` Against the Confirmed Contract**
- **Dependencies:** Task 01 (and Task 02 if Option A).

**Task 04 — Build Devices Screen and Revocation Modal**
- **Files to Create:** `page.tsx`, `device-revocation-confirmation-modal.tsx`.

**Task 05 — Write the Child-Data-Absence Negative Test**
- **Files to Create:** `device-revocation.test.tsx`.
- **Definition of Done:** Structurally verifies no `child_id` ever appears in this screen's data or rendering.

**Task 06 — Localization, RTL, Analytics, Full Test Suite**

## 30. Definition of Done
A parent can view and revoke their own account/browser sessions from the web portal — with the underlying session-contract ambiguity (parent-own vs. child-mode) resolved in writing before any implementation proceeded, and a standing negative test guaranteeing no child-scoped data can ever render on this screen regardless of which resolution was chosen.

## 31. Final Verification Checklist
- [ ] Task 01's Option A/B resolution obtained in writing before implementation began
- [ ] If Option A, the new parent-session backend sub-feature is specified and built before this screen ships
- [ ] Negative test confirms no `child_id` ever appears in this screen's data or UI
- [ ] Revocation gated behind fresh `StepUpModal` elevation
- [ ] Empty state and revoke-success/failure states all handled
- [ ] Full localization and RTL verified

---
**Figma flagged, not guessed:** No dedicated Figma prompt is provided in PRD §2.5 for Devices and Sessions — request a mockup from design, and do so only after Task 01 resolves the underlying data-model question, since the correct screen framing depends on that resolution.
