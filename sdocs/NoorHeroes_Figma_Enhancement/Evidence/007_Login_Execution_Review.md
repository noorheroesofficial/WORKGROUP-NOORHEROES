# Screen 007 — Login implementation review

13 October 2026. Screen implemented for user review, not final sign-off. Work stopped before Screen 008.

[Open Login](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1278-155)

## Scope and content

User approved [the copy/layout proposal](007_Login_Readiness_and_Copy_Proposal.md). Existing NoorHeroes V2 Design1128:2 → Onboarding1270:140 was reused; no new file or module. All Login states are390×844. Existing approved gradient, typography roles, rounded Material icon components, Back transparency,18px canvases,4px icon-label gaps and350×56/r18 primary button were reused. Official Google artwork was cloned from1095:45 without recoloring. Added only readable auth text roles: NH/V2/Auth/Input16/24 Regular and NH/V2/Auth/Helper14/20 Regular.

All237 prompt files were read programmatically to create [the catalog](007_Screen_Prompt_Catalog.json);237 link the finalized baseline. Detailed requirement reconciliation in this turn focused on Screen007 and its adjacent authentication routes, not a fresh full-product audit.

## Frames

| State | Phone | Email |
|---|---|---|
| Default |1278:155|1278:780|
| Invalid/empty submission |1278:213|1278:838|
| Sending OTP |1278:271|1278:896|
| Timeout |1278:439|1278:1064|
| Offline |1278:497|1278:1122|
| Generic Google error |1278:555|1278:1180|
| Google processing simulation |1278:613|1278:1238|

Session expired1278:1405; Country code overlay1282:466. These are15 states of Screen007 plus one owned overlay, not15 additional journey screens. All are under Onboarding. The parent section was extended vertically to contain them; no alternate viewport sizes were added.

## Interaction review paths

1. From any Intro, click Skip; or from Parent Shield click the final CTA. All five now reach Login1278:155. Origin variable preserves which Intro the Login Back control returns to. First three Intro forward connections were retained.
2. Empty Phone → Send code → inline approved validation. Tapping the identifier field populates a sourced test fixture and clears the validation state. Email behaves equivalently. Field hit area is350×56; country control has its own44×44 hit area.
3. Switch Phone/Email; session prototype variables preserve each value. This is fixture-based input simulation, not native keyboard editing.
4. Populated identifier → Send code → animated pending with duplicate submission disabled →10-second timeout → Try again. The prototype intentionally exercises the timeout branch while OTP destination is absent. It does not imply all real requests fail or impose a10-second wait on successful production responses.
5. Google → animated processing → generic error after2seconds. Google Try again retries that same Google scenario; the OTP button remains Send code. Back/Escape during processing restores the form without a cancellation error. No Google account picker or real SDK call occurs.
6. Start the named Offline flow. OTP and Google are disabled; field fixture changes and method switching remain offline. Try again simulates connectivity recovery to the matching default form, preserving values. Keyboard R provides the same reviewer shortcut. Production must recheck actual connectivity, not clear offline unconditionally.
7. Country code → overlay →+1 or+971 → close; visible Back and Escape also close. These two options are project fixtures only. Full country search/list/empty-search behavior remains pending a confirmed country dataset.

Fixtures: RegistrationViewModelTest.kt uses5551234567 (line111) and test@example.com (lines184–185). OnboardingDraftState.kt defaults to+1. CrossScreenStateContinuityTest.kt line318 uses+971. These are existing test values, not live parent identities or an approved worldwide support list. No additional account data was invented.

## Motion

Default form groups use400ms opacity/8px-rise entrances with80ms stagger. Existing layout and typography remain fixed; transitions use250ms Dissolve. Sending and Google states contain three opacity-pulsed loading dots. OTP pending spans the10-second timeout scenario; Google failure scenario spans2seconds. Leaving a frame stops its motion. No separate success screen.

Reduced-motion specification remains opacity-only/short-dissolve with static loading text. Automatic OS reduced-motion detection and a separate reduced-motion prototype path were not implemented. No frame extractor was available from PATH, and no live Present playback or motion export was performed; screenshots validate resting layout only.

## Confirmed versus deferred routing

Confirmed inbound: Intro Skip1219:44/106/163/220 and final1219:246 →1278:155, with origin bookkeeping. No Login route was added before approved content existed.

Deliberately unmapped: Register →future008; successful OTP →future010; Forgot access →future030; successful Google →bootstrap-directed existing/created destinations when confirmed. No links to original Registration or arbitrary Profile Picker were added. These visible links will receive reactions once confirmed V2 destinations exist, per explicit user instruction.

## Verification performed

- Compared Login and all four finalized Intro screens side by side at equal scale; inspected Login at1x.
- Compared Email, validation, loading, timeout and offline layouts; inspected final offline view at1x. Temporary comparison frames were removed.
- Repaired unwanted solid backgrounds on transparent icon bounds; retained actual shared vector artwork and icon meanings.
- Corrected offline tab/input navigation to retain offline, and Google retry to retry Google.
- Final structural audit:94 inspected navigation branches, zero nonexistent destinations, no blank text nodes, and no connected Control node smaller than44×44.
- All16 Login-owned frames/overlay are390×844 and parented to1270:140. Longest content ends at804, leaving40px below. No clipped errors or overlapping actions in reviewed screenshots.
- Primary/secondary text, teal action and error text use approved readable roles. Disabled controls visibly differ. No runtime screen-reader, keyboard, text-scaling or OS lifecycle verification was performed.
- [Machine-readable audit](007_Login_Structural_Audit.json) records current frame IDs, routes, timings, and source-container geometry.

## Preservation observation

No writes targeted original designs, PRD, blueprints, Screens, web or admin nodes. Source containers1095:2 and1085:13003 retained their dimensions and child counts (70 and35). Their X positions changed between reads:79296→58509 and96835→77201. The cause was not established; this may reflect live canvas changes outside the scoped mutations. Their positions were not restored over potentially concurrent user work. Therefore this report does not claim byte-for-byte or positional invariance of the whole shared file.

## Review limits and next step

Layout and stored reaction graph verified; interactive Present playback remains unverified. Prototype uses fixed test fixtures and simulated outcomes, not real text input, authentication, network detection, server validation or durable storage. Full country coverage, localized Login copy, actual keyboard avoidance and automatic reduced motion remain unimplemented. Future destination links remain intentionally pending.

Review Screen007 before proceeding to Screen008. Do not interpret the number of alternate states as authorization to create further product screens.
