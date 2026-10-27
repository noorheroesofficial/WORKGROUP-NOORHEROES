**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 134 — Locked Item Detail — Unlock Criteria View

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **A12 — Locked Item Detail — Unlock Criteria View**.
- Surface: **overlay**. Number is controlled review order, not a forced linear user journey.
- Execution status: **Preserve all literal Frame 1 text; source sample statistics are fixtures only and religious strings remain subject to source verification.**.
- Journey entry / previous screen: Locked-Item Teaser.
- Next screen(s) / result: "Go to activity" deep link, or dismiss.
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_A12_Avatar_System.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Child App (1-12)/Feature_A12_Avatar_System.md>); **§1.18 row 6; §1.7; §2; §6; §13**.
- Current mobile reference: [NoorHeroes current preview](https://noorheroes.figma.site/) → selector **Locked Item**; exact text captured below.
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: [Locked Item Detail - Desert Caravan Cloak](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1109-5024) — `1109:5024`. Exact/closest named existing frame; preserve purpose and copy; theme/player subtype must be checked
- Frame 2 container: `1085:13003`; visual reference: [Avatar Studio & Character Evolution](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1085-19545) — `1085:19545`. Related enhanced feature hub for visual patterns only; not an exact screen equivalent
- Reference qualification: [].
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- [Avatar-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Avatar/Avatar-01.png>)
- [Avatar-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Avatar/Avatar-02.png>)
- [Avatar-03.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Avatar/Avatar-03.png>)
- [Evolution.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Avatar/Evolution.png>)
- [Locked Item-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Avatar/Locked Item-01.png>)
- [Locked Item-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Avatar/Locked Item-02.png>)
- Blueprint alignment:
- [01-avatar-screen-3d-preview-experience.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A12_Avatar_System/KMP/01-avatar-screen-3d-preview-experience.md>)
- [02-owned-items-grid-equip-interaction.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A12_Avatar_System/KMP/02-owned-items-grid-equip-interaction.md>)
- [03-locked-item-detail-unlock-criteria-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A12_Avatar_System/KMP/03-locked-item-detail-unlock-criteria-flow.md>)
- [04-auto-unlock-detection-celebration-notification.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A12_Avatar_System/KMP/04-auto-unlock-detection-celebration-notification.md>)
- [05-character-evolution-milestone-reveal.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A12_Avatar_System/KMP/05-character-evolution-milestone-reveal.md>)
- [06-offline-inventory-cache-equip-outbox-sync.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A12_Avatar_System/KMP/06-offline-inventory-cache-equip-outbox-sync.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: No screen-specific ID supplied; still check global G-01–G-10 and source content differences. See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Enable Locked Item Detail — Unlock Criteria View in the established A12 journey. Entry: Locked-Item Teaser. Required outcome: "Go to activity" deep link, or dismiss.

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

**FR-1** Avatar screen sections: 3D avatar preview, owned-items grid (organized by slot: outfit/glow/accessory), locked-item teasers showing unlock criteria (source: screen catalog "Avatar — UI Sections: 3D avatar preview, owned-items grid (outfits, glow states), locked-item teasers with unlock criteria").

**FR-2** User actions: equip/unequip an owned item, preview a locked item (a non-committal visual preview without actually equipping it), and navigate directly to the activity that would unlock a given locked item (source: screen catalog "User Actions: Equip/unequip an item, preview a locked item, navigate to the activity that unlocks it").

**FR-4** Every `avatar_item`'s `unlock_rule` must map to an existing badge, level threshold, or habit milestone — admin tooling must reject any attempt to define an arbitrary or opaque unlock condition with no underlying verifiable criteria (source: Admin module Validation Rules — restated here as the rule this feature's read/evaluation path depends on).

**FR-5** Items are never sold for real money in child mode — equivalent to and consistent with A.11 FR-1's Noor-Heroes-Points-only economy; this feature's equip/unlock layer has no payment-related code path at all (source: Admin module Validation Rules).

**FR-6** Equipping an item is immediate (optimistic client update, server-confirmed) and instantly reflected in the avatar preview (source: Avatar Flow diagram, "POST equip → Avatar preview updates").

**FR-7** Locked items display their specific unlock criteria (e.g., "7-day streak") rather than a generic lock icon with no explanation, consistent with the platform's general locked-content transparency principle established in A.3/A.5.

**FR-8** When a child's activity causes a locked item's criteria to become met, the item is **auto-unlocked** and a notification is sent — the child is never required to manually "claim" an avatar-item unlock the way they might claim a mission/challenge reward in A.11 (source: Avatar Flow diagram, "Criteria met later? → Yes → Item auto-unlocked + notification").

**FR-9** Character Evolution: avatars and Noor companions evolve through learning-based progression — Quran skills, story morals, kindness actions, and habit consistency unlock new outfits, glow states, and story-world abilities (source: "Character Evolution" feature card — "Avatars and Noor companions evolve through learning-based progression... unlock new outfits, glow states, and story-world abilities").

**FR-10** Retiring an `avatar_item` from the catalog (Admin "Delete" action) never revokes it from children who already own it — retired items remain fully equippable for existing owners, only new acquisition is prevented (source: Admin module CRUD Operations, "Retire item (owned items remain equippable)").

**FR-12** All avatar assets (base avatars and every `avatar_item`) must pass a modesty/age-appropriateness review by the same content governance pipeline used for other content types — "it's just a cosmetic" is never an exemption from this review.

## 4. Exact content specification

### Current mobile source — exact captured text

```text
Locked Item

✦
✦
✦
✦
✦
✦
★
🔒
Locked
Scholar's Robe
outfits · Locked

HOW TO UNLOCK

📖

Complete a 10-day reading streak

Explore this activity at your own pace. This preview does not unlock or equip the item.

Your progress
7 / 10 days ✦

✦ Preview progress — there is no rush.

👁️
Preview (try on without equipping)
Explore related activity →
```

### Frame 1 — exact layer text (separate source; differences need approval)

```text
Noor Companion
Level 4
SUNNAH JOURNEY SERIES
Desert Caravan Cloak
Modest traveler's travel mantle woven for blessed
journeys under desert stars.
Locked Reward
Unlock Criteria
5 of 7 Days
Complete a 7-day Quran Reading Streak
Day 1
Day 3
Day 5
Day 7
Masha'Allah! You're getting so close —
just 2 more daily readings to unlock this
cloak!
Go to Daily Quran Reading
Try On (Preview)
Earned with patience (Sabr) and daily consistency. No
loot boxes, no surprises.
Story Reader
240
```

### Requirement-driven fields and content roles

- Not supplied by this source; resolve before execution.

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Preview above slot-segmented inventory; Outfits/Glow/Accessories retain selection/equipped states. Locked criteria remain visible. Rotation has tappable alternatives. Locked preview is reversible and never persistent; keep existing approved assets without uploads.

- Preserve content order and screen purpose. Use a vertical auto-layout content stack; horizontal inset 20, base spacing 4/8/12/16/24/32; card content padding 12–16. Keep compact controls next to their labels; align headings and cards to one column edge.
- Use existing cream `#FAF7F0`, surface `#FFFFFF`, ink `#1C2B33`, teal `#0E7C7B`, gold `#D4A24C`. Gold/bright teal are accents, not untested small-text colors. Body 14/16; heading 20/24; brand-only display 28/32. Preserve actual font assets; PRD Latin sans, display serif, separate verified Arabic content font.
- Do not import Frame 2's sample statistics, claims, religious text, section additions or combined desktop layouts. Borrow hierarchy, restrained surface separation and image framing only where they support this surface.
- Screen viewport is separate from long content height. Use vertical overflow when content exceeds available height; header/footer may be fixed only with bottom and top content clearance. At 320/360/390/420 logical widths, long labels wrap. At 200% text scale, stack grids or allow scrolling; no fixed text block height or sacred-text ellipsis.
- Essential touch target≥44×44 logical units; younger-child primary tasks≥56 where A2 specifies. Decorative icons have no hit targets. Assets retain aspect ratio; no text burned into illustrations. Safe area and keyboard must never obscure the current action.
- Source frames, unrelated screens and existing design direction remain unchanged. Token/component changes require separate review; never detach or globally mutate a source instance to fix this screen.

## 6. Screen states and conditional scenarios

- Default as described in cited source
- Criteria not met
- Preview active without persistent equip
- Deprecated unlock criteria unavailable



Only apply states that belong to this surface. List-only empty/skeleton states are not added to legal documents or static intros. Network submit has a pending/timeout/retry result; retry preserves draft and must not duplicate a server-confirmed operation. Voice states need consent + OS grant; denial supplies listen/text/manual alternative. Loading/error/disabled/offline wording missing from source is a content approval gap.

<details><summary>Authoritative state/edge source context — apply screen-relevant cases, not all cases indiscriminately</summary>

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

</details>

## 7. Interactions and navigation

- {"element": "Preview", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "Non-persistent locked-item try-on", "destination": "Non-persistent locked-item try-on", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Go to Activity", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "Exact unlocking activity from server criteria", "destination": "Exact unlocking activity from server criteria", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Dismiss", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "Avatar with actual equipped state restored", "destination": "Avatar with actual equipped state restored", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}

For every action below, use the cited preconditions and source validation. Preserve the invoking route and selected child. Back/cancel dismisses only the current overlay or returns to the invoking screen, preserving drafts and completed progress where specified. Unavailable actions remain visibly labeled with their reason and never activate. Permission prompts occur only after parent consent and a deliberate related action. A prototype simulates outcomes; it never validates identity, grants permissions, charges money or mutates production data.

Verified current-preview controls, retained to prevent omitted clickable elements:

- {"disabled": false, "label": "Go back", "placeholder": null, "tag": "BUTTON", "text": "", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "👁️\nPreview (try on without equipping)", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Explore related activity →", "type": null}

For any captured control absent from an explicit action above, reconcile it against the screen-specific source below before wiring. Do not connect it to a convenient unrelated screen. Mark it **unresolved, non-executable** until its actual destination/state is confirmed; the navigation appendix reports this limitation. Decorative source-layer names are not automatically click targets.

<details><summary>Screen-specific PRD specification / click behavior</summary>

#### Screen: Locked Item Detail

- **Purpose:** Clearly communicate what's needed to unlock a specific item and offer a direct path there.
- **Components:** Item illustration (desaturated/locked styling), unlock criteria text (specific, e.g., "Complete a 7-day Quran reading streak"), a "Preview" action (non-committal try-on), and a "Go to [Activity]" primary action deep-linking to the relevant feature.
- **States:** Default, Criteria-recently-progressed (an optional subtle "you're getting close!" framing if progress data is available and meaningful to surface), Unavailable (deprecated unlock-rule reference, Edge Case 3).



</details>

## 8. Motion and animation specification

| Trigger | Start → end / direction | Timing | Interruption / leave | Reduced motion | Figma approach |
|---|---|---|---|---|---|
| Open/close by defined control | Closed ↔ visible, opacity0→1; sheet bottom→rest only if sheet specified | 200ms ease-out opening;160ms ease-in closing;no delay | Reversible; cancel closes and returns focus; navigate away closes | Instant show/hide | Open overlay / Close overlay; Move in from bottom only for actual sheet |
| Data-confirmed success or first entry | Hidden status→visible check/progress; splash logo opacity0→1 scale.98→1 | 400ms ease-out; splash≤1200ms; reward total≤2000ms;no mandatory wait | Skippable/interruptible; stop on leave; no reward repeats after resume | Static success/brand state | Smart Animate between matching states; After delay only for visual sequence, never server validation |
| Press/release enabled control | Rest→pressed→rest; preserve hit area | 100ms ease-out scale.96 (proposal);0ms delay | Release/cancel reverses; disabled has no activation | Color/border pressed feedback only | While pressing → Change to pressed; On click → approved action |



Timing not quoted from the PRD is a labeled design proposal. No loop, flashing or parallax is required. Animate compositor-friendly opacity/transform; never delay an enabled essential action. Stop all animation/media/recording simulation on leave; no second reward reveal on restore. Status/validation always has visible text/icon independently of motion.

## 9. Figma implementation instructions — future approved execution

1. Open the exact page/node links in section2. Confirm the source text/identity; stop if the references disagree or required copy is unavailable.
2. Locate the approved reference frame. Duplicate only that frame into a user-approved enhanced-design working area; preserve original nodes and IDs. If no frame exists, create only the missing requirement-driven surface after its layout/copy approval, using approved shared assets.
3. Create `NH/Enhanced/134/Locked_Item_Detail_Unlock_Criteria_View/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Locked_Item_Detail_Unlock_Criteria_View`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] A12 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
