# K-05 — Invoice History & Invoice Detail Screens

## 1. Feature Context
Two screens: a list of past invoices (billing history) and a detail view per invoice, reached from the Subscription landing screen.

## 2. Parent Feature
Feature C.24 — Subscription & Billing

## 3. Sub-feature
2.5 Invoice History & Invoice Detail Screens (ID: **K-05**)

## 4. Objective
Build `InvoiceHistoryScreen` and an invoice detail view sourced from `GET /v1/parent/subscription` (invoice summary list) and `GET /v1/parent/subscription/invoices/{id}` (detail), with a friendly empty state for new subscribers.

## 5. Business Requirements
- §1.12 Empty States: zero invoice history → "Your first invoice will appear here after your trial converts."
- §1.18 Screens 7–8: Invoice History → Invoice Detail → Back.

## 6. Existing Architecture
Part of `:feature:subscription`; consumes `SubscriptionRepository.getInvoices()`/`getInvoiceDetail(id)`.

## 7. Existing Code to Reuse
- K-01's `SubscriptionRepository` and offline-cache pattern.
- `:core:design-system` list/empty-state components.

## 8. Files to Create
- `feature/subscription/ui/InvoiceHistoryScreen.kt`
- `feature/subscription/ui/InvoiceDetailScreen.kt`
- `feature/subscription/viewmodel/InvoiceHistoryViewModel.kt`
- `test/feature/subscription/InvoiceHistoryViewModelTest.kt`

## 9. Files to Modify
- `feature/subscription/data/SubscriptionRepository.kt` — add `getInvoices()`, `getInvoiceDetail(id)`
- `feature/subscription/navigation/SubscriptionRoute.kt` — add `InvoiceHistoryRoute`, `InvoiceDetailRoute`

## 10. KMP Requirements
- `InvoiceHistoryViewModel` loads the invoice list (from K-01's already-fetched subscription response where possible, or a dedicated call if the list needs to be paginated separately).
- Empty state renders the exact friendly copy from §1.12, not a generic "no data" placeholder.
- Invoice Detail loads on tap, keyed by `invoice_id`; handles a not-found/removed invoice gracefully.
- Date/currency formatting fully locale-aware.

## 11. Required API
`GET /v1/parent/subscription` (B-05, invoice summary), `GET /v1/parent/subscription/invoices/{id}` (B-05, detail). **User API.**

## 12. Offline First
Last-cached invoice list renders offline; invoice detail for a not-yet-cached invoice requires connectivity, shown with a clear offline-state message rather than a blank screen.

## 13. Local Data
Invoice list cached alongside K-01's subscription snapshot cache.

## 14. Localization
All labels, empty-state copy, and date/currency formatting localized EN/HI/AR/UR.

## 15. RTL
List and detail layouts mirror correctly in RTL; currency/date formatting respects locale conventions independent of layout direction.

## 16. Analytics
`invoice_viewed` on invoice detail open.

## 17. Performance
Paginate invoice list if it grows large (defensive, though typically small per family); avoid re-fetching the full list on every detail-screen return via back navigation (cache in ViewModel scope).

## 18. Security
Read-only screens; no mutation capability. Family-ownership already enforced server-side (B-05) — client trusts but doesn't need to re-derive this check.

## 19. Testing
- Unit: empty state renders correct friendly copy for zero invoices.
- Unit: invoice list renders correctly from a populated response.
- UI: invoice detail loads correctly on tap; not-found invoice shows a graceful error, not a crash.
- UI: offline state for both list and detail screens.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Implement Repository Methods**
Objective: `getInvoices()`, `getInvoiceDetail(id)`. Files to Modify: `SubscriptionRepository.kt`. Dependencies: K-01.

**Task 02 — Implement `InvoiceHistoryViewModel`**
Objective: list state incl. empty-state handling. Files to Create: `InvoiceHistoryViewModel.kt`. Dependencies: Task 01.

**Task 03 — Implement `InvoiceHistoryScreen` & `InvoiceDetailScreen` Composables**
Objective: list + detail UI per §10. Files to Create: both screen files. Dependencies: Task 02.

**Task 04 — Wire Navigation**
Objective: Subscription landing → History → Detail → Back. Files to Modify: `SubscriptionRoute.kt`. Dependencies: Task 03.

**Task 05 — Add Analytics & Test Suite**
Objective: `invoice_viewed`, coverage per §19. Dependencies: Tasks 01–04.

## 21. Final Verification Checklist
- [ ] Empty state matches exact PRD copy
- [ ] Invoice detail handles not-found gracefully
- [ ] Offline states verified for both screens
- [ ] Locale-aware date/currency formatting verified
- [ ] RTL layout verified

## 22. Definition of Done
Invoice History and Invoice Detail screens render correctly from server data with a friendly empty state, graceful error handling, and full offline/localization/RTL support.
