# NoorHeroes V2 — Profile Picker and Child Lock baseline
Saved 27 October 2026 at the user's explicit request. This records the latest applied design and decisions from 25–27 October. It does not authorize new design work.

## Scope and precedence
- Figma only. Do not edit mobile, backend, admin, website or companion code without new explicit authorization.
- Existing file MR9935oQZACMjndzGIUgq5; mobile page 928:2; V2 section 1128:2. Standard mobile size 390 × 844.
- Preserve original/reference/web/admin designs. Requirements directories remain read-only.
- This baseline supersedes conflicting 25–26 October notes about the picker footer, full-page scrolling, card dimensions, Add Child layout, selected styling, recovery height and unmapped recovery controls.
- The 23 October baseline still governs unrelated V2 areas and NH component/palette conventions. Inspect live Figma before another edit: IDs and saved snapshots are not proof of current state.

## Key Figma nodes
| Role | Node |
|---|---|
| Profile Picker section | 2188:7267 |
| Default picker | 2188:7275 |
| Empty / Offline / Loading / Error | 2188:7543 / 2188:7787 / 2188:8027 / 2188:8267 |
| Configured picker | 2189:7165 |
| Child card family | 2232:10365 |
| Four-state component preview | 2254:12023 |
| Reference grid / selected card / Add Child | 1095:296 / 1095:298 / 1095:356 |
| Child Lock section | 2194:7250 |
| Child PIN / Pattern / Biometric | 2194:7284 / 2194:7545 / 2194:7727 |
| Child cooldown A / B | 2194:7880 / 2194:8023 |
| Child biometric system simulation | 2194:8153 |
| Parent recovery section | 2207:8061 |
| Parent verification / Verifying | 2207:8134 / 2207:8314 |
| New child PIN / Confirm / Saving | 2207:8374 / 2207:8550 / 2207:8718 |
| Parent cooldown A / B | 2207:8778 / 2207:8837 |
| Parent biometric simulation | 2207:8886 |
| Verified new PIN / Confirm / No Lock review | 2209:16137 / 2209:16352 / 2209:16556 |
| Parent error / cooldown / mismatch / network reviews | 2215:9019 / 2215:9234 / 2215:9364 / 2215:9571 |

## Final Profile Picker layout
- Main cream surface: 366 × 738 at x12/y82; bottom y820. All 13 picker states use the same main-card height.
- Toolbar/background remain fixed. **Only inner profile choices scroll. No full-page scrolling.** Card title stays outside the inner scroll viewport.
- Outer page wrapper 2268:12135 has overflow NONE. Main inner viewport 2188:7403 has vertical overflow, clipping and 4 px inner padding to protect selected outlines.
- Profile grid is 350 px wide, 14 px horizontal/vertical gaps, two columns, 168 px tile width.
- All child, Parent and Add Child tiles are 209.5 px high, including Empty-state tiles. The user explicitly requested matching heights after the original reference-height restoration.
- Parent and Add Child are grid tiles; never restore the obsolete compact full-width Add Child row.
- Manage Profile(s) and Back to Setup remain removed. Do not reintroduce them.
- Three demo profiles: saved setup child plus fictional Zayd and Maryam. Saved name/DOB/avatar/language/learning data remain bound. Do not invent earned progress from learning difficulty.
- Child 1 progress: Level — • — Stars when unavailable. Sample Zayd: Level 2 • 35 Stars; Maryam: Level 1 • 12 Stars. Preserve sample labels.
- Long names use a one-line ending ellipsis while selected-child verification retains the full name; missing images use the existing Material person fallback.

