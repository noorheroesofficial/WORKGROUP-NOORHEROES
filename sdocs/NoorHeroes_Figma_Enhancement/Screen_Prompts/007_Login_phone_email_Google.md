**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 007 — Login (phone/email + Google)

**Current status — 13 October 2026:** User approved the [Login copy and layout proposal](../Evidence/007_Login_Readiness_and_Copy_Proposal.md). Screen 007 is implemented for review in Onboarding at 390 × 844; [execution report and prototype limits](../Evidence/007_Login_Execution_Review.md). Phone default: `1278:155`; Email default: `1278:780`. This update supersedes the historical copy blocker and old multi-width instructions below. Stop after this screen.

## 1. Screen identification

- Feature/sub-feature: **A1 — Login (phone/email + Google)**.
- Surface: **screen**. Number is controlled review order, not a forced linear user journey.
- Execution status: **Documentation prepared; approval and any copy gaps resolved before Figma execution**.
- Journey entry / previous screen: Intro, session expiry, logout, switch account.
- Next screen(s) / result: OTP Verification, Registration.
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_A1_Splash_Auth_Onboarding.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Child App (1-12)/Feature_A1_Splash_Auth_Onboarding.md>); **§1.18 row 7; §1.7; §2.4**.
- Current mobile reference: **Missing independently mapped current-site screen.**
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: **Missing corresponding screen reference.** Do not substitute a visually related hub as functional evidence.
- Frame 2 container: `1085:13003`; visual reference: **Missing corresponding screen reference.** Do not substitute a visually related hub as functional evidence.
- Reference qualification: Any feature-hub mapping is visual-only; compare exact screen identity before execution..
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- Missing corresponding local screen reference.
- Blueprint alignment:
- [01-splash-bootstrap-update-gating-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A1_Splash_Auth_Onboarding/KMP/01-splash-bootstrap-update-gating-flow.md>)
- [02-language-selection-intro-onboarding-sequence.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A1_Splash_Auth_Onboarding/KMP/02-language-selection-intro-onboarding-sequence.md>)
- [03-registration-consent-otp-verification-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A1_Splash_Auth_Onboarding/KMP/03-registration-consent-otp-verification-flow.md>)
- [04-google-sign-in-authentication-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A1_Splash_Auth_Onboarding/KMP/04-google-sign-in-authentication-flow.md>)
- [05-parent-pin-biometric-enrollment-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A1_Splash_Auth_Onboarding/KMP/05-parent-pin-biometric-enrollment-flow.md>)
- [06-add-child-profile-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A1_Splash_Auth_Onboarding/KMP/06-add-child-profile-flow.md>)
- [07-onboarding-draft-persistence-resume-offline-sync.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A1_Splash_Auth_Onboarding/KMP/07-onboarding-draft-persistence-resume-offline-sync.md>)
- [08-profile-picker-child-lock-first-mission-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A1_Splash_Auth_Onboarding/KMP/08-profile-picker-child-lock-first-mission-flow.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: - G-01
- G-02
- G-03 See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Authenticate returning parent through phone/email OTP or Google.

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

The complete feature obligations are retained in [every-FR register](../10_REQUIREMENT_COVERAGE_REGISTER.md); section 2 identifies the exact screen-inventory row.

## 4. Exact content specification

### Requirement-driven fields and content roles

- Phone/email segmented control
- Identifier input
- Country selector for phone
- Google button
- Register link
- Forgot Access

**Copy gap resolved by explicit user approval:** “Use the proposed Login copy and layout.” Use the exact strings in [the approved proposal](../Evidence/007_Login_Readiness_and_Copy_Proposal.md). There is still no original standalone Login frame; the proposal is an approved requirement-driven addition, not a discovered original reference. Test fixtures and prototype limitations are recorded in the execution review.

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Single column identity form; prominent one submit; Google secondary; recovery always readable.

- Preserve content order and screen purpose. Use a vertical auto-layout content stack; horizontal inset 20, base spacing 4/8/12/16/24/32; card content padding 12–16. Keep compact controls next to their labels; align headings and cards to one column edge.
- Use existing cream `#FAF7F0`, surface `#FFFFFF`, ink `#1C2B33`, teal `#0E7C7B`, gold `#D4A24C`. Gold/bright teal are accents, not untested small-text colors. Body 14/16; heading 20/24; brand-only display 28/32. Preserve actual font assets; PRD Latin sans, display serif, separate verified Arabic content font.
- Do not import Frame 2's sample statistics, claims, religious text, section additions or combined desktop layouts. Borrow hierarchy, restrained surface separation and image framing only where they support this surface.
- Screen viewport is separate from long content height. Use vertical overflow when content exceeds available height; header/footer may be fixed only with bottom and top content clearance. At 320/360/390/420 logical widths, long labels wrap. At 200% text scale, stack grids or allow scrolling; no fixed text block height or sacred-text ellipsis.
- Essential touch target≥44×44 logical units; younger-child primary tasks≥56 where A2 specifies. Decorative icons have no hit targets. Assets retain aspect ratio; no text burned into illustrations. Safe area and keyboard must never obscure the current action.
- Source frames, unrelated screens and existing design direction remain unchanged. Token/component changes require separate review; never detach or globally mutate a source instance to fix this screen.

## 6. Screen states and conditional scenarios

- Empty
- Invalid format
- Sending OTP
- Generic server error
- Offline
- Session expired



Only apply states that belong to this surface. List-only empty/skeleton states are not added to legal documents or static intros. Network submit has a pending/timeout/retry result; retry preserves draft and must not duplicate a server-confirmed operation. Voice states need consent + OS grant; denial supplies listen/text/manual alternative. Loading/error/disabled/offline wording missing from source is a content approval gap.

<details><summary>Authoritative state/edge source context — apply screen-relevant cases, not all cases indiscriminately</summary>

### 1.10 Edge Cases

1. Parent enters a phone number already registered to a different family → enumeration-safe generic OTP flow proceeds; if OTP succeeds, route to existing account's Profile Picker (not a new registration), with a "looks like you already have an account" message shown **after** verification, never before.
2. Parent changes device language mid-onboarding (OS-level change while app is backgrounded) → app re-renders current step in new language on resume, without losing entered data.
3. Parent's OTP SMS arrives after the resend cooldown already expired and a second code was requested → both codes valid within their respective TTL windows; entering either succeeds (server tracks multiple active codes per session, not just the latest).
4. Parent attempts registration with a VOIP/disposable number flagged by carrier-lookup → allowed but flagged for elevated risk scoring; not auto-blocked unless explicit fraud policy dictates.
5. Parent loses connectivity exactly between OTP verify success and consent screen render → on reconnect, app re-fetches session state via bootstrap and resumes at Consent (token already issued server-side).
6. Two children with identical nickname and identical DOB and identical avatar are attempted → second save blocked with a clarification prompt forcing differentiation.
7. Parent's device clock is significantly skewed → OTP TTL validation must use server time, not device time, to avoid false-expired codes.
8. Parent attempts to use Google account already linked to a deleted/soft-deleted NoorHeroes family → recovery/reactivation flow triggered instead of fresh registration, with Support escalation if data retention window has lapsed.
9. Parent is mid-"Add Child" and backgrounds the app for >30 days → on return, session token has expired; app re-authenticates (silent refresh if refresh token valid, else re-login) before resuming Add Child with previously entered draft data restored locally.
10. Parent enters child DOB that implies age > 17 → system either blocks (children only) or routes to an age-band ceiling with a warning, per business policy (must be explicitly defined; default: block with explanatory copy).
11. Parent enters child DOB implying age < 3 (below supported minimum) → blocked with explanatory copy and link to support.
12. SMS OTP provider returns success but message never arrives (carrier issue) → "Resend" available immediately offers fallback channel (email or alternate SMS route) without waiting full cooldown, after first failed delivery confirmation.



</details>

## 7. Interactions and navigation

- Submit valid identifier online → OTP Verification. Google success → bootstrap-directed downstream flow. Register → Registration + Consent. Forgot access → recovery entry.
- Back returns intro or invoking expired-session context; never reveal account existence before verification.

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
| Approved forward/back action | Current frame→destination, preserving directional history | 250ms ease-in-out;no delay | Reversible with Back; cancel pending animation when leaving | Instant navigation or ≤100ms dissolve | Navigate to + Dissolve; matched-layer Smart Animate only after layer-name/structure check |
| Press/release enabled control | Rest→pressed→rest; preserve hit area | 100ms ease-out scale.96 (proposal);0ms delay | Release/cancel reverses; disabled has no activation | Color/border pressed feedback only | While pressing → Change to pressed; On click → approved action |



Timing not quoted from the PRD is a labeled design proposal. No loop, flashing or parallax is required. Animate compositor-friendly opacity/transform; never delay an enabled essential action. Stop all animation/media/recording simulation on leave; no second reward reveal on restore. Status/validation always has visible text/icon independently of motion.

## 9. Figma implementation instructions — future approved execution

1. Open the exact page/node links in section2. Confirm the source text/identity; stop if the references disagree or required copy is unavailable.
2. Locate the approved reference frame. Duplicate only that frame into a user-approved enhanced-design working area; preserve original nodes and IDs. If no frame exists, create only the missing requirement-driven surface after its layout/copy approval, using approved shared assets.
3. Create `NH/Enhanced/007/Login_phone_email_Google/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Login_phone_email_Google`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] A1 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
