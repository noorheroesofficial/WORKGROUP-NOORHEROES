# Current Figma context and next-screen handoff

## CURRENT — 27 October 2026: Profile Picker / Child Lock

Read [the Profile Picker and Child Lock baseline](Evidence/2026-10-27_Profile_Picker_Child_Lock_Baseline.md) for Screens022–024. It supersedes conflicting historical card sizes, full-page scrolling, compact Add Child rows, selected borders, recovery height and recovery-unmapped notes. Final layout uses inner-only scrolling, 366×738 main cards and 168×209.5 picker tiles. Independent child locks and verified-parent recovery remain simulated; Child Home/Add Child/parent management destinations remain pending. Figma only; no next screen is authorized. The23October baseline continues to govern unrelated V2 standards.

## CURRENT — 23 October 2026 (supersedes historical entries below)

Read [the 22–23 October current baseline](Evidence/2026-10-23_V2_Current_Baseline.md) first. It records current V2 component/palette standardization, Profile Setup, avatar carousel, direct family-sheet connection, nickname autofill, and verification limits. **Figma only; do not modify application code without new explicit authorization.** NH Color foundation310:6 is authoritative; no new UI colors. Use existing NH components/styles/tokens. Inspect live Figma before edits. Historical “OTP pending,” older ivory colors, compact local-chip dimensions, conditional family-sheet wiring and pre-48px button instructions below are superseded where they conflict. No next screen is authorized by a context save.

## Latest — 2026-10-21 Auth14pxpadding and Terms below identifier

Login/Registration cards/actions/inputs/continuation now use14pxall-side padding; innerwidth338. Buttons retain56pxminimum height; input72pxsupports44pxtargets+14pxvertical insets. User confirmed moving existing Registration Terms1459:1059directly below identifier1459:753with14pxgap. Same consent variables/gates; other rows remain scrollable. Reg fieldheight146default/178error; fixedfooter/card adjusted(card576,Loginlinkbottom836). All loading/timeout visuals aligned to controls.33checks passed,including16consent combinations; both default renders inspected. Existing manually edited Login copy retained. See [spacing evidence](Evidence/2026-10-21_Auth_Padding_14_and_Terms.md). Live Present/OS behavior unverified.

## Latest — 2026-10-20 Auth icon gap now0

Per user correction,both auth icon containers1383:3078/1459:413now have0top and0bottom padding,height118. Icon-canvas-to-form gap verified0on Login/Registration; card tops now200. Registration footer and all normal/Google loading/timeout visuals realigned. Button behavior and toolbar branding unchanged. Supersedes16pxbottom-gap entry below; source PNG intrinsic transparency remains preserved.

## Latest — 2026-10-20 Auth icon padding0top/16bottom

Login/Registration icon slots1383:3078and1459:413now have0top padding,16bottom padding,height134for118pxicon. Login icon/card grouped in transparent Auto Layout to preserve the24pxgap after the card; Registration card/footer shifted correspondingly. Both card tops now216(previous228); internal fields/styles/actions unchanged. Updated normal/Google processing and timeout loader positions to match shifted buttons. Toolbar/wordmarks unchanged. Verified icon localy0and exact16pximage-canvas-to-card gap on both screens. Intrinsic transparency inside approved source PNG is preserved.

## Latest — 2026-10-20 Larger splash icon

Increased approved1299:19icon artwork from118×118to160×160on all5existing splash variants. Centered artwork at-21,-21within unchanged118×118motion/layout canvases; disabled canvas clipping. Text,wordmark,subtitle,lockup positions and navigation unchanged. Main enlarged composition visually reviewed.

## Latest — 2026-10-20 Splash icons use exact1299:19

All5existingSplash_Screenframes1131:2,1146:2/125/248/371now use cloned original icon1299:19(image274d62e30d3d1546da25c1baedf1f43cf1a79565)inside existing118×118canvases1154:2/276/316/356/396. Exact source proportions/colors/transparency preserved; replaced prior cropped Login-derived icon copies. Icon-slot bounds and routes verified unchanged across all five; main render inspected. Existing splash wordmark,subtitle,spacing,background,loading and motion on icon canvases unchanged. Login/Registration unchanged.

## Latest — 2026-10-20 Restore centered icon on both auth screens

User clarified not to remove icon logo and supplied original1299:19(image274d62e30d3d1546da25c1baedf1f43cf1a79565). Restored exact image as118×118transparent square artwork in preserved366×122brand slots1383:3078and1459:413,centered with2pxvertical inset. Existing toolbar wordmarks1474:389/394remain. Both form/card and toolbar-wordmark bounds verified unchanged; source image hash matched. Login composite visually inspected. This supersedes the prior centered-icon removal decision; centered wordmark stays removed.

## Latest — 2026-10-20 Login/Registration toolbar branding

User confirmed exact linked asset1345:1449(full monochrome-light wordmark),rather than NH symbol. Login toolbar1355:2697and Registration1459:407now contain120×23.3668transparent wordmark instances1474:389/394at far-right,20pxscreen padding,centered in44pxbar. Removed centered symbol+wordmark nodes1355:2702/2700and1459:414/416; kept transparent122pxlayout reservations to preserve form positions. Source library and Splash unchanged.343/253non-brand node snapshots,Back geometry/reactions and toolbar320/360/390/420width checks passed;both screens visually inspected. Old brand node references below are obsolete. See [toolbar evidence](Evidence/2026-10-20_Auth_Toolbar_Branding.md).

## Latest — 2026-10-20 Screen 008 Registration + Consent ready for review

Created390×844Registration1459:256in008section1459:216under existing Onboarding. Matches finalized Login branding/card/components. User approved4required(Privacy,Terms,18+,child data)and3optional(Personalization/AI,Voice,Marketing),allOFF. Scroll form viewport292px; primary/Google fixed at556/682to avoid animation displacement. Shared Checkbox398:469,Button322:99,Primary loader329:6,Google329:33andSnackbar1420:18. Independent collection1459:217. Runtime normal1461:474,Google475,timeout476/477,snack478,country1462:435(245selectable rows). Login Register1355:2744now→Registration; Back/Log in→Login1355:2696. No other Login behavior changed.82saved graph checks passed;245country actions checked;default and expanded content visually inspected. Native text/search/API/persistence/accessibility/RTL/live Present unverified. Full legal text/009/031/032andOTP010still pending; no guessed links. legalAvailable default is a demo fixture,not approved legal provenance. Stop here for008review. See [screen handoff](Evidence/2026-10-20_008_Registration_Consent/README.md).

## Current baseline saved — 20 October 2026

Start with [current design baseline](Evidence/2026-10-20_V2_Current_Baseline.md) and [live-verified structure snapshot](Evidence/2026-10-20_V2_Current_Structure.json). This recap supersedes conflicting historical entries below. Latest instruction: Send code uses329:6and resets animation on entry; leave Google behavior unchanged. Google uses329:33in its processing overlays, dark dots, visible-disabled Send code. Inline host1444:174remains hidden. All splash branding uses Login artwork at existing splash-specific sizes/padding. Read reusable prompt, requested screen documentation and live V2 before the next screen. No new screen was requested by this save.

## Latest — 2026-10-20 Google loader restarts on processing entry

User reports inline animation still not playing. Replaced hidden-inline activation strategy with the working Send code pattern: Google processing/timeout overlay now displays white329:33loading instances1428:205/211/7655/7656with dark dot loop327:17→19→21→23→19. Click and Retry routes to1428:172and timeout swap to1428:7654now explicitly resetInteractiveComponents=true. Old inline host1444:174is permanently hidden with visibility binding removed so it cannot obscure active dots. White surface, original342×56geometry, Send code visible-disabled and reduced motion preserved.15saved graph checks passed. Live Present remains unverified due saved figma.com browser-access denial. This supersedes inline-rendering entry below.

## Latest — 2026-10-20 All splash branding uses Login artwork

Updated existing splash1131:2, reduced1146:2and existing QA1146:125/248/371with actual Login monogram1355:2702and wordmark1355:2700. Existing118×118icon canvases,26pxspacer,225×52title slots(203×52on320variant),subtitle,224pxlockup height and placements preserved; artwork proportionally fitted. Preserved existing motion and routes; title motion transferred to new wordmark containers. Main render inspected; five geometry/subtitle/route checks passed. Login/source assets unchanged. See [branding evidence](Evidence/2026-10-20_Splash_Login_Branding.md).

## Latest — 2026-10-20 Inline Google loader replaces overlay-painted button

