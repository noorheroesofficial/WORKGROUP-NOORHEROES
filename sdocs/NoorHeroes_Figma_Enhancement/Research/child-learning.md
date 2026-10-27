# A2–A12 Child Learning Research Audit

Documentation only. Original PRDs, blueprints, screenshots and Figma are unchanged.

## Review status and limits

All feature files programmatically extracted; FRs, inventory, key UX and Android mapping plus all KMP objectives reviewed. Exact remaining product/Android/QA sections retained for downstream full review. Do not describe extraction as complete human inspection of every paragraph.

Only the ten images listed below were visually inspected. Remaining screenshot paths are candidate inventories, not verified screen-to-frame mappings. Figma and hosted-mobile inspection are delegated to the parent audit. Religious screenshot content is existing reference content, not independently scholar-verified content.

- `Screens/Mobile App/Home/Home-01.png`
- `Screens/Mobile App/Learn/Skill Tree-01.png`
- `Screens/Mobile App/Stories/Story Detail-01.png`
- `Screens/Mobile App/Bedtime Audio/Audio Player.png`
- `Screens/Mobile App/Du'as/Dua Card-01.png`
- `Screens/Mobile App/Habits/Habit Checklist-01.png`
- `Screens/Mobile App/Quiz Engine/Quiz Question-01.png`
- `Screens/Mobile App/Games/Games Hub-01.png`
- `Screens/Mobile App/Rewards/Rewards Wallet-01.png`
- `Screens/Mobile App/Avatar/Avatar-01.png`

## Verified visual language

Warm cream canvas, deep teal actions and selection, gold rewards/progress, serif display headings, rounded sans body, white rounded cards, neutral outline dividers and soft shadows. These are observations, not measured hex/font/radius tokens. Existing bottom navigation visibly reads Home / Learn / Stories / Rewards / Profile. Avatar has tap-based rotation alternatives. Dua Card shows Arabic/transliteration/translation/audio simultaneously. Story Detail includes scholar-review status, synopsis and resume CTA.

## Conflicts requiring explicit resolution

### CL-10 — Story offline sequential unlock

PRD permits immediate local next-episode unlock after offline completion; blueprint forbids client-side unlock computation and relies only on cached server state.

Sources: A3 §1.10 edge 1; Development_Blueprints/A3_Stories_Module/KMP/02-story-detail-episode-unlock-presentation.md

Approve a signed/package-provided unlock policy or clarify which behavior applies; do not silently suppress offline progression or invent entitlement logic.

### CL-11 — Arabic Letters exercise inventory

FR requires contextual form matching and harakah sound pairing absent from the four-screen inventory.

Sources: A5 §1.7 FR-6; A5 §1.18 rows 8–11

Add two independently reviewable exercise prompts or obtain explicit mapping to existing mode variants; flag absent screenshots.

### CL-12 — Bedtime ending after window boundary

PRD holds visual/narration mode at story start but re-evaluates ending at completion; blueprint launch-time boolean risks holding both.

Sources: A3 §1.10 edge 6; Development_Blueprints/A3_Stories_Module/KMP/05-bedtime-mode-player-experience.md

Approve distinct launch-theme and completion-ending context so entering bedtime mid-story yields calm reflection without theme flicker.

### CL-01 — Rewards Wallet / Daily Missions

Verified screenshot says 3 of 4 done; PRD daily missions are three/day.

Sources: A2 §1.7 FR-4; A11 §1.7 FR-10; Screens/Mobile App/Rewards/Rewards Wallet-01.png

Preserve source screenshot; obtain approval for requirement-driven enhanced variant with three daily missions and validated sample data. Do not silently change copy.

### CL-02 — Quiz Completion Result

UX and blueprint demand equal-weight actions; image prompt assigns filled gold primary to Continue.

Sources: A9 §2.1; A9 §2.2 image-generation prompt; Development_Blueprints/A9_Skill_Tree_Mastery_Engine/KMP/02-quiz-completion-result-screen.md

Seek approval for equal visual weight per normative UX/blueprint; preserve exact action labels.

### CL-03 — Home / Games entry

A10 names Home Trending Games rail, absent from A2 fixed ten-section priority.

Sources: A2 §1.7 FR-1; A10 §2.3

Do not add an eleventh Home section; approve mapping Games entries within existing recommendation section or clarify requirements.

### CL-04 — Rewards rules / Quiz completion

A8 participation reward is accuracy-independent; A11 representative table specifies pass-quiz 100% and >=80% rewards.

Sources: A8 §1.7 FR-5; A9 §1.7 FR-6; A11 §1.7 FR-7

Clarify whether A11 amounts are supplemental accuracy bonuses; no prototype may withhold base effort reward.

### CL-05 — Shared favorites, downloads, subscription, avatar references

Legacy A.14 subscription, A.16 downloads, A.13 search and A.9 avatar references conflict with current C24, B15, B13, A12 IDs.

Sources: A3 §1.18; A6 §1.7 FR-12; A7 §1.18

Use current feature-name destination mapping; record original references and corrected targets explicitly.

### CL-06 — Home first-day CTA

FR uses Let’s start your first mission framing while implementation prompt names Start My First Mission.

Sources: A2 §1.7 FR-15; A2 §7 Android prompt

Obtain exact approved CTA from original frame or content registry; neither phrase silently replaces existing source copy.

### CL-07 — Game Hub

Default, Loading, Offline selectors are visible in reference screenshot; intended production controls versus preview fixture switches is unverified.

Sources: Screens/Mobile App/Games/Games Hub-01.png

Document as reference state demonstration until original interaction inspection confirms purpose.

### CL-08 — Dua badge dismissal

PRD inventory dismiss destination Achievements; KMP blueprint returns to Dua Card/Catalog caller.

Sources: A6 §1.18 row 11; Development_Blueprints/A6_Dua_Learning/KMP/04-dua-master-badge-progress-celebration.md

Approval needed for dismissal versus optional View Achievements action; do not silently select destination.

### CL-09 — Sharing gate order

Stories gate precedes approved preview; rewards inventory preview precedes gate but FR says generating card requires parent verification.

Sources: A3 §1.18 rows 20-21; A11 §1.18 rows 8-9; A11 §1.7 FR-12

Clarify preview privacy and verification order; OS share remains blocked until parent verification.

## A2 — Feature_A2_Home_Dashboard_AI_Personalization

PRD: `PRD_Documents/Child App (1-12)/Feature_A2_Home_Dashboard_AI_Personalization.md`

Coverage: 18 mandatory FR records; all preserved verbatim below. Feature has 21 inventory records including components/states. Components and states must not inflate independently executed screen count.

### Existing screenshot candidates

- `Screens/Mobile App/Home/Home-01.5.png` — inventoried only
- `Screens/Mobile App/Home/Home-01.png` — visually inspected
- `Screens/Mobile App/Home/Home-02.png` — inventoried only
- `Screens/Mobile App/Home/Home-03.5.png` — inventoried only
- `Screens/Mobile App/Home/Home-03.png` — inventoried only
- `Screens/Mobile App/Home/Home-04.png` — inventoried only
- `Screens/Mobile App/Home/Home-05.png` — inventoried only
- `Screens/Mobile App/Home/Home-06.png` — inventoried only
- `Screens/Mobile App/Home/Home-07.png` — inventoried only
- `Screens/Mobile App/Home/Home-08.png` — inventoried only
- `Screens/Mobile App/Home/Home-09.png` — inventoried only
- `Screens/Mobile App/Home/Home-10.png` — inventoried only
- `Screens/Mobile App/Home/Home-11.png` — inventoried only
- `Screens/Mobile App/Home/Home-12.png` — inventoried only
- `Screens/Mobile App/Home/Home-13.png` — inventoried only

### Complete normative functional coverage

### 1.7 Functional Requirements

**FR-1** Home must render the following sections **in this fixed priority order**, not user-reorderable (source §21.8 / §5.8): (1) Greeting/streak/XP bar + notifications + search, (2) Today's Mission, (3) Continue Learning / Continue Watching, (4) Recommended Next Step, (5) Daily Quiz / quick practice, (6) Habit & Good Deed check-in, (7) Weekly Challenge & progress map, (8) Milestones & reward summary, (9) Bedtime Corner (conditional on time window), (10) Islamic Fact of the Day.
**FR-2** Greeting must include the child's name and, where applicable, a reference to the current Islamic occasion (Jummah, Ramadan, Eid, etc.) sourced from an Islamic calendar service.
**FR-3** "Continue Learning/Watching" must surface the furthest-valid resume position per content type (story episode, Quran lesson, quiz-in-progress), sourced from the Progress Service — never duplicate entries for the same content across "Continue Learning" and "Continue Watching" (type-segmented, not content-deduplicated incorrectly).
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
**FR-15** First-day empty state must replace data-dependent sections (Continue Learning, Weekly Challenge, Milestones) with a guided "Let's start your first mission" single CTA rather than rendering empty/broken-looking widgets.
**FR-16** Offline mode must render Home using the last successfully cached payload, visually marked as offline, with only downloaded content actionable; non-downloaded recommended content shows a "download to access offline" affordance rather than a dead link.
**FR-17** Home must refresh its data on: app foreground after >15 minutes background, pull-to-refresh gesture, and immediately after completing any activity that affects its own sections (e.g., completing a habit check-in updates the streak bar in place, not on next full reload).
**FR-18** The Noor companion greeting must vary phrasing/tone across repeated sessions (non-repetitive script pool) to avoid feeling robotic, while staying within scholar-approved language bounds — no AI-freeform-generated greeting text is shown unfiltered.

### Ordered source inventory

### 1.18 Screen Inventory (Complete — Zero Missing)

| # | Screen / Component | Type | Entry Points | Exit Points |
|---|---|---|---|---|
| 1 | Child Home (composite screen) | Primary | Profile Picker, app resume, bottom nav "Home" tab | All feature tabs, Search, Notifications |
| 2 | Greeting / Streak / XP / Notification Bell / Search Bar (header widget) | Component | Top of Home | Notifications screen, Search screen |
| 3 | Today's Mission Card | Component | Home | Relevant feature (Story/Quran/Quiz/Habit) |
| 4 | Continue Learning Rail | Component | Home | Story Detail / Quran Lesson / Quiz-in-progress |
| 5 | Continue Watching Rail | Component | Home | Story Player (video) |
| 6 | Recommended Next Step Card(s) | Component | Home | Relevant content detail screen |
| 7 | Daily Quiz Widget | Component | Home | Quiz Player (inline or full screen) |
| 8 | Habit & Good Deed Check-in Widget | Component | Home | Inline check-in (no nav) / Habit Builder (full) |
| 9 | Weekly Challenge & Progress Map Widget | Component | Home | Weekly Challenge Detail screen |
| 10 | Milestones & Reward Summary Widget | Component | Home | Achievements screen / Rewards Wallet |
| 11 | Bedtime Corner Widget (conditional) | Component | Home, within bedtime window only | Bedtime Mode / Audio Bedtime Player |
| 12 | Islamic Fact of the Day Card | Component | Home | Fact Detail / related Quiz item |
| 13 | First-Day Guided Empty State | Screen variant | Home, zero-activity child | First Mission flow |
| 14 | Offline Home State | Screen variant | Home, no connectivity | Retry / downloaded content |
| 15 | Home Loading Skeleton State | Screen variant | Home, initial/refresh load | Resolves to full Home |
| 16 | "Content No Longer Available" Toast/Modal | Component | Tap on withdrawn content | Dismiss, returns to Home |
| 17 | Parent Summary Preview Widget (Parent-mode "Preview Child Home" sub-view) | Screen variant | Parent Dashboard → "Preview [Child]" | Back to Parent Dashboard |
| 18 | No-Habits-Configured Empty State | Component | Habit widget, zero habits | Parent setup deep link |
| 19 | Zero-Challenge-Participation Empty State | Component | Weekly Challenge widget | Join Challenge action |
| 20 | Zero-Achievement Teaser State | Component | Milestones widget | Achievements screen |
| 21 | Full-Screen Retry (no cache, no network) | Screen | Home, true cold-start offline | Retry → Home |

### Exact mobile UX and behavior sources

### 1.9 Acceptance Criteria

- Given a child with an in-progress story, when Home loads, then "Continue Learning/Watching" shows that story at its last saved position, not from the beginning.
- Given a child profile created today with zero activity, when Home loads, then the First-Day empty-state guided flow renders instead of empty data widgets.
- Given the current time falls within the parent-configured bedtime window, when Home loads, then the Bedtime Corner section is present; outside that window, it is absent entirely from the API response.
- Given the AI Safety Filter rejects a candidate recommendation, when Home renders, then that item never appears in any section, with no visible gap or error indicating something was removed.
- Given a child is offline with cached Home data, when Home loads, then all previously-downloaded actionable items remain tappable, and non-downloaded items show a clear "needs internet/download" state rather than a broken link.
- Given a child checks in a habit directly from the Home widget, when the check-in succeeds, then the streak/XP bar updates in place without a full page reload.
- Given a child's account is in any state, when Home renders, then no subscription/billing/upsell content is present anywhere on the page (verified via automated content-audit test, not just manual QA).
- Given a parent is in an active Parent session and opens "Preview [Child]'s Home," when the preview renders, then it does not re-prompt for PIN and shows the condensed Parent Summary widget overlay, not the child's literal habit-check-in controls.

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

### 1.16 User Flow (Narrative)

Child selects profile from Profile Picker (passes through Child Lock if configured, per A.1) → Home loads (skeleton → progressive section render) → Greeting/streak bar renders first → child either taps Today's Mission, Continue Learning, a Recommended item, the Quiz widget, or a Habit check-in → each tap routes to the relevant feature (Stories/Quran/Quiz/Habits) with the originating Home section recorded for analytics attribution → on completion, child is typically routed back to Home (not deep into another flow), where the relevant section now reflects the completed state.

### 2.1 Home-Specific Design System Extensions

- **Section Card Elevation:** Each Home section uses a consistent card surface (`Surface` token, 12dp radius, soft shadow `0 2px 8px rgba(0,0,0,0.06)` light / glow-based separation in dark theme) so the fixed-order feed reads as a coherent list of distinct "todo" cards, not a single dense page.
- **Age-Group Visual Density:** Ages 4 to 6: larger illustration-to-text ratio, fewer simultaneous on-screen elements per card, bigger tap targets (≥56dp). Ages 6 to 9: balanced icon+text. Ages 9 to 12 / 12 to 15 / 15 to 18+: more text density permitted, smaller decorative illustration footprint, stat-forward (XP numbers, streak counts shown more prominently).
- **Streak/XP Bar:** Always positive-framed — uses a warm gold progress fill, never red/orange "warning" hues even at a broken streak; a missed-streak state shows a "Mercy Day" icon (gentle moon/star) rather than a crossed-out flame.
- **Bedtime Corner Theme:** Automatically applies the app's dimmed Bedtime/Dark theme variant to this single widget even if the rest of Home is in light theme (visually signals "wind-down" contextually).

### 2.2 Home Page Requirements (Full Section Spec)

| Section | Purpose | Components | Empty State | Error State | Loading State | Offline State |
|---|---|---|---|---|---|---|
| Greeting/Streak/XP header | Orientation + quick stats + entry to search/notifications | Noor companion avatar, name greeting text, occasion tag, streak flame-equivalent icon, XP bar, notification bell (badge count), search icon | N/A (always renders once child exists) | Falls back to name-only greeting, no occasion | Shimmer bar | Renders from cache, occasion omitted if stale >24h |
| Today's Mission | Single clear daily focus | Mission card, icon, short label, progress ring if partially done | N/A — system always assigns up to 3 | Hides card if assignment service fails, does not block rest of Home | Shimmer card | Last cached mission shown, marked "may be outdated" only if >24h stale |
| Continue Learning | Resume reading/lesson | Horizontal rail of resume cards w/ progress bar overlay | Section omitted entirely if nothing in progress | Section hides on error | Shimmer rail | Shows only downloaded resumable items |
| Continue Watching | Resume video | Horizontal rail, thumbnail + progress bar | Section omitted if nothing in progress | Section hides on error | Shimmer rail | Shows only downloaded video |
| Recommended Next Step | AI-personalized suggestion(s) | 1–3 cards, "Why this?" optional micro-explanation tag (e.g., "Because you liked Prophet Stories") | Falls back to curated evergreen set (Edge Case 2) | Falls back to evergreen set | Shimmer cards | Shows only downloaded/cached recommendations |
| Daily Quiz | Quick practice | Quiz widget card, "X questions, ~1 min", completed-state checkmark variant | N/A | Hides if quiz service fails | Shimmer card | Cached quiz-of-day playable offline if pre-downloaded |
| Habit & Good Deed Check-in | Frictionless habit logging | Checklist rows (icon + label + checkbox/tap target), streak mini-calendar peek | Friendly parent-setup prompt (no habits) | Optimistic local update even on submit failure (queued) | Shimmer checklist | Fully functional offline, queued sync |
| Weekly Challenge & Progress Map | Multi-day goal visualization | Progress map illustration, % complete, days remaining | "Join Challenge" CTA state | Hides progress map, shows static challenge description | Shimmer | Cached progress shown, "may be outdated" if stale |
| Milestones & Reward Summary | Celebrate recent achievement | Badge/achievement mini-cards, "view all" link | Teaser of next achievable milestone | Hides section | Shimmer | Cached badges shown |
| Bedtime Corner (conditional) | Calm wind-down content | Dimmed-theme card, audio bedtime story shortcut, dua/reflection prompt | N/A (absent outside window) | Section simply absent on error (fails safe to "not shown") | Shimmer (only within window) | Cached bedtime audio playable offline |
| Islamic Fact of the Day | Light daily learning nugget | Fact card, source/scholar badge, optional related-quiz link | N/A — always has a fallback evergreen fact pool | Hides card | Shimmer | Cached fact shown |

### 2.3 Tab Structure

Home is Tab 1 of 5 (Home / Learn / Stories / Rewards / Profile per the Feature Reference navigation table). For every Home-originating click:

| Click Target | Destination Screen | API Called | Analytics Event | Permission Check | Error Handling |
|---|---|---|---|---|---|
| Notification bell | Notifications screen | `GET /v1/notifications` | `notifications_opened` (defined in Feature A.12) | None | Standard list error/empty states |
| Search icon | Search screen | N/A until query typed | `search_opened` (Feature A.13) | None | N/A |
| Today's Mission card | Relevant feature screen (deep link by content_type) | `GET /v1/content/{id}` | `today_mission_started` | Entitlement check (free/premium) | "Content unavailable" graceful toast |
| Continue Learning/Watching item | Story Detail / Quran Lesson / Quiz Player | `GET /v1/progress/{content_id}` | `continue_learning_resumed` / `continue_watching_resumed` | Entitlement + download-availability check if offline | Withdrawn-content graceful handling |
| Recommended card | Relevant content detail | `GET /v1/content/{id}` | `recommendation_clicked` | Entitlement check | Same as above |
| Daily Quiz widget | Inline quiz player (modal) or Quiz tab | `GET /v1/quizzes/daily` | `daily_quiz_started_from_home` | None (quizzes always free-tier accessible per child-safety/equity principle — confirm with Subscription feature) | Quiz-load failure → retry inline |
| Habit checklist row | Inline check-in (no navigation) | `POST /v1/habits/check-ins` | `habit_checkin_completed_from_home` | None | Optimistic update + offline queue |
| Weekly Challenge widget | Weekly Challenge Detail | `GET /v1/challenges/weekly` | `weekly_challenge_widget_viewed` → `_joined` | None | Static fallback description on error |
| Milestones widget | Achievements screen | `GET /v1/children/{id}/achievements` | `milestones_widget_viewed` | None | Teaser fallback |
| Bedtime Corner card | Bedtime Mode / Audio Player | `GET /v1/content/{id}?context=bedtime` | `bedtime_corner_entered` | Download-availability if offline | Section absent if unavailable, no error shown |
| Islamic Fact card | Fact Detail / related quiz | `GET /v1/facts/daily` | `islamic_fact_clicked` | None | Evergreen fallback |

### 2.4 Wireframe Description (Composite)

Single vertically-scrolling screen with a sticky-on-scroll condensed header (avatar + streak only, once the full greeting scrolls past), followed by the 10 sections in strict fixed order, each as a distinct rounded card or horizontally-scrollable rail. No tab/filter controls exist on Home itself (all filtering/personalization happens server-side, invisibly) — this is intentional to avoid turning Home into a "browse" surface, which is reserved for Stories/Learn tabs.

### 2.5 Screen Image Generation Prompts

**Screen: Child Home Dashboard (full composite)**
- *Prompt 1 (English):* "Mobile app home screen UI mockup for a children's Islamic learning app, designed for a child user aged 6-9. Warm, bright, playful flat-vector illustration style. Top header shows a friendly round cartoon companion character (crescent-moon-shaped mascot with a gentle smiling face) next to a greeting text area, a horizontal gold progress/XP bar, a small streak icon shaped like a glowing star, and a notification bell icon. Below, a large rounded card labeled 'Today's Mission' with a simple icon. Below that, a horizontally scrollable row of rounded thumbnail cards with progress bars labeled 'Continue Learning'. Further down, a checklist-style card with rounded checkboxes for habits like prayer, Quran, kind deeds, each with a small icon. Bottom navigation bar with 5 rounded icons: home, book, play, star, profile. Color palette: warm off-white background, teal and gold accents, soft shadows, rounded corners throughout, no sharp edges, no realistic human faces, joyful and calm mood."
- *Prompt 2 (Arabic RTL):* "نفس واجهة الشاشة الرئيسية لتطبيق تعليم إسلامي للأطفال، مصممة لطفل بعمر 6-9 سنوات، بتخطيط كامل من اليمين إلى اليسار. أسلوب رسم متجه دافئ ومرح ومسطح. يعرض الرأس العلوي شخصية كرتونية ودودة على شكل هلال بوجه مبتسم بجانب نص ترحيب، وشريط تقدم ذهبي أفقي للنقاط، وأيقونة صغيرة لمتتالية الإنجاز على شكل نجمة متوهجة، وأيقونة جرس للإشعارات. أسفل ذلك بطاقة كبيرة مستديرة الزوايا بعنوان 'مهمة اليوم' مع أيقونة بسيطة. وتحتها صف قابل للتمرير أفقيًا من البطاقات المصغرة المستديرة مع أشرطة تقدم بعنوان 'استمر في التعلم'. وأسفل ذلك بطاقة على شكل قائمة تحقق بمربعات اختيار مستديرة لعادات مثل الصلاة والقرآن والأعمال الطيبة، كل منها بأيقونة صغيرة. شريط تنقل سفلي بخمس أيقونات مستديرة: الرئيسية، كتاب، تشغيل، نجمة، الملف الشخصي. الألوان: خلفية بيج فاتح دافئ، لمسات فيروزية وذهبية، ظلال خفيفة، زوايا دائرية في كل مكان، بدون وجوه بشرية واقعية، بطابع مرح وهادئ."

**Screen: First-Day Guided Empty State**
- *Prompt 1 (English):* "Mobile app empty-state/welcome screen UI mockup for a children's app, shown on a child's very first day. Centered warm flat-vector illustration of a small friendly crescent-moon mascot waving, surrounded by soft sparkle stars, with a single large rounded gold button below labeled 'Start My First Mission'. Minimal layout, lots of breathing room, warm off-white background, teal and gold accent colors, soft shadows, no clutter, joyful and inviting mood, no realistic human faces."
- *Prompt 2 (Arabic RTL):* "نفس شاشة الترحيب/الحالة الأولى لتطبيق أطفال، تظهر في أول يوم للطفل، بتخطيط من اليمين إلى اليسار. رسمة متجهة دافئة ومسطحة مركزية لشخصية هلال ودودة تلوّح بيدها محاطة بنجوم متلألئة لطيفة، مع زر ذهبي كبير مستدير الزوايا أسفلها بعنوان 'ابدأ مهمتي الأولى'. تخطيط بسيط مع مساحات فارغة كافية، خلفية بيج فاتح دافئ، ألوان فيروزية وذهبية ظلال خفيفة، بدون ازدحام، بطابع مرح ومرحب، بدون وجوه بشرية واقعية."

**Screen: Bedtime Corner Widget**
- *Prompt 1 (English):* "Mobile app widget card UI mockup, dimmed dark-theme 'bedtime mode' card embedded within a lighter home screen. Deep navy/teal night-sky gradient background within the card, small twinkling star illustrations, a crescent moon icon, soft warm gold text reading 'Bedtime Corner', a small play button icon suggesting an audio story, calm and soothing visual tone, rounded card corners, contrasts gently against a brighter surrounding page, no harsh contrast, no realistic faces."
- *Prompt 2 (Arabic RTL):* "نفس بطاقة عنصر واجهة 'ركن وقت النوم' بنمط الوضع الداكن الخافت، مدمجة داخل شاشة رئيسية أكثر إضاءة، بتخطيط من اليمين إلى اليسار. خلفية متدرجة بلون كحلي وفيروزي غامق يشبه سماء الليل داخل البطاقة، رسومات نجوم متلألئة صغيرة، أيقونة هلال، نص بلون ذهبي دافئ وهادئ بعنوان 'ركن وقت النوم'، أيقونة زر تشغيل صغيرة تشير إلى قصة صوتية، طابع بصري هادئ ومريح للغاية، زوايا بطاقة مستديرة، تباين لطيف مع الصفحة المحيطة الأكثر سطوعًا، بدون تباين قاسٍ وبدون وجوه بشرية واقعية."

*(Remaining widget-level screens — Habit Checklist, Daily Quiz Widget, Weekly Challenge Map, Milestones Summary, Islamic Fact Card, Parent Summary Preview, Offline State, Loading Skeleton — follow the same two-prompt EN/AR template using the Global Design System tokens from A.1 §2.1; full set generated on request.)*

---

### 6.1 Technical Requirements
Kotlin, Jetpack Compose, MVVM, Clean Architecture, module `:feature:home`, depends on `:core:design-system`, `:core:network`, `:core:offline-cache`. Pure ranking-irrelevant logic (e.g., bedtime-window evaluation for client-side display nuance, streak display formatting) is KMP-shareable.

### 6.2 Screen Mapping
`HomeScreen` Composable composed of independent section Composables (`TodayMissionSection`, `ContinueLearningRail`, `HabitChecklistSection`, etc.), each driven by its own slice of a single `HomeUiState` exposed from `HomeViewModel` as `StateFlow<HomeUiState>` — sections render independently so a slow/failed section never blocks others (mirrors backend's graceful per-section degradation).

### 6.3 Navigation Flow
Home is the default start destination of the main bottom-nav graph. Each section item navigates via a typed `NavigationEvent` sealed class consumed once (no re-trigger on rotation/recomposition) routing to the appropriate feature module's entry point.

### 6.4 State Management
`HomeUiState` models each section as `Loading | Content(data) | Error | Hidden` independently (not one global enum for the whole screen) — this directly reflects the backend's per-section null/degraded contract. Optimistic updates for habit check-ins mutate local state immediately, with a reconciliation step against the server response (or queued offline job) afterward.

### 6.5 API Mapping
`HomeRepository.getHome()` → `GET /v1/home`; `HabitRepository.checkIn()` → `POST /v1/habits/check-ins` with a locally-generated `client_event_id` (UUID) attached at the moment of tap, reused on any retry.

### 6.6 Analytics Mapping
`HomeAnalytics` interface fires `home_viewed` once per successful render (not per recomposition) and `home_section_rendered` once per section as each resolves — implemented via a one-shot `LaunchedEffect` keyed on the resolved-section identity, not on every state emission.

### 6.7 Offline Support
`HomeLocalCache` (Room) stores the last successful `/v1/home` payload per `child_id`; on cold start without connectivity, render from this cache immediately, then attempt a background refresh. Habit check-ins write to a local outbox table and sync via WorkManager on reconnect, using the same `client_event_id` idempotency pattern as the backend.

### 6.8 Deep Linking
`noorheroes://home/section/{section_id}` supported for push-notification deep links (e.g., a habit-reminder notification opens Home scrolled to the Habit section, not a separate screen).

### 6.9 Push Notifications
Home itself does not send notifications, but is the landing target for habit-reminder, mission-reminder, and streak-encouragement notifications managed by Feature A.12 (Notifications) and A.7 (Habit Tracker) — this feature only needs to support the scroll-to-section deep link target.

### 6.10 Testing Strategy
- Unit: `HomeViewModel` state-reduction logic per section, including the "first-day empty state" branching and bedtime-window display logic.
- Compose UI tests: each section's Loading/Content/Error/Hidden visual states independently, snapshot tests verifying section order never changes.
- Integration: full Home load with simulated backend partial-failure responses (mocked per-section nulls) verifying graceful degradation client-side.
- Content-safety regression test: an automated UI test that asserts no view in the Home screen tree contains text matching a billing/subscription term blocklist (Android-side mirror of the backend audit test).

---

### 13.1 Test Plan Summary
Coverage spans: fixed-section-order verification, graceful per-section degradation, billing-content-absence audit (the feature's signature non-negotiable test), offline caching/sync, bedtime-window edge cases, multi-child session isolation, and all 12 edge cases from §1.10.

### 13.2 Test Cases — Happy Path
1. Child with in-progress story, active habit streak, and an active weekly challenge opens Home → all 10 sections (minus conditional Bedtime Corner if outside window) render with correct data within performance targets.
2. Child checks in all configured habits directly from Home → streak/XP bar updates in place, no full reload.
3. Child taps a Recommended card → routes correctly to the content detail screen with the originating section recorded in analytics.

### 13.3 Edge Cases
All 12 items from §1.10, each as a discrete test case.

### 13.4 Negative Cases
- Recursively scan a full matrix of `/v1/home` fixture responses (free/premium/trial-expired/various locales) for billing-blocklist terms → must return zero matches, automated, blocking CI.
- Submit duplicate habit check-in (same `client_event_id`, replayed) → exactly one `habit_checkin` row exists in DB afterward.
- Force Recommendation Service to time out → `/v1/home` still returns `200` with `recommended` falling back to evergreen content within the same response.
- Request `/v1/home` with a token scoped to a different child than the one referenced by a manually-tampered path/header → `403`, zero data leakage in the response body (not even an error message confirming the other child's existence).

### 13.5 Regression Cases
Full Home suite re-run on every release touching `:feature:home`, Home Aggregation Service, Recommendation Service, or the AI Safety Filter — gated pre-merge.

### 13.6 Automation Cases
End-to-end: cold-start-offline-with-cache scenario, bedtime-window-crossing-midnight scenario, first-day-empty-state scenario, full content-safety-audit matrix (automated, CI-blocking, re-run nightly against production-sampled data as well).

---

### Corresponding KMP blueprint requirements

#### `Development_Blueprints/A2_Home_Dashboard_AI_Personalization/KMP/01-home-screen-composition-state-management.md`

##### 4. Objective
Build the `:feature:home` module's `HomeScreen` Composable as a composition of independent section Composables, each driven by its own slice of a single `HomeUiState` exposed via `HomeViewModel: StateFlow<HomeUiState>`, where each section is modeled as `SectionState { Loading, Content(data), Error, Hidden }` — mirroring the backend's per-section graceful-degradation contract from B-01.

##### 5. Business Requirements
Per PRD §6.1–6.4, §1.13, FR-1:
- Sections render in the exact fixed priority order (Greeting/Streak/XP → Today's Mission → Continue Learning → Continue Watching → Recommended → Daily Quiz → Habits → Weekly Challenge → Milestones → Bedtime Corner (conditional) → Islamic Fact); a Compose UI test must fail the build if reordered.
- Each section resolves independently — a slow/failed section never blocks others.
- Skeleton-screen loading per section (shimmer placeholders matching widget shape), not one full-screen spinner.
- Pull-to-refresh with brand-consistent (non-default-platform) indicator.
- Refresh triggers: app foreground after >15 min background, pull-to-refresh, immediately after any activity affecting Home's own sections.

##### 11. KMP Requirements
- `HomeUiState` models each of the 10 sections as an independent `SectionState` field (not one global loading/error flag).
- `HomeScreen` composed of independent section Composables, each collecting only its own state slice to minimize recomposition scope.
- Skeleton/shimmer Composable per section shape, shown during `Loading`.
- Pull-to-refresh gesture wired to `HomeViewModel.refresh()`.
- Foreground-resume-after-15-min-background triggers refresh via lifecycle observer.
- `home_viewed` analytics fired once per successful render (one-shot `LaunchedEffect` keyed on resolved-section identity, not on every state emission) — reuse `NoorHeroes/core/core-analytics/CORE_ANALYTICS_INSTRUCTIONS.md` conventions.

##### 15. Validation
`HomeUiState` mapping from the network DTO must handle a `null` `bedtime_corner` correctly as `SectionState.Hidden`, distinct from `SectionState.Error`.

##### 18. Error Handling
Each section's `SectionState.Error` renders a section-local, non-blocking error affordance (not a full-screen error) per the backend's per-section degradation contract. Full-payload fetch failure (no cache, true first launch offline) is K-07's scope (Full-Screen Retry state).

##### 19. Offline First
This sub-feature defines the state model that K-07's offline cache reads into; `HomeRepository` interface here should be cache-agnostic (K-07 implements the cache-first strategy behind this interface).

##### 21. Localization
All section labels/copy sourced from shared string resources per `CORE_UI_INSTRUCTIONS.md` convention; no hardcoded user-facing strings.

##### 22. RTL
Full layout mirroring for Arabic/Urdu via Compose's built-in `LayoutDirection` — verify horizontal rails and icons (e.g., back/forward affordances) mirror correctly.

##### 25. Security
Content-safety regression UI test (recursive semantics-tree scan for billing-term blocklist) — client-side mirror of B-08's backend audit, non-negotiable per PRD §7 item 5.

##### 27. Testing
- Unit: `HomeViewModel` state-reduction per section, including first-day branching (though First-Day full behavior is K-07's scope, the state-shape support belongs here).
- Compose UI: each section's Loading/Content/Error/Hidden states independently rendered.
- Compose UI: section-order snapshot/semantics-tree traversal test that fails the build if reordered.
- Compose UI: content-safety regression test (billing-term blocklist scan across the rendered tree, multiple fixture states).

##### 31. Final Verification Checklist
- [ ] Section order matches FR-1 exactly, verified by a build-failing snapshot test
- [ ] Each section state (Loading/Content/Error/Hidden) independently verified via Compose UI tests
- [ ] `HomeUiState`/section models are `@Immutable`/`@Stable`
- [ ] Client-side content-safety regression test passes with a working canary
- [ ] `home_viewed`/`home_section_rendered` analytics fire correctly (once per render/resolution, not per recomposition)
- [ ] RTL layout verified for section order and mirroring
- [ ] Pull-to-refresh and 15-minute background-resume refresh triggers verified
- [ ] No colors/spacing/typography redefined outside `:core:design-system`

#### `Development_Blueprints/A2_Home_Dashboard_AI_Personalization/KMP/02-continue-learning-watching-resume-rails.md`

##### 4. Objective
Build the two resume rails as independent section Composables plugging into K-01's `HomeUiState`, consuming B-05's `/v1/progress/resume` data (via B-01's aggregated response), with correct empty/error/offline behavior.

##### 5. Business Requirements
Per PRD FR-3, §2.2, §2.3:
- Type-segmented rails (no cross-type dedup bleed).
- Section omitted entirely (not empty placeholder) when nothing in progress.
- Section hides on error, other sections unaffected.
- Offline: shows only downloaded resumable items.
- Tap routes to Story Detail/Quran Lesson/Quiz Player with entitlement + download-availability check.
- Withdrawn-content tap → graceful "no longer available" + silent cache removal.

##### 11. KMP Requirements
- Horizontal rail Composable with progress-bar overlay per card.
- Omit rail entirely (`SectionState.Hidden`) when the item list is empty — not an empty rail shell.
- Filter to downloaded-only items when `HomeUiState` indicates offline mode (coordinate flag/source with K-07).
- Tap handler performs entitlement + download-availability check before navigating (reuse existing entitlement-check utility from the platform if one exists, e.g., from Subscription/Entitlement feature — do not reimplement).
- Withdrawn-content tap: catch a specific "content unavailable" signal from the navigation/detail-fetch call, show a toast, and remove the item from local state/cache.

##### 15. Validation
Distinguish `SectionState.Hidden` (nothing in progress) from `SectionState.Error` (Progress Service failure) — both result in no visible content, but only `Error` should log/telemetry-flag as a degradation event.

##### 18. Error Handling
Section hides silently on `Error` state (no error banner shown to child, per PRD §2.2 table: "Section hides on error"). Withdrawn-content tap shows a graceful toast, not a raw error.

##### 19. Offline First
Rail filters to downloaded-only items when offline; non-downloaded resumable items are simply excluded from the rail in offline mode (not shown disabled) per K-01/K-07's offline state contract.

##### 21. Localization
Card titles/labels via string resources; content titles are pre-localized from the backend.

##### 22. RTL
Rail scroll direction mirrors correctly in RTL locales (verify horizontal scroll gesture direction, not just text alignment).

##### 25. Security
N/A beyond standard entitlement checks (no new security surface).

##### 27. Testing
- Compose UI: rail renders correctly with 1, multiple, and zero items (zero → section hidden entirely).
- Compose UI: error state hides section without visible error UI.
- Unit: offline filtering logic (downloaded-only inclusion).
- Integration: withdrawn-content tap shows toast and removes item from local list.

##### 31. Final Verification Checklist
- [ ] Rails omitted entirely (not empty shell) when nothing in progress
- [ ] Rails hide silently on Progress Service error
- [ ] Offline mode filters to downloaded-only items
- [ ] Withdrawn-content tap shows graceful toast and removes item locally
- [ ] Type-segmentation confirmed (no learning/watching cross-bleed)
- [ ] RTL scroll direction verified
- [ ] All tests pass

#### `Development_Blueprints/A2_Home_Dashboard_AI_Personalization/KMP/03-habit-checkin-widget-offline-sync.md`

##### 4. Objective
Build the habit checklist Composable with optimistic local updates, a Room-backed offline outbox using tap-time-generated idempotent `client_event_id`s, WorkManager-based retry on reconnect, and correct handling of `409 ALREADY_CHECKED_TODAY` as success (not rollback).

##### 5. Business Requirements
Per PRD FR-7, FR-8, §6.7, §7 item 3, Edge Case 10:
- Same-screen check-in for at least Salah, Quran, dua, good deed, dhikr; deep-link to full Habit Builder for fasting/detailed logging.
- Streak display never shaming (gold fill, "Mercy Day" icon, never red warning).
- Optimistic UI update on tap, before network resolves.
- Offline: queue to local outbox with tap-time `client_event_id`, retry via WorkManager on reconnect, reusing the same UUID.
- `409 ALREADY_CHECKED_TODAY` treated as success — must NOT roll back the optimistic UI.
- Reconcile locally-queued offline check-ins in causal order on reconnect (deduplicated via idempotency keys) before showing "live" data, avoiding a visible streak regression flash.
- Empty state: friendly "ask a grown-up to set up your first habit" prompt when zero habits configured.

##### 11. KMP Requirements
- Checklist rows (icon + label + tap target) per configured habit.
- Tap → immediate optimistic local state update (checkbox ticks) before network call resolves.
- On network failure, write to Room outbox with a UUID `client_event_id` generated **at tap time** (not retry time), enqueue `HabitCheckinSyncWorker`.
- On `409 ALREADY_CHECKED_TODAY` response, treat as success — do not roll back the optimistic tick.
- On a genuine permanent failure (e.g., validation error, not network/idempotent-duplicate), roll back the optimistic tick and surface a subtle retry affordance.
- Streak mini-calendar peek; Mercy Day icon (gentle moon/star) instead of a crossed-out flame on a missed day.
- Deep link "Habit Builder" for fasting tracker/detailed logging.
- Empty state Composable when zero habits configured.

##### 15. Validation
`client_event_id` generated once per tap and persisted with the outbox entry — retries must reuse the same ID, never regenerate.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Network failure on tap | Optimistic tick stands; queued to outbox; subtle "saving..." indicator |
| `409 ALREADY_CHECKED_TODAY` | Treated as success; no rollback |
| Genuine validation failure (e.g., invalid habit_id) | Roll back optimistic tick; show retry affordance |
| Zero habits configured | Friendly setup-prompt empty state, not an empty checklist |

##### 19. Offline First
This is the offline-first reference implementation for the Home feature: full write capability offline via the outbox, synced on reconnect in causal (submission) order, deduplicated via `client_event_id`.

##### 21. Localization
Habit labels via string resources or pre-localized backend strings (follow K-01's established pattern); empty-state copy localized.

##### 22. RTL
Checklist row layout (icon + label + checkbox) mirrors correctly; streak mini-calendar peek direction verified for RTL.

##### 25. Security
`client_event_id` is a client-generated UUID, not guessable/sequential; no sensitive data in the outbox beyond habit/date references.

##### 27. Testing
- Unit: optimistic update applies immediately on tap.
- Unit: `409` response does NOT trigger rollback (explicit regression test per PRD §7 item 8).
- Unit: genuine failure DOES trigger rollback.
- Integration: offline tap → outbox entry created → reconnect → `HabitCheckinSyncWorker` syncs → outbox entry cleared.
- Integration: causal-order reconciliation with multiple queued check-ins avoids a visible streak regression flash.

##### 31. Final Verification Checklist
- [ ] Optimistic tick applies immediately on tap
- [ ] `409 ALREADY_CHECKED_TODAY` does not roll back the optimistic UI
- [ ] Genuine validation failure does roll back with a retry affordance
- [ ] Offline check-ins queue with tap-time `client_event_id`, reused on retry
- [ ] Reconnect sync processes queue in causal order, no duplicate server-side rows
- [ ] Streak visuals never use shaming/red treatment; Mercy Day icon used correctly
- [ ] Empty state shown when zero habits configured
- [ ] All tests pass

#### `Development_Blueprints/A2_Home_Dashboard_AI_Personalization/KMP/04-daily-mission-quiz-widgets.md`

##### 4. Objective
Build both widgets as independent Composables with correct completed-state rendering (no re-assignment/replay on same-day re-open), consuming B-04 (missions) and the quiz-of-day data surfaced via B-01.

##### 5. Business Requirements
Per PRD FR-4, Edge Case 6, Edge Case 11, §2.2:
- Today's Mission: system-assigned, progress ring if partial, completed state with positive reinforcement on re-open (not re-assignment).
- Daily Quiz: "X questions, ~1 min," completed/celebratory state after finishing; not replayable same day by default (unless retry-for-mastery explicitly enabled — default not-replayable).
- Both hide gracefully on their respective service failure.
- Quiz cached for offline play if pre-downloaded.

##### 11. KMP Requirements
- Mission card: icon, short label, progress ring if partially done; completed state shows positive-reinforcement visual, not a "come back tomorrow" negative framing.
- Quiz widget: question count + estimated time; completed-state checkmark variant; tapping a completed quiz does not relaunch it (default), shows the celebratory state instead.
- Tap routes to relevant feature screen (deep link by `content_type`) with entitlement check, per PRD §2.3.
- Quiz-of-day playable offline if pre-downloaded (reuse existing offline-download availability check from K-02/B.15).

##### 15. Validation
`completed_today` flag from backend is authoritative for quiz replay-blocking — client must not infer completion from local state alone (avoids drift if the child completes the quiz on a different device).

##### 18. Error Handling
Both widgets hide gracefully (`SectionState.Error` → hidden) on their respective service failure, per PRD §2.2 table ("Hides if quiz service fails" / assignment-service failure hides card).

##### 19. Offline First
Quiz-of-day playable offline if pre-downloaded; mission card shows last-cached mission if stale (>24h marked "may be outdated" per PRD §2.2 table — coordinate exact staleness-marking behavior with K-07's offline cache implementation).

##### 21. Localization
Widget labels via string resources; mission/quiz titles pre-localized from backend.

##### 22. RTL
Progress ring and checkmark iconography mirror appropriately (progress ring direction should remain visually consistent, not literally mirrored in a confusing way — follow existing Design System RTL guidance for circular progress indicators).

##### 25. Security
N/A beyond standard entitlement checks.

##### 27. Testing
- Compose UI: mission card renders correctly for incomplete/partial/completed states.
- Compose UI: quiz widget renders correctly for not-started/completed states; tapping completed quiz does not relaunch it.
- Unit: `completed_today` flag correctly drives replay-blocking (server-authoritative, not locally inferred).
- Compose UI: both widgets hide on `Error` state.

##### 31. Final Verification Checklist
- [ ] Mission completed state shows positive reinforcement, no re-assignment same day
- [ ] Quiz completed state blocks replay by default (server-authoritative flag)
- [ ] Both widgets hide gracefully on respective service error
- [ ] Progress ring and checkmark render correctly across all states
- [ ] All tests pass

#### `Development_Blueprints/A2_Home_Dashboard_AI_Personalization/KMP/05-weekly-challenge-milestones-widgets.md`

##### 4. Objective
Build both widgets consuming B-06's challenge/achievement data, with correct empty-state handling (Join Challenge CTA, next-achievable teaser) rather than blank modules.

##### 5. Business Requirements
Per PRD §2.2:
- Weekly Challenge: progress map illustration, % complete, days remaining; "Join Challenge" CTA state when zero participation; static description on error (not blank).
- Milestones: badge/achievement mini-cards, "view all" link; teaser of next achievable milestone when zero achievements (not blank).

##### 11. KMP Requirements
- Weekly Challenge widget: progress map, percent complete, days remaining; if `challenge == null`, render "Join Challenge" CTA state with challenge description instead of a progress bar.
- Milestones widget: recent badge mini-cards + "view all" link to Achievements screen; if zero recent unlocks, render `next_teaser` as a preview card, not a blank module.
- Join action calls the join endpoint and optimistically updates to the joined/in-progress visual.

##### 15. Validation
Distinguish "no active challenge" (`null` object, valid state → Join CTA or description-only) from "Challenge Service error" (static fallback description, per PRD §2.2 table) — these produce similar-looking UI but different telemetry.

##### 18. Error Handling
Challenge widget: static fallback description + hidden progress map on error. Milestones widget: hides on error (per PRD §2.2 table "Hides section").

##### 19. Offline First
Cached progress/badges shown with "may be outdated" marker if stale, consistent with K-07's offline cache contract.

##### 21. Localization
Widget labels, challenge title, badge titles via string resources/pre-localized backend strings.

##### 22. RTL
Progress map illustration and days-remaining counter mirror correctly; badge mini-card row scrolls in correct RTL direction.

##### 25. Security
N/A beyond standard scoped-session access.

##### 27. Testing
- Compose UI: challenge widget renders correctly for null-challenge (Join CTA), joined-in-progress, and error states.
- Compose UI: milestones widget renders correctly for zero-achievements (teaser) and populated states.
- Unit: join action optimistic-update logic.

##### 31. Final Verification Checklist
- [ ] Challenge widget shows Join CTA (not progress bar) when unjoined
- [ ] Challenge widget shows static description (not blank) on service error
- [ ] Milestones widget shows next-achievable teaser (not blank) on zero achievements
- [ ] Milestones widget hides on service error
- [ ] Join action optimistic update reconciles correctly with server response
- [ ] All tests pass

#### `Development_Blueprints/A2_Home_Dashboard_AI_Personalization/KMP/06-bedtime-corner-conditional-widget.md`

##### 4. Objective
Build the Bedtime Corner Composable that emits no node at all when the corresponding state is null/absent (never an empty card/placeholder), automatically applies the dimmed Bedtime theme variant to itself regardless of the rest of Home's theme, and routes to Bedtime Mode/Audio Bedtime Player.

##### 5. Business Requirements
Per PRD FR-12, Edge Case 4, §2.1, §7 item 2:
- Section present only within the parent-configured bedtime window for that specific child; server evaluates the window and returns `null` outside it (present key, null value).
- Client must render nothing (no node emitted) when null — not an empty/placeholder card.
- Bedtime Corner theme automatically applies the dimmed/dark theme variant to this single widget even if the rest of Home is in light theme.
- Cached bedtime audio playable offline if pre-downloaded.

##### 11. KMP Requirements
- Composable returns/emits nothing when `SectionState.Hidden` (mapped from backend `null`) — verified via a semantics-tree test asserting zero nodes for this section's test-tag when hidden.
- When present, wraps content in a locally-scoped dark/dimmed theme override (`CompositionLocalProvider` for the theme, scoped only to this Composable's subtree) independent of the rest of Home's theme.
- Tap routes to Bedtime Mode / Audio Bedtime Player via deep link/content_id, per PRD §2.3.
- Content playable offline if pre-downloaded (reuse existing offline-download availability check).

##### 15. Validation
Client must not perform its own bedtime-window time calculation to decide visibility — the server (B-01) is the single source of truth per FR-12; client only reacts to `null` vs. present.

##### 18. Error Handling
Section absent on error (fails safe to "not shown"), per PRD §2.2 table — identical visual outcome to the normal "outside window" `null` case, but should be distinguishable in internal telemetry (error vs. legitimately-outside-window).

##### 19. Offline First
Cached bedtime audio playable offline if pre-downloaded, per PRD §2.2/§1.14.

##### 21. Localization
Widget copy via string resources; content title pre-localized.

##### 22. RTL
Dimmed-theme card layout mirrors correctly; verify the "wind-down" visual composition (moon/star icon placement) is appropriately mirrored per Design System RTL guidance rather than literally flipped if that would look wrong (confirm against Figma RTL mockup, per PRD §2.5 Bedtime Corner Arabic RTL prompt).

##### 25. Security
N/A beyond standard scoped-session access.

##### 27. Testing
- Compose UI: zero semantics nodes emitted when state is `Hidden`/null (explicit absence test, not just "invisible").
- Compose UI: dimmed theme correctly scoped to only this widget's subtree when rest of Home is in light theme.
- Compose UI: tap routes correctly to Bedtime Mode/Audio Player.

##### 31. Final Verification Checklist
- [ ] Zero semantics nodes emitted when hidden (verified, not assumed)
- [ ] Dimmed theme scoped only to this widget, rest of Home unaffected
- [ ] Client does not perform its own bedtime-window time calculation
- [ ] Fails safe (absent) on error, same visual as legitimately-outside-window
- [ ] Cached audio playable offline if pre-downloaded
- [ ] All tests pass

#### `Development_Blueprints/A2_Home_Dashboard_AI_Personalization/KMP/07-home-offline-cache-first-day-deep-linking.md`

##### 4. Objective
Implement `HomeLocalCache` (Room) persisting the last successful `/v1/home` payload per `child_id`, cache-first cold-start rendering with a persistent non-alarming offline badge, strict per-`child_id` cache isolation on profile switch, the First-Day guided empty-state branching, causal-order offline habit-check-in reconciliation on reconnect, and the `noorheroes://home/section/{section_id}` deep link.

##### 5. Business Requirements
Per PRD FR-15, FR-16, Edge Case 7, Edge Case 10, §6.7, §6.8, §7 items 4, 6, 7:
- Full cached-Home rendering with persistent, non-alarming offline indicator; never a blank/error screen if a cache exists.
- Cache strictly keyed per `child_id`, cleared/isolated on profile switch (zero cross-child leakage).
- First-Day empty state: replaces Continue Learning/Weekly Challenge/Milestones with a single "Start My First Mission" CTA, state-driven conditional render (not a separate screen/Activity).
- True first-launch offline (no cache, no network): friendly retry screen, never a raw technical error.
- Deep link scrolls to the matching section without re-triggering a full data reload if the screen is already in memory.
- Reconcile locally-queued offline habit check-ins in causal order before showing "live" data, avoiding a visible streak regression flash (shared responsibility with K-03; this sub-feature owns the reconciliation-before-render sequencing at the Home level).

##### 11. KMP Requirements
- `HomeLocalCacheDao` stores the last successful full `/v1/home` response payload (serialized) per `child_id`.
- `HomeRepositoryImpl.getHome()`: on cold start, read cache immediately for instant render, then attempt a background network refresh; on refresh success, update cache and `HomeUiState`; on refresh failure, keep showing cached data with an offline badge.
- Cache read/write strictly scoped by `child_id`; on profile switch, clear (or simply never read) another child's cache entry — verified via an explicit isolation test (Multiple siblings sharing a device, per Edge Case 7).
- `is_first_day == true` → `HomeUiState` carries a flag that `HomeScreen` (K-01) uses to swap Continue Learning/Weekly Challenge/Milestones for a single `FirstDayEmptyState` CTA Composable.
- True cold-start-offline-no-cache → render `FullScreenRetry` (friendly copy, retry control), never a raw error.
- Deep link handler resolves `section_id`, and if `HomeScreen` is already composed/in memory, scrolls to it via `bringIntoViewRequester` without a full data reload; if not in memory, launches Home normally then scrolls once loaded.
- Reconciliation sequencing: on reconnect, wait for K-03's outbox sync to complete (or timeout) before treating the next `HomeUiState` refresh as "live," to avoid a visible streak regression flash.

##### 15. Validation
Deserialized cache payload validated against the same `HomeUiState`-mapping logic as a fresh network response, so a stale/malformed cache entry degrades gracefully (e.g., falls through to `FullScreenRetry` if truly corrupt) rather than crashing.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Cache exists, network fails | Render cached data + offline badge, never blank/error |
| No cache, no network (true first launch offline) | `FullScreenRetry` with retry control |
| No cache, network succeeds | Normal render |
| Corrupt/unparseable cache entry | Treated as no-cache; fall through to network or `FullScreenRetry` |

##### 19. Offline First
This sub-feature is the primary implementation of Home's offline-first contract:
```
Remote Data (GET /v1/home)
   ↓
HomeRepositoryImpl (cache-first read, background refresh)
   ↓
HomeLocalCache (Room, keyed by child_id)
   ↓
HomeUiState → HomeScreen
```
Scenarios: initial local load, remote refresh, offline read, retry, sync (habit outbox via K-03), cache invalidation (on refresh success), network recovery (reconciliation sequencing).

##### 21. Localization
Cached payload retains whatever localization was baked into the response at cache time; if the child's language changes, the next successful network refresh supersedes the stale-language cache (acceptable per existing platform convention — flag if a more aggressive cache-invalidation-on-language-change behavior is required elsewhere in the app).

##### 22. RTL
`FirstDayEmptyState` and `FullScreenRetry` Composables follow the same RTL mirroring rules as the rest of Home.

##### 25. Security
Cache isolation per `child_id` is the primary security-adjacent concern (prevents a sibling profile switch from momentarily showing stale data belonging to another child) — verify via the explicit isolation test, not just by code review.

##### 27. Testing
- Unit: cache-first read returns cached data immediately, then updates after background refresh.
- Integration: cache-isolation test — switch between two child profiles on the same device, assert no fragment of child A's cached data ever renders for child B, even momentarily.
- Compose UI: `FirstDayEmptyState` renders correctly when `is_first_day=true`, replacing exactly the three specified sections.
- Compose UI: `FullScreenRetry` renders on true cold-start-offline (no cache, no network).
- Integration: deep link to an already-in-memory `HomeScreen` scrolls without a full reload; deep link to a cold-started Home launches then scrolls once loaded.
- Integration: reconnect sequencing — outbox sync (K-03) completes before the next "live" Home render, no visible streak regression flash.

##### 31. Final Verification Checklist
- [ ] Cold start with cache renders instantly, background-refreshes silently
- [ ] Cold start with no cache and no network shows `FullScreenRetry`, never a raw error
- [ ] Cache strictly isolated per `child_id`, verified via rapid profile-switch test
- [ ] First-Day empty state replaces exactly the three specified sections, state-driven not a separate screen
- [ ] Deep link to an in-memory Home scrolls without reload; cold-start deep link launches then scrolls
- [ ] Offline habit reconciliation sequenced before "live" render, no visible streak regression flash, bounded timeout respected
- [ ] All tests pass

#### `Development_Blueprints/A2_Home_Dashboard_AI_Personalization/KMP/08-parent-summary-preview-submode.md`

##### 4. Objective
Build the Parent Summary Preview overlay that renders a condensed "today's progress" widget when a parent is in an active Parent session, without re-prompting for PIN and without exposing the child's interactive habit-check-in controls.

##### 5. Business Requirements
Per PRD FR-14, §1.9 Acceptance Criteria, §1.18 Screen 17:
- Visible only when the Parent Profile views a child's Home in "preview" sub-mode, not visible to the child.
- Shows today's completed activities and healthy-usage status.
- Does not require full Parent PIN re-entry if already in an active Parent session.
- Renders the condensed Parent Summary widget overlay, not the child's literal habit-check-in controls.

##### 11. KMP Requirements
- `HomeScreen(previewMode: Boolean = false)` — when `true`, renders `ParentSummaryPreviewOverlay` instead of the full interactive section stack.
- Overlay shows: today's completed activities summary, healthy-usage status (e.g., screen-time-within-limits indicator) — condensed, not the full section-by-section child view.
- No interactive habit-check-in controls rendered in this mode (read-only).
- No PIN re-prompt if `ParentSessionState.isActive == true` (checked via existing C.19 session mechanism) — reuse, do not duplicate the check.
- "Back to Parent Dashboard" exit action.

##### 15. Validation
Preview mode must never expose the child's actual interactive controls (e.g., tapping a "completed activity" in the summary must not trigger a habit check-in mutation) — this is a rendering-mode distinction enforced by using a distinct, non-interactive Composable (`ParentSummaryPreviewOverlay`), not by disabling interactive controls after the fact.

##### 18. Error Handling
Same per-section graceful degradation as child-mode Home (inherits `HomeUiState`'s existing Loading/Content/Error/Hidden handling), condensed into the summary view.

##### 19. Offline First
Not a primary offline scenario for this sub-feature (parent preview is a lower-frequency, typically-online interaction); if offline, reuse K-07's existing cache-or-network behavior as-is rather than building a parallel path.

##### 21. Localization
Overlay copy via string resources, parent-facing tone (per A.1's parent-facing localization conventions, distinct from child-facing copy tone).

##### 22. RTL
Overlay layout mirrors correctly per existing parent-facing screen RTL conventions (from A.1's Parent PIN Setup/Add Child screens).

##### 25. Security
No interactive child-mode mutation paths reachable from this overlay (§15); reuses existing Parent session/authorization checks rather than introducing a new, potentially weaker check.

##### 27. Testing
- Compose UI: preview overlay renders condensed summary correctly, with no interactive habit-check-in controls present in the semantics tree.
- Integration: active Parent session does not trigger a PIN re-prompt when entering preview mode.
- Integration: preview mode correctly blocks any attempt to trigger a child-mode mutation (e.g., simulate a tap on a summary item, assert no `POST /v1/habits/check-ins` call is made).

##### 31. Final Verification Checklist
- [ ] Overlay contains zero interactive child-mode controls in its semantics tree
- [ ] No PIN re-prompt occurs when entering preview during an active Parent session
- [ ] No mutation API call (e.g., habit check-in) can be triggered from the overlay, verified by test
- [ ] Authorization reuses existing C.19/C.20 checks, no new/weaker check introduced
- [ ] RTL and parent-facing localization verified
- [ ] All tests pass

## A3 — Feature_A3_Stories_Module

PRD: `PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md`

Coverage: 20 mandatory FR records; all preserved verbatim below. Feature has 29 inventory records including components/states. Components and states must not inflate independently executed screen count.

### Existing screenshot candidates

- `Screens/Mobile App/Stories/Bedtime Player.png` — inventoried only
- `Screens/Mobile App/Stories/Choice.png` — inventoried only
- `Screens/Mobile App/Stories/Complete.png` — inventoried only
- `Screens/Mobile App/Stories/Moral Card.png` — inventoried only
- `Screens/Mobile App/Stories/Player.png` — inventoried only
- `Screens/Mobile App/Stories/Stories-01.png` — inventoried only
- `Screens/Mobile App/Stories/Stories-02.png` — inventoried only
- `Screens/Mobile App/Stories/Stories-03.png` — inventoried only
- `Screens/Mobile App/Stories/Stories-04.png` — inventoried only
- `Screens/Mobile App/Stories/Stories-05.png` — inventoried only
- `Screens/Mobile App/Stories/Stories-06.png` — inventoried only
- `Screens/Mobile App/Stories/Stories-07.png` — inventoried only
- `Screens/Mobile App/Stories/Story Detail-01.png` — visually inspected
- `Screens/Mobile App/Stories/Story Detail-02.png` — inventoried only

### Complete normative functional coverage

### 1.7 Functional Requirements

**FR-1** Stories Library must organize content into the categories: Bedtime Stories, Prophet Stories, Islamic Shorts, Animated Series, Values & Manners, Ramadan & Eid, Downloads (source §21.11).
**FR-2** Library filters must include: age band, duration, language, format (video/audio/text), topic, downloaded-only, free/premium.
**FR-3** Story Detail must show: cover art, synopsis, episode list (for series), age/source/scholar-approval tags, related stories, and current per-episode progress.
**FR-4** Sequential Episode Unlock applies to every episodic series: Episode 1 unlocked by default; Episode N+1 unlocks only after Episode N reaches a per-series-configured completion threshold (playback %, final interaction, or quiz completion).
**FR-5** Locked episodes must display the specific unlock prerequisite text (e.g., "Complete Episode 2 to unlock") — never a generic lock icon with no explanation, and never presented as a paywall unless the series is genuinely tier-gated (in which case it shows a parent-gated paywall card, not a hidden item).
**FR-6** Rewatching a completed episode is always available; there is no re-locking after completion.
**FR-7** Story Player supports video, audio, and text formats with: play/pause, caption toggle, audio-track selection, quality selection, in-story interactive choice overlays, pause-and-quiz moments, and a moral-summary card at the end.
**FR-8** Every story interaction is tracked via `POST /v1/playback/{id}` events and finalized via `POST /v1/content/{id}/complete` on reaching the completion threshold.
**FR-9** On completion: award XP/Noor Heroes Points/badge per the content's configured reward rule, then display the AI-generated (or human-fallback) moral summary via the Noor companion, then optionally show the post-story quiz, then offer "Next Learning" AI-suggested continuation from pre-approved branches only.
**FR-10** Moral Summary Generation: must be generated only from the approved story version and its approved sources (never free-form from unlicensed content); vocabulary adapted to the child's age band; run through Islamic-accuracy and child-safety validation; if AI confidence is below threshold, use a human-reviewed fallback moral instead; accepted moral stored as a versioned artifact (`content_moral_versions`) and surfaced to parents in story insights.
**FR-11** Bedtime Mode: dims the player UI, disables stimulating reward animations, uses calmer/slower narration, soft nasheed underscore, and always ends with a dua or calm reflection — never a bright "level up" animation (source §7.5, §"Bedtime Emotional Mode").
**FR-12** Bedtime Mode supports a parent-configured sleep timer that fades audio/dims screen and can auto-pause/auto-exit the player at expiry.
**FR-13** Sharing any story moment must open a parent gate and produce either an approved deep link or a parent-facing card — direct, ungated sharing is never available in child mode (source §7.5).
**FR-14** Story "comments"/reactions are never public; only moderated child-safe reaction stickers or parent-facing feedback exist — no open comment system anywhere in Stories.
**FR-15** Offline download manifests must include only the currently unlocked episodes of a series at manifest-generation time — never pre-bundling locked future episodes.
**FR-16** Media removed/withdrawn mid-playback must stop playback safely, explain unavailability in age-appropriate language, and recommend an approved alternative — never a silent failure or crash (source §7.5 Error Handling).
**FR-17** Admin/Support preview or override access to locked episodes (for troubleshooting) must be fully audited and must never grant the child any reward (XP/badge) as a side effect.
**FR-18** AI "Personalized Story Continuation" must only suggest from a pre-approved branch set per story (e.g., "learn more about sabr," "try the dua," "watch the next Prophet story") — never an open-ended free-text AI suggestion.
**FR-19** Dynamic Narration Tone adapts per playback context: energetic (afternoon/general), calm (bedtime), Ramadan reflection, Eid celebration, low-stimulation focus mode — selected server-side based on time-of-day, active seasonal mode, and parent-configured sensory preferences (accessibility).
**FR-20** Parent Story Insights view must show: stories watched, time spent, quiz scores, and the moral lessons learned — accessible only from the Parent Area, never duplicated into the child's own view in a way that exposes analytics framing to the child.

### Ordered source inventory

### 1.18 Screen Inventory (Complete — Zero Missing)

| # | Screen | Type | Entry Points | Exit Points |
|---|---|---|---|---|
| 1 | Stories Library (Landing) | Primary | Bottom nav "Stories" tab, Home, Search results | Story Detail |
| 2 | Category Filter Panel | Modal/Sheet | Library filter icon | Library (filtered) |
| 3 | Story Detail | Primary | Library, Search, Home "Continue", Favorites | Story Player, Episode list items |
| 4 | Episode List (within Story Detail, series only) | Component | Story Detail | Story Player (per unlocked episode) |
| 5 | Lock Badge / Unlock Condition Tooltip | Component | Episode List, locked items | Dismiss / stays inline |
| 6 | Parent-Gated Paywall Card | Component | Episode List / Story Detail, tier-gated content | Parent PIN gate → Subscription (A.14) |
| 7 | Story Player — Video | Primary | Story Detail, Continue Watching | Completion flow / Back to Detail |
| 8 | Story Player — Audio | Primary | Story Detail, Continue Listening, Bedtime Corner | Completion flow / Back to Detail |
| 9 | Story Player — Text | Primary | Story Detail (text-format stories) | Completion flow / Back to Detail |
| 10 | Interactive Choice Overlay | Component (in-player) | Mid-playback, scripted choice points | Resumes playback with branch |
| 11 | Pause-and-Quiz Moment Overlay | Component (in-player) | Mid-playback, scripted quiz points | Resumes playback |
| 12 | Bedtime Mode Player Variant | Primary (theme variant of 7/8) | Bedtime Corner, bedtime window auto-trigger | Dua/reflection ending |
| 13 | Sleep Timer Control | Component (in-player, Bedtime Mode) | Bedtime Mode player | Auto-pause/exit at expiry |
| 14 | Media Unavailable / Safe-Stop Screen | Screen variant | Mid-playback withdrawal event | Recommended alternative card |
| 15 | Completion / Reward Reveal Screen | Screen variant | End of playback, threshold reached | Moral Summary |
| 16 | Moral Summary Card ("Noor says...") | Screen variant | Post-completion | Post-story Quiz or Next Learning |
| 17 | Post-Story Quiz | Screen (shared with A.8 Daily Quiz engine) | Moral Summary | Next Learning suggestion |
| 18 | AI "Next Learning" Suggestion Card | Component | Post-quiz / post-moral-summary | Next episode / related story / Stories Library |
| 19 | Achievement/Badge Unlock Modal | Modal | Completion flow, if a badge threshold is crossed | Dismiss → returns to flow |
| 20 | Share Story Moment — Parent Gate | Modal | Player "Share" action | Approved share card/deep link, or cancel |
| 21 | Approved Share Card Preview | Screen | Parent gate success | Send/cancel |
| 22 | Favorites List | Screen | Profile/Library "Favorites" entry | Story Detail |
| 23 | Downloads Manager (Stories scope) | Screen | Library "Downloads" category, Settings | Story Player (offline) |
| 24 | Caption/Audio-Track/Quality Settings Sheet | Modal (in-player) | Player settings icon | Resumes playback with new settings |
| 25 | Empty State — No content in category | Screen variant | Library, sparse category | Alternate category |
| 26 | Empty State — No downloads yet | Screen variant | Downloads Manager | Library |
| 27 | Parent Story Insights (per-child) | Screen (Parent Area) | Parent Dashboard → Child Progress → Stories | Story Detail (parent preview) |
| 28 | Parent Story Insights — Individual Story Detail (moral + quiz score) | Screen (Parent Area) | Parent Story Insights list | Back |
| 29 | Admin/Support Preview Mode Banner (overlay on Story Player) | Screen variant (internal use) | Admin override tool | Exit preview (no reward granted) |

### Exact mobile UX and behavior sources

### 1.9 Acceptance Criteria

- Given a series with Episode 1 complete below threshold, when the child opens Story Detail, then Episode 2 shows a lock badge with the specific unlock condition text, not a generic lock.
- Given a child completes Episode 1 past its threshold, when they return to Story Detail, then Episode 2 is unlocked immediately (real-time, not requiring app restart).
- Given a story ends, when the moral-summary AI confidence is below the configured threshold, then the human-reviewed fallback moral is shown instead, and the low-confidence event is logged for editorial review.
- Given the current time falls within the parent-configured bedtime window, when the child opens any story marked eligible for Bedtime Mode (or explicitly opens via Bedtime Corner), then the player renders in dimmed/calm mode and ends with a dua, never a bright reward animation.
- Given a child attempts to share a story moment, when they tap Share, then a parent gate (PIN/biometric) appears before any link/card is generated — no direct ungated share path exists.
- Given media is withdrawn by Admin while a child is mid-playback, when the next playback heartbeat fails to resolve the media, then the player stops safely with an age-appropriate explanation and a recommended alternative — never a crash or blank freeze.
- Given a parent generates an offline download manifest for a series with 5 episodes where only 2 are currently unlocked, when the manifest is built, then it contains exactly those 2 episodes' media, not all 5.
- Given Support uses the admin override to preview a locked episode for a troubleshooting ticket, when the preview session ends, then no XP/badge/reward was granted to the actual child account, and the override action is recorded in the audit log.

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

### 1.16 User Flow (Narrative)

Child taps "Stories" tab or a Home "Continue Watching" card → Stories Library (if from tab) with category rails and filters → taps a story → Story Detail (cover, synopsis, episode list with lock states) → taps Play on an unlocked episode → Story Player (full-screen, format-appropriate controls) → encounters interactive choice moment(s) → reaches completion threshold → completion event fires → XP/reward awarded → moral summary shown via Noor companion → optional post-story quiz → "Next Learning" AI-suggested continuation offered → child either continues to next episode/story or returns to Stories Library/Home.

Bedtime variant: child enters via Home's Bedtime Corner widget (or Stories Library's "Bedtime Stories" category within the bedtime window) → Story Player renders in dimmed Bedtime Mode automatically → calmer narration tone → sleep timer control visible → ends with dua/reflection card instead of a bright reward animation, though XP/reward is still quietly recorded.

### 2.1 Stories-Specific Design System Extensions

- **Player Chrome:** Full-screen immersive player uses soft Islamic geometric border framing (subtle, not distracting) around the content viewport in the standard theme; this border is removed/simplified in Bedtime Mode to reduce visual stimulation.
- **Bedtime Theme Override:** Independent of system light/dark theme — Bedtime Mode always applies a dimmed navy/teal palette with reduced animation, regardless of the device's current theme setting, since it is a content-context state, not a display preference.
- **Choice Overlay Design:** Two-to-three large, clearly differentiated rounded option cards (never more than 3 simultaneous choices, to avoid decision paralysis for young children), each with an icon + short label, no countdown-timer pressure on choice moments (children may take their time).
- **Reward Reveal Animation:** Celebratory but brief (≤2s), never blocking required next action, never using randomized/variable visual surprise mechanics (consistent, predictable reward presentation per the anti-dark-pattern Ethical Rule).
- **Moral Summary Card:** Distinct visual treatment — warm parchment-like card background, Noor companion illustration speaking, large legible text, calm tone, no surrounding clutter.

### 2.2 Screen-Level Design Requirements (Key Screens)

#### Screen: Story Player (Video)

- **Purpose:** Deliver immersive, safe, controllable video playback with embedded interactive/educational moments.
- **Components:** Full-screen video surface, top-overlay minimal controls (back, caption toggle, settings gear) auto-hiding after inactivity, bottom scrubber/progress bar (scrubbing disabled past the furthest-unlocked point in a not-yet-completed episode, to prevent skip-to-end gaming of the completion threshold — configurable per series policy), play/pause center control, choice/quiz overlays appearing at scripted timestamps.
- **States:** Loading/buffering, Playing, Paused, Choice-Overlay-Active, Quiz-Moment-Active, Media-Unavailable (safe-stop), Completed (transitions to Completion screen), Offline-Playing (downloaded).
- **Accessibility:** All controls reachable via TalkBack/switch-access; captions always toggleable and on by default for children flagged with accessibility hearing preferences in their profile; no control relies solely on a swipe gesture without a tappable alternative.
- **Responsive Rules:** Full-bleed on phone; on tablet, video maintains aspect ratio with letterboxing rather than stretching/cropping.
- **Empty/Error/Loading/Success/Offline:** Covered in §1.11–1.14.

#### Screen: Story Detail

- **Purpose:** Inform the child's choice to start/continue a story/series before committing to playback.
- **Components:** Hero cover art, title, short synopsis (age-appropriate length), scholar-approval/source badge, duration/format tags, episode list (series) with per-episode progress ring and lock state, "Add to Favorites" toggle, Download button, Related Stories rail.
- **States:** Default, Loading (skeleton), Error (catalog fetch failure — retry), Locked-series-paywall variant.
- **Accessibility:** Episode list items individually labeled with lock state read aloud ("Episode 3, locked, complete Episode 2 to unlock").
- **Responsive Rules:** Single column mobile; two-column (cover + info side-by-side) on tablet landscape.

#### Screen: Bedtime Mode Player Variant

- **Purpose:** Provide a calming, low-stimulation playback experience appropriate for wind-down/bedtime.
- **Components:** Dimmed full-screen surface, soft star-particle ambient overlay (subtle, non-distracting), sleep-timer control (15/30/45/60 min or "until story ends"), simplified minimal controls, dua/reflection ending card instead of celebratory reward screen.
- **States:** Same lifecycle as standard player, plus a distinct "Sleep Timer Expiring" gentle fade-warning state before auto-pause.
- **Accessibility:** Reduced-motion respected even more strictly here; no flashing elements under any circumstance.

### 2.3 Tab Structure

Stories is Tab 3 of 5 (Home / Learn / **Stories** / Rewards / Profile). Click mapping:

| Click Target | Destination | API Called | Analytics Event | Permission Check | Error Handling |
|---|---|---|---|---|---|
| Story card (Library) | Story Detail | `GET /v1/content/{id}` | `story_detail_viewed` | Entitlement check (free/premium) | Graceful "unavailable" state |
| Episode (unlocked) | Story Player | `GET /v1/content/{id}/manifest` (signed media URL) | `story_player_opened` | Unlock-state + entitlement check | Lock badge if not actually unlocked (race condition guard) |
| Episode (locked) | Lock tooltip (no navigation) | None | `episode_lock_viewed` | N/A | N/A |
| Download icon | Downloads Manager / inline download start | `POST /v1/downloads/manifest` | `story_download_started` | Parent download-policy check | Retry on failure |
| Share icon (in-player) | Parent Gate Modal | None until gate passes | `story_share_gate_opened` | Parent PIN/biometric | Cancel returns to player |
| Favorite icon | Inline toggle | `POST /v1/favorites` | `story_favorited` | None | Optimistic update + retry |

### 2.4 Wireframe Description (Composite)

Library: vertically-scrolling page of horizontally-scrollable category rails (consistent with Home's rail pattern), a sticky filter bar beneath the page header. Story Detail: single-column hero-first layout (cover → metadata → episode list → related). Story Player: true full-screen edge-to-edge with auto-hiding minimal chrome — the single screen in the entire app with no persistent bottom navigation visible, by design, to maximize immersion (back gesture/button always available to exit safely).

### 2.5 Screen Image Generation Prompts

**Screen: Stories Library**
- *Prompt 1 (English):* "Mobile app stories library/browse screen UI mockup for a children's Islamic learning app. Warm off-white background. Top shows a row of pill-shaped category filter chips labeled with simple icons (moon for Bedtime, lantern for Prophet Stories, scroll for Values). Below, multiple horizontally-scrollable rows of rounded rectangular story cover thumbnails with soft shadows, each showing a colorful animated-style illustration (Prophet-era desert scenes, gentle lantern characters, no realistic human faces, modest and respectful depictions), small duration/age badges in the corner of each card. Warm teal and gold accent colors, rounded corners throughout, joyful and inviting children's app aesthetic, bottom navigation bar visible with 5 icons."
- *Prompt 2 (Arabic RTL):* "نفس شاشة مكتبة القصص لتطبيق تعليم إسلامي للأطفال، بتخطيط كامل من اليمين إلى اليسار. خلفية بيج فاتح دافئ. يعرض الأعلى صفًا من رقاقات تصفية الفئات بيضاوية الشكل بأيقونات بسيطة (هلال لقصص النوم، فانوس لقصص الأنبياء، لفافة للقيم). أسفل ذلك عدة صفوف قابلة للتمرير أفقيًا من صور مصغرة مستديرة الزوايا لأغلفة القصص بظلال خفيفة، كل منها يعرض رسمة متحركة الطابع وملونة (مشاهد صحراوية من العصر النبوي، شخصيات فانوس لطيفة، بدون وجوه بشرية واقعية، تصوير محتشم ومحترم)، وشارات صغيرة للمدة والعمر في زاوية كل بطاقة. ألوان فيروزية وذهبية دافئة، زوايا دائرية في كل مكان، طابع تطبيق أطفال مرح ومرحب، شريط تنقل سفلي ظاهر بخمس أيقونات."

**Screen: Story Player — Bedtime Mode**
- *Prompt 1 (English):* "Mobile app full-screen video player UI mockup in a calm bedtime mode for a children's app. Deep dimmed navy-teal night-sky background with soft twinkling star particles, a small gentle glowing lantern-shaped companion character illustration in the corner, minimal translucent playback controls (play/pause, small sleep-timer icon showing '30 min') at the bottom that fade after a few seconds, soft rounded caption text bar near the bottom in a warm cream color, no bright UI elements anywhere, extremely calm and soothing visual tone, no realistic human faces."
- *Prompt 2 (Arabic RTL):* "نفس واجهة مشغل الفيديو بملء الشاشة في وضع وقت النوم الهادئ لتطبيق أطفال، بتخطيط من اليمين إلى اليسار للعناصر النصية. خلفية كحلية فيروزية داكنة خافتة تشبه سماء الليل مع جزيئات نجوم متلألئة لطيفة، شخصية فانوس متوهج صغيرة ولطيفة في الزاوية، عناصر تحكم تشغيل شفافة وبسيطة (تشغيل/إيقاف مؤقت، أيقونة صغيرة لمؤقت النوم تعرض '30 دقيقة') في الأسفل تتلاشى بعد ثوانٍ قليلة، شريط نص ترجمة مستدير الزوايا بلون كريمي دافئ قريب من الأسفل، بدون أي عناصر واجهة زاهية، طابع بصري هادئ ومريح للغاية، بدون وجوه بشرية واقعية."

**Screen: Moral Summary Card**
- *Prompt 1 (English):* "Mobile app modal card UI mockup, warm parchment-textured rounded card centered on a softly blurred background. A small friendly lantern-shaped companion character illustration appears to be 'speaking' via a rounded speech-bubble shape, with calm centered text below reading a short moral lesson. A small gold star/badge icon in the top corner indicating XP earned, a single warm gold 'Continue' button at the bottom. Soft shadows, gentle warm lighting, no clutter, respectful and calm illustration style, no realistic human faces."
- *Prompt 2 (Arabic RTL):* "نفس بطاقة نافذة منبثقة لملخص العبرة الأخلاقية، بتخطيط من اليمين إلى اليسار. بطاقة مستديرة الزوايا بملمس شبيه بالرق الدافئ في وسط خلفية ضبابية ناعمة. شخصية فانوس صغيرة وودودة تظهر وهي 'تتحدث' عبر شكل فقاعة كلام مستديرة، مع نص هادئ في المنتصف أسفلها يعرض عبرة أخلاقية قصيرة. أيقونة نجمة أو وسام ذهبي صغير في الزاوية العلوية يشير إلى نقاط الخبرة المكتسبة، وزر ذهبي دافئ واحد بعنوان 'استمرار' في الأسفل. ظلال خفيفة، إضاءة دافئة ولطيفة، بدون ازدحام، أسلوب رسم محترم وهادئ، بدون وجوه بشرية واقعية."

*(Remaining screens — Story Detail, Episode Lock Tooltip, Interactive Choice Overlay, Completion/Reward Reveal, Downloads Manager, Parent Story Insights, Share Gate Modal, Favorites List — follow the same two-prompt EN/AR template using these tokens; full set available on request.)*

---

### 6.1 Technical Requirements
Kotlin, Jetpack Compose, MVVM, Clean Architecture, module `:feature:stories`, depends on `:core:media-player` (Media3/ExoPlayer-based), `:core:design-system`, `:core:offline-cache`, `:core:network`.

### 6.2 Screen Mapping
Each screen in §1.18 maps to a Composable; the Story Player itself wraps a Media3 `PlayerView` inside Compose via `AndroidView` interop, with all overlay UI (choice moments, quiz moments, controls) as Compose layers above it.

### 6.3 Navigation Flow
Story Player is launched as a distinct full-screen destination (not a dialog) with system UI (status/nav bars) hidden for immersion, restored on exit. Deep link `noorheroes://stories/{episode_id}` supported for Home "Continue Watching" and notification entry points.

### 6.4 State Management
`StoryPlayerViewModel` holds `PlayerState` (Loading/Buffering/Playing/Paused/ChoiceActive/QuizActive/Unavailable/Completed) and drives both the Media3 player instance and the Compose overlay visibility from a single source of truth, preventing desync between actual playback state and UI state.

### 6.5 API Mapping
`PlaybackRepository.sendHeartbeat()` → `POST /v1/playback/{id}` (throttled to once every 5–10s, not per-frame); `completeEpisode()` → `POST /v1/content/{id}/complete` with a UUID `client_event_id` generated once per playback session and reused on retry.

### 6.6 Analytics Mapping
`StoriesAnalytics` fires playback lifecycle events tied to actual Media3 player listener callbacks (not assumed/optimistic timing) to ensure heartbeat/completion analytics reflect real playback state.

### 6.7 Offline Support
Downloaded episodes stored via Media3's `DownloadManager` with custom `Cache` implementation scoped per `child_id` (sandboxed so Child B cannot access Child A's downloaded media per the multi-child isolation rule, enforced at the file-access layer, not just UI hiding). Offline choice/quiz logic runs entirely client-side using the bundled `interactive_script` from the manifest, with sync-on-reconnect for analytics only.

### 6.8 Deep Linking
`noorheroes://stories/{episode_id}`, `noorheroes://stories/series/{series_id}`, `noorheroes://stories/bedtime` (opens directly into Bedtime Corner's current recommended bedtime story).

### 6.9 Push Notifications
Landing target for "new episode unlocked," "bedtime story ready," and "new content" notification types (managed by A.12 Notifications) — this feature implements the deep-link targets only.

### 6.10 Testing Strategy
- Unit: Sequential-unlock client-side mirror logic (for offline choice branching only — never used for actual access-control decisions, which remain server-authoritative).
- Player tests: simulate Media3 playback events to verify heartbeat throttling, completion-threshold detection, and safe-stop behavior on a simulated media-unavailable error.
- UI tests: Choice Overlay rendering with max-3-options constraint, Bedtime Mode visual-state toggling correctly based on a mocked time-window.
- Integration: full download → offline playback → reconnect-sync flow.

---

### 13.1 Test Plan Summary
Coverage spans: sequential unlock correctness (including config-change-after-unlock edge case), idempotent completion/reward issuance, offline download/playback/sync, Bedtime Mode behavior, moral-summary fallback gating, withdrawn-content handling, and all 12 edge cases from §1.10.

### 13.2 Test Cases — Happy Path
1. Child watches Episode 1 to completion → reward awarded once, Episode 2 unlocks, moral summary shown, quiz offered.
2. Child enters Bedtime Corner within bedtime window → player launches directly in Bedtime Mode with sleep timer visible, ends with dua card.
3. Child downloads a 3-episode series where only Episode 1 is unlocked → manifest contains exactly 1 episode; after completing Episode 1 online, re-requesting the manifest includes Episode 2.

### 13.3 Edge Cases
All 12 items from §1.10.

### 13.4 Negative Cases
- Fire the same `/complete` request 10 times concurrently → exactly one `story_completion` row and one reward grant exist afterward.
- Request a manifest for a locked episode directly (bypassing UI) → `403 EPISODE_LOCKED`.
- Kill the AI Moral Summary Service mid-request → completion flow still returns within the 600ms timeout budget with the human-fallback moral.
- Use the Admin Preview tool to "complete" a locked episode → confirm zero reward/unlock-state change on the real child record.
- Attempt to scrub a video past the furthest reached position on a `scrub_restricted: true` series → server rejects the resulting heartbeat as anomalous (flagged, not silently accepted as a valid completion signal).

### 13.5 Regression Cases
Full Stories suite re-run on every release touching `:feature:stories`, Content & Playback Service, Reward Service, or AI Moral Summary Service.

### 13.6 Automation Cases
End-to-end: full series completion-to-unlock chain across 3 episodes, offline-download-to-sync round trip, Bedtime Mode visual-state automated screenshot diff test, withdrawn-content-mid-playback safe-stop scenario (simulated via a feature flag that withdraws content during an active test session).

---

### Corresponding KMP blueprint requirements

#### `Development_Blueprints/A3_Stories_Module/KMP/01-stories-library-category-discovery.md`

##### 4. Objective
Build the `feature:stories` module's Library screen — category rails, filter panel, empty/loading/error/offline states — backed by a repository that reads B-01's catalog API with a local cache-first read for the Downloads category.

##### 5. Business Requirements
- FR-1: exactly the seven defined categories.
- FR-2: filters — age band, duration, language, format, downloaded-only, free/premium.
- §1.12 Empty States: "More stories for you are on the way" per empty category, never a blank grid.
- §1.13 Loading States: skeleton category rails.
- §1.14 Offline States: Downloads category always available offline; other categories show cached metadata browsable, non-downloaded items show "connect to internet or download" rather than a dead tap.

##### 10. KMP Requirements
- `StoryCatalogRepository.getLibrary(filters)`: cache-first for the Downloads category (reads local downloaded-episode index maintained by K-07's `DownloadRepository`), network-first-with-cache-fallback for all other categories.
- `StoriesLibraryViewModel`: exposes a single sealed `LibraryUiState` (Loading, Content(rails), Empty(category), Error) per rail/category combination — never a single global loading flag masking per-category empty states.
- Filter panel state (age band, duration, language, format, downloaded-only, free/premium) held in the ViewModel, re-triggers `GetStoriesLibraryUseCase` on change with debounced re-fetch (avoid a network call per keystroke/toggle-flicker).
- Offline non-Downloads items: rendered with a distinct visual affordance ("connect to internet or download") rather than a dead/no-op tap target — tapping surfaces an explanatory toast/snackbar, not silent failure.

##### 12. Offline First
```
Remote Catalog API (B-01)
    ↓
StoryCatalogRepository (cache-first for Downloads, network-first-with-fallback otherwise)
    ↓
StoryCatalogCache (core-datastore-backed local metadata cache)
    ↓
StoriesLibraryViewModel / UI
```
Downloads category sourced entirely from K-07's local download index — zero network dependency. Other categories browsable from last-cached metadata when offline, with a clear non-interactive affordance on items that aren't actually downloaded.

##### 14. Localization
English, Hindi, Arabic, Urdu — category names, filter labels, empty-state copy all sourced from the shared localization resource system, never hardcoded strings.

##### 15. RTL
Category rail scroll direction mirrors in Arabic/Urdu; filter chip row order mirrors; category icons (moon, lantern, scroll) do not require mirroring themselves but their surrounding layout does.

##### 18. Security
No sensitive data on this screen; entitlement/premium badges are informational only (enforcement happens server-side at B-07, never trusted client-side here).

##### 19. Testing
- Unit: filter-change debounce behavior, cache-first-for-Downloads routing logic, offline-affordance state derivation.
- UI: empty-state-per-category rendering, skeleton-to-content transition, RTL rail-direction snapshot tests.
- Accessibility: TalkBack traversal across filter chips and rail items with correct content descriptions (including lock/premium state where applicable).

##### 21. Final Verification Checklist
- [ ] All seven categories render correctly with correct filter support
- [ ] Downloads category fully functional offline with zero network dependency
- [ ] Non-Downloads categories browsable from cache when offline, with a clear non-dead-tap affordance on non-downloaded items
- [ ] Empty-category state matches PRD copy, never a blank grid
- [ ] Skeleton loading renders immediately, no blocking network wait
- [ ] Filter changes debounced, not fired per keystroke/toggle-flicker
- [ ] `stories_library_viewed`/`stories_category_filtered` events fire correctly
- [ ] Full RTL mirroring verified for rails and filter bar
- [ ] No client-side entitlement/premium enforcement (informational badges only)

#### `Development_Blueprints/A3_Stories_Module/KMP/02-story-detail-episode-unlock-presentation.md`

##### 4. Objective
Build the Story Detail screen and its ViewModel, reading B-01's detail endpoint (which already embeds server-computed `unlock_state`/`unlock_condition` per episode), with a real-time-on-resume refresh and full withdrawn-content/paywall handling.

##### 5. Business Requirements
- FR-3: cover, synopsis, episode list, age/source/scholar-approval tags, related stories, per-episode progress.
- FR-5: locked episodes show the specific unlock-condition text server-supplied, never a generic lock icon.
- Acceptance Criteria: Episode 2 unlocks immediately (real-time, not requiring app restart) once Episode 1 crosses threshold.
- Accessibility: episode list items individually labeled with lock state read aloud ("Episode 3, locked, complete Episode 2 to unlock").

##### 10. KMP Requirements
- `StoryDetailViewModel`: fetches detail on entry and again `onResume` (lightweight re-fetch, not a full screen reload) so unlock-state changes from a just-completed episode are reflected without navigating away and back.
- Episode list items render `unlock_state`/`unlock_condition` exactly as supplied by B-01 — no client-side re-derivation of unlock logic (the client never computes unlock state itself, only displays what the server says).
- Tier-gated (paywall) vs. simply-locked distinguished by response metadata — paywall renders `ParentGatedPaywallCard` routing to Parent PIN Gate → Subscription (A.14), plain-locked renders the lock badge + condition text with no navigation on tap.
- Withdrawn content: `410` response renders a "no longer available" state rather than a generic error.

##### 12. Offline First
Cache-first read from K-01's `StoryCatalogCache` when offline (last-known detail + unlock state); a banner indicates data may be stale if offline, since unlock state is server-authoritative and could have changed.

##### 14. Localization
English, Hindi, Arabic, Urdu — synopsis/unlock-condition text is server-supplied and already locale-resolved by B-01; UI chrome labels (buttons, tab names) sourced from shared localization resources.

##### 15. RTL
Episode list, progress rings, and lock badges mirror correctly; hero-image/metadata two-column tablet layout mirrors column order in RTL.

##### 18. Security
No client-side unlock computation exists anywhere on this screen — purely a display of server-supplied state, eliminating an entire class of client-side unlock-bypass risk.

##### 19. Testing
- Unit: paywall-vs-locked branching logic, withdrawn-content `410` handling, resume-refresh triggering exactly once per resume (not on every recomposition).
- UI: lock badge + condition text rendering, paywall card navigation to Parent Gate, related-stories rail rendering.
- Accessibility: TalkBack reads "Episode 3, locked, complete Episode 2 to unlock" verbatim from server-supplied `unlock_condition` text.

##### 21. Final Verification Checklist
- [ ] Locked episodes always show the specific server-supplied unlock-condition text, never a bare lock icon
- [ ] Episode 2 reflects unlock immediately on resume after completing Episode 1, no app restart needed
- [ ] Tier-gated content renders the paywall card, not a plain lock, and routes through Parent Gate
- [ ] Withdrawn content renders a "no longer available" state, not a generic error
- [ ] No client-side unlock-state computation exists anywhere in this screen
- [ ] TalkBack reads lock state + condition text correctly per accessibility requirement
- [ ] Full RTL mirroring verified
- [ ] All four analytics events fire correctly

#### `Development_Blueprints/A3_Stories_Module/KMP/03-story-player-core-playback-engine.md`

##### 4. Objective
Build `StoryPlayerViewModel` and the player Composable wrapping `library:kmpplayer`, implementing throttled heartbeats, safe-stop on media-unavailable, session-scoped idempotent completion calls, and cold-start performance targets — as the shared engine that K-04, K-05, and K-06 layer on top of.

##### 5. Business Requirements
- FR-7: video/audio/text formats with play/pause, caption toggle, audio-track selection, quality selection.
- §6.4 State Management: single sealed `PlayerState` is the sole source of truth for both Media3 calls and Compose overlay visibility.
- §6.5 API Mapping: heartbeats throttled 5–10s of actual playback time; `client_event_id` generated once per session, reused on retry.
- FR-16 / Error Handling: media withdrawn mid-playback → safe stop, age-appropriate explanation, recommended alternative — never a raw error/crash.
- NFR: cold start (cached manifest) p95 < 1.5s; video start-to-first-frame p95 < 2s on 3G-equivalent throttling.

##### 10. KMP Requirements
- `PlayerState` sealed class: `Loading, Buffering, Playing, Paused, ChoiceActive(choicePointId), QuizActive, Unavailable(reason), Completed(reward)` — the SOLE source of truth driving both `KMPPlayerController` calls and Compose overlay visibility; no code path may show "Playing" UI while the underlying controller reports buffering.
- Manifest fetch (B-07) on entry; `MediaSourceValidator.isValid()` checked before `controller.prepare()`.
- Heartbeat throttling: driven by `library:kmpplayer`'s player-state callbacks (playing/paused/position), NOT a naive wall-clock timer that keeps firing while paused — sent every 5–10s of actual playback time via `PlaybackHeartbeatRepository` (B-03).
- `client_event_id` generated once at session start (`StoryPlayerViewModel.init`), reused identically on any retry of the eventual completion call (K-06 consumes this same ID) — never regenerated mid-session.
- Scrub-ahead UX clamp: when the manifest indicates `scrub_restricted: true`, the scrubber clamps forward-seek to furthest-reached-position + small tolerance; this is explicitly a UX nicety only — real enforcement is B-07's server-side re-validation, not this clamp.
- Safe-stop: on a fatal `KMPPlayerError` from the controller, transition immediately to `PlayerState.Unavailable(reason)` — render a child-friendly message + "Recommended for you instead" card sourced from the manifest's fallback field; never surface raw `KMPPlayerError` codes or technical text to the child.
- Resume position: read via `PlaybackSessionManager.getResumePosition()` and passed as `KMPPlayerConfig(startPositionMs=...)` on `prepare()`.
- Text-format stories use a dedicated `StoryTextPlayer` Composable (not part of `library:kmpplayer`, which is video/audio-focused) but still reports into the same `PlayerState` machine for consistency with the completion/choice/quiz flow.

##### 12. Offline First
```
Downloaded Media (K-07's DownloadRepository cache)
    ↓
StoryPlayerViewModel (prefers local KMPPlayerSource.Local if downloaded, else Network from manifest)
    ↓
KMPPlayerController
    ↓
UI
```
Heartbeats queue locally when offline and sync on reconnect (delegated to K-07's sync mechanism, this sub-feature only needs to fail heartbeat sends gracefully without blocking playback).

##### 14. Localization
Captions/audio-track selection defaults resolve per active locale; on mid-session OS locale change, re-evaluate available tracks on resume (fallback to original audio + captions if no dub exists for the new locale, never silent/blank audio).

##### 15. RTL
Caption text rendering right-to-left for Arabic/Urdu; player control layout (back, caption toggle, settings gear) mirrors position.

##### 18. Security
- Manifest signed URLs (from B-07) are short-TTL and never persisted to disk in plaintext beyond `library:kmpplayer`'s own secure cache handling; this ViewModel does not log the raw playback URL.
- `client_event_id` generated client-side using a secure UUID generator — no predictable/sequential IDs.

##### 19. Testing
- Unit: heartbeat throttling driven by actual player-state callbacks (not wall-clock), `client_event_id` stability across retries, scrub-clamp logic for `scrub_restricted` series.
- Player simulation tests: safe-stop transition on a simulated `KMPPlayerError`, verifying no raw error text reaches any rendered string.
- Integration: cold-start timing measurement against the p95 budget on a low-end device profile (per PRD NFR).

##### 21. Final Verification Checklist
- [ ] `PlayerState` is the sole source of truth — no code path shows overlay UI diverging from actual controller state
- [ ] Heartbeats throttled to actual playback time (5–10s), never fire while paused
- [ ] `client_event_id` generated once per session, identical across retries
- [ ] Safe-stop on media-unavailable shows child-friendly message + alternative, zero raw technical text (blocklist-tested)
- [ ] Scrub-ahead clamp applied for `scrub_restricted` series, documented as non-authoritative
- [ ] Cold start p95 < 1.5s with cached manifest
- [ ] No direct Media3/AVPlayer API calls anywhere in this module (uses `library:kmpplayer` exclusively)
- [ ] Resume position correctly read/persisted via `PlaybackSessionManager`
- [ ] Text-format stories report into the same `PlayerState` machine as video/audio

#### `Development_Blueprints/A3_Stories_Module/KMP/04-interactive-choice-quiz-moment-overlays.md`

##### 4. Objective
Build the Choice Overlay and Quiz Moment Overlay Composables driven by `PlayerState.ChoiceActive`/`QuizActive` (from K-03), with deterministic client-side branch mirroring, input debouncing, and offline-safe event queuing to B-05.

##### 5. Business Requirements
- FR-7: in-story interactive choice overlays, pause-and-quiz moments.
- §2.1 Design: two-to-three large, clearly differentiated option cards, never more than 3, no countdown-timer pressure.
- Edge Case 3: rapid repeated taps debounced/queued so no choice is silently dropped or double-counted.
- §7 Android AI Code-Generation Prompt requirement #4: Choice Overlay hard-enforces max 3 options via a `require()` assertion in debug builds, failing loudly rather than silently rendering a 4th option.

##### 10. KMP Requirements
- `ChoiceOverlay` accepts a maximum of 3 options; a `require(options.size <= 3)` assertion fails loudly in debug builds if manifest data ever violates this (defense in depth alongside B-11's server-side cap) — release builds degrade gracefully (render only the first 3, log an error) rather than crashing in production.
- Tap-input debouncing: a `Flow`-based debounce (or equivalent) on the choice-selection callback so rapid double-taps register exactly one selection, never zero and never two.
- `BranchResolver.resolve(choicePointId, selectedOptionId)`: deterministic, purely client-side, using the same `interactive_script` branch data bundled in the manifest — playback continues immediately on selection without waiting for `ChoiceEventRepository`'s network call.
- `ChoiceEventRepository.recordChoice()`: fire-and-forget from the player's perspective; queues locally (via `core-datastore`-backed outbox, mirroring K-07's sync pattern) if offline/failed, synced later — never retried inline in a way that could stall playback.
- No countdown timer on choice moments — children may take their time; the overlay remains visible until a selection is made.

##### 12. Offline First
```
Bundled interactive_script (from manifest, downloaded or streamed)
    ↓
BranchResolver (deterministic, client-side, zero network dependency for branching itself)
    ↓
ChoiceEventRepository (queues sync-only event, never gates playback)
```

##### 14. Localization
Choice option labels and quiz question/answer text are server-supplied, already locale-resolved; overlay chrome (e.g., any "Choose one" prompt copy) sourced from shared localization resources.

##### 15. RTL
Option card layout order mirrors in Arabic/Urdu; icon + label horizontal arrangement mirrors.

##### 18. Security
Choice/quiz data carries no sensitive information; no new security surface beyond standard input validation (reject malformed manifest `interactive_script` data gracefully per §10).

##### 19. Testing
- Unit: `BranchResolver` determinism (same input always same branch), debounce behavior (rapid double-tap → exactly one selection), 3-option-cap `require()` assertion in debug builds.
- UI: Choice Overlay never renders a 4th option even with malformed fixture data (release-build graceful-degradation path), no countdown-timer element present, quiz overlay delegates to the shared A.8 component correctly.
- Integration: offline choice event queues and syncs correctly on reconnect (shared test harness with K-07 if practical).

##### 21. Final Verification Checklist
- [ ] Choice Overlay never renders more than 3 options, in debug (assertion) or release (graceful truncation) builds
- [ ] Rapid double-tap registers exactly one selection, never zero or two
- [ ] Branch resolution is fully deterministic and client-side — playback never waits on the network for branching
- [ ] No countdown-timer element exists on the Choice Overlay
- [ ] Offline choice events queue locally and sync on reconnect without loss or duplication
- [ ] Quiz Moment Overlay reuses the shared A.8 quiz component, no duplicated quiz UI logic
- [ ] `story_choice_made`/`story_quiz_moment_answered` events fire correctly
- [ ] Full RTL mirroring verified

#### `Development_Blueprints/A3_Stories_Module/KMP/05-bedtime-mode-player-experience.md`

##### 4. Objective
Implement `isBedtimeMode` as a boolean resolved once at player-launch time and passed into K-03's player Composable, driving a dimmed theme override, sleep timer control, and a dua-ending path — independent of the device's light/dark theme setting.

##### 5. Business Requirements
- FR-11: dims UI, disables stimulating reward animations, calmer/slower narration, soft nasheed underscore, always ends with dua/reflection.
- FR-12: parent-configured sleep timer fades audio/dims screen, can auto-pause/auto-exit at expiry.
- §2.1 Design: Bedtime Theme Override is independent of system light/dark theme — a content-context state, not a display preference.
- Edge Case 6: bedtime-eligible story started just before the window begins, finishes just after → visual/narration treatment evaluated at story-start time and held consistent for the session (no mid-session flicker); ending dua/reflection treatment respects the window state at completion time if materially different.

##### 10. KMP Requirements
- `BedtimeModeResolver.resolve(entryPoint, currentTime, parentBedtimeWindow)`: pure function evaluated exactly once when the player screen is composed/launched — the result is passed down as an immutable parameter, never re-evaluated mid-session even if the window boundary is crossed during playback.
- Theme override applies regardless of device light/dark mode — dimmed navy/teal palette, reduced/removed geometric border framing (per §2.1, simplified relative to standard theme), no flashing elements under any circumstance (stricter reduced-motion than standard mode).
- Reward-reveal behavior branches: standard mode shows the brief celebratory reveal (K-06); Bedtime Mode suppresses it and instead shows `DuaReflectionEndingCard` — XP/reward is still recorded quietly server-side (B-04 is unaffected; this is purely a presentation branch).
- Sleep Timer: options 15/30/45/60 min or "until story ends"; a distinct "Sleep Timer Expiring" gentle fade-warning state before auto-pause; auto-pause/auto-exit calls K-03's `PlayerState` transitions (pause via `KMPPlayerController.pause()`), never a raw platform timer bypassing the state machine.
- Ending-treatment exception: per Edge Case 6, the ending card's window-state check happens at completion time (may differ from the entry-time `isBedtimeMode` resolution if materially different) — this is the one deliberate exception to "resolved once at entry," and must be implemented as a separate, explicit check at the completion step, not a re-evaluation of the whole `isBedtimeMode` flag.

##### 12. Offline First
Bedtime-window configuration should be cached locally (via the existing parent-settings local cache, not a new one) so bedtime-mode resolution works fully offline.

##### 14. Localization
Dua/reflection text, sleep-timer labels, and calmer narration cues (if text-rendered) sourced from shared localization resources across EN/HI/AR/UR.

##### 15. RTL
Sleep timer control and dua card layout mirror correctly; star-particle ambient overlay is symmetric and requires no directional mirroring itself.

##### 18. Security
No new security surface; sleep-timer auto-pause/auto-exit must not interfere with B-04's completion idempotency (if a session is paused/exited mid-story, no completion call has fired yet — nothing to reconcile).

##### 19. Testing
- Unit: `BedtimeModeResolver` determinism (mocked time-window boundary cases per Edge Case 6), sleep-timer expiry state transitions.
- UI: dimmed theme applies regardless of device light/dark mode (mocked both), no flashing elements verified via a reduced-motion assertion, dua ending replaces (not supplements) the standard reward reveal.
- Integration: mid-session window-boundary crossing does NOT cause the standard-vs-bedtime visual treatment to flicker (explicit Edge Case 6 regression test).

##### 21. Final Verification Checklist
- [ ] `isBedtimeMode` resolved exactly once at player entry, never flickers on mid-session window-boundary crossing
- [ ] Ending-treatment exception (completion-time re-check) implemented as the one deliberate exception, per Edge Case 6
- [ ] Dimmed theme applies independent of device light/dark mode
- [ ] Zero flashing elements under any circumstance (stricter than standard mode)
- [ ] Sleep timer auto-pause/auto-exit routes through K-03's `PlayerState` machine, never a raw bypass
- [ ] Reward still recorded server-side in Bedtime Mode, just not celebratorily displayed
- [ ] Bedtime Mode is implemented as a theme/behavior overlay on the same Composable, not a separate screen/Activity
- [ ] All three analytics events fire correctly
- [ ] Full RTL mirroring verified

#### `Development_Blueprints/A3_Stories_Module/KMP/06-story-completion-reward-moral-summary-flow.md`

##### 4. Objective
Build the post-playback completion flow screens/state driven by a single idempotent call to B-04, rendering reward reveal, moral summary, optional quiz, and next-learning suggestion in sequence, with graceful quiz-service-unavailable handling.

##### 5. Business Requirements
- FR-9: award reward → moral summary via Noor companion → optional quiz → AI Next Learning from pre-approved branches only.
- §2.1 Design: reward reveal celebratory but brief (≤2s), never blocking required next action, never randomized/variable-surprise mechanics.
- FR-18: AI Next Learning suggests only from a pre-approved branch set — never open-ended free-text AI suggestion.
- Error Handling: quiz-service unavailable → completion/reward still finalizes independently, quiz step skipped with a "quiz coming back soon" note.

##### 10. KMP Requirements
- `CompletionFlowViewModel.completeSession(episodeId, finalPositionSeconds, clientEventId, completionMethod)`: calls B-04 exactly once; on retry (e.g., process death recovery), reuses the identical `clientEventId` — never regenerates it, relying on B-04's server-side idempotency for a safe retry.
- Reward Reveal: ≤2s celebratory animation, consistent/predictable presentation (no randomized visual surprise), never blocks the "Continue" action — the child can tap through immediately if they choose.
- Moral Summary Card renders `source: ai|human_fallback` transparently to the flow logic (visually identical to the child regardless of source — the distinction is purely for internal analytics, never surfaced as a UI difference).
- Post-Story Quiz: optional step, delegates entirely to the shared A.8 quiz component; if the quiz service is unavailable, render a "quiz coming back soon" note and proceed directly to Next Learning — reward/completion state is already finalized by this point regardless.
- Next Learning: renders only the pre-approved branch suggestions returned by B-04's response — the UI has no free-text input or open-ended AI suggestion surface at all (architecturally impossible to violate FR-18 from the client side).
- Badge Unlock Modal shown only if `reward.badge_id` is present in the response; dismissing returns to the main completion flow, never blocks progression.

##### 12. Offline First
If completion occurs offline, the call queues via the same offline-outbox mechanism established in K-07 (reuse, do not duplicate); the UI proceeds optimistically through reward-reveal/moral-summary using locally-computed provisional values where safe (e.g., XP amount if deterministic and known client-side from content config) and reconciles/corrects on sync if the server response differs — per Edge Case 1's "never abruptly re-lock without explanation" spirit applied here to rewards as well.

##### 14. Localization
Moral summary text, next-learning suggestion labels, and "quiz coming back soon" copy sourced from shared localization resources / server-supplied locale-resolved text.

##### 15. RTL
Moral Summary Card (parchment background, speech-bubble shape), reward reveal, and next-learning card all mirror layout correctly.

##### 18. Security
Next Learning suggestions are rendered strictly from B-04's response data — no client-side generation or free-text surface exists, eliminating any possibility of an unapproved AI suggestion reaching the child from this screen.

##### 19. Testing
- Unit: single-call-per-session enforcement (retry reuses `clientEventId`), quiz-unavailable graceful skip, badge-modal-only-when-present logic.
- UI: reward reveal is non-blocking and dismissible immediately, moral summary renders identically regardless of `source` value, Next Learning renders only server-supplied options with zero free-text input anywhere on screen.
- Integration: offline completion queues and reconciles correctly on reconnect.

##### 21. Final Verification Checklist
- [ ] Exactly one B-04 completion call fires per session, using the session-scoped `client_event_id`, even across retries
- [ ] Reward reveal is ≤2s, non-blocking, and never uses randomized/variable presentation
- [ ] Moral Summary Card renders identically regardless of `source: ai|human_fallback`
- [ ] Quiz-service unavailability shows a graceful note and never blocks reward/completion (already finalized independently)
- [ ] Next Learning renders exclusively server-supplied pre-approved options — zero free-text/open-ended input exists in this flow
- [ ] Badge Unlock Modal shown only when `reward.badge_id` is present
- [ ] Offline completion queues and reconciles correctly on reconnect
- [ ] All nine analytics events fire correctly

#### `Development_Blueprints/A3_Stories_Module/KMP/07-offline-downloads-sync-stories.md`

##### 4. Objective
Build the Downloads Manager screen and sync infrastructure on top of `library:kmpplayer::DownloadRepository`, consuming B-08's unlock-aware manifest, scoping cache storage per `child_id`, and providing the offline-outbox mechanism K-04/K-06 depend on.

##### 5. Business Requirements
- §6.7 Offline Support: downloaded episodes via Media3 `DownloadManager` with a custom `Cache` scoped per `child_id`; offline choice/quiz logic runs entirely client-side from the bundled `interactive_script`.
- Edge Case 4: two siblings share a device — Child A's downloads never exposed in Child B's Stories Library.
- Edge Case 7: parent disables downloads entirely while in-progress downloads exist → halted gracefully; already-completed downloads remain playable until offline access is additionally revoked (two distinct controls).
- §1.14 Offline States: Downloads category always available offline, fully functional.

##### 10. KMP Requirements
- `StoryDownloadRepository.startDownload(childId, contentId)`: fetches B-08's manifest, calls `library:kmpplayer::DownloadRepository.startDownload()` per included episode with a cache key prefixed by `child_id` — this prefix is the sandboxing mechanism; verified by an explicit cross-child isolation test (Edge Case 4).
- Bundles `interactive_script` alongside the downloaded media package so K-04's choice/quiz overlays work fully offline.
- Resumable downloads: partial/failed downloads resumable via `library:kmpplayer::DownloadRepository`'s existing progress `StateFlow`, never restarted from zero.
- `DownloadPolicyRepository` exposes two independent flags: `allow_new_downloads` (gates starting new downloads — halting in-progress downloads gracefully, not silently failing, when flipped false mid-download) and `offline_access_revoked` (gates whether already-downloaded content remains playable — a separate, more severe control).
- `OfflineEventOutbox`: generic queue-and-sync mechanism for any Stories event that must work offline-first (heartbeats from B-03, choices from B-05, completion from B-04) — a single shared implementation rather than three bespoke queues, consumed by K-03, K-04, K-06.

##### 12. Offline First
```
B-08 Manifest (unlock-aware, entitlement-checked)
    ↓
StoryDownloadRepository (child_id-scoped cache key)
    ↓
library:kmpplayer::DownloadRepository (Media3 DownloadManager)
    ↓
Local Cache (sandboxed per child_id)
    ↓
K-03 Player (prefers local KMPPlayerSource.Local when available)
```
`OfflineEventOutbox` handles the reverse direction: local event → queue → sync on reconnect, for heartbeats/choices/completions.

##### 14. Localization
Downloads Manager UI chrome (empty state, retry buttons, quality selector) sourced from shared localization resources.

##### 15. RTL
Downloads list layout, progress indicators, and retry controls mirror correctly.

##### 18. Security
- Cross-child cache isolation is a hard security/privacy requirement, not just a UX nicety — explicitly integration-tested (Edge Case 4).
- Downloaded media stored in app-sandboxed storage only, never exposed via shared/public storage paths (per PRD §12.4 Mobile Security).

##### 19. Testing
- Unit: `allow_new_downloads` vs `offline_access_revoked` independence (flipping one never affects the other's behavior), resumable-download-not-restarted-from-zero logic.
- **Mandatory integration test**: Child B's player cannot resolve Child A's downloaded cache entries when both profiles exist on the same device (per PRD Android AI-prompt requirement #5).
- Integration: full offline flow — download a fixture episode → simulate airplane mode → play to completion → verify completion event queues locally with the correct `client_event_id` → simulate reconnect → verify exactly one sync call fires (per PRD Android AI-prompt requirement #10).

##### 21. Final Verification Checklist
- [ ] Mandatory cross-child cache isolation test passes — Child B cannot access Child A's downloads
- [ ] `allow_new_downloads` and `offline_access_revoked` are independently controllable, verified by test
- [ ] Resumable downloads never restart from zero on retry
- [ ] `interactive_script` bundled with downloads — offline choice/quiz overlays fully functional
- [ ] Full offline-to-sync flow (download → airplane mode → complete → reconnect) results in exactly one sync call
- [ ] No direct `DownloadDao` access anywhere — exclusively via `library:kmpplayer::DownloadRepository`
- [ ] Downloaded media stored in app-sandboxed storage only
- [ ] All four analytics events fire correctly

#### `Development_Blueprints/A3_Stories_Module/KMP/08-story-favorites-parent-gated-sharing.md`

##### 4. Objective
Build the Favorites List screen (optimistic toggle + retry) and the Share flow (parent gate → approved share card preview), consuming B-09 and reusing the existing Parent PIN/Biometric Gate component from A.1/C.19.

##### 5. Business Requirements
- FR-13: sharing opens a parent gate and produces an approved deep link or parent-facing card — direct ungated sharing never available in child mode.
- FR-14: no open comment system; only moderated child-safe reaction stickers or parent-facing feedback.
- Edge Case 11: favorite reference resolves to the new canonical content ID after admin restructuring, never a broken reference.

##### 10. KMP Requirements
- `FavoriteRepository.toggleFavorite(episodeId)`: optimistic local state update immediately on tap, reconciled/rolled-back on API failure (retry affordance shown on failure, not a silent revert).
- `FavoritesViewModel`: renders `is_available: false` items (withdrawn content) with a "no longer available" treatment rather than removing them or crashing on a broken reference; resolves restructured content to the canonical ID transparently per B-09's response shape.
- `ShareFlowViewModel`: on Share tap, invokes the existing Parent PIN/Biometric Gate component — no share card/link is generated or even requested from any API until the gate resolves successfully. Cancel at the gate returns cleanly to the player with zero residual share state.
- No open comment/reaction system exists anywhere in this sub-feature — only the parent-gated share path and (if in scope elsewhere) moderated reaction stickers, never a public comment field.

##### 12. Offline First
Favorite toggles queue via the shared `OfflineEventOutbox` (K-07) when offline, applied optimistically to local state immediately.

##### 14. Localization
Favorites List and Share Gate copy sourced from shared localization resources.

##### 15. RTL
Favorites list item layout, share card preview layout mirror correctly.

##### 18. Security
- No share card/deep-link generation occurs before the Parent Gate resolves successfully — this is the feature's core child-safety control for this sub-feature and must have zero bypass path (verified by an explicit UI test asserting no network call to any share-related endpoint fires before gate success).
- No child-facing input surface for open comments exists anywhere in this module.

##### 19. Testing
- Unit: optimistic-toggle-with-rollback-on-failure logic, withdrawn/restructured favorite resolution.
- UI: **mandatory security test** — assert zero share-related API call occurs before the Parent Gate resolves; cancel-at-gate leaves zero residual state.
- Accessibility: Favorites List item labeling, Share Gate focus management (gate modal traps focus appropriately).

##### 21. Final Verification Checklist
- [ ] Favorite toggle is optimistic, instant, with rollback-and-retry on failure
- [ ] Withdrawn favorited content shows "no longer available", never a broken reference or crash
- [ ] Restructured/merged favorited content resolves to the new canonical ID transparently
- [ ] Zero share-related API call fires before the Parent PIN/Biometric Gate resolves successfully (mandatory security test)
- [ ] Cancel at the gate leaves zero residual share state
- [ ] No open comment/public-reaction input surface exists anywhere in this module
- [ ] All four analytics events fire correctly
- [ ] Full RTL mirroring verified

#### `Development_Blueprints/A3_Stories_Module/KMP/09-parent-story-insights-in-app.md`

##### 4. Objective
Build the Parent Story Insights list and per-story detail screens inside the existing Parent Area navigation graph, consuming B-10, with correct empty/offline-staleness states.

##### 5. Business Requirements
- FR-20: shows stories watched, time spent, quiz scores, morals learned; accessible only from the Parent Area, never duplicated into the child's own view.
- §1.12 Empty States: "Once [Child] watches their first story, you'll see their progress here."
- §1.14 Offline States: shows last-synced data with a "may not reflect today's offline activity yet" note if relevant.

##### 10. KMP Requirements
- `ParentStoryInsightsViewModel.load(childId)`: calls B-10, renders empty state on zero-activity, renders a "may not reflect today's offline activity yet" note when the response indicates stale/last-synced data.
- Detail screen navigates from a list item to the full moral + quiz score view for that specific story.
- This screen is reachable exclusively from the Parent Area's existing navigation entry points (Parent Dashboard → Child Progress → Stories) — never linked from anywhere in the child-facing `feature:stories` module.

##### 12. Offline First
Cache-first read from the last-synced insights response (via `core-datastore`), with the staleness note rendered whenever the cached data's timestamp indicates it may not reflect the most recent offline child activity.

##### 14. Localization
All UI copy sourced from shared localization resources across EN/HI/AR/UR.

##### 15. RTL
List and detail layouts mirror correctly.

##### 18. Security
This screen is only reachable through the Parent Area's existing access-control path (behind the Parent PIN/Biometric Gate at the Parent Area entry point) — this sub-feature does not need to re-implement gating, only correctly nest within the existing gated navigation graph.

##### 19. Testing
- Unit: empty-state and staleness-note derivation logic.
- UI: list-to-detail navigation, empty state matches PRD copy exactly.
- Regression: confirm this screen/route is unreachable from anywhere in the child-facing `feature:stories` navigation graph (an explicit navigation-graph test asserting no edge exists from any child-facing route to `ParentStoryInsightsRoute`).

##### 21. Final Verification Checklist
- [ ] Screen lives exclusively within the existing Parent Area navigation graph
- [ ] Confirmed unreachable from any child-facing `feature:stories` route (explicit isolation test)
- [ ] Empty state matches PRD copy exactly ("Once [Child] watches their first story...")
- [ ] Offline/stale data shows the "may not reflect today's offline activity yet" note when applicable
- [ ] List-to-detail navigation works correctly, showing moral + quiz score
- [ ] `parent_story_insights_viewed` analytics event fires correctly
- [ ] Full RTL mirroring verified

## A4 — Feature_A4_Audio_Bedtime_Player_Bedtime_Mode

PRD: `PRD_Documents/Child App (1-12)/Feature_A4_Audio_Bedtime_Player_Bedtime_Mode.md`

Coverage: 14 mandatory FR records; all preserved verbatim below. Feature has 17 inventory records including components/states. Components and states must not inflate independently executed screen count.

### Existing screenshot candidates

- `Screens/Mobile App/Bedtime Audio/Audio Player.png` — visually inspected
- `Screens/Mobile App/Bedtime Audio/Dua Card.png` — inventoried only
- `Screens/Mobile App/Bedtime Audio/Sleep Timer.png` — inventoried only

### Complete normative functional coverage

### 1.7 Functional Requirements

**FR-1** Audio Bedtime Player must display: cover art, story/content title, moral lesson teaser, source/scholar-approval status, episode list (for multi-part audio content), and read/listen counts where privacy-safe (aggregate, never exposing other specific children's identities).
**FR-2** Controls required: Play/Pause, Seek (scrub bar), Playback Speed (e.g., 0.8x/1x/1.2x), Sleep Timer, Download, Next Episode, Previous Episode (source §21.11).
**FR-3** Sleep Timer options must be parent-configurable as a bounded range (e.g., parent sets a max of 30/45/60 minutes); within that bound, the child may freely choose a duration up to the parent-set ceiling, or "until episode ends."
**FR-4** Bedtime Mode is a **system-wide state**, not exclusive to this player: any content surface entered during the parent-configured wind-down window (or explicitly via the Home Bedtime Corner widget) must apply the same dimmed visual treatment, disabled stimulating-reward-animation rule, and dua/calm-reflection ending rule (cross-reference A.3 §2.1 "Bedtime Theme Override").
**FR-5** Bedtime Mode must dim the UI (reduced brightness/contrast theme), disable stimulating reward effects (no confetti/badge-burst/level-up animations), and end every session with a dua or calm reflection — this rule has zero exceptions, including for content that would otherwise show a bright completion animation outside the window (source §7.5).
**FR-6** Sleep Timer expiry must trigger a gentle audio fade-out (not an abrupt cut) over a configurable fade duration (default 15 seconds), followed by auto-pause; the screen may also auto-dim further or return to a calm "goodnight" idle state.
**FR-7** Audio playback must continue uninterrupted if the device screen locks or the app backgrounds (foreground media service), since children commonly fall asleep mid-playback with the screen off.
**FR-8** "Next/Previous Episode" navigation must respect the same Sequential Unlock rules defined in A.3 §1.7 FR-4 for any episodic audio series — Previous is always available (no re-locking), Next is gated by the unlock state.
**FR-9** Read/listen counts displayed must be privacy-safe aggregates (e.g., "12,400 children have listened to this story") — never displaying or implying identification of specific other children.
**FR-10** Ending sequence: on reaching the completion threshold, the player transitions directly to a dua/calm-reflection card (not the standard celebratory Completion/Reward screen used outside Bedtime Mode) — reward (XP/Noor Heroes Points) is still recorded quietly in the background but not visually celebrated in this context.
**FR-11** Download must support the same entitlement/parent-policy checks as A.3 §3.4 `POST /v1/downloads/manifest`; Bedtime category content is prioritized for "auto-suggest download" given its predictable, recurring usage pattern (low-connectivity-evening resilience).
**FR-12** Parent must be able to configure: bedtime window start/end time per child, sleep-timer max ceiling, whether bedtime audio auto-suggests/auto-starts when entering the window, and whether a lightweight "bedtime ritual happened" indicator appears in their Parent Dashboard (non-invasive — completion fact only, not full listening transcript/analytics).
**FR-13** Entering Bedtime Mode must never require re-authentication/PIN if the child is already in an active, validly-locked child session — Bedtime Mode is a content-context state, not a security boundary.
**FR-14** If a child opens the Audio Bedtime Player outside the configured bedtime window (e.g., daytime listening), the player still functions normally but does **not** force Bedtime Mode visuals unless the child explicitly opts in via a "Calm Mode" toggle available at any time of day (giving children agency to use the calming experience whenever they want, while keeping the *automatic* window-based trigger separate).

### Ordered source inventory

### 1.18 Screen Inventory (Complete — Zero Missing)

| # | Screen / Component | Type | Entry Points | Exit Points |
|---|---|---|---|---|
| 1 | Audio Bedtime Player (main screen) | Primary | Home Bedtime Corner, Stories Library "Bedtime Stories" category, Calm Mode toggle, Continue Listening (Home) | Dua ending card, Next Episode, Back to Library |
| 2 | Cover/Info Header (component) | Component | Player top section | N/A |
| 3 | Episode List Sheet (for multi-part audio series) | Modal/Sheet | "Episodes" control in player | Selecting an episode → Player (new content) |
| 4 | Sleep Timer Selector | Modal/Sheet | Sleep Timer icon | Player (timer active) |
| 5 | Playback Speed Selector | Modal/Sheet | Speed icon | Player (speed applied) |
| 6 | Download Control / In-Progress Indicator | Component | Player download icon | Downloads Manager (shared with A.3) |
| 7 | Sleep-Timer-Expiring Gentle Warning (fade-pre-warning state) | Screen variant (in-player) | Final ~10s before fade begins | Fade-out state |
| 8 | Fade-Out / Auto-Pause Visual State | Screen variant (in-player) | Sleep timer expiry | Goodnight Idle State |
| 9 | Goodnight Idle State | Screen variant | Sleep timer auto-pause, or manual pause-and-leave | Resume playback / Exit player |
| 10 | Dua / Calm-Reflection Ending Card | Screen variant | Completion threshold reached during Bedtime Mode | Next Episode offer / Back to Library |
| 11 | Media Unavailable / Safe-Stop (Bedtime-styled variant) | Screen variant | Mid-playback withdrawal | Recommended alternative / dua fallback |
| 12 | Offline — No Bedtime Content Available | Screen variant | Offline + no downloaded bedtime content | Suggested "read a dua together" fallback |
| 13 | Next-Episode-Not-Downloaded (offline) Notice | Component | Tap Next on a not-downloaded-but-unlocked episode while offline | Dismiss, stays on current episode |
| 14 | Calm Mode Toggle (accessible from standard player) | Component | Standard Story Player / Audio Player controls | Re-renders current screen in calm visual treatment |
| 15 | First-Use Sleep Timer Explainer Tooltip | Component (one-time) | First Sleep Timer interaction | Dismiss |
| 16 | Parent "Bedtime Ritual" Status Indicator (Parent Dashboard widget) | Component (Parent Area) | Parent Dashboard | Story Insights (A.3) for full detail, if parent drills in |
| 17 | Parent Bedtime Window/Sleep-Timer-Ceiling Configuration Screen | Screen (Parent Area, cross-ref C.23) | Parent Dashboard → Controls | Saves to Parent Controls |

### Exact mobile UX and behavior sources

### 1.9 Acceptance Criteria

- Given a child sets a 30-minute sleep timer (within the parent's configured ceiling), when 30 minutes elapse during active playback, then audio fades out gently over the configured fade duration and then pauses — the device does not continue playing at full volume past the timer.
- Given a parent has set a sleep-timer ceiling of 30 minutes, when the child attempts to select 60 minutes, then only options up to 30 minutes (or "until episode ends" if explicitly allowed) are selectable.
- Given the child is within the parent-configured bedtime window and opens any story (audio or video), when the player launches, then Bedtime Mode visual/behavioral rules apply automatically without an extra toggle.
- Given an audio episode completes its threshold during Bedtime Mode, when the ending sequence plays, then a dua/calm-reflection card is shown — not the standard bright celebratory completion screen used outside the window.
- Given the app is backgrounded or the screen locks during audio playback, when 10 minutes pass, then audio continues playing uninterrupted (assuming sleep timer hasn't expired).
- Given a child taps "Next Episode" on a locked-next-episode series, when the tap registers, then the same lock-explanation behavior from A.3 applies (specific unlock condition shown, not silently ignored).
- Given a parent views their Dashboard, when they check "Bedtime Ritual" status, then they see a simple completion indicator (e.g., "Bedtime story completed tonight ✓") without exposing a full play-by-play transcript of content/duration unless they explicitly drill into Story Insights (A.3).

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

### 1.16 User Flow (Narrative)

Child enters via Home's Bedtime Corner widget (within window) or directly via Stories Library's "Bedtime Stories" category, or via the explicit "Calm Mode" toggle at any time → Audio Bedtime Player opens (Bedtime Mode visuals auto-applied if within window or Calm-Mode-toggled) → child optionally sets/adjusts Sleep Timer → playback begins, controls available (play/pause/seek/speed/next/prev/download) → child may lock the screen/background the app, audio continues via foreground service → either (a) episode completes naturally → dua/calm-reflection ending → quiet reward recorded → optional Next Episode if unlocked, or (b) sleep timer expires first → gentle fade-out → auto-pause → app shows a calm "goodnight" idle state, no further interaction required from the child.

### 2.1 Bedtime-Specific Design Extensions

- **Calm Palette Application:** Deep dimmed navy/teal gradient background (consistent with A.3's Bedtime Mode), large soft-glow cover art as the dominant visual element (since there's no video to watch — the cover art "breathes" gently, a slow subtle scale pulse synced loosely to playback, never jarring or fast).
- **Large Low-Light Controls:** All primary controls (play/pause, seek, next/prev) sized ≥56dp with high contrast against the dim background; secondary controls (speed, sleep timer, download) grouped in a less prominent row, still ≥44dp.
- **No Bright Reward Color in This Context:** The standard gold "celebration" accent is muted/desaturated specifically within Bedtime Mode screens (a deliberate token override: `gold-bedtime` is a dimmer, warmer amber rather than the vibrant daytime gold) — reinforcing the "calm, not exciting" tone even in incidental UI accents.
- **Dua Ending Card:** Warm, soft, parchment-on-navy contrast card, gentle fade-in (≥800ms, slower than standard UI transitions elsewhere in the app), no XP/badge counters visible on this specific card even though the reward was recorded — that data lives only in Parent Story Insights, never surfaced to the child in this calm moment.

### 2.2 Screen-Level Design Requirements (Key Screens)

#### Screen: Audio Bedtime Player (Main)

- **Purpose:** Provide a calm, simple, reliable nightly listening experience.
- **Components:** Large cover art (breathing animation), title + episode indicator, moral-lesson teaser line, scholar-approval micro-badge, scrub bar with large thumb, play/pause (largest control, center), next/previous (flanking), secondary row: speed selector, sleep timer, download, episode-list entry.
- **States:** Loading/buffering (ambient glow pulse, no spinner), Playing, Paused, Sleep-Timer-Active (small persistent countdown chip), Sleep-Timer-Expiring-Warning (gentle dimming pre-fade), Fading-Out, Goodnight-Idle, Media-Unavailable, Offline.
- **Accessibility:** All controls labeled; scrub bar operable via screen-reader increment/decrement gestures, not drag-only; speed/timer selectors are simple list-style modals, not complex gesture-based pickers (low-light, possibly half-asleep child usage context demands maximum simplicity).
- **Responsive Rules:** Cover art scales to fill available vertical space above the control cluster; tablet layout centers a max-width column rather than stretching cover art edge-to-edge.

#### Screen: Sleep Timer Selector

- **Purpose:** Let the child choose a listening duration within parent-set bounds.
- **Components:** Simple vertical list of duration options (only those ≤ parent ceiling are shown/selectable — options above the ceiling are not displayed at all, not shown-disabled, to avoid confusing/frustrating a child with an option they can never pick), "Until episode ends" option (if parent allows), Cancel/current-timer-off option.
- **States:** Default (no timer set), Timer-active (shows current selection highlighted), Just-changed (brief confirmation feedback).

#### Screen: Dua / Calm-Reflection Ending Card

- **Purpose:** Close every Bedtime Mode session with a genuinely calming, spiritually grounding moment.
- **Components:** Short dua text (Arabic + transliteration + translation, per the same Dua content pattern as A.5/Dua Learning), soft Noor companion illustration in a "sleepy/calm" pose (distinct visual variant from its energetic daytime pose), single low-key "Done" or "Next Episode" (if applicable) action — no bright button styling.

### 2.3 Tab Structure

Audio Bedtime Player is not a standalone tab; it's reached via Home's Bedtime Corner (Tab 1), Stories Library's Bedtime category (Tab 3), or the Calm Mode toggle exposed within other players. Click mapping:

| Click Target | Destination | API Called | Analytics Event | Permission Check | Error Handling |
|---|---|---|---|---|---|
| Home Bedtime Corner card | Audio Bedtime Player | `GET /v1/content/{id}/manifest` | `bedtime_player_opened` | Entitlement + download-availability if offline | Falls back gracefully per §1.11 |
| Sleep Timer icon | Sleep Timer Selector modal | None (local config + `GET /v1/parent-controls/{child_id}/bedtime` cached) | `sleep_timer_opened` | Reads parent-set ceiling | Defaults to a safe conservative ceiling if config fetch fails |
| Download icon | Inline download start | `POST /v1/downloads/manifest` (shared with A.3) | `bedtime_download_started` | Parent download-policy | Retry on failure |
| Next/Previous Episode | Player reloads with new content | `GET /v1/content/{id}/manifest` | `bedtime_next_episode_tapped` / `_previous_episode_tapped` | Unlock-state check (Next only) | Lock explanation if locked |
| Calm Mode toggle (in standard player) | Re-renders current player in calm visual treatment | None (client-side state) | `calm_mode_manually_toggled` | None | N/A |

### 2.4 Wireframe Description (Composite)

Single full-screen, vertically-centered layout: large cover art occupies the upper ~50% of the screen, title/metadata directly below, scrub bar, then the primary control row, then the secondary control row — a simpler, less information-dense layout than the video Story Player given audio's "ambient companion" usage pattern (often not actively watched, just listened to in a dim room).

### 2.5 Screen Image Generation Prompts

**Screen: Audio Bedtime Player (Main)**
- *Prompt 1 (English):* "Mobile app audio player UI mockup in calm bedtime mode for a children's app. Full-screen deep dimmed navy-teal gradient background resembling a night sky with very soft twinkling star particles. Large centered circular or rounded-square album-style cover art glowing gently, depicting a peaceful crescent moon and lantern illustration (no realistic human faces). Below the cover, a title text line and a thin horizontal scrub/progress bar with a soft glowing thumb. Below that, three large circular control buttons in a row: previous, a larger central play/pause button, and next, all in a muted warm amber tone rather than bright gold. A smaller secondary row below with three small icon buttons: playback speed, sleep timer (showing a small moon-and-clock icon), and download. Extremely calm, soothing, low-stimulation visual tone throughout, generous spacing, soft shadows only, no bright or saturated colors anywhere."
- *Prompt 2 (Arabic RTL):* "نفس واجهة مشغل الصوت بوضع وقت النوم الهادئ لتطبيق أطفال، بتخطيط من اليمين إلى اليسار. خلفية كاملة الشاشة متدرجة كحلية فيروزية داكنة وخافتة تشبه سماء الليل مع جزيئات نجوم متلألئة ناعمة للغاية. غلاف مركزي كبير دائري أو مربع الزوايا مستديرة يتوهج بهدوء، يصور رسمة هلال وفانوس مسالمة (بدون وجوه بشرية واقعية). تحت الغلاف سطر نص العنوان وشريط تقدم رفيع أفقي بمؤشر متوهج ناعم. وتحته ثلاثة أزرار تحكم دائرية كبيرة في صف واحد: السابق، زر تشغيل/إيقاف مؤقت أكبر في المنتصف، والتالي، جميعها بلون كهرماني دافئ خافت بدلاً من الذهبي الزاهي. صف ثانوي أصغر تحته بثلاث أيقونات صغيرة: سرعة التشغيل، مؤقت النوم (يعرض أيقونة هلال وساعة صغيرة)، والتحميل. طابع بصري هادئ ومريح للغاية ومنخفض التحفيز البصري في كل مكان، تباعد كبير، ظلال خفيفة فقط، بدون ألوان زاهية أو مشبعة في أي مكان."

**Screen: Dua / Calm-Reflection Ending Card**
- *Prompt 1 (English):* "Mobile app modal card UI mockup for a gentle bedtime story ending, shown over a dimmed night-sky background. A soft parchment-toned rounded card centered on screen, containing centered short calligraphic-style Arabic text at the top, a transliteration line beneath in italic-style Latin font, and an English translation below that, all in warm cream and soft gold tones. A small sleepy-looking lantern-shaped companion character illustration rests at the bottom of the card with closed peaceful eyes. A single small low-key 'Done' text button below, no bright colors, no badges or XP counters visible anywhere on this card, extremely calm and serene mood, no realistic human faces."
- *Prompt 2 (Arabic RTL):* "نفس بطاقة نهاية قصة وقت النوم الهادئة، تظهر فوق خلفية ليلية خافتة، بتخطيط من اليمين إلى اليسار. بطاقة مستديرة الزوايا بلون شبيه بالرق الدافئ في وسط الشاشة، تحتوي في الأعلى على نص عربي بخط زخرفي قصير في المنتصف، وتحته سطر بالنقل الصوتي بخط لاتيني مائل الطابع، وترجمة إنجليزية أو أخرى أسفل ذلك، جميعها بألوان كريمية وذهبية ناعمة. شخصية فانوس صغيرة تبدو نعسانة بعينين مغمضتين هادئتين في أسفل البطاقة. زر نصي صغير وخافت بعنوان 'تم' أسفل ذلك، بدون ألوان زاهية، بدون أي أوسمة أو عدادات نقاط خبرة ظاهرة على هذه البطاقة، بطابع هادئ وسكينة بالغة، بدون وجوه بشرية واقعية."

*(Remaining screens — Sleep Timer Selector, Episode List Sheet, Goodnight Idle State, Offline No-Content state, Parent Bedtime Configuration screen — follow the same two-prompt EN/AR template using these calm-mode tokens; full set available on request.)*

---

### 6.1 Technical Requirements
Kotlin, Jetpack Compose, MVVM, Clean Architecture, module `:feature:bedtime-audio`, depends on `:core:media-player` (shared Media3/ExoPlayer foundation from A.3), `:core:design-system`, `:core:offline-cache`.

### 6.2 Screen Mapping
`BedtimeAudioPlayerScreen` Composable; reuses the Media3 player session architecture from A.3's `:core:media-player` module rather than building a parallel audio engine.

### 6.3 Navigation Flow
Full-screen destination, deep link `noorheroes://bedtime/{content_id}`; "Calm Mode" toggle available from the standard Story Player navigates into this same screen/composable with a `forceCalmMode = true` parameter rather than being a wholly separate codepath.

### 6.4 State Management
`BedtimeAudioViewModel` manages `PlayerState` (shared sealed type with A.3's player where applicable) plus a dedicated `SleepTimerState` (Off, Active(remainingSeconds), Warning(secondsLeft), FadingOut, Expired) implemented via a **foreground Service + `AlarmManager`-backed fallback** (not a plain coroutine `delay()` in a ViewModel, which would be killed if the process is reclaimed) — this is the feature's most safety-critical implementation detail given FR-6's "100% reliability" requirement.

### 6.5 API Mapping
`BedtimeRepository.getConfig()` → `GET /v1/parent-controls/{child_id}/bedtime` (cached); `completeEpisode(silent=true)` → `POST /v1/content/{id}/complete` with `silent_completion: true` when in Bedtime Mode.

### 6.6 Analytics Mapping
`BedtimeAnalytics` fires sleep-timer lifecycle events tied to the actual foreground-service timer callbacks (not optimistic UI timing), ensuring `sleep_timer_expired`/`sleep_timer_fade_started`/`sleep_timer_auto_paused` accurately reflect real playback engine state.

### 6.7 Offline Support
Identical download/offline-cache mechanism as A.3 (Media3 `DownloadManager`, per-`child_id` cache namespace); Bedtime category content flagged for proactive "auto-suggest download" UI prompts per FR-11/Edge Case 9 (prompt only, never silent auto-download without explicit child/parent action).

### 6.8 Deep Linking
`noorheroes://bedtime/{content_id}` for "bedtime story ready" notification entry; `noorheroes://bedtime/continue` resumes the most recent in-progress bedtime content.

### 6.9 Push Notifications
Landing target for the "Tonight's bedtime story is ready 🌙" notification (sent ~30 min before the configured bedtime window start, per the platform notification table) — implemented by A.12, this feature only owns the deep-link destination.

### 6.10 Testing Strategy
- Unit: `SleepTimerState` transition logic, including mid-playback timer extension/cancellation (Edge Case 2), and natural-completion-before-timer-expiry cleanup (Edge Case 1).
- Foreground-service reliability test: simulate process trim/low-memory conditions and verify the `AlarmManager` fallback still fires the auto-pause within an acceptable tolerance window even if the primary in-process timer is killed.
- UI tests: Sleep Timer Selector only displays options ≤ parent ceiling; Dua Ending Card never renders XP/badge counters; Calm Mode toggle correctly forces calm visuals outside the bedtime window.
- Integration: full offline download → bedtime playback → sleep-timer-expiry → auto-pause flow with airplane mode enabled throughout.

---

### 13.1 Test Plan Summary
Coverage spans: sleep-timer reliability (the feature's signature risk), midnight-crossing bedtime windows, silent-completion reward parity, offline bedtime playback, and all 12 edge cases from §1.10.

### 13.2 Test Cases — Happy Path
1. Child sets a 20-minute sleep timer, listens, timer expires mid-episode → gentle fade → auto-pause → goodnight idle state, no abrupt cutoff.
2. Child listens to a bedtime episode to natural completion within the bedtime window → quiet reward recorded, Dua Ending Card shown (no celebratory animation), Next Episode offered if unlocked.
3. Parent configures a 22:00–06:00 (midnight-crossing) bedtime window → child opening the app at 23:30 or 05:00 correctly sees Bedtime Mode auto-applied; opening at 14:00 does not.

### 13.3 Edge Cases
All 12 items from §1.10.

### 13.4 Negative Cases
- Simulate OS process kill of the foreground audio/timer service mid-countdown → AlarmManager fallback still triggers auto-pause within acceptable tolerance (e.g., ±5 seconds).
- Attempt to `PUT` bedtime config using a child-mode session token → rejected.
- Attempt to select a sleep-timer duration above the parent-configured ceiling via a tampered API call (bypassing the UI's option-filtering) → server validates and rejects/clamps server-side as well, not relying solely on client-side option-hiding for enforcement of the underlying playback completion logic (note: the sleep timer itself is client-managed, so server enforcement here specifically refers to ensuring the bedtime_config ceiling value itself cannot be exceeded by a tampered write, not policing every local timer selection in real time).
- Force the Bedtime Configuration Service to be unreachable → app defaults to NOT auto-forcing Bedtime Mode (fails safe per §1.11), Calm Mode toggle remains manually available.

### 13.5 Regression Cases
Full Bedtime Audio suite re-run on every release touching this module, the shared Content & Playback Service, or the Reward Service.

### 13.6 Automation Cases
End-to-end: full offline download → bedtime playback → sleep-timer-expiry → auto-pause flow with airplane mode enabled; midnight-crossing-window automated time-travel test (mock system clock across the boundary); silent-completion reward-ledger-parity automated comparison test.

---

### Corresponding KMP blueprint requirements

#### `Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/01-bedtime-audio-player-core-screen.md`

##### 4. Objective
Build the `:feature:bedtime-audio` module's `BedtimeAudioPlayerScreen` Composable and `BedtimeAudioViewModel`, wrapping `library:kmpplayer`'s `AudioPlayerController`, driven by a `PlayerState`-equivalent sealed state consistent with A.3/K-03's state-machine discipline, fetching the audio manifest (B-02) on entry and rendering cover art, controls, and episode navigation.

##### 5. Business Requirements
- FR-1: displays cover art, title, moral lesson teaser, source/scholar-approval status, episode list, privacy-safe listen counts.
- FR-2: Play/Pause, Seek, Playback Speed, Sleep Timer, Download, Next/Previous Episode controls.
- FR-7: playback continues uninterrupted if the screen locks or app backgrounds (foreground media service).
- FR-8: Next/Previous respects A.3's Sequential Unlock rules — Previous always available, Next gated.
- FR-9: listen counts are privacy-safe aggregates only (consumed from B-02's `listen_count_aggregate`).
- §1.8 NFR: audio start-to-first-sound p95 < 800ms cached, < 1.5s streamed; controls ≥56dp primary, ≥44dp secondary.
- §6.1–6.4: module `:feature:bedtime-audio`, depends on `:core:media-player` (shared Media3 foundation from A.3), `:core:design-system`, `:core:offline-cache`.

##### 10. KMP Requirements
- `BedtimePlayerState` sealed class: `Loading, Buffering, Playing, Paused, Unavailable(reason), Completed(reward)` plus Bedtime-specific composed states from K-02/K-03/K-04 (`SleepTimerState`, calm-mode flag) rather than duplicating A.3/K-03's `PlayerState` — this is a parallel-but-consistent state machine for the audio-only surface, not a fork of A.3's exact type (different screen, different states like `ChoiceActive`/`QuizActive` are not applicable here).
- Manifest fetch (B-02, `format=audio`) on entry via `BedtimeManifestRepository`; `MediaSourceValidator.isValid()` checked before `controller.prepare()`.
- Resume position via `PlaybackSessionManager.getResumePosition()`, passed as the controller's start position on `prepare()`.
- Episode List Sheet: multi-part audio series, respects Sequential Unlock (reads unlock state from the manifest, same contract as A.3's episode list — reuse the unlock-state rendering component from `core-designsystem` if one exists, do not rebuild it).
- Next/Previous Episode: Previous always enabled; Next checks unlock state, shows the same lock-explanation pattern as A.3 (reuse the existing lock-explanation composable, do not duplicate).
- Foreground playback continuity: audio continues via a foreground `MediaSessionService` when backgrounded/screen-locked (the service itself is implemented/shared via `library:kmpplayer`; this screen configures and observes it, does not reimplement it).
- Loading/Buffering state renders an ambient glow pulse on the cover art (no platform spinner), title/cover visible immediately from cached manifest metadata even if audio itself buffers.

##### 12. Offline First
```
Downloaded Media (K-05's offline-cache, shared A.3 DownloadManager)
    ↓
BedtimeAudioViewModel (prefers local source if downloaded, else network from manifest)
    ↓
AudioPlayerController
    ↓
UI
```

##### 14. Localization
Title, moral-lesson teaser, and all on-screen text sourced from shared localization resources (EN/HI/AR/UR); audio dub track selection resolves per active locale, consistent with A.3/K-03's caption/audio-track locale-resolution pattern.

##### 15. RTL
Cover/header layout, control row order (previous/play/next), and scrub bar direction all mirror correctly for Arabic/Urdu; secondary control row (speed/timer/download/episode-list) also mirrors.

##### 18. Security
- Manifest signed URLs (from B-02/A.3) short-TTL, never logged in plaintext, handled entirely by `library:kmpplayer`'s existing secure cache handling.
- No new credential surface.

##### 19. Testing
- Unit: manifest-fetch success/failure handling, resume-position wiring, Next/Previous unlock-state gating.
- Player simulation: safe-stop transition to `Unavailable` on a fatal player error, verifying no raw technical text reaches any rendered string (mirror A.3/K-03's blocklist test approach).
- UI: cover art breathing animation renders correctly, control tap targets meet ≥56dp/≥44dp minimums, screen-reader labels present on all controls.
- Integration: cold-start timing measurement against the p95 budget on a low-end device profile.

##### 21. Final Verification Checklist
- [ ] `BedtimePlayerState` is the sole source of truth — no overlay/controller divergence
- [ ] Zero direct Media3/AVPlayer API calls anywhere in this module
- [ ] Cold start p95 < 1.5s with cached manifest; audio start p95 < 800ms cached / < 1.5s streamed
- [ ] All primary controls ≥56dp, secondary ≥44dp, screen-reader labeled
- [ ] Next Episode respects unlock state; Previous always available
- [ ] Playback continues via foreground service on background/screen-lock
- [ ] Resume position correctly read/persisted via `PlaybackSessionManager`
- [ ] All analytics events fire correctly with exactly one call site each, including `app_backgrounded_during_bedtime_playback`/`bedtime_playback_resumed_after_background` fired from the foreground service's own lifecycle, not Compose lifecycle
- [ ] Full RTL mirroring verified

#### `Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/02-sleep-timer-reliability-engine.md`

##### 4. Objective
Implement `SleepTimerState` as a sealed class and back it with both a foreground Service holding a coroutine countdown and an `AlarmManager.setExactAndAllowWhileIdle` fallback alarm targeting the same expiry instant, driving a smooth volume-ramp fade-out and auto-pause through K-01's `BedtimePlayerState` machine — never a raw bypass of it.

##### 5. Business Requirements
- FR-3: Sleep Timer options bounded by parent-set ceiling (B-01); child freely chooses up to the ceiling, or "until episode ends" if allowed.
- FR-6: expiry triggers a gentle audio fade-out (not abrupt cut) over a configurable duration (default 15s), followed by auto-pause.
- §1.8 NFR: sleep-timer-expiry auto-pause must be foreground-service-backed, not UI-thread-only — 100% reliability, non-negotiable.
- §1.10 Edge Case 1: natural completion before timer expiry cancels the now-moot timer cleanly, no leftover fade/pause attempt.
- §1.10 Edge Case 2: mid-playback timer change applies from the change moment, cancels/reschedules any pending fade under the old timer.
- §1.10 Edge Case 8: sleep-timer expiry coinciding with natural episode completion — completion/ending sequence takes precedence (handled jointly with K-04).
- §6.4/§7 Android AI Prompt: dual foreground-Service + `AlarmManager` architecture is the feature's most safety-critical implementation detail.

##### 10. KMP Requirements
- `SleepTimerState` sealed class exactly as specified: `Off, Active(remainingSeconds), Warning(secondsLeft), FadingOut, Expired`.
- Sleep Timer Selector renders **only** options ≤ the parent-set ceiling (from K-07) plus "until episode ends" if `allow_until_episode_ends_option` is true — options above the ceiling are not rendered disabled, they do not appear at all.
- Dual-timer architecture (Android): foreground Service coroutine countdown for the primary UI-driving timer, plus `AlarmManager.setExactAndAllowWhileIdle` scheduled at the identical expiry instant as a fallback; if the in-process timer is killed by the OS, the `BroadcastReceiver` triggers the same fade/pause logic path (not a separate/divergent implementation).
- iOS equivalent: since iOS background execution differs fundamentally from Android's `AlarmManager` model, the iOS implementation must use the platform's background audio session + a scheduled local notification or background task API as the fallback mechanism — confirm the exact iOS background-task API available to the app's existing background-audio entitlement setup before implementing; do not assume Android's exact API surface transfers directly.
- Fade-out: smooth volume ramp (200–500ms coroutine ticks) over the configured duration (default 15s, overridable per-content via B-02's `recommended_fade_duration_seconds` if populated) — never an abrupt volume-to-zero jump or a hard `pause()` without the ramp.
- Mid-playback timer extension: changing from e.g. 15 to 30 minutes recalculates expiry from the **change moment**, cancels any pending fade/pause callback scheduled under the old timer, and reschedules both the in-process timer and the `AlarmManager` fallback.
- Natural completion before timer expiry: cancel the pending timer (both in-process and `AlarmManager` fallback) cleanly — no leftover fade/pause attempt firing against already-stopped audio.
- All auto-pause/auto-fade actions call into K-01's `BedtimeAudioViewModel`'s exposed transition methods (e.g., `onSleepTimerExpired()`) — never a raw `controller.pause()` call from this module bypassing `BedtimePlayerState`.
- Wake-lock/foreground-service scope released promptly on pause/completion (battery NFR) — no continuous wake-lock beyond what's needed for active playback.
- `GoodnightIdleState`: on reaching `SleepTimerState.Expired` (fade + auto-pause complete), render this dedicated calm terminal composable — Screen Inventory §1.18 item 9, distinct from `SleepTimerControl`'s countdown-chip UI — offering only "Resume playback" or "Exit player" actions, no further interaction required from the child; also reachable via a manual pause-and-leave (not exclusively sleep-timer-driven).

##### 12. Offline First
Fully local/on-device mechanism; the only network dependency is the initial config fetch (K-07), which itself fails safe (defaults to no ceiling override needed since the timer itself is client-managed — confirm K-07's fail-safe default still yields a sane conservative ceiling for the selector to render, per B-01's safe-default response).

##### 14. Localization
Sleep timer duration labels (e.g., "30 minutes", "Until episode ends") sourced from shared localization resources across EN/HI/AR/UR; duration formatting respects locale-specific number formatting.

##### 15. RTL
Sleep Timer Selector list and countdown chip mirror correctly for Arabic/Urdu layouts.

##### 18. Security
No new security surface. Sleep-timer auto-pause/auto-exit must not interfere with B-03's completion idempotency — if a session is paused/exited via the sleep timer mid-episode, no completion call has fired, so there is nothing to reconcile with K-04's silent-completion flow.

##### 19. Testing
- Unit: `SleepTimerState` transition logic including mid-playback extension (Edge Case 2) and natural-completion-before-expiry cleanup (Edge Case 1).
- **Foreground-service reliability test (signature test for this sub-feature):** instrumented test simulating process trim/low-memory conditions, verifying the `AlarmManager` fallback still fires the auto-pause within acceptable tolerance (±5 seconds) even if the primary in-process timer is killed.
- Unit: fade-out uses a smooth volume ramp, never an abrupt cut (assert multiple intermediate volume values are set, not a single jump-to-zero call).
- UI: Sleep Timer Selector renders only options ≤ parent ceiling (mocked ceiling values).
- Unit: expiry-vs-natural-completion race — when both occur at the same instant, verify K-04's completion path takes precedence over the fade (this test may need to be co-located with or cross-referenced against K-04's test suite).

##### 21. Final Verification Checklist
- [ ] `SleepTimerState` implemented exactly as the five-state sealed class specified
- [ ] Dual-mechanism reliability (foreground Service + `AlarmManager` fallback) verified via a process-death simulation test
- [ ] Fade-out is a smooth multi-tick volume ramp, never an abrupt cut
- [ ] Sleep Timer Selector renders only options ≤ parent ceiling — no disabled-but-visible options above it
- [ ] Mid-playback timer extension reschedules correctly from the change moment, cancelling stale callbacks
- [ ] Natural completion before expiry cancels the timer cleanly with no leftover fade/pause attempt
- [ ] All auto-pause/fade actions route through `BedtimePlayerState`, zero raw controller bypass
- [ ] Wake-lock/foreground-service scope released promptly on pause/completion
- [ ] `GoodnightIdleState` renders on both the sleep-timer-expiry path and the manual pause-and-leave path, offering only Resume/Exit
- [ ] All seven analytics events fire tied to real timer callbacks or the corresponding UI-render event, not optimistic UI timing
- [ ] iOS fallback mechanism confirmed against actual platform capability, not assumed from Android's API

#### `Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/03-calm-mode-bedtime-theme-application.md`

##### 4. Objective
Implement `forceCalmMode` as a parameter accepted by `BedtimeAudioPlayerScreen` (K-01), resolved once at entry from the time-window (K-07) or explicit toggle, applying dimmed theme tokens, muted accent overrides, and breathing cover-art animation — sourced from the same `core-designsystem` token set A.3/K-05 already established, not a second parallel theming system.

##### 5. Business Requirements
- FR-4: Bedtime Mode is a system-wide state — any content surface entered during the window (or via explicit entry) applies the same dimmed visual treatment.
- FR-5: dims UI, disables stimulating reward effects, ends every session with dua/reflection — zero exceptions.
- FR-14: outside the window, the player functions normally unless the child explicitly opts in via "Calm Mode" toggle — the automatic window-based trigger stays separate from the manual toggle.
- §2.1: Calm Palette Application — dimmed navy/teal gradient, breathing cover art, `gold-bedtime` muted accent override (a deliberate token override, not a hardcoded local color).
- §1.10 Edge Case 10: daytime Calm Mode toggle used, then the actual window begins mid-session — no jarring transition, session continues in the already-calm visual state.
- A.3/K-05 §10: `isBedtimeMode` resolved exactly once at entry, no mid-session flicker on window-boundary crossing — this same discipline applies here, adapted to K-01's screen rather than K-05's overlay.

##### 10. KMP Requirements
- `forceCalmMode` resolved exactly once when `BedtimeAudioPlayerScreen` is composed/launched — passed down as an immutable parameter, never re-evaluated mid-session even if the window boundary is crossed during playback (identical discipline to A.3/K-05).
- Resolution inputs: entry point (Home Bedtime Corner / Stories Bedtime category / explicit Calm Mode toggle / direct deep link) + current time + K-07's cached bedtime window.
- Theme override applies regardless of device light/dark mode: dimmed navy/teal gradient background, `gold-bedtime` muted amber accent (not the vibrant daytime gold), large soft-glow breathing cover art (slow subtle scale pulse loosely synced to playback, never jarring/fast).
- Edge Case 10 handling: if Calm Mode was already manually toggled and the actual window begins mid-session, no re-render/flicker occurs since the visual state was already calm-mode-equivalent — the resolved `forceCalmMode` value simply remains `true` throughout.
- Zero flashing elements under any circumstance within calm-mode visuals — stricter reduced-motion enforcement than the standard (non-bedtime) player state.

##### 12. Offline First
Bedtime-window configuration cached locally via K-07 (reused, not duplicated) — calm-mode resolution works fully offline.

##### 14. Localization
No new localized strings beyond what K-01 already renders; calm-mode is a purely visual/theme state.

##### 15. RTL
Breathing cover-art animation is symmetric and requires no directional mirroring; surrounding layout mirroring is inherited from K-01's existing RTL handling.

##### 18. Security
No new security surface.

##### 19. Testing
- Unit: `BedtimeCalmModeResolver` determinism — mocked time-window boundary cases (mirrors A.3/K-05's boundary test suite), explicit-toggle override cases.
- Unit: Edge Case 10 — Calm Mode already active before window begins mid-session, verify no `forceCalmMode` value change/flicker.
- UI: theme applies identically regardless of device light/dark mode (mocked both).
- UI: reduced-motion assertion — zero flashing elements verified.
- Integration: confirm this module's resolver produces identical results to A.3/K-05's resolver given identical inputs (a cross-module consistency test, given both must agree on what "within the bedtime window" means for the same child at the same instant).

##### 21. Final Verification Checklist
- [ ] `forceCalmMode` resolved exactly once at K-01's screen entry, never flickers mid-session
- [ ] Resolver logic is genuinely shared with (or provably consistent with) A.3/K-05's `BedtimeModeResolver` — not a silently-drifting duplicate
- [ ] Dimmed theme tokens (`gold-bedtime`, navy/teal palette) sourced from `core-designsystem`, not hardcoded locally
- [ ] Breathing cover-art animation isolated to its own recomposition scope
- [ ] Zero flashing elements under any circumstance
- [ ] Edge Case 10 (Calm Mode already active before window begins) produces no flicker
- [ ] Standard Story Player's Calm Mode toggle correctly routes audio-format content into K-01
- [ ] Both analytics events fire exactly once per resolution

#### `Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/04-dua-calm-reflection-ending-flow.md`

##### 4. Objective
On completion threshold reached while `forceCalmMode` (K-03) is true, call B-03's completion endpoint with `silent_completion: true` and render the Dua/Calm-Reflection Ending Card instead of the standard celebratory completion screen — verified to contain zero XP/points/badge counters while still confirming the reward was recorded via a separate repository-level assertion.

##### 5. Business Requirements
- FR-10: on reaching the completion threshold, the player transitions directly to a dua/calm-reflection card — reward still recorded quietly, not visually celebrated.
- §2.1: Dua Ending Card — warm parchment-on-navy card, gentle fade-in (≥800ms), no XP/badge counters visible even though the reward was recorded.
- §1.10 Edge Case 7: completion-threshold calculation based on actual content consumed (percentage of duration), not wall-clock time — correct even at altered playback speed.
- §1.10 Edge Case 8: sleep-timer expiry coinciding with natural completion — completion/ending sequence takes precedence (child still gets the calm dua ending, not pre-empted by a fade cutting off the dua itself).

##### 10. KMP Requirements
- Completion-threshold detection: based on percentage of actual content consumed (using `AudioPlayerController`'s reported position/duration), not wall-clock elapsed time — so a 1.5x-speed listen still correctly registers full completion at the same content-percentage threshold as 1x speed.
- On threshold reached with `forceCalmMode == true`: call `BedtimeCompletionRepository.completeEpisode(contentId, silentCompletion=true)` (B-03), then transition `BedtimePlayerState` to a completion state rendering `DuaReflectionEndingCard` instead of any standard celebratory completion UI.
- On threshold reached with `forceCalmMode == false`: standard (non-bedtime) completion flow applies — this module does not alter that path, it only adds the calm-mode branch.
- `DuaReflectionEndingCard`: dua text (reusing A.5's rendering pattern) via `dua_ending_ref` (B-02), sleepy/calm Noor companion illustration variant, single low-key "Done"/"Next Episode" action, gentle fade-in (≥800ms) — the composable tree for this card must contain **zero** XP/points/badge counter views, verified by a dedicated UI test.
- Reward-recorded-but-not-celebrated verification: a **separate repository-level test** (not a UI assertion) confirms `BedtimeCompletionRepository.completeEpisode()` was actually called with `silentCompletion=true` — decoupling "was the reward recorded" from "was it visually celebrated" as two independently-tested facts.
- Edge Case 8 handling: if sleep-timer expiry (K-02) and natural completion threshold occur at the same instant, this module's completion path takes precedence — coordinate with K-02 via a shared "completion in progress" guard so K-02's fade-out logic checks and yields if a completion transition has already begun.
- Next Episode offer: if unlocked (per K-01's Sequential Unlock check), offered from the Dua Ending Card with the same Bedtime Mode treatment retained if still within the window.

##### 12. Offline First
Completion calls queue/retry per the existing offline-heartbeat-and-completion pattern established in A.3/K-03 (fail gracefully without blocking the UI transition to the Dua Ending Card — the child should see the calm ending immediately even if the network call is still in flight/retrying in the background).

##### 14. Localization
Dua text (Arabic + transliteration + translation) via A.5's existing localization resources; "Done"/"Next Episode" labels via shared localization resources across EN/HI/AR/UR.

##### 15. RTL
Dua card layout mirrors correctly (text alignment, companion illustration placement, action button position) for Arabic/Urdu — reuse A.5's already-verified RTL handling for the dua-text component itself.

##### 18. Security
No new security surface; completion call reuses B-03's existing idempotency-key handling (via K-01's session-scoped `client_event_id`, generated once per session per A.3/K-03's established convention — reused here, not regenerated).

##### 19. Testing
- Unit: completion-threshold detection correctness at altered playback speeds (Edge Case 7) — assert percentage-based, not wall-clock-based.
- Unit: `forceCalmMode` branching — calm-mode sessions route to `DuaReflectionEndingCard`; non-calm sessions route to the standard completion flow (unaffected).
- **UI test:** `DuaReflectionEndingCard` composable tree contains no XP/points/badge counter views anywhere.
- **Repository-level test:** confirms the reward completion call still occurred with `silentCompletion=true`, independent of the UI assertion above.
- Integration: Edge Case 8 — simulate simultaneous sleep-timer expiry and natural completion, verify the Dua Ending Card is shown (not pre-empted by the fade).

##### 21. Final Verification Checklist
- [ ] Completion-threshold detection is percentage-of-content-consumed based, correct at any playback speed
- [ ] `forceCalmMode=true` sessions call B-03 with `silent_completion=true` and route to the Dua Ending Card
- [ ] `forceCalmMode=false` sessions are entirely unaffected by this sub-feature's changes
- [ ] `DuaReflectionEndingCard` composable tree verified to contain zero XP/points/badge views
- [ ] Reward-call-occurred fact independently verified via a repository-level test, decoupled from the UI assertion
- [ ] Edge Case 8 (simultaneous timer expiry + completion) resolves in favor of the completion/dua flow
- [ ] Next Episode offered correctly when unlocked, retaining Bedtime Mode treatment
- [ ] All three analytics events fire correctly

#### `Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/05-bedtime-offline-downloads-auto-suggest.md`

##### 4. Objective
Wire K-01's Bedtime Audio Player to A.3's existing offline-download/cache mechanism, add Bedtime-category "auto-suggest download" prompting (prompt-only, never silent auto-download), and implement the offline-state UX for no-content and next-episode-not-downloaded scenarios specific to this screen.

##### 5. Business Requirements
- FR-11: download uses the same entitlement/parent-policy checks as A.3's download manifest endpoint; Bedtime category content is prioritized for "auto-suggest download."
- §1.8 NFR: full offline playback parity with online, since bedtime is a predictable recurring need best served by pre-downloaded content.
- §1.10 Edge Case 5: no internet + no pre-downloaded content → calm fallback message, never a hard error.
- §1.10 Edge Case 9: repeated streaming failures in a low-connectivity region → system may proactively prompt (not auto-execute) "Would you like to download tonight's story for offline listening?"
- §1.10 Edge Case 11: Next Episode unlocked but not downloaded, offline → clear "needs internet" message, not a silent failure or hanging network call.

##### 10. KMP Requirements
- Source selection: `BedtimeAudioViewModel` prefers `KMPPlayerSource.Local` (via A.3's DownloadManager cache) when available, falling back to network per the manifest's signed URL — identical selection logic to A.3/K-03, reused not reimplemented.
- `BedtimeDownloadSuggestionEngine`: flags content as Bedtime-category-eligible for proactive suggestion (from the manifest/catalog's existing category metadata); detects repeated streaming failures (a simple failure-count-over-window heuristic, confirm against any existing low-connectivity-detection utility elsewhere in the codebase before building a new one) and surfaces a one-time, dismissible "Would you like to download tonight's story for offline listening?" prompt — never a silent/automatic download regardless of this signal.
- No-content offline fallback: when offline with zero downloaded bedtime-eligible content, render a calm "no story available right now, here's a dua to read together" fallback (reusing A.5's dua-rendering component per K-04's pattern) rather than a blank screen or hard error.
- Next-episode-not-downloaded offline notice: tapping Next on an unlocked-but-undownloaded episode while offline shows a clear "needs internet to fetch this episode" message and does not attempt a network call that could hang — stays on the current episode.
- Download entitlement/parent-policy checks reuse A.3's `POST /v1/downloads/manifest` call exactly as-is — no new entitlement logic introduced here.

##### 12. Offline First
```
Downloaded Media (A.3's DownloadManager cache, per-child_id namespace)
    ↓
BedtimeAudioViewModel (prefers Local source, else Network from manifest)
    ↓
AudioPlayerController
    ↓
UI (offline-state components when applicable)
```

##### 14. Localization
Offline fallback messages and "needs internet" notices sourced from shared localization resources across EN/HI/AR/UR.

##### 15. RTL
Offline-state components (fallback card, not-downloaded notice) mirror correctly for Arabic/Urdu, consistent with K-01's existing RTL handling.

##### 18. Security
No new security surface — download entitlement/parent-policy checks are exactly A.3's existing, unmodified logic.

##### 19. Testing
- Unit: `BedtimeDownloadSuggestionEngine` — Bedtime-category detection, failure-count-threshold triggering, prompt-only behavior (assert no download call is ever made without explicit user confirmation, even when the suggestion condition is met).
- UI: no-content offline fallback renders the calm dua-fallback message, not a blank/error screen.
- UI: next-episode-not-downloaded notice renders correctly and does not attempt a network call (mocked offline state, assert zero network client invocations).
- Integration: full offline download → bedtime playback → sleep-timer-expiry → auto-pause flow with airplane mode enabled throughout (shared integration scenario with K-02).

##### 21. Final Verification Checklist
- [ ] Source selection prefers local downloaded content, falls back to network — identical logic to A.3/K-03
- [ ] `BedtimeDownloadSuggestionEngine` never triggers a download without explicit user confirmation
- [ ] No-content offline state renders a calm fallback (dua suggestion), never a blank/error screen
- [ ] Next-episode-not-downloaded offline tap shows a clear message, attempts zero network calls
- [ ] Full offline download → playback → sleep-timer-expiry → auto-pause flow verified under airplane mode
- [ ] Download entitlement checks reuse A.3's existing `POST /v1/downloads/manifest` unmodified
- [ ] All four analytics events fire correctly

#### `Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/06-bedtime-notification-deep-link-continue-listening.md`

##### 4. Objective
Register `noorheroes://bedtime/{content_id}` and `noorheroes://bedtime/continue` deep links in `core-navigation`, routing correctly into K-01's `BedtimeAudioPlayerRoute` whether the app is cold-started or already running, and handling not-entitled/withdrawn-content edge cases gracefully.

##### 5. Business Requirements
- §6.8: `noorheroes://bedtime/{content_id}` for "bedtime story ready" notification entry; `noorheroes://bedtime/continue` resumes the most recent in-progress bedtime content.
- §6.9: landing target for the "Tonight's bedtime story is ready 🌙" notification (sent ~30 min before the configured window start) — implemented by A.12, this feature only owns the deep-link destination.
- FR-14: deep link arriving outside the bedtime window does not force Bedtime Mode visuals unless explicitly toggled (consistent with K-03's resolution logic, which already accounts for entry point as one of its inputs).

##### 10. KMP Requirements
- `noorheroes://bedtime/{content_id}`: resolves directly to `BedtimeAudioPlayerRoute(contentId)` — identical handling whether the app is cold-started (deep link resolved after app init) or already running (immediate navigation).
- `noorheroes://bedtime/continue`: resolves the most recent in-progress bedtime content via `PlaybackSessionManager`'s existing resume-position tracking (reused, not duplicated) filtered to Bedtime-category content, then navigates to `BedtimeAudioPlayerRoute` with that resolved `contentId`; if no in-progress bedtime content exists, falls back to the Bedtime Corner/Stories Bedtime category screen rather than a dead end.
- Not-entitled/withdrawn content via deep link: routes into K-01's existing safe-stop + alternative pattern (reuses K-01's `Unavailable` state handling, no separate error path for the deep-link case).
- Outside-window entry: `forceCalmMode` resolution (K-03) treats deep-link entry the same as any other entry point — no special-casing that would force calm mode simply because the entry came from a notification (the window/toggle inputs alone determine the result, consistent with FR-14).

##### 12. Offline First
Deep-link resolution itself requires no network call; the subsequent manifest fetch (K-01) follows K-01's existing offline-first behavior.

##### 14. Localization
No new localized strings (notification copy itself is owned by A.12).

##### 15. RTL
Not applicable — this sub-feature is navigation-only, no new UI surface.

##### 18. Security
Deep-link `content_id` is validated against the same entitlement checks K-01's manifest fetch already performs — a malformed or unauthorized `content_id` in the deep link cannot bypass entitlement, it simply surfaces K-01's existing `Unavailable`/error handling.

##### 19. Testing
- Unit: deep-link pattern matching for both `noorheroes://bedtime/{content_id}` and `noorheroes://bedtime/continue`.
- Unit: "continue" resolution correctly filters to Bedtime-category in-progress content, falls back to the Bedtime Corner when none exists.
- Integration: cold-start deep-link resolution vs. already-running-app resolution both navigate correctly.
- Integration: deep link to withdrawn/not-entitled content routes into K-01's existing safe-stop pattern, not a raw crash or unhandled route.

##### 21. Final Verification Checklist
- [ ] Both deep-link patterns registered and correctly route to `BedtimeAudioPlayerRoute`
- [ ] "Continue" correctly resolves the most recent in-progress Bedtime-category content, with a sane fallback when none exists
- [ ] Cold-start and already-running-app resolution both work identically
- [ ] Not-entitled/withdrawn content via deep link reuses K-01's existing safe-stop pattern, no separate crash-prone path
- [ ] Deep-link entry does not bypass K-03's `forceCalmMode` resolution logic or force calm mode inappropriately
- [ ] `entry_source` correctly reflects `notification` vs. `continue_listening` on `bedtime_player_opened`

#### `Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/07-parent-bedtime-configuration-repository.md`

##### 4. Objective
Implement `BedtimeRepository.getConfig()` as a cached client for B-01's `GET /v1/parent-controls/{child_id}/bedtime`, applying the "changes apply at next session" caching rule, and a documented fail-safe default when the fetch fails.

##### 5. Business Requirements
- §3.4: client caches aggressively (5–15 min); config changes apply at next session, not mid-session.
- §1.11 Error Handling: parent bedtime-window config fetch failure → player defaults to NOT forcing Bedtime Mode automatically (fails safe), but the explicit Calm Mode toggle remains available regardless.
- §1.10 Edge Case 4: parent narrows the bedtime window while a session is already in Bedtime Mode within the now-excluded time — current session remains in Bedtime Mode until exited; new window applies next session (this is a direct consequence of this repository's caching contract, not re-fetching mid-session).
- §12: Bedtime config tampering by a child is a write-side (B-01) concern; this repository only reads.

##### 10. KMP Requirements
- `getConfig(childId)`: cache-first read (5–15 min TTL) against B-01's endpoint; on cache miss, fetches remotely and updates the local cache.
- **Fail-safe default:** if the remote fetch fails (network error, `5xx`, timeout) and no valid cached value exists, `getConfig()` returns a safe-default `BedtimeConfig` with `windowStart = null`, `windowEnd = null` (i.e., "no auto-applied window") rather than throwing — callers (K-03) must never crash or block on this failure, and the Calm Mode manual toggle must remain available regardless of this fallback.
- Config-changes-apply-at-next-session rule: this repository does **not** poll or re-fetch mid-session; a cached value read at session start remains authoritative for that session's `forceCalmMode` resolution (K-03), even if the parent changes the config on another device mid-session (Edge Case 4).
- Reuses the existing parent-settings local cache store (no new local database/table) — if the existing cache infrastructure is keyed generically (e.g., a generic key-value parent-settings cache), this repository's config is stored under a namespaced key rather than introducing a dedicated new local table.

##### 12. Offline First
Bedtime-window configuration is cached locally so bedtime-mode resolution (K-03) and sleep-timer ceiling lookup (K-02) both work fully offline once an initial fetch has succeeded at least once; a fully offline first-ever session (never previously fetched) uses the fail-safe default.

##### 14. Localization
Not applicable — data-layer only, no user-facing strings.

##### 15. RTL
Not applicable.

##### 18. Security
No new security surface — this repository only reads; B-01 enforces all write-side authorization. No sensitive data beyond the child's own bedtime schedule is cached (not treated as high-sensitivity PII, consistent with B-01's own data-classification).

##### 19. Testing
- Unit: cache-hit path returns the cached value without a network call.
- Unit: cache-miss path fetches remotely and populates the cache.
- **Unit: fetch-failure fail-safe test** — simulate a network error with no valid cache present, assert `getConfig()` returns the safe-default (`null` window fields) rather than throwing.
- Unit: fetch-failure with a valid (possibly stale) cache present — assert the stale cached value is used rather than the fail-safe default (stale-but-valid data preferred over no data, consistent with the "apply at next session" rule not requiring real-time freshness).
- Integration: confirms no duplicate local storage mechanism is introduced — assert the underlying storage call sites match the existing parent-settings cache infrastructure's API, not a newly introduced one.

##### 21. Final Verification Checklist
- [ ] `getConfig()` is cache-first with a 5–15 minute TTL
- [ ] Fetch failure with no valid cache returns a safe null-window default, never throws
- [ ] Fetch failure with a valid (possibly stale) cache uses the cached value in preference to the fail-safe default
- [ ] No new local storage mechanism introduced — reuses the existing parent-settings cache infrastructure
- [ ] Config read at session start remains authoritative for that session (no mid-session re-fetch), consistent with Edge Case 4
- [ ] `BedtimeRepository` correctly injectable into K-02 and K-03 via existing DI conventions

#### `Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/08-playback-speed-selector.md`

##### 4. Objective
Build `PlaybackSpeedSelector` as a simple list-style modal (matching the Sleep Timer Selector's low-light simplicity requirement), reading available speeds from B-02's `playback_speed_options` manifest field, applying the selected rate to `AudioPlayerController`, and correctly re-deriving completion-threshold math at the new speed (coordinating with K-04's percentage-based, not wall-clock-based, completion detection).

##### 5. Business Requirements
- FR-2: Playback Speed (e.g., 0.8x/1x/1.2x) is one of the required controls on the Audio Bedtime Player.
- §1.8 NFR: all controls large-tap-target (≥56dp primary / ≥44dp secondary), high-contrast, full screen-reader support — speed selector is a secondary control (≥44dp entry point) but its modal options list must still meet the same low-light-usability bar as the Sleep Timer Selector.
- §2.2: "speed/timer selectors are simple list-style modals, not complex gesture-based pickers (low-light, possibly half-asleep child usage context demands maximum simplicity)."
- §1.10 Edge Case 7: playback speed changed mid-episode → completion-threshold calculation must still be based on actual content consumed (percentage of total duration), not wall-clock time, so a 1.5x-speed listen still correctly registers full completion.
- §1.19: `playback_speed_changed` analytics event.

##### 10. KMP Requirements
- `PlaybackSpeedSelector`: simple vertical list of speed options sourced from B-02's `playback_speed_options` (e.g., `[0.8, 1.0, 1.2]`) — no hardcoded option list in the composable itself, since content-specific overrides could exist in a future manifest revision.
- Current selection highlighted; selecting a new option applies immediately (no separate "confirm" step, consistent with the low-friction list-modal pattern) and closes the sheet.
- Rate change applies to `AudioPlayerController` immediately, mid-playback, without a pause/resume glitch.
- Completion-threshold math (owned by K-04) must remain percentage-of-duration-consumed based regardless of the active rate — this sub-feature's only obligation is to ensure the rate change is correctly reflected in whatever position/duration values K-04 reads (i.e., don't let a rate change desync the controller's reported position), not to reimplement K-04's threshold logic itself.
- Accessibility: options list items ≥44dp tap targets, screen-reader labeled with the speed value and "currently selected" state.

##### 12. Offline First
Fully local — speed selection and application require no network access; works identically online/offline.

##### 14. Localization
Speed labels (e.g., "0.8x — Slower", "1.0x — Normal", "1.2x — Faster") sourced from shared localization resources across EN/HI/AR/UR; numeric formatting respects locale conventions.

##### 15. RTL
List items and the modal sheet mirror correctly for Arabic/Urdu.

##### 18. Security
No new security surface.

##### 19. Testing
- Unit: selector renders options exactly matching `playback_speed_options` from the manifest (no hardcoded fallback list masking a missing/malformed manifest field — confirm the correct empty/error-state behavior if the field is absent, likely falling back to a safe default `[1.0]`).
- Unit: `setPlaybackSpeed()` correctly calls `AudioPlayerController`'s rate-setting API with the selected value.
- UI: current-selection highlighting; tap-target size ≥44dp; screen-reader labels present.
- Integration (coordinate with K-04): completion-threshold correctness at 1.5x speed remains percentage-based, not wall-clock (this is primarily K-04's test, but this sub-feature's rate-change implementation must not break it — a regression check against K-04's existing Edge-Case-7 test is sufficient, not a duplicate test).

##### 21. Final Verification Checklist
- [ ] Speed options rendered directly from B-02's `playback_speed_options`, with a safe `[1.0]` default if the field is absent — never a hardcoded list masking a manifest gap
- [ ] Rate change applies immediately mid-playback with no glitch
- [ ] Current selection visibly highlighted, ≥44dp tap targets, screen-reader labeled
- [ ] `playback_speed_changed` fires exactly once per user-initiated change, never on initial mount
- [ ] K-04's percentage-based completion-threshold test still passes with a rate change applied mid-session
- [ ] Full RTL mirroring verified

#### `Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/09-parent-bedtime-ritual-status-widget.md`

##### 4. Objective
Build `BedtimeRitualStatusWidget`, a small Composable placed on the Parent Dashboard (A.2's screen — this sub-feature contributes the component, not a new page) that reads B-04's `GET /v1/children/{id}/bedtime-ritual-status` and renders a simple completion indicator, with an optional drill-in link to A.3's Story Insights for full detail.

##### 5. Business Requirements
- FR-12: parent sees a lightweight "bedtime ritual happened" indicator, non-invasive (completion fact only, not full listening transcript/analytics), on their Dashboard.
- §1.9 Acceptance Criteria: "Given a parent views their Dashboard, when they check 'Bedtime Ritual' status, then they see a simple completion indicator (e.g., 'Bedtime story completed tonight ✓') without exposing a full play-by-play transcript... unless they explicitly drill into Story Insights (A.3)."
- §1.18 Screen Inventory item 16: Component (Parent Area), entry point Parent Dashboard, exit point "Story Insights (A.3) for full detail, if parent drills in."
- §12.6: this widget's data source (`bedtime_session_log`) stores only a boolean + date by design — the widget itself must not attempt to render or request anything beyond that.
- §19 (B-04's analytics requirement): `parent_bedtime_ritual_status_viewed` fired when the widget is viewed.

##### 10. KMP Requirements
- `BedtimeRitualStatusRepository.getStatus(childId, date = today)`: thin client for B-04's endpoint, no local caching required beyond standard short-TTL request de-duplication (this is a low-frequency, low-cost read — a full offline-cache layer is not warranted, unlike K-07's config, which many other modules depend on repeatedly).
- Widget renders exactly what §1.9's acceptance criteria specifies: a simple completion indicator (e.g., "Bedtime story completed tonight ✓" if `ritual_completed: true`, or a neutral/no-indicator state if `false` — confirm the PRD's implied behavior for the false case is "no alarming negative indicator," consistent with the feature's overall non-invasive, non-shaming tone toward missed nights).
- Drill-in: tapping/clicking the widget (only when `ritual_completed: true`, or generally — confirm against Screen Inventory's stated exit point) navigates to A.3's existing Story Insights screen for full detail — this widget itself never renders duration, content title, or any other listening detail beyond the boolean fact.
- Widget uses standard (non-bedtime) `core-designsystem` visual tokens — this is parent-facing daytime UI, not a Bedtime Mode surface, and must not inherit K-03's dimmed theme overrides.
- Loading state: brief skeleton/placeholder while the status fetch resolves; error state: silently omit the widget or show a neutral "unable to load" placeholder rather than a jarring error banner on the Dashboard (a single non-critical widget failing should not disrupt the rest of the Dashboard).

##### 12. Offline First
Not a primary concern for this widget (Parent Dashboard is typically viewed with connectivity); on fetch failure, degrade to the neutral "unable to load" placeholder described above rather than blocking the Dashboard.

##### 14. Localization
"Bedtime story completed tonight ✓" and neutral/placeholder copy sourced from shared localization resources across EN/HI/AR/UR.

##### 15. RTL
Widget layout (icon/checkmark placement relative to text) mirrors correctly for Arabic/Urdu.

##### 18. Security
- Parent-session-only (inherits the Parent Dashboard's existing auth context — no separate auth check needed in this widget beyond what hosting the widget on an already-parent-gated Dashboard provides).
- Renders strictly the boolean+date fact B-04 returns — no code path in this widget can request or display more detailed data (there is no more detailed field in B-04's response to accidentally expose).

##### 19. Testing
- Unit: widget correctly renders the "completed" state vs. the neutral/no-indicator state based on `ritual_completed`.
- Unit: fetch-failure renders the neutral placeholder, not an error that disrupts the Dashboard.
- UI: drill-in tap navigates to A.3's Story Insights screen.
- UI: widget renders using standard (non-bedtime) theme tokens regardless of whether the child is currently in an active Bedtime Mode session elsewhere in the app (theme independence test — this widget's theme must never accidentally inherit K-03's overrides).
- Integration: `parent_bedtime_ritual_status_viewed` fires exactly once per successful widget render.

##### 21. Final Verification Checklist
- [ ] Widget renders "completed" vs. neutral state correctly from B-04's boolean response
- [ ] No code path in the widget can render duration, content title, or any data beyond the boolean+date fact
- [ ] Fetch failure degrades to a neutral placeholder, never a Dashboard-disrupting error
- [ ] Drill-in navigates to A.3's existing Story Insights screen, no duplicate detail screen created
- [ ] Widget uses standard (non-bedtime) theme tokens, verified independent of any active Bedtime Mode session elsewhere in the app
- [ ] `parent_bedtime_ritual_status_viewed` fires exactly once per successful render
- [ ] Widget registered via A.2's existing Dashboard widget-hosting convention, no Dashboard layout logic modified directly

## A5 — Feature_A5_Quran_Arabic_Learning

PRD: `PRD_Documents/Child App (1-12)/Feature_A5_Quran_Arabic_Learning.md`

Coverage: 21 mandatory FR records; all preserved verbatim below. Feature has 35 inventory records including components/states. Components and states must not inflate independently executed screen count.

### Existing screenshot candidates

- `Screens/Mobile App/Learn/Feedback.png` — inventoried only
- `Screens/Mobile App/Learn/Skill Tree-01.png` — visually inspected
- `Screens/Mobile App/Learn/Skill Tree-02.png` — inventoried only
- `Screens/Mobile App/Learn/Skill Tree-03.png` — inventoried only
- `Screens/Mobile App/Learn/Skill Tree-04.png` — inventoried only
- `Screens/Mobile App/Learn/Skill Tree-05.png` — inventoried only
- `Screens/Mobile App/Learn/Skill Tree-06.png` — inventoried only
- `Screens/Mobile App/Learn/Skill Tree-07.png` — inventoried only
- `Screens/Mobile App/Learn/Skill Tree-08.png` — inventoried only
- `Screens/Mobile App/Learn/Surah Practice-01.png` — inventoried only
- `Screens/Mobile App/Learn/Surah Practice-02.png` — inventoried only

### Complete normative functional coverage

### 1.7 Functional Requirements

**FR-1** Learn Tab entry point ("Quran Learning Home") shows a skill-tree map with mastery indicators, organized by Surah/skill-node, plus mode selectors for Quran Game variants and a placement-check option for new learners (source: Blueprint screen catalog, "Quran Learning (Quran Game Hub)").
**FR-2** Skill Tree states are exactly: `Locked → Ready → Learning → Practicing → Mastered → Needs Refresh` (source §6.3/§21.9). A node's `Locked` state must display what prerequisite unlocks it, not just a generic lock.
**FR-3** Mastery score is computed from: accuracy, independent attempts, recency, difficulty, and transfer across question types — the child-facing UI shows progress (e.g., a filling progress ring, a state label) without exposing the raw composite confidence score (source §21.9: "should show progress without revealing a confusing raw model score").
**FR-4** `Needs Refresh` state is triggered by spaced-repetition decay logic (time since last correct demonstration, weighted by original mastery strength) and surfaces as a gentle "let's review this together" prompt, never framed as a regression/failure.
**FR-5** Quran Game modes must include at minimum: ayah ordering, listen-and-select matching ayah, find-the-missing-word, surah-name-to-theme matching (child-safe/approved context only), recitation echo with pronunciation coaching, and progressive-reveal memorization (source §21.9 "Quran Game" game ideas).
**FR-6** Arabic Letters module must include: hear-and-match, tracing, isolated/initial/medial/final form matching, harakah (diacritic) sound pairing, find-the-letter-in-an-approved-word, build-a-word-from-sound-tiles — with spaced review scheduling applied across sessions (source §21.9 "Arabic Letters").
**FR-7** Arabic Letter detailed flow: play phoneme → child selects 1-of-4 letters → child traces the correct shape → letter shown in a familiar word → scheduled for spaced review. Mastery requires correct performance across different question forms and across more than one session (not masterable in a single sitting) — source §21.9.
**FR-8** Surah Learning screen shows ayah-by-ayah list with audio, a translation toggle, Tajweed-rule highlighting inline with the text, and a recitation recorder; actions: listen, repeat, record pronunciation attempt, request a hint, mark ayah as practiced (source: Blueprint screen catalog "Surah Learning").
**FR-9** Microphone-denied or parent-disabled state must fall back to listen-only practice — the child can still progress through listening/repetition-without-recording paths; this is not a dead end (source: Blueprint, "Mic-denied state falls back to listen-only practice").
**FR-10** AI pronunciation scores are advisory and confidence-aware: the system must never label a recitation/worship act as "accepted" or "rejected," must never imply religious/spiritual validity, and must present feedback strictly as pedagogical coaching (e.g., "try emphasizing this letter more" rather than "incorrect") — source §6.3/§21.9, a hard non-negotiable rule.
**FR-11** Raw child voice recordings are not retained after processing by default; only derived, non-reversible feedback signals (e.g., a phoneme-level score) may be retained for progress tracking, never the raw audio itself unless a parent explicitly opts in to a distinct "save recordings" feature (off by default) for their own private playback.
**FR-12** Low-confidence AI pronunciation results must fall back to a "compare against the recorded reference example" self-assessment mode rather than presenting an uncertain automated score as if it were reliable (source §21.9: "Low-confidence results fall back to recorded examples").
**FR-13** Parent must be able to disable microphone/AI pronunciation features per child (not just globally) from Parental Controls (cross-ref C.23); when disabled, all recitation practice defaults to listen-and-self-assess mode app-wide for that child, with no UI path to bypass this setting from within the Learn tab.
**FR-14** Tajweed module flow: introduce one rule with an approved example → listen at normal and slow speed → identify the rule in an example → optional microphone repeat with visual coaching → short assessment (source §21.9 "Tajweed" flow) — each step is sequential and the microphone step is skippable/replaced by listen-only per FR-9/FR-13.
**FR-15** Daily Quiz (Learn-tab-specific instance, shared engine with A.8) assembles exactly 5 questions from recently-learned content plus identified weak skills; question types: multiple choice, sequence, true/false, image match, audio match; immediate explanation shown after each answer; incorrect answers enter a short retry set within the same session (source §21.9).
**FR-16** Quiz completion awards effort XP for participation regardless of accuracy; accuracy affects mastery-score computation, not base participation XP — this separation is intentional (a child should never feel "punished" with zero reward for attempting a hard quiz) (source §21.9: "Completion awards effort XP; accuracy affects mastery, not base participation XP").
**FR-17** Parent-facing Quran/Quiz reports must show concepts/skills, not just a raw numeric score (source §21.9: "Parent report shows concepts, not just a score").
**FR-18** Hint system: hints must be progressive/partial (e.g., eliminate one wrong option, reveal the first letter) rather than immediately revealing the full answer; hint usage is tracked as a data point (`hint_count`) feeding the mastery-confidence calculation, not treated as a penalty visible to the child.
**FR-19** Islamic Facts surfaced within or adjacent to Learn-tab content must carry: locale/age-banded text, topic and related-content linkage, primary/secondary source references, scholar approval and version, an explanation, a linked quiz item, and jurisprudential-scope/exclusion notes where relevant (source §21.9 "Islamic Facts").
**FR-20** Adaptive difficulty: lesson difficulty must adjust based on performance (source: Blueprint use case "Get adaptive lesson") — implemented via the mastery-score/skill-state model, not a separate disconnected difficulty slider.
**FR-21** Quran content data integrity: Ayah text itself is never editable post-seed (verified-source-seeded once); only translations, tafseer notes, and learning metadata are versioned/editable, each requiring scholar sign-off before publish (source: Admin Quran Management module rules, cross-referenced here as a hard content-integrity constraint this feature's read path must respect).

### Ordered source inventory

### 1.18 Screen Inventory (Complete — Zero Missing)

| # | Screen | Type | Entry Points | Exit Points |
|---|---|---|---|---|
| 1 | Learn Tab Landing / Quran Learning Home (Skill Tree Map) | Primary | Bottom nav "Learn" tab, Home "Continue Learning" | Surah Learning, Arabic Letters, Tajweed, Quran Game modes |
| 2 | Placement Check (first-time) | Screen | Quran Learning Home, first visit | Skill Tree (pre-populated states) |
| 3 | Mode Selector Sheet | Modal | Quran Learning Home | Specific game mode screen |
| 4 | Surah Learning | Primary | Skill Tree node tap | Recitation Recorder, Dua Learning (A.6), back to Skill Tree |
| 5 | Recitation Recorder Overlay | Component (in Surah Learning) | "Record" action | Feedback screen / Listen-only fallback |
| 6 | AI Pronunciation Feedback Screen | Screen variant | Recorder submission | Mark-practiced action, Retry |
| 7 | Listen-Only Self-Assessment Screen | Screen variant | Mic disabled/denied path | Mark-practiced action |
| 8 | Arabic Letters — Hear & Match | Screen | Skill Tree (letter node) | Tracing screen |
| 9 | Arabic Letters — Tracing | Screen | Hear & Match | Word-context screen |
| 10 | Arabic Letters — Word Context | Screen | Tracing | Skill Tree (progress update) |
| 11 | Arabic Letters — Word-Building (sound tiles) | Screen (game mode) | Mode Selector | Skill Tree |
| 12 | Tajweed — Rule Introduction | Screen | Skill Tree (Tajweed node) | Listen step |
| 13 | Tajweed — Listen (normal/slow) | Screen | Rule Introduction | Identification step |
| 14 | Tajweed — Rule Identification Exercise | Screen | Listen step | Optional Record / Assessment |
| 15 | Tajweed — Assessment | Screen | Identification (or Record) | Skill Tree (progress update) |
| 16 | Quran Game — Ayah Ordering | Screen | Mode Selector | Skill Tree |
| 17 | Quran Game — Listen & Select Matching Ayah | Screen | Mode Selector | Skill Tree |
| 18 | Quran Game — Missing Word | Screen | Mode Selector | Skill Tree |
| 19 | Quran Game — Surah Theme Matching | Screen | Mode Selector | Skill Tree |
| 20 | Quran Game — Recitation Echo | Screen | Mode Selector | AI Feedback / Listen-only fallback |
| 21 | Quran Game — Progressive Memorization Reveal | Screen | Mode Selector | Skill Tree |
| 22 | Daily Quiz (Learn-tab instance) | Screen (shared engine, A.8) | Skill Tree, Home Daily Quiz widget | Quiz Results |
| 23 | Quiz Per-Answer Explanation Overlay | Component (in Quiz) | Each answer submission | Next question |
| 24 | Quiz Retry Set (mistakes) | Screen | Quiz Results (if mistakes made) | Quiz Results (updated) |
| 25 | Quiz Results / Effort XP Reveal | Screen | Quiz completion | Skill Tree / Home |
| 26 | "Needs Refresh" Gentle Review Prompt | Component | Skill Tree, due-for-review node | Review session (routes to relevant node type) |
| 27 | Hint Overlay (progressive hint) | Component (cross-cutting, in any exercise) | "Hint" control | Resumes exercise |
| 28 | Islamic Fact Detail (Learn-tab linked) | Screen | Linked from quiz/lesson content | Related Quiz item / back |
| 29 | Mastery Badge/Node-Unlock Celebration | Modal | Skill Tree, threshold crossed | Dismiss → Skill Tree |
| 30 | Parent Quran/Arabic Progress Report | Screen (Parent Area) | Parent Dashboard → Child Progress → Learning | Concept Detail Drill-in |
| 31 | Parent Progress Report — Concept Detail | Screen (Parent Area) | Progress Report list | Back |
| 32 | Parent AI/Microphone Permission Toggle (per child) | Screen (Parent Area, cross-ref C.23) | Parent Controls | Saves setting |
| 33 | Microphone Permission Rationale / One-Time Explainer | Modal | First recording attempt | Dismiss → proceeds per permission outcome |

### Exact mobile UX and behavior sources

### 1.9 Acceptance Criteria

- Given a child opens Quran Learning Home for the first time, when the skill tree renders, then a placement-check option is offered before defaulting them into Surah 1 from scratch (respecting prior knowledge where determinable).
- Given a skill node is `Locked`, when the child taps it, then the specific prerequisite/unlock condition is shown, not a generic lock icon.
- Given a parent has disabled microphone/AI features for a child, when that child opens Surah Learning or Tajweed practice, then no microphone-recording UI is rendered anywhere in the flow — listen-only/self-assess paths are the only options presented.
- Given an AI pronunciation feedback confidence score falls below the configured threshold, when feedback is generated, then the system falls back to the "compare with recorded reference" self-assessment mode instead of presenting an uncertain score as authoritative.
- Given a child completes a Daily Quiz with 1 out of 5 correct, when results are shown, then participation/effort XP is still awarded, paired with supportive retry language and a simpler next recommendation — never a zero-reward outcome.
- Given a child's recitation attempt is processed by the AI Pronunciation Service, when feedback is returned, then the language used is strictly coaching-style (e.g., "try again, listen for the heavy sound") and never implies religious acceptance/rejection — verified via an automated content-safety check on the feedback-template library (analogous to A.2's billing-content audit pattern).
- Given a child has not practiced a previously-mastered skill in a configured decay window, when they open Quran Learning Home, then that node shows `Needs Refresh` with a gentle, non-shaming "let's review this together" framing.
- Given a parent opens the Quran Progress Report, when it renders, then it lists mastered/in-progress concepts and consistency trends — not merely a percentage score with no context.

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

### 1.16 User Flow (Narrative)

Child opens Learn tab → Quran Learning Home (skill-tree map + mode selector) → taps a Ready/Learning node → routes to Surah Learning (verse-by-verse practice) or a Quran Game mode or Arabic Letters lesson or Tajweed module, depending on node type → practices via listen/repeat/(optionally record) → receives coaching feedback (AI or self-assessment) → marks progress → mastery score updates → if threshold met, node transitions to Mastered and dependent nodes unlock → child may then take the Daily Quiz (mixing this and prior content) → quiz completion awards effort XP, updates mastery, surfaces a parent-report-visible concept summary.

### 2.1 Learn-Specific Design System Extensions

- **Quranic Arabic Typography:** A distinct, more formal Naskh/Uthmani-style typeface (separate from the general-UI Arabic font used for menus/labels per A.1) is used specifically for ayah text, with correct diacritic (tashkeel) rendering verified across all supported devices/OS versions — this is a content-integrity requirement, not a stylistic preference.
- **Skill Tree Visual Language:** Node states map to distinct, non-color-only visual treatments: Locked (greyed, padlock icon), Ready (outlined, gentle pulse), Learning (partially filled progress ring), Practicing (filled ring, no checkmark yet), Mastered (filled gold ring + checkmark), Needs Refresh (filled ring + small gentle "refresh" icon, warm amber not alarming red).
- **Pronunciation Feedback Visual Language:** Feedback is presented via supportive iconography (e.g., a gentle upward arrow for "getting closer," a star-sparkle for "great job on this part") — explicitly avoiding red X / green check binary-correctness imagery for recitation specifically (distinct from the binary-correct UI used in non-religious quiz contexts elsewhere), to reinforce the "coaching, not judgment" principle visually as well as textually.
- **Hint Button:** Small, secondary-styled, always visibly present but never pulsing/highlighted in a way that pressures use.

### 2.2 Screen-Level Design Requirements (Key Screens)

#### Screen: Quran Learning Home (Skill Tree Map)

- **Purpose:** Orient the child within their overall learning journey and let them choose what to practice.
- **Components:** Scrollable/zoomable tree or path visualization of skill nodes grouped by Surah/topic, mode-selector entry point, mastery summary header (e.g., "12 skills mastered"), placement-check re-offer (for returning low-activity users, subtly, not naggy).
- **States:** Loading (skeleton tree), Default, Error (cached fallback per §1.11), First-time (placement-check prominent).
- **Accessibility:** Tree navigable linearly via screen reader (a logical reading order independent of the visual spatial layout, with each node's state announced).
- **Responsive Rules:** Tree layout reflows for tablet (wider node spacing) without changing the underlying logical structure.

#### Screen: Surah Learning

- **Purpose:** Core verse-by-verse practice experience.
- **Components:** Ayah list (Quranic-typography Arabic + transliteration-optional + translation toggle), Tajweed-rule inline highlight markers, per-ayah audio play/slow-play controls, record button (conditional on permission state), hint control, "mark practiced" action.
- **States:** Default, Recording-active, AI-processing ("Listening... checking"), Feedback-shown, Listen-only-mode, Error (audio load failure).
- **Accessibility:** Translation toggle and transliteration visibility independently controllable, never forced on (per source: "transliteration is optional and controlled by lesson design, not always shown" — here extended to also remain a user-accessible toggle where lesson design permits).

#### Screen: AI Pronunciation Feedback Screen

- **Purpose:** Deliver coaching feedback without implying religious judgment.
- **Components:** Waveform-style visual (decorative, not data-precise) of the attempt, 1-2 specific, constructive coaching phrases (e.g., "Nice! Try holding this letter a bit longer next time"), a "Try Again" and a "Continue" action, never a numeric score displayed to the child (numeric/confidence data exists only in the backend mastery model, never shown raw to a child).
- **States:** High-confidence-positive, High-confidence-needs-practice, Low-confidence-fallback (routes to reference-comparison instead of this screen entirely).

### 2.3 Tab Structure

Learn is Tab 2 of 5 (Home / **Learn** / Stories / Rewards / Profile). Click mapping:

| Click Target | Destination | API Called | Analytics Event | Permission Check | Error Handling |
|---|---|---|---|---|---|
| Skill node (unlocked) | Relevant practice screen | `GET /v1/learning/nodes/{id}` | `skill_node_started` | None beyond entitlement (most Learn content free-tier per source) | Cached fallback |
| Skill node (locked) | Inline unlock-condition display | None | `skill_node_locked_tapped` | None | N/A |
| Record button | Recitation Recorder | `POST /v1/learning/attempts` | `recitation_record_submitted` | Mic OS permission + parent AI toggle | Falls back to listen-only |
| Hint control | Hint Overlay | `GET /v1/learning/hints/{question_id}` (shared with A.5) | `hint_requested` | None | Falls back to generic encouragement text if hint service fails |
| Daily Quiz widget/entry | Daily Quiz screen | `GET /v1/quizzes/daily?context=learn` | `daily_quiz_started` | None | Graceful unavailable message |

### 2.4 Wireframe Description (Composite)

Skill Tree: a vertically-scrolling, organically-curved path (not a rigid grid) connecting nodes in learning-sequence order, with horizontal branching for parallel tracks (e.g., Arabic Letters track running alongside the Quran/Surah track), consistent with a "journey map" metaphor rather than a flat menu list. Practice screens (Surah Learning, Tajweed, Letters) follow a consistent single-column, single-primary-action wireframe pattern similar to A.1's onboarding philosophy, appropriate given the focused, one-task-at-a-time nature of learning exercises.

### 2.5 Screen Image Generation Prompts

**Screen: Quran Learning Home (Skill Tree Map)**
- *Prompt 1 (English):* "Mobile app skill-tree/learning-path map UI mockup for a children's Islamic education app. Warm off-white background. A gently curving illustrated path winding vertically up the screen, connecting circular node icons representing learning skills — some nodes shown filled and glowing gold with a small checkmark (mastered), some partially filled with a teal progress ring (in progress), and some greyed out with a small padlock icon (locked). Small decorative Islamic geometric pattern flourishes along the path. A small mastery summary chip near the top reading a simple stat. Warm, encouraging, game-like but respectful and calm aesthetic, rounded shapes throughout, no realistic human faces, bottom navigation bar visible."
- *Prompt 2 (Arabic RTL):* "نفس واجهة خريطة مسار التعلم/شجرة المهارات لتطبيق تعليم إسلامي للأطفال، بتخطيط من اليمين إلى اليسار. خلفية بيج فاتح دافئ. مسار رسومي منحني بلطف يتصاعد عموديًا على الشاشة، يربط بين أيقونات عقد دائرية تمثل المهارات التعليمية — بعضها معبأ ومتوهج بالذهبي مع علامة صح صغيرة (مكتسبة بالكامل)، وبعضها معبأ جزئيًا بحلقة تقدم فيروزية (قيد التعلم)، وبعضها رمادي اللون مع أيقونة قفل صغيرة (مقفلة). زخارف هندسية إسلامية صغيرة تزين المسار. شريحة ملخص صغيرة قريبة من الأعلى تعرض إحصائية بسيطة. طابع مشجع وشبيه باللعبة لكن محترم وهادئ، أشكال مستديرة في كل مكان، بدون وجوه بشرية واقعية، شريط تنقل سفلي ظاهر."

**Screen: Surah Learning (Ayah Practice)**
- *Prompt 1 (English):* "Mobile app verse-by-verse Quran practice screen UI mockup for children. Clean warm off-white background. A scrollable list of rounded card rows, each showing elegant Arabic Quranic-style calligraphy text at the top of the card, a smaller transliteration line beneath in italic Latin font, and a translation line beneath that in regular font, with a small play-button icon and a slower-speed icon to the side of each card. One card highlighted with a soft teal border indicating the active verse, showing a small record-microphone icon button and a small lightbulb hint icon button beneath it. Respectful, calm, focused educational aesthetic, generous spacing, soft shadows, warm gold accent details, no realistic human faces."
- *Prompt 2 (Arabic RTL):* "نفس شاشة ممارسة القرآن آية بآية للأطفال، بتخطيط من اليمين إلى اليسار بالكامل. خلفية بيج فاتح دافئ ونظيفة. قائمة قابلة للتمرير من صفوف بطاقات مستديرة الزوايا، كل بطاقة تعرض نصًا قرآنيًا بخط عربي أنيق في الأعلى، وسطرًا أصغر للنقل الصوتي بخط لاتيني مائل الطابع أسفله، وسطر ترجمة بخط عادي أسفل ذلك، مع أيقونة زر تشغيل صغيرة وأيقونة سرعة أبطأ بجانب كل بطاقة. بطاقة واحدة مميزة بحد فيروزي ناعم تشير إلى الآية النشطة، تعرض زر أيقونة ميكروفون تسجيل صغير وزر أيقونة لمبة تلميح صغيرة أسفلها. طابع تعليمي محترم وهادئ ومركّز، تباعد كبير، ظلال خفيفة، تفاصيل ذهبية دافئة، بدون وجوه بشرية واقعية."

**Screen: AI Pronunciation Feedback**
- *Prompt 1 (English):* "Mobile app feedback screen UI mockup for a children's pronunciation-practice app, deliberately avoiding any pass/fail or right/wrong iconography. Warm off-white background. A decorative soft wave-pattern illustration in teal representing a sound recording, centered. Below it, a friendly short text message in a rounded speech-bubble shape giving constructive coaching ('Nice try! Let's hold this sound a little longer next time'), with a small upward-trending sparkle icon (not a checkmark or X) suggesting encouraging progress. Two rounded buttons below: 'Try Again' (outlined, secondary style) and 'Continue' (filled, warm gold, primary style). No numeric scores or percentages visible anywhere, calm and encouraging tone, no realistic human faces."
- *Prompt 2 (Arabic RTL):* "نفس شاشة التغذية الراجعة لتطبيق ممارسة النطق للأطفال، بتخطيط من اليمين إلى اليسار، مع تجنب متعمد لأي رموز نجاح/فشل أو صحيح/خاطئ. خلفية بيج فاتح دافئ. رسمة زخرفية لنمط موجي ناعم بلون فيروزي تمثل تسجيلًا صوتيًا، في المنتصف. تحتها رسالة نصية قصيرة وودودة بشكل فقاعة كلام مستديرة تقدم توجيهًا بنّاءً ('محاولة جيدة! لنحافظ على هذا الصوت لفترة أطول في المرة القادمة')، مع أيقونة بريق صاعد صغيرة (ليست علامة صح أو خطأ) تشير إلى تقدم مشجع. زرّان مستديران أسفلها: 'حاول مرة أخرى' (بنمط ثانوي محدد الحواف) و'استمرار' (بنمط أساسي ذهبي دافئ معبأ). بدون أي نقاط أو نسب ظاهرة في أي مكان، طابع هادئ ومشجع، بدون وجوه بشرية واقعية."

*(Remaining screens — Arabic Letters Tracing, Tajweed Rule Introduction, Quran Game modes, Needs Refresh prompt, Hint Overlay, Parent Progress Report — follow the same two-prompt EN/AR template using these tokens; full set available on request.)*

---

### 6.1 Technical Requirements
Kotlin, Jetpack Compose, MVVM, Clean Architecture, module `:feature:learn`, depends on `:core:audio-recording` (new shared module for mic capture, separate from `:core:media-player` used for playback in A.3/A.4), `:core:design-system`, `:core:network`, `:core:offline-cache`.

### 6.2 Screen Mapping
Each screen in §1.18 maps to a Composable; `:core:audio-recording` provides a `RecitationRecorder` abstraction wrapping `MediaRecorder`/`AudioRecord` with a strict in-memory-buffer-only mode (no file-write path exposed at all from this module's public API, architecturally preventing accidental raw-audio persistence on-device too, not just server-side).

### 6.3 Navigation Flow
Standard Compose Navigation graph under the Learn tab's nested graph; Skill Tree is the graph's start destination.

### 6.4 State Management
`SkillTreeViewModel` mirrors backend node states client-side for instant UI response, but treats the server as authoritative on every fetch (no client-side mastery computation that could drift from server logic — client only renders states, never computes them). `RecitationViewModel` manages a strict state machine: `Idle → Recording → Uploading → AwaitingFeedback → FeedbackShown(...)`, with the recorded audio buffer explicitly cleared from memory (`null`-ed out, buffer reference dropped) immediately upon receiving the server response, mirroring the backend's zero-retention guarantee on the client side too.

### 6.5 API Mapping
`RecitationRepository.submit()` → `POST /v1/learning/recitation`, sending the in-memory audio buffer directly as a multipart stream without ever writing it to a temp file on device storage (to avoid leaving recoverable audio artifacts in app-local storage even transiently).

### 6.6 Analytics Mapping
`LearnAnalytics` fires `recitation_ai_feedback_shown` with only `confidence_band` (categorical) — the analytics layer must structurally be unable to attach raw audio or transcript data to any event payload (enforced by the event's typed Kotlin data class simply not having a field for it).

### 6.7 Offline Support
Lesson content/audio downloadable per the standard offline pattern; recitation/AI feedback explicitly requires connectivity (client shows a clear "needs internet" state rather than queuing raw audio for later upload, since queuing audio would extend its on-device lifetime in tension with the data-minimization principle — recitation attempts made offline are simply not available until reconnected, with self-assessment offered immediately as the offline alternative).

### 6.8 Deep Linking
`noorheroes://learn/node/{node_id}` for Home "Continue Learning" entry points.

### 6.9 Push Notifications
Landing target for "Quran practice reminder" / "your skill is ready for review" notifications (owned by A.12/A.7 habit-linked reminders) — this feature owns the deep-link destinations only.

### 6.10 Testing Strategy
- Unit: Skill Tree client-side state-rendering logic (render-only, never compute), Recitation state-machine transitions, buffer-clearing verification (memory-leak/retention test asserting the audio buffer reference is nulled post-response).
- UI tests: Listen-only fallback rendering when mic permission/parent-toggle is off; AI Feedback screen never displays a numeric score; Hint Overlay never reveals a full answer at any hint level.
- Integration: full recitation submit → feedback flow with mocked server responses for high-confidence, low-confidence-fallback, and service-error scenarios, verifying identical safe UX for the latter two.
- Privacy-specific instrumented test: record a test audio clip, submit it, and assert (via a file-system/memory scan in the test harness) that no audio file was ever written to any on-device path during the entire flow.

---

### 13.1 Test Plan Summary
Coverage spans: zero-audio-retention guarantee (signature test), parent-toggle server-side enforcement, confidence-gating/fallback correctness, skill-tree state-machine legality, spaced-repetition capping, and all 12 edge cases from §1.10.

### 13.2 Test Cases — Happy Path
1. Child completes Arabic Letter lesson (hear → trace → word-context) across two sessions, achieving mastery only after the second session's correct performance (single-session-mastery is correctly disallowed per FR-7).
2. Child with mic/AI enabled submits a high-confidence recitation → coaching feedback shown, no numeric score visible, mastery updated.
3. Parent disables AI for a child → child's next Surah Learning session shows listen-only mode with zero record-button presence.

### 13.3 Edge Cases
All 12 items from §1.10.

### 13.4 Negative Cases
- Submit a recitation request with the parent toggle explicitly disabled (server-side state) → `403`, and assert via test instrumentation that the inference call was never invoked.
- Attempt to save a Feedback Template containing a blocklisted term via the Admin API directly (bypassing the UI) → rejected server-side, not just client-side.
- Attempt a direct database `UPDATE` on `ayah.arabic_text_immutable` → rejected by the database-layer protection.
- Construct an admin curriculum-graph save that would introduce a prerequisite cycle → rejected with the cycle path shown.
- Simulate 5 simultaneously-due spaced-review nodes for one child → exactly 2 surfaced today (default cap), remainder scheduled for later dates.

### 13.5 Regression Cases
Full Quran & Arabic Learning suite re-run on every release touching `:feature:learn`, `:core:audio-recording`, the Learning Path & Mastery Service, or the AI Pronunciation Coaching Service.

### 13.6 Automation Cases
End-to-end: full skill-node mastery journey across two sessions, recitation submit → feedback flow across high/low/error confidence scenarios, automated file-system-scan privacy test (CI-blocking on every relevant PR), curriculum-graph cycle-detection automated test suite.

---

### Corresponding KMP blueprint requirements

#### `Development_Blueprints/A5_Quran_Arabic_Learning/KMP/01-quran-skill-tree-map.md`

##### 4. Objective
Render a scrollable/zoomable skill-tree map purely from server data (B-01's `GET /v1/learning/paths`), with distinct visual states per node, correct locked-node unlock-condition display, offline/cached fallback, and full accessibility/RTL/localization support.

##### 5. Business Requirements
- FR-1: skill-tree map with mastery indicators, mode selectors, placement-check option for new learners.
- FR-2: node states rendered exactly as `Locked/Ready/Learning/Practicing/Mastered/Needs Refresh`; locked nodes show the specific unlock condition.
- FR-3: progress shown via visual indicators (ring, label) without exposing the raw composite score.
- UX §2.1: node-state visual language — Locked (greyed, padlock), Ready (outlined, pulse), Learning (partial ring), Practicing (filled ring), Mastered (gold ring+check), Needs Refresh (amber ring+icon).
- Acceptance Criteria: first-time child sees placement-check offer before Surah 1 default; locked-node tap shows specific unlock condition.
- Loading State: skeleton node-grid shimmer. Error State: cached last-known tree with "may be slightly out of date" indicator.

##### 11. KMP Requirements
- **Composable**: scrollable/zoomable organically-curved path (not rigid grid) connecting node icons, grouped by Surah/topic, horizontal branching for parallel tracks (Arabic Letters alongside Quran/Surah track).
- **Mastery summary header**: e.g., "12 skills mastered," sourced directly from the response payload's `mastery_summary`.
- **Node visual states**: six distinct, non-color-only treatments per §2.1 design tokens.
- **Locked-node tap**: shows the specific `unlock_condition` text from the response, never a generic lock message.
- **Mode-selector entry point**: opens the Mode Selector Sheet (modal, routes into K-05/K-06/K-07 game/lesson modes).
- **Placement-check re-offer**: prominent for first-time users (zero progress), subtle for returning low-activity users — logic driven by whether `mastery_summary.mastered_count == 0` and no prior placement-check completion flag.
- **`SkillTreeViewModel`**: mirrors backend node states client-side for instant UI response, treats server as authoritative on every fetch — contains NO client-side mastery-score calculation logic whatsoever.
- **Offline/error fallback**: on fetch failure, render the last Room-cached response with a "may be slightly out of date" indicator, never a blank/broken map.
- **Tablet responsive reflow**: wider node spacing, same logical structure — implemented via `WindowSizeClass`-aware layout, consistent with existing responsive patterns in `core-designsystem`.
- **Accessibility**: tree navigable linearly via screen reader in a logical reading order independent of visual spatial layout; each node's state announced via `contentDescription`/semantics.
- **Deep link**: `noorheroes://learn/node/{node_id}` resolves to `LearnRoute.SkillTree(focusNodeId = node_id)` via `core-navigation`'s route parsing, used by Home's "Continue Learning" entry point.

##### 15. Validation
N/A client-side beyond standard null/empty-state handling; all authoritative validation happens server-side (B-01).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Network/API failure | Render last Room-cached skill tree with "may be slightly out of date" indicator |
| Zero cached data + fetch failure (true first-run offline) | Friendly empty/error state, retry action, never a crash |
| `403`/`401` (session issue) | Delegate to app-level session-expiry handling (existing global auth-error interceptor in `core-network`) |

##### 19. Offline First
Downloaded/cached skill-tree data fully viewable offline (read-only); actions requiring connectivity (attempt submission, recitation) are gated at the destination screens (K-03/K-05/K-06/K-07), not here.

##### 21. Localization
Surah/topic/node labels resolved via the existing `core-common/localization` reactive provider; supports English, Hindi, Arabic, Urdu per app-wide requirement.

##### 22. RTL
Full RTL layout support for Arabic locale — the organically-curved path direction, node ordering, and text alignment must mirror correctly; verified against the app's existing RTL-support patterns in `core-designsystem`.

##### 25. Security
No sensitive data rendered on this screen (no audio, no raw scores). Standard authenticated-session data exposure only.

##### 27. Testing
- Unit: `SkillTreeViewModel` state mapping is render-only (assert no mastery-score computation occurs client-side — inspect that the ViewModel never derives a `state` value, only passes through the server's `state` field).
- Unit: locked-node display logic always surfaces the server-provided `unlock_condition`, never a hardcoded generic message.
- UI test: tablet reflow renders wider node spacing without altering logical node order.
- UI test: screen-reader traversal order is linear/logical, independent of visual spatial layout.
- Integration: offline/error fallback renders cached data with the correct "may be slightly out of date" indicator.

##### 31. Final Verification Checklist
- [ ] Zero client-side mastery-score computation anywhere in `SkillTreeViewModel` (render-only verified)
- [ ] All six node states render with distinct, non-color-only visual treatments
- [ ] Locked-node tap always shows the specific server-provided unlock condition
- [ ] Offline/error fallback shows cached data with "may be slightly out of date" indicator, never blank
- [ ] Tablet reflow preserves logical node order
- [ ] Screen-reader traversal is linear and logical
- [ ] RTL layout verified for Arabic locale
- [ ] Deep link `noorheroes://learn/node/{node_id}` resolves correctly
- [ ] Uses Koin/Ktor/Room per actual project architecture (not Hilt/Retrofit as in the earlier PRD draft)
- [ ] Full test suite green in CI

#### `Development_Blueprints/A5_Quran_Arabic_Learning/KMP/02-placement-check-flow.md`

##### 4. Objective
Present the placement-check question flow, submit responses to B-02, and route the resulting recommended/provisional skill-tree state back into K-01 — always offering an explicit "start from the beginning" alternative.

##### 5. Business Requirements
- Acceptance Criteria: first-time skill-tree render offers a placement-check option before defaulting into Surah 1.
- Edge Case 9: Tajweed-prerequisite provisional handling must be visibly reflected (not silently skipped) if the flow surfaces any interim confirmation.

##### 11. KMP Requirements
- **Presentation**: question-by-question flow (reusing shared quiz-question components where they exist), with a clearly visible "start from the beginning" alternative at every step, never forcing completion.
- **Submission**: `PlacementCheckViewModel` collects responses, submits via `SubmitPlacementCheckUseCase`, and on success invalidates/refreshes K-01's cached skill-tree state so the returned `recommended_starting_nodes`/`provisional_states` are reflected immediately on return to the Skill Tree screen.
- **Edge Case 9 UX**: if the response indicates Tajweed-track nodes were marked provisional, no special interstitial is required here (the state itself renders correctly on K-01 as `ready` with a visible "confirm your understanding" affordance or `needs_refresh` scheduling) — this screen's responsibility ends at correct submission and navigation back to the Skill Tree.
- **Failure handling**: submission failure shows a non-blocking retry option; the "start from beginning" alternative remains available regardless of submission outcome.

##### 15. Validation
Client-side: ensure all required questions answered before enabling submit; server remains authoritative (B-02 validates payload completeness).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Submission API failure | Non-blocking retry, "start from beginning" always available |
| Duplicate-submission `409` from B-02 | Treat as success — navigate to Skill Tree using the returned prior result |

##### 19. Offline First
Placement check requires connectivity to submit; if offline, show a clear "needs internet to place you correctly" message with the "start from beginning" alternative immediately available (consistent with the app's stance on connectivity-gated AI/scoring flows).

##### 21. Localization
Question/answer text localized via existing `core-common/localization` provider.

##### 22. RTL
Full RTL support for question flow layout.

##### 25. Security
No sensitive data; standard authenticated-session flow.

##### 27. Testing
- Unit: `PlacementCheckViewModel` submission flow (success, failure-retry, duplicate-409-treated-as-success).
- UI test: "start from beginning" alternative always visible/tappable regardless of flow state.
- Integration: successful submission triggers K-01's skill-tree cache refresh.

##### 31. Final Verification Checklist
- [ ] "Start from beginning" alternative visible and functional at every step
- [ ] Successful submission immediately reflected in K-01's Skill Tree on return
- [ ] Duplicate-submission `409` treated as success, not an error
- [ ] Offline state shows a clear connectivity-needed message with the beginning-alternative still available
- [ ] RTL/localization verified
- [ ] Full test suite green in CI

#### `Development_Blueprints/A5_Quran_Arabic_Learning/KMP/03-surah-learning-verse-practice.md`

##### 4. Objective
Render the ayah-by-ayah practice screen with Quranic-typography Arabic text, translation/transliteration toggles, inline Tajweed highlighting, audio playback, and a conditional record entry point — with correct offline playback and graceful audio-failure fallback.

##### 5. Business Requirements
- FR-8: ayah-by-ayah list with audio, translation toggle, inline Tajweed-rule highlighting, recitation recorder; actions: listen, repeat, record, hint, mark practiced.
- FR-9: mic-denied/parent-disabled state falls back to listen-only, not a dead end.
- NFR: audio playback start p95 < 600ms for cached/downloaded ayah audio.
- NFR: Quranic Arabic typography — distinct Naskh/Uthmani-style typeface, correct diacritic (tashkeel) rendering verified across devices/OS versions.
- Error Handling: ayah audio load failure retries with backoff, falls back to lower-bitrate/alternate CDN source before a hard error.

##### 11. KMP Requirements
- **Ayah list**: Quranic-typography Arabic (Naskh/Uthmani), optional transliteration, translation toggle — both independently controllable, never forced on.
- **Inline Tajweed highlighting**: rendered as inline markers within ayah text per content-service-provided rule spans.
- **Audio controls**: play + slow-play per ayah via `core-kmp-player`; retry-with-backoff on load failure, falls back to alternate CDN/bitrate before a hard error.
- **Record entry point**: conditionally rendered based on BOTH RECORD_AUDIO permission AND server-confirmed parent AI-toggle (delegates actual recording UI/logic entirely to K-04's `RecitationRecorder`/`RecitationViewModel` — this screen only decides whether to show the entry point and routes into K-04's flow).
- **Hint control**: routes to K-10's Hint Overlay.
- **"Mark practiced" action**: submits via B-03 (or a dedicated lightweight progress-marker call if `attempt_type` doesn't cleanly cover ayah-marking — confirm exact mechanism against B-03's contract before implementation).
- **States**: Default, Recording-active, AI-processing, Feedback-shown, Listen-only-mode, Error (audio load failure) — the Recording/AI-processing/Feedback states are owned by K-04's `RecitationViewModel`, this screen's `SurahLearningViewModel` observes/delegates to it rather than duplicating state.
- **Offline**: downloaded ayah audio/lesson content fully usable offline for listen/repeat/trace flows.

##### 15. Validation
N/A client-side beyond standard empty/error-state handling.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Ayah audio load failure | Retry with backoff, fallback to alternate CDN/bitrate, then hard error only as last resort |
| Mic permission or parent toggle false | Record entry point not rendered at all; screen shows Listen-Only mode instead (delegates to K-04's Listen-Only screen variant) |
| "Mark practiced" submission failure | Non-blocking retry, does not block continued practice |

##### 19. Offline First
Downloaded ayah audio/lesson content fully usable offline (listen/repeat/trace); recitation coaching requires connectivity (owned by K-04) — offline recitation attempts are not queued (per K-04's data-minimization design), self-assessment offered immediately as the offline alternative.

##### 21. Localization
Translation/transliteration text localized via `core-common/localization`; both remain user-accessible, independently toggleable, never forced on (per source guidance extended to a user-accessible toggle where lesson design permits).

##### 22. RTL
Full RTL rendering with correct diacritic (tashkeel) display verified across devices/OS versions — this is called out in the PRD as the single most typography-critical screen in the app; dedicated device-matrix visual-regression testing recommended (cross-ref QA requirements).

##### 25. Security
No sensitive data beyond what K-04's recitation flow already governs (this screen itself doesn't touch audio recording).

##### 27. Testing
- Unit: translation/transliteration toggle independence.
- Unit: record-entry-point visibility logic (permission AND parent-toggle both required).
- UI test: Tajweed inline highlighting renders correctly against sample marked-up ayah text.
- Integration: audio-load-failure retry/fallback sequence.
- Integration: offline playback of downloaded content succeeds without network.

##### 31. Final Verification Checklist
- [ ] Translation/transliteration toggles independently controllable, never forced on
- [ ] Record entry point rendered only when BOTH permission and parent toggle are true
- [ ] Ayah audio load failure retries with backoff and CDN/bitrate fallback before hard error
- [ ] Offline playback works for downloaded content
- [ ] Diacritic (tashkeel) rendering verified correct across device/OS matrix
- [ ] No duplicate playback engine built (reuses `core-kmp-player`)
- [ ] No duplicate recording logic built (delegates fully to K-04)
- [ ] Full test suite green in CI

#### `Development_Blueprints/A5_Quran_Arabic_Learning/KMP/04-recitation-recorder-zero-retention-capture.md`

##### 4. Objective
Build a new `core-audio-recording` module exposing an API structurally incapable of file-based recording, and a `RecitationViewModel` state machine that explicitly nulls its audio buffer reference immediately on reaching a terminal state — mirroring B-04's server-side zero-retention guarantee on-device.

##### 5. Business Requirements
- FR-9: mic-denied/parent-disabled state falls back to listen-only, not a dead end.
- FR-10: feedback never implies religious/spiritual validity — never a numeric score shown to the child.
- FR-11: raw audio not retained after processing by default.
- FR-12: low-confidence results fall back to reference-comparison self-assessment.
- FR-13: parent per-child mic/AI disable — no UI path bypasses it.
- Edge Case 2: parent disabling mid-session must gracefully exit to listen-only on next app-state check, never a dangling broken record control.
- Edge Case 5: no microphone hardware → recitation UI hidden entirely (not shown-disabled), via device-capability detection at app start.
- Edge Case 10: network-drop mid-upload retry allowed, but raw audio still discarded post-processing.
- §7 Android AI Code-Generation Prompt: the full set of hard privacy requirements for this module (adapted below to the project's actual Koin/Ktor/Room-based KMP architecture rather than the prompt's original Hilt/Retrofit assumptions).

##### 11. KMP Requirements
- **`RecitationRecorder` public API**: ONLY `start()`, `stop(): ByteArray`, and a streaming-upload helper — structurally impossible for any caller to request file-based recording, since no method in the public API accepts or returns a file path.
- **Audio capture**: directly into an in-memory buffer (`AudioRecord`/platform-equivalent with a `ByteArray`/`ByteBuffer` sink) — never a file-writing recorder API.
- **Upload**: streamed to the server as a multipart request body directly from memory via `RecitationApi`, never written to a temp file on device storage at any point in the lifecycle, even transiently.
- **`RecitationViewModel` state machine**: `Idle → Recording → Uploading → AwaitingFeedback → FeedbackShown(confidenceBand, templateText) | FallbackToReference | Error`. On entering `FeedbackShown`, `FallbackToReference`, or `Error`, explicitly set the held audio `ByteArray` reference to `null` in the same state-transition code path — not relying on scope-exit alone.
- **Record-button gating**: visible only when BOTH RECORD_AUDIO runtime permission is granted AND a server-confirmed parent AI-toggle value (fetched via K-13's `ParentalControlsRepository`) is true; if either is false/denied, render `ListenOnlySelfAssessmentScreen` instead, with zero record-button nodes anywhere in the composable tree.
- **Device-capability detection (Edge Case 5)**: at app start, detect absence of microphone hardware and hide the recitation-recording UI entirely (identical UX to parent-disabled), not shown-disabled.
- **`AiPronunciationFeedbackScreen`**: waveform-style decorative visual (not data-precise), 1-2 categorical coaching-copy strings keyed by `confidence_band`, "Try Again"/"Continue" actions — NEVER renders a numeric score, percent, or confidence value as visible text anywhere on the screen.
- **`ListenOnlySelfAssessmentScreen`**: rendered for mic-denied/parent-disabled/no-hardware/low-confidence-fallback cases — a single consistent screen variant reused across all these triggers.
- **`MicPermissionRationaleModal`**: one-time explainer, non-repeated nagging beyond the platform-standard one-time re-prompt affordance.
- **Mid-session parent-disable (Edge Case 2)**: on next app-state check (e.g., process resume, or a periodic toggle re-check while the recorder screen is active), gracefully exit any in-progress recording UI to listen-only mode — never leave a dangling record button that silently fails.
- **Offline (Edge Case per §6.7)**: recitation/AI feedback explicitly requires connectivity; client shows a clear "needs internet" state rather than queuing raw audio locally (queuing would extend on-device audio lifetime, in tension with data minimization) — self-assessment offered immediately as the offline alternative.
- **Hint control**: routes to K-10, available during Surah Learning's recitation flow same as any other exercise.

##### 15. Validation
N/A beyond standard audio-format/size sanity checks before upload (delegated to the platform capture API's own constraints).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Parent disables mid-session (Edge Case 2) | Graceful exit to listen-only on next app-state check, no dangling broken control |
| Network drop mid-upload (Edge Case 10) | Local retry of the in-memory buffer only until server ack; raw audio still discarded (buffer nulled) post-processing regardless of retry outcome — no extended in-memory retention loophole |
| Inference low-confidence/error from B-04 | Route to `FallbackToReference`/`ListenOnlySelfAssessmentScreen`, not a degraded feedback screen |
| No microphone hardware (Edge Case 5) | Recitation UI hidden entirely at app start, identical UX to parent-disabled |
| Offline | Clear "needs internet" state, no local audio queuing |

##### 19. Offline First
Recitation explicitly requires connectivity by design (see §11) — this is a deliberate exception to the app's general offline-first posture, justified by the data-minimization principle (queuing audio would extend its on-device lifetime).

##### 21. Localization
Coaching-phrase copy (`templateText`) is server-supplied per the child's locale (via B-10's `locale`-scoped templates) — the client renders whatever text is returned, never synthesizes or translates it locally.

##### 22. RTL
Full RTL layout for Arabic/Urdu coaching-feedback copy and screen layout.

##### 25. Security
This module's restricted public API (no file-path-accepting methods) is itself a security control, not just engineering convenience — it makes a class of privacy bugs structurally impossible rather than merely discouraged, per the PRD's explicit framing. This is the client-side mirror of B-04's server-side zero-retention guarantee, and both must be verified by CI-blocking automated tests (Task 09 below), not code-review checklists alone.

##### 27. Testing
- **Unit**: weak-reference test — hold a `WeakReference` to the audio `ByteArray`, trigger the transition to `FeedbackShown`/`Error`/`FallbackToReference`, force GC, assert the buffer becomes garbage-collectable shortly after (proves the explicit-null discipline, not just scope-exit reliance).
- **UI test**: scan the full composable tree when permission or parent-toggle is false — assert zero nodes with a "record" content-description/semantics tag exist anywhere.
- **UI test**: scan all text nodes on `AiPronunciationFeedbackScreen` — assert none match a regex for a standalone number followed by `%` or a decimal between 0 and 1 (proves no numeric score ever renders).
- **Instrumented test (CI-blocking, the signature privacy guarantee)**: start a recording, stop it (obtain a `ByteArray`), submit via a mocked repository, then use a file-system scanner walking the app's full sandboxed storage directory tree, asserting ZERO new files were created during the entire test run.
- **Integration**: full submit→feedback flow with mocked server responses for high-confidence, low-confidence-fallback, and service-error scenarios, verifying identical safe UX for the latter two (same `ListenOnlySelfAssessmentScreen`/`FallbackToReference` path).
- **Integration**: Edge Case 2 — simulated mid-session parent-disable triggers graceful exit to listen-only on the next app-state check.

##### 31. Final Verification Checklist
- [ ] `RecitationRecorder`'s public API has no method accepting or returning a file path
- [ ] Audio captured directly to an in-memory buffer, never `MediaRecorder`-to-file
- [ ] Audio streamed to server directly from memory, never via an intermediate temp file
- [ ] Audio `ByteArray` reference explicitly nulled in the same code path as every terminal-state transition
- [ ] Weak-reference test confirms buffer becomes garbage-collectable shortly after terminal state
- [ ] Instrumented file-system-scan test confirms ZERO new files created during a full record→submit flow (CI-blocking)
- [ ] Record button rendered only when BOTH permission AND parent toggle are true; zero record-content-description nodes otherwise
- [ ] No numeric score/percent/confidence value ever rendered as visible text
- [ ] No microphone hardware → recitation UI hidden entirely, not shown-disabled
- [ ] Mid-session parent-disable gracefully exits to listen-only, no dangling broken control
- [ ] `core-audio-recording` has zero dependency on `core-database`/Room
- [ ] Analytics event data classes structurally cannot carry audio/transcript/raw-confidence data
- [ ] Uses Koin/Ktor per actual project architecture (not Hilt/Retrofit as in the earlier PRD draft)
- [ ] Full test suite green in CI, instrumented privacy test is a mandatory CI gate

#### `Development_Blueprints/A5_Quran_Arabic_Learning/KMP/05-arabic-letters-learning-flow.md`

##### 4. Objective
Render the four Arabic Letters exercise screens (Hear & Match, Tracing, Word Context, Word-Building) in sequence, with a non-gesture-dependent tracing alternative, submitting each attempt to B-03 and never allowing single-session mastery.

##### 5. Business Requirements
- FR-6: Hear-and-match, tracing, isolated/initial/medial/final form matching, harakah sound pairing, find-the-letter-in-word, build-a-word-from-sound-tiles — with spaced review scheduling.
- FR-7: play phoneme → select 1-of-4 → trace correct shape → letter in familiar word → scheduled for spaced review; mastery requires correct performance across different question forms and more than one session.
- NFR/Accessibility: tracing exercises must have a non-gesture-dependent alternative (multiple-choice shape matching) for assistive-input users.

##### 11. KMP Requirements
- **Hear & Match**: phoneme playback via `core-kmp-player`, 1-of-4 letter selection UI.
- **Tracing**: gesture-based tracing canvas PLUS a non-gesture-dependent multiple-choice shape-matching alternative, toggleable/auto-offered for assistive-input users (detected via platform accessibility service state where feasible, or a persistent user-accessible toggle).
- **Word Context**: renders the letter within a familiar, content-team-approved word.
- **Word-Building**: sound-tile drag/tap-to-build game mode.
- **Sequencing**: hear-and-match → trace → word-context, per FR-7, with each step's attempt submitted individually to B-03 (not batched), so B-03's multi-session mastery enforcement operates on real historical data.
- **Isolated/initial/medial/final letter-form matching, harakah sound pairing, find-the-letter-in-word**: implemented as variant question types within Hear & Match/Word Context screens, driven by content-service question metadata, not hardcoded per-letter logic.
- **Spaced review**: no client-side scheduling logic — entirely server-driven via B-06, this flow just submits attempts.

##### 15. Validation
N/A client-side beyond standard input handling; server-side (B-03) is authoritative on correctness evaluation.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Audio playback failure | Retry/fallback via `core-kmp-player`'s existing error handling |
| Attempt submission failure | Non-blocking retry, does not block continued practice |
| Tracing gesture input unavailable/unreliable | Non-gesture alternative always accessible, never a dead end |

##### 19. Offline First
Lesson content/audio downloadable and usable offline; attempt submission requires connectivity (queued for sync on reconnect per the app's standard offline-write pattern via `core-data`'s `SyncQueue`, consistent with other non-recitation attempt types).

##### 21. Localization
All instructional copy and content localized via `core-common/localization`.

##### 22. RTL
Full RTL layout; letter-shape rendering itself is inherently script-correct (Arabic letterforms), UI chrome around it mirrors for RTL locales.

##### 25. Security
No sensitive data; standard authenticated-session flow.

##### 27. Testing
- Unit: sequencing logic (hear-and-match → trace → word-context) submits each step independently.
- UI test: non-gesture tracing alternative is always reachable and functionally equivalent.
- Integration: offline attempt submission queues via `SyncQueue` and syncs on reconnect.

##### 31. Final Verification Checklist
- [ ] Non-gesture tracing alternative always available and functionally equivalent
- [ ] Each exercise step submits its own attempt (no batching that would defeat multi-session mastery tracking)
- [ ] Offline attempt submission queues and syncs correctly
- [ ] RTL/localization verified
- [ ] Full test suite green in CI

#### `Development_Blueprints/A5_Quran_Arabic_Learning/KMP/06-tajweed-learning-flow.md`

##### 4. Objective
Render the sequential Tajweed flow (Rule Introduction → Listen → Identification → optional Record → Assessment), routing the optional record step through K-04's shared Recitation Recorder rather than duplicating recording logic.

##### 5. Business Requirements
- FR-14: introduce one rule with an approved example → listen at normal/slow speed → identify the rule in an example → optional microphone repeat with visual coaching → short assessment; each step sequential; microphone step skippable/replaced by listen-only per FR-9/FR-13.

##### 11. KMP Requirements
- **Rule Introduction**: renders one rule + approved example.
- **Listen**: normal and slow-speed playback via `core-kmp-player`.
- **Rule Identification Exercise**: submits attempt via B-03.
- **Optional Record step**: directly embeds/routes to K-04's `RecitationRecorderOverlay`/`RecitationViewModel` flow; skippable and replaced by listen-only automatically per the same permission/parent-toggle gating K-04 already implements — no duplicate gating logic here.
- **Assessment**: short assessment closing the flow, submits via B-03.
- **Sequential enforcement**: each step only unlocks after the prior step completes; UI must not allow skipping ahead out of order (though the record step specifically may be skipped/bypassed to listen-only, per FR-14).

##### 15. Validation
N/A client-side beyond standard sequencing enforcement.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Audio playback failure | Retry/fallback via `core-kmp-player` |
| Attempt submission failure | Non-blocking retry |
| Record step unavailable (gating) | Automatically replaced by listen-only, per K-04's existing behavior |

##### 19. Offline First
Rule content/audio downloadable and offline-usable; identification/assessment attempts queue via `SyncQueue` when offline; record step inherits K-04's connectivity-required stance.

##### 21. Localization
Rule text/examples localized via `core-common/localization`.

##### 22. RTL
Full RTL layout; Tajweed-rule Arabic-text examples rendered with correct diacritic display (shares typography requirements with K-03).

##### 25. Security
No new sensitive surface — the record step's privacy guarantees are entirely inherited from K-04's reuse.

##### 27. Testing
- Unit: sequential-step enforcement (cannot skip ahead out of order, except the record step's designed skip-to-listen-only behavior).
- Integration: record step correctly delegates to K-04's existing recorder flow with identical gating behavior (no divergence in permission/toggle logic between K-03's and K-06's record entry points).
- Integration: offline content usable, attempt sync on reconnect.

##### 31. Final Verification Checklist
- [ ] Steps enforced in correct sequence (Introduction → Listen → Identification → optional Record → Assessment)
- [ ] Record step is a direct reuse of K-04, not a parallel implementation
- [ ] Record step correctly skippable/replaced by listen-only per the same gating as K-03/K-07
- [ ] Offline content usable, attempts sync on reconnect
- [ ] RTL/diacritic rendering verified for Tajweed-rule Arabic examples
- [ ] Full test suite green in CI

#### `Development_Blueprints/A5_Quran_Arabic_Learning/KMP/07-quran-game-modes.md`

##### 4. Objective
Render all six Quran Game mode screens, routing non-recitation game types through B-03 and the Recitation Echo mode through K-04's shared recorder, with smooth drag-drop/tile interaction performance.

##### 5. Business Requirements
- FR-5: Quran Game modes must include at minimum: ayah ordering, listen-and-select matching ayah, find-the-missing-word, surah-name-to-theme matching (child-safe/approved context only), recitation echo with pronunciation coaching, and progressive-reveal memorization.

##### 11. KMP Requirements
- **Ayah Ordering**: drag-drop or tap-to-order UI, submits final order as the `answer_payload` to B-03.
- **Listen & Select Matching Ayah**: audio playback (`core-kmp-player`) + selection UI, submits via B-03.
- **Missing Word**: fill-in-the-blank/selection UI, submits via B-03.
- **Surah Theme Matching**: matching UI using only child-safe/approved theme content supplied by the content service (this screen must not allow free-text or unapproved-content pairing — content is fully server-curated).
- **Recitation Echo**: directly embeds K-04's `RecitationRecorderOverlay`/`RecitationViewModel`, identical reuse pattern to K-06 — falls back to Listen-Only/AI-Feedback identically to Surah Learning's record path.
- **Progressive-Reveal Memorization**: reveals ayah text progressively (e.g., word-by-word fade-in/reveal-on-tap) as a memorization aid, submits a completion/attempt marker via B-03 if scored, or is a pure practice mode with no scored submission (confirm against content/product intent before implementation — do not assume scoring behavior).
- **Mode Selector Sheet**: modal listing all available game modes plus lesson-type entries (Surah Learning, Arabic Letters, Tajweed), routed from K-01.
- **Performance**: drag-drop/tile interactions must not cause recomposition/frame-drop — use stable keys and avoid unnecessary state hoisting during active gestures.

##### 15. Validation
Surah Theme Matching restricted entirely to server-curated approved content — no client-side content generation/free-text path exists.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Game content load failure | Retry/fallback, friendly error state, does not block access to other game modes |
| Attempt submission failure | Non-blocking retry |
| Recitation Echo gating (mic/toggle false) | Automatically falls back to Listen-Only/AI-Feedback path identically to Surah Learning |

##### 19. Offline First
Non-recitation game content downloadable/offline-usable where feasible; attempts queue via `SyncQueue` when offline. Recitation Echo inherits K-04's connectivity-required stance.

##### 21. Localization
All game instructional copy and content localized via `core-common/localization`.

##### 22. RTL
Full RTL layout across all six modes, including drag-drop ordering direction correctness for RTL locales.

##### 25. Security
No new sensitive surface beyond what K-04 already governs for Recitation Echo; Surah Theme Matching's server-curated-only content is itself a content-safety control.

##### 27. Testing
- Unit: per-mode attempt-payload construction (ordering sequence, selection, missing-word answer, theme match).
- UI test: drag-drop ordering interaction responsiveness (no dropped frames in a scripted gesture test where feasible).
- Integration: Recitation Echo gating behavior matches K-03/K-06 exactly (parity test).
- Integration: Surah Theme Matching never presents unapproved/non-curated content (verified against a fixture content set).

##### 31. Final Verification Checklist
- [ ] All six game modes implemented per FR-5's minimum list
- [ ] Recitation Echo behaves identically to K-03/K-06's record-step gating and fallback (parity verified)
- [ ] Surah Theme Matching never presents unapproved/non-curated content
- [ ] Drag-drop/tile interactions perform without frame drops
- [ ] Mode Selector Sheet correctly wired from K-01 and routes to all modes/lessons
- [ ] RTL layout verified, including drag-drop direction correctness
- [ ] Full test suite green in CI

#### `Development_Blueprints/A5_Quran_Arabic_Learning/KMP/08-daily-quiz-learn-tab-experience.md`

##### 4. Objective
Render the Daily Quiz flow (question set, per-answer explanation, retry set, results/XP reveal) sourced from B-07, reusing A.8's existing quiz UI components rather than building a parallel quiz UI.

##### 5. Business Requirements
- FR-15: 5 questions, types multiple choice/sequence/true-false/image-match/audio-match, per-answer explanation, incorrect answers enter a retry set within the same session.
- FR-16: completion awards effort XP regardless of accuracy; accuracy affects mastery, not participation XP.
- Empty State: zero quiz history → friendly first-time framing, not an empty chart.
- Offline: pre-downloaded subset of likely-quiz-content cacheable for offline attempts, syncing results on reconnect with idempotent submission.

##### 11. KMP Requirements
- **Delegation, not duplication**: this blueprint's ViewModel supplies `context=learn` and displays A.8's existing quiz screen/results/retry-set components — no new question-rendering, retry-set, or XP-reveal UI is built here.
- **Offline caching**: pre-download a subset of likely `context=learn` quiz content (via the existing offline-content-download pattern) for offline attempts; sync results on reconnect with idempotent submission (reuses A.8's existing idempotency mechanism if present, or `client_event_id`-style idempotency consistent with B-03's pattern — confirm against A.8's actual sync contract).
- **Empty state**: zero quiz history renders A.8's existing first-time framing (if A.8 already handles this) rather than a Learn-tab-specific reimplementation.
- **Entry points**: from the Skill Tree screen (K-01) and from Home's Daily Quiz widget (cross-feature, confirm Home's actual widget-to-quiz navigation contract before wiring).

##### 15. Validation
N/A client-side beyond what A.8's existing quiz components already validate.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Quiz service unavailable | A.8's existing "quiz will be ready again soon" friendly message, reused as-is |
| Offline with no cached content | Clear unavailable state, does not block other Learn-tab content |

##### 19. Offline First
Pre-downloaded subset of `context=learn` quiz content cacheable for offline attempts; results sync on reconnect idempotently.

##### 21. Localization
Reuses A.8's existing localization handling for quiz content.

##### 22. RTL
Reuses A.8's existing RTL support for quiz UI.

##### 25. Security
No new sensitive surface; standard authenticated-session flow, fully inherited from A.8's existing implementation.

##### 27. Testing
- Unit: `LearnDailyQuizEntryViewModel` correctly supplies `context=learn` to the underlying quiz-fetch call.
- Integration: full quiz flow renders using A.8's existing components with Learn-tab-sourced content.
- Integration: offline cached quiz content usable, results sync on reconnect.
- Contract test: confirms no duplicate quiz-rendering component was introduced (code-review/architecture-conformance check rather than a runtime test).

##### 31. Final Verification Checklist
- [ ] No duplicate quiz-question-rendering, retry-set, or results UI introduced (confirmed via architecture review against A.8)
- [ ] `context=learn` correctly passed through the full fetch→render→submit chain
- [ ] Effort XP awarded regardless of accuracy (inherited from A.8, verified via integration test)
- [ ] Offline cached quiz content usable, idempotent sync on reconnect
- [ ] Both entry points (Skill Tree, Home widget) correctly wired
- [ ] Full test suite green in CI

#### `Development_Blueprints/A5_Quran_Arabic_Learning/KMP/09-spaced-review-needs-refresh-prompt.md`

##### 4. Objective
Render the "Needs Refresh" prompt component on K-01's Skill Tree, respecting the server-provided daily cap, framed consistently as a gentle review invitation rather than a failure signal.

##### 5. Business Requirements
- FR-4: `Needs Refresh` surfaces as a gentle "let's review this together" prompt, never framed as regression/failure.
- Edge Case 6: multiple due nodes capped per day (server-enforced by B-06), remainder queued for subsequent days without being dumped simultaneously.

##### 11. KMP Requirements
- **Rendering**: gentle prompt component (per §2.1 design tokens — amber ring + gentle refresh icon, never alarming red) shown inline on due nodes within the Skill Tree.
- **Cap respected**: the prompt only renders for nodes the server has already marked `shown_today`/`needs_refresh` in the response — no client-side re-capping or re-computation of which nodes to show.
- **Framing**: copy consistently reads as "let's review this together" or equivalent gentle language — never regression/failure wording, verified via a copy-review checklist item as well as UI test string assertions.
- **Routing**: tapping the prompt routes to the relevant node-type screen (Surah Learning, Arabic Letters, Tajweed, or a Quran Game mode) based on the node's `node_type`, reusing K-03/K-05/K-06/K-07's existing navigation entry points — no new practice-screen logic introduced here.

##### 15. Validation
N/A (purely presentational component).

##### 18. Error Handling
N/A beyond K-01's existing skill-tree fetch error handling (this component simply doesn't render if the parent screen has no data).

##### 19. Offline First
Renders from K-01's cached skill-tree data, consistent with K-01's offline/cache-fallback behavior.

##### 21. Localization
Prompt copy localized via `core-common/localization`, with locale-appropriate gentle phrasing (not a literal machine translation of "let's review this together" without tone review per locale).

##### 22. RTL
Full RTL layout for the prompt component.

##### 25. Security
N/A (no sensitive data, no separate network call).

##### 27. Testing
- Unit: routing logic correctly maps `node_type` to the right destination screen.
- UI test: prompt copy asserted against a gentle-language allowlist / against a negative-language blocklist (no "failed," "wrong," "regressed," etc.).
- Integration: prompt only renders for nodes the server marked `needs_refresh`, never client-computed.

##### 31. Final Verification Checklist
- [ ] Prompt renders only for server-marked `needs_refresh` nodes, no client-side re-capping
- [ ] Copy consistently gentle, never regression/failure-framed (verified via string assertion test)
- [ ] Tap-routing correctly maps to each node type's existing screen
- [ ] RTL layout verified
- [ ] Full test suite green in CI

#### `Development_Blueprints/A5_Quran_Arabic_Learning/KMP/10-progressive-hint-overlay.md`

##### 4. Objective
Render a reusable Hint Overlay invoked from any exercise's "Hint" control, displaying server-supplied progressive hint text and never synthesizing reveal content client-side.

##### 5. Business Requirements
- FR-18: hints progressive/partial, never revealing the full answer; hint usage tracked, never a visible penalty.
- Edge Case 8: question types without a meaningful partial hint fall back to an explanatory micro-hint.

##### 11. KMP Requirements
- **Progressive levels**: renders `hint_level` 1/2/3 sequentially as the child requests more, each level's text supplied entirely by the server response — the client renders whatever level text is returned and never synthesizes additional reveal content locally.
- **Fallback handling**: if B-05 returns a generic-encouragement fallback (service degraded or no-meaningful-partial-hint question type), render it identically to a normal hint (no special "broken" UI state).
- **Resume**: dismissing the overlay resumes the underlying exercise state exactly where the child left off — no exercise-state loss.
- **Hint control styling**: small, secondary-styled, always visibly present but never pulsing/highlighted in a way that pressures use (per PRD §2.1 UX requirement).
- **`hint_count` tracking**: this overlay itself does not mutate `hint_count` — the invoking exercise screen increments its own local counter and includes it in its own B-03/B-04 attempt submission (consistent with B-05's "read-only, no double-counting" design).

##### 15. Validation
N/A client-side beyond standard fetch handling.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Hint fetch failure | Generic encouragement fallback text rendered identically to a normal hint (per B-05's own graceful-degradation design) |
| Unknown question_id | Should not occur in practice (exercise screens always pass valid IDs); if it does, render the fallback text rather than an error |

##### 19. Offline First
Hints require connectivity (lightweight fetch); if offline, show a brief "hints need internet" inline message without blocking the underlying exercise.

##### 21. Localization
`hint_text` resolved server-side per locale (B-05 delegates to the `localization` context) — client renders as-is.

##### 22. RTL
Full RTL layout for the overlay.

##### 25. Security
No sensitive data.

##### 27. Testing
- Unit: overlay never synthesizes hint text locally — always renders exactly the server-provided string for the requested level.
- Unit: `hint_count` is NOT mutated by this component (verified via a test asserting no write/state-mutation call exists in this ViewModel targeting `hint_count`).
- UI test: dismissing the overlay resumes the exact prior exercise state (no state loss).
- Integration: fallback text renders identically to a normal hint on service failure (no distinct "broken" UI state).

##### 31. Final Verification Checklist
- [ ] Hint text always exactly server-provided, never client-synthesized
- [ ] `hint_count` mutation happens only in the invoking exercise screen's own attempt submission, never in this component
- [ ] Fallback text renders identically to a normal hint (no distinct broken-state UI)
- [ ] Dismissing the overlay resumes the exact prior exercise state
- [ ] Hint control styled per UX spec (secondary, non-pulsing)
- [ ] Full test suite green in CI

#### `Development_Blueprints/A5_Quran_Arabic_Learning/KMP/11-islamic-fact-detail-mastery-celebration.md`

##### 4. Objective
Render Islamic Fact detail content with full scholar-approval metadata and source references, and a Mastery Badge/Node-Unlock Celebration modal triggered by a `mastered` state transition.

##### 5. Business Requirements
- FR-19: Islamic Facts must carry locale/age-banded text, topic/related-content linkage, primary/secondary source references, scholar approval and version, an explanation, a linked quiz item, and jurisprudential-scope/exclusion notes where relevant.

##### 11. KMP Requirements
- **Islamic Fact Detail**: renders locale/age-banded text, topic and related-content linkage (navigable), primary/secondary source references, scholar-approval badge + version, an explanation, a linked quiz item (routes into K-08's quiz flow for that specific item if supported by A.8's contract), and jurisprudential-scope/exclusion notes where present.
- **Mastery Celebration**: `MasteryCelebrationModal` triggered when `SkillTreeViewModel` detects a node transitioning to `mastered` (comparing before/after skill-tree fetch results, or a dedicated event emitted by the mutation flow that caused the transition — e.g., B-03's attempt-submission response, if it surfaces the resulting state change); dismissible, routes back to Skill Tree.
- Reuse existing celebratory-modal visual pattern from elsewhere in the app if present (e.g., Rewards feature) rather than introducing a new one-off celebration UI paradigm.

##### 15. Validation
N/A client-side.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Fact content load failure | Friendly error state, does not block navigation back |
| Celebration trigger ambiguity (unclear which mutation caused mastery) | Fall back to comparing consecutive skill-tree fetches rather than skipping the celebration entirely |

##### 19. Offline First
Fact content offline-cacheable if `content` context supports it generally; Mastery Celebration works offline trivially since it's derived from already-cached skill-tree state.

##### 21. Localization
Fact text and all metadata fields localized/age-banded per `core-common/localization`.

##### 22. RTL
Full RTL layout for both screens.

##### 25. Security
No sensitive data.

##### 27. Testing
- Unit: Islamic Fact detail correctly surfaces all required metadata fields (scholar approval/version, source references, jurisprudential-scope notes when present).
- Unit: Mastery Celebration trigger logic correctly detects `mastered` transitions without false-triggering on unrelated state changes.
- UI test: linked quiz item and related-content navigation work correctly.

##### 31. Final Verification Checklist
- [ ] Islamic Fact detail includes all FR-19 required fields (scholar approval/version, sources, jurisprudential-scope notes where applicable)
- [ ] Mastery Celebration triggers only on genuine `mastered` transitions, no false positives
- [ ] Linked quiz item and related-content navigation function correctly
- [ ] RTL/localization verified
- [ ] Full test suite green in CI

#### `Development_Blueprints/A5_Quran_Arabic_Learning/KMP/12-parent-progress-report-in-app.md`

##### 4. Objective
Render the Parent Progress Report and Concept Detail drill-in screens using B-08's concept-level data, with a proper empty state for zero-activity children.

##### 5. Business Requirements
- FR-17: parent-facing reports show concepts/skills, not just a raw score.
- Acceptance Criteria: report lists mastered/in-progress concepts and consistency trends, not merely a percentage.
- Empty State: "Once [Child] starts practicing, you'll see their progress here."

##### 11. KMP Requirements
- **Parent Learning Report screen**: lists mastered/in-progress/needs-refresh concepts with plain-language labels and a consistency trend visualization — never a single raw percentage as the headline (mirroring B-08's schema constraint at the UI layer too, i.e., no numeric score prominently displayed even if a raw number happened to leak into the payload).
- **Concept Detail screen**: drill-in from the report list, showing per-concept detail.
- **Empty state**: "Once [Child] starts practicing, you'll see their progress here" for zero-activity children — reuses the report screen's own empty-state handling rather than a separate screen.
- **Error handling**: report fetch failure shows a graceful retry state, not a broken/blank screen.

##### 15. Validation
N/A client-side.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Report fetch failure | Graceful retry state |
| Zero-activity child | Empty-state framing, not a broken/blank view |

##### 19. Offline First
N/A (parent-session screen, connectivity assumed, no offline requirement specified in PRD).

##### 21. Localization
Concept labels/trend copy localized via `core-common/localization`.

##### 22. RTL
Full RTL layout.

##### 25. Security
Parent-session auth only; no child-session token accepted. No recitation audio/raw-confidence data ever surfaced (inherited from B-08's design).

##### 27. Testing
- Unit: report rendering never surfaces a raw percentage as the headline UI element.
- Integration: zero-activity empty state renders correctly.
- Integration: report fetch failure shows graceful retry, not a crash/blank screen.

##### 31. Final Verification Checklist
- [ ] No raw percentage/score ever rendered as the headline UI element
- [ ] Zero-activity empty state matches PRD copy intent
- [ ] Report fetch failure handled gracefully, no blank/broken screen
- [ ] Correctly wired into existing Parent Area navigation structure
- [ ] RTL/localization verified
- [ ] Full test suite green in CI

#### `Development_Blueprints/A5_Quran_Arabic_Learning/KMP/13-parent-ai-microphone-permission-control.md`

##### 4. Objective
Provide the per-child AI/Microphone toggle within Parental Controls, persisted server-side, with mid-session-change handling that never leaves a child on a broken control.

##### 5. Business Requirements
- FR-13: parent can disable microphone/AI per child (not just globally); when disabled, all recitation practice defaults to listen-and-self-assess app-wide for that child, no UI bypass path.
- Edge Case 2: mid-session disable applies at next session per the standing Parent Dashboard rule, but must never leave the child stuck on a broken control if it does interrupt mid-session.
- Permission States §1.15: OS-level permission + parent-level toggle both gate recording UI; either false routes to listen-only.

##### 11. KMP Requirements
- **Toggle rendering**: per-child AI/Microphone toggle within the existing Parental Controls surface.
- **Persistence**: writes via `ParentalControlsRepository`, confirmed server-side (the write must succeed against the backend before the UI reflects the new state — no optimistic-only update that could desync from B-04's server-side enforcement).
- **Scope enforcement**: when disabled, this is the single source of truth K-04's record-button gating reads from — no separate/duplicate toggle-reading logic anywhere else in the app.
- **Mid-session handling (Edge Case 2)**: the toggle change itself doesn't need special mid-session logic here — this is K-04's responsibility (re-checking on app-state resume) — this screen's job is simply to persist the change correctly and promptly.
- **Save failure**: clear error state, retry option, toggle UI does not silently appear to have saved if the write failed.

##### 15. Validation
N/A beyond standard toggle-state handling.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Toggle save failure | Clear error state, retry option, UI does not falsely show success |
| Toggle read failure on screen load | Retry option, does not default to a silently-incorrect state |

##### 19. Offline First
N/A (parent-session, connectivity-required write action).

##### 21. Localization
Toggle label/description localized via `core-common/localization`.

##### 22. RTL
Full RTL layout, consistent with the rest of Parental Controls.

##### 25. Security
This toggle is a UX-layer convenience for K-04's client-side gating — the authoritative enforcement is always B-04's server-side re-validation on every recitation request, so a failure/inconsistency in this screen's persistence cannot be exploited to bypass the actual safety control (defense in depth, per B-04's design).

##### 27. Testing
- Unit: toggle write correctly calls `ParentalControlsRepository.setAiMicPermission()` and only reflects UI success after server confirmation (no optimistic-only update).
- Integration: toggle change is correctly readable by K-04's gating logic on next check (cross-feature consistency test).
- UI test: save failure shows a clear error state, not a false-success UI.

##### 31. Final Verification Checklist
- [ ] Toggle is embedded within C.23's existing Parental Controls surface, not a duplicate standalone screen
- [ ] Write only reflects UI success after server confirmation (no optimistic-only update)
- [ ] K-04's gating logic correctly reads this toggle as its single source of truth
- [ ] Save failure shows a clear error state, no false-success UI
- [ ] RTL/localization verified
- [ ] Full test suite green in CI

## A6 — Feature_A6_Dua_Learning

PRD: `PRD_Documents/Child App (1-12)/Feature_A6_Dua_Learning.md`

Coverage: 14 mandatory FR records; all preserved verbatim below. Feature has 20 inventory records including components/states. Components and states must not inflate independently executed screen count.

### Existing screenshot candidates

- `Screens/Mobile App/Du'as/Dua Card-01.png` — visually inspected
- `Screens/Mobile App/Du'as/Dua Card-02.png` — inventoried only
- `Screens/Mobile App/Du'as/Dua Categories-01.png` — inventoried only
- `Screens/Mobile App/Du'as/Dua Categories-02.png` — inventoried only
- `Screens/Mobile App/Du'as/Dua Categories-03.png` — inventoried only
- `Screens/Mobile App/Du'as/Dua Categories-04.png` — inventoried only
- `Screens/Mobile App/Du'as/Dua Categories-05.png` — inventoried only
- `Screens/Mobile App/Du'as/Dua Categories-06.png` — inventoried only
- `Screens/Mobile App/Du'as/Dua Categories-07.png` — inventoried only
- `Screens/Mobile App/Du'as/Dua Categories-08.png` — inventoried only
- `Screens/Mobile App/Du'as/Dua Quiz-01.png` — inventoried only
- `Screens/Mobile App/Du'as/Dua Quiz-02.png` — inventoried only
- `Screens/Mobile App/Du'as/Dua Quiz-03.png` — inventoried only
- `Screens/Mobile App/Du'as/Dua Quiz-04.png` — inventoried only

### Complete normative functional coverage

### 1.7 Functional Requirements

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

### Ordered source inventory

### 1.18 Screen Inventory (Complete — Zero Missing)

| # | Screen | Type | Entry Points | Exit Points |
|---|---|---|---|---|
| 1 | Dua Learning Landing (Category List) | Primary | Learn Tab, Search | Category Dua List |
| 2 | Category Dua List | Screen | Dua Learning Landing | Dua Card Detail |
| 3 | Dua Card Detail (Arabic/Transliteration/Translation/Audio) | Screen | Category List, Search, Favorites, Habit Tracker deep link | Recall Quiz, back to list |
| 4 | Audio Playback Controls (in-card component) | Component | Dua Card Detail | N/A |
| 5 | Read-Along Text Highlight (component, during playback) | Component | Dua Card Detail (while playing) | N/A |
| 6 | Mark-as-Learned Confirmation (lightweight, inline) | Component | Dua Card Detail "Mark as Learned" action | Recall Quiz prompt |
| 7 | Recall Quiz Entry Prompt | Component | Post-Mark-as-Learned, or re-entry on an already-Learned dua | Recall Quiz screen |
| 8 | Recall Quiz Question Screen | Screen | Recall Quiz Entry Prompt | Next question / Result |
| 9 | Recall Quiz Incorrect — Supportive Retry + Dua Card Recall | Screen variant | Incorrect answer | Retry question |
| 10 | Recall Quiz Result / Pass Screen | Screen | Final question answered correctly | Dua Master badge progress / back to list |
| 11 | Dua Master Badge Progress Celebration (milestone) | Modal | Crossing a badge threshold | Dismiss → Achievements (A.11) |
| 12 | Habit Tracker Reminder Suggestion Prompt | Modal/inline card | Dua marked Learned | Habit Tracker (A.7) setup, or dismiss |
| 13 | Favorites List (Dua-filtered view, shared component with A.3) | Screen | Dua Learning Landing "Favorites" entry, Profile | Dua Card Detail |
| 14 | Search Results (Dua-scoped) | Screen | Global Search (A.13), scoped to duas | Dua Card Detail |
| 15 | Empty State — No duas in category | Screen variant | Sparse/new category | Alternate category |
| 16 | Empty State — No favorites yet | Screen variant | Favorites List | Dua Learning Landing |
| 17 | Offline — Dua Not Downloaded Notice | Component | Tap on a non-downloaded dua while offline | Dismiss, suggests downloaded alternative |
| 18 | Dua Temporarily Unavailable (archived/withdrawn) | Screen variant | Tap on a withdrawn dua | Suggested alternative from same category |
| 19 | Downloads Manager (Dua scope, shared with A.16) | Screen | Dua Card Detail download icon, Settings | Dua Card Detail (offline) |
| 20 | Parent Dua Progress View | Screen (Parent Area) | Parent Dashboard → Child Progress → Learning → Duas | Concept-level dua list, individual dua status |

### Exact mobile UX and behavior sources

### 1.9 Acceptance Criteria

- Given a child opens the Dua Learning screen, when the category list renders, then exactly the six defined categories (Morning, Bedtime, Food, Travel, Gratitude, Protection) are shown (plus any additional scholar-approved categories added over time, but never fewer than these six as the baseline taxonomy).
- Given a child opens a specific dua, when the Dua Card renders, then Arabic text, transliteration, translation, and an audio control are all visible without additional taps.
- Given a child has not marked a dua as Learned, when they look for a Recall Quiz entry point for that dua, then none is presented (quiz is gated on Learned status).
- Given a child answers a Recall Quiz question incorrectly, when the result is shown, then supportive retry language appears alongside the full dua card, not a bare incorrect indicator.
- Given a child marks a dua as Learned, when they next open the Habit Tracker, then that dua appears as a suggested candidate for a daily reminder habit.
- Given a child has a free-tier (non-premium) account, when they open any dua, then it is fully accessible with no paywall/upsell shown — this is true for every dua in the catalog without exception.
- Given a dua draft has no audio attached, when an editor attempts to submit it for scholar review, then the submission is blocked with a clear "audio required" validation message.
- Given a child is offline with a previously-downloaded dua, when they open it, then the full card (Arabic/transliteration/translation/audio) renders and plays identically to the online experience.

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

### 1.16 User Flow (Narrative)

Child opens Learn tab → navigates to Dua Learning → browses by category or searches → opens a Dua Card → listens to the audio, reads Arabic/transliteration/translation → repeats practice across one or more sessions → marks the dua as Learned when confident → optionally attempts the Recall Quiz → on quiz pass, dua contributes toward the Dua Master badge progress and becomes a suggested Habit Tracker reminder candidate → child may favorite frequently-used duas for quick future access.

### 2.1 Dua-Specific Design System Extensions

- **Dua Typography:** Arabic dua text uses the same formal Naskh-style typeface established for Quranic content in A.5 (consistency across all sacred/liturgical text in the app), distinct from general UI Arabic. Transliteration uses an italicized Latin font; translation uses standard body text — the three-line stacked layout (Arabic / transliteration / translation) is a consistent, recognizable pattern repeated across every Dua Card.
- **Category Iconography:** Each of the six categories has a distinct, simple, warm icon (e.g., a sun for Morning, a moon for Bedtime, a small plate for Food, a small path/road for Travel, an open hand for Gratitude, a shield-like soft shape for Protection) — consistent, friendly, non-threatening even for "Protection" (avoid anything resembling a weapon or alarming imagery).
- **Read-Along Highlight:** During audio playback, the Arabic text's current word/phrase is gently highlighted (soft background color sweep) to support read-along literacy — this is a recommended default for dua content given its memorization purpose, distinct from optional captions in Stories.

### 2.2 Screen-Level Design Requirements (Key Screens)

#### Screen: Dua Card Detail

- **Purpose:** Present a complete, learnable dua in one view.
- **Components:** Category tag, large Arabic text block (top, primary visual weight), transliteration line, translation line, audio play/pause control with a progress scrubber, Favorite (heart) icon, Mark-as-Learned toggle/button, Recall Quiz entry button (visible but distinctly secondary until Learned status is set, at which point it becomes primary-styled).
- **States:** Default (not yet learned), Learned (badge/checkmark indicator visible), Playing (read-along highlight active), Offline-available, Offline-unavailable, Error (audio load failure).
- **Accessibility:** Read-along highlight has a screen-reader-friendly alternative (sequential text exposure, not relying on visual highlight alone); translation/transliteration always screen-reader-readable regardless of visual toggle state if one exists.
- **Responsive Rules:** Single-column on mobile; tablet may show category list + dua card side-by-side (master-detail layout) rather than full-screen navigation per tap.

#### Screen: Recall Quiz Question Screen

- **Purpose:** Lightweight, low-pressure check of dua recall.
- **Components:** Question text/audio, 2-4 answer options (consistent with the platform's max-3-or-4-option pattern for child-friendly choice UIs), progress indicator only if more than one question exists for this dua (avoid a misleading "Question 1 of 1" framing — simply omit the counter when there's only one question, per Edge Case 8).
- **States:** Default, Answered-correct (immediate positive feedback), Answered-incorrect (supportive retry + full dua card resurfaced inline or via a clear "review" link).

### 2.3 Tab Structure

Dua Learning is reached via the Learn tab (Tab 2 of 5). Click mapping:

| Click Target | Destination | API Called | Analytics Event | Permission Check | Error Handling |
|---|---|---|---|---|---|
| Category tile | Category Dua List | `GET /v1/catalog?type=dua&category=` | `dua_category_selected` | None (always free-tier) | Cached fallback |
| Dua card (list item) | Dua Card Detail | `GET /v1/catalog/dua/{id}` | `dua_card_opened` | None | Graceful unavailable state |
| Mark as Learned | Inline state update | `POST /v1/progress` | `dua_marked_learned` | None | Optimistic + retry |
| Recall Quiz button | Recall Quiz Question Screen | `GET /v1/quizzes/dua/{dua_id}` | `dua_recall_quiz_started` | Gated on Learned status (client + server) | Friendly unavailable message |
| Favorite icon | Inline toggle | `POST /v1/favorites` | `dua_favorited` | None | Optimistic + retry |
| Download icon | Inline download start | `POST /v1/downloads/manifest` | `dua_download_started` | Parent download-policy (shared A.16) | Retry on failure |

### 2.4 Wireframe Description (Composite)

Category List: a simple grid or list of six (or more) category tiles with icon + label, consistent with other catalog-browsing patterns in the app (similar visual family to Stories' category rails but simpler given the smaller, more enumerable dua taxonomy). Dua Card Detail: a single-column, vertically-stacked layout prioritizing the Arabic text visually, consistent with the "single clear focus" wireframe philosophy used for Surah Learning (A.5).

### 2.5 Screen Image Generation Prompts

**Screen: Dua Learning — Category List**
- *Prompt 1 (English):* "Mobile app category selection screen UI mockup for a children's Islamic learning app's dua section. Warm off-white background. A grid of six rounded square category cards, each with a simple friendly icon and a short label: a sun icon for 'Morning', a crescent moon for 'Bedtime', a small plate-and-utensil icon for 'Food', a winding path icon for 'Travel', an open-hand icon for 'Gratitude', and a soft rounded shield-like shape for 'Protection'. Each card in a slightly different soft pastel-teal-and-gold tint, rounded corners, soft shadows, warm and friendly aesthetic, no realistic human faces, bottom navigation bar visible with 5 icons."
- *Prompt 2 (Arabic RTL):* "نفس شاشة اختيار الفئات لقسم الأدعية في تطبيق تعليم إسلامي للأطفال، بتخطيط من اليمين إلى اليسار. خلفية بيج فاتح دافئ. شبكة من ست بطاقات فئات مربعة مستديرة الزوايا، كل منها بأيقونة بسيطة وودودة وتسمية قصيرة: أيقونة شمس لـ 'الصباح'، هلال لـ 'وقت النوم'، أيقونة صحن وأداة طعام صغيرة لـ 'الطعام'، أيقونة طريق متعرج لـ 'السفر'، أيقونة يد مفتوحة لـ 'الشكر'، وشكل درع ناعم ومستدير لـ 'الحماية'. كل بطاقة بدرجة لون باستيل فيروزي وذهبي مختلفة بلطف، زوايا دائرية، ظلال خفيفة، طابع دافئ وودود، بدون وجوه بشرية واقعية، شريط تنقل سفلي ظاهر بخمس أيقونات."

**Screen: Dua Card Detail**
- *Prompt 1 (English):* "Mobile app dua learning detail screen UI mockup for children. Warm off-white background, rounded card layout. At the top, large elegant Arabic calligraphic text centered, generously spaced. Below it, a smaller italic-style transliteration line, and below that a translation line in regular font, both in soft ink-grey color. Below the text block, a horizontal audio player bar with a play button, soft teal progress line, and a small replay icon. To the side, a heart-shaped favorite icon outline and a rounded checkmark-style 'Mark as Learned' button in warm gold when active. A small secondary 'Practice Quiz' button below, more subdued in styling until the dua is marked learned. Calm, respectful, focused educational aesthetic, soft shadows, generous spacing, no realistic human faces."
- *Prompt 2 (Arabic RTL):* "نفس شاشة تفصيل تعلم الدعاء للأطفال، بتخطيط من اليمين إلى اليسار بالكامل. خلفية بيج فاتح دافئ، تخطيط بطاقة مستديرة الزوايا. في الأعلى نص عربي أنيق بخط زخرفي كبير في المنتصف بتباعد كبير. تحته سطر أصغر للنقل الصوتي بخط مائل الطابع، وتحت ذلك سطر ترجمة بخط عادي، كلاهما بلون رمادي حبري ناعم. أسفل كتلة النص شريط مشغل صوت أفقي بزر تشغيل وخط تقدم فيروزي ناعم وأيقونة إعادة تشغيل صغيرة. بجانبه أيقونة قلب لإضافة المفضلة وزر بشكل علامة صح مستدير بعنوان 'تم التعلم' بلون ذهبي دافئ عند تفعيله. زر ثانوي صغير بعنوان 'تدريب الاختبار' أسفل ذلك، بنمط أكثر هدوءًا حتى يتم تعليم الدعاء كمكتسب. طابع تعليمي هادئ ومحترم ومركّز، ظلال خفيفة، تباعد كبير، بدون وجوه بشرية واقعية."

*(Remaining screens — Recall Quiz, Badge Celebration, Habit Reminder Suggestion, Favorites List, Parent Dua Progress View — follow the same two-prompt EN/AR template using these tokens; full set available on request.)*

---

### 6.1 Technical Requirements
Kotlin, Jetpack Compose, MVVM, Clean Architecture, module `:feature:dua-learning`, depends on `:core:media-player` (shared, for audio playback — simpler usage than the full Story Player, just play/pause/scrub), `:core:design-system`, `:core:offline-cache`.

### 6.2 Screen Mapping
Each screen in §1.18 maps to a Composable; `DuaCardDetailScreen` reuses `:core:media-player`'s lightweight audio-only playback wrapper (not the full immersive video player UI from A.3).

### 6.3 Navigation Flow
Nested graph under the Learn tab, parallel to A.5's Quran/Arabic graph; `noorheroes://learn/dua/{dua_id}` deep link for Habit Tracker reminder-tap entry and Search results.

### 6.4 State Management
`DuaCardViewModel` holds `DuaCardUiState` (content, learnedStatus, isFavorited, playbackState) — `learnedStatus` toggling is optimistic-update-then-reconcile, consistent with the platform's habit-check-in optimistic pattern (A.2).

### 6.5 API Mapping
`DuaRepository.markLearned()` → `POST /v1/progress` with `content_type: "dua"`; `DuaRepository.getCatalog()` → `GET /v1/catalog?type=dua` (no entitlement-check call needed/made client-side either, consistent with the always-free design).

### 6.6 Analytics Mapping
`DuaLearningAnalytics` fires events per §1.19; `dua_recall_quiz_started` only fires after a successful server `200` (not on tap) to avoid mis-counting attempts blocked by the `403 NOT_YET_LEARNED` server check.

### 6.7 Offline Support
Standard download/offline-cache pattern shared with A.16; Mark-as-Learned and Favorite actions queue in a local outbox synced via WorkManager on reconnect, using `client_event_id` idempotency.

### 6.8 Deep Linking
`noorheroes://learn/dua/{dua_id}`, `noorheroes://learn/dua/category/{category}`.

### 6.9 Push Notifications
Not a notification source itself; Habit Tracker (A.7)-originated dua-reminder notifications deep-link here.

### 6.10 Testing Strategy
- Unit: `DuaCardViewModel` optimistic-update/reconcile logic, Recall Quiz gating logic (client mirrors server's `NOT_YET_LEARNED` check for fast local UX but treats server as authoritative on actual quiz-start).
- UI tests: Recall Quiz question screen correctly omits the "Question X of Y" counter when `total_available == 1`; Dua Card renders all four required elements (Arabic/transliteration/translation/audio control) simultaneously without requiring extra taps.
- Integration: full mark-as-learned → quiz-unlock → quiz-pass → badge-progress-update flow against a mocked backend.
- **Always-free-tier UI regression test:** render the Dua Card/Catalog screens using a mocked "trial-expired" or "free-tier" account fixture and assert NO paywall/upsell UI component is present anywhere in the composable tree (Android-side mirror of the backend's P0 regression test).

---

### 13.1 Test Plan Summary
Coverage spans: always-free-tier guarantee (signature test), mark-as-learned/quiz-gating correctness, habit-suggestion event integration, content-versioning integrity, and all 12 edge cases from §1.10.

### 13.2 Test Cases — Happy Path
1. Child browses Morning category, opens a dua, listens, marks it learned, passes the recall quiz, sees badge progress update, accepts the habit-reminder suggestion.
2. Free-tier (non-premium) child account accesses every dua in the catalog with full functionality and zero paywall prompts anywhere.
3. Parent views Dua Progress and sees a concept-level list of learned duas with linked habit-reminder status.

### 13.3 Edge Cases
All 12 items from §1.10.

### 13.4 Negative Cases
- Attempt `GET /v1/quizzes/dua/{id}` for a dua not yet marked learned → `403 NOT_YET_LEARNED`.
- Attempt to submit a dua draft for scholar review with no audio attached via direct admin API call → rejected.
- Run the always-free-tier regression suite against a deliberately-misconfigured staging build with tier-gating middleware accidentally applied to all content types → confirm the test suite correctly fails (a test-of-the-test sanity check, run periodically).
- Mark a dua learned, confirm badge awarded at threshold, un-mark it, re-check badge state → badge remains present.

### 13.5 Regression Cases
Full Dua Learning suite re-run on every release touching this module, the shared Content/Progress/Quiz services, the entitlement middleware, or the Reward Service.

### 13.6 Automation Cases
End-to-end: full learn → quiz → badge → habit-suggestion flow; always-free-tier UI regression across all account-tier fixtures (CI-blocking); offline mark-as-learned → sync round trip.

---

### Corresponding KMP blueprint requirements

#### `Development_Blueprints/A6_Dua_Learning/KMP/01-dua-catalog-category-discovery.md`

##### 4. Objective
Render the category landing screen and per-category dua lists, using the real network/data/navigation stack, with a CI-blocking regression test proving no paywall UI ever appears.

##### 5. Business Requirements
FR-1, FR-4, FR-13; baseline six categories plus admin-added ones (K-09); empty-state for sparse categories.

##### 11. KMP Requirements
- `DuaCatalogViewModel` exposes `DuaCatalogUiState` (categories, loading, error, cached-stale flag)
- `DuaRepositoryImpl.getCatalog(category, locale)` — cache-then-network via `SafeDatabaseHelper`/Room, wrapped in `safeCall<T>{}`
- Deep link registration via `Navigator`'s `NavigationAction` for `noorheroes://learn/dua/category/{category}`
- No client-side entitlement check performed anywhere (always-free by design)

##### 15. Validation
Category list fetched from B-11's `GET /v1/dua/categories` via K-09, not hardcoded.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Catalog fetch failure | `HttpResponse.toAppError()` mapped to a local `AppError`, cached last-known catalog rendered with a subtle staleness indicator |
| Empty category | Empty state per PRD §1.12 |

##### 19. Offline First
`SafeDatabaseHelper`-backed cache-then-network, consistent with the real Room-based offline pattern documented in `CORE_DATABASE_INSTRUCTIONS.md`.

##### 21. Localization
Category labels/dua titles rendered in active locale; sourced from B-11's category metadata (K-09), not hardcoded strings.

##### 22. RTL
Full RTL layout via `NoorColorScheme`/`ThemeSpec` conventions.

##### 25. Security
Standard bearer-token reuse via `core/network`'s existing interceptor.

##### 27. Testing
- Unit: `DuaCatalogViewModel` category-filter/search logic, cache-then-network transitions
- UI: empty/loading/error states
- **Always-free-tier UI regression (CI-blocking)**: render against free/trial-expired/premium fixtures, assert identical composable tree

##### 31. Final Verification Checklist
- [ ] Uses Koin (`koinInject`), not Hilt
- [ ] Uses cursor-based pagination matching `PagedResponseDto<T>`, not offset/page
- [ ] Cache-then-network via `SafeDatabaseHelper`/Room
- [ ] Always-free-tier UI regression test passes and is CI-blocking
- [ ] Category rendering is data-driven (K-09), not hardcoded
- [ ] Navigation via `Navigator`/`NavigationAction`, not a bespoke API

#### `Development_Blueprints/A6_Dua_Learning/KMP/02-dua-card-detail-audio-playback-experience.md`

##### 4. Objective
Render the complete Dua Card in one composition pass with read-along highlight, optimistic-then-server-confirmed Mark-as-Learned, and Favorite toggling — using the real `AudioPlayerController`/`AudioPlayer` (audio-only playback, not the video-oriented `KMPPlayer`).

##### 5. Business Requirements
FR-2, FR-3, FR-5; Edge Case 12 (single-active-audio-session).

##### 11. KMP Requirements
- `DuaCardViewModel` holds `DuaCardUiState(content, learnedStatus, isFavorited, playbackState)`
- `learnedStatus`/`isFavorited`: optimistic-update-then-reconcile
- Playback via `koinInject<AudioPlayerController>()` + `AudioPlayer` composable; single-active-audio-session behavior is `AudioPlayerController`'s existing responsibility (per `CORE_KMP_PLAYER_INSTRUCTIONS.md` — confirm it already handles cross-controller session exclusivity, or whether `KMPPiPManager`-adjacent global state is needed, before assuming it's automatic)

##### 15. Validation
Client mirrors server withdrawn-state checks but treats server as authoritative.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Audio fails to load/play | `AudioPlayerController`'s existing retry/error-state handling; fall back to a lower-bitrate source if configured |
| Mark-as-learned submission fails | Optimistic local update, queued via `SyncQueueEntity`, never blocks further interaction |
| Favorite toggle fails | Optimistic + retry |
| Dua withdrawn while open | Graceful "temporarily unavailable" + suggested alternative |

##### 19. Offline First
Remote → `DuaRepositoryImpl` → Room (`SafeDatabaseHelper`) → UI; mark-learned/favorite actions queue via `SyncQueueDao`/`SyncQueueEntity` (shared K-07 mechanism) when offline.

##### 21. Localization
Transliteration/translation independently localizable; Arabic locale-independent.

##### 22. RTL
Full RTL; Arabic text uses the established Naskh-style typeface from A.5 (confirm the exact `core/designsystem` token name for this typeface before referencing it as if already named).

##### 25. Security
No new sensitive data; standard bearer-token reuse.

##### 27. Testing
- Unit: optimistic-update/reconcile for mark-learned and favorite
- UI: all four elements present in the semantics tree on initial render
- UI: read-along highlight has an accessible sequential-exposure fallback
- **Always-free-tier UI regression** (CI-blocking signature test for this screen)
- Integration: confirm `AudioPlayerController`'s actual single-session behavior (verify, don't assume, per §11)

##### 31. Final Verification Checklist
- [ ] Uses real `AudioPlayerController`/`AudioPlayer`, not an invented player wrapper
- [ ] Uses Koin, not Hilt
- [ ] `client_request_id` used, not `client_event_id`
- [ ] Single-active-audio-session behavior confirmed (not assumed) against the real controller
- [ ] Always-free-tier UI regression test passes and is CI-blocking
- [ ] Offline outbox uses real `SyncQueueDao`/`SyncQueueEntity`, not an invented outbox table

#### `Development_Blueprints/A6_Dua_Learning/KMP/03-dua-recall-quiz-flow.md`

##### 4. Objective
Wire the Dua Card Detail screen's "Practice Quiz" entry point to `:core:quiz-engine`'s `QuizSessionScreen(context = QuizContext.DuaRecall, childId, sourceId = duaId)`, handle the returned `QuizResult`, and confirm (or, if missing, request as a coordination item) the engine's support for the two dua-specific PRD requirements: supportive-retry-with-full-dua-card, and "Question X of Y" omission when `total_available == 1`.

##### 5. Business Requirements
FR-6, FR-7; Edge Case 8. Per `A8-K01` §11: `QuizContext` already models per-context behavior, so these two requirements are plausibly already generic engine capabilities (e.g., a per-question "review content" slot) — **confirm against the engine's actual implementation before assuming a gap exists.**

##### 11. KMP Requirements
- "Practice Quiz" entry button disabled/secondary-styled until `learnedStatus` reflects a **server-confirmed** learned state (K-02's `DuaCardUiState`) — this gating logic lives in `feature:dua-learning`, upstream of the engine call, since the engine itself has no knowledge of dua-specific learned-state
- On tap, invoke `QuizSessionScreen(QuizContext.DuaRecall, childId, sourceId = duaId)`
- Handle `QuizResult(accuracyPercent, rewardGranted, conceptsTouched)` on return — `rewardGranted` likely already reflects A11's reward-ledger outcome (confirm against A8-K01's actual `QuizResult` semantics), meaning K-03 does not need to independently trigger any reward/badge UI beyond what the engine's result already communicates

##### 15. Validation
N/A directly.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Engine reports quiz-unavailable | Whatever generic state `:core:quiz-engine` already defines for this (confirm and reuse, don't invent a dua-specific "coming soon" message that duplicates it) |
| `QuizResult` callback never fires (user backs out) | Dua Card Detail screen simply re-renders in its prior state, no special handling needed |

##### 19. Offline First
Delegated to the engine's own offline-bundling mechanism (A8-KMP/06).

##### 21. Localization / 22. RTL
Inherited from the engine.

##### 25. Security
The actual `NOT_YET_LEARNED` security gate lives server-side (B-02/B-03), enforced by the engine's backend call — this file's only responsibility is not showing a falsely-enabled button before server confirmation (§11).

##### 27. Testing
- Unit: Practice Quiz button gating (server-confirmed only, never purely optimistic)
- Integration: full `QuizSessionScreen(QuizContext.DuaRecall, ...)` invocation → `QuizResult` handling
- **Confirm, via reading the engine's actual implementation once built**: counter-omission at `total_available == 1`, and supportive-retry-with-full-dua-card — if either is missing from the generic engine, file a coordination request with A8 rather than forking a dua-specific quiz screen

##### 31. Final Verification Checklist
- [ ] No dua-specific quiz question/retry screen built outside `:core:quiz-engine`
- [ ] `QuizContext.DuaRecall` + `sourceId=duaId` used correctly
- [ ] Practice Quiz button gated on server-confirmed state only
- [ ] Engine's counter-omission and supportive-retry capabilities confirmed (not assumed) — gap filed with A8 if missing
- [ ] `QuizResult` handled without re-deriving reward/badge state independently

#### `Development_Blueprints/A6_Dua_Learning/KMP/04-dua-master-badge-progress-celebration.md`

##### 4. Objective
Trigger `core/design-system`'s existing `BadgeUnlockModal` when the child's Dua Master badge is awarded (per B-05's real, A11-driven award flow), with `onDismiss` navigating back to the Dua Card/Catalog screen the child was on, per the modal's own documented dismiss contract ("dismiss always navigates the calling screen back to its own 'next step'").

##### 5. Business Requirements
FR-10; Edge Case 2 (stickiness — already guaranteed by A11's `child_badges` table, nothing to implement here).

##### 11. KMP Requirements
- Detect a new "Dua Master" badge award via A11's shared rewards client (confirm exact mechanism per §6, do not assume)
- Call `BadgeUnlockModal(badge = BadgeUiModel(...), onDismiss = { /* navigate per the modal's documented contract */ })`
- Deferred/queued trigger if the award happens while the child is on an unrelated screen — confirm whether A11's shared rewards client already handles this queuing generically (likely, given 4+ consumers) before building dua-specific queuing logic

##### 15. Validation
N/A beyond confirming the badge code/type matches "Dua Master" as configured in B-05/B-10's A11 admin setup.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Badge-progress signal arrives off-screen | Deferred per A11's shared client behavior (confirm, don't reinvent) |
| Rewards read API unavailable | Celebration simply doesn't trigger this session — non-critical, non-blocking |

##### 19. Offline First
N/A — live-state signal; deferred until online per A11's existing pattern.

##### 21. Localization / 22. RTL
Inherited from `BadgeUnlockModal`'s existing localization.

##### 24. Performance / 25. Security
N/A directly — inherited from A11's already-hardened shared components.

##### 27. Testing
- Unit: trigger-detection logic for a Dua Master award specifically (filtering A11's generic badge-award stream for this one badge code)
- Integration: `BadgeUnlockModal` renders correctly with dua-specific `BadgeUiModel` content, dismiss navigates correctly

##### 31. Final Verification Checklist
- [ ] No local badge celebration modal built — `BadgeUnlockModal` (A11-K09) reused directly
- [ ] Badge-award detection mechanism confirmed against A11's real shared client, not assumed
- [ ] Filter correctly isolates the "Dua Master" badge from A11's generic award stream
- [ ] Dismiss behavior matches the modal's documented contract

#### `Development_Blueprints/A6_Dua_Learning/KMP/05-habit-tracker-reminder-suggestion-integration.md`

##### 4. Objective
Show a dismissible inline suggestion card after server-confirmed mark-as-learned, deep-linking into A.7's real habit-creation flow pre-filled with the dua's reference, with per-dua dismissal persistence via the real datastore module.

##### 5. Business Requirements
FR-9; dismissed flag persists per dua but allows re-suggestion if no habit was ever created; Edge Case 11 (un-marking never deletes an existing habit — enforced by B-06 never emitting an "unlearned" event, nothing for this file to additionally guard against).

##### 11. KMP Requirements
- Card shown only after server-confirmed mark-as-learned (K-02's `DuaCardUiState`, not optimistic local state)
- Primary action calls `Navigator.navigateTo(NavigationAction.ToHabitCreation(prefill = duaId))` or A.7's actual real equivalent (Task 01)
- Dismissed flag persisted per-dua via `PreferenceManager`
- Re-suggestion allowed if child re-visits the dua's own detail screen and the habit was never actually created (requires A.7's habit-existence query — confirm it exists before assuming)

##### 15. Validation
N/A beyond dua_id validity (inherited from K-02's already-loaded context).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Deep-link into A.7 fails | Fallback to in-app navigation to the Habit Tracker tab via `Navigator` |
| Habit-existence check unavailable | Default to showing the suggestion (fail-open, since suppressing a valid suggestion is worse UX than an occasional redundant one) |

##### 19. Offline First
Dismissed-flag read/write works fully offline via `PreferenceManager`.

##### 21. Localization / 22. RTL
Suggestion copy fully localized, RTL-correct.

##### 25. Security
No new sensitive data; deep-link payload limited to a dua reference id.

##### 27. Testing
- Unit: dismissed-flag persistence and re-suggestion logic
- UI: card visibility across dismissed/never-created/eligible states
- Integration: mark-as-learned confirmation → card appears → deep link → A.7's real flow receives the correct prefill (verified against A.7's actual contract, not a mock of an assumed one)

##### 31. Final Verification Checklist
- [ ] A.7's real deep-link contract confirmed before implementation, not assumed
- [ ] Card shown only after server-confirmed mark-as-learned
- [ ] Dismissed flag suppresses repeats; re-suggestion works when habit never created
- [ ] Uses real `PreferenceManager`/`Navigator`, not invented placeholders

#### `Development_Blueprints/A6_Dua_Learning/KMP/06-dua-favorites-management.md`

##### 4. Objective
Ensure duas are correctly favoritable via B.14's shared toggle component and correctly discoverable via B.14's shared Favorites tab (type-filtered to `dua`), without building a parallel favorites list or toggle button.

##### 5. Business Requirements
FR-8; Edge Case 1, Edge Case 9 — all owned by B.14's shared implementation.

##### 11. KMP Requirements
- Mount B14-K01's shared toggle on the Dua Card and any dua list item
- Rely on B14-K02's shared Favorites tab for the dua-filtered favorites view — dua's own navigation entry to "Favorites" should route into that shared tab pre-filtered to `dua`, not a locally-built screen
- Withdrawn-favorited-dua handling ("temporarily unavailable") — confirm this is already generic in B14-K02 (likely, since it's the same shape of problem for Stories/Quran/Dua) before adding dua-specific handling

##### 15. Validation
N/A directly.

##### 18. Error Handling
Inherited from B.14's shared toggle/tab — no dua-specific error handling needed unless a gap is found.

##### 19. Offline First
Delegated entirely to B14-K03's `FavoritesRepository` offline-sync layer.

##### 21. Localization / 22. RTL
Inherited from B.14's shared components.

##### 25. Security
N/A directly.

##### 27. Testing
- Integration: favorite a dua via B14-K01's shared toggle → confirm it appears correctly in B14-K02's shared Favorites tab when filtered to `dua`
- Integration: withdraw a favorited dua → confirm B14-K02's existing unavailable-state handling covers it correctly

##### 31. Final Verification Checklist
- [ ] No local favorites list screen built — B14-K02's shared tab reused
- [ ] No local favorite toggle built — B14-K01's shared component reused
- [ ] Dua favorites correctly appear when filtering the shared tab to `content_type=dua`
- [ ] Withdrawn-favorite handling confirmed generic or coordinated, not duplicated

#### `Development_Blueprints/A6_Dua_Learning/KMP/07-offline-downloads-sync-dua-content.md`

##### 4. Objective
Make dua content downloadable and offline-playable via B.15's existing download-initiation/chunked-download/outbox-sync engine, scoped to `content_type=dua`, and ensure B-02's mark-as-learned/B-04's favorite-toggle actions route through B.15's real `SyncQueueDao`/`SyncQueueEntity`-based outbox (per `06-offline-progress-sync-outbox-integration.md`) rather than a dua-specific one.

##### 5. Business Requirements
FR-12; Edge Case 4 (offline quiz for a downloaded-and-learned dua — depends on `:core:quiz-engine`'s own offline bundling, A8-KMP/06, not something this file separately implements); Edge Case 5 (download-permission revocation doesn't remove existing downloads — B.15's existing policy, `B15_Offline_Downloads_Sync/Backend/03-entitlement-download-policy-enforcement-service.md`).

##### 11. KMP Requirements
- Download initiation for dua content uses B.15's existing entitlement-gated flow (K-01) — no dua-specific download-permission logic
- Downloaded dua fully functional offline: full card render + audio playback + bundled quiz (if `:core:quiz-engine`'s own offline mechanism includes it)
- Offline mark-as-learned/favorite queue via the real `SyncQueueDao`/`SyncQueueEntity`, synced on reconnect per B15-KMP/06's existing pattern

##### 15. Validation
N/A directly — inherited from B.15's engine.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Download failure | B.15's existing retry/backoff and failed-state UI |
| Non-downloaded dua accessed offline | "Connect to internet or download" affordance, consistent with B.15's existing pattern for other content types |
| Outbox sync failure | B.15's existing retry/backoff |

##### 19. Offline First
Entirely delegated to B.15's real engine; this file's only job is correct `content_type=dua` scoping.

##### 21. Localization / 22. RTL
Inherited from B.15's Downloads Manager UI, if a shared one exists (per `B15_Offline_Downloads_Sync/KMP/03-downloads-tab-inventory-management-ui.md`) — dua downloads should appear in that shared inventory UI, not a dua-specific downloads screen.

##### 25. Security
Inherited from B.15's entitlement-gated flow.

##### 27. Testing
- Integration: `content_type=dua` download initiates, downloads, and completes correctly through B.15's real engine
- Integration: offline mark-as-learned (B-02) queues via the real `SyncQueueEntity` and syncs exactly-once on reconnect via `client_request_id`
- Integration: download-permission revocation → existing dua downloads remain playable (B.15's existing policy, verified here as a dua-specific regression)

##### 31. Final Verification Checklist
- [ ] No dua-specific download engine/outbox built — B.15's real engine reused
- [ ] `SyncQueueDao`/`SyncQueueEntity` used for offline mark-learned/favorite queuing, not an invented outbox
- [ ] `DownloadRepository` (kmpplayer) vs. B.15-engine relationship clarified, not assumed
- [ ] Download-permission revocation behavior verified against B.15's real policy

#### `Development_Blueprints/A6_Dua_Learning/KMP/08-parent-dua-progress-view.md`

##### 4. Objective
Add a Duas entry to the existing Parent Area → Child Progress → Learning navigation, rendering B-07's concept-level progress data, following the same structural pattern as A5-KMP/12 and A8-KMP/07.

##### 5. Business Requirements
User story 9; empty state per PRD §1.12.

##### 11. KMP Requirements
- `ParentDuaProgressViewModel` fetches and exposes the concept-level list with `learned_status`, `learned_at`, `habit_reminder_linked`
- Multi-child selector reused from the existing Parent Area pattern
- Empty state per PRD §1.12
- Cached last-known state with staleness indicator on failure, via `SafeDatabaseHelper`

##### 15. Validation
N/A beyond existing child-selection validity.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| API failure | Cached last-known state with staleness indicator |
| Zero learned duas | Empty state per §1.12 |

##### 19. Offline First
Read-only cached rendering; no offline write actions originate from this screen.

##### 21. Localization / 22. RTL
Full localization/RTL for parent-facing copy.

##### 25. Security
No new sensitive surface; relies entirely on B-07's server-side family-membership enforcement.

##### 27. Testing
- Unit: ViewModel fetch/empty-state logic
- UI: empty and populated states
- Integration: API-failure fallback to cached state with staleness indicator

##### 31. Final Verification Checklist
- [ ] Reachable via Parent Area → Child Progress → Learning → Duas
- [ ] Empty state matches PRD copy
- [ ] Populated state shows `learned_status`/`learned_at`/habit-linkage
- [ ] API failure falls back to cached state with staleness indicator
- [ ] Reuses sibling components where genuinely generic, per Task 01's decision

#### `Development_Blueprints/A6_Dua_Learning/KMP/09-dynamic-category-metadata-rendering.md`

##### 4. Objective
Fetch category metadata (icon key, localized label, sort order) from B-11's real `GET /v1/dua/categories` instead of hardcoding it client-side, so an admin-added category (via N-04) renders correctly with zero app release.

##### 5. Business Requirements
PRD §4.2, §2.1.

##### 11. KMP Requirements
- `DuaCategoryMetadataRepositoryImpl.getCategories()` — cache-then-network via `SafeDatabaseHelper`
- `DuaCategoryIconResolver.resolve(iconKey: String): IconResource` — known-key mapping with a generic fallback, never throws
- Tiles render in `sort_order`; label rendered in active locale from the metadata payload

##### 15. Validation
`icon_key` resolution never throws — always resolves to a matched icon or the default fallback.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Fetch failure | Cached last-known metadata; if no cache exists (first launch, offline), a minimal built-in six-category fallback |
| Unrecognized `icon_key` | Generic default icon, correct label still shown |
| Missing label for active locale | Fall back to English |

##### 19. Offline First
Remote (B-11) → `DuaCategoryMetadataRepositoryImpl` → Room cache → UI.

##### 21. Localization
Fully data-driven per-locale labels from the API payload.

##### 22. RTL
Unchanged from K-01's existing RTL handling — only the data source changes.

##### 25. Security
No new sensitive data.

##### 27. Testing
- Unit: `DuaCategoryIconResolver` known/unknown key handling
- Unit: cache-then-network and offline-fallback-to-built-in-defaults logic
- UI: unrecognized `icon_key` renders the fallback, not a crash or blank tile
- Integration: a category added via N-04/B-11 renders correctly on next refresh without an app update

##### 31. Final Verification Checklist
- [ ] Category tiles render from real API metadata (B-11), not a hardcoded list
- [ ] Unrecognized `icon_key` falls back gracefully
- [ ] Offline cold-start falls back to a minimal built-in default set
- [ ] A category added via N-04/B-11 renders correctly without an app update
- [ ] Uses Koin, `core/network`, `core/database` — real classes, not placeholders

## A7 — Feature_A7_Habit_Tracker

PRD: `PRD_Documents/Child App (1-12)/Feature_A7_Habit_Tracker.md`

Coverage: 22 mandatory FR records; all preserved verbatim below. Feature has 21 inventory records including components/states. Components and states must not inflate independently executed screen count.

### Existing screenshot candidates

- `Screens/Mobile App/Habits/Habit Checklist-01.png` — visually inspected
- `Screens/Mobile App/Habits/Habit Checklist-02.png` — inventoried only
- `Screens/Mobile App/Habits/Noor Garden-01.png` — inventoried only
- `Screens/Mobile App/Habits/Noor Garden-02.png` — inventoried only
- `Screens/Mobile App/Habits/Streak Recovery-01.png` — inventoried only
- `Screens/Mobile App/Habits/Streak Recovery-02.png` — inventoried only

### Complete normative functional coverage

### 1.7 Functional Requirements

**FR-1** Habit Builder's "Today" view shows a checklist of the child's currently-configured habits: Salah (by prayer), Quran reading, daily duas, good deeds, dhikr counter, and optionally a Ramadan fasting tracker — scoped by parent configuration and child age (source §6.5, §21.14, screen catalog "Habit Builder").
**FR-2** Habit check-in is offline-first: local database updates immediately on tap; server sync and reward posting happen asynchronously (source §6.5 Detailed Workflow step 2: "Local database updates immediately (offline-first)").
**FR-3** Exactly one capped reward is granted per `(child_id, habit_id, local_date)` — repeated taps on the same habit on the same day do not farm additional XP/Noor Heroes Points (source §9.3 DB notes: "one capped habit reward per (child_id, habit_id, local_date)"; §6.5 "Rewards have daily caps to prevent farming").
**FR-4** Habit check-in events store: local date, timezone, source, an optional parent-verification flag, and an optional note category — sensitive personal notes are never required (source §6.5/§21.14).
**FR-5** Parent chooses which habits appear, scoped by child age (FR carried from §6.5/§21.14) — the child never sees a habit type the parent has not enabled for them.
**FR-6** Parent verification of a habit claim is **optional** per habit/child and must never be framed in copy or UI treatment as "religious policing" — verification is presented as supportive co-participation (e.g., "Mark this together"), never surveillance (source: hard ethical/copy constraint, §6.5/§screen-catalog).
**FR-7** Streak System implements the exact state machine: `Inactive → Active → AtRisk → Protected/Broken → Recovery → Active/Inactive` per the canonical diagram in §7.4/§21.13 (full transition table specified in §1.17 below) — this is the feature's most safety-critical logic and must be implemented exactly as specified, not approximated.
**FR-8** A "meaningful activity" counting toward a streak is: a completed lesson, a story watched past a minimum-engagement threshold, a quiz, or an approved habit check-in — repeated low-value taps never count (source §7.4/§21.13).
**FR-9** Calendar-day boundaries for streak evaluation use a **server-maintained child timezone**, not raw device-reported time, to resist trivial manipulation while still being fair to genuine travel (source §7.4).
**FR-10** Timezone changes and travel require bounded, abuse-resistant grace logic with server-side reconciliation — a streak must never be silently broken by a timezone shift alone (source §6.5 Error Handling, §21.13).
**FR-11** A "streak shield" (the `Protected` transition from `AtRisk`) is earned through learning/consistency, never purchasable with real money (source §7.4, §21.13 — a hard anti-monetization-of-grace rule).
**FR-12** Family Streak (Noor Garden): multiple children in the same family may contribute to a shared family streak/garden, but **individual sibling habit completion is never compared, ranked, or displayed competitively anywhere**, including in parent reports (source §6.5 Business Rules, §21.12 "Never rank siblings in parent reports" — applies platform-wide but is specifically enforced here at the point of data origin).
**FR-13** Broken-streak and missed-day messaging emphasizes returning, never failure or shame — no UI treatment (color, iconography, copy) may imply punishment (source §6.5/§7.4 Failure Scenario language).
**FR-14** Missed-habit pattern detection triggers a mercy-toned suggestion (smaller target, alternate time, or family reminder) — never a shaming message (source: screen catalog "Habit Builder" Navigation Flow rule; Habit Intelligence Model table "Missed habit pattern → Suggests a smaller target, alternate time, or family reminder. Prevents shame and helps parents coach gently").
**FR-15** Habit reminders respect family hours, bedtime, and parent quiet windows (source §6.5 Engagement Mechanics) — no reminder may fire during a configured quiet/bedtime window.
**FR-16** Dhikr Counter provides a gentle tactile interface, audio pronunciation support, and a daily target, distinct in interaction model from the simple checkbox-style habits (source §6.5 Habit Types).
**FR-17** Fasting Tracker (Ramadan/practice fasts) is optional and parent-controlled, with age-appropriate fasting education content linked (source §6.5 Habit Types, §6.5 "fasting tracker (optional, parent-controlled)").
**FR-18** Seasonal mode integration: when Ramadan mode is active, missions/habits switch to fasting, charity, Quran, dua, and family iftar reflections (source: Habit Intelligence Model table "Ramadan mode active → Switches missions to fasting, charity, Quran, dua, and family iftar reflections").
**FR-19** Noor Garden visual progression: each habit type grows a distinct part of a personal progress world (Quran tree, kindness flowers, Salah lanterns, dua stars, Ramadan moon path); siblings contribute to shared Family Garden milestones (e.g., 100 duas, 30 good deeds, 7 family story nights, a complete Ramadan journey) (source §"Noor Garden Progress World").
**FR-20** Habit check-in is idempotent via `client_request_id`; offline check-ins sync in causal order with server-side deduplication.
**FR-21** Weekly habit reports (parent-facing) use child-friendly highlights framing, not raw failure/success scorecards, and never rank siblings (source §6.5 Engagement Mechanics, cross-ref FR-12/FR-13).
**FR-22** Churn-risk detection (declining habit engagement trend) triggers encouragement-oriented interventions, never pressure-oriented ones (source §6.5 Engagement Mechanics "Churn-risk detection that triggers encouragement, not pressure").

### Ordered source inventory

### 1.18 Screen Inventory (Complete — Zero Missing)

| # | Screen / Component | Type | Entry Points | Exit Points |
|---|---|---|---|---|
| 1 | Habit Builder — Today's Checklist | Primary | Home habit widget, bottom-nav/Learn-adjacent entry, deep links | Streak Calendar, Noor Garden, individual habit detail interactions |
| 2 | Habit Check-In Inline Interaction (per habit row) | Component | Today's Checklist | Streak/XP update in place |
| 3 | Dhikr Counter Screen | Screen | Today's Checklist (dhikr habit tap) | Today's Checklist (progress updated) |
| 4 | Fasting Tracker (Ramadan/practice) | Screen | Today's Checklist (if parent-enabled) | Today's Checklist |
| 5 | Good Deed Logging — Category Selector | Modal/Sheet | Today's Checklist (good deed habit tap) | Optional Note entry / direct check-in |
| 6 | Good Deed Optional Note Entry | Screen variant | Category Selector | Check-in confirmation |
| 7 | Streak Calendar / History View | Screen | Today's Checklist "view streak history" | Today's Checklist |
| 8 | Streak State Detail (AtRisk/Broken/Recovery messaging) | Component/Screen variant | Streak Calendar, Today's Checklist banner | Recovery Mission entry, dismiss |
| 9 | Recovery Mission Screen | Screen | Streak State Detail (Broken → Recovery) | Today's Checklist (streak restored to Active) |
| 10 | Mercy-Toned Smaller-Target Suggestion Prompt | Modal | Missed-habit pattern detected | Accept (adjusts target) / Dismiss |
| 11 | Noor Garden — Personal View | Screen | Today's Checklist "Open Noor Garden" | Family Garden (if applicable), Avatar (A.9) |
| 12 | Noor Garden — Family View | Screen | Personal Garden entry point | Personal Garden |
| 13 | Family Streak Milestone Celebration | Modal | Family threshold crossed | Dismiss → Family Garden |
| 14 | Habit Reminder Settings (per-child, Parent Area) | Screen (Parent Area, cross-ref C.23) | Parent Controls | Saves configuration |
| 15 | Habit Visibility/Age-Scoping Configuration (Parent Area) | Screen (Parent Area) | Parent Controls → Children | Saves configuration |
| 16 | Parent Verification Pending Item (Parent Dashboard widget) | Component (Parent Area) | Parent Dashboard | Verification confirm action |
| 17 | Weekly Habit Report (Parent Area) | Screen (Parent Area) | Parent Dashboard → Child Progress → Habits | Habit Detail Drill-in |
| 18 | Weekly Habit Report — Per-Habit Detail | Screen (Parent Area) | Weekly Habit Report | Back |
| 19 | Empty State — No Habits Configured Yet | Screen variant | Today's Checklist, zero habits | Parent setup deep link |
| 20 | Empty State — No Streak History Yet | Screen variant | Streak Calendar, first-time | N/A |
| 21 | Ramadan Mode Checklist Variant | Screen variant | Today's Checklist, Ramadan mode active | Standard checklist (post-Ramadan) |

### Exact mobile UX and behavior sources

### 1.9 Acceptance Criteria

- Given a child checks in the same habit twice in one local day, when the second check-in is submitted, then no additional XP/Noor Heroes Points are awarded, and the system records this gracefully (not as an error).
- Given a child's streak is in `Active` state and they complete a meaningful activity the next eligible local day, when evaluated, then the streak remains `Active` and increments — given they do nothing that day and the day closes, then it transitions to `AtRisk` and then `Broken` per the state machine, never skipping states.
- Given a streak is `Broken`, when the child returns and engages, then it enters `Recovery`; completing a recovery mission returns it to `Active`; the recovery window expiring without completion returns it to `Inactive` — never silently jumping straight back to a high `Active` count.
- Given a child travels and their device timezone changes mid-streak, when the server evaluates the day boundary, then bounded grace logic applies and the streak is not silently broken purely due to the timezone shift, per a server-side reconciliation rule (not an oracle — abuse-resistant bounds apply).
- Given two siblings in the same family both have habit data, when a parent views any report screen, then no UI element compares, ranks, or juxtaposes their individual completion rates competitively — this must be verified across every parent-facing report screen, not just the primary dashboard.
- Given a parent has not enabled the Fasting Tracker for a child, when that child opens Habit Builder, then no fasting-related habit type appears in their checklist.
- Given a missed-habit pattern is detected for a child, when the system responds, then the suggestion shown is a smaller target, alternate time, or family reminder — never a message implying failure or guilt.
- Given Ramadan mode is active, when a child opens Habit Builder, then the checklist reflects Ramadan-relevant habits (fasting, charity, Quran, dua, family iftar reflection) rather than the standard year-round set.

### 1.10 Edge Cases

1. Child checks in a habit at 11:58pm local time, and the check-in's server-processing completes at 12:01am due to a slow network request → the `local_date` recorded must reflect the time of the **client-side check-in action** (captured client-side at tap time and sent in the request payload), not the server's processing timestamp, to avoid an unfair day-boundary mismatch.
2. Child rapidly taps a habit checkbox on/off multiple times before the request completes (accidental double-tap or indecision) → idempotent handling via `client_request_id` per distinct intended state ensures the final persisted state matches the child's last intended action, without duplicate reward issuance and without a flickering UI.
3. Parent disables a previously-visible habit type while the child has an active streak partially built on that habit type → the historical streak/reward data for that habit is preserved (not deleted), but it's removed from today's checklist going forward; if the disabled habit was the sole contributor to an active daily streak chain, the streak's continuation now depends on other still-enabled habits or a different meaningful activity, evaluated fairly (the child isn't penalized retroactively for the parent's configuration change).
4. Two children share a device; Child A checks in a habit, then the device switches to Child B before Child A's offline check-in has synced → the queued offline check-in remains correctly attributed to Child A's `child_id` (captured at action time, not sync time) and syncs correctly regardless of which child's session is currently active when connectivity returns.
5. Family Streak threshold is met by the combined effort of multiple siblings on the same day, but one sibling's individual check-in event hasn't synced yet (still offline) → the Family Streak's authoritative server-side evaluation only counts confirmed, synced check-ins; the family reward/milestone fires once that sibling's event syncs and crosses the threshold (no premature/optimistic family-level reward issuance based on unconfirmed client state).
6. Child sets up a recurring Dhikr Counter target, then changes the target mid-day after having already partially completed today's count → today's progress is preserved proportionally against the new target (not reset to zero), with a sensible recalculation (e.g., if they did 50 of an old 100 target and change to a new 150 target, they're now at 50/150, not back to 0/150).
7. A child's account is flagged for Mercy Day usage many days in a row (e.g., genuinely inconsistent engagement rather than occasional grace) → the system does not editorialize or "punish" this pattern through any UI signal, but the Habit Intelligence Model's missed-pattern detection (FR-14) may still surface a gentle, supportive suggestion — this is fundamentally different from any punitive escalation, and the distinction must be preserved in implementation (suggestion frequency may increase, tone never sharpens).
8. Parent enables "parent verification" for a habit, but is unavailable/offline for an extended period and never verifies a pending claim → the child's own streak/reward progress is **not blocked** waiting on parent verification (verification is supplementary/optional context for the parent, never a gate on the child's actual reward/streak mechanics) — this must be true even though FR-6 allows verification to exist, since verification is "optional" precisely in this sense.
9. Ramadan mode activates mid-cycle while a child has an active non-Ramadan streak → the streak doesn't reset; "meaningful activity" eligibility simply expands to include the newly-relevant Ramadan-specific habit types for that period, then reverts appropriately when Ramadan mode ends (no streak discontinuity purely due to the seasonal mode switch).
10. A child attempts to log an excessive number of "good deeds" in a single day (e.g., 50 taps) in an apparent attempt to inflate engagement metrics or test the system → the daily cap (FR-3) limits actual reward issuance to the configured cap regardless of tap count, and an anomalous-volume pattern may be flagged for fraud/abuse monitoring (not shown to the child as an error — the excess taps simply don't yield additional reward, framed neutrally).
11. Child's server-maintained timezone record becomes stale/incorrect (e.g., they moved permanently to a new timezone months ago but the system never updated) → there must be a mechanism (automatic detection via repeated device-timezone-mismatch signals, or explicit parent/child confirmation) to update the server-maintained timezone of record without requiring a manual support ticket for every case, while still being resistant to abuse (frequent flip-flopping triggers a different, more conservative grace path than a single stable shift).
12. A habit check-in attempt is made for a `local_date` significantly in the past (e.g., backfilling after being offline for several days while traveling with no connectivity at all) → the system must support reconciling a batch of queued historical check-ins on reconnect, each evaluated against its own correct historical `local_date`, with the streak state machine re-computed correctly across the gap (not just blindly applied as if it were "today") — this is a more complex version of the standard offline-sync pattern, specific to a calendar-day-sensitive feature.

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Habit check-in sync fails (network) | Local state already updated (offline-first); background retry with exponential backoff; never shown as a child-facing error, since the local experience already succeeded |
| Streak state-machine evaluation service unavailable | Last-known cached streak display shown with no alarming "error" framing; recalculated once the service is reachable, never silently reset to zero as a fallback |
| Family Streak aggregation service degraded | Personal/individual habit check-ins and rewards proceed unaffected; Family Garden visual simply doesn't update until the aggregation service recovers, shown as a gentle "growing..." state rather than an error |
| Dhikr Counter audio pronunciation asset fails to load | Counter still fully functional without audio (silent tactile counting), audio retried in background |
| Backfilled historical check-in conflicts with an already-recorded entry for that date | Idempotent merge — existing entry wins, no duplicate reward, no error shown |
| Parent verification request fails to deliver/notify parent | Child's progress is entirely unaffected (per Edge Case 8); parent sees the pending-verification item next time they open the relevant screen, no urgency-framed error |

### 1.12 Empty States
- New child, zero habits configured by parent yet → Habit Builder shows a friendly "ask a grown-up to set up your first habit" prompt with a parent deep-link (consistent with A.2 Edge Case 9).
- Zero streak history yet → Streak display shows a warm "Let's start your first day!" framing rather than a "0" presented starkly.
- Family Garden with zero family-level milestones reached yet → shows the garden's "seedling" starting state with a description of the first milestone to work toward.

### 1.13 Loading States
- Habit checklist: skeleton checklist shimmer (rare given offline-first design — mostly relevant on true first load).
- Streak calendar: skeleton calendar grid.

### 1.14 Offline States
- Full offline check-in functionality per FR-2; persistent (non-alarming) "syncing..." indicator when there's a pending local queue.
- Dhikr Counter and other purely-local-interaction habit types function identically offline.

### 1.15 Permission States
- No new runtime permissions; relies on existing notification permission (shared with A.12) for habit reminders.

### 1.16 User Flow (Narrative)

Child opens Habit Builder (via Home widget or bottom-nav, if surfaced there) → sees Today's checklist scoped to parent-enabled habit types for their age → taps to check in a habit (instant local feedback) → streak/XP updates optimistically, reconciled with server in background → views Streak Calendar/history or Noor Garden visualization → if a day was missed, sees mercy-toned messaging and a smaller-target suggestion rather than a broken-streak penalty screen → if part of a multi-child family, sees Family Garden progress (without sibling comparison) → may request a parent-verification co-marking for a specific habit if that's been enabled.

### 2.1 Habit-Specific Design System Extensions

- **Streak Visual Language:** Consistent with A.5's `Needs Refresh` treatment philosophy — streak risk/broken states use warm amber/gentle iconography (a softly dimming flame or a gentle moon-phase motif), never red/alarming. `Protected` state shows a small shield-glow accent. `Recovery` state uses a distinct "welcome back" warm visual, not a "penalty box" treatment.
- **Noor Garden Illustration System:** A cohesive, evolving illustrated garden scene — Quran tree, kindness flowers, Salah lanterns, dua stars, Ramadan moon path — each growing incrementally with habit consistency, rendered as a single composed scene (not separate disconnected icons), reinforcing the "you're growing something real" metaphor.
- **No-Comparison Enforcement (Design Principle):** Every component used in any parent-facing multi-child report context (Weekly Habit Report, Family Garden) is designed as either (a) an aggregate-only view (combined family totals, no per-child breakdown side-by-side) or (b) a single-child-at-a-time view requiring an explicit child-switcher tap (never a simultaneous side-by-side comparison layout) — this is a structural design constraint, not just a content-writing guideline.
- **Dhikr Counter Interaction:** Large, satisfying single-tap target (oversized relative to standard buttons, ≥72dp) with a gentle haptic pulse per tap (where platform supports it) and a soft incrementing count display — designed to feel meditative, not game-like/frantic.

### 2.2 Screen-Level Design Requirements (Key Screens)

#### Screen: Habit Builder — Today's Checklist

- **Purpose:** Frictionless daily logging of configured habits.
- **Components:** Date header, per-habit checklist rows (icon + label + large tap-target checkbox, or a count-based mini-display for Dhikr), streak summary chip, "View Streak History" and "Open Noor Garden" links.
- **States:** Default, All-complete-today (celebratory but calm acknowledgment, not over-the-top), Partial, Mercy-Day-active (a gentle distinct banner, not hidden, but framed supportively), Offline (small persistent indicator), Empty (zero habits configured).
- **Accessibility:** Each checklist row fully labeled including current state ("Fajr prayer, not yet checked in today"); Dhikr Counter's large tap target has an additional smaller decrement/reset control reachable via standard navigation, not gesture-only.
- **Responsive Rules:** Single column list on mobile; tablet may show checklist alongside a persistent Noor Garden preview panel.

#### Screen: Streak State Detail (Broken/Recovery messaging)

- **Purpose:** Communicate a missed streak and a path forward without shame.
- **Components:** Warm, non-alarming illustration (e.g., a softly glowing garden at dusk rather than a wilted/dead plant — even visual metaphors must avoid implying failure), supportive copy ("Let's pick this back up together!"), a clear single "Start Recovery" or "Try a Smaller Goal" CTA.
- **States:** AtRisk-warning (gentle, time-remaining-today framing), Broken-transition (the moment of transition, softest possible framing), Recovery-active, Recovery-window-closing-soon (gentle nudge, not a countdown-pressure timer).

#### Screen: Noor Garden (Personal & Family)

- **Purpose:** Visualize cumulative habit consistency as a living, growing world.
- **Components:** Layered illustrated scene with distinct zones per habit type, a subtle "last grew on [date]" indicator, Family Garden toggle (if applicable) showing combined-only progress.
- **States:** Seedling (new/low activity), Growing, Flourishing, Family-milestone-celebration overlay.

### 2.3 Tab Structure

Habit Builder is reachable from Home (Tab 1) and is itself part of the bottom-nav structure per some navigation maps as its own entry, or nested under Learn depending on the IA decision already reflected elsewhere in the blueprint — this document assumes Home-widget + a dedicated reachable screen (not necessarily its own bottom-nav tab, consistent with the 5-tab structure: Home/Learn/Stories/Rewards/Profile, where Habit Builder is most naturally reached via Home and via a Rewards-adjacent "Garden" entry point). Click mapping:

| Click Target | Destination | API Called | Analytics Event | Permission Check | Error Handling |
|---|---|---|---|---|---|
| Habit checklist row | Inline check-in | `POST /v1/habits/check-ins` | `habit_checked_in` | None | Optimistic + offline queue |
| Dhikr counter tap | Inline increment | `POST /v1/habits/check-ins` (batched/throttled, not per-tap) | `dhikr_target_reached` (on completion only) | None | Fully offline-capable |
| "View Streak History" | Streak Calendar | `GET /v1/habits/streaks/{child_id}` | N/A (view, implicit) | None | Cached fallback |
| "Open Noor Garden" | Noor Garden screen | `GET /v1/habits/garden/{child_id}` | `noor_garden_viewed` | None | Cached fallback |
| Mercy suggestion "Accept" | Adjusts habit target inline | `PATCH /v1/habits/{habit_id}/target` | `mercy_suggestion_accepted` | None | Optimistic + retry |

### 2.4 Wireframe Description (Composite)

Today's Checklist: a simple vertical list, consistent with the platform's general "checklist card" pattern (similar density to Daily Quiz's results list), with the Dhikr Counter rendered as a visually distinct, larger interactive card rather than a simple checkbox row given its different interaction model. Noor Garden: a full-bleed illustrated scene screen, more visual/immersive than list-based screens elsewhere, intentionally evoking a "place you visit" feeling rather than a "data screen."

### 2.5 Screen Image Generation Prompts

**Screen: Habit Builder — Today's Checklist**
- *Prompt 1 (English):* "Mobile app daily habit checklist screen UI mockup for a children's Islamic app. Warm off-white background. A date header at top, below it a vertical list of rounded checklist rows, each with a small friendly icon (a lantern for prayer, an open book for Quran, a small star for dua, a heart for good deeds) and a label, with a large rounded checkbox on the right side of each row — some checked with a soft gold checkmark, some unchecked outlined in teal. One larger, visually distinct card near the bottom for a dhikr counter showing a big circular tap button with a number count inside it. A small streak-summary chip near the top showing a simple flame-free icon (a small glowing lantern instead) with a number. Warm, calm, encouraging aesthetic, rounded shapes, soft shadows, no realistic human faces, bottom navigation visible."
- *Prompt 2 (Arabic RTL):* "نفس شاشة قائمة العادات اليومية لتطبيق إسلامي للأطفال، بتخطيط من اليمين إلى اليسار بالكامل. خلفية بيج فاتح دافئ. رأس بالتاريخ في الأعلى، وتحته قائمة عمودية من صفوف اختيار مستديرة الزوايا، كل منها بأيقونة صغيرة ودودة (فانوس للصلاة، كتاب مفتوح للقرآن، نجمة صغيرة للدعاء، قلب للأعمال الطيبة) وتسمية، مع مربع اختيار كبير مستدير على الجانب الأيسر من كل صف — بعضها معلّم بصح ذهبي ناعم، وبعضها غير معلّم بحدود فيروزية. بطاقة أكبر ومميزة بصريًا قرب الأسفل لعداد الذكر تعرض زر ضغط دائري كبير برقم العد في داخله. شريحة ملخص صغيرة للمتتالية قرب الأعلى تعرض أيقونة فانوس متوهج بسيطة (بدلاً من اللهب) مع رقم. طابع دافئ وهادئ ومشجع، أشكال مستديرة، ظلال خفيفة، بدون وجوه بشرية واقعية، شريط تنقل سفلي ظاهر."

**Screen: Noor Garden (Personal View)**
- *Prompt 1 (English):* "Mobile app full-screen illustrated progress-world UI mockup for a children's app, depicting a peaceful, lush garden scene viewed from a gentle isometric angle. Distinct zones within the garden: a small flourishing tree with leaves shaped subtly like open book pages (representing Quran progress), soft glowing lantern-shaped flowers along a path (representing prayer), small star-shaped blossoms (representing dua), and gentle kindness-themed flowers in warm pink and gold tones. Warm sunset-toned sky gradient in the background, soft clouds, no realistic human faces or figures, a small treasure-chest-like glowing marker indicating the next milestone to grow toward. Calm, magical, rewarding visual tone, rounded organic shapes, soft lighting, gentle color palette of teals, golds, and soft greens."
- *Prompt 2 (Arabic RTL):* "نفس واجهة عالم التقدم المصور بملء الشاشة لتطبيق أطفال، بتخطيط من اليمين إلى اليسار للعناصر النصية، يصور مشهد حديقة هادئة وخصبة من زاوية متباعدة لطيفة. مناطق مميزة داخل الحديقة: شجرة صغيرة مزهرة بأوراق تشبه بشكل خفي صفحات كتاب مفتوح (تمثل تقدم القرآن)، أزهار على شكل فوانيس متوهجة بلطف على طول المسار (تمثل الصلاة)، أزهار صغيرة على شكل نجوم (تمثل الدعاء)، وأزهار لطيفة بألوان وردية وذهبية دافئة تمثل الأعمال الطيبة. سماء بتدرج لوني يشبه غروب الشمس في الخلفية، غيوم ناعمة، بدون وجوه بشرية أو شخصيات واقعية، علامة متوهجة صغيرة تشبه صندوق كنز تشير إلى الإنجاز التالي المراد الوصول إليه. طابع بصري هادئ وسحري ومُجزٍ، أشكال عضوية مستديرة، إضاءة ناعمة، لوحة ألوان هادئة من الفيروزي والذهبي والأخضر الناعم."

*(Remaining screens — Streak Calendar, Recovery Mission, Mercy Suggestion Prompt, Family Garden, Dhikr Counter detail, Weekly Habit Report — follow the same two-prompt EN/AR template using these tokens; full set available on request.)*

---

### 6.1 Technical Requirements
Kotlin, Jetpack Compose, MVVM, Clean Architecture, module `:feature:habits`, depends on `:core:design-system`, `:core:network`, `:core:offline-cache`.

### 6.2 Screen Mapping
Each screen in §1.18 maps to a Composable; `HabitChecklistViewModel` exposes per-row optimistic state independent of overall screen loading state (consistent with A.2's per-section independence pattern).

### 6.3 Navigation Flow
Reachable from Home (deep link) and a dedicated nav-graph entry; Noor Garden and Streak Calendar are sibling destinations off the main Habit Builder screen.

### 6.4 State Management
`HabitChecklistViewModel` captures `local_date` and `timezone` at the exact moment of the check-in tap (using the device's current locale-date and `TimeZone.getDefault()`), embedding both directly into the outgoing request — never recomputed later at sync time, consistent with the backend's client-trusted-`local_date` design (§5 item 2). Offline check-ins are queued in a local Room outbox keyed by `client_request_id`.

### 6.5 API Mapping
`HabitRepository.checkIn()` → `POST /v1/habits/check-ins`; `HabitRepository.getGarden()` → `GET /v1/habits/garden/{child_id}`, with the response DTO's Kotlin data class **structurally having no per-sibling field** (mirroring the backend's schema guarantee on the client side too, so even a hypothetical malicious/buggy server response extension couldn't be rendered by a client that has no field to deserialize it into).

### 6.6 Analytics Mapping
`HabitAnalytics` fires `habit_checked_in` once per genuine new check-in (not on duplicate-ignored taps, which fire a distinct `habit_checkin_duplicate_ignored` event instead, sourced from the server's response indicating whether this was a fresh check-in or an idempotent replay).

### 6.7 Offline Support
Local Room outbox for check-ins, Dhikr Counter progress, and good-deed logs; WorkManager-backed sync on reconnect, processing queued items in chronological `local_date` order to ensure correct streak-state recomputation server-side (Edge Case 12).

### 6.8 Deep Linking
`noorheroes://habits`, `noorheroes://habits/garden`, `noorheroes://habits/streak-risk` (notification entry point).

### 6.9 Push Notifications
Landing targets for streak-risk and habit-reminder notifications (owned by A.12); this feature owns the deep-link destinations and the quiet-hours/bedtime-window suppression logic is enforced server-side by the Notification Service, not duplicated client-side.

### 6.10 Testing Strategy
- Unit: Streak state-machine client-side *display* logic (render-only, mirrors server state, never independently computes transitions); Dhikr target-change proportional-preservation calculation (Edge Case 6).
- UI tests: Mercy-toned messaging screens never contain shaming language (a Compose UI test scanning text nodes against a blocklist of negative-framing terms: "fail", "broke", "lost"); Family Garden screen renders with zero per-child comparative UI elements (structural UI test mirroring the backend's schema guarantee).
- Integration: full offline check-in → backgrounded → reconnect → correct streak recomputation flow, including a multi-day-gap backfill scenario.

---

### 13.1 Test Plan Summary
Coverage spans: reward-farming prevention (signature test), streak state-machine exhaustive correctness, timezone/travel grace logic, no-sibling-comparison structural guarantee, mercy-toned messaging content-safety, and all 12 edge cases from §1.10.

### 13.2 Test Cases — Happy Path
1. Child checks in all configured habits for the day → daily streak increments, Noor Garden grows, no duplicate rewards on accidental re-taps.
2. Child misses a day, returns the next day → streak transitions Broken → Recovery; completing a recovery mission returns it to Active.
3. Two siblings each check in habits on the same day, contributing to a Family Garden milestone → milestone reached, no comparative breakdown shown anywhere to the parent.

### 13.3 Edge Cases
All 12 items from §1.10.

### 13.4 Negative Cases
- Fire 10 concurrent identical check-in requests → exactly one `habit_log` row and one reward grant.
- Attempt to construct an admin Habit Report template containing a per-sibling comparison pattern → blocked by the linter.
- Attempt to read the Family Garden API response and look for any `child_id`-bearing field → none exists.
- Submit a check-in with `local_date` 30 days in the past → rejected per the bounded backfill window; submit one 10 days in the past → accepted.
- Simulate 6 timezone changes within 30 days for one child → conservative grace window applied on the next at-risk evaluation, distinct from the generous single-change path.

### 13.5 Regression Cases
Full Habit Tracker suite re-run on every release touching `:feature:habits`, the Habit/Streak/Family Aggregation Services, or the shared Reward/Notification Services.

### 13.6 Automation Cases
End-to-end: full multi-day streak journey including a deliberate miss-and-recovery cycle (using the staging time-travel utility per §10); offline multi-day backfill sync with correct chronological-order processing; mercy-toned-copy content-safety scan across all published locale strings (CI-blocking, run on every relevant content-string change).

---

### Corresponding KMP blueprint requirements

#### `Development_Blueprints/A7_Habit_Tracker/KMP/01-habit-builder-todays-checklist-experience.md`

##### 4. Objective
Build the Habit Builder screen rendering today's checklist, with `HabitChecklistViewModel` capturing `local_date`/`timezone` synchronously at tap time and per-row independent optimistic state, backing FR-1, FR-2, FR-5.

##### 5. Business Requirements
- Show only parent-enabled, age-appropriate habits (FR-5), scoped by B-01's `GET /v1/habits`.
- Tap-to-local-update latency < 100ms (NFR Performance) — instantaneous optimistic feedback.
- Each row's optimistic state is independent — tapping one habit must not disable/loading-state any other row.
- Default, all-complete (calm celebratory), partial, Mercy-Day-active, offline, and empty states all rendered distinctly.
- Full accessibility labeling per row including current check-in state.

##### 11. KMP Requirements
- `HabitChecklistViewModel` captures `LocalDate.now()`/`TimeZone.currentSystemDefault()` (kotlinx-datetime, multiplatform-correct API — not `java.time`/`TimeZone.getDefault()` which are JVM/Android-only) **synchronously in the tap handler**, not in a later coroutine that could execute after a delay.
- Per-row optimistic state via `Map<habitId, RowState>` in `HabitChecklistUiState`, not a screen-wide loading flag.
- Streak summary chip, "View Streak History" (→ K-04) and "Open Noor Garden" (→ K-05) navigation via `Navigator`.
- Tablet layout with persistent Noor Garden preview panel (responsive Compose layout).
- Full accessibility labeling: "Fajr prayer, not yet checked in today" pattern per row.

##### 15. Validation
Unit test using a fake `Clock`/`TimeZone` provider that advances time between tap and request-send, asserting the request payload reflects tap-time date, not send-time date (mandatory, per PRD §7 Android prompt item 1).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Network failure on catalog load | Show cached `habit_catalog_cache` with a small persistent offline indicator |
| Zero habits configured | Friendly "ask a grown-up to set up your first habit" empty state with parent deep link |
| Check-in tap while offline | Delegated to K-06's outbox; row shows optimistic-pending state, not an error |

##### 19. Offline First
Catalog read is cached locally (§14); check-in writes are fully offline-capable via K-06's outbox — this screen only owns the optimistic-UI and cached-read behavior, not the outbox mechanics itself.

##### 21. Localization
Habit labels resolved via string resources / backend-provided translation keys (English, Hindi, Arabic, Urdu) — no hardcoded user-facing strings.

##### 22. RTL
Checklist row layout (icon + label + checkbox) mirrors correctly; verified via a dedicated RTL layout test.

##### 25. Security
No new sensitive data handling at this layer.

##### 27. Testing
- Unit: fake-clock tap-time capture test (mandatory).
- Unit: per-row independent optimistic state (tapping one row doesn't affect another's `RowState`).
- UI: empty state, all-complete state, offline indicator rendering.
- Accessibility: row content-description correctness test.

##### 31. Final Verification Checklist
- [ ] `feature-habits`/`feature-habits-domain` modules scaffolded and DI-wired
- [ ] Tap-time `LocalDate`/`TimeZone` capture is synchronous (fake-clock test passes)
- [ ] Per-row optimistic state independent (no whole-list recomposition on single tap)
- [ ] All documented states (default, all-complete, partial, Mercy-Day, offline, empty) render correctly
- [ ] Accessibility labels correct per row
- [ ] Localization (EN/HI/AR/UR) and RTL verified
- [ ] Analytics events wired via `AnalyticsTracker`
- [ ] Existing `feature/home`/`feature/dua-learning` habit code flagged for follow-up refactor, not silently duplicated

#### `Development_Blueprints/A7_Habit_Tracker/KMP/02-dhikr-counter-interaction-target-adjustment.md`

##### 4. Objective
Build the Dhikr Counter screen with a large tap target, gentle haptic pulse, batched/throttled submission, audio pronunciation support, and proportional target-change recalculation (Edge Case 6).

##### 5. Business Requirements
- Large tap-target (≥72dp), gentle haptic pulse where platform supports it, meditative not game-like interaction (PRD §2.1).
- Non-gesture accessibility alternative (decrement/reset reachable via standard navigation).
- Batch/throttle count submission — not a network call per tap (PRD §2.3 click-mapping table).
- Audio pronunciation support with graceful silent fallback if the asset fails to load.
- Target change mid-day preserves progress proportionally, capping at new target if smaller (Edge Case 6).

##### 11. KMP Requirements
- Large circular tap button with count display, haptic pulse per tap.
- Local count accumulation; batched submission to backend (throttled, not per-tap network call).
- Audio pronunciation asset load with silent tactile fallback on failure, background retry.
- Non-gesture accessible decrement/reset control.
- Target-change proportional recalculation matching B-05's server formula exactly, applied optimistically client-side.

##### 15. Validation
Unit test for proportional recalculation: 50/100 → target 150 → 50/150 (unchanged); 80/100 → target 50 → capped at 50/50 "target reached" (mandatory boundary case per PRD §7 Android prompt item 6).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Audio asset fails to load | Counter remains fully functional (silent tactile counting); background retry |
| Batched sync fails | Local count preserved; retried via K-06's outbox pattern |
| Target change fails to sync | Local optimistic recalculation stands; retried in background |

##### 19. Offline First
Fully offline-capable — local count accumulation and target-change math work without connectivity; sync is opportunistic/batched.

##### 21. Localization
Dhikr text/audio pronunciation assets localized per supported language; count display uses locale-correct number formatting.

##### 22. RTL
Large tap target and count display mirror correctly; decrement/reset control position verified for RTL.

##### 25. Security
No elevated risk; standard local-cache handling.

##### 27. Testing
- Unit: proportional recalculation formula, both directions (mandatory).
- UI: large-tap-target accessibility test, non-gesture alternative control test.
- Integration: audio-fallback behavior, batched-sync-failure retry behavior.

##### 31. Final Verification Checklist
- [ ] Large tap target (≥72dp) with haptic pulse implemented
- [ ] Non-gesture accessible decrement/reset control present
- [ ] Batched/throttled submission, not per-tap network calls
- [ ] Audio pronunciation fallback verified
- [ ] Proportional target recalculation correct in both directions (mandatory test)
- [ ] Fully offline-capable local counting
- [ ] Localization and RTL verified
- [ ] Analytics events wired

#### `Development_Blueprints/A7_Habit_Tracker/KMP/03-good-deed-logging-fasting-tracker-flow.md`

##### 4. Objective
Build the Good Deed category selector + optional note entry, and the Fasting Tracker screen (parent-enabled only), backing FR-4 and FR-17.

##### 5. Business Requirements
- Good deed note is always optional, never required (FR-4).
- Fasting Tracker only renders if parent-enabled for the child (FR-17), with linked age-appropriate fasting education content.
- Both flows fully offline-capable for logging.

##### 11. KMP Requirements
- Category selector as a Modal/Sheet on good-deed habit tap.
- Optional note entry screen, clearly skippable (no forced text field).
- Fasting Tracker screen only rendered when `fasting_tracker_enabled=true` in the catalog response; linked fasting-education content entry point.
- Both flows check in via the standard `CheckInHabitUseCase` (K-01) with the appropriate `note_category`.

##### 15. Validation
Test asserting the note entry screen can be skipped/dismissed without blocking check-in completion.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Good deed check-in offline | Queued via K-06 outbox, same as any other habit type |
| Fasting habit not enabled | Screen/row simply absent, not shown-then-blocked |
| Fasting education content fails to load | Fasting check-in still functional; content shown as unavailable with retry, not a blocking error |

##### 19. Offline First
Both flows fully offline-capable for the check-in action itself, per K-06's shared outbox mechanism.

##### 21. Localization
Good-deed category labels and fasting-education content fully localized (EN/HI/AR/UR).

##### 22. RTL
Category selector grid/list and note entry field mirror correctly.

##### 25. Security
Optional note content is standard child-generated content, not specially sensitive; never required, minimizing collection by design (FR-4 cross-ref PRD §12.6).

##### 27. Testing
- Unit: skip-note-and-check-in-succeeds test.
- Unit: fasting row absent when not parent-enabled.
- UI: category selector and note entry Compose tests.

##### 31. Final Verification Checklist
- [ ] Good deed note entry is always skippable
- [ ] Fasting Tracker only renders when parent-enabled
- [ ] Both flows check in via the shared offline outbox
- [ ] Fasting education content linked correctly
- [ ] Localization and RTL verified
- [ ] Analytics events wired

#### `Development_Blueprints/A7_Habit_Tracker/KMP/04-streak-calendar-state-detail-recovery-mission-flow.md`

##### 4. Objective
Build the Streak Calendar, Streak State Detail (AtRisk/Broken/Recovery), Recovery Mission, and Mercy Suggestion Prompt screens, with a mandatory shame-word blocklist test across all locales (FR-13, FR-14).

##### 5. Business Requirements
- Warm, non-alarming iconography for AtRisk/Broken states — never red/alarming (PRD §2.1).
- Client-side display only mirrors server-computed streak state (B-03); never independently computes transitions.
- The internal `broken` state name must never be surfaced as raw user-facing text — always translated into supportive copy.
- Mercy Suggestion Prompt offers a smaller target/alternate time/family reminder, never implies failure (FR-14).
- Recovery Mission completion returns streak to Active; window expiry returns to Inactive — both communicated without shame framing.

##### 11. KMP Requirements
- Streak Calendar with skeleton loading state.
- Streak State Detail with warm illustration (softly glowing garden at dusk, not a wilted plant), AtRisk-warning/Broken-transition/Recovery-active/Recovery-closing-soon states.
- Recovery Mission screen; completing it navigates back to Habit Builder with streak restored to Active.
- Mercy Suggestion Prompt: Accept (adjusts target inline) / Dismiss.
- Compose UI test utility scanning all rendered `Text` composables on these screens against a case-insensitive blocklist: "fail", "failed", "broke", "broken", "lost", "didn't" — run against every locale's string resources, not just default.

##### 15. Validation
Mandatory: shame-word blocklist Compose UI test across every locale's string resources (PRD §7 Android prompt item 5).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Streak Service degraded (B-03 cached fallback) | Client shows last-known cached state with a calm "reconnecting" indicator, never a zero-reset flash |
| Recovery window expiring | Gentle nudge, not a countdown-pressure timer |

##### 19. Offline First
Streak display works from local cache when offline; recovery-mission completion requires connectivity (delegates to K-06 outbox if the completion action itself is a check-in-equivalent).

##### 21. Localization
All streak-state and mercy-suggestion copy fully localized and culturally reviewed (not just translated) per B-11's review workflow — consume only `status='published'` copy.

##### 22. RTL
Calendar grid, state-detail illustration layout, and prompt buttons verified for RTL mirroring.

##### 25. Security
No elevated risk; the mandatory blocklist test is a content-safety control, not a security control per se, but treated with equivalent CI-gate rigor.

##### 27. Testing
- Mandatory: shame-word blocklist test across all locales (CI-blocking).
- Unit: client never independently computes state transitions (render-only verification).
- UI: all documented streak-state visual variants render correctly with correct iconography.

##### 31. Final Verification Checklist
- [ ] Shame-word blocklist test passes across every locale (mandatory CI gate)
- [ ] Internal `broken` state name never surfaced as raw text
- [ ] Client mirrors server state only, never independently computes transitions
- [ ] Cached-fallback display never zero-resets on service degradation
- [ ] All documented state variants render with warm, non-punitive iconography
- [ ] Localization and RTL verified
- [ ] Analytics events wired

#### `Development_Blueprints/A7_Habit_Tracker/KMP/05-noor-garden-personal-family-visualization.md`

##### 4. Objective
Build the Noor Garden Personal and Family screens plus the Family Streak Milestone Celebration, with the Family Garden response DTO structurally incapable of holding a per-child breakdown, mirroring B-06's server-side guarantee on the client (FR-12).

##### 5. Business Requirements
- Family Garden shows combined-only aggregate progress; requires explicit child-switcher tap, never simultaneous side-by-side comparison layout (PRD §2.1 No-Comparison Enforcement design principle).
- Personal Garden is a single composed illustrated scene with distinct zones per habit type, not disconnected icons.
- Zero-milestone state shows a "seedling" starting description.
- Degraded Family Aggregation Service shows a non-alarming "growing..." state.

##### 11. KMP Requirements
- Personal Garden: full-bleed illustrated scene, distinct zones (Quran tree, kindness flowers, Salah lanterns, dua stars, Ramadan moon path), "last grew on [date]" indicator.
- Family Garden: aggregate-only view; explicit child-switcher control (tap to view a different child's *personal* garden — never a simultaneous multi-child layout).
- `FamilyGardenDto` (deserialized from `GET /v1/habits/garden/{child_id}`) must contain **only aggregate fields** — no `List<ChildContribution>` or any nested `childId`/`child_id`-bearing field.
- Reflection-based test enumerating the DTO's declared fields, asserting none are collection types containing a nested child-identifying field (mandatory, mirrors B-06's server-side structural test).
- Family Streak Milestone Celebration modal on threshold crossing.

##### 15. Validation
Mandatory reflection test asserting the `FamilyGardenDto` class's declared fields contain no collection type with a nested `childId`/`child_id` field (PRD §7 Android prompt item 4) — this guards against a future well-intentioned but policy-violating addition slipping through code review.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Family Aggregation Service degraded | "Growing..." non-alarming state, personal garden unaffected |
| Zero family milestones | "Seedling" starting state with next-milestone description |
| Garden fetch fails entirely | Cached last-known garden shown, not a blank error screen |

##### 19. Offline First
Garden state cached locally for offline/degraded viewing; not a write path (read-only visualization).

##### 21. Localization
Zone labels, milestone descriptions, "last grew on" date formatting all localized (EN/HI/AR/UR) with correct date-format conventions per locale.

##### 22. RTL
Isometric garden scene layout and zone labels verified for RTL; child-switcher control mirrors correctly.

##### 25. Security
Reflection test on `FamilyGardenDto` is the client-side half of the defense-in-depth sibling-comparison guarantee (server-side half is B-06's schema test).

##### 27. Testing
- Mandatory: `FamilyGardenDto` reflection test (no child-identifying nested fields).
- UI: Family Garden screen renders with zero per-child comparative UI elements (structural UI test mirroring the backend's schema guarantee, per PRD §6.10).
- UI: personal garden zone rendering, milestone celebration modal.

##### 31. Final Verification Checklist
- [ ] `FamilyGardenDto` reflection test passes (no child-identifying nested fields)
- [ ] Family Garden requires explicit child-switcher tap, never simultaneous comparison layout
- [ ] Personal Garden renders as a single composed scene with distinct zones
- [ ] "Growing..."/"seedling" fallback states implemented
- [ ] Family Milestone Celebration modal triggers correctly
- [ ] Localization and RTL verified
- [ ] Analytics events wired

#### `Development_Blueprints/A7_Habit_Tracker/KMP/06-offline-checkin-outbox-chronological-sync-engine.md`

##### 4. Objective
Build a Room-backed offline outbox for check-ins keyed by `client_request_id`, with a background sync worker processing queued items in ascending `local_date` order regardless of insertion order, backing FR-2, FR-20, Edge Cases 4 and 12.

##### 5. Business Requirements
- Full offline check-in capability; local state updates immediately (FR-2).
- Offline items queued with `client_request_id`, generated at tap time and reused on retry (never regenerated).
- Sync processes items in ascending `local_date` order (oldest first) regardless of queue-insertion order, to ensure correct server-side streak recomputation across a gap (Edge Case 12).
- Two-children-share-device: a queued check-in stays attributed to the acting child's `child_id` captured at action time, not sync time, even if the active session switches before sync (Edge Case 4).
- Sync failures use exponential backoff, never surfaced as a child-facing error.

##### 11. KMP Requirements
- `HabitCheckInOutboxEntity(client_request_id PK, child_id, habit_id, local_date, timezone, source, note_category, status, retry_count, created_at)`.
- `client_request_id` generated once at the tap/action moment; reused verbatim on every retry.
- `child_id` captured at action time and persisted with the outbox row — never re-resolved from "current session" at sync time (Edge Case 4).
- Sync engine processes the queue in **ascending `local_date`** order on each sync attempt, regardless of insertion order.
- Exponential backoff on transient failure; entries removed only on confirmed success or confirmed idempotent-duplicate response.

##### 15. Validation
Mandatory test: queue check-ins for "today," "yesterday," and "3 days ago" in that insertion order (out of chronological order); assert sync submits them in chronological order regardless of queue-insertion order (PRD §7 Android prompt item 3).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Network failure during sync | Exponential backoff retry; entry remains queued, never shown as a child-facing error |
| Server returns duplicate/idempotent success | Entry removed from queue, treated identically to a fresh success |
| Multi-day gap backfill | All queued entries reconciled in chronological order in a single sync pass |
| Device/session switch mid-queue | Queued entry's persisted `child_id` is used, not the currently-active session |

##### 19. Offline First
This sub-feature **is** the offline-first mechanism for Habit Tracker — full write capability offline, synced opportunistically and correctly ordered on reconnect.

##### 21. Localization
N/A (internal sync mechanism, no user-facing strings beyond the shared "syncing..." indicator owned by K-01).

##### 22. RTL
N/A.

##### 25. Security
`client_request_id` is a client-generated UUID, non-guessable/sequential; outbox data is low-sensitivity (habit-completion booleans and dates, not raw content).

##### 27. Testing
- Mandatory: chronological sync-order test regardless of insertion order (§15).
- Mandatory: multi-child attribution correctness test (Edge Case 4) — queued entry retains acting child's `child_id` even after an active-session switch.
- Integration: full offline → backgrounded → reconnect → correct streak recomputation flow (coordinates with B-03's server-side recomputation), including a multi-day-gap backfill scenario.
- Unit: exponential backoff behavior, idempotent-duplicate handling.

##### 31. Final Verification Checklist
- [ ] Chronological sync-order test passes regardless of insertion order (mandatory)
- [ ] Multi-child attribution test passes (Edge Case 4, mandatory)
- [ ] `client_request_id` generated once at action time, never regenerated on retry
- [ ] Exponential backoff implemented for transient failures
- [ ] Idempotent-duplicate responses correctly clear the queue entry
- [ ] A2's existing outbox reconciliation decision documented and actioned
- [ ] All habit-type ViewModels route through this shared engine
- [ ] Full offline-backfill integration test passes

#### `Development_Blueprints/A7_Habit_Tracker/KMP/07-habit-reminder-deep-link-quiet-hours-landing.md`

##### 4. Objective
Implement deep-link routing for `noorheroes://habits`, `noorheroes://habits/garden`, `noorheroes://habits/streak-risk`, landing notification taps on the correct Habit Tracker screens (FR-15 cross-reference).

##### 5. Business Requirements
- Notification-tap deep links land on the correct destination screen (Habit Builder, Noor Garden, or a streak-risk-focused view).
- Quiet-hours/bedtime-window suppression is enforced **server-side by the Notification Service** — this sub-feature must not duplicate that suppression logic client-side (PRD §6.9).

##### 11. KMP Requirements
- `noorheroes://habits` → Habit Builder (K-01)
- `noorheroes://habits/garden` → Noor Garden Personal (K-05)
- `noorheroes://habits/streak-risk` → Streak State Detail / AtRisk-focused view (K-04)
- No client-side quiet-hours suppression logic — trust the server-side Notification Service entirely for delivery timing.

##### 15. Validation
Unit test asserting each of the three deep-link patterns routes to the correct destination screen.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Deep link received with an unknown/malformed path | Fall back to Habit Builder (safe default), not a crash or blank screen |
| Target child/session no longer valid | Route to standard auth/session-recovery flow (existing app-wide pattern), not a Habit-Tracker-specific error |

##### 19. Offline First
N/A (navigation routing only).

##### 21. Localization
N/A (routing logic, no user-facing strings).

##### 22. RTL
N/A.

##### 25. Security
Deep-link handler validates the resolved route against the current authenticated session before navigating (standard app-wide deep-link security pattern, reused not reinvented).

##### 27. Testing
Unit tests for all three deep-link patterns; integration test for malformed-path fallback behavior.

##### 31. Final Verification Checklist
- [ ] `noorheroes://habits`, `/garden`, `/streak-risk` all route correctly
- [ ] Malformed/unknown deep link falls back to Habit Builder, not a crash
- [ ] No client-side quiet-hours suppression logic implemented
- [ ] Session validation applied before navigation
- [ ] Tests passing for all patterns

#### `Development_Blueprints/A7_Habit_Tracker/KMP/08-parent-area-habit-visibility-reminder-verification-configuration.md`

##### 4. Objective
Build the Habit Visibility/Age-Scoping Configuration screen, Habit Reminder Settings screen, and Parent Verification Pending Item widget, framing verification as supportive co-participation, never surveillance (FR-5, FR-6, FR-15).

##### 5. Business Requirements
- Only parent-enabled habits are ever visible to the child (FR-5) — configuration changes take effect immediately on the child's next checklist load.
- Verification framed as "Mark this together," never "checking up" language or iconography (FR-6).
- Reminder settings respect quiet-hours/bedtime windows configured via C.23's `BedtimeSettingsScreen`/`BedtimeSettingsViewModel` — this screen only sets habit-specific reminder timing preferences within those bounds.
- Screen gated behind `ParentGateLauncher.requireParentAuth()` (C.19, per §6/§7 corrected API).

##### 11. KMP Requirements
- Habit Visibility Configuration: per-habit-type toggle scoped to the child's age band, immediate save.
- Habit Reminder Settings: per-child reminder timing preferences, respecting existing quiet-hours bounds (read-only display of those bounds, not editable here).
- Parent Verification Pending Item: list of pending verification requests with "Mark this together" framing; tapping calls `SubmitVerificationUseCase` → B-08.
- Route guarded by `ParentGateLauncher.requireParentAuth(triggerContext)` (C.19).

##### 15. Validation
Test asserting the child's Habit Builder (K-01) cache is correctly invalidated/refreshed after a parent saves a visibility configuration change.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Save fails (network) | Standard retry affordance, no data loss of the in-progress form state |
| Verification submission fails to deliver | Per B-08, child unaffected; item remains pending, shown again next visit |

##### 19. Offline First
Configuration writes are not required to be offline-first (parent-initiated, infrequent action); standard online-required form submission with retry is acceptable, consistent with C.20/C.22/C.23's parent-facing screens.

##### 21. Localization
All copy, especially verification framing language, fully localized and reviewed for tone (cross-reference B-11's review workflow, since verification copy carries the same ethical-tone sensitivity as mercy-suggestion copy).

##### 22. RTL
Toggle rows, settings form, and pending-item widget verified for RTL.

##### 25. Security
Route-level `ParentGateLauncher.requireParentAuth()` guard (C.19) is the primary control; verification framing is a child-wellbeing/trust control (FR-6), not just a UX nicety.

##### 27. Testing
- Unit: cache-invalidation-on-save test.
- UI: verification widget copy/iconography never uses surveillance-adjacent language (a text-scan test mirroring K-04's shame-word blocklist approach, applied to a "surveillance-language" blocklist instead: "check up", "monitor", "spy", "watch").
- Integration: full visibility-configuration save → child checklist reflects change.

##### 31. Final Verification Checklist
- [ ] Habit visibility write endpoint contract confirmed (not guessed)
- [ ] Visibility changes correctly invalidate/refresh the child's checklist cache
- [ ] Verification widget passes the surveillance-language blocklist scan
- [ ] Route gated behind `ParentGateLauncher.requireParentAuth()` (C.19 Parent PIN/Biometric)
- [ ] Screens live in `feature-habits`'s own parent-facing package, not an invented shared "Parent Area" module
- [ ] Reminder settings respect existing quiet-hours bounds
- [ ] Localization and RTL verified
- [ ] Analytics events wired

#### `Development_Blueprints/A7_Habit_Tracker/KMP/09-weekly-habit-report-in-app-parent-view.md`

##### 4. Objective
Build the Weekly Habit Report and Per-Habit Detail screens rendering B-07's single-child, highlights-framed report data, with a structural UI test verifying zero per-child comparative elements (FR-21).

##### 5. Business Requirements
- Highlights framing, never raw failure/success scorecards (FR-21).
- Single-child-at-a-time rendering enforced at the component level — no simultaneous sibling comparison layout, mirroring K-05's Family Garden constraint.
- Zero-history state handled gracefully, not as an error.

##### 11. KMP Requirements
- Weekly Habit Report: highlights-framed summary, single child in view at a time.
- Per-Habit Detail drill-in from the summary.
- Structural UI test enumerating rendered components on both screens, asserting no component ever receives more than one child's data simultaneously.

##### 15. Validation
Structural UI test verifying zero per-child comparative UI elements — mirrors B-07's single-child-only API schema guarantee at the presentation layer.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Zero habit history | "Just getting started" highlights-framed empty state, not an error |
| Report fetch fails | Cached last report shown if available; otherwise a calm retry prompt |

##### 19. Offline First
Cached last-fetched report available offline; not a write path.

##### 21. Localization
Report copy sourced from B-13's approved templates via B-07; fully localized.

##### 22. RTL
Report layout, charts/summaries, and detail drill-in verified for RTL.

##### 25. Security
No elevated risk; standard parent-session scoping.

##### 27. Testing
- Structural: no-comparative-UI test (mandatory).
- Unit: cache-fallback behavior.
- UI: highlights-framing content rendering, empty state.

##### 31. Final Verification Checklist
- [ ] Structural no-comparative-UI test passes (mandatory)
- [ ] Report content uses highlights framing, not raw scorecards
- [ ] Zero-history empty state handled gracefully
- [ ] Per-Habit Detail drill-in works correctly
- [ ] Localization and RTL verified
- [ ] Analytics events wired

#### `Development_Blueprints/A7_Habit_Tracker/KMP/10-ramadan-mode-checklist-variant-ethical-messaging-safeguards.md`

##### 4. Objective
Render the Ramadan Mode Checklist Variant when seasonal mode is active, plus the "No Habits Configured" and "No Streak History" empty states, with correct reversion when Ramadan ends without streak discontinuity (FR-18, Edge Case 9).

##### 5. Business Requirements
- When Ramadan mode is active, checklist reflects fasting, charity, Quran, dua, and family iftar reflection habits (FR-18).
- Reverts to standard checklist post-Ramadan without streak discontinuity purely from the seasonal switch (Edge Case 9).
- Empty state (zero habits): friendly "ask a grown-up" prompt with parent deep link.
- Empty state (zero streak history): warm "Let's start your first day!" framing, never a stark "0".

##### 11. KMP Requirements
- Ramadan checklist variant swaps in seasonal habit rows without discarding the underlying streak state.
- Reversion to standard checklist post-Ramadan is a pure UI/data-source swap, not a streak reset.
- Empty states per §5, both using warm, non-stark framing consistent with the feature's anti-shaming design language.

##### 15. Validation
Test simulating Ramadan-mode activation mid-cycle with an active non-Ramadan streak, asserting no streak discontinuity occurs purely from the mode switch (Edge Case 9, mirrors B-03's server-side guarantee).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Ramadan-mode state fails to load | Default to standard checklist, not a blocked/error state |
| Zero habits configured | Friendly setup-prompt empty state with parent deep link |
| Zero streak history | "Let's start your first day!" framing, never a bare "0" |

##### 19. Offline First
Ramadan-mode flag cached alongside the habit catalog (K-01); works offline from last-known state.

##### 21. Localization
Ramadan-specific habit labels and empty-state copy fully localized, culturally reviewed per PRD NFR Localization requirement (mercy/encouragement language must land appropriately across cultures, not just literal translation).

##### 22. RTL
Ramadan checklist variant and empty-state illustrations verified for RTL.

##### 25. Security
No elevated risk.

##### 27. Testing
- Unit: Ramadan-transition no-discontinuity test (mandatory, mirrors Edge Case 9).
- UI: both empty states render with correct warm framing.
- Unit: reversion post-Ramadan correctly restores standard checklist.

##### 31. Final Verification Checklist
- [ ] Ramadan-mode activation/deactivation causes no streak discontinuity (mandatory test)
- [ ] Ramadan checklist correctly reflects seasonal habit set
- [ ] Zero-habits empty state includes parent deep link
- [ ] Zero-streak-history empty state uses warm framing, never a bare "0"
- [ ] F.36's existing seasonal-state provider reused, not re-derived
- [ ] Localization and RTL verified
- [ ] Analytics events wired

#### `Development_Blueprints/A7_Habit_Tracker/KMP/11-habit-tracker-analytics-cross-platform-event-instrumentation.md`

##### 4. Objective
Verify and complete the full analytics event taxonomy across all Habit Tracker screens, including the two ethically-important funnels (main engagement funnel and recovery-path funnel), with aggregate-only schema enforcement carried through to the analytics layer for Family Garden events.

##### 5. Business Requirements
- Full event taxonomy per PRD §1.19 wired across every relevant screen (cross-cutting verification task, not new UI).
- Main funnel: `habit_builder_viewed` → `habit_checked_in` → `streak_state_changed` (to active) → `family_streak_milestone_reached` (if applicable).
- Recovery funnel: `streak_broken_shown` → `recovery_mission_started` → `recovery_mission_completed` — this validates the feature's core ethical-design hypothesis (does mercy/recovery design actually re-engage children).
- Family Garden/aggregate events remain schema-aggregate-only, mirroring B-06's structural guarantee even at the analytics layer.

##### 11. KMP Requirements
- Audit every screen built in K-01–K-10 against the full PRD §1.19 event list: `habit_builder_viewed`, `habit_checked_in`, `habit_checkin_duplicate_ignored`, `habit_unchecked` (if toggle-off supported), `dhikr_counter_opened`, `dhikr_target_reached`, `dhikr_target_changed_midday`, `fasting_tracker_logged`, `good_deed_category_selected`, `good_deed_note_added`, `streak_state_changed`, `streak_shield_applied`, `streak_broken_shown`, `recovery_mission_started`, `recovery_mission_completed`, `recovery_window_expired`, `mercy_suggestion_shown`, `mercy_suggestion_accepted`, `family_streak_milestone_reached`, `noor_garden_viewed`, `parent_habit_visibility_configured`, `parent_verification_requested`, `parent_verification_completed`, `weekly_habit_report_viewed`, `ramadan_mode_checklist_activated`, `ramadan_mode_checklist_deactivated`, `timezone_change_grace_applied` (server-emitted, verify client surfaces it if needed), `backfilled_checkin_synced`.
- Verify event-parameter shapes match documented fields (`habit_type`, `local_date`, `from_state`, `to_state`, `streak_type`, etc.).

##### 15. Validation
Mandatory: event-coverage test enumerating the full §1.19 list against the actual call sites found in K-01–K-10; any missing event fails the test and must be added.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Analytics call fails | Never blocks or delays the underlying user action; fire-and-forget with existing `core-analytics` retry/queue behavior |

##### 19. Offline First
Analytics events queue via existing `core-analytics` offline-tolerant dispatch, consistent with the rest of the app.

##### 21. Localization
N/A (event names/params are not user-facing).

##### 22. RTL
N/A.

##### 25. Security
`family_streak_milestone_reached`/Family Garden events verified free of any per-child parameter, mirroring B-06/K-05's structural guarantees.

##### 27. Testing
- Mandatory: full event-coverage test against §1.19 list.
- Mandatory: Family Garden event schema test (no per-child params).
- Funnel verification: manual/QA trace of both documented funnels end-to-end in staging.

##### 31. Final Verification Checklist
- [ ] Every event in PRD §1.19 has a verified firing call site
- [ ] Event-coverage test passes 100% (mandatory)
- [ ] Family Garden event schema test passes (no per-child params, mandatory)
- [ ] Main engagement funnel traceable end-to-end in staging
- [ ] Recovery-path funnel traceable end-to-end in staging
- [ ] Event parameter shapes match documented fields

## A8 — Feature_A8_Daily_Quiz_Engine

PRD: `PRD_Documents/Child App (1-12)/Feature_A8_Daily_Quiz_Engine.md`

Coverage: 15 mandatory FR records; all preserved verbatim below. Feature has 15 inventory records including components/states. Components and states must not inflate independently executed screen count.

### Existing screenshot candidates

- `Screens/Mobile App/Quiz Engine/Quiz Complete-01.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Complete-02.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Question-01.png` — visually inspected
- `Screens/Mobile App/Quiz Engine/Quiz Question-02.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Question-03.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Question-04.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Result-01.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Result-02.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Result-03.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Result-04.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Result-05.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Result-06.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Result-07.png` — inventoried only

### Complete normative functional coverage

### 1.7 Functional Requirements

**FR-1** Daily Quiz assembles exactly 5 questions per session, sourced from a mix of recently-learned content and identified weak skills (source §6.3/§21.9).
**FR-2** Supported question types: multiple choice, sequence/ordering, true/false, image match, audio match (source §6.3/§21.9/§23.5) — the engine must support all five types as first-class, reusable across every consuming feature.
**FR-3** Immediate explanation is shown after every answer submission, regardless of correctness (source §6.3/§21.9) — this is not optional or skippable-by-default; it is always presented.
**FR-4** Incorrect answers enter a short retry set within the same session (source §6.3/§21.9) — the retry set is assembled from only the missed questions (or close variants, per content design), not the full original set.
**FR-5** Quiz completion always awards effort XP, regardless of accuracy; accuracy independently feeds the Skill Mastery model's confidence calculation but never reduces or withholds the base participation reward (source §6.3/§21.9/§A.5 FR-16 cross-reference — a hard, platform-wide rule restated here as this engine's authoritative implementation point).
**FR-6** Parent-facing reporting from any quiz attempt must surface concepts/skills addressed, not a bare numeric score as the headline (source §6.3/§21.9).
**FR-7** Each question records: `question_id`, `content_version_id`, attempt number, answer, response time, hint count, and an offline flag (source §21.9 "Detailed sample screen" data fields) — this data model is shared across all question types and all consuming features.
**FR-8** Hints are progressive/partial (consistent with A.5 FR-18) and tracked via `hint_count` feeding mastery-confidence calculation, never shown as a visible penalty to the child.
**FR-9** The Quiz Engine must be embeddable/contextualized by the calling feature — a Daily Quiz widget instance (Home), a Learn-tab skill-practice instance (A.5), a post-Story instance (A.3, "3 to 5 questions"), and a Dua recall instance (A.6, "1 to 3 questions") all use the same underlying attempt/response/scoring contract, parameterized by question count and source pool rather than divergent implementations.
**FR-10** Offline quiz attempts are supported when the question bank was included in a content download package; results sync on reconnect with idempotent submission (cross-ref A.3/A.5/A.6 offline patterns).
**FR-11** A quiz attempt that references a question later withdrawn for safety reasons must still sync for historical record purposes, but the withdrawn item is **excluded from mastery and reward calculation** even if the attempt predates the withdrawal and is syncing late (source: Error & Edge-Case Matrix, "Offline quiz uses a withdrawn question → Sync the attempt for history, but exclude the withdrawn item from mastery/reward if it was withdrawn for safety reasons").
**FR-12** Distractor (wrong-answer-option) quality is governed by the Quiz Builder's content-authoring validation, including a "preview for mobile and screen reader" check before publish (source §23.5) — this engine's read path trusts that published questions have passed this authoring-side quality gate.
**FR-13** Question versions are locked after publication (source §23.5 "Version lock after publication") — an in-flight quiz session must never have a question's content change underneath it mid-attempt; edits create a new version for future sessions only.
**FR-14** Quiz attempts are idempotent via `client_request_id` at the attempt level, consistent with the platform's universal idempotency pattern (source §9.3 `quiz_attempts`/`quiz_responses` schema notes).
**FR-15** The engine must support per-question skill-tagging (linking a question to one or more skill/mastery nodes) so that a single quiz session can simultaneously update mastery confidence across multiple distinct skills.

### Ordered source inventory

### 1.18 Screen Inventory (Complete — Zero Missing)

| # | Screen / Component | Type | Entry Points | Exit Points |
|---|---|---|---|---|
| 1 | Quiz Entry Card (context-specific: Daily Quiz widget, post-Story prompt, Learn-tab practice, Dua recall) | Component | Home, Story completion flow (A.3), Skill Tree (A.5), Dua Card (A.6) | Quiz Question Screen |
| 2 | Quiz Question Screen — Multiple Choice | Screen | Quiz Entry Card | Per-Answer Explanation |
| 3 | Quiz Question Screen — Sequence/Ordering | Screen | Quiz Entry Card | Per-Answer Explanation |
| 4 | Quiz Question Screen — True/False | Screen | Quiz Entry Card | Per-Answer Explanation |
| 5 | Quiz Question Screen — Image Match | Screen | Quiz Entry Card | Per-Answer Explanation |
| 6 | Quiz Question Screen — Audio Match | Screen | Quiz Entry Card | Per-Answer Explanation |
| 7 | Hint Overlay (cross-cutting, shared with A.5) | Component | Any Question Screen "Hint" control | Resumes question |
| 8 | Per-Answer Explanation Overlay | Component | Every question, after submission | Next question / Retry Set / Completion |
| 9 | Media-Load-Failure Graceful Skip Notice | Component | Image/Audio Match question, asset failure | Next question (question excluded) |
| 10 | Retry Set Entry Screen | Screen | End of main question set, if any incorrect | Retry Question Screens |
| 11 | Retry Question Screen (reuses type-specific screens 2-6) | Screen | Retry Set Entry | Per-Answer Explanation |
| 12 | Quiz Completion / Effort XP Reveal | Screen | End of main set (no misses) or end of retry round | Skill Mastery update (background), Parent report availability |
| 13 | Resume-In-Progress-Session Prompt | Component | Re-entry to a quiz context with an abandoned partial session | Resumes at the correct question index |
| 14 | Offline Quiz Indicator | Component | Any quiz screen, while offline | N/A |
| 15 | Parent Quiz/Concept Summary Report (context-aggregated) | Screen (Parent Area) | Parent Dashboard → Child Progress | Concept Detail Drill-in (shared with A.5 §1.18) |

### Exact mobile UX and behavior sources

### 1.9 Acceptance Criteria

- Given a child starts a Daily Quiz, when the question set is assembled, then exactly 5 questions are presented, drawn from a mix of recent-content and weak-skill pools.
- Given a child answers any question (correct or incorrect), when the answer is submitted, then an explanation is shown immediately before proceeding to the next question.
- Given a child answers 2 of 5 questions incorrectly, when the main set is complete, then a retry set containing those 2 (or close variants, per content design) is offered within the same session.
- Given a child completes a quiz with a low accuracy score, when completion is processed, then effort XP is still awarded at the standard participation rate — accuracy never reduces the base reward.
- Given a parent opens a quiz-linked progress report, when it renders, then it lists concepts/skills addressed (e.g., "Practicing: Surah Al-Fatiha recitation") rather than leading with a raw percentage.
- Given a quiz question is withdrawn by Admin for safety reasons after a child took it offline but before their attempt syncs, when the sync occurs, then the attempt record is stored for history but that specific question's response is excluded from mastery/reward calculation.
- Given the same `client_request_id` is submitted twice for a quiz attempt completion (e.g., a network retry), when the server processes both, then only one completion result (and one reward grant) exists.
- Given a question's content is edited and republished mid-day, when a child who started their session before the edit submits a still-in-progress answer, then their session continues to reference the version that was active when their session started (no mid-session content drift).

### 1.10 Edge Cases

1. A child's weak-skill pool is empty (e.g., a brand-new learner with very little history) → the 5-question assembly falls back to a sensible default mix (recent content + a small set of foundational/placement-relevant questions) rather than failing to produce a full 5-question set.
2. A child has so many weak skills that more than 5 qualify for inclusion → the assembly algorithm prioritizes (e.g., by recency-of-weakness, skill importance, or balanced topic coverage) rather than arbitrarily; this prioritization logic should be deterministic and explainable for QA/debugging purposes, not a black box.
3. A retry-set question is also answered incorrectly a second time → the system does not infinitely re-loop the same question within one session; after a bounded number of retry rounds (e.g., 1 retry round), the session concludes with supportive framing and the concept is flagged more strongly for future weak-skill prioritization, rather than trapping the child in an endless retry loop.
4. A child attempts a quiz offline using a downloaded question bank, and one of those questions happens to be a "weak skill" question whose weak-skill status has since changed server-side (the child since improved on it through other practice) → the offline-served question bank reflects whatever was true at download time; on sync, the server's authoritative mastery model is what's actually updated (the stale client-side weak-skill framing doesn't cause incorrect mastery double-counting, since mastery is recalculated server-side from the actual response data, not from the client's assumed reason-for-inclusion).
5. A child rapidly answers all 5 questions in an implausibly short time (e.g., random tapping) → `response_time_ms` is recorded and may feed an anomaly/quality signal for mastery-confidence weighting (a suspiciously fast correct answer contributes less confidence than a thoughtfully-timed one), without blocking the child's reward (effort XP is unconditional per FR-5) or accusing them of cheating in any visible way.
6. Two consuming features (e.g., Stories' post-episode quiz and Home's Daily Quiz widget) could theoretically select overlapping questions for the same child on the same day → this is acceptable and not treated as an error (repetition across distinct contexts has its own spaced-repetition value), but the weak-skill-pool logic should avoid recommending the *exact same* question instance twice within a very short time window (e.g., the same hour) to avoid a jarring "didn't I just answer this" experience.
7. An image-match or audio-match question's media asset fails to load mid-quiz → the question gracefully skips (treated as unanswered, not as an incorrect answer) with a brief explanation ("This question will come back another time") and the assembly logic backfills if possible, or the session simply proceeds with 4 questions rather than blocking entirely.
8. A child uses the maximum hint level on every question → mastery-confidence is appropriately discounted for heavily-hinted correct answers (consistent with A.5 FR-18's "hint usage... feeding the mastery-confidence calculation"), but this is invisible to the child — no UI signal makes them feel penalized for using hints.
9. A quiz attempt spans a midnight boundary (started at 11:58pm, finished at 12:03am) → the attempt is attributed to the day it was *started* for daily-quiz-eligibility purposes (a child shouldn't be blocked from "today's" Daily Quiz just because they happened to finish a late-night one slightly past midnight, nor should they be able to get two Daily Quiz instances by timing it this way — the eligibility window logic must handle this gracefully, consistent in spirit with A.7's local_date handling).
10. A parent-facing skill-summary report is requested for a quiz attempt that included questions from multiple distinct skill domains (e.g., a Daily Quiz mixing a Quran question and a Dua question) → the report correctly attributes each question's contribution to its respective skill domain's mastery tracking, never conflating them into one ambiguous combined score.
11. A child completes the main 5-question set with zero incorrect answers → no retry set is offered (there's nothing to retry); the completion flow proceeds directly to the reward/summary screen without an empty or skipped-feeling intermediate step.
12. A quiz session is abandoned mid-way (child closes the app after 2 of 5 questions) → partial progress is not silently lost; on next entry, the child is offered to resume the same session (if still within a reasonable time window) rather than being forced to restart from question 1, consistent with the platform's general resumability philosophy (A.1 FR-16 spirit).

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Question-set assembly service unavailable | Falls back to a cached/default deterministic question set rather than blocking quiz access entirely |
| Media asset failure (image/audio question) | Graceful skip per Edge Case 7, never a hard quiz-blocking error |
| Quiz attempt submission fails (network) | Local state preserved (offline-first), retried with idempotency key, never re-prompts the child to re-answer already-answered questions |
| Mastery/reward processing failure post-completion | Completion UI still shows (the child's experience isn't blocked), with reward/mastery reconciliation happening asynchronously and retried server-side |
| Withdrawn question encountered mid-session (rare, real-time withdrawal during an active session) | The specific question is excluded from that session's remaining flow if not yet answered; if already answered, the response is still recorded but flagged for mastery/reward exclusion per FR-11 |

### 1.12 Empty States
- Zero quiz history yet (brand-new learner) → first-time quiz framing rather than a stark "no data" report for parents.
- A consuming feature (e.g., Dua Learning) has no qualifying question pool for a specific item → that quiz entry point is simply not offered (consistent with A.6 FR-6, "Recall Quiz... only offered for duas already marked Learned" — absence is expected, not an error state).

### 1.13 Loading States
- Question-set assembly: brief skeleton/loading state, typically near-instant given p95 < 500ms target.
- Per-answer explanation: pre-fetched alongside the question payload, so there is no additional loading state between answer submission and explanation display.

### 1.14 Offline States
- Full offline quiz-taking for downloaded question banks; results queue and sync per FR-10/FR-11.

### 1.15 Permission States
- No new runtime permissions; audio-match questions reuse existing media-playback capability, no microphone involvement (quizzes are answer-selection based, not recitation-recording based — that's A.5's distinct Tajweed/recitation flow).

### 1.16 User Flow (Narrative)

Child enters a quiz context (Home's Daily Quiz widget, post-Story, Learn-tab practice, or Dua recall) → Quiz Engine assembles the appropriate question set (5 for Daily Quiz, 3–5 for post-Story, 1–3 for Dua recall) → child answers each question, receiving immediate explanation after every answer → incorrect answers are collected into a retry set offered at the end of the main set → child optionally retries → session completes → effort XP awarded unconditionally → accuracy-derived mastery-confidence updates propagate to the Skill Mastery model → parent-facing concept-level summary becomes available in the relevant Progress Report.

### 2.1 Quiz-Specific Design System Extensions

- **Question Type Visual Consistency:** All five question types share a consistent screen skeleton (header with progress dots, central question-content area, answer-options area, persistent Hint control) so children recognize "I'm in a quiz" regardless of which feature launched it — critical given this engine is invoked from four different contexts.
- **Non-Punitive Incorrect-Answer Treatment:** Consistent with A.5's pronunciation-feedback philosophy, incorrect quiz answers use supportive iconography (not a harsh red X as the *dominant* visual element) paired with the immediate explanation — the explanation card is the visual focus, not a failure indicator.
- **Retry Set Framing:** Visually distinguished from the main set (e.g., a subtitle "Let's try these again" rather than feeling like a punishment lap), with its own short progress indicator separate from the main set's.
- **Effort XP Reveal:** Always positive/celebratory regardless of accuracy — the completion screen's tone and visual treatment do not vary based on score (a 1/5 and a 5/5 completion both get a warm, celebratory effort-acknowledgment screen; only the parent-facing report, never the child-facing completion screen, reflects accuracy detail).

### 2.2 Screen-Level Design Requirements (Key Screens)

#### Screen: Quiz Question Screen (generic template across types)

- **Purpose:** Present one question clearly with type-appropriate interaction.
- **Components:** Progress indicator (dots or "Question 2 of 5"), question prompt (text/image/audio depending on type), answer-options area (2-4 multiple-choice cards, drag-to-order tiles for sequence, true/false large dual buttons, tap-to-match grid for image/audio match), Hint control (secondary, always visible), Submit/auto-advance-on-select behavior depending on type.
- **States:** Default, Answer-selected-not-yet-submitted (where applicable), Submitting, Explanation-shown, Media-loading, Media-load-failed-skip.
- **Accessibility:** Sequence/ordering questions must support a non-drag alternative (e.g., numbered-tap-to-place) for accessibility; audio-match questions provide a text-transcript fallback option; image-match questions provide descriptive alt-text per option.
- **Responsive Rules:** Answer-option grids reflow for tablet (more columns) without changing interaction model.

#### Screen: Per-Answer Explanation Overlay

- **Purpose:** Immediately teach the correct concept regardless of the child's answer.
- **Components:** Correct-answer restatement, brief explanation text, source/reference tag where applicable (consistent with Islamic Facts' source-citation pattern), "Next" control.
- **States:** Correct-answer-given (light positive accent), Incorrect-answer-given (same explanation content, supportive — not punitive — framing, never hidden or abbreviated compared to the correct-answer case).

### 2.3 Tab Structure

The Quiz Engine has no dedicated tab of its own — it is embedded contextually. Click mapping (representative, per context):

| Click Target | Destination | API Called | Analytics Event | Permission Check | Error Handling |
|---|---|---|---|---|---|
| Home "Daily Quiz" widget | Quiz Question Screen (session start) | `GET /v1/quizzes/daily` | `quiz_started` (context=home_daily) | None | Friendly unavailable message (A.2 pattern) |
| Story post-completion quiz prompt | Quiz Question Screen | `GET /v1/quizzes/content/{episode_id}` | `quiz_started` (context=story_post) | Entitlement (inherited from already-unlocked episode) | Quiz step skippable, reward still finalizes (A.3 §1.11) |
| Skill Tree practice quiz entry | Quiz Question Screen | `GET /v1/quizzes/skill/{node_id}` | `quiz_started` (context=learn_practice) | None | Cached fallback |
| Dua recall quiz entry | Quiz Question Screen | `GET /v1/quizzes/dua/{dua_id}` | `quiz_started` (context=dua_recall) | Learned-status gate (A.6 §3.4) | `403 NOT_YET_LEARNED` |
| Answer option tap | Per-Answer Explanation | `POST /v1/quiz-attempts/{id}/responses` | `quiz_question_answered` | None | Optimistic local advance, retry sync |
| Hint control | Hint Overlay | `GET /v1/learning/hints/{question_id}` (shared with A.5) | `hint_requested` | None | Generic encouragement fallback |

### 2.4 Wireframe Description (Composite)

A single-question-per-screen, full-attention wireframe (no surrounding navigation chrome visible during an active quiz session, similar in spirit to the Story Player's immersive full-screen treatment, though without hiding system status bars) — minimizes distraction during the short, focused quiz experience. The Explanation Overlay appears as a bottom-sheet-style overlay rather than a full screen transition, keeping the question content visible above it for context.

### 2.5 Screen Image Generation Prompts

**Screen: Quiz Question Screen (Multiple Choice)**
- *Prompt 1 (English):* "Mobile app quiz question screen UI mockup for a children's Islamic learning app. Warm off-white background. A small progress indicator at top showing 'Question 2 of 5' with simple dot markers. Center area shows a short question prompt in friendly rounded text, with a small decorative icon. Below, four large rounded rectangular answer-option cards stacked vertically, each with simple text and a small leading icon, one card highlighted with a soft teal border indicating selection. A small lightbulb-shaped hint icon button in a corner. Calm, focused, encouraging aesthetic, soft shadows, generous spacing, no realistic human faces, no harsh red/green colors anywhere yet (pre-submission state)."
- *Prompt 2 (Arabic RTL):* "نفس شاشة سؤال الاختبار لتطبيق تعليم إسلامي للأطفال، بتخطيط من اليمين إلى اليسار بالكامل. خلفية بيج فاتح دافئ. مؤشر تقدم صغير في الأعلى يعرض 'السؤال 2 من 5' بعلامات نقطية بسيطة. منطقة المنتصف تعرض نص سؤال قصير بخط مستدير ودود، مع أيقونة زخرفية صغيرة. أسفل ذلك أربع بطاقات اختيار إجابة كبيرة مستديرة الزوايا مرصوصة عموديًا، كل منها بنص بسيط وأيقونة قائدة صغيرة، بطاقة واحدة مميزة بحد فيروزي ناعم تشير إلى التحديد. زر أيقونة لمبة تلميح صغيرة في الزاوية. طابع هادئ ومركّز ومشجع، ظلال خفيفة، تباعد كبير، بدون وجوه بشرية واقعية، بدون ألوان أحمر/أخضر قاسية في أي مكان حتى الآن (حالة ما قبل الإرسال)."

**Screen: Per-Answer Explanation Overlay**
- *Prompt 1 (English):* "Mobile app bottom-sheet overlay UI mockup for a children's quiz feedback screen, shown over a dimmed/blurred quiz question screen behind it. The sheet has rounded top corners, warm cream background. At the top, a small supportive icon (a soft upward sparkle, not a checkmark or X), below it bold restated correct-answer text, then a short friendly explanation paragraph, then a small source/reference tag chip. A single rounded gold 'Next' button at the bottom. Calm, instructive, non-judgmental visual tone, soft shadows, generous padding, no realistic human faces."
- *Prompt 2 (Arabic RTL):* "نفس واجهة النافذة المنبثقة من الأسفل لشاشة تغذية راجعة اختبار الأطفال، تظهر فوق شاشة سؤال الاختبار المعتمة/الضبابية خلفها، بتخطيط من اليمين إلى اليسار. للورقة زوايا علوية مستديرة وخلفية كريمية دافئة. في الأعلى أيقونة داعمة صغيرة (بريق صاعد ناعم، ليست علامة صح أو خطأ)، تحتها نص الإجابة الصحيحة بخط عريض، ثم فقرة شرح قصيرة وودودة، ثم شريحة صغيرة لمصدر/مرجع. زر ذهبي مستدير واحد بعنوان 'التالي' في الأسفل. طابع بصري هادئ وتعليمي وغير قاسٍ في الحكم، ظلال خفيفة، حشوة كبيرة، بدون وجوه بشرية واقعية."

*(Remaining screens — Sequence/Ordering, True/False, Image Match, Audio Match question types, Retry Set Entry, Completion/Effort XP Reveal, Parent Concept Summary — follow the same two-prompt EN/AR template using these tokens; full set available on request.)*

---

### 6.1 Technical Requirements
Kotlin, Jetpack Compose, MVVM, Clean Architecture, module `:core:quiz-engine` (built as a **shared core module**, not a feature module, since it's consumed by `:feature:home`, `:feature:stories`, `:feature:learn`, and `:feature:dua-learning`), depends on `:core:design-system`, `:core:network`, `:core:offline-cache`, `:core:media-player` (for audio-match questions).

### 6.2 Screen Mapping
`QuizSessionScreen` is a single reusable Composable accepting a `QuizContext` parameter (home_daily/story_post/learn_practice/dua_recall) and a `questionCount`; each question type renders via a `QuestionTypeRenderer` sealed-dispatch pattern (one Composable per type, sharing the common screen skeleton).

### 6.3 Navigation Flow
`QuizSessionScreen` is launched as a modal/full-screen destination from any of the four consuming feature modules, returning a `QuizResult` to the caller via a typed navigation result channel (not a shared mutable global state) so each consumer can react appropriately (e.g., Stories proceeds to "Next Learning," Dua Learning updates its badge-progress UI).

### 6.4 State Management
`QuizSessionViewModel` holds the full session state machine: `Assembling → QuestionActive(index) → Submitting → ExplanationShown → (NextQuestion | RetrySet | Completed)`. Resume-after-abandonment is handled by re-calling the same `GET` endpoint, which the backend guarantees returns the same in-progress attempt (§5 item 2) — the client doesn't need its own separate resume-detection logic beyond simply re-fetching.

### 6.5 API Mapping
`QuizRepository.startQuiz(context, childId)` → context-appropriate `GET /v1/quizzes/...` endpoint; `submitResponse()` → `POST /v1/quiz-attempts/{id}/responses`; `completeAttempt()` → `POST /v1/quiz-attempts/{id}/complete`.

### 6.6 Analytics Mapping
`QuizAnalytics` fires `quiz_started` with the correct `context` value sourced from the calling feature's parameter, enabling cross-feature funnel analysis without each feature needing its own duplicate analytics wrapper.

### 6.7 Offline Support
Downloaded content packages (Stories/Learn/Dua, per their respective offline specs) may bundle a pre-assembled question set for offline use; `:core:quiz-engine` accepts either a server-fetched or a locally-bundled question set via the same internal model, so the question-rendering/answering/explanation UI code path is identical regardless of source. Offline responses queue in a shared outbox keyed by `client_request_id`.

### 6.8 Deep Linking
Not directly deep-linked (always entered via a consuming feature's own entry point), but the shared `:core:quiz-engine` module exposes a stable internal API contract so any future feature can adopt it without new engine work.

### 6.9 Push Notifications
N/A directly; consuming features (Home/Habit Tracker) may send quiz-related reminders, deep-linking into their own entry points which then launch the shared quiz engine.

### 6.10 Testing Strategy
- Unit: question-type-agnostic session state machine (Assembling/Active/Submitting/Explanation/Retry/Completed transitions), shared across all four consumers — tested once in `:core:quiz-engine`, not duplicated per feature.
- UI tests: each of the 5 question-type renderers individually (multiple choice, sequence, true/false, image match, audio match), explanation overlay always appears regardless of correctness, completion screen visual treatment is identical regardless of accuracy (a structural UI test comparing rendered tree similarity between a 0%-accuracy and 100%-accuracy completion screen, asserting no accuracy-conditional visual branching exists on this specific screen).
- Integration: full main-set → retry-set → completion flow across all four `QuizContext` values, offline question-bank flow, resume-after-abandonment flow.

---

### 13.1 Test Plan Summary
Coverage spans: deterministic question-set assembly, accuracy-independent reward issuance (signature test), withdrawn-question exclusion, retry-set bounding, resume-after-abandonment, and all 12 edge cases from §1.10.

### 13.2 Test Cases — Happy Path
1. Child completes a 5-question Daily Quiz with 4/5 correct, retries the 1 missed question correctly, receives standard effort XP, and the parent's concept summary reflects the relevant skill as improving.
2. Child completes a Dua recall quiz (1 question) instantly, with the same engine code path as the 5-question Daily Quiz, just parameterized differently.
3. Child abandons a quiz at question 3 of 5, returns the next day, and resumes at question 3 (not restarted).

### 13.3 Edge Cases
All 12 items from §1.10.

### 13.4 Negative Cases
- Submit a response for a `question_id` not in the assembled attempt's set → `400`.
- Complete two attempts with 0% and 100% accuracy respectively → identical base reward amount on both.
- Withdraw a question referenced by an already-recorded-but-not-yet-completed-and-synced response, then complete the attempt → accuracy computed excluding that response; response row still present in DB.
- Call the Daily Quiz `GET` endpoint twice before completing → identical `attempt_id` and question set both times.
- Miss the same question in both the main set and the single retry round → no third round offered.

### 13.5 Regression Cases
Full Quiz Engine suite re-run on every release touching `:core:quiz-engine`, the shared Quiz Service, Reward Service, or Skill Mastery Service — given this engine's shared/cross-cutting nature, regression testing here has outsized blast-radius importance across four consuming features.

### 13.6 Automation Cases
End-to-end: full assembly → answer → explanation → retry → completion flow across all four `QuizContext` values; offline question-bank flow with sync-time withdrawn-question exclusion; resume-after-abandonment automated test; accuracy-independent-reward production-sampling canary check.

---

### Corresponding KMP blueprint requirements

#### `Development_Blueprints/A8_Daily_Quiz_Engine/KMP/01-shared-quiz-engine-core-module.md`

##### 4. Objective
Stand up `:core:quiz-engine` as a genuinely shared core module — not a feature module — consumed by `:feature:home`, `:feature:stories`, `:feature:learn`, and `:feature:dua-learning`, establishing the `QuizContext` contract and `QuizSessionScreen` entry point every consumer will call into.

##### 5. Business Requirements
FR-9 (engine embeddable/contextualized by the calling feature, single contract parameterized by count/pool, not forked per consumer); §6.1 (module boundary: core, not feature).

##### 11. KMP Requirements
- Public `QuizContext` enum: `HomeDaily`, `StoryPost`, `LearnPractice`, `DuaRecall`
- Single `QuizSessionScreen` composable: `(context: QuizContext, childId: String, questionCount: Int? = null, sourceId: String? = null) -> QuizResult`
- `QuizResult` data class: `accuracyPercent`, `rewardGranted`, `conceptsTouched` — returned via typed navigation result mechanism (callback or `SavedStateHandle`-backed result flow), **not** a shared mutable singleton
- Hilt DI wiring scoped to the quiz session lifecycle
- Module-boundary lint/test: `:core:quiz-engine` must not import from any `:feature:*` module

##### 15. Validation
`questionCount`/`sourceId` are nullable and validated contextually — `sourceId` required for `StoryPost`/`LearnPractice`/`DuaRecall`, not required for `HomeDaily`.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Consumer passes invalid `QuizContext`/`sourceId` combination | Compile-time-enforced where possible (sealed parameter validation); runtime `IllegalArgumentException` in debug builds only, graceful no-op entry-point suppression in release |
| Module accidentally depends on a `:feature:*` module | Build-time failure via module-boundary test/lint (Task 07) |

##### 19. Offline First
N/A at this scaffolding layer (owned by K-06).

##### 21. Localization / 22. RTL
N/A (module contract only; no strings rendered directly by this sub-feature).

##### 25. Security
No new sensitive data handling at this scaffolding layer.

##### 27. Testing
- Unit: `QuizResult` contract shape stable and correctly typed across all 4 contexts
- Build/lint: module-boundary test asserting `:core:quiz-engine` has zero `:feature:*` imports (signature test — this is the guarantee the other 3 consuming-feature blueprints already assume holds)
- Unit: `sourceId` requiredness validated per context

##### 31. Final Verification Checklist
- [ ] `:core:quiz-engine` has zero `:feature:*` imports (module-boundary test passing)
- [ ] `QuizContext` covers all 4 required values, no forked per-feature enums
- [ ] `QuizResult` returned via typed navigation result, no shared mutable global state
- [ ] All 4 consuming feature modules successfully depend on this module
- [ ] Hilt DI graph resolves cleanly

#### `Development_Blueprints/A8_Daily_Quiz_Engine/KMP/02-quiz-session-state-management-resume-flow.md`

##### 4. Objective
Implement `QuizSessionViewModel`'s sealed state machine, trusting B-03's backend-guaranteed idempotent resume rather than building separate client-side resume-detection logic — this is the behavioral core every consuming feature's quiz entry relies on.

##### 5. Business Requirements
§6.4 (state machine: `Assembling → QuestionActive(index) → Submitting → ExplanationShown → (NextQuestion | RetrySet | Completed)`), Edge Case 12 (resume-after-abandonment via simple re-fetch, no separate resume detection).

##### 11. KMP Requirements
- `QuizSessionViewModel` sealed state: `Assembling`, `QuestionActive(index, question)`, `Submitting`, `ExplanationShown(correct, explanation)`, `RetrySetIntro`, `Completed(accuracyPercent, reward)`
- On re-entering a quiz context with an in-progress backend attempt, the ViewModel simply re-calls the same repository fetch — **no separate client-side "is this a resume?" detection logic**, trusting the backend's idempotent response (B-03)
- `QuizRepository.startQuiz(context, childId)` → context-appropriate `GET`; `submitResponse()` → `POST .../responses`; `completeAttempt()` → `POST .../complete`
- `QuizAnalytics` fires `quiz_started` with the correct `context` sourced from the calling feature's parameter (single wrapper, no per-feature duplication)
- Coroutine cancellation on screen exit; stable/immutable state classes to avoid unnecessary recomposition

##### 15. Validation
State transitions are compile-time-restricted to the sealed class's valid paths (no illegal transition possible, e.g. `Assembling → Completed` directly).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| `Assembling` fetch fails (network/server) | Transition to an error-with-retry state, never a silent stuck spinner |
| `Submitting` fails (network) | Optimistic local advance, background retry, never re-prompt an already-answered question |
| Backend returns an in-progress attempt on resume | ViewModel treats it identically to a fresh `Assembling → QuestionActive` transition at the resumed index — no special-cased resume state |
| Process death mid-session | State restored via `SavedStateHandle`, re-fetch confirms via B-03 |

##### 19. Offline First
`QuizRepository` interface is source-agnostic (server vs. locally-bundled) — full offline wiring is K-06; this sub-feature defines the interface contract K-06 implements against.

##### 21. Localization / 22. RTL
N/A (state layer; no UI strings here).

##### 25. Security
No new sensitive data handling; relies entirely on B-03/B-04/B-05's server-side authorization.

##### 27. Testing
- Unit: every state transition in the sealed state machine, shared once in `:core:quiz-engine`, not duplicated per feature (signature test)
- Unit: resume flow — simulate an in-progress backend attempt on re-entry, assert ViewModel re-fetches via the same repository call with no separate resume-detection branch (signature test, Edge Case 12)
- Unit: `Submitting` failure triggers optimistic advance + background retry, never a re-prompt
- Unit: coroutine cancellation on screen exit (no leaked jobs)

##### 31. Final Verification Checklist
- [ ] All sealed state transitions tested, no illegal transition representable
- [ ] Resume-after-abandonment verified via simple re-fetch, no separate client-side detection branch
- [ ] `Submitting` failure never re-prompts an already-answered question
- [ ] `QuizAnalytics` shared across all 4 consumers, no per-feature duplication
- [ ] No coroutine leaks on screen exit

#### `Development_Blueprints/A8_Daily_Quiz_Engine/KMP/03-question-type-renderers-accessibility-paths.md`

##### 4. Objective
Build the 5 first-class question-type renderer composables behind a single dispatcher, sharing one screen skeleton, with mandatory non-visual/non-auditory alternative interaction paths for sequence-ordering, audio-match, and image-match types.

##### 5. Business Requirements
FR-2 (all 5 types first-class, reusable across every consuming context), NFR Accessibility (§1.8: "preview for mobile and screen reader" verified path; image-match/audio-match require non-visual/non-auditory alternatives), Edge Case 7 (media-load-failure graceful skip).

##### 11. KMP Requirements
- `QuestionTypeRenderer` dispatcher switches on `question.type`, delegating to one of the 5 renderers
- `SequenceOrderingRenderer` **must** provide a non-drag, tap-to-place alternative interaction mode (not drag-only) — mandatory accessibility path, not optional
- `AudioMatchRenderer` provides a text-transcript fallback option
- `ImageMatchRenderer` provides descriptive alt-text per option
- Shared screen skeleton across all 5 types: progress indicator ("Question 2 of 5" / dots), question-content area, answer-options area (2–4 cards / drag-or-tap tiles / dual buttons / tap-to-match grid), persistent Hint control
- States per type: Default, Answer-selected-not-yet-submitted, Submitting, Explanation-shown, Media-loading, Media-load-failed-skip
- Media-load-failure → graceful skip (treated as unanswered, brief "comes back another time" notice via `MediaLoadFailureNotice`), never a hard block (Edge Case 7)
- Answer-option grids reflow for tablet (more columns) without changing the interaction model

##### 15. Validation
Client validates a selection/arrangement is present before enabling submit (where applicable per type), never bypassing server-side answer-correctness validation.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Image/audio asset fails to load | `MediaLoadFailureNotice` shown, question treated as unanswered, session proceeds (Edge Case 7) |
| Malformed `prompt_payload` for declared type | Defensive fallback rendering (generic text-only presentation) rather than a crash |
| Hint request fails | Generic encouragement fallback message, non-blocking |

##### 19. Offline First
Renderers consume the same internal question model whether server-fetched (K-02) or locally-bundled (K-06) — no renderer-level branching on data source.

##### 21. Localization / 22. RTL
All question text/audio-transcript/image-alt-text localized (EN/HI/AR/UR); full RTL layout for Arabic-script content across all 5 renderers, including drag/tap-to-place directionality for `SequenceOrderingRenderer`.

##### 25. Security
No new sensitive data handling.

##### 27. Testing
- UI: each of the 5 renderers individually (rendering correctness, selection/arrangement interaction)
- UI: `SequenceOrderingRenderer` tap-to-place path exercised end-to-end **without ever issuing a drag gesture** (signature test, accessibility-mandatory)
- UI: media-load-failure graceful skip — question excluded, session proceeds, no crash
- Accessibility: screen-reader pass per renderer (5 total), verifying alt-text/transcript presence
- UI: tablet reflow test (answer-option grid column count changes, interaction model unchanged)

##### 31. Final Verification Checklist
- [ ] `SequenceOrderingRenderer` tap-to-place path works end-to-end with zero drag gestures issued
- [ ] `AudioMatchRenderer` text-transcript fallback present and functional
- [ ] `ImageMatchRenderer` descriptive alt-text present per option
- [ ] Media-load-failure treated as graceful skip, never a hard error
- [ ] Answer-option grids reflow correctly for tablet without changing interaction model
- [ ] Full RTL layout verified for all 5 renderers with Arabic-script content

#### `Development_Blueprints/A8_Daily_Quiz_Engine/KMP/04-per-answer-explanation-non-punitive-feedback-ui.md`

##### 4. Objective
Build the Per-Answer Explanation Overlay so it renders structurally identically regardless of answer correctness — teaching the correct concept every time, never treating an incorrect answer as a punitive event — as a bottom-sheet over the still-visible question.

##### 5. Business Requirements
FR-3 (immediate, never-skippable explanation, always presented), §2.1 (non-punitive incorrect-answer treatment — supportive iconography, not a harsh red X as the dominant element), §2.2 (explanation content identical regardless of correctness, never hidden or abbreviated for incorrect answers).

##### 11. KMP Requirements
- Bottom-sheet-style overlay, question content remains visible above it (not a full-screen transition)
- Renders **identically in structure** whether `correct=true` or `false` — only the small leading icon and a brief lead-in phrase differ; explanation text/source-citation rendering is the byte-for-byte same code path for both cases
- Correct-answer restatement always shown, regardless of the child's answer
- Supportive iconography for incorrect answers (soft upward-sparkle style, never a dominant harsh red X)
- Pre-fetched — no additional loading state between submission and explanation display (payload already present in `ExplanationShown` state)
- "Next" control advances to next question / retry set / completion per K-02's state machine

##### 15. Validation
N/A (display-only component; correctness already computed server-side by B-04).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| `explanation` payload missing/malformed | Fallback generic "Let's review this together" message, never a blank overlay |
| Source citation absent for a question that doesn't have one | Citation chip simply omitted, not rendered as empty |

##### 19. Offline First
Explanation payload sourced identically whether the question came from server (K-02) or bundled offline set (K-06) — no branching in this component.

##### 21. Localization / 22. RTL
Explanation text/citation fully localized (EN/HI/AR/UR); RTL layout for the bottom sheet, including RTL-correct icon/text ordering.

##### 25. Security
No new sensitive data handling.

##### 27. Testing
- UI: **signature test** — assert the Explanation overlay's semantics tree, with the correct-vs-incorrect icon node excluded from comparison, is otherwise structurally identical between a correct and incorrect answer rendering of the same question
- UI: source-citation chip renders when present, omitted (not blank) when absent
- UI: overlay is genuinely non-blocking of the underlying question content (bottom-sheet, not full-screen)
- Localization: RTL layout verified for the overlay in Arabic

##### 31. Final Verification Checklist
- [ ] Structural-parity signature test passing (correct vs. incorrect rendering, icon node excluded)
- [ ] Explanation is never skippable and always shown after every answer
- [ ] No additional loading state between submission and explanation display
- [ ] Incorrect-answer treatment uses supportive iconography, never a dominant harsh red X
- [ ] RTL layout verified in Arabic

#### `Development_Blueprints/A8_Daily_Quiz_Engine/KMP/05-retry-set-accuracy-independent-completion-experience.md`

##### 4. Objective
Build the Retry Set Entry/Question flow and the Completion/Effort-XP-Reveal screen, with the completion screen's visual treatment provably unaffected by accuracy — the client-side embodiment of the platform's defining hard rule for this feature.

##### 5. Business Requirements
FR-5 (unconditional reward, never visually or structurally conditioned on accuracy), §2.1 (Retry Set Framing — supportive subtitle, not a punishment lap; Effort XP Reveal always positive/celebratory regardless of accuracy), Edge Case 3 (bounded retry, supportive framing on conclusion), Edge Case 11 (no retry-set UI when zero misses).

##### 11. KMP Requirements
- Retry Set Entry screen: visually distinguished framing (e.g., "Let's try these again" subtitle), own short progress indicator separate from the main set's
- Retry questions reuse K-03's type-specific renderers unchanged
- Zero-miss case: skip Retry Set Entry entirely, proceed directly to Completion (Edge Case 11 — no empty/skipped-feeling intermediate step)
- Bounded retry-round conclusion: after the single retry round, session concludes with supportive framing regardless of remaining incorrect answers (Edge Case 3)
- **Completion screen composable must NOT branch its visual treatment (colors, animation, layout) based on `accuracyPercent`** — only the numeric text content legitimately differs
- Always positive/celebratory tone and visual treatment at completion, independent of score

##### 15. Validation
N/A (presentation layer; business rule enforcement is server-side per B-06).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Completion API call fails after main set finishes | Local state preserved, retried with idempotent `client_request_id`, child not forced to re-answer |
| Retry-set fetch fails | Falls back to concluding the session directly with supportive framing rather than blocking on an unavailable retry set |

##### 19. Offline First
Retry-set and completion flow function fully offline against a locally-bundled question set (K-06); completion syncs on reconnect via idempotent `client_request_id`.

##### 21. Localization / 22. RTL
Retry/completion copy fully localized (EN/HI/AR/UR), reviewed for supportive, non-punitive tone in every locale; RTL layout for both screens.

##### 25. Security
No new sensitive data handling; this sub-feature's core value is a UX-integrity guarantee, not a data-security one.

##### 27. Testing
- UI: **signature test** — render Completion screen with `accuracyPercent=0` and `accuracyPercent=100`, assert the rendered composable tree (excluding only the numeric text content) uses identical component types, colors, and layout structure in both cases
- UI: Retry Set Entry framing visually distinguished from main-set question screens
- UI: zero-miss flow skips Retry Set Entry entirely, no empty intermediate screen shown
- UI: bounded-retry conclusion after 1 round, supportive copy shown regardless of remaining misses (no third round offered client-side, mirroring B-05's server enforcement)

##### 31. Final Verification Checklist
- [ ] Completion screen structural-identity signature test passing (0% vs. 100% accuracy)
- [ ] Retry Set Entry visually distinguished, own progress indicator
- [ ] Zero-miss flow skips Retry Set Entry with no empty intermediate step
- [ ] Bounded retry (1 round) enforced client-side, consistent with B-05's server enforcement
- [ ] Completion tone/visual treatment always positive regardless of score
- [ ] All 6 completion/retry analytics events verified firing correctly

#### `Development_Blueprints/A8_Daily_Quiz_Engine/KMP/06-offline-quiz-bank-sync-withdrawn-question-handling.md`

##### 4. Objective
Implement a source-agnostic `QuizRepository` backing (server vs. Room-cached bundled question set) so the entire question-rendering/answering/explanation code path (K-02–K-05) is identical regardless of source, with a sync outbox that correctly surfaces the server's withdrawn-question exclusion outcome without local error.

##### 5. Business Requirements
FR-10 (offline attempts supported for downloaded question banks, idempotent sync), FR-11 (withdrawn-question exclusion applies even to late-syncing offline attempts), Edge Case 4 (stale client-side weak-skill framing doesn't cause incorrect double-counting — server is authoritative), Edge Case 7 (media-load-failure handling applies equally offline).

##### 11. KMP Requirements
- `QuizRepository` implementable by either a server-backed or a locally-bundled (Room-cached) data source through the same interface — `QuizSessionViewModel` (K-02) is unaware of which is active
- Offline responses queue in a shared outbox keyed by `client_request_id`
- Local flow: Remote Data (B-03) → Repository → Local Storage (Room) → UI (K-03/K-04)
- Network-recovery listener triggers outbox flush automatically
- Sync-time handling: when a locally-answered question was withdrawn server-side in the interim, the client simply accepts the server's response (exclusion is server-authoritative per B-06) without local error or double-counting
- Stale client-side "weak skill" framing at download time never causes incorrect local double-counting — client trusts server's authoritative recalculation on sync (Edge Case 4)
- `OfflineQuizIndicator` component shown on any quiz screen while offline

##### 15. Validation
Outbox entries validated for well-formed `answer_json` before local queueing (same per-type validation as K-03's renderers already enforce at submission time).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Offline with bundled question set | Quiz functions fully, results queue locally |
| Offline without a bundled set for the requested context | Entry point shows a "download to practice offline" affordance rather than a broken quiz attempt |
| Sync-time server response indicates a question was withdrawn and excluded | Client accepts the server's authoritative result silently, no error surfaced, no local recalculation attempted |
| Duplicate outbox flush attempt (e.g., app relaunch mid-sync) | Idempotent via `client_request_id`, safely re-flushable |
| Network recovery mid-flush | Outbox resumes from last unsynced entry, no duplicate submissions |

##### 19. Offline First
This sub-feature **is** the offline-first implementation: Initial local load → remote refresh → offline read → offline action → retry → sync, per the platform's standard offline-first flow.

##### 21. Localization / 22. RTL
Bundled question payload retains the same localized fields as the server response — no re-fetch needed for locale changes mid-offline-session (locale is baked into the bundle at download time, consistent with each consuming feature's own offline-locale handling).

##### 25. Security
No new sensitive data handling; offline-cached question content is standard learning-progress data under existing platform child-data handling policies (consistent with PRD §12.4).

##### 27. Testing
- Integration: **signature test** — offline attempt answers a question later withdrawn server-side; sync occurs; assert the client accepts the server's exclusion outcome without local error, crash, or incorrect recalculation (Edge Case 4/FR-11 client-side verification)
- Unit: outbox flush idempotency — duplicate flush attempt produces no duplicate server-side submissions
- Integration: full offline flow — download fixture bundle → offline → answer 5 questions → reconnect → verify exactly the expected number of sync calls, each with a unique `client_request_id`
- Unit: `OfflineQuizIndicator` visibility tied correctly to network state

##### 31. Final Verification Checklist
- [ ] `QuizSessionViewModel` requires no code changes to function against either repository implementation
- [ ] Offline attempt on a since-withdrawn question syncs without local error, matching server's exclusion outcome (signature test passing)
- [ ] Outbox flush idempotent — no duplicate submissions on repeated/interrupted flush attempts
- [ ] `OfflineQuizIndicator` correctly reflects network state
- [ ] No main-thread blocking on offline bundle read/write

#### `Development_Blueprints/A8_Daily_Quiz_Engine/KMP/07-parent-concept-summary-report.md`

##### 4. Objective
Render the quiz-specific concept-level summary within the Parent Area (Parent Dashboard → Child Progress), consuming B-07's API, showing concepts practiced/mastered rather than a raw score, and linking into the broader concept-detail drill-in shared with A.5's own mastery reporting screen.

##### 5. Business Requirements
FR-6 (concept-level, not score-level, headline), Acceptance Criteria (§1.9: report lists concepts like "Practicing: Surah Al-Fatiha recitation"), Edge Case 10 (multi-domain attribution displayed distinctly per skill), §1.12 Empty States (first-time-learner framing).

##### 11. KMP Requirements
- Renders a concept list (`skill`, `status`, `recent_accuracy_trend`) with **no raw numeric score as the visual headline** — concept status is the primary visual element
- Multi-domain sessions display each skill's contribution as a distinct row, never a merged/ambiguous combined item (Edge Case 10)
- First-time-learner (zero quiz history) state renders distinct first-time framing copy, not a stark "no data" empty state
- Tapping a concept row navigates to Concept Detail Drill-in (shared component with A.5 §1.18 — reuse, do not fork)
- `period` selector (e.g., weekly) if the container screen supports period switching

##### 15. Validation
N/A (display-only; data correctness owned by B-07).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| B-07 unavailable | Friendly "concept summary will be ready again soon" message, does not block the rest of the Parent Progress Report |
| Zero quiz history | First-time framing panel, not a blank/error state |
| Skill Mastery status enrichment degraded (per B-07 §18) | Panel still renders skill names with accuracy-trend data, no blank rows |

##### 19. Offline First
N/A (Parent Area is an online, low-frequency-access surface; not part of the child's offline quiz-taking flow).

##### 21. Localization / 22. RTL
Concept/status/trend labels fully localized (EN/HI/AR/UR); RTL layout for the panel, consistent with the rest of the Parent Progress Report container.

##### 25. Security
No new sensitive data handling; standard parent-session-scoped access to their own family's child data only.

##### 27. Testing
- UI: **signature test** — assert the panel's headline visual element is the concept/status list, not a raw numeric score (structural/semantics-tree assertion)
- UI: multi-domain summary displays each skill as a distinct row
- UI: first-time-learner state renders distinct framing, not a blank/error empty state
- Unit: ViewModel correctly maps B-07's response to `QuizConceptSummaryUiState`

##### 31. Final Verification Checklist
- [ ] No raw numeric score rendered as the panel's visual headline (signature test passing)
- [ ] Multi-domain session displays each skill as a distinct row, never merged
- [ ] First-time-learner state distinct from a blank/error empty state
- [ ] Concept Detail Drill-in reuses A.5's shared component, not a forked implementation
- [ ] Integration point with C.22's container confirmed against that feature's actual blueprint, not assumed
- [ ] RTL layout verified

## A9 — Feature_A9_Skill_Tree_Mastery_Engine

PRD: `PRD_Documents/Child App (1-12)/Feature_A9_Skill_Tree_Mastery_Engine.md`

Coverage: 11 mandatory FR records; all preserved verbatim below. Feature has 9 inventory records including components/states. Components and states must not inflate independently executed screen count.

### Existing screenshot candidates

- `Screens/Mobile App/Quiz Engine/Quiz Complete-01.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Complete-02.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Question-01.png` — visually inspected
- `Screens/Mobile App/Quiz Engine/Quiz Question-02.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Question-03.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Question-04.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Result-01.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Result-02.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Result-03.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Result-04.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Result-05.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Result-06.png` — inventoried only
- `Screens/Mobile App/Quiz Engine/Quiz Result-07.png` — inventoried only

### Complete normative functional coverage

### 1.7 Functional Requirements

**FR-1** The Mastery Engine exposes exactly six skill states across every domain: `Locked → Ready → Learning → Practicing → Mastered → Needs Refresh` (source §6.3/§21.9 — restated here as the canonical, domain-agnostic definition; A.5 documents the Quran/Arabic-specific UI treatment of these same states).
**FR-2** Mastery score is computed from a weighted combination of: accuracy, independent-attempt count, recency of evidence, item difficulty, and cross-question-format transfer (source §21.9 "Mastery score combines accuracy, independent attempts, recency, difficulty, and transfer across question types") — this formula is implemented once, centrally, and parameterized per domain/skill rather than reimplemented per domain.
**FR-3** The child-facing UI must show progress (a state label, a progress ring, etc.) without ever revealing the raw numeric mastery/confidence score (source §21.9, restated as a hard product rule the engine's API contract enforces by never including a raw score field in any child-facing response).
**FR-4** A child can retry any practice item without losing XP or breaking a streak — mastery-affecting accuracy and reward-affecting participation are fully decoupled systems (source §6.3, shared architectural principle with A.8's quiz engine).
**FR-5** Single-session mastery is disallowed by design: reaching `Mastered` requires repeated correct performance across more than one practice session and, where applicable, across more than one question format (source: A.5 FR-7, generalized here as the engine's domain-agnostic rule — "Mastery requires correct performance across different question forms and across more than one session").
**FR-6** Quiz Completion Result flow (the shared result screen after any quiz/practice attempt): validate the attempt and its idempotency key → calculate skill evidence → post the reward-ledger entry (unconditional, per A.8 FR-5) → show a result screen with **strengths and exactly one concrete next step** → offer `Review Mistakes`, `Try Again`, or `Continue` → record a parent-report event (source §21.10 "Quiz Completion" flow, items 1–7).
**FR-7** "Review Mistakes" re-presents the specific items missed (with their explanations, reusing A.8's Per-Answer Explanation pattern) without re-triggering a scored attempt. "Try Again" launches a fresh attempt (new `attempt_id`) of the same or an equivalent item. "Continue" simply proceeds, with no penalty for declining either of the other two options.
**FR-8** Spaced Repetition Scheduling computes a `next_review_at` timestamp per `(child_id, skill_id)` based on a decay function over time-since-`last_evidence_at`, weighted by mastery strength — generalized from A.5's Quran/Arabic-specific scheduler into the shared engine, with the same daily-prompt cap (default 2) to avoid overwhelming the child (source: A.5 §5 item 6, generalized here).
**FR-9** The engine must support domain-agnostic skill-graph definitions: any domain can define its own `skill_node` catalog, prerequisite graph, and content linkage, while relying on the shared engine for state-machine evaluation, mastery scoring, and spaced-repetition scheduling — no domain may implement a parallel, divergent mastery calculation.
**FR-10** A withdrawn/safety-flagged quiz item's evidence is excluded from mastery-score computation even if the response was recorded before withdrawal (shared rule with A.8 FR-11, enforced once here at the mastery-aggregation layer so every domain inherits it automatically).
**FR-11** The engine exposes a domain-agnostic Parent Report contract: concept-level summaries (skill labels + state + trend), never a single raw aggregate score as the headline metric (source: shared principle with A.5 FR-17/A.6/A.8 §3.4).

### Ordered source inventory

### 1.18 Screen Inventory (Complete — Zero Missing)

| # | Screen / Component | Type | Entry Points | Exit Points |
|---|---|---|---|---|
| 1 | Quiz Completion Result Screen (shared, generic) | Screen | End of any quiz/practice attempt (any domain, any A.8 `QuizContext`) | Review Mistakes / Try Again / Continue |
| 2 | Strengths Summary Component | Component | Quiz Completion Result | N/A |
| 3 | "One Next Step" Recommendation Card | Component | Quiz Completion Result | Relevant practice/content screen if tapped |
| 4 | Review Mistakes Screen | Screen | Quiz Completion Result "Review Mistakes" | Back to Result / Continue |
| 5 | Try Again — Fresh Attempt Launch | Screen transition | Quiz Completion Result "Try Again" | New quiz/practice session |
| 6 | Mastery State Transition Celebration (generic, domain-agnostic wrapper around A.5's mastery celebration) | Modal | Any skill crossing into Mastered, any domain | Dismiss → relevant skill tree |
| 7 | Needs-Refresh Cross-Domain Daily Cap Notice (internal-only state, surfaces via each domain's own prompt UI) | Component | Spaced Repetition Scheduler output | Domain-specific review session |
| 8 | Parent Cross-Domain Mastery Summary (Parent Area) | Screen (Parent Area) | Parent Dashboard → Child Progress → Learning (aggregated across domains) | Domain-specific detail (e.g., A.5's Quran/Arabic report) |

### Exact mobile UX and behavior sources

### 1.9 Acceptance Criteria

- Given a child answers a practice item correctly on their very first attempt in their very first session, when mastery is evaluated, then the skill does **not** transition directly to `Mastered` — it must show evidence across more than one session per FR-5.
- Given a child views any skill's progress, when the UI renders, then no raw numeric mastery/confidence score is ever displayed — only a state label and/or a progress-ring visualization.
- Given a child completes a quiz with some mistakes, when the Result screen renders, then it shows strengths, exactly one concrete next-step recommendation, and the three options `Review Mistakes`/`Try Again`/`Continue` — never just a bare score.
- Given a child selects `Try Again`, when the new attempt is created, then it is a genuinely new `attempt_id` (fresh idempotency scope), not a re-submission of the original attempt.
- Given a child selects `Continue` without reviewing mistakes or retrying, when they proceed, then there is no penalty to their reward or streak for declining those options.
- Given a skill's mastery decays into `Needs Refresh` and the child completes a spaced-review session, when evaluated, then the state returns to `Mastered` (not back to `Learning` or `Practicing` from scratch, since the underlying knowledge wasn't lost, just due for reinforcement).
- Given a new learning domain is added by Admin (e.g., a future Islamic Facts skill tree), when its `skill_node` catalog is configured, then it inherits state-machine evaluation, mastery scoring, and spaced-repetition scheduling automatically, with zero new mastery-calculation code required.

### 1.10 Edge Cases

1. A child answers correctly across two sessions but always via the exact same question format (e.g., always multiple choice, never audio match) for a skill that has multiple available formats → the cross-format-transfer component of the mastery formula appropriately limits confidence growth, keeping the skill in `Practicing` rather than `Mastered` until transfer evidence exists, consistent with FR-2/FR-5.
2. A child has overwhelming evidence of mastery on a skill, then gets one unusual wrong answer (e.g., a misclick) → a single low-quality data point should not catastrophically collapse a strongly-evidenced mastery state; the recency/weighting formula must be resilient to single-attempt noise, not just simplistically averaging.
3. Two different domains (e.g., a Quran skill and a hypothetical future Islamic Facts skill) are tagged on the same quiz question (cross-domain question reuse) → mastery evidence updates correctly and independently for both domains' respective skill nodes from the same single response event, without conflation.
4. A child reaches `Needs Refresh` on multiple skills simultaneously across different domains on the same day → the platform-wide daily-prompt cap (default 2, per FR-8) applies globally across all domains combined, not per-domain (a child should not see 2 Quran refreshes AND 2 Arabic refreshes on the same day if the intent is to cap total daily review load) — this requires the engine to coordinate the cap centrally rather than each domain enforcing its own independent cap.
5. A child selects `Review Mistakes` from the Quiz Completion Result, reviews the explanations, then closes the app without selecting `Continue` explicitly → the underlying quiz attempt is still considered complete (reward already issued per A.8's unconditional rule) regardless of whether the child formally dismisses the result screen — no dangling "incomplete" state should result from simply not tapping a final button.
6. A new domain is configured by Admin with a skill-node catalog that has a prerequisite cycle (e.g., copy-paste error from another domain's graph) → the shared engine's cycle-detection validation (same mechanism specified in A.5 §9 for curriculum graphs) applies uniformly to any domain's graph, not just Quran/Arabic's.
7. A child's mastery-score computation coincides with a quiz-completion event for a withdrawn-question-containing attempt (per FR-10) — the score computed and the score that *would have been* computed without the exclusion are different; this difference itself should be logged for content-quality monitoring (a spike in withdrawal-driven exclusions for a given skill might indicate a content-quality issue in that skill's question pool worth flagging to Admin).
8. A child attempts to "game" the spaced-repetition scheduler by intentionally answering incorrectly on a skill they've already mastered, theoretically to trigger more frequent review sessions (an unusual but conceivable motivation, e.g., wanting more practice) → the system doesn't need to detect or prevent this; if a child genuinely wants more practice, more low-confidence evidence naturally extending their practice opportunities is not a harmful outcome, so no special anti-gaming logic is required here (distinct from genuinely harmful gaming like reward-farming, which IS prevented elsewhere).
9. Mastery-score formula parameters (the relative weights of accuracy/recency/difficulty/transfer) are updated by Admin for model-quality-improvement reasons → already-computed historical mastery states are **not retroactively recalculated** under the old evidence with new weights (which could cause confusing, unexplained state changes for children with no new activity) — the new weights apply only to future evidence-driven recalculations, with a clear changelog/versioning of which formula version produced which historical state.
10. A child's account is merged/migrated (e.g., a rare data-correction scenario) and brings mastery evidence from two previously-separate `child_id` records for the same skill → the engine must have a defined, tested reconciliation behavior (e.g., taking the union of evidence, recalculating from scratch) rather than undefined behavior from a naive merge.
11. A `skill_node`'s prerequisite is itself a node from a different domain (a genuinely cross-domain prerequisite, e.g., a hypothetical future "basic Arabic literacy" prerequisite gating a Quran-domain node) → the engine's prerequisite-evaluation logic must support cross-domain references without special-casing, since `skill_node` and `skill_node_state` are domain-agnostic tables by design.
12. The spaced-repetition decay function computes a `next_review_at` date that has already passed by the time the batch scheduler runs (e.g., due to a scheduler outage/delay) → the review is still correctly queued (not skipped) on the next successful run, with the existing daily-prompt cap preventing a backlog from dumping many overdue reviews on the child at once.

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Mastery-score computation service unavailable post-quiz | Reward issuance (unconditional, A.8) still completes independently; mastery update queues for retry, Quiz Completion Result screen shows strengths/next-step based on the most recent available state rather than blocking on a synchronous recomputation |
| Spaced Repetition Scheduler batch job failure | No reviews lost — overdue reviews queue correctly on next successful run (Edge Case 12), capped per the standing daily limit |
| Cross-domain prerequisite graph contains a cycle (admin error) | Rejected at admin-save time with the cycle path shown (shared validation mechanism with A.5) |
| Quiz attempt's idempotency key resubmitted (e.g., network retry of the completion call) | Returns the original mastery/reward result, never double-processes evidence |

### 1.12 Empty States
- New child, zero mastery evidence for a domain → all relevant skill nodes show `Locked`/`Ready` states appropriately per prerequisite graph, never an error or blank tree (consistent with A.5's first-time experience).
- Quiz Completion Result with zero mistakes to review → "Review Mistakes" option simply isn't offered (only `Try Again`/`Continue` shown), consistent with A.8 Edge Case 11.

### 1.13 Loading States
- Quiz Completion Result: brief "calculating your progress..." state if mastery computation hasn't completed synchronously within a short budget, though typically near-instant given the p95 < 300ms target.

### 1.14 Offline States
- Mastery-state display uses last-synced cached state when offline; recomputation requiring fresh evidence happens upon reconnect sync, consistent with A.5/A.8's offline patterns.

### 1.15 Permission States
- No new runtime permissions specific to this engine.

### 1.16 User Flow (Narrative)

A child completes a quiz/practice attempt in any domain (Quran, Arabic, Tajweed, or a future domain) via A.8's shared Quiz Engine → the attempt's final response submission triggers this Mastery Engine's evidence-calculation step → mastery score and skill state are recomputed for every skill tagged on the attempt's questions → the Quiz Completion Result screen renders strengths + one next-step recommendation + `Review Mistakes`/`Try Again`/`Continue` → the child picks one → if mastery crosses into `Mastered`, the relevant domain's skill-tree UI (e.g., A.5's map) reflects the unlock in real time → over subsequent days, the Spaced Repetition Scheduler may surface a `Needs Refresh` prompt for that skill once its evidence decays past the configured threshold.

### 2.1 Quiz Completion Result — Design Requirements

- **Purpose:** Close out any quiz/practice attempt (regardless of originating domain) with genuinely useful, concept-level feedback and a clear, low-pressure set of next-action choices.
- **Components:** A "Strengths" section (1-2 short, specific, positively-framed statements — e.g., "You're getting really confident with Surah Al-Fatiha!"), a single "Next Step" recommendation card (one concrete, specific suggestion, never a vague "keep practicing"), and three equally-weighted, non-hierarchical action buttons: `Review Mistakes` (only shown if mistakes exist), `Try Again`, `Continue`.
- **States:** All-correct (Strengths section is more prominent, no Review Mistakes option), Some-incorrect (Strengths + Next Step + all three options), Mastery-threshold-crossed-this-session (an additional small celebratory accent, layered on top of the standard result screen, not replacing it).
- **Accessibility:** All three action buttons equally reachable/labeled via screen reader; no default-focused button implies a "correct" choice (this is a values-neutral decision point for the child, not a forced-default).
- **Responsive Rules:** Single-column, consistent with the platform's general single-primary-focus screen philosophy (though here there are three valid equally-weighted actions, not one primary CTA — a deliberate deviation reflecting genuine user choice).

### 2.2 Screen Image Generation Prompts

**Screen: Quiz Completion Result**
- *Prompt 1 (English):* "Mobile app quiz results screen UI mockup for a children's learning app. Warm off-white background. At the top, a small celebratory but calm icon (a gentle upward sparkle), below it a 'Strengths' section with two short positive statements in rounded text bubbles. Below that, a distinct highlighted card labeled 'Next Step' with a single concrete suggestion and a small icon. At the bottom, three equally-sized rounded buttons side by side or stacked: 'Review Mistakes' (outlined secondary style), 'Try Again' (outlined secondary style), and 'Continue' (filled warm gold primary style) -- all three clearly tappable and not implying a forced hierarchy beyond Continue's natural visual weight as a primary action. No raw percentage or score number displayed anywhere. Calm, encouraging, educational aesthetic, soft shadows, rounded corners, no realistic human faces."
- *Prompt 2 (Arabic RTL):* "نفس شاشة نتائج الاختبار لتطبيق تعليم للأطفال، بتخطيط من اليمين إلى اليسار بالكامل. خلفية بيج فاتح دافئ. في الأعلى أيقونة احتفالية هادئة صغيرة (بريق صاعد لطيف)، تحتها قسم 'نقاط القوة' بعبارتين إيجابيتين قصيرتين في فقاعات نص مستديرة. أسفل ذلك بطاقة مميزة بعنوان 'الخطوة التالية' مع اقتراح واحد محدد وأيقونة صغيرة. في الأسفل ثلاثة أزرار مستديرة بحجم متساوٍ جنبًا إلى جنب أو مرصوصة: 'مراجعة الأخطاء' (نمط ثانوي محدد الحواف)، 'حاول مرة أخرى' (نمط ثانوي محدد الحواف)، و'استمرار' (نمط أساسي ذهبي دافئ معبأ) — جميعها قابلة للنقر بوضوح وبدون فرض تسلسل هرمي إلزامي بخلاف الثقل البصري الطبيعي لزر الاستمرار كإجراء أساسي. بدون أي نسبة أو رقم خام للنتيجة ظاهر في أي مكان. طابع هادئ ومشجع وتعليمي، ظلال خفيفة، زوايا دائرية، بدون وجوه بشرية واقعية."

---

### 6.1 Technical Requirements
Kotlin, Jetpack Compose, MVVM, Clean Architecture, module `:core:mastery-engine` (a **shared core module**, mirroring A.8's `:core:quiz-engine` pattern), consumed by `:feature:learn` (A.5) and any future domain feature module. Depends on `:core:design-system`, `:core:network`.

### 6.2 Screen Mapping
`QuizCompletionResultScreen` is a single reusable Composable (analogous to A.8's `QuizSessionScreen`) rendered immediately after any quiz session completes, regardless of originating domain/feature.

### 6.3 Navigation Flow
Launched by `:core:quiz-engine`'s session-completion handoff (A.8 §6.3's `QuizResult` callback triggers navigation into this screen) before returning control to the calling feature — i.e., the flow is: consuming feature → `:core:quiz-engine` session → `:core:mastery-engine` result screen → back to consuming feature.

### 6.4 State Management
`MasteryResultViewModel` fetches `GET /v1/mastery/result/{attempt_id}` once on entry; the three action buttons (`Review Mistakes`/`Try Again`/`Continue`) are modeled as a sealed `ResultAction` the calling feature handles via its own navigation (e.g., A.5's Learn tab routes `TryAgain` back into a fresh A.8 quiz session; A.3's Stories context might route `Continue` into "Next Learning").

### 6.5 API Mapping
`MasteryRepository.getResult()` → `GET /v1/mastery/result/{attempt_id}`; domain skill-tree screens (A.5) call `MasteryRepository.getSkillStates(domain)` → `GET /v1/mastery/skills?domain=`, with the response DTO **structurally containing no raw score field** (a Kotlin data class with no numeric confidence field defined at all, mirroring the backend's schema-level guarantee).

### 6.6 Analytics Mapping
`MasteryAnalytics` fires `quiz_result_screen_shown` and the three selection events; domain feature modules (A.5) consume the same shared analytics interface rather than each defining a parallel one.

### 6.7 Offline Support
Skill-state display uses cached last-synced state when offline (Room-cached `skill_node_state` rows); the Result screen itself requires connectivity (mastery computation is server-side), consistent with other server-computed-feedback patterns in the app (e.g., A.5's AI pronunciation feedback) — offline quiz completions defer their Result screen until reconnect, showing a simpler "saved, will show your results when you're back online" interim state instead.

### 6.8 Deep Linking
Not directly deep-linked; always reached via the quiz-completion handoff from `:core:quiz-engine`.

### 6.9 Push Notifications
Spaced-review reminder notifications (owned by A.12, cross-domain-capped per §5 item 5) deep-link into the relevant domain's own skill-tree entry point (e.g., A.5's `noorheroes://learn/node/{node_id}`), not into this engine's screens directly.

### 6.10 Testing Strategy
- Unit: `MasteryResultViewModel`'s handling of the has_mistakes-conditional `Review Mistakes` button visibility; DTO reflection test confirming no raw score field exists anywhere in `:core:mastery-engine`'s public data classes.
- UI tests: all three result-screen action buttons render with equal visual weight (no implied "correct choice" styling beyond Continue's natural primary-action treatment); Result screen never displays a percentage/score number anywhere in its semantics tree.
- Integration: full quiz-completion → mastery-result → Try-Again-relaunches-fresh-attempt flow, verified across at least two different domains (e.g., a Quran context and a Dua-recall context) using the same shared module code path.

---

### 13.1 Test Plan Summary
Coverage spans: cross-domain extensibility (signature architectural test), no-single-session-mastery enforcement, no-raw-score-exposure, cross-domain spaced-repetition capping, formula-version governance, and all 12 edge cases from §1.10.

### 13.2 Test Cases — Happy Path
1. Child answers correctly across two separate sessions and at least two question formats for a skill → transitions to `Mastered`; Result screen after the second session shows the mastery celebration layered on the standard result screen.
2. Child completes a quiz with 2 mistakes, selects `Review Mistakes`, reviews explanations, then separately selects `Try Again` → a fresh attempt is created and scored independently.
3. A fictitious new domain is configured via Admin data-only changes and works end-to-end through the shared engine with zero new code deployed.

### 13.3 Edge Cases
All 12 items from §1.10.

### 13.4 Negative Cases
- Answer correctly 10 times in one session → state does not reach `Mastered`.
- Request `GET /v1/mastery/skills` and inspect the response for any numeric score field → none exists.
- Simulate 3 due Quran skills + 2 due Arabic skills on the same day → exactly 2 total returned as due, not 4.
- Change the active formula version, then re-fetch an unrelated child's existing `skill_node_state` with no new evidence → score and `formula_version` unchanged.

### 13.5 Regression Cases
Full Mastery Engine suite re-run on every release touching `:core:mastery-engine`, the shared Mastery Service, or any domain consumer (A.5, and any future domain).

### 13.6 Automation Cases
End-to-end: full multi-session mastery journey across two question formats; cross-domain daily-cap automated test; fictitious-new-domain extensibility automated test (run periodically as an architectural-integrity regression check, not just at initial launch).

---

### Corresponding KMP blueprint requirements

#### `Development_Blueprints/A9_Skill_Tree_Mastery_Engine/KMP/01-shared-mastery-engine-core-module.md`

##### 4. Objective
Stand up `:core:mastery-engine` with `MasteryRepository`, score-free DTOs, Hilt DI wiring, Retrofit networking against B-04/B-05/B-06, and Room caching — the dependency every other KMP sub-feature in this feature (K-02 through K-06) and every domain consumer builds on.

##### 5. Business Requirements
- FR-3: no raw numeric mastery/confidence field anywhere client-side, enforced structurally in the DTOs themselves (Android AI Prompt item 2).
- NFR-Extensibility: consumed by `:feature:learn` today, designed for future domain modules to adopt without new engine work.
- Architecture requirement (A.9 PRD §6.1): module mirrors `:core:quiz-engine`'s established pattern.

##### 11. KMP Requirements
- **`MasteryApi`:** Retrofit interface with suspend functions mapping to `GET /v1/mastery/result/{attemptId}`, `GET /v1/mastery/skills`, `POST /v1/mastery/review-due`.
- **`MasteryRepository`:** `getResult(attemptId): QuizResultDto`, `getSkillStates(domain): List<SkillStateDto>`, `getReviewDue(childId): List<DueSkillDto>` — remote-first with Room-cached fallback for `getSkillStates` (offline-first per A.9 PRD §6.7), remote-only (no cache) for `getResult` (server-computed feedback, requires connectivity per K-04's design).
- **DTOs:** `SkillStateDto` and any other public data class in this module must contain NO field of numeric type named matching `/score|confidence/i` — enforced by a reflection-based unit test (Android AI Prompt item 2).
- **Room caching:** `SkillNodeStateEntity`/`MasteryDao` cache the last-synced `skill_node_state` per child/skill for offline display (K-04 consumes this).
- **Hilt DI:** `MasteryEngineModule` provides `MasteryApi`, `MasteryRepository`, `MasteryDao` bindings, following `:core:quiz-engine`'s existing DI module structure.

##### 15. Validation
DTO parsing via Retrofit's Moshi/kotlinx.serialization converter (whichever the platform standard is per `CORE_NETWORK_INSTRUCTIONS.md`); malformed responses surface as a typed `MasteryApiException`, not a raw parse crash.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Network failure on `getSkillStates` | Fall back to Room-cached last-synced state, surface a "may be outdated" signal to the ViewModel layer (consumed by K-03's renderer) |
| Network failure on `getResult` | Propagate as a typed error to K-02's ViewModel — no cache fallback (this data requires a live server computation) |
| Malformed/unexpected API response shape | Typed `MasteryApiException`, logged via `:core:logger`, does not crash the app |

##### 19. Offline First
`getSkillStates` is offline-capable via Room cache (remote-first, cache-fallback). `getResult` is NOT offline-capable by design (server-computed) — K-04 owns the offline-completion interim-state handling around this constraint.

##### 21. Localization
N/A directly in this module (raw state enums/domain keys only; human-readable label mapping and localization happen in K-03's renderer and K-02's screen).

##### 22. RTL
N/A (data layer, no UI in this module).

##### 25. Security
No new sensitive data handling; mastery-progress metadata only, no raw content/voice data (consistent with A.9 PRD §12.4).

##### 27. Testing
- Unit: `MasteryRepositoryImpl` remote/cache-fallback branching logic.
- **DTO reflection test (mandatory):** enumerate every public data class in `:core:mastery-engine`, assert none contains a numeric field matching `/score|confidence/i` (Android AI Prompt item 2).
- Unit: DTO parsing against representative B-04/B-05/B-06 response fixtures.

##### 31. Final Verification Checklist
- [ ] Module builds and is registered in `settings.gradle.kts`
- [ ] DTO reflection test passing (no score/confidence field anywhere)
- [ ] `MasteryRepository` remote-first/cache-fallback behavior verified for `getSkillStates`
- [ ] `getResult` correctly has no offline fallback (by design)
- [ ] Room cache entity/DAO working, indexed correctly
- [ ] Hilt DI graph resolves cleanly
- [ ] No dependency from this core module back onto any `:feature:*` module
- [ ] `:feature:learn` successfully migrated to consume this module

#### `Development_Blueprints/A9_Skill_Tree_Mastery_Engine/KMP/02-quiz-completion-result-screen.md`

##### 4. Objective
Build `QuizCompletionResultScreen(attemptId: String) -> ResultAction` as a single reusable, domain-blind Composable backed by `MasteryResultViewModel`, with equal-weight action buttons, conditional "Review Mistakes" visibility, and full accessibility/localization/RTL support.

##### 5. Business Requirements
- FR-6, FR-7 (via B-06 consumption).
- §2.1 UX Requirements: Strengths section, single Next Step card, three equally-weighted non-hierarchical buttons (`Review Mistakes` only if mistakes exist).
- §2.1 Accessibility: all three buttons equally reachable/labeled via screen reader; no default-focused button implies a "correct" choice.
- Screen Inventory #1-3: Quiz Completion Result Screen, Strengths Summary Component, "One Next Step" Recommendation Card.

##### 11. KMP Requirements
- **Composable signature:** `QuizCompletionResultScreen(attemptId: String, onAction: (ResultAction) -> Unit)` — no domain-specific logic inside; all navigation decisions delegated to the caller via `onAction`.
- **`MasteryResultViewModel`:** fetches `MasteryRepository.getResult(attemptId)` once on entry (`init` block or `LaunchedEffect`), exposes a `StateFlow<ResultUiState>` (Loading/Success/Error).
- **Conditional Review Mistakes button:** rendered ONLY when `has_mistakes == true` — exactly two buttons (`Try Again`, `Continue`) when `false` (Android AI Prompt item 3).
- **Equal visual weight:** `Review Mistakes` and `Try Again` use IDENTICAL secondary-button design-system tokens; `Continue` uses the standard primary-button token (its only differentiation being the platform's normal primary/secondary convention, not an implied "better choice").
- **Mastery celebration layering:** when `transitioned: true` toward `mastered` is detected in the result (via K-01's skill-state data, cross-referenced), layer a small celebratory accent on top of the standard result screen, per §2.1 States — never replacing the standard layout.
- **Loading state:** brief "calculating your progress..." shown if the fetch hasn't resolved within a short budget.

##### 15. Validation
`attemptId` passed in must be non-blank; ViewModel surfaces an error state if the fetch fails or `attemptId` is invalid.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| `getResult()` fetch fails (network/server error) | Error state shown with a retry affordance; never silently blank |
| `has_mistakes = false` | Exactly two buttons rendered (Try Again, Continue) |
| Fetch pending beyond a short budget | "calculating your progress..." loading state (near-instant given B-06's p95 target) |

##### 19. Offline First
This screen requires connectivity (server-computed feedback) — per A.9 PRD §6.7, offline quiz completions defer showing this screen entirely; that deferral logic lives in K-04, not here. This screen itself assumes it's only ever launched when connectivity is available.

##### 21. Localization
All strings (`strengths` display wrapper text, `next_step` label/reason if not already localized server-side, button labels "Review Mistakes"/"Try Again"/"Continue") must be localized EN/HI/AR/UR via `:core:design-system`'s string-resource pattern.

##### 22. RTL
Full RTL layout support for Arabic/Urdu — button order, icon mirroring (the "gentle upward sparkle" accent), text alignment all mirror correctly; verified via RTL-mode UI tests.

##### 25. Security
No raw score ever rendered (enforced upstream by K-01's DTOs having no such field to begin with — this screen literally cannot display what it doesn't receive).

##### 27. Testing
- Unit: `MasteryResultViewModel`'s has-mistakes-conditional button-visibility logic.
- Unit: DTO reflection test confirming no raw score field anywhere in `:core:mastery-engine`'s public data classes (covered in K-01, referenced here as a dependency).
- UI test: `has_mistakes = false` → exactly two buttons present, not three (Android AI Prompt item 3).
- UI test: `Review Mistakes` and `Try Again` render with IDENTICAL secondary-button styling tokens (Android AI Prompt item 4).
- UI test: Result screen never displays a percentage/score number anywhere in its semantics tree (accessibility-tree scan).
- Integration test: full quiz-completion → mastery-result → Try-Again-relaunches-fresh-attempt flow, verified across at least two different domains (e.g., a Quran context and a Dua-recall context) using the same shared module code path.

##### 31. Final Verification Checklist
- [ ] Zero domain-specific logic inside the shared Composable
- [ ] `has_mistakes=false` → exactly two buttons (verified by UI test)
- [ ] Review Mistakes / Try Again use identical secondary-button tokens
- [ ] No percentage/score anywhere in the semantics tree (accessibility-tree scan test)
- [ ] Full EN/HI/AR/UR localization + RTL mirroring verified
- [ ] Mastery-celebration accent layers correctly without replacing standard layout
- [ ] Integration test passes across ≥2 domains using the same shared code path
- [ ] All four analytics events firing correctly via K-05's interface

#### `Development_Blueprints/A9_Skill_Tree_Mastery_Engine/KMP/03-skill-tree-state-renderer.md`

##### 4. Objective
Extract and centralize the state-to-visual-token mapping (`Locked/Ready/Learning/Practicing/Mastered/Needs Refresh` → design-system visuals) into `:core:mastery-engine`, replacing any per-feature-module duplication of this mapping, and consumed by A.5's `K-01 Quran Skill Tree Map`.

##### 5. Business Requirements
- FR-1: exactly six canonical states, domain-agnostic.
- Android AI Prompt item 6: "Provide a SkillTreeStateRenderer reusable composable... do not redefine the state-to-visual mapping separately inside `:feature:learn`; centralize it here."
- §21.9 (referenced): Locked node shows a specific unlock condition, not a generic lock; Needs Refresh uses a gentle, non-regression framing.

##### 11. KMP Requirements
- **`SkillStateVisualMapper.map(state: SkillState): SkillStateVisualTokens`** — pure function returning the design-system token set (color, icon, progress-ring style, label-key) for each of the six states, sourced entirely from `:core:design-system`, no new visual definitions invented here.
- **`SkillTreeStateRenderer` Composable:** renders a single skill node's visual treatment given its state and optional `unlockCondition` text (for `Locked` nodes) — accepts domain-agnostic input, no domain-specific rendering branches.
- **`Locked` node treatment:** must display the specific unlock-condition text passed in, never a generic "locked" message.
- **`Needs Refresh` node treatment:** gentle, encouraging visual/copy framing — never a regression/failure visual language (e.g., no red "X" or downward arrow).

##### 15. Validation
`SkillState` enum values constrained to the six canonical states; `SkillStateVisualMapper` exhaustively handles all six (compile-time exhaustiveness via Kotlin's `when` on a sealed/enum type, so a future seventh state would fail to compile until handled — intentional safety net).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| `Locked` node with no `unlockCondition` text provided | Falls back to a documented generic-but-still-informative message (e.g., "Complete the previous skill first") rather than crashing or showing blank |
| Unknown/future state value not yet in the six-value set | Compile-time exhaustiveness check prevents this from shipping unhandled; if reached via a malformed API response, renders a safe default/error visual and logs a warning |

##### 19. Offline First
Works identically whether `SkillStateDto` came from a live fetch or K-01's Room cache — this component is agnostic to data freshness (that concern is owned upstream).

##### 21. Localization
State labels (e.g., "Mastered", "Needs Refresh") and unlock-condition text sourced from string resources, EN/HI/AR/UR.

##### 22. RTL
Progress-ring direction, icon placement, and text alignment must all mirror correctly in RTL layouts (Arabic/Urdu) — verified via RTL-mode UI tests.

##### 25. Security
No new attack surface (pure presentation component).

##### 27. Testing
- Unit: `SkillStateVisualMapper` returns the correct token set for all six states (exhaustive test, one per state).
- UI test: `Locked` node renders the specific unlock-condition text passed in, not a generic message, when provided.
- UI test: `Needs Refresh` visual treatment verified as non-punitive (no red/failure iconography) — a design-review-style assertion on the token set used.
- UI test: RTL layout correctness across all six states.
- Performance test/lint: component does not trigger unnecessary recomposition when its state parameter is unchanged (stability annotations verified).

##### 31. Final Verification Checklist
- [ ] All six states covered by the mapper (exhaustive, compile-time enforced)
- [ ] `Locked` renders specific unlock-condition text
- [ ] `Needs Refresh` uses gentle, non-punitive visual language (verified, not assumed)
- [ ] Full EN/HI/AR/UR localization + RTL mirroring verified
- [ ] A.5's skill-tree map migrated with zero visual regression (screenshot/visual test)
- [ ] No duplicated state-to-visual mapping remains anywhere in `:feature:learn`
- [ ] Component is `@Stable`/`@Immutable`-annotated to avoid unnecessary recomposition in large trees

#### `Development_Blueprints/A9_Skill_Tree_Mastery_Engine/KMP/04-mastery-result-offline-handling-sync.md`

##### 4. Objective
Detect offline quiz-attempt completion, show a simple "Saved! We'll show your results when you're back online" interim screen instead of attempting `QuizCompletionResultScreen`, and queue a deferred navigation to the real Result screen once connectivity returns and the attempt has synced.

##### 5. Business Requirements
- A.9 PRD §6.7 Offline Support: "The Result screen itself requires connectivity (mastery computation is server-side)... offline quiz completions defer their Result screen until reconnect, showing a simpler 'saved, will show your results when you're back online' interim state instead."
- Android AI Prompt item 5: exact offline-then-reconnect-then-show-result sequence must be integration-tested.
- Consistency with A.5's AI pronunciation feedback pattern (another server-computed-feedback flow already handling this class of problem).

##### 11. KMP Requirements
- **Connectivity detection at completion time:** when a quiz attempt completes, check current connectivity via the existing observer; if offline, do NOT attempt to call `MasteryRepository.getResult()` or render `QuizCompletionResultScreen` at all.
- **`OfflineResultInterimScreen`:** simple, calm "Saved! We'll show your results when you're back online" message — no error framing (this is an expected, handled state, not a failure).
- **`DeferredResultNavigationQueue`:** persists (at minimum in-memory for the current app session, ideally via a small local store surviving process death) the set of `attempt_id`s awaiting result display; on reconnect + sync-completion signal from A.8's offline-sync mechanism, triggers navigation into `QuizCompletionResultScreen` for the now-synced attempt.
- **Reconnect trigger:** observes the same connectivity signal used elsewhere in the app; on transition offline→online, checks the deferred queue and, once A.8's sync confirms the attempt is processed server-side, navigates automatically (or prompts the child gently, depending on whether the child has since navigated elsewhere in the app — a sensible UX fallback if the child is no longer on a relevant screen when sync completes).

##### 15. Validation
Only attempts genuinely completed offline (not attempts that simply had a slow/failed single request while online) enter this deferred flow — distinguish "offline at completion time" from "online but request failed," which should instead use standard retry/error handling, not this offline-specific path.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Quiz attempt completes offline | `OfflineResultInterimScreen` shown, no error state, attempt queued for deferred result display |
| Reconnect occurs but A.8's sync hasn't yet confirmed the attempt processed server-side | Deferred queue waits for the sync-completion signal, does not prematurely call `getResult()` (which would 404/error against an attempt the server hasn't processed yet) |
| Child navigates away before sync/reconnect completes | Deferred entry persists; on next app open (or next reconnect) with the entry still pending, the app can surface the result then, rather than losing it |
| Sync ultimately fails (e.g., attempt data corrupted) | Falls back to A.8's existing offline-sync failure handling (not re-solved here — this sub-feature only owns the "sync succeeded, now show the result" hop) |

##### 19. Offline First
This entire sub-feature IS the offline-first handling for this specific data type (server-computed result). It correctly acknowledges that unlike `skill_node_state` (offline-viewable via K-01's cache), the Result screen's data cannot be offline-first by nature — this sub-feature manages that limitation gracefully rather than pretending it doesn't exist.

##### 21. Localization
"Saved! We'll show your results when you're back online" and any related copy localized EN/HI/AR/UR.

##### 22. RTL
Interim screen layout mirrors correctly in RTL.

##### 25. Security
No new attack surface; deferred queue only stores non-sensitive attempt IDs.

##### 27. Testing
- Integration test (Android AI Prompt item 5, mandatory): exact offline-then-reconnect-then-show-result sequence — complete an attempt offline, verify `OfflineResultInterimScreen` shown (not an error, not the real Result screen), reconnect, verify A.8's sync completes, verify automatic navigation into `QuizCompletionResultScreen` with correct data.
- Unit: `DeferredResultNavigationQueue` add/observe/clear logic.
- Unit: connectivity-check branching at completion time (offline → interim screen; online → normal Result screen).

##### 31. Final Verification Checklist
- [ ] Offline-at-completion correctly detected and branched (not conflated with "online but failed")
- [ ] `OfflineResultInterimScreen` never uses error/failure framing
- [ ] Deferred queue survives the child navigating away before reconnect
- [ ] Reconnect + A.8 sync-completion correctly triggers automatic navigation to the real Result screen
- [ ] Mandatory offline→reconnect→result integration test passing
- [ ] No duplicate/parallel offline-sync mechanism built (hooks into A.8's existing one)
- [ ] Full EN/HI/AR/UR localization + RTL on the interim screen

#### `Development_Blueprints/A9_Skill_Tree_Mastery_Engine/KMP/05-cross-domain-mastery-analytics-integration.md`

##### 4. Objective
Implement `MasteryAnalytics` in `:core:mastery-engine`, firing every event from A.9 PRD §1.19 with correct parameters and `domain` tagging, consumed by K-02/K-03/K-06 and any domain feature module — replacing any risk of each domain defining a parallel, inconsistent analytics interface.

##### 5. Business Requirements
- A.9 PRD §1.19: full event list — `quiz_result_screen_shown`, `quiz_result_review_mistakes_selected`, `quiz_result_try_again_selected`, `quiz_result_continue_selected`, `mastery_score_recomputed`, `skill_state_transitioned`, `mastery_single_session_block_applied`, `spaced_review_due_cross_domain_capped`, `cross_domain_mastery_summary_viewed`, `mastery_formula_version_applied`.
- §6.6 Analytics Mapping: "`MasteryAnalytics` fires `quiz_result_screen_shown` and the three selection events; domain feature modules (A.5) consume the same shared analytics interface rather than each defining a parallel one."
- §11.1 Event Taxonomy: all events tagged with `domain` where relevant, enabling cross-domain comparison.

##### 11. KMP Requirements
- **`MasteryAnalytics` interface:** one method per event in §1.19's list, strongly typed parameters (e.g., `fun onQuizResultScreenShown(strengthsCount: Int, nextStepSkillId: String)`), always accepting/tagging `domain` where the event is domain-scoped.
- **Default implementation:** delegates to `:core:analytics`'s underlying SDK wrapper, mapping each typed method call to the correct event name/parameter payload.
- **Internal/aggregate events** (`mastery_score_recomputed`, `mastery_single_session_block_applied`, `spaced_review_due_cross_domain_capped`, `mastery_formula_version_applied`): fired without raw score values in their parameters (consistent with the platform-wide no-raw-score principle) — these are transition/occurrence signals, not score-value carriers.
- **Consumption contract:** any domain feature module (current or future) fires mastery-related analytics ONLY through this interface — never directly through the raw `:core:analytics` SDK for these specific event types, to prevent drift/inconsistency.

##### 15. Validation
Parameter types enforced at compile time via the typed interface (e.g., `strengthsCount: Int`, not a loosely-typed `Map<String, Any>`) — reduces the risk of malformed event payloads reaching the analytics pipeline.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Underlying analytics SDK call fails/throws | Caught and logged via `:core:logger`, never propagates to crash the user-facing flow (analytics failures must be non-blocking, per standard platform convention) |
| Event fired with a `domain` value not yet known to analytics tooling (e.g., a brand-new domain) | Fired as-is; analytics dashboards are expected to handle new domain tags gracefully (no client-side allowlist blocking new domains, which would undermine FR-9's extensibility goal) |

##### 19. Offline First
Relies on `:core:analytics`'s existing offline-queueing/batching behavior (events fired while offline are queued and flushed on reconnect) — not reimplemented here.

##### 21. Localization
N/A (event names/parameters are not user-facing text).

##### 22. RTL
N/A.

##### 25. Security
No PII beyond what the existing analytics pipeline already handles for other event types; `skill_id`/`domain` are non-sensitive metadata, never raw score values.

##### 27. Testing
- Unit: each `MasteryAnalytics` method correctly maps to the expected underlying event name and parameter shape (mock the underlying SDK, assert call arguments).
- Unit: analytics failures are caught and don't propagate.

##### 31. Final Verification Checklist
- [ ] All 10 events from §1.19 implemented with correct parameter shapes
- [ ] `domain` tagging present on every domain-scoped event
- [ ] No raw score value in any event parameter
- [ ] Analytics SDK failures caught, non-blocking to user flows
- [ ] K-02, K-03 (if applicable), K-06, and A.5's `:feature:learn` all wired to this shared interface
- [ ] No remaining direct `:core:analytics` calls for these event types outside this interface

#### `Development_Blueprints/A9_Skill_Tree_Mastery_Engine/KMP/06-cross-domain-parent-mastery-summary.md`

##### 4. Objective
Build the Parent Area screen consuming B-08's `GET /v1/children/{id}/mastery-summary`, rendering concept-level summaries (skill labels + state + trend) grouped by domain, with an optional domain filter and drill-through to domain-specific detail (e.g., A.5's existing Quran/Arabic report).

##### 5. Business Requirements
- FR-11: domain-agnostic Parent Report contract — concept-level summaries, never a raw aggregate score as headline.
- User Story: "As a parent, I want every learning domain in the app to report progress in the same consistent, trustworthy way."
- Screen Inventory #8: Parent Cross-Domain Mastery Summary — entry point Parent Dashboard → Child Progress → Learning (aggregated across domains); exit point domain-specific detail (e.g., A.5's Quran/Arabic report).

##### 11. KMP Requirements
- **`CrossDomainMasterySummaryViewModel`:** fetches `MasteryRepository.getMasterySummary(childId, domain = null)` on entry for the full rollup; supports re-fetching with a specific `domain` filter when the parent taps a domain-filter chip.
- **Screen layout:** grouped-by-domain sections, each showing concept-level skill cards (label + state + trend) — never a numeric aggregate score as the page's headline element.
- **Drill-through:** tapping a domain section (or a "view full report" affordance) navigates to that domain's existing detailed report screen (e.g., A.5's `K-12`) — this screen is a rollup/entry-point, not a replacement for domain-specific depth.
- **Empty state:** child with zero evidence in any domain shows an appropriate "just getting started" empty state, not an error or blank screen.

##### 15. Validation
`childId` must be a valid child in the parent's family (enforced server-side by B-08; client just surfaces the resulting `403` gracefully if somehow reached with an invalid child).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Fetch fails (network/server error) | Error state with retry affordance |
| Child has zero evidence in any domain | "Just getting started" empty state, not an error |
| Domain filter selected with zero data for that domain | Empty state scoped to that domain, with an easy way back to "all domains" |

##### 19. Offline First
Not required to be fully offline-capable (parent-initiated report view, expected to be used online); may show a last-cached summary with a "may be outdated" indicator if implemented, but this is an enhancement, not a hard requirement for this sub-feature.

##### 21. Localization
All labels, state names, trend descriptors, and empty-state copy localized EN/HI/AR/UR.

##### 22. RTL
Full RTL layout support for the grouped-section/card layout.

##### 25. Security
No raw score exposure (consistent with B-08's structural guarantee); parent-session-scoped auth prevents cross-family access.

##### 27. Testing
- Unit: ViewModel fetch/filter logic, empty-state branching.
- UI test: grouped-by-domain rendering, domain-filter interaction, drill-through navigation trigger.
- UI test: no numeric score displayed anywhere in the screen's semantics tree.

##### 31. Final Verification Checklist
- [ ] Screen reachable via `Parent Dashboard → Child Progress → Learning`
- [ ] Grouped-by-domain rendering correct for a multi-domain child
- [ ] Domain filter interaction working
- [ ] Drill-through to domain-specific report (e.g., A.5's `K-12`) working
- [ ] Empty state for zero-evidence child correct, not an error
- [ ] No numeric score displayed anywhere (semantics-tree scan)
- [ ] Full EN/HI/AR/UR localization + RTL verified
- [ ] `cross_domain_mastery_summary_viewed` analytics event firing correctly

## A10 — Feature_A10_Games_Module

PRD: `PRD_Documents/Child App (1-12)/Feature_A10_Games_Module.md`

Coverage: 12 mandatory FR records; all preserved verbatim below. Feature has 12 inventory records including components/states. Components and states must not inflate independently executed screen count.

### Existing screenshot candidates

- `Screens/Mobile App/Games/Game Complete-01.png` — inventoried only
- `Screens/Mobile App/Games/Game Complete-02.png` — inventoried only
- `Screens/Mobile App/Games/Game Complete-03.png` — inventoried only
- `Screens/Mobile App/Games/Games Hub-01.png` — visually inspected
- `Screens/Mobile App/Games/Games Hub-02.png` — inventoried only
- `Screens/Mobile App/Games/Games Hub-03.png` — inventoried only
- `Screens/Mobile App/Games/Games Hub-04.png` — inventoried only
- `Screens/Mobile App/Games/Games Hub-05.png` — inventoried only

### Complete normative functional coverage

### 1.7 Functional Requirements

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

### Ordered source inventory

### 1.18 Screen Inventory (Complete — Zero Missing)

> Individual game mechanics already detailed in A.5 (Quran Game variants, Arabic Letters variants) are not re-inventoried here; this lists the Games Hub's own screens plus the generic session-lifecycle screens that wrap any game.

| # | Screen / Component | Type | Entry Points | Exit Points |
|---|---|---|---|---|
| 1 | Games Hub (tile grid landing) | Primary | Home "Trending Games" rail, Rewards screen, dedicated nav entry (if present) | Individual game session |
| 2 | Skill-Area Filter/Group Selector | Component | Games Hub | Filtered tile grid |
| 3 | Game Tile (component, age-band-filtered) | Component | Games Hub | Game Session Launch |
| 4 | Daily Quiz Entry Tile (routes into shared A.8 engine) | Component | Games Hub | A.8 Quiz Session |
| 5 | Game Session — Generic Loading State | Screen variant | Any game tile tap | Game-specific play screen |
| 6 | Game-Specific Play Screen (per game, mechanics detailed in A.5 for Quran/Arabic games; new mini-games follow the same wrapper) | Screen | Game Session Loading | Session Completion |
| 7 | In-Session Difficulty-Adaptive Feedback (component, generic) | Component | Within any game session | N/A |
| 8 | Session Abandonment (implicit, no dedicated screen — simply exits without reward per Edge Case 3) | N/A (absence of state) | N/A | Returns to launching screen |
| 9 | Session Completion Screen (generic wrapper, reuses A.9's "strengths + next step" framing where applicable) | Screen | End of any game session | Replay / Return to launching screen |
| 10 | Offline/Download-Required Notice | Component | Game tile tap, offline + not downloaded | Dismiss, suggests downloaded alternative |
| 11 | Empty State — No Games for Skill Area/Age Band | Screen variant | Filtered Games Hub view | Alternate skill area |
| 12 | Admin Game-Skill-Mapping Validation Error (Admin-side, surfaced at publish time) | Admin screen variant | Admin Game Catalog Editor | Blocks publish until resolved |

### Exact mobile UX and behavior sources

### 1.9 Acceptance Criteria

- Given the Games Hub is opened, when the tile grid renders, then every visible tile is age-band-appropriate for the active child and groupable by skill area.
- Given an admin attempts to publish a game catalog entry with zero linked `skill_node_id` values, when they submit, then publication is blocked with a clear validation error.
- Given a child completes a game session with low accuracy, when the session ends, then they still receive the standard participation XP/Noor Heroes Points reward — accuracy affects only the mastery-evidence signal sent to A.9.
- Given a child finishes a game launched from Home, when the session ends, then they are returned to Home (not the Games Hub or any other unrelated screen) — the same game launched from the Games Hub returns to the Games Hub.
- Given a child replays a previously-completed game, when they start a new session, then it functions identically to the first play (no lock, no degraded experience).
- Given a game involves Quran/Tajweed/Dua content, when it is submitted for publish, then it is routed through the same scholar-review pipeline as any other content of that type — there is no "games" content-governance shortcut.
- Given a game session reaches its natural end condition, when the round/session concludes, then the game does not automatically begin a new round without an explicit child action.

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

### 1.16 User Flow (Narrative)

Child opens the Games Hub (from Home's "Trending Games" rail, the Rewards screen, or a dedicated nav entry) → browses tiles grouped by skill area, automatically age-band-filtered → selects a game → a session launches at the appropriate difficulty tier → plays through to a natural completion point → skill evidence and participation reward are recorded → child is returned to whichever screen launched the session → may immediately replay or browse another tile.

### 2.1 Games-Specific Design System Extensions

- **Tile Grid Visual Language:** Consistent rounded tile cards (matching A.3's category-rail card treatment) with a small skill-area icon badge (reusing the same iconography family as A.5's domain tagging) and an age-band-tier indicator that is informational only (e.g., a subtle "for ages 6-9" micro-label), never a separate selectable control on the child's own view (tiering is automatic per FR-8).
- **Difficulty-Adaptive Feedback:** In-session difficulty shifts are never visually jarring or called out explicitly to the child (e.g., no "Level Up!" interruption mid-game) — the experience should feel smoothly responsive, not gamified in a way that creates pressure.
- **Session Completion Wrapper:** Reuses A.9's "Strengths + one next step" framing where the underlying game maps cleanly to that pattern (e.g., a quiz-like game), or a simpler "Nice work! 🌟 [XP earned]" celebratory wrapper for more free-form mini-games where a strengths/next-step breakdown wouldn't make sense — the choice of wrapper style is a per-game content-configuration decision, not a hardcoded split.

### 2.2 Screen-Level Design Requirements (Key Screens)

#### Screen: Games Hub

- **Purpose:** Discoverable, organized entry point into all available skill-reinforcement games.
- **Components:** Skill-area filter chips/tabs (Quran, Arabic, Tajweed, etc., per the extensible domain registry), a "Daily Quiz" tile always pinned near the top (high-frequency entry point), a tile grid below grouped by skill area, each tile showing a small illustrative thumbnail, title, and skill-area icon badge.
- **States:** Default, Filtered-by-skill-area, Loading (skeleton grid), Empty-for-filter (Edge Case/empty state), Offline (downloaded tiles only actionable).
- **Accessibility:** Tile grid navigable in a logical reading order via screen reader; filter chips clearly labeled with their current selected/unselected state.
- **Responsive Rules:** 2-column grid on mobile, 3-4 columns on tablet.

#### Screen: Session Completion Screen (generic wrapper)

- **Purpose:** Close out any game session positively and route back correctly.
- **Components:** Celebratory but calm visual treatment (consistent with A.8/A.9's accuracy-independent tone), XP/Noor Heroes Points reveal, optional strengths/next-step block (per-game-configurable), "Play Again" and "Done" (returns to launching screen) actions.
- **States:** Standard-completion, Mastery-threshold-crossed-this-session (layered celebratory accent, consistent with A.9's pattern).

### 2.3 Tab Structure

Games Hub is reachable from Home and Rewards (per the source navigation table), not necessarily its own bottom-nav tab. Click mapping:

| Click Target | Destination | API Called | Analytics Event | Permission Check | Error Handling |
|---|---|---|---|---|---|
| Home "Trending Games" rail item | Game Session (direct launch) | `GET /v1/games/{game_id}/manifest` | `game_session_started` | Age-band/entitlement check | Falls back to Games Hub if unavailable |
| Rewards screen "Games" entry | Games Hub | `GET /v1/games?age_band=` | `games_hub_viewed` | None | Cached fallback |
| Games Hub tile | Game Session | `GET /v1/games/{game_id}/manifest` | `game_tile_tapped` → `game_session_started` | Age-band-appropriate (filtered at list time, re-validated at launch) | Graceful unavailable message |
| Skill-area filter chip | Filtered tile grid | `GET /v1/games?skill_area=` | `games_skill_area_filtered` | None | Cached fallback |

### 2.4 Wireframe Description (Composite)

Games Hub: a filter-chip row at top, then a responsive tile grid below — visually similar in density to A.3's Stories Library but with a flatter, less hierarchical structure (no "categories as full-width rails," just a straightforward grouped grid, reflecting Games' lighter, more snackable nature compared to Stories' longer-form content). Session Completion: single-column, consistent with the platform's general result-screen pattern (A.8/A.9).

### 2.5 Screen Image Generation Prompts

**Screen: Games Hub**
- *Prompt 1 (English):* "Mobile app games hub screen UI mockup for a children's Islamic learning app. Warm off-white background. A row of rounded filter chips at top labeled with skill areas and small icons (a book for Quran, Arabic letter shape for Arabic, a musical-note-like symbol for Tajweed). Below, a responsive grid of rounded square game tiles, each showing a simple colorful playful illustration (geometric shapes, friendly abstract icons, no realistic human faces), a short title, and a small subtle age-range micro-label in the corner. One tile near the top visually distinct and slightly larger, labeled 'Daily Quiz' with a small lightning-bolt-like icon. Bright, playful, organized aesthetic, rounded corners, soft shadows, warm teal and gold accents, bottom navigation bar visible."
- *Prompt 2 (Arabic RTL):* "نفس شاشة مركز الألعاب لتطبيق تعليم إسلامي للأطفال، بتخطيط من اليمين إلى اليسار بالكامل. خلفية بيج فاتح دافئ. صف من رقاقات تصفية مستديرة في الأعلى موسومة بمجالات المهارات وأيقونات صغيرة (كتاب للقرآن، شكل حرف عربي للعربية، رمز يشبه نوتة موسيقية للتجويد). أسفل ذلك شبكة متجاوبة من بطاقات ألعاب مربعة مستديرة الزوايا، كل منها تعرض رسمة بسيطة وملونة ومرحة (أشكال هندسية، أيقونات تجريدية ودودة، بدون وجوه بشرية واقعية)، وعنوانًا قصيرًا، وتسمية صغيرة وخفية للفئة العمرية في الزاوية. بطاقة واحدة قرب الأعلى مميزة بصريًا وأكبر قليلاً بعنوان 'اختبار اليوم' مع أيقونة صغيرة تشبه البرق. طابع مشرق ومرح ومنظم، زوايا دائرية، ظلال خفيفة، لمسات فيروزية وذهبية دافئة، شريط تنقل سفلي ظاهر."

*(Session Completion Screen follows the same two-prompt EN/AR template, visually consistent with A.8/A.9's result-screen prompts already provided; available on request.)*

---

### 6.1 Technical Requirements
Kotlin, Jetpack Compose, MVVM, Clean Architecture, module `:feature:games`, depends on `:core:mastery-engine` (A.9), `:core:quiz-engine` (A.8, for the Daily Quiz entry tile), `:core:design-system`, `:core:network`, `:core:offline-cache`.

### 6.2 Screen Mapping
`GamesHubScreen` Composable with a filter-chip row and a `LazyVerticalGrid` of `GameTile` composables; individual game play screens are implemented per-game (reusing A.5's existing Quran Game/Arabic Letters composables where applicable) behind a common `GameSessionWrapper` that handles the generic completion/evidence/reward submission flow.

### 6.3 Navigation Flow
`GameSessionWrapper` accepts a `returnDestination` parameter captured at launch time (Home, Rewards, or Games Hub) and navigates back there explicitly on completion — implemented via a typed navigation argument, not relying on a generic back-stack pop (which could be fragile if intermediate screens were pushed during the session).

### 6.4 State Management
`GamesHubViewModel` applies age-band filtering purely by trusting the server's already-filtered response (no client-side re-filtering logic that could drift from the server's authoritative age-band derivation). `GameSessionWrapper`'s ViewModel delegates evidence/reward submission to the shared `MasteryRepository`/`RewardRepository` interfaces from A.9/A.11 rather than implementing its own submission logic.

### 6.5 API Mapping
`GamesRepository.getCatalog()` → `GET /v1/games`; `GamesRepository.getManifest()` → `GET /v1/games/{id}/manifest`; session completion delegates through the shared Mastery/Reward repositories.

### 6.6 Analytics Mapping
`GamesAnalytics` fires `games_hub_viewed`/`game_tile_tapped`/`game_session_started`/`game_session_completed`/`game_session_abandoned`; abandonment is detected via a ViewModel lifecycle check (session not completed before the screen is destroyed) rather than requiring an explicit "I'm abandoning" signal from the child.

### 6.7 Offline Support
Downloadable game content follows A.5's existing offline-manifest pattern; session completion while offline queues evidence/reward submission via the shared outbox pattern already established in A.8/A.9, requiring no new offline infrastructure.

### 6.8 Deep Linking
`noorheroes://games`, `noorheroes://games/{game_id}`.

### 6.9 Push Notifications
Not a notification source itself; Home's "Trending Games" recommendations may surface via existing notification channels owned by A.12.

### 6.10 Testing Strategy
- Unit: `GameSessionWrapper`'s return-destination routing logic (Home vs. Rewards vs. Games Hub, captured correctly at launch and honored at completion).
- UI tests: Games Hub tile grid never renders a tile the server didn't include (no client-side age-band override logic exists to test against, by design — this is itself a test of *absence* of such logic); abandonment correctly results in zero evidence/reward submission calls (mocked repository verification).
- Integration: full game-session-complete → shared Mastery/Reward delegation flow, verified to call the exact same repository methods A.8's quiz completion uses (a structural reuse-verification test, mirroring the backend's item-4 test).

---

### 13.1 Test Plan Summary
Coverage spans: the skill-mapping hard gate (signature governance test), server-side age-band enforcement, shared-infrastructure-reuse verification, session abandonment handling, and all 12 edge cases from §1.10.

### 13.2 Test Cases — Happy Path
1. Child opens Games Hub from Home, filters by "Quran," plays a game to completion, receives participation reward, and is returned to Home (not the Games Hub).
2. Child replays a previously-completed game multiple times across different days, eventually contributing to a `Mastered` transition on the linked skill via A.9's standard multi-session evidence rule.
3. Admin attempts to publish a new game without linking any skill node and is blocked; after linking a skill node, publish succeeds.

### 13.3 Edge Cases
All 12 items from §1.10.

### 13.4 Negative Cases
- Attempt to publish/update a game to have zero `skill_node_ids` via direct admin API call → `422`, regardless of role.
- Request the games catalog with a client-supplied `age_band` query parameter different from the authenticated child's actual age band → results reflect the server-derived age band, not the client's claim.
- Abandon a game session mid-round → confirm zero evidence/reward repository calls were made.
- Deprecate a skill node that is the sole link for a published game → confirm the reconciliation job sets that game to `is_withdrawn=true`.

### 13.5 Regression Cases
Full Games Module suite re-run on every release touching `:feature:games`, the Games Catalog Service, or any of the shared services it wraps (A.5/A.8/A.9/A.11).

### 13.6 Automation Cases
End-to-end: full Games Hub browse → play → complete → reward/evidence flow; skill-mapping-gate automated test (CI-blocking); auto-withdrawal cascade automated test; reuse-verification automated test confirming no scoring/reward logic drift over time (run as a standing regression check, not just at initial launch, given the architectural-drift risk it specifically guards against).

---

### Corresponding KMP blueprint requirements

#### `Development_Blueprints/A10_Games_Module/KMP/01-games-hub-screen-skill-area-filtering.md`

##### 4. Objective
Render a filter-chip row plus a `LazyVerticalGrid` of `GameTile` composables sourced entirely from `GET /v1/games` (B-01), with zero client-side age-band filtering logic — a structural absence of such logic is itself the correctness requirement (PRD §7 item 1).

##### 5. Business Requirements
- FR-1: Hub sections include pinned Daily Quiz tile, Arabic Letters games, skill-area-grouped mini-games.
- FR-8: filtering is automatic and server-derived; no manual age-band override exposed to the child.
- NFR: Games Hub tile grid load p95 < 600ms (cached) (§1.8).
- §1.12 Empty States: zero-games-for-filter shows a friendly "more games coming soon" message.
- §1.13 Loading States: skeleton tile-grid shimmer.
- §1.14 Offline States: cached tiles rendered with "may be outdated" indicator; non-downloaded tiles show connect/download affordance.

##### 11. KMP Requirements
- `GamesHubScreen` Composable: filter-chip row (`SkillAreaFilterChipRow`) + `LazyVerticalGrid` of `GameTile`, 2-column mobile / 3–4-column tablet (PRD §2.2 Responsive Rules).
- `GameTile` shows thumbnail, title, skill-area icon badge, informational-only age-band micro-label (never a selectable control, PRD §2.1).
- Daily Quiz tile pinned near top, visually distinct; tapping it deep-links into `:core:quiz-engine` (A.8) — not reimplemented here.
- `GamesHubViewModel` calls `GamesRepository.observeCatalog(skillArea, domain)` and renders whatever the server returns with **zero additional filtering logic** — this absence is itself tested (Task/Test in §27).
- States: Default, Filtered-by-skill-area, Loading (skeleton shimmer), Empty-for-filter, Offline (downloaded-only actionable).

##### 15. Validation
No client-side validation of server response beyond basic null/shape safety (deserialization failure maps to `AppError.Validation` or `AppError.Server.Error`, never a crash).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Catalog fetch failure (network) | Render cached last-known catalog (via K-05's local cache) with a subtle "may be outdated" indicator — never a hard error blocking the screen |
| Game asset/thumbnail fails to load | Graceful retry with backoff; fallback placeholder image, never a crash |
| Empty result for skill-area filter | Friendly empty state with link to a populated skill area |
| Deserialization/shape mismatch | Logged via `NoorHeroesLogger`, mapped to `AppError`, generic non-blocking error state shown |

##### 19. Offline First
```
Remote Data (GET /v1/games)
   ↓
GamesRepositoryImpl
   ↓
Local Cache (Room/SQLDelight, owned by K-05)
   ↓
GamesHubViewModel (observes Flow)
   ↓
GamesHubScreen (UI)
```
This blueprint defines the `Flow`-based observation contract; K-05 completes the local-cache-backed implementation.

##### 21. Localization
All UI text (`title`, filter-chip labels, empty-state copy) localized for English, Hindi, Arabic, Urdu via `core-common/localization`'s reactive localization provider — no hardcoded strings.

##### 22. RTL
Filter-chip row and tile grid must mirror correctly for Arabic/Urdu (RTL) — grid reading order right-to-left, chip row reversed, consistent with `CORE_DESIGNSYSTEM_INSTRUCTIONS.md` RTL conventions.

##### 25. Security
No sensitive data displayed; relies entirely on the server-side age-band enforcement from B-01 — this module has no independent security boundary to maintain beyond correctly trusting (not re-deriving) the server response.

##### 27. Testing
- **Structural absence test (primary):** `GamesHubStructuralAbsenceTest` — static/reflective or code-review-assisted test asserting `GamesHubViewModel` contains no age-band comparison/filtering code path at all.
- Unit: `GamesHubViewModel` correctly maps `NoorResult.Success`/`Failure` to UI state.
- Unit: empty-filter-result maps to the empty state, not an error state.
- UI test: Games Hub tile grid never renders a tile the server didn't include in its response (verified via a mocked repository returning a known fixed set).
- UI test: filter-chip selection triggers the correct repository call parameters.
- Accessibility test: tile grid navigable in logical reading order via screen reader; filter chips correctly announce selected/unselected state.

##### 31. Final Verification Checklist
- [ ] Structural absence test passing (no age-band filtering logic in ViewModel)
- [ ] Tile grid never renders a server-omitted tile (mocked-repository UI test)
- [ ] All five UI states implemented and tested
- [ ] Daily Quiz tile delegates to `:core:quiz-engine`, not reimplemented
- [ ] Localization complete for EN/HI/AR/UR
- [ ] RTL layout verified for Arabic/Urdu
- [ ] Analytics events verified via mocked client
- [ ] Accessibility (screen reader order, chip state announcement) verified
- [ ] No files outside declared scope modified

---

#### `Development_Blueprints/A10_Games_Module/KMP/02-game-session-wrapper-return-destination-navigation.md`

##### 4. Objective
Build `GameSessionWrapper(gameId, returnDestination: ReturnDestination)` where `ReturnDestination` is a sealed class (`Home`, `Rewards`, `GamesHub`) captured at launch time and honored explicitly on completion via `Navigator.navigateTo()`, not a generic back-stack pop — correct even if intermediate screens were pushed during the session (PRD FR-7, §6.3, §7 item 2).

##### 5. Business Requirements
- FR-7: on completion, return to the exact screen that launched the session — never an unrelated destination.
- FR-9: replaying a completed game is always available (no re-locking).
- FR-12: session has a clear natural end state; no auto-continuing without explicit child action.
- §2.1 Difficulty-Adaptive Feedback: in-session difficulty shifts must never be visually jarring (no "Level Up!" interruption).
- §2.2 Session Completion Screen: celebratory-but-calm treatment, XP reveal, optional strengths/next-step block, "Play Again"/"Done" actions.

##### 11. KMP Requirements
- `GameSessionRoute(gameId: String, returnDestination: ReturnDestination)` — `@Serializable`, minimal payload per §6 note.
- `ReturnDestination` sealed class: `Home`, `Rewards`, `GamesHub` — captured at the moment of launch from whichever screen initiated the session (Home's Trending Games rail → `Home`; Rewards screen entry → `Rewards`; Games Hub tile → `GamesHub`).
- `GameSessionWrapper` composable: generic loading state (lightweight, per-game-asset-appropriate) → delegates to the game-specific play screen (reused from A.5) → generic `SessionCompletionScreen` → explicit `navigator.navigateTo(returnDestination.toRoute(), popUpTo = GameSessionRoute::class, inclusive = true)` on "Done."
- "Play Again" restarts a fresh session at the same `gameId`/`returnDestination` without leaving the wrapper (no lock, no degraded repeat experience per FR-9).
- Difficulty-adaptive feedback rendered smoothly, no jarring interruption (§2.1) — implemented as a subtle, non-modal visual cue only.

##### 15. Validation
`gameId` presence validated before manifest fetch; malformed/missing `gameId` routes back to Games Hub defensively rather than crashing.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Manifest fetch returns `403 AGE_BAND_MISMATCH` | Return to Games Hub with a brief "this game isn't available right now" message, no crash |
| Manifest fetch returns `410 GAME_WITHDRAWN` | Same graceful fallback |
| A.5 game-play composable throws/errors internally | Wrapper catches at its boundary, logs via `NoorHeroesLogger`, routes to a generic error state with "Try Again"/"Back" options |
| Session completion API call fails (network) | Handled by K-03, not this blueprint — completion screen still shown per FR-7 intent |

##### 19. Offline First
`GameSessionWrapper` requests the manifest via `GamesRepository.getManifest()`, which (per K-05) resolves from local cache when offline for downloaded games; non-downloaded games show the offline/download-required notice (PRD §1.14) rather than attempting the wrapper flow.

##### 21. Localization
All Session Completion Screen text ("Nice work! 🌟", strengths/next-step framing, button labels) localized EN/HI/AR/UR.

##### 22. RTL
Completion screen layout mirrors correctly for Arabic/Urdu; "Play Again"/"Done" button order follows RTL convention (not simply mirrored left-right blindly — follow platform RTL button-ordering guidance from `CORE_DESIGNSYSTEM_INSTRUCTIONS.md`).

##### 25. Security
No new sensitive data surface; relies on B-02's server-side re-validation as the actual security boundary.

##### 27. Testing
- **Primary navigation test:** all three `ReturnDestination` values (`Home`, `Rewards`, `GamesHub`) verified to route correctly on completion, including when intermediate screens were pushed during the session (simulated back-stack manipulation in test).
- Unit: "Play Again" correctly restarts without navigating away from the wrapper.
- Unit: `403`/`410` manifest errors correctly route to graceful fallback, not a crash.
- Integration: full manifest-fetch → play-screen-delegation → completion → return-navigation round trip (play-screen mocked/stubbed since it's owned by A.5).
- Structural test: confirm `GameSessionWrapper` invokes A.5's existing composables rather than containing duplicated game-mechanic rendering code.

##### 31. Final Verification Checklist
- [ ] Explicit navigation (not back-stack pop) verified for Home/Rewards/GamesHub
- [ ] Navigation correctness holds even with intermediate screens pushed during session
- [ ] "Play Again" does not trigger unintended navigation
- [ ] `403 AGE_BAND_MISMATCH`/`410 GAME_WITHDRAWN` both gracefully handled, no crash
- [ ] A.5 game-play composables reused via public interface, not duplicated
- [ ] Completion screen localized EN/HI/AR/UR with correct RTL button ordering
- [ ] Difficulty-adaptive feedback confirmed non-jarring (no modal interruption)
- [ ] No files outside declared scope modified

---

#### `Development_Blueprints/A10_Games_Module/KMP/03-game-evidence-reward-delegation.md`

##### 4. Objective
On natural session completion, `GameSessionViewModel` calls the existing `MasteryRepository.submitEvidence()` (`:core:mastery-engine`, A.9) and `RewardRepository` (A.11) with correctly-shaped parameters, verified via structural reuse tests confirming no new, parallel submission logic exists anywhere in `:feature:games` (PRD §7 item 3).

##### 5. Business Requirements
- FR-5: every completed session emits skill evidence via the shared A.9 contract — first-class, not a lesser signal.
- FR-6: participation reward accuracy-independent.
- §6.4 State Management: `GameSessionWrapper`'s ViewModel delegates to shared repository interfaces rather than implementing its own submission logic.
- §6.7 Offline Support: completion while offline queues evidence/reward submission via the shared outbox pattern already established in A.8/A.9.

##### 11. KMP Requirements
- `GameSessionCompletionHandler.onSessionComplete(gameId, sessionId, responses)`:
  1. Generates `client_request_id` (idempotency key) via existing ID utility.
  2. Calls `GamesRepository.completeSession(gameId, sessionId, responses, clientRequestId)` → internally calls B-03.
  3. On success, surfaces the reward result to `SessionCompletionScreen` for display.
  4. Does **not** independently call `MasteryRepository`/`RewardRepository` from this module — B-03's backend orchestration is the single source of truth for evidence/reward side effects (avoids client-side double-submission risk); this module's role is purely to invoke the completion endpoint and surface its result.

**Confirmed resolution to the PRD §6.4/§7 item 3 framing (previously flagged for architecture-owner confirmation):** `Feature_A9_Skill_Tree_Mastery_Engine.md` §3.4 states `POST /v1/mastery/evidence` is explicitly "internal, called by the Quiz Service on attempt completion" — i.e., backend-to-backend only. A.9's own KMP requirements (§6.4–§6.5) confirm `:core:mastery-engine`'s public client surface exposes only *read* methods (`MasteryRepository.getResult()`, `.getSkillStates()`); no client-callable `submitEvidence()` method is specified anywhere in A.9's Android contract. This is now a confirmed fact, not an assumption: there is no legitimate client-side entry point for evidence submission to call in the first place. The single-call design via `GamesRepository.completeSession()` → B-03 (which internally calls `POST /v1/mastery/evidence` server-side) is therefore the only correct integration point, matching A.8's identical pattern (its KMP layer likewise never calls a client-side mastery-submission method). No further architecture-owner sign-off is required on this point.

##### 15. Validation
`client_request_id` generated once per session-completion attempt and reused on retry (never regenerated) to preserve idempotency across retries/offline-queue replay.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Completion API call fails (network) | Session Completion screen still shown to the child (non-blocking per PRD §1.11); call queued for retry via the shared outbox pattern (K-05) |
| Completion API returns `409` (already completed) | Treated as success client-side (idempotent-equivalent outcome), no error shown to child |
| Completion API returns `403`/`404` (session ownership/not-found) | Logged as an anomaly (should not occur in normal flow), generic fallback shown |

##### 19. Offline First
```
GameSessionCompletionHandler
   ↓ (on natural completion)
GamesRepository.completeSession()
   ↓
SyncQueue.enqueue() [if offline] — reused via core-data's existing outbox pattern (K-05 owns full offline integration)
   ↓ (on reconnect)
Idempotent replay via client_request_id
```

##### 21. Localization
Reward-amount display text localized (number formatting per locale via `core-common/format`).

##### 22. RTL
Reward display mirrors correctly for RTL locales.

##### 25. Security
No client-side reward or evidence calculation exists to secure — by design, all calculation happens server-side (B-03), eliminating an entire class of client-tampering risk.

##### 27. Testing
- **Structural reuse-verification test (primary):** confirm `GameSessionCompletionHandler` and `GameSessionViewModel` contain no direct calls to `MasteryRepository`/`RewardRepository` — only to `GamesRepository.completeSession()` — using Mockito/MockK verification asserting zero interactions with those repositories.
- Unit: `client_request_id` generated once and reused across retries (not regenerated).
- Unit: `409` response treated as success client-side.
- Integration: offline completion queues via `SyncQueue`, replays idempotently on reconnect (coordinated with K-05).
- Integration: reward display correctly reflects the amount returned by B-03 regardless of session accuracy (low-accuracy fixture test).

##### 31. Final Verification Checklist
- [ ] Structural reuse-verification test passing (zero direct Mastery/Reward repository calls from this module)
- [ ] Idempotency key generated once, reused on retry (not regenerated)
- [ ] `409` (already-completed) handled as success client-side
- [ ] Offline completion queues correctly and replays idempotently on reconnect
- [ ] Reward display confirmed accuracy-independent (low-accuracy fixture test)
- [ ] §11 PRD-vs-backend-contract discrepancy explicitly confirmed with architecture owner
- [ ] Analytics events fire only after confirmed success, not on request-send
- [ ] No files outside declared scope modified

---

#### `Development_Blueprints/A10_Games_Module/KMP/04-session-abandonment-detection.md`

##### 4. Objective
Detect `GameSessionWrapper` reaching `ON_DESTROY` (or the Composable leaving composition) before a completion event has been recorded, fire `game_session_abandoned`, and explicitly avoid calling `GameSessionCompletionHandler`/`completeSession()` — verified via a lifecycle-simulation test asserting zero calls to the completion/evidence/reward path (PRD §7 item 4).

##### 5. Business Requirements
- Edge Case 3: a child abandoning a session mid-round records no reward or evidence — distinct from A.8's quiz-resume pattern, a deliberate design simplification for Games (documented as such, not an oversight).
- §6.6 Analytics Mapping: abandonment detected via ViewModel lifecycle check, not requiring an explicit "I'm abandoning" signal from the child.
- FR-9: the child can simply start a new session at any time after abandonment — no special resume state to manage.

##### 11. KMP Requirements
- `GameSessionViewModel` holds a `private var isCompleted: Boolean = false`, set `true` only inside the natural-completion path (K-03's success callback).
- `SessionAbandonmentTracker` observes the wrapper's lifecycle (`DisposableEffect { onDispose { ... } }` in Compose, or equivalent `ON_DESTROY` hook) and, if `isCompleted == false` at disposal, fires `game_session_abandoned` and explicitly skips any completion/evidence/reward call.
- No dedicated "abandonment" screen exists (PRD Screen Inventory item 8 — "implicit, no dedicated screen") — the child simply exits and can start a fresh session anytime (FR-9).
- Immediate replay ("Try Again") is explicitly **not** abandonment — verified as distinct from the abandonment path (it is a `GameSessionCompletionHandler`-adjacent "restart," not a lifecycle-destroy event).

##### 15. Validation
N/A (no user input to validate in an abandonment path).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| App killed abruptly (process death) mid-round | No completion call was ever made; server-side session simply remains `completed_at IS NULL` indefinitely — acceptable per Edge Case 3's design (no cleanup job required for this table beyond standard retention, §4.5 of B-03) |
| Child navigates back mid-round via system back gesture | `ON_DESTROY`/`onDispose` fires, `game_session_abandoned` recorded, no completion call |
| Child briefly backgrounds the app then returns (not a true abandonment) | Must NOT be misdetected as abandonment — verified via a dedicated test distinguishing `ON_STOP`/backgrounding from `ON_DESTROY`/actual disposal (Android's process lifecycle nuance is explicitly tested, not assumed) |

##### 19. Offline First
N/A — no network call is made on abandonment, so offline state is irrelevant to this specific path.

##### 21. Localization
N/A — no user-facing text in the abandonment path (it's a silent, implicit state per Screen Inventory item 8).

##### 22. RTL
N/A.

##### 25. Security
No security surface — this is a purely defensive correctness control ensuring no unearned reward/evidence path exists.

##### 27. Testing
- **Primary lifecycle test:** simulate `GameSessionWrapper` reaching disposal (`ON_DESTROY`/`onDispose`) before `isCompleted` is set, assert `GameSessionCompletionHandler.onSessionComplete()` (and therefore `MasteryRepository`/`RewardRepository`, transitively) receives **zero** calls (Mockito/MockK verification).
- Unit: `game_session_abandoned` analytics event fires exactly once on this path.
- Unit: natural completion path (`isCompleted = true` before disposal) does NOT fire `game_session_abandoned`.
- Unit: backgrounding (`ON_STOP`) alone, without full disposal, does NOT trigger abandonment detection (distinguishes true abandonment from a brief app-switch).
- Integration: "Try Again"/immediate replay does not trigger the abandonment path.

##### 31. Final Verification Checklist
- [ ] Primary lifecycle test passing: zero completion-handler calls on abandonment
- [ ] `game_session_abandoned` fires exactly once, no duplicates
- [ ] `ON_STOP`/backgrounding correctly distinguished from true disposal/abandonment
- [ ] "Try Again"/immediate replay confirmed not to trigger abandonment path
- [ ] Behavior verified on both Android and iOS lifecycle models
- [ ] No completion, evidence, or reward network call ever fires on this path
- [ ] No files outside declared scope modified

---

#### `Development_Blueprints/A10_Games_Module/KMP/05-offline-game-content-catalog-caching.md`

##### 4. Objective
Complete `GamesRepositoryImpl`'s offline-first data flow (remote → repository → local storage → UI), enabling full offline gameplay for downloaded games and reliable, idempotent sync of queued evidence/reward submissions on reconnect (PRD §6.7: "requiring no new offline infrastructure" — reuse the existing outbox pattern rather than building a parallel one).

##### 5. Business Requirements
- Edge Case 8: downloaded/cached games fully playable offline; evidence/reward events queue for sync on reconnect, idempotently.
- §1.14 Offline States: downloaded games playable offline; non-downloaded games show a clear "connect to internet or download" affordance, not a dead tile.
- §1.11 Error Handling: Games Hub catalog fetch failure renders cached last-known catalog with a subtle "may be outdated" indicator.
- §6.7: downloadable content follows A.5's existing offline-manifest pattern; session completion while offline queues via the shared outbox pattern already established in A.8/A.9.

##### 11. KMP Requirements
- `GamesRepositoryImpl.observeCatalog()`: emits from local `GameCatalogDao` `Flow` immediately (cache-first), then triggers a background `refresh()` that fetches `GET /v1/games` and updates the local DB, which the `Flow` automatically re-emits (per §8 "Offline-First Screen" scenario pattern).
- `refresh()` failure (no connectivity) leaves the last-cached data in place; UI (K-01) surfaces the "may be outdated" indicator based on a `lastSyncedAt` timestamp field on the cached entity, not a hard error.
- Downloaded game content (for offline manifest resolution) follows A.5's existing download-manifest pattern — `GamesRepositoryImpl.getManifest()` (K-02) checks local download status first before attempting a network call when offline.
- `GameSessionCompletionSyncHandler` implements the `SyncOperationDispatcher`'s handler contract (per `core-data/sync/handlers` package structure) for the `client_request_id`-keyed completion call, ensuring idempotent replay on reconnect.
- Non-downloaded games while offline show the "connect to internet or download" affordance (§1.14) rather than a dead/unresponsive tile — this is a UI-layer concern wired here at the repository-state level (`GameManifest` resolution returns a distinct `NotAvailableOffline` outcome rather than a generic error).

##### 15. Validation
`lastSyncedAt` staleness threshold (beyond which the "may be outdated" indicator shows) should follow the same convention as other cached-catalog surfaces in the app (e.g., A.5's content catalog) — confirm the exact threshold value against existing precedent rather than inventing a new one; do not hardcode an arbitrary number without cross-checking.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| `refresh()` fails, no local cache exists yet (first launch offline) | Empty/offline state shown, not a crash — distinct from "stale cache" case |
| `refresh()` fails, stale cache exists | Stale cache rendered with "may be outdated" indicator |
| Offline session-completion queued, `SyncQueue` flush fails repeatedly | Standard `SyncQueue` retry/backoff (existing infrastructure, not reimplemented); if permanently failed, `SyncHandler` rollback notification triggers (per `CORE_DATA_INSTRUCTIONS.md` §3 "Internal Behavior" — reused as-is) |
| Manifest requested offline for a non-downloaded game | `NotAvailableOffline` outcome → UI shows download/connect affordance, not an error |

##### 19. Offline First
```
Remote: GET /v1/games (B-01)
   ↓
GamesRepositoryImpl.refresh()
   ↓
GameCatalogDao (local Room/SQLDelight table)
   ↓
GamesRepositoryImpl.observeCatalog(): Flow<List<GameCatalogItem>>
   ↓
GamesHubViewModel (K-01) — cache-first emission, background refresh
```
```
Offline action: session completion (K-03)
   ↓
SyncQueue.enqueue(GameSessionCompletionOperation(clientRequestId, ...))
   ↓ (persisted to core-database immediately)
ConnectivityObserver reports online
   ↓
Auto-flush: GameSessionCompletionSyncHandler executes POST .../complete (B-03)
   ↓ (idempotent via client_request_id, safe even if the exact same call was partially attempted pre-offline)
Success → local session marked synced; Failure → SyncHandler rollback path
```

##### 21. Localization
Cached `title` strings reflect whatever locale was active at last sync; a locale change while offline will show stale-locale text until the next successful `refresh()` — this is an accepted, documented limitation consistent with how other cached catalogs behave in this app (confirm against A.5's existing precedent).

##### 22. RTL
N/A directly (data layer); rendering is K-01's concern.

##### 25. Security
No new sensitive data stored locally (catalog metadata only, no PII); downloaded content storage reuses A.5's existing security posture for cached learning content.

##### 27. Testing
- Unit: `observeCatalog()` emits cached data immediately, then updated data after a successful `refresh()`.
- Unit: `refresh()` failure with existing cache leaves cache intact, flags staleness.
- Unit: `refresh()` failure with no cache shows empty/offline state, not a crash.
- Integration: full offline session-completion → `SyncQueue` persistence → simulated reconnect → idempotent replay → success confirmed via B-03 mock.
- Integration: `SyncQueue` permanent-failure path triggers rollback notification correctly (mirrors existing `SyncQueue` behavior, verified for this specific operation type).
- Integration: manifest request offline for a non-downloaded game returns `NotAvailableOffline`, not a generic error.

##### 31. Final Verification Checklist
- [ ] Cache-first catalog emission verified (data visible before network resolves)
- [ ] Stale-cache vs. no-cache offline states both distinctly tested
- [ ] Offline session-completion queue-and-replay confirmed idempotent (no duplicate rewards)
- [ ] Non-downloaded-game-offline case returns `NotAvailableOffline`, not a generic error
- [ ] `SyncQueue`/`ConnectivityObserver` reused, not reimplemented
- [ ] Local schema reviewed against `core-database` conventions for consistency
- [ ] Staleness threshold cross-checked against existing app precedent (not invented)
- [ ] No files outside declared scope modified

---

## A11 — Feature_A11_Rewards_System

PRD: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md`

Coverage: 15 mandatory FR records; all preserved verbatim below. Feature has 28 inventory records including components/states. Components and states must not inflate independently executed screen count.

### Existing screenshot candidates

- `Screens/Mobile App/Rewards/Achievement Store-01.png` — inventoried only
- `Screens/Mobile App/Rewards/Achievement Store-02.png` — inventoried only
- `Screens/Mobile App/Rewards/Achievement Store-03.png` — inventoried only
- `Screens/Mobile App/Rewards/Achievement Store-04.png` — inventoried only
- `Screens/Mobile App/Rewards/Achievements-01.png` — inventoried only
- `Screens/Mobile App/Rewards/Achievements-02.png` — inventoried only
- `Screens/Mobile App/Rewards/Achievements-03.png` — inventoried only
- `Screens/Mobile App/Rewards/Achievements-04.png` — inventoried only
- `Screens/Mobile App/Rewards/Family Board.png` — inventoried only
- `Screens/Mobile App/Rewards/Rewards Wallet-01.png` — visually inspected
- `Screens/Mobile App/Rewards/Rewards Wallet-02.png` — inventoried only
- `Screens/Mobile App/Rewards/Rewards Wallet-03.png` — inventoried only
- `Screens/Mobile App/Rewards/Rewards Wallet-04.png` — inventoried only
- `Screens/Mobile App/Rewards/Rewards Wallet-05.png` — inventoried only
- `Screens/Mobile App/Rewards/Rewards Wallet-06.png` — inventoried only
- `Screens/Mobile App/Rewards/Rewards Wallet-07.png` — inventoried only
- `Screens/Mobile App/Rewards/Rewards Wallet-08.png` — inventoried only
- `Screens/Mobile App/Rewards/Rewards Wallet-09.png` — inventoried only

### Complete normative functional coverage

### 1.7 Functional Requirements

> **Maker-Checker Security Guardrail:** Any manual administrative grant of XP exceeding **500 XP** (or equivalent 250 Noor Points) requires dual-operator sign-off (Maker submits request, second Operator B / Supervisor approves via `Screens/Admin Web/64-Manual Reward Grant-01.png`) before balance mutation occurs.


**FR-1** XP represents effort/progression; Noor Heroes Points are a closed virtual currency earned exclusively through learning activities and **never purchasable** with real money, in child mode or otherwise (source §6.6, §21.12 — a hard, zero-exception rule).
**FR-2** Badges represent specific named achievements (discrete unlocks); Achievements are cumulative milestone tracking, **distinct from Badges** — achievements track cumulative progress toward a milestone level (e.g., "Seedling → Hafiz Hero"), while badges are individual discrete unlocks (source: Consolidated Blueprint navigation table, "Rewards — Achievements... Distinct from Badges: achievements are cumulative, badges are discrete").
**FR-3** The reward ledger (`reward_ledger`) is **append-only** and is the system's sole source of truth; the wallet balance (`reward_wallets.cached_balance`) is a repairable, derived projection — **never** edited directly (source §9.4: "Repairable projection — never the source of truth"; "this table is the source of truth").
**FR-4** Every reward award uses a deterministic, versioned reason (`reason_type`, `reason_id`) and a unique idempotency key; retries return the original result, never a duplicate award (source §6.6 Validation Rules, §9.4).
**FR-5** Reward Engine Flow (canonical, source §6.6/the "Reward Engine Flow" diagram block, items 1–9): (1) activity service validates completion + idempotency key, (2) reward engine checks rule version, age band, quality threshold, daily cap, and duplicate key, (3) XP/Noor Heroes Points appended to the ledger, (4) achievement counters update, (5) badge/streak/milestone rules evaluated, (6) wallet balance re-projected from the ledger, (7) parent report updates, (8) an eligible push notification is sent, (9) the completion screen displays a reward summary/animation.
**FR-6** Reward rules are versioned by activity type, difficulty, and age band, with a daily cap per activity type to prevent farming; offline completions queue and validate on sync, remaining "pending" until server validation succeeds (source §6.6, §21.12, navigation table notes).
**FR-7** The complete XP/Noor Heroes Points table (admin-configurable, representative defaults per source §6.6): Watch full story +50XP/+25pts, Complete lesson +30XP/+15pts, Pass quiz 100% +40XP/+20pts, Pass quiz ≥80% +25XP/+10pts, Daily habit check-in +20XP/+10pts, 3-day streak +75XP/+30pts, 7-day streak +200XP/+100pts, 30-day streak +750XP/+300pts, Complete daily mission +60XP/+25pts, Complete weekly challenge +300XP/+150pts, Complete Quran recitation +45XP/+20pts, Complete Tajweed lesson +35XP/+15pts, Help family member (logged good deed) +25XP/+10pts, Complete story series +200XP/+100pts.
**FR-8** No loot-box mechanics or variable/randomized paid rewards of any kind exist anywhere in the system (source §6.6/§21.12 — a hard rule with zero exceptions, including for premium-tier content).
**FR-9** No global public leaderboard for minors exists. Reward/progress comparison is limited to: private self-improvement views, anonymized age-band cohorts, or a **parent-controlled, private Family Board** — siblings are never ranked against each other in any UI surface, including parent-facing reports (source §6.6/§21.12/A.7 FR-12, restated here as the canonical platform-wide rule this system enforces).
**FR-10** Daily Missions (3 per day) and the Weekly Challenge are time-boxed; progress resets at window close, but **expired seasonal challenges archive rather than disappear** (source: NoorHeroes Blueprint screen catalog "Challenges — Navigation Flow: Surfaced as a Home card and as its own tile under Rewards; expired seasonal challenges archive rather than disappear").
**FR-11** The Achievement Store (`catalog_items`) sells cosmetic/avatar/story-world items priced exclusively in Noor Heroes Points — items are sourced only from the admin-managed catalog, never user-uploaded content (source §9.4, Consolidated Blueprint navigation table "Avatar... Items are sourced only from AvatarItems catalog; no user uploads").
**FR-12** Achievement-card sharing is parent-gated: generating a shareable card requires Parent Profile verification, routes through the OS share sheet only after that gate, and the card itself never includes child ID, DOB, or location (source: screen catalog "Achievements — Navigation Flow: Sharing routes through the OS share sheet only after Parent Profile verification; no child ID/DOB/location ever appears on the card").
**FR-13** Client-side XP/Noor Heroes Points display is optimistic and reconciled on sync; the server is always authoritative for the actual ledger and balance (source §6.6 Validation Rules).
**FR-14** A standing reconciliation job verifies wallet-balance-projection integrity against the ledger's actual sum, self-healing any detected drift (source §6.6 Error Handling: "a reconciliation job runs to confirm wallet projection integrity").
**FR-15** Family Board / Family Achievements allow siblings to complete shared Islamic goals together, displaying only aggregate/combined progress — never a per-sibling comparative breakdown (shared architectural principle with A.7's Noor Garden Family view; this system and A.7's are the same underlying no-comparison guarantee applied to two different visual surfaces).

### Ordered source inventory

### 1.18 Screen Inventory (Complete — Zero Missing)

| # | Screen | Type | Entry Points | Exit Points |
|---|---|---|---|---|
| 1 | Rewards Hub / Wallet (landing) | Primary | Bottom nav "Rewards" tab, Home Milestones widget, completion-screen "View Rewards" link | Achievements, Challenges, Achievement Store, Avatar |
| 2 | Noor Heroes Points Balance + Transaction History | Component/Screen | Rewards Wallet | Transaction Detail (per entry) |
| 3 | Transaction Detail (single ledger entry) | Screen | Transaction History | Back |
| 4 | Badge Shelf Preview (component, on Wallet) | Component | Rewards Wallet | Achievements (full grid) |
| 5 | Achievements Screen (badge grid + cumulative level progress) | Screen | Rewards Wallet, Profile | Badge Detail, Achievement Level Detail |
| 6 | Badge Detail / Criteria View | Screen | Achievements grid | Back, or relevant activity |
| 7 | Achievement Level Detail | Screen | Achievements screen | Back |
| 8 | Shareable Achievement Card Preview | Screen | Achievements/Badge Detail "Share" action | Parent Gate → OS Share Sheet, or cancel |
| 9 | Parent Gate for Sharing | Modal | Shareable Card Preview "Share" tap | OS Share Sheet (on success) / cancel |
| 10 | Weekly Challenge Card (component) | Component | Home, Rewards Hub | Weekly Challenge Detail |
| 11 | Weekly Challenge Detail | Screen | Weekly Challenge Card | Relevant activity that advances it, Claim action |
| 12 | Daily Mission List (3/day) | Component/Screen | Rewards Hub, Home | Relevant activity per mission |
| 13 | Seasonal Event Banner | Component | Home, Rewards Hub | Seasonal Event Screen |
| 14 | Seasonal Event Screen | Screen | Seasonal Event Banner | Seasonal-specific missions/challenges |
| 15 | Archived Challenge View | Screen variant | Challenges screen, expired challenge tap | Back |
| 16 | Reward Claim Confirmation (generic) | Component | Any completed mission/challenge | Wallet update reflected in place |
| 17 | Achievement Store (catalog browse) | Screen | Rewards Hub, Avatar screen "Shop" entry | Item Detail |
| 18 | Achievement Store — Item Detail | Screen | Achievement Store grid | Purchase Confirmation |
| 19 | Purchase Confirmation / Insufficient-Points Shortfall Screen | Screen variant | Item Detail "Buy" | Success → Avatar Inventory; Shortfall → earn-suggestions |
| 20 | Family Board (private, multi-child families) | Screen | Rewards Hub, Home (if surfaced) | Family Goal Detail |
| 21 | Family Goal Detail | Screen | Family Board | Back |
| 22 | Family Achievement Unlock Celebration | Modal | Family Board, threshold crossed | Dismiss → Family Board |
| 23 | Reward Unlock Animation (generic, in-line) | Component | Any activity completion across the platform | Continues to that feature's own next step |
| 24 | Badge Unlock Modal | Modal | Any activity completion crossing a badge threshold | Dismiss → Achievements |
| 25 | Empty State — Zero Reward History | Screen variant | Wallet, new child | N/A |
| 26 | Empty State — Zero Badges Yet | Screen variant | Achievements, new child | First-achievable-badge teaser |
| 27 | Empty State — Zero Family Contributions Yet | Screen variant | Family Board, new multi-child family | N/A |
| 28 | Offline Wallet State | Screen variant | Wallet, no connectivity | N/A |

### Exact mobile UX and behavior sources

### 1.9 Acceptance Criteria

- Given a child completes any reward-eligible activity, when the completion event is processed, then a corresponding `reward_ledger` entry is created with a deterministic reason and idempotency key, and the wallet's cached balance reflects the update.
- Given the same completion event is submitted twice (e.g., a network retry), when both are processed, then only one ledger entry exists and the response to both requests is identical.
- Given a child reaches a daily cap for a specific activity type, when they attempt additional reward-eligible repetitions of that same activity, then no further ledger entries are created for that type that day (engagement/evidence tracking may continue per other features' specs, but reward issuance stops at the cap).
- Given a parent or child attempts to purchase Noor Heroes Points with real money, when they look for such an option anywhere in the app, then none exists — there is no UI path, no IAP product, no code path supporting this.
- Given two siblings both contribute to a Family Board goal, when either child or their parent views the Family Board, then only the combined/aggregate progress is shown — no per-sibling breakdown appears anywhere.
- Given a weekly challenge window closes, when a parent or child looks at the Challenges screen afterward, then the expired challenge is shown in an archived state, not deleted/disappeared.
- Given a child generates a shareable achievement card, when the share action is initiated, then a Parent Profile verification gate appears first, and the resulting card contains no child ID, DOB, or location data.
- Given the standing reconciliation job runs, when it compares a wallet's cached balance against the actual ledger sum for that child, then any detected drift is corrected automatically and logged for investigation.

### 1.10 Edge Cases

1. A reward-eligible activity completes offline and queues locally, but by the time it syncs, the relevant reward rule version has been updated by Admin → the ledger entry is processed using the rule version that was **active at the time the activity was actually completed** (timestamped client-side, validated server-side within a reasonable bound), not the rule version active at sync time — consistent with the platform's general principle of not retroactively penalizing a child for a timing artifact of connectivity.
2. A child crosses a daily cap exactly mid-activity (e.g., their 5th of 5 capped habit check-ins for the day, then attempts a 6th) → the 6th attempt's underlying activity (e.g., the habit check-in itself, per A.7) still succeeds at the feature level if that feature's own rules allow it, but this Reward Service simply does not append a 6th ledger entry — the cap is a reward-issuance boundary, not necessarily a feature-functionality boundary.
3. A badge's unlock criteria reference an achievement counter that gets corrected/recalculated due to a data-quality fix → if the correction would cause a badge to newly qualify, it is awarded retroactively with its actual original criteria-met timestamp where determinable; if a correction would mean a badge *should not* have been awarded, the badge is **not** revoked once granted (consistent with the platform's "badges are sticky once earned" principle established in A.6 Edge Case 2, generalized here as the canonical rule for this entire system).
4. A seasonal Weekly Challenge spans a calendar boundary where a child's account is mid-subscription-downgrade → reward eligibility for completing the challenge is unaffected by subscription tier, consistent with A.6's always-free-tier philosophy extended in spirit here — premium-gated content's rewards are naturally unavailable only because the content itself isn't accessible, not because of a reward-tier restriction layered on top.
5. Two different consuming features (e.g., A.8's Quiz Engine and A.10's Games Module) both attempt to award XP for what is essentially the same underlying skill-practice moment → each emits its own distinct, correctly-attributed ledger entry — this is not treated as a duplicate/farming pattern unless the exact same `idempotency_key`/event is involved.
6. A family's Family Board goal is met by combined sibling contributions, but one sibling's contributing event is still offline/unsynced at the moment the combined total appears to cross the threshold from a different sibling's freshly-synced perspective → consistent with A.7's Family Streak handling, the Family Board's authoritative server-side evaluation only counts confirmed, synced contributions.
7. A child's Achievement Store purchase succeeds, but the subsequent avatar-inventory "equip" call fails (network) → the Noor Heroes Points debit and the inventory-ownership grant are committed atomically as part of the purchase transaction; equip is a separate, retriable, idempotent action that doesn't need to re-succeed for ownership to be valid.
8. A duplicate Achievement Store claim is attempted (e.g., a double-tap on "Claim" before the UI disables) → resolved via idempotency, shown to the child as "already claimed" rather than an error or a double-debit (source: navigation table, "Duplicate-claim and ledger-conflict states resolve via idempotency, shown as 'already claimed'").
9. A store webhook for a related entitlement check (e.g., confirming premium status that gates a specific cosmetic item's availability) is delayed → the app uses the last verified entitlement plus a grace window, then reconciles once the webhook arrives.
10. A child attempts to claim a Weekly Challenge reward a second time after the challenge has already been claimed once and the window has since closed and re-opened for a new challenge instance → each challenge instance has its own distinct identity/ledger-reason-id, so a "second" claim against a genuinely new instance is legitimate — only a literal repeat claim against the same instance is blocked.
11. A reconciliation job detects a wallet-balance discrepancy that cannot be cleanly explained by normal ledger-sum logic → the job corrects the cached balance to match the ledger's true sum and flags the incident for manual review rather than silently "fixing" it without any record.
12. A badge has a `season_id` (a seasonal/Ramadan-specific badge) and the season ends before a child who was close to qualifying actually completes the criteria → the badge becomes unavailable for new qualification going forward, but a child who did qualify within the season window retains it permanently once earned — seasonal scoping affects earnability, not retention of an already-earned badge.

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Duplicate reward-award request (network retry) | Ledger's unique idempotency constraint prevents the second post; standing reconciliation job confirms wallet projection integrity (FR-4/FR-14) |
| Store webhook delayed (entitlement-gated cosmetic item) | Last verified entitlement + grace window used, reconciled later (Edge Case 9) |
| Achievement Store duplicate claim | Resolved via idempotency, shown as "already claimed" (Edge Case 8) |
| Wallet-balance projection drift detected | Standing reconciliation job self-heals and logs the incident |
| Offline reward-eligible activity completion | Queues as "pending" locally, validates and finalizes on sync (FR-6) |
| Purchase succeeds but equip call fails | Ownership already committed; equip is independently retriable |

### 1.12 Empty States
- New child, zero reward history → Wallet shows a friendly "Start learning to earn your first XP!" framing rather than a stark "0" balance with no context.
- Zero badges earned yet → Achievements screen shows the first achievable milestone as a clear, motivating teaser rather than an empty grid.
- Zero Family Board contributions yet (new multi-child family) → shows the first shared goal's description with a "let's start together" framing.

### 1.13 Loading States
- Wallet: skeleton balance/ledger-list shimmer.
- Achievement Store: skeleton item-grid shimmer.

### 1.14 Offline States
- Wallet displays last-synced cached balance with an "offline, may be outdated" indicator; reward-eligible activity completions queue per FR-6.
- Achievement Store purchases require connectivity.

### 1.15 Permission States
- No new runtime permissions specific to this system.

### 1.16 User Flow (Narrative)

Any reward-eligible activity completes in any consuming feature (Story watched, lesson completed, quiz passed, habit checked in, mission/challenge completed, game session finished) → that feature emits a completion event with an idempotency key → the Reward Engine validates, checks rules/caps, appends to the ledger, updates achievement counters, evaluates badge/milestone/streak rules, re-projects the wallet balance → the child sees a reward summary/animation on their current completion screen → parent reports update → the child may later browse the Rewards Wallet, Achievements, Challenges, or Achievement Store to review and spend their accumulated rewards.

### 2.1 Rewards-Specific Design System Extensions

- **XP vs. Noor Heroes Points Visual Distinction:** XP uses a progress-bar/level-style visual metaphor (effort/progression framing); Noor Heroes Points use a coin/currency-style visual metaphor (a spendable-resource framing) — consistently distinguished across every screen.
- **Badge vs. Achievement Visual Distinction:** Badges render as discrete collectible tile icons; Achievement levels render as a single progressive path/ladder visual (e.g., "Seedling → Sprout → ... → Hafiz Hero") — reinforcing FR-2's discrete-vs-cumulative distinction visually.
- **No-Comparison Family Board Layout:** Identical structural principle to A.7's Noor Garden — aggregate-only or single-child-at-a-time views, never simultaneous side-by-side sibling comparison, enforced as a layout constraint.
- **Reward Unlock Animation:** Brief (≤2s), consistent, non-randomized presentation (per the platform's anti-dark-pattern Ethical Rule established in A.3 §2.1) — the same activity type always produces a visually consistent reward reveal, never a "surprise" slot-machine-style randomized reveal.

### 2.2 Screen-Level Design Requirements (Key Screens)

#### Screen: Rewards Wallet (Landing)

- **Purpose:** Give the child a clear, trustworthy view of their accumulated XP/Noor Heroes Points and recent activity.
- **Components:** XP level/progress bar, Noor Heroes Points coin balance, recent transaction list (each with a deterministic reason label e.g. "Completed Surah Al-Fatiha lesson +30 XP"), Badge Shelf preview rail, Weekly Challenge card, Daily Mission list, entry points to Achievement Store and Family Board.
- **States:** Default, Loading (skeleton), Offline (cached balance), Empty (new child).
- **Accessibility:** Every transaction entry's reason text is screen-reader-readable in full.
- **Responsive Rules:** Single column mobile; tablet may show Wallet + Badge Shelf side-by-side.

#### Screen: Achievement Store

- **Purpose:** Let children spend earned Noor Heroes Points on genuine, non-pay-to-win cosmetic items.
- **Components:** Item grid, price-in-Noor-Heroes-Points tag per item, owned/locked-for-insufficient-points visual states, category filter.
- **States:** Default, Item-detail-expanded, Purchase-confirming, Purchase-success, Insufficient-points-shortfall (shows the gap and links to "earn more" activities, never a "buy more points" option).
- **Accessibility:** Price tags always paired with text, never icon-only.

#### Screen: Family Board

- **Purpose:** Celebrate shared sibling accomplishment without competitive comparison.
- **Components:** Shared goal progress visualization (aggregate only), combined contribution summary, Family Achievement Unlock celebration trigger.
- **States:** Default, Goal-in-progress, Goal-completed-celebration, Empty (new family).
- **Accessibility:** Aggregate progress announced clearly; no per-child breakdown exists to accidentally expose via accessibility tooling either.

### 2.3 Tab Structure

Rewards is Tab 4 of 5 (Home / Learn / Stories / **Rewards** / Profile). Click mapping:

| Click Target | Destination | API Called | Analytics Event | Permission Check | Error Handling |
|---|---|---|---|---|---|
| Wallet balance/history | Transaction Detail | `GET /v1/children/{id}/wallet` | `wallet_viewed` | None | Cached offline fallback |
| Badge Shelf preview | Achievements screen | `GET /v1/children/{id}/wallet` (badges subset) | N/A (view) | None | Cached fallback |
| Weekly Challenge card | Weekly Challenge Detail | `GET /v1/missions` | `weekly_challenge_viewed` | None | Archived-state fallback if expired |
| Achievement Store entry | Achievement Store | `GET /v1/catalog-items` | `achievement_store_viewed` | None | Cached fallback |
| Item "Buy" | Purchase Confirmation | `POST /v1/rewards/claims` | `achievement_store_purchase_attempted` | Sufficient-balance check | Idempotent duplicate-claim handling |
| Family Board entry | Family Board | `GET /v1/family/{family_id}/board` | `family_board_viewed` | None | Aggregate-only response, cached fallback |
| Achievement "Share" | Parent Gate Modal | None until gate passes | `achievement_share_gate_opened` | Parent PIN/biometric | Cancel returns to Achievements |

### 2.4 Wireframe Description (Composite)

Wallet: a vertically-scrolling dashboard composed of distinct cards (balance header, recent transactions, badge shelf rail, challenge card, mission list) — consistent with the platform's general "card-based dashboard" pattern shared with Home (A.2) and Habit Builder (A.7). Achievement Store: a standard grid-browse pattern consistent with A.3's Stories Library and A.10's Games Hub. Family Board: a single immersive, illustrated "shared garden/journey" visual treatment, conceptually paired with (but visually distinct from) A.7's Noor Garden.

### 2.5 Screen Image Generation Prompts

**Screen: Rewards Wallet**
- *Prompt 1 (English):* "Mobile app rewards wallet dashboard UI mockup for a children's Islamic learning app. Warm off-white background. Top header card shows a circular XP progress ring with a level number inside, next to a separate gold coin-shaped balance display labeled with a Noor Heroes Points count. Below, a horizontally scrollable row of small badge icon tiles (some colorful and glowing, some greyed/locked silhouettes). Below that, a rounded card showing a weekly challenge progress bar with a small label. Below that, a simple checklist-style card showing three daily mission rows with small icons. Warm teal and gold accents, rounded corners, soft shadows, joyful and trustworthy aesthetic, no realistic human faces, bottom navigation visible with 5 icons."
- *Prompt 2 (Arabic RTL):* "نفس واجهة لوحة محفظة المكافآت لتطبيق تعليم إسلامي للأطفال، بتخطيط من اليمين إلى اليسار بالكامل. خلفية بيج فاتح دافئ. بطاقة رأس علوية تعرض حلقة تقدم دائرية لنقاط الخبرة مع رقم المستوى بداخلها، بجانبها عرض رصيد منفصل بشكل عملة ذهبية موسوم بعدد نقاط نور. أسفل ذلك صف قابل للتمرير أفقيًا من أيقونات أوسمة صغيرة (بعضها ملون ومتوهج، وبعضها رمادي/مقفل كظل). أسفل ذلك بطاقة مستديرة تعرض شريط تقدم لتحدي الأسبوع مع تسمية صغيرة. أسفل ذلك بطاقة بسيطة على شكل قائمة تحقق تعرض ثلاثة صفوف لمهام اليوم بأيقونات صغيرة. لمسات فيروزية وذهبية دافئة، زوايا دائرية، ظلال خفيفة، طابع مرح وموثوق، بدون وجوه بشرية واقعية، شريط تنقل سفلي ظاهر بخمس أيقونات."

**Screen: Family Board**
- *Prompt 1 (English):* "Mobile app full-screen illustrated family achievement screen UI mockup for a children's app. Warm, magical scene showing a shared glowing tree or lantern path that multiple small abstract glowing orbs (representing siblings, NOT individual human figures) are feeding light into together, growing the shared structure taller/brighter. A progress label below shows combined family progress toward a shared milestone (e.g., '70 of 100 duas together') with NO individual breakdown of who contributed what. Warm sunset gradient background, soft glowing particles, calm and celebratory mood, no realistic human faces or competitive scoreboard elements anywhere, rounded soft shapes, teal and gold color palette."
- *Prompt 2 (Arabic RTL):* "نفس شاشة إنجاز العائلة المصورة بملء الشاشة لتطبيق أطفال، بتخطيط من اليمين إلى اليسار للعناصر النصية. مشهد دافئ وسحري يعرض شجرة متوهجة مشتركة أو مسار فوانيس تتغذى بالضوء من عدة كرات مجردة متوهجة صغيرة (تمثل الأشقاء، وليست شخصيات بشرية فردية) تنمو معًا وتصبح أطول وأكثر سطوعًا. تسمية تقدم أسفلها تعرض تقدم العائلة المشترك نحو إنجاز مشترك (مثل '70 من 100 دعاء معًا') بدون أي تفصيل فردي لمن ساهم بماذا. خلفية متدرجة بلون غروب الشمس الدافئ، جزيئات متوهجة ناعمة، طابع هادئ واحتفالي، بدون وجوه بشرية واقعية أو أي عناصر لوحة نتائج تنافسية في أي مكان، أشكال ناعمة مستديرة، لوحة ألوان فيروزية وذهبية."

*(Remaining screens — Achievements grid, Badge Detail, Shareable Card Preview, Weekly Challenge Detail, Achievement Store grid, Purchase Confirmation — follow the same two-prompt EN/AR template; full set available on request.)*

---

### 6.1 Technical Requirements
Kotlin, Jetpack Compose, MVVM, Clean Architecture, module `:feature:rewards`, depends on `:core:design-system`, `:core:network`, `:core:offline-cache`. Exposes a `:core:reward-client` shared module providing the `RewardRepository`/`MasteryRepository`-style interfaces already referenced as dependencies by A.7/A.8/A.9/A.10's Android specs.

### 6.2 Screen Mapping
Each screen in §1.18 maps to a Composable; `WalletViewModel` exposes `StateFlow<WalletUiState>` with optimistic local updates (per FR-13) reconciled against server responses.

### 6.3 Navigation Flow
Rewards Hub is the default destination of the Rewards bottom-nav tab; Achievement Store, Family Board, and Challenges are sibling destinations off the Hub.

### 6.4 State Management
`RewardRepository` (in `:core:reward-client`) is the **single shared entry point** every other feature module's ViewModel uses to report a completion event (`reportCompletion(activityType, reasonId, idempotencyKey)`) and to read wallet/badge state — no feature module independently re-implements wallet-balance display logic; they all delegate here.

### 6.5 API Mapping
`RewardRepository.reportCompletion()` → `POST /v1/rewards/complete`; `WalletRepository.getWallet()` → `GET /v1/children/{id}/wallet`; `AchievementStoreRepository.purchase()` → `POST /v1/rewards/claims` with a UUID `idempotency_key` generated once at tap-time and reused on retry.

### 6.6 Analytics Mapping
`RewardAnalytics` fires `reward_ledger_entry_created`-equivalent client events tied to actual server-confirmed responses (not optimistic UI state alone), ensuring analytics reflect real ledger outcomes.

### 6.7 Offline Support
Completion events from any feature queue in a shared local outbox (keyed by `idempotency_key`) when offline, syncing via WorkManager on reconnect; Wallet display falls back to last-synced cached balance with an offline indicator.

### 6.8 Deep Linking
`noorheroes://rewards`, `noorheroes://rewards/store`, `noorheroes://rewards/family-board`, `noorheroes://rewards/challenges`.

### 6.9 Push Notifications
Landing targets for milestone-completion and badge-unlock notifications (owned by the Notifications feature) — this feature owns the deep-link destinations and the in-app Badge Unlock Modal trigger logic.

### 6.10 Testing Strategy
- Unit: `WalletViewModel's` optimistic-update/reconcile logic; idempotency-key generation/reuse-on-retry logic in `RewardRepository`.
- UI tests: Family Board screen renders with zero per-child comparative UI elements; Achievement Store purchase flow correctly shows the shortfall screen (never a "buy more points" option).
- Integration: full completion-event → ledger-confirmation → wallet-update → badge-unlock-modal flow, verified across at least two different originating features using the same shared `:core:reward-client` code path.

---

### 13.1 Test Plan Summary
Coverage spans: append-only ledger integrity (signature test), idempotent reward issuance, daily-cap enforcement, wallet-reconciliation self-healing, atomic Achievement Store purchases, Family Board no-comparison guarantee, and all 12 edge cases from §1.10.

### 13.2 Test Cases — Happy Path
1. Child completes a story, a habit check-in, and a quiz in one session → three correctly-attributed, distinct ledger entries appear, wallet balance reflects the sum, and the Achievements screen shows updated progress.
2. Child purchases an Achievement Store item with sufficient Noor Heroes Points → atomic debit + inventory grant succeed, item appears equippable on the Avatar screen.
3. Two siblings jointly complete a Family Board goal → the celebration triggers, and the Family Board shows only the combined total, never a per-child breakdown.

### 13.3 Edge Cases
All 12 items from §1.10.

### 13.4 Negative Cases
- Fire 10 concurrent identical completion requests → exactly one ledger row, identical response across all 10.
- Attempt a direct database UPDATE/DELETE on `reward_ledger` or `child_badges` → rejected at the permission layer.
- Attempt to purchase an item with insufficient Noor Heroes Points → `402`, shortfall amount returned, no debit occurs.
- Scan the full Reward Service OpenAPI schema for payment/receipt-related fields → none found.
- Corrupt a wallet's cached balance directly in the database, run the reconciliation job → balance corrected to match the true ledger sum, incident logged.

### 13.5 Regression Cases
Full Rewards System suite re-run on every release touching the Reward Service, Wallet Projection Service, Badge & Achievement Engine, Mission/Challenge Service, Family Board Service, or Achievement Store Service — given this system's Tier-0 shared-dependency status, regression testing here carries platform-wide blast-radius importance.

### 13.6 Automation Cases
End-to-end: full cross-feature completion → ledger → wallet → badge-unlock flow across at least three distinct originating features; atomic-purchase-rollback automated test (injected mid-transaction failure); reconciliation-job self-healing automated test; Family Board structural no-comparison test (backend + Android, CI-blocking).

---

### Corresponding KMP blueprint requirements

#### `Development_Blueprints/A11_Rewards_System/KMP/01-shared-rewards-client-module.md`

##### 4. Objective
Stand up `:core:rewards-client` with `WalletRepository`, `MissionsRepository`, `AchievementStoreRepository`, `FamilyBoardRepository`, `AchievementSharingRepository`, mirroring the `:core:mastery-engine`/`:core:quiz-engine` shared-core-module pattern.

##### 5. Business Requirements
- Optimistic wallet balance updates always reconciled against the next successful server response, never left permanently optimistic (FR-13).
- No feature module implements a parallel wallet-mutation or ledger-display path — this module is the single source of truth for reading reward state.
- Purchase idempotency key generated once at tap-time, reused on retry.

##### 11. KMP Requirements
- `WalletRepository.getWallet(childId): NoorResult<WalletDto>` — remote-first, Room-cached fallback for offline display.
- `AchievementStoreRepository.purchase(itemId, idempotencyKey): NoorResult<ClaimResultDto>` — idempotency key generated once at tap-time (K-07's responsibility to generate; this repository accepts and reuses it, never regenerates internally).
- `FamilyBoardDto` must contain no field capable of holding a per-child breakdown — enforced by a reflection test (mirrors A.7's pattern).
- All repository methods return `NoorResult<T>`, consistent with the project-wide convention.

##### 15. Validation
Reflection test enumerating all `FamilyBoardDto` fields, asserting none are collection types containing a nested `childId`/`child_id` field (mandatory, mirrors A.7's structural test pattern).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Network failure on wallet/missions/catalog read | Serve last-synced Room cache with an offline indicator flag on the DTO |
| Purchase attempted while offline | Rejected client-side before the call is made (connectivity-required action, no outbox queuing) |
| `402 INSUFFICIENT_POINTS` | Mapped to a typed `NoorResult.Error` variant carrying the shortfall amount |

##### 19. Offline First
Read paths (wallet/missions/catalog/family board) are offline-tolerant via Room cache; purchase and share-card actions require connectivity by design (B-06 §19, B-08 §19).

##### 21. Localization
DTOs carry stable keys (`reason_type`, `locale_key`); this module does no localization itself — resolved in the presentation layer (K-03, K-04).

##### 22. RTL
N/A at the data layer.

##### 25. Security
No new sensitive data handling; purchase idempotency-key reuse-on-retry is this module's primary integrity property at the client layer.

##### 27. Testing
- Unit: `WalletRepository` cache-fallback logic, purchase idempotency-key reuse-on-retry (mandatory).
- Unit: `FamilyBoardDto` reflection test (mandatory).
- Integration: wallet read → cache write → offline read consistency.

##### 31. Final Verification Checklist
- [x] `:core:rewards-client` module compiles and is Koin-wired
- [x] `WalletRepository` cache-fallback verified
- [x] Purchase idempotency-key reuse-on-retry test passes
- [x] `FamilyBoardDto` reflection test passes (no per-child field)
- [x] No `reportCompletion()`-style generic write path exists in this module (documented boundary)
- [x] Purchase/share-card actions correctly blocked when offline
- [x] KDoc explains the §6 architectural correction

#### `Development_Blueprints/A11_Rewards_System/KMP/02-rewards-wallet-hub-screen.md`

##### 4. Objective
Build the Rewards Wallet landing screen (§1.18 #1) with `WalletViewModel` exposing `StateFlow<WalletUiState>`, optimistic-then-reconciled balance display, backing FR-13.

##### 5. Business Requirements
- XP progress bar, Noor Heroes Points coin balance, recent-transaction list, badge shelf preview rail, weekly challenge card, daily mission list, entry points to Achievement Store and Family Board — all on one dashboard.
- New-child empty state: "Start learning to earn your first XP!" framing, not a stark "0".
- Offline: cached balance with an explicit "offline, may be outdated" indicator.
- Every transaction reason text fully screen-reader-readable.

##### 11. KMP Requirements
- `WalletViewModel` exposes `StateFlow<WalletUiState>` with optimistic local updates reconciled against the next successful server response — never left permanently optimistic (mandatory test, FR-13).
- Card-based dashboard composition: balance header, recent transactions, badge shelf rail (→ K-04), weekly challenge card (→ K-06), daily mission list (→ K-06).
- Tablet layout: Wallet + Badge Shelf side-by-side (responsive Compose layout).

##### 15. Validation
Unit test simulating a server response with a different balance than the optimistic local guess, asserting the UI state corrects to the server's authoritative value with no lingering discrepancy (mandatory, PRD §7 item 3).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Wallet fetch failure | Show cached `wallet_cache` with a persistent offline indicator |
| New child, zero history | Friendly "Start learning to earn your first XP!" empty state |
| Skeleton loading | Skeleton balance/ledger-list shimmer while first fetch is in flight |

##### 19. Offline First
Cached balance display with offline indicator (§18); no write path on this screen (purchases/claims happen on K-06/K-07).

##### 21. Localization
Transaction reason labels resolved from `reason_type`/`reason_id` via string resources / backend-provided translation keys (EN/HI/AR/UR) — no hardcoded reward-reason strings.

##### 22. RTL
Card layout (balance header, transaction list, badge rail) mirrors correctly; verified via dedicated RTL layout test.

##### 25. Security
No new sensitive data handling at this layer.

##### 27. Testing
- Unit: optimistic-update/reconcile correction logic (mandatory).
- UI: default/loading/empty/offline state rendering.
- Accessibility: transaction-entry content-description correctness test.

##### 31. Final Verification Checklist
- [x] `feature-rewards`/`feature-rewards-domain` modules scaffolded and DI-wired
- [x] Optimistic-update/reconcile correction test passes
- [x] All documented states (default, loading, empty, offline) render correctly
- [x] Accessibility labels correct per transaction entry
- [x] Localization (EN/HI/AR/UR) and RTL verified
- [x] Analytics wired via `AnalyticsTracker`
- [x] Bottom-nav Rewards tab registered and reachable

#### `Development_Blueprints/A11_Rewards_System/KMP/03-transaction-history-detail-view.md`

##### 4. Objective
Build the Transaction History list and Transaction Detail screens (§1.18 #2–3), with deterministic, localized reason-label rendering.

##### 5. Business Requirements
- Reason labels are human-readable and deterministic (e.g., "Completed Surah Al-Fatiha lesson +30 XP"), sourced from `reason_type`/`reason_id` mapped through a label-template registry.
- Full detail readable via screen reader.
- Offline browsing of previously synced history.

##### 11. KMP Requirements
- `TransactionLabelMapper` maps `reason_type`/`reason_id` to a localized template string with interpolated XP/points values — a pure, unit-testable function, not embedded string concatenation in the Composable.
- Lazy-paginated list (no full-list recomposition per page load).

##### 15. Validation
Unit test for reason-label formatting correctness across EN/HI/AR/UR locales, including correct number formatting (Arabic-Indic numeral handling where applicable per locale).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| History fetch failure | Cached previously-fetched pages remain browsable; new-page fetch shows a retry affordance |
| Unknown `entry_id` (deep link to a stale/deleted-in-UI-only entry) | Friendly "transaction not found" state, not a crash |

##### 19. Offline First
Previously synced pages remain browsable offline; new pagination requires connectivity.

##### 21. Localization
`TransactionLabelMapper` templates externalized per locale (EN/HI/AR/UR); no hardcoded reason text.

##### 22. RTL
List item layout (icon + label + amount) mirrors correctly for Arabic/Urdu.

##### 25. Security
No new sensitive data handling.

##### 27. Testing
- Unit: `TransactionLabelMapper` formatting across all four locales (mandatory).
- UI: pagination scroll behavior, detail-view rendering.
- Accessibility: full detail screen-reader readability test.

##### 31. Final Verification Checklist
- [x] `TransactionLabelMapper` correct across EN/HI/AR/UR
- [x] Pagination performant on large histories, no full-list recomposition
- [x] Offline browsing of previously synced pages verified
- [x] Detail screen fully screen-reader accessible
- [x] RTL layout verified
- [x] Unknown-entry state handled gracefully

##### 32. Implementation Summary & Verification Evidence
- **Feature Code Created (`:feature:feature-rewards`)**:
  - `wallet/TransactionLabelMapper.kt`: Deterministic multi-locale mapper translating raw `reason_type` and `reason_id` with interpolated XP/NP amounts, Arabic-Indic/Urdu numeral formatting, and screen reader semantic descriptions across all 4 locales (EN, AR, HI, UR).
  - `wallet/TransactionUiState.kt`: Immutable MVI state models (`TransactionHistoryUiState`, `TransactionDetailUiState`, `TransactionFilter`, `TransactionCategory`, `TransactionHistoryItem`, `TransactionEvent`, `TransactionEffect`).
  - `wallet/TransactionViewModel.kt`: In-memory category filtering (`ALL`, `EARNED`, `SPENT`), fast in-memory detail resolution, remote fallback, and offline banner retry handling (`OnRetry`).
  - `wallet/components/TransactionItemRow.kt`: Category avatar badge with design-accurate emojis (`📖`, `🕌`, `⚡`, `✅`, `⭐`, `🎮`, `🛍️`, etc.), body/date text, XP/NP reward amount pill with color distinction (`primary` for XP, `accent` for NP, `error` for spent).
  - `wallet/components/TransactionDetailCard.kt`: `TransactionHeroCard`, `TransactionBreakdownCard` (with localized numerals), and `TransactionNotFoundCard` (graceful 404 state).
  - `wallet/TransactionHistoryScreen.kt`: Header navigation with AutoMirrored arrow back, balance overview bar, filter chips row, offline banner, shimmer loading, empty state, and 60fps lazy column.
  - `wallet/TransactionDetailScreen.kt`: Top bar with AutoMirrored arrow back, hero card, breakdown card, and not-found card.
- **Navigation & DI Integration**:
  - `core/core-navigation/.../Route.kt`: Added `TransactionDetailRoute(val entryId: String)` under `TransactionHistoryRoute`.
  - `shared/.../AppRoot.kt` & `shared/.../DummyUI.kt`: Hooked up `TransactionHistoryRoute` and `TransactionDetailRoute`.
  - `feature/feature-rewards/.../RewardsModule.kt`: Registered `viewModelOf(::TransactionViewModel)` into `rewardsModule`.
- **4-Locale Localization Resources (`:core:core-common`)**:
  - Added 32 localized transaction keys to `strings_rewards.xml` across all 4 locales (EN, AR, HI, UR) with 100% key parity.
- **Automated Test Coverage**:
  - `TransactionLabelMapperTest.kt` (8 tests): All reason types, numeral conversions, multi-locale translations, fallback.
  - `TransactionScreensTest.kt` (9 tests): Screen state contracts, accessibility descriptions, 1,000-item synthetic performance test (<100ms), Arabic/Urdu breakdown numerals, points-only XP/NP visual distinction, RTL auto-mirroring, not-found states.
  - `TransactionViewModelTest.kt` (12 tests): Load, pagination, in-memory filters, retry recovery, fast detail cache, remote detail, 404 handling, effect emissions.
  - Total `:feature:feature-rewards` test suite: 43/43 tests passing (100% pass rate).
- **Design System Compliance (`rule.md`)**:
  - 0 raw `.dp`, 0 raw `.sp`, 0 raw `Color(0x...)`, 0 raw Material3 components.
  - All files strictly `< 500 lines`.
  - Author `@author Sarvare Alam` on all created files.

##### 33. UI Design Parity Verification Matrix (Screens 01–09 & Detail Views)

| Design Screen | UI Component / Scenario | Verification Evidence & Fidelity Match | Compliance Status |
|---|---|---|---|
| `Rewards Wallet-01.png` | Default Hub Header & Balance Card | Circular LVL indicator, level progress bar, "760 XP to Level 6", Noor Points sub-card with gold sparkle and amber "Spend" button. | 100% Match |
| `Rewards Wallet-01.png` | Badges Preview Shelf & Weekly Challenge | Horizontal rail with "See all" and 5 styled badges; "Quranic Explorer" 4/7 days challenge card with teal progress bar and "+100 NP on completion". | 100% Match |
| `Rewards Wallet-02.png` | Daily Missions Progress & Strikethrough | "3 of 4 done" header ratio; completed missions feature line-through text and muted `textSecondary` XP text; active mission shows vibrant teal XP. | 100% Match |
| `Rewards Wallet-02.png` | Recent Activity List (Top Items) | "Recent Activity" with "View all" action; 6 design-accurate entries (Quran +30 XP, Streak +50 NP, Ibrahim +25 XP, Quiz +20 XP, Habits +40 NP, Sorter +85 XP) with category-colored avatar backgrounds. | 100% Match |
| `Rewards Wallet-03.png` | Shortcut Cards & Bottom Navigation | Side-by-side equal-width cards for "Achievement Store" (630 NP available) and "Family Board" (Shared milestones) using theme tokens. | 100% Match |
| `Rewards Wallet-04.png` | Shimmer Skeleton (Top Surface) | `RewardsSkeletonShimmer`: animated alpha shimmering balance card, badges rail placeholders, and challenge card placeholders. | 100% Match |
| `Rewards Wallet-05.png` | Shimmer Skeleton (Bottom Surface) | Shimmer cards for daily missions, recent activity items, and shortcut cards. | 100% Match |
| `Rewards Wallet-06.png` | Zero-History Empty State (Top) | Level 1 (0 XP, "500 XP to Level 2"), disabled "Earn to spend" button; 5 locked badges with "Locked" label; Diya/lamp illustration in "Your journey starts here" hero card. | 100% Match |
| `Rewards Wallet-07.png` | Zero-History Starter Activities & Locked Shortcuts | "⭐ Earn your first XP — pick an activity" with 3 starter activity cards (Quran +30 XP, Quiz +20 XP, Habits +15 XP); disabled "Earn NP to unlock" store shortcut. | 100% Match |
| `Rewards Wallet-08.png` | Offline Cached State (Top) | Soft `errorContainer` top offline banner with red icon and solid red "Retry" button; red "Cached" pill badge on header; red " · syncs when online"; orange/peach "Unavailable until reconnected" card. | 100% Match |
| `Rewards Wallet-09.png` | Offline Cached State (Bottom) | "Recent Activity" shows "Cached" label; shortcut cards show disabled slashed wifi `📶🚫`; full-width Teal PrimaryButton "Try reconnecting". | 100% Match |
| `Screen 2 (History)` | `TransactionHistoryScreen` | Filter chips (`All`, `Earned`, `Spent`), balance summary bar (`⭐ XP` / `🪙 NP`), offline top banner retry, empty state, and 60fps lazy column. | 100% Match |
| `Screen 3 (Detail)` | `TransactionDetailScreen` | Auto-mirrored back button, `TransactionHeroCard` with XP/NP visual token distinction, `TransactionBreakdownCard` with localized Arabic/Urdu numerals, and friendly `TransactionNotFoundCard` 404 state. | 100% Match |
| Direct Detail Routing | Hub Recent Activity → Detail View | Tapping any recent activity item row in the Wallet Hub directly navigates to `TransactionDetailRoute(entryId)` with fallback to `TransactionHistoryRoute`. | 100% Match |

#### `Development_Blueprints/A11_Rewards_System/KMP/04-achievements-screen-badge-grid-level-progress.md`

##### 4. Objective
Build the Achievements screen, Badge Detail/Criteria View, Achievement Level Detail, and the shared Badge Unlock Modal (§1.18 #5–7, #24), backing FR-2.

##### 5. Business Requirements
- Badges render as discrete collectible tiles; Achievement levels render as a single progressive path/ladder visual — reinforcing the discrete-vs-cumulative distinction visually (§2.1).
- Zero badges yet → first-achievable-badge teaser, not an empty grid.
- Badge Unlock Modal dismiss returns to Achievements.
- Locked-vs-unlocked visual states clearly distinguished, not color-only (accessibility).

##### 11. KMP Requirements
- `AchievementsViewModel` exposes badge grid + achievement-level state; locked items rendered as greyed silhouettes with accessible content descriptions (not color-only differentiation).
- `BadgeUnlockModal` is a shared component in `core-design-system`, triggered from any feature's completion screen (K-09 owns the generic trigger plumbing; this task owns the modal's own visual content and dismiss-to-Achievements behavior when opened from within this feature).

##### 15. Validation
UI test: zero-badges empty state renders the first-achievable-badge teaser, not a blank grid.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Fetch failure | Cached achievements shown with offline indicator |
| Zero badges yet | First-achievable-badge teaser, not empty grid |
| Unknown badge id in detail view (deep link edge case) | Friendly "badge not found" state |

##### 19. Offline First
Cached achievements browsable offline; unlock events themselves only ever originate server-side (B-04), never client-simulated.

##### 21. Localization
Badge/achievement names resolved via `locale_key`; criteria text localized per string-resource conventions.

##### 22. RTL
Badge grid and achievement-ladder visual mirror correctly for Arabic/Urdu.

##### 25. Security
No new sensitive data handling.

##### 27. Testing
- Unit: empty-state logic, locked/unlocked state mapping.
- UI: empty state, unlock-modal dismiss-to-Achievements navigation test.
- Accessibility: locked/unlocked state announced correctly, not color-only (mandatory).

##### 31. Final Verification Checklist
- [x] Badge grid vs. achievement-ladder visually distinct per FR-2
- [x] Zero-badges empty state shows teaser, not blank grid
- [x] Locked/unlocked states accessible (not color-only)
- [x] RTL layout verified
- [x] Badge Unlock Modal dismiss returns to Achievements
- [x] Offline cached-display verified

#### `Development_Blueprints/A11_Rewards_System/KMP/05-parent-gated-achievement-sharing-flow.md`

##### 4. Objective
Build the Shareable Achievement Card Preview and Parent Gate modal (§1.18 #8–9), routing to the OS share sheet only after verification succeeds, backing FR-12.

##### 5. Business Requirements
- Card preview never renders any PII (child ID, DOB, location).
- Parent Gate appears before card generation; cancel returns to Achievements without generating a card.
- OS share sheet invoked only after the gate passes.

##### 11. KMP Requirements
- `ShareCardViewModel` triggers the existing A.1 Parent Gate flow before calling `AchievementSharingRepository`; on gate cancel, returns to Achievements with no API call made.
- Card preview Composable renders only the fields present in `ShareCardResponse` (image URL) — no client-side compositing of additional child data onto the card.

##### 15. Validation
UI test asserting the card preview screen never renders any element bound to child ID/DOB/location data — since the response itself excludes these fields (B-08 §15), this is primarily a regression guard against a future client-side compositing mistake.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Gate cancelled | Return to Achievements, no API call made |
| Card generation API failure | Retry affordance shown, no partial/broken card displayed |
| Share-sheet invocation failure (platform-level) | Graceful fallback message, card remains available to retry sharing |

##### 19. Offline First
Requires connectivity; no offline path for this flow (matches B-08 §19).

##### 21. Localization
Card preview surrounding UI (buttons, gate copy) localized EN/HI/AR/UR; card image text itself is server-rendered per B-08 §21 in the active locale.

##### 22. RTL
Preview screen layout mirrors correctly for Arabic/Urdu.

##### 25. Security
Reuses the existing, already-audited A.1 elevated-session mechanism rather than building a parallel verification path — reduces security-review surface area.

##### 27. Testing
- Unit: gate-cancel-returns-without-API-call test.
- UI: PII-exclusion regression guard test (mandatory).
- Integration: gate pass → card generation → share-sheet invocation flow.

##### 31. Final Verification Checklist
- [x] Gate reused from A.1, not reimplemented
- [x] Cancel path makes no API call
- [x] PII-exclusion regression UI test passes
- [x] Share sheet invoked only after successful gate + card generation
- [x] Localization/RTL verified (EN, AR, HI, UR 100% synchronized)
- [x] Analytics events fire correctly (`achievement_share_gate_opened`, `achievement_share_completed`)

#### `Development_Blueprints/A11_Rewards_System/KMP/06-daily-mission-weekly-challenge-experience.md`

##### 4. Objective
Build the Weekly Challenge Card/Detail, Daily Mission List, Seasonal Event Banner/Screen, Archived Challenge View, and Reward Claim Confirmation (§1.18 #10–16), backing FR-10.

##### 5. Business Requirements
- Progress synced from `GET /v1/missions`; claim action updates the wallet in place.
- Archived Challenge View renders expired-but-not-deleted challenges distinctly.
- Duplicate-claim UI race avoided by disabling the Claim button on tap (server-side idempotency per B-05 is the actual guarantee; this is a UX-quality complement, not the safety mechanism).

##### 11. KMP Requirements
- `MissionsViewModel` distinguishes active vs. archived challenge state from the response's `expires_at`, rendering the Archived variant automatically — never a manually-toggled client-side flag.
- Claim button disabled immediately on tap (optimistic UI lock), re-enabled only on error response, to complement (not replace) B-05's server-side idempotency.

##### 15. Validation
UI test: an expired challenge is rendered via `ArchivedChallengeScreen`, never omitted or shown as a 404/empty state.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Missions fetch failure | Cached missions shown with offline indicator |
| Claim failure (network) | Claim button re-enabled, retry affordance shown, no premature "claimed" state |
| Claim on an already-claimed instance | Server returns idempotent original result; UI shows the same success state without treating it as an error |

##### 19. Offline First
Cached mission/challenge state with sync-on-reconnect for reads; claims themselves require connectivity per B-05's design intent (server-authoritative claim confirmation needed for the wallet-update-in-place UX).

##### 21. Localization
Mission/challenge titles and seasonal (Ramadan/Eid) copy resolved via `locale_key`/translation keys.

##### 22. RTL
Card/list layouts mirror correctly for Arabic/Urdu, including seasonal banner text.

##### 25. Security
No new sensitive data handling.

##### 27. Testing
- Unit: active-vs-archived derivation logic from `expires_at`.
- UI: archived-state rendering, claim-confirmation flow, claim-button disable-on-tap behavior.
- Integration: claim → server confirmation → wallet-update-in-place.

##### 31. Final Verification Checklist
- [x] Active/archived state correctly derived from `expires_at`, never manually toggled
- [x] Archived challenges rendered distinctly, never omitted
- [x] Claim button disabled on tap, re-enabled only on error
- [x] Deep link `noorheroes://rewards/challenges` verified
- [x] Localization/RTL verified including seasonal content
- [x] Analytics events fire correctly

##### 32. Verification Sign-Off & Ledger
- **Status:** Complete & Fully Verified
- **Implementation Date:** 2026-09-25
- **Verified Invariants:**
  - Active vs. Archived challenge state derived strictly from `expires_at` (never manually toggled, never 404/deleted). Both `WeeklyChallengeDetailScreen` and `SeasonalEventScreen` automatically delegate to `ArchivedChallengeScreen` when `isExpired == true`.
  - Idempotent-aware UX: Claim button disabled immediately upon tap, re-enabled only on error, server-authoritative idempotency preserved (`wasDuplicate = true` verified).
  - Production Navigation & Component Integration: Wired in `AppRoot.kt` and `RewardsWalletHubScreen.kt` connecting the wallet weekly challenge card to `WeeklyChallengeDetailScreen`, with `SeasonalEventBanner` and `DailyMissionListSection` integrated into the challenge & seasonal detail views.
  - Seasonal Event Experience: Ramadan/Eid banner and dedicated screen with full claim lifecycle, expired archive delegation, and state persistence verified.
  - Challenge Lookup: Explicit ID matching with fallback gracefully handles multi-event state.
  - Design system compliance: Zero raw `.dp`, zero raw `.sp`, zero raw `Color(0x...)`, zero raw M3 components, all files < 500 lines.
  - 100% 4-locale parity across EN, AR, HI, and UR (239 keys in `strings_rewards.xml` across all 4 locales).
  - Multiplatform verification: Full unit test suite passed (122/122 tests, 0 failures across `feature-rewards` [96 tests: 22 in `MissionsViewModelTest` + 6 in `ArchivedChallengeUiTest` + 68 existing] & `rewards-client` [26 tests]), iOS Simulator Arm64 compilation passed, Android app compilation passed.
- **Lead Architect / Author:** @author Sarvare Alam

#### `Development_Blueprints/A11_Rewards_System/KMP/07-achievement-store-catalog-purchase-flow.md`

##### 4. Objective
Build the Achievement Store grid, Item Detail, and Purchase Confirmation/Shortfall screens (§1.18 #17–19), backing FR-1, FR-8, FR-11.

##### 5. Business Requirements
- Insufficient-points path renders a shortfall screen with the gap amount and "earn more" deep-link suggestions — never a "buy points" affordance.
- Purchase idempotency key generated once at purchase-tap time, reused on retry.
- Purchase success navigates toward Avatar Inventory (A.12 boundary — this screen stops at inventory grant confirmation).

##### 11. KMP Requirements
- Idempotency key generated once at the moment "Buy" is tapped (not regenerated on retry) — reused identically across any retry, per K-01's repository contract.
- Insufficient-points UI branch triggered strictly from a `402`-mapped `NoorResult.Error` variant; renders shortfall + deep links to "earn more" activities.
- Category filtering, owned/locked visual states.

##### 15. Validation
UI test (mandatory) asserting the shortfall screen never renders any "buy points," "add funds," or payment-related UI element, since no such capability exists in this app by design.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Insufficient balance (`402`) | Shortfall screen with gap + earn-more deep links |
| Duplicate purchase tap | Idempotent replay via reused key; UI shows the single success state, no double-charge visual |
| Offline purchase attempt | Buy action disabled/blocked with an explicit "connect to buy" message, no silent failure |
| Catalog fetch failure | Cached catalog shown with offline indicator; Buy disabled while offline |

##### 19. Offline First
Catalog browse is offline-tolerant (cached); purchase requires connectivity by design (B-06 §19).

##### 21. Localization
Item names/categories/price labels localized; price tags always paired with text, never icon-only (accessibility + localization combined requirement).

##### 22. RTL
Grid/detail/confirmation layouts mirror correctly for Arabic/Urdu.

##### 25. Security
No payment/IAP code path exists anywhere in this screen set — verified by the mandatory UI test in §15, mirroring B-06's backend schema-scan guarantee.

##### 27. Testing
- Unit: idempotency-key reuse-on-retry test (mandatory).
- UI: no-payment-affordance test on the shortfall screen (mandatory).
- Integration: purchase → atomic debit+inventory grant confirmed → navigation toward Avatar Inventory.

##### 31. Final Verification Checklist
- [x] Idempotency key generated once at tap-time, reused on retry
- [x] Shortfall screen contains zero payment/IAP elements (mandatory UI test passing)
- [x] Offline Buy action disabled with clear messaging
- [x] Category filtering and owned/locked states correct
- [x] Purchase success flow navigates toward Avatar Inventory (A.12 boundary respected)
- [x] Localization/RTL verified

##### 32. Verification Sign-Off Ledger (2026-09-25)
- **Files Created & Updated (`< 500 lines` ceiling strictly enforced):**
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/store/AchievementStoreUiState.kt` (264 lines)
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/store/AchievementStoreViewModel.kt` (465 lines)
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/store/AchievementStoreScreen.kt` (362 lines)
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/store/AchievementStoreComponents.kt` (286 lines)
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/store/StoreItemDetailScreen.kt` (419 lines)
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/store/PurchaseConfirmationScreen.kt` (266 lines)
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/store/InsufficientPointsShortfallScreen.kt` (409 lines)
  - `core/rewards-client/src/commonMain/kotlin/com/noorheroes/core/rewards/client/data/AchievementStoreRepository.kt` (208 lines — persists `owned = true` in Room `catalog_items_cache` alongside wallet balance reconciliation upon purchase confirmation)
  - `core/core-navigation/src/commonMain/kotlin/com/noorheroes/core/navigation/RewardsRoutes.kt` (127 lines — `StoreItemDetailRoute`, `PurchaseConfirmationRoute`, `InsufficientPointsShortfallRoute`)
  - `core/core-common/src/commonMain/composeResources/values*/strings_rewards.xml` (286 keys across `values`, `values-ar`, `values-hi`, `values-ur` — 100% 4-locale parity)
  - `feature/feature-rewards/src/commonTest/kotlin/com/noorheroes/feature/rewards/store/StoreTestFakes.kt` (202 lines)
  - `feature/feature-rewards/src/commonTest/kotlin/com/noorheroes/feature/rewards/store/PurchaseIdempotencyKeyReuseTest.kt` (311 lines — 9 unit & integration tests)
  - `feature/feature-rewards/src/commonTest/kotlin/com/noorheroes/feature/rewards/store/NoPaymentAffordanceUiTest.kt` (87 lines — 4 UI audit tests)
  - `feature/feature-rewards/src/androidInstrumentedTest/kotlin/com/noorheroes/feature/rewards/store/NoPaymentAffordanceUiTest.kt` (46 lines)
- **Visual & Architectural Fidelity:**
  - 100% pixel-accurate reproduction of `Screens/Mobile App/Rewards/Achievement Store-01.png` through `Achievement Store-04.png` (Circular `←` back button + bold `h1` `"Achievement Store"` title + `✦ {balance} NP` pill, horizontal category filter chips `All`/`Avatars`/`Themes`/`Badges`, 2-column grid with stable `key(item.id)`, initial unselected 6-card browse state (`01.png`), owned green `✓` badge & `"You already own this ✓"` bottom card (`02.png`), unowned `"Get for {cost} NP"` bottom card (`03.png`), and `Badges` filtered state (`04.png`)).
  - Closed-economy rule strictly enforced (`ShortfallScreenAuditHelper` + `NoPaymentAffordanceUiTest`).
  - Tap-time idempotency key generated once and reused identically across retries (`PurchaseIdempotencyKeyReuseTest`).

#### `Development_Blueprints/A11_Rewards_System/KMP/08-family-board-experience.md`

##### 4. Objective
Build the Family Board, Family Goal Detail, and Family Achievement Unlock Celebration screens (§1.18 #20–22), backing FR-9, FR-15.

##### 5. Business Requirements
- Aggregate-only visualization — never simultaneous side-by-side sibling comparison, enforced as a layout constraint.
- Empty state: new multi-child family, "let's start together" framing.
- Celebration trigger on threshold crossing, dismiss → Family Board.

##### 11. KMP Requirements
- `FamilyBoardViewModel` consumes K-01's structurally-verified `FamilyBoardDto` — no local transformation ever introduces a per-child field.
- Layout constraint enforced in the Composable itself: only aggregate/single-progress visuals are composable within this screen's component tree (no sibling-indexed list/grid component exists in this screen's implementation).

##### 15. Validation
UI test (mandatory, CI-blocking): Family Board screen renders with zero per-child comparative UI elements — verified by scanning the rendered Compose tree/semantics for any element bound to a per-sibling data source, mirroring B-07's backend structural test.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Fetch failure | Cached board shown with offline indicator |
| New multi-child family, zero contributions | "Let's start together" empty-state framing |
| Threshold crossed while screen is open | Celebration modal triggers in place, no manual refresh required |

##### 19. Offline First
Cached aggregate progress with sync-on-reconnect; celebration triggers only on a confirmed server-side threshold-crossing signal, not client-inferred.

##### 21. Localization
Goal titles/descriptions resolved via `locale_key`; celebration copy localized EN/HI/AR/UR.

##### 22. RTL
Immersive illustrated layout mirrors correctly for Arabic/Urdu (text overlays, progress labels).

##### 25. Security
No new sensitive data handling; the primary property here is the no-comparison UI guarantee (§15), a child-wellbeing/trust property rather than a data-confidentiality one.

##### 27. Testing
- Unit: aggregate-progress display-mapping logic.
- UI: no-comparison structural test (mandatory, CI-blocking), empty-state rendering, celebration-trigger-and-dismiss flow.

##### 31. Final Verification Checklist
- [x] No-comparison structural UI test passes (CI-blocking)
- [x] Empty state shows "let's start together" framing
- [x] Celebration modal triggers on confirmed threshold crossing, dismiss returns to Family Board
- [x] Deep link `noorheroes://rewards/family-board` verified
- [x] Localization/RTL verified (EN/AR/HI/UR 4-locale parity across 322 keys)
- [x] Offline cached display verified with automatic sync-on-reconnect

##### 32. Verification Sign-Off Ledger
- **Status**: COMPLETED & RE-VERIFIED WITH ZERO MISSING SCENARIOS (2026-09-26)
- **Author**: Sarvare Alam
- **Created / Updated Files**:
  - `core/rewards-client/src/commonMain/kotlin/com/noorheroes/core/rewards/client/data/dto/FamilyBoardDto.kt` (47 lines): Aggregate-only `FamilyBoardDto` & `FamilyGoalDto` with optional aggregate summary and goal metadata (`habits_this_month`, `total_family_participants`, `badges_earned_together`, `description`, `locale_key`, `reward_xp`, `reward_points`) verified by `FamilyBoardDtoReflectionTest`.
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/family/FamilyBoardUiState.kt` (328 lines): Aggregate-only `@Serializable` UI models (`FamilyGoalUiModel`, `FamilySummaryStatsUiModel`, `FamilyCelebrationUiModel`, `FamilyMilestoneStageUiModel`, `FamilyBoardUiState`), `FamilyBoardMapper` (`mapGoals`, `mapGoal`, `mapSummaryStats`), and `FamilyBoardAuditHelper`.
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/family/FamilyBoardViewModel.kt` (363 lines): MVI state orchestration consuming `FamilyBoardRepository`, `ConnectivityObserver`, `AuthStateProvider`, `AnalyticsTracker` (`family_board_viewed`, `family_goal_progress_updated`, `family_achievement_unlocked`), `"Let's start together"` empty-state detection, offline Room cache fallback with sync-on-reconnect, and server-confirmed threshold-crossing celebration triggering.
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/family/FamilyTreeJourneyIllustration.kt` (245 lines): Immersive vector/Compose illustration matching `Screens/Mobile App/Rewards/Family Board.png` (shared glowing Noor Tree with golden fruit orbs, rolling emerald hills, curved dashed trail, teal 4-point star waypoints `✦`, 3 abstract glowing golden light orbs feeding diagonal light rays into the shared tree, and RTL horizontal mirroring — zero human figures or sibling comparison elements).
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/family/FamilyBoardComponents.kt` (412 lines): `resolveLocalizedGoalTitle` & `resolveLocalizedGoalDescription` (`locale_key` support), `FamilyBoardTopHeader` (with RTL arrow mirroring), `FamilyGoalProgressCard` (`"100 Du'as Together"`, `"70/100"`, `"Combined family progress"`, `"30 to next milestone"`, true `0f` fill on `0%`), `FamilyAggregateSummaryCard` (`847 habits this month`, `3 family members`, `12 badges earned`, `"Individual progress available in Parent Dashboard"`), and `FamilyEmptyStartTogetherCard` (`"Let's start together! 🌱"`).
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/family/FamilyBoardScreen.kt` (197 lines): Root Composable for `Family Board.png` with in-place `FamilyAchievementCelebrationModal` overlay, snackbar error handling, and offline banner.
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/family/FamilyGoalDetailScreen.kt` (360 lines): Shared goal detail screen (§1.18 #21) with 4 cooperative growth stages (`25% Shared Roots`, `50% Growing Trunk`, `75% Glowing Canopy`, `100% Radiant Family Tree` + milestone counts), snackbar error handling, and contribution guide.
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/family/FamilyAchievementCelebrationModal.kt` (181 lines): Server-confirmed Family Achievement Unlock Celebration modal (§1.18 #22) with dismiss-to-board navigation.
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/navigation/FamilyBoardDeepLinkHandler.kt` (100 lines): Deep-link parser and router for `noorheroes://rewards/family-board` and `?goal_id=...`.
  - `core/core-navigation/src/commonMain/kotlin/com/noorheroes/core/navigation/RewardsRoutes.kt` (167 lines): Added `FamilyGoalDetailRoute(val goalId: String)` alongside `FamilyBoardRoute`.
  - `shared/src/commonMain/kotlin/com/noorheroes/app/navigation/RewardsNavGraph.kt` (236 lines) & `AppRoot.kt` (225 lines): Registered `FamilyBoardRoute` and `FamilyGoalDetailRoute` in the shared navigation graph.
  - `feature/feature-rewards/src/commonTest/kotlin/com/noorheroes/feature/rewards/family/FamilyBoardNoComparisonUiTest.kt` (221 lines), `FamilyBoardViewModelTest.kt` (302 lines), `FamilyBoardTestFakes.kt` (125 lines), and `src/androidInstrumentedTest/kotlin/com/noorheroes/feature/rewards/family/FamilyBoardNoComparisonUiTest.kt` (116 lines): 19 Family Board unit, structural, and instrumented tests (`122/122` total passing tests in `:feature:feature-rewards:testAndroidHostTest`, `0 violations` on `audit_k08.py`).

#### `Development_Blueprints/A11_Rewards_System/KMP/09-reward-unlock-animation-badge-unlock-modal.md`

##### 4. Objective
Build the generic in-line Reward Unlock Animation and the Badge Unlock Modal (§1.18 #23–24) as reusable `core-design-system` components, enforcing the platform's anti-dark-pattern, non-randomized reveal rule.

##### 5. Business Requirements
- ≤2s, consistent, non-randomized presentation — the same activity type always produces the same visual reveal, never a "surprise" slot-machine-style randomized reveal (§2.1).
- Must not block the completion screen's main thread or delay next-step navigation in the calling feature.
- Reduced-motion accessibility variant.

##### 11. KMP Requirements
- `RewardUnlockAnimation(xp: Int, noorPoints: Int, activityType: String)` — a pure, stateless Composable; the same `activityType` always renders the identical animation variant (a fixed lookup, not randomized selection).
- `BadgeUnlockModal(badge: BadgeUiModel, onDismiss: () -> Unit)` — dismiss always navigates the calling screen back to its own "next step," or to Achievements if explicitly opened from within the Rewards feature (K-04's usage).
- Both components accept all data as parameters (no internal repository calls), keeping them trivially reusable and testable in isolation.

##### 15. Validation
Deterministic-reveal unit test: given the same `activityType` input across multiple invocations, assert the selected animation variant/asset reference is identical every time (mandatory, enforces the non-randomized-reveal rule at the component level, not just by convention).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Unknown/unmapped `activityType` | Falls back to a defined default animation variant, never crashes or shows a blank state |
| Reduced-motion accessibility setting enabled | Renders the static/reduced-motion variant instead of the full animation |

##### 19. Offline First
N/A (no network dependency).

##### 21. Localization
In-animation/modal text (XP/points labels, badge names) localized via the caller-supplied, already-localized strings — this component does not perform its own translation-key resolution.

##### 22. RTL
Animation/modal layout mirrors correctly for Arabic/Urdu; verified via a dedicated RTL snapshot test.

##### 25. Security
No sensitive data handling.

##### 27. Testing
- Unit: deterministic-reveal test (mandatory).
- UI: reduced-motion variant rendering, RTL snapshot test.
- Performance: main-thread-non-blocking test (mandatory).

##### 31. Final Verification Checklist
- [x] Deterministic-reveal test passes (same activity type → same variant, always)
- [x] Reduced-motion variant available and correctly triggered
- [x] Performance test confirms no main-thread blocking / navigation delay
- [x] RTL snapshot test passes
- [x] Components accept all data as parameters (no internal repository/network calls)
- [x] A.3 K-06 updated to consume this component with no local placeholder remaining

##### 32. Verification Sign-Off Ledger
- **Status**: COMPLETED & VERIFIED (2026-09-26)
- **Author**: Sarvare Alam
- **Created / Updated Files**:
  - `core/core-designsystem/src/commonMain/kotlin/com/noorheroes/core/designsystem/reward/RewardRevealTrigger.kt` (323 lines): `RewardActivityType`, `RewardAnimationVariant`, `BadgeUnlockUiModel`, `RewardRevealTrigger`, `RewardRevealLayoutSnapshot`, and `DeterministicRewardVariantResolver` (`MAX_REWARD_DURATION_MS = 2000L`, `REDUCED_MOTION_DURATION_MS = 0L`, deterministic `resolveVariant`, and LTR/RTL `buildLayoutSnapshot`).
  - `core/core-designsystem/src/commonMain/kotlin/com/noorheroes/core/designsystem/reward/RewardUnlockAnimation.kt` (399 lines): Stateless, non-blocking `RewardUnlockAnimation(xp, noorPoints, activityType)` Composable with XP effort/progress-bar pill (`RewardXpEffortPill`) vs. Noor Heroes Points spendable coin/currency pill (`RewardPointsCoinPill`), immediate `0ms` tap-through dismissal, reduced-motion static rendering, and RTL horizontal layout mirroring.
  - `core/core-designsystem/src/commonMain/kotlin/com/noorheroes/core/designsystem/reward/BadgeUnlockModal.kt` (320 lines): Shared cross-feature `BadgeUnlockModal(badge, onDismiss)` reusing K-04's badge-tile visual tokens (`emblem`, `radius22`, `primarySubtle`, `primary`) with caller-controlled dismiss destination (supporting both A.3 K-06 completion next-step continuation and A.11 K-04 Achievements return).
  - `core/core-designsystem/src/commonMain/kotlin/com/noorheroes/core/designsystem/theme/NoorHeroesTheme.kt` (170 lines): Published `NoorHeroesTheme.rewards` on `core-designsystem`'s public export surface.
  - `core/core-ui/src/commonMain/kotlin/com/noorheroes/core/ui/component/Rewards.kt` (229 lines): Exported delegating overloads for `RewardUnlockAnimation(xp, noorPoints, activityType)` and `BadgeUnlockModal(badge, onDismiss)`.
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/achievements/components/BadgeUnlockModal.kt` (41 lines): Delegated K-04's `BadgeUnlockModal` to `core-designsystem`'s shared `BadgeUnlockModal` to eliminate duplication.
  - `core/core-designsystem/src/commonTest/kotlin/com/noorheroes/core/designsystem/reward/DeterministicRevealTest.kt` (189 lines) & `src/androidInstrumentedTest/kotlin/com/noorheroes/core/designsystem/reward/RewardAnimationPerformanceTest.kt` (85 lines): 9 deterministic-reveal, unknown-fallback, `<=2s` ceiling, reduced-motion, RTL snapshot, caller-controlled dismiss, and single-frame `<16ms` non-blocking performance tests (`0 violations` on `audit_k09.py`).

#### `Development_Blueprints/A11_Rewards_System/KMP/10-rewards-data-freshness-cross-screen-invalidation-engine.md`

##### 4. Objective
Implement a cache-freshness strategy so that navigating into any Rewards screen (Wallet Hub, Achievements, Missions) always triggers a fresh fetch when the local cache could plausibly be stale, rather than trusting an indefinitely-long cache lifetime.

##### 5. Business Requirements
- A child who checks in a habit (A.7), then immediately opens the Rewards tab, must see the updated balance, not a pre-award cached snapshot (a direct UX consequence of FR-13's "optimistic, reconciled" promise applying platform-wide, not just within the Rewards feature's own screens).
- No indefinite cache staleness: a simple "always refetch on screen-enter, with cache as instant-paint fallback while the fresh fetch completes" strategy is acceptable and matches the existing platform convention (remote-first, cache-as-fallback, not cache-first).

##### 11. KMP Requirements
- Every Rewards screen ViewModel triggers a remote fetch on screen-enter (not merely on first app launch), with the last-cached value painted instantly while that fetch resolves, then replaced once the fresh response arrives.
- No screen in this feature ever displays only a cached value with a live network path available and unused — cache is a *fallback for offline*, not a default *instead of* fetching.

##### 15. Validation
Integration test: simulate an award occurring "elsewhere" (direct fixture ledger insert, bypassing the app), then navigate into the Wallet Hub screen — assert the displayed balance reflects the fresh value within one screen-enter cycle, not the stale pre-award cache.

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Screen-enter refresh fails (offline) | Falls back to last-cached value with an offline indicator, consistent with each screen's already-documented offline state |
| Rapid repeated screen-enters (e.g., fast tab-switching) | Refresh calls are debounced/de-duplicated to avoid redundant network load |

##### 19. Offline First
Cache remains the offline fallback exactly as documented per-screen (K-02/K-04/K-06/K-07/K-08); this task only changes the *online* default from "cache-first" to "remote-first, cache-as-instant-paint."

##### 21. Localization
N/A.

##### 22. RTL
N/A.

##### 25. Security
No new sensitive data handling.

##### 27. Testing
- Unit: freshness-policy debounce/de-duplication logic.
- Integration: cross-screen staleness scenario per §15 (mandatory).

##### 31. Final Verification Checklist
- [x] Cross-screen staleness integration test passes (award-elsewhere → fresh Wallet Hub read)
- [x] Rapid repeated screen-enters debounced/de-duplicated
- [x] Offline fallback behavior unchanged (cache still serves when genuinely offline)
- [x] All Rewards screens' ViewModels apply the freshness policy consistently
- [x] KDoc documents the architectural rationale

##### 32. Verification Sign-Off Ledger (Executed 2026-09-26)
- **Status**: COMPLETED & VERIFIED (2026-09-26)
- **Author**: Sarvare Alam
- **Shared Freshness & Invalidation Policy**:
  - Implemented `RewardsFreshnessPolicy` (`core/rewards-client/src/commonMain/kotlin/com/noorheroes/core/rewards/client/data/RewardsFreshnessPolicy.kt`, 221 lines) providing remote-first reads, Room cache persistence/fallback, concurrent in-flight request de-duplication (`CompletableDeferred`), rapid screen-enter debounce (`DEFAULT_DEBOUNCE_WINDOW_MS = 500L`), `invalidateScope(scopeKey)`, `invalidateAllChildScopes(childId)`, and `invalidateAllFamilyScopes()`.
- **Repository Integration (All 5 K-01 Repositories)**:
  - Applied `RewardsFreshnessPolicy` and `refreshOnEnter(childId/familyId, forceRefresh)` across `WalletRepositoryImpl`, `MissionsRepositoryImpl`, `AchievementsRepositoryImpl`, `AchievementStoreRepositoryImpl`, and `FamilyBoardRepositoryImpl`, with cross-screen scope invalidation on `claimMission`, `purchaseStoreItem`, and `recordFamilyGoalContribution`, plus singleton DI binding in `RewardsClientModule`.
- **ViewModel & Screen-Enter Triggers (All 12 Rewards Screens & Sub-Screens)**:
  - Wired `onScreenEnter()` across all 12 screens/sub-screens in `:feature:feature-rewards`:
    1. `RewardsWalletHubScreen` (`WalletViewModel.onScreenEnter()`)
    2. `TransactionHistoryScreen` (`TransactionHistoryViewModel.onScreenEnter()`)
    3. `TransactionDetailScreen` (`TransactionHistoryViewModel.onScreenEnter()`)
    4. `AchievementsScreen` (`AchievementsViewModel.onScreenEnter()`)
    5. `BadgeDetailScreen` (`AchievementsViewModel.onScreenEnter()`)
    6. `AchievementLevelDetailScreen` (`AchievementsViewModel.onScreenEnter()`)
    7. `WeeklyChallengeDetailScreen` (`MissionsViewModel.onScreenEnter()`)
    8. `ArchivedChallengeScreen` (`MissionsViewModel.onScreenEnter()`)
    9. `SeasonalEventScreen` (`MissionsViewModel.onScreenEnter()`)
    10. `AchievementStoreScreen` (`AchievementStoreViewModel.onScreenEnter()`)
    11. `StoreItemDetailScreen` (`AchievementStoreViewModel.onScreenEnter()`)
    12. `FamilyBoardScreen` (`FamilyBoardViewModel.onScreenEnter()`)
- **18-Screen KMP UI Fidelity Audit (`Screens/Mobile App/Rewards`)**:
  - Verified 100% visual, structural, and data-model parity across `Rewards Wallet-01..09.png`, `Achievements-01..04.png`, `Achievement Store-01..04.png`, and `Family Board.png`.
- **Automated Verification**:
  - `:core:rewards-client:testAndroidHostTest` (`RewardsFreshnessPolicyTest`, 7 unit tests) — **PASSED**
  - `:feature:feature-rewards:testAndroidHostTest` (`CrossScreenFreshnessInvalidationTest`, 6 end-to-end tests covering §15 cross-screen staleness, rapid debounce, offline fallback, Achievements/Missions refresh, and cross-screen mutation invalidation) — **PASSED**
  - `recheck_zero_gaps.py` (`NoorHeroes/docs/rule.md` compliance across 141 files) — **0 violations**

#### `Development_Blueprints/A11_Rewards_System/KMP/11-rewards-cross-platform-analytics-instrumentation.md`

##### 4. Objective
Implement `RewardAnalytics` firing every event from PRD §1.19 via the existing `AnalyticsTracker` interface, tied to server-confirmed responses only, never optimistic UI state.

##### 5. Business Requirements
- Every event listed in PRD §1.19 is emitted from the correct screen/action.
- Events fire only after server confirmation (e.g., `wallet_viewed` on a confirmed wallet response, not on cache-only display) so analytics reflect real ledger outcomes.
- No PII in analytics payloads.

##### 11. KMP Requirements
- `RewardAnalytics` exposes one strongly-typed function per event (e.g., `fun walletViewed()`, `fun badgeUnlocked(badgeId: String)`, `fun achievementStorePurchaseCompleted(itemId: String, newBalance: Int)`) rather than free-form string/map construction at each call site — reduces the risk of a typo'd event name or missing parameter.
- Every function's implementation is called only from a code path that has already received a successful server response for the relevant action (never from an optimistic-update code path).

##### 15. Validation
Test asserting each `RewardAnalytics` function is only invoked from call sites gated behind a successful server response type (verified via a structural/lint-style check or a mocked-ViewModel test per event, per PRD §6.6 Android convention: "tied to actual server-confirmed responses (not optimistic UI state alone)").

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Analytics call fails silently (network-level, handled by `AnalyticsTracker` internally) | No impact on the calling screen's own success/error state — analytics failures are non-blocking |

##### 19. Offline First
Analytics events queued by `AnalyticsTracker`'s own existing offline-buffering behavior (if any) — this task does not introduce a separate queue.

##### 21. Localization
N/A (event names/params are not user-facing strings).

##### 22. RTL
N/A.

##### 25. Security
No PII in any event payload — verified per event during code review; masked/child-safe identifiers only where an identifier is needed at all.

##### 27. Testing
- Unit: server-confirmation-gating test per event category (mandatory).
- Integration: full flow per screen (K-02–K-08) firing the correct event at the correct trigger point.

##### 31. Final Verification Checklist
- [x] All §1.19 events implemented in `RewardAnalytics` (all 27 PRD §1.19 events exposed as strongly-typed functions + `ALL_PRD_1_19_EVENTS` set)
- [x] Every event verified to fire only post-server-confirmation (`isServerConfirmed == true`), never on optimistic state alone (`WalletEvent.ApplyOptimisticDelta`) or offline Room cache fallbacks (`isOffline == true`)
- [x] No PII present in any event payload (`RewardAnalytics.sanitizeNoPii` strips `child_id`, `family_id`, `parent_id`, `nickname`, `email`, `phone`, `dob`, etc.)
- [x] Each K-02–K-08 screen/ViewModel (`WalletViewModel`, `TransactionViewModel`, `AchievementsViewModel`, `ShareCardViewModel`, `MissionsViewModel`, `AchievementStoreViewModel`, `FamilyBoardViewModel`, and `RewardsModule.kt`) wired to the correct events
- [x] KDoc lists the full event taxonomy and architectural invariants

---

##### 32. Verification Sign-Off Ledger (2026-09-26)
- **Implementation & Test Suite**:
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/analytics/RewardAnalytics.kt`
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/di/RewardsModule.kt`
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/wallet/WalletViewModel.kt`
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/wallet/TransactionViewModel.kt`
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/achievements/AchievementsViewModel.kt`
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/missions/MissionsViewModel.kt`
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/store/AchievementStoreViewModel.kt`
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/family/FamilyBoardViewModel.kt`
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/sharing/ShareCardViewModel.kt`
  - `feature/feature-rewards/src/commonTest/kotlin/com/noorheroes/feature/rewards/analytics/RewardAnalyticsServerConfirmationTest.kt`
  - `feature/feature-rewards/src/commonTest/kotlin/com/noorheroes/feature/rewards/analytics/RewardAnalyticsViewModelGatingTest.kt`
- **Automated Verification**:
  - `python recheck_zero_gaps.py`: **0 violations across all 61 `:feature:feature-rewards` files / 146 git-status files** (`NoorHeroes/docs/rule.md` compliance).
  - `./gradlew :feature:feature-rewards:testAndroidHostTest`: **136/136 tests passing** (`BUILD SUCCESSFUL`).

#### `Development_Blueprints/A11_Rewards_System/KMP/12-rewards-localization-rtl-foundation.md`

##### 4. Objective
Ensure all reward-reason labels, badge/achievement names, mission/challenge copy, and store item descriptions are fully externalized (EN/HI/AR/UR) with correct RTL mirroring across K-02 through K-09.

##### 5. Business Requirements
- No hardcoded child-facing strings anywhere in the Rewards feature.
- RTL mirroring across Wallet, Achievements, Achievement Store, Family Board, and Challenge screens.
- Correct number/currency-style formatting for XP and Noor Heroes Points per locale.
- Pluralization rules correctly applied for transaction/badge counts.

##### 11. KMP Requirements
- `RewardsLocalizationCompletenessTest` scans every string-resource key referenced within the Rewards feature module and asserts a translation exists for all four supported locales — a structural completeness guard, not just a manual QA pass.
- Text-expansion tolerance verified in card/tile layouts (German/Arabic-length-variance-style testing pattern applied to Arabic/Urdu specifically) — no truncated or overlapping text in badge tiles, mission cards, or price tags.
- Arabic-Indic numeral handling for XP/points display, per-locale, where the platform's existing number-formatting convention specifies it.

##### 15. Validation
`RewardsLocalizationCompletenessTest` passes with zero missing translations across EN/HI/AR/UR (mandatory).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Missing translation key at runtime (should be prevented by the completeness test, but as a defensive fallback) | Falls back to the English string rather than rendering a raw key or blank text |

##### 19. Offline First
N/A (localization resources are bundled, not fetched).

##### 21. Localization
This entire sub-feature *is* the localization work: full EN/HI/AR/UR coverage across every Rewards screen (K-02–K-09).

##### 22. RTL
Full RTL verification pass across Wallet, Transaction History, Achievements, Achievement Store, Family Board, and Challenge screens — snapshot/UI tests per screen for the Arabic and Urdu locales.

##### 25. Security
N/A.

##### 27. Testing
- Unit: localization-completeness test (mandatory).
- Snapshot/UI: RTL rendering across all six listed screens, for both Arabic and Urdu.
- Text-expansion tolerance test on card/tile layouts.

##### 31. Final Verification Checklist
- [x] Zero hardcoded user-facing strings remain in the Rewards feature
- [x] Localization completeness test passes (all four locales, all keys)
- [x] RTL verified across Wallet, History, Achievements, Store, Family Board, Challenges
- [x] Text-expansion tolerance verified (no truncation/overlap)
- [x] Arabic-Indic numeral handling verified where applicable
- [x] Key-naming convention documented for future admin-authored content

---

##### 32. String-Resource Key Naming Convention & Verification Sign-Off Ledger (2026-09-26)

### A. Admin-Authored & Bundled Key Naming Convention (`RewardsKeyNamingConvention` — §28)
| Content Surface (Backend Source) | Key Pattern | Helper Method | Example Key |
| :--- | :--- | :--- | :--- |
| **Badge Title** (`B-04` / `B-10`) | `rewards_badge_<slug>` | `RewardsKeyNamingConvention.badgeTitleKey(slug)` | `rewards_badge_quran_star` |
| **Badge Description** (`B-04` / `B-10`) | `rewards_badge_<slug>_desc` | `RewardsKeyNamingConvention.badgeDescriptionKey(slug)` | `rewards_badge_quran_star_desc` |
| **Daily Mission Title** (`B-05` / `B-12`) | `rewards_mission_<slug>` | `RewardsKeyNamingConvention.missionTitleKey(slug)` | `rewards_mission_quran_lesson` |
| **Weekly / Seasonal Challenge** (`B-05` / `B-12`) | `rewards_challenge_<slug>_title` | `RewardsKeyNamingConvention.challengeTitleKey(slug)` | `rewards_challenge_ramadan_week_1_title` |
| **Store Item Title** (`B-06` / `B-11`) | `rewards_store_item_<slug>_title` | `RewardsKeyNamingConvention.storeItemTitleKey(slug)` | `rewards_store_item_golden_lantern_avatar_title` |
| **Store Item Description** (`B-06` / `B-11`) | `rewards_store_item_<slug>_desc` | `RewardsKeyNamingConvention.storeItemDescriptionKey(slug)` | `rewards_store_item_golden_lantern_avatar_desc` |
| **Ledger Reason Label** (`B-02`) | `rewards_reason_<reason_type>` | `RewardsKeyNamingConvention.ledgerReasonKey(type)` | `rewards_reason_surah_completed` |
| **Accessibility Description** (`K-02`–`K-09`) | `cd_<surface>_<element>` | `RewardsKeyNamingConvention.contentDescriptionKey(s, e)` | `cd_store_item_card` |

### B. Implementation & Test Files
- `core/core-common/src/commonMain/composeResources/values/strings_rewards.xml` (330 keys)
- `core/core-common/src/commonMain/composeResources/values-hi/strings_rewards.xml` (330 keys)
- `core/core-common/src/commonMain/composeResources/values-ar/strings_rewards.xml` (330 keys)
- `core/core-common/src/commonMain/composeResources/values-ur/strings_rewards.xml` (330 keys)
- `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/localization/RewardsLocalizationFoundation.kt` (integrates `MinorUnitsFormatter.formatPoints` from `core-common/format` & `LocalizationFormatter`)
- `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/wallet/TransactionLabelMapper.kt` (reuses `RewardsLocalizationFoundation` numeral and locale resolution per `K-12 §7`)
- `feature/feature-rewards/src/commonTest/kotlin/com/noorheroes/feature/rewards/localization/RewardsLocalizationCompletenessTest.kt` (8 unit & integration tests)
- `feature/feature-rewards/src/androidHostTest/kotlin/com/noorheroes/feature/rewards/localization/RewardsResourceXmlFilesystemCompletenessTest.kt` (3 structural XML & source-code AST tests)
- Updated `DailyMissionsCard.kt`, `RecentActivitySection.kt`, `TransactionDetailCard.kt`, `TransactionHistoryScreen.kt`, `DailyMissionListSection.kt`, `SeasonalEventScreen.kt`, `WeeklyChallengeCard.kt`, `WeeklyChallengeDetailScreen.kt`, `BadgeUnlockModal.kt` (`K-09`), and `RewardUnlockAnimation.kt` (`K-09`) to replace all remaining inline formatted strings with `Res.string.*` resource keys.
- **Automated Verification**:
  - `python recheck_zero_gaps.py`: **`0 violations` across 150 git-status files** (`NoorHeroes/docs/rule.md`).
  - `./gradlew :feature:feature-rewards:testAndroidHostTest`: **`147 / 147` tests passing (`BUILD SUCCESSFUL`)**.
  - `./gradlew :core:core-designsystem:testAndroidHostTest`: **`BUILD SUCCESSFUL`**.

## A12 — Feature_A12_Avatar_System

PRD: `PRD_Documents/Child App (1-12)/Feature_A12_Avatar_System.md`

Coverage: 12 mandatory FR records; all preserved verbatim below. Feature has 12 inventory records including components/states. Components and states must not inflate independently executed screen count.

### Existing screenshot candidates

- `Screens/Mobile App/Avatar/Avatar-01.png` — visually inspected
- `Screens/Mobile App/Avatar/Avatar-02.png` — inventoried only
- `Screens/Mobile App/Avatar/Avatar-03.png` — inventoried only
- `Screens/Mobile App/Avatar/Evolution.png` — inventoried only
- `Screens/Mobile App/Avatar/Locked Item-01.png` — inventoried only
- `Screens/Mobile App/Avatar/Locked Item-02.png` — inventoried only

### Complete normative functional coverage

### 1.7 Functional Requirements

**FR-1** Avatar screen sections: 3D avatar preview, owned-items grid (organized by slot: outfit/glow/accessory), locked-item teasers showing unlock criteria (source: screen catalog "Avatar — UI Sections: 3D avatar preview, owned-items grid (outfits, glow states), locked-item teasers with unlock criteria").
**FR-2** User actions: equip/unequip an owned item, preview a locked item (a non-committal visual preview without actually equipping it), and navigate directly to the activity that would unlock a given locked item (source: screen catalog "User Actions: Equip/unequip an item, preview a locked item, navigate to the activity that unlocks it").
**FR-3** Avatar items are sourced **only** from the admin-managed `avatar_items` catalog — there is no user-upload path anywhere in the app for avatar customization (source: navigation table, "Items are sourced only from `AvatarItems` catalog; no user uploads" — a hard, zero-exception architectural rule).
**FR-4** Every `avatar_item`'s `unlock_rule` must map to an existing badge, level threshold, or habit milestone — admin tooling must reject any attempt to define an arbitrary or opaque unlock condition with no underlying verifiable criteria (source: Admin module Validation Rules — restated here as the rule this feature's read/evaluation path depends on).
**FR-5** Items are never sold for real money in child mode — equivalent to and consistent with A.11 FR-1's Noor-Heroes-Points-only economy; this feature's equip/unlock layer has no payment-related code path at all (source: Admin module Validation Rules).
**FR-6** Equipping an item is immediate (optimistic client update, server-confirmed) and instantly reflected in the avatar preview (source: Avatar Flow diagram, "POST equip → Avatar preview updates").
**FR-7** Locked items display their specific unlock criteria (e.g., "7-day streak") rather than a generic lock icon with no explanation, consistent with the platform's general locked-content transparency principle established in A.3/A.5.
**FR-8** When a child's activity causes a locked item's criteria to become met, the item is **auto-unlocked** and a notification is sent — the child is never required to manually "claim" an avatar-item unlock the way they might claim a mission/challenge reward in A.11 (source: Avatar Flow diagram, "Criteria met later? → Yes → Item auto-unlocked + notification").
**FR-9** Character Evolution: avatars and Noor companions evolve through learning-based progression — Quran skills, story morals, kindness actions, and habit consistency unlock new outfits, glow states, and story-world abilities (source: "Character Evolution" feature card — "Avatars and Noor companions evolve through learning-based progression... unlock new outfits, glow states, and story-world abilities").
**FR-10** Retiring an `avatar_item` from the catalog (Admin "Delete" action) never revokes it from children who already own it — retired items remain fully equippable for existing owners, only new acquisition is prevented (source: Admin module CRUD Operations, "Retire item (owned items remain equippable)").
**FR-11** Avatar base selection happens at child-profile creation (A.1) from the `avatars` base library; this feature does not re-implement avatar-base selection, only the items/customization layered on top of the chosen base.
**FR-12** All avatar assets (base avatars and every `avatar_item`) must pass a modesty/age-appropriateness review by the same content governance pipeline used for other content types — "it's just a cosmetic" is never an exemption from this review.

### Ordered source inventory

### 1.18 Screen Inventory (Complete — Zero Missing)

| # | Screen / Component | Type | Entry Points | Exit Points |
|---|---|---|---|---|
| 1 | Avatar Screen (3D preview + owned grid + locked teasers) | Primary | Rewards Hub (A.11), Profile tab avatar thumbnail | Item Detail, Locked Item Detail, relevant unlocking feature |
| 2 | 3D Avatar Preview (component) | Component | Avatar Screen | N/A |
| 3 | Owned-Items Grid, grouped by slot (outfit/glow/accessory) | Component | Avatar Screen | Item Detail |
| 4 | Item Detail (owned) — Equip/Unequip | Screen/Modal | Owned-Items Grid | Avatar Screen (preview updated) |
| 5 | Locked-Item Teaser (component) | Component | Avatar Screen | Locked Item Detail |
| 6 | Locked Item Detail — Unlock Criteria View | Screen/Modal | Locked-Item Teaser | "Go to activity" deep link, or dismiss |
| 7 | Locked-Item Non-Committal Preview | Screen/Modal variant | Locked Item Detail "Preview" action | Dismiss (no persistent change) |
| 8 | Auto-Unlock Celebration Notification (in-app banner/modal) | Component | Server-evaluated criteria-met event | Dismiss → Avatar Screen (item now owned) |
| 9 | Character Evolution Milestone Reveal | Modal | Noor companion/avatar crossing an evolution threshold | Dismiss → returns to current screen (e.g., Home) |
| 10 | Asset-Load-Failure Placeholder (per grid item) | Component | Owned-Items Grid, asset failure | Retry |
| 11 | Locked Item — "Currently Unavailable to Unlock" State | Component variant | Locked Item Detail, deprecated unlock-rule reference | Dismiss |
| 12 | Offline Avatar State | Screen variant | Avatar Screen, no connectivity | N/A (fully functional from cache except new-unlock evaluation) |

### Exact mobile UX and behavior sources

### 1.9 Acceptance Criteria

- Given a child opens the Avatar screen, when it renders, then they see their 3D preview, an owned-items grid organized by slot, and locked-item teasers each showing specific unlock criteria.
- Given a child taps an owned item, when they equip it, then the avatar preview updates immediately and the change persists across app sessions.
- Given a child taps a locked item, when they view its detail, then they see the specific unlock criteria and a direct navigation link to the relevant unlocking activity.
- Given a child's activity causes a locked item's criteria to be met, when this is evaluated server-side, then the item auto-unlocks and a notification is sent — no manual claim action is required.
- Given an Admin retires an `avatar_item` from the catalog, when a child who already owns it opens their Avatar screen, then the item remains fully visible and equippable.
- Given an Admin attempts to create an `avatar_item` with an unlock rule that doesn't reference an existing badge/level/habit-milestone, when they submit, then the system rejects it with a clear validation error.
- Given a parent or child looks for any avatar-customization path involving a photo upload or real-money purchase, when they search the entire Avatar screen and flow, then no such path exists.

### 1.10 Edge Cases

1. A child equips an item from a slot (e.g., "outfit"), then later that specific item is retired by Admin (FR-10) → the item remains equipped and visible exactly as it was; retirement only prevents *new* acquisition by other children, never affects an existing owner's equipped state.
2. Two avatar items from different slots have a default-equipped state when a child's profile is first created → the system must have a well-defined default outfit/glow/accessory combination at child-creation time (set during A.1's Add Child avatar selection) so the Avatar screen never renders an avatar with an undefined or null equipped state in any slot.
3. A child's age-band changes (birthday rollover) and a previously-displayed avatar item was only ever intended for a younger age band visually (e.g., a more babyish design) → items are not retroactively un-equipped based on age-band changes (a child keeps what they've earned and equipped), though the *available-to-unlock* catalog going forward may reasonably skew toward age-appropriate new items via the standard age-banded content filtering already used elsewhere in the platform.
3. *(renumbered)* A locked item's unlock criteria references a badge that has since been deprecated/retired by Admin (an unusual content-lifecycle edge case) → the item's locked-teaser state should gracefully indicate "currently unavailable to unlock" rather than show a broken/dangling reference to a non-existent badge, and should not block rendering of the rest of the Avatar screen.
4. A child rapidly taps "equip" on multiple different items within the same slot in quick succession → idempotent, last-tap-wins handling ensures the final equipped state matches the child's actual last intended selection, without a race condition leaving an inconsistent or flickering state.
5. A child previews a locked item (FR-2's non-committal preview action) and then closes the app without equipping anything → the preview action has zero persistent side effects; on reopening, the avatar shows whatever was actually equipped before the preview, not the previewed item.
6. An item's `unlock_rule` references a habit milestone (e.g., "30-day Quran-reading streak") and that streak is later broken (per A.7's streak state machine transitioning to `Broken`) after the item was already unlocked → consistent with the platform's general "badges/unlocks are sticky once earned" principle (A.6/A.11), the avatar item remains unlocked permanently; a broken streak never retroactively re-locks a previously-earned item.
7. Two siblings share a device; switching from Child A to Child B mid-session → the Avatar screen must fully reset to Child B's own avatar base, owned items, and equipped state — zero visual or data carryover from Child A's session (consistent with the platform-wide multi-child session-isolation rule).
8. A child's Noor companion "evolves" (Character Evolution, FR-9) crossing a visible milestone while the child is actively on the Home screen looking at the companion → the evolution visual update should apply gracefully (e.g., on next Home load or via a graceful in-place transition), never an abrupt jarring change mid-interaction that could startle a young child.
9. An `avatar_item`'s asset fails to load (CDN/media issue) → the owned-items grid shows a graceful placeholder/retry state for that specific item rather than a broken image or a crash, and the 3D preview falls back to the last successfully-rendered equipped state rather than showing a broken avatar.
10. A child attempts to equip an item they do not actually own (e.g., via a tampered/replayed client request referencing a locked item's ID) → the server validates ownership at equip time and rejects the request; the locked item remains locked regardless of the client-side request.
11. An Admin updates an existing `avatar_item`'s `unlock_rule` (e.g., changing the streak length required) after some children have already unlocked it under the old rule → consistent with the platform's non-retroactivity principle (A.9 Edge Case 9), children who already unlocked it keep it; the new rule applies only to children who haven't yet unlocked it going forward.

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Equip request fails (network) | Optimistic local UI update shown immediately; retried via background sync; reconciled with server state on next successful response |
| Avatar item asset fails to load | Graceful placeholder/retry for that specific grid item; 3D preview falls back to last successfully-rendered state (Edge Case 9) |
| Equip request for an unowned item (tampered/stale client state) | Server rejects with a clear "not yet unlocked" response; client re-syncs ownership state |
| Locked item's unlock_rule references a deprecated badge/level | Locked-teaser shows "currently unavailable to unlock" gracefully (Edge Case 3) |
| Auto-unlock notification fails to deliver | The unlock itself (the `child_inventory` grant) is unaffected; the child will simply see the newly-unlocked item next time they open the Avatar screen even if the notification was missed |

### 1.12 Empty States
- New child, default avatar/items only → owned-items grid shows the default set with no "empty" framing needed (every child starts with at least a base equipped look); locked-item teasers populate normally from the catalog.

### 1.13 Loading States
- Avatar screen: skeleton 3D-preview placeholder + skeleton items-grid shimmer while loading.

### 1.14 Offline States
- Last-synced avatar state (owned items, equipped state) renders fully offline; equip actions taken offline queue and sync on reconnect, consistent with the platform's offline-first equip pattern (FR-6).
- Locked-item criteria display uses cached catalog data; auto-unlock evaluation itself requires connectivity (it's a server-side process) but the child is never blocked from viewing/equipping their already-owned items offline.

### 1.15 Permission States
- No new runtime permissions; explicitly **no camera/photo-library permission is ever requested by this feature**, since there is no upload path (FR-3) — this absence is itself a deliberate, testable property.

### 1.16 User Flow (Narrative)

Child opens the Avatar screen (from Rewards or the Profile tab's avatar thumbnail) → views their 3D preview and owned-items grid → equips/unequips items, seeing instant preview updates → browses locked-item teasers, optionally taps one to preview it or to navigate directly to the activity that would unlock it → continues using the app normally; whenever an activity elsewhere in the app causes a locked item's criteria to be met, the item auto-unlocks server-side and the child receives a notification, discoverable next time they open the Avatar screen (now showing the item as owned) or immediately via the notification's deep link.

### 2.1 Avatar-Specific Design System Extensions

- **3D Preview Lighting/Staging:** A consistent, warm, soft-lit staging environment (a subtle radial glow, no busy background) frames the 3D avatar regardless of which outfit/glow is equipped, keeping focus on the character itself.
- **Modesty-by-Default Asset Guidelines:** Every outfit asset (by content-authoring guideline, enforced via the admin review pipeline per FR-12) adheres to modest, age-appropriate design — there is no "swimwear," overly form-fitting, or otherwise immodest item category in the catalog by design, consistent with the platform's Islamic values orientation.
- **Locked-Item Visual Language:** A soft greyscale/desaturated silhouette (never a harsh blackout or a "?" mystery-box treatment, which could imply gacha-style randomness contrary to the platform's anti-loot-box principle) with the unlock-criteria text always visible beneath, not hidden behind an additional tap.
- **Character Evolution Visual Language:** Evolution milestones use a gentle, growth-themed transition (e.g., a soft glow bloom, consistent with A.7's Noor Garden growth metaphor) rather than an abrupt "transform" effect — reinforcing the "gradual real progress" framing over a sudden game-like power-up.

### 2.2 Screen-Level Design Requirements (Key Screens)

#### Screen: Avatar Screen

- **Purpose:** Let the child view, customize, and understand the progression path of their personal avatar.
- **Components:** Large centered 3D preview (rotatable via simple swipe/drag gesture, with a non-gesture rotation-arrow alternative for accessibility), a tabbed or segmented control for slot categories (Outfits/Glow/Accessories), a scrollable grid of items per slot showing owned (tappable, equip-state-indicated) and locked (desaturated, criteria-labeled) items together in a unified browsing experience.
- **States:** Default, Loading (skeleton), Item-equip-in-progress (brief optimistic transition), Offline (cached state), Asset-load-failure (per-item placeholder).
- **Accessibility:** 3D preview has a text-description fallback ("Currently wearing: Garden Explorer outfit, Golden Glow"); rotation gesture has a button-based alternative; locked-item criteria text always present and screen-reader-readable, never icon-only.
- **Responsive Rules:** Single-column preview-on-top/grid-below on mobile; tablet may show preview and grid side-by-side.

#### Screen: Locked Item Detail

- **Purpose:** Clearly communicate what's needed to unlock a specific item and offer a direct path there.
- **Components:** Item illustration (desaturated/locked styling), unlock criteria text (specific, e.g., "Complete a 7-day Quran reading streak"), a "Preview" action (non-committal try-on), and a "Go to [Activity]" primary action deep-linking to the relevant feature.
- **States:** Default, Criteria-recently-progressed (an optional subtle "you're getting close!" framing if progress data is available and meaningful to surface), Unavailable (deprecated unlock-rule reference, Edge Case 3).

### 2.3 Tab Structure

Avatar is reachable from Rewards (Tab 4) and from the Profile tab's (Tab 5) avatar thumbnail — not its own bottom-nav tab. Click mapping:

| Click Target | Destination | API Called | Analytics Event | Permission Check | Error Handling |
|---|---|---|---|---|---|
| Rewards Hub "Avatar" entry / Profile avatar thumbnail | Avatar Screen | `GET /v1/children/{id}/inventory` | `avatar_screen_viewed` | None | Cached fallback |
| Owned item tap | Item Detail / direct equip | `POST /v1/children/{id}/inventory/{itemId}/equip` | `avatar_item_equipped` | Ownership check (server-side) | Optimistic + retry |
| Locked item tap | Locked Item Detail | None (client-rendered from cached catalog criteria) | `avatar_locked_item_viewed` | None | "Unavailable" fallback if criteria reference is stale |
| Locked item "Go to [Activity]" | Relevant feature screen (deep link) | N/A | `avatar_locked_item_unlock_activity_navigated` | None | Standard deep-link fallback |

### 2.4 Wireframe Description (Composite)

A single, immersive screen with the 3D preview dominating the upper portion and a segmented, scrollable item grid below — consistent with the platform's general "hero visual + browsable grid" pattern shared with A.3's Story Detail (cover + episode list) and A.5's Surah Learning (companion presence + ayah list).

### 2.5 Screen Image Generation Prompts

**Screen: Avatar Screen**
- *Prompt 1 (English):* "Mobile app avatar customization screen UI mockup for a children's app. Warm off-white background. Top half shows a large centered 3D-style friendly character illustration (a soft, rounded, child-safe abstract character wearing a simple modest outfit with a gentle golden glow aura, NOT a realistic human figure) staged on a soft circular glowing platform with subtle radial light. Below, a segmented tab control labeled 'Outfits / Glow / Accessories', and beneath that a scrollable grid of rounded square item tiles -- some colorful and clearly owned, some desaturated grey silhouettes with a small text label underneath reading something like '7-day streak to unlock'. Warm teal and gold accents, rounded corners, soft shadows, joyful and magical aesthetic, no realistic human faces, bottom navigation visible."
- *Prompt 2 (Arabic RTL):* "نفس شاشة تخصيص الصورة الرمزية لتطبيق أطفال، بتخطيط من اليمين إلى اليسار بالكامل. خلفية بيج فاتح دافئ. النصف العلوي يعرض شخصية ودودة كبيرة بأسلوب ثلاثي الأبعاد في المنتصف (شخصية تجريدية ناعمة ومستديرة وآمنة للأطفال ترتدي زيًا بسيطًا ومحتشمًا مع هالة توهج ذهبية لطيفة، ليست شخصية بشرية واقعية) موضوعة على منصة دائرية متوهجة ناعمة بإضاءة شعاعية خفيفة. أسفل ذلك عنصر تحكم مقسم بعنوان 'الأزياء / التوهج / الإكسسوارات'، وتحته شبكة قابلة للتمرير من بطاقات عناصر مربعة مستديرة الزوايا — بعضها ملون وواضح أنه مملوك، وبعضها ظل رمادي غير مشبع مع تسمية نصية صغيرة أسفله تقول مثلاً 'متتالية 7 أيام للفتح'. لمسات فيروزية وذهبية دافئة، زوايا دائرية، ظلال خفيفة، طابع مرح وسحري، بدون وجوه بشرية واقعية، شريط تنقل سفلي ظاهر."

**Screen: Character Evolution Milestone Reveal**
- *Prompt 1 (English):* "Mobile app full-screen celebratory modal UI mockup for a children's app character evolution moment. Centered soft abstract companion character (a friendly lantern or crescent-moon-shaped creature, not a human figure) shown mid-transformation with a gentle blooming golden-light particle effect radiating outward, suggesting graceful growth rather than a sudden power-up. Warm gradient background transitioning from soft teal to warm gold. Below the character, a short celebratory text line about the milestone reached, and a single rounded 'Continue' button. No realistic human faces, no aggressive flash/strobe effects, calm-but-joyful magical mood, soft particle glow, rounded shapes."
- *Prompt 2 (Arabic RTL):* "نفس النافذة الاحتفالية بملء الشاشة لتطبيق أطفال، لحظة تطور الشخصية، بتخطيط من اليمين إلى اليسار. شخصية رفيق مجردة ناعمة في المنتصف (مخلوق ودود على شكل فانوس أو هلال، ليست شخصية بشرية) تظهر في وسط عملية تحول مع تأثير جزيئات ضوء ذهبي متوهج ينتشر للخارج بلطف، يشير إلى نمو رشيق وليس قوة مفاجئة. خلفية متدرجة دافئة تتحول من فيروزي ناعم إلى ذهبي دافئ. تحت الشخصية سطر نصي احتفالي قصير عن الإنجاز الذي تم الوصول إليه، وزر مستدير واحد بعنوان 'استمرار'. بدون وجوه بشرية واقعية، بدون تأثيرات وميض أو ومضات عدوانية، طابع سحري هادئ لكن مفرح، توهج جزيئات ناعم، أشكال مستديرة."

---

### 6.1 Technical Requirements
Kotlin, Jetpack Compose, MVVM, Clean Architecture, module `:feature:avatar`, depends on `:core:design-system`, `:core:network`, `:core:offline-cache`, and a 3D-rendering capability (e.g., Filament or a lightweight glTF-based renderer wrapped in `AndroidView`/Compose interop) optimized for low-end device performance per the platform's general performance commitment.

### 6.2 Screen Mapping
`AvatarScreen` Composable hosts the 3D preview (via the rendering engine's view wrapped in Compose) plus the segmented owned/locked items grid; `AvatarViewModel` exposes `StateFlow<AvatarUiState>` covering both.

### 6.3 Navigation Flow
Reachable from Rewards Hub and the Profile tab's avatar thumbnail; Locked Item Detail and its "Go to Activity" action deep-link into the relevant other feature module (e.g., `noorheroes://habits` for a streak-based unlock).

### 6.4 State Management
`AvatarViewModel`'s equip action is optimistic (immediately updates the local equipped state and re-renders the 3D preview) then reconciled against the server response — consistent with the platform's standard optimistic-update pattern (A.2/A.7). Locked-item criteria descriptions are rendered directly from the server's pre-resolved `unlock_rule_description` string; the client never parses raw criteria JSON.

### 6.5 API Mapping
`InventoryRepository.getInventory()` → `GET /v1/children/{id}/inventory`; `InventoryRepository.equip()` → `POST /v1/children/{id}/inventory/{itemId}/equip`.

### 6.6 Analytics Mapping
`AvatarAnalytics` fires events per §1.19; `avatar_item_auto_unlocked` is fired client-side upon detecting a newly-owned item in a fresh `GET /v1/children/{id}/inventory` response compared to the previously-cached state (a diffing approach, since the unlock itself happens server-side asynchronously).

### 6.7 Offline Support
Last-synced inventory state (Room-cached) renders fully offline; equip/unequip actions queue in a local outbox and sync via WorkManager on reconnect, consistent with the platform's standard offline-action pattern.

### 6.8 Deep Linking
`noorheroes://avatar`, `noorheroes://avatar/item/{itemId}` (for a notification deep link landing directly on a newly-unlocked item's detail).

### 6.9 Push Notifications
Landing target for the auto-unlock notification (owned by the Notifications feature) and for Character Evolution milestone alerts.

### 6.10 Testing Strategy
- Unit: `AvatarViewModel`'s optimistic-equip/reconcile logic; one-equipped-per-slot client-side state consistency (mirroring backend's invariant for fast local UX, though the server remains authoritative).
- UI tests: Locked-item teaser never renders a raw/unparsed JSON criteria string (always the server-resolved human-readable description); 3D preview accessibility fallback text renders correctly for the current equipped state.
- Integration: full equip → preview-update → app-restart-persists flow; offline equip → reconnect → sync flow; auto-unlock-detection-via-diffing flow against a mocked server response sequence.

---

### 13.1 Test Plan Summary
Coverage spans: ownership re-validation, one-equipped-per-slot invariant, idempotent criteria-based auto-unlock, retired-item-remains-equippable guarantee, and all 12 edge cases from §1.10.

### 13.2 Test Cases — Happy Path
1. Child equips an owned outfit and a glow effect simultaneously (different slots) → both apply to the preview correctly, persisting across app restart.
2. Child completes a 7-day Quran streak whose criteria matches a locked avatar item → the item auto-unlocks server-side, a notification is sent, and the item appears owned next time the Avatar screen loads.
3. Admin retires an item that a child already owns → the child's Avatar screen still shows it as owned and fully equippable.

### 13.3 Edge Cases
All edge cases from §1.10 (12 items, noting the duplicate "3" numbering in the source list corresponds to two distinct scenarios both covered as discrete test cases).

### 13.4 Negative Cases
- Attempt to equip an item_id the requesting child does not own → `403`.
- Equip two different outfits in rapid succession → exactly one ends up equipped in that slot, never both.
- Attempt to create an avatar_item via direct Admin API call with an unlock_rule referencing a fake badge_id → rejected.
- Replay the same badge_unlocked Kafka event twice → exactly one `child_inventory` row created, exactly one notification sent.

### 13.5 Regression Cases
Full Avatar System suite re-run on every release touching `:feature:avatar`, the Avatar & Inventory Service, the Unlock Evaluation Engine, or any upstream event producer (A.7/A.9/A.11).

### 13.6 Automation Cases
End-to-end: full equip/unequip flow across multiple slots; criteria-based auto-unlock triggered via a fixture badge event through to Avatar-screen reflection; offline equip → reconnect → sync flow; retired-item-remains-equippable regression test (run standingly, not just at initial launch, given its importance to the platform's trust commitments).

---

### Corresponding KMP blueprint requirements

#### `Development_Blueprints/A12_Avatar_System/KMP/01-avatar-screen-3d-preview-experience.md`

##### 4. Objective
Build the `AvatarScreen` Composable and `AvatarViewModel` rendering the 3D preview, owned-items grid, and locked-item teasers with full loading/offline/asset-failure states, backing FR-1, NFR Performance (screen load p95 < 1s), and Edge Cases 2, 7, 9.

##### 5. Business Requirements
- Screen renders 3D avatar preview, owned-items grid (grouped by slot), and locked-item teasers in one unified browsing surface (FR-1).
- A new child always has a well-defined default equipped state in every slot — never a null/undefined slot render (Edge Case 2).
- Full reset on multi-child session switch — zero visual/data carryover between siblings sharing a device (Edge Case 7).
- Per-item asset load failure shows a graceful placeholder/retry, never a broken image or crash; 3D preview falls back to the last successfully-rendered equipped state (Edge Case 9).
- 3D preview has a screen-reader text-description fallback describing the currently-equipped look (NFR Accessibility).
- Screen load p95 < 1s on low-end Android (NFR Performance).

##### 11. KMP Requirements
- `AvatarViewModel` exposes `StateFlow<AvatarUiState>` covering: `avatarBase`, `ownedItemsBySlot: Map<Slot, List<OwnedItem>>`, `lockedItems: List<LockedItem>`, `equippedBySlot: Map<Slot, ItemId>`, `loadState` (Loading/Default/Offline/Error).
- Default-equipped-state guarantee: `AvatarUiState` initialization never renders a slot with a null/undefined equipped value — if the backend response is somehow incomplete, the ViewModel falls back to a documented default rather than an undefined render (defensive client-side guard even though B-01 guarantees this server-side).
- 3D preview rotation via simple swipe/drag gesture on `Avatar3DRenderer`'s Compose wrapper, with a non-gesture rotation-arrow button alternative for accessibility.
- Per-item asset load failure: `Avatar3DRenderer` and grid item composables catch load failures independently, each falling back to its own placeholder/retry state without affecting sibling items or the overall screen.
- 3D preview accessibility fallback: a `contentDescription`/semantics property describing the current equipped combination in plain text (e.g., "Currently wearing: Garden Explorer outfit, Golden Glow").
- Tablet responsive layout: preview and grid side-by-side; mobile: preview-on-top/grid-below.
- Segmented/tabbed control for slot categories (Outfits/Glow/Accessories).

##### 15. Validation
Unit test asserting `AvatarUiState`'s default-equipped-state fallback triggers correctly when fed a fixture response missing an equipped item in one slot (defensive-guard test, since this should be structurally impossible per B-01 but must be verified client-side too, per Edge Case 2's "never render an undefined equipped state" requirement).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Network failure on inventory load | Show cached `avatar_inventory_cache` with a small persistent offline indicator |
| Individual item asset fails to load | Per-item placeholder/retry state; rest of grid unaffected |
| 3D preview asset fails to load | Falls back to last successfully-rendered equipped state, never a broken/blank render |
| New child, no prior cache | Render default-equipped state from the fresh inventory response, no "empty" framing needed (every child starts with a base equipped look) |

##### 19. Offline First
Last-synced inventory (owned items, equipped state) renders fully offline from `avatar_inventory_cache`; locked-item criteria display uses cached catalog data too (auto-unlock evaluation itself requires connectivity, but viewing/equipping owned items never blocks offline).

##### 21. Localization
Item/base names and locked-item criteria descriptions resolved via backend-provided translation keys or pre-resolved strings (English, Hindi, Arabic, Urdu) — no hardcoded user-facing strings.

##### 22. RTL
Segmented slot-category control and grid layout mirror correctly for RTL locales (Arabic/Urdu); verified via a dedicated RTL layout test. 3D preview staging itself (a centered radial-glow composition) is inherently direction-neutral.

##### 25. Security
No new sensitive data handling at this layer.

##### 27. Testing
- Unit: `AvatarViewModel`'s default-equipped-state fallback guard.
- Unit: multi-child session-switch triggers full state reset (no carryover from a previous child's `AvatarUiState`).
- UI: 3D preview accessibility fallback text renders and updates correctly for the current equipped state.
- UI: per-item asset-load-failure placeholder renders without affecting sibling grid items.
- UI: offline indicator renders when cached data is served without connectivity.
- Accessibility: rotation-arrow alternative reachable and functional without gesture input.

##### 31. Final Verification Checklist
- [ ] `feature-avatar`/`feature-avatar-domain` modules scaffolded and DI-wired
- [ ] `Avatar3DRenderer` abstraction renders on both Android and iOS
- [ ] Default-equipped-state guard verified (never an undefined slot render)
- [ ] Multi-child session switch triggers full state reset (no carryover)
- [ ] Per-item asset-load-failure isolated to that item, 3D preview falls back gracefully
- [ ] 3D preview accessibility fallback text correct and updates with equipped state
- [ ] Rotation-arrow non-gesture alternative functional
- [ ] Localization (EN/HI/AR/UR) and RTL verified
- [ ] Analytics event wired via `AnalyticsTracker`
- [ ] Screen load performance meets p95 < 1s budget on low-end Android target

#### `Development_Blueprints/A12_Avatar_System/KMP/02-owned-items-grid-equip-interaction.md`

##### 4. Objective
Implement `AvatarViewModel`'s `equip()`/`unequip()` actions as optimistic, locally-slot-invariant, server-reconciled operations, backing FR-2, FR-6, NFR Performance (equip latency p95 < 300ms), and Edge Case 4.

##### 5. Business Requirements
- Equip is optimistic: the avatar preview updates immediately on tap, before the server responds (FR-6).
- One-equipped-item-per-slot is enforced in the client's local state model as well as the server's, for instant correct local UX (mirroring B-01's server-side invariant).
- Server rejection (e.g., `403 ITEM_NOT_OWNED` from a stale client state) rolls back the optimistic change and shows a brief non-alarming "couldn't equip that" message — never leaves the UI in an incorrect optimistic state.
- Rapid repeated taps across items in the same slot resolve to a stable last-tap-wins state, without flicker or an inconsistent intermediate render (Edge Case 4).
- Equip action tap-to-local-update latency budget < 300ms (server-confirmed round trip; local optimistic update itself is near-instant).

##### 11. KMP Requirements
- `AvatarViewModel.equip(itemId)`: immediately updates `AvatarUiState.equippedBySlot[slot] = itemId` (optimistic), immediately re-renders the 3D preview via K-01's `Avatar3DRenderer`, then calls `InventoryRepository.equip()`.
- On success response, no visible change (already optimistically correct); on failure (e.g., `403 ITEM_NOT_OWNED`), roll back `equippedBySlot[slot]` to the previously-equipped item and surface a brief, non-alarming inline message.
- Local one-equipped-per-slot enforcement: `equippedBySlot` is a `Map<Slot, ItemId>` by construction — assigning a new value for a slot key inherently replaces the prior value, structurally preventing two simultaneously-equipped items in one slot at the type level.
- Rapid-tap handling: use a `Channel`/debounced coroutine sequencing per slot so that only the last tap's request is authoritative for that slot's final reconciliation, while still sending each request (idempotent server-side per B-01) — avoid a naive "cancel-in-flight" approach that could drop a legitimately final request.
- `unequip(itemId)` mirrors the same optimistic/reconcile pattern, clearing `equippedBySlot[slot]` to a "nothing equipped in this slot" sentinel only where the PRD's underlying data model allows an empty slot (cross-reference B-01/Edge Case 2's default-equipped-state guarantee — in practice every slot always has *some* default item equipped, so `unequip` should be understood as "return to default," not "leave empty," unless product confirms otherwise; treat this as a flagged assumption pending explicit product confirmation rather than guessed silently).

##### 15. Validation
Unit test simulating a server rejection (`403 ITEM_NOT_OWNED`) and asserting the UI state rolls back to the previously-equipped item, never left in the optimistic (incorrect) state (mandatory, per PRD §7 Android prompt item 1). Unit test asserting the local `equippedBySlot` map never holds two items claiming the same slot under any sequence of rapid taps (mandatory, per PRD §7 Android prompt item 2).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Equip request rejected (`403 ITEM_NOT_OWNED`) | Roll back optimistic state to previously-equipped item; brief "couldn't equip that" message |
| Network failure during equip | Optimistic state remains pending; retried via K-06's outbox on reconnect (delegated, not re-implemented here) |
| Rapid repeated taps in the same slot | Last tap's target becomes the final authoritative local state; all requests sent, server's idempotent handling (B-01) resolves the true final state |
| Unequip on an item not currently equipped | No-op locally; server call still made for consistency, idempotent response expected |

##### 19. Offline First
This sub-feature's core reconcile logic assumes connectivity; offline equip actions are captured and queued by K-06's outbox, with this sub-feature's optimistic-update layer providing the immediate visual feedback regardless of connectivity state.

##### 21. Localization
"Couldn't equip that" and related inline messages resolved via string resources (English, Hindi, Arabic, Urdu) — no hardcoded user-facing strings.

##### 22. RTL
Grid item selection/equipped-indicator visuals mirror correctly for RTL locales; verified via a dedicated RTL layout test.

##### 25. Security
No new sensitive data handling; server remains authoritative for all ownership/equip state (§17).

##### 27. Testing
- Unit (P0): server-rejection rollback test — simulate `403 ITEM_NOT_OWNED`, assert UI state reverts correctly.
- Unit (P0): one-equipped-per-slot local-state transition test — equip two different items in the same slot in sequence, assert only the most recent is ever marked equipped.
- Unit: rapid-tap sequencing test — multiple taps in quick succession resolve to a stable final state matching the last tap.
- UI: equipped-state visual indicator updates instantly on tap (optimistic), independent of network latency in the test harness.

##### 31. Final Verification Checklist
- [ ] Equip/unequip optimistic update is synchronous and immediate on tap
- [ ] Server-rejection rollback test passes (P0)
- [ ] One-equipped-per-slot local invariant test passes (P0)
- [ ] Rapid-tap sequencing resolves to a stable, correct final state
- [ ] Equipped-state visual indicator updates instantly and correctly
- [ ] Localization (EN/HI/AR/UR) and RTL verified
- [ ] Analytics events wired via `AnalyticsTracker`
- [ ] Performance budget (p95 < 300ms) validated
- [ ] Item/slot-scoped recomposition only (no unrelated grid re-renders)

#### `Development_Blueprints/A12_Avatar_System/KMP/03-locked-item-detail-unlock-criteria-flow.md`

##### 4. Objective
Build the locked-item teaser component and Locked Item Detail screen rendering server-resolved unlock criteria, a non-committal preview action, and a direct deep link to the unlocking activity, backing FR-2, FR-7, and Edge Cases 3, 5.

##### 5. Business Requirements
- Locked items display specific unlock criteria text (e.g., "7-day streak"), never a generic lock icon with no explanation (FR-7).
- Locked-item visual language is a soft greyscale/desaturated silhouette — never a harsh blackout or "?" mystery-box treatment, which could imply gacha-style randomness contrary to the platform's anti-loot-box principle (PRD §2.1).
- Criteria text is always visible beneath the item, not hidden behind an additional tap (PRD §2.1).
- Locked Item Detail offers a "Preview" action (non-committal try-on) with zero persistent side effects — closing without equipping leaves the actually-equipped state unchanged (Edge Case 5).
- Locked Item Detail offers a "Go to [Activity]" action deep-linking directly to the relevant unlocking feature (FR-2).
- A locked item whose criteria reference a deprecated badge/level gracefully shows "currently unavailable to unlock" rather than a broken reference (Edge Case 3).
- Criteria text is rendered exclusively from the server-provided `unlock_rule_description` string — the client never parses or renders raw JSON (mirrors B-01's server-resolution guarantee).

##### 11. KMP Requirements
- `LockedItemTeaser` renders the item's desaturated silhouette, name, and `unlock_rule_description` text directly beneath — never behind a second tap.
- `LockedItemDetailScreen` shows the full criteria, a "Preview" button, and a "Go to [Activity]" primary button.
- "Preview" action: temporarily renders the previewed item in K-01's `Avatar3DRenderer` via a local-only, non-persisted UI state flag (`previewedItemId: ItemId?` in `AvatarUiState` or a scoped child state) — this flag is never written to `avatar_inventory_cache` or sent to the server; on screen dismiss, the preview flag is cleared and the actually-equipped state (from K-02) renders again.
- "Go to [Activity]" resolves a deep-link target from the item's `unlock_rule` type (badge → relevant feature, level → relevant feature, habit-milestone → `noorheroes://habits` per A.7's established target) and navigates via `Navigator`.
- `unlock_rule_available: false` renders a distinct "currently unavailable to unlock" visual variant instead of the standard criteria text, without blocking the rest of the screen (Edge Case 3).
- Criteria text rendering must never attempt to parse the string as JSON or apply any client-side interpretation — it is treated as an opaque, already-localized display string.

##### 15. Validation
Unit test asserting the "Preview" action produces zero persistent state change — after previewing an item and then dismissing without equipping, re-reading `AvatarUiState.equippedBySlot` must exactly match its pre-preview value (Edge Case 5, mandatory).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| `unlock_rule_available: false` | "Currently unavailable to unlock" variant rendered gracefully, rest of screen unaffected |
| Deep-link target for "Go to [Activity]" fails to resolve (unknown/removed feature route) | Standard deep-link fallback (existing platform-wide deep-link error handling, not re-implemented here) |
| Preview action attempted on an already-equipped item's slot | Preview simply shows the target item in place of the current one temporarily; no error, treated as a normal preview |

##### 19. Offline First
Locked-item criteria display uses cached catalog data (`avatar_inventory_cache`, K-01) and works fully offline; only the "Go to [Activity]" deep-link's destination feature may itself require connectivity, which is that destination feature's own concern, not this sub-feature's.

##### 21. Localization
`unlock_rule_description` and "currently unavailable to unlock" copy resolved via backend-provided translation keys / pre-resolved strings (English, Hindi, Arabic, Urdu).

##### 22. RTL
Locked Item Detail layout (illustration, criteria text, action buttons) mirrors correctly for RTL locales; verified via a dedicated RTL layout test.

##### 25. Security
No new sensitive data handling; criteria text is treated as an opaque server-provided string, never executed/parsed/evaluated client-side (defense against any theoretical injection via a compromised criteria string).

##### 27. Testing
- Unit (P0): preview action has zero persistent side effects — assert `equippedBySlot` unchanged after preview-then-dismiss.
- UI (P0): regex assertion that the displayed criteria text never contains raw JSON-like patterns (curly braces, quoted keys) — confirms exclusive reliance on the server-resolved description string.
- UI: "currently unavailable to unlock" variant renders correctly for a fixture item with `unlock_rule_available: false`.
- Integration: "Go to [Activity]" navigates to the correct deep-link target for each of the three unlock-rule types (badge/level/habit-milestone).

##### 31. Final Verification Checklist
- [ ] Criteria text always visible beneath teaser, never hidden behind an extra tap
- [ ] Preview action verified to have zero persistent side effects (P0 test passing)
- [ ] Criteria text never rendered from raw JSON (regex UI test passing, P0)
- [ ] "Currently unavailable to unlock" variant renders correctly for deprecated references
- [ ] "Go to [Activity]" correctly deep-links for badge/level/habit-milestone rule types
- [ ] Localization (EN/HI/AR/UR) and RTL verified
- [ ] Analytics events wired via `AnalyticsTracker`
- [ ] Preview state fully isolated from K-02's equipped-state model

#### `Development_Blueprints/A12_Avatar_System/KMP/04-auto-unlock-detection-celebration-notification.md`

##### 4. Objective
Implement diffing-based auto-unlock detection against successive `GET /v1/children/{id}/inventory` responses, firing `avatar_item_auto_unlocked` and an in-app celebration when the app is foregrounded, plus notification deep-link handling — backing FR-8 and PRD §6.6/§7 item 5.

##### 5. Business Requirements
- The child is never required to manually "claim" an avatar-item unlock — auto-unlock is detected and surfaced automatically (FR-8).
- Detection is diffing-based: since the unlock itself happens server-side asynchronously (B-02), the client compares each fresh inventory response's owned-items list against the previously-cached list to identify newly-owned items.
- If the app is foregrounded when a new item is detected, an in-app celebration surfaces; otherwise the item is simply discoverable next time the Avatar screen opens.
- A missed/failed notification never affects the underlying unlock — the grant itself (server-side `child_inventory` row, B-02) is authoritative regardless of notification delivery (PRD §1.11 Error Handling).
- Notification deep link lands directly on the newly-unlocked item's detail (`noorheroes://avatar/item/{itemId}`).

##### 10. KMP Requirements
- `AutoUnlockDiffDetector.detectNewlyOwned(previous: List<OwnedItem>, current: List<OwnedItem>): List<OwnedItem>` — pure function comparing item ID sets, returning items present in `current` but absent from `previous`.
- Invoked by `InventoryRepository` immediately after each successful inventory fetch and immediately before the fetched response overwrites the cached previous state (ordering is critical — diffing must always compare against the *prior* cache, never against itself).
- For each newly-detected item, fire `avatar_item_auto_unlocked` via `AnalyticsTracker.logEvent()` regardless of foreground state.
- If the app is foregrounded at detection time, present `AutoUnlockCelebrationModal` (gentle, non-jarring reveal, consistent with the platform's Character Evolution/badge-celebration visual language, not an aggressive flash/strobe effect).
- If the app is backgrounded, rely on the existing `notifications` module's push delivery for the primary discovery path; the diffing detector still runs on next foreground/fetch and will simply find the item already reflected as owned (no duplicate celebration if the child already saw the item via the notification).
- Notification deep-link landing target `noorheroes://avatar/item/{itemId}` navigates directly to the item's (now-owned) detail view within the Avatar Screen.

##### 15. Validation
Unit test (P0, mandatory per PRD §7 Android prompt item 5): feed two sequential mocked inventory responses, the second containing exactly one additional owned item, and assert `AutoUnlockDiffDetector` correctly identifies exactly that one new item — no false positives from re-ordering, no false negatives from a changed-but-not-new item (e.g., an equip-state change on an already-owned item must not be misidentified as a new unlock).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Notification delivery fails/is missed | Item still discoverable via diffing on next Avatar screen open/fetch; grant itself unaffected (§1.11) |
| App backgrounded at unlock-detection time | No in-app celebration shown; push notification (if delivered) is the primary discovery path; diffing still logs `avatar_item_auto_unlocked` |
| Two items unlocked between fetches | Both correctly identified by the diff (not just the first); celebration handles a multi-item unlock gracefully (queued or combined presentation, not a dropped second item) |
| Diff baseline missing (first-ever fetch, fresh install) | No false "newly unlocked" celebration fires for a brand-new child's initial owned-items set — the detector must treat an empty/absent previous state as "no diff to report," not "everything is new" |

##### 19. Offline First
Diff detection only runs on a successful network fetch (it requires two real response snapshots to compare); it does not run against purely-cached/offline reads, consistent with the PRD's "auto-unlock evaluation requires connectivity" principle (§1.14).

##### 21. Localization
Celebration modal copy ("You unlocked a new outfit! 🎉"-style text) resolved via string resources (English, Hindi, Arabic, Urdu).

##### 22. RTL
Celebration modal layout mirrors correctly for RTL locales; verified via a dedicated RTL layout test.

##### 25. Security
No new sensitive data handling.

##### 27. Testing
- Unit (P0): two-sequential-mocked-responses diff test, asserting exactly the correct new item is identified (per PRD §7 item 5).
- Unit: empty/absent-baseline case does not produce false "everything is new" celebration.
- Unit: equip-state-only change on an already-owned item is not misidentified as a new unlock.
- Integration: multi-item simultaneous unlock correctly identifies all new items, not just the first.
- Integration: notification deep link `noorheroes://avatar/item/{itemId}` navigates to the correct item detail.

##### 31. Final Verification Checklist
- [ ] Diff detector correctly identifies newly-owned items across two sequential mocked responses (P0 test passing)
- [ ] Empty/absent baseline does not produce a false "everything is new" celebration
- [ ] Equip-state-only changes are not misidentified as new unlocks
- [ ] Multi-item simultaneous unlock correctly identifies all new items
- [ ] Diff-before-overwrite ordering verified and documented
- [ ] Celebration modal renders gently, non-jarringly, matching platform visual language
- [ ] Notification deep link lands on correct item detail
- [ ] Localization (EN/HI/AR/UR) and RTL verified
- [ ] Analytics events wired via `AnalyticsTracker`

#### `Development_Blueprints/A12_Avatar_System/KMP/05-character-evolution-milestone-reveal.md`

##### 4. Objective
Build the Character Evolution Milestone Reveal modal and its graceful in-place/next-load application logic, backing FR-9 and Edge Case 8.

##### 5. Business Requirements
- Avatars and Noor companions evolve through learning-based progression — Quran skills, story morals, kindness actions, and habit consistency unlock new outfits, glow states, and story-world abilities (FR-9).
- If a child is actively viewing the companion (e.g., on Home) when an evolution milestone is crossed, the visual update applies gracefully — on next Home load or via a graceful in-place transition — never an abrupt, jarring change mid-interaction that could startle a young child (Edge Case 8).
- Evolution milestones use a gentle, growth-themed transition (a soft glow bloom, consistent with A.7's Noor Garden growth metaphor) rather than an abrupt "transform" effect, reinforcing "gradual real progress" over a sudden game-like power-up (PRD §2.1).
- Success metric target: Character Evolution milestone view-through rate ≥ 70% (PRD §1.4) — the reveal must be genuinely engaging, not skippable-by-default in a way that undermines this metric.

##### 10. KMP Requirements
- `CharacterEvolutionDetector` reuses the same diffing principle as K-04's `AutoUnlockDiffDetector`, but scoped to companion-evolution-tier fields within the inventory/companion-state response (e.g., a `companion_tier`/`evolution_stage` field) rather than owned-items — detects a tier/stage increase between successive fetches.
- If the child is **not** actively viewing the companion at detection time, the new tier is simply reflected on next Home load (no special transition needed — the companion just renders at its new tier).
- If the child **is** actively viewing the companion (Home screen foregrounded) when the detector identifies a crossed milestone, `CharacterEvolutionRevealModal` presents with a soft glow-bloom transition, then dismisses back to the current screen (e.g., Home) — never an abrupt swap of the rendered companion mid-frame.
- Modal presentation must be interruptible/dismissible without causing any inconsistency in the underlying companion-tier state (dismissing the modal is purely a UI action, not a state mutation).

##### 15. Validation
Unit test asserting that when the companion is actively being viewed at milestone-crossing detection time, the transition is applied gracefully (via the documented glow-bloom path) rather than an abrupt state swap — verified by asserting the transition-state flag sequence, not a visual/pixel comparison (Edge Case 8, mandatory).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Evolution milestone crossed while child is off Home/not viewing companion | New tier simply reflected on next Home load, no special transition needed |
| Evolution milestone crossed while child is actively viewing companion | Graceful glow-bloom transition applied in-place, never an abrupt swap |
| Modal dismissed mid-transition | Underlying companion-tier state is unaffected by the dismissal action; companion settles at its correct new tier regardless |
| Detector runs with no prior baseline (fresh install) | No false "evolution" reveal fires for a brand-new child's initial tier |

##### 19. Offline First
Companion-tier detection only runs on a successful network fetch, mirroring K-04's connectivity-dependent diffing principle; offline sessions simply render the last-known tier from cache without triggering a reveal.

##### 21. Localization
Milestone reveal celebratory copy resolved via string resources (English, Hindi, Arabic, Urdu).

##### 22. RTL
Reveal modal layout mirrors correctly for RTL locales; verified via a dedicated RTL layout test.

##### 25. Security
No new sensitive data handling.

##### 27. Testing
- Unit (P0): graceful in-place transition applied when companion is actively viewed at detection time (Edge Case 8).
- Unit: no false reveal on fresh-install/no-baseline case.
- Unit: dismissing the modal mid-transition does not corrupt the underlying tier state.
- UI: reveal modal renders the correct gentle glow-bloom transition, not an abrupt swap (visual-language conformance test against design tokens).
- Integration: milestone crossed while off Home → new tier correctly reflected on next Home load without a modal ever firing outside the viewing context.

##### 31. Final Verification Checklist
- [ ] Tier-crossing detection correctly identifies genuine milestones only (no false positives on unrelated field changes)
- [ ] Graceful in-place transition verified when companion is actively viewed at detection time (P0 test passing)
- [ ] No abrupt/jarring swap ever occurs while the child is actively viewing the companion
- [ ] Reveal modal matches the established gentle glow-bloom visual language, not a sudden "transform" effect
- [ ] A.2 Home integration hook added without disrupting existing Home dashboard behavior
- [ ] Localization (EN/HI/AR/UR) and RTL verified
- [ ] Analytics events wired via `AnalyticsTracker`
- [ ] Animation performance smooth on low-end Android target

#### `Development_Blueprints/A12_Avatar_System/KMP/06-offline-inventory-cache-equip-outbox-sync.md`

##### 4. Objective
Implement Room-backed offline rendering of `avatar_inventory_cache` and a WorkManager/coroutine-scheduled outbox for equip/unequip actions taken offline, backing FR-6 (offline-tolerant equip) and PRD §1.14 Offline States.

##### 5. Business Requirements
- Last-synced avatar state (owned items, equipped state) renders fully offline (PRD §1.14).
- Equip actions taken offline queue and sync on reconnect, consistent with the platform's offline-first equip pattern (FR-6).
- Locked-item criteria display uses cached catalog data even offline; auto-unlock evaluation itself requires connectivity (it's a server-side process, B-02) — the child is never blocked from viewing/equipping their already-owned items offline (§1.14).
- Offline-queued equip actions must reconcile correctly with server state on sync — including the case where a queued equip is rejected on sync (e.g., ownership state changed server-side in the interim).

##### 10. KMP Requirements
- `EquipOutboxEntry` (Room entity): `id`, `childId`, `itemId`, `action` (`EQUIP`|`UNEQUIP`), `slot`, `queuedAt`, `syncStatus` (`PENDING`|`SYNCING`|`FAILED`).
- `QueueOfflineEquipUseCase`: when offline, writes an `EquipOutboxEntry` and immediately applies K-02's optimistic local state update — the child's experience is identical whether online or offline (instant visual feedback either way).
- `EquipOutboxSyncWorker`: triggered on reconnect (via `core-network`'s connectivity observer), processes pending outbox entries in `queuedAt` order, calling B-01's equip/unequip endpoints (idempotent server-side, safe for retry).
- On sync success, the outbox entry is removed and the local optimistic state is confirmed (no visible change, since it was already correct).
- On sync rejection (e.g., `403 ITEM_NOT_OWNED` — ownership state changed server-side while offline), the outbox entry is marked `FAILED`, removed, and the local state is rolled back per K-02's existing rejection-handling logic, with a non-alarming message shown to the child on next screen view.
- If multiple offline equip actions were queued for the *same slot* (e.g., child tried on three different offline outfits in sequence), only the **last** queued action for that slot needs to actually reach the server as authoritative (earlier same-slot entries are superseded) — the outbox processor should collapse same-slot entries to the most recent before syncing, consistent with the platform's last-tap-wins principle (mirroring K-02's rapid-tap handling, extended to the offline-queue case).

##### 15. Validation
Unit test simulating the full offline-equip-then-reconnect-then-sync flow: queue an offline equip, simulate reconnect, assert the sync worker calls B-01's endpoint exactly once for the correct final item, and the outbox entry is cleared on success (mandatory offline-sync integration test per PRD §6.10/§7).

##### 18. Error Handling
| Scenario | Behavior |
|---|---|
| Equip attempted while offline | Optimistic local update applied immediately (K-02's logic); action queued in `equip_outbox` |
| Multiple offline equips in the same slot | Collapsed to the last-queued action before sync; only that one reaches the server |
| Sync fails due to server-side ownership rejection | Outbox entry marked `FAILED`, removed; local state rolled back per K-02; non-alarming message shown |
| Sync worker interrupted mid-batch (app killed) | Remaining pending entries persist in Room and resume processing on next connectivity/app-start event, no data loss |
| Reconnect while another equip is already syncing | Sync worker processes entries sequentially per child to avoid racing concurrent writes to the same slot |

##### 19. Offline First
This sub-feature **is** the offline-first mechanism for equip/unequip — K-01/K-02's read/optimistic-update layers depend on this sub-feature's outbox to fully honor the offline-tolerant equip requirement (FR-6) rather than only working online.

##### 21. Localization
Sync-failure messages resolved via string resources (English, Hindi, Arabic, Urdu), reusing K-02's existing rejection-message localization.

##### 22. RTL
N/A directly (no new user-facing layout beyond reusing K-02's existing rejection-message presentation, already RTL-verified there).

##### 25. Security
No new sensitive data handling; the outbox stores only item/slot/action identifiers, no payment or PII data (consistent with FR-5's no-payment-path guarantee).

##### 27. Testing
- Unit: `EquipOutboxEntry` same-slot-collapse logic — multiple queued entries for one slot reduce to exactly one authoritative sync call.
- Integration (mandatory): full offline-equip → reconnect → sync flow, asserting exactly one correct server call and correct outbox cleanup.
- Integration: sync rejection correctly rolls back local state and clears the failed outbox entry.
- Integration: app-killed-mid-sync recovery — pending entries persist and resume correctly on next launch/reconnect.

##### 31. Final Verification Checklist
- [ ] `EquipOutboxEntry`/`EquipOutboxDao` implemented and registered in `core-database`
- [ ] Offline equip applies the identical optimistic UI update as online equip (K-02 reused, not duplicated)
- [ ] Same-slot collapse logic verified (only the last queued action per slot syncs)
- [ ] Full offline-equip → reconnect → sync integration test passes
- [ ] Sync-rejection correctly rolls back local state and clears the outbox entry
- [ ] App-killed-mid-sync recovery verified (no data loss)
- [ ] No duplicate analytics firing on sync confirmation (fired once, at optimistic-action time)
- [ ] No PII/payment data ever stored in the outbox

## Independent completeness review

- A5 requires four Arabic Letters screens and six Quran game modes; Learn screenshot cluster names do not establish that all exist. Add requirement-driven prompts with missing-reference flags rather than assuming hidden frames.
- A8 requires five independently reviewable question-type layouts; screenshot Quiz Question-01 only verifies multiple choice. Preserve separate sequence, true/false, image-match, audio-match prompt entries.
- Share previews, item/transaction detail, achievement level, family goal, seasonal archive, placement check and saved/deferred results destinations must remain explicit even when absent from screenshot inventory.
- Deduplicate shared quizzes, favorites, downloads, parent gate, hints, facts and badge modals by owning feature; maintain alias entries and exact originating-context return paths.
- No A10 game mechanics can be invented for future catalog entries; six A5 modes are specified; generic game session is a wrapper requiring a manifest-specific mechanic reference.
- No mandatory FR is discarded: backend/ledger/scholar-governance rules are retained as constraints on design/prototype fixture outcomes, not turned into fabricated child screens.
- Full paragraph-level audit of every retained section and exact source-screen mapping remains a parent handover task; avoid certifying extraction as all PRD text reviewed.
- Educational catalog strings and all uninspected screenshot exact content remain execution blockers for affected prompts; source-preserving duplication is possible only after original frame/copy access.
