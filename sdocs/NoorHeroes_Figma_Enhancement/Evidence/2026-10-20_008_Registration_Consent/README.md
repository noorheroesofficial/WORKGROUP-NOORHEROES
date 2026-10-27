# Screen 008 — Registration + Consent

[Review Registration](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1459-256)

## Scope and approval
Built only Screen008and necessary local prototype dependencies inside existing V2→Onboarding→008 — Registration & Consent1459:216. Main390×844frame1459:256. User explicitly approved preserving the age18+row and adding child-data-processing plus three optional consents: four required and three optional total. No other module/new Figma file/new device-size variants were created.

## Sources
- Screen_Prompts/008_Registration_Consent.md; companion009/010/031/032dependency prompts. All237screen-prompt files enumerated/read by the source-index pass; only008implemented.
- PRD_Documents/Child App (1-12)/Feature_A1_Splash_Auth_Onboarding.md,FR-5/6/9/19/20/21,§1.18row8,§2.4Registration.
- Development_Blueprints/A1_Splash_Auth_Onboarding/KMP/03-registration-consent-otp-verification-flow.md;04Google;07draft persistence referenced.
- Existing Figma1095:24and1085:18950were inspected. Their password/statistics/security claims were excluded because they conflict with the current PRD/approved screen content.
- Protected Screens/Mobile App/Onboarding/Register-01.png inspected. No protected source files changed.
- Finalized Login1355:2696provided exact background/stars, branding, Back, curved card, fonts, selector, identifier, Google mark and action system.

## Visual implementation
Login branding remains at original dimensions. Registration uses same366pxcard,342pxcontent/action widths and18/48alternating card corners. Content has its own292pxvertical viewport; full default form544pxand expandable optional rows scroll. Primary and Google actions are fixed at screeny556/y682to avoid loader jumps while scrolling. Card bottom770; Login link remains786. Poppins24/32heading,14/20description,14/24checkbox labels,12/18read/status roles. Form gaps12px,headergap4px; source assets retain aspect ratio. Required/optional groups use Auto Layout; rows60pxwith existing NH/Checkbox398:469instances, centered controls/text. Adult confirmation has no unrequested Read link. Legal links for six actual consent documents remain unmapped.

## Exact content and resolved differences
Preserved preview heading “Create your account”, description “Join as a parent to set up your family”, Phone/Email,Create Account,Continue with Google,required Privacy/Terms/age wording,Optional preferences and Already have an account? Log in.
PRD-driven additions, explicitly approved by user: Child-data-processing consent;Personalization/AI consent;Voice-feature consent;Marketing consent. Labels are sourced from FR-5; no legal body, translations or religious text invented.
Actions are grouped in the fixed footer in the finalized Login order, while consent inputs scroll above. This is a layout adaptation to preserve readable text in390×844.
PRD FR-10post-verification consent differs from its own Registration inventory/journey; Screen008follows the explicit registration-plus-consent inventory/blueprint and user's approval, with no invented downstream route.

## Interaction model
- Default: required and optional all unchecked; primary/Google unavailable.
- Consent booleans independent. Valid identity+all4required+online+legalAvailable+notprocessing→Create Account. Google requires all4required+online+legalAvailable; it does not require manually entered phone/email.
- Phone/Email mode changes retain both drafts. Tap identifier uses approved existing Login demo fixtures2015550123/test@example.com; this is not native text entry.
-245country choices copied from actual Login country data, with own independent code selection and invalidated phone-ready status. No dead country-commit controller dependency. Country field shows code only, as approved captured Registration source. Native search entry remains unsupported/unmapped; use the existing list, not a claim of arbitrary search.
- Optional preferences toggles its three rows, allOFFinitially. No optional consent affects required readiness.
- Primary329:6and Google329:33loading variants; static reduced-motion alternatives. Processing overlays block duplicate submission.2second result simulation; timeout2+8seconds=10seconds. “Creating account...” shown in status role.
- Shared Snackbar1420:18for generic API failure/timeout;Retry preserves identity and consents and restarts correct operation. No account-enumerating responses.
- Back/Log in→confirmed Login1355:2696. Existing Login Create-an-account control1355:2744now connects to Registration. Existing Login Google/Send code behaviors unchanged.
- No OTP destination, no fake legal documents. Successful simulation restores this screen without inventing a next screen.
- Keyboard scenarios: I invalid;Ooffline;Rrestore online/legal availability;Llegal unavailable;Scomplete;NAPI failure;Ttimeout. Draft and consent values persist between screen navigation in the prototype session.
- legalAvailable=trueis an explicit demo fixture for gating, not evidence that versioned legal text is approved, loaded or legally sufficient. Ltests mandatory legal-unavailable blocking; Rsimulates cached recovery. Production acceptance must remain blocked until actual approved versioned documents and destinations are supplied.

## Verification
82saved graph checks passed:16required combinations,7unchecked defaults,optional isolation/disclosure,offline/legal gating and recovery,normal/Google processing,duplicate blocking,errors/retry/10second timeout,draft retention,Back/Login routes,shared sizing,scroll configuration and no broken authored destinations.245country rows checked for correct variable assignment+dismiss action. Default screen and expanded consent content visually inspected; temporary preview variable/clip changes restored.
The graph tests are not live Present playback. Saved figma.combrowser access is denied; native text/search entry,realAPI/auth,durable restart persistence,screen-reader/OS/keyboard/RTL behavior remain unverified. No unapproved machine translations created.

## Review gate
Screen008is ready for visual/interaction review within these explicit prototype limits. Do not begin009or010without user direction. Original Figma/source/PRD/Blueprints/screens/web/admin untouched. Only existing Login entry link and V2section bounds changed as necessary dependencies.

