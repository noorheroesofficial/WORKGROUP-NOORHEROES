# NoorHeroes — Finalized V2 Design Prompt

## CURRENT — 27 October 2026: Profile Picker / Child Lock

Read [the Profile Picker and Child Lock baseline](Evidence/2026-10-27_Profile_Picker_Child_Lock_Baseline.md) for Screens022–024. It supersedes conflicting historical card sizes, full-page scrolling, compact Add Child rows, selected borders, recovery height and recovery-unmapped notes. Final layout uses inner-only scrolling, 366×738 main cards and 168×209.5 picker tiles. Independent child locks and verified-parent recovery remain simulated; Child Home/Add Child/parent management destinations remain pending. Figma only; no next screen is authorized. The23October baseline continues to govern unrelated V2 standards.

## CURRENT OVERRIDE — 23 October 2026

Use [the 22–23 October baseline](Evidence/2026-10-23_V2_Current_Baseline.md) before all historical guidance below. Apply changes **only in Figma** unless the user explicitly authorizes code changes. Reuse NH components, shared typography and layout tokens. NH Color foundation310:6 / existing33-color palette overrides older raw colors; map UI differences to closest existing colors, preserving transparency and asset identity. Do not introduce new UI colors. Current Learning Focus uses NH/Chip instances with standard44px touch controls, not the obsolete28px local chip frames. Use48px primary actions,18px heading icons with6px gaps, and current approved per-role spacing. Inspect current node properties and prototype routes; no automatic route guesses or next-screen authorization. Preserve all content and non-requested layout/functionality. Treat stored graph checks and screenshots as structural/visual evidence, not live playback verification.

For future edits, follow the personal skill [noorheroes-figma-v2](C:/Users/Sarva/.codex/skills/noorheroes-figma-v2/SKILL.md). Latest explicit user decisions override conflicting historical entries.

### User-approved baseline — 21 October 2026, through Registration

The user has finalized the current design through Registration and explicitly requested **no further changes**. Use [the approved-through-Registration baseline](Evidence/2026-10-21_Approved_Through_Registration_Baseline.md) first for future work. Its current measurements and approval status supersede historical entries below. Preserve all approved screens; no next screen is authorized yet. Recheck live Figma read-only when resuming, then apply these standards only to the next explicitly requested screen. NH input boundary is now56px with8/16px internal padding, and total label/input group88px default /116px error; older72/104px statements below are historical. Registration now exists and is approved; OTP alone remains a pending, unmapped future destination.

**Mandatory reusable instruction for every upcoming mobile screen.** Approved visual baseline captured from live Figma on 13 October 2026. Apply automatically alongside the screen-specific prompt; do not ask the user to repeat these standards.

### Authentication spacing update — 21 October 2026

For equivalent Login/Registration roles,latest explicit user instruction supersedes older12/20/24pxauth insets:14pxpadding on all sides of cards,primary/Googleactions,continuation row andidentifier controls. Current contentwidth338inside366pxcard; action minimum56px; identifier72pxaccommodates44pxtarget+28pxpadding. Title/description align within14pxcard inset. Registration Terms checkbox sits14pxbelowinput; preserve all consent gates. See current handoff and spacing evidence for exact positions. This is a consuming-screen update,not a global library or Intro redesign.

### Current baseline — 20 October 2026

Read [the saved current V2 baseline](Evidence/2026-10-20_V2_Current_Baseline.md) first, then recheck live Figma. It supersedes historical IDs/behavior below. Reuse existing public Button322:99, Loading Button329:49and Snackbar1420:18; removed local button set1355:2610and Snackbar1383:3295are no longer active. V2 is1128:2 → Onboarding1270:140; live Authentication Prototype is1355:2564. All splash branding now derives from Login1355:2696at splash-specific sizes. Send code uses329:6; Google uses329:33white surface/dark dots with visible-disabled Send code. Preserve the latest Google behavior. No future route guesses or additional screen-size variants. Live animation verification and deleted country-commit repair remain outstanding; consult the baseline for exact details.

