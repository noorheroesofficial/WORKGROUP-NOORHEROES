# Add Child refinements — implementation and verification

Date: 2026-10-22. Applies to Screen 014 only. Existing approved Splash–Registration, OTP, PIN, biometric designs and original references remain outside this refinement scope.

## Implemented in Figma

File MR9935oQZACMjndzGIUgq5 → NoorHeroes V2 Design → Onboarding → 014 — Add Child (1804:2599).

- Removed the specified centered logo from Default, Saving, Timeout and Valid Review. Retained toolbar back/wordmark. Card now y82, 366×738; same bottom-aligned 48px Save action and 14px card padding.
- Left-aligned existing heading and description, preserving approved copy and typography.
- Removed nickname sample sheet 1804:3045, custom DOB sheet 1804:3064 and year sheet 1808:3361, including inbound reactions. Editable field designs remain; these native interactions execute in the mobile app rather than fake Figma overlays.
- One shared portrait carousel component 1872:3298, instantiated in four screen states. Uses all 80 original age-wise library images, circular crops, 100px selected/72px surrounding previews, gold rings and lower-right check badges, no visible avatar names. Original image hashes match all 80 sources.
- Four review-only age fixtures demonstrate user-approved display ranges: 3–7 → 5_8, 8–9 → 8_10, 10–13 → 10_14, 14–17 → 14_18_plus. These ranges do not redefine server AgeBand enums.
- Preferred Language sheet 1804:3229 reuses reference 1174:97 rows (flags, English names, autonyms and selection checks). Taps stage a choice; Done commits; dismissal cancels. Global app locale remains separate.
- Learning artwork uses the reference's 🌱 / 🌿 / 🌳 characters. Original reference font Liberation Serif is unavailable in Figma; the new text artwork uses existing Poppins, preserving the emoji meanings. Original nodes remain untouched.
- Duplicate-name sheet now uses portrait choices rather than stale character-name buttons. Selection, comparison portrait, confirmation state and save values remain synchronized.

Main screen: https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1804-2656

Valid visual review: https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1806-3639

## Implemented in mobile

Paths below are relative to NoorHeroes/:

| Area | Files |
|---|---|
| Screen integration, editable nickname/IME, child language field | feature/feature-onboarding/src/commonMain/kotlin/com/noorheroes/feature/onboarding/ui/AddChildScreen.kt |
| Optional text-field keyboard actions/single-line configuration, existing consumer defaults preserved | core/core-ui/src/commonMain/kotlin/com/noorheroes/core/ui/component/NoorTextFields.kt |
| Native picker declaration/field | feature/feature-onboarding/src/commonMain/kotlin/com/noorheroes/feature/onboarding/ui/ChildDatePickerComponents.kt |
| Actual Android DatePickerDialog | feature/feature-onboarding/src/androidMain/kotlin/com/noorheroes/feature/onboarding/ui/ChildDatePickerDialog.android.kt |
| Actual UIKit UIDatePicker and UIKit sheet | feature/feature-onboarding/src/iosMain/kotlin/com/noorheroes/feature/onboarding/ui/ChildDatePickerDialog.ios.kt |
| Exact calendar DOB, leap-year and 3–17 bounds | feature/feature-onboarding/src/commonMain/kotlin/com/noorheroes/feature/onboarding/data/ChildBirthDatePolicy.kt |
| Lazy center-snapping/scaling, stable keys, selected semantics, reduced motion, gold ring/check | feature/feature-onboarding/src/commonMain/kotlin/com/noorheroes/feature/onboarding/ui/AvatarSelectionComponents.kt |
| Correct DOB eligibility, retained API catalog, separate approved portrait-group helper | feature/feature-onboarding/src/commonMain/kotlin/com/noorheroes/feature/onboarding/data/{AvatarCatalogRepository,AvatarPortraitCatalog}.kt |
| Staged language sheet and shared existing language rows | feature/feature-onboarding/src/commonMain/kotlin/com/noorheroes/feature/onboarding/ui/{ChildPreferredLanguageSheet,LanguageSelectionScreen}.kt |
| Eligible/default avatar selection; supported language setter and draft retention | feature/feature-onboarding/src/commonMain/kotlin/com/noorheroes/feature/onboarding/viewmodel/{AddChildViewModel,ChildPreferredLanguages}.kt |
| Backward-compatible child language draft field | feature/feature-onboarding/src/commonMain/kotlin/com/noorheroes/feature/onboarding/state/OnboardingDraftState.kt |
| Existing datetime dependency and two localized-resource keys | feature/feature-onboarding/build.gradle.kts; core/core-common/src/commonMain/composeResources/values/strings.xml |

