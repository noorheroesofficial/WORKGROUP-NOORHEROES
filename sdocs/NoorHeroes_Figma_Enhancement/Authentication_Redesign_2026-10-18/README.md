# NoorHeroes V2 — Authentication Redesign

Date: 2026-10-18. Status: editable designs saved for review; embedded Code Layer blocked by account capability.

[Open redesign section](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1330-5686) · [Login prototype](https://www.figma.com/proto/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?page-id=928%3A2&node-id=1330-5697) · [Local functional companion](http://127.0.0.1:8765/) · [Evidence](evidence/figma-audit.json)

## Scope and authority

The user's attached 2026-10-18 Login, Branding & Language Selector Redesign brief supersedes earlier visual treatment for these copies. Existing approved copy and phone/email OTP plus Google behavior remain the functional reference. The screenshot with password fields supplies composition only; no password login was added. The original Figma screens, brand assets, web/admin content and protected PRD/Blueprint/Screens directories were not targeted by design writes.

Relevant requirements: PRD_Documents/Child App (1-12)/Feature_A1_Splash_Auth_Onboarding.md; Screen_Prompts/007_Login_phone_email_Google.md; 12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md; Evidence/007_Login_Readiness_and_Copy_Proposal.md. Proposed Login copy/layout had explicit prior user approval. No religious copy was added.

## Saved organization

New top-level section: NoorHeroes V2 — Authentication Redesign (1330:5686), on Mobile page928:2 in the existing file. Eight sub-sections follow the requested names and order:

1. 01 — Splash Reference & Brand Tokens:1330:5687
2. 02 — Login Screen Redesign:1330:5688
3. 03 — Authentication Components:1330:5689
4. 04 — Gradient Button Variants:1330:5690
5. 05 — Country Code Bottom Sheet:1330:5691
6. 06 — Language Selector Branding:1330:5692
7. 07 — Animation & Interaction States:1330:5693
8. 08 — Responsive & Edge Cases:1330:5694

## Screen traceability

| Existing state | Original | Redesigned copy |
|---|---|---|
| Phone-Default | [1278:155](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1278-155) | [1330:5697](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1330-5697) |
| Phone-Invalid | [1278:213](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1278-213) | [1330:5800](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1330-5800) |
| Phone-Sending | [1278:271](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1278-271) | [1330:5873](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1330-5873) |
| Phone-Timeout | [1278:439](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1278-439) | [1330:6053](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1330-6053) |
| Phone-Offline | [1278:497](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1278-497) | [1330:6126](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1330-6126) |
| Phone-Error | [1278:555](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1278-555) | [1330:6201](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1330-6201) |
| Phone-Google-Processing | [1278:613](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1278-613) | [1330:6274](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1330-6274) |
| Email-Default | [1278:780](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1278-780) | [1330:6456](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1330-6456) |
| Email-Invalid | [1278:838](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1278-838) | [1330:6559](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1330-6559) |
| Email-Sending | [1278:896](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1278-896) | [1330:6632](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1330-6632) |
| Email-Timeout | [1278:1064](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1278-1064) | [1330:6812](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1330-6812) |
| Email-Offline | [1278:1122](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1278-1122) | [1330:6885](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1330-6885) |
| Email-Error | [1278:1180](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1278-1180) | [1330:6960](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1330-6960) |
| Email-Google-Processing | [1278:1238](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1278-1238) | [1330:7033](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1330-7033) |
| Session-Expired | [1278:1405](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1278-1405) | [1330:7215](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1330-7215) |

All15 current V2 Login states were copied and redesigned. No separate approved Registration/OTP/Forgot-access screens currently exist in V2; the original reference frames are preserved. This task does not invent those screens or their destinations.

Language copies:1330:7288 English;1330:7470 Hindi;1330:7652 Arabic;1330:7834 Urdu. Preserve exact four languages, native labels, original selection states and Continue semantics. Approved monogram1300:65 is instanced at the top-right at45px width with original aspect ratio; primary button uses the shared gradient.

## Confirmed flow

Splash copy1330:8061 — after4s → Language1330:7288. Each row links to its corresponding copied selected-language state. Continue opens Processing1330:8016 — after1.95s → first copied Intro1336:1535, then1336:1631 →1336:1722 →1336:1820. Intro screens are unmodified visual copies of the approved set; Skip and final exit lead to redesigned Login1330:5697. Intro Back uses prototype history. Processing does not flash Continue before navigation.

Login retains phone/email method switching, test-fixture input taps, validation, processing,10s timeout,2s Google-failure simulation, retry and offline recovery. New Login Back routing resolves all four recorded Intro origins rather than the original two-branch fallback. All confirmed destinations are preserved; OTP010, Register008, Forgot-access030 and Google-success destinations remain unmapped under the user's explicit rule.

Four flow starts are saved: Splash to Login, Login, Offline recovery and Language. Static QA copies are inspection aids rather than new product destinations.

## Shared visual system

Background copies actual1131:2 fills, including transform and stops:0=(.047,.45,.447),.48=(.06,.20,.20),1=(.055,.08,.094). RGB values are normalized. The backdrop is teal to dark teal to near-black; it is not a newly invented multicolor palette.

Primary gradient is vertical, using exact first and middle splash colors. Paint styles: NH/V2/Auth Redesign/Primary Vertical — Splash Stops0 &0.48, and Background — Exact Splash. Button component set1334:643 provides Default1334:499, Pressed1334:507, Disabled1334:515, Loading1334:633, Focused1334:639. Height56px, radius18px, Poppins14/20 semibold; language CTA keeps its approved64px height. Default/Focused use press feedback; Disabled/Loading have no submission action. Labels and arrows are centered with4px gaps and18px icon canvases.

Login uses an ivory approved-logo surface above a curved light form panel. Reused approved Logo Without Tagline1300:30 includes the original NH monogram and NoorHeroes wordmark. Panel top-left/bottom-right radii56px; remaining corners square. Poppins24/32 semibold heading,14/20 supporting copy,16/24 input text. Form uses24px horizontal padding and20px section gaps; source content is preserved exactly. Secondary links retain their meanings, with readable gold on the dark background. Scroll handles longer error layouts.

## Country selector

Native sheets: All1332:1815, fragment-search simulation1332:3065, no-results simulation1332:3105. Full list contains245 countries/territories, each with actual flag artwork, country name and dialing code; content scrolls. A slide-up sheet, backdrop dismiss, close/back control and Escape are wired. Selecting a country sets country name, ISO and dialing code, then closes without resetting phone/email variables.

Native limitations are explicit: search is a staged simulation, not arbitrary typed filtering. Color-emoji flags rendered blank in Figma; list rows therefore use84×63px source-derived PNG assets displayed at28×21px. The dynamically changing native selected-country marker uses the ISO label. The local companion updates the actual selected flag image. Native dynamic image replacement is not represented as implemented.

Country data is a pinned snapshot of libphonenumber-js1.12.24 metadata, with English display names from Intl.DisplayNames. Includes country/territory entries only; non-geographic calling services are excluded. It is a dialing-data coverage set, not a legal list of sovereign states. Flag sources: flag-icons7.5.0, with AC/TA from country-flag-icons1.5.21. Source files and licenses are retained in prototype/.

## Motion

Login brand entrance: opacity.35→1 in550ms, translationY7→0 in650ms, Ease Out. The form remains stable. Country sheet: translationY676→0 in320ms, Ease Out; Escape/close/backdrop cancel. Primary press feedback uses100ms Smart Animate. Existing Intro, Language row entrance and processing motion are retained in copies. Native Login reduced-motion QA copy1336:2409 removes descendant authored motion; this is a separate inspection state, not OS preference detection.

Local companion:320ms button width/radius morph into a104px progress pill; three dots pulse continuously with1.05s cycles and140ms stagger. The56px button slot stays fixed. Failure/timeout returns the action to full width, restores input and allows retry. No success screen is invented. Country sheet320ms slide-up; brand650ms fade/rise. prefers-reduced-motion and a review toggle disable motion and leave a static progress indicator. No animation constitutes a backend completion signal.

## Local functional companion

Open http://127.0.0.1:8765/ while the local server is running. To restart, run this command from prototype/:

```powershell
python -m http.server 8765 --bind 127.0.0.1
```

The companion implements actual DOM inputs, name/fragments/dial-code search, clear/no-results, all245 selectable country rows, selected indicator, flag/code updates, modal focus containment, Escape and backdrop dismiss, preserved field values across method changes/country selection, and selected country/language persistence. Country data is bundled, so no runtime list-fetch/loading/error scenario is fabricated. No phone/email input values are stored persistently.

Review controls outside the phone expose timeout, request failure, offline, expired session,200% text, RTL layout and reduced-motion checks. Authentication is simulated; no request is made to an auth backend. Continue on Language links after progress to the existing confirmed first Intro in the original prototype. Standalone Back, Register and Forgot-access are unavailable because the companion has no confirmed embedded screens for those exits. These controls do not guess destinations.

## Capability block and import status

Fresh whoami retries on2026-10-18 report code_layers_enabled:false for the signed-in account and both listed plans. No import was attempted and no new file was created. User authorization to add a Code Layer is recorded, but it does not enable the account feature.

The figma-code-workflows skill says: “Only choose or import a Design Code Layer when whoami.code_layers_enabled is true.” Skill source: C:/Users/Sarva/.codex/plugins/cache/openai-curated-remote/figma/16.0.0/skills/figma-code-workflows/SKILL.md. Once available, import this prepared companion into the same Design file/page through send_code_to_figma, following its returned upload/archive instructions. Recheck capability first. A standalone Make file requires a separate user destination decision.

## Verification and remaining limits

See [validation report](VALIDATION.md), [native graph/copy audit](evidence/figma-audit.json), [node handoff](figma-state.json), and screenshots: [Login](evidence/login.png), [Language](evidence/language.png), [Country sheet](evidence/country-sheet.png).

Native audit:15 Login states,4 language states,245 country rows and245 flag assets; zero exact-copy omissions after including hidden instance text;183 node destinations checked with none missing. Opening native Present was blocked by a saved browser permission denying access to figma.com, so live playback remains unverified. No browser workaround was attempted. Auth/network outcomes are simulated, and arbitrary native search/dynamic selected-flag artwork remain blocked by unavailable Code Layers.

Native QA frames cover320×568,390×844,430×932,390×544 reduced viewport, and a reduced-motion copy. Local browser checks cover small/large widths,200% text, RTL layout, country filtering/selection, validation, loading lockout and recovery. These are browser/layout checks, not physical-device keyboard, safe-area, screen-reader or complete localization certification. English copy was mirrored for RTL layout testing; no translations were invented.