## Shared card styling and clipping safeguards
- Family 2232:10365: Locked/Unlocked/Loading/Error × Rest/Selected, eight variants. Reuse in place.
- Neutral card: 1 px inside border from 2232:9613, radius16. Preserve exact reference paint and opacity; do not guess a new border.
- Selected card: solid 2 px teal border, one 2 px gold outer outline, rounded Active pill, one gold avatar ring. Selection and lock status remain distinct.
- Active pill: height21/radius10.5. Avatar64. Existing functional 44 px lock hit target is preserved; do not replace its action with a decorative check.
- Body/header/grid clipping is disabled where it would cut the gold ring or outline. Keep clipping on the actual inner scroll viewport and preserve its 4 px outline gutter.
- Avoid duplicate gold spread shadows plus strokes. The previous avatar-top cut and overlapping border were caused by clipping and double outlines.
- Level/star pill is content sized and centered; name/detail/pill bounds do not overlap. Selected avatar-to-name clearance6 px; resting8 px.
- Preserve control names Control/Lock action and Control/Profile selection so instance action overrides survive variant swaps.
- Component preview 2254:12023 is 746 × 277.5; four 168 × 209.5 instances, row gap14, safe4 px insets, no clipping. Selected preview portrait ring restored after stale override was found.

## Empty, error and loading states
- Empty message card 2188:7676: child_care Material icon above approved title and message; NH primary color. Existing copy unchanged.
- Error frame 2188:8267: error_outline Material icon in existing NH error color above approved generic load-error text. Error card plus separate Retry button form a centered group in the inner viewport.
- Error and Empty message cards use the neutral profile-card border: same exact paint, 1 px inside, radius16.
- Retry action 2188:8418 still navigates to 2188:7275.
- Reuse NH state-card artwork properties (Show artwork / Artwork) rather than detaching or modifying unrelated global state-card masters.
- Local icons: Error2319:12426; Empty2319:12428.
- Loading uses a two-column grid of five reusable skeletons matching the three child, Parent and Add Child silhouettes. All skeleton tiles168 × 209.5.
- Skeleton components: Child2311:12391, Parent2313:12426, Add2313:12465. Reuse existing NH Skeleton Line/Circle primitives588:3/588:4 and palette.
- Add Child skeleton border matches the actual dashed Add Child tile. Keep the semantic distinction from neutral profile borders.
- Shimmer sweep uses manual translation tracks, 30 keyframes over24 seconds. Timeline metadata was configured/read back; continuous live playback was not verified. Do not claim an infinite loop or reduced-motion support from these tracks.

## Selection, locking and pending destinations
- Each child independently stores simulated lock type/configuration, Unlocked, Selected, attempts, cooldown, remaining timer and saved opaque PIN markers.
- Locked card/body opens that child's configured PIN/pattern/biometric gate. Success unlocks only that child; failed input, Cancel and failed saves do not unlock anyone.
- Unlocked body selects the child only. Open-lock control re-locks a configured child. A child without a configured lock requires verified-parent recovery before configuration.
- Loading guards prevent selection/lock actions.
- Per-child attempts/cooldown persist when switching children; recovery saves only the selected child's markers/configuration.
- Back and accepted return preserve the invoking picker, including Offline. Child accepted action is Back to profiles, not a guessed Home route.
- **User explicitly kept Child Home navigation pending.** No substitute home frame, child-mode activation or entitlement claim.
- **User explicitly kept Add Child navigation pending.** Existing form overwrites the demo profile and does not append another child. Do not wire it as a multi-child flow.
- Parent management destination also remains pending. Do not invent routes into the recovery gate as a substitute dashboard.

## Slots and scenarios
- PRD capacities: Free1, Mobile Family4, Premium Family8. Do not copy the original reference's fictional 5-slot plan.
- Slot maximum/used/available, availability, status and sample-plan text are derived by scenario initialization and the main picker callback.
- Full Free scenario shows No slots available; available/disabled icon/title colors use existing semantic variables.
- Scenario starts: All unlocked2245:11287; All locked2245:11582; Mixed2245:11877; Only one unlocked2245:12172; Long name/missing image2245:12467; Single2245:12762; No selection2269:12112.
- Scenario starts initialize the same runtime picker; they are fixtures, not independent production flows.
- Picker simulation collection VariableCollectionId:2232:9474. Re-query names/IDs rather than relying on old partial maps.

