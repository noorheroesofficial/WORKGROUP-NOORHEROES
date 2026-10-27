**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 194 — Support Center (landing)

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **C25 — Support Center (landing)**.
- Surface: **screen**. Number is controlled review order, not a forced linear user journey.
- Execution status: **Reference available; unresolved conflicts require approval before design**.
- Journey entry / previous screen: Parent Dashboard, Settings, Privacy & Support.
- Next screen(s) / result: FAQ Search, Contact Support Form, Ticket History.
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_C25_Notifications_Parent_Support.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Parent Area In-App (19-26)/Feature_C25_Notifications_Parent_Support.md>); **§1.18 row 7; §1.7; §2; §6; §13**.
- Current mobile reference: [NoorHeroes current preview](https://noorheroes.figma.site/) → selector **Support Center**; exact text captured below.
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: [Support Center](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1113-10319) — `1113:10319`. 
- Frame 2 container: `1085:13003`; visual reference: **Missing corresponding screen reference.** Do not substitute a visually related hub as functional evidence.
- Reference qualification: No independently verified equivalent for this screen; global style inspiration must not replace approved copy.
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- [Support Center-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Support/Support Center-01.png>)
- [Support Center-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Support/Support Center-02.png>)
- [Support Center-03.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Support/Support Center-03.png>)
- Blueprint alignment:
- [01-notifications-inbox-screen-read-state-sync.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C25_Notifications_Parent_Support/KMP/01-notifications-inbox-screen-read-state-sync.md>)
- [02-notification-preferences-safety-critical-channel-selector.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C25_Notifications_Parent_Support/KMP/02-notification-preferences-safety-critical-channel-selector.md>)
- [03-support-center-faq-search.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C25_Notifications_Parent_Support/KMP/03-support-center-faq-search.md>)
- [04-contact-support-form-ticket-history-status-tracking.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C25_Notifications_Parent_Support/KMP/04-contact-support-form-ticket-history-status-tracking.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: - P-C21-02: C25 FR-8 points to C21 FR-8 step 7 for account deletion cancellation; actual C21 FR-8 governs plan capacity. C26 links full account deletion into C21, but C21 has only child-deletion screens. Full account deletion warning, 7-day countdown, pending access policy and support-cancellation destination need authoritative reconciliation, not invention.
- P-C25-01: QA §13 reuses child-notification binding/reminder cases and says 11 edge cases, while C25 §1.10 lists 8 parent support cases. Retain parent cases and shared B17 dependency; do not invent parent journey screens from stale QA wording.
- P-C25-02: New Ticket-01.png lacks explicit safety-concern and account-deletion-cancellation category chips required by C25 FR-8/9; urgent safety email instruction has no visible address. Requires source continuation inspection and verified contact content. See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Provide parent-scoped notifications, delivery preferences and governed support with reliable ticket submission/status follow-up. Screen-specific role: Support Center (landing).

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

The complete feature obligations are retained in [every-FR register](../10_REQUIREMENT_COVERAGE_REGISTER.md); section 2 identifies the exact screen-inventory row.

## 4. Exact content specification

### Current mobile source — exact captured text

```text
Support Center

Contact Support

Send us a message

My Tickets

2

Track your requests

POPULAR TOPICS

How do I add a new child profile?

Can my child use the app without internet?

How do I change my subscription plan?

What are Noor Points and how do I earn them?

How does the parental PIN work?

Is the Quran content scholar-reviewed?

Privacy Policy
Terms of Service
Community Guidelines
```

### Frame 1 — exact layer text (separate source; differences need approval)

```text
Support Center
Search help articles, FAQs, billing...
POPULAR TOPICS
View All
Account & Security
Logins, PIN, privacy
Child Profiles
Age filters & lessons
Subscription
Plans, renewal, receipts
Screen Time
Daily limits & quiet hours
MY RECENT TICKETS
1 Active
#TK-4821
In Progress
Question about Age Filter for Surah
Stories
2d ago
Submitted
In Review
Resolved
Family Safety team is reviewing. Agent replying
soon.
FREQUENTLY ASKED QUESTIONS
How do safety notifications differ from
regular updates?
Can I set different quiet hours for each
child profile?
How does family subscription billing
work?
Support Online
Avg reply: < 2 hours
New Ticket
```

### Requirement-driven fields and content roles

- Inbox All/System/Safety/Marketing filter
- Read/unread/timestamp
- Safety-critical channel selector always on
- Marketing toggle
- Parent quiet hours
- FAQ search/results/article
- Category billing/technical/content/safety/account-deletion-cancellation/general
- Ticket subject/details/status/history/follow-up

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Screen scope: Support Center (landing). Arrange only these vertical content roles: Inbox All/System/Safety/Marketing filter → Read/unread/timestamp → Safety-critical channel selector always on → Marketing toggle → Parent quiet hours → FAQ search/results/article → Category billing/technical/content/safety/account-deletion-cancellation/general → Ticket subject/details/status/history/follow-up. Use one clear heading and context row; source-approved primary action follows this screen content. Reuse local shared components without pulling other module sections onto this screen. Retain verified source content order where it differs; required missing content requires source approval before placement.

- Preserve content order and screen purpose. Use a vertical auto-layout content stack; horizontal inset 20, base spacing 4/8/12/16/24/32; card content padding 12–16. Keep compact controls next to their labels; align headings and cards to one column edge.
- Use existing cream `#FAF7F0`, surface `#FFFFFF`, ink `#1C2B33`, teal `#0E7C7B`, gold `#D4A24C`. Gold/bright teal are accents, not untested small-text colors. Body 14/16; heading 20/24; brand-only display 28/32. Preserve actual font assets; PRD Latin sans, display serif, separate verified Arabic content font.
- Do not import Frame 2's sample statistics, claims, religious text, section additions or combined desktop layouts. Borrow hierarchy, restrained surface separation and image framing only where they support this surface.
- Screen viewport is separate from long content height. Use vertical overflow when content exceeds available height; header/footer may be fixed only with bottom and top content clearance. At 320/360/390/420 logical widths, long labels wrap. At 200% text scale, stack grids or allow scrolling; no fixed text block height or sacred-text ellipsis.
- Essential touch target≥44×44 logical units; younger-child primary tasks≥56 where A2 specifies. Decorative icons have no hit targets. Assets retain aspect ratio; no text burned into illustrations. Safe area and keyboard must never obscure the current action.
- Source frames, unrelated screens and existing design direction remain unchanged. Token/component changes require separate review; never detach or globally mutate a source instance to fix this screen.

## 6. Screen states and conditional scenarios

- Default for Support Center (landing) Applicable pending/success/error only for actions explicitly named in action_rules Cached offline read only where supported; online-only mutations show sourced reconnect reason Back/cancel restores invoking context; actual unresolved source behavior blocks execution



Only apply states that belong to this surface. List-only empty/skeleton states are not added to legal documents or static intros. Network submit has a pending/timeout/retry result; retry preserves draft and must not duplicate a server-confirmed operation. Voice states need consent + OS grant; denial supplies listen/text/manual alternative. Loading/error/disabled/offline wording missing from source is a content approval gap.

<details><summary>Authoritative state/edge source context — apply screen-relevant cases, not all cases indiscriminately</summary>

### 1.10 Edge Cases

1. A parent mutes every notification category they can (everything except the un-mutable safety-critical ones) → the inbox still functions normally for viewing any notifications that do arrive (the safety-critical ones, plus any the parent didn't fully mute), never breaking or hiding the inbox itself based on preference state.
2. A parent submits a ticket, then submits a second, related ticket on the same topic before the first is resolved → both tickets exist independently in their ticket history (no automatic merging), though a support agent may manually link/merge them on the admin side if appropriate — the parent always sees an accurate reflection of what they actually submitted.
3. A parent's Account Deletion grace period expires (cascade completes) while they have an open, unresolved "Account Deletion Cancellation" ticket → consistent with C.21's cascade-worker boundary logic, if the ticket/cancellation wasn't actioned by Support before the deadline, the cascade proceeds as scheduled; the ticket should then be updated to reflect this outcome rather than remaining ambiguously "open" forever.
4. A parent searches the FAQ for a topic with no matching content → a clear "no results, here's how to contact Support" fallback is shown, never a dead-end blank search result.
5. A parent's billing-failure notification is configured to de-prioritized delivery (e.g., email-only, push de-prioritized) → it still must actually arrive via that remaining enabled channel; "de-prioritized" never means "sometimes doesn't arrive at all" — it's a channel/ordering preference, not a delivery-reliability reduction.
6. A parent views the Notifications inbox while offline → renders from cache with a staleness indicator; marking-as-read actions taken offline queue and sync on reconnect, consistent with the platform's general offline-action pattern.
7. A parent's ticket category is "safety concern" but the actual content, on review, turns out to be a routine billing question → support agents can recategorize a ticket on the admin side without the parent needing to resubmit; the parent's ticket-status view reflects the corrected category and any resulting SLA change transparently.
8. Two co-guardians on different devices both submit feedback/tickets about the same underlying issue independently → each ticket is tracked separately (consistent with Edge Case 2's no-auto-merge default), with support agents responsible for recognizing and coordinating related tickets manually if warranted.

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| FAQ search returns zero results | Clear "no results, contact Support" fallback (Edge Case 4) |
| Ticket submission fails (network) | Local draft preserved, retried, never silently lost |
| Notifications inbox fetch failure | Cached last-known list shown with a staleness indicator |
| Mark-as-read action fails (network) | Optimistic local update, queued for retry, never blocks further interaction |
| Safety-critical notification delivery channel itself fails (e.g., push token invalid) | Falls back to the next enabled channel (e.g., email) rather than silently failing to deliver at all |

### 1.12 Empty States
- Zero notifications yet (new account) → friendly "Nothing here yet" empty state.
- Zero ticket history yet → friendly "You haven't contacted Support yet — search our FAQ or reach out anytime" framing.

### 1.13 Loading States
- Notifications inbox / Support Center: skeleton list shimmer.

### 1.14 Offline States
- Notifications inbox renders from cache; FAQ search and ticket submission require connectivity, indicated clearly if attempted offline.

### 1.15 Permission States
- No new runtime permissions; relies on the existing OS notification-permission state already governed by the platform's general notification infrastructure (B.17).



</details>

## 7. Interactions and navigation

- Entry: Parent Dashboard, Settings, Privacy & Support. Primary result: FAQ Search, Contact Support Form, Ticket History. Apply only the named screen required_fields; parent-sensitive mutations pass fresh C19 gate. Back/cancel returns to invoking surface without committing. Exact unspecified controls/copy remain approval gaps.

For every action below, use the cited preconditions and source validation. Preserve the invoking route and selected child. Back/cancel dismisses only the current overlay or returns to the invoking screen, preserving drafts and completed progress where specified. Unavailable actions remain visibly labeled with their reason and never activate. Permission prompts occur only after parent consent and a deliberate related action. A prototype simulates outcomes; it never validates identity, grants permissions, charges money or mutates production data.

Verified current-preview controls, retained to prevent omitted clickable elements:

- {"disabled": false, "label": "Go back", "placeholder": null, "tag": "BUTTON", "text": "", "type": null}
- {"disabled": false, "label": "Search frequently asked questions", "placeholder": "Search help articles…", "tag": "INPUT", "text": "", "type": "search"}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Contact Support\n\nSend us a message", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "My Tickets\n\n2\n\nTrack your requests", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "How do I add a new child profile?", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Can my child use the app without internet?", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "How do I change my subscription plan?", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "What are Noor Points and how do I earn them?", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "How does the parental PIN work?", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Is the Quran content scholar-reviewed?", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Privacy Policy", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Terms of Service", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Community Guidelines", "type": null}

For any captured control absent from an explicit action above, reconcile it against the screen-specific source below before wiring. Do not connect it to a convenient unrelated screen. Mark it **unresolved, non-executable** until its actual destination/state is confirmed; the navigation appendix reports this limitation. Decorative source-layer names are not automatically click targets.

<details><summary>Screen-specific PRD specification / click behavior</summary>

Screen: Support Center (landing)
Source PRD_Documents/Parent Area In-App (19-26)/Feature_C25_Notifications_Parent_Support.md §1.18 row 7; §1.7; §2; §6; §13
Purpose: Provide parent-scoped notifications, delivery preferences and governed support with reliable ticket submission/status follow-up. Screen-specific role: Support Center (landing).
Fields: Inbox All/System/Safety/Marketing filter; Read/unread/timestamp; Safety-critical channel selector always on; Marketing toggle; Parent quiet hours; FAQ search/results/article; Category billing/technical/content/safety/account-deletion-cancellation/general; Ticket subject/details/status/history/follow-up
Action contract:
Entry: Parent Dashboard, Settings, Privacy & Support. Primary result: FAQ Search, Contact Support Form, Ticket History. Apply only the named screen required_fields; parent-sensitive mutations pass fresh C19 gate. Back/cancel returns to invoking surface without committing. Exact unspecified controls/copy remain approval gaps.
States:
Default for Support Center (landing) Applicable pending/success/error only for actions explicitly named in action_rules Cached offline read only where supported; online-only mutations show sourced reconnect reason Back/cancel restores invoking context; actual unresolved source behavior blocks execution

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
3. Create `NH/Enhanced/194/Support_Center_landing/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Support_Center_landing`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] C25 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
