**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 165 — Per-Child Report (full view)

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **C22 — Per-Child Report (full view)**.
- Surface: **screen**. Number is controlled review order, not a forced linear user journey.
- Execution status: **Reference available; unresolved conflicts require approval before design**.
- Journey entry / previous screen: Parent Dashboard, Child Management.
- Next screen(s) / result: AI Interaction History, Screen Time & Bedtime Settings (C.23), Skill Detail.
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_C22_Per_Child_Reports.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Parent Area In-App (19-26)/Feature_C22_Per_Child_Reports.md>); **§1.18 row 1; §1.7; §2; §6; §13**.
- Current mobile reference: [NoorHeroes current preview](https://noorheroes.figma.site/) → selector **Per-Child Report**; exact text captured below.
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: [Per-Child Report - Polished](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1113-8090) — `1113:8090`. 
- Frame 2 container: `1085:13003`; visual reference: **Missing corresponding screen reference.** Do not substitute a visually related hub as functional evidence.
- Reference qualification: No independently verified equivalent for this screen; global style inspiration must not replace approved copy.
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- [Per-Child Report-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Child Reports/Per-Child Report-01.png>)
- [Per-Child Report-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Child Reports/Per-Child Report-02.png>)
- [Per-Child Report-03.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Child Reports/Per-Child Report-03.png>)
- [Per-Child Report-04.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Child Reports/Per-Child Report-04.png>)
- [Per-Child Report-05.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Child Reports/Per-Child Report-05.png>)
- [Per-Child Report-06.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Child Reports/Per-Child Report-06.png>)
- [Per-Child Report-07.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Child Reports/Per-Child Report-07.png>)
- [Per-Child Report-08.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Child Reports/Per-Child Report-08.png>)
- [Per-Child Report-09.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Child Reports/Per-Child Report-09.png>)
- [Per-Child Report-10.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Child Reports/Per-Child Report-10.png>)
- [Per-Child Report-11.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Child Reports/Per-Child Report-11.png>)
- [Per-Child Report-12.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Child Reports/Per-Child Report-12.png>)
- Blueprint alignment:
- [01-per-child-report-screen-and-state-architecture.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C22_Per_Child_Reports/KMP/01-per-child-report-screen-and-state-architecture.md>)
- [02-skill-mastery-grid-and-skill-detail-drilldown.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C22_Per_Child_Reports/KMP/02-skill-mastery-grid-and-skill-detail-drilldown.md>)
- [03-ai-interaction-history-screen.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C22_Per_Child_Reports/KMP/03-ai-interaction-history-screen.md>)
- [04-safety-report-screen.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C22_Per_Child_Reports/KMP/04-safety-report-screen.md>)
- [05-monthly-family-report-screen.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C22_Per_Child_Reports/KMP/05-monthly-family-report-screen.md>)
- [06-ai-insight-report-screen-premium.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C22_Per_Child_Reports/KMP/06-ai-insight-report-screen-premium.md>)
- [07-report-pdf-export-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C22_Per_Child_Reports/KMP/07-report-pdf-export-flow.md>)
- [08-share-report-flow-parent-gated.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C22_Per_Child_Reports/KMP/08-share-report-flow-parent-gated.md>)
- [09-report-offline-caching-and-deep-link-handling.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C22_Per_Child_Reports/KMP/09-report-offline-caching-and-deep-link-handling.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: - P-C26-01: C22 AI history is flags/safety events only (FR-5/13); C26 history is write-time-redacted input/output summaries with model_version/policy_result/expires_at (FR-6/7). Treat distinct scoped views or seek approval for merge; do not silently present full history in safety-only report. See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Explain learning trends for a selected child and safely connect to deeper skill, AI-safety, report and usage-control views. Screen-specific role: Per-Child Report (full view).

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

The complete feature obligations are retained in [every-FR register](../10_REQUIREMENT_COVERAGE_REGISTER.md); section 2 identifies the exact screen-inventory row.

## 4. Exact content specification

### Current mobile source — exact captured text

```text
Progress Report
👧

Aisha

Sample learning report · preview only

Past Month
Default
⏳ Loading
⏱️ Delayed
📭 No Activity
📶 Offline
Learning Activity
120 XP
Mon
180 XP
Tue
95 XP
Wed
210 XP
Thu
165 XP
Fri
240 XP
Sat
145 XP
Sun

1,155

Total XP

165

Daily Avg

7/7

Days Active

Learning activity chart showing 7 days of XP earned: Monday 120 XP, Tuesday 180 XP, Wednesday 95 XP, Thursday 210 XP, Friday 165 XP, Saturday 240 XP, Sunday 145 XP. Total 1,155 XP earned with daily average of 165 XP. Active all 7 days.
Habit Check-ins
This Month
S
M
T
W
T
F
S
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
None
Some
Most
All
Skill Progress
All Skills
📖 Quran
ا Arabic
⭐ Stories
🤲 Du'as

Surah Al-Fatiha

Mastered

Surah Al-Ikhlas

Mastered
75%

Surah Al-Asr

Practicing
35%

Basic Tajweed

Learning

Arabic Alphabet

Mastered
60%

Morning Du'as

Practicing

Prophet Ibrahim

Mastered

Advanced Letters

Ready

Prophet Musa

Needs Refresh

4

Mastered

3

In Progress

1

Ready

AI Activity
View All →

All interactions safe

4 AI interactions recorded this month. All content appropriately filtered and age-appropriate.

Question redirected to approved content

2 hours ago

Question about prayer times approved

Yesterday

Export PDF
Share

💡 Sample effort and engagement patterns only — this is not a live assessment of your child.
```

### Frame 1 — exact layer text (separate source; differences need approval)

```text
Default
Loading
Delayed
No
Activity
Offline
Aisha
Grade 3
Detailed learning & character report
Past Month
Focus Time
18.5 hrs
Habit Score
94%
Reflections
12 logs
Learning
Activity
Consistent
rhythm
140
M
180
T
160
W
195
T
150
F
210
S
120
S
Total XP
1,155
Daily Avg
165
Days Active
7 / 7
Habit Check-ins
This Month
S
M
T
W
T
F
S
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
None
Some
Most
All Habits
Skill Progress
8 Total Tracked
All Skills
📖 Quran
Arabic
Stories
Curriculum
Balance
4 Mastered • 3 In Progress • 1
Ready
Surah Al-Fatiha
Recitation & Meaning
Mastered
Surah Al-Ikhlas
Memorization & Theme
Mastered
Surah Al-Asr
Pronunciation fluency
75%
Basic Tajweed
Madd rules & elongation
35%
Arabic Alphabet
Letter forms & sounds
Mastered
Morning Du'as
Daily gratitude routine
60%
AI Activity
View All
All interactions safe
4 AI interactions recorded this month.
All content appropriately filtered and
age-appropriate.
Question redirected to approved content
2 hours ago • Curious
exploration
Resolved
Question about prayer times approved
Yesterday • Astronomy
query
Resolved
Export PDF
Share
This report shows effort and engagement
patterns. Detailed accuracy metrics are
available in the full parent dashboard.
Detailed Learning Report
Aisha
Detailed learning report
```

### Requirement-driven fields and content roles

- Global date range
- Weekly trend
- Habit calendar
- Six-state mastery grid
- AI safety-event link
- Freshness timestamp
- Export PDF
- Share via WhatsApp
- Weekly/monthly/AI insight/safety report content

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Screen scope: Per-Child Report (full view). Arrange only these vertical content roles: Global date range → Weekly trend → Habit calendar → Six-state mastery grid → AI safety-event link → Freshness timestamp → Export PDF → Share via WhatsApp → Weekly/monthly/AI insight/safety report content. Use one clear heading and context row; source-approved primary action follows this screen content. Reuse local shared components without pulling other module sections onto this screen. Retain verified source content order where it differs; required missing content requires source approval before placement.

- Preserve content order and screen purpose. Use a vertical auto-layout content stack; horizontal inset 20, base spacing 4/8/12/16/24/32; card content padding 12–16. Keep compact controls next to their labels; align headings and cards to one column edge.
- Use existing cream `#FAF7F0`, surface `#FFFFFF`, ink `#1C2B33`, teal `#0E7C7B`, gold `#D4A24C`. Gold/bright teal are accents, not untested small-text colors. Body 14/16; heading 20/24; brand-only display 28/32. Preserve actual font assets; PRD Latin sans, display serif, separate verified Arabic content font.
- Do not import Frame 2's sample statistics, claims, religious text, section additions or combined desktop layouts. Borrow hierarchy, restrained surface separation and image framing only where they support this surface.
- Screen viewport is separate from long content height. Use vertical overflow when content exceeds available height; header/footer may be fixed only with bottom and top content clearance. At 320/360/390/420 logical widths, long labels wrap. At 200% text scale, stack grids or allow scrolling; no fixed text block height or sacred-text ellipsis.
- Essential touch target≥44×44 logical units; younger-child primary tasks≥56 where A2 specifies. Decorative icons have no hit targets. Assets retain aspect ratio; no text burned into illustrations. Safe area and keyboard must never obscure the current action.
- Source frames, unrelated screens and existing design direction remain unchanged. Token/component changes require separate review; never detach or globally mutate a source instance to fix this screen.

## 6. Screen states and conditional scenarios

- Default for Per-Child Report (full view) Applicable pending/success/error only for actions explicitly named in action_rules Cached offline read only where supported; online-only mutations show sourced reconnect reason Back/cancel restores invoking context; actual unresolved source behavior blocks execution

Owning inline components / variants (do not create unrelated standalone routes):
- {"name": "Date Range Filter (component)", "entry": "Per-Child Report", "classification": "Component", "exit": "Filtered report view"}
- {"name": "Weekly Trend Chart", "entry": "Per-Child Report", "classification": "Component", "exit": "N/A (display)"}
- {"name": "Habit Calendar", "entry": "Per-Child Report", "classification": "Component", "exit": "Habit detail (cross-ref A.7)"}
- {"name": "Skill Mastery Grid", "entry": "Per-Child Report", "classification": "Component", "exit": "Skill Detail Drill-down"}
- {"name": "AI Interaction Log Link (component)", "entry": "Per-Child Report", "classification": "Component", "exit": "AI Interaction History"}
- {"name": "Delayed-Analytics State (component variant)", "entry": "Report generation delayed", "classification": "Component variant", "exit": "N/A"}
- {"name": "No-Activity Empty State (component variant)", "entry": "Zero activity in range", "classification": "Component variant", "exit": "N/A"}
- {"name": "Offline Export/Share Blocked State", "entry": "Export/Share attempted offline", "classification": "Screen variant", "exit": "N/A"}

Only apply states that belong to this surface. List-only empty/skeleton states are not added to legal documents or static intros. Network submit has a pending/timeout/retry result; retry preserves draft and must not duplicate a server-confirmed operation. Voice states need consent + OS grant; denial supplies listen/text/manual alternative. Loading/error/disabled/offline wording missing from source is a content approval gap.

<details><summary>Authoritative state/edge source context — apply screen-relevant cases, not all cases indiscriminately</summary>

### 1.10 Edge Cases

1. A parent selects a date range that spans a period before the child's account even existed → the report correctly shows "no activity" only for the portion of the range after account creation, never an error for the impossible pre-existence portion, and clearly communicates the child's actual account-start boundary if relevant to the parent's understanding.
2. A parent shares an achievement via WhatsApp, but the underlying badge is later revoked due to a data-quality correction (cross-ref A.11 Edge Case 3's "badges are sticky once earned" rule) → the already-shared card remains valid/unaffected (it was generated and sent at a point in time, a static artifact, not a live-updating reference); future report views simply reflect current state without retroactively invalidating a prior share.
3. A parent requests a Safety Report "on demand" for a child with zero blocked requests or content flags ever recorded → the report generates successfully showing a clean/reassuring "no safety events recorded" state, never an error or an empty-looking broken section.
4. AI Insight Report access is requested for a child whose family's premium entitlement expires mid-generation (a race between the async report job and a billing-state change) → the report generation job re-checks entitlement at completion time, not just at request time, and the delivered report respects the entitlement state actually in effect when it's served to the parent.
5. A parent drills into a skill mastery grid item for a skill belonging to a domain the child hasn't engaged with at all yet → shows a clear "not started" state for that skill rather than an empty/confusing detail view, consistent with A.9's `Locked`/`Ready` state language.
6. Two co-guardians view the same child's report on different devices simultaneously and one exports a PDF while the other adjusts the date filter → these are independent, read-mostly view actions with no shared-state conflict requiring coordination (distinct from C.21's mutating-action concurrency concerns).
7. A parent's PDF export or WhatsApp share is requested for a report that itself failed content-safety validation (the underlying weekly/AI-insight report row has `content_safety_passed = false`) → the export/share action operates only against the last *passing* report, exactly mirroring C.20's read-API fallback behavior, never exporting/sharing content that was never eligible to be shown in-app in the first place.
8. A child's AI permission is disabled by the parent partway through a reporting period → the AI Interaction History for that period correctly shows activity only up to the point AI was disabled, with no further entries after that point, and the report doesn't imply ongoing AI activity that didn't actually occur.
9. A parent requests an export/share action while offline → blocked with a clear "needs internet" message, since both actions require a fresh, server-validated report payload, never operating on a potentially-stale local cache for an action with external-sharing consequences.

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Report generation delayed | Last successfully generated report shown with explicit "as of" framing (consistent with C.20's established pattern) |
| Zero activity in the selected range/report type | Explicit "no activity yet" / "no safety events recorded" state, never a blank/broken chart |
| AI Insight Report entitlement lapses mid-generation | Delivered report respects entitlement state at serve time, not request time (Edge Case 4) |
| Export/share requested against a content-safety-failed report | Operates against the last passing report instead, mirroring C.20's fallback |
| Export/share requested offline | Blocked with a clear "needs internet" message |

### 1.12 Empty States
- Zero activity in the selected date range → "Once [Child] starts learning, you'll see their progress here" framing, consistent with the platform's general empty-state philosophy.
- Zero AI interactions/safety events ever → a clean, reassuring "no safety events recorded" state, not an alarming or confusing absence.

### 1.13 Loading States
- Per-Child Report: skeleton shimmer per component, independently resolving (consistent with C.20's per-component independence pattern).
- PDF export: a clear "Generating your report..." progress indicator given the few-second generation time.

### 1.14 Offline States
- The in-app report view renders from cache when offline (read-only, consistent with C.20); export/share actions are blocked offline per Edge Case 9.

### 1.15 Permission States
- No new runtime permissions; WhatsApp sharing uses the standard OS share sheet, which itself may surface its own permission/app-selection UI outside this app's control.



</details>

## 7. Interactions and navigation

- Entry: Parent Dashboard, Child Management. Primary result: AI Interaction History, Screen Time & Bedtime Settings (C.23), Skill Detail. Apply only the named screen required_fields; parent-sensitive mutations pass fresh C19 gate. Back/cancel returns to invoking surface without committing. Exact unspecified controls/copy remain approval gaps.

For every action below, use the cited preconditions and source validation. Preserve the invoking route and selected child. Back/cancel dismisses only the current overlay or returns to the invoking screen, preserving drafts and completed progress where specified. Unavailable actions remain visibly labeled with their reason and never activate. Permission prompts occur only after parent consent and a deliberate related action. A prototype simulates outcomes; it never validates identity, grants permissions, charges money or mutates production data.

Verified current-preview controls, retained to prevent omitted clickable elements:

- {"disabled": false, "label": "Go back", "placeholder": null, "tag": "BUTTON", "text": "", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Past Month", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Default", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "⏳ Loading", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "⏱️ Delayed", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "📭 No Activity", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "📶 Offline", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "All Skills", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "📖 Quran", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "ا Arabic", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "⭐ Stories", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "🤲 Du'as", "type": null}
- {"disabled": false, "label": "Surah Al-Fatiha: Fully mastered", "placeholder": null, "tag": "BUTTON", "text": "Surah Al-Fatiha\n\nMastered", "type": null}
- {"disabled": false, "label": "Surah Al-Ikhlas: Fully mastered", "placeholder": null, "tag": "BUTTON", "text": "Surah Al-Ikhlas\n\nMastered", "type": null}
- {"disabled": false, "label": "Surah Al-Asr: Actively practicing", "placeholder": null, "tag": "BUTTON", "text": "75%\n\nSurah Al-Asr\n\nPracticing", "type": null}
- {"disabled": false, "label": "Basic Tajweed: Currently learning", "placeholder": null, "tag": "BUTTON", "text": "35%\n\nBasic Tajweed\n\nLearning", "type": null}
- {"disabled": false, "label": "Arabic Alphabet: Fully mastered", "placeholder": null, "tag": "BUTTON", "text": "Arabic Alphabet\n\nMastered", "type": null}
- {"disabled": false, "label": "Morning Du'as: Actively practicing", "placeholder": null, "tag": "BUTTON", "text": "60%\n\nMorning Du'as\n\nPracticing", "type": null}
- {"disabled": false, "label": "Prophet Ibrahim: Fully mastered", "placeholder": null, "tag": "BUTTON", "text": "Prophet Ibrahim\n\nMastered", "type": null}
- {"disabled": false, "label": "Advanced Letters: Ready to start", "placeholder": null, "tag": "BUTTON", "text": "Advanced Letters\n\nReady", "type": null}
- {"disabled": false, "label": "Prophet Musa: Could use review", "placeholder": null, "tag": "BUTTON", "text": "Prophet Musa\n\nNeeds Refresh", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "View All →", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Export PDF", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Share", "type": null}

For any captured control absent from an explicit action above, reconcile it against the screen-specific source below before wiring. Do not connect it to a convenient unrelated screen. Mark it **unresolved, non-executable** until its actual destination/state is confirmed; the navigation appendix reports this limitation. Decorative source-layer names are not automatically click targets.

<details><summary>Screen-specific PRD specification / click behavior</summary>

Screen: Per-Child Report (full view)
Source PRD_Documents/Parent Area In-App (19-26)/Feature_C22_Per_Child_Reports.md §1.18 row 1; §1.7; §2; §6; §13
Purpose: Explain learning trends for a selected child and safely connect to deeper skill, AI-safety, report and usage-control views. Screen-specific role: Per-Child Report (full view).
Fields: Global date range; Weekly trend; Habit calendar; Six-state mastery grid; AI safety-event link; Freshness timestamp; Export PDF; Share via WhatsApp; Weekly/monthly/AI insight/safety report content
Action contract:
Entry: Parent Dashboard, Child Management. Primary result: AI Interaction History, Screen Time & Bedtime Settings (C.23), Skill Detail. Apply only the named screen required_fields; parent-sensitive mutations pass fresh C19 gate. Back/cancel returns to invoking surface without committing. Exact unspecified controls/copy remain approval gaps.
States:
Default for Per-Child Report (full view) Applicable pending/success/error only for actions explicitly named in action_rules Cached offline read only where supported; online-only mutations show sourced reconnect reason Back/cancel restores invoking context; actual unresolved source behavior blocks execution

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
3. Create `NH/Enhanced/165/Per_Child_Report_full_view/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Per_Child_Report_full_view`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] C22 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
