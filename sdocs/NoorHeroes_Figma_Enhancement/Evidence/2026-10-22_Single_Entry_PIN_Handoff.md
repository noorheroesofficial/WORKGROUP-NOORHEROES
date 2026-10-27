# OTP and single-entry Parent PIN — latest behavior

22 October 2026. User explicitly removed PIN confirmation and subsequently clarified: **no PIN-success dialog; open Biometric directly**. This supersedes the older two-pass PIN and proposed success-dialog flow. Existing Figma V2/Onboarding reused.

## Current flow

Successful OTP verification → Set Parent PIN1650:502 → Continue saves once → eligible Biometric offer1670:1069. Successful resend and invalid/failed OTP do not advance to PIN. Per the newest instruction, successful verification from generic Login as well as Registration now opens confirmed PIN setup; the earlier new-parent-only gate is retired for this prototype route. Consent checks on Registration remain unchanged.

No Confirm PIN screen or PIN-length selector exists in this active step. Continue remains disabled for0–3 digits, enables for4–6, and additional input beyond6 is prevented. Deletion below4 disables again. Main button and keyboard Enter immediately start saving; no second entry. Setup title, explanatory copy and Continue label remain consistent.

PIN input is a count-only simulation: actual PIN digits are never stored, displayed or logged. This Figma prototype does not perform secure hashing, local storage, server persistence or OS biometric authentication. Production must do secure persistence before the success response. Do not describe the prototype as implementing those systems.

## Changed elements

- Existing PIN keypad, main button, Back, keyboard input, Reset, save/timeout/error and Retry actions use the single-entry state. Busy blocks input and duplicate submission. Save failure preserves the entered count, restores Continue and reuses approved Snackbar copy. Retry swaps to the input guard without stacking overlays. Saving success clears transient entry counts and marks the simulated PIN saved, then directly swaps to Biometrics if eligible.
- Back/Escape returns to a usable OTP state, preserving the invoking auth context and masked recipient. On OTP→PIN entry, initialize six maximum masked slots and Continue, regardless of the previous saved length.
- Confirmation and Mismatch review compositions1654:544/1654:840 and their Match/Mismatch review rows1650:901/1650:903 removed. Remaining Saving/Offline review compositions and instructions updated to single-entry wording. No confirmation copy or actions remain in the module. Legacy variables retained only where earlier initialization/review compatibility still references them; they do not create a confirmation step.
- Approved12×12 gold star artwork cloned from1612:1298 under the OTP card in the main screen and four review compositions. It is centered atx189,24px below each card, visible and inside the390×844 root. Existing OTP fields, resend, inline recipient/Edit and Verify styling preserved.
- OTP flow-start label now **OTP Verification → Set Parent PIN → Biometrics**. Full Registration start and direct PIN start remain available.

## Biometric and future destination boundary

Existing offer, system simulation and error/retry sheets reused. Cancel, Skip and backdrop/Escape dismissal preserve saved PIN and stop transient processing; unavailable hardware bypasses the offer. These exits do not navigate to a fabricated destination. Add Child014 still has no approved V2 frame; its future connection remains unmapped under the prior explicit user rule. No success dialog was created.

## Validation

33 stored-action checks passed, covering direct OTP success/error/resend, all digit lengths, deletion/input cap, one-entry save for4/5/6 digits, duplicate guards, offline/API/timeout recovery, Back/reverification, biometric enable/skip/cancel/unavailable/error/retry.21 prototype destinations resolve; zero confirmation actions/copy remain. Five below-card stars are visible and fit. Final OTP and PIN screenshots inspected at390×844. Present playback, real OS/native lifecycle and production security remain unverified.

[Verification](2026-10-22_Single_Entry_PIN_Verification.json) · [Native-action test](2026-10-22_Single_Entry_PIN_Test.js) · [OTP screenshot](2026-10-22_OTP_Star.png) · [PIN screenshot](2026-10-22_Single_Entry_PIN.png).

Figma: [OTP](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1612-1277), [single PIN entry](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1650-502), [Biometrics](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1670-1061).

Stop for review; do not automatically create the next screen. Earlier two-pass tests/handoffs are historical and must not be treated as the current interaction contract.

> **Later correction —22 October2026:** User requested preservation of every screen in Parent PIN section1650:465. Main1650:502 was never deleted. Removed Confirmation/Mismatch review compositions have now been reconstructed at1709:675/1709:947 using editable existing assets, in their original canvas positions. The old deleted IDs are not recoverable through the available API. They are retained as references without incoming live prototype connections. The one-entry active flow is unchanged. Do not remove screens to retire a navigation step.

