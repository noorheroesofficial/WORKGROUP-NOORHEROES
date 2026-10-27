# NoorHeroes V2 — Shared full-screen star system
Date: 2026-10-22

This supersedes the earlier top-only star treatment. The user explicitly included Splash in this update.

## Current implementation
- Existing file MR9935oQZACMjndzGIUgq5, NoorHeroes V2 Design → Onboarding only.
- 22 full-screen compositions: both Splash variants, four Language selections, four Intro screens, Login, Registration, five OTP compositions and five PIN compositions.
- 16 bottom sheets receive ten quiet accents each.17 transparent processing, timeout, error and keypad overlays inherit the underlying field. Two controlled testing panels remain unchanged.
- Each full-screen composition uses36 stars: the24-star stratified field plus12 scattered additions. Use deterministic seeded variation, avoid dense clusters, and retain the field across selection states.
- Reuse approved Calm Star component family1726:1206. No new star artwork or animation master family.
- Sizes4–13px, varied opacity, existing A/B/C rhythm/phase variants; staggered native AFTER_TIMEOUT → CHANGE_TO loops. Normal screens use7–9 starting phases. Reduced Motion Splash uses static Still.
- Star fields are transparent overlays with absolute positioning in Auto Layout parents, stretch constraints, and no click/press handlers. Stars have only their inherited timed animation.
- Text and branding bounds guide placement. Very low opacity applies where all candidate positions intersect protected content. Full-screen field opacity reduces over cards; sheet accents use0.10–0.16 instance opacity before artwork opacity.
- Previous decorative atmosphere layers are disabled, retained as references. No active decorative circle particles remain. Functional dots, indicators, radio controls, loaders, icon details and illustration content are preserved.
- Bottom sheets add only ten accents because the full-screen field remains visible beneath them; no additional field is added to transparent guards or snackbars.

## Reusable prompt for new screens
Apply the shared star-only system to this V2 mobile screen without changing its approved foreground. Reuse the existing Calm Star variants; do not recreate assets, add circles, or copy legacy atmosphere layers. Scatter a maximum of36 stars across the full viewport using a seeded stratified pattern, varied sizes and phases. Use fewer and quieter stars on sheets; inherit the field on transparent overlays. Keep typography and branding readable, preserve original interactions, and retain reduced-motion behavior. Ensure a decorative overlay never participates in Auto Layout flow and has no click, press, drag or scrolling handlers. Compare foreground properties and app reactions before/after; inspect the final screen and audit visible decorations for circles. Leave uncreated routes unmapped.

## Verification and boundaries
All57 V2-frame foreground/application-interaction fingerprints match. All38 edited compositions passed star geometry, varied-size/phase, minimum-spacing, no-click-handler and star-only checks; screenshots of all38 were reviewed in four contact sheets. Native Present playback, actual input hit testing, device performance and runtime accessibility were not validated. This is a Figma prototype implementation, not a production app release; no application repository or local companion code was changed.

For runtime implementation, use the app platform's equivalent of a non-interactive decorative layer, a single shared implementation, bounded particle count, stable seeds, reduced-motion support and measured device performance. Those runtime steps remain outside this Figma change.

Evidence: Evidence/2026-10-22_Full_Screen_Stars_Verification.json and 2026-10-22_Full_Star_Field_QA_1.jpg through QA_4.jpg.




## Latest density increase — 2026-10-22

User requested more animated stars on every screen. Increased22 full-screen fields from24 to36, and16 sheet fields from6 to10.328 new instances reuse the approved A/B/C rhythms and staggered starting phases. Reduced Motion Splash remains static. Minimum measured center separation28px; all fields in bounds and star-only. All38 foreground/application-interaction comparisons pass. Splash, Login and Optional Preferences visual samples inspected. Transparent overlays inherit the denser base field; no navigation or functional control changes. Live Present playback remains unverified. Evidence: Evidence/2026-10-22_Increased_Star_Density.json.
