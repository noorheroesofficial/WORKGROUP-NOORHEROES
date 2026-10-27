# Latest Parent PIN flow — separate confirmation screen

22 October2026. User explicitly requested **enter Parent PIN → Continue → Confirm your Parent PIN → Save PIN →013 Biometric Enrollment**. This supersedes the earlier single-entry instruction. No screen was removed.

## Live screens

- First entry1650:502 remains in section1650:465. Enter4–6 masked positions;0–3 disables Continue, more than6 prevented. No length-selection controls.
- Continue captures the first-entry length and opens the preserved confirmation1709:675. It does not start saving. This frame is now named NH/V2/Onboarding/012/Parent_PIN_Confirmation/Default, in its existing position.
- Confirmation accepts exactly the captured4/5/6 length. Save PIN stays disabled until complete. Back returns to first entry retaining its count; Continue reopens an empty confirmation.
- Save PIN starts existing1650:844 processing only after the matching fixture passes. Successful response marks the simulated PIN saved, clears counts and opens existing Biometric offer1670:1069 when hardware is eligible. No success dialog.
- Confirmed entry is retained on offline/API/timeout failure. Existing Snackbar Retry processes the confirmation again. Busy prevents duplicate saves/edits. Mismatch clears confirmation only and shows the existing approved message.

All eight390×844 screens in1650:465 are preserved, including historical Mismatch1709:947, Saving/Offline review compositions and all processing/timeout/error views. Review-only Match/Mismatch fixture rows were restored as1711:905/1711:908. No reference frame is deleted to alter navigation.

## Components and state

Existing keypad, buttons, loading dots, text and masks reused. First-entry and confirmation masks now bind to separate derived count variables so the two canvas frames remain visually distinct. Continue and Save PIN use their own readiness states. Confirmation loader inherits the approved primary loader animation; Cancel/back is unavailable while saving. Keyboard digits/Delete/Enter/Escape and D review controls are mapped on both screens. OTP entry and the review launcher refresh masked indicators without stale previous values.

This native Figma prototype intentionally stores counts rather than actual PIN strings. Match/mismatch remains a controlled review fixture, not real digit comparison, hashing or secure storage. Production secure verification/storage and real biometric APIs are outside this artifact. No raw PIN is displayed or logged. Existing optional biometric Skip/Cancel/unavailable behavior and future Add Child unmapped boundary remain unchanged.

## Verification

39 stored native-action checks passed: OTP entry,0–6 readiness, cap/deletion, explicit confirmation for each valid length, incomplete/full confirmation, Save loading, success→Biometric, retained input on Back, clean re-entry, mismatch/correction, duplicate guards, offline/API Retry, timeout, full end-to-end biometric enable, Skip and Cancel.22 destinations resolve. All eight screens remain, confirmation fits390×844 with card bottom680. Final screenshot inspected. Present playback and real OS/backend behavior remain unverified.

[Verification/state ledger](2026-10-22_Two_Screen_PIN_Verification.json) · [Test script](2026-10-22_Two_Screen_PIN_Test.js) · [Confirmation screenshot](2026-10-22_PIN_Confirmation_Live.png).

Figma: [Set PIN](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1650-502) → [Confirm PIN](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1709-675) → [Biometrics](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1670-1061). Stop for review; no later screen is authorized by this change.

