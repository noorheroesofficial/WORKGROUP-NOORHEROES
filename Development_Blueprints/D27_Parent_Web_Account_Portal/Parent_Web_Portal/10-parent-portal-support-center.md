# N-10 — Parent Web Portal Support Center

## 1. Feature Context
Part of Feature D.27 — Parent Web Account Portal. The Support Center screen: FAQ search and ticket submission/status, reusing C.25's existing, content-governed FAQ service and ticket lifecycle contract unmodified.

## 2. Parent Feature
D.27 Parent Web Account Portal (`account.noorheroes.com`)

## 3. Sub-feature
**N-10 — Parent Web Portal Support Center**

## 4. Objective
Build the Support Center, FAQ Search, Contact Support Form, and Ticket History/Detail screens against C.25's existing FAQ and ticket APIs, preserving the structural guarantee that FAQ answers are always admin-authored/scholar-reviewed content, never AI-freeform-generated.

## 5. Business Requirements
- FR-12: "Support Center screen: FAQ search and ticket submission/status, reusing C.25's exact backend contract."
- C.25 FR-10 (inherited): "FAQ search is content-governed... never an AI-freeform-generated answer presented as official guidance" — a structural, testable guarantee this screen must not undermine.
- C.25's Edge Case 4 (inherited): zero-results search shows a "no results, contact Support" fallback, never an error.