### Reusable Snackbar — 20 October 2026

Use `NH/Snackbar`1420:18on library page1420:2for future equivalent snackbar roles. This derives from the user's current1383:3295/1383:3294references and intentionally has **square corners**, dark #1C2B33surface,1pxwhite border at12%alpha, Poppins12/18message and gold12/18action. Default350×60; controls are at least44×44; text wraps and height grows. Configure Message, Action label, Show action and Show dismiss through properties. Do not duplicate full-screen error layouts for snackbar content or add unrequested status colors.

The reusable master has no Login variables or failed-operation routes. Attach the consuming screen's confirmed action to its instance; Dismiss closes an overlay. Demo/template1420:98shows source-matched bottom placement and6-second dismissal, not verified OS safe-area/keyboard handling. Preserve the existing Login-specific snackbar/overlay until an explicit migration is authorized. See [Snackbar evidence](Evidence/2026-10-20_Snackbar_Component/README.md).

### Final Button library — 20 October 2026

For new reusable button work, the existing library has now been synchronized to the finalized V2 sources: public `NH/Button`322:99on page319:2and `NH/ButtonLoading`329:49on page327:2. Reuse these families and their retained properties instead of generating another family. Primary: exact final multicolor gradient,18px radius,Poppins SemiBold14/20,4px content gap,42% Disabled and88% Pressed. Use Large342×56as the finalized mobile standard; Regular48px remains an explicit compatibility option. Match foreground and surface contrast for Secondary/Quiet.

Loading replaces the visual label with a centered44×10group of three10px dots,7px gaps, keeping button dimensions fixed. Primary has no outline. Phase=Still is the reduced-motion option; animated phases pulse on a750ms cycle. Preserve the original action's accessible name in production code. Existing prototype-specific Login button IDs and routes stay unchanged; do not migrate them automatically. Read [library evidence](Evidence/2026-10-20_Button_Library_Sync/README.md) and the latest handoff before modifying components.

### Latest Login-specific standard

For authentication form roles, the later explicit Login standardization brief and live Login1355:2696 supersede earlier Login compositions. Read [the current Login handoff](Final_Authentication_2026-10-19/Login_Standardization/README.md) and CURRENT_CONTEXT_AND_NEXT_SCREEN.md first. Reuse centered approved branding, common aligned input/action widths, dark Phone/Email selectors, consistent Auto Layout, inline field validation, shared service-error snackbars and fixed-dimension language-style3-dot loading. Preserve the exact requested registration wording and original artwork. Main Login is390×844; its current card is366px/content342px with20px vertical/12px horizontal padding and16px section/12px form gaps. These authentication-specific surfaces do not replace Intro's existing background or typography roles.

Use public Button322:99, Loading Button329:49and Snackbar1420:18where equivalent roles apply. Local set1355:2610and Snackbar1383:3295were deleted by explicit request. Never recreate duplicate full-screen errors for minor field/service changes. Connect only confirmed approved destinations; OTP/Registration remain pending. Compare against live finalized screens and document native prototype fixture/playback limits. Do not treat static responsive inspection as device/keyboard verification.

## Source and precedence

Work in the existing NoorHeroes APP file, key `MR9935oQZACMjndzGIUgq5`, mobile page `928:2`, main section **NoorHeroes V2 Design** `1128:2`, with current module **Onboarding** `1270:140`. Finalized visual references: Welcome `1215:34`, Quran & Stories `1215:138`, Daily Habits `1215:246`, Parent Shield `1215:356`. Local reusable icon components: frame `1253:34`, named `NH/Intro/Icon/<meaning>/<size>`.

These finalized screens are the single source of truth for **visual design**. PRD and blueprints remain authoritative for behavior, business rules and required content; explicit user decisions override prior visual proposals. This document supersedes older conflicting visual sizing/style rules in the screen prompts and design-system guide. Verify live IDs and inspect actual reference layers before use. Do not reconstruct deleted assets from memory or silently adopt an unapproved user edit as a new standard.

