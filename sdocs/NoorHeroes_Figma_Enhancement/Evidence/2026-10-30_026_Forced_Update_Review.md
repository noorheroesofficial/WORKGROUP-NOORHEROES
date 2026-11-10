# Screen 026 — Forced Update review

Date: 30 October 2026. Figma only. Screen 025 was approved before this work. Screen 027 is not authorized until review approval.

## Review links and scope

- [Blocking gate](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=2382-15437)
- Error: 2382:15589; reduced motion: 2382:15747; reduced-motion error: 2382:16043.
- Store-handoff simulation: 2382:16345, Return control: 2382:16364.
- External review controls: 2382:16382. Section: 2382:15428 inside existing V2 1128:2 on mobile page 928:2.

Built four 390×844 variants with the approved NH background, palette, wordmark, Poppins styles, shared 48px primary button and shared NH/Snackbar instance. Cards remain 366×738 at x12/y82 with inner scrolling and a fixed footer. The toolbar has branding only. No product Back, Skip or Dismiss route is supplied. Reduced-motion stars reuse static editable vector artwork.

## Copy and source evidence

Sources: Screen_Prompts/026_Forced_Update_Blocking_Screen.md; PRD_Documents/Child App (1-12)/Feature_A1_Splash_Auth_Onboarding.md FR2/screen inventory; Development_Blueprints/A1_Splash_Auth_Onboarding/KMP/01-splash-bootstrap-update-gating-flow.md; existing ForcedUpdateScreen.kt, SplashViewModel.kt, AppRoot.kt and common strings.xml, all read-only.

Exact existing app strings: “Update Required”, “To keep learning and exploring NoorHeroes safely, please update to the latest version.”, “Update Now”, and “Minimum version required: %1$s”. The version label is bound and hidden when the minimum is blank. 2.0.0 is sourced from an app preview and explicitly a sample, not a verified current minimum version.

User approved “Couldn’t open the app store. Please try again.” and a clearly labelled simulated store handoff. Existing store links could not be verified through the available web tool; no real store URL is wired. This does not establish that the configured links are invalid.

## Prototype behavior

- Existing normal Splash 1131:2 retains its 4-second trigger and exact original normal route to 1166:215. A local required-update flag, default false, branches to 026 when enabled by the external review controls. This is the only necessary pre-existing screen reaction change; Splash visuals are unchanged. Original reaction JSON is recorded in the ledger.
- Update Now opens the store simulation when the local outcome is available. Android/iOS review controls supply Google Play/App Store text. Return closes the overlay, retaining the gate underneath. No install success or gate bypass is simulated.
- Unavailable outcome opens the corresponding error gate with the approved shared snackbar. Retry repeats the same outcome logic. Dismiss and the 6-second timer hide feedback only; neither clears the required gate nor opens app content. Update Now stays reachable.
- Reduced-motion navigation uses <=100ms dissolves. Normal proposed transitions are 250ms. All newly written state belongs to the local 026 collection; existing authentication/profile data is not changed.

## Verification and limitations

42/42 saved-reaction evaluation and structural checks passed; see 2026-10-30_026_Forced_Update_Checks.json. Native stored reactions and node/variable ledger are in 2026-10-30_026_Forced_Update_Ledger.json. Default, error, store simulation and reduced-motion screenshots were captured and visually inspected for copy, wrapping, icon, fixed action clearance and snackbar overlap.

These checks do not prove live Present playback, real store handoff, real installation/version revalidation, OS Back interception or production bootstrap enforcement. No device, text-scaling, RTL/localized-copy or backend test was performed. Scope is one standard mobile size per the user. No application code, protected source documentation, original reference design or unrelated V2 product screens were edited. Screens 027–033 remain unbuilt.

## Review gate

Screen 026 §11 explicitly says: “Stop and wait for my review and approval before moving to another screen.” Await approval before Screen 027 Recommended Update Banner.
