**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 056 — Dua / Calm-Reflection Ending Card

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **A4 — Dua / Calm-Reflection Ending Card**.
- Surface: **screen**. Number is controlled review order, not a forced linear user journey.
- Execution status: **Preserve all literal Frame 1 text; source sample statistics are fixtures only and religious strings remain subject to source verification.**.
- Journey entry / previous screen: Completion threshold reached during Bedtime Mode.
- Next screen(s) / result: Next Episode offer / Back to Library.
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_A4_Audio_Bedtime_Player_Bedtime_Mode.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Child App (1-12)/Feature_A4_Audio_Bedtime_Player_Bedtime_Mode.md>); **§1.18 row 10; §1.7; §2; §6; §13**.
- Current mobile reference: **Missing independently mapped current-site screen.**
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: [Dua Bedtime Reflection Card](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1105-2898) — `1105:2898`. Exact/closest named existing frame; preserve purpose and copy; theme/player subtype must be checked
- Frame 2 container: `1085:13003`; visual reference: [Stories & Bedtime Hub](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1085-16216) — `1085:16216`. Related enhanced feature hub for visual patterns only; not an exact screen equivalent
- Reference qualification: [].
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- [Audio Player.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Bedtime Audio/Audio Player.png>)
- [Dua Card.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Bedtime Audio/Dua Card.png>)
- [Sleep Timer.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Bedtime Audio/Sleep Timer.png>)
- Blueprint alignment:
- [01-bedtime-audio-player-core-screen.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/01-bedtime-audio-player-core-screen.md>)
- [02-sleep-timer-reliability-engine.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/02-sleep-timer-reliability-engine.md>)
- [03-calm-mode-bedtime-theme-application.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/03-calm-mode-bedtime-theme-application.md>)
- [04-dua-calm-reflection-ending-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/04-dua-calm-reflection-ending-flow.md>)
- [05-bedtime-offline-downloads-auto-suggest.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/05-bedtime-offline-downloads-auto-suggest.md>)
- [06-bedtime-notification-deep-link-continue-listening.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/06-bedtime-notification-deep-link-continue-listening.md>)
- [07-parent-bedtime-configuration-repository.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/07-parent-bedtime-configuration-repository.md>)
- [08-playback-speed-selector.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/08-playback-speed-selector.md>)
- [09-parent-bedtime-ritual-status-widget.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/09-parent-bedtime-ritual-status-widget.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: No screen-specific ID supplied; still check global G-01–G-10 and source content differences. See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Enable Dua / Calm-Reflection Ending Card in the established A4 journey. Entry: Completion threshold reached during Bedtime Mode. Required outcome: Next Episode offer / Back to Library.

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

**FR-4** Bedtime Mode is a **system-wide state**, not exclusive to this player: any content surface entered during the parent-configured wind-down window (or explicitly via the Home Bedtime Corner widget) must apply the same dimmed visual treatment, disabled stimulating-reward-animation rule, and dua/calm-reflection ending rule (cross-reference A.3 §2.1 "Bedtime Theme Override").

**FR-5** Bedtime Mode must dim the UI (reduced brightness/contrast theme), disable stimulating reward effects (no confetti/badge-burst/level-up animations), and end every session with a dua or calm reflection — this rule has zero exceptions, including for content that would otherwise show a bright completion animation outside the window (source §7.5).

**FR-6** Sleep Timer expiry must trigger a gentle audio fade-out (not an abrupt cut) over a configurable fade duration (default 15 seconds), followed by auto-pause; the screen may also auto-dim further or return to a calm "goodnight" idle state.

**FR-10** Ending sequence: on reaching the completion threshold, the player transitions directly to a dua/calm-reflection card (not the standard celebratory Completion/Reward screen used outside Bedtime Mode) — reward (XP/Noor Heroes Points) is still recorded quietly in the background but not visually celebrated in this context.

**FR-14** If a child opens the Audio Bedtime Player outside the configured bedtime window (e.g., daytime listening), the player still functions normally but does **not** force Bedtime Mode visuals unless the child explicitly opts in via a "Calm Mode" toggle available at any time of day (giving children agency to use the calming experience whenever they want, while keeping the *automatic* window-based trigger separate).

## 4. Exact content specification

### Frame 1 — exact layer text (separate source; differences need approval)

```text
Bedtime Reflection &
Du'a
بِاسْمِكَ رَبِّي وَضَعْتُ جَنْبِي، وَبِكَ
أَرْفَعُهُ
“Bismika Rabbi wada’tu janbi
wa bika arfa’uh”
‘In Your name, my Lord, I lie
down, and by Your grace, I rise.’
“Tonight, let your heart rest in peace,
knowing you are protected and loved.”
Goodnight & Peace (Done)
May peaceful sleep surround your home
Noor is resting peacefully under the night sky.
BEDTIME STORIES
Bedtime Du'a &
Reflection
Whisper
```

### Requirement-driven fields and content roles

- Not supplied by this source; resolve before execution.

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Use low-light calm-theme tokens and restrained contrast while preserving readable text. Cover/title/verified source precede scrubber and large play controls; timer/speed/download/episode controls remain secondary. Selector sheets use simple vertically stacked options, not dense wheels. Ending shows verified calm reflection without XP counters.

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

1. Sleep timer is set, but the child finishes the episode naturally before the timer expires → playback simply ends per normal completion flow; the now-moot timer is cancelled cleanly (no leftover background timer attempting to fade/pause audio that has already stopped).
2. Child changes the sleep timer mid-playback (e.g., extends from 15 to 30 minutes) → the new duration applies from the moment of change, not from original playback start, and any pending fade-out scheduled under the old timer is cancelled and rescheduled.
3. Device is rebooted or the app is force-killed by the OS mid-overnight playback (e.g., low memory) → playback does not silently resume in the background after an OS-level kill (expected/acceptable, since a foreground service surviving an explicit force-kill is not guaranteed by the platform), but the app must not auto-resume playback unexpectedly on next foreground open either — resumes only on explicit user action, to avoid surprising late-night/early-morning playback.
4. Parent narrows the bedtime window (e.g., from 8–10pm down to 8:30–9:30pm) while a session is already in Bedtime Mode within the now-excluded time → per the general rule "changes apply at next session, not mid-session" (A.1/Parent Dashboard rule), the current session remains in Bedtime Mode until exited; the new window applies starting the next session.
5. Child has no internet and no pre-downloaded bedtime content, opens the Bedtime Corner at night → friendly offline-state message suggesting previously-downloaded content if any exists, or a calm "no story available right now, here's a dua to read together" fallback rather than a hard error (important given the emotionally sensitive context).
6. Two children share a device; Child A falls asleep mid-playback and the device is handed off / picked up by Child B the next day → no carryover of Child A's playback position or sleep-timer state into Child B's session (full session isolation per the multi-child rule).
7. Playback speed is changed mid-episode → completion-threshold calculation must still be based on actual content consumed (e.g., percentage of total duration), not wall-clock time, so a 1.5x-speed listen still correctly registers full completion.
8. Sleep timer expires exactly at the same moment the episode reaches its natural end → completion/ending-sequence flow takes precedence (child should still get the calm dua ending, not have it pre-empted by a sleep-timer fade that cuts off the dua itself).
9. Parent has disabled "auto-suggest download" but a family is in a known low-connectivity region (detected via repeated streaming failures) → system may still proactively prompt (not auto-execute) "Would you like to download tonight's story for offline listening?" as a helpful one-time suggestion, never silently downloading without consent.
10. Child uses the explicit daytime "Calm Mode" toggle (FR-14) outside the bedtime window, then the actual bedtime window begins while they're still in that session → no jarring transition needed since the visual state was already calm-mode equivalent; session simply continues, and the ending-sequence rule (dua, not celebration) applies as it would for genuine Bedtime Mode.
11. A multi-part audio series' Episode 1 was downloaded, but Episode 2 (just unlocked) was not yet downloaded, and the child is offline at bedtime → "Next Episode" tap on the now-unlocked-but-not-downloaded Episode 2 shows a clear "needs internet to fetch this episode" message rather than a silent failure or attempting a network call that hangs.
12. Volume is at system maximum when the app is opened at night → no special forced-volume-reduction behavior is required (NoorHeroes should not silently override the user/parent's device volume control), but the first-launch-of-bedtime-mode-ever experience may include a one-time gentle tip suggesting a comfortable volume for nighttime listening (a UX nicety, not a technical control).

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Audio stream fails to load (network) | Friendly retry with explicit control; auto-retry with backoff before surfacing error; suggest downloading for next time |
| Sleep timer fails to fire due to OS process death | Mitigated via foreground service + AlarmManager-backed fallback (Android) — see §6; if both fail (rare OS-level edge case), no audio should be playing anyway since the process itself would have died, so the failure mode is "silence," never "stuck blaring" |
| Media withdrawn mid-playback | Same safe-stop + explanation + alternative pattern as A.3 §1.11, rendered in the calm Bedtime Mode visual style if applicable |
| Download for offline bedtime content fails | Clear retry in Downloads Manager; falls back to streaming if connectivity exists at time of actual playback |
| Parent bedtime-window config fails to load (e.g., Home Aggregation Service degraded) | Player defaults to NOT forcing Bedtime Mode automatically (fails safe toward the less-intrusive standard mode) but the explicit "Calm Mode" toggle remains available regardless, so the calming experience is never entirely unreachable |

### 1.12 Empty States

- No bedtime-eligible content available for the child's age band/locale yet → calm fallback message + suggestion to read a dua together (FR per Edge Case 5), never a blank screen.
- No sleep-timer history/usage yet (first time) → simple, friendly first-use explainer tooltip on the Sleep Timer control.

### 1.13 Loading States

- Audio buffering: gentle pulsing glow on the cover art (no spinning platform-default spinner — calm, ambient loading treatment consistent with Bedtime Mode's tone) with the title/cover already visible (metadata loads instantly from cache even if audio itself buffers).

### 1.14 Offline States

- Full offline parity per FR-11; persistent small "offline" indicator, non-alarming.
- Next-episode-not-downloaded state per Edge Case 11.

### 1.15 Permission States

- No new runtime permissions; relies on existing storage (downloads) and notification (if a "bedtime story ready" reminder notification is enabled) permissions already covered elsewhere.

</details>

## 7. Interactions and navigation

- {"element": "Next Episode offer", "trigger": "Tap the corresponding source-defined control", "precondition": "Active correct child session; relevant content/permission/unlock state satisfied per cited requirements", "behavior": "Next Episode offer", "destination": "Next Episode offer", "validation": "Preserve cited source-specific validation; no simulated outcome may bypass parent gate, learned status, content unlock or offline availability", "back_cancel": "Dismiss overlay to originating screen; screen back returns to caller with context preserved; unresolved explicit destination must be approved", "unavailable": "Disabled or source-specific explanation when permission/unlock/content requirements fail"}
- {"element": "Back to Library", "trigger": "Tap the corresponding source-defined control", "precondition": "Active correct child session; relevant content/permission/unlock state satisfied per cited requirements", "behavior": "Back to Library", "destination": "Back to Library", "validation": "Preserve cited source-specific validation; no simulated outcome may bypass parent gate, learned status, content unlock or offline availability", "back_cancel": "Dismiss overlay to originating screen; screen back returns to caller with context preserved; unresolved explicit destination must be approved", "unavailable": "Disabled or source-specific explanation when permission/unlock/content requirements fail"}

For every action below, use the cited preconditions and source validation. Preserve the invoking route and selected child. Back/cancel dismisses only the current overlay or returns to the invoking screen, preserving drafts and completed progress where specified. Unavailable actions remain visibly labeled with their reason and never activate. Permission prompts occur only after parent consent and a deliberate related action. A prototype simulates outcomes; it never validates identity, grants permissions, charges money or mutates production data.

Verified current-preview controls, retained to prevent omitted clickable elements:

- Not supplied by this source; resolve before execution.

For any captured control absent from an explicit action above, reconcile it against the screen-specific source below before wiring. Do not connect it to a convenient unrelated screen. Mark it **unresolved, non-executable** until its actual destination/state is confirmed; the navigation appendix reports this limitation. Decorative source-layer names are not automatically click targets.

<details><summary>Screen-specific PRD specification / click behavior</summary>

#### Screen: Dua / Calm-Reflection Ending Card

- **Purpose:** Close every Bedtime Mode session with a genuinely calming, spiritually grounding moment.
- **Components:** Short dua text (Arabic + transliteration + translation, per the same Dua content pattern as A.5/Dua Learning), soft Noor companion illustration in a "sleepy/calm" pose (distinct visual variant from its energetic daytime pose), single low-key "Done" or "Next Episode" (if applicable) action — no bright button styling.



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
3. Create `NH/Enhanced/056/Dua_Calm_Reflection_Ending_Card/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Dua_Calm_Reflection_Ending_Card`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] A4 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