Keep original designs, web/admin and protected PRD_Documents, Development_Blueprints and Screens unchanged. Create only the currently authorized screen and necessary local dependencies inside V2. Do not create another Figma file or advance to the next screen without the required review.

## Execute this prompt for each new screen

1. Read the individual screen prompt, relevant PRD/blueprint, and CURRENT_CONTEXT_AND_NEXT_SCREEN.md. Resolve exact copy, state and flow mapping using verified sources. Preserve all approved strings and icon meanings; never invent religious content or translations.
2. Inspect all four finalized V2 reference screens and the closest equivalent component. Reuse existing instances and text styles. Apply the rules below to equivalent roles; use product-appropriate screen composition, rather than copying the Intro hero/card arrangement into unrelated forms or hubs.
3. Build at **390 x 844** only, with safe-area clearance and scrolling when required. Use Auto Layout for icon/text groups, cards, forms, button contents and vertical content stacks. Use fixed widths, hug heights and deliberate shared slots to prevent wrapping from displacing icons.
4. Preserve the existing design language, palette, typography, component treatments and motion. For a new role without a suitable existing pattern, make the smallest consistent local extension, document it and avoid global source-library changes.
5. Connect only existing, confirmed destinations. Use PRD navigation wherever clear. Leave future destinations unmapped; never create dummy connections or substitute Registration for Login. Ask the user when an existing destination is ambiguous.
6. Verify the complete screen against the finalized references, correct discrepancies, record affected IDs and report checks and limitations. Stop for screen review when required.

## Shared color and surface rules

| Role | Final standard |
|---|---|
| Background gradient | #FAF7F0 at0%, #F3F7F2 at55%, #DFEEEA at100%; reuse exact Figma paint/transform [[0,1,0],[-1,0,1]] |
| Brand/action/icon | #0E7C7B |
| Primary text, Skip text, Back arrow | #1C2B33 |
| Secondary/supporting text | #606B72 |
| Cards | White;1px #DBE6E0 border;18px radius |
| Feature icon tile |36 x36;10px radius;brand-teal fill at8% alpha |
| Back/Skip/caption pill background | White at45% alpha;1px white border at20% alpha; text/icon opacity100% |
| Top screen/hero corners | Square; bottom hero corner treatment retained from reference |

Do not mix opacity of text with paint opacity. Preserve transparency but inspect readability over each illustration. Copy approved fills and effects directly instead of substituting approximate gradients/shadows. No decorative claims or extra educational content.

## Shared typography — use existing NH/Intro styles

All values below are **font size / line height in pixels**. Poppins for Latin UI; Noto Sans Arabic SemiBold for the finalized mixed-script category role. Do not force Latin fonts onto Arabic glyphs. Use verified script-capable fonts and approved localization for any future locale.

| Existing style suffix (prefix NH/Intro/) | Size/line | Weight | Alignment |
|---|---|---|---|
| Label/Skip |14/20|SemiBold|Center|
| Header/Badge Text |11/16|SemiBold|Center within icon/text row|
| Content/Category |10/16|SemiBold|Center|
| Content/Heading |20/28|SemiBold|Center for intro-equivalent roles|
| Content/Description |12/18|Regular|Center for intro-equivalent roles|
| Feature/Title |12/17|SemiBold|Left within copy stack|
| Feature/Badge |9/13|SemiBold|Left within copy stack|
| Feature/Description |11/16|Regular|Left within copy stack|
| Button/Label |14/20|SemiBold|Center the whole label/icon group|
| Footer/Copy |9/14|Regular|Center the whole icon/copy group|

Apply the same style ID to every equivalent role. Preserve source line breaks and punctuation. Use wrapped/hug text where appropriate; never truncate educational or sacred copy. The small supporting/tag styles are reference fidelity values, not authorization to make essential instructions, validation or form fields tiny. Any necessary new readable text role must be documented and compared visually.

## Icons and alignment — no exceptions for equivalent roles