Following continued user-reported mismatch, moved rendering into the original Google control1355:2734. New inline host1444:174contains329:33instances1444:175/181with transparent surface and no border, dark animated327:17/static327:25dots. Original Google frame itself supplies unchanged white fill/border/342×56geometry. Content1355:2735binds Google content visible1444:173; host binds Google loading visible1444:172. Google click and Retry set loading true/content false; completion, API/offline failure, timeout and Back/Escape cancellation restore loading false/content true. Send code remains visible disabled. Old Google overlay-painted instances1428:205/211/7655/7656are explicitly hidden; controller overlays still own timing/input blocking.17targeted structural/state checks passed; actual inline loading button resting render inspected by temporary variable preview with defaults restored. Live Present could not be inspected because saved browser security settings deny figma.com access. Do not claim live playback validated.

## Latest — 2026-10-20 Exact Login loader component IDs

Per explicit user request, Google normal/timeout and reduced-motion loaders1428:205/211/7655/7656now reference exact329:33(Secondary/Regular), overriding height to existing342×56Google bounds and preserving white surface/border, position and dark animated/static dots. Send code loaders1428:175/181/190/196retain exact329:6(Primary/Large). All eight main-component IDs verified live. Routes unchanged. This supersedes329:37Google reference in the prior entry.

## Latest — 2026-10-20 Google button retains white surface during loading

Google loading instances1428:205/211and timeout instances1428:7655/7656now use Secondary/Large loader329:37, the56px counterpart of requested329:33. All four retain exact Google idle1355:2734white fill, border,18pxcorners,342×56bounds and position24,618. Animated dark dots use327:17with verified327:19→21→23→19loop; reduced motion uses327:25. Appearance inspected. Send code remains visible disabled; no prototype routes changed. Live Present remains unverified.

## Latest — 2026-10-20 Language loader clipping and Google disabled Send code

Removed conflicting WIDTH/TRANSLATION_X keyframes from Language loader host1259:141, preserving350×64geometry and shared nested animated dots. Moved reduced-motion fallback1428:7745from page into host. Language still navigates after1.95s to1215:34. Google click1355:2734and Google Retry branch now keep Idle=true with disabled Send code during processing; OTP behavior unchanged.16targeted checks pass; repaired resting render inspected. Live Present unverified. Supersedes prior Google pending !Idle audit expectation. See [fix evidence](Evidence/2026-10-20_Language_Loader_Google_Disabled_Fix.md).

## Latest — 2026-10-20 Shared component integration in V2

Login now uses public NH/Button and NH/ButtonLoading instances, with shared NH/Snackbar for simulated offline/API failure and10second timeout. Runtime area1428:170contains processing1428:171, Google1428:172, normal timeout1428:173, Google timeout1428:7654, Snackbar1428:174. Retry/dismiss/cancel, duplicate blocking, input preservation and static reduced-motion dots are connected. OTP destination remains pending. Four Language Continue instances and four Intro CTA wrappers now use public shared Button visuals, retaining labels, geometry and routes. Language processing uses shared loader with no text flash.100saved graph checks passed; static visual QA performed. Live Present/backend behavior remains unverified. Country-commit controller removed in the prior task remains absent and needs separate repair. See [integration evidence](Evidence/2026-10-20_V2_Shared_Component_Integration/README.md).

## Latest — 2026-10-20 User-confirmed removal of both entire sections

Deleted sections `1355:2567` (Shared Buttons & Feedback) and `1383:3275` (Loading & Snackbar Overlays), including every child, after explicit user confirmation. Both IDs verified absent; main Login and Country Selector section remain. This supersedes older references to local masters and runtime overlays inside those sections. Dependent Login processing, Snackbar feedback and country-commit flows need replacement/reconnection; do not claim the complete prototype still passes earlier audits. No guessed replacement routes were added. See [removal evidence](Evidence/2026-10-20_Section_Removal.md). Dedicated reusable component library pages were not edited.

## Latest — 2026-10-20 Reusable Snackbar library component

Created `NH/Snackbar`1420:18on dedicated page1420:2, named `🧩 NH Components / Snackbar`, positioned after the existing Toast page. Sources1383:3295/1383:3294were re-inspected live: their current styling is square corners, dark #1C2B33surface,1pxwhite border at12%alpha, Poppins12/18message and gold12/18action. Do not restore older rounded Snackbar snapshots. Default350×60,44pxcontrols, Auto Layout height growth and text wrapping. Properties: Message, Action label, Show action, Show dismiss. Six configuration specimens are in1420:34;280px narrow case grows to70px without clipping. Shared matching message text style was reused; action/dismiss styles and scoped tokens were added.

Generic Action is host-owned and contains no Login variables/routes. Dismiss closes an overlay. Separate demo start1420:89opens overlay1420:98with a390×72bar at x0/y772, matching the source's edge placement. Local demo Retry/Dismiss feedback,6-second timeout, Escape and outside dismissal are connected. No requests are sent. Existing Login snackbar/overlay and Toast family were not replaced.55component/interaction checks and7source-preservation checks passed. Static layouts were inspected; live Present/device/accessibility tests remain unverified.

See [Snackbar handoff and evidence](Evidence/2026-10-20_Snackbar_Component/README.md). Future screens should use the new reusable master and screen-specific confirmed Action behavior; preserve the existing Login-specific retry logic unless explicitly migrating it. The overlay is a prototype template; actual safe-area/keyboard behavior remains the consuming application's responsibility.

## Latest — 2026-10-20 Button and Loading Button library synchronization

User explicitly authorized updating the existing library pages319:2(Button) and327:2(Loading Button) from final V2 source sections1355:2567/1383:3275. Public sets322:99and329:49retain their original IDs and30/6variants, with all public property IDs preserved. Primary now uses the exact final gradient,18px radius,Poppins SemiBold14/20,4px content gap,42% Disabled and88% Pressed. Default master width is342px; Large56px is the finalized mobile size, while Regular48px remains for compatibility. Secondary/Quiet remain contrast-appropriate and theme-aware. Optional local icon canvases are18px.

Loading Button is loader-only: three10px dots,7px gaps, centered44×10group. Private set328:2keeps its legacy name/Tone/Phase IDs but uses dots instead of arcs. Quarter/Half/ThreeQuarter loop with250ms steps,750ms cycle; Still is static. The old Label property is retained but visually hidden. Host screens still own submission and completion. Final Login sources were not modified or migrated to the public components.

New component-scoped tokens are in VariableCollectionId:1412:50. Opacity bindings use percentage token values42/88; node.opacity reads0.42/0.88. Shared foundation tokens were not edited. Existing consumers may inherit updated master styling/default sizes; no whole-file consumer-layout regression sweep was performed.

See [library handoff and evidence](Evidence/2026-10-20_Button_Library_Sync/README.md). Button321checks and Loader95checks passed,416total;30/6review instances,42valid Button state routes, source matching, properties and loop/Still graphs were verified. Light/dark specimens were visually inspected. Live Present playback, device/runtime accessibility and application integration remain unverified. Final source component fill/stroke/geometry/opacity preservation checks passed.

## Latest — 2026-10-20 Login top/bottom stars

User requested more stars on Login1355:2696 inside1355:2565, matching Splash1131:2. Atmosphere1383:3082 now has18stars:9above the card and9in the lower band. Fifteen added copies reuse original Splash artwork, sizes, gold/glow and staggered OPACITY keyframes. Stars remain outside the form, centered logo and registration text; the reduced-motion visibility binding remains intact. Final composition was visually inspected. Original Splash, content, buttons and navigation were unchanged.

## Latest — 2026-10-20 Login wordmark colors

User requested wordmark1355:2700match the NoorHeroes colors of linked Original Teal logo caption1306:733 (actual asset1304:202 on brand page1299:2). Reference was visually inspected: ivory “Noor,” gold “Heroes,” gold underline. Login wordmark now applies that treatment using existing ivory/gold palette tokens1300:4/5 and preserves native gold raster shading through an aligned crop of its original image. Only target1355:2700and its local tint overrideI1355:2700;1304:210were changed. Bounds120×23.3668, position, original image hash and source brand assets remain unchanged. Final rendered wordmark was inspected. The source label itself was not mistaken for the logo artwork.

## Latest — 2026-10-20 Loading button finish

User requested removal of the rounded stroke on loading master1383:3236 and instances1383:3277/3283. All three now have no strokes and use the exact multicolor gradient from active button1355:2582, replacing the flat language-loader teal. Content remains loader-only, with no visible text.342×56bounds,18px corners, existing dot animation and reduced-motion fallback are preserved. Gradient equality, absence of strokes/text and final rendering were checked. This supersedes earlier flat-teal loading-surface descriptions, while retaining the language dots/timing.

## Latest — 2026-10-20 Phone/Email selector reference match

Latest color refinement: user supplied #0C7372 and requested a slightly darker shade. Selected Phone/Email pills now use **#0B6867** (approximately10% darker), superseding #0F3333 below. Both selected-state variable defaults and switching actions were updated and checked; white container, transparent unselected segment, labels and layout remain unchanged.

