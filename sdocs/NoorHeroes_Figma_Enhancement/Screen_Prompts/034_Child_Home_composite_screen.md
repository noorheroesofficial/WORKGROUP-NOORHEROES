**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 034 — Child Home (composite screen)

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **A2 — Child Home (composite screen)**.
- Surface: **screen**. Number is controlled review order, not a forced linear user journey.
- Execution status: **Preserve all literal Frame 1 text; source sample statistics are fixtures only and religious strings remain subject to source verification.**.
- Journey entry / previous screen: Profile Picker, app resume, bottom nav "Home" tab.
- Next screen(s) / result: All feature tabs, Search, Notifications.
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_A2_Home_Dashboard_AI_Personalization.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Child App (1-12)/Feature_A2_Home_Dashboard_AI_Personalization.md>); **§1.18 row 1; §1.7; §2; §6; §13**.
- Current mobile reference: [NoorHeroes current preview](https://noorheroes.figma.site/) → selector **Home**; exact text captured below.
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: [Html → Body](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1096-1090) — `1096:1090`. Exact/closest named existing frame; preserve purpose and copy; theme/player subtype must be checked
- Frame 2 container: `1085:13003`; visual reference: [Child Home Dashboard](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1085-16820) — `1085:16820`. Related enhanced feature hub for visual patterns only; not an exact screen equivalent
- Reference qualification: [].
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- [Home-01.5.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Home/Home-01.5.png>)
- [Home-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Home/Home-01.png>)
- [Home-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Home/Home-02.png>)
- [Home-03.5.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Home/Home-03.5.png>)
- [Home-03.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Home/Home-03.png>)
- [Home-04.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Home/Home-04.png>)
- [Home-05.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Home/Home-05.png>)
- [Home-06.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Home/Home-06.png>)
- [Home-07.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Home/Home-07.png>)
- [Home-08.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Home/Home-08.png>)
- [Home-09.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Home/Home-09.png>)
- [Home-10.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Home/Home-10.png>)
- [Home-11.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Home/Home-11.png>)
- [Home-12.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Home/Home-12.png>)
- [Home-13.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Home/Home-13.png>)
- Blueprint alignment:
- [01-home-screen-composition-state-management.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A2_Home_Dashboard_AI_Personalization/KMP/01-home-screen-composition-state-management.md>)
- [02-continue-learning-watching-resume-rails.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A2_Home_Dashboard_AI_Personalization/KMP/02-continue-learning-watching-resume-rails.md>)
- [03-habit-checkin-widget-offline-sync.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A2_Home_Dashboard_AI_Personalization/KMP/03-habit-checkin-widget-offline-sync.md>)
- [04-daily-mission-quiz-widgets.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A2_Home_Dashboard_AI_Personalization/KMP/04-daily-mission-quiz-widgets.md>)
- [05-weekly-challenge-milestones-widgets.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A2_Home_Dashboard_AI_Personalization/KMP/05-weekly-challenge-milestones-widgets.md>)
- [06-bedtime-corner-conditional-widget.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A2_Home_Dashboard_AI_Personalization/KMP/06-bedtime-corner-conditional-widget.md>)
- [07-home-offline-cache-first-day-deep-linking.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A2_Home_Dashboard_AI_Personalization/KMP/07-home-offline-cache-first-day-deep-linking.md>)
- [08-parent-summary-preview-submode.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A2_Home_Dashboard_AI_Personalization/KMP/08-parent-summary-preview-submode.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: - CL-01
- CL-03
- CL-06 See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Enable Child Home (composite screen) in the established A2 journey. Entry: Profile Picker, app resume, bottom nav "Home" tab. Required outcome: All feature tabs, Search, Notifications.

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

**FR-1** Home must render the following sections **in this fixed priority order**, not user-reorderable (source §21.8 / §5.8): (1) Greeting/streak/XP bar + notifications + search, (2) Today's Mission, (3) Continue Learning / Continue Watching, (4) Recommended Next Step, (5) Daily Quiz / quick practice, (6) Habit & Good Deed check-in, (7) Weekly Challenge & progress map, (8) Milestones & reward summary, (9) Bedtime Corner (conditional on time window), (10) Islamic Fact of the Day.

**FR-2** Greeting must include the child's name and, where applicable, a reference to the current Islamic occasion (Jummah, Ramadan, Eid, etc.) sourced from an Islamic calendar service.

**FR-4** Today's Mission is system-assigned (not child-selectable) and must be achievable within the child's typical session length; default cap is 3 daily missions (source: "Daily Missions (3 per day)").

**FR-5** The Recommendation Engine must accept: age band, locale, parent restrictions, skill-gap/mastery confidence, incomplete activity, variety/fatigue controls, recent dislikes/skips, time-of-day/bedtime state, and offline content availability as ranking inputs (source §21.8 "Home ranking inputs").

**FR-6** Every AI-generated recommendation must pass through an AI Safety Filter service before being eligible for display; recommendations failing the filter are silently excluded (never shown with a "blocked" placeholder that could intrigue a child).

**FR-7** Habit check-in widget must support same-screen check-in (no navigation away from Home required) for at least: Salah, Quran reading, daily dua, good deed, dhikr — and deep-link to the full Habit Builder for fasting tracker and detailed logging.

**FR-8** Streak display must never use shaming language or visual treatment (e.g., no red "broken streak" warnings); a missed day must be handled via "Mercy Day" protection logic (defined in A.7 Habit Tracker, referenced here as a Home-display rule).

**FR-9** Home must NEVER display subscription, billing, paywall, or upsell messaging to the child profile context, under any system state (hard rule, zero exceptions — enforced at the API response-shaping layer, not just client-side hiding).

**FR-10** Home must NEVER autoplay video with sound (source §21.8).

**FR-11** Home must NOT implement infinite scroll; the feed is a fixed, bounded set of sections per FR-1, each internally scrollable (e.g., a horizontal rail) but the page itself terminates after section 10.

**FR-12** Bedtime Corner section appears only within the parent-configured bedtime window for that specific child; outside the window it is omitted entirely from the response (not rendered-but-hidden).

**FR-13** Islamic Fact of the Day must be scholar-approved content, versioned, and not repeat for the same child within a rolling 30-day window where catalog size allows.

**FR-14** Parent Summary Preview (a condensed widget, visible only when the Parent Profile views a child's Home in "preview" sub-mode, not visible to the child) shows today's completed activities and healthy-usage status without requiring full Parent PIN re-entry if already in an active Parent session.

**FR-16** Offline mode must render Home using the last successfully cached payload, visually marked as offline, with only downloaded content actionable; non-downloaded recommended content shows a "download to access offline" affordance rather than a dead link.

**FR-17** Home must refresh its data on: app foreground after >15 minutes background, pull-to-refresh gesture, and immediately after completing any activity that affects its own sections (e.g., completing a habit check-in updates the streak bar in place, not on next full reload).

## 4. Exact content specification

### Current mobile source — exact captured text

```text
Good morning ✨

Aisha!
🌙 Ramadan Day 14
⭐

Day streak

7 days

XP this week

1,240 XP

Level 5
1,240 / 2,000 XP
Today's Mission
📖

Memorise Surah Al-Asr

Quran · 3 verses · ~10 min

Continue Learning
See all
📖

Prophet Ibrahim

Islamic Stories · Ch.2

60% complete

🌙

Surah Al-Mulk

Quran · Verse 8 of 30

35% complete

✨

Tajweed Basics

Arabic · Lesson 4

80% complete

Continue Watching
See all
🎬

Stories of the Prophets

Episode 4 · 12 min left

🕌

How to Pray: Fajr

Prayer Guide · 5 min left

Recommended for Aisha
⭐

Prophet Yusuf (AS)

Islamic Stories

Because you liked Prophet Ibrahim
📿

Surah Al-Asr

Quran · Short Surah

Matches your current level
💚

Kindness in Islam

Akhlaq · 3 min read

Based on your interests
🧠

Today's Islamic Quiz

Prophet Stories · 5 questions · ~2 min

Start
Habits & Good Deeds
2/4 today
🌅
Fajr prayer
+10 XP
📖
Quran reading
+10 XP
📿
Afternoon dhikr
💚
Kind deed today
M
T
W
T
F
S
S
Weekly Challenge
4 / 7 days

Quranic Explorer

Read one Surah every day

57%

3 days left

M
★
T
★
W
★
T
★
F
S
S
Recent Achievements
View all
🌟

Quran Star

Completed 5 surahs

2d ago

📚

Story Explorer

Read 10 Prophet stories

5d ago

🔥

Next: 7-Day Streak

5 of 7 days complete

🌙
Bedtime Corner
8:30 PM

Time to wind down, Aisha ✨

Bedtime Story

Moonlit Lantern · 8 min

🤲

Night Dua

Bedtime reflection

☀️
Fact of the Day

The word "Islam" comes from the Arabic root "Salama" — meaning peace, purity, and submission.

📜
Scholar-reviewed
Learn more →
Home
Learn
Stories
Rewards
Profile
```

### Frame 1 — exact layer text (separate source; differences need approval)

```text
Jumu’ah Mubarak! 🌿
Assalamu Alaikum,
Zayd! 👋
5 Day Streak!
🌟
Active
🔥
Mercy Day active if missed!
Shielded
Level 3: Seeker
380 / 500 XP to Explorer ⭐
DAILY MISSION
6h left today
2/3
steps
Learn the Meaning of
Bismillah
Discover why we start every good…
Continue Mission
Continue Learning
View all
ج
Lesson 4
Arabic: Letter Jeem (ج)
Camel & Jungle words
🐪
Progress
80%
Step 5 of 6
Wudu: Washing Arms
Right arm to the elbow!
💧
Progress
80%
Verse 4
Surah Al-Fatiha Recite
Repeat after Qari
📜
Progress
60%
Continue Watching
View all
Episode 2
6m left
Prophet Yunus & the Whale
Storybook Animation • 85% done
Sing Along
3m left
Surah Al-Fatiha with Little…
Melody & Meaning • 40% done
Moral Tale
4m left
The Kind Shepherd
Little Believers • 75% done
Because you loved Prophet Stories ✨
The Story of Prophet
Dawud & the Birds
5 min interactive read & listen with
melodious sounds 🐦🎶
Explore Now
Daily Wonder
Quiz 🎯
3 quick questions • ~1 min
+50
XP
Can you guess which surah is known as
the "Mother of the Book"? Test your
smarts!
Start Quiz Now
My Good Deeds Today 🌱
2/4 completed today! Keep shining ☀️
M
T
W
T
F
🌿
S
S
Fajr Prayer
Completed with Baba!
+15 XP
Read 1 Page of Quran
Surah Al-Mulk or Al-Ikhlas
+20 XP
Helped family with a
smile
Cleaned playroom
+10
XP
Said Alhamdulillah 10
times
Remembering Allah's gifts
+10
XP
Kindness Caravan
🐪
3 days
left
Complete 7 daily acts of kindness across the
week!
4 🐪
5
6
4 of 7 Deeds Complete (57%)
Reward: "Keeper of Kindness" Badge
My Treasures &
Badges 🏆
See all 14
badges ➔
First Reciter
Unlocked
Curious…
Unlocked
Dawn Riser
2 Fajr left
Bedtime Corner 🌙
Wind down with calm sounds &
dua
Night
Mode
Sleepy Stars of Medina
8 min gentle audio sleep story
🤲
Before you sleep:
"Bismika Rabbi wada’tu janbi wa bika arfa’uh..."
Wonder Fact of the Day 💡
Did you know? Prophet Muhammad
(peace be upon him) taught us that
smiling at your brother or sister is a
good deed (Sadaqah)!
Source: Jami` at-Tirmidhi
Take 1-Question Mini Quiz
NOOR & WONDER
Home
Home
Learn
Stories
Rewards
Profile
```

### Requirement-driven fields and content roles

- Not supplied by this source; resolve before execution.

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Preserve bounded vertical Home and the exact FR-1 section priority. Header and mission carry strongest hierarchy; separate resume rails without duplicated content. Same-screen habit rows update independently. Conditional bedtime card is absent outside the window. Keep child Home free of billing.

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

1. Child has two equally "furthest-valid" in-progress items of the same content type (e.g., two stories both 50% complete due to a sync race) → Continue Learning shows only the most-recently-interacted-with one; the other surfaces lower in Recommended Next Step, not duplicated.
2. Recommendation Engine returns zero eligible items after AI Safety Filter exclusion (e.g., new low-content-volume locale) → Recommended Next Step section falls back to scholar-curated "evergreen" content set, never renders empty.
3. Child's age band changes (birthday rollover) between sessions → Home recommendations must reflect the new age band immediately on next load, not stale-cached from the prior band.
4. Bedtime window spans midnight (e.g., 8pm–6am) → Bedtime Corner logic must correctly evaluate window crossing midnight, not just simple start<now<end comparison.
5. Parent changes screen-time/AI-permission settings while child is mid-session on Home → per Parent Dashboard rule, "changes apply at the next child-app session, not mid-session" — Home must not abruptly mutate mid-session even if settings change server-side.
6. Child completes the Today's Mission item, then re-opens Home same day → Today's Mission shows a completed state with positive reinforcement, not a re-assignment of a new mission (missions are daily-bounded, max 3, not infinitely regenerating).
7. Multiple siblings share a device and switch profiles rapidly → Home payload for child B must never contain any cached fragment of child A's session (cache keyed strictly per child_id, cleared on switch per the multi-child session-isolation rule).
8. Islamic calendar service is unavailable at request time → Greeting gracefully omits the occasion reference rather than showing an error or stale/incorrect date claim.
9. Child has zero habits configured yet (parent hasn't set any up) → Habit & Good Deed check-in section shows a friendly "ask a grown-up to set up your first habit" prompt instead of an empty checklist.
10. Network reconnects mid-session after an offline period → Home should reconcile any locally-queued offline habit check-ins (synced in causal order, deduplicated via idempotency keys) before showing "live" data, to avoid a visible streak regression flash.
11. Daily Quiz has already been completed for the day but the child navigates back to Home → quiz widget shows a completed/celebratory state with a "come back tomorrow" framing, not a re-playable quiz (unless retry-for-mastery is explicitly permitted by design — must be a deliberate decision, defaulting to not-replayable for the "Quiz of the Day" framing).
12. Recommendation payload includes content that was withdrawn by Admin between cache time and tap time → tapping shows a graceful "this content is no longer available" message and silently removes it from the cached Home payload, not a raw 404.

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Recommendation Service timeout/failure | Serve rule-based fallback feed (deterministic, scholar-curated) seamlessly — child never sees an error for this specific failure |
| Progress Service failure (Continue Learning data) | Section gracefully hides rather than showing a broken card; other sections render normally |
| Habit check-in submit fails (network) | Optimistic UI update locally, queued for retry via background sync, with a subtle "saving..." indicator; never blocks the rest of Home |
| Full Home payload fetch failure (no cache available — true first launch on flaky network) | Show a friendly retry screen, never a raw technical error message |
| Islamic calendar/occasion service failure | Omit occasion phrase from greeting silently |
| Content item withdrawn/unavailable on tap | Graceful "no longer available" toast + silent removal from local cache |

### 1.12 Empty States

- First-day / zero-activity child: guided single-CTA "start your first mission" replacing data-dependent widgets (FR-15).
- Zero habits configured: friendly parent-setup prompt (Edge Case 9).
- Zero weekly-challenge participation yet: challenge widget shows the challenge description and a "Join Challenge" CTA instead of progress bar.
- Zero achievements yet: milestone summary shows the next achievable milestone as a preview/teaser, not a blank module.

### 1.13 Loading States

- Skeleton-screen loading per section (shimmer placeholders matching each widget's shape), not a single full-screen spinner — sections that resolve faster render progressively rather than waiting for the slowest section.
- Pull-to-refresh shows a brand-consistent (non-default-platform) refresh indicator.

### 1.14 Offline States

- Full cached-Home rendering per FR-16, with a persistent small "offline" indicator (not alarming, not blocking).
- Habit check-ins queue locally and sync on reconnect (Edge Case 10).
- Non-cached recommended content shows "download to access offline" rather than disabled-greyed-out-no-explanation.

### 1.15 Permission States

- No new runtime permissions are requested by this feature itself (notifications/microphone are requested by other features); Home simply reflects whatever permission state already exists (e.g., if notification permission was denied, the notification bell still renders but indicates no push capability via a subtle badge state).

</details>

## 7. Interactions and navigation

- {"element": "Mission card", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "Relevant assigned Story/Quran/Quiz/Habit activity", "destination": "Relevant assigned Story/Quran/Quiz/Habit activity", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Continue Learning", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "Saved content position", "destination": "Saved content position", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Continue Watching", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "Story Player at saved media position", "destination": "Story Player at saved media position", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Daily Quiz", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "A8 Daily Quiz unless completed today", "destination": "A8 Daily Quiz unless completed today", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Habit checkbox", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "Update this Home row and XP/streak in place", "destination": "Update this Home row and XP/streak in place", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Search", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "B13 Search", "destination": "B13 Search", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Notification bell", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "B17 Child Notifications", "destination": "B17 Child Notifications", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Weekly Challenge", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "A11 Weekly Challenge Detail", "destination": "A11 Weekly Challenge Detail", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Milestones", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "A11 Achievements / Wallet", "destination": "A11 Achievements / Wallet", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Bedtime Corner", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "A4 Audio Bedtime Player", "destination": "A4 Audio Bedtime Player", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Islamic Fact", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "B18 Fact Detail", "destination": "B18 Fact Detail", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}

For every action below, use the cited preconditions and source validation. Preserve the invoking route and selected child. Back/cancel dismisses only the current overlay or returns to the invoking screen, preserving drafts and completed progress where specified. Unavailable actions remain visibly labeled with their reason and never activate. Permission prompts occur only after parent consent and a deliberate related action. A prototype simulates outcomes; it never validates identity, grants permissions, charges money or mutates production data.

Verified current-preview controls, retained to prevent omitted clickable elements:

- {"disabled": false, "label": "Search", "placeholder": null, "tag": "BUTTON", "text": "", "type": null}
- {"disabled": false, "label": "Notifications", "placeholder": null, "tag": "BUTTON", "text": "", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "📖\n\nMemorise Surah Al-Asr\n\nQuran · 3 verses · ~10 min", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "See all", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "📖\n\nProphet Ibrahim\n\nIslamic Stories · Ch.2\n\n60% complete", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "🌙\n\nSurah Al-Mulk\n\nQuran · Verse 8 of 30\n\n35% complete", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "✨\n\nTajweed Basics\n\nArabic · Lesson 4\n\n80% complete", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "See all", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "🎬\n\nStories of the Prophets\n\nEpisode 4 · 12 min left", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "🕌\n\nHow to Pray: Fajr\n\nPrayer Guide · 5 min left", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "⭐\n\nProphet Yusuf (AS)\n\nIslamic Stories\n\nBecause you liked Prophet Ibrahim", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "📿\n\nSurah Al-Asr\n\nQuran · Short Surah\n\nMatches your current level", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "💚\n\nKindness in Islam\n\nAkhlaq · 3 min read\n\nBased on your interests", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Start", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "🌅\nFajr prayer\n+10 XP", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "📖\nQuran reading\n+10 XP", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "📿\nAfternoon dhikr", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "💚\nKind deed today", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "View all", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Bedtime Story\n\nMoonlit Lantern · 8 min", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "🤲\n\nNight Dua\n\nBedtime reflection", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Learn more →", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Home", "type": "button"}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Learn", "type": "button"}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Stories", "type": "button"}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Rewards", "type": "button"}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Profile", "type": "button"}

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
3. Create `NH/Enhanced/034/Child_Home_composite_screen/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Child_Home_composite_screen`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] A2 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