- Use the shared **Material Icons Round filled** component family throughout, preserving icon meaning. Reuse existing Figma icon components; no emoji fallback, arbitrary outline mix, mismatched glyph fonts or malformed restored vector networks.
- Main/navigation/feature/CTA/caption icon canvases: **18 x18**. Bottom supporting icon canvases: **14 x14**.
- Keep intrinsic artwork proportions and optical padding. Prefer purpose-built18/14px components over repeatedly rescaling vector children. Adjust optical inset only when necessary to balance different shapes; keep the outer role dimensions stable.
- Caption and CTA icon/text gap: **4px**. Bottom supporting icon/text gap: **2px**.
- Feature icon tile/copy gap: **12px**. Center18px icon inside36px tile.
- Horizontal groups use cross-axis CENTER. Center the combined icon-and-text group, not independent elements. Stacked groups share a center axis where the product layout calls for centered content.
- Back arrows match Skip text #1C2B33; CTA arrows white; other role icons teal.
- Preserve **44px minimum touch targets** for small controls; canvas size is not hit-target size. Back44 x44 and Skip64 x44, radius22.
- Prevent glyph wrapping, negative bounds and clipping. Do not hide alignment defects by clipping overflowing artwork.

## Auto Layout and component rules

- Mobile content width350, horizontal inset20. Reuse4/8/12/16/24/32 spacing rules; use explicit finalized2px footer gap and10/18px radii where specified.
- Primary CTA350 x56, teal, radius18. Label+18px arrow in a horizontal hug row with4px gap, centered both axes. Equivalent button styles and press feedback must match across screens.
- Caption pill: horizontal hug layout;12px left/right,8px top/bottom;18px icon;4px gap;centered under illustration. Preserve45% white alpha.
- Supporting row:14px icon,2px gap,4px internal padding;hug contents; centered in350 x24 footer. Text9/14. No cropped bottom icons.
- Feature cards350 x84;12px horizontal/8px vertical padding; centered36px icon tile;12px gap;278px vertical copy stack with2px gap. Card list gap8px. Allow height growth for genuinely longer content rather than clipping or shifting the icon independently.
- Finalized Intro geometry, when creating intro-equivalent screens: hero220px high; content starts236; shared copy stack132px (category16, heading56, description36,12px gaps);46px gap before cards (card Y414);indicators700;CTA724;supporting footer792. Do not impose these content positions on unrelated product screens.
- Reusable styles/components must be local to V2 or approved library dependencies. Do not detach good instances or create duplicate styles for identical roles. Keep construction assets outside screen review canvases and report them as dependencies.

## Motion, state and navigation rules

- Shared Intro entrance: restrained opacity/8px rise,400ms Ease Out,80ms stagger where appropriate. Screen transitions250ms Dissolve Ease In And Out; no distracting perpetual loops.
- Reduced motion: omit translation; instant or short dissolve. Do not claim the reference already implements automatic OS preference detection.
- Only show loading where a real requirement or approved simulation calls for processing. Avoid network blocking for bundled offline Intro content. Empty/missing remote Intro content falls back to bundled content.
- Latest Language exception: Continue -> compact pulsing progress -> **directly Welcome**; do not restore Continue text, show a success screen or expand the button after progress. Current dependency1259:140 navigates after1.95s to1215:34;verify live existence before edits. Fixed timing is prototype simulation, not data persistence or server confirmation.
- Preserve selected language/state on Back and retry as far as prototype capabilities allow. State/history variables are session simulation, not production local storage.
- Prevent duplicate submits during loading; provide approved cancellation/error/retry behavior. Do not invent error copy or simulated business outcomes.
- Skip/final Intro -> Login is now connected to confirmed V2 Login `1278:155`, after explicit approval of Screen 007 copy/layout. Login's OTP, Register, recovery and successful Google downstream destinations remain unmapped until their V2 screens exist and are confirmed. Never create placeholder routing. Do not require the user to name clear PRD destinations, but ask for genuinely ambiguous mappings.

## Mandatory pre-completion consistency checks

