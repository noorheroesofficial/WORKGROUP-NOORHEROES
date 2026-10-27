# Phase 3 — core-notifications: Real FCM/APNs Platform Bindings (Gap Closure)

**Blueprint ID:** `Development_Blueprints.Phase3_Shared_Core_Modules.KMP.20-core-notifications-fcm-apns-production-binding`
**Platform:** KMP (`core-notifications` module, Android `androidMain` + iOS `iosMain` actuals)
**Phase:** Phase 3 — Shared Core Modules
**Closes:** `core-notifications` is 🟡 **COMPLETED (partial)** — the `NotificationHandler` abstraction, `NoOpNotificationHandler`, and the common/platform Koin module skeleton (`notificationsModule`, `androidNotificationsModule`, `iosNotificationsModule`) are built and in production use, but `CORE_NOTIFICATIONS_INSTRUCTIONS.md` §7 itself documents the platform bindings only as **"intended to bind"** — no concrete FCM/APNs implementation exists behind the interface today. Every `getPushToken()` call in production currently returns `null` forever (the `NoOpNotificationHandler` contract), and every `onNotificationReceived()` call never fires, because no real push message is ever received.
**Depends on:**
- `core-network` (already built) — referenced, not directly consumed by this document's own new code (see §2.2 and §12.1 for the precise, evidence-based boundary of that dependency).
- `core-datastore` (already built) — this document adds one new specialized domain store (`PushTokenStore`) to it, following the exact pattern `CORE_DATASTORE_INSTRUCTIONS.md` §5 already establishes for `FamilyTimezoneStore`/`ClockSkewStore`.
**Also cross-references (do not re-implement):**
- `Development_Blueprints/B17_Notifications_Child_Facing/Backend/01-device-profile-binding-service.md` (B-01) — already implements `POST /v1/devices` and `PATCH /v1/devices/{id}/active-profile`. This document produces the `fcm_token` value B-01 consumes; it does not re-specify B-01's endpoints, schema, or atomicity guarantee.
- `Development_Blueprints/B17_Notifications_Child_Facing/Backend/05-delivery-adapter-push-token-lifecycle.md` (B-05) — already implements the server-side Firebase Admin SDK send, retry, and token-invalid/rotated lifecycle bookkeeping. This document is the send's *receiving end* on-device; it does not re-implement server-side delivery, retry, or lifecycle bookkeeping.
- `Development_Blueprints/B17_Notifications_Child_Facing/Backend/03-notification-policy-engine-send-time-evaluation.md` (B-03) — already implements quiet-hours/bedtime, frequency-budget, consent, and active-binding re-checks **at actual send time, server-side**, reading `screen_time_policies` (owned by C.23). This document does not implement any client-side quiet-hours logic — see §9.4 for why that would be actively wrong to add.
- `Development_Blueprints/B17_Notifications_Child_Facing/KMP/01-device-binding-lifecycle-integration.md` (K-01) — already implements `DeviceBindingManager`/`DeviceBindingRepository`, which call `NotificationHandler.getPushToken()` and register/re-register the token with B-01's endpoints, including the offline-queue-and-retry-with-backoff behavior. This document does not re-implement token registration, profile-switch binding, or retry/backoff — it only guarantees `getPushToken()` returns a real, current value for K-01 to consume.
- `Development_Blueprints/B17_Notifications_Child_Facing/KMP/02-deep-link-resolution-navigation-interception.md` (K-02) — already implements `DeepLinkResolutionHandler`, which intercepts every notification-tap intent and calls `GET /v1/notifications/resolve` before any navigation. This document's job is to ensure a tapped system notification actually reaches K-02's existing interception point carrying the `deep_link_token` — not to re-implement resolution or navigation routing.
- `Development_Blueprints/B17_Notifications_Child_Facing/Backend/04-child-safe-template-governance-rendering.md` (B-04) — already validates every child-facing notification body against `ChildSafetyBlocklistValidator` before it is ever sent. This document never generates, mutates, or re-assembles notification copy client-side; it renders exactly what B-05 sends, verbatim (§9.3).
- `Development_Blueprints/C23_Parental_Controls/KMP/03-quiet-hours-bedtime-settings.md` (C.23 K-03) — already implements the parent-facing quiet-hours/bedtime *configuration* UI, writing to `screen_time_policies`, which B-03 reads at send time. This document does not touch quiet-hours configuration; it only guarantees that the delivery pipeline B-03 gates is the *real* pipeline (§9.4).
**Consumers of the outcome:** B17 K-01 `DeviceBindingManager` (the direct, immediate consumer of `getPushToken()`'s now-real return value); B17 K-02 `DeepLinkResolutionHandler` (the consumer of a correctly-constructed, correctly-tapped system notification); C.25 KMP-01 Notifications Inbox / KMP-02 Notification Preferences Safety-Critical Channel Selector (parent-facing consumers that reuse this exact shared delivery architecture per that feature's own PRD FR-11/§96, cited in full in §12.4).
**Status of underlying code:** `NotificationHandler` interface: complete, stable, **do not change its contract** — every existing consumer keeps compiling unmodified. `NoOpNotificationHandler`: complete, stable, **kept and still bound for local/debug builds** (§18 point 1). The concrete FCM/APNs bindings behind the interface: **do not exist; this document specifies and implements them in full.**

---

## 1. Objective and purpose

`CORE_NOTIFICATIONS_INSTRUCTIONS.md` §7 states, as a plain fact about the current codebase:

> **Android**: `androidNotificationsModule` is intended to bind `NotificationHandler` to an FCM-based implementation.
> **iOS**: `iosNotificationsModule` is intended to bind `NotificationHandler` to an APNs-based implementation.

The word "intended" is the entire finding this document acts on: the abstraction, the DI seams, and every downstream consumer of that abstraction have already been built *as if* the binding existed — B17 K-01's own text states plainly, "Firebase issues one token per app installation, not per child," and K-01's `DeviceBindingManager` is written entirely around `NotificationHandler.getPushToken()` returning a real value. But nothing in the corpus, and nothing in `core-notifications`'s package structure (`com.noorheroes.core.notifications.handler` / `.di`, per §3 of that same document), ever names a concrete class that talks to `FirebaseMessaging` or `UNUserNotificationCenter`. The only concrete `NotificationHandler` implementation the corpus documents is `NoOpNotificationHandler` — "a safe, do-nothing implementation" whose `getPushToken()` returns `null` and whose `onNotificationReceived()` does nothing, by design, so the app can run without configuring Firebase or APNs locally (§9 Scenario 3 of that document).

**The consequence in today's build, stated plainly:** every code path downstream of `NotificationHandler` is fully built and waiting for input that never arrives. K-01's `DeviceBindingManager.switchActiveProfile()` runs on every profile switch exactly as designed, calls `getPushToken()`, receives `null`, and — per K-01 §18's own error table, which already anticipates a `null`/failure token — has nothing valid to register with B-01's `POST /v1/devices`. B-05's `DeliveryAdapter` on the backend is fully implemented and ready to call the Firebase Admin SDK, but has no real, live token to send to, for any installation, ever. B17's entire notification feature — device binding, policy evaluation, template rendering, delivery, deep-link resolution — is complete and correct end-to-end **except for the one seam this document closes**: a real device producing a real token and receiving a real push.

