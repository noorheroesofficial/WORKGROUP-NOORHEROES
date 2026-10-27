# N-09 — Parent Web Portal Account Deletion Request & Status

## 1. Feature Context
Part of Feature D.27 — Parent Web Account Portal. The Parent Deletion Request, Deletion Warning, Deletion Confirmation, and Deletion Status/Countdown screens — carrying an inherited, previously-flagged architecture gap: whether a family-level (whole-account) deletion endpoint, distinct from C.21's per-child deletion, actually exists.

## 2. Parent Feature
D.27 Parent Web Account Portal (`account.noorheroes.com`)

## 3. Sub-feature
**N-09 — Parent Web Portal Account Deletion Request & Status**

## 4. Objective
Build the deletion request, warning, confirmation, and status/countdown screens against a confirmed family-level deletion contract — resolving, before implementation, the same "per-child vs. whole-family deletion" ambiguity that C.26's KMP blueprint (K-07) already flagged for the Mobile App, ensuring both surfaces resolve it identically.

## 5. Business Requirements
- FR-11: "a parent may initiate the account-deletion request from the web portal (step-up gated, full warning shown, identical to C.21's mobile flow) and view the countdown status during the grace period; cancellation remains Support-mediated only, with zero self-service cancellation capability on the web either."
- §1.9 Acceptance Criteria: "Given a parent initiates an account-deletion request from the web portal, when they confirm, then the same 7-day grace period, warning copy, and `deletion_pending` state apply exactly as the Mobile App's equivalent flow would produce."
- §2.2 Screen-Level Design, Deletion Status/Countdown: "deliberately no 'Cancel' button anywhere on this screen."
- §7 Frontend AI Code-Generation Prompt item 4: UI test asserting no "Cancel" button exists anywhere on this screen under any state.

## 6. Existing Architecture — Inherited, Confirmed Blocking Gap
This is not a newly discovered gap — it is the **same open question C.26's own KMP blueprint (K-07, "Settings Exit Actions — Logout Guard & Account Deletion Entry Point") already flagged for the Mobile App**, carried into D.27 unchanged:

> "the C.26 PRD describes this entry point as leading to 'C.21's Account Deletion Flow,' but the reviewed C.21 blueprints (B-06/K-05) implement **per-child profile deletion**, not whole-family-account deletion. If C.26's 'Delete Account' is intended as a distinct, family-level action... no such flow currently exists in the reviewed blueprints."

D.27's own §3.4 API List cites `POST /v1/parent/deletion-request`, `GET /v1/parent/deletion-status` as though this family-level contract already exists — but the reviewed C.21 backend blueprints (B-04 "Child Disable & Session Revocation Service," B-06 "Permanent Child Deletion & Audit Trail Service," K-05 "Permanent Deletion Warning & Confirmation Flow") implement only **per-child** deletion, with no whole-account-closure endpoint found anywhere in the reviewed set.

**This ambiguity must be resolved once, consistently, and the resolution must be identical for both the Mobile App (C.26 K-07) and this web screen** — it would be a serious cross-surface inconsistency bug if the Mobile App's "Delete Account" meant "delete all children" while the web portal's meant a genuine whole-family closure, or vice versa.

```
Existing Architecture
   → C.21's reviewed blueprints implement per-child deletion only
   → C.26 KMP K-07 already flagged this exact ambiguity for the Mobile App,
     unresolved as of that blueprint's writing
        ↓
Problem
   → D.27's PRD assumes POST /v1/parent/deletion-request /
     GET /v1/parent/deletion-status exist as family-level endpoints with a
     7-day grace period, deletion_pending state, and delete_after
     timestamp — none of which appear in the reviewed C.21 backend
        ↓
Proposed Improvement (requires product/architecture decision — Task 01,
   shared with C.26 K-07's Task 00, not resolved independently here)
   → If a genuine whole-family-closure flow is intended, it needs its own
     backend sub-feature (net-new, likely under C.21 or a new bounded
     context), a 7-day grace-period job (mirroring the pattern already
     established by C.21's per-child deletion's own grace/purge job, per
     that blueprint's `purge_expired_child_deletions.py` reference found
     during B-03 (C.26)'s investigation), and both this web screen and
     C.26 K-07's mobile entry point must be updated to target it
     consistently
        ↓
Impact
   → Materially new backend scope; blocks N-09 and re-opens C.26 K-07's
     Task 00 as the same, shared question
        ↓
Implementation
   → Blocked on Task 01; this file's remaining sections assume the
     family-level flow is confirmed to exist or will be built (the PRD's
     evident intent, and the only reading consistent with a "7-day
     countdown" framing), but implementation must not proceed past
     Task 01 without written, cross-surface-consistent confirmation
        ↓
Documentation Update
   → C.26 K-07 must be updated/cross-referenced once resolved, so the
     Mobile App and web portal are never resolved independently and
     inconsistently
```

