# Screen 029 — No Connectivity, pre-auth: review

30 October 2026. Figma only. Screen028 approved. Screen030 requires approval before work begins.

## Review and nodes

- [Offline screen](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=2401-13531)
- V2 section2401:13523, existing page928:2 / V2 1128:2.
- Checking connection2401:13585; online bootstrap pending2401:13644; online timeout2401:13703.
- Reduced offline2401:13762; reduced check2401:14031; reduced bootstrap2401:14309; reduced timeout2401:14587.
- Isolated offline-launch review2401:14882; review controls2401:15120, including disconnect-during-bootstrap2403:13977.

## Authoritative sources and exact content

Read Screen_Prompts/029_No_Connectivity_Screen_pre_auth.md, current/finalized V2 standards, A1 PRD§1.14 and§6.7, the KMP01 splash/bootstrap blueprint, NoConnectivityScreen.kt, SplashViewModel.kt and common values/strings.xml. These source/protected files were read-only.

The missing prompt copy is resolved by existing app strings: “No Internet Connection”, “Please check your network settings and try again.”, “Retry Connection”, “Request timed out”. The offline icon uses the approved Material Rounded wifi_off meaning. Online request-timeout states use “Request timed out” as their heading rather than asserting a service outage or continuing to diagnose the device as offline. No new product wording was invented.

Published no-connectivity composite discovery returned no match; the approved028 layout foundation and current NH Primary322:2, ButtonLoading329:2, loader328:2 and Snackbar1420:18 were reused. New colors/library primitives were not created. The maintenance description binding and estimate are removed from local029 clones; original028 is unchanged.

## Composition and interactions

Eight390×844 review frames retain the approved366×738 card at12/82, inner-only scrolling, fixed48px footer, approved wordmark, palette/typography and decorative stars. The toolbar has no product Back/dismiss action. No service-outage estimate or maintenance wording appears in the offline UI. Reduced pending states use existing Phase=Still and static vector stars.

- Offline launch checks the simulated connectivity observation immediately, rather than waiting for a request timeout. It is a cloned review bootstrap, leaving original Splash unchanged.
- Retry Connection guards duplicate activation and enters an inert shared loading control. A150ms prototype-only check routes immediately back to Offline if still disconnected; otherwise it enters simulated bootstrap pending. It never requires waiting for the2-second response simulation when offline is already known.
- At response time connectivity is checked again. A disconnect while pending returns Offline. A connected timeout shows exact existing “Request timed out” feedback, with Retry and feedback-only dismissal/6-second hiding.
- Connected ready results use fresh review session/children flags: no valid session→Language Selection1166:215; parent/no children→Add Child1804:2656; parent/children→Picker2188:7275. These are existing verified destinations; no guessed Home route is added.
- Connected maintenance response opens approved028 and clears stale estimate/custom-message fixtures. Connected forced response opens approved026 and marks its local required-update simulation flag. These are simulated response conditions, not actual service claims.
- Review-only controls cover offline launch, remaining offline, all ready routes, timeout, maintenance, forced update, reduced motion and disconnecting before a pending response completes. No029 action submits authentication or profile data.

## Known requirement gap for review

PRD§1.14 requires bundled intro slides to remain viewable offline. The existing NoConnectivityScreen and its documented source control have only Retry Connection, with no approved offline-intro entry or copy. The source interceptor also prevents ordinary pre-auth navigation while this gate is displayed. No new CTA, unofficial return route or changes to approved Intro/Login/Registration screens were invented. **The offline-intro entry remains unresolved and is not claimed complete.** The existing auth screens' offline enforcement was not changed or verified by this work.

The app's authenticated valid-session/cached-profile offline bypass is a separate branch outside this pre-auth screen. It was inspected in source but not redesigned or newly simulated here. The online ready-result matrix is a bootstrap demonstration, not evidence of authentication security or cached storage correctness.

## Verification and limitations

122/122 saved-reaction evaluation/structural checks passed. They include64 response combinations across normal/reduced variants, immediate connectivity guards, loss during pending bootstrap, duplicate-retry prevention, semantic timeout copy, exact source strings, approved geometry, Still loading phase, shared snackbar clearance, feedback-only dismissal and unchanged original Splash graph. See2026-10-30_029_No_Connectivity_Checks.json and Ledger.json. The unresolved intro entry is explicitly outside the passing checks.

Offline, Bootstrap_Pending and Timeout PNGs were captured and visually inspected. No title/icon clipping, body overflow, footer displacement or snackbar overlap was observed at390×844. Reduced geometry/Still phase were inspected structurally. No live Present, real observer/API/bootstrap, OS Back/exit, device keyboard, text scaling or RTL/accessibility behavior was tested. One standard mobile size only as requested. Pending preview retains the previous offline context while its loader communicates an in-flight recheck; it makes no server outage claim.

Only Figma029 and evidence/handoff files changed. Original reference designs, source code, protected requirements and prior screen designs remain unchanged. Session flags are prototype variables, not real credentials or persisted account data. Screens030–033 remain unbuilt.

## Required review gate

Screen029 §11 says: “Stop and wait for my review and approval before moving to another screen.” Await approval before030 Forgot Access. Review must acknowledge the offline-intro entry gap or request a follow-up for it.
