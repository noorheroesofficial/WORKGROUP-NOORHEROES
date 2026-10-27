# K-04 — Spaced-Repetition Resurfacing Prompt Integration

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). Consumes A.9's existing generic review-prompt UI component, parameterized for the `islamic_facts` domain — no facts-specific resurfacing UI is built.

## 2. Parent Feature
B.18 — Islamic Facts Module

## 3. Sub-feature
2.4 Spaced-Repetition Resurfacing Prompt Integration (ID: K-04)

## 4. Objective
Wire A.9's `:core:mastery-engine` generic spaced-repetition resurfacing prompt component to surface `islamic_facts` domain nodes (registered via B-05), routing a tap into Fact Detail, subject to the platform-wide cross-domain daily prompt cap.

## 5. Business Requirements
- FR-4: Islamic Facts participates in A.9's shared spaced-repetition scheduler, subject to the same global daily-prompt cap as Quran/Arabic/Tajweed.
- Acceptance Criteria: when the scheduler determines a fact is due and the daily cap allows it, the fact may be resurfaced as a gentle review prompt.
- Edge Case 4: same fact instance not shown twice across surfaces same day — the resurfacing prompt itself must respect this, which the backend's B-02 same-day-distinctness logic already enforces server-side; this sub-feature simply consumes whatever the backend returns without independently re-selecting.

## 6. Existing Architecture
A.9's `:core:mastery-engine` already exposes a generic, domain-parameterized review-prompt Composable (per A.5/A.9's own K-09 "Spaced Review Needs-Refresh Prompt" pattern) — this sub-feature configures it for `islamic_facts`, adding zero new prompt-rendering logic.

## 7. Existing Code to Reuse
- A.9/A.5's existing generic review-prompt Composable and its `ReviewPromptContext` parameterization pattern (mirror A.5's K-09 configuration exactly, substituting the `islamic_facts` domain).
- `:core:mastery-engine`'s existing scheduler-query client (already fetches due-for-review items across all registered domains).

## 8. Files to Create
- `feature-facts/src/commonMain/kotlin/.../FactResurfacingPromptConfig.kt` (thin config/parameterization, not a new prompt UI).
- `feature-facts/src/commonTest/kotlin/.../FactResurfacingIntegrationTest.kt`.

## 9. Files to Modify
- Wherever A.9's generic review-prompt is composed into Home/Skill Tree surfaces — register `islamic_facts` as a domain whose resurfacing prompts route into `FactDetailScreen` (K-01) when tapped.

## 10. Backend Requirements
Consumes B-05's domain registration and A.9's existing scheduler API (`GET /v1/skills/state`, A.9's cross-domain spaced-repetition scheduler) — no facts-specific backend call in this sub-feature.

## 11. KMP Requirements
- Register `islamic_facts` → `FactDetailScreen` route mapping in the generic review-prompt component's domain-to-destination resolver (the same resolver pattern other domains like Quran/Arabic already use).
- Tap on a facts resurfacing prompt navigates to `FactDetailScreen(factId)` via `:core:navigation`.
- No independent fact-selection logic client-side — trust the backend's (B-02) daily-cap-respecting, same-day-distinct selection entirely.
- Add analytics: `fact_spaced_repetition_resurfaced`, fired via `FactsAnalytics` when a facts-domain resurfacing prompt is shown.

## 12. NextJS Requirements
N/A.

## 13. API Contract
No new contract — consumes A.9's existing `GET /v1/skills/state` / scheduler response, which now includes `islamic_facts` nodes per B-05's registration.

## 14. Database Requirements
None new — reads A.9's existing `skill_node` data via its established client.

## 15. Validation
`factId` extracted from the resurfacing prompt payload validated non-null before navigation; malformed payload → prompt not rendered for that item (fail-safe, not a crash).

## 16. Authentication
Reuses A.9's existing authenticated scheduler-query client.

## 17. Authorization
N/A beyond authenticated child session.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Scheduler returns a facts-domain item with malformed/missing `factId` | Prompt not rendered for that item |
| Tap on prompt fails to resolve a valid fact (edge race — fact withdrawn between scheduling and tap) | Fact Detail's own `410`/not-found handling (K-01) takes over |

## 19. Offline First
Resurfacing prompts require the scheduler data to have been fetched at least once; offline behavior inherits `:core:mastery-engine`'s existing offline handling for the scheduler query (unmodified here).

## 20. Local Data
None new — inherits A.9's existing local caching for scheduler state, if any.

## 21. Localization
Prompt copy ("You might have forgotten this fact...") sourced from A.9's existing generic prompt string resources, not duplicated locally.

## 22. RTL
Inherits A.9's existing generic prompt component's RTL handling.

## 23. Analytics
`fact_spaced_repetition_resurfaced` — the only new event in this sub-feature, layered on top of A.9's existing generic resurfacing-shown event (both may fire; this is the domain-specific funnel marker).

## 24. Performance
Negligible — this sub-feature adds only a domain-to-destination mapping entry, not new computation.

## 25. Security
No new attack surface; inherits A.9's existing security posture entirely.

## 26. Library Requirements
None new.

## 27. Testing
- Integration test: confirm `islamic_facts` domain resurfacing prompts render using A.9's exact existing generic component (reuse-verification, mirroring K-02's pattern for the quiz engine).
- Unit: malformed resurfacing payload for a facts item does not crash, prompt simply not rendered.
- Unit: tap correctly navigates to `FactDetailScreen(factId)`.

## 28. Documentation
KDoc noting this is a pure domain-registration/configuration integration, not a new UI component.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Register Domain-to-Destination Mapping**
Objective: Add `islamic_facts` → `FactDetailScreen` entry to A.9's existing resolver.
Existing Architecture to Follow: The mapping pattern already used for Quran/Arabic domains.
Files to Create: `FactResurfacingPromptConfig.kt`.
Dependencies: K-01 complete, B-05 complete.
Definition of Done: Mapping registered, resolver correctly routes `islamic_facts` taps.

**Task 02 — Analytics Wiring**
Objective: `fact_spaced_repetition_resurfaced` event.
Dependencies: Task 01.
Definition of Done: Event fires correctly on prompt display.

**Task 03 — Tests**
Objective: Coverage per §27.
Dependencies: Tasks 01–02.
Definition of Done: All green, reuse-verification test confirms no new prompt UI built.

**Task 04 — Documentation**
Dependencies: Task 03.
Definition of Done: KDoc complete.

## 30. Definition of Done
- `islamic_facts` domain correctly surfaces in A.9's existing generic resurfacing prompt, zero new prompt UI.
- Daily cap and same-day-distinctness fully trusted from backend, no client-side re-selection logic.
- Tests green.

## 31. Final Verification Checklist
- [ ] Reuse-verification test confirms A.9's exact existing component is used, no new prompt UI
- [ ] Tap correctly routes to Fact Detail
- [ ] Malformed resurfacing payload handled gracefully, no crash
- [ ] Analytics event firing correctly
- [ ] No independent client-side fact-selection logic introduced