This document's objective is narrow and precise, in the same spirit as this project's other Phase-3 gap-closure documents: **implement the two concrete `NotificationHandler` actuals** — `FcmNotificationHandler` (`androidMain`, backed by the Firebase Cloud Messaging SDK) and `ApnsNotificationHandler` (`iosMain`, backed by `UNUserNotificationCenter` + APNs device-token registration, bridged into Firebase Messaging so the token shape the backend already expects — a single `fcm_token` string, per B-01 §13's request schema — is what both platforms produce) — bind them in place of `NoOpNotificationHandler` for non-debug build variants, and correctly wire the platform-level notification-received and notification-tap paths into the already-built `onNotificationReceived()` delegate and K-02's already-built deep-link interception point. Nothing downstream of `NotificationHandler` is redesigned, extended, or reinterpreted; this document makes the interface's existing contract true in production for the first time.

**Explicitly not the objective:** rewriting `NotificationHandler`'s signature, reimplementing K-01's token-registration/retry logic, reimplementing K-02's deep-link resolution, reimplementing B-03's quiet-hours policy evaluation, or writing any new backend endpoint. Every existing call site of `NotificationHandler.getPushToken()` / `.onNotificationReceived()` continues to compile and behave identically to how its own specification already assumes it behaves — because by the time this document's code runs, the interface simply returns real values instead of `null`/never-firing ones, the exact same input shape every downstream consumer was already written against.

---

## 2. Scope and requirements

### 2.1 In scope

- **Android**: `FcmNotificationHandler` (concrete `NotificationHandler` actual, Firebase Cloud Messaging SDK), `NoorFirebaseMessagingService` (a `FirebaseMessagingService` subclass — the OS-instantiated bridge that receives `onNewToken`/`onMessageReceived` callbacks and delegates into shared code), `AndroidNotificationPermissionController` (Android 13+ `POST_NOTIFICATIONS` runtime permission), `SystemNotificationBuilder` (constructs the visible system-tray notification with a `PendingIntent` that carries the `deep_link_token` into `:core:navigation`'s existing notification-tap entry point, which K-02 already intercepts).
- **iOS**: `ApnsNotificationHandler` (concrete `NotificationHandler` actual — captures the raw APNs device token via `UIApplicationDelegate`/`UNUserNotificationCenter` registration, bridges it into Firebase Messaging to obtain the FCM token, per the reasoning in §3.5), `NoorNotificationCenterDelegate` (`UNUserNotificationCenterDelegate` implementation — foreground presentation options, tap handling, deep-link forwarding), `IosNotificationPermissionController` (`UNUserNotificationCenter.requestAuthorization` wiring).
- **Common (`commonMain`)**: `NotificationPermissionController` — a new, small, additive interface (§6.2) alongside `NotificationHandler`, deliberately **not** a change to `NotificationHandler` itself (§2.2). `PushTokenStore` — a new `core-datastore` specialized domain store caching the most recently issued token value (§8), purely a local-caching concern internal to the platform actuals, distinct from and not a duplicate of K-01's own separate pending-binding-update-queue cache.
- **DI**: extending `notificationsModule` (common), `androidNotificationsModule`, `iosNotificationsModule` to bind the new concrete classes, gated by build variant so `NoOpNotificationHandler` remains the bound implementation for local/debug builds (§5, §13).
- **Configuration/provisioning**: Firebase project setup, `google-services.json` / `GoogleService-Info.plist`, APNs Auth Key upload to the Firebase console, Android Gradle plugin wiring, iOS `Info.plist`/entitlements/CocoaPods wiring (§7).
- **Correcting `CORE_NOTIFICATIONS_INSTRUCTIONS.md` §7**, whose "intended to bind" phrasing is itself part of why this gap was easy to leave unnoticed as a documented-but-unbuilt seam rather than a flagged defect (mirroring the documentation-as-contributing-cause pattern this project's other Phase-3 gap-closure documents already establish for `core-security`).

### 2.2 Explicitly out of scope

- **B-01's device-registration/binding-switch endpoints and their schema** (`POST /v1/devices`, `PATCH /v1/devices/{id}/active-profile`) — already fully specified and, per this document's framing, already implemented. This document produces the `fcm_token` string those endpoints consume; it does not touch their contract, their atomicity guarantee, or their database schema.
- **K-01's `DeviceBindingManager`/`DeviceBindingRepository`** — already implements the call into B-01, the offline-queue-and-retry-with-backoff behavior (K-01 §18/§19/Task 04), and the per-profile-switch binding update. This document's `PushTokenStore` is a *different* cache from K-01's *own* separately-specified "pending binding-update queue persisted via `:core:datastore`" (K-01 §14/§20) — the two must not be merged or confused; see §8.3 for the exact boundary.
- **B-03's Policy Engine** (quiet hours/bedtime, frequency budget, consent, age/locale eligibility, active-binding re-check, all evaluated server-side at actual send time) and **C.23 K-03's quiet-hours configuration UI** — this document implements zero client-side notification-suppression logic of any kind. See §9.4 for the explicit reasoning on why that boundary is correct, not merely convenient.
- **K-02's `DeepLinkResolutionHandler`** and B-06's `GET /v1/notifications/resolve` — already implements the full re-validation-on-open flow. This document's job stops at "the tapped system notification correctly reaches `:core:navigation`'s existing entry point carrying `deep_link_token`" — everything after that point is K-02's already-built territory.
- **B-04's template rendering / `ChildSafetyBlocklistValidator` content governance** — this document never constructs, mutates, or re-assembles notification title/body text from raw payload fields; it renders exactly the pre-rendered `title`/`body` strings B-05 sends, verbatim (§9.3).
- **Local (non-push) notification scheduling** — `CORE_NOTIFICATIONS_INSTRUCTIONS.md` §1 itself explicitly scopes this out of `core-notifications` ("Do not use this for local notifications (e.g., alarms, reminders). Use a dedicated local notification utility if available."). This document is exclusively about *remote push* delivery via FCM/APNs; it introduces no alarm/reminder-scheduling capability.
- **Any new backend endpoint, schema, or service.** This document is 100% client-side (`core-notifications` module only); zero backend files are created or modified.
- **Huawei Mobile Services (HMS) Push Kit or any non-Google Android push channel.** Devices without Google Play Services cannot receive FCM push under this document's implementation — documented as a known, accepted limitation in §15, not silently ignored.

### 2.3 Non-functional requirements carried forward from the source corpus

- **"Never access `FirebaseMessaging`/`UNUserNotificationCenter` directly from shared code"** — a hard rule stated twice in the existing corpus (`CORE_NOTIFICATIONS_INSTRUCTIONS.md` §7's "Do Not," restated verbatim by K-01 §6: "do not access `FirebaseMessaging`/`UNUserNotificationCenter` directly from shared code"). Every line of code this document adds that touches a platform SDK type lives in `androidMain`/`iosMain`; `commonMain` interacts only through `NotificationHandler` and the new `NotificationPermissionController`.
- **Interface stability** — `NotificationHandler`'s two methods (`getPushToken()`, `onNotificationReceived(payload)`) keep their exact signatures; K-01 and K-02 require zero source changes to keep compiling and functioning.
- **"if denied, the child simply doesn't receive push notifications; in-app banner-style notifications (FR-13) remain unaffected... No special in-app re-prompt nagging beyond the platform-standard one-time OS re-prompt affordance"** — B.17 PRD §1.15's explicit, binding statement of the required permission-denied UX. This document's permission-request implementation must not add custom nagging/priming flows beyond the platform-standard prompt (§9.5, §10).
- **"Firebase issues one token per app installation, not per child"** (K-01 §1/B-01 §5 FR-8) — the token this document produces is installation-scoped, never child-scoped; per-profile targeting remains entirely B-01's active-binding responsibility, not something this document's token-production logic participates in.

---

## 3. Technical implementation details

### 3.1 The core design question this document resolves: does `getPushToken()` stay pull-based?

`NotificationHandler.getPushToken()` is documented as a `suspend fun ... : String?` — a one-shot pull, not a `Flow`. But FCM tokens are **not** static: the OS/SDK can rotate a token at any time for reasons outside the app's control (Play Services data reset, security-related rotation, app restore to a new device, APNs re-registration on iOS). K-01 §11/§18 already documents "Handle token refresh/rotation from the OS; re-register via `POST /v1/devices` on rotation" as one of `DeviceBindingManager`'s own existing responsibilities — which means K-01 was already written assuming *some* mechanism surfaces a rotated token to it, and the only mechanism K-01's code is documented to use is `NotificationHandler.getPushToken()` itself (K-01 §6: "Token retrieval uses the existing `NotificationHandler.getPushToken()` suspend function").

**The two candidate designs, both evaluated:**

- **Candidate A — add a token-changed event stream to the interface** (e.g., a new `SharedFlow<String>` on `NotificationHandler`, or a callback parameter). **Rejected.** This is a signature change to the one interface this document is explicitly required to leave untouched (task framing; §2.2), and — more importantly — it is unnecessary, because Candidate B fully satisfies K-01's already-documented behavior with zero interface change.
- **Candidate B — keep `getPushToken()` pull-based; the platform actual internally caches the most recently issued token, updated on every `onNewToken`/registration-token-refresh callback, so any caller polling `getPushToken()` at any time observes the freshest value.** **Adopted.** K-01's already-written rotation-handling logic (re-register on a value change it detects) works correctly against this design with **zero modification to K-01's code** — it already calls `getPushToken()` at the lifecycle points its own spec documents (app start, token refresh, every profile switch); this document's job is only to guarantee that call always returns the current, live value rather than a stale one.

This is the single most important design decision in this document, and every subsequent section builds on it: **`FcmNotificationHandler`/`ApnsNotificationHandler` are the sole owners of "what is the current token"; `getPushToken()` is a fast, cache-backed read that is refreshed asynchronously by the OS-driven callback, never a slow path that blocks on a fresh network round-trip unless no cached value exists yet.**

### 3.2 Android — Firebase Cloud Messaging

**Dependency:** `com.google.firebase:firebase-messaging-ktx` (via the Firebase BoM, `com.google.firebase:firebase-bom`), applied through the `com.google.gms.google-services` Gradle plugin, which reads `google-services.json` at build time (§7.1).

**Token retrieval** — `FirebaseMessaging.getInstance().token` returns a Google Play Services `Task<String>`; converted to a suspend call via `kotlinx-coroutines-play-services`'s `Task<T>.await()`:

```kotlin
// androidMain
package com.noorheroes.core.notifications.handler

import com.google.firebase.messaging.FirebaseMessaging
import kotlinx.coroutines.tasks.await
import java.io.IOException

internal class FcmNotificationHandler(
    private val tokenStore: PushTokenStore,
    private val logger: NoorHeroesLogger,
) : NotificationHandler {

    override suspend fun getPushToken(): String? {
        // Fast path: a cached value (kept fresh by onNewToken, §3.4) avoids an
        // unnecessary round-trip to Play Services on every call — this is the
        // mechanism that makes §3.1 Candidate B correct in practice, not just in theory.
        tokenStore.currentToken()?.let { return it }

        return try {
            val token = FirebaseMessaging.getInstance().token.await()
            tokenStore.saveToken(token)
            token
        } catch (e: Exception) {
            // Play Services missing/outdated surfaces here as an IOException-family
            // exception, exactly as CORE_NOTIFICATIONS_INSTRUCTIONS.md §5 already
            // documents as the expected Android failure mode. Never swallowed —
            // logged, then rethrown, per that document's §10 "Don't swallow
            // exceptions during token retrieval without logging."
            logger.warn("FcmNotificationHandler.getPushToken failed", e)
            throw e
        }
    }

    override fun onNotificationReceived(payload: Map<String, String>) {
        // Base contract per CORE_NOTIFICATIONS_INSTRUCTIONS.md §4: no-op by default in
        // the common definition; this actual's job is only to guarantee this method is
        // actually invoked with the real payload (§3.4) — any feature-layer decoration
        // of behavior here belongs to whatever module already overrides/decorates it,
        // per that document's own package-boundary rule (§1 "What should NOT be added").
    }
}
```

**Note on `IOException` specifically:** if Google Play Services is missing, disabled, or requires an update, `FirebaseMessaging.getInstance().token` fails with `IOException("MISSING_INSTANCEID_SERVICE")` (or a comparable Play-Services-unavailable error depending on SDK version) — this is the exact scenario `CORE_NOTIFICATIONS_INSTRUCTIONS.md` §5 already documents by name ("e.g., `IOException` on Android if Play Services are missing"). This document's implementation does not attempt to work around it (no HMS Push Kit fallback — §2.2, §15); it surfaces the exception faithfully so K-01's existing `try`/`catch` around `getPushToken()` degrades correctly (device stays unregistered for push; B.17 PRD §1.15's documented fallback — in-app banner notifications — remains unaffected, since that path never depends on `NotificationHandler` at all).

### 3.3 Android — receiving messages and constructing the system notification

```kotlin
// androidMain
package com.noorheroes.core.notifications.service

import android.app.NotificationManager
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import com.noorheroes.core.notifications.handler.NotificationHandler
import com.noorheroes.core.notifications.handler.PushTokenStore
import com.noorheroes.core.notifications.notify.SystemNotificationBuilder
import org.koin.android.ext.android.inject

/**
 * OS-instantiated bridge. FirebaseMessagingService is created by the Android system, not by
 * Koin's constructor injection — dependencies are resolved via KoinComponent field injection,
 * the standard pattern for system-instantiated Android components in a Koin-based app.
 */
internal class NoorFirebaseMessagingService : FirebaseMessagingService() {

    private val notificationHandler: NotificationHandler by inject()
    private val tokenStore: PushTokenStore by inject()
    private val notificationBuilder: SystemNotificationBuilder by inject()

    override fun onNewToken(token: String) {
        // This is the callback that makes §3.1's "cache stays fresh" design correct:
        // every rotation the OS/SDK issues lands here, and PushTokenStore is updated
        // before any subsequent getPushToken() call — no interface change required for
        // K-01's already-documented rotation handling to keep working correctly.
        tokenStore.saveToken(token)
    }

    override fun onMessageReceived(message: RemoteMessage) {
        // Delegate the raw data payload to the shared, already-built contract exactly as
        // CORE_NOTIFICATIONS_INSTRUCTIONS.md §4 documents: "onNotificationReceived(payload)".
        notificationHandler.onNotificationReceived(message.data)

        // The backend (B-05) sends a data-only FCM message (no "notification" block) —
        // see §3.5 for why this is the correct, deliberate choice for this platform —
        // so the client is fully responsible for constructing the visible system-tray
        // notification itself, in every app state (foreground/background/killed-but-
        // process-started-by-FCM). This is what makes K-02's "no notification-tap path
        // bypasses server-side deep-link resolution" guarantee (K-02 §25) achievable:
        // the client controls 100% of the PendingIntent, so there is no OS-auto-displayed
        // notification whose tap target this module doesn't fully own.
        val title = message.data["title"].orEmpty()
        val body = message.data["body"].orEmpty()
        val deepLinkToken = message.data["deep_link_token"]
        notificationBuilder.show(title = title, body = body, deepLinkToken = deepLinkToken)
    }
}
```

```kotlin
// androidMain
package com.noorheroes.core.notifications.notify

import android.app.PendingIntent
import android.content.Intent
import android.net.Uri
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat

internal class SystemNotificationBuilder(
    private val context: android.content.Context,
) {
    fun show(title: String, body: String, deepLinkToken: String?) {
        // The deep-link URI scheme/host is whatever :core:navigation's existing
        // notification-tap entry point already expects (K-02 §9 "Files to Modify:
        // :core:navigation's intent-handling entry point") — confirm the exact scheme
        // during Task 13.2 rather than assuming; represented here as noorheroes://notification.
        val deepLinkUri = Uri.parse("noorheroes://notification").buildUpon()
            .apply { deepLinkToken?.let { appendQueryParameter("deep_link_token", it) } }
            .build()
        val intent = Intent(Intent.ACTION_VIEW, deepLinkUri).apply {
            setPackage(context.packageName)
        }
        val pendingIntent = PendingIntent.getActivity(
            context, deepLinkToken?.hashCode() ?: 0, intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE,
        )
        val notification = NotificationCompat.Builder(context, DEFAULT_CHANNEL_ID)
            .setContentTitle(title)          // rendered verbatim — never re-composed (§9.3)
            .setContentText(body)            // rendered verbatim — never re-composed (§9.3)
            .setSmallIcon(com.noorheroes.core.designsystem.R.drawable.ic_notification) // confirm exact resource during Task 13.3
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .build()
        NotificationManagerCompat.from(context).notify(deepLinkToken?.hashCode() ?: 0, notification)
    }

    companion object {
        const val DEFAULT_CHANNEL_ID = "noorheroes_default"
    }
}
```

### 3.4 Android — `POST_NOTIFICATIONS` runtime permission (API 33+)

```kotlin
// androidMain
package com.noorheroes.core.notifications.permission

internal class AndroidNotificationPermissionController(
    private val context: android.content.Context,
) : NotificationPermissionController {

    override fun currentPermissionState(): NotificationPermissionState {
        if (android.os.Build.VERSION.SDK_INT < android.os.Build.VERSION_CODES.TIRAMISU) {
            // Below API 33, POST_NOTIFICATIONS does not exist as a runtime permission;
            // notifications are permitted by default at install time.
            return NotificationPermissionState.Granted
        }
        val granted = androidx.core.content.ContextCompat.checkSelfPermission(
            context, android.Manifest.permission.POST_NOTIFICATIONS,
        ) == android.content.pm.PackageManager.PERMISSION_GRANTED
        return if (granted) NotificationPermissionState.Granted else NotificationPermissionState.Denied
    }

    // Actual request must be launched from an Activity via
    // rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) in the
    // Compose feature layer that owns the permission-priming moment (per B.17 PRD §1.15, no
    // custom priming screen is mandated — the platform-standard one-time system prompt is
    // sufficient). This controller exposes currentPermissionState() for that feature layer to
    // read before/after the OS dialog; it does not itself own an Activity reference (Context-leak
    // avoidance, per CORE_NOTIFICATIONS_INSTRUCTIONS.md §8's existing "no raw platform Context
    // into the common handler interface" rule, applied here to this new controller too).
}
```

### 3.5 iOS — APNs via `UNUserNotificationCenter`, bridged into Firebase Messaging

**The decision this section resolves, stated and justified explicitly:** does iOS register directly with raw APNs and send a *raw APNs device token* to the backend, or does it bridge that token into Firebase Messaging and send an *FCM token*? The evidence in the corpus settles this unambiguously:

- B-01 §13's request schema for `POST /v1/devices` is `{ "fcm_token": "string", ... }` — a single field name, used uniformly, with no separate `apns_token` field or platform discriminator anywhere in that contract.
- B-05 §26's Library Requirements list **"Firebase Admin SDK (FCM)"** as the sole server-side send mechanism — the backend never calls Apple's APNs HTTP/2 API directly.
- K-01 §1 states, platform-agnostically, "Firebase issues one token per app installation" — not "Firebase on Android, raw APNs on iOS."

**Conclusion: iOS must produce an FCM token, obtained by handing the raw APNs device token to the Firebase Messaging SDK.** This is Apple's and Google's own standard, documented integration pattern for exactly this reason (a single backend integration surface for both platforms) — not a deviation this document is inventing. The `UNUserNotificationCenter` work (permission authorization, foreground presentation, tap handling) is real APNs-facing work this document owns; the token that ultimately reaches the backend is the FCM token Firebase Messaging derives from the raw APNs token, per B-01/B-05's existing, fixed contract.

```kotlin
// iosMain
package com.noorheroes.core.notifications.handler

import kotlinx.coroutines.suspendCancellableCoroutine
import platform.UserNotifications.*
import kotlin.coroutines.resume

internal class ApnsNotificationHandler(
    private val tokenStore: PushTokenStore,
    private val logger: NoorHeroesLogger,
) : NotificationHandler {

    override suspend fun getPushToken(): String? {
        tokenStore.currentToken()?.let { return it }

        // The FCM token is vended asynchronously by the Firebase Messaging iOS SDK only after:
        //   1. UIApplication.registerForRemoteNotifications() has been called (typically from
        //      IosNotificationPermissionController.requestPermission(), §3.6), and
        //   2. the app's UIApplicationDelegate has received the raw APNs device token via
        //      application(_:didRegisterForRemoteNotificationsWithDeviceToken:) and forwarded it
        //      to Messaging.messaging().apnsToken = deviceToken (native-side bridge — see the
        //      Swift-shim note below).
        // If registration hasn't completed yet (e.g., called before permission was granted, or
        // before the app has been backgrounded/foregrounded once post-registration on some SDK
        // versions), this returns null — the exact, already-documented "null = try again later"
        // contract from CORE_NOTIFICATIONS_INSTRUCTIONS.md §5, no different in kind from Android's.
        return suspendCancellableCoroutine { continuation ->
            // Native-side call into the Firebase Messaging SDK's token-fetch API (via the Swift
            // interop shim — §3.5.1). Resolves with the FCM token, or null/error if APNs
            // registration has not yet completed or authorization was denied.
            fetchFcmTokenNative { token, error ->
                if (error != null) {
                    logger.warn("ApnsNotificationHandler.getPushToken failed", error)
                }
                token?.let { tokenStore.saveToken(it) }
                if (continuation.isActive) continuation.resume(token)
            }
        }
    }

    override fun onNotificationReceived(payload: Map<String, String>) {
        // Same no-op base contract as the Android actual (§3.2) — decoration happens upstream.
    }
}
```

#### 3.5.1 Why a small Swift interop shim, not direct Kotlin/Native cinterop, for the delegate-based APIs

Kotlin/Native can call Objective-C frameworks (including Firebase's iOS SDK, which is Objective-C-based) directly via CocoaPods cinterop for straightforward method calls. But `UNUserNotificationCenterDelegate` and Firebase's `MessagingDelegate` are **delegate protocols** with several optional callback methods, invoked by the OS/SDK at arbitrary times — implementing an Objective-C protocol conformance ergonomically from Kotlin/Native is possible but is meaningfully more awkward than in native Swift, and this exact class of problem is why this project's own `core-security` gap-closure document (Phase3.17, §7) flags iOS cinterop specifics as "confirm during implementation, do not assume" rather than prescribing a single fixed approach. **This document's recommendation, to be confirmed during Task 13.2 against the project's actual iOS app-target structure:** implement `NoorNotificationCenterDelegate` (conforms to `UNUserNotificationCenterDelegate`) and the `MessagingDelegate` conformance as a small native Swift file inside the iOS app target (not inside the KMP shared framework's Kotlin source), which then calls into the shared Kotlin framework's exposed `expect`/`actual` entry points (`ApnsNotificationHandler`'s token-set callback, and `:core:navigation`'s existing notification-tap entry point) via the auto-generated Objective-C header the Kotlin/Native framework already produces for consumption by Swift. This is the standard, lowest-friction pattern for KMP apps needing native iOS delegate integration, and it does not violate the "no `UNUserNotificationCenter` access from shared code" rule (§2.3) — the Swift shim lives in the iOS app target, calling *into* shared code through the shared framework's own public Kotlin API, exactly the same directional relationship Android's `NoorFirebaseMessagingService` already has (a platform-owned OS-instantiated class calling into shared `commonMain` interfaces).

### 3.6 iOS — notification permission

```kotlin
// iosMain
package com.noorheroes.core.notifications.permission

import kotlinx.coroutines.suspendCancellableCoroutine
import platform.UserNotifications.*
import kotlin.coroutines.resume

internal class IosNotificationPermissionController : NotificationPermissionController {

    override suspend fun requestPermission(): NotificationPermissionState =
        suspendCancellableCoroutine { continuation ->
            UNUserNotificationCenter.currentNotificationCenter().requestAuthorizationWithOptions(
                options = UNAuthorizationOptionAlert or UNAuthorizationOptionBadge or UNAuthorizationOptionSound,
            ) { granted, _ ->
                if (granted) {
                    // registerForRemoteNotifications() must be called on the main thread from the
                    // native (Swift/AppDelegate) side after authorization is granted — this is the
                    // step that eventually produces the raw APNs device token consumed by §3.5.
                    triggerRemoteRegistrationNative()
                }
                if (continuation.isActive) {
                    continuation.resume(
                        if (granted) NotificationPermissionState.Granted else NotificationPermissionState.Denied,
                    )
                }
            }
        }

    override fun currentPermissionState(): NotificationPermissionState {
        // Synchronous read of UNUserNotificationCenter's current settings; implementation detail
        // left to Task 13.4 (the underlying API — getNotificationSettingsWithCompletionHandler —
        // is itself asynchronous on iOS, so this method's "synchronous" framing may need to become
        // a cached-last-known-value read rather than a true synchronous OS call; resolve during
        // implementation against NotificationPermissionController's exact common-side contract, §6.2).
    }
}
```

---

## 4. Architecture and component responsibilities

```
Feature Layer (B17 K-01 DeviceBindingManager, K-02 DeepLinkResolutionHandler,
               C.25 KMP-01/02 parent notification screens, onboarding permission-priming UI)
    ↓ calls (UNCHANGED)
NotificationHandler (interface, com.noorheroes.core.notifications.handler) — UNCHANGED CONTRACT
NotificationPermissionController (interface, NEW — additive, separate from NotificationHandler)
    ↓ implemented by (THIS DOCUMENT'S DELIVERABLE)
┌─────────────────────────────┬──────────────────────────────┐
│ FcmNotificationHandler        │ ApnsNotificationHandler        │
│ (androidMain)                 │ (iosMain)                      │
│ AndroidNotificationPermission-│ IosNotificationPermission-     │
│ Controller                    │ Controller                     │
└─────────────────────────────┴──────────────────────────────┘
    ↓ delegates platform SDK calls to
[AndroidMain: FirebaseMessaging SDK, NoorFirebaseMessagingService,
              SystemNotificationBuilder (NotificationCompat)]
[IosMain: UNUserNotificationCenter, NoorNotificationCenterDelegate (Swift shim),
          Firebase Messaging iOS SDK (bridged from raw APNs device token)]
    ↓ token cache reuses (NEW, this document, but architecturally identical to
      the existing FamilyTimezoneStore/ClockSkewStore pattern)
PushTokenStore (core-datastore, com.noorheroes.core.notifications.handler)
    ↓ consumed by (EXISTING, UNCHANGED)
DeviceBindingManager / DeviceBindingRepository (B17 K-01)
    ↓ POST /v1/devices, PATCH /v1/devices/{id}/active-profile (EXISTING, UNCHANGED)
DeviceBindingService (B17 B-01, backend)
```

**Component responsibilities introduced or changed by this document:**

| Component | Responsibility | New or changed? |
|---|---|---|
| `NotificationHandler` (interface) | `getPushToken()`, `onNotificationReceived(payload)` | **Unchanged** — contract stability is a hard requirement (§2.2, §18). |
| `FcmNotificationHandler` | Concrete Android `NotificationHandler`, Firebase Messaging SDK-backed, cache-first `getPushToken()` (§3.1–§3.2). | **New** — replaces the `NoOpNotificationHandler` binding for non-debug Android build variants. |
| `ApnsNotificationHandler` | Concrete iOS `NotificationHandler`, APNs-registration-then-Firebase-Messaging-bridged (§3.5). | **New** — replaces the `NoOpNotificationHandler` binding for non-debug iOS build variants. |
| `NoorFirebaseMessagingService` | OS-instantiated `FirebaseMessagingService` bridge: `onNewToken` → `PushTokenStore`; `onMessageReceived` → `NotificationHandler.onNotificationReceived()` + `SystemNotificationBuilder`. | **New.** |
| `NoorNotificationCenterDelegate` (Swift shim, iOS app target) | `UNUserNotificationCenterDelegate`/`MessagingDelegate` conformance; forwards token updates and tap events into the shared Kotlin framework's public API. | **New**, lives outside `core-notifications`'s Kotlin sources (§3.5.1). |
| `SystemNotificationBuilder` | Constructs the visible Android system-tray notification and its tap `PendingIntent` carrying `deep_link_token` into `:core:navigation`. | **New.** |
| `NotificationPermissionController` (interface) + platform actuals + `NoOpNotificationPermissionController` | Requests/reads OS notification-authorization state. | **New**, additive — not a change to `NotificationHandler`. |
| `PushTokenStore` | `core-datastore`-backed cache of the current token value; the mechanism that makes §3.1's pull-based design correct. | **New.** |
| `notificationsModule` / `androidNotificationsModule` / `iosNotificationsModule` | DI bindings. | **Modified** — bind the new concrete classes, gated by build variant (§5, §13). |
| `NoOpNotificationHandler` | Fallback for local/debug builds. | **Unchanged**, still bound for those variants (§18 point 1). |
| `DeviceBindingManager`, `DeviceBindingRepository` (K-01) | Call `getPushToken()`, register/re-register with B-01. | **Unchanged call sites** — this document guarantees the values they receive are now real. |
| `DeepLinkResolutionHandler` (K-02) | Intercepts notification-tap intents, resolves via B-06. | **Unchanged** — this document guarantees the tap intent it already intercepts now actually originates from a real, correctly-constructed system notification. |
| `CORE_NOTIFICATIONS_INSTRUCTIONS.md` | Documents the bindings. | **Corrected** (§7's "intended to bind" language, per §15 of this document's diff). |

---

## 5. Folder/file structure

```
core-notifications/
  src/
    commonMain/kotlin/com/noorheroes/core/notifications/
      handler/
        NotificationHandler.kt                       # interface — UNCHANGED
        NoOpNotificationHandler.kt                    # UNCHANGED — kept bound for local/debug builds
        NotificationPermissionController.kt           # NEW — interface, additive
        NoOpNotificationPermissionController.kt       # NEW — debug/local fallback
        NotificationPermissionState.kt                # NEW — sealed/enum: Granted, Denied, NotDetermined
        PushTokenStore.kt                             # NEW — interface, core-datastore-backed
      di/
        NotificationsModule.kt                        # MODIFIED — binds NoOp by default; binds
                                                        # PushTokenStore's real impl always (it has
                                                        # no platform dependency itself)
        AndroidNotificationsModule.kt                  # MODIFIED — binds FcmNotificationHandler,
                                                        # AndroidNotificationPermissionController
        IosNotificationsModule.kt                      # MODIFIED — binds ApnsNotificationHandler,
                                                        # IosNotificationPermissionController
      binding/                                         # EXISTING (B17 K-01) — untouched, referenced only
      deeplink/                                        # EXISTING (B17 K-02) — untouched, referenced only
    androidMain/kotlin/com/noorheroes/core/notifications/
      handler/
        FcmNotificationHandler.kt                      # NEW
      service/
        NoorFirebaseMessagingService.kt                 # NEW
      notify/
        SystemNotificationBuilder.kt                    # NEW
      permission/
        AndroidNotificationPermissionController.kt      # NEW
      store/
        PushTokenStoreImpl.android.kt                   # NEW — actual, or shared commonMain impl if
                                                          # PreferenceManager is already expect/actual
                                                          # (confirm during Task 13.1, §8.2)
    iosMain/kotlin/com/noorheroes/core/notifications/
      handler/
        ApnsNotificationHandler.kt                      # NEW
      permission/
        IosNotificationPermissionController.kt           # NEW
    commonTest/kotlin/com/noorheroes/core/notifications/
      handler/
        NotificationPermissionControllerTest.kt          # NEW
        PushTokenStoreTest.kt                             # NEW
    androidUnitTest/.../handler/
      FcmNotificationHandlerTest.kt                       # NEW
      NoorFirebaseMessagingServiceTest.kt                 # NEW
    iosTest/.../handler/
      ApnsNotificationHandlerTest.kt                      # NEW

androidApp/  (or the project's equivalent platform app module — confirm exact module name, Task 13.1)
  google-services.json                                    # NEW — per-environment variants (§7.1)
  src/main/AndroidManifest.xml                             # MODIFIED — POST_NOTIFICATIONS permission,
                                                             # NoorFirebaseMessagingService <service>
                                                             # registration, default notification-channel
                                                             # <meta-data> (§7.3)
  src/main/kotlin/.../NoorFirebaseInitializer.kt            # NEW or extends existing Application.onCreate
                                                             # — FirebaseApp.initializeApp(context) if not
                                                             # already auto-initialized by the plugin

iosApp/
  GoogleService-Info.plist                                  # NEW — per-environment variants (§7.1)
  Info.plist                                                # MODIFIED — UIBackgroundModes: remote-notification
  iosApp.entitlements                                       # MODIFIED — aps-environment (development/production)
  Sources/NoorNotificationCenterDelegate.swift               # NEW — Swift shim (§3.5.1)
  Sources/AppDelegate.swift (or App.swift life-cycle hooks)  # MODIFIED — FirebaseApp.configure(),
                                                             # UNUserNotificationCenter.delegate assignment,
                                                             # didRegisterForRemoteNotificationsWithDeviceToken
                                                             # → Messaging.messaging().apnsToken bridge

NoorHeroes/core/
  CORE_NOTIFICATIONS_INSTRUCTIONS.md                        # MODIFIED — §7 corrected (§15 of this document)
```

**Note on exact platform-module names:** the corpus provided to this task names `androidMain`/`iosMain` source sets and `androidNotificationsModule`/`iosNotificationsModule` Koin modules, but does not name the exact top-level Android/iOS application module (`androidApp`, `app`, or a project-specific name) or the exact iOS app-target Swift source layout. **Do not assume the names above** — Task 13.1 requires confirming the real module/target names before creating any file under them.

---

## 6. APIs, models, interfaces, and data flow

### 6.1 `NotificationHandler` — unchanged interface (reproduced for reference only)

```kotlin
package com.noorheroes.core.notifications.handler

interface NotificationHandler {
    suspend fun getPushToken(): String?
    fun onNotificationReceived(payload: Map<String, String>)
}
```
No signature change. `FcmNotificationHandler` and `ApnsNotificationHandler` are new implementers; every existing call site (K-01's `DeviceBindingManager`, any decorator of `onNotificationReceived`) continues to compile unmodified.

### 6.2 `NotificationPermissionController` — new, additive interface

```kotlin
package com.noorheroes.core.notifications.handler

/** Additive to core-notifications; deliberately NOT a change to NotificationHandler (§3.1, §18 point 3). */
interface NotificationPermissionController {
    /** Triggers the platform's OS-level permission prompt if not already determined; suspends
     * until the user responds (or resolves immediately if already granted/denied). */
    suspend fun requestPermission(): NotificationPermissionState

    /** Synchronous best-effort read of the current authorization state, without prompting. */
    fun currentPermissionState(): NotificationPermissionState
}

sealed class NotificationPermissionState {
    data object Granted : NotificationPermissionState()
    data object Denied : NotificationPermissionState()
    data object NotDetermined : NotificationPermissionState()
}
```

```kotlin
package com.noorheroes.core.notifications.handler

/** Fallback for local/debug builds, mirroring NoOpNotificationHandler's role (§18 point 1). */
internal class NoOpNotificationPermissionController : NotificationPermissionController {
    override suspend fun requestPermission(): NotificationPermissionState = NotificationPermissionState.Denied
    override fun currentPermissionState(): NotificationPermissionState = NotificationPermissionState.Denied
}
```

### 6.3 `PushTokenStore` — new, `core-datastore`-backed

```kotlin
package com.noorheroes.core.notifications.handler

/**
 * Caches the most recently issued push token so getPushToken() (§3.1) can return the current
 * value without an unnecessary round-trip on every call, and so an OS-driven token-refresh
 * callback (onNewToken / the iOS FCM registration-token callback) has somewhere to write the new
 * value that a subsequent getPushToken() call will observe.
 *
 * Distinct from, and not a replacement for, K-01's own separately-specified pending-binding-
 * update-queue cache (§2.2, §8.3) — this store holds only the raw token value, nothing about
 * registration/retry state.
 */
interface PushTokenStore {
    /** Synchronous best-effort read of the last-cached token, or null if none is cached yet. */
    fun currentToken(): String?
    fun saveToken(token: String)
    /** Not called on ordinary logout (§9.2) — reserved for a full local-data-wipe path (e.g. C.21). */
    fun clear()
}
```

### 6.4 Data flow — end-to-end, showing exactly which document owns which segment

```
App start / login / profile switch
    ↓
DeviceBindingManager.switchActiveProfile()  [B17 K-01 — EXISTING, unchanged]
    ↓ calls
NotificationHandler.getPushToken()  [interface — unchanged]
    ↓ dispatches to (THIS DOCUMENT)
FcmNotificationHandler / ApnsNotificationHandler
    ↓ PushTokenStore cache hit → return immediately
    ↓ PushTokenStore cache miss → platform SDK call (§3.2 / §3.5) → cache → return
Real FCM token string
    ↓ (back in K-01 — EXISTING, unchanged)
DeviceBindingRepository.registerToken()  →  POST /v1/devices { fcm_token, app_version, locale, timezone }
    ↓ (backend — EXISTING, unchanged)
DeviceBindingService.register_installation()  [B17 B-01]  →  push_installations / push_tokens rows
    ↓ (later, on a trigger — EXISTING, unchanged)
PolicyEngine.evaluate()  [B-03]  →  TemplateRenderer.render()  [B-04]  →  DeliveryAdapter.send_fcm()  [B-05]
    ↓ Firebase Admin SDK server-side send, over the real Firebase Cloud Messaging backend
    ↓ push delivered over-the-wire to the specific installation's real device (THIS DOCUMENT, receiving end)
NoorFirebaseMessagingService.onMessageReceived()  [Android]  /  Firebase Messaging + APNs delivery  [iOS]
    ↓ NotificationHandler.onNotificationReceived(payload)  [interface — unchanged, now actually fires]
    ↓ SystemNotificationBuilder.show(...)  [Android]  /  UNUserNotificationCenter display  [iOS]
    ↓ user taps the system notification
:core:navigation's existing notification-tap entry point  [EXISTING — K-02 already intercepts this]
    ↓
DeepLinkResolutionHandler  [B17 K-02 — EXISTING, unchanged]  →  GET /v1/notifications/resolve  [B-06]
    ↓
Resolved navigation destination (or lock-gate / content-unavailable / offline fallback, per K-02 §11)
```

---

## 7. Dependencies and configuration requirements

### 7.1 Firebase project and platform config files

- **One Firebase project** (recommend one project per deployment tier — Dev, Staging, Production — mirroring the project's existing tiered-environment convention rather than one shared project across tiers, to keep test/dev pushes fully isolated from production delivery).
- **Android**: register the app's package name/applicationId per build variant in the Firebase console; download the resulting `google-services.json` (one per tier) and place it at `androidApp/google-services.json` (or the flavor-specific `androidApp/src/<flavor>/google-services.json` path, if the project's existing build-variant setup uses flavor-scoped resources — confirm during Task 13.1). Apply the `com.google.gms.google-services` Gradle plugin in `androidApp/build.gradle.kts`.
- **iOS**: register the app's Bundle ID per tier in the same Firebase project; download `GoogleService-Info.plist` (one per tier) and add it to the Xcode project target (must be added via Xcode itself, not just copied into the filesystem, so it is bundled into the app — confirm the project's existing Xcode/XcodeGen or Fastlane config for how per-tier config files are already switched, if any equivalent pattern exists elsewhere in the iOS build, before inventing a new one).
- **APNs Auth Key (recommended over a legacy push certificate — see §15):** generate a `.p8` Auth Key in the Apple Developer portal (Certificates, Identifiers & Profiles → Keys), scoped to Apple Push Notifications service (APNs); upload it to the Firebase console under Project Settings → Cloud Messaging → Apple app configuration, along with the Key ID and Team ID. **Do not commit the `.p8` file to the repository** — it is a credential; store it via the project's existing secrets-management convention (`Development_Blueprints.Phase1_Infra_Config.Infra.02-secrets-management-env-example-gitleaks.md`) if server-side APNs access is ever added directly (not required by this document, since B-05 sends via the Firebase Admin SDK, not raw APNs — but the Auth Key itself must still never enter version control regardless of which SDK layer uses it).

### 7.2 Gradle / Kotlin Multiplatform dependencies

```kotlin
// core-notifications/build.gradle.kts — androidMain dependencies
implementation(platform("com.google.firebase:firebase-bom:<latest-stable>"))
implementation("com.google.firebase:firebase-messaging-ktx")
implementation("org.jetbrains.kotlinx:kotlinx-coroutines-play-services:<version>") // Task<T>.await()
implementation("androidx.core:core-ktx:<version>") // NotificationCompat, ContextCompat

// core-notifications/build.gradle.kts — iOS cocoapods block
cocoapods {
    // ...
    pod("FirebaseMessaging")
}
```

Confirm the project's existing Firebase BoM/Kotlin coroutines version pins (if any core module already depends on `kotlinx-coroutines-play-services` or a Firebase BoM version, per the corpus's general "reuse existing conventions" discipline) before introducing a new, potentially conflicting version.

### 7.3 Android manifest additions

```xml
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />

<service
    android:name=".NoorFirebaseMessagingService"
    android:exported="false">
    <intent-filter>
        <action android:name="com.google.firebase.MESSAGING_EVENT" />
    </intent-filter>
</service>

<meta-data
    android:name="com.google.firebase.messaging.default_notification_channel_id"
    android:value="noorheroes_default" />
```
`POST_NOTIFICATIONS` is declared here but must still be **requested at runtime** on API 33+ via `AndroidNotificationPermissionController` (§3.4) — declaring it in the manifest alone does not grant it.

### 7.4 iOS `Info.plist` / entitlements

- `UIBackgroundModes` array must include `remote-notification` (required for the app to receive background/silent pushes and for the FCM/APNs registration flow to function correctly when the app is not in the foreground).
- The app's entitlements file must include `aps-environment` set to `development` for debug/ad-hoc builds and `production` for release/TestFlight/App Store builds — this must match the APNs Auth Key's environment scope and the provisioning profile used; a mismatch here is the single most common cause of "token obtained but no pushes ever arrive" on iOS (documented explicitly in §10 as an edge case).

---

## 8. Database/storage requirements

### 8.1 No new backend database tables

This document is entirely client-side (§2.2). All backend schema (`push_installations`, `push_tokens`, `device_profile_bindings`) is already owned and implemented by B-01; this document introduces zero new backend tables.

### 8.2 `PushTokenStore` — new `core-datastore` specialized domain store

Following the exact pattern `CORE_DATASTORE_INSTRUCTIONS.md` §5 already establishes (`FamilyTimezoneStore`, `ClockSkewStore`, `LastObservedTimeZoneStore`):

| Store | Data managed | Key method |
|---|---|---|
| `PushTokenStore` (NEW) | Current push token value | `saveToken(token: String)`, `currentToken(): String?`, `clear()` |

Implemented internally via the module's existing `PreferenceManager` (`prefs.getString("push_token", default = null)` / `prefs.setString("push_token", token)`), exactly the same underlying mechanism `CORE_DATASTORE_INSTRUCTIONS.md` §4 already documents for any other semantic wrapper — **no new persistence technology, no `core-database`/Room table** (a single string value is exactly the "lightweight, non-sensitive application state" `core-datastore`'s own scope statement already describes; it is not "Complex Data" requiring `core-database`, and a push token is not a credential requiring `core-security`'s Keystore-backed storage — it identifies an installation for delivery targeting, not an authentication secret).

### 8.3 Explicit boundary against K-01's own, separate cache

K-01 §14/§20 already specifies a **different** local cache: "Local persistence of pending/queued binding-update requests (for offline retry) via `:core:datastore`." That cache holds *retry-queue state for the network call to B-01*; `PushTokenStore` (this document) holds *the raw token value itself*. They may both live under `core-datastore` and even in the same physical DataStore file, but they are logically distinct stores with distinct keys and distinct owners — this document does not read, write, or reuse K-01's queue store, and K-01's queue store does not need to change to accommodate `PushTokenStore`'s introduction.

### 8.4 Token refresh handling

Handled entirely by the cache-freshness design in §3.1/§3.3/§3.5: `onNewToken` (Android) / the Firebase Messaging registration-token callback (iOS) writes through `PushTokenStore.saveToken()` immediately, so the next `getPushToken()` call — whenever K-01 next makes one — observes the refreshed value with no additional signaling mechanism required.

---

## 9. Authentication, authorization, validation, and security considerations

### 9.1 The token is not a secret and is not, by itself, session-bound

A push token identifies an **installation**, not an authenticated user or session (§2.3, restating K-01/B-01's own "one token per installation, not per child"). It requires no encryption-at-rest treatment beyond `core-datastore`'s ordinary handling (§8.2) and is not a `core-security`/Keystore concern. What *is* security-relevant is which **profile** (parent or a specific child) is currently bound to that installation — and that binding, its exclusivity guarantee, and its authenticated (`get_current_parent`/`get_current_child`) registration call are entirely B-01/K-01's already-implemented, already-audited responsibility (B-01 §25: "the binding-switch transaction is this service's most security-critical operation"). This document does not weaken, bypass, or duplicate that guarantee — it only supplies the raw token value the already-authenticated registration call carries.

### 9.2 Token lifecycle on logout — the naive answer is wrong; here is the correct one

**The naive assumption** — "logout should invalidate/delete the local push token, the same way it clears other session state" — **is incorrect for this specific value**, and stating why is important given how easy it would be for an implementing agent to add exactly that as a seemingly-obvious hygiene step:

- The token is scoped to the **app installation**, not the session (§9.1). Deleting/regenerating it on every logout would force a fresh Firebase/APNs registration round-trip on every subsequent login for no security benefit, since the token itself grants no access to anything — only the **active binding** (server-side, B-01) determines which profile, if any, receives deliveries to that installation.
- K-01 §18 already documents the correct, existing behavior for logout: **"Local binding state cleared; server-side binding revoked via existing logout flow"** — i.e., the binding is set to `None`/deactivated, which is sufficient on its own to guarantee no further deliveries reach that installation for the logged-out profile, per B-03's send-time active-binding re-check (§9.4).
- **This document's `PushTokenStore.clear()` is therefore deliberately *not* wired into the ordinary logout path.** It exists as an available primitive for a genuinely different scenario — a full local-data-wipe request (e.g., cross-referencing C.21 Parent Account Deletion's own local-data-cleanup procedure, if one exists) — not for routine logout. If a future requirement changes this decision, it is a one-line call-site addition in whatever module owns the logout transition (`:core:auth`, per K-01 §9's own file-modification note), not a change to this document's classes.

### 9.3 Content integrity — never construct or mutate notification copy client-side

`SystemNotificationBuilder` (§3.3) and its iOS equivalent render exactly the `title`/`body` string values the backend's `RemoteMessage.data` payload provides — never reassembled from other raw fields, never templated client-side, never appended to. This is a direct, load-bearing consequence of B-04's `ChildSafetyBlocklistValidator` having already validated the *exact* rendered string that left the backend (B-04 §44: "run every child-facing template body through `ChildSafetyBlocklistValidator` **before** save... no override parameter accepted anywhere in the API"): if this document's code altered that string in any way before display, it would silently bypass a content-safety control this project treats as non-negotiable for a children's product. This is the specific mechanism through which this document satisfies the task's "child-facing notification content must comply with the same AI-safety/content-moderation standards as any other child-facing content" requirement — not by re-implementing content moderation, but by guaranteeing the already-moderated string is what actually reaches the child's screen, unmodified.

### 9.4 Quiet hours / bedtime — entirely server-enforced; this document adds zero client-side suppression logic, deliberately

The task brief that produced this document explicitly asks for the push-delivery path to "respect the parental controls/quiet-hours settings already specified in C.23." **The evidence in the corpus shows the correct way to satisfy that requirement is to add no client-side logic at all**, and adding any would be a regression, not an enhancement:

- B-03 §10 (Policy Engine) already evaluates "quiet-hours/bedtime check against current `screen_time_policies`" as step 2 of its mandatory, ordered, server-side send-time evaluation — explicitly **"at actual send time, never against stale intent-creation-time state"** (B-03 §4's own framing of its single most important architectural principle).
- B-03 §10 further states: **"Redis or PostgreSQL failure during evaluation must fail safe (suppress) rather than fail-open (never send unpoliced)"** — the server-side design already treats "no delivery" as the safe default under any uncertainty.
- If this document additionally implemented a client-side quiet-hours check (e.g., silently discarding a received push if it arrives during the configured bedtime window), it would create a **second, independent, potentially-inconsistent copy of quiet-hours logic** on the device — one that could drift from the server's `screen_time_policies` read (e.g., a parent changes the quiet-hours window on another device; this device's local copy is stale until its next sync), directly re-introducing the exact "stale intent-creation-time state" failure mode B-03 §4 was written specifically to eliminate. Worse, a received-but-suppressed push is not the same as a never-sent push from a fairness/quota perspective (it still consumed the family's B-05 delivery attempt and B-03's frequency budget) — so a client-side suppression layer would not even correctly replicate what "quiet hours" is supposed to mean operationally.
- **Conclusion, matching the reasoning pattern this project's other Phase-3 gap-closure documents already apply to similar "should this layer duplicate a check the layer below it already owns" questions:** this document's platform bindings faithfully deliver whatever B-03/B-05 already decided to send, and faithfully do nothing when B-03 decides to suppress (because a suppressed notification is never sent by B-05 in the first place — there is nothing for this document's code to receive or act on). Quiet-hours compliance for push delivery is **already fully satisfied**, by the already-built backend, before this document's code ever runs. This document's contribution to "respecting C.23" is exactly the fact that it introduces no code that could ever undermine that guarantee.

### 9.5 Permission-denied handling — matches the PRD's stated UX exactly, no more

Per B.17 PRD §1.15 (§2.3 of this document): a denied notification permission means the device silently receives no push notifications, with in-app banner-style notifications (FR-13, a separate, already-existing mechanism outside this document's scope) remaining fully functional as the fallback. `NotificationPermissionController` (§6.2) exposes exactly the primitives a feature-layer onboarding/settings screen needs to implement that PRD-specified behavior — a single request call and a state read — and this document does not add any custom re-prompt nagging, blocking modal, or repeated-priming flow beyond what those two methods make possible, per the PRD's explicit "no special in-app re-prompt nagging beyond the platform-standard one-time OS re-prompt affordance."

### 9.6 Validation

- `getPushToken()` never throws on an *expected* not-ready state (no cached value, registration still in flight) — it returns `null`, exactly per `CORE_NOTIFICATIONS_INSTRUCTIONS.md` §5's existing contract. It **does** throw (and log, never swallow) on a genuine platform-level failure (Play Services missing — §3.2's `IOException` path), per that same document's §10 "Don't swallow exceptions during token retrieval without logging."
- `SystemNotificationBuilder.show()` never displays a notification with an empty/missing `title`/`body` in a way that could look broken or, worse, be tap-navigable to an undefined destination — if either field is absent from the payload, the notification is not shown at all rather than shown with placeholder/blank text (an edge case explicitly enumerated in §10).

---

## 10. Error handling and edge cases

| Scenario | System behavior |
|---|---|
| Google Play Services missing/outdated/disabled (Android) | `getPushToken()` throws `IOException` (§3.2); logged, not swallowed; K-01's existing `try`/`catch` around the call handles it exactly as its own spec already anticipates. No push for this device; B.17 PRD §1.15's in-app-banner fallback remains unaffected (out of this document's scope). |
| Device has no Google Play Services at all (e.g., some Huawei/AOSP hardware) | Same as above, permanently — documented as a known limitation, not a bug to work around within this document's scope (§2.2, §15). |
| Notification permission denied by the user (either platform) | `NotificationPermissionController.requestPermission()` resolves `Denied`; the token may still be obtainable on Android (POST_NOTIFICATIONS gates *display*, not FCM token issuance) but on iOS, denial typically prevents `registerForRemoteNotifications()` from ever yielding a usable APNs token, so `getPushToken()` continues returning `null`. No custom re-prompt beyond the platform-standard one-time OS affordance (§9.5). |
| iOS Simulator (no APNs support) | `getPushToken()` returns `null` indefinitely in local development on a Simulator — this is an Apple platform limitation, not a bug in this document's code; local/debug builds should rely on `NoOpNotificationHandler` (§18 point 1) for this reason among others, and any manual push-delivery testing (§14) must use a physical iOS device. |
| APNs environment mismatch (`aps-environment` entitlement vs. the Auth Key/provisioning profile's environment, §7.4) | Token may be obtained successfully but no push ever arrives — the single most common iOS push-delivery failure mode; verified explicitly as part of §14's acceptance criteria (a real end-to-end delivered test push, not just "a token string was produced"). |
| Backend registration call (`POST /v1/devices`) fails after a real token is produced | **Already K-01's responsibility** (K-01 §18: retry with backoff; §19: offline queue-and-retry) — this document does not re-implement retry logic. This document's obligation is narrower and already satisfied by design: never mask or swallow a `getPushToken()` failure in a way that would prevent K-01's own retry/error-handling code from engaging correctly (§9.6). |
| Token refresh/rotation arrives mid-session (`onNewToken` / iOS registration-token callback fires while the app is running) | `PushTokenStore.saveToken()` updates the cache immediately (§3.3, §8.4); the next `getPushToken()` call — at whatever lifecycle point K-01 already calls it — observes the new value and K-01's already-existing rotation-handling re-registers it. No new event/notification is pushed proactively to K-01 (§3.1's Candidate B design), by deliberate choice. |
| `RemoteMessage.data` (Android) is missing `title`/`body`/`deep_link_token` entirely (malformed or non-notification data message) | `SystemNotificationBuilder` does not display a blank/placeholder notification (§9.6); `NotificationHandler.onNotificationReceived(payload)` still fires with whatever data is present, since that delegate's contract makes no assumption about payload shape. |
| App force-quit by the user (iOS) | Apple's documented platform limitation: a user-force-quit app does not receive background/silent remote notifications at all until the user manually relaunches it — this is not fixable by any app-level code and is not a defect in this document's implementation (documented in §15 as a known platform constraint). |
| Rapid repeated pushes / duplicate delivery from FCM's at-least-once delivery guarantee | `SystemNotificationBuilder.show()` uses `deepLinkToken.hashCode()` as the Android notification ID, so a genuine duplicate delivery of the same logical notification collapses to a single visible system-tray entry rather than stacking duplicates (a defensive, low-cost correctness property, not a requirement stated elsewhere in the corpus but consistent with K-02 §11's "prevent duplicate navigation on rapid repeated taps" spirit applied one layer earlier). |

---

## 11. State management and lifecycle considerations

### 11.1 Token lifecycle

```
[No token yet]
    ↓ app start, permission granted (or Android pre-33, granted by default)
[Obtained] — FirebaseMessaging.token / APNs→FCM bridge succeeds; cached in PushTokenStore
    ↓ (existing, unchanged) K-01's DeviceBindingManager calls getPushToken() → registers
[Registered with backend] — B-01's push_installations/push_tokens rows exist for this installation
    ↓ OS/SDK-driven rotation at any time (onNewToken / iOS registration-token callback)
[Refreshed] — PushTokenStore updated; next getPushToken() call observes the new value;
              K-01's existing rotation-handling re-registers (§3.1, §10)
    ↓ profile switch to a different child/parent, or logout
[Binding deactivated server-side] — token itself remains cached and valid; only the
                                     active-profile binding changes/clears (§9.2)
    ↓ app uninstall, or a genuine full local-data wipe (e.g. C.21)
[Invalidated] — PushTokenStore.clear() (§6.3); on uninstall this is moot (all app storage
                is removed by the OS); on an in-app full-data-wipe flow, this document's
                clear() is the primitive that flow would call
```

### 11.2 Notification-permission lifecycle

`NotDetermined → Granted` or `NotDetermined → Denied`, each a one-way transition from the app's perspective on both platforms **except** that the user can always change the OS-level setting from the system Settings app at any time outside the app's control — `currentPermissionState()` (§6.2) is therefore always a best-effort read of current OS state, never a value the app should cache indefinitely without re-checking at relevant moments (e.g., app foreground resume), though the exact re-check cadence is a feature-layer UX decision outside this document's scope.

### 11.3 What must not regress

- K-01's `DeviceBindingManager` state machine (its own profile-switch/binding-transition logic) is untouched by this document — it already correctly handles every transition (§4 of this document, "Unchanged call sites").
- `AuthState`/session lifecycle (owned by `core-security`/`core-auth`) is entirely independent of push-token lifecycle; this document introduces no coupling between the two beyond the pre-existing, unchanged fact that K-01's registration call is made with the currently authenticated session's Bearer token (§9.1).

---

## 12. Integration points with existing modules

### 12.1 `core-network` — indirect only, not a new dependency edge from this document's own code

`CORE_NOTIFICATIONS_INSTRUCTIONS.md` §8 lists `core-notifications -> core-common` as the module's only allowed dependency, notably omitting `core-network` — yet K-01 §8 places `DeviceBindingRepository` (which calls `POST /v1/devices` via `core-network` conventions, per K-01 §26's own Library Requirements) inside `core-notifications` itself. **This is a pre-existing inconsistency in the corpus, upstream of this document and not something this document resolves** — flag it during Task 13.1 for whoever owns the module-dependency-graph documentation, but do not block this document's own work on it. **This document's own new code — `FcmNotificationHandler`, `ApnsNotificationHandler`, `PushTokenStore`, `NotificationPermissionController` and their platform actuals — makes zero HTTP calls and has no direct `core-network` dependency at all.** The task brief's framing of `core-network` as a "depends on" for this document is therefore satisfied transitively (this document supplies the value K-01's `core-network`-dependent repository call carries), not by this document's own code importing anything from `core-network`.

### 12.2 `core-datastore` — one new specialized domain store

`PushTokenStore` (§6.3, §8.2) is added following the exact existing pattern (`FamilyTimezoneStore`/`ClockSkewStore`); no change to `PreferenceManager`'s own interface or to `core-datastore`'s DI wiring beyond registering the one new store.

### 12.3 B17 K-01 `DeviceBindingManager` / `DeviceBindingRepository`

Zero source changes required. `getPushToken()` now returns real values instead of `null`; K-01's already-written registration and rotation-handling logic engages correctly with no modification (§3.1, §4, §10).

### 12.4 B17 K-02 `DeepLinkResolutionHandler`

Zero source changes required to K-02 itself. This document's `SystemNotificationBuilder` (Android) and `NoorNotificationCenterDelegate` (iOS, §3.5.1) are responsible for ensuring a tapped system notification reaches `:core:navigation`'s existing notification-tap entry point — the exact point K-02 §9 already documents as a file it modifies to intercept all such intents. This document supplies real, correctly-constructed tap intents for K-02 to intercept; it does not touch K-02's interception or resolution logic.

### 12.5 C.25 Notifications (Parent) & Support — shared-infrastructure reuse, confirmed by that feature's own PRD

C.25 §44/§96 states explicitly: **"Maintain the shared notification-delivery architecture's integrity (exclusive device-profile binding, server-side quiet-hours enforcement) at the parent-facing half of the system, consistent with B.17's child-facing specification"** and **"this feature's notification-delivery mechanics reuse B.17's exact shared infrastructure (binding, Policy Engine, Deep Link Resolution) — no parallel, divergent implementation for the parent-facing half."** This document's platform bindings are therefore consumed identically by parent-facing pushes (C.25) and child-facing pushes (B.17) — there is no parent-specific or child-specific branch anywhere in `FcmNotificationHandler`/`ApnsNotificationHandler`/`SystemNotificationBuilder`, by design, matching this explicit cross-feature architectural commitment.

### 12.6 `core-navigation` — the deep-link tap target this document must reach, not redefine

This document assumes `:core:navigation` already exposes the notification-tap entry point K-02 §9 references (it must, since K-02 is already built against it). Task 13.1 requires locating that exact entry point (its function/Intent-filter/URI-scheme shape) before implementing `SystemNotificationBuilder`'s `PendingIntent` construction (§3.3) or the iOS Swift shim's tap-forwarding call (§3.5.1) — do not invent a new, parallel navigation entry point.

---

## 13. Development steps in the correct implementation order

**Task 01 — Confirm real module/file names and the exact `:core:navigation` deep-link entry point.**
Locate the actual Android/iOS app module names (§5's note), confirm whether `core-notifications` genuinely has no `core-network` dependency edge in the real `build.gradle.kts` (flag the K-01 inconsistency per §12.1 without attempting to fix it), and locate the exact function/Intent-filter/URI-scheme `:core:navigation` already exposes for K-02's interception (§12.6). Do not proceed to Task 05 with assumed names.

**Task 02 — Firebase project setup and config file provisioning.**
Create/confirm the Firebase project(s) per deployment tier; register Android/iOS app identifiers; download `google-services.json`/`GoogleService-Info.plist`; generate and upload the APNs Auth Key (§7.1). Confirm secrets-management handling for the `.p8` key per the project's existing convention.

**Task 03 — Implement `PushTokenStore` (§6.3, §8.2) and its tests.**
Pure `core-datastore` logic, no platform SDK dependency — implement and test first as the foundation both platform actuals build on.

**Task 04 — Implement `NotificationPermissionController` + `NotificationPermissionState` (§6.2) and `NoOpNotificationPermissionController`.**
Common interface first; platform actuals in Tasks 06/08.

**Task 05 — Android: Gradle/manifest wiring (§7.2, §7.3).**
Apply the Google Services plugin, add dependencies, update `AndroidManifest.xml` (`POST_NOTIFICATIONS`, `NoorFirebaseMessagingService` `<service>` registration, default channel `<meta-data>`).

**Task 06 — Implement `FcmNotificationHandler`, `NoorFirebaseMessagingService`, `SystemNotificationBuilder`, `AndroidNotificationPermissionController` (§3.2–§3.4).**
Wire into `androidNotificationsModule`, gated by build variant (§13 Task 11).

**Task 07 — iOS: `Info.plist`/entitlements/CocoaPods wiring (§7.2, §7.4).**
Add `UIBackgroundModes: remote-notification`, configure `aps-environment` per build configuration, add the `FirebaseMessaging` pod.

**Task 08 — Implement `NoorNotificationCenterDelegate` (Swift shim, §3.5.1), `ApnsNotificationHandler`, `IosNotificationPermissionController` (§3.5–§3.6).**
Confirm the Swift-shim-vs-direct-cinterop decision against the real iOS app-target structure before writing the delegate conformances (§3.5.1's explicit "confirm during implementation" note). Wire into `iosNotificationsModule`, gated by build configuration (§13 Task 11).

**Task 09 — Wire `onNewToken`/registration-token-refresh callbacks into `PushTokenStore` on both platforms.**
Confirms §3.1's cache-freshness design end-to-end.

**Task 10 — Wire notification-tap handling into `:core:navigation`'s confirmed entry point (Task 01) on both platforms.**
`SystemNotificationBuilder`'s `PendingIntent` (Android) and the Swift shim's tap-forwarding call (iOS) — confirm K-02's `DeepLinkResolutionHandler` is genuinely reached end-to-end with a real `deep_link_token`, not just that navigation occurs.

**Task 11 — Build-variant gating: bind real implementations only for non-debug variants; confirm `NoOpNotificationHandler`/`NoOpNotificationPermissionController` remain bound for local/debug builds (§18 point 1).**
This is a Koin module-inclusion/build-flavor change, not a new architectural mechanism — `notificationsModule` already establishes the "common binds NoOp, platform module overrides if loaded" pattern (`CORE_NOTIFICATIONS_INSTRUCTIONS.md` §8's "Recommended Patterns"); this task only makes the platform module's *inclusion in the Koin start list* conditional on build variant/flavor.

**Task 12 — Correct `CORE_NOTIFICATIONS_INSTRUCTIONS.md` §7 (§15 of this document specifies the exact text change).**

**Task 13 — Full test suite (§14) and manual real-device delivery verification.**

**Task 14 — Final review** confirming: `NotificationHandler`'s two methods have zero signature changes; K-01/K-02 compile and pass their own existing tests unmodified; a real test push is delivered end-to-end to both a physical Android device and a physical iOS device (§14.6).

---

## 14. Testing strategy and acceptance criteria

### 14.1 Unit — `PushTokenStore`
- `saveToken`/`currentToken` round-trip correctly through the underlying `PreferenceManager`.
- `clear()` removes the cached value; `currentToken()` returns `null` afterward.

### 14.2 Unit — `NotificationPermissionController` (both platforms, plus `NoOp`)
- `NoOpNotificationPermissionController` always resolves `Denied`, confirming debug/local builds behave safely with no OS permission dialog ever triggered.
- Android: `currentPermissionState()` correctly reflects `PERMISSION_GRANTED`/`PERMISSION_DENIED` for both pre-33 (always `Granted`) and 33+ (real check) cases, via a `ContextCompat.checkSelfPermission` test double.
- iOS: `requestPermission()` correctly maps the `UNUserNotificationCenter` authorization callback's `granted` boolean to `Granted`/`Denied`.

### 14.3 Unit — `FcmNotificationHandler` / `ApnsNotificationHandler`
- `getPushToken()` returns the cached value without invoking the platform SDK call when `PushTokenStore.currentToken()` is non-null (proves §3.1's fast-path design).
- `getPushToken()` invokes the platform SDK call and caches the result when no cached value exists.
- Android: a simulated Play-Services-unavailable failure results in a logged, rethrown `IOException` — never swallowed (§9.6).
- `onNotificationReceived(payload)` is invoked with the exact `RemoteMessage.data` map, unmodified.

### 14.4 Unit — `SystemNotificationBuilder`
- A payload with `title`/`body`/`deep_link_token` present produces a notification whose `PendingIntent` carries the exact `deep_link_token` value as a query parameter on the confirmed (Task 01) deep-link URI scheme.
- A payload missing `title` or `body` does not produce a visible notification (§9.6, §10).
- Two deliveries with the same `deep_link_token` collapse to a single notification ID, not a stacked duplicate (§10).

### 14.5 Integration — token reaches K-01 unmodified
- With `FcmNotificationHandler`/`ApnsNotificationHandler` bound (test build variant) and a fake/stub platform SDK returning a known token string, confirm `DeviceBindingManager.switchActiveProfile()` (K-01's real, unmodified code) receives and attempts to register that exact token — proving the seam this document closes without requiring any change to K-01's own test suite.

### 14.6 Manual / device — real end-to-end delivery (the acceptance criterion the task brief names explicitly)
- **Android:** a physical device (or an emulator with Google Play Services installed) obtains a real FCM token; a test push sent via the Firebase console (or a direct Firebase Admin SDK call from a local script, using the real backend's send path if a staging environment is available) is received, displayed in the system tray with correct title/body, and tapping it correctly launches the app and reaches K-02's `DeepLinkResolutionHandler` with the expected `deep_link_token`.
- **iOS:** a physical device (**not** the Simulator, per §10) obtains a real FCM token via the APNs-bridge path; the same test-push-and-tap flow is verified, additionally confirming the `aps-environment` entitlement matches the Auth Key's environment (§7.4, §10) — a mismatched-environment failure (token obtained, no push arrives) must be explicitly ruled out, not just assumed absent.
- Both platforms: a token-refresh event (simulated by force-clearing the app's Firebase/Play-Services data on Android, or reinstalling on iOS) results in a new token being obtained and, per §14.5, correctly reaching K-01's registration path again.

### 14.7 Acceptance criteria (summary)
- [ ] `getPushToken()` returns a real, non-null token on both platforms on a physical device with notification permission granted.
- [ ] A test push sent through the real FCM pipeline is delivered and correctly displayed on both a physical Android and a physical iOS device.
- [ ] Tapping the delivered notification reaches K-02's `DeepLinkResolutionHandler` with the correct `deep_link_token`, unmodified from the sent payload.
- [ ] `NotificationHandler`'s two methods compile with zero signature changes; K-01/K-02's existing test suites pass unmodified.
- [ ] `NoOpNotificationHandler`/`NoOpNotificationPermissionController` remain the bound implementations for local/debug build variants, verified by a build-variant-specific DI test.
- [ ] A Play-Services-unavailable / permission-denied scenario degrades to `null`/`Denied` without a crash on either platform.
- [ ] No notification body/title text is ever constructed or altered client-side (§9.3), verified by the §14.4 unit tests.

---

## 15. Production-readiness considerations

- **APNs Auth Key vs. certificate — deliberately recommending the Auth Key (§7.1).** A legacy APNs push *certificate* expires annually and requires manual regeneration/re-upload — a recurring operational burden and a real production-outage risk if missed. An APNs *Auth Key* (`.p8`, token-based authentication) **does not expire** and is Apple's own recommended modern approach; this document specifies it as the default precisely to eliminate the annual-expiry monitoring burden the task brief anticipates. **What still needs monitoring under the Auth Key approach:** the key can be manually revoked in the Apple Developer portal (by a team member, intentionally or by mistake), and Team ID/Key ID misconfiguration in the Firebase console is a silent failure mode — monitor via Firebase console delivery-error-rate reporting and/or B-05's own `push_token_invalidated`/delivery-failure analytics (already implemented server-side, B-05 §23) as the operational proxy for "is the APNs credential still healthy," rather than a calendar-based expiry reminder that wouldn't apply to this credential type anyway. If the project ever adds a legacy certificate-based path for any reason, that certificate's annual expiry *would* need an explicit calendar/monitoring reminder — documented here as a contingency, not a current requirement.
- **FCM quota/rate considerations.** Standard FCM sending has no hard published rate limit for typical application volumes, but B-05 §98 already specifies its own p95 < 30s delivery-latency target and batch-send support for large fan-outs — this document's client-side code has no send-rate concern of its own (it never sends, only receives/displays), so no additional client-side throttling is needed; any future scaling concern belongs entirely to B-05's already-scoped batch-send/throttle logic.
- **Devices without Google Play Services** (§2.2, §10) are a known, accepted limitation of this document's scope, not silently unhandled — they degrade to B.17 PRD §1.15's documented in-app-banner fallback. If the target market's device mix later shows this to be a material gap, an HMS Push Kit integration would be a separate, future document (a new `NotificationHandler` actual variant selected by a runtime device-capability check), not a retrofit onto this document's classes.
- **iOS force-quit limitation** (§10) is an Apple platform constraint with no app-level workaround; document it in user-facing support materials (C.25's FAQ content, potentially) rather than treating it as an implementation defect to chase.
- **Crash-and-visible-failure over silent degradation for genuine misconfiguration.** A missing/invalid `google-services.json`/`GoogleService-Info.plist`, or an `aps-environment` mismatch, should fail loudly and early in CI/QA builds (a smoke test attempting real token retrieval on a real or emulated device in the CI pipeline, if the project's existing CI already has device/emulator test capacity — confirm against the project's existing CI pipeline documents rather than assuming) rather than only being discovered when a real production push silently never arrives.
- **Per-environment config file isolation** (§7.1's one-Firebase-project-per-tier recommendation) prevents a Staging test push from ever being deliverable to a Production build's real token, and vice versa — a meaningful safety property for a children's product where an accidental cross-environment test send reaching real users' devices would be a genuine incident, not just a nuisance.

---

## 16. Dependencies/prerequisites

- `core-notifications` module itself — already implemented (`NotificationHandler`, `NoOpNotificationHandler`, `notificationsModule` skeleton all pre-exist and are reused/extended, not rebuilt).
- `core-datastore`'s `PreferenceManager` — already implemented; `PushTokenStore` is built on top of it, not a parallel persistence mechanism.
- B17 B-01 (`POST /v1/devices`, `PATCH /v1/devices/{id}/active-profile`) and B-05 (Firebase Admin SDK server-side send) — already implemented; this document's output is consumed by the former and received from the latter, with no code dependency in either direction beyond the existing, unchanged API contracts.
- B17 K-01 (`DeviceBindingManager`) and K-02 (`DeepLinkResolutionHandler`) — already implemented; this document assumes both exist exactly as their own specifications describe and requires zero changes to either.
- A Firebase project, an Apple Developer account with APNs Auth Key generation access, and the project's existing secrets-management convention for the `.p8` key — external/organizational prerequisites, not code.
- No new backend dependency of any kind (§2.2).

---

## 17. Definition of Done

- [ ] `FcmNotificationHandler` (Android) and `ApnsNotificationHandler` (iOS) are the bound `NotificationHandler` implementations for non-debug build variants; `NoOpNotificationHandler` remains bound for local/debug variants.
- [ ] `NotificationHandler`'s interface contract is unchanged; K-01 and K-02 compile and pass their own existing test suites with zero source modifications.
- [ ] `PushTokenStore` and `NotificationPermissionController` (+ platform actuals + `NoOp` fallbacks) implemented and tested per §14.1–§14.4.
- [ ] A real test push, sent through the real FCM pipeline, is delivered and correctly displayed on both a physical Android device and a physical iOS device (§14.6, §14.7).
- [ ] Tapping a delivered notification correctly reaches K-02's `DeepLinkResolutionHandler` with the correct, unmodified `deep_link_token`.
- [ ] `google-services.json`/`GoogleService-Info.plist` are correctly provisioned per deployment tier; the APNs Auth Key is uploaded to the Firebase console and never committed to version control.
- [ ] `POST_NOTIFICATIONS` (Android 13+) and `UNUserNotificationCenter` authorization (iOS) are correctly requested at runtime, with `Denied` handled per B.17 PRD §1.15's exact stated UX (no custom nagging).
- [ ] Zero notification body/title text is ever constructed or mutated client-side (§9.3) — verified by unit test.
- [ ] Zero client-side quiet-hours/frequency-suppression logic exists anywhere in this document's code (§9.4) — verified by code review against §9.4's explicit reasoning.
- [ ] `CORE_NOTIFICATIONS_INSTRUCTIONS.md` §7 corrected per §15's exact text.
- [ ] Full test suite (§14) passing.

---

## 18. Assumptions or decisions the coding agent must follow

1. **`NoOpNotificationHandler` (and the new `NoOpNotificationPermissionController`) must remain bound and fully functional for local/debug build variants.** This is not achieved by adding a new opt-out mechanism — it falls out of `CORE_NOTIFICATIONS_INSTRUCTIONS.md` §8's own already-documented Koin module-load-order convention ("platform-specific Koin module is loaded *after* the common module to correctly override the NoOp implementation"): gate the platform module's *inclusion* in the app's `startKoin { modules(...) }` call by build variant/flavor (§13 Task 11), rather than inventing a runtime feature-flag or a change to `notificationsModule`'s own binding logic.
2. **The token this document produces is always an FCM token, on both platforms, per the evidence in §3.5** — never a raw APNs device token sent directly to the backend. Do not "simplify" iOS by skipping the Firebase Messaging bridge and sending the raw APNs token to `POST /v1/devices`; that would not match B-01's fixed `fcm_token`-only request schema.
3. **`getPushToken()` stays pull-based/suspend-only; no `Flow`, callback parameter, or other signature change is added to `NotificationHandler`.** Freshness is achieved entirely via `PushTokenStore`'s cache-on-callback design (§3.1). Any temptation to "improve" this into a reactive stream must be resisted for this Definition of Done — it is an explicit, evidence-based choice (§3.1), not an oversight, and K-01's existing code already works correctly against the pull-based design without modification.
4. **`PushTokenStore.clear()` is not called on ordinary logout** (§9.2) — only the server-side active-profile binding is revoked on logout, which is already K-01's job and already sufficient. Do not add a `clear()` call to the logout transition as a "belt and suspenders" hygiene measure; it is based on a mistaken analogy to session-scoped credentials that does not apply to an installation-scoped token, and doing so would force unnecessary re-registration churn with zero security benefit.
5. **Zero client-side quiet-hours, frequency-cap, or any other delivery-suppression logic may be added anywhere in this document's code**, even as a defensive/redundant measure. §9.4 explains in full why this would be a regression, not a safety improvement — trust B-03's server-side, send-time-evaluated policy engine completely; this document's job is display fidelity for whatever B-05 already decided to send, nothing more.
6. **Never construct, template, or mutate notification title/body text client-side from raw payload fields** (§9.3) — always render the pre-rendered `title`/`body` strings verbatim. This is a content-safety-governance boundary, not a stylistic preference.
7. **Do not attempt an HMS Push Kit / non-Google-Play-Services fallback for this Definition of Done** (§2.2, §15) — it is an explicitly out-of-scope, documented future option, not a silently-dropped requirement.
8. **If the real `:core:navigation` deep-link entry point (§12.6) or the real Android/iOS app module names (§5) differ from this document's placeholder examples, adapt this document's file paths and `PendingIntent`/Swift-shim wiring to the real names — do not rename the real project structure to match this document's examples**, mirroring the same discipline this project's other Phase-3 gap-closure documents already apply to similar "confirm the real name before writing code" situations.
9. **If, during implementation, `core-notifications` is found to genuinely have a `core-network` Gradle dependency edge already** (resolving the §12.1 inconsistency in the other direction than assumed), that does not change any code this document specifies — it only means the §12.1 documentation flag can be closed as "already consistent" rather than escalated further.

---

## AI Agent Development Prompt

You are implementing the real FCM (Android) and APNs (iOS) platform bindings behind NoorHeroes's KMP `core-notifications` module's already-built `NotificationHandler` abstraction. Read this entire document first, then follow it exactly — it is a **gap-closure task on top of already-working, already-built downstream code (B17 K-01, K-02, B-01, B-05)**, not a redesign of any of it.

**Context:** `core-notifications` already has a complete, stable `NotificationHandler` interface (`getPushToken(): String?` suspend, `onNotificationReceived(payload: Map<String, String>)`) and a `NoOpNotificationHandler` fallback, documented in `NoorHeroes/core/core-notifications/CORE_NOTIFICATIONS_INSTRUCTIONS.md`. Every downstream consumer — most importantly B17 K-01's `DeviceBindingManager` (which registers the token with the backend, handles rotation, and manages the offline retry queue) and B17 K-02's `DeepLinkResolutionHandler` (which intercepts every notification tap and re-validates it server-side before navigating) — is already fully implemented and was written *assuming* `getPushToken()` returns a real value and that a real, receivable push eventually arrives. It never has, because `CORE_NOTIFICATIONS_INSTRUCTIONS.md` §7 itself documents the platform bindings only as "intended to bind" — no concrete implementation exists. Your job is to build that concrete implementation, and nothing else.

**What to implement, in order (full detail in §13):**
1. Confirm the real Android/iOS app module names and the exact `:core:navigation` notification-tap entry point K-02 already integrates with (§12.6) — do not assume names.
2. Set up the Firebase project(s), `google-services.json`/`GoogleService-Info.plist` per deployment tier, and an APNs Auth Key (`.p8`, not a legacy certificate — §7.1, §15) uploaded to the Firebase console.
3. Implement `PushTokenStore` (§6.3, `core-datastore`-backed, following the existing `FamilyTimezoneStore`/`ClockSkewStore` pattern) and `NotificationPermissionController` + `NoOpNotificationPermissionController` (§6.2) — both new, additive, common-layer components.
4. Implement Android: `FcmNotificationHandler`, `NoorFirebaseMessagingService`, `SystemNotificationBuilder`, `AndroidNotificationPermissionController` (§3.2–§3.4), plus the required Gradle/manifest changes (§7.2–§7.3).
5. Implement iOS: `ApnsNotificationHandler`, the `NoorNotificationCenterDelegate` Swift shim, `IosNotificationPermissionController` (§3.5–§3.6), plus the required `Info.plist`/entitlements/CocoaPods changes (§7.2, §7.4). Confirm the Swift-shim-vs-cinterop approach against the real iOS app-target structure before writing delegate conformances (§3.5.1).
6. Bind the new concrete classes in `androidNotificationsModule`/`iosNotificationsModule`, gated by build variant so `NoOpNotificationHandler`/`NoOpNotificationPermissionController` remain bound for local/debug builds (§13 Task 11, §18 point 1) — this is a Koin module-inclusion change using the pattern the corpus already documents, not a new mechanism.
7. Correct `CORE_NOTIFICATIONS_INSTRUCTIONS.md` §7 per the exact text in §15.
8. Implement the full test suite in §14, and manually verify a real test push is delivered end-to-end (system-tray display + correct tap-to-K-02 routing) on a physical Android device and a physical iOS device — not the Simulator (§10, §14.6).

**What you must NOT change:**
- `NotificationHandler`'s two method signatures — zero changes. K-01 and K-02 must compile and pass their existing test suites completely unmodified.
- B17 K-01's `DeviceBindingManager`/`DeviceBindingRepository` — do not reimplement token registration, profile-switch binding, or offline retry/backoff; that is already built and already correct once `getPushToken()` returns real values.
- B17 K-02's `DeepLinkResolutionHandler` — do not reimplement deep-link resolution or navigation routing; your only obligation is that a tapped notification correctly reaches its existing interception point.
- B17 B-03's Policy Engine or C.23's quiet-hours configuration — implement **zero** client-side quiet-hours/frequency-suppression logic of any kind. This is a deliberate, fully-justified decision (§9.4), not an omission — adding such logic would be a regression, introducing a second, driftable copy of a check the server already performs correctly at actual send time.
- B17 B-04's template content — never construct, template, or mutate notification title/body text client-side; render exactly what the backend sends (§9.3).
- Any backend file, endpoint, or schema — this is a 100% client-side (`core-notifications`) document.
- Local (non-push) notification scheduling — out of scope per `CORE_NOTIFICATIONS_INSTRUCTIONS.md` §1 itself.

**How to verify you're done (full checklist in §14.7, §17):**
- `NotificationHandler`'s interface is byte-for-byte unchanged; a clean compile of K-01/K-02 against the new implementations, with zero source edits to either, is achieved.
- A real device on each platform obtains a non-null, real token, and a real test push (sent via the Firebase console or the real backend's staging pipeline) is delivered, displayed correctly, and — on tap — correctly reaches K-02's `DeepLinkResolutionHandler` with the correct `deep_link_token`.
- `NoOpNotificationHandler`/`NoOpNotificationPermissionController` remain the bound implementations for local/debug build variants (confirm via a build-variant-specific DI test, not just manual inspection).
- A simulated Play-Services-unavailable (Android) and a simulated permission-denied (either platform) scenario each degrade gracefully to `null`/`Denied` with no crash, and are logged, never silently swallowed.
- No notification text is ever constructed or altered client-side, and no client-side quiet-hours/suppression logic exists anywhere in your diff — both confirmed by code review against §9.3/§9.4's explicit reasoning, not just by passing tests.
- `google-services.json`/`GoogleService-Info.plist` are present and correct per tier; no `.p8` APNs key or other credential appears anywhere in your diff.

If, during implementation, you discover that a downstream file this document assumes exists (K-01's `DeviceBindingManager`, K-02's `DeepLinkResolutionHandler`, `:core:navigation`'s notification-tap entry point) does not actually exist yet or differs materially from how this document describes it, **stop and escalate rather than proceeding** — this document's entire design rests on those pieces already being correctly built exactly as their own specifications describe, and if that assumption is false, the scope boundary in §2.2 needs to be re-evaluated, not silently worked around.
