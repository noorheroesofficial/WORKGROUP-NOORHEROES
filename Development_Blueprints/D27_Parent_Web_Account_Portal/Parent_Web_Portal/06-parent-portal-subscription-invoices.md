# N-06 — Parent Web Portal Subscription & Invoices

## 1. Feature Context
Part of Feature D.27 — Parent Web Account Portal. The screen carrying this document's single highest-priority store-policy guarantee: a parent can review billing and cancel, but no path anywhere on this screen can initiate a purchase.

## 2. Parent Feature
D.27 Parent Web Account Portal (`account.noorheroes.com`)

## 3. Sub-feature
**N-06 — Parent Web Portal Subscription & Invoices**

## 4. Objective
Build the Subscription & Invoices screen against C.24 B-05's existing parent subscription/cancellation/invoice contract, with zero purchase-initiation UI anywhere, and a "Manage on Mobile App" guidance card replacing where an upgrade/restore action would otherwise appear.

## 5. Business Requirements
- FR-2: zero-exception rule — no purchase-initiation UI anywhere on this screen.
- FR-8: current plan, entitlements, invoice history, cancellation (access continues until period end per C.24's lifecycle rules), restore-purchase guidance directing to mobile.
- §2.2 Screen-Level Design: "Current plan/entitlement summary, invoice list with download links, 'Cancel Subscription' action (step-up gated), and a 'Manage on Mobile App' guidance card replacing where an upgrade/purchase button would otherwise be."
- §1.12 Empty States: "Zero invoices yet (new subscriber) → friendly 'Your invoices will appear here' framing."
- §7 Frontend AI Code-Generation Prompt item 3: UI test scanning this screen for any purchase-initiating button/link.

## 6. Existing Architecture
C.24 B-05 ("Parent Subscription Status, Invoice History & Cancellation API") is confirmed, fully investigated, and matches the PRD's intent closely: `GET /v1/parent/subscription`, `POST /v1/parent/subscription/cancel`, `GET /v1/parent/subscription/invoices/{invoice_id}`. One confirmed exclusion: C.24 B-05 also implements `POST /v1/parent/subscription/restore` (store-receipt re-validation) — this endpoint exists but **must never be allowlisted for the web origin** (B-01), since restore-purchase is "inherently a mobile-OS-billing-API action" (FR-8) requiring a native store receipt the web client cannot produce. This screen calls `GET`/`cancel`/invoice-detail only.

## 7. Existing Code to Reuse
- C.24 B-05's `GET /v1/parent/subscription`, `POST /v1/parent/subscription/cancel`, `GET /v1/parent/subscription/invoices/{invoice_id}` — consumed unmodified.
- N-02's `apiClient`, `StepUpModal`, `ManageOnMobileCard`.

## 8. Files to Create
- `noorheroes-account-portal/src/app/(portal)/subscription/page.tsx`
- `noorheroes-account-portal/src/app/(portal)/subscription/invoices/[invoiceId]/page.tsx`
- `noorheroes-account-portal/src/features/subscription/api/subscription-client.ts`
- `noorheroes-account-portal/src/features/subscription/components/cancellation-confirmation.tsx`
- `noorheroes-account-portal/tests/features/subscription/no-purchase-ui.test.tsx`

## 9. Files to Modify
- N-02's `allowed-endpoints.ts` — register `GET /v1/parent/subscription`, `POST /v1/parent/subscription/cancel`, `GET /v1/parent/subscription/invoices/{invoice_id}` **only** — `restore` is deliberately never added here.

## 10. Backend Requirements
Consumes C.24 B-05 exclusively, excluding its `restore` endpoint by design.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Current plan/entitlement summary (`plan`, `state`, `renewal_date`, `child_capacity`, `active_child_count` from C.24 B-05's response).
- Invoice list (from the same response's `invoices` array) with links to Invoice Detail (`GET /v1/parent/subscription/invoices/{invoice_id}`).
- "Cancel Subscription" action, `StepUpModal`-gated, calling `POST /v1/parent/subscription/cancel`; on success show `access_until` from the response verbatim (never recompute client-side).
- `ManageOnMobileCard` rendered in place of any upgrade/purchase/restore action — the component itself structurally has no click-through to a purchase flow (per N-02's build).
- Restore-Purchase Guidance screen variant: static content directing to the mobile app, no interactive purchase element.
- Empty state: "Your invoices will appear here" for zero invoices.
- States: Default, Loading, Cancellation-confirming, Cancellation-confirmed (§2.2).
- Fire `web_subscription_viewed`, `web_invoice_viewed`, `web_cancellation_initiated`, `web_cancellation_completed`, `web_restore_purchase_guidance_shown`.

## 13. API Contract
Consumes C.24 B-05's contract exactly as documented in that blueprint (`GET /v1/parent/subscription`, `POST /v1/parent/subscription/cancel`, `GET /v1/parent/subscription/invoices/{invoice_id}`); `POST /v1/parent/subscription/restore` and `POST /api/v1/billing/subscribe` are explicitly and permanently excluded from this screen's `apiClient` calls.

## 14. Database Requirements
Not applicable (frontend).

## 15. Validation
`invoice_id` route param passed through to the API; ownership validated server-side (C.24 B-05 §15).

## 16. Authentication
Requires active `SessionContext`.

## 17. Authorization
Cancellation requires fresh `StepUpModal` elevation (FR-3); invoice detail requires only an active session (read-only, family-scoped server-side).

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Zero invoices | "Your invoices will appear here" empty state |
| Cancel attempted on non-cancelable state (`409`) | Inline error, no confirmation state shown |
| Invoice not found/not owned (`404`) | Standard not-found handling, no data leakage |
| Cancellation succeeds | `access_until` displayed verbatim from server response |

## 19. Offline First
Not applicable — mutating actions require connectivity.

## 20. Local Data
Not applicable beyond N-02's in-memory session state.

## 21. Localization
Full EN/HI/AR/UR localization; currency/date formatting via the shared design-token package's formatters (mirrors `noorheroes-admin`'s `useFormatters()`/`CurrencyText` pattern per `NEXT-JS-INSTRUCTIONS.md` §5/§8, replicated in this new codebase).

## 22. RTL
Full RTL layout, including invoice list and currency formatting mirroring.

## 23. Analytics
`web_subscription_viewed`, `web_invoice_viewed`, `web_cancellation_initiated`, `web_cancellation_completed`, `web_restore_purchase_guidance_shown` (§1.19).

## 24. Performance
Standard screen-load performance; invoice list is typically small (no pagination specified in C.24 B-05's response shape — confirm whether large invoice histories require pagination before assuming the full list is always returned).

## 25. Security
- **The single most business-critical guarantee in this entire D.27 document:** this screen must contain zero purchase-initiating UI, verified structurally (no such component exists in the codebase) and by the negative UI test in Task 05.
- `ManageOnMobileCard`'s reuse from N-02 ensures this guarantee is enforced by a shared, previously-tested component rather than a per-screen reimplementation that could drift.
- `POST /api/v1/billing/subscribe` and `POST /v1/parent/subscription/restore` never appear in this screen's `apiClient` calls, backed by B-01/B-02's gateway/middleware rejection as a second and third layer even if a frontend bug somehow attempted it.

## 26. Library Requirements
No new libraries beyond N-02's established stack.

## 27. Testing
- Integration: subscription summary renders correctly from fixture data.
- Integration: cancellation flow requires `StepUpModal` elevation before the cancel call fires.
- Integration: cancellation success displays server-provided `access_until` unmodified.
- Integration: empty invoices state renders "Your invoices will appear here."
- **Negative test (highest priority, §7 item 3):** scan this screen's entire rendered output and component tree for any purchase-initiating button/link/form — must find none, under any state.
- Integration: confirm `POST /v1/parent/subscription/restore` and `POST /api/v1/billing/subscribe` are never present as callable functions in this screen's feature directory (mirrors N-02's global `apiClient` scope test, applied specifically here).

## 28. Documentation
Document explicitly, in code comments on the Subscription page, that `restore` is a deliberately excluded endpoint — not a missing feature, so a future contributor doesn't "helpfully" add a restore button.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Build `subscription-client.ts` (Restore Excluded by Design)**
- **Files to Create:** `subscription-client.ts`.
- **Implementation Details:** Only `getSubscription()`, `cancelSubscription()`, `getInvoiceDetail()` — no `restorePurchase()` function exists in this module.

**Task 02 — Build Subscription Summary and Invoice List**
- **Files to Create:** `page.tsx`.

**Task 03 — Build Invoice Detail Page**
- **Files to Create:** `[invoiceId]/page.tsx`.

**Task 04 — Build Cancellation Flow with Step-Up Gate**
- **Files to Create:** `cancellation-confirmation.tsx`.

**Task 05 — Write the No-Purchase-UI Negative Test (highest priority)**
- **Files to Create:** `no-purchase-ui.test.tsx`.

**Task 06 — Build `ManageOnMobileCard` Integration and Restore-Guidance Variant**

**Task 07 — Localization, RTL, Analytics, Full Test Suite**

## 30. Definition of Done
A parent can review their subscription, invoices, and cancel from the web portal with access preserved until period end — with a structurally, testably zero-purchase-initiation guarantee holding across every state this screen can render.

## 31. Final Verification Checklist
- [ ] No purchase-initiating UI exists anywhere on this screen (negative test passes)
- [ ] `restore` and `billing/subscribe` are never callable from this screen's `apiClient` module
- [ ] Cancellation gated behind fresh step-up elevation
- [ ] `access_until` displayed verbatim from server response, never recomputed client-side
- [ ] Empty invoices state uses the specified friendly framing
- [ ] Full localization and RTL verified
