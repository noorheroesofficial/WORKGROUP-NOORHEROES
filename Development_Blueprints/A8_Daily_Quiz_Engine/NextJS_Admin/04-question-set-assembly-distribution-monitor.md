# N-04 — Question-Set Assembly Distribution Monitor

## 1. Feature Context
A read-only editorial-quality dashboard showing which skills/topics are actually appearing in assembled quizzes across the whole user base over time — a curriculum-quality signal, deliberately walled off from any per-child data to keep it a content-design tool, not a surveillance one.

## 2. Parent Feature
Feature A.8 — Daily Quiz & Quiz Completion Engine

## 3. Sub-feature
3.4 Question-Set Assembly Distribution Monitor (ID: **N-04**)

## 4. Objective
Build a recharts-based aggregate dashboard against B-08's distribution endpoint, with filtering by date range, context, and skill domain — and a hard architectural guarantee that no per-child field can ever reach this page.

## 5. Business Requirements
PRD §8 ("Question-Set Assembly Monitor (Read-only): Visibility into the deterministic assembly algorithm's actual output distribution... an editorial/curriculum-quality signal, not a per-child surveillance tool"), §9 item 5 ("must NOT expose any per-child quiz history, only aggregate topic-distribution data").

## 6. Existing Architecture
`src/features/quiz-assembly-monitor/` module, following the existing recharts-based dashboard pattern used elsewhere in the Admin Portal (e.g., A.2's Home Composition Health Monitor).

## 7. Existing Code to Reuse
- `src/shared/components/require-permission.tsx::RequirePermission`
- Existing recharts wrapper components/theming from other Admin Portal dashboards
- `src/shared/hooks/use-date-range-filter.ts` (if it already exists — confirm before building a new one)

## 8. Files to Create
- `src/app/(dashboard)/quiz-engine/assembly-monitor/page.tsx`
- `src/features/quiz-assembly-monitor/api/assembly-distribution-repository.ts`
- `src/features/quiz-assembly-monitor/hooks/use-assembly-distribution.ts`
- `src/features/quiz-assembly-monitor/components/topic-distribution-chart.tsx`
- `src/features/quiz-assembly-monitor/components/assembly-monitor-filters.tsx`
- `src/features/quiz-assembly-monitor/types/assembly-distribution.ts` — Zod schema, deliberately with no per-child-identifiable field types

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `QUIZ_ASSEMBLY_DISTRIBUTION.*` endpoint
- `src/shared/components/dashboard-shell.tsx` — nav item (read-only role sufficient)

## 10. NextJS Requirements
- `AssemblyMonitorFilters`: date-range picker, context filter (home_daily/story_post/learn_practice/dua_recall), skill-domain filter
- `TopicDistributionChart`: recharts bar/line chart showing aggregate skill/topic appearance frequency over the selected range
- The Zod schema for this page's data type must structurally exclude any per-child field (e.g., no `child_id`, no per-child breakdown) — this is enforced at the type level, not just by convention, so a future accidental backend field addition would fail schema validation loudly rather than silently rendering

## 11. Required API
**Admin API** — B-08: `GET /admin/v1/quiz-assembly/distribution`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; a read-only admin role is sufficient — no write actions exist on this page, so no elevated `content_editor`/`trust_safety` gating is needed here (broader Admin Portal read-access is the only bar).

## 13. Loading / Empty / Error States
Chart-loading skeleton; empty state for a date range with no assembled quizzes yet ("No quiz data in this range"); error state distinct from empty (API failure vs. genuinely no data).

## 14. Responsive UI / Accessibility
Chart includes a data-table fallback/toggle for screen-reader and low-vision accessibility (charts alone are not sufficient); filters collapse to a stacked layout on narrow viewports.

## 15. Localization / RTL
Skill/topic names and axis labels localized; RTL layout for filters and chart legend positioning.

## 16. Security
**This page's defining security property is a data-boundary guarantee, not an access-control one**: even with full admin read access, no per-child data must ever be renderable here. Verified by a dedicated test asserting the response schema and rendered UI contain zero per-child-identifiable fields, treated with the same rigor as a PII-exposure control.

## 17. Testing
Unit: Zod schema rejects/flags any per-child-identifiable field if present in a mocked response (signature test — a defense against future backend regression). Integration: filters correctly scope the chart data (date range, context, skill domain). UI: empty vs. error state correctly distinguished. Accessibility: data-table fallback present and correctly populated.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Aggregate-Only Zod Schema**
Objective: `assembly-distribution.ts` with no per-child field types representable. Files: types file. Tests: schema-boundary test. Definition of Done: signature test passes — schema structurally cannot represent a per-child field.

**Task 02 — Implement AssemblyDistributionRepositoryImpl**
Objective: repository for B-08's distribution endpoint. Files: repository, `api-endpoints.ts`. Dependencies: Task 01. Definition of Done: mocked-fetch tests pass.

**Task 03 — Implement useAssemblyDistribution Hook**
Objective: data-fetching hook with filter parameters. Dependencies: Task 02. Definition of Done: hook correctly passes date-range/context/skill filters.

**Task 04 — Implement AssemblyMonitorFilters**
Objective: date-range, context, skill-domain filter controls. Dependencies: Task 03. Definition of Done: filter changes trigger correct refetch.

**Task 05 — Implement TopicDistributionChart with Accessible Fallback**
Objective: recharts visualization + data-table toggle. Dependencies: Task 03. Tests: accessibility fallback test. Definition of Done: table fallback populated correctly.

**Task 06 — Implement Assembly Monitor Page**
Objective: compose `RequirePermission` + filters + chart + states. Dependencies: Task 05. Definition of Done: page smoke test passes against mocked API.

**Task 07 — Add Full Test Suite**
Objective: complete coverage per §17, with the schema-boundary test as the highest-priority case. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: confirm zero per-child-identifiable data is reachable anywhere in this module's code path. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Response schema structurally cannot represent a per-child-identifiable field (signature test passing)
- [ ] Filters (date range, context, skill domain) correctly scope the displayed data
- [ ] Empty state and error state are visually and semantically distinct
- [ ] Chart has an accessible data-table fallback, not chart-only presentation
- [ ] Read-only admin access is sufficient — no elevated role required for this page
- [ ] RTL layout verified for filters and chart legend

## 20. Definition of Done
Curriculum and editorial teams can see aggregate topic-distribution trends across all assembled quizzes with zero per-child data ever reachable, backed by a schema-level guarantee rather than a convention-only one.
