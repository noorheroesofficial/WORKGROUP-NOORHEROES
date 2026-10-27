**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 058 — Learn Tab Landing / Quran Learning Home (Skill Tree Map)

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **A5 — Learn Tab Landing / Quran Learning Home (Skill Tree Map)**.
- Surface: **screen**. Number is controlled review order, not a forced linear user journey.
- Execution status: **Preserve all literal Frame 1 text; source sample statistics are fixtures only and religious strings remain subject to source verification.**.
- Journey entry / previous screen: Bottom nav "Learn" tab, Home "Continue Learning".
- Next screen(s) / result: Surah Learning, Arabic Letters, Tajweed, Quran Game modes.
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_A5_Quran_Arabic_Learning.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Child App (1-12)/Feature_A5_Quran_Arabic_Learning.md>); **§1.18 row 1; §1.7; §2; §6; §13**.
- Current mobile reference: [NoorHeroes current preview](https://noorheroes.figma.site/) → selector **Skill Tree**; exact text captured below.
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: [Quran Learning Home - Skill Tree Map](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1100-2) — `1100:2`. Exact/closest named existing frame; preserve purpose and copy; theme/player subtype must be checked
- Frame 2 container: `1085:13003`; visual reference: [Quran & Arabic Learning](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1085-16521) — `1085:16521`. Related enhanced feature hub for visual patterns only; not an exact screen equivalent
- Reference qualification: [].
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- [Feedback.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Learn/Feedback.png>)
- [Skill Tree-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Learn/Skill Tree-01.png>)
- [Skill Tree-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Learn/Skill Tree-02.png>)
- [Skill Tree-03.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Learn/Skill Tree-03.png>)
- [Skill Tree-04.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Learn/Skill Tree-04.png>)
- [Skill Tree-05.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Learn/Skill Tree-05.png>)
- [Skill Tree-06.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Learn/Skill Tree-06.png>)
- [Skill Tree-07.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Learn/Skill Tree-07.png>)
- [Skill Tree-08.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Learn/Skill Tree-08.png>)
- [Surah Practice-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Learn/Surah Practice-01.png>)
- [Surah Practice-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Learn/Surah Practice-02.png>)
- Blueprint alignment:
- [01-quran-skill-tree-map.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A5_Quran_Arabic_Learning/KMP/01-quran-skill-tree-map.md>)
- [02-placement-check-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A5_Quran_Arabic_Learning/KMP/02-placement-check-flow.md>)
- [03-surah-learning-verse-practice.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A5_Quran_Arabic_Learning/KMP/03-surah-learning-verse-practice.md>)
- [04-recitation-recorder-zero-retention-capture.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A5_Quran_Arabic_Learning/KMP/04-recitation-recorder-zero-retention-capture.md>)
- [05-arabic-letters-learning-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A5_Quran_Arabic_Learning/KMP/05-arabic-letters-learning-flow.md>)
- [06-tajweed-learning-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A5_Quran_Arabic_Learning/KMP/06-tajweed-learning-flow.md>)
- [07-quran-game-modes.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A5_Quran_Arabic_Learning/KMP/07-quran-game-modes.md>)
- [08-daily-quiz-learn-tab-experience.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A5_Quran_Arabic_Learning/KMP/08-daily-quiz-learn-tab-experience.md>)
- [09-spaced-review-needs-refresh-prompt.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A5_Quran_Arabic_Learning/KMP/09-spaced-review-needs-refresh-prompt.md>)
- [10-progressive-hint-overlay.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A5_Quran_Arabic_Learning/KMP/10-progressive-hint-overlay.md>)
- [11-islamic-fact-detail-mastery-celebration.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A5_Quran_Arabic_Learning/KMP/11-islamic-fact-detail-mastery-celebration.md>)
- [12-parent-progress-report-in-app.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A5_Quran_Arabic_Learning/KMP/12-parent-progress-report-in-app.md>)
- [13-parent-ai-microphone-permission-control.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A5_Quran_Arabic_Learning/KMP/13-parent-ai-microphone-permission-control.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: - CL-11 See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Enable Learn Tab Landing / Quran Learning Home (Skill Tree Map) in the established A5 journey. Entry: Bottom nav "Learn" tab, Home "Continue Learning". Required outcome: Surah Learning, Arabic Letters, Tajweed, Quran Game modes.

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

**FR-1** Learn Tab entry point ("Quran Learning Home") shows a skill-tree map with mastery indicators, organized by Surah/skill-node, plus mode selectors for Quran Game variants and a placement-check option for new learners (source: Blueprint screen catalog, "Quran Learning (Quran Game Hub)").

**FR-2** Skill Tree states are exactly: `Locked → Ready → Learning → Practicing → Mastered → Needs Refresh` (source §6.3/§21.9). A node's `Locked` state must display what prerequisite unlocks it, not just a generic lock.

**FR-5** Quran Game modes must include at minimum: ayah ordering, listen-and-select matching ayah, find-the-missing-word, surah-name-to-theme matching (child-safe/approved context only), recitation echo with pronunciation coaching, and progressive-reveal memorization (source §21.9 "Quran Game" game ideas).

**FR-8** Surah Learning screen shows ayah-by-ayah list with audio, a translation toggle, Tajweed-rule highlighting inline with the text, and a recitation recorder; actions: listen, repeat, record pronunciation attempt, request a hint, mark ayah as practiced (source: Blueprint screen catalog "Surah Learning").

**FR-13** Parent must be able to disable microphone/AI pronunciation features per child (not just globally) from Parental Controls (cross-ref C.23); when disabled, all recitation practice defaults to listen-and-self-assess mode app-wide for that child, with no UI path to bypass this setting from within the Learn tab.

**FR-15** Daily Quiz (Learn-tab-specific instance, shared engine with A.8) assembles exactly 5 questions from recently-learned content plus identified weak skills; question types: multiple choice, sequence, true/false, image match, audio match; immediate explanation shown after each answer; incorrect answers enter a short retry set within the same session (source §21.9).

**FR-17** Parent-facing Quran/Quiz reports must show concepts/skills, not just a raw numeric score (source §21.9: "Parent report shows concepts, not just a score").

**FR-19** Islamic Facts surfaced within or adjacent to Learn-tab content must carry: locale/age-banded text, topic and related-content linkage, primary/secondary source references, scholar approval and version, an explanation, a linked quiz item, and jurisprudential-scope/exclusion notes where relevant (source §21.9 "Islamic Facts").

**FR-20** Adaptive difficulty: lesson difficulty must adjust based on performance (source: Blueprint use case "Get adaptive lesson") — implemented via the mastery-score/skill-state model, not a separate disconnected difficulty slider.

**FR-21** Quran content data integrity: Ayah text itself is never editable post-seed (verified-source-seeded once); only translations, tafseer notes, and learning metadata are versioned/editable, each requiring scholar sign-off before publish (source: Admin Quran Management module rules, cross-referenced here as a hard content-integrity constraint this feature's read path must respect).

## 4. Exact content specification

### Current mobile source — exact captured text

```text
Quran Learning
⭐
12 skills mastered
📖
✓
Al-Fatiha
7 ayahs
⭐
✓
Al-Ikhlas
4 ayahs
🌙
Al-Asr
3 ayahs
📚
Al-Falaq
5 ayahs
ا
✓
Letters A–H
8 letters
ن
Letters I–N
7 letters
🌟
▶
Al-Nas
6 ayahs
🔄
↻
Tajweed 1
Ikhfa
🔒
Al-Kawthar
3 ayahs

Want to check your current level? Placement check · not connected

Home
Learn
Stories
Rewards
Profile
```

### Frame 1 — exact layer text (separate source; differences need approval)

```text
Home
Stories
Rewards
Profile
Learn
Noorani
Learn Quran
7d
340
Surah Journey
Arabic Letters
Al-Fatiha Progress: 5 of 7 Ayahs
Gentle step-by-step recitation journey
۞
12 Mastered
3 In Progress
الفَاتِحَة ١-٣
Al-Fatiha: Verse 1–3
The Opening (Pt 1)
70%
الفَاتِحَة ٤-٥
Al-Fatiha: Verse 4–5
Start
الفَاتِحَة ٦-٧
Al-Fatiha: Verse 6–7
حُرُوفُ المَدّ
Tajweed: Madd Letters
Revisit together
سُورَةُ الإِخْلَاص
Surah Al-Ikhlas
سُورَةُ الفَلَق
Surah Al-Falaq
Daily Tajweed Quest
Practice Ayah 2 Makhraj (+20 stars)
Play
```

### Requirement-driven fields and content roles

- Not supplied by this source; resolve before execution.

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Retain spatial skill path with a linear accessible reading alternative. Verse-practice layout gives verified Arabic highest visual weight, independent translation/transliteration controls and per-ayah audio/conditional recorder. Exercises focus on one bounded task, partial hint and accessible alternatives to drag/tracing.

- Preserve content order and screen purpose. Use a vertical auto-layout content stack; horizontal inset 20, base spacing 4/8/12/16/24/32; card content padding 12–16. Keep compact controls next to their labels; align headings and cards to one column edge.
- Use existing cream `#FAF7F0`, surface `#FFFFFF`, ink `#1C2B33`, teal `#0E7C7B`, gold `#D4A24C`. Gold/bright teal are accents, not untested small-text colors. Body 14/16; heading 20/24; brand-only display 28/32. Preserve actual font assets; PRD Latin sans, display serif, separate verified Arabic content font.
- Do not import Frame 2's sample statistics, claims, religious text, section additions or combined desktop layouts. Borrow hierarchy, restrained surface separation and image framing only where they support this surface.
- Screen viewport is separate from long content height. Use vertical overflow when content exceeds available height; header/footer may be fixed only with bottom and top content clearance. At 320/360/390/420 logical widths, long labels wrap. At 200% text scale, stack grids or allow scrolling; no fixed text block height or sacred-text ellipsis.
- Essential touch target≥44×44 logical units; younger-child primary tasks≥56 where A2 specifies. Decorative icons have no hit targets. Assets retain aspect ratio; no text burned into illustrations. Safe area and keyboard must never obscure the current action.
- Source frames, unrelated screens and existing design direction remain unchanged. Token/component changes require separate review; never detach or globally mutate a source instance to fix this screen.

## 6. Screen states and conditional scenarios

- Default as described in cited source
- Source-specified skeleton loading
- Cached offline view; only locally available actions enabled
- Source-specified empty content if applicable



Only apply states that belong to this surface. List-only empty/skeleton states are not added to legal documents or static intros. Network submit has a pending/timeout/retry result; retry preserves draft and must not duplicate a server-confirmed operation. Voice states need consent + OS grant; denial supplies listen/text/manual alternative. Loading/error/disabled/offline wording missing from source is a content approval gap.

<details><summary>Authoritative state/edge source context — apply screen-relevant cases, not all cases indiscriminately</summary>

### 1.10 Edge Cases

1. Child completes a skill node's assessment with borderline mastery score (e.g., exactly at the mastery threshold) → system rounds in the child's favor for the *state transition* (Practicing → Mastered) but the underlying continuous mastery score still feeds future spaced-repetition-decay scheduling accurately — borderline cases are not penalized twice.
2. Parent disables microphone mid-session while the child is actively in a recitation-recording flow → the in-progress recording UI must gracefully exit to listen-only mode on the next app-state check (not abruptly crash or leave a dangling "record" button that silently fails); per the standing Parent Dashboard rule, the change can apply at the next session rather than instantly interrupting, but must never leave the child stuck on a broken control if it does interrupt mid-session.
3. Child attempts the same quiz question multiple times across different days (e.g., it recurs in the weak-skills pool) → repeated correct answers should reduce its weak-skill priority over time (the system must not keep re-surfacing an already-remastered concept indefinitely).
4. AI Pronunciation Service returns a high-confidence score that is nonetheless wildly inconsistent with the child's historical performance trend (e.g., sudden perfect score after weeks of struggle, possibly due to background noise/false positive) → flagged internally as an anomaly for model-quality monitoring, but the child still simply sees positive feedback (a false positive in the child's favor is a lower-severity issue than a false negative that discourages a child, so the UX defaults to "do not punish for model uncertainty in either direction" — true uncertainty triggers fallback per FR-12, but a too-good-to-be-true score isn't second-guessed to the child's face).
5. Child's device has no microphone hardware at all (rare, e.g., certain tablets) → recitation-recording UI is hidden entirely (not shown-disabled), identical UX to the parent-disabled case, determined via device capability detection at app start.
6. Spaced-review decay logic computes multiple nodes simultaneously due for refresh on the same day → system caps the number of "Needs Refresh" prompts surfaced at once (e.g., max 2 per day) to avoid overwhelming the child, queuing the remainder for subsequent days rather than dumping all due-reviews simultaneously.
7. Child switches locale mid-curriculum (e.g., from English UI to Arabic UI) → translation/transliteration display updates immediately; the underlying Arabic ayah text and skill-tree progress state remain unchanged (progress is locale-independent, tied to the universal ayah/skill identifiers, not to a locale-specific content version).
8. Hint is requested on a question type that doesn't have a meaningful "partial" hint (e.g., true/false) → falls back to an explanatory micro-hint (e.g., a related fact nudge) rather than a no-op or a broken UI state.
9. Child completes a placement check that places them past Surah-tree nodes that have configured Tajweed-rule prerequisites not yet individually verified as mastered → system either (a) marks prerequisite Tajweed nodes as provisionally "Ready" pending a light confirmation check, or (b) explicitly schedules them for near-term review — never silently skips foundational Tajweed rules entirely based on a placement check alone, since recitation correctness depends on them.
10. Network drops mid-recitation-recording upload → recording is preserved locally and retried (not discarded), but per FR-11's retention rule, once successfully processed server-side and feedback returned, the raw audio is still deleted post-processing even after a retry path (the retry exception does not create a longer-retention loophole).
11. Two siblings practice the same Surah on a shared device on the same day → each child's mastery/progress state, recording, and AI feedback are fully isolated per `child_id`; no cross-contamination of spaced-review scheduling or weak-skill pools.
12. A scholar-issued correction updates a Tajweed rule's approved example or a translation mid-curriculum (content versioning) → children with in-progress mastery of that node retain their progress state (mastery isn't reset by a content text update), but newly-served example content reflects the corrected version going forward.

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| AI Pronunciation Service unavailable/timeout | Falls back to "compare with recorded reference example" self-assessment mode, no error shown to child, logged for ops monitoring |
| Microphone permission denied at OS level | Recitation UI silently switches to listen-only mode; a one-time non-blocking explainer may inform the child/parent why (no repeated nagging) |
| Quiz service unavailable | Daily Quiz widget/screen shows a friendly "quiz will be ready again soon" message, does not block access to other Learn-tab content |
| Skill-tree data fetch failure | Cached last-known skill-tree state rendered with an "may be slightly out of date" indicator rather than a blank/broken map |
| Recording upload failure (network) | Local retry per Edge Case 10; if retries exhaust, child is informed gently ("let's try that again later") and can re-attempt fresh rather than being stuck |
| Ayah audio media fails to load | Retry with backoff; falls back to a lower-bitrate/alternate CDN source if configured before surfacing a hard error |

### 1.12 Empty States
- New child, zero skill-tree progress → guided placement-check offer + a clearly marked "start from the beginning" alternative, never a blank map.
- Zero quiz history yet → Daily Quiz widget shows a friendly first-time framing rather than an empty score history chart.
- Parent Quran Progress Report with zero activity yet → "Once [Child] starts practicing, you'll see their progress here."

### 1.13 Loading States
- Skill-tree map: skeleton node-grid shimmer.
- AI pronunciation feedback: explicit "Listening... checking your recitation" state (sets honest expectation that this takes a few seconds, distinct from instant UI feedback elsewhere in the app).

### 1.14 Offline States
- Downloaded ayah audio and lesson content fully usable offline (listen/repeat/trace flows); AI pronunciation coaching requires connectivity (model inference is server-side) — offline recitation attempts queue locally and are either processed on reconnect or the child is clearly told this feature needs internet, with self-assessment as the immediate offline alternative.
- Quiz: a pre-downloaded subset of likely-quiz-content can be cached for offline quiz attempts, syncing results on reconnect with idempotent submission (per the general pattern established in A.2/A.3).

### 1.15 Permission States
- **Microphone:** OS-level permission + parent-level toggle (C.23) both gate recording features; both must be true for recording UI to appear; either being false routes to listen-only mode, no separate "request permission" nag once denied at the OS level beyond the platform-standard one-time re-prompt affordance.

</details>

## 7. Interactions and navigation

- {"element": "Ready/Learning/Practicing node", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "Correct Surah/Arabic/Tajweed exercise", "destination": "Correct Surah/Arabic/Tajweed exercise", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Locked node", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "Display prerequisite without launching", "destination": "Display prerequisite without launching", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Needs Refresh node", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "Gentle relevant review session", "destination": "Gentle relevant review session", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Placement check", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "Placement Check", "destination": "Placement Check", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Mode selector", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "Mode Selector Sheet", "destination": "Mode Selector Sheet", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}

For every action below, use the cited preconditions and source validation. Preserve the invoking route and selected child. Back/cancel dismisses only the current overlay or returns to the invoking screen, preserving drafts and completed progress where specified. Unavailable actions remain visibly labeled with their reason and never activate. Permission prompts occur only after parent consent and a deliberate related action. A prototype simulates outcomes; it never validates identity, grants permissions, charges money or mutates production data.

Verified current-preview controls, retained to prevent omitted clickable elements:

- {"disabled": false, "label": "Search learning content", "placeholder": null, "tag": "BUTTON", "text": "", "type": null}
- {"disabled": true, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Placement check · not connected", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Home", "type": "button"}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Learn", "type": "button"}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Stories", "type": "button"}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Rewards", "type": "button"}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Profile", "type": "button"}