## 7. Existing Code to Reuse
- **If a family-level flow is confirmed/built:** whatever grace-period/purge job pattern C.21's per-child deletion already establishes (reused as an architectural pattern for the family-level equivalent, not duplicated logic).
- N-02's `apiClient`, `StepUpModal`.
- The exact warning copy and 7-day framing, sourced from wherever the confirmed backend flow defines it — this screen must not invent its own warning text independent of the backend/legal-approved copy.

## 8. Files to Create
- `noorheroes-account-portal/src/app/(portal)/delete-account/page.tsx`
- `noorheroes-account-portal/src/app/(portal)/delete-account/warning/page.tsx`
- `noorheroes-account-portal/src/app/(portal)/delete-account/confirm/page.tsx`
- `noorheroes-account-portal/src/app/(portal)/delete-account/status/page.tsx`
- `noorheroes-account-portal/src/features/account-deletion/api/account-deletion-client.ts`
- `noorheroes-account-portal/tests/features/account-deletion/no-cancel-button.test.tsx`

## 9. Files to Modify
- N-02's `allowed-endpoints.ts` — register the confirmed family-level deletion endpoints once they exist.

## 10. Backend Requirements
Pending Task 01's resolution: either a new family-level deletion backend sub-feature (not yet specified in this document's Backend section, and requiring coordination with C.26 K-07's identical open question) or a corrected understanding that "Account Deletion" here means "delete all children via C.21's existing per-child flow," in which case this screen's entire framing (a single "delete my account" action with one 7-day countdown) would need reconsideration against C.21's actual per-child, potentially-staggered deletion model.

## 11. KMP Requirements
Not applicable to this file directly, but this sub-feature's Task 01 is explicitly shared with C.26 K-07's Task 00 — they must not be resolved independently.

## 12. NextJS Requirements
- Parent Deletion Request screen, `StepUpModal`-gated.
- Deletion Warning screen: full warning copy (sourced from the confirmed backend/legal-approved text, not invented here), 7-day framing.
- Deletion Confirmation screen.
- Deletion Status/Countdown screen (shown on subsequent logins during the grace period): countdown showing days remaining, exact warning copy, and a single "Contact Support" action — **deliberately no "Cancel" button anywhere on this screen, under any state**.
- Fire `web_deletion_request_initiated`, `web_deletion_warning_shown`, `web_deletion_confirmed`, `web_deletion_status_viewed_during_grace`.

## 13. API Contract
Pending Task 01. If confirmed as PRD-described: `POST /v1/parent/deletion-request` (step-up gated), `GET /v1/parent/deletion-status` returning `{ deletion_pending: true, delete_after: "..." }` or equivalent.

## 14. Database Requirements
Not applicable (frontend) — backend schema questions belong to the eventual confirmed backend sub-feature.

## 15. Validation
Not applicable beyond standard confirmation-flow UX.

## 16. Authentication
Requires active `SessionContext`.

## 17. Authorization
Deletion request requires fresh `StepUpModal` elevation (FR-3).

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Deletion request fails | Inline error, no state transition to Warning/Confirmation |
| Parent logs in during an active grace period | Deletion Status/Countdown screen shown automatically, per §1.18 screen #19's entry point ("Login during grace period") |
| Parent seeks to cancel | Directed to "Contact Support" only — no self-service cancellation UI exists anywhere, consistent with C.21's platform-wide rule this inherits |

## 19. Offline First
Not applicable — mutating actions require connectivity; the status/countdown display could show last-known state if offline, consistent with N-02's offline banner.

## 20. Local Data
Not applicable beyond N-02's in-memory session state.

## 21. Localization
Full EN/HI/AR/UR localization of the warning copy, countdown text, and confirmation flow — sourced from the same localization keys as the Mobile App's equivalent flow (once Task 01 resolves), never an independently-translated copy that could drift from the mobile version's legal-approved text.

