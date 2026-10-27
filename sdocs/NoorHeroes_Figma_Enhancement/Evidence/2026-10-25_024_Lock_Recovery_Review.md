# Screen 024 — Parent-verified Child Lock Recovery

Status: applied in Figma and ready for user review. Stop after this screen.

## Scope and references

- Figma file MR9935oQZACMjndzGIUgq5; mobile page 928:2; existing V2 section 1128:2.
- New recovery section 2207:8061; standard mobile viewport 390 × 844 only.
- Source prompt: Screen_Prompts/024_Lock_Recovery_via_verified_Parent_Profile.md; finalized reusable prompt and current V2 baseline.
- Product sources: Feature_A1_Splash_Auth_Onboarding.md; Parent Area In-App (19-26)/Feature_C19_Parent_PIN_Biometric_Gate.md; A1 KMP blueprint 08-profile-picker-child-lock-first-mission-flow.md.
- Exact reset/parent-gate copy reused from mobile core-common values/strings.xml and values/strings_restrictions.xml. Reset choices follow existing LockRecoveryScreen and ViewModel: 4-Digit PIN and No Lock.
- User approved proceeding after Screen 023 and separately approved progressive parent-recovery cooldowns.
- Figma only. No app, backend, admin, web, protected requirements, original source screens, or global NH component masters were changed.

## Applied flow

Child Lock “Ask a grown-up for help” → Parent verification → New lock → Confirm new PIN → Save New Lock → existing Profile Picker.

Parent verification uses masked 4–6-digit input, a six-digit maximum, automatic enabling from four digits, and an optional simulated device-biometric path. Child details and reset controls appear only after simulated verification. The existing deterministic app parent-PIN fixture is used solely for review; this is not production authentication or a shared credential from Parent PIN Setup.

New child PINs require exactly four digits and matching confirmation. Only explicit successful Save commits the new lock. A No Lock save clears the configured-lock flag. Successful reset clears the target child's failed attempts/cooldown. Cancellation and service errors preserve the saved lock and child attempt state. Newly saved simulation markers are used by Screen 023 PIN matching; they are opaque demo identifiers, not cryptographic credential storage.

Approved parent policy: fourth failure 30 seconds; fifth 300 seconds; sixth onward (attempts − 5) × 600 seconds. Expiry preserves failure history. Successful parent verification resets parent failures. Cancel/reopen does not clear a parent cooldown.

## Main nodes

| Role | Node |
|---|---|
| Parent verification | 2207:8134 |
| Verifying | 2207:8314 |
| New child lock | 2207:8374 |
| Confirm new PIN | 2207:8550 |
| Saving | 2207:8718 |
| Countdown A / B | 2207:8778 / 2207:8837 |
| Parent biometric simulation | 2207:8886 |
| Verified PIN review | 2209:16137 |
| Confirmation review | 2209:16352 |
| No Lock review | 2209:16556 |
| Verification-error review | 2215:9019 |
| Lockout review | 2215:9234 |
| Confirmation-mismatch review | 2215:9364 |
| Network-save-error review | 2215:9571 |

Screen 023 help controls were enabled on its five runtime frames. Its numeric keypad now compares saved simulation markers. Screen 022's default active-child tile routes to the configured lock conditionally. These are necessary flow dependencies; read-only 023 review frames were preserved.

## Reused design system

NH primary/quiet buttons (48px primary, 44px quiet), NH keypad, masked OTP/PIN cells, existing text-only chips, shared snackbar, loading dots, approved header/wordmark, shared Poppins styles, semantic palette variables and existing star/background layers. No new component family or palette was introduced. Cards hug content; long feedback remains in a bounded scrolling viewport with separate accessible actions.

## Evidence and verification

- **35/35 assertions passed against the actual Figma reaction JSON.** This evaluator simulates Figma expressions/actions; it is not a browser Present test.
- Parent input lengths 0–6, deletion, six-digit maximum, correct/incorrect parent verification and auth network failure.
- Confirmation mismatch, disabled Save, no early commit, successful PIN commit and subsequent new-PIN acceptance in Screen 023.
- Save network rollback, Cancel rollback, No Lock commit, direct-save/editor bypass prevention, child cooldown preservation and parent biometric simulation.
- Progressive 4th/5th/6th/7th failure durations, cooldown input blocking, cancel/reopen protection and history preservation at expiry.
- All 15 screen/review frames remain 390 × 844; all recovery card bounds fit within the viewport. Runtime editor bodies are intentionally hidden in an unverified canvas default. Read-only verified fixtures provide visual review.
- Final PNGs visually inspected: 2026-10-25_024_Parent_Gate.png, _New_PIN.png, _Confirm_PIN.png, _No_Lock.png. Card content fits and primary actions retain 48px height.
- Machine-readable results: 2026-10-25_024_Lock_Recovery_Checks.json.

## Limits and remaining review

- Live Present playback was blocked by saved browser permissions for figma.com. No workaround was attempted. Screenshots and reaction checks must not be described as live playback verification.
- Figma Design simulates verification, PIN input, network outcomes and biometrics; no identity, API, OS permission or production storage is involved. Do not enter actual credentials.
- To review network/API branches, set Auth outcome or Save outcome to network/error in the simulation collection; restore success for the normal path. Repeated submissions are guarded with Busy.
- Child Home/restrictions activation remains unmapped because its approved destination does not exist here. No substitute navigation was added. No Lock returns to Picker without inventing a child-home route.
- Device safe areas, keyboards, RTL/localization, 200% text scaling and OS reduced-motion playback were not verified. Only the authorized standard mobile viewport was designed.
- Await Screen 024 review before any later prompt.
