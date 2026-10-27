# Authentication redesign — validation evidence

Date:2026-10-18. Result: editable Figma redesign and local companion prepared for review. Embedded Code Layer is blocked by account capability; this is not a completed in-file functional search implementation.

## Native Figma checks

- PASS: requested named section and8sub-sections exist in the original file.
- PASS: all15 current V2 Login states redesigned as copies;4 language states branded;4 visually unchanged Intro copies connected as dependencies.
- PASS: exact original Login text multiset retained across all15 states, including hidden component labels. Early audit omitted hidden instance children; rerunning with skipInvisibleInstanceChildren=false produced zero omissions.
- PASS: exact source splash fills copied, with two source colors used for vertical primary gradients.
- PASS: approved logo/monogram assets instanced, original aspect ratios retained.
- PASS: shared primary component set has Default, Pressed, Disabled, Loading and Focused. Press handling and instance navigation are authored; native Present interaction priority has not been playback-tested.
- PASS:183 node destinations inspected; none missing. This verifies destination existence, not every runtime transition.
- PASS: country list contains245 rows with245 source-derived flag assets and selection actions. Selected country name/ISO/code update through variables without resetting phone/email values.
- PASS: country backdrop/control/Escape dismissal authored. Native search and no-results are explicit staged simulations.
- PASS: copied processing frame routes after1.95s to confirmed first Intro; copied splash routes after4s to Language. New Login Back resolves all4 recorded Intro origins.
- PASS: width320,390,430 and reduced-height544 inspection frames plus reduced-motion copy created; small-layout screenshot inspected. Error states use scroll rather than hiding their lower actions.
- PASS: source nodes were not targeted by writes. Spot checks retain original390×844 dimensions and child counts for Splash1131:2, Phone Login1278:155, Email Login1278:780 and Language1166:215.
- BLOCKED: opening live Figma Present in the browser was rejected by a saved origin permission denying access to figma.com. No alternate browser or indirect workaround was attempted. Physical-device safe areas/keyboard, screen-reader operation and native runtime text scaling remain unverified.
- BLOCKED: embedded Code Layer; fresh whoami on retry reports code_layers_enabled:false.
- NOT IMPLEMENTED IN NATIVE DESIGN: arbitrary typed filtering and dynamic selected-flag image replacement. Selected marker is ISO text; list flags are actual artwork. These behaviors are implemented in the local companion.

## Local browser checks actually exercised

| Scenario | Observed result |
|---|---|
| Enter5551234567; search ind |3results: British Indian Ocean Territory, India, Indonesia |
| Select India+91 |Sheet dismisses, flag/code update, entered phone value remains |
| Reopen selected country |India row checked; selected country persists after reload |
| Search+971 |1result: United Arab Emirates+971 |
| Search zzzz |0results and No countries found |
| Clear search |All245rows restored |
| Escape |Sheet dismisses and focus returns to opener |
| Request-failure submission |Compact progress state; methods/fields/submit/Google disabled while busy; failure restores full button and retry |
| Email invalid |Enter a valid email address. displayed; no processing started |
| Valid email / timeout |104px loading button in unchanged full-width56px slot; after10s returns to Try again with timeout copy |
| Offline / switch to Email |Offline message retained; submit/Google disabled; method remains usable |
| Offline Try again with browser online |Restores editable state without clearing country/input values |
| Google processing |Three animated dots; aria-busy=true; all duplicate-submit paths locked |
| Google failure recovery |After2s, inputs recover, primary action remains Send code, Google action becomes Try again |
| Reduced motion |Computed brand animation none and button transition0s |
|320×568 /200%text / country search |No horizontal document overflow. Initial narrow-name wrapping issue fixed by placing code below country name in large-text mode; corrected screenshot inspected |
|430×932 /RTL layout |No horizontal overflow; all4language rows retain~81px height; no row overflow |
|RTL monogram position |Monogram right edge equals language header right edge after explicit LTR brand-row alignment |

The browser checks use deterministic local simulations, not a production authentication service. Phone validation is a prototype-level shape check, not production libphonenumber validation. Review controls expose failure/timeout/offline/expired states without sending personal data to a backend.

## Sources and evidence

- Native machine-readable audit: evidence/figma-audit.json.
- Country/asset validation: evidence/data-validation.json; node prototype/verify.mjs passes for all245unique entries, matching dial codes and nonempty84×63flag files.
- Figma screenshot exports: evidence/login.png, language.png, country-sheet.png.
- Node mapping: figma-state.json.
- Local sources: prototype/index.html, style.css, app.js, countries.json/js, flags/, approved logo.png/monogram.png and Poppins fonts/licenses.
- Country metadata:[libphonenumber-js](https://github.com/catamphetamine/libphonenumber-js), pinned1.12.24; flags:flag-icons7.5.0 and AC/TA country-flag-icons1.5.21.

## Remaining execution

Recheck code_layers_enabled before importing. When true, use send_code_to_figma in this same file/page928:2, then validate the resulting live preview, not just its import receipt. Do not switch destinations or create another file without user authorization. Review the redesigned screens before advancing to a future numbered product screen.