User requested reference1355:3070's design on target1355:2713, changing only the button color to dark. Target now uses the reference's white container,1px #DBE6E0border,18px radius,4px inset/gap and164×44segments in342×52bounds. The selected pill uses existing dark #0F3333 with white text; the unselected segment is transparent with source #606B72text. Phone and Email preserve existing node IDs, mode switching, input persistence and readiness actions. Dynamic fill variables1383:3067/3068 now alternate dark/transparent; label color variables1396:3047/3048 alternate white/muted. Source1355:3070was unchanged. Both selection action branches and final screenshot were checked. This explicitly supersedes the earlier dark-container selector standard; other Login styling stays unchanged.

## Latest — Login standardization and consolidated prototype

The attached “Login Screen Standardization & Final Working Prototype” brief supersedes the earlier22-screen authentication implementation. Main Login remains1355:2696, now named `NH/Final/Auth/Login — Standard`, within Final Authentication1355:2564 → Onboarding1270:140 → NoorHeroes V2 Design1128:2. Use [current standardization handoff](Final_Authentication_2026-10-19/Login_Standardization/README.md) and [current node state](Final_Authentication_2026-10-19/Login_Standardization/figma-state.json). The older review notes below are historical.

One variable-driven Login now contains Phone/Email selection, preserved inputs, readiness and inline errors. Approved logo/wordmark are centered above a366px card,342px controls,20px vertical/12px horizontal padding,16px section/12px form gaps. The registration text is exactly “Don't have an account? Create an account?” in white plus brand gold. Dark method selectors stretch correctly on small widths. Card height466px includes one reserved validation line. Preserve existing artwork and the approved gradient/night palette.

Button source1355:2567 supplies Default/Disabled (42% opacity). Pressed and Loading have been restored as shared variants. Language1259:140 supplies exact3-dot artwork/timing; latest brief explicitly keeps Login loading342×56 instead of shrinking. Google uses a light loading surface and dark dots. Shared processing overlays1383:3276/3282/3288 provide normal/timeout/Google simulation with tappable Back cancellation. Snackbar overlay1383:3294 and component1383:3295 replace service-error screens, with44×44Retry/Dismiss,6-second dismissal and operation-specific recovery. Recreated country-commit controller1383:3307 restores245actual flag selections. Source Splash stars appear only outside the card; R previews reduced motion with static dots.

Twenty-one obsolete Login screens were checked for incoming references and moved out of active V2 to archive1386:5901. No source designs were deleted. All five existing Intro exits still target1355:2696 and four-origin Back behavior remains. No persistent QA screen duplicates were created. Final saved-action audit passed1,576assertions across552routes, zero missing destinations/active archive links. Static390/320/430layouts and loading/snackbar compositions were inspected. Input/search are fixtures, not actual entry/filtering. Live Present, physical devices, actual keyboard/safe-area behavior and runtime accessibility remain unverified. Native overlays target390×844; snackbar overlays require dismissal before form interaction.

**OTP success and Registration remain unmapped until approved destinations exist.** Simulated completion closes loading and restores enabled Login without claiming authentication. Do not create future screens or guess connections. The guide1391:3057 is a review artifact, not a product screen. Read current live nodes before any edit; users may manually delete states. The current audit/source is under `Login_Standardization/evidence/`; prior counts and original geometry-preservation claims are superseded.

## Latest — 2026-10-19 Final Authentication Prototype

This entry supersedes the rejected October 18 generated authentication layouts below. Use the user's manually corrected Login1330:5697 and country selector1330:5691 as visual sources. Final work is1355:2564 under NoorHeroes V2 Design1128:2 → Onboarding1270:140; main Login1355:2696. Six groups contain approved Login states, country picker, buttons, loading, errors/retry and connected flow. Original sources remain intact; older generated Login states are archived outside active V2 in1358:5860. Intro exits now target the final Login and Back preserves all four origins.

See [final review handoff](Final_Authentication_2026-10-19/README.md), [saved-action audit](Final_Authentication_2026-10-19/evidence/native-graph-audit.json) and [node state](Final_Authentication_2026-10-19/figma-state.json). Saved reaction evaluation passed1,256assertions with847node routes, zero missing destinations and no routes into rejected layouts. Country selection now uses245actual flag assets rather than an ISO-only label. Phone examples are sourced valid mobile examples, replacing the older5551234567 fixture. Inputs and search are still explicit native simulations; no Code Layer, API or real authentication was implemented. Present playback remains unverified because figma.com browser access is denied; do not bypass it.

**Latest user decision: leave success destination pending until OTP is approved.** Do not create or guess OTP routes. Simulated completion currently restores the corresponding ready Login view. Register remains unmapped; manually removed Forgot access was not reintroduced. Do not treat copy/layout approval as final-screen sign-off or advance automatically. Verify live nodes before editing. Refer to final handoff for fixtures, timeout/retry behavior and the separate guarded conditional-action workaround.

## Latest — 2026-10-19 Login header wordmark

User requested exact light wordmark1345:1449 on Login1330:5697, aligned to Back at the header's right edge. Latest refinement: Header1347:726 contains wordmark instance1347:727 at120×23.367px,80%opacity and transparent background,20px right inset, vertical center40px matching Back. Form/body bounds and Back reactions were preserved, including recent manual edits. Only this specified Login frame was updated. See [header evidence](Evidence/007_Login_Header_Wordmark_2026-10-19.md).

## Latest — 2026-10-18 Authentication redesign

The attached Login/Branding/Country Selector brief authorized a new separate section in the same file: `NoorHeroes V2 — Authentication Redesign`1330:5686, Mobile page928:2. All15current V2 Login states are copied/redesigned, four Language states carry approved monogram branding, four unchanged Intro copies complete the confirmed flow. Main redesigned Login1330:5697; Language1330:7288; country sheet1332:1815. See [redesign handoff](Authentication_Redesign_2026-10-18/README.md), [validation](Authentication_Redesign_2026-10-18/VALIDATION.md) and [node state](Authentication_Redesign_2026-10-18/figma-state.json).

User approved an embedded functional Code Layer. Fresh account checks, including the explicit retry, return `code_layers_enabled:false`; no import or new file was attempted. Local functional companion is prepared at Authentication_Redesign_2026-10-18/prototype/ and http://127.0.0.1:8765/ while its local server runs. Actual search/selected-flag replacement work locally; native Design search is explicitly simulated, and native selected country uses an ISO label. Do not claim the Code Layer is embedded or native filtering is implemented.

Native audit:183 node destinations, none missing; zero original Login copy omissions across15states;245country rows/flag assets. Screenshots and structural checks are recorded. Opening live Present was blocked by a saved browser permission denying figma.com access; do not work around that restriction. Native playback and physical-device checks remain unverified. OTP/Register/Forgot-access/Google-success exits remain unmapped until confirmed screens exist. Preserve original designs and new review copies. Do not automatically promote the unreviewed redesign over finalized source standards or advance to another screen.

Saved: 2026-10-13. Latest execution: Screen 007 Login implemented for review; see the latest entry below. Earlier entries preserve historical decisions and are superseded by later explicit updates.

## Latest — Screen 007 Login implementation

User approved the proposed Login copy/layout in this conversation. Evidence/007_Login_Execution_Review.md records the implementation and limits. Main screen1278:155, Email1278:780;15 same-size390x844 states plus country overlay1282:466, all under Onboarding1270:140. All four Intro Skip controls and final1219:246 now route to1278:155, recording the invoking Intro for Back. Existing forward Intro, Splash and Language connections were not targeted.

Phone/email form taps populate sourced test fixtures (5551234567, test@example.com); prototype variables preserve them across tabs/retry. This is simulated entry, not a native editable field or real authentication. Send code -> animated pending ->10-second timeout scenario; Google ->2-second simulated generic failure, with cancellation and Google retry. Offline controls remain disabled during tab/input changes; Try again simulates connectivity recovery. Country picker offers only project fixture codes+1/+971. No production country coverage claim.

OTP010, Registration008, Forgot Access030 and Google success routes are still unmapped per user rule; do not create substitute destinations. Next numbered screen is008 but await Screen007 review. Copy proposal was approved, not the finished screen. Live Present playback was not exercised; graph and screenshots were verified. No further screen is authorized automatically by this handoff.

Original source frames were not targeted by writes. Their dimensions/child counts remained stable, but their canvas X positions changed during this live session; the cause is unverified and their positions were not restored over potentially concurrent user changes. See review for recorded values.

## Scope and source rules

Existing file: https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP
File key MR9935oQZACMjndzGIUgq5. Mobile page 928:2. V2 section 1128:2.
Work exclusively within V2. Preserve original Frame 1 (1095:2), Frame 2 (1085:13003), web/admin and unrelated designs. Never create another file. PRD_Documents, Development_Blueprints and Screens are read-only. Generated documentation belongs in sdocs.
Verify live node existence before further modifications; user may delete or change screens between turns.

