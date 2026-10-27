**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 086 — Dua Card Detail (Arabic/Transliteration/Translation/Audio)

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **A6 — Dua Card Detail (Arabic/Transliteration/Translation/Audio)**.
- Surface: **screen**. Number is controlled review order, not a forced linear user journey.
- Execution status: **Preserve all literal Frame 1 text; source sample statistics are fixtures only and religious strings remain subject to source verification.**.
- Journey entry / previous screen: Category List, Search, Favorites, Habit Tracker deep link.
- Next screen(s) / result: Recall Quiz, back to list.
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_A6_Dua_Learning.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Child App (1-12)/Feature_A6_Dua_Learning.md>); **§1.18 row 3; §1.7; §2; §6; §13**.
- Current mobile reference: [NoorHeroes current preview](https://noorheroes.figma.site/) → selector **Dua Card**; exact text captured below.
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: [Dua Card Detail](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1104-1101) — `1104:1101`. Exact/closest named existing frame; preserve purpose and copy; theme/player subtype must be checked
- Frame 2 container: `1085:13003`; visual reference: [Dua Learning Studio](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1085-17126) — `1085:17126`. Related enhanced feature hub for visual patterns only; not an exact screen equivalent
- Reference qualification: ["CL-13: Hosted translation says 'after having taken it from us'; Frame1 says 'after causing us to die'. Transliteration ahyānā/baʿda versus aḥyānā/ba'da differs. Hosted unlearned+disabled quiz versus Frame1 learned+active quiz are conditional states, not copy to merge. Frame1 Sunnah Tip and 20 Golden Stars require approved source/economy provenance. Choose coherent source/state by approval; preserve both originals."].
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- [Dua Card-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Du'as/Dua Card-01.png>)
- [Dua Card-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Du'as/Dua Card-02.png>)
- [Dua Categories-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Du'as/Dua Categories-01.png>)
- [Dua Categories-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Du'as/Dua Categories-02.png>)
- [Dua Categories-03.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Du'as/Dua Categories-03.png>)
- [Dua Categories-04.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Du'as/Dua Categories-04.png>)
- [Dua Categories-05.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Du'as/Dua Categories-05.png>)
- [Dua Categories-06.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Du'as/Dua Categories-06.png>)
- [Dua Categories-07.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Du'as/Dua Categories-07.png>)
- [Dua Categories-08.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Du'as/Dua Categories-08.png>)
- [Dua Quiz-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Du'as/Dua Quiz-01.png>)
- [Dua Quiz-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Du'as/Dua Quiz-02.png>)
- [Dua Quiz-03.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Du'as/Dua Quiz-03.png>)
- [Dua Quiz-04.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Du'as/Dua Quiz-04.png>)
- Blueprint alignment:
- [01-dua-catalog-category-discovery.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A6_Dua_Learning/KMP/01-dua-catalog-category-discovery.md>)
- [02-dua-card-detail-audio-playback-experience.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A6_Dua_Learning/KMP/02-dua-card-detail-audio-playback-experience.md>)
- [03-dua-recall-quiz-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A6_Dua_Learning/KMP/03-dua-recall-quiz-flow.md>)
- [04-dua-master-badge-progress-celebration.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A6_Dua_Learning/KMP/04-dua-master-badge-progress-celebration.md>)
- [05-habit-tracker-reminder-suggestion-integration.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A6_Dua_Learning/KMP/05-habit-tracker-reminder-suggestion-integration.md>)
- [06-dua-favorites-management.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A6_Dua_Learning/KMP/06-dua-favorites-management.md>)
- [07-offline-downloads-sync-dua-content.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A6_Dua_Learning/KMP/07-offline-downloads-sync-dua-content.md>)
- [08-parent-dua-progress-view.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A6_Dua_Learning/KMP/08-parent-dua-progress-view.md>)
- [09-dynamic-category-metadata-rendering.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A6_Dua_Learning/KMP/09-dynamic-category-metadata-rendering.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: - CL-05
- CL-08
- CL-13 See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Enable Dua Card Detail (Arabic/Transliteration/Translation/Audio) in the established A6 journey. Entry: Category List, Search, Favorites, Habit Tracker deep link. Required outcome: Recall Quiz, back to list.

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

**FR-1** Dua Learning is a standalone screen reachable from the Learn tab, organized by category: Morning, Bedtime, Food, Travel, Gratitude, Protection (source: screen catalog).

**FR-2** Each Dua Card must display: Arabic text (Quranic-adjacent but dua-appropriate typography — see §2.1), transliteration, translation, and an audio play control — all four elements present simultaneously, not hidden behind extra taps, given duas are short enough to display in full (source: screen catalog "dua card with Arabic, transliteration, translation, audio").

**FR-3** User actions per dua: Listen (play audio), Mark as Learned, Practice Recall Quiz, Favorite (source: screen catalog).

**FR-4** Duas are **always free-tier** — no entitlement/paywall check is ever applied to any dua content, regardless of subscription state (hard rule, zero exceptions, enforced at the API response layer consistent with the pattern established for billing-content exclusion in A.2).

**FR-5** "Mark as Learned" is a child-initiated, self-assessed action (not AI-graded) — the child decides when they feel ready; this status is distinct from and a prerequisite to attempting the Recall Quiz for that dua.

**FR-6** Recall Quiz per dua is short (recommend 1–3 questions given dua length, e.g., "what does this dua ask for," "fill in the missing word," "match the occasion to the dua") and only offered for duas already marked Learned.

**FR-7** Recall Quiz incorrect answers must show supportive, non-shaming retry language and re-surface the dua's full card (Arabic/transliteration/translation/audio) for review before allowing a retry — never a bare "wrong" with no path back to the learning content (consistent with the platform's Ethical Rule against shaming).

**FR-8** Favoriting a dua surfaces it in a dedicated Favorites view (shared mechanic with A.3 Stories favorites) for quick access.

**FR-9** Learning a dua (reaching "Learned" status) must emit an event consumable by the Habit Tracker to offer that dua as a candidate daily-habit reminder (e.g., "Remind me to read this every morning") — this is an explicit cross-feature integration point, not a passive coincidence.

**FR-10** Dua Master badge (and any intermediate milestone badges) criteria are evaluated by the shared Reward/Achievement Service based on cumulative "Learned" dua count, consistent with the append-only reward-ledger pattern used platform-wide.

**FR-11** Every dua requires a source citation before leaving draft status in the CMS, and audio is mandatory before scholar review — text-only duas (no audio) cannot publish to children (source: Admin "Dua Management" module validation rules — this is a read-path guarantee this feature's content consumers rely on, not just an authoring-side rule).

**FR-12** Dua content must be downloadable for offline access (shared Downloads mechanism, A.16) given duas' high real-world recurring-use value (a child should be able to access a learned travel dua without connectivity while actually traveling).

**FR-13** Dua category filtering and search must support locale-aware sorting (e.g., displaying category labels and dua titles in the active locale) with full RTL support for Arabic UI.

**FR-14** A dua's translation/transliteration text is versioned and editable (new version on edit, not in-place mutation) per the same content-integrity pattern as Quran translations (A.5) — children always consume the latest *published* (scholar-approved) version, never a draft.

## 4. Exact content specification

### Current mobile source — exact captured text

```text
☀️
Morning
Upon Waking

دعاء الاستيقاظ

الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ

Alhamdu lillāhil-ladhī ahyānā baʿda mā amātanā wa ilayhin-nushūr

All praise is for Allah who gave us life after having taken it from us, and unto Him is the resurrection.

📜
Narrated by Al-Bukhari
↺
Mark as Learned
🔒
Practice Quiz (mark learned first)
```

### Frame 1 — exact layer text (separate source; differences need approval)

```text
Morning Duas • Sahih Al-Bukhari
Word 3 of 7
Active
0.8x
Slow
Tap
Words
الْحَمْدُ لِلَّهِ الَّذِي
أَحْيَانَا
بَعْدَ مَا
أَمَاتَنَا وَإِلَيْهِ النُّشُورُ
“Alhamdu lillāhil-ladhī aḥyānā ba'da mā
amātanā wa ilayhin-nushūr”
MEANING
“All praise is for Allah, who gave us life after
causing us to die, and unto Him is the
resurrection.”
Sunnah Tip: Say this cheerful prayer with a
big smile right as you open your eyes in the
morning to thank Allah for a brand new
day!
0:08
0:18
Loop 3x
5x
Learned & Memorized!
Tapped 7 times this week
🎯
Take Recall Quiz Challenge
Earn 20 Golden Stars
Next: Dua Before Sleeping
Bedtime Routine • 3 mins
Dua Recitation
5
```

### Requirement-driven fields and content roles

- Not supplied by this source; resolve before execution.

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Dua detail simultaneously includes exact Arabic, transliteration, translation and audio; do not collapse these behind taps. Keep source citation visible. Favorite and Mark as Learned remain distinct; recall quiz availability reflects learned status. Categories use metadata-driven icons/order.

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

1. Child favorites a dua, then the dua is later updated to a new scholar-approved version (e.g., a corrected transliteration) → the favorite reference resolves to the latest published version automatically; the child sees updated content without needing to re-favorite.
2. Child marks a dua as Learned, then later un-marks it (changes their mind / wants to re-practice from scratch) → "Learned" status can be toggled off by the child; doing so does not retroactively revoke an already-awarded Dua Master badge milestone if the cumulative count had already crossed a threshold at time of award (badges are sticky once earned, consistent with the append-only reward-ledger principle — a later un-mark doesn't claw back history).
3. Two different duas in different categories are functionally near-duplicates (e.g., a "before eating" and "before drinking" dua with overlapping wording) → each is tracked as an independently learnable/markable content item; the Recall Quiz must be specific enough to discriminate between them rather than risk a false sense of mastery from confusing one for the other (an editorial/QA concern flagged for content review, not purely a technical edge case, but the system must support per-item independent tracking regardless).
4. Child attempts a Recall Quiz offline for a downloaded-and-learned dua → quiz functions fully offline if the quiz question bank was included in the dua's offline package; result syncs on reconnect with idempotent submission, consistent with the platform's offline-progress pattern.
5. Parent revokes download permissions while a child has several duas already downloaded → already-downloaded dua content remains playable (per the general two-distinct-controls download policy established in A.3/A.4: "allow new downloads" vs. "revoke existing offline content") unless the parent additionally explicitly revokes existing offline content.
6. A dua is archived/retired by Admin (e.g., due to a citation issue requiring removal pending correction) while several children have already marked it Learned → existing "Learned" status and any historical quiz attempts are preserved (not cascade-deleted), but the dua becomes non-discoverable in the active catalog until republished; if a child had it favorited, the favorite shows a "temporarily unavailable" state rather than breaking.
7. Child's locale changes mid-session → transliteration/translation re-render in the new locale immediately; Arabic text is locale-independent (always the same verified Arabic) and never changes.
8. Recall Quiz question pool for a given dua is very small (e.g., only 1 possible question due to the dua's brevity) → the system allows repeated practice of the same single question without it feeling broken, but must avoid presenting it as if there were "multiple new questions" when there's actually just one (e.g., UI doesn't show a misleading "Question 1 of 1" if there's only 1 available).
9. Child rapidly toggles Favorite on/off multiple times in quick succession → idempotent handling ensures the final state is correctly persisted without a race condition leaving a stale/incorrect favorited state.
10. A dua targeted at a specific age range (`age_min`/`age_max` per the Admin schema) is encountered by a child outside that range via direct search/deep-link → the dua still displays respectfully (ages ranges for duas are about appropriateness of complexity/length, not strict content-safety gating like other features), but Home/Recommended surfaces would not have proactively suggested it outside its intended age band.
11. Habit Tracker reminder created from a Learned dua, then the child later un-marks that dua as Learned (Edge Case 2) → the existing habit reminder configuration is not automatically deleted (the parent/child may still want the reminder regardless of the marked-learned status), but the Habit Tracker may show a gentle note that the source dua is no longer marked as fully learned, without forcibly removing the habit.
12. Child taps "Listen" on a dua while another piece of audio (e.g., a Story) is already playing elsewhere in the app (multi-screen/background audio edge case) → standard single-active-audio-session behavior applies (the other audio pauses), consistent with general app-wide audio session management, not a Dua-specific behavior to reinvent.

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Dua catalog fetch failure | Cached last-known catalog rendered with a subtle "may be outdated" indicator, never a blank screen |
| Audio fails to load/play | Retry with backoff; falls back to a lower-bitrate alternate source if configured before surfacing a hard error |
| Mark-as-Learned submission fails (network) | Optimistic local update, queued for retry, never blocks further interaction |
| Recall Quiz service unavailable | Quiz entry point shows a friendly "quiz coming back soon" message; dua remains fully viewable/learnable regardless |
| Favorite toggle submission fails | Optimistic local update + retry, consistent with platform-wide favoriting pattern (A.3) |
| Dua archived/withdrawn while open | Graceful "this dua is temporarily unavailable" message with a suggested alternative from the same category, never a raw 404 |

### 1.12 Empty States
- Category with zero published duas yet (e.g., a newly-added category) → friendly "more duas for this category are coming soon" message with a link to a populated category.
- Favorites list with zero favorites → "Tap the heart on any dua to save it here" guided empty state.
- Parent Dua Progress view with zero learned duas yet → "Once [Child] learns their first dua, you'll see it here."

### 1.13 Loading States
- Dua Library: skeleton category list + card shimmer.
- Audio: gentle loading pulse on the play button, consistent with other audio-loading treatments across the app.

### 1.14 Offline States
- Downloaded/favorited duas fully functional offline (FR-12); non-downloaded duas show a clear "connect to internet or download" affordance.
- Mark-as-Learned and Favorite actions queue locally and sync on reconnect.

### 1.15 Permission States
- No new runtime permissions; relies on existing storage permission for downloads (shared with A.16).

</details>

## 7. Interactions and navigation

- {"element": "Listen", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "Single active audio playback with read-along", "destination": "Single active audio playback with read-along", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Favorite", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "B14 favorite toggle", "destination": "B14 favorite toggle", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Mark as Learned", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "Self-assessed learned status; enable recall entry after confirmation", "destination": "Self-assessed learned status; enable recall entry after confirmation", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Practice Recall Quiz", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "A8 DuaRecall only when learned", "destination": "A8 DuaRecall only when learned", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Download", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "B15 Dua download; always free-tier", "destination": "B15 Dua download; always free-tier", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}

For every action below, use the cited preconditions and source validation. Preserve the invoking route and selected child. Back/cancel dismisses only the current overlay or returns to the invoking screen, preserving drafts and completed progress where specified. Unavailable actions remain visibly labeled with their reason and never activate. Permission prompts occur only after parent consent and a deliberate related action. A prototype simulates outcomes; it never validates identity, grants permissions, charges money or mutates production data.

Verified current-preview controls, retained to prevent omitted clickable elements:

- {"disabled": false, "label": "Go back", "placeholder": null, "tag": "BUTTON", "text": "", "type": null}
- {"disabled": false, "label": "Add dua to favorites", "placeholder": null, "tag": "BUTTON", "text": "", "type": null}
- {"disabled": false, "label": "Play dua preview", "placeholder": null, "tag": "BUTTON", "text": "", "type": null}
- {"disabled": false, "label": "Restart dua preview", "placeholder": null, "tag": "BUTTON", "text": "↺", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Mark as Learned", "type": null}
- {"disabled": true, "label": null, "placeholder": null, "tag": "BUTTON", "text": "🔒\nPractice Quiz (mark learned first)", "type": null}

For any captured control absent from an explicit action above, reconcile it against the screen-specific source below before wiring. Do not connect it to a convenient unrelated screen. Mark it **unresolved, non-executable** until its actual destination/state is confirmed; the navigation appendix reports this limitation. Decorative source-layer names are not automatically click targets.

<details><summary>Screen-specific PRD specification / click behavior</summary>

#### Screen: Dua Card Detail

- **Purpose:** Present a complete, learnable dua in one view.
- **Components:** Category tag, large Arabic text block (top, primary visual weight), transliteration line, translation line, audio play/pause control with a progress scrubber, Favorite (heart) icon, Mark-as-Learned toggle/button, Recall Quiz entry button (visible but distinctly secondary until Learned status is set, at which point it becomes primary-styled).
- **States:** Default (not yet learned), Learned (badge/checkmark indicator visible), Playing (read-along highlight active), Offline-available, Offline-unavailable, Error (audio load failure).
- **Accessibility:** Read-along highlight has a screen-reader-friendly alternative (sequential text exposure, not relying on visual highlight alone); translation/transliteration always screen-reader-readable regardless of visual toggle state if one exists.
- **Responsive Rules:** Single-column on mobile; tablet may show category list + dua card side-by-side (master-detail layout) rather than full-screen navigation per tap.



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
3. Create `NH/Enhanced/086/Dua_Card_Detail_Arabic_Transliteration_Translation_Audio/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Dua_Card_Detail_Arabic_Transliteration_Translation_Audio`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] A6 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
