# V2 Multiple-child Profile Picker — 26 October 2026

Applied to the existing Figma design, file MR9935oQZACMjndzGIUgq5. Mobile page 928:2, V2 1128:2, Profile Picker section 2188:7267, original Default frame 2188:7275. No application/backend/admin/web code was changed.

## Requested design and applied result

The supplied attachment and screenshot govern the card layout. Existing teal gradient, star atmosphere, toolbar, cream screen surface, heading and footer were preserved. The actual main screen paint JSON matches the pre-edit snapshot exactly.

- Two-column, wrapping grid; child cards are 163 × 236 with 12 px gaps. Parent tile follows the card grid; Add Child uses a compact full-width dashed tile. The existing fixed footer remains outside the vertical scrolling viewport.
- Three profiles: saved Profile Setup identity plus fictional Zayd and Maryam samples. Saved name, DOB, avatar and learning level remain connected to the saved setup variables. The saved child's DOB is shown directly rather than inventing an age calculation. No unsupported star totals, achievements or subscription-slot claims were copied from the image.
- Radio/checkmark selection is replaced by a 44 × 44 Material lock/open-lock control. A gold outline and explicit Selected label distinguish selection from lock status.
- Shared NH/V2/ChildProfileCard family 2232:10365 has Locked, Unlocked, Loading and Error states, each with Rest/Selected variants. It exposes name, details, information, avatar swap and missing-image properties. Existing NH colors, text styles, spacing and radii are reused. Loading uses the approved dark-dot component 327:17; error feedback uses existing semantic error tokens.
- Nicknames wrap to two lines. Exceptionally long names use an ending ellipsis without changing the stored full name; verification context retains the full name. The review sample Abdurrahman Yusuf fits fully in two lines. Missing images use a Material person fallback in both the card and selected-child verification views.

## Functional prototype behavior

Each child has independent access state, configured lock type, attempts, cooldown, remaining countdown and simulated saved PIN markers. The existing Screen 023 gate is reused with a selected-child context; no new authentication mechanism was invented.

Closed lock or locked card body loads that child's state and opens its PIN/pattern/biometric gate. Successful verification unlocks only that child. It does not remove the configured security method. An open-lock control re-locks a configured profile. If a profile has no configured lock, its lock control enters the existing verified-parent recovery flow before configuration. Loading controls do not activate.

Wrong credentials, cancellation and failed saves do not grant access. Existing progressive lockouts are retained independently per child. Switching profiles cannot reset a child's failed attempts or cooldown. Recovery commits only the selected child's new markers/configuration; another child's PIN remains valid. Back and accepted return preserve the invoking picker frame, including Offline. Biometric Cancel closes only its simulated system sheet.

**User decision: keep Child Home navigation pending.** An unlocked card currently updates the selected profile without inventing a home destination or activating a production session. After verification, Back to profiles shows the updated open lock. Existing Parent/Add Child management destinations remain pending as before; they were not replaced with guessed routes.

## Review and scenario nodes

| Scenario | Node |
|---|---|
| Original Default / mixed family | 2188:7275 |
| All unlocked | 2245:11287 |
| All locked | 2245:11582 |
| Mixed profiles | 2245:11877 |
| Only one unlocked | 2245:12172 |
| Long name / missing image | 2245:12467 |
| Single child | 2245:12762 |
| Four component states as instances | 2254:12023 |

Scenario-start frames display their review state on canvas. In Present they initialize the scenario and navigate to the existing Default frame, so the same actual card/gate implementation handles all scenarios. Existing Empty 2188:7543, Offline 2188:7787, Loading 2188:8027 and Error 2188:8267 states were retained.

## Sources and verification

Reviewed the actual linked picker and surrounding 023/024 frames; Feature_A1_Splash_Auth_Onboarding.md; the A1 KMP 08-profile-picker-child-lock-first-mission-flow.md blueprint; existing ProfilePickerViewModel/Screen and NH components/tokens. Product behavior follows the PRD/blueprint rather than assuming that changing an icon authenticates a child.

**42/42 assertions passed against actual Figma reaction JSON.** They cover the unlocked/locked/mixed/single scenarios, target-only PIN/pattern/biometric unlock, failed attempts, cancel/back, per-child cooldown persistence, progressive fifth failure, targeted parent recovery, preservation of other PINs, No Lock configuration gating, loading guards, full long-name context, background equality, absence of radio controls and destination validity. All 18 referenced destinations in the evaluated changed flows exist.

Canvas screenshots were inspected for Default, long name/fallback, single child, all unlocked, all locked, Error, Loading and the component-state review. All mobile frames remain 390 × 844. The full-width Add Child tile intentionally continues below the viewport in the three-child case and is reached by scrolling; the footer does not cover the scroll content's final position.

Evidence files: 2026-10-26_Profile_Picker_Default.png, _LongName.png, _Single.png, _AllUnlocked.png, _AllLocked.png, _Error.png, _Loading.png and _ComponentStates.png. Created IDs, variable map, related mutations and assertion results are recorded in 2026-10-26_Profile_Picker_Ledger.json.

## Verification limits

Canvas inspection and reaction evaluation are not live Present playback. The existing saved browser restriction prevented prior figma.com Present access; live playback remains unverified. These are native Figma simulations, not backend identity verification, secure credential storage or OS biometric authentication. Do not enter actual credentials.

The countdown simulation advances while its timer frame runs; it is not an authoritative wall-clock/server timer. Device accessibility, screen readers, keyboard/safe-area behavior and OS reduced-motion playback were not tested. Only the authorized standard mobile viewport was designed. No new home, dashboard or subscription navigation was invented.
