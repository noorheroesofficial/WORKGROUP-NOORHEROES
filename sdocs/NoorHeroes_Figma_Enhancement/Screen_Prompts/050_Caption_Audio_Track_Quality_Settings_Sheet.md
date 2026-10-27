**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 050 — Caption/Audio-Track/Quality Settings Sheet

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **A3 — Caption/Audio-Track/Quality Settings Sheet**.
- Surface: **overlay**. Number is controlled review order, not a forced linear user journey.
- Execution status: **BLOCKED for exact approved copy: no exact Frame 1 counterpart verified. Do not fabricate copy, Arabic, educational items, user data or stats.**.
- Journey entry / previous screen: Player settings icon.
- Next screen(s) / result: Resumes playback with new settings.
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_A3_Stories_Module.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md>); **§1.18 row 24; §1.7; §2; §6; §13**.
- Current mobile reference: **Missing independently mapped current-site screen.**
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: **Missing corresponding screen reference.** Do not substitute a visually related hub as functional evidence.
- Frame 2 container: `1085:13003`; visual reference: [Stories & Bedtime Hub](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1085-16216) — `1085:16216`. Related enhanced feature hub for visual patterns only; not an exact screen equivalent
- Reference qualification: ['Required layout has no verified exact source-frame match; access exact approved content before execution.'].
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- [Bedtime Player.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Stories/Bedtime Player.png>)
- [Choice.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Stories/Choice.png>)
- [Complete.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Stories/Complete.png>)
- [Moral Card.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Stories/Moral Card.png>)
- [Player.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Stories/Player.png>)
- [Stories-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Stories/Stories-01.png>)
- [Stories-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Stories/Stories-02.png>)
- [Stories-03.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Stories/Stories-03.png>)
- [Stories-04.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Stories/Stories-04.png>)
- [Stories-05.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Stories/Stories-05.png>)
- [Stories-06.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Stories/Stories-06.png>)
- [Stories-07.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Stories/Stories-07.png>)
- [Story Detail-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Stories/Story Detail-01.png>)
- [Story Detail-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Stories/Story Detail-02.png>)
- Blueprint alignment:
- [01-stories-library-category-discovery.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A3_Stories_Module/KMP/01-stories-library-category-discovery.md>)
- [02-story-detail-episode-unlock-presentation.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A3_Stories_Module/KMP/02-story-detail-episode-unlock-presentation.md>)
- [03-story-player-core-playback-engine.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A3_Stories_Module/KMP/03-story-player-core-playback-engine.md>)
- [04-interactive-choice-quiz-moment-overlays.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A3_Stories_Module/KMP/04-interactive-choice-quiz-moment-overlays.md>)
- [05-bedtime-mode-player-experience.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A3_Stories_Module/KMP/05-bedtime-mode-player-experience.md>)
- [06-story-completion-reward-moral-summary-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A3_Stories_Module/KMP/06-story-completion-reward-moral-summary-flow.md>)
- [07-offline-downloads-sync-stories.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A3_Stories_Module/KMP/07-offline-downloads-sync-stories.md>)
- [08-story-favorites-parent-gated-sharing.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A3_Stories_Module/KMP/08-story-favorites-parent-gated-sharing.md>)
- [09-parent-story-insights-in-app.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A3_Stories_Module/KMP/09-parent-story-insights-in-app.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: - CL-10
- CL-12
- CL-05
- CL-09 See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Enable Caption/Audio-Track/Quality Settings Sheet in the established A3 journey. Entry: Player settings icon. Required outcome: Resumes playback with new settings.

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

**FR-2** Library filters must include: age band, duration, language, format (video/audio/text), topic, downloaded-only, free/premium.

**FR-7** Story Player supports video, audio, and text formats with: play/pause, caption toggle, audio-track selection, quality selection, in-story interactive choice overlays, pause-and-quiz moments, and a moral-summary card at the end.

**FR-12** Bedtime Mode supports a parent-configured sleep timer that fades audio/dims screen and can auto-pause/auto-exit the player at expiry.

## 4. Exact content specification

### Requirement-driven fields and content roles

- Not supplied by this source; resolve before execution.

**Exact copy unavailable: execution blocked for copy-dependent design.** Locate the authoritative content registry/original frame; do not insert placeholder, paraphrased or AI-generated copy. This document still specifies the required surface so it is not omitted.

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Library retains category rails and filter affordances; Detail orders cover/synopsis/governance tags before episode rows and relevant stories. Player uses immersive media area and reachable overlay controls, never distort aspect ratio. Completion follows reward → moral → optional quiz → next learning.

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

1. Child completes Episode 2 exactly at the threshold boundary while offline (no connectivity to report completion) → local completion recorded immediately (unlocking Episode 3 locally for continued offline browsing), event queued with a client ID, reconciled with the server on reconnect; server is authoritative on conflict (e.g., if server-side threshold differs due to a mid-flight config change, server value wins on sync, but the child is never abruptly re-locked once unlocked locally without clear explanation).
2. A series' unlock-threshold configuration is changed by Admin after a child has already unlocked Episode 3 under the old rule → previously unlocked episodes remain unlocked (no retroactive re-locking); only future episodes are governed by the new threshold.
3. Child rapidly taps through interactive choice moments faster than the narration/animation completes → choice overlay inputs are debounced/queued so no choice is silently dropped or double-counted.
4. Two siblings share a device; Child A downloads a series, then the device switches to Child B who does not have entitlement to that series (different age band or parent restriction) → downloaded media remains on-device but is not exposed in Child B's Stories Library (entitlement-checked at the UI/data layer per active child session, not just at download time).
5. AI moral-summary generation service times out entirely (not just low-confidence, but unavailable) → falls back immediately to the human-reviewed fallback moral, same as the low-confidence path — never blocks the completion flow waiting on AI.
6. A bedtime-eligible story is started just before the bedtime window begins and finishes just after it starts → Bedtime Mode visual/narration treatment is evaluated at story-start time and held consistent for that session (does not flicker into dimmed mode mid-playback), but the ending dua/reflection treatment respects the window state at completion time if materially different.
7. Parent disables downloads entirely while a child has in-progress downloads → in-progress downloads are halted gracefully (not silently failed); already-completed downloads remain playable until parent additionally revokes offline access explicitly (two distinct controls: "allow new downloads" vs. "revoke existing offline content").
8. Child's locale changes mid-session (e.g., device language changed while app backgrounded) → on resume, captions/audio-track defaults re-evaluate to the new locale's available tracks; if the new locale lacks a dub, audio falls back to original with captions, never silent/blank audio.
9. Quiz-completion-gated unlock threshold is configured, but the child skips the quiz entirely (closes app) → Episode N+1 remains locked until the quiz is actually completed; app resume routes back to the pending quiz state, not silently abandoning the gate.
10. Story is withdrawn entirely from the catalog while several children have it fully downloaded and completed → already-completed progress history is preserved (per the general "withdrawn content becomes unavailable... while safe progress history remains" rule), but the content becomes non-replayable/non-discoverable going forward.
11. A child's "favorite" story is later re-categorized or merged into a different series by Admin (content restructuring) → favorite reference must resolve to the new canonical content ID, not silently break or point to a 404.
12. Two completion-triggering events arrive out of order due to network retry (e.g., a retried `/complete` call arrives after a newer playback heartbeat) → server applies idempotency/event-ordering logic (timestamp + client event ID) so the furthest-valid state is never regressed by a stale retried event.

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Media fails to load/stream (CDN issue) | Player shows a friendly retry state with an explicit retry control; auto-retries with backoff before surfacing the error UI |
| Media withdrawn mid-playback | Safe stop, age-appropriate explanation, recommended alternative content card (FR-16) |
| AI moral-summary generation failure/timeout | Immediate fallback to human-reviewed moral, no visible delay or error to the child |
| Quiz service unavailable post-story | Story completion (XP/reward) still finalizes independently; quiz step is skipped with a "quiz coming back soon" note rather than blocking reward issuance |
| Download manifest request fails | Clear retry option in Downloads Manager; partial downloads resumable, not restarted from zero |
| Interactive choice overlay fails to record choice (network) | Choice still drives the immediate in-story branching locally (deterministic client-side branch logic mirrors server logic), and the choice event is queued for later sync — playback is never blocked waiting on a network round-trip for a choice |
| Sequential unlock check fails (service error) | Fails closed for newly-encountered episodes (treat as locked, retry check) but never fails closed for already-unlocked episodes the child has previously accessed (cached unlock state persists) |

### 1.12 Empty States

- Library category with zero content for the child's age band/locale → "More stories for you are on the way" friendly message with a link to a different, populated category — never a blank grid.
- Downloads Manager with zero downloads → friendly illustration + "Download a story to watch offline" CTA pointing to the Library.
- Story Insights (parent view) with zero stories watched yet → "Once [Child] watches their first story, you'll see their progress here."

### 1.13 Loading States

- Library: skeleton category rails while catalog loads.
- Story Detail: skeleton cover/synopsis block, episode list shimmer.
- Story Player: branded loading spinner with the story's own cover art as background (not a generic platform spinner) while media buffers; minimum perceived-loading time avoided (show as soon as first frame is ready, don't artificially delay).

