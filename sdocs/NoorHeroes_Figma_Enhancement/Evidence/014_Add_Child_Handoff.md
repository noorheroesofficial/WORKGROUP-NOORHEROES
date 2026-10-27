# Screen014 — Add Child

Created in the existing file: NoorHeroes V2 Design1128:2 → Onboarding1270:140 → **014 — Add Child1804:2599**. Main screen1804:2656; valid review1806:3639. All product/state roots are390×844; no new Figma file, original-screen edits, web/admin edits or additional screen sizes.

## Approved direction

User approved screenshot wording and PRD additions, plus the3–17 DOB rule and proposed error/saved/accessibility copy. Reused finalized Login/PIN background, toolbar, approved logo/wordmark, Poppins typography, shared fields/buttons,48px primary/loading heights,14px layout spacing, shared Snackbar and approved staggered stars. Required form content scrolls within the card; Save remains fixed.

Required: nickname, DOB, avatar, preferred language, learning level. No raw age selector. Optional sheet: seven existing-catalog interests, daily goal5/15/30/45, AI Voice Guidance OFF, Large text and High contrast. Parent personalization AND voice opt-in is required before per-child AI selection can turn on; no real permission is granted. Portrait assets are the existing standalone Tariq/Maryam/Noor pictures1085:21471/21480/21490; rejected embedded thumbnail mockups1095:452/462/468. These portraits are visual sample choices, not a verified mapping to the production age-tagged companion catalog.

## Interactions

- Nickname/date/language controls open local sheets; avatar and level choices remain embedded in the Add Child form. Optional preferences scroll independently and preserve selection on dismissal.
- Save requires all five fields, supported DOB, connectivity, capacity, no pending request and no saved result. It changes to the shared same-height loader; duplicate clicks are guarded.
- API/timeout/offline/capacity feedback uses the shared Snackbar. Error retry preserves the simulated attempt key and draft. DOB errors expand the field slot from88 to116px with a14px clear gap; invalid selected dates remain displayed.
- Duplicate nickname requires a different avatar AND explicit Confirm Name. Cancel/Change Details retains the draft. Back during saving restores an editable draft rather than stranding the loader.
- Confirmed inbound routes now open014 after successful PIN when biometrics are unavailable, biometric Skip, and biometric success. Cancel/Escape in the simulated OS prompt returns to the existing biometric offer, without enabling biometrics. Source PIN screens remain intact.
- A saved result shows “Child profile saved.” Future018 Add Another Child and019 confirmation remain unmapped. Screens015–017 were not separately created; this014 form contains its required basic selections. Stop here for user review.

## Prototype limits

Native Figma Design uses **controlled fixtures**: Aisha/Yusuf nickname choices; June dates in2000/2009/2015/2019/2025; sample portraits; simulated outcomes. It does not provide unrestricted typing, a complete platform date picker, verified age-band/catalog filtering, actual profile creation, encrypted persistence, a server-issued idempotency guarantee, consent recording or OS biometric grants. The Review/014 panel is explicitly separate from app UI. Accessibility choices record preferences; they do not prove runtime font scaling or contrast settings.

The fixed prototype dates demonstrate below-minimum/above-maximum cases and supported samples against the approved3–17 policy; full date-boundary validation remains a runtime responsibility. Existing mobile code currently accepts3–18, a documented PRD conflict; this Figma task does not change production code.

Saved browser policy continues to deny figma.com. **Native Present clicking, scrolling, keyboard behavior and real-device accessibility remain unverified.** Stored graph evaluation is not live playback, and does not establish that the earlier reported PIN Present issue is fixed.

## Verification

- [Add Child stored-action checks](014_Verification.json): **64/64 pass**.
- [Upstream OTP/PIN/biometric regression checks](014_Upstream_Verification.json): **39/39 pass**, updated to expect the now-confirmed014 destination after Skip.
- [Final inventory](014_Final_Inventory.json):23 stored destinations resolve; all product/state roots390×844;12 primary/loading instances48px; no interactive target below44px;212 editable text nodes.204 stars reuse the shared family: four full-screen compositions×36, six sheets×10.
- [Default](014_Default.png), [valid draft](014_Valid_Draft.png), [DOB picker](014_Date_Picker.png), [optional preferences](014_Optional_Preferences.png) screenshots inspected. Also inspected DOB error, duplicate sheet, and full field content; corrected clipping/overflow and source thumbnail misuse.

Existing global component masters were reused, not modified or detached. Original reference frames remain unchanged. Incoming route edits are limited to the confirmed new destination and biometric cancellation recovery. No API/backend or local companion implementation is included.

Future work: review014, then follow015 only when requested. Keep all future destinations unmapped until confirmed. Preserve the current48px primary height and root/stable hit-target ownership; do not put decorative full-screen frames above active click targets.