## Latest approved screen decisions

### 001 Splash

Main V2 Splash: 1131:2. Existing brand, logo, title and subtitle retained according to the user's later screenshot instructions, which superseded the earlier wordmark-only preference. Sharp moon, restrained synchronized motion; stars around the icon were requested removed. Do not rebuild or infer the logo.
Latest verified prototype reaction: After Timeout 4 seconds -> Language English-selected 1166:215, Dissolve 300 ms Ease In And Out.
Other Splash QA/reduced-motion frames remain outside the current button task and must not be removed without authorization.

### 002 Language Selection

Exactly four preserved Language mobile screen states:
- 1166:215: NH/Enhanced/002/Language_Selection/Selected-en
- 1166:250: NH/Enhanced/002/Language_Selection/Selected-hi
- 1166:285: NH/Enhanced/002/Language_Selection/Selected-ar
- 1166:320: NH/Enhanced/002/Language_Selection/Selected-ur

Copy: Choose your language; Select the language for your experience; Continue.
Languages: English / English, Hindi / हिंदी, Arabic / العربية, Urdu / اردو.
Four languages were explicitly approved. The user's later reference and button requests authorized Continue despite earlier immediate-advance preference and PRD conflict; do not silently change back.
Each language row selects its corresponding screen. Selected row has no redundant navigation.
Cream #FAF7F0, teal #0E7C7B, primary text #1C2B33, secondary #606B72. Poppins; script-appropriate Noto fonts. 390 x 844 mobile canvas. Language cards 350 x 81 with 18 px radius. Footer button 350 x 64 at x20/y752. Preserve exact verified assets and copy.
Language cards now have entrance opacity 0 -> 1 plus translation Y 12 -> 0, 320 ms Ease Out, starting 80 ms with 70 ms stagger.

## Latest button implementation

Local component set 1194:62: NH/Local Components/Language Continue — Interactive.
Instances 1194:69, 1194:82, 1194:95, 1194:108 in the four Language screen footers.
All variants retain a fixed 350 x 64 footprint. Inner button morphs from full width to centered 180 x 64. Continue stays 19 px; label fades rather than scaling/distorting.
Variant IDs:
- Idle: 1194:2
- Loading0: 1194:12
- Loading1: 1194:22
- Loading2: 1194:32
- Loading3: 1194:42
- Loading4: 1199:38
- Loading5: 1199:48
- Return: 1194:52

On Click Idle -> Loading0, Smart Animate 320 ms. Loading variants advance with 10 ms waits and 320 ms Ease In And Out transitions, producing two three-dot pulse cycles. Final phase -> Return takes 420 ms. Return -> Idle after 10 ms without visible change, allowing retry.
No visible success message/checkmark or separate Success screen. Old component descendants for spinner/rail/checkmark are hidden and disconnected; deletion was rejected by Figma, so do not repeat the invalid remove operation.
Keyboard E during loading demonstrates error restoration via Return and allows another click. This is a prototype test mechanism, not production error logic.
Processing uses fixed mock timing. It does not persist data, wait for backend success or provide an indefinite server-conditioned loop.

## Validation and evidence

Current review: Evidence/002_Compact_Button_Review.md.
Figma writes accepted; reaction graph, fixed bounds, Splash timeout and entrance tracks checked. Resting Language and compact dots screenshots inspected. Interactive Present playback has not been exercised. Earlier native-motion MP4 files and full-screen Loading/Success reviews are historical and do not verify this component revision.

## Next screen

Prompt: Screen_Prompts/003_Intro_Slide_1_Stories.md.
Read that prompt and its exact PRD/blueprint references before creating the screen. Inspect original Frame 1/Frame 2 and relevant Screens references live. Do not invent copy or Islamic content.
Screen 003 has NOT been built or approved in V2. The temporary Intro handoff was deleted by explicit user request. User explicitly chose to keep the success destination pending until Screen 003 is ready.
Create only the next authorized screen and necessary dependencies in V2, preserve all current screens, validate and stop for review. Do not implement remaining prompts automatically. Resolve eventual Continue -> Intro wiring after Screen 003 exists, respecting the latest button return sequence.

## Screen 003 update — 2026-10-13

Screen 003 now CREATED FOR REVIEW, node 1207:34, 390 x 844, V2. User approved Stories first with Frame 2 exact heading/description and existing image; omit spotlight/playback and extra claims. Current review: Evidence/003_Intro_Slide_1_Review.md. Previous statement that Screen 003 is not built is superseded.
Continue Return 1194:52 now navigates after 250 ms to 1207:34; E error shortcut restores Idle without navigation. Back uses history. Next/Skip destinations remain pending (Screen 004/Login absent). Next implementation prompt is Screen 004 only after Screen 003 approval. No multi-size variants created. Present playback remains unverified.

Correction: Figma rejected the Return component navigation write and rolled it back. Language -> Intro remains pending; existing Return -> Idle button behavior is preserved. Screen 003 exists successfully at 1207:34. Review it directly. Next and Skip also remain pending.

## User-directed intro sequence replacement — 2026-10-13

Supersedes prior Stories-first decision. User requested existing Frame 1 sequence starting from linked 1095:704. Inspected named siblings and recreated Welcome -> Quran & Stories -> Daily Habits & Duas -> Family & Parent Shield in V2. Removed only former V2 Stories Intro 1207:34.
New frames: 1215:34, 1215:138, 1215:246, 1215:356. One standard 390 x 844 viewport each, vertical overflow preserves longer source content. All text strings matched original frames exactly. Original references 1095:936/704/862/788 unchanged. Source illustrations reused. Arabic-containing labels now use Noto Sans Arabic Bold to repair missing glyphs, strings unchanged.
Added restrained 400 ms fade/rise entrance tracks with 60 ms stagger; first three CTA links advance through sequence with 250 ms Dissolve. User-directed order overrides PRD Stories-first order for this design revision; keep recorded as explicit exception. Source trust claims retained as source copy, not independently verified.
Language entry remains pending due component-source navigation restriction. Skip/final Get Started destinations remain pending until Login exists in V2. Present playback not exercised. No new multi-size QA variants. Review current sequence before further screen work.

## Unified intro styling — 2026-10-13

