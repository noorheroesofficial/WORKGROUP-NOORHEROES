# Screen 014 native DOB refinement

Source: user refinement request section 4; PRD A.1 FR-13 and edge cases 10–11; K-06 Add Child flow. The explicit native Android/iOS request supersedes the blueprint's older Compose Material picker instruction. No network fields or storage contracts change.

Acceptance: tapping DOB presents Android DatePickerDialog / iOS UIDatePicker; existing valid selection initializes the native control; inclusive bounds represent completed ages 3 through 17 in the user's local calendar; cancel leaves the draft untouched; confirm updates once; composition disposal dismisses the native UI without confirming or repeating callbacks. Calendar dates, leap days, birthday boundaries and initialization are covered by shared tests.

Implementation scope: shared date policy and tests, common native picker declaration, Android and iOS actual implementations. Parent agent owns screen wiring. Native device playback and iOS compilation require their respective SDK/device environments; Windows cannot establish iOS runtime verification.

## Verification evidence

- Tests added before implementation: `ChildBirthDatePolicyTest`, five tests covering birthday eligibility, inclusive native bounds, leap day, invalid civil dates, prior-value initialization/clamping.
- RED: `014_Native_DOB_RED.log` records compilation failure for missing `ChildBirthDatePolicy` and the not-yet-added `dobIso` argument (no assertion-level RED was reached because shared repository and screen wiring already referenced the pending API).
- GREEN: `014_Native_DOB_GREEN.log` reports BUILD SUCCESSFUL; the JUnit XML reports 5 tests, zero failures/errors. Android main compilation was part of this run. A subsequent cleanup replaced deprecated datetime month/day getters and is included in the parent agent's combined verification.
- Command: `JAVA_HOME=C:\Program Files\Java\jdk-21`, `gradlew.bat :feature:feature-onboarding:testAndroidHostTest --tests '*ChildBirthDatePolicyTest' --console=plain`.
- Current Windows environment's inherited JAVA_HOME points at an invalid wildcard directory; process-local override only was used. No machine configuration changed.
- iOS implementation is present but not compiled or played on a device here. Native modal confirmation, cancellation, swipe dismissal, VoiceOver, larger text and date-wheel interaction require macOS/iOS verification. Android dialog interaction likewise requires device/emulator playback; passing policy tests is not proof of native interaction.
