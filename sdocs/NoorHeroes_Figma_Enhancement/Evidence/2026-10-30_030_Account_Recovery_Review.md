# Screen 030 — Forgot Access / Account Recovery review

Work began30 October2026. Figma only. Screen029 was approved with its offline-intro entry pending. Screens031–033 require later review gates.

## Review and node map

- [Recovery entry](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=2412-14013)
- V2 section2412:13979 on existing mobile page928:2 / V2 1128:2.
- Sending2412:14414; recovery OTP2412:16038; verifying2412:16508; verified fixture with server destination pending2412:16970; expired challenge2412:17443.
- Reduced entry2412:14810, sending2412:15423, OTP2412:17906, verifying2412:18519, pending boundary2412:19128.
- Shared feedback overlay2412:19744 / NH Snackbar instance2412:19752. Review-only entry/scenarios2412:19801.

## Explicit user decisions

User approved “Recover account access”, “Enter your phone number or email address to receive a verification code.” and “Continue”, with existing field/error copy. User explicitly chose **Login unchanged; review-only entry**, and **post-OTP recovery destination pending**. No Forgot access link was restored to Login.

## Sources and reuse

Read Screen_Prompts/030_Forgot_Access_Account_Recovery_Entry.md, finalized/current V2 standards, A1 PRD FR22 and recovery-start contract, KMP03 registration/consent/OTP blueprint, Backend02 authentication blueprint, AuthApiService/RecoveryStartRequestDto/TokenResponseDto and common values/strings.xml. Existing Login1355:2696 and OTP1612:1277 were inspected live. All source/protected documentation and app code were read-only.

Exact sources require enumeration-safe recovery through OTP, never a Parent-PIN bypass. Current app search found a startRecovery API interface/DTO but no dedicated Forgot Access UI/route implementation. This Figma prototype does not establish application/backend support. The token response's generic next-step values are not assumed to be an approved account-recovery destination.

No published recovery composite was found. Reuse includes approved brand/wordmark, current star field, Login curved card/method selector, NH TextField356:125 and states, OTP cells491:14/21, Primary/Quiet Button322 family, Loading329 family and Snackbar1420:18. No library primitive/color was created. Selected tab colors are bound directly to the exact existing NH foundation aliases295:25/4/8, removing inherited Login-state color bindings. Normal Login, registration, OTP/PIN and picker flows were not rewritten.

## Layout and prototype behavior

All frames remain390×844. Auth cards are366px wide at12/200, with14px padding, current asymmetric curve, content-driven height and48px actions. Default recovery card340px; normal OTP314px; expired OTP348px. Approved icon logo is retained above the card. The masked-recipient row has10px between its text slot and Change. Default/reduced modes reuse current artwork and existing Still loading phase.

- Phone/Email switch the local method state and preserve separate fictional drafts. Tapping the field autofills +12025550123 or parent@example.com, clearly labelled as fictional samples by the external review panel. This is a controlled syntax-validity fixture, not native typing, a full international phone parser or real email validation.
- Empty/invalid identifiers cannot continue. Invalid fixture uses existing inline field copy. Offline retains editable fields/draft while Continue is disabled and “Connect to the internet to continue” is shown.
- Continue guards valid/online/not-busy state. The2-second recovery-start simulation prevents duplicate activation. Success alone marks a local recovery challenge issued, clears old OTP state and opens recovery OTP. Failure and timeout use enumeration-safe shared feedback while retaining the draft. Retry is labelled as a successful retry fixture; it respects reduced motion and all send guards.
- Known/unknown-identifier review scenarios have exactly identical actions and presentation. Real server response shape/timing and account-enumeration resistance were not tested.
- OTP uses six approved cells. Six cell taps add masked demo digits; only a count/cell states are stored, not a plaintext PIN/OTP. A challenge-issued guard is required for input and verification. Additional taps beyond six cannot add digits.
- Verify enters an isolated1-second fixture, then shows incorrect-code, expired-challenge or a verified boundary. No normal Login/registration OTP success logic or Parent PIN route is reused. The verified boundary has a disabled primary action and no onward route, as approved. Back/Change invalidate the local challenge and return to the recovery draft; entry/reset and resend cannot reuse stale challenges.
- Resend is deliberately a server-available review fixture. It reuses guarded recovery sending and refreshes the masked challenge. There is no claim of a real server cooldown/TTL, SMS/email dispatch, keyboard/paste, arbitrary digit input or live OTP verification. Expiry is a selected response fixture, not a wall-clock TTL implementation.
- Feedback uses shared NH Snackbar,6-second close and explicit dismissal. No account-existence-specific failure copy, auth/session token write, Parent Area unlock, Child Home or Profile Picker navigation is added.

## Verification and limits

137/137 saved-native-reaction and structural checks passed. Coverage includes send validity/offline/busy combinations, masked count capped at six, issued-challenge/expiry/verified guards, reduced retry routing, same known/unknown actions, draft-return paths, palette/state isolation,48px actions, card containment, unchanged Login children/no Forgot access link and no navigation to PIN/account destinations. All behavior writes stay in the local030 collection. One030 section exists. See2026-10-30_030_Account_Recovery_Checks.json.

Ledger.json contains the core graph snapshot; Final_Overrides.json records final deterministic entry/scenario resets. Review fixtures were hardened after the initial snapshot so phone/email/expiry scenarios cannot carry a mismatched identifier or stale challenge. Their native returned actions and entry resets were inspected separately.

Entry, OTP and Expired PNGs were captured and visually inspected. No heading, input, icon, button or card clipping was seen in those standard-size renders. Invalid/offline state bindings and reduced-mode geometry/Still phase were structurally inspected, not separately proven by live playback. One standard size only; no device,200% text, RTL or runtime accessibility verification was performed.

**Live Present, native typing, full validation, real API/authentication, secure storage, authoritative resend/expiry timing and the server recovery next step remain unverified/pending.** This is an editable Figma prototype, not production account recovery. No code changes were made. Screen029's offline-intro entry remains pending by explicit approval.

## Required review gate

Screen030 §11: “Stop and wait for my review and approval before moving to another screen.” Await approval before031 Terms of Service full document. Screens031–033 remain unbuilt.
