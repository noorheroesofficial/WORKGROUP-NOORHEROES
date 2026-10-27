# N-04 — Unmasked Full-PII View & Unmask-Active Banner

## 1. Feature Context
The time-boxed "grant is active" rendering variant of N-01/N-02, plus a persistent, unmissable banner reminding the operator exactly how much time remains — both driven entirely by the server's response shape, never a client-side timer guessing at expiry.

## 2. Parent Feature
E.32 — User Management & Child Safety View

## 3. Sub-feature
2.4 Unmasked Full-PII View & Unmask-Active Banner (ID: **N-04**)

## 4. Objective
Build the `UnmaskActiveBanner` (shown globally under an active grant) and confirm N-01/N-02's `MaskedField` correctly renders real values when the server response contains them, with automatic revert-to-masked the moment the server stops returning genuine data.

## 5. Business Requirements
- Under an active unmask grant, every screen shows a persistent banner: remaining time, justification, and the scope it applies to.
- The unmasked rendering itself is not a separate component from `MaskedField` — it is the same component, rendering whatever the server sends (real value vs. placeholder), reinforcing that the client never independently decides.
- The banner's countdown is cosmetic only — it is refreshed from the server's `expires_at` on each poll/reload, never a purely client-side timer that could drift out of sync with the actual backend expiry.
- The moment a request (post-expiry) returns masked data again, the banner disappears and fields revert — no separate "re-mask" action.

## 6. Existing Architecture
`src/features/unmask-active-banner/` module, a cross-cutting component mounted in `dashboard-shell.tsx`, polling/reading grant state from B-02's masking-aware responses (no dedicated "is a grant active" endpoint needed — inferred from whether the current screen's data came back unmasked, confirmed against B-03's grant detail if a global check is required).

## 7. Existing Code to Reuse
- N-01's `MaskedField` (this sub-feature verifies and extends its unmasked-rendering path, does not rebuild it)
- `src/shared/components/dashboard-shell.tsx` (banner mount point)

## 8. Files to Create
- `src/features/unmask-active-banner/components/unmask-active-banner.tsx`
- `src/features/unmask-active-banner/hooks/use-active-grant-status.ts` — polls/derives active-grant state from server-sourced data only
- `src/features/unmask-active-banner/types/active-grant.ts` — Zod schema

## 9. Files to Modify
- `src/shared/components/dashboard-shell.tsx` — mount `UnmaskActiveBanner` globally
- `src/features/parent-account-detail/components/masked-field.tsx` (N-01) — confirm/extend to handle the unmasked-render branch cleanly (still zero independent logic — purely rendering whichever value the server response contains)

## 10. NextJS Requirements
- `useActiveGrantStatus`: derives "is there an active grant, and how much time remains" strictly from the server's grant-detail response (`expires_at`), refetched on interval and on navigation — never computed by a client-only `setInterval` counting down from a value cached at mount time without re-verification.
- `UnmaskActiveBanner`: renders only when `useActiveGrantStatus` confirms an active grant server-side; disappears the instant the server confirms expiry — the banner's absence and `MaskedField`'s reversion to placeholders happen for the same underlying reason (server state changed), never independently.

## 11. Required API
**Admin API** — B-03: `GET /v1/admin/unmask-requests/{id}` (grant detail, including `expires_at`), reused for status polling.

## 12. Authentication / Authorization
`useAdminSession()` base auth; visible to any `support`+ admin who currently holds an active grant.

## 13. Loading / Empty / Error States
No grant: banner absent (this is the default, not an error/empty state to render). Poll failure: banner shows a "status unknown, re-verifying" transient state rather than assuming the grant is still active on a failed check (fail-closed, matching the platform's masking-by-default philosophy).

## 14. Responsive UI / Accessibility
Banner uses `role="status"` for screen-reader announcement of remaining time changes at reasonable intervals (not on every second-tick, to avoid announcement spam).

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()` for the countdown display.

## 16. Security
Fail-closed poll-failure handling is this component's key guarantee — mandatory test confirms that a failed status check never causes the banner (or `MaskedField`'s unmasked rendering) to remain in an active-looking state past its last-confirmed `expires_at`.

## 17. Testing
Unit: `useActiveGrantStatus` fail-closed derivation on poll failure. UI: **mandatory** — banner disappears and `MaskedField` reverts to placeholders within one poll cycle after the server begins returning masked data; **mandatory** — a failed status poll does not extend or preserve an active-looking banner state. Integration: full grant-created → banner-appears → grant-expires → banner-disappears-and-fields-remask flow.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `active-grant.ts` schema. Files: `types/active-grant.ts`, `api-endpoints.ts` (reuse existing B-03 entries). Tests: schema validation. Definition of Done: schema used by Task 02.

**Task 02 — Implement `useActiveGrantStatus`**
Objective: Server-polled, fail-closed active-grant derivation. Files: `hooks/use-active-grant-status.ts`. Dependencies: Task 01. Tests: **mandatory** — fail-closed-on-poll-failure test. Definition of Done: test passes.

**Task 03 — Implement `UnmaskActiveBanner`**
Objective: Persistent banner reflecting server-sourced grant state. Dependencies: Task 02. Tests: appearance/disappearance tests tied to server state changes. Definition of Done: tests pass.

**Task 04 — Verify/Extend `MaskedField`'s Unmasked-Render Path**
Objective: Confirm zero independent logic exists for the unmasked branch — purely renders server value. Dependencies: N-01. Tests: **mandatory** — unmasked-fixture-renders-real-value, then masked-fixture-reverts-immediately test. Definition of Done: test passes.

**Task 05 — Mount Globally in Dashboard Shell**
Objective: Banner visible across all screens under an active grant. Dependencies: Task 03. Tests: cross-screen-persistence smoke test. Definition of Done: test passes.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §17, both mandatory tests included. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm no client-only timer exists anywhere that could keep the banner or unmasked rendering alive past actual server-side expiry. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Banner and `MaskedField` unmasked rendering are both driven exclusively by server response state — mandatory tests passing
- [ ] Poll failure fails closed (never preserves an active-looking state) — mandatory test passing
- [ ] Banner disappears within one poll cycle of the server reverting to masked
- [ ] Countdown display re-verifies against server `expires_at`, never a pure client-side timer

## 20. Definition of Done
The unmasked-viewing experience and its persistent time-remaining banner are both provably and exclusively driven by server-confirmed grant state, with fail-closed behavior on any uncertainty — completing the UI-layer reinforcement of B-02's and B-03's backend guarantees.