Existing nickname text entry was retained rather than replaced. It remains limited to 30 characters, supports editing/selection and now dismisses the keyboard on Done. Opening DOB/language clears focus. DOB initializes the existing valid date, bounds dates to completed ages 3–17 and leaves the draft unchanged on cancellation. Native callbacks are one-shot and presentation is disposed safely.

Existing API DTOs, API avatar IDs, navigation destinations, global app locale and idempotency contract are unchanged. The repository's calendar calculation fixes approximate-year behavior. Eligible current avatars are retained, otherwise the first eligible existing catalog avatar is selected; invalid and repeated avatar events are ignored.

## Verification

- Final Android command: `gradlew.bat :feature:feature-onboarding:testAndroidHostTest --no-daemon`, with process-local JAVA_HOME pointing to the installed JDK21. Final build successful. JUnit totals: **309 tests, 0 failures, 0 errors, 0 skipped**.
- Includes date-policy tests, avatar boundary and DOB edge tests, avatar selection tests, language persistence/submission and backward-compatible draft tests. See 014_Refinement_Android_Final.log and the module's test-results/testAndroidHostTest XML files.
- **116/116** Figma stored-action/structure checks pass: all 80 portrait selections, one selected library, selected scale, staged language, dismissal/reopen, duplicate-name confirmation, processing, duplicate-submit prevention, offline/API recovery, no obsolete sheets, correct stage artwork and no dangling destinations. See 014_Refinement_Verification.json. These checks are not live Present playback.
- All 80 source image hashes match; all badges fit their cell bounds; one shared carousel master drives the four states. Valid layout and language-sheet screenshots visually inspected. Final saved image: 014_Refined_Valid_Draft.png.
- git diff --check passed. Existing unrelated worktree changes were preserved. No credentials, new network integrations or API-field inventions were introduced.

## Explicit remaining gaps — not production sign-off

1. **Portrait/API mapping:** user approved preserving current API IDs until mapping is approved. The eight existing API avatar IDs/artwork therefore remain in the mobile carousel. The 80 new portraits are integrated in Figma only. AvatarPortraitCatalog encodes the approved display-group boundaries but does not silently substitute portraits for unrelated API avatars. Production portrait filtering/rendering/persistence requires an approved catalog mapping.
2. **Figma capability:** native Design cannot type arbitrary names or present real Android/iOS dialogs; Code Layers are disabled on the account. The removed sample sheets are not replaced with misleading simulated native controls. Figma demonstrates portrait/language/save states through explicitly labelled review fixtures. Smooth center snapping and continuous scroll-based scaling execute in the mobile carousel; live Figma snapping is not claimed.
3. **Devices/iOS:** Android code compiled and host tests passed. adb found no connected device/emulator. Actual keyboard/dialog/carousel interactions, screen-reader/large-text behavior and device performance were not played on hardware. Windows cannot compile or run the iOS actual; macOS/Xcode verification is still required.
4. **Live Figma playback:** saved browser policy continues to prohibit figma.com browser automation. Connector writes and screenshots succeeded; no live Present verification is claimed.

No future screen or uncertain navigation destination was added. Screen 014 remains awaiting user visual review and the above runtime integration/verification work.
