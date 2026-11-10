# Screen 027 — Recommended Update Banner review

30 October 2026. Figma only. Screen026 approved; Screen028 awaits approval.

## Review and node map

- [Displayed banner](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=2391-14727)
- Review/session controls2391:16404; section2391:14720 inside existing V2 1128:2, mobile page928:2.
- Error2391:14951, reduced2391:15181, reduced error2391:15658.
- Simulated external store2391:16141; Return2391:16147.
- Isolated bootstrap review2391:16166. Original product Splash1131:2 and its approved026 branch remain unchanged.

## Sources and exact copy

Read Screen_Prompts/027_Recommended_Update_Banner_Dismissible.md; the finalized V2 reusable prompt/current context; A1 PRD FR2 and screen inventory27; KMP blueprint01-splash-bootstrap-update-gating-flow.md; RecommendedUpdateBanner.kt, SplashState.kt, SplashViewModel.kt and AppRoot.kt; core-common values/strings.xml. All source/code files were read-only.

The prompt had no exact copy. The existing app resolves that gap: “New Version Available”, “Update NoorHeroes for new features and improvements.”, “Update”, “Dismiss”. The app's star indicator and top-aligned compact banner role are reused. Store failure text reuses the user-approved026 “Couldn’t open the app store. Please try again.”. Store URLs remain unverified; only a clearly labelled simulation opens. No real listing is wired.

Design-system discovery returned no published recommended-update composite; existing local NH Button Primary322:2, Quiet322:69, Snackbar1420:18, text styles and NH color variables are reused. No new library components or color tokens were created. No Code Connect mapping was found for the required existing core UI in the prior flow audit.

## Composition

Four390×844 local review hosts reuse the existing Language Selection1166:215, the verified unauthenticated bootstrap destination. The366×154 banner at12/60 covers only that host's header region, ends before language choices at232, and keeps the choice/Continue controls active. It is an inline layer in these previews, avoiding a modal full-screen hit interceptor. Dismiss returns to the unchanged original Language Selection with its header restored. The copied host's four existing language/Continue reactions match the source exactly. This is a scoped demonstration of the transient banner, not a redesign of Language Selection.

Primary and quiet actions are112×48. Rounded16px banner, source star indicator, current cream surface, neutral border, Poppins title/body, and palette bindings are preserved. Error feedback at20/668 clears the language list and Continue footer; its action/dismiss targets reuse NH/Snackbar. Reduced-motion preview uses approved static editable vector stars and <=100ms action transitions. Normal open/close transitions are proposed200/160ms dissolves.

## Prototype behavior

- New session(Android/iOS) resets local dismissal, enables recommendation and opens the isolated bootstrap. It supplies Google Play/App Store text to the simulation.
- Bootstrap guards are mutually exclusive: forced update goes to approved026; otherwise recommended and not dismissed displays027; otherwise the existing normal destination1166:215 continues. This review uses the verified unauthenticated bootstrap branch, not a fabricated authenticated-session decision matrix.
- Dismiss records the session flag, hides feedback and continues1166:215. Re-enter current session suppresses the banner after dismissal. New session allows it again. No persistent DataStore/API state is claimed.
- Update opens the labelled store simulation and does not mark the recommendation dismissed. Return closes the store overlay back to the banner host.
- Unavailable store opens the matching error state. Retry repeats the simulated store outcome. Snackbar Dismiss and6-second timeout clear only feedback; they do not dismiss the recommendation.
- Existing original source screens, routes and app code are unchanged. There is one027 section. New session controls affect the local027 collection and reuse026's local required-update simulation flag solely to demonstrate priority.

## Verification and limits

59/59 saved-reaction evaluation/structural checks passed, including all eight bootstrap flag combinations, same-session suppression, new-session reset, both platform names, store return, all four Update/Dismiss variants, Retry/timer behavior, card containment, matching original host reactions and unchanged original Splash reactions. See2026-10-30_027_Recommended_Update_Checks.json and Ledger.json. Displayed, Error and Reduced_Motion PNGs were visually inspected; no banner/control or snackbar/Continue overlap was observed at390×844.

This is not live Present or device evidence. Real store opening, installation/version revalidation, actual app process/session lifecycle, global overlay persistence across every downstream route, OS back/accessibility APIs, localized RTL and text scaling remain unverified. Localized copy was not invented. No other screen sizes were generated, per the user's one-standard-size instruction. Original Language Selection and026 store layouts were reused without source changes. No production functionality claim is made.

## Required approval gate

Screen027 §11: “Stop and wait for my review and approval before moving to another screen.” Await user approval before028 Maintenance Mode. Screens028–033 remain unbuilt.
