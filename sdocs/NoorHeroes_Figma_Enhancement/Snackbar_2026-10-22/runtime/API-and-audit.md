# Shared mobile Snackbar runtime

The production KMP runtime lives in core-ui, shared by Android and iOS source sets. It is independent of the Figma prototype and local simulation companion.

## Usage

```kotlin
val feedback = rememberNoorSnackbarHostState()
Scaffold(snackbarHost = { NoorSnackbarHost(feedback) }) { padding ->
    // Existing feature content using padding.
}
// In the existing one-off effect collector, preserve its message:
feedback.post(effect.message, tone = SnackbarTone.Error)
```

Use NoorFeedbackOverlay(feedback) { existingContent() } when the screen has no Scaffold. A sheet hosts NoorSnackbarHost inside its own content so feedback stays above its modal surface. Use Success for confirmed success, Warning for caution and Info for informational messages. The component never infers tone from translated message text.

For a genuine caller-provided action:

```kotlin
scope.launch {
    val result = feedback.showSnackbar(
        message = existingMessage,
        actionLabel = existingActionLabel,
        tone = SnackbarTone.Error,
    )
    if (result == SnackbarResult.ActionPerformed) {
        existingAction() // invoked only here; never by the renderer or queue
    }
}
```

The renderer does not perform requests, retries or navigation. Actions default to Indefinite duration and retain explicit dismissal. No-action messages default to Short; Material SnackbarHost applies accessible timeout recommendations. Displayed/waiting identical visuals are deduplicated. Capacity is four distinct requests including visible; duplicates, blank messages and excess requests return Dismissed. This intentionally shares Material result semantics; suppression is not an action. FIFO is owned by Material. Cancellation removes visible/waiting requests and releases capacity in NonCancellable cleanup. post begins admission immediately and is tied to the composition's coroutine scope, so rapid feedback cannot block navigation collectors. Use showSnackbar when a result is needed.

Legacy NoorSnackbarHost(SnackbarHostState), NoorSnackbar(SnackbarHostState), and NoorToast(message, modifier) signatures remain available. Static NoorToast shares the new renderer; new one-off feedback should use the host so lifecycle/timeouts/deduplication apply. All current feature consumers use the bounded state.

## Visual contract

Approved source: NH/Snackbar Error master1420:18; reference1654:1726, parent audit2026-10-22. Square #1C2B33, 1dp white12% border, zero shadow, no leading icon, minimum60dp; message Poppins Regular12/18 white, action Poppins SemiBold12/18 #F4D695, dismiss18/20. Row16dp start/8end,7vertical,8gap; action/dismiss targets at least44dp. Long message/action text wrap without maxLines or fixed container height. On wide screens width is capped560dp. Horizontal margins20dp, bottom24dp plus union of safe drawing/keyboard insets; Compose consumes already handled insets. RTL uses start/end layout. Dismiss label reuses localized btn_dismiss, symbol semantics are hidden, and feedback uses a polite live region. Poppins assets and license are copied from the previously approved local review companion, not downloaded or substituted.

Error uses the approved fixed surface in both themes; Success/Info/Warning use existing design-system successSurface/infoSurface/accentSubtle and corresponding semantic action tokens. No guessed domain copy or religious content is added.

## Complete consumer audit

Baseline: evidence/audit-baseline.txt (tracked HEAD); final search: evidence/audit-after.txt. All mobile Kotlin sources were searched for SnackbarHost/Snackbar, Toast/ShowToast/ShowSnackbar, transient, messagebar and success/error message equivalents.

| Area | Consumers | Change |
| --- | --- | --- |
| Rewards family | FamilyBoardScreen, FamilyGoalDetailScreen | 2 Material hosts to shared bounded state; existing messages retained |
| Rewards missions | ArchivedChallengeScreen, SeasonalEventScreen, WeeklyChallengeDetailScreen | 3 Material hosts to shared state; explicit error effects use Error |
| Rewards store/wallet | AchievementStoreScreen, PurchaseConfirmationScreen, StoreItemDetailScreen, RewardsWalletHubScreen | 4 Material hosts to shared state; existing errors preserved |
| Bedtime audio | BedtimeAudioPlayerScreen | 1 Material host; locked/offline explanation and original copy preserved |
| Stories | StoriesLibraryScreen, StoryDetailScreen | 2 existing shared hosts migrated to bounded state; existing localized copy retained |
| Stories inert effects | DownloadsManagerScreen, FavoritesListScreen, ParentStoryInsightsScreen, StoryPlayerScreen, ApprovedShareCardPreview | 5 previously ignored ShowToast effects now display; parent sync failure uses Error; copy confirmation Success |
| Onboarding inert effects | AddChildScreen, OtpVerificationScreen, RegistrationConsentScreen | 3 previously ignored ShowToast effects now display |

Totals: 10 default Material hosts replaced, 2 existing shared hosts upgraded, 8 inert consumers wired; 20 current consumers use the shared runtime. No feature-level default Material SnackbarHost or platform Toast call remains. Share preview's existing CopyLink effect was also a no-op; it now writes its existing deepLink using common Compose clipboard before the existing success event is shown. Its API, message and parent gate remain unchanged.

Reviewed, deliberately retained:

- Inline field validation, AddChildErrorBanner, OTP error/lockout, offline/connectivity and persistent server alerts: authoritative PRD requires persistent/inline presentation; these are not transient feedback.
- XpGainToast, achievement/reward reveal, badge and celebration flows: domain-specific reward feedback, not a generic toast replacement.
- ChildProfileEffect.ShowSnackbar, SplashEvent.ShowToast and OnboardingEvent.ShowToast: declarations have no current emitted instances. No destination or feature flow was invented.
- Alternative presentation/signup/SignUpViewModel and presentation/otp/OtpVerificationViewModel ShowSnackbar(messageKey): no active UI consumer/route references those legacy classes. Existing active Registration/OtpVerificationScreen flows use the other viewmodels and are covered. Do not display raw resource keys or invent replacement routes.

No backend/admin/web files, ViewModel business/API logic, navigation contracts or protected requirement/screen files changed.