## 22. RTL
Full RTL layout, including the countdown display (numeral direction handled per standard RTL numeric-field convention, as established in N-03).

## 23. Analytics
`web_deletion_request_initiated`, `web_deletion_warning_shown`, `web_deletion_confirmed`, `web_deletion_status_viewed_during_grace` (§1.19).

## 24. Performance
Standard screen-load performance; no special optimization required for this low-frequency flow.

## 25. Security
- **The "no Cancel button anywhere on this screen" guarantee is this sub-feature's most important, most testable property** — verified structurally (no such component exists in the codebase) and by Task 05's negative test, mirroring N-06's equivalent no-purchase-UI discipline.
- Deletion request itself is step-up gated, consistent with every other sensitive action in this portal.
- This screen must never diverge from C.21's/C.26's confirmed rule that cancellation is Support-mediated only — a self-service cancellation button appearing here, even accidentally, would be a platform-wide policy violation.

## 26. Library Requirements
No new libraries beyond N-02's established stack.

## 27. Testing
- Integration: deletion request flow requires `StepUpModal` elevation before the call fires.
- Integration: warning copy matches the confirmed backend/legal-approved text exactly (once Task 01 resolves).
- Integration: logging in during an active grace period automatically shows the Deletion Status/Countdown screen.
- **Negative test (highest priority, §7 item 4):** scan the Deletion Status/Countdown screen's entire rendered output under every reachable state and assert no "Cancel" button/link/form exists anywhere.
- **Cross-surface consistency test:** a deletion request initiated via this screen shows the identical `deletion_pending` state and `delete_after` timestamp as the same request would show via a simulated Mobile App call, once Task 01's backend is confirmed/built (mirrors Edge Case 4).

## 28. Documentation
Document that Task 01 is a **shared, cross-surface decision** with C.26 K-07 — this file and C.26 K-07 must never resolve the per-child-vs-family-level question independently or inconsistently. Update both files' documentation once resolved.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Resolve the Family-Level vs. Per-Child Deletion Scope (blocking, shared with C.26 K-07's Task 00)**
- **Objective:** Obtain written product/architecture confirmation of whether a genuine whole-family-account deletion flow exists/will be built, or whether "Account Deletion" means initiating C.21's existing per-child flow for every child on the account.
- **Why This Is Required:** Both this file and C.26's Mobile App blueprint independently discovered the same gap; resolving them inconsistently would be a serious cross-surface bug.
- **Definition of Done:** Written confirmation obtained, cross-referenced in both this file and C.26 K-07; blocks every subsequent task here.

**Task 02 — (If Confirmed) Specify and Build the Family-Level Deletion Backend Sub-Feature**
- **Objective:** Net-new backend scope, out of this file's ability to fully specify; becomes its own Backend sub-feature once Task 01 resolves affirmatively.
- **Dependencies:** Task 01.

**Task 03 — Build `account-deletion-client.ts` Against the Confirmed Contract**
- **Dependencies:** Tasks 01–02.

**Task 04 — Build Request, Warning, Confirmation, and Status/Countdown Screens**
- **Files to Create:** the four page files listed in §8.

**Task 05 — Write the No-Cancel-Button Negative Test (highest priority)**
- **Files to Create:** `no-cancel-button.test.tsx`.

**Task 06 — Write the Cross-Surface Consistency Test**

**Task 07 — Localization, RTL, Analytics, Full Test Suite**

## 30. Definition of Done
A parent can initiate an account-deletion request from the web portal and view its 7-day grace-period status on subsequent logins, with zero self-service cancellation capability anywhere — and the underlying family-level-vs-per-child scope ambiguity resolved in writing, consistently with C.26 K-07's identical open question, before any implementation proceeded.

## 31. Final Verification Checklist
- [ ] Task 01's scope resolution obtained in writing and is consistent with C.26 K-07's resolution
- [ ] If a new backend sub-feature was required, it is specified and built before this screen ships
- [ ] Deletion request gated behind fresh step-up elevation
- [ ] No "Cancel" button/link/form exists anywhere on the Deletion Status/Countdown screen, under any state (negative test passes)
- [ ] Cross-surface consistency test passes (once backend confirmed)
- [ ] Full localization and RTL verified

---
**Figma:** Deletion Status / Countdown has explicit EN + AR-RTL image-generation prompts in PRD §2.5 — use these as the visual source of truth once Task 01 resolves the underlying data model, since the copy/framing shown in those prompts assumes the resolved flow.
