# K-05 — Noor Garden — Personal & Family Visualization

## 1. Feature Context
NoorHeroes KMP app. The immersive, illustrated progress-world visualization for personal and family habit consistency, structurally guaranteed free of sibling comparison.

## 2. Parent Feature
A.7 Habit Tracker — KMP App (Android/iOS)

## 3. Sub-feature
K-05 Noor Garden — Personal & Family Visualization

## 4. Objective
Build the Noor Garden Personal and Family screens plus the Family Streak Milestone Celebration, with the Family Garden response DTO structurally incapable of holding a per-child breakdown, mirroring B-06's server-side guarantee on the client (FR-12).

## 5. Business Requirements
- Family Garden shows combined-only aggregate progress; requires explicit child-switcher tap, never simultaneous side-by-side comparison layout (PRD §2.1 No-Comparison Enforcement design principle).
- Personal Garden is a single composed illustrated scene with distinct zones per habit type, not disconnected icons.
- Zero-milestone state shows a "seedling" starting description.
- Degraded Family Aggregation Service shows a non-alarming "growing..." state.

## 6. Existing Architecture
Extends `feature-habits`/`feature-habits-domain` (K-01). This sub-feature also owns the reconciliation with A6's existing `feature/dua-learning/.../habit/HabitReminderSuggestionCard.kt` and A2's Home widget only insofar as both should eventually deep-link into this canonical Noor Garden screen rather than rendering their own garden previews, if any exist (verify and flag, do not silently duplicate).

## 7. Existing Code to Reuse
- `HabitRepository` extended with `GetGardenUseCase` (K-01 pattern)
- `core-design-system` illustration system tokens (if a garden/illustration component library already exists elsewhere in the app, reuse it; otherwise this sub-feature establishes the reusable themed components per PRD §2.5 image-generation prompts as the visual reference)

## 8. Files to Create
- `feature-habits/src/commonMain/kotlin/.../garden/NoorGardenPersonalScreen.kt`
- `feature-habits/src/commonMain/kotlin/.../garden/NoorGardenFamilyScreen.kt`
- `feature-habits/src/commonMain/kotlin/.../garden/FamilyMilestoneCelebrationModal.kt`
- `feature-habits/src/commonMain/kotlin/.../garden/FamilyGardenDto.kt` (aggregate-only fields, no per-child structure)
- `feature-habits-domain/src/commonMain/kotlin/.../GetGardenUseCase.kt`
- `feature-habits/src/commonTest/kotlin/.../FamilyGardenDtoReflectionTest.kt`

## 9. Files to Modify
None required beyond navigation wiring from K-01/K-04.

## 10. Backend Requirements
Consumes `GET /v1/habits/garden/{child_id}` (B-06).

## 11. KMP Requirements
- Personal Garden: full-bleed illustrated scene, distinct zones (Quran tree, kindness flowers, Salah lanterns, dua stars, Ramadan moon path), "last grew on [date]" indicator.
- Family Garden: aggregate-only view; explicit child-switcher control (tap to view a different child's *personal* garden — never a simultaneous multi-child layout).
- `FamilyGardenDto` (deserialized from `GET /v1/habits/garden/{child_id}`) must contain **only aggregate fields** — no `List<ChildContribution>` or any nested `childId`/`child_id`-bearing field.
- Reflection-based test enumerating the DTO's declared fields, asserting none are collection types containing a nested child-identifying field (mandatory, mirrors B-06's server-side structural test).
- Family Streak Milestone Celebration modal on threshold crossing.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`GET /v1/habits/garden/{child_id}` (B-06).

## 14. Database Requirements (Local)
Room cache of last-fetched garden state for offline/degraded display, mirroring B-06's "growing..." fallback philosophy.

## 15. Validation
Mandatory reflection test asserting the `FamilyGardenDto` class's declared fields contain no collection type with a nested `childId`/`child_id` field (PRD §7 Android prompt item 4) — this guards against a future well-intentioned but policy-violating addition slipping through code review.

## 16. Authentication
Shared `core-network` Bearer token attachment.

## 17. Authorization
N/A at UI layer (enforced server-side, B-06).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Family Aggregation Service degraded | "Growing..." non-alarming state, personal garden unaffected |
| Zero family milestones | "Seedling" starting state with next-milestone description |
| Garden fetch fails entirely | Cached last-known garden shown, not a blank error screen |