For any captured control absent from an explicit action above, reconcile it against the screen-specific source below before wiring. Do not connect it to a convenient unrelated screen. Mark it **unresolved, non-executable** until its actual destination/state is confirmed; the navigation appendix reports this limitation. Decorative source-layer names are not automatically click targets.

<details><summary>Screen-specific PRD specification / click behavior</summary>

#### Screen: Quran Learning Home (Skill Tree Map)

- **Purpose:** Orient the child within their overall learning journey and let them choose what to practice.
- **Components:** Scrollable/zoomable tree or path visualization of skill nodes grouped by Surah/topic, mode-selector entry point, mastery summary header (e.g., "12 skills mastered"), placement-check re-offer (for returning low-activity users, subtly, not naggy).
- **States:** Loading (skeleton tree), Default, Error (cached fallback per §1.11), First-time (placement-check prominent).
- **Accessibility:** Tree navigable linearly via screen reader (a logical reading order independent of the visual spatial layout, with each node's state announced).
- **Responsive Rules:** Tree layout reflows for tablet (wider node spacing) without changing the underlying logical structure.



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
3. Create `NH/Enhanced/058/Learn_Tab_Landing_Quran_Learning_Home_Skill_Tree_Map/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Learn_Tab_Landing_Quran_Learning_Home_Skill_Tree_Map`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] A5 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
