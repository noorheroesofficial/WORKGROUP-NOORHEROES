# Screen022 — Profile Picker review

Figma-only.25October2026. Existing file MR9935oQZACMjndzGIUgq5, mobile page928:2, V2 section1128:2. No app code changed.

## Delivered

Section2188:7267 contains six390×844 review frames:

| State | Node |
|---|---|
| Default, new child without configured lock |2188:7275|
| Empty / no active children |2188:7543|
| Offline cached profiles, configured lock fixture |2188:7787|
| Loading |2188:8027|
| Load error with Retry |2188:8267|
| Child lock configured |2189:7165|

Reused existing NH/ChildIdentity Hero639:2048, original saved avatar artwork stack, NH/EmptyState589:3/589:37, NH/Skeleton588:5, NH Button322:21/322:69, approved toolbar, stars, palette, typography and layout tokens. Added local review-state variables; no new global component, color or text-style definitions.

Family Summary Confirm2137:6721 is now enabled and navigates to2188:7275. Picker Back and Back to setup return to2137:6635. Error Retry returns to Default. Active child name and avatar consume the saved-profile snapshot from Add Child. Empty state puts Add Child first. No progress comparisons, fictional extra children, capacity slots or ungated editing were introduced.

## Source decisions and unresolved routes

- Reviewed prompts022–024, current live reference1095:282, child-lock reference1111:7445, Feature_A1_Splash_Auth_Onboarding.md, KMP blueprint08-profile-picker-child-lock-first-mission-flow.md, current app English strings, and finalized V2 guidance.
- Used current-mobile/source app copy for Picker rather than Frame1's different title, sample stars/levels, claims and hard-coded children.
- Age labels are omitted pending a saved/server-derived age value. The current snapshot has DOB but no authoritative age property. No approximate age calculation was introduced. This is a documented content difference for review.
- New child Default has no PIN-required label. The configured-lock and offline fixtures show PIN required. Actual child-lock configuration/server policy is not implemented by these review variables.
- Child, Parent and Add Child tiles deliberately have no navigation until Child Lock023, a verified Parent Gate and relevant approved destinations are available. No ungated Parent/Add Child bypass was created. Child Home and Parent Dashboard do not yet exist in V2.
- Original reference frames and web/admin designs were preserved.

## Checks and evidence

All six frames measured390×844 with footer inside the card, vertical overflow enabled for content and exactly one visible saved avatar in the identity stack. Verified current saved-name binding, default/configured-lock label visibility, empty-state Add Child ordering, existing Confirm destination, and Retry destination. Default and Empty screenshots inspected:2026-10-25_022_Profile_Picker_Default.png /2026-10-25_022_Profile_Picker_Empty.png.

Live Present playback, production child filtering, device security, backend persistence, locale/RTL and text-scale behavior were not tested. These are editable review designs and stored-link checks.

## Review gate

Screen022 prompt section11 states: “Stop and wait for my review and approval before moving to another screen.” Screen023 and024 were read and source-audited but have not been created. Existing app resources contain their PIN/pattern/biometric/recovery strings, including the two-phase parent verification → new-lock configuration flow; these will inform the next approved screen.
