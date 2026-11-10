# Screen 028 — Maintenance Mode review

30 October 2026. Figma only. Screen027 approved; Screen029 requires approval before work begins.

## Review and nodes

- [Maintenance active](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=2395-15853)
- Existing V2 section2395:15841, on mobile page928:2 under1128:2.
- Supplied-estimate source fixture2395:15906; retrying2395:15959; timeout2395:16018.
- Reduced active2395:16077; reduced retrying2395:16346; reduced timeout2395:16624.
- Review outcome/session controls2395:17157; isolated bootstrap2395:16919.

## Sources and exact copy

Read Screen_Prompts/028_Maintenance_Mode_Screen.md, the finalized V2 reusable prompt/current context, A1 PRD screen28/system-pattern obligations, KMP01 splash/bootstrap blueprint, MaintenanceModeScreen.kt, SplashViewModel.kt, OnboardingGraphInterceptor.kt and common values/strings.xml. Protected/source files were read-only.

The prompt lacked exact copy; existing app strings resolve it: “Under Maintenance”, “We are currently improving NoorHeroes. Please check back shortly.”, “Estimated return: %1$s”, “Check Again”, and “Request timed out”. No new product copy was invented. The calm settings/gear artwork uses the approved Material Rounded icon language and the source maintenance gear meaning, distinct from network failure.

No subscribed/published maintenance-screen composite was found. The approved026 card/wordmark/stars foundation, NH Primary322:2, ButtonLoading329:2, loader family328:2 and Snackbar1420:18 were reused. No new color variables or shared library components were created. Font/color/geometry styles remain current NH tokens and source paints.

## Layout and state handling

All seven frames remain390×844 with366×738 cards at12/82, inner-only scrolling and fixed48px actions. The toolbar contains the approved wordmark only. There is no in-app Back, Skip or Dismiss bypass. The prompt's exit means leaving through the OS; no fabricated app-exit URL or destination was created. OS Back/exit cannot be validated by this design graph.

Default has no estimated return. Raw message/estimate and formatted/visibility variables are local to028. On entry, an empty provided message uses the exact app fallback; supplied messages are preserved verbatim in the controlled simulation. Nonempty estimates are formatted and shown; empty estimates hide. This is not a free-text/API parser or live server connection.

The provided-estimate frame is explicitly a historical app-preview fixture:2026-09-16T22:00:00Z. It is labelled in the frame name and external review instructions, not presented as a current server promise. Its caption is a visible local fixture override for canvas review; ordinary runtime frames retain conditional variable bindings. Entering that fixture supplies the same value to local retry state.

## Prototype behavior

- Check Again guards against a second activation, marks the request in flight and opens the matching loading state. The shared loading button is inert; reduced motion uses the existing Phase=Still variant. The2-second wait is a prototype-only demonstration, not a server SLA.
- The simulated new bootstrap result is evaluated after loading. Active maintenance returns to the gate. Timeout returns to a shared snackbar with exact existing copy and Retry. Required update continues blocking through approved026, following the actual interceptor's forced-before-maintenance order.
- Restored service uses the documented bootstrap matrix: invalid session→Language Selection1166:215; valid session without children→Add Child1804:2656; valid session with children→Profile Picker2188:7275. Existing destinations were inspected; no new Home or pending route was fabricated. Only local review session/children flags choose these destinations. Existing family/profile fields are not reset.
- Timeout snackbar Retry uses the same guarded request. Dismiss and6-second timeout clear feedback only, keeping maintenance blocking. Main gate is retained after transient feedback disappears.
- Review controls demonstrate active maintenance, supplied estimate, all restored destinations, timeout, forced-update priority and reduced motion. An isolated cloned bootstrap preserves all original Splash and earlier screen reactions.

## Verification and limitations

112/112 saved-reaction evaluation and structural checks passed. These cover48 normal/reduced response/session/children/forced combinations, duplicate retry guards, source strings, estimate visibility/formatting, message fallback, fixed geometry, inert loading actions, Still phase, feedback-only dismissal and original Splash isolation. See2026-10-30_028_Maintenance_Checks.json and Ledger.json. The supplied-estimate fixture caption was fixed after the original detail snapshot; its final override/returned bounds are separately recorded in the ledger.

Active, Retrying, Timeout and Supplied_Estimate_Fixture PNGs were captured and visually inspected. No icon/text clipping, footer displacement or snackbar/primary overlap was seen at the standard size. Reduced-state geometry, static-star source reuse and Still loader phase were inspected structurally; no claim of separate reduced playback is made.

No live Present playback, real bootstrap/API call, real auth/session validation, process-resume or OS Back/exit interception was tested. No device, text-scaling or RTL/localized-copy test was performed. One standard mobile size only, as requested. No app/backend/admin/web code, protected documentation or original reference screen was edited. Screens029–033 remain unbuilt.

## Required review gate

Screen028 §11 says: “Stop and wait for my review and approval before moving to another screen.” Await approval before029 No Connectivity.
