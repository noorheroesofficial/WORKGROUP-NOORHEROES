# K-03 — Skill Tree State Renderer

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). A single, shared `SkillTreeStateRenderer` Composable that maps the six canonical skill states to the visual tokens already established in `:core:design-system` from A.5's work — centralizing state-to-visual mapping so any current or future domain's skill-tree UI gets consistent visuals for free.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
K-03 — Skill Tree State Renderer (Shared Component)

## 4. Objective
Extract and centralize the state-to-visual-token mapping (`Locked/Ready/Learning/Practicing/Mastered/Needs Refresh` → design-system visuals) into `:core:mastery-engine`, replacing any per-feature-module duplication of this mapping, and consumed by A.5's `K-01 Quran Skill Tree Map`.

## 5. Business Requirements
- FR-1: exactly six canonical states, domain-agnostic.
- Android AI Prompt item 6: "Provide a SkillTreeStateRenderer reusable composable... do not redefine the state-to-visual mapping separately inside `:feature:learn`; centralize it here."
- §21.9 (referenced): Locked node shows a specific unlock condition, not a generic lock; Needs Refresh uses a gentle, non-regression framing.

## 6. Existing Architecture
Kotlin, Jetpack Compose. Global Design System tokens and the skill-state visual language are already defined per A.1 §2.1 and A.5 §2.1 ("Skill Tree Visual Language" — node treatments per state). A.5's `K-01 Quran Skill Tree Map` currently implements (or is expected to implement) this mapping directly inside `:feature:learn` — this sub-feature extracts that logic into the shared module.

## 7. Existing Code to Reuse
- `:core:design-system`'s existing skill-state visual tokens (colors, icons, progress-ring styles per state) — this component consumes those tokens, it does not define new ones.
- A.5's existing skill-tree map rendering logic, if already implemented — refactor it to delegate to this new shared component rather than duplicating the mapping.
- K-01's `SkillStateDto`/skill-state data shapes.

## 8. Files to Create
- `core/mastery-engine/src/commonMain/kotlin/.../presentation/components/SkillTreeStateRenderer.kt`
- `core/mastery-engine/src/commonMain/kotlin/.../presentation/SkillStateVisualMapper.kt` — pure mapping function (state → token set).
- `core/mastery-engine/src/commonTest/kotlin/.../SkillStateVisualMapperTest.kt`
- `core/mastery-engine/src/androidInstrumentedTest/kotlin/.../SkillTreeStateRendererUiTest.kt`

## 9. Files to Modify
- A.5's `K-01 Quran Skill Tree Map` implementation — replace any inline state-to-visual mapping with a call into this shared `SkillTreeStateRenderer`/`SkillStateVisualMapper`.