## Child Lock and verified-parent recovery
- Child PIN is four digits; pattern is discrete tap simulation, not drawn gesture capture; biometrics is a labelled system-prompt simulation, not OS authentication.
- Child and parent lockout policy explicitly approved: fourth failure30 seconds, fifth300 seconds, sixth onward (attempts − 5) ×600 seconds. Do not restore older app constants with a2-minute fifth tier.
- Countdown simulation advances on timer frames; it is not a server or wall-clock security timer.
- Ask a grown-up for help is enabled and routes to existing Screen024. Older 023 notes saying recovery is unavailable are superseded.
- Recovery: verify parent → choose4-digit child PIN or No Lock → confirm PIN → explicit Save New Lock → picker.
- Parent PIN accepts4–6 digits, max6, masked. New child PIN requires exactly4 and matching confirmation.
- Only explicit successful Save commits; cancellation and network errors preserve prior lock state. Successful recovery clears only target child attempts/cooldown. No Lock requires parent verification.
- Review credentials are labelled demo fixtures in historical evidence; never request real credentials. Stored opaque markers are not secure credential storage.

## Final recovery card layout, 27 October
- All14 full-screen recovery state/review cards in2207:8061 are366 ×738 at x12/y82. This supersedes the old content-hugging122–690 px surfaces.
- Separate internal vertical scroll viewport fills space above fixed footer actions; footer ends16 px above the card bottom.
- Primary actions remain48 px; quiet/cancel actions44 px. Existing details, keypad geometry, typography and labels retained.
- Longer error/form content scrolls internally. Verifying/Saving/cooldown messages are centered. Footer remains accessible.
- Inherited viewport maxHeight594 was removed; footerless states use706 px viewport, single44px-footer states650, two-action100px-footer states594.
- Runtime reset fields intentionally remain hidden before parent verification; verified review fixtures show the real layout. Do not remove visibility gating to make the canvas look populated.
- Parent biometric system sheet2207:8888 remains352 px high; do not stretch OS simulation sheets to the main-card height.
- Last equal-height pass preserved all64 existing reaction-bearing nodes unchanged.

## Evidence and verification limits
Relevant files in this Evidence folder:
- 2026-10-26_Profile_Picker_Ledger.json: independent-child simulation IDs and original42 reaction checks; historic card measurements superseded.
- 2026-10-27_Picker_Border_Clipping_Checks.json:68 checks passed before later inner-scroll/equal-height refinements. Do not imply these exact old geometry assertions were rerun unchanged afterward.
- 2026-10-27_Picker_Inner_Scroll_Checks.json.
- 2026-10-27_Picker_Shimmer_Height_Checks.json.
- 2026-10-27_Picker_Error_Empty_Icons_Checks.json.
- 2026-10-27_Picker_Final_Border_Edge_Audit.json:13 picker states/eight variants, no reported overlap/edge issues.
- 2026-10-27_Recovery_Equal_Height_Checks.json:14 recovery layouts, unchanged64 reaction nodes.
- Latest screenshots: Picker_Error_Border, Picker_Empty_Border, Picker_Long_Name_Edges, Picker_Component_Preview_Fixed, Picker_Shimmer, Recovery_Height_0/1 and Recovery_Status_0/1 (2026-10-27 prefix, .png).
- 2026-10-25_023_Child_Lock_Review.md and 2026-10-25_024_Lock_Recovery_Review.md explain source behavior; conflicting pending gates/card geometry are historical.

Canvas screenshots, bounds and reaction-graph evaluation are not live Present playback. Saved browser restrictions previously blocked figma.com. Device accessibility, keyboard/safe-area behavior, OS authentication, actual API integration, server lockouts and production security are not verified. No real app code changed during these Figma refinements.

## Future work
Read this baseline, relevant screen prompt/PRD/blueprint, and live Figma before any newly authorized change. Preserve approved designs. No next screen or navigation destination is authorized by this context save.

