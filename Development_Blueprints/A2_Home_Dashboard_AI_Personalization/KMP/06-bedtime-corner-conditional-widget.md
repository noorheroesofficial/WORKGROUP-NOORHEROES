# K-06 — Bedtime Corner Conditional Widget

## 1. Feature Context
NoorHeroes Child App (KMP). Renders the conditional, dimmed-theme "Bedtime Corner" section that appears only within the parent-configured bedtime window.

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization

## 3. Sub-feature
2.6 Bedtime Corner Conditional Widget (ID: K-06)

## 4. Objective
Build the Bedtime Corner Composable that emits no node at all when the corresponding state is null/absent (never an empty card/placeholder), automatically applies the dimmed Bedtime theme variant to itself regardless of the rest of Home's theme, and routes to Bedtime Mode/Audio Bedtime Player.

## 5. Business Requirements
Per PRD FR-12, Edge Case 4, §2.1, §7 item 2:
- Section present only within the parent-configured bedtime window for that specific child; server evaluates the window and returns `null` outside it (present key, null value).
- Client must render nothing (no node emitted) when null — not an empty/placeholder card.
- Bedtime Corner theme automatically applies the dimmed/dark theme variant to this single widget even if the rest of Home is in light theme.
- Cached bedtime audio playable offline if pre-downloaded.

## 6. Existing Architecture
Plugs into K-01's `SectionState`/`HomeUiState`. Reuse the platform's existing dark/dimmed theme definition (from `:core:design-system`) rather than defining a new theme locally.

## 7. Existing Code to Reuse
K-01's `SectionState`; `:core:design-system` dark/dimmed theme tokens; existing Bedtime Mode/Audio Player module (external feature, launched via navigation, not reimplemented here).

## 8. Files to Create
- `feature/home/src/commonMain/kotlin/.../components/BedtimeCornerWidget.kt`
- `feature/home/src/commonMain/kotlin/.../models/BedtimeCornerItem.kt`
- `feature/home/src/androidInstrumentedTest/.../BedtimeCornerAbsenceTest.kt`

## 9. Files to Modify
- `HomeScreen.kt`, `HomeUiState.kt` (K-01)

## 10. Backend Requirements
Consumes `sections.bedtime_corner` from B-01 (`null` when outside window, present object within window).

