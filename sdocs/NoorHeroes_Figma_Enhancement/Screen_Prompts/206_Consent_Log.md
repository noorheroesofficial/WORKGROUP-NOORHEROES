**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 206 — Consent Log

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **C26 — Consent Log**.
- Surface: **screen**. Number is controlled review order, not a forced linear user journey.
- Execution status: **Reference available; unresolved conflicts require approval before design**.
- Journey entry / previous screen: Privacy & Support.
- Next screen(s) / result: Consent Detail / Withdraw Confirmation.
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_C26_Privacy_Consent_Account_Security_Data_Rights.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Parent Area In-App (19-26)/Feature_C26_Privacy_Consent_Account_Security_Data_Rights.md>); **§1.18 row 6; §1.7; §2; §6; §13**.
- Current mobile reference: [NoorHeroes current preview](https://noorheroes.figma.site/) → selector **Consent Log**; exact text captured below.
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: [Consent Log Settings](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1117-10626) — `1117:10626`. 
- Frame 2 container: `1085:13003`; visual reference: **Missing corresponding screen reference.** Do not substitute a visually related hub as functional evidence.
- Reference qualification: No independently verified equivalent for this screen; global style inspiration must not replace approved copy.
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- [Consent Log-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Privacy/Consent Log-01.png>)
- [Consent Log-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Privacy/Consent Log-02.png>)
- [Consent Log-03.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Privacy/Consent Log-03.png>)
- [Consent Log-04.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Privacy/Consent Log-04.png>)
- [Consent Log-05.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Privacy/Consent Log-05.png>)
- [Consent Log-06.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Privacy/Consent Log-06.png>)
- Blueprint alignment:
- [01-settings-privacy-navigation-hub.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C26_Privacy_Consent_Account_Security_Data_Rights/KMP/01-settings-privacy-navigation-hub.md>)
- [02-consent-log-withdrawal-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C26_Privacy_Consent_Account_Security_Data_Rights/KMP/02-consent-log-withdrawal-flow.md>)
- [03-ai-interaction-history-screen.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C26_Privacy_Consent_Account_Security_Data_Rights/KMP/03-ai-interaction-history-screen.md>)
- [04-account-security-device-session-management.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C26_Privacy_Consent_Account_Security_Data_Rights/KMP/04-account-security-device-session-management.md>)
- [05-family-language-picker.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C26_Privacy_Consent_Account_Security_Data_Rights/KMP/05-family-language-picker.md>)
- [06-data-export-request-status-tracking.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C26_Privacy_Consent_Account_Security_Data_Rights/KMP/06-data-export-request-status-tracking.md>)
- [07-settings-exit-actions-logout-deletion-entry.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C26_Privacy_Consent_Account_Security_Data_Rights/KMP/07-settings-exit-actions-logout-deletion-entry.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: - P-C21-02: C25 FR-8 points to C21 FR-8 step 7 for account deletion cancellation; actual C21 FR-8 governs plan capacity. C26 links full account deletion into C21, but C21 has only child-deletion screens. Full account deletion warning, 7-day countdown, pending access policy and support-cancellation destination need authoritative reconciliation, not invention.
- P-C26-01: C22 AI history is flags/safety events only (FR-5/13); C26 history is write-time-redacted input/output summaries with model_version/policy_result/expires_at (FR-6/7). Treat distinct scoped views or seek approval for merge; do not silently present full history in safety-only report.
- P-C26-02: Blueprint boilerplate suggests XP particles/Islamic illustrations/runtime camera-microphone-storage permissions on all mapped screens. PRD privacy/deletion/security surfaces do not require these; specificity and sober parent register take precedence. See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Give parents granular consent, safe AI-history, account security, language and asynchronous family data-rights controls. Screen-specific role: Consent Log.

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

The complete feature obligations are retained in [every-FR register](../10_REQUIREMENT_COVERAGE_REGISTER.md); section 2 identifies the exact screen-inventory row.

## 4. Exact content specification

### Current mobile source — exact captured text

```text
Consent Log

Required consents cannot be withdrawn while you have an active account. You can withdraw Optional consents at any time.

REQUIRED CONSENTS

Terms of Service & Privacy Policy

Granted
Required

Last changed Jun 12, 2025

Required to use NoorHeroes. Covers data handling, user rights, and platform rules.

Child Data Processing

Granted
Required

Last changed Jun 12, 2025

Required processing of your child's learning data to provide the service.

Age Verification

Granted
Required

Last changed Jun 12, 2025

You confirmed the child using this profile is under 13.

OPTIONAL CONSENTS

Personalization & AI Recommendations

Granted
Optional

Last changed Jun 12, 2025

Enables AI-powered content recommendations based on learning history.

Withdraw

Analytics & Product Improvement

Granted
Optional

Last changed Jun 12, 2025

Anonymised usage data helps us improve the app for all children.

Withdraw

Marketing Communications

Withdrawn
Optional

Last changed Jun 20, 2025

Occasional emails about new features, content, and promotions.

Re-grant
```

### Frame 1 — exact layer text (separate source; differences need approval)

```text
Consent Log
Required consents cannot be withdrawn while
you have an active account. You can withdraw
Optional consents at any time.
REQUIRED CONSENTS
Terms of Service & Privacy
Policy
Granted
Required
Last changed Jun 12, 2025
Required to use NoorHeroes. Covers data handling,
user rights, and platform rules.
By using NoorHeroes, you agree to our Terms of
Service and Privacy Policy. These govern your
account, data handling, and use of the platform.
Read full consent text
›
Child Data Processing
Granted
Required
Last changed Jun 12, 2025
Required processing of your child's learning data to
provide the service.
Age Verification
Granted
Required
Last changed Jun 12, 2025
You confirmed the child using this profile is under 13.
OPTIONAL CONSENTS
Personalization & AI
Recommendations
Granted
Withdraw
Optional
Last changed Jun 12, 2025
Enables AI-powered content recommendations based
on learning history.
Withdraw this consent?
Withdrawing "Personalization & AI
Recommendations" will disable features that rely
on it. This takes effect immediately.
Cancel
Withdraw
Analytics & Product
Improvement
Granted
Withdraw
Optional
Last changed Jun 12, 2025
Anonymised usage data helps us improve the app for all
children.
We collect anonymised, aggregated usage data to
improve app performance and feature quality. No
personally identifiable data is shared externally.
Read full consent text
›
Marketing
Communications
Withdrawn
Re-grant
Optional
Last changed Jun 20, 2025
Occasional emails about new features, content, and
promotions.
Consent withdrawn. Changes take effect
immediately.
```

### Requirement-driven fields and content roles

- Consent name/status/last-changed date
- Required/optional tag
- Full detail entry

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Show consent name/status/date/required-optional tags in readable rows; full governed text opens Detail.
- Required rows use information action, never off toggle. Optional withdrawal confirmation explains sourced consequence with equally available Cancel.
- Do not add export indicator, language controls or AI history sections to consent screens.

- Preserve content order and screen purpose. Use a vertical auto-layout content stack; horizontal inset 20, base spacing 4/8/12/16/24/32; card content padding 12–16. Keep compact controls next to their labels; align headings and cards to one column edge.
- Use existing cream `#FAF7F0`, surface `#FFFFFF`, ink `#1C2B33`, teal `#0E7C7B`, gold `#D4A24C`. Gold/bright teal are accents, not untested small-text colors. Body 14/16; heading 20/24; brand-only display 28/32. Preserve actual font assets; PRD Latin sans, display serif, separate verified Arabic content font.
- Do not import Frame 2's sample statistics, claims, religious text, section additions or combined desktop layouts. Borrow hierarchy, restrained surface separation and image framing only where they support this surface.
- Screen viewport is separate from long content height. Use vertical overflow when content exceeds available height; header/footer may be fixed only with bottom and top content clearance. At 320/360/390/420 logical widths, long labels wrap. At 200% text scale, stack grids or allow scrolling; no fixed text block height or sacred-text ellipsis.
- Essential touch target≥44×44 logical units; younger-child primary tasks≥56 where A2 specifies. Decorative icons have no hit targets. Assets retain aspect ratio; no text burned into illustrations. Safe area and keyboard must never obscure the current action.
- Source frames, unrelated screens and existing design direction remain unchanged. Token/component changes require separate review; never detach or globally mutate a source instance to fix this screen.

## 6. Screen states and conditional scenarios

- Loading cached consent rows/detail
- Required consent informational only → deletion explanation
- Optional withdrawal confirmation and fresh step-up
- Granted/Withdrawn after ledger update
- Offline cached view; mutation requires reconnect
- Failure retry preserves current ledger
- AI/voice field updates C23 shared state



Only apply states that belong to this surface. List-only empty/skeleton states are not added to legal documents or static intros. Network submit has a pending/timeout/retry result; retry preserves draft and must not duplicate a server-confirmed operation. Voice states need consent + OS grant; denial supplies listen/text/manual alternative. Loading/error/disabled/offline wording missing from source is a content approval gap.

<details><summary>Authoritative state/edge source context — apply screen-relevant cases, not all cases indiscriminately</summary>

### 1.10 Edge Cases

1. A parent withdraws the marketing consent, then later wants to re-grant it (e.g., decides they do want promotional emails after all) → re-granting an optional consent is supported as a straightforward toggle-back-on action, creating a new consent-ledger entry (consistent with A.1's append-only, versioned consent-recording pattern) rather than attempting to "undelete" the prior withdrawal record.
2. A parent requests a data export, then immediately requests a second one before the first completes → the second request either queues behind the first or is recognized as a duplicate-in-progress request (returning the existing request's status rather than spawning a redundant parallel export job) — implementation may choose either approach, but the parent must never see two simultaneously-conflicting "your export is ready" notifications for what should be one logical export.
3. An AI interaction occurs for a child whose family later requests full account deletion, and the 7-day grace period elapses → the AI Interaction History records for that family are subject to the same cascade-deletion/legal-retention rules as all other family data (cross-ref C.21's cascade worker), not independently retained beyond what's legally required.
4. A parent's AI Interaction History query spans a period with zero AI interactions (e.g., AI was disabled for that child the whole time) → shows an explicit "No AI interactions in this period" state, consistent with C.22's established empty-state pattern for the same conceptual absence.
5. A parent revokes a device that is, at that exact moment, in the middle of an active data-export-status poll from that same device → the in-flight read request may complete (read-only, low-risk), but any subsequent request from that revoked device fails authentication immediately after, consistent with C.23's established device-revocation timing pattern.
6. A parent changes the family-level language preference while a specific child has their own individually-overridden display language (per B.16) → the child's own override is unaffected; this screen's language picker only affects the family/parent-level default and any child without their own override.
7. A data export request is made for a family with a very large amount of historical data (long-tenured, many children) → the export job may take longer; the async status model already accommodates this via its "preparing" state, with no different handling needed beyond what the async design already provides.
8. A parent attempts to view AI Interaction History for a child whose AI has always been disabled (never enabled) → shows a friendly empty state distinct from "no interactions this period" — something like "AI has been off for this child the entire time," reinforcing that the absence is by configuration, not a missing-data issue worth flagging as suspicious.

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Data export request fails to start (backend issue) | Clear retry option, never a silent failure |
| Duplicate export request while one is in-progress | Recognized and deduplicated, or queued; never two conflicting "ready" states |
| Consent withdrawal attempted on a required consent | Routed to the account-deletion explanation rather than a toggle action |
| PIN reset / device revocation failure | Standard C.19 error handling reused, no separate error path |
| Logout attempted with unsynced downloads | Confirmation prompt required before proceeding (FR-4) |

### 1.12 Empty States
- Zero AI interactions ever (AI always disabled) → distinct "AI has been off the entire time" framing (Edge Case 8).
- Zero AI interactions in a selected period (AI enabled but unused) → "No AI interactions in this period" framing (Edge Case 4).
- Zero data-export history yet → friendly "Request your first export anytime" framing.

### 1.13 Loading States
- Settings/Privacy screens: skeleton list shimmer for Consent Log, AI Interaction History, device list.

### 1.14 Offline States
- Settings screens render last-cached data offline; export requests, consent withdrawal, PIN reset, and device revocation all require connectivity and indicate this clearly if attempted offline.

### 1.15 Permission States
- No new runtime permissions; relies entirely on the existing step-up authentication gate (C.19).



</details>

## 7. Interactions and navigation

- Consent row/info → Consent Detail full governed text/status
  Optional Withdraw → fresh Parent Gate → Withdraw Optional Consent Confirmation; confirm appends withdrawal
  Optional regrant → append granted consent ledger entry
  Required info/withdrawal attempt → required-consent deletion explanation, not toggle off
  AI/voice withdrawal → same shared AI settings as C23; cross-screen state updates
  Back → invoking Privacy & Support/Settings

For every action below, use the cited preconditions and source validation. Preserve the invoking route and selected child. Back/cancel dismisses only the current overlay or returns to the invoking screen, preserving drafts and completed progress where specified. Unavailable actions remain visibly labeled with their reason and never activate. Permission prompts occur only after parent consent and a deliberate related action. A prototype simulates outcomes; it never validates identity, grants permissions, charges money or mutates production data.

Verified current-preview controls, retained to prevent omitted clickable elements:

- {"disabled": false, "label": "Go back", "placeholder": null, "tag": "BUTTON", "text": "", "type": null}
- {"disabled": false, "label": "Terms of Service & Privacy Policy, Required, granted", "placeholder": null, "tag": "BUTTON", "text": "Terms of Service & Privacy Policy\n\nGranted\nRequired\n\nLast changed Jun 12, 2025\n\nRequired to use NoorHeroes. Covers data handling, user rights, and platform rules.", "type": null}
- {"disabled": false, "label": "This consent is required to use NoorHeroes", "placeholder": null, "tag": "BUTTON", "text": "", "type": null}
- {"disabled": false, "label": "Child Data Processing, Required, granted", "placeholder": null, "tag": "BUTTON", "text": "Child Data Processing\n\nGranted\nRequired\n\nLast changed Jun 12, 2025\n\nRequired processing of your child's learning data to provide the service.", "type": null}
- {"disabled": false, "label": "This consent is required to use NoorHeroes", "placeholder": null, "tag": "BUTTON", "text": "", "type": null}
- {"disabled": false, "label": "Age Verification, Required, granted", "placeholder": null, "tag": "BUTTON", "text": "Age Verification\n\nGranted\nRequired\n\nLast changed Jun 12, 2025\n\nYou confirmed the child using this profile is under 13.", "type": null}
- {"disabled": false, "label": "This consent is required to use NoorHeroes", "placeholder": null, "tag": "BUTTON", "text": "", "type": null}
- {"disabled": false, "label": "Personalization & AI Recommendations, Optional, granted", "placeholder": null, "tag": "BUTTON", "text": "Personalization & AI Recommendations\n\nGranted\nOptional\n\nLast changed Jun 12, 2025\n\nEnables AI-powered content recommendations based on learning history.", "type": null}
- {"disabled": false, "label": "Withdraw consent for Personalization & AI Recommendations", "placeholder": null, "tag": "BUTTON", "text": "Withdraw", "type": null}
- {"disabled": false, "label": "Analytics & Product Improvement, Optional, granted", "placeholder": null, "tag": "BUTTON", "text": "Analytics & Product Improvement\n\nGranted\nOptional\n\nLast changed Jun 12, 2025\n\nAnonymised usage data helps us improve the app for all children.", "type": null}
- {"disabled": false, "label": "Withdraw consent for Analytics & Product Improvement", "placeholder": null, "tag": "BUTTON", "text": "Withdraw", "type": null}
- {"disabled": false, "label": "Marketing Communications, Optional, withdrawn", "placeholder": null, "tag": "BUTTON", "text": "Marketing Communications\n\nWithdrawn\nOptional\n\nLast changed Jun 20, 2025\n\nOccasional emails about new features, content, and promotions.", "type": null}
- {"disabled": false, "label": "Re-grant consent for Marketing Communications", "placeholder": null, "tag": "BUTTON", "text": "Re-grant", "type": null}

For any captured control absent from an explicit action above, reconcile it against the screen-specific source below before wiring. Do not connect it to a convenient unrelated screen. Mark it **unresolved, non-executable** until its actual destination/state is confirmed; the navigation appendix reports this limitation. Decorative source-layer names are not automatically click targets.

<details><summary>Screen-specific PRD specification / click behavior</summary>

Screen: Consent Log
Source PRD_Documents/Parent Area In-App (19-26)/Feature_C26_Privacy_Consent_Account_Security_Data_Rights.md §1.18 row 6; §1.7; §2; §6; §13
Purpose: Give parents granular consent, safe AI-history, account security, language and asynchronous family data-rights controls. Screen-specific role: Consent Log.
Fields: Consent name/status/last-changed date; Required/optional tag; Full detail entry
Action contract:
Consent row/info → Consent Detail full governed text/status
Optional Withdraw → fresh Parent Gate → Withdraw Optional Consent Confirmation; confirm appends withdrawal
Optional regrant → append granted consent ledger entry
Required info/withdrawal attempt → required-consent deletion explanation, not toggle off
AI/voice withdrawal → same shared AI settings as C23; cross-screen state updates
Back → invoking Privacy & Support/Settings
States:
Loading cached consent rows/detail
Required consent informational only → deletion explanation
Optional withdrawal confirmation and fresh step-up
Granted/Withdrawn after ledger update
Offline cached view; mutation requires reconnect
Failure retry preserves current ledger
AI/voice field updates C23 shared state

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
3. Create `NH/Enhanced/206/Consent_Log/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Consent_Log`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] C26 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
