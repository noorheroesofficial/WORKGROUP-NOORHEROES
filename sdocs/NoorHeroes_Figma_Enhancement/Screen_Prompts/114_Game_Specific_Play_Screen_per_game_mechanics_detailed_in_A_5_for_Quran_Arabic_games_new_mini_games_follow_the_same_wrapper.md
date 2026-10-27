**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 114 — Game-Specific Play Screen (per game, mechanics detailed in A.5 for Quran/Arabic games; new mini-games follow the same wrapper)

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **A10 — Game-Specific Play Screen (per game, mechanics detailed in A.5 for Quran/Arabic games; new mini-games follow the same wrapper)**.
- Surface: **screen**. Number is controlled review order, not a forced linear user journey.
- Execution status: **BLOCKED for exact approved copy: no exact Frame 1 counterpart verified. Do not fabricate copy, Arabic, educational items, user data or stats.**.
- Journey entry / previous screen: Game Session Loading.
- Next screen(s) / result: Session Completion.
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_A10_Games_Module.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Child App (1-12)/Feature_A10_Games_Module.md>); **§1.18 row 6; §1.7; §2; §6; §13**.
- Current mobile reference: **Missing independently mapped current-site screen.**
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: **Missing corresponding screen reference.** Do not substitute a visually related hub as functional evidence.
- Frame 2 container: `1085:13003`; visual reference: [Skill-Reinforcement Games Hub](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1085-17757) — `1085:17757`. Related enhanced feature hub for visual patterns only; not an exact screen equivalent
- Reference qualification: ['Required layout has no verified exact source-frame match; access exact approved content before execution.'].
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- [Game Complete-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Games/Game Complete-01.png>)
- [Game Complete-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Games/Game Complete-02.png>)
- [Game Complete-03.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Games/Game Complete-03.png>)
- [Games Hub-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Games/Games Hub-01.png>)
- [Games Hub-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Games/Games Hub-02.png>)
- [Games Hub-03.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Games/Games Hub-03.png>)
- [Games Hub-04.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Games/Games Hub-04.png>)
- [Games Hub-05.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Games/Games Hub-05.png>)
- Blueprint alignment:
- [01-games-hub-screen-skill-area-filtering.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A10_Games_Module/KMP/01-games-hub-screen-skill-area-filtering.md>)
- [02-game-session-wrapper-return-destination-navigation.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A10_Games_Module/KMP/02-game-session-wrapper-return-destination-navigation.md>)
- [03-game-evidence-reward-delegation.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A10_Games_Module/KMP/03-game-evidence-reward-delegation.md>)
- [04-session-abandonment-detection.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A10_Games_Module/KMP/04-session-abandonment-detection.md>)
- [05-offline-game-content-catalog-caching.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A10_Games_Module/KMP/05-offline-game-content-catalog-caching.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: - CL-03 See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Enable Game-Specific Play Screen (per game, mechanics detailed in A.5 for Quran/Arabic games; new mini-games follow the same wrapper) in the established A10 journey. Entry: Game Session Loading. Required outcome: Session Completion.

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

**FR-1** The Games Hub presents a tile grid of available games, with UI sections: Daily Quiz (entry point into the shared A.8 engine), Arabic Letters games (per A.5), and mini-game tiles grouped by skill area (source: NoorHeroes Blueprint screen catalog "Games — UI Sections: Daily Quiz, Arabic Letters games, mini-game tiles grouped by skill area").

**FR-2** Every game catalog entry must declare exactly one or more linked `skill_node_id` references (from A.9's domain-agnostic skill graph) — **a game with zero linked skill nodes cannot be published**, enforced as a hard validation rule, not a content-review guideline (source: hard platform rule, "Games always map to a learning skill — none are content-free filler").

**FR-3** Game difficulty is tiered by age band (4 to 6, 6 to 9, 9 to 12, 12 to 15, 15 to 18+, per the platform's standard age-group taxonomy), with each tier adjusting parameters such as time pressure, number of distractor options, and complexity of the underlying skill content — never the correctness-evaluation logic itself.

**FR-4** Within a single game session, difficulty may adapt based on in-session accuracy (consistent with A.5/§6.3's principle: "Accuracy changes difficulty; speed never outranks correctness" — a rule restated here as binding across every game in this hub, not just Quran Game specifically).

**FR-5** Every completed game session emits skill-evidence events to the shared Mastery Engine (A.9), using the same evidence contract as quiz attempts (FR shared with A.9 §3.4 `POST /v1/mastery/evidence`) — game-derived evidence is first-class, not a lesser/ignored signal.

**FR-6** Game session completion awards XP/Noor Heroes Points via the shared Reward Service (A.11), following the same accuracy-independent-participation-reward principle established in A.8 FR-5/A.9 FR-4 — a child who plays earnestly but performs poorly still receives a participation reward; accuracy affects mastery evidence, never the base reward.

**FR-7** On game-session completion, the child returns to the screen that launched the session (Home, Rewards, or the Games Hub itself) — never to an unrelated or unexpected destination (source: navigation table, "Game session, then back to launching screen").

**FR-8** The Games Hub tile grid must be filterable/groupable by skill area (Quran, Arabic, Tajweed, and any future domain per A.9's extensible domain registry), age-band-appropriate filtering applied automatically (a child only sees tiles appropriate to their own age band by default, with no manual override exposed to the child).

**FR-9** Replaying a completed game is always available (no re-locking after first completion, consistent with A.3's "rewatching is always available" principle for stories) — repeat play is explicitly encouraged for skill reinforcement, distinct from a content-consumption context where repetition might be less valuable.

**FR-10** A game entry tagged with Quran, Tajweed, or Dua content must pass the same scholar-review/content-governance pipeline as any other content of that type (cross-reference A.5/A.6's scholar-approval gates) before publish — "it's just a game" is never an exemption from content governance.

**FR-11** No game in this hub may implement loot-box mechanics, variable/randomized paid rewards, or purchasable in-game advantages — consistent with the platform-wide reward-economy rule (source §21.12: "No purchasing virtual currency in child mode... No loot-box mechanics or variable paid rewards").

**FR-12** Each game session is bounded in length (no infinitely-replayable single-session loop designed to maximize time-on-device) — a session has a clear natural end state (e.g., a fixed round count or a completion condition), after which the child is returned per FR-7, rather than auto-continuing into a new round without an explicit child action.

## 4. Exact content specification

### Requirement-driven fields and content roles

- Not supplied by this source; resolve before execution.

**Exact copy unavailable: execution blocked for copy-dependent design.** Locate the authoritative content registry/original frame; do not insert placeholder, paraphrased or AI-generated copy. This document still specifies the required surface so it is not omitted.

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Two-column mobile game grid grouped/filterable by domain; Daily Quiz is pinned near top. Age/learning tier is informational, server-selected. Game completion preserves calm participation reward and explicit Play Again/Done; no automatic endless rounds.

- Preserve content order and screen purpose. Use a vertical auto-layout content stack; horizontal inset 20, base spacing 4/8/12/16/24/32; card content padding 12–16. Keep compact controls next to their labels; align headings and cards to one column edge.
- Use existing cream `#FAF7F0`, surface `#FFFFFF`, ink `#1C2B33`, teal `#0E7C7B`, gold `#D4A24C`. Gold/bright teal are accents, not untested small-text colors. Body 14/16; heading 20/24; brand-only display 28/32. Preserve actual font assets; PRD Latin sans, display serif, separate verified Arabic content font.
- Do not import Frame 2's sample statistics, claims, religious text, section additions or combined desktop layouts. Borrow hierarchy, restrained surface separation and image framing only where they support this surface.
- Screen viewport is separate from long content height. Use vertical overflow when content exceeds available height; header/footer may be fixed only with bottom and top content clearance. At 320/360/390/420 logical widths, long labels wrap. At 200% text scale, stack grids or allow scrolling; no fixed text block height or sacred-text ellipsis.
- Essential touch target≥44×44 logical units; younger-child primary tasks≥56 where A2 specifies. Decorative icons have no hit targets. Assets retain aspect ratio; no text burned into illustrations. Safe area and keyboard must never obscure the current action.
- Source frames, unrelated screens and existing design direction remain unchanged. Token/component changes require separate review; never detach or globally mutate a source instance to fix this screen.

## 6. Screen states and conditional scenarios

- Default as described in cited source



Only apply states that belong to this surface. List-only empty/skeleton states are not added to legal documents or static intros. Network submit has a pending/timeout/retry result; retry preserves draft and must not duplicate a server-confirmed operation. Voice states need consent + OS grant; denial supplies listen/text/manual alternative. Loading/error/disabled/offline wording missing from source is a content approval gap.

<details><summary>Authoritative state/edge source context — apply screen-relevant cases, not all cases indiscriminately</summary>

### 1.10 Edge Cases

1. A child's age band changes (birthday rollover) mid-way through frequent play of a specific game tile → the next session launched reflects the new age band's difficulty tier; historical session/evidence data is preserved and attributed under whichever tier was active at the time of each past session (no retroactive reclassification).
2. A game is linked to skill nodes across two different domains simultaneously (e.g., a hypothetical cross-domain matching game) → completing it emits evidence correctly to both domains' respective skill states via the shared A.9 evidence contract, without conflation (consistent with A.9 Edge Case 3).
3. A child abandons a game session mid-round (closes the app or navigates away) → no reward or evidence is recorded for that incomplete session (distinct from A.8's quiz-resume pattern, since games are typically short enough that resuming a specific mid-round state is less valuable than simply restarting fresh — this is a deliberate design simplification specific to Games, documented as such rather than an oversight) — the child can simply start a new session at any time per FR-9.
4. Admin disables/unpublishes a game while a child has an active in-progress session → the current session is allowed to complete gracefully (not abruptly terminated), but the tile no longer appears in the Hub for future sessions once the change propagates.
5. A child plays the same game many times in rapid succession in an apparent attempt to farm participation rewards → the shared Reward Service's existing daily-cap/anti-farming mechanisms (consistent with A.7's habit daily-cap pattern, generalized) apply — rewards beyond a reasonable daily threshold for a given game/skill combination taper or cap, while the child can still play for enjoyment/practice value without an artificial hard block on play itself.
6. Two age bands (e.g., 6 to 9 and 9 to 12) overlap in practice for a borderline-age child whose parent has configured a different effective learning level than their raw age would suggest (cross-reference A.1's Add Child "learning level" field) → difficulty tiering should respect the configured learning level where it diverges from raw age-band default, not blindly apply raw-age-derived difficulty.
7. A game's linked skill node is later deprecated/marked inactive in the skill graph (A.9 §4.4) → the game tile is automatically hidden/unpublished going forward (since it would otherwise violate FR-2's "must map to an active learning skill" intent), with historical evidence/session data preserved.
8. Offline play: a child plays a downloaded/cached game while offline → the session functions fully offline (most game mechanics are self-contained, similar to A.8's offline question-bank pattern), with evidence/reward events queuing for sync on reconnect, idempotently.
9. A child using an assistive-technology-only interaction path (per the accessibility requirement) completes a game meaningfully slower than a typical touch/drag interaction would allow within an in-game time-pressure mechanic → time-pressure-based difficulty parameters must have an accessibility-aware adjustment (extended or removed time pressure) rather than penalizing a child for using their necessary interaction method.
10. A new game is added to the catalog that reuses an existing skill node already heavily represented by other games/quizzes → no special handling needed; this is healthy content variety, though the Admin's content-distribution monitor (analogous to A.8's Assembly Monitor) may flag heavy skill-node concentration for editorial awareness.
11. A child plays a game, then immediately requests "Try Again" or replays — does this count as the "more than one session" requirement for A.9's no-single-session-mastery rule? → No: per A.9 FR-5, mastery requires evidence across genuinely distinct sessions (different calendar days or sufficiently time-separated attempts per A.9 §5 item 3's documented rule) — rapid immediate replay within the same sitting does not satisfy this, consistent with the shared Mastery Engine's existing anti-single-session-mastery protection, inherited automatically by Games since they use the same evidence pipeline.
12. A game session's evidence references a quiz-style question that has since been withdrawn for safety reasons (where a game internally reuses quiz-bank content) → the same withdrawn-question exclusion rule from A.8/A.9 applies identically, since Games route through the same shared evidence contract.

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Games Hub catalog fetch failure | Cached last-known catalog rendered with a subtle "may be outdated" indicator |
| Game asset (media/sprite) fails to load | Graceful retry with backoff; falls back to a simpler asset tier if configured, never a hard crash |
| Evidence/reward submission fails post-session (network) | Session completion screen still shows (the child's experience isn't blocked); evidence/reward queued for retry, consistent with A.9's general resilience pattern |
| Game tile references a since-deprecated skill node | Tile automatically hidden from the Hub (Edge Case 7), no error shown to the child |

### 1.12 Empty States
- A skill-area filter with zero available games for the child's age band → friendly "more games for this area are coming soon" message with a link to a populated skill area, consistent with A.3/A.6's empty-category pattern.

### 1.13 Loading States
- Games Hub: skeleton tile-grid shimmer.
- Individual game session: lightweight loading state appropriate to the specific game's assets (reusing each game's own loading pattern where it already exists per A.5).

### 1.14 Offline States
- Downloaded/cached games fully playable offline (Edge Case 8); non-downloaded games show a clear "connect to internet or download" affordance rather than a dead tile.

### 1.15 Permission States
- No new runtime permissions beyond what individual games may already require via their underlying mechanics (e.g., a tracing game's standard touch input — no microphone/camera involved in any game covered by this hub's standard catalog).

</details>

## 7. Interactions and navigation

- {"element": "Session Completion", "trigger": "Tap the corresponding source-defined control", "precondition": "Active correct child session; relevant content/permission/unlock state satisfied per cited requirements", "behavior": "Session Completion", "destination": "Session Completion", "validation": "Preserve cited source-specific validation; no simulated outcome may bypass parent gate, learned status, content unlock or offline availability", "back_cancel": "Dismiss overlay to originating screen; screen back returns to caller with context preserved; unresolved explicit destination must be approved", "unavailable": "Disabled or source-specific explanation when permission/unlock/content requirements fail"}

For every action below, use the cited preconditions and source validation. Preserve the invoking route and selected child. Back/cancel dismisses only the current overlay or returns to the invoking screen, preserving drafts and completed progress where specified. Unavailable actions remain visibly labeled with their reason and never activate. Permission prompts occur only after parent consent and a deliberate related action. A prototype simulates outcomes; it never validates identity, grants permissions, charges money or mutates production data.

Verified current-preview controls, retained to prevent omitted clickable elements:

- Not supplied by this source; resolve before execution.

For any captured control absent from an explicit action above, reconcile it against the screen-specific source below before wiring. Do not connect it to a convenient unrelated screen. Mark it **unresolved, non-executable** until its actual destination/state is confirmed; the navigation appendix reports this limitation. Decorative source-layer names are not automatically click targets.

<details><summary>Screen-specific PRD specification / click behavior</summary>

No independently named per-screen UX subsection exists. The PRD screen inventory entry, feature click-target table and functional requirements remain the authority; use research evidence and resolve unmatched targets before execution.

</details>

## 8. Motion and animation specification

| Trigger | Start → end / direction | Timing | Interruption / leave | Reduced motion | Figma approach |
|---|---|---|---|---|---|
| Approved forward/back action | Current frame→destination, preserving directional history | 250ms ease-in-out;no delay | Reversible with Back; cancel pending animation when leaving | Instant navigation or ≤100ms dissolve | Navigate to + Dissolve; matched-layer Smart Animate only after layer-name/structure check |
| Press/release enabled control | Rest→pressed→rest; preserve hit area | 100ms ease-out scale.96 (proposal);0ms delay | Release/cancel reverses; disabled has no activation | Color/border pressed feedback only | While pressing → Change to pressed; On click → approved action |



Timing not quoted from the PRD is a labeled design proposal. No loop, flashing or parallax is required. Animate compositor-friendly opacity/transform; never delay an enabled essential action. Stop all animation/media/recording simulation on leave; no second reward reveal on restore. Status/validation always has visible text/icon independently of motion.

## 9. Figma implementation instructions — future approved execution

1. Open the exact page/node links in section2. Confirm the source text/identity; stop if the references disagree or required copy is unavailable.
2. Locate the approved reference frame. Duplicate only that frame into a user-approved enhanced-design working area; preserve original nodes and IDs. If no frame exists, create only the missing requirement-driven surface after its layout/copy approval, using approved shared assets.
3. Create `NH/Enhanced/114/Game_Specific_Play_Screen_per_game_mechanics_detailed_in_A_5_for_Quran_Arabic_games_new_mini_games_follow_the_same_wrapper/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Game_Specific_Play_Screen_per_game_mechanics_detailed_in_A_5_for_Quran_Arabic_games_new_mini_games_follow_the_same_wrapper`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] A10 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
- [ ] Every captured product control has an approved trigger, precondition, destination/state and cancel/back result; no unresolved control is silently wired.
- [ ] Applicable states are visibly reviewable; retry/draft/permission-denial/resume behavior matches the cited rules. No irrelevant states were added.
- [ ] All body text/background pairs≥4.5:1 and large text≥3:1; status has text/icon, not color alone.
- [ ] Touch targets≥44×44; no clipped text or action overlap at320/360/390/420 widths or200% text scaling; Arabic/Urdu RTL tested with numeral exceptions.
- [ ] Motion timing/interruptibility matches section8; reduced motion retains all feedback; navigation is immediately available.
- [ ] Reference IDs and any new working-node IDs recorded; original and unrelated nodes unchanged.
- [ ] Sample data/price/religious verification provenance is identified; missing legal/localized/educational content blocks execution rather than being fabricated.
- [ ] Default and relevant alternate states captured as evidence and compared; screen approved by user before proceeding.

## 11. Review and correction instructions

Implement only this screen and its necessary local dependencies after approval. Do not modify unrelated screens or source frames. Report inaccessible references, missing requirements and unmatched controls. List changes, exact-copy comparison and acceptance checks performed, with evidence and created node IDs. Record unresolved questions. **Stop and wait for my review and approval before moving to another screen.**