- [ ] Exact approved copy and icon meanings preserved; no religious/localized content invented.
- [ ] All equivalent roles use shared style IDs, correct font/weight/size/line height and alignment.
- [ ] Every icon uses the shared rounded family and correct18px/14px role canvas; perceived sizes balanced.
- [ ] Icon/text groups vertically centered; caption/CTA gaps4px and footer gap2px.
- [ ] Padding, borders, radii, transparency, text colors and gradients match verified finalized counterparts.
- [ ] Auto Layout handles wrapping; no icon drift, clipped glyphs, overlap, stretched artwork or unexpected text-height changes.
- [ ] CTA row is centered as a group; touch targets and safe areas retained.
- [ ] Compare the new screen and **all four finalized intros side by side at the same zoom**. Also inspect the new screen at1x. Fix discrepancies before claiming completion. Remove temporary review frames afterward.
- [ ] Confirm existing destination IDs and validate every in-scope reaction. Future/uncertain destinations explicitly remain unmapped.
- [ ] Check applicable loading, disabled, validation, offline and retry states against requirements. No generic states added to static screens without purpose.
- [ ] Test motion in playback when available; structural checks and resting screenshots do not prove animation playback. State any untested behavior plainly.
- [ ] Original designs and unrelated screens unchanged. Record created/mutated IDs, evidence and unresolved gaps in sdocs.

End each screen handoff with a concise list of changes, completed checks, real limitations and the screen review link. Never mark a known inconsistency as complete or automatically advance to the next screen when review is required.

## Mandatory module placement override

Read [Incremental module organization](13_INCREMENTAL_MODULE_ORGANIZATION.md). Place each new screen inside its PRD-owned module under NoorHeroes V2 Design. Current Onboarding section is1270:140. Create future sections only when starting that module; do not pre-create examples or invent module names. This supersedes prior instructions that placed new frames directly in V2.

## 2026-10-21 — Authentication button padding override
- Login Send code and Registration Create Account: bottom internal padding 0 px.
- Continue with Google on both screens: top internal padding 0 px.
- Applied to enabled, disabled, animated loading, reduced-motion, and hold instances (22 nodes).
- Other padding remains 14 px. All buttons remain 338 × 56 px; reactions unchanged.
- Verified live Figma properties and screenshots of both screens. No Present playback claim.

## 2026-10-21 — Rollback of last button padding override
User requested rollback. Restore primary button bottom padding and Google button top padding to 14 px on Login and Registration, including all loading/disabled/hold variants. This supersedes the earlier zero-padding override. All 22 node properties verified restored; dimensions and reactions unchanged.

## 2026-10-21 — Fixed card action footers
- Login footer 1502:385: 338 × 160 at x14/y294 in card 1355:2705. Card stays 366 × 468. Content 1355:2706 is a clipped 338 × 266 vertical scroll viewport; moved existing Submit, Separator and Google nodes into the footer, preserving IDs and reactions.
- Registration footer 1459:1200: 338 × 160 at x14/y402 in 366 × 576 card. Primary y0, separator y70/h20, Google y104/h56; 14 px gaps. Status 1459:1209 is retained above footer at y-32 with footer clipping disabled. Scroll viewport 1459:734 is 338 × 342.
- Both action groups have exactly 14 px left/right/bottom card inset. Separators have 0 top/bottom padding and retain 14 px horizontal padding. Button internal padding remains 14 px throughout.
- Loading overlays updated: Login primary y494, Google y598; Registration primary y602, Google y706; all x26. Animated, reduced-motion and hold variants updated.
- Live property checks and both screen screenshots reviewed. No Present playback verification. Other copy, consent states and navigation retained.

## 2026-10-21 — Compact Registration consent and separate legal sheets
Supersedes the old inline list and pending full-text destination notes for Screen 008. User authorized prototype draft wording and fictional sample data. Main compact summary 1513:429; Optional preferences 1459:1128 sits 14 px below. Terms 1513:350 closes before Privacy 1513:386 opens. Adult and child-data confirmations remain explicit and separate; Terms and Privacy confirmations remain separate. Optional sheet 1511:380 has three independent off-by-default choices; Read details 1514:354 / 1514:384 / 1514:414. Summary uses variables 1513:348/349, all four required gates preserved. Field default/error height 72/104 and helper y86. Existing fixed card footer and loaders unchanged. Final copy, node manifest and 29 structural checks: Evidence/2026-10-21_Consent_Bottom_Sheets.md and corresponding _Manifest.json. Screenshots reviewed; Present playback unverified. OTP still unmapped pending approved screen. All legal wording is draft requiring review.