## 6. Existing Architecture
Confirmed. C.25 B-03 ("FAQ Content & Search API") implements `GET /v1/support/faq?q=`, `GET /v1/support/faq/{id}` (public or Bearer, not subscription-gated), serving exclusively `published=true` admin-authored articles. C.25 B-04 implements the ticket lifecycle (`POST /v1/support/tickets`, `GET /v1/support/tickets`, per D.27's own §3.4 citation). No gaps found for this sub-feature — a direct, low-risk reuse case.

## 7. Existing Code to Reuse
- C.25 B-03's `GET /v1/support/faq?q=`, `GET /v1/support/faq/{id}` — consumed unmodified.
- C.25 B-04's `POST /v1/support/tickets`, `GET /v1/support/tickets` — consumed unmodified.
- N-02's `apiClient`, `PortalShell`.

## 8. Files to Create
- `noorheroes-account-portal/src/app/(portal)/support/page.tsx`
- `noorheroes-account-portal/src/app/(portal)/support/faq/page.tsx`
- `noorheroes-account-portal/src/app/(portal)/support/faq/[articleId]/page.tsx`
- `noorheroes-account-portal/src/app/(portal)/support/contact/page.tsx`
- `noorheroes-account-portal/src/app/(portal)/support/tickets/[ticketId]/page.tsx`
- `noorheroes-account-portal/src/features/support/api/support-client.ts`
- `noorheroes-account-portal/tests/features/support/faq-no-ai-generation.test.ts`

## 9. Files to Modify
- N-02's `allowed-endpoints.ts` — register `GET /v1/support/faq`, `GET /v1/support/faq/{id}`, `POST /v1/support/tickets`, `GET /v1/support/tickets`.

## 10. Backend Requirements
Consumes C.25 B-03/B-04 exclusively, zero new backend work required.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Support Center landing: entry to FAQ Search and Contact Support Form.
- FAQ Search screen: search input calling `GET /v1/support/faq?q=`, results list, zero-results fallback ("no results, contact Support," linking to Contact Support Form).
- FAQ Article Detail screen: `GET /v1/support/faq/{id}`, "Was this helpful?" feedback capture (per C.25 B-03's documented feedback mechanism) if in scope for this client (confirm whether feedback capture is part of the allowlisted contract or mobile-only — Task 01).
- Contact Support Form: ticket submission via `POST /v1/support/tickets`.
- Ticket History/Detail: `GET /v1/support/tickets` (list) and detail view.
- Loading/empty/error states throughout.
- Fire `web_support_center_viewed`, `web_faq_search_performed`, `web_ticket_submitted`.

## 13. API Contract
Consumes C.25 B-03/B-04's contracts exactly as documented in those blueprints.

## 14. Database Requirements
Not applicable (frontend).

## 15. Validation
Ticket submission form validation mirrors C.25 B-04's server-side required-field rules (confirm exact fields from that blueprint before finalizing the form).

## 16. Authentication
FAQ browsing works for "any parent, even pre-subscription" per C.25 B-03 §5 — but within this portal, a parent must still be logged in (per N-02's shell requiring an active session for all 23 routes); ticket submission/history requires the active session regardless.

## 17. Authorization
Not applicable beyond standard session/family-scoping already enforced server-side by C.25.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Zero FAQ search results | "No results, contact Support" fallback, never an error state |
| Ticket submission fails | Inline error, form data preserved for retry |
| FAQ article ID not found | Standard not-found handling |

## 19. Offline First
Not applicable — search and submission require connectivity; offline banner per N-02 applies.

## 20. Local Data
Not applicable beyond N-02's in-memory session state.

## 21. Localization
Full EN/HI/AR/UR localization of UI chrome; FAQ article content localization is sourced from the article's own `locale` field (C.25 B-03 §7, reusing the platform's canonical locale codes) — this screen renders whatever locale the content is authored in per the parent's active language, not a client-side translation.

## 22. RTL
Full RTL layout for search, list, and forms.

## 23. Analytics
`web_support_center_viewed`, `web_faq_search_performed`, `web_ticket_submitted` (§1.19).

## 24. Performance
Standard search-and-list performance; C.25 B-03's FAQ search is a straightforward query against published content, no special frontend optimization required.

## 25. Security
- This screen must never render unpublished/draft FAQ content — relies entirely on C.25 B-03's server-side `published=true` filter; no client-side filtering substitutes for this guarantee.
- No AI-generation call path exists anywhere in this screen's code — mirrors C.25 B-03's own structural guarantee, verified here by a corresponding frontend-side negative test (Task 05).

## 26. Library Requirements
No new libraries beyond N-02's established stack.

## 27. Testing
- Integration: FAQ search returns results correctly; zero-results shows the contact-Support fallback, not an error.
- Integration: ticket submission succeeds and appears in Ticket History.
- Integration: FAQ Article Detail never renders an unpublished article (fixture test).
- **Negative test:** no AI-generation/completion API call exists anywhere in this screen's code — mirrors C.25 B-03's structural guarantee on the frontend side.

## 28. Documentation
Document that FAQ content is always sourced from C.25's admin-governed article store — never generate or client-side-synthesize an FAQ answer under any circumstance, including as a "helpful suggestion" fallback for zero-results searches.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm "Was This Helpful?" Feedback Scope**
- **Objective:** Confirm whether FAQ feedback capture is part of this client's allowlisted contract or mobile-only, before building it into the Article Detail screen.

**Task 02 — Build `support-client.ts`**
- **Files to Create:** `support-client.ts`.

**Task 03 — Build Support Center, FAQ Search, and Article Detail Screens**
- **Files to Create:** `page.tsx`, `faq/page.tsx`, `faq/[articleId]/page.tsx`.

**Task 04 — Build Contact Support Form and Ticket History/Detail**
- **Files to Create:** `contact/page.tsx`, `tickets/[ticketId]/page.tsx`.

**Task 05 — Write the No-AI-Generation Negative Test**
- **Files to Create:** `faq-no-ai-generation.test.ts`.

**Task 06 — Localization, RTL, Analytics, Full Test Suite**

## 30. Definition of Done
A parent can search FAQs, view admin-authored article detail, and submit/track support tickets from the web portal, reusing C.25's existing contract unmodified, with the content-governance guarantee (never AI-freeform-generated) holding on this surface exactly as it does on the Mobile App.

## 31. Final Verification Checklist
- [ ] FAQ feedback-capture scope confirmed (Task 01)
- [ ] Zero-results search shows the contact-Support fallback, never an error
- [ ] No unpublished FAQ content ever renders (fixture test)
- [ ] No AI-generation call path exists anywhere in this screen's code
- [ ] Full localization and RTL verified
