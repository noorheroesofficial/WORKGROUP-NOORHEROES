# N-03 — Active-Subscription Search & Detail (Billing Timeline)

## 1. Feature Context
The investigation workspace: search, then a chronological billing timeline whose visual treatment — real billing event vs. amber-badged comp grant — is selected entirely from the server's `type` field, with zero client-side string-matching or heuristic guesswork.

## 2. Parent Feature
E.33 — Subscription Management & Billing Ops

## 3. Sub-feature
2.3 Active-Subscription Search & Detail (Billing Timeline) (ID: **N-03**)

## 4. Objective
Build the Subscription Search, Subscription Detail (billing timeline), and Billing Event Detail screens against B-02, with the timeline's visual treatment driven exclusively by each entry's server-provided `type` field.

## 5. Business Requirements
- §1.18 screens 6–8: Active-Subscription Search, Subscription Detail, Billing Event Detail.
- §6.4: the timeline component renders each entry's `type` field directly from the server response to select visual treatment — never inferring type from any other heuristic.
- §7 Frontend AI prompt item 1: no client-side heuristic or string-matching logic is used to determine billing-event vs. comp-grant styling.
- §2.1: comp grants render with a consistent, unmistakable badge ("Comp Grant — Not Real Revenue") everywhere they appear.

## 6. Existing Architecture
`src/features/subscription-search/` module, following the Admin Portal's dense professional-tool register (E.28 §2.1), the billing timeline visually similar in spirit to C.22's Activity Timeline but in the denser Admin Portal register.

## 7. Existing Code to Reuse
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/components/data-table.tsx::DataTable` (search results)
- E.32 N-01's search-screen structural pattern (reused conceptually, not the component itself, given the different domain)

## 8. Files to Create
- `src/app/(dashboard)/commerce/subscriptions/search/page.tsx`
- `src/app/(dashboard)/commerce/subscriptions/[id]/page.tsx`
- `src/app/(dashboard)/commerce/subscriptions/[id]/billing-events/[eventId]/page.tsx`
- `src/features/subscription-search/api/subscription-search-repository.ts`
- `src/features/subscription-search/hooks/use-subscription-search.ts`, `use-subscription-detail.ts`
- `src/features/subscription-search/components/billing-timeline.tsx`
- `src/features/subscription-search/components/billing-event-entry.tsx`
- `src/features/subscription-search/components/comp-grant-entry.tsx` — distinct amber-badge styling
- `src/features/subscription-search/types/subscription-detail.ts` — Zod discriminated-union schema matching B-02's `type` field

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `SUBSCRIPTIONS.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav item under "Commerce" group

## 10. NextJS Requirements
- `BillingTimeline`: iterates the server's `timeline` array and renders `BillingEventEntry` or `CompGrantEntry` based solely on `entry.type === 'billing_event' | 'comp_grant'` — a single `switch`/discriminated-union render, no `if (entry.description.includes(...))` or any other content-based inference.
- `CompGrantEntry`: fixed amber badge + "Comp Grant — Not Real Revenue" label + reason code + issuing admin, conveyed via both color and accessible label text (never color alone, per §2.2 accessibility requirement).
- Search results and detail both use `MaskedField`-equivalent conventions where any PII-adjacent field appears (cross-ref E.32's pattern if family/parent names are shown — confirm scope; this module's data is primarily financial, not PII-masked, per PRD §12.6 "no new PII surface").

## 11. Required API
**Admin API** — B-02: `GET /v1/admin/subscriptions/search`, `GET /v1/admin/subscriptions/{id}`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="support"` (read-only visibility per PRD §1.15/§2.3).

## 13. Loading / Empty / Error States
Search: loading skeleton, "No results" empty state. Detail: loading skeleton, "Awaiting first billing event" empty state for a brand-new subscription (§1.12).

## 14. Responsive UI / Accessibility
Timeline entries screen-reader-announce their type explicitly (e.g., "Billing event: Renewal succeeded" vs. "Comp grant: not real revenue, reason: goodwill credit") — never relying on badge color alone, per §2.2.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`; Arabic RTL layout mirrors the timeline direction per the PRD's Arabic mockup prompt (§2.5).

## 16. Security
The `type`-field-only rendering discipline is this screen's defining guarantee — mandatory test confirms `CompGrantEntry` is never rendered for a `billing_event`-typed entry and vice versa, using fixture data with no other distinguishing signal (e.g., identical-looking descriptions) to prove the render decision genuinely comes from `type` alone.

## 17. Testing
Unit: discriminated-union render-selection logic. UI: **mandatory** — no client-side heuristic or string-matching logic determines visual treatment (test using adversarial fixture data where a billing event's description text resembles comp-grant language, confirming it still renders as a billing event because `type='billing_event'`). Integration: full search → detail → interleaved-timeline-renders-correctly flow; billing event detail drill-in.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define the Discriminated-Union Zod Schema**
Objective: `subscription-detail.ts` matching B-02's `type`-tagged timeline entries. Files: `types/subscription-detail.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `SubscriptionSearchRepositoryImpl`**
Objective: Repository for B-02's two endpoints. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `BillingTimeline` with Type-Driven Rendering**
Objective: Discriminated-union switch on `entry.type` only. Dependencies: Task 02. Tests: **mandatory** — adversarial-fixture-data type-driven-rendering test. Definition of Done: test passes.

**Task 04 — Implement `BillingEventEntry` and `CompGrantEntry`**
Objective: Distinct visual treatments, accessible label text for both. Dependencies: Task 03. Tests: accessibility-label test for both entry types. Definition of Done: tests pass.

**Task 05 — Implement the Search, Detail, and Billing Event Detail Pages**
Objective: Compose all components with loading/empty/error states. Dependencies: Tasks 02–04. Tests: full-page smoke tests. Definition of Done: tests pass.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §17, including the mandatory adversarial-fixture test. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm zero content-based inference exists anywhere in the timeline-rendering path. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Timeline visual treatment selected exclusively from server `type` field — mandatory adversarial test passing
- [ ] Comp grant entries always show the amber badge + explicit label, conveyed via text not color alone
- [ ] "Awaiting first billing event" empty state for new subscriptions
- [ ] `support`+ scope enforced (read-only)

## 20. Definition of Done
Billing Ops can search and inspect any subscription's history through a timeline whose comp-grant-vs-real-revenue distinction is provably server-driven and unmistakable, both visually and to assistive technology.