## 2026-10-21 — Single-line Registration acceptance links
Compact row 1513:429 is 338×44, zero outer padding and zero checkbox-to-label gap. Checkbox artwork canvas is 24 px; transparent 44×44 state-dependent hit areas retain tap accessibility without visible padding. Text stays on one line at Poppins 12 px, with 3 px typographic word gaps between spans. Terms and Conditions link 1526:312 and Privacy Policy link 1526:317 are independently underlined and open 1513:350 / 1513:386 respectively, with original motion/processing guards. Optional preferences remains 14 px below. Direct Privacy reading grants nothing; eligibility variables 1527:326/327 require Terms, adult confirmation and child-data choice for acknowledgement. Required toggle/Terms/revoke actions update eligibility. All eight eligibility combinations and link/spacing checks passed. Screenshot reviewed at 390×844; Present playback remains unverified.

## 2026-10-21 — Fixed Registration card content
Removed all scrolling inside Registration main frame 1459:256. Former viewport 1459:734 renamed Content/Registration — Fixed, overflow NONE, 338×356 with clipping disabled; content 1459:735 clipping disabled. Default content 324 px and validation content 356 px fit. Card, controls, footer positions, loader positions and interactions preserved; footer bottom inset remains 14 px. Separate legal bottom-sheet document scrolling remains enabled. Live properties and default screenshot verified.

## 2026-10-21 — Exact Registration gaps: 6 px / 14 px
Overrides the prior zero checkbox gap and reserved fixed content height. Summary 1513:429 uses itemSpacing 6; checkbox canvas and label group remain 24×44 and single-line Poppins 12, vertically centered. Optional preferences to Create Account is exactly 14 px measured by absolute bounds, not component padding.
Existing card 1459:421 and content container 1459:734 now use non-scrollable vertical Auto Layout with content-fitting height and 14 px card padding/gap; no duplicate components created. Default card height 526; validation 558. Button dimensions remain 338×56 and existing labels/styles unchanged. Existing action group retains its internal 14 px gaps.
Existing status text 1459:1209 follows the action group only when nonempty; visibility variable 1533:328 is maintained alongside existing status-setting actions. No original navigation or submission condition was removed. This added visual visibility bookkeeping accounts for changed reaction JSON; authentication behavior is preserved.
Existing processing instances were reparented into transparent layout hosts, each with a spacer bound to existing field height 1464:254, so default/error positions match controls without duplicate buttons. Primary hosts 1533:427/429 at x26/y480; Google hosts 1533:431/433 at x26/y584. Default processing Y: primary552, Google656; validation Y: primary584, Google688.
Checked default, validation, offline-feedback, and combined states: all have 14 px preference/button gap, matching loader positions, and no overlap with Log in. Checkbox/text gap verified 6 px; single-line copy fits 338 px. Screenshots reviewed at 390×844; initial variable defaults restored. Main registration remains non-scrollable; separate legal sheets retain scrolling. See Evidence/2026-10-21_Registration_Exact_Gaps.json. Present playback remains unverified.

## 2026-10-21 — Compact checkbox reduced by 4 px
For summary 1513:429 only, selected and unselected visual boxes reduced from 24×24 to 20×20. Container 1526:308 is 21×44 with 1 px right padding. Existing checkbox instances scaled locally, with shared library masters unchanged. Row gap remains 6 px; text stays single-line Poppins 12 and vertically centered. Existing transparent 44×44 click areas and consent/link interactions preserved. Both artwork dimensions and padding verified; row screenshot reviewed.