## 10. Backend Requirements
N/A (pure presentation-layer component; consumes B-05's state data via K-01).

## 11. KMP Requirements
- **`SkillStateVisualMapper.map(state: SkillState): SkillStateVisualTokens`** — pure function returning the design-system token set (color, icon, progress-ring style, label-key) for each of the six states, sourced entirely from `:core:design-system`, no new visual definitions invented here.
- **`SkillTreeStateRenderer` Composable:** renders a single skill node's visual treatment given its state and optional `unlockCondition` text (for `Locked` nodes) — accepts domain-agnostic input, no domain-specific rendering branches.
- **`Locked` node treatment:** must display the specific unlock-condition text passed in, never a generic "locked" message.
- **`Needs Refresh` node treatment:** gentle, encouraging visual/copy framing — never a regression/failure visual language (e.g., no red "X" or downward arrow).

## 12. NextJS Requirements
N/A.

## 13. API Contract
Consumes K-01's `SkillStateDto` (from B-05) — no independent network calls in this component.

## 14. Database Requirements
N/A.

## 15. Validation
`SkillState` enum values constrained to the six canonical states; `SkillStateVisualMapper` exhaustively handles all six (compile-time exhaustiveness via Kotlin's `when` on a sealed/enum type, so a future seventh state would fail to compile until handled — intentional safety net).

## 16. Authentication
N/A.

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `Locked` node with no `unlockCondition` text provided | Falls back to a documented generic-but-still-informative message (e.g., "Complete the previous skill first") rather than crashing or showing blank |
| Unknown/future state value not yet in the six-value set | Compile-time exhaustiveness check prevents this from shipping unhandled; if reached via a malformed API response, renders a safe default/error visual and logs a warning |

## 19. Offline First
Works identically whether `SkillStateDto` came from a live fetch or K-01's Room cache — this component is agnostic to data freshness (that concern is owned upstream).

## 20. Local Data
N/A directly (consumes whatever K-01 provides).

## 21. Localization
State labels (e.g., "Mastered", "Needs Refresh") and unlock-condition text sourced from string resources, EN/HI/AR/UR.

## 22. RTL
Progress-ring direction, icon placement, and text alignment must all mirror correctly in RTL layouts (Arabic/Urdu) — verified via RTL-mode UI tests.

## 23. Analytics
N/A directly (this is a pure rendering component; any tap-through analytics belong to the consuming screen, e.g., A.5's skill-tree map screen).

## 24. Performance
Pure, stateless, stable-parameter Composable — must not cause unnecessary recomposition when rendered inside a potentially large skill-tree grid/list (A.5's map may render dozens of nodes); use `@Stable`/`@Immutable` annotations on the token data class.

## 25. Security
No new attack surface (pure presentation component).

## 26. Library Requirements
Jetpack Compose only — no new libraries.

## 27. Testing
- Unit: `SkillStateVisualMapper` returns the correct token set for all six states (exhaustive test, one per state).
- UI test: `Locked` node renders the specific unlock-condition text passed in, not a generic message, when provided.
- UI test: `Needs Refresh` visual treatment verified as non-punitive (no red/failure iconography) — a design-review-style assertion on the token set used.
- UI test: RTL layout correctness across all six states.
- Performance test/lint: component does not trigger unnecessary recomposition when its state parameter is unchanged (stability annotations verified).

## 28. Documentation
KDoc explicitly instructing future domain feature modules to consume this component rather than reimplementing state-to-visual mapping locally — this is the centralization contract the Android AI Prompt explicitly calls for.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement SkillStateVisualMapper Pure Function**
- Task ID: K-03-T01
- Objective: Exhaustive, pure state→token mapping.
- Why This Is Required: The single source of truth every domain's skill-tree UI must share.
- Existing Architecture to Follow: `:core:design-system`'s existing token definitions from A.5's visual-language work.
- Existing Files to Reuse: `:core:design-system` skill-state tokens (colors/icons/progress-ring styles).
- Files to Create: `SkillStateVisualMapper.kt`.
- Files to Modify: None.
- Implementation Details: `when (state)` exhaustive over the six-value enum, returning a `@Immutable data class SkillStateVisualTokens`.
- Business Rules: `Needs Refresh` must use non-punitive visual language; `Locked` treatment separate from the unlock-condition text (which is passed in, not part of this mapping).
- Validation: Compile-time exhaustiveness.
- Error Handling: N/A (exhaustive, cannot be incomplete).
- Security: N/A. Performance: `@Immutable` annotated result type.
- Localization: Returns a label string-resource key, not raw text. RTL: N/A (data only). Analytics: N/A.
- Tests: `SkillStateVisualMapperTest.kt` — one assertion per state.
- Documentation: KDoc.
- Dependencies: `:core:design-system` tokens (existing).
- Do Not Change: `:core:design-system`'s token definitions themselves (consume, don't redefine).
- Expected Result: Complete, tested mapping function.
- Definition of Done: All six states covered by tests.

**Task 02 — Build SkillTreeStateRenderer Composable**
- Task ID: K-03-T02
- Objective: The reusable rendering component.
- Why This Is Required: Direct deliverable requested by the Android AI Prompt.
- Existing Architecture to Follow: `:core:design-system` component conventions.
- Existing Files to Reuse: Task 01's mapper.
- Files to Create: `SkillTreeStateRenderer.kt`.
- Files to Modify: None.
- Implementation Details: `SkillTreeStateRenderer(state: SkillState, unlockCondition: String? = null, modifier: Modifier = Modifier)` — pure presentational, no domain logic.
- Business Rules: `Locked` state requires `unlockCondition` to render specific text; falls back gracefully per §18 if absent.
- Validation: N/A. Error Handling: Per §18.
- Security: N/A. Performance: `@Stable` parameters.
- Localization: Full string-resource coverage. RTL: Full mirroring.
- Analytics: N/A.
- Tests: `SkillTreeStateRendererUiTest.kt`.
- Documentation: KDoc per §28.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working shared component.
- Definition of Done: All UI tests (six-state rendering, Locked-with-condition, RTL) green.

**Task 03 — Migrate A.5's Skill Tree Map to Use the Shared Renderer**
- Task ID: K-03-T03
- Objective: Remove duplicated mapping logic from `:feature:learn`, delegate to the shared component.
- Why This Is Required: Completes the centralization; leaving A.5's original inline mapping in place alongside this new shared one would be exactly the kind of duplicated/parallel logic the feature is meant to eliminate.
- Existing Architecture to Follow: A.5's existing skill-tree map screen structure.
- Existing Files to Reuse: A.5's `K-01 Quran Skill Tree Map` composable.
- Files to Create: None.
- Files to Modify: A.5's skill-tree map screen implementation.
- Implementation Details: Replace inline per-state visual branching with calls to `SkillTreeStateRenderer` per node.
- Business Rules: Zero visual regression for existing Quran/Arabic/Tajweed skill-tree rendering (behavioral-equivalence expectation, consistent with the backend's B-01 gate).
- Validation/Error Handling/Security: N/A beyond Task 02's coverage.
- Performance: No regression in list/grid rendering performance for a full skill tree.
- Localization: N/A (already covered). RTL: N/A (already covered).
- Analytics: N/A.
- Tests: Visual regression test (screenshot comparison if the platform's test tooling supports it) confirming A.5's skill tree renders identically before/after migration.
- Documentation: N/A (migration task).
- Dependencies: Task 02.
- Do Not Change: A.5's navigation/interaction logic (only the visual-rendering delegation changes).
- Expected Result: A.5 fully delegating to the shared renderer.
- Definition of Done: Visual regression test passes; no duplicated mapping logic remains in `:feature:learn`.

## 30. Definition of Done
`SkillTreeStateRenderer` and `SkillStateVisualMapper` live in `:core:mastery-engine`, exhaustively covering all six canonical states with correct, non-punitive `Needs Refresh` treatment and specific `Locked` unlock-condition display; A.5's skill-tree map fully migrated to consume it with zero visual regression.

## 31. Final Verification Checklist
- [ ] All six states covered by the mapper (exhaustive, compile-time enforced)
- [ ] `Locked` renders specific unlock-condition text
- [ ] `Needs Refresh` uses gentle, non-punitive visual language (verified, not assumed)
- [ ] Full EN/HI/AR/UR localization + RTL mirroring verified
- [ ] A.5's skill-tree map migrated with zero visual regression (screenshot/visual test)
- [ ] No duplicated state-to-visual mapping remains anywhere in `:feature:learn`
- [ ] Component is `@Stable`/`@Immutable`-annotated to avoid unnecessary recomposition in large trees
