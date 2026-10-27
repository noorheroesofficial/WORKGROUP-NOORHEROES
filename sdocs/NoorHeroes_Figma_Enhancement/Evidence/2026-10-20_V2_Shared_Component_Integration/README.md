# V2 shared component integration — 20 October 2026

Updated existing NoorHeroes file MR9935oQZACMjndzGIUgq5, inside V2 Onboarding.

## Components and scope
- Public NH/Button 322:99, Primary/Large Default322:24 and Disabled322:36.
- Public NH/ButtonLoading 329:49, Primary/Large329:6.
- Public NH/Snackbar1420:18. User's old reference1383:3275 was verified deleted; it was not recreated.
- Login1355:2696 now uses shared enabled/disabled controls1428:237/242.
- Four Language Continue instances1194:69/82/95/108 retain350×64 geometry and loading route.
- Four Intro primary wrappers1219:70/132/189/246 retain labels,350×56 geometry and existing destinations. Shared visuals use original arrow1253:43, with white foreground override for contrast.
- Language processing1259:140 now displays shared loader1428:7739 and static reduced-motion alternate1428:7745. No Continue label flashes before Intro.
- No source design, PRD, Blueprint, Screens, app code, or library master was edited.

## Login prototype behavior
New runtime area1428:170 is under existing Final Authentication section1355:2564.
Normal processing1428:171, Google processing1428:172, normal timeout hold1428:173, Google timeout hold1428:7654, Snackbar overlay1428:174.
OTP and Google submission hide the idle submit visuals, block duplicates, and show loader-only feedback. Cancellation via Escape or the existing Back position restores state.
At2seconds: complete restores Login and closes the overlay, failure/offline shows the shared Snackbar, timeout continues processing for8seconds then shows timeout Snackbar. Total timeout10seconds.
Snackbar Retry restarts the original OTP/Google action using a simulated recovered result. Dismiss, Escape, outside click and6second expiration close feedback. Invalid OTP inputs cannot retry past validation. Phone/email, selected language/method and country variables are not reset by these processing/error actions.
Keyboard scenarios: S complete; N API failure; O offline; T timeout. Choose a scenario before submitting. Existing input fixtures remain simulations.
Reduced motion uses Still dot variant327:15, with existing motion preferences1389:3044/3045.

## Verification and limits
75 saved graph checks passed for Login plus25 onboarding checks:100total. Login, Snackbar and Intro button renders inspected. Audit evaluates saved Figma reactions, expressions, variables and destinations; it is not live Present playback or backend testing.
No real API/network/auth requests occur. Success navigation to OTP remains pending as approved; no destination is invented.
Country-commit controller and local flag master deleted in the previous confirmed removal were not recreated by this task. Country selector commit behavior still needs separate repair; do not cite this work as complete end-to-end authentication verification.

