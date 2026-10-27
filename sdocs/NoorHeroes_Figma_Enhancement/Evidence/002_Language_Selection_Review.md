# Screen 002 — Language Selection review

> Historical revision, superseded by the [current reference revision](002_Reference_Revision.md). Its QA/handoff frames have been deleted at the user's request. Current interaction uses Continue with loading/success feedback and an explicitly pending Screen 003 destination.

Date: 2026-10-13. Status: built in existing V2; awaiting user screen review. All 237 screen prompt Markdown files were read. Screen 003 enhancement has not started.

## Approved conflict resolution

User explicitly selected: **PRD/blueprint: four languages, select on tap and proceed to Intro**. This supersedes the preview's eight-language list and Continue button for this screen. Order follows blueprint localization list: English, Hindi, Arabic, Urdu. PRD A1 §2.4 table requires immediate persistence without separate confirmation; K-02 blueprint §§10,14 specifies immediate local save and four launch locales.

Exact heading and description retained: `Choose your language`; `Select the language for your experience`. Autonyms: `English`, `हिंदी`, `العربية`, `اردو`. Hindi comes from existing onboarding `LanguageSelectionState.kt` and Hindi `strings.xml`; it is a requirement-driven addition, not a generated translation.

## Figma references and deliverables

- Page 928:2; reused V2 section 1128:2.
- Default: [1166:181](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1166-181).
- Selected English/Hindi/Arabic/Urdu: 1166:215 / 1166:250 / 1166:285 / 1166:320.
- QA 320/360/420: 1168:128 / 1168:162 / 1168:196.
- 320 at 200% text: 1168:230. Vertical cards, wrapping text, scrollable viewport.
- Reduced motion: 1168:264; immediate navigation, no transition.
- Intro reference handoff: 1168:2, copied from Frame 2 1085:19139, clearly named `NH/Reference Handoff/003/Intro Slide 1 — Pending Review`. It preserves source copy; unavailable source fonts were replaced on the copy with loaded Poppins. The original was not altered. This dependency is a visual destination, not an approved enhanced or translated Intro screen; its own controls are intentionally unwired until Screen 003.
- Frame 2 visual reference 1085:18818 inspected; combined desktop layout, unverifiable trust claims and richer extra content were not imported into Language Selection.
- Local source screenshot `Screens/Mobile App/Onboarding/Language.png` inspected read-only. Library search found no matching Language selection or Globe icon components; local screen layers reuse source token/font direction.

## Visual changes

Warm cream canvas, single column of white rounded cards, compact globe header, Poppins typography, native-script fonts Noto Sans Devanagari and Noto Sans Arabic. Selected state combines teal outline, tinted surface and checkmark. Unselected radio outline darkened for contrast. No extra product copy or statistics added.

## Prototype and motion

First-launch demonstration: V2 Splash 1131:2 → Language Default after 2.5s → tapped locale selected state (160ms Smart Animate) → Intro reference handoff after 180ms, with 180ms dissolve. Tapping the already-selected locale proceeds directly. Each card is fully clickable. These transitions are restrained proposals, cancel on navigation, and do not delay real application persistence. Reduced-motion test uses no transitions.

Real DataStore persistence, parent-profile synchronization, session/bootstrap branches, OS back/exit, restoration after app kill, offline operation and OS locale refresh remain production behavior specified by the PRD/blueprint. Selected frames simulate feedback; they do not write production preferences. No network loading/error state was fabricated for this bundled list.

## Validation and limitations

Screenshots inspected for Default, Arabic selection and large-text QA. Structural checks report four cards in every variant, 79px minimum card height, no horizontal text overflow, and vertical scrolling. Narrow layouts cover 320/360/390/420. Large text content height 1314px scrolls in an 844px viewport. Original Frame1 and Frame2 bounds and direct child counts are unchanged (70 and 35). Prototype destination IDs and reaction definitions were checked programmatically; interactive Present playback was not exercised.

Localized interface headings and full RTL translated Intro content remain unavailable in the supplied prompt. Arabic/Urdu autonyms use native shaping, but the current selection and Intro reference retain verified English interface copy. Full locale rendering, RTL mirroring and returning-user restoration require localized source review; no translations were invented. Do not claim those acceptance items complete.

Back from Intro in the future enhanced flow must return to the selected locale context without discarding the stored preference. First-launch OS back exits/returns to the entry context according to platform implementation; no invented visible Back button was added. Later settings reuse must return to its invoking Settings surface, not Intro. These alternate entry routes are documented, not wired into this pre-auth demonstration.

Await user review before enhancing Screen 003. Source PRD/blueprint/screens, original Figma designs, web and admin remain unchanged.