## 2026-10-21 — Consent sheet labels single-line; spacing reduced by 4 px
Updated Child-data-processing 1459:1105, adult confirmation 1459:1082 and all three rows inside Optional preferences 1511:382 (1459:1131/1154/1177). For both selected and unselected existing instances, itemSpacing changed from 12 to 8 px after unbinding the local gap token. This removes 4 px between the checkbox target and label and widens labels from 222 to 226 px. All five labels now fit a single 24 px line at the approved 390×844 viewport, preserving exact copy, Poppins Medium 14, checkbox artwork, row heights and all reactions. Twenty checks passed, covering all ten instance gaps/reactions and ten visible-state label measurements. Temporary selection defaults restored. Three sheet screenshots reviewed. Main Registration compact checkbox 1513:429 unchanged; no original library master modified. Present playback not tested. See Evidence/2026-10-21_Sheet_Consent_Label_Spacing.json.

## 2026-10-21 — Login Optional preferences and loading-copy cleanup
Removed the Creating account... processing string from Registration submit/Google/retry actions by setting the status to empty. Existing nonempty-status visibility logic now hides that line while loading; button loaders and network/error feedback remain. Four processing-label actions updated.
Login now includes Optional preferences control 1552:940 cloned from approved 1459:1128, opening the existing sheet 1511:380 and retaining its shared optional selections. Entry uses the Login processing guard 1383:3061 and existing reduced-motion behavior.
Login card/body now fit non-scrollable content. Input -> preferences = 14 px; preferences -> Send code = 14 px. Existing helper is visible only for validation and has 14 px adjacent gaps. Existing title/copy, fonts, colors, buttons and routes preserved. Field layout-height variable 1552:429 is 72 by default / 104 in validation; all existing Login error set/reset actions, including country selectors, also update this layout value.
Existing loader instances use transparent layout hosts 1552:947/949/951/953 with a spacer bound to that field height. Default Send/Google Y=498/602; validation Y=530/634, x26. Default Login card height472, validation504. Existing Google white surface/dark loader and Send code gradient/light loader remain.
Seven checks passed: Registration processing-status suppression for both buttons; preferences entry/processing guards; default/validation 14 px gaps and four loader alignments; no remaining Creating account status actions. Normal/validation screenshots reviewed. Original variable defaults restored. Present playback remains unverified. Evidence: Evidence/2026-10-21_Login_Optional_Preferences.json.

## 2026-10-21 — Fixed bottom Login account-creation footer
Moved existing 1355:2744 out of scrollable body 1355:2701 into Login root 1355:2696. Anchored at x12/y792, 366×44 on 390×844, matching Registration footer 1459:1210 with 8 px bottom inset. Horizontal STRETCH / vertical MAX constraints retain bottom anchoring when frame height changes. Copy, typography, colors and Registration navigation unchanged. Geometry, original text/reactions and Login screenshot verified. No duplicate footer created.
> **Prototype reliability update —22 October2026:** For app actions on components that change variant on hover/press or variable binding, use stable Frame click targets with the same bounds and explicit readiness/busy guards. Do not place critical navigation solely on a variant-changing instance. Verify inherited component interactions, target ownership and duplicate-submit protection. Preserve every reference screen; removing a live step does not authorize deleting its design.

> **Decoration standard —22 October2026:** Reuse Calm Star1726:1206 with A/B/C staggered native opacity rhythms and Still. Keep a mix of static/twinkling5–12px approved gold stars in clear sky above/below cards; fewer around dense content. Place behind UI, outside branding/copy/controls/footer/keyboard/Snackbar bounds, never inside legal or biometric sheet content. Preserve foreground and navigation. Existing Login/Biometric reduced-motion flags stop loops; document native playback/device verification limits.


## Latest decoration override — 2026-10-22

Use14_SHARED_FULL_SCREEN_STAR_SYSTEM.md for all current and new V2 screens, including Splash, explicitly included by the user. It supersedes top-only star placement and prior Splash exclusions. Reuse approved star assets and shared native rhythms,24 scattered stars per full screen,6 quiet accents per sheet; transparent processing/error overlays inherit. No decorative circle particles. Preserve foreground readability, functional circular controls/loaders, app interactions and reduced-motion behavior. Never put decorative layers into Auto Layout flow or give them input handlers. Production runtime hit testing/performance must be verified separately from Figma structural checks.

