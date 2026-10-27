**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 153 — Parent Profile PIN/Biometric Gate

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **C19 — Parent Profile PIN/Biometric Gate**.
- Surface: **screen**. Number is controlled review order, not a forced linear user journey.
- Execution status: **Reference available; unresolved conflicts require approval before design**.
- Journey entry / previous screen: Who Is Learning "Parent Profile" tile, "Switch Profile" from Child Mode, any override-requiring action.
- Next screen(s) / result: Parent Dashboard / the specific override action.
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_C19_Parent_PIN_Biometric_Gate.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Parent Area In-App (19-26)/Feature_C19_Parent_PIN_Biometric_Gate.md>); **§1.18 row 5; §1.7; §2; §6; §13**.
- Current mobile reference: [NoorHeroes current preview](https://noorheroes.figma.site/) → selector **Parent Gate**; exact text captured below.
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: **Missing corresponding screen reference.** Do not substitute a visually related hub as functional evidence.
- Frame 2 container: `1085:13003`; visual reference: **Missing corresponding screen reference.** Do not substitute a visually related hub as functional evidence.
- Reference qualification: No independently verified equivalent for this screen; global style inspiration must not replace approved copy.
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- [Parent Gate-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Parent Area/Parent Gate-01.png>)
- [Parent Gate-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Parent Area/Parent Gate-02.png>)
- Blueprint alignment:
- [01-who-is-learning-profile-picker.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C19_Parent_PIN_Biometric_Gate/KMP/01-who-is-learning-profile-picker.md>)
- [02-child-lock-verification-screen.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C19_Parent_PIN_Biometric_Gate/KMP/02-child-lock-verification-screen.md>)
- [03-parent-profile-gate-grace-window-management.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C19_Parent_PIN_Biometric_Gate/KMP/03-parent-profile-gate-grace-window-management.md>)
- [04-child-lock-recovery-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C19_Parent_PIN_Biometric_Gate/KMP/04-child-lock-recovery-flow.md>)
- [05-session-activation-cross-profile-state-clearing.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C19_Parent_PIN_Biometric_Gate/KMP/05-session-activation-cross-profile-state-clearing.md>)
- [06-offline-lock-verification-secure-local-cache.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C19_Parent_PIN_Biometric_Gate/KMP/06-offline-lock-verification-secure-local-cache.md>)
- [07-restriction-screen-time-bedtime-override-response-screens.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C19_Parent_PIN_Biometric_Gate/KMP/07-restriction-screen-time-bedtime-override-response-screens.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: - Source PIN 5678/Preview gate only is demo-only; source 4-6 digit label needs A1 canonical PIN-rule reconciliation. Source support/email text cannot replace A1 phone/email OTP account reverification. See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Safely select and verify the intended child or parent context before checking restrictions and activating the scoped session. Screen-specific role: Parent Profile PIN/Biometric Gate.

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

The complete feature obligations are retained in [every-FR register](../10_REQUIREMENT_COVERAGE_REGISTER.md); section 2 identifies the exact screen-inventory row.

## 4. Exact content specification

### Current mobile source — exact captured text

```text
Preview gate only · PIN 5678. This is not account security.

Preview parent sign-in instead
Parent Area

Enter your parent PIN to access settings and controls

4-6 digit PIN

Enter Parent Area

🔒 Forgot your PIN? Contact support or check your email for recovery options.

💡 Demo: Try PIN "5678"
```

### Requirement-driven fields and content roles

- Parent PIN pad
- Available OS biometric
- Fallback PIN
- Retry/lockout feedback
- Account OTP recovery

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Formal parent context header → source-approved purpose → PIN progress/input pad → available biometric → OTP recovery.
- Focused input only; no profile picker tiles/zero-child state or child stats.
- Retain demo PIN 5678 only in evidence; production content omits demo credentials after copy approval.

- Preserve content order and screen purpose. Use a vertical auto-layout content stack; horizontal inset 20, base spacing 4/8/12/16/24/32; card content padding 12–16. Keep compact controls next to their labels; align headings and cards to one column edge.
- Use existing cream `#FAF7F0`, surface `#FFFFFF`, ink `#1C2B33`, teal `#0E7C7B`, gold `#D4A24C`. Gold/bright teal are accents, not untested small-text colors. Body 14/16; heading 20/24; brand-only display 28/32. Preserve actual font assets; PRD Latin sans, display serif, separate verified Arabic content font.
- Do not import Frame 2's sample statistics, claims, religious text, section additions or combined desktop layouts. Borrow hierarchy, restrained surface separation and image framing only where they support this surface.
- Screen viewport is separate from long content height. Use vertical overflow when content exceeds available height; header/footer may be fixed only with bottom and top content clearance. At 320/360/390/420 logical widths, long labels wrap. At 200% text scale, stack grids or allow scrolling; no fixed text block height or sacred-text ellipsis.
- Essential touch target≥44×44 logical units; younger-child primary tasks≥56 where A2 specifies. Decorative icons have no hit targets. Assets retain aspect ratio; no text burned into illustrations. Safe area and keyboard must never obscure the current action.
- Source frames, unrelated screens and existing design direction remain unchanged. Token/component changes require separate review; never detach or globally mutate a source instance to fix this screen.

## 6. Screen states and conditional scenarios

- Parent PIN entry
- Fresh gate every Child→Parent Switch Profile regardless grace
- Existing Parent background return within grace may skip UI; no button
- Incorrect PIN/progressive lockout; disabled input until cooldown
- Biometric unavailable/enrollment changed → PIN
- Forgot PIN → A1 OTP account recovery
- Cancel pending protected action unchanged



Only apply states that belong to this surface. List-only empty/skeleton states are not added to legal documents or static intros. Network submit has a pending/timeout/retry result; retry preserves draft and must not duplicate a server-confirmed operation. Voice states need consent + OS grant; denial supplies listen/text/manual alternative. Loading/error/disabled/offline wording missing from source is a content approval gap.

<details><summary>Authoritative state/edge source context — apply screen-relevant cases, not all cases indiscriminately</summary>

### 1.10 Edge Cases

1. A child correctly enters their lock, but the device loses connectivity exactly at the "Check Restrictions" stage → this stage also falls back to the last-signed policy snapshot offline, rather than blocking activation entirely.
2. Two children share a device; Child A is PIN-locked, Child B has no lock → switching always returns to the picker and re-runs the full pipeline, including UI-state-clearing, for every switch.
3. A parent's enrolled biometric changes at the OS level → the app gracefully falls back to PIN entry rather than permanently locking the parent out; PIN remains the durable fallback at all times.
4. A child's lock-recovery flow is initiated and parent-verified, but the parent backs out before resetting the new lock → the child's original lock configuration remains unchanged and functional.
5. A device sits idle on the Who Is Learning picker for an extended period → no special device-level timeout is required by this feature, but each individual profile selection always re-runs the full verification pipeline.
6. A parent's grace window expires while they are mid-action inside an already-open Parent Mode screen → this only affects the next re-entry check, not the already-active session.
7. A child enters a correct pattern while an active lockout countdown is still running → the lockout is still honored; correct credentials don't bypass an active cooldown.
8. Two guardians share the same family account on different devices → each device's grace window is tracked independently, with no shared/synced clock across devices.
9. A screen-time override is requested from within Child Mode (a child asks a nearby parent) → still requires the full Parent Profile gate, never a lighter in-context-only check.
10. A child's lock type is changed by the parent while that child might have an active session elsewhere (rare multi-device case) → the change takes effect for future verification attempts; an already-active session isn't retroactively affected mid-session.

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Wrong PIN/pattern entered | Inline error, retry count increments, progressive lockout once threshold exceeded |
| Biometric assertion fails/unavailable | Falls back to PIN/pattern entry, never a dead end |
| Lockout active, correct credential entered | Lockout countdown still honored, not accepted until countdown expires |
| Offline lock verification | Local cached salted-hash comparison; offline restriction check uses last-signed policy |
| Interrupted lock-recovery flow | Original lock configuration preserved unchanged |
| Biometric enrollment change at OS level | Graceful fallback to PIN, never permanent lockout |

### 1.12 Empty States
- A family with zero children yet → the picker shows only the Parent Profile tile and the Add Child tile.

### 1.13 Loading States
- Profile activation (stage 4): a brief loading state while session/binding/cache-clearing complete, before Home renders.

### 1.14 Offline States
- Full offline functionality for lock verification and restriction-checking per FR-15.

### 1.15 Permission States
- **Biometric (OS-level):** if not enrolled or denied, the biometric option simply isn't offered, consistent with the "hide, don't show-disabled" pattern.



</details>

## 7. Interactions and navigation

- Enter PIN/available OS biometric → fresh verify → original trigger destination, Parent Dashboard only for ordinary Parent entry
  Child Mode Switch Profile → always show fresh verification regardless of grace-window timing
  Existing active Parent Mode background return → grace skip allowed only within configured window; no Skip control
  Forgot Parent PIN → A1 phone/email OTP account reverification → Parent PIN Reset; never generic recovery bypass
  Wrong PIN → progressive lockout/input disabled until cooldown; biometric failure/enrollment change → durable PIN
  Cancel/back → invoking screen without authorizing pending operation

For every action below, use the cited preconditions and source validation. Preserve the invoking route and selected child. Back/cancel dismisses only the current overlay or returns to the invoking screen, preserving drafts and completed progress where specified. Unavailable actions remain visibly labeled with their reason and never activate. Permission prompts occur only after parent consent and a deliberate related action. A prototype simulates outcomes; it never validates identity, grants permissions, charges money or mutates production data.

Verified current-preview controls, retained to prevent omitted clickable elements:

- {"disabled": false, "label": "Go back", "placeholder": null, "tag": "BUTTON", "text": "", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Preview parent sign-in instead", "type": null}
- {"disabled": false, "label": "Parent PIN", "placeholder": "Enter PIN", "tag": "INPUT", "text": "", "type": "password"}
- {"disabled": false, "label": "Show PIN", "placeholder": null, "tag": "BUTTON", "text": "", "type": "button"}
- {"disabled": true, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Enter Parent Area", "type": "submit"}

For any captured control absent from an explicit action above, reconcile it against the screen-specific source below before wiring. Do not connect it to a convenient unrelated screen. Mark it **unresolved, non-executable** until its actual destination/state is confirmed; the navigation appendix reports this limitation. Decorative source-layer names are not automatically click targets.

<details><summary>Screen-specific PRD specification / click behavior</summary>

Screen: Parent Profile PIN/Biometric Gate
Source PRD_Documents/Parent Area In-App (19-26)/Feature_C19_Parent_PIN_Biometric_Gate.md §1.18 row 5; §1.7; §2; §6; §13
Purpose: Safely select and verify the intended child or parent context before checking restrictions and activating the scoped session. Screen-specific role: Parent Profile PIN/Biometric Gate.
Fields: Parent PIN pad; Available OS biometric; Fallback PIN; Retry/lockout feedback; Account OTP recovery
Action contract:
Enter PIN/available OS biometric → fresh verify → original trigger destination, Parent Dashboard only for ordinary Parent entry
Child Mode Switch Profile → always show fresh verification regardless of grace-window timing
Existing active Parent Mode background return → grace skip allowed only within configured window; no Skip control
Forgot Parent PIN → A1 phone/email OTP account reverification → Parent PIN Reset; never generic recovery bypass
Wrong PIN → progressive lockout/input disabled until cooldown; biometric failure/enrollment change → durable PIN
Cancel/back → invoking screen without authorizing pending operation
States:
Parent PIN entry
Fresh gate every Child→Parent Switch Profile regardless grace
Existing Parent background return within grace may skip UI; no button
Incorrect PIN/progressive lockout; disabled input until cooldown
Biometric unavailable/enrollment changed → PIN
Forgot PIN → A1 OTP account recovery
Cancel pending protected action unchanged

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
3. Create `NH/Enhanced/153/Parent_Profile_PIN_Biometric_Gate/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Parent_Profile_PIN_Biometric_Gate`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] C19 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
