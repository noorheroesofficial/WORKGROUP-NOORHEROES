# NoorHeroes V2 — Current baseline, 22–23 October 2026

This handoff records the latest decisions in this conversation. It supersedes conflicting 20–21 October baseline entries. User requested saving context on 23 October 2026. Reinspect live Figma before the next edit; node IDs and manually edited content can drift.

## Scope and authority

- **Figma-only work from 23 October onward. Do not edit application, backend, admin, website, or companion-prototype code unless the user explicitly reauthorizes it.** Earlier app edits were not rolled back by this instruction.
- Same file: MR9935oQZACMjndzGIUgq5. Mobile page 928:2. Main section 1128:2, NoorHeroes V2 Design. Onboarding 1270:140; current Add Child section 1804:2599 is also a child of V2.
- Preserve original/old designs, web/admin, approved copy and interaction meanings. One standard 390 × 844 mobile size.
- Incremental PRD module sections only when a module starts. Never guess destinations or make placeholder routes.
- PRD_Documents, Development_Blueprints, Screens remain read-only. Read the relevant PRD/screen prompt before a new screen.
- Use NH components, shared text styles, color variables and layout tokens by default for all new Figma changes. Load the applicable Figma skill before its tool calls.

## Latest palette authority — 23 October

The Color foundation page **310:6** is authoritative. Existing NH Primitives collection 294:4 / mode 294:0 has 33 reference colors; NH Color 294:5 has Light 294:1 and Dark 294:2 semantic aliases. Reuse these, not new colors or older raw V2 shades.

Reference hex values:
white #FFFFFF; cream #FAF7F0; parchment #FDF6E3; ink #1C2B33; muted #6B7280; border #E5E0D5;
teal #0E7C7B; teal-bright #3FB6B4; gold #D4A24C; gold-bright #E8C27A;
night #10181C; night-surface #16232A; night-ink #F4F1E8; night-border #28363D; night-muted #9AA5AA;
success #2E8B57; success-bright #4CAF7D; error #C0392B; error-bright #E0594B; info #2E86C1; info-bright #5AA9D6;
teal-hover #096665; teal-pressed #075352; teal-tint #E6F4F1; teal-night-tint #183A3B;
gold-ink #805B20; gold-night-tint #3B301E; disabled #E9E6DF; disabled-ink #737873;
success-tint #EAF4ED; error-tint #FBEDE9; info-tint #EAF3FA; night-raised #203139.

Nearest existing reference colors were applied to editable V2 UI paints, gradient stops, effect colors and prototype color literals/defaults. Flags, logos, portraits and image artwork retain original asset colors. Latest audit: **0 off-palette editable UI colors**, 24 palette colors used, 7,972 variable bindings, 158 prototype destinations, no missing destinations. No new color variables/styles were created.

Transparency requires care: binding an opaque color variable can resolve a paint's alpha to 1. A bulk binding exposed transparent click targets; these were repaired and screens visually rechecked. Keep hit targets transparent, sheet scrims translucent and gradient alpha fades intact. Use a palette RGB with explicit alpha when binding cannot preserve transparency. Intro Back/Skip/badge treatments restored from documented white45% / white20% border guidance; feature-icon backgrounds use existing NH primary-subtle. No successful whole-file before/after layout hash was established: traversal counts changed when hidden instance children were materialized. Do not claim exhaustive geometry identity based on the audit.

The old ivory style S:8e5bfca7e0f151c0a4e7e393ac08ddb943d7d323, previously had #FDFBF7 → #FEFAF1. Those raw colors are historical; V2 consuming paints were mapped to the authoritative palette. Do not reintroduce the old raw stops. Inspect style/instance inheritance before reusing it.

## Shared components and foundations

- Existing NH Button/Loading, TextField, Checkbox, OTP cell, KeypadKey, DateField, Select, Snackbar remain the reusable sources.
- Primary button height is **48 px**, token VariableID:295:85. Earlier 56/64 px button instructions are superseded. Input groups have separate sizing; do not flatten them to button height.
- Send/Create loader source 329:6. Google loader 329:33, white Google surface/dark dots; do not swap its button type. While Google loads, Send code stays visible and disabled.
- NH/Snackbar family 1769:53 on 1420:2. Error 1420:18; Success1769:35, Warning1769:41, Info1769:47. Preserve caller actions/message bindings and semantic meaning.
- Shared BottomSheet page 604:2, family605:52. Existing Open LTR605:2, Open RTL605:16, Expanded LTR605:28, Expanded RTL605:40 updated to V2: 390 widths, 420/640 heights, 28 px top corners, square bottom corners, 40×4 handle, padding16/26/28/26, gap16, 20/28 title and14/22 body, scrollable body with fixed48px actions. Existing expand/collapse/dismiss flows retained. Main source ivory gradient predates final palette normalization; inspect and map reference colors when consuming.
- NH Chip family459:14, Off459:15 and On459:47. Learning Focus now uses **40 NH/Chip state instances** across four profile states. Uses NH standard44px control /40px pill,14px label,16px icon,16px horizontal pill padding,8px icon gap. Earlier compact28px local chips are superseded by the user's NH-component standardization.
- Approved V2 icon artwork reused as components on459:2: Quran2040:82, Stories2040:85, Duas2040:88, Arabic2040:91, Manners2040:94.
- 1,847 text nodes linked to shared styles and1,461 layout containers linked to spacing tokens. Added20 NH/V2/Typography styles to represent existing approved metrics and8 missing layout tokens in NH/V2/Layout Extensions. Keep language-specific fonts and mixed footer text. Do not globally force all typography into one size.
- Shared stars: 36 per full screen /10 per sheet, stars only, including Splash; independent gentle twinkle rhythms, no decorative circles, no input interception. Splash logo animation was separately removed. Do not mistake functional round avatars/loaders for decorative circles.

