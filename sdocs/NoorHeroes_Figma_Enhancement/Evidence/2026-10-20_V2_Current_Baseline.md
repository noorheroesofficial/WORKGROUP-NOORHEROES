# Current V2 design baseline — 20 October 2026

Read this, CURRENT_CONTEXT_AND_NEXT_SCREEN.md and12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md before the next screen. Reinspect the live Figma nodes; manual changes may occur.

## Location and scope
Existing file MR9935oQZACMjndzGIUgq5, Mobile page928:2, NoorHeroes V2 Design1128:2 → Onboarding1270:140. Authentication Prototype section1355:2564. No other module created. For each future module, determine its name from PRD/blueprints and create a section only when work begins. Preserve originals/web/admin. New screens390×844 only; existing splash QA widths remain.

## Design and assets
- Finalized equivalent-role typography, alignment, spacing and colors are authoritative visual references. PRD/blueprints remain functional authority.
- Poppins for UI; primary button14/20SemiBold,18pxcorners. Primary shared NH/Button322:99, Large342×56 where matching Login. Intro existing350×56 and Language350×64 retained.
- Reuse existing icon meanings/assets. Intro bottom supporting icon canvases14×14,2pxicon-to-text gap; other equivalent icon roles18×18,4pxgap. Center artwork optically; Auto Layout shared groups and consistent perceived weights.
- Intro square top corners; transparent Back/Skip and tight content-hugging supporting pills; source exact live alpha, spacing and text styles.
- Login1355:2696uses centered approved monogram1355:2702and exact wordmark1355:2700. White form card and original Google button; approved content retained.
- All five splash variants now use copies of that Login monogram and wordmark. Preserve118×118icon canvases,26pxspacer,title slot225×52(203×52in320variant),subtitle/224pxlockup and original placement. Source images/brand tint preserved. See splash evidence.

## Current flows and button rules
- Splash1131:2 → Language after4seconds.
- Four Language states1166:215/250/285/320 → Processing1259:140 → Welcome1215:34 after1.95seconds. No Continue-text flash after progress.
- Intro1215:34 →1215:138 →1215:246 →1215:356; confirmed Skip/final exits to Login1355:2696.
- Send code uses exact Primary/Large loader329:6with white dots; instances1428:175/181/190/196. Most recent change: click control1428:237sets resetInteractiveComponents=true for processing1428:171.
- Google uses exact Secondary loader329:33with white original-button-matched surface and dark dots; instances1428:205/211/7655/7656. On click/Retry, opens1428:172with resetInteractiveComponents=true. Timeout1428:7654also resets. Reduced motion uses327:25.
- Google Send code behavior: stays visible disabled while Google processes. Do not change Google behavior when editing Send code.
- Old inline Google host1444:174is permanently hidden; do not reactivate. Previous inline strategies are superseded.
- Shared NH/Snackbar1420:18handles simulated network/API failure and10second timeout, with Retry/dismiss. Square corners,#1C2B33,12%white border,goldaction,Poppins12/18,44pxtargets.
- Runtime controller area1428:170under Authentication. Original sections1355:2567and1383:3275were explicitly deleted in full. Never use them or their removed local masters as active dependencies.

## Limits and unresolved destinations
OTP/Registration destinations remain pending; never invent screens or connections. Deleted country-commit controller and local flag master still require separate repair. No real API/auth is implemented; native inputs/search use fixtures. Structural audits and resting screenshots passed for scoped work, but they do not prove live motion. Present playback cannot currently be inspected because saved browser policy denies figma.com. Do not claim full journey complete or user approval of animation playback.

## Next-screen workflow
Read the requested screen prompt and relevant protected PRD/blueprint. Use finalized V2 as visual baseline, preserving approved copy. Make one screen, add only its necessary states/dependencies, connect confirmed existing destinations, verify consistency and present it for review. No next screen is selected by this save-context request.