## 19. Offline First
Garden state cached locally for offline/degraded viewing; not a write path (read-only visualization).

## 20. Local Data
```
GET /v1/habits/garden/{child_id}
   ↓
GetGardenUseCase
   ↓
Room garden_cache
   ↓
NoorGardenPersonalScreen / NoorGardenFamilyScreen
```

## 21. Localization
Zone labels, milestone descriptions, "last grew on" date formatting all localized (EN/HI/AR/UR) with correct date-format conventions per locale.

## 22. RTL
Isometric garden scene layout and zone labels verified for RTL; child-switcher control mirrors correctly.

## 23. Analytics
`noor_garden_viewed` (personal/family), `family_streak_milestone_reached` via `AnalyticsTracker` — both aggregate-only event schemas.

## 24. Performance
Illustration assets lazy-loaded/cached; avoid loading the full garden scene at once if it impacts initial render time — consider progressive/layered loading of garden zones.

## 25. Security
Reflection test on `FamilyGardenDto` is the client-side half of the defense-in-depth sibling-comparison guarantee (server-side half is B-06's schema test).

## 26. Library Requirements
Compose Multiplatform, Koin, Ktor, Room, Kotlin reflection (`KClass.memberProperties` or equivalent multiplatform-safe reflection utility).

## 27. Testing
- Mandatory: `FamilyGardenDto` reflection test (no child-identifying nested fields).
- UI: Family Garden screen renders with zero per-child comparative UI elements (structural UI test mirroring the backend's schema guarantee, per PRD §6.10).
- UI: personal garden zone rendering, milestone celebration modal.

## 28. Documentation
KDoc explicitly stating `FamilyGardenDto` must never gain a per-child field, referencing B-06's server-side guarantee and this file's reflection test as the enforcement mechanism.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define `FamilyGardenDto` (Aggregate-Only)**
- Objective: Client-side mirror of B-06's structural no-comparison guarantee.
- Why Required: Defense-in-depth — even a buggy/malicious server response extension couldn't be rendered by a client with no field to deserialize it into.
- Files to Create: `FamilyGardenDto.kt`
- Do Not Change: never add a per-child field to this DTO.
- Definition of Done: DTO contains only aggregate fields.

**Task 02 — Implement `GetGardenUseCase` + Local Cache**
- Files to Create: `GetGardenUseCase.kt`, Room cache entity/DAO.
- Tests: cached-fallback unit test.
- Definition of Done: use case correctly caches and falls back on degradation.

**Task 03 — Build Noor Garden Personal & Family Screens**
- Files to Create: `NoorGardenPersonalScreen.kt`, `NoorGardenFamilyScreen.kt`
- Implementation Details: illustrated zones, child-switcher (not simultaneous comparison), "growing..."/"seedling" states.
- Tests: Compose UI tests for structural no-comparison UI verification.
- Definition of Done: screens render correctly per all documented states.

**Task 04 — Build Family Milestone Celebration Modal**
- Files to Create: `FamilyMilestoneCelebrationModal.kt`
- Definition of Done: modal triggers correctly on threshold-crossing event.

**Task 05 — Write Mandatory Reflection Test**
- Files to Create: `FamilyGardenDtoReflectionTest.kt`
- Definition of Done: test passes, registered as CI gate alongside B-06's server-side structural test.

**Task 06 — Final Code Review**
- Do Not Change: `FamilyGardenDto` field set.
- Expected Result: PR merge-ready, both client and server structural tests green.

## 30. Definition of Done
Noor Garden Personal/Family screens live; `FamilyGardenDto` verified aggregate-only via mandatory reflection test; no simultaneous sibling-comparison UI exists anywhere in this flow.

## 31. Final Verification Checklist
- [ ] `FamilyGardenDto` reflection test passes (no child-identifying nested fields)
- [ ] Family Garden requires explicit child-switcher tap, never simultaneous comparison layout
- [ ] Personal Garden renders as a single composed scene with distinct zones
- [ ] "Growing..."/"seedling" fallback states implemented
- [ ] Family Milestone Celebration modal triggers correctly
- [ ] Localization and RTL verified
- [ ] Analytics events wired