## Add Child / Profile Setup

Current section1804:2599. Four roots:
default1804:2656; saving1804:3379; timeout1806:3489; valid-review1806:3639.
Required nickname, DOB, avatar, preferred language, Learning Level retained. Age3–17. Existing age-library boundaries:3–7→5–8 assets;8–9→8–10;10–13→10–14;14–17→14–18+.
- Removed standalone Interests, Daily Goal and Accessibility sections. Learning Focus retained as one inline section with transparent outer surface and no outer card border.
- Learning Focus options: Quran Reading, Prophet Stories, Daily Duas, Arabic Letters, Islamic Manners. Existing state IDs preserved; no API changes authorized.
- AI Voice Guidance control retained; supporting strings “Enable interactive AI voice for activities (default off)” and “Opt-in required” removed.
- All six main headings use18×18 Material Icons Round with6px text gap: person, calendar_today, face, language, school, auto_stories. Teal mapped to NH primary.
- Learning Level cards preserve107.333×108 dimensions,8px padding,4px gaps and existing artwork/copy/radius. White unselected fill + NH border; selected teal border/title and pale palette-mapped fill. No checkmark. The screenshot's #EEF0EA selected fill was superseded by the palette-only normalization; inspect current bound primitive.
- Learning Focus selected/unselected follows the same light/teal visual language; no checkmarks; NH Chip state visibility uses existing Interest0–4 and InterestOff0–4.
- Nickname sheet1897:3203 deleted. Four field hit targets1806:3274/3277/3541/3691 now directly autofill “Ayaan” when idle and recalculate validation. This is a simulated Figma input, not real typing.
- DOB simulated sheet1897:3417 retained; DOB controls reveal age-specific avatar library. Native app input is outside current scope.
- Old sheets1804:3252 Optional preferences and1804:3346 Duplicate Nickname deleted. Duplicate-name business rule now appears as inline review; bool VariableID:1908:5170; default panel1908:5301. Keep avatar disambiguation/confirmation logic.
- Footer one line: “Have multiple children? Add another child later”; first part neutral, action teal and underlined. Latest reference1095:557 restored this full two-part text, superseding the earlier action-only version.
- Four footer frames1908:5426/5683/5940/6197 **now directly open** family-plan information overlay1965:6718. The latest explicit connection request replaced the earlier Free/parent/one-child conditional entry. Close1965:6928 dismisses to the current screen. Do not report that the current direct wiring is eligibility-gated.
- Original eligibility variables retained: IsFreePlan1965:6715, IsParentFlow1965:6716, ActiveChildCount1965:6717. A successful save increments active count. If later asked to restore production gating, use parent AND Free AND exactly1active child, with processing guard; do not infer eligibility from saved-attempt count alone.
- Family sheet uses exact supplied title “Add more children with a family plan”; Free1active profile explanation; purchase guidance via Profile → Parent PIN → Subscription & Billing → Google Play/App Store; single Close text action. Sheet1965:6720. No purchase route invented.

## Avatar picker

Shared component1872:3298, four age viewports. Latest user change: only three visible slots, selected circular portrait centered; tap config scrolls it to center. Slots106px +10px gaps across338px viewport; circle100px selected,72px others; gold ring/check retained. Twenty original avatars per group preserved (80 total), with wrap sentinels added at each track end. No library deletion.
Stored SCROLL_TO actions target the previous slot to center the selected portrait. Screenshot verified initial three-avatar composition. Live scrolling/edge-wrap playback was not tested; do not claim runtime centering verified.

## Earlier flow decisions still apply

OTP1612:1246, PIN1650:465, Biometric1670:1061 exist. Parent PIN:4–6 digits, no length-selection buttons, Continue after valid entry → Confirm Parent PIN → Save PIN → existing biometric sheet directly; no PIN-success dialog and no screen deletion. Prior live navigation failures were reported repeatedly; structural checks are not proof these are resolved.
OTP copy uses six digits; one-line recipient text with •••1204. and bold underlined Change link. Preserve current approved implementation after live inspection.
Existing Terms → close → separate Privacy sheet flow remains; draft NoorHeroes legal/sample content is not production-approved legal text. No optional consent implied by Terms acceptance. Screen009/011 changes were rolled back at the user's request; do not reintroduce them from old plans.

## Verification and limits

Current palette audit and selected screenshots are stored in this conversation; see Evidence/2026-10-23_V2_Color_Standardization_Audit.json.
Earlier current-context docs/evidence include116/116 Add Child stored-action checks and311 passing Android host tests before the Figma-only rule. Those code tests do not verify today's Figma interactions.
Code Layers disabled; prior browser figma.com access remained denied despite user enabling attempts. Live Present, native typing/date entry, device keyboard/RTL/accessibility, backend auth/network and iOS rendering remain unverified.
No new screen is automatically authorized by this context save.

