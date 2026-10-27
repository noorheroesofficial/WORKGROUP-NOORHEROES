# N-05 — Quiz Result Recommendation Quality Monitor

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). A read-only Admin Portal dashboard showing the aggregated distribution of B-06's "next step" recommendations actually being generated across the user base — a curriculum-quality signal analogous to A.8's Assembly Monitor, helping teams spot gaps or over-concentration in the recommendation logic's output.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
N-05 — Quiz Result Recommendation Quality Monitor (Admin Read-Only Dashboard)

## 4. Objective
Build a read-only dashboard (recharts) visualizing which skills get recommended most/least often as B-06's "next step," aggregated across the user base and filterable by domain, sourced from a read-only aggregation endpoint.

## 5. Business Requirements
- Admin Requirements (A.9 PRD §8): "Quiz Result Recommendation Quality Monitor (Read-only): Visibility into the 'one next step' recommendation logic's actual output distribution across the user base — a curriculum-quality signal analogous to A.8's Assembly Monitor."
- Admin AI Code-Generation Prompt item 5: read-only dashboard (recharts), distribution of next-step recommendations, sourced from a read-only aggregated endpoint.
- CRUD permissions: Read-only.

## 6. Existing Architecture
React + TypeScript Admin Portal, recharts for data visualization (already used elsewhere in the platform, e.g., A.8's Assembly Monitor — reuse its chart-component conventions rather than introducing a different charting approach).

## 7. Existing Code to Reuse
- A.8's Assembly Monitor (`04-question-set-assembly-distribution-monitor.md`) — the direct architectural and visual precedent for this dashboard; reuse its chart-component patterns, data-fetching conventions, and layout structure rather than designing a new dashboard pattern from scratch.
- Existing RBAC read-access patterns.

## 8. Files to Create
- `app/admin/mastery/recommendation-quality/page.tsx`
- `app/admin/mastery/recommendation-quality/components/RecommendationDistributionChart.tsx`
- `app/admin/mastery/recommendation-quality/components/DomainFilterControl.tsx`
- `lib/api/masteryRecommendationQuality.ts`
- `lib/types/recommendationQuality.ts`
- `__tests__/admin/mastery/recommendation-quality/RecommendationDistributionChart.test.tsx`

## 9. Files to Modify
None (self-contained new read-only page).

## 10. Backend Requirements
**Resolved.** The originally-flagged missing dependency is now covered by **B-12 — Admin Recommendation Quality Aggregation API**, which logs every `next_step` selection from B-06 to a child-anonymous `next_step_recommendation_log` table and exposes `GET /admin/v1/mastery/recommendation-quality?domain=&days=` as a read-only, aggregate-only endpoint. This page builds against that endpoint's confirmed contract (§13).

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- **Dashboard layout:** bar or histogram chart (recharts) showing recommendation frequency per skill, with a domain filter control.
- **Aggregation display:** highlight skills with unusually high concentration (potential over-recommendation, may indicate other skills' recommendation logic is under-triggering) or skills with zero/near-zero recommendations (potential content gap).
- **Loading/empty/error states:** standard patterns; empty state for a domain with insufficient data to chart meaningfully.
- **RBAC:** read-only; confirm which role(s) should have access (likely `product_admin` and/or `curriculum_editor` and/or `learning_science` — this is a curriculum-quality signal relevant to multiple roles; default to the broadest reasonable read-only admin access unless product intent narrows it).

## 13. API Contract
Consumes B-12's `GET /admin/v1/mastery/recommendation-quality?domain=&days=` exactly as specified there:
```json
{
  "window_days": 30,
  "domain": "quran",
  "distribution": [
    { "skill_node_id": "uuid", "label": "Surah Al-Fatiha, Ayah 4", "recommendation_count": 214 }
  ]
}
```
No invented fields beyond this confirmed shape.

## 14. Database Requirements
N/A (frontend only; backend aggregation query is B-12's concern, not yet scoped).

## 15. Validation
N/A beyond standard domain-filter input validation once the API contract is defined.

## 16. Authentication
Reuses existing Admin Portal auth/session context.

## 17. Authorization
Read-only; specific role scope to be confirmed (see §12).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Fetch failure | Error state with retry |
| Domain with insufficient data | Empty/low-data state, not a broken chart |
| Invalid `days`/`domain` query param (client-constructed) | Client-side guard against constructing an out-of-bounds request; server-side `422` as a defense-in-depth backstop |

## 19. Offline First
N/A (admin web app).

## 20. Local Data
N/A.

## 21. Localization
Per N-01 §21's platform-wide Admin Portal localization scope decision.

## 22. RTL
Per N-01 §22's decision.

## 23. Analytics
N/A (this page itself surfaces analytics-like data; it doesn't need to be separately analytics-instrumented beyond standard admin-page-view tracking if the platform does that universally).

## 24. Performance
Chart rendering performance for potentially large skill catalogs — use recharts' standard performance patterns (already established via A.8's Assembly Monitor precedent); aggregation itself should be pre-computed server-side (B-12's concern), not computed client-side from raw per-child data (which would be both slow and a data-exposure risk).

## 25. Security
Read-only, aggregated data only — no per-child identifiable information should ever reach this dashboard (aggregate counts only, consistent with the platform's general child-privacy posture).

## 26. Library Requirements
recharts (already an established dependency per A.8's Assembly Monitor precedent) — no new libraries.

## 27. Testing
- Component test: chart renders correctly given representative aggregated data matching B-12's confirmed response shape.
- Component test: domain filter correctly re-scopes the displayed data.
- Empty/low-data state test.
- Integration test: full fetch → render cycle against B-12's live endpoint (or a faithful mock of its confirmed contract).

## 28. Documentation
Cross-reference B-12 as this page's backing data source in the page's code comments.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Build API Client & Types Against B-12's Confirmed Contract**
- Task ID: N-05-T01
- Objective: Typed client for B-12's aggregation endpoint.
- Why This Is Required: Data layer for the dashboard.
- Existing Architecture to Follow: Existing Admin Portal API-client conventions.
- Existing Files to Reuse: Existing typed-fetch wrapper.
- Files to Create: `lib/api/masteryRecommendationQuality.ts`, `lib/types/recommendationQuality.ts`.
- Files to Modify: None.
- Implementation Details: Match B-12's `GET /admin/v1/mastery/recommendation-quality?domain=&days=` contract exactly (§13) — no invented fields.
- Business Rules: N/A. Validation: Type-safe shape.
- Error Handling: Typed error propagation. Security: N/A. Performance: N/A.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: N/A (thin layer).
- Documentation: TSDoc.
- Dependencies: B-12.
- Do Not Change: N/A.
- Expected Result: Working typed client against B-12's real contract.
- Definition of Done: Types match B-12's schema exactly.

**Task 02 — Build RecommendationDistributionChart Dashboard**
- Task ID: N-05-T02
- Objective: The read-only visualization page.
- Why This Is Required: Core deliverable.
- Existing Architecture to Follow: A.8's Assembly Monitor's chart/dashboard conventions.
- Existing Files to Reuse: A.8's recharts component patterns.
- Files to Create: `page.tsx`, `RecommendationDistributionChart.tsx`, `DomainFilterControl.tsx`.
- Files to Modify: None.
- Implementation Details: Bar/histogram chart with domain and time-window filtering, per §12.
- Business Rules: Read-only, no mutation affordances anywhere on this page.
- Validation: N/A. Error Handling: Per §18.
- Security: Aggregate-only data, role-gated read access.
- Performance: Standard recharts performance practices.
- Localization: Per decision. RTL: Per decision. Analytics: N/A.
- Tests: `RecommendationDistributionChart.test.tsx`.
- Documentation: N/A.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working, read-only curriculum-quality dashboard.
- Definition of Done: Tests green against B-12's real aggregated data shape.

## 30. Definition of Done
Quiz Result Recommendation Quality Monitor live as a read-only dashboard, built against B-12's confirmed, implemented aggregation endpoint — the previously-flagged open API-contract dependency is fully resolved.

## 31. Final Verification Checklist
- [ ] B-12's aggregation endpoint confirmed and consumed (no invented fields)
- [ ] Dashboard renders correctly against real aggregated data
- [ ] Domain and time-window filters working
- [ ] Read-only — no mutation affordances anywhere
- [ ] No per-child identifiable data exposed (aggregate-only, verified by B-12's data-boundary test)
- [ ] Empty/low-data state handled
- [ ] RBAC read-scope explicitly confirmed and enforced