All four current V2 intro frames refined in place: 1215:34/138/246/356. Original references unchanged. One 390 x 844 viewport each. Shared cream-to-pale-teal gradient (#FAF7F0, #F3F7F2, #DFEEEA); Poppins Latin typography with Noto Sans Arabic for Arabic-containing category labels. Main heading20 SemiBold, body12, feature title12 SemiBold, feature description11, CTA14 SemiBold, supporting copy9. Exact main headings/descriptions/card labels/CTA/supporting text retained. Reused original illustrations and feature icons (36 x 36 container); source feature icon artwork retained, including its original vector/emoji differences.
Shared positions: hero0..220, content236, heading264, description330, cards414; three82-high cards,10 gaps; indicators700, CTA724 (350 x56, radius18), supporting text792. Button row centers label+18px vector arrow with10px gap, white on #0E7C7B. Supporting copy centered gray. Shared400ms staggered fade/rise and250ms Dissolve between first three CTA destinations.
Four screens visually reviewed via screenshots across composition/fix calls; position dot overlap fixed. Present playback unverified. Language entry, Skip and final Login destination remain pending. Icon source differences remain retained rather than replacing approved assets. Prior child node IDs superseded by this refinement; root IDs stable.

## Connected language and intro prototype — 2026-10-13

All four Continue instances now open Processing Overlay 1228:34 (390 x 844, transparent, CENTER, background interaction NONE). Overlay contains button at20/752, morph350->180->350 with three pulsing dots, then AFTER_TIMEOUT2.5 seconds navigates to Welcome1215:34. All actions accepted and reaction graph inspected. Underlying controls are blocked during overlay; E or Escape closes it for retry without changing selected Language frame. Processing is fixed prototype timing, not data saving. Prior orphan component Return navigation rejected and rolled back; instance overlay routing now replaces it.
Intro forward path remains1215:34 ->1215:138 ->1215:246 ->1215:356. Added visible44 x44 Back controls1228:95/98/101/104 using BACK/history. Previous language remains represented by originating frame; prototype history is not production/local-storage persistence. User-directed Welcome-first and Continue-button exceptions remain approved over PRD baseline.
K-02 requires bundled offline Intro and no API dependency. No internet, failed remote fetch, timeout or empty remote content should use the same bundled intro route, not add an artificial network error blocking screen. Actual simulated network toggles not implemented. Language localized intro strings/RTL not supplied; current English copy retained without translation invention.
Remaining completeness blocker: Screen007 Login prompt explicitly marks exact copy unavailable and both source frames missing. Skip/final Get Started cannot connect to a fabricated or substitute Registration screen. Requested authoritative Login copy/reference from user. Authentication controls and errors remain outside implemented screens. Present playback, motion render and device interruption/persistence tests have not been executed; graph validation alone is not end-to-end playback validation.

## Material rounded icon and navigation refinement — 2026-10-13

Four V2 intros only: root1215:34/138/246/356 and hero top-left/top-right radii0, bottom radii retained. Back/Skip white paint alpha0.82, white border alpha0.35, control opacity1 to keep labels/icons crisp. Existing44px hit targets and reactions unchanged. Back arrow, CTA arrows and all12 feature icons replaced with official Google Material Icons Round SVG assets, 24px optical canvas, native filled rounded geometry (no artificial stroke added). Feature containers36px, teal glyphs on8% teal fill, radius10. Button rows re-centered after arrow replacement. All main copy, theme, layout and route destinations preserved. Two representative screenshots reviewed; live playback not exercised.
Source https://github.com/google/material-design-icons; SVG source map Evidence/Material_Round_Icons/icons.json. Existing missing Login destinations remain unmapped under user's explicit rule; never guess or create placeholder routing.

## Transparency and content-hugging pills — 2026-10-13

Four intro Back/Skip and bottom-center hero badge fills now white45% alpha (55% transparent), border20% white. Text/node opacity1. Hero badges use horizontal auto layout, hug content,12px side and7px vertical padding, centered under illustration. Badge text dark #1C2B33 for readability. Existing Figma Material icons verified24 x24 and retained; no new external icons imported. Copy, route reactions, gradients and other layout unchanged. Quran and Parent screenshots reviewed after write. The interpreted bottom-center text is the pill at the bottom of the hero illustration, previously350px wide.

## Restored original caption and footer icons — 2026-10-13

Hero caption icons cloned directly from original source containers1095:941/710/867/793 into matching Welcome/Quran/Daily/Parent pills. Original dimensions22x21,18x17.5,7.38x16.5,8.56x16.5 respectively retained per explicit request (supersedes uniform24px for these caption assets only). Pills auto-hug icon+text with6px gap and existing transparency/padding. Quran footer icon from1095:784 and Parent stopwatch from1095:858 restored. Welcome/Daily existing inline lock glyphs retained without duplication. Supporting content now sits in a centered horizontal hug row within350px footer,6px gap and vertical centering. Source icons never altered; route reactions unchanged. Quran/Parent screenshots checked.

## Uniform icon canvases — 2026-10-13

Caption/footer icons now use24 x24 canvas with20px optical artwork, centered both axes; Material feature/navigation/button icons retain24 x24 canvases. Caption/footer icon-text gap8px; auto-hug pills and footer rows re-centered. Extracted existing inline lock glyphs into separate icon slots while preserving accompanying copy. Existing emoji icon meanings retained with Noto Emoji rendering to avoid clipped source glyphs. Daily/Parent screenshots reviewed. Colors, gradients, content semantics and navigation unchanged. Caption/footer20px optical versus24px main Material artwork is intentional for balance with smaller text; canvas dimensions uniform.

## Final icon sizing override — 2026-10-13

User explicitly requested18 x18 canvases and4px icon-to-text gap. Applied across all four intros: Material navigation/feature/button icons18px; source caption/footer icon containers18px with centered16px optical artwork. Caption pills, footer rows and button label-arrow groups use4px gaps and were re-centered. Touch targets unchanged. Daily screenshot reviewed. This supersedes prior24px/8px sizing rules. Navigation unchanged.

## Alignment/clipping fix and bottom icon override — 2026-10-13

All footer icon canvases14x14, gap2px, inner artwork12px. Caption18px and navigation/feature18px retained. Caption auto-layout padding12px horizontal/8px vertical, centered icon+text, gap4px. Feature containers now symmetric zero padding with centered children; inherited uneven padding removed. Footer row padding4px all sides,22px row vertically centered in24px footer; content centered atscreenX195. Clipping disabled on necessary nested rows/containers. Emoji icons now fixed-size text boxes with centered12px font for14px canvas and no text auto-height wrapping; timer previously18x36 now14x14. Restored vector networks were malformed when rescaled; re-imported exact original icon-container SVGs from1095:941/710/784 into proper canvas wrappers to repair visual bounds. Verified Quran after final fix plus Welcome/Parent composition. Content/routes/transparency unchanged. Supersedes prior footer18px/4px settings.

## Complete consistency audit supersedes isolated sizing fixes — 2026-10-13

See Evidence/Intro_Complete_Consistency_Review.md. All four V2 intros audited and visually compared side by side at equal0.85 scale. All visible icons now component instances from a single Material Round family,18px main/14px footer; shared text styles, centered Auto Layout cards/copy stacks/rows. Component library frame1253:34. Caption/footer centerX195 verified. Temporary review removed. Copy comparison passed; original references and navigation unchanged. This supersedes prior mixed-source glyph and manual-positioning instructions for current V2 intros only.

## Continue connection restoration — 2026-10-13

Live inspection found prior Processing Overlay1228:34 deleted and all four Continue reactions empty. Restored a required transparent390x844 processing overlay and reconnected all four instance buttons. Button morph/pulsing dots/restore completes at2.35seconds; overlay AFTER_TIMEOUT2.5seconds navigates automatically to Welcome1215:34 with250ms Dissolve. Escape closes for cancellation; underlying controls blocked. Canvas graph accepted and inspected; live Present playback not tested. Processing overlay is a necessary prototype dependency and should not be removed during screen cleanup.

## Direct redirect after progress — 2026-10-13

User superseded button-return behavior. Processing overlay1259:140 now keeps compact180px loading state and label opacity0 after initial fade. Removed full-width restore and Continue reappearance. After1.95seconds navigate directly to Welcome1215:34 with200ms Dissolve. Pulse keyframes finish at1.65seconds and final processing hold lasts300ms; no restored-button phase. Four Continue entry connections unchanged; Escape cancellation retained. API reaction/track update accepted; Present playback untested.

## Back arrow color match — 2026-10-13

All four intro Back arrow instance vector fills now match the corresponding Skip text color #1C2B33. Component masters and other icons retain teal. Background transparency, size, alignment and navigation unchanged.

## Approved ongoing visual source of truth — 2026-10-13

User finalized the design and instructed automatic reuse for every upcoming screen. Mandatory baseline:12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md. Read it before every screen; all237 individual prompts now link it. It supersedes older conflicting visual guidance. PRD/blueprints still govern behavior and exact content. Verify live finalized refs1215:34/138/246/356 and reusable components1253:34. Perform side-by-side equal-scale comparison plus1x new-screen inspection before handoff; fix discrepancies. Do not ask the user to repeat icon/type/spacing/color rules. No new screen or Figma change performed in this documentation update.

## Finalized Figma organization — 2026-10-13

Main section1128:2 renamed NoorHeroes V2 Design. Nested Onboarding section1270:140 created. All15 current onboarding frames and dependencies moved inside, retaining IDs, visual positions relative to their module, original-source bounds/counts and all25 reaction definitions. Language naming repaired to002; current root naming NH/V2/Onboarding/<number>/.... Future work automatically follows13_INCREMENTAL_MODULE_ORGANIZATION.md: derive owner/name from PRD, create section only when module work begins, no speculative module sections. All237 prompts inherit this through12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md. No new designs or future modules created.

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

## Responsive follow-up — 2026-10-21
All six new consent/detail overlays have stretch backdrops, responsive horizontal sizing, and bottom positioning. Legal panels use flexible document viewport height; paragraphs and fixed actions resize with the panel. At 320×568, legal panels are 320×444, inner body/actions 268 px wide, with 134 px scroll viewport; text wraps without horizontal clipping. Optional sheet remains 380 px high at y188. Checked six panel bounds, two button widths and two legal text widths. Compact screenshots reviewed; all frames restored to 390×844, no QA frames created. Additional results: Evidence/2026-10-21_Consent_Bottom_Sheets_Responsive.json. Total: 39 structural/graph/layout checks passed; Present playback remains unverified.

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

## 2026-10-21 — Standard NH inputs and controlled HTTP companion

Latest input layout supersedes earlier 72/104 values: Login field height variable 1552:429 and Registration 1464:254 are now 88 default / 116 error, with the source NH 56 px boundary. Genuine NH TextField 357:2 instances: Login 1563:936; Registration 1563:1399. Their State properties are variable-bound; originals/source masters untouched. Country controls remain in transparent interaction overlays. Dynamic loader layout hosts follow the new height (Login primary/Google Y514/618 default; Registration Y568/672; error adds28).

Native D review panels: 1563:946 / 1563:1409. G focus, B blur, V fictional fill, C clear, Q required. Scrollable cases demonstrate invalid phone/email, 422 inline, safe global failures, network, timeout, 429 and success. Google field-response errors remain global. Native Snackbar Retry visibility is configured per outcome; native 429 holds overlay15s. Success destination still pending approved OTP.

User approved extending the existing local prototype because whoami reports code_layers_enabled:false. Functional companion: Authentication_Redesign_2026-10-18/prototype/index.html, app-v2.js, auth-core.cjs, auth-v2.css, server.cjs. Start node server.cjs and use http://127.0.0.1:8766/ (8765 is the older server). It supports true input/focus/blur, libphonenumber-js/max1.13.15 international validation, validator13.15.35 email validation, real controlled HTTP responses, inline/server-safe Snackbar mapping, Retry-After, duplicate guards, distinct loader styles, country/value preservation in RAM and existing consent flow. No production auth/OAuth request or Code Layer.

Evidence: Evidence/2026-10-21_NH_Input_Handoff.md and Verification.json; five test groups,32 native action checks, eight variant mappings,245 country checks, visual/browser verification. Present playback, real device keyboard and production auth remain unverified. Continue only with a user-selected next screen; do not invent OTP routing.

## 2026-10-21 — User approval: finalized through Registration

The user confirmed the current design through Registration is correct, no changes are required, and requested saving context for future reference. Treat all current Onboarding screens through Registration and their current dependencies as the approved visual baseline. Do not make further design changes or advance to another screen without a new request.

Read Evidence/2026-10-21_Approved_Through_Registration_Baseline.md first when resuming; it consolidates current IDs, input measurements, loader boundaries, consent behavior, prototype limitations and future-work rules. The reusable prompt now points to this approval. OTP remains pending/unmapped. This approval does not imply production backend, legal, device-keyboard or Present validation. No Figma designs were changed while saving this context.

## 2026-10-21 — Screen 009 consent details implemented; awaiting review

User chose to keep the existing bottom-sheet format. Screen009 is now grouped under Onboarding in section1588:337. Terms1588:346, Privacy1588:381, Child-data1588:418; optional detail IDs1514:354/384/414 retained and reused. All six are390x844 with720px bottom sheets, fixed Close/footer and scrolling exact draft text. The child-data detail shares the approved full Privacy source; no standalone policy was invented.

Read links now open shared Loading1588:486, then the confirmed document. Error1588:533 supports Retry. Close/Escape/backdrop return to the invoking agreement/preferences sheet with no consent-choice writes. L online-load, O offline, C cached, E failure, N recovery. Legal availability blocks acknowledgement/account actions on failure and restores correctly after cancellation/recovery. Main Login/Registration layouts, branding, inputs, action styles and explicit Terms-to-Privacy agreement sequence preserved; necessary Read and availability dependencies only. No OTP connection added.

96 final structural/action/geometry checks passed and defaults restored; screenshots inspected. Published legal version still unavailable: footer states Version pending legal review / Prototype draft - Legal review required. Production version criterion remains open. Present playback and real network/cache/screen-reader behavior unverified. Handoff: Evidence/2026-10-21_009_Consent_Detail_Handoff.md. Screen009 is NOT yet user-approved; do not advance automatically.

## 2026-10-21 — Screen 009 rolled back by explicit user request

The user requested rollback of the last design change. The entire Screen009 implementation was reverted, restoring the approved state through Registration. Section1588:337, its new reading/loading/error views and009 variable collection were removed. Optional detail IDs1514:354/384/414 are back under Registration1459:216 at their previous coordinates, with380px sheets and the original Read/Back/Escape behavior. Added Read controls and legal-availability bindings/guards were removed; agreement handlers and Registration R/L handlers restored. Main Login and Registration designs, prior NH TextFields, loaders, snackbars, and the local companion were preserved.

No dangling009 action/property references were found after rollback. The009 implementation handoff and screenshots are retained only as historical evidence and marked rolled back. Screen009 has not been approved or advanced; resume from the user's approved-through-Registration baseline. Rollback evidence: Evidence/2026-10-21_009_Rollback.json.
# 2026-10-21 — Screen 010 OTP implemented; awaiting review

Latest continuation: [Screen010 OTP handoff](Evidence/2026-10-21_010_OTP_Handoff.md). User approved the documented mobile OTP copy, proposed error copy and finalized Login styling. Main1612:1277 in Onboarding section1612:1246,390×844; six existing NH/OtpCell instances, approved auth shell, Send-style dot loading, shared Snackbar and mobile tap keypad. Normal Send/Create complete routes1428:171/1461:474 now enter OTP; Google behavior remains unchanged. Back returns the invoking Login or Registration with existing values/consents retained. Success and fallback destinations remain unmapped until approved. Screen009 rollback preserved; local companion unchanged.

27 stored-action checks,17 structural checks and9 approved/original screen preservation fingerprints passed. Visual states inspected. Native input/paste, server time, persistence and network are controlled simulations; Present playback remains unverified.15s lockout is a review fixture, not server policy. This does not approve Screen010 or authorize Screen011. Follow the handoff for exact IDs and limitations.

## 2026-10-21 — Screen 011 rolled back by explicit user request

Screen011 section1636:477 and its40-variable collection were removed, including all fallback sheets, processing/timeout views and review examples. Restored Screen010 Resend, delivery-failure review case and processing behavior; removed fallback reset additions from the OTP Reset control; restored the incoming OTP actions on Login1428:171 and Registration1461:474. The prior OTP screen1612:1277 and its existing flow remain. V2/Onboarding dimensions restored to4800×9734 /4700×9634.

Twelve prior screen/reference preservation checks passed, no dangling011 references or variables remain, and29 saved reaction/action comparisons passed. Screen009 rollback remains intact; the local companion was unchanged.011 evidence files are historical and inactive. No further screen work is authorized by this rollback. See [rollback verification](Evidence/2026-10-21_011_Rollback.json).

## 2026-10-21 — Screen 012 Parent PIN implemented; awaiting review

User approved Frame1’s4–6-digit instructions, confirmation/validation copy and PRD behavior. Main1650:502 in Onboarding section1650:465 is390×844, using finalized auth shell, shared keypad/buttons, masked14px indicators, primary dot loading and Snackbar. The prototype holds counts only; PIN values are not stored and match/mismatch is a controlled fixture. Four-to-six-digit choice, confirmation, mismatch clearing Confirm only, format error, saving, offline/API/timeout Retry are wired. No real hashing, backend or OS biometric implementation.

Only the explicit verified-new-parent/consent-complete OTP review branch routes to012. Generic/returning success remains unmapped; successful resend is preserved. New OTP review cases1651:526/1651:529; review height800. Biometric013 and Add Child014 remain uncreated/unmapped.009/011 rollbacks remain intact, and the local companion is unchanged.

28 stored-action and15 structural checks passed;12 prior screen/source visual fingerprints unchanged. Default/confirmation/mismatch/saving/offline screenshots inspected. Present playback unverified. See [PIN handoff](Evidence/2026-10-21_012_PIN_Handoff.md) and [verification](Evidence/2026-10-21_012_Verification.json). Stop at012 for review; do not advance automatically.

## 2026-10-21 — PIN length selection removed; Continue enables automatically

Latest012 behavior supersedes the prior explicit4/5/6 choices. Removed selection controls from main1650:502 and all four review states. Set-pass input accepts up to6 masked positions. Continue:0–3 disabled,4–6 enabled; deletion below4 disables again. Continue captures entered length for confirmation. Preserve all previous confirmation, mismatch-only-clear, save/loading, recovery and navigation behavior. Count-only prototype still stores no PIN values; matching is simulated.

39 stored-action checks passed;12 prior design/source visual fingerprints unchanged; default layout visually inspected at390×844. Current card height480. See [automatic-length verification](Evidence/2026-10-21_012_Automatic_Length_Update.json) and latest section of the [PIN handoff](Evidence/2026-10-21_012_PIN_Handoff.md). Earlier selector IDs/state examples are historical. Future013/014 destinations remain unmapped;009/011 rollbacks remain intact. Present playback unverified.

## 2026-10-21 — Screen 013 implemented; awaiting review

Latest continuation: [Biometric enrollment handoff](Evidence/2026-10-21_013_Handoff.md). User approved proposed copy and existing bottom-sheet layout. New section1670:1061 inside existing V2/Onboarding,390×844 offer1670:1069, annotated system simulation1670:1136 and retry/error1670:1206. Existing PIN save1650:844 opens the optional offer only after success/Saved and eligible hardware; unavailable hardware hides it entirely. Skip/cancel/errors retain PIN fallback. Add Child014 remains uncreated/unmapped.

29 stored-action checks and39 automatic-length PIN regression checks passed;11 prior visual fingerprints unchanged. Screens009/011 remain rolled back. Present playback, OS authentication and hardware detection unverified; controlled fixtures only. Local companion unchanged. Stop for013 review. This entry supersedes earlier013-uncreated notes without approving or advancing014.

## 2026-10-21 — OTP inline recipient and Edit revision

User requested single-line “We sent a 6-digit code to •••1204” with Edit after an exact10px gap. Updated OTP main1612:1277 and four review compositions, reusing the existing recipient binding and correction control rather than a second standalone dot row. Inline text gap4px; Edit44×44 hit area, text left aligned for exactly10px visible separation. Original live Login/Registration correction routes preserved. Both incoming auth processing fixtures now set the approved masked example instead of bare dots; other actions unchanged. Five rows fit at390×844 with no wrapping; final screenshot inspected. [Evidence](Evidence/2026-10-21_010_Inline_Recipient_Update.json). Screen013 remains awaiting review; no later screen created.

## 2026-10-21 — Connected OTP/PIN/Biometric navigation repaired

Latest: [navigation handoff](Evidence/2026-10-21_010_012_013_Navigation_Handoff.md). Registration processing now carries actual four-required-consent eligibility into OTP instead of forcing the new-parent flag false. OTP success automatically enters PIN; PIN save opens the existing eligible biometric offer. PIN Back/Escape restores a usable OTP state; review Success preserves actual registration context. Duplicate inherited review/timeout flow starts removed. Use **New parent — Registration → OTP → PIN → Biometrics** at1459:256 to test the full journey. Direct/generic Login OTP still has no invented returning-account destination; Add Child014 stays unmapped.

24 connected-flow checks and39 PIN regression checks passed;21 destinations resolve and7 checked visual fingerprints are unchanged. Stored-action evaluation only; Present/real OS authentication unverified. No new screens or visual changes. Screen013 still awaits user review; do not advance014 automatically.

## 2026-10-22 — Latest: single PIN entry, direct Biometric, no success dialog

User explicitly removed PIN confirmation and clarified **no success dialog**. [Current handoff](Evidence/2026-10-22_Single_Entry_PIN_Handoff.md) supersedes prior two-pass PIN/navigation notes. All successful OTP verification now enters Set Parent PIN1650:502; resend and invalid OTP do not. Enter4–6 digits once → Continue saves → existing Biometric offer1670:1069 if eligible.0–3 disabled, max6, deletion below4 disables. Saving/error/retry/timeout and Back/Escape are wired without a confirmation step. Confirmation/Mismatch review compositions removed; residual copy/actions cleared.

Approved star artwork added24px beneath all five OTP card compositions.33 stored-action checks pass;21 destinations resolve; no confirmation copy/actions remain. Screenshots inspected at390×844. Present/real secure PIN storage/OS biometric work remain unverified or simulated. Add Child014 remains uncreated/unmapped; no placeholder added. Stop for review.

## 2026-10-22 — Preserve every Parent PIN screen; removed references restored

User explicitly instructed: do not remove any screen from section1650:465. Main1650:502 was never removed. The two deleted review frames were reconstructed as editable source-based references in their previous positions: Confirmation1709:675 at40/1040, Mismatch1709:947 at500/1040. Original deleted IDs1654:544/1654:840 cannot be reused. All eight390×844 screens are present, plus the fixture panel. Restored references have no incoming prototype edges; active flow still uses one PIN entry and goes directly to Biometrics. Keep all these frames; do not delete reference screens to remove a step from live navigation.

Visual section review captured in Evidence/2026-10-22_PIN_References_Restored.png. Both restored cards fit within844px. The older “zero confirmation copy” audit is superseded only for archived reference compositions; the live flow remains confirmation-free.

## 2026-10-22 — Latest: separate Confirm PIN screen restored to live flow

User now explicitly requests **Set Parent PIN1650:502 → Continue → Confirm your Parent PIN1709:675 → Save PIN →013 Biometric Enrollment1670:1069**. This supersedes earlier single-entry notes. [Current handoff](Evidence/2026-10-22_Two_Screen_PIN_Handoff.md). Continue captures4–6 entry length and navigates without saving. Confirmation requires that many positions; Save processes the controlled matching fixture. Back retains first entry; failures retain both counts for retry. No success dialog.

All eight PIN screens are preserved.39 stored-action checks pass;22 destinations resolve. Confirmation screenshot inspected at390×844. Match/mismatch is simulated with counts only, not real secure PIN verification; Present/OS/backend unverified. Add Child remains unmapped. Keep every screen in1650:465 and stop for review.

## 2026-10-22 — OTP punctuation and Change link

Latest OTP subtitle: **We sent a 6-digit code to •••1204.** followed by **Change** in Poppins Bold14 with underline. Preserved10px gap,44px hit height and original correction navigation. Updated main and four review compositions plus incoming display fixtures. All five rows fit on one line306px within338px at390×844; screenshot inspected. [Evidence](Evidence/2026-10-22_OTP_Change_Link.json). No screen removed; two-screen PIN → Biometric flow unchanged.

## 2026-10-22 — Latest live-click reliability repair

User reported PIN Continue failure in Present. [Current click-target handoff](Evidence/2026-10-22_PIN_Stable_Click_Handoff.md). Shared button masters swap variants on hover/down/up; keypad masters swap on press, conflicting with instance-level app clicks. Application handlers now live on29 stable transparent Frame hit areas covering both PIN keypads, Continue/Save and biometric button instances. Sources keep their design/state bindings; duplicate local source clicks cleared. Continue target1718:803 opens Confirm1709:675; Save target1718:811 processes then opens Biometric1670:1069.

39 stored-action checks pass through new targets;29 geometry/ownership checks pass; confirmation screenshot byte-identical. All8 PIN screens preserved. Native Present playback remains unverified; restart prototype to load updated targets. No secure PIN/backend/OS claims; Add Child unmapped. Future fixes must inspect inherited hover/press behavior and actual hit ownership, not just ON_CLICK arrays.

## 2026-10-22 — Calm blinking stars across18 current V2 compositions

[Star enhancement handoff](Evidence/2026-10-22_Star_Enhancement_Handoff.md) · [Verification/node ledger](Evidence/2026-10-22_Star_Enhancement_Verification.json). Reused Calm Star1726:1206 and corrected its nearly invisible artwork opacity.181 added instances across Splash,4intros,Login/Registration,5OTP and5PIN compositions; native staggered6–8s opacity loops mixed with static stars.102 existing decorative stars moved clear of protected branding/card/footer areas; no deletion. Dense lists/legal/country views stay clear; Biometric overlays inherit underlying PIN sky.

All18 foreground/application-interaction fingerprints preserved; all loops/reduced-motion branches and39 PIN/Biometric regression checks pass. Final representative screenshots inspected. Live Present/device performance unverified. Existing reduced-motion controls work at next hold; restart to resume after reduced mode is disabled. No new screens, routes or success dialog. Stop for review.


## 2026-10-22 — PIN navigation handlers simplified after repeated playback report

User still reported Continue/Save failure. Replaced chained frozen-gate handlers with direct native condition branches on stable PIN hit targets and keyboard handlers. Continue1718:803 has one conditional block capturing length and navigating to Confirm1709:675 in the same branch. Save1718:811 has two independent conditionals for mismatch/save; processing1650:844 has separate success-eligible, success-unavailable, offline, API and timeout branches. No success dialog. Existing Biometric1670:1069 remains the destination after successful save. Hit fills now have0.001 alpha rather than zero. All eight PIN screens preserved; no layout/content changes.

Found serialization limitation during repair: a multi-block CONDITIONAL retained only first condition plus an unconditional else; remaining else-if branches were discarded. Replaced these with independent single-block conditionals and re-read/tested saved results.39 stored-action regression checks pass. This does not identify/prove the prior live-playback cause, and native Present playback remains unverified. Do not claim this test substitutes for real click playback. Latest repair script and evidence: Evidence/2026-10-22_PIN_Atomic_Navigation_Repair.js and Verification.json.


## 2026-10-22 — Distributed top stars; Splash excluded

Latest top decoration: Evidence/2026-10-22_Distributed_Top_Stars_Handoff.md and Verification.json.12 authentication compositions now use seven animated top stars each, with four scattered position patterns,6–10px canvases and seven starting rhythm/phase combinations per screen. Original static four-point top decoration hidden, retained as references. Clean approved component instances replace cumulative inherited sizing overrides. Shared masters, both Splash screens/animations, illustrated Intro headers, bottom stars and app navigation unchanged. Biometric sheets inherit enhanced PIN sky. Foreground fingerprints, bounds/brand clearance and representative final screenshots pass. Native Present playback remains unverified. Do not change Splash stars in future propagation of this top-star treatment.

## 2026-10-22 — Latest: shared full-screen star-only system, including Splash

User explicitly confirmed Include Splash. This supersedes previous Splash exclusions and top-only star layouts. Read14_SHARED_FULL_SCREEN_STAR_SYSTEM.md.22 full-screen compositions have24 stratified seeded stars each;16 sheets have6 quiet accents each.17 transparent processing/error/keypad overlays inherit the underlying field. Two test-only review panels unchanged. Approved Calm Star1726:1206 reused; previous decorative atmosphere layers disabled; zero active decorative circles. Functional loaders/OTP dots/radio controls remain unchanged.

All57 foreground/app-reaction comparisons pass; all38 edited compositions pass geometry/phase/shape audits and were visually reviewed via full-screen screenshots/contact sheets. Native Present hit testing, playback and real device performance remain unverified. No production app or local companion code changed. Evidence: Evidence/2026-10-22_Full_Screen_Stars_Verification.json. Preserve every existing screen and route. This shared star-only treatment is now the default for upcoming V2 screens.

## 2026-10-22 — Latest star density:36 per full screen,10 per sheet

User requested more stars with animation on every screen. Added328 approved reusable star instances across22 full screens and16 sheets; counts now36/10. Existing staggered A/B/C rhythms and reduced-motion behavior preserved. Existing UI and app reactions unchanged across all38 affected compositions; all in bounds, no decorative circles, minimum measured spacing28px. Splash/Login/preferences screenshots inspected; native Present playback unverified. Use the updated14_SHARED_FULL_SCREEN_STAR_SYSTEM.md; earlier24/6 counts are superseded.

## 2026-10-22 — Shared Snackbar standard supersedes earlier snackbar guidance

Use the existing NH/Snackbar family `1769:53` on page `1420:2`. Retained Error master `1420:18`; semantic Success `1769:35`, Warning `1769:41`, Info `1769:47`. Properties: `Message#1769:0`, `Action label#1769:1`, `Show action#1769:2`, `Show dismiss#1769:3`, and `Tone`. Existing consuming-screen retry/dismiss reactions and message variable bindings remain authoritative. No route guessing. Error matches screen1654:1428 exactly: square #1C2B33, 12% white1px border, no shadow/leading icon, Poppins12/18, gold action, minimum44px controls, HUG height60 minimum. Mobile390px uses350px snackbar,20px side/24px bottom margins; grow for long text. All six active V2 consumers standardized. Future equivalent transient feedback must reuse this family, not a local duplicate. Other tones reuse semantic tokens and meaningful caller-provided copy. Production mobile now uses NoorSnackbarHost/NoorSnackbarHostState; current20 consumers migrated, bounded/deduplicated and inset-aware. Local companion also uses centralized feedback. See Snackbar_2026-10-22/README.md for evidence, test failures and native/device verification limits. Do not infer release readiness from structural screenshots or unit tests.

## 2026-10-22 — Primary button height is48px

User referenced322:2 (Primary Regular Default,48px). All53 primary button/loading instances in V2 now bind height to existing size/control-regular VariableID:295:85, resolving48px. This supersedes earlier56/64px primary button instructions. Existing widths, typography, colors, variant state bindings and reaction arrays were preserved. Primary wrappers and PIN/biometric hit areas synchronized; Google button styling/height retained, its loading overlays shifted8px to follow footer reflow. Login wrapper clipping corrected and Login/Registration/Confirm PIN/Biometric screenshots inspected. Use48px for upcoming primary actions and their loading states; do not change shared56px field/large-control token. Original reference designs and other pages unchanged. Live Present testing remains blocked by the saved figma.com browser policy; this was a design geometry change, not a claim that the unresolved PIN live-click issue is fixed. Evidence: Evidence/2026-10-22_Primary_Button_48px.json.

## 2026-10-22 — Splash icon static on both screens

User requested removal of the approved crescent/NH icon animation on both remaining Splash screens1131:2/1146:2. Removed OPACITY/TRANSLATION_Y tracks from ancestor lockup1145:57 and ROTATION/SCALE_XY tracks from icon canvas1154:2. Reduced Motion lockup1146:58/icon1154:276 already had no tracks. Both icons and ancestors now static, full opacity, zero rotation, original118px size/artwork/layout preserved. Wordmark/subtitle's own tracks, decorative stars and main Splash four-second navigation remain unchanged.

## 2026-10-22 — PIN/biometric click targets above full-screen decoration

User screenshot shows four entered dots and enabled Continue but no navigation. Moved existing Continue1718:803, Save1718:811 and five biometric hit targets1718:815/819/822/825/828 to their390×844 screen roots, after the full-screen star layers. Absolute bounds and exact action arrays preserved; visual components stay in cards/sheets and all eight PIN frames remain. All seven root ownership/source-geometry checks and39 stored-action checks pass. This addresses potential interception by overlying decoration; native Present root cause and playback remain unverified because browser policy explicitly denies figma.com. Do not describe stored-action checks as live verification. Keep these root hit targets aligned with their source controls during future layout or sizing changes. Evidence: Evidence/2026-10-22_PIN_Root_Hit_Ownership.json.

## 2026-10-22 — Screen014 Add Child designed; awaiting review

New section014 — Add Child1804:2599 under existing V2→Onboarding; main1804:2656, valid review1806:3639. User approved screenshot copy plus PRD required/optional fields and3–17 age rule/additional copy. Read Evidence/014_Add_Child_Handoff.md,014_Verification.json and014_Final_Inventory.json. Uses390×844 only, finalized auth branding, fixed48px primary/loading action,14px gaps, shared inputs/Snackbar,36 stars per full screen and10 quiet margin stars per sheet. Required fields scroll; Save stays fixed. Optional interests/goals/AI voice OFF/accessibility selections are in a bottom sheet. Standalone approved portraits are Tariq/Maryam/Noor1085:21471/21480/21490; thumbnail mockups rejected.

Confirmed PIN/biometric exits now open014. System biometric Cancel/Escape returns to offer; Skip/success/unavailable-hardware continue to014. No018/019 destination guessed and015–017 standalone screens not created.64 stored Add Child checks and39 upstream checks pass; all targets≥44px and primary states48px. Native Present remains blocked by figma.com browser permission; name/DOB/catalog/API/storage/idempotency are controlled prototype fixtures, not real runtime processing. Date picker shows June for the documented five year samples; no claim of arbitrary text/date entry. Production code's3–18 rule remains a conflict; user approved3–17 for this design only. Stop for014 review; do not advance015 until requested.

## 2026-10-22 — Screen 014 refinement override
The latest Add Child refinement supersedes the initial 014 name/date sample sheets and three-avatar grid. See Evidence/014_Refinement_Handoff.md and 014_Refinement_*_Nodes.json. The specified centered logo is removed, headers are start-aligned, stage artwork is corrected, and shared portrait carousel 1872:3298 uses 80 source portraits. The language sheet stages selection until Done. Custom nickname/DOB/year sheets and their inbound destinations are removed. Main 1804:2656 and valid review 1806:3639 remain; primary height stays 48 px. Approved display age ranges: 3–7 / 8–9 / 10–13 / 14–17.
Mobile now has native Android/iOS DOB actuals, direct nickname IME handling, a keyed snapping/scaling carousel and a persisted child-language sheet. All 309 Android host tests and 116 stored Figma checks pass. New portrait/API mapping is not approved: mobile retains eight existing API catalog IDs/artwork, while Figma uses 80 new portraits. iOS compilation, native device playback and live Present checks remain unverified. No future destination was created. Older 014_test.js targets removed sheets; use 014_refinement_test.js for current refinements. Earlier approved screens and unrelated repositories are unchanged by this refinement.

## 2026-10-22 — Card and bottom-sheet ivory gradient
User clarified: update white cards and sheets only; keep teal page backgrounds. Reuse shared Figma Paint Style NH/V2/Surface/Ivory Vertical (S:8e5bfca7e0f151c0a4e7e393ac08ddb943d7d323,). Vertical top #FAF7F0 to bottom #FDF6E3, opaque stops, transform [[0,1,0],[-1,0,1]]. Applies to major auth/profile cards, legal and selection sheets, intro feature cards, learning/language choice cards, country-list cards and empty-avatar cards. Preserve selected-state colors, inputs, buttons, teal backgrounds, layout and reactions. 818 eligible nodes updated in V2; no reference pages or production code changed. Geometry and reaction equality checks passed. Evidence: Evidence/2026-10-22_Ivory_Card_Sheet_Gradient.json and _Rows.json. Use this surface style for future white cards/sheets.

### Lighter ivory surface override — 2026-10-22
The user requested a lighter gradient. Shared NH/V2/Surface/Ivory Vertical now uses top #FDFBF7 and bottom #FEFAF1, replacing the earlier #FAF7F0 / #FDF6E3 stops. All 818 linked V2 card and sheet surfaces inherit the update. Keep the same vertical direction, teal page backgrounds, inputs, buttons, layout and interactions. This is a Figma surface-style update only.
