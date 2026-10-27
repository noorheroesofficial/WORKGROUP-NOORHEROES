**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 157 — Parent Dashboard (landing)

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **C20 — Parent Dashboard (landing)**.
- Surface: **screen**. Number is controlled review order, not a forced linear user journey.
- Execution status: **Reference available; unresolved conflicts require approval before design**.
- Journey entry / previous screen: C.19 gate success (Parent Profile or Switch Profile).
- Next screen(s) / result: Child Management, Per-Child Reports, Screen Time/AI Controls, Subscription, Notifications/Support.
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_C20_Parent_Dashboard.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Parent Area In-App (19-26)/Feature_C20_Parent_Dashboard.md>); **§1.18 row 1; §1.7; §2; §6; §13**.
- Current mobile reference: [NoorHeroes current preview](https://noorheroes.figma.site/) → selector **Parent Dashboard**; exact text captured below.
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: [Html → Body → Mobile Viewport Wrapper (390px iOS format)](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1111-7561) — `1111:7561`. 
- Frame 2 container: `1085:13003`; visual reference: **Missing corresponding screen reference.** Do not substitute a visually related hub as functional evidence.
- Reference qualification: No independently verified equivalent for this screen; global style inspiration must not replace approved copy.
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- [Parent Dashboard-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Parent Area/Parent Dashboard-01.png>)
- [Parent Dashboard-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Parent Area/Parent Dashboard-02.png>)
- [Parent Dashboard-03.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Parent Area/Parent Dashboard-03.png>)
- [Parent Dashboard-04.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Parent Area/Parent Dashboard-04.png>)
- [Parent Dashboard-05.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Parent Area/Parent Dashboard-05.png>)
- [Parent Dashboard-06.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Parent Area/Parent Dashboard-06.png>)
- Blueprint alignment:
- [01-parent-dashboard-landing-screen.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C20_Parent_Dashboard/KMP/01-parent-dashboard-landing-screen.md>)
- [02-child-switcher-component.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C20_Parent_Dashboard/KMP/02-child-switcher-component.md>)
- [03-weekly-ai-report-card-preview.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C20_Parent_Dashboard/KMP/03-weekly-ai-report-card-preview.md>)
- [04-activity-timeline-preview-component.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C20_Parent_Dashboard/KMP/04-activity-timeline-preview-component.md>)
- [05-screen-time-summary-preview-component.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C20_Parent_Dashboard/KMP/05-screen-time-summary-preview-component.md>)
- [06-module-shortcut-grid-navigation.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C20_Parent_Dashboard/KMP/06-module-shortcut-grid-navigation.md>)
- [07-dashboard-offline-caching-sync.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C20_Parent_Dashboard/KMP/07-dashboard-offline-caching-sync.md>)
- [08-dashboard-deep-link-handling.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C20_Parent_Dashboard/KMP/08-dashboard-deep-link-handling.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: - P-C20-01: Dashboard and Report screenshots contain Default/Loading/Offline/Empty state toggles. Their product status is unverified; classify as probable preview/demo state controls pending actual site/Figma interaction audit. See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Give a verified parent a single-child-at-a-time overview with trustworthy freshness and shortcuts to every parent module. Screen-specific role: Parent Dashboard (landing).

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

The complete feature obligations are retained in [every-FR register](../10_REQUIREMENT_COVERAGE_REGISTER.md); section 2 identifies the exact screen-inventory row.

## 4. Exact content specification

### Current mobile source — exact captured text

```text
Parent Dashboard
Default
⏳ Loading
📶 Offline
📭 Empty

SELECT CHILD

👧
Aisha
👦
Omar
📊

Weekly Report

Today, 9:00 AM

📈
Positive

Aisha explored Quran practice this week

M

T

W

T

F

S

S

View Full Report

This Week

See all
📖

Completed: Prophet Yusuf story

2 hours ago

✓

Checked off: Evening dua

5 hours ago

🏆

Earned: 7-Day Streak badge

Yesterday

🧠

Completed: Prophet Stories quiz practice

Yesterday

Screen Time

Today, 9:00 AM

Healthy
35 min used
of 45 min

Healthy balance this week

Manage Screen Time

Quick Actions

👧
Children
📊
Reports
⚙️
Settings
💳
Subscription
💬
Support

📊 Dashboard data updates every 15 minutes
```

### Frame 1 — exact layer text (separate source; differences need approval)

```text
SELECT CHILD
🧕
Aisha
👦
Omar
👧
Fatima
Weekly Report
Today, 9:00 AM
Positive
Aisha had a great week with consistent Quran
practice and gentle curiosity.
M
T
W
T
F
S
S
View Full Report
This Week
See all
📖
Completed: Prophet Yusuf story
2 hours ago
Checked off: Evening dua
5 hours ago
🏆
Earned: 7-Day Streak badge
Yesterday
🧠
Completed: Prophet Stories quiz
(100%)
Yesterday
Screen Time
Today, 9:00 AM
Healthy
35 min used
of 45 min
Healthy balance this week
Manage Screen Time
Quick Actions
🧕
Children
Reports
Settings
Subscription
Support
📊
Dashboard data updates every 15 minutes
Parent Dashboard
Default
⏳
Loading
📶
Offline
📪
Empty
```

### Requirement-driven fields and content roles

- Child selector
- Milestones/course/lesson/Quran/story/quiz/habit/streak summaries
- Badges
- Weekly/monthly report previews
- Screen-time and bedtime status
- AI reasons and safe history link
- Plan capacity
- As-of timestamp

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Screen scope: Parent Dashboard (landing). Arrange only these vertical content roles: Child selector → Milestones/course/lesson/Quran/story/quiz/habit/streak summaries → Badges → Weekly/monthly report previews → Screen-time and bedtime status → AI reasons and safe history link → Plan capacity → As-of timestamp. Use one clear heading and context row; source-approved primary action follows this screen content. Reuse local shared components without pulling other module sections onto this screen. Retain verified source content order where it differs; required missing content requires source approval before placement.

- Preserve content order and screen purpose. Use a vertical auto-layout content stack; horizontal inset 20, base spacing 4/8/12/16/24/32; card content padding 12–16. Keep compact controls next to their labels; align headings and cards to one column edge.
- Use existing cream `#FAF7F0`, surface `#FFFFFF`, ink `#1C2B33`, teal `#0E7C7B`, gold `#D4A24C`. Gold/bright teal are accents, not untested small-text colors. Body 14/16; heading 20/24; brand-only display 28/32. Preserve actual font assets; PRD Latin sans, display serif, separate verified Arabic content font.
- Do not import Frame 2's sample statistics, claims, religious text, section additions or combined desktop layouts. Borrow hierarchy, restrained surface separation and image framing only where they support this surface.
- Screen viewport is separate from long content height. Use vertical overflow when content exceeds available height; header/footer may be fixed only with bottom and top content clearance. At 320/360/390/420 logical widths, long labels wrap. At 200% text scale, stack grids or allow scrolling; no fixed text block height or sacred-text ellipsis.
- Essential touch target≥44×44 logical units; younger-child primary tasks≥56 where A2 specifies. Decorative icons have no hit targets. Assets retain aspect ratio; no text burned into illustrations. Safe area and keyboard must never obscure the current action.
- Source frames, unrelated screens and existing design direction remain unchanged. Token/component changes require separate review; never detach or globally mutate a source instance to fix this screen.

## 6. Screen states and conditional scenarios

- Default for Parent Dashboard (landing) Applicable pending/success/error only for actions explicitly named in action_rules Cached offline read only where supported; online-only mutations show sourced reconnect reason Back/cancel restores invoking context; actual unresolved source behavior blocks execution

Owning inline components / variants (do not create unrelated standalone routes):
- {"name": "Child Switcher Chips", "entry": "Parent Dashboard", "classification": "Component", "exit": "Refreshes Dashboard for selected child"}
- {"name": "Weekly AI Report Card (preview)", "entry": "Parent Dashboard", "classification": "Component", "exit": "Full Per-Child Report (C.22)"}
- {"name": "Activity Timeline Preview", "entry": "Parent Dashboard", "classification": "Component", "exit": "Full Activity Timeline (within C.22)"}
- {"name": "Screen-Time Summary (preview)", "entry": "Parent Dashboard", "classification": "Component", "exit": "Full Screen Time & Bedtime Settings (C.23)"}
- {"name": "Module Shortcut Grid", "entry": "Parent Dashboard", "classification": "Component", "exit": "Each respective module (C.21-C.25)"}
- {"name": "Report-Delayed State (component variant)", "entry": "Weekly/Monthly report generation delay", "classification": "Component variant", "exit": "N/A (shows last-known report)"}
- {"name": "Archived/Disabled Child Read-Only Selector State", "entry": "Child Switcher, archived/disabled child selected", "classification": "Component variant", "exit": "Read-only view of that child's historical data"}
- {"name": "Empty State — Zero Activity Yet", "entry": "New family/child, no activity", "classification": "Screen variant", "exit": "N/A"}
- {"name": "Offline Dashboard State", "entry": "No connectivity", "classification": "Screen variant", "exit": "Cached data shown, module shortcuts requiring connectivity indicate this on tap"}
- {"name": "AI Insight Report Locked/Upsell State (premium-gated component)", "entry": "Non-premium plan viewing the AI Insight Report card", "classification": "Component variant", "exit": "Subscription & Billing (C.24)"}

Only apply states that belong to this surface. List-only empty/skeleton states are not added to legal documents or static intros. Network submit has a pending/timeout/retry result; retry preserves draft and must not duplicate a server-confirmed operation. Voice states need consent + OS grant; denial supplies listen/text/manual alternative. Loading/error/disabled/offline wording missing from source is a content approval gap.

<details><summary>Authoritative state/edge source context — apply screen-relevant cases, not all cases indiscriminately</summary>

### 1.10 Edge Cases

1. A parent has zero children with any activity yet (e.g., immediately post-onboarding) → the Dashboard renders with an explicit "no activity yet" empty state for the relevant components (timeline, weekly report) rather than blank/broken cards, consistent with the platform-wide explicit-empty-state philosophy.
2. A parent's only child profile is disabled (cross-ref C.21) → the Dashboard's child switcher still allows selecting that disabled child for **read-only** viewing purposes (consistent with C.21's "disabled profiles retain data and remain visible" rule), but no live/active-session actions are offered for it from here.
3. A parent has a free-tier plan with only 1 active child slot, but the family previously had more children before a downgrade (cross-ref C.24's "excess profiles become read-only archives, never silently deleted" rule) → the child switcher includes these archived profiles in a clearly-distinguished, read-only-labeled state, not mixed in indistinguishably with active children.
4. Analytics/report data for a specific child is delayed beyond the normal generation window (e.g., a backend processing delay) → the affected card shows the explicit delayed-state messaging (FR-11) rather than other Dashboard components being blocked waiting on it — each component degrades independently.
5. A parent's premium subscription (which gates the AI Insight Report specifically, per FR-8) expires or downgrades while they're viewing the Dashboard → the AI Insight Report component reflects the new entitlement state on next load (showing an upsell/locked state appropriately, since this is a parent surface where such messaging is explicitly permitted per FR-10), without crashing or showing stale premium content past expiry.
6. Two parents (co-guardians) on different devices view the Dashboard for the same family simultaneously → each sees their own independently-rendered Dashboard (per their own device's session/grace-window state per C.19), with no shared "currently viewing" lock or conflict — this is a read-mostly screen, not a collaborative-editing surface requiring such coordination.
7. A parent taps a module shortcut (e.g., Child Management) and then uses the back button to return to the Dashboard → the Dashboard re-renders from cache instantly rather than re-fetching everything from scratch, with a background refresh if the cache is stale, consistent with the platform's general cache-then-refresh pattern.
8. A request reaches a Dashboard API with a parent-session token that has technically expired or been revoked (e.g., the parent logged out on another device) → rejected with a standard re-authentication flow, not confused with the child-mode-token-rejection rule (FR-6), which is a distinct, additional check beyond ordinary session validity.
9. A family's weekly report contains AI-generated content that, due to a model error, drifts toward language resembling a developmental/behavioral observation about a specific child → this must be caught by the content-safety validation pipeline (mirroring the platform's established pattern for AI-generated content elsewhere) before ever reaching the Dashboard, never relying on the parent to simply not notice or not mind.

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Weekly/monthly report generation delayed | Last successfully generated report shown with explicit "as of [date]" timestamp (FR-11) |
| Child-mode token used on any Dashboard API | Outright rejection, regardless of family/child ownership (FR-6) |
| Web portal access attempt | Blocked by design — no route exists (FR-12) |
| Individual component data fetch failure (e.g., activity timeline) | That specific component shows a graceful "may be unavailable right now" state; other components unaffected |
| AI-generated content failing content-safety validation | Suppressed/excluded from display rather than shown unfiltered (Edge Case 9) |

### 1.12 Empty States
- Zero activity yet for the selected child → explicit "Once [Child] starts learning, you'll see their progress here" framing across the relevant components, never a blank/broken-looking chart.

### 1.13 Loading States
- Dashboard: skeleton shimmer for each component independently (child switcher chips load fast/first; weekly report and timeline may resolve slightly later without blocking the rest of the screen).

### 1.14 Offline States
- Dashboard renders from last-cached data when offline, with a clear "may be outdated" indicator; module shortcuts requiring connectivity show this clearly on tap rather than navigating into a broken destination screen.

### 1.15 Permission States
- No new runtime permissions; this screen is purely a data-aggregation/navigation surface.



</details>

## 7. Interactions and navigation

- Select child chip → refresh independent report/activity/usage slices for that child
  View Full Report → Per-Child Report with selected child
  See all activity → Full Activity Timeline, never unrelated learning screen
  Screen-time preview → Screen Time Settings; bedtime control → Bedtime Settings
  Module shortcuts → Child Management, Reports, Controls, Subscription, Notifications, Support, Settings respectively
  Premium AI insight lock → parent Subscription; family trends → aggregate-only Monthly Family Report

For every action below, use the cited preconditions and source validation. Preserve the invoking route and selected child. Back/cancel dismisses only the current overlay or returns to the invoking screen, preserving drafts and completed progress where specified. Unavailable actions remain visibly labeled with their reason and never activate. Permission prompts occur only after parent consent and a deliberate related action. A prototype simulates outcomes; it never validates identity, grants permissions, charges money or mutates production data.

Verified current-preview controls, retained to prevent omitted clickable elements:

- {"disabled": false, "label": "Go back", "placeholder": null, "tag": "BUTTON", "text": "", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Default", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "⏳ Loading", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "📶 Offline", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "📭 Empty", "type": null}
- {"disabled": false, "label": "View Aisha's dashboard", "placeholder": null, "tag": "BUTTON", "text": "👧\nAisha", "type": null}
- {"disabled": false, "label": "View Omar's dashboard", "placeholder": null, "tag": "BUTTON", "text": "👦\nOmar", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "View Full Report", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "See all", "type": null}
- {"disabled": false, "label": "Completed: Prophet Yusuf story, 2 hours ago", "placeholder": null, "tag": "BUTTON", "text": "📖\n\nCompleted: Prophet Yusuf story\n\n2 hours ago", "type": null}
- {"disabled": false, "label": "Checked off: Evening dua, 5 hours ago", "placeholder": null, "tag": "BUTTON", "text": "✓\n\nChecked off: Evening dua\n\n5 hours ago", "type": null}
- {"disabled": false, "label": "Earned: 7-Day Streak badge, Yesterday", "placeholder": null, "tag": "BUTTON", "text": "🏆\n\nEarned: 7-Day Streak badge\n\nYesterday", "type": null}
- {"disabled": false, "label": "Completed: Prophet Stories quiz practice, Yesterday", "placeholder": null, "tag": "BUTTON", "text": "🧠\n\nCompleted: Prophet Stories quiz practice\n\nYesterday", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Manage Screen Time", "type": null}
- {"disabled": false, "label": "Children", "placeholder": null, "tag": "BUTTON", "text": "👧\nChildren", "type": null}
- {"disabled": false, "label": "Reports", "placeholder": null, "tag": "BUTTON", "text": "📊\nReports", "type": null}
- {"disabled": false, "label": "Settings", "placeholder": null, "tag": "BUTTON", "text": "⚙️\nSettings", "type": null}
- {"disabled": false, "label": "Subscription", "placeholder": null, "tag": "BUTTON", "text": "💳\nSubscription", "type": null}
- {"disabled": false, "label": "Support", "placeholder": null, "tag": "BUTTON", "text": "💬\nSupport", "type": null}

For any captured control absent from an explicit action above, reconcile it against the screen-specific source below before wiring. Do not connect it to a convenient unrelated screen. Mark it **unresolved, non-executable** until its actual destination/state is confirmed; the navigation appendix reports this limitation. Decorative source-layer names are not automatically click targets.

<details><summary>Screen-specific PRD specification / click behavior</summary>

Screen: Parent Dashboard (landing)
Source PRD_Documents/Parent Area In-App (19-26)/Feature_C20_Parent_Dashboard.md §1.18 row 1; §1.7; §2; §6; §13
Purpose: Give a verified parent a single-child-at-a-time overview with trustworthy freshness and shortcuts to every parent module. Screen-specific role: Parent Dashboard (landing).
Fields: Child selector; Milestones/course/lesson/Quran/story/quiz/habit/streak summaries; Badges; Weekly/monthly report previews; Screen-time and bedtime status; AI reasons and safe history link; Plan capacity; As-of timestamp
Action contract:
Select child chip → refresh independent report/activity/usage slices for that child
View Full Report → Per-Child Report with selected child
See all activity → Full Activity Timeline, never unrelated learning screen
Screen-time preview → Screen Time Settings; bedtime control → Bedtime Settings
Module shortcuts → Child Management, Reports, Controls, Subscription, Notifications, Support, Settings respectively
Premium AI insight lock → parent Subscription; family trends → aggregate-only Monthly Family Report
States:
Default for Parent Dashboard (landing) Applicable pending/success/error only for actions explicitly named in action_rules Cached offline read only where supported; online-only mutations show sourced reconnect reason Back/cancel restores invoking context; actual unresolved source behavior blocks execution

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
3. Create `NH/Enhanced/157/Parent_Dashboard_landing/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Parent_Dashboard_landing`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] C20 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