### Latest star count override — 2026-10-22

The user requested more stars. Default shared field density is now36 stars per full screen and10 per bottom sheet; supersedes earlier24/6 counts. Keep approved assets, varied blink phases, restrained opacity over content, reduced motion, and inherited fields on transparent overlays.

## 2026-10-22 — Shared Snackbar standard supersedes earlier snackbar guidance

Use the existing NH/Snackbar family `1769:53` on page `1420:2`. Retained Error master `1420:18`; semantic Success `1769:35`, Warning `1769:41`, Info `1769:47`. Properties: `Message#1769:0`, `Action label#1769:1`, `Show action#1769:2`, `Show dismiss#1769:3`, and `Tone`. Existing consuming-screen retry/dismiss reactions and message variable bindings remain authoritative. No route guessing. Error matches screen1654:1428 exactly: square #1C2B33, 12% white1px border, no shadow/leading icon, Poppins12/18, gold action, minimum44px controls, HUG height60 minimum. Mobile390px uses350px snackbar,20px side/24px bottom margins; grow for long text. All six active V2 consumers standardized. Future equivalent transient feedback must reuse this family, not a local duplicate. Other tones reuse semantic tokens and meaningful caller-provided copy. Production mobile now uses NoorSnackbarHost/NoorSnackbarHostState; current20 consumers migrated, bounded/deduplicated and inset-aware. Local companion also uses centralized feedback. See Snackbar_2026-10-22/README.md for evidence, test failures and native/device verification limits. Do not infer release readiness from structural screenshots or unit tests.

## 2026-10-22 — Primary button height is48px

User referenced322:2 (Primary Regular Default,48px). All53 primary button/loading instances in V2 now bind height to existing size/control-regular VariableID:295:85, resolving48px. This supersedes earlier56/64px primary button instructions. Existing widths, typography, colors, variant state bindings and reaction arrays were preserved. Primary wrappers and PIN/biometric hit areas synchronized; Google button styling/height retained, its loading overlays shifted8px to follow footer reflow. Login wrapper clipping corrected and Login/Registration/Confirm PIN/Biometric screenshots inspected. Use48px for upcoming primary actions and their loading states; do not change shared56px field/large-control token. Original reference designs and other pages unchanged. Live Present testing remains blocked by the saved figma.com browser policy; this was a design geometry change, not a claim that the unresolved PIN live-click issue is fixed. Evidence: Evidence/2026-10-22_Primary_Button_48px.json.

## 2026-10-22 — Card and bottom-sheet ivory gradient
User clarified: update white cards and sheets only; keep teal page backgrounds. Reuse shared Figma Paint Style NH/V2/Surface/Ivory Vertical (S:8e5bfca7e0f151c0a4e7e393ac08ddb943d7d323,). Vertical top #FAF7F0 to bottom #FDF6E3, opaque stops, transform [[0,1,0],[-1,0,1]]. Applies to major auth/profile cards, legal and selection sheets, intro feature cards, learning/language choice cards, country-list cards and empty-avatar cards. Preserve selected-state colors, inputs, buttons, teal backgrounds, layout and reactions. 818 eligible nodes updated in V2; no reference pages or production code changed. Geometry and reaction equality checks passed. Evidence: Evidence/2026-10-22_Ivory_Card_Sheet_Gradient.json and _Rows.json. Use this surface style for future white cards/sheets.

### Lighter ivory surface override — 2026-10-22
The user requested a lighter gradient. Shared NH/V2/Surface/Ivory Vertical now uses top #FDFBF7 and bottom #FEFAF1, replacing the earlier #FAF7F0 / #FDF6E3 stops. All 818 linked V2 card and sheet surfaces inherit the update. Keep the same vertical direction, teal page backgrounds, inputs, buttons, layout and interactions. This is a Figma surface-style update only.
