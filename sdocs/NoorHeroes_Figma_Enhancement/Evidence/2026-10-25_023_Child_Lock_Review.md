# Screen023 — Child Lock review

Figma-only update,25October2026. User approved022 and authorized023 using current app PIN/pattern/biometric/error copy. File MR9935oQZACMjndzGIUgq5, mobile page928:2, existing V2 section1128:2. No app/backend code changed.

## Created nodes

Section2194:7250 contains390×844 frames:

| Surface | ID |
|---|---|
| Runtime PIN entry |2194:7284|
| Runtime pattern tap simulation |2194:7545|
| Runtime biometric entry |2194:7727|
| Cooldown timer A |2194:7880|
| Cooldown timer B, same visual |2194:8023|
| System-prompt simulation overlay |2194:8153|
| Static Entering preview |2199:7728|
| Static Incorrect preview |2199:8017|
| Static Credential accepted preview |2199:8310|

Review-control board and notes are outside application frames. Runtime collection VariableCollectionId:2194:7251 holds count, prefix-match booleans, error/lock/accepted flags, remaining seconds, formatted countdown, method, fixture switches and selected pattern nodes. New-failure guard VariableID:2196:7728 prevents existing lockouts from being reassigned by further input.

## Reuse and presentation

Reused NH/OtpCell491:14/491:16, NH/KeypadKey494:18/494:36/494:56, NH Button322:21/322:69, NH/Snackbar1420:18 and NH/StatusBadge502:17; shared saved avatar stack, saved nickname, toolbar, star field, palette and text styles. Pattern uses a local3×3 functional grid because no NH pattern component was found; static dots are input controls, not decorative circle animations. No new color/text styles or global components were created.

Greeting uses saved child identity. All entered PIN cell properties are masked with bullets. The simulation stores count and Boolean prefix matches, not an entered PIN string. Test credentials/pattern are explicitly labelled fixtures in external review notes. Real credentials/hash verification are outside Figma.

## Flow and policy

- Configured-lock Profile Picker2189:7165 and offline configured-lock fixture2188:7787 route according to simulated configured method; an active cooldown routes to the timer instead. New unlocked-child Default Picker remains unmapped pending Child Home.
- Wrong PIN/pattern: first3 attempts retry;4th failure30seconds;5th failure5minutes per the user's explicit choice of blueprint timing over the app's2-minute fifth-tier constant. Sixth and later use existing10-minute escalation increments.
- Countdown uses two visually identical frames alternating with instant transitions and1-second After Timeout triggers. Attempts persist after cooldown expiry. Timers pause when playback leaves the timer frame; real elapsed-time/security enforcement is not provided by this simulation.
- Pattern accepts discrete taps; native Design does not capture real drawn gestures.
- Biometric request opens a sheet explicitly labelled System prompt simulation. A deliberate fingerprint tap simulates acceptance. Unavailable/cancel returns to PIN; active cooldown cannot be bypassed by simulated biometrics.
- Correct credentials set an accepted UI state. Continue remains disabled because restriction-check results and Child Home do not yet exist in V2. No child-mode context or entitlement is activated.
- Ask a grown-up remains visible but disabled until approved Screen024 provides parent-verified recovery. Parent and Add Child picker routes also await that gate. No parent-verification bypass was created.

## Evidence

Read prompt023, A1 PRD, C19 canonical access-pipeline PRD, KMP blueprint08, current ChildLock UI/ViewModel and English resources, and security constants. Inspected original1111:7445; preserved original/reference/web/admin designs.

Evaluated cached copies of actual stored action graphs:

-10000 PIN sequences: exactly the intended fixture accepted; expected result matched every sequence.
-6561 pattern tap sequences: exactly one intended fixture accepted.
-Backspace correction accepted the corrected sequence.
-Fourth/fifth failure thresholds,30/300-second expiry and preserved attempt count passed; sixth-tier600seconds passed.
-Correct PIN and biometric acceptance were blocked during cooldown; unavailable biometrics fell back to PIN.
-All8 PIN cell instances use the bullet Digit property. No4-digit plaintext credential defaults exist in the screen's collection. Keypad labels0–9 are intentionally visible.
-All9 application frames390×844. Body/footer bounds fit in inspected states.

Screenshots inspected:2026-10-25_023_Child_Lock_PIN.png, _Pattern.png, _Incorrect.png, _Biometric.png and _Cooldown.png.

Attempted live Present mode through the browser tool. It rejected opening figma.com because a saved permission/managed policy blocks that origin. No workaround was attempted. Live playback, actual OS authentication, device timing/performance, signed offline policy, restriction results, accessibility APIs, RTL/text scaling and production security were not verified. Stored-graph checks are not live execution evidence.

## Next review

Prompt023 section11 requires stopping for review before another screen. Screen024 has not been created. Approval is needed to proceed to parent verification and child-lock reset UI.