### 1.14 Offline States

- Library: "Downloads" category always available offline, fully functional; other categories show cached metadata (browsable) but non-downloaded items show a clear "connect to internet or download" affordance rather than a dead tap.
- Story Player: downloaded content plays identically offline as online, including interactive choices (deterministic client-side logic) and quiz (if quiz content was included in the download package) — completion/reward events queue for sync.
- Story Insights (parent): shows last-synced data with a "may not reflect today's offline activity yet" note if relevant.

### 1.15 Permission States

- No new runtime permissions specific to this feature beyond storage access already covered by the Downloads feature (A.16) for offline media; microphone is not used by Stories (interactive choices are tap-based, not voice-based, unless a future voice-narration-practice feature explicitly extends this).

</details>

## 7. Interactions and navigation

- {"element": "Resumes playback with new settings", "trigger": "Tap the corresponding source-defined control", "precondition": "Active correct child session; relevant content/permission/unlock state satisfied per cited requirements", "behavior": "Resumes playback with new settings", "destination": "Resumes playback with new settings", "validation": "Preserve cited source-specific validation; no simulated outcome may bypass parent gate, learned status, content unlock or offline availability", "back_cancel": "Dismiss overlay to originating screen; screen back returns to caller with context preserved; unresolved explicit destination must be approved", "unavailable": "Disabled or source-specific explanation when permission/unlock/content requirements fail"}

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
| Open/close by defined control | Closed ↔ visible, opacity0→1; sheet bottom→rest only if sheet specified | 200ms ease-out opening;160ms ease-in closing;no delay | Reversible; cancel closes and returns focus; navigate away closes | Instant show/hide | Open overlay / Close overlay; Move in from bottom only for actual sheet |
| Press/release enabled control | Rest→pressed→rest; preserve hit area | 100ms ease-out scale.96 (proposal);0ms delay | Release/cancel reverses; disabled has no activation | Color/border pressed feedback only | While pressing → Change to pressed; On click → approved action |



Timing not quoted from the PRD is a labeled design proposal. No loop, flashing or parallax is required. Animate compositor-friendly opacity/transform; never delay an enabled essential action. Stop all animation/media/recording simulation on leave; no second reward reveal on restore. Status/validation always has visible text/icon independently of motion.

## 9. Figma implementation instructions — future approved execution

1. Open the exact page/node links in section2. Confirm the source text/identity; stop if the references disagree or required copy is unavailable.
2. Locate the approved reference frame. Duplicate only that frame into a user-approved enhanced-design working area; preserve original nodes and IDs. If no frame exists, create only the missing requirement-driven surface after its layout/copy approval, using approved shared assets.
3. Create `NH/Enhanced/050/Caption_Audio_Track_Quality_Settings_Sheet/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Caption_Audio_Track_Quality_Settings_Sheet`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] A3 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