## 11. KMP Requirements
- Composable returns/emits nothing when `SectionState.Hidden` (mapped from backend `null`) — verified via a semantics-tree test asserting zero nodes for this section's test-tag when hidden.
- When present, wraps content in a locally-scoped dark/dimmed theme override (`CompositionLocalProvider` for the theme, scoped only to this Composable's subtree) independent of the rest of Home's theme.
- Tap routes to Bedtime Mode / Audio Bedtime Player via deep link/content_id, per PRD §2.3.
- Content playable offline if pre-downloaded (reuse existing offline-download availability check).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`sections.bedtime_corner` — `null` outside window, `{ content_id, ... }` within window — per B-01 §13.

## 14. Database Requirements
Not applicable directly.

## 15. Validation
Client must not perform its own bedtime-window time calculation to decide visibility — the server (B-01) is the single source of truth per FR-12; client only reacts to `null` vs. present.

## 16. Authentication
N/A (inherits session).

## 17. Authorization
N/A at UI layer.

## 18. Error Handling
Section absent on error (fails safe to "not shown"), per PRD §2.2 table — identical visual outcome to the normal "outside window" `null` case, but should be distinguishable in internal telemetry (error vs. legitimately-outside-window).

## 19. Offline First
Cached bedtime audio playable offline if pre-downloaded, per PRD §2.2/§1.14.

## 20. Local Data
Reads from `HomeUiState`; offline playability check reads existing offline-download local store.

## 21. Localization
Widget copy via string resources; content title pre-localized.

## 22. RTL
Dimmed-theme card layout mirrors correctly; verify the "wind-down" visual composition (moon/star icon placement) is appropriately mirrored per Design System RTL guidance rather than literally flipped if that would look wrong (confirm against Figma RTL mockup, per PRD §2.5 Bedtime Corner Arabic RTL prompt).

## 23. Analytics
`bedtime_corner_shown`, `bedtime_corner_entered`.

## 24. Performance
Theme-scoping via `CompositionLocalProvider` must not force a recomposition of the rest of `HomeScreen` — verify scoping is correctly localized.

## 25. Security
N/A beyond standard scoped-session access.

## 26. Library Requirements
Compose Multiplatform theming APIs, existing navigation library.

## 27. Testing
- Compose UI: zero semantics nodes emitted when state is `Hidden`/null (explicit absence test, not just "invisible").
- Compose UI: dimmed theme correctly scoped to only this widget's subtree when rest of Home is in light theme.
- Compose UI: tap routes correctly to Bedtime Mode/Audio Player.

## 28. Documentation
KDoc explaining the "emit nothing" requirement explicitly (a common mistake is rendering an invisible/zero-height placeholder instead of truly emitting no node, which can still affect semantics-tree/accessibility traversal).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define `BedtimeCornerItem` Model**
- Objective: Typed model for widget content.
- Why Required: Type-safe mapping from B-01's response.
- Existing Architecture to Follow: K-01 conventions.
- Existing Files to Reuse: `SectionState`.
- Files to Create: `models/BedtimeCornerItem.kt`
- Files to Modify: `HomeUiState.kt`
- Implementation Details: `data class BedtimeCornerItem(contentId, title, audioUrl, isDownloaded)`; mapped to `SectionState.Hidden` when backend value is `null`.
- Business Rules: `null` → `Hidden`, not `Error`.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: `@Immutable`.
- Localization: `title` pre-localized.
- RTL: N/A.
- Analytics: N/A.
- Tests: Mapping unit test for null-to-Hidden.
- Documentation: KDoc.
- Dependencies: K-01 Task 01.
- Do Not Change: N/A.
- Expected Result: Model defined.
- Definition of Done: Unit test passes.

**Task 02 — Build `BedtimeCornerWidget` Composable (True Absence + Scoped Theme)**
- Objective: Widget that emits nothing when hidden and scopes its own dark theme when present.
- Why Required: FR-12, PRD §7 item 2, §2.1 theme requirement.
- Existing Architecture to Follow: `:core:design-system` dark theme tokens; Compose `CompositionLocalProvider` pattern.
- Existing Files to Reuse: Existing dark/dimmed theme definition.
- Files to Create: `components/BedtimeCornerWidget.kt`
- Files to Modify: `HomeScreen.kt`
- Implementation Details: `if (state is SectionState.Hidden) return` (no Composable emitted) at the top of the function, before any layout code; when `Content`, wrap in `CompositionLocalProvider(LocalAppTheme provides DimmedBedtimeTheme) { ... }` scoped only to this subtree.
- Business Rules: True absence, not zero-height/invisible.
- Validation: N/A.
- Error Handling: Also returns nothing on `Error` state (fails safe).
- Security: N/A.
- Performance: Scoped `CompositionLocalProvider` avoids full-screen recomposition.
- Localization: String resources.
- RTL: Verified per Figma Bedtime Corner RTL mockup.
- Analytics: `bedtime_corner_shown` fired on successful (non-hidden) resolution; `bedtime_corner_entered` on tap.
- Tests: Semantics-tree absence test (zero nodes with this widget's test-tag when hidden); theme-scoping test (rest of screen unaffected).
- Documentation: KDoc on the "true absence" requirement.
- Dependencies: Task 01.
- Do Not Change: Do not render an invisible/zero-alpha placeholder instead of true absence.
- Expected Result: Correctly conditional widget.
- Definition of Done: Absence and theme-scoping tests pass.

## 30. Definition of Done
Bedtime Corner renders with true absence when hidden/error, correctly scopes its own dimmed theme when present, and routes correctly to Bedtime Mode; all tests green.

## 31. Final Verification Checklist
- [ ] Zero semantics nodes emitted when hidden (verified, not assumed)
- [ ] Dimmed theme scoped only to this widget, rest of Home unaffected
- [ ] Client does not perform its own bedtime-window time calculation
- [ ] Fails safe (absent) on error, same visual as legitimately-outside-window
- [ ] Cached audio playable offline if pre-downloaded
- [ ] All tests pass
