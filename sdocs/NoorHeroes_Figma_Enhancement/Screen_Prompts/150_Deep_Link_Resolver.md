**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 150 — Deep Link Resolver

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **B17 — Deep Link Resolver**.
- Surface: **state**. Number is controlled review order, not a forced linear user journey.
- Execution status: **Pending documentation approval and screen-specific source reconciliation**.
- Journey entry / previous screen: Contextual entry in source narrative.
- Next screen(s) / result: OS push→resolve session/child/content/parent gate; offline→reconnect retry; required auth→shared gate/picker; unavailable→safe alternative/Home. Bedtime→A4; streak→A7; content→A3/A5/A6; reward→A11. No gate bypass or sibling disclosure..
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_B17_Notifications_Child_Facing.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Child App Supporting (13-18)/Feature_B17_Notifications_Child_Facing.md>); **§1.7; §1.18; §2.2–2.3; §1.10–1.15**.
- Current mobile reference: [NoorHeroes current preview](https://noorheroes.figma.site/) → selector **Deep Link Resolver**; exact text captured below.
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: [Deep Link Resolution & Fallback States - Polished](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1111-7197) — `1111:7197`. 
- Frame 2 container: `1085:13003`; visual reference: [Child Home Dashboard](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1085-16820) — `1085:16820`. 
- Reference qualification: Any feature-hub mapping is visual-only; compare exact screen identity before execution..
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- [Deep Link Resolver.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Notifications/Deep Link Resolver.png>)
- Blueprint alignment:
- [01-device-binding-lifecycle-integration.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/B17_Notifications_Child_Facing/KMP/01-device-binding-lifecycle-integration.md>)
- [02-deep-link-resolution-navigation-interception.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/B17_Notifications_Child_Facing/KMP/02-deep-link-resolution-navigation-interception.md>)
- [03-in-app-notification-banner-component.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/B17_Notifications_Child_Facing/KMP/03-in-app-notification-banner-component.md>)
- [04-notification-destination-routing-integration.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/B17_Notifications_Child_Facing/KMP/04-notification-destination-routing-integration.md>)
- [05-notifications-cross-platform-analytics-instrumentation.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/B17_Notifications_Child_Facing/KMP/05-notifications-cross-platform-analytics-instrumentation.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: - Only loading image verified; offline/unavailable exact copy absent. See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

OS push→resolve session/child/content/parent gate; offline→reconnect retry; required auth→shared gate/picker; unavailable→safe alternative/Home. Bedtime→A4; streak→A7; content→A3/A5/A6; reward→A11. No gate bypass or sibling disclosure.

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

The complete feature obligations are retained in [every-FR register](../10_REQUIREMENT_COVERAGE_REGISTER.md); section 2 identifies the exact screen-inventory row.

## 4. Exact content specification

### Current mobile source — exact captured text

```text
Content Not Available

This content isn't available right now. It may have been updated or removed.

Go to Home
```

### Frame 1 — exact layer text (separate source; differences need approval)

```text
SIMULATE DEEP LINK STATE
Live Sandbox
1. Resolving
2. Offline
3. Unavailable
4. Lock Gate
Push URI: familyapp://story/bedtime/leo/chapter-4
Incoming Link Handler
Child Mode
Handshaking Story Gate
Opening Leo's bedtime
story...
Revalidating secure family link and
checking your audio sync checkpoint.
Hold tight, tuck in the blankets and
prepare your cozy chapter.
Gate Unlocked! Redirecting to Parental
Settings...
Notifications Center
```

### Requirement-driven fields and content roles

- Opening...|Just a moment

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Loading uses centered crescent/progress and Opening.../Just a moment. Distinct unavailable state uses confirmed friendly heading/body and Go to Home. Offline/retry and gate-required states use owning shared components; no unrelated inbox or permanent navigation added.

- Preserve content order and screen purpose. Use a vertical auto-layout content stack; horizontal inset 20, base spacing 4/8/12/16/24/32; card content padding 12–16. Keep compact controls next to their labels; align headings and cards to one column edge.
- Use existing cream `#FAF7F0`, surface `#FFFFFF`, ink `#1C2B33`, teal `#0E7C7B`, gold `#D4A24C`. Gold/bright teal are accents, not untested small-text colors. Body 14/16; heading 20/24; brand-only display 28/32. Preserve actual font assets; PRD Latin sans, display serif, separate verified Arabic content font.
- Do not import Frame 2's sample statistics, claims, religious text, section additions or combined desktop layouts. Borrow hierarchy, restrained surface separation and image framing only where they support this surface.
- Screen viewport is separate from long content height. Use vertical overflow when content exceeds available height; header/footer may be fixed only with bottom and top content clearance. At 320/360/390/420 logical widths, long labels wrap. At 200% text scale, stack grids or allow scrolling; no fixed text block height or sacred-text ellipsis.
- Essential touch target≥44×44 logical units; younger-child primary tasks≥56 where A2 specifies. Decorative icons have no hit targets. Assets retain aspect ratio; no text burned into illustrations. Safe area and keyboard must never obscure the current action.
- Source frames, unrelated screens and existing design direction remain unchanged. Token/component changes require separate review; never detach or globally mutate a source instance to fix this screen.

## 6. Screen states and conditional scenarios

- loading
- offline retry
- unavailable
- gate required
- resolved



Only apply states that belong to this surface. List-only empty/skeleton states are not added to legal documents or static intros. Network submit has a pending/timeout/retry result; retry preserves draft and must not duplicate a server-confirmed operation. Voice states need consent + OS grant; denial supplies listen/text/manual alternative. Loading/error/disabled/offline wording missing from source is a content approval gap.

<details><summary>Authoritative state/edge source context — apply screen-relevant cases, not all cases indiscriminately</summary>

Use the linked PRD §1.10–1.15 and the independently mapped states above; unspecified messages remain blocked.

</details>

## 7. Interactions and navigation

- OS push→resolve session/child/content/parent gate; offline→reconnect retry; required auth→shared gate/picker; unavailable→safe alternative/Home. Bedtime→A4; streak→A7; content→A3/A5/A6; reward→A11. No gate bypass or sibling disclosure.

For every action below, use the cited preconditions and source validation. Preserve the invoking route and selected child. Back/cancel dismisses only the current overlay or returns to the invoking screen, preserving drafts and completed progress where specified. Unavailable actions remain visibly labeled with their reason and never activate. Permission prompts occur only after parent consent and a deliberate related action. A prototype simulates outcomes; it never validates identity, grants permissions, charges money or mutates production data.

Verified current-preview controls, retained to prevent omitted clickable elements:

- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Go to Home", "type": null}

For any captured control absent from an explicit action above, reconcile it against the screen-specific source below before wiring. Do not connect it to a convenient unrelated screen. Mark it **unresolved, non-executable** until its actual destination/state is confirmed; the navigation appendix reports this limitation. Decorative source-layer names are not automatically click targets.

<details><summary>Screen-specific PRD specification / click behavior</summary>

#### Screen: Deep Link Resolution States

- **Purpose:** Safely and transparently resolve a notification tap into the correct, validated destination.
- **Components:** Loading spinner/branded indicator; for the offline case, a friendly "Connect to the internet to open this" message with a retry action; for the content-unavailable case, a graceful "this isn't available right now" message with a suggested alternative, consistent with the platform's established withdrawn-content UX pattern (A.3/A.6).
- **States:** Resolving (loading), Offline, Content-unavailable, Requires-lock-gate (routes into the shared Lock Gate from A.1/B.16), Success (lands on destination).



</details>

## 8. Motion and animation specification

| Trigger | Start → end / direction | Timing | Interruption / leave | Reduced motion | Figma approach |
|---|---|---|---|---|---|
| State response changes | Previous state→new labeled state; no decorative entrance | 120ms dissolve;no delay | Interruptible; ignore stale completion after leaving | Instant replace with same labels | State variants via Change to or separately labeled scenario frames |
| Press/release enabled control | Rest→pressed→rest; preserve hit area | 100ms ease-out scale.96 (proposal);0ms delay | Release/cancel reverses; disabled has no activation | Color/border pressed feedback only | While pressing → Change to pressed; On click → approved action |



Timing not quoted from the PRD is a labeled design proposal. No loop, flashing or parallax is required. Animate compositor-friendly opacity/transform; never delay an enabled essential action. Stop all animation/media/recording simulation on leave; no second reward reveal on restore. Status/validation always has visible text/icon independently of motion.

## 9. Figma implementation instructions — future approved execution

1. Open the exact page/node links in section2. Confirm the source text/identity; stop if the references disagree or required copy is unavailable.
2. Locate the approved reference frame. Duplicate only that frame into a user-approved enhanced-design working area; preserve original nodes and IDs. If no frame exists, create only the missing requirement-driven surface after its layout/copy approval, using approved shared assets.
3. Create `NH/Enhanced/150/Deep_Link_Resolver/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Deep_Link_Resolver`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] B17 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
