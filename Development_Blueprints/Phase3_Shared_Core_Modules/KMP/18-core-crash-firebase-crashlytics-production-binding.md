# Phase 3 — core-crash: Real Firebase Crashlytics Binding (Gap Closure)

> **Type:** Gap-Closure Blueprint (not a from-scratch build spec)
> **Module:** `core-crash` (KMP, Android/iOS) — with a small, additive, non-breaking touch to `composeApp`'s Koin wiring and to `CORE_CRASH_INSTRUCTIONS.md` itself
> **Closes:** The "Future: Firebase Crashlytics" gap documented in `CORE_CRASH_INSTRUCTIONS.md` §8 ("**Android**: Currently provides `LoggerCrashReporter`. Future: Firebase Crashlytics." / "**iOS**: Currently provides `LoggerCrashReporter`. Future: Native iOS crash handler with symbolication.")
> **Consumes:** A Firebase project (infra prerequisite — provisioned alongside Phase 1, see §7.1). Does not consume any backend API; Crashlytics is a direct device-to-Firebase integration.
> **Does not re-spec:** The `CrashReporter` interface, `BreadcrumbLevel` enum, `LoggerCrashReporter`, `NoOpCrashReporter`, the `core-logger` → `CrashReporter` breadcrumb-forwarding wiring, or `logAppError()`'s classification rules — all already built, all stay exactly as they are today.

---

## 1. Objective and Purpose

### 1.1 What this file is

`core-crash` is **already fully built** as an abstraction layer. Per `CORE_CRASH_INSTRUCTIONS.md` §5 and §8:

> **`LoggerCrashReporter`** — Redirects all reporting calls to the standard console output. **When to use:** Default for local development and as a fallback.
> **`NoOpCrashReporter`** — A "No-Operation" implementation that ignores all calls. **When to use:** Unit tests...
> **Android**: Currently provides `LoggerCrashReporter`. **Future: Firebase Crashlytics.**
> **iOS**: Currently provides `LoggerCrashReporter`. **Future: Native iOS crash handler with symbolication.**

The `CrashReporter` interface (`core-common`), the `crashModule` `expect`/`actual` seam (`core-crash`), the `BreadcrumbLevel` enum, and the `core-logger` → `CrashReporter` breadcrumb-forwarding pipeline are all already implemented and in production use — every feature module that injects `CrashReporter` today, and every call `logger.e(throwable) { ... }` or `logger.logAppError(...)` makes, already flows correctly through this abstraction. What is missing is that, at the very bottom of the stack, both platform `actual crashModule` definitions currently bind `LoggerCrashReporter` unconditionally — **nothing today ever reaches a real crash-reporting backend.** Every "crash," non-fatal, and breadcrumb the app has ever produced in any build has gone to `println`/console output and nowhere else. There is no Firebase project wiring, no `google-services.json`/`GoogleService-Info.plist`, and no dashboard where a real crash can be observed.

This document specs **exactly and only** the work needed to:

1. Add a real `FirebaseCrashReporter` implementation of the existing, unchanged `CrashReporter` interface, backed by the **GitLive Kotlin Multiplatform Firebase wrapper** (`dev.gitlive:firebase-crashlytics`) — the library `CORE_CRASH_INSTRUCTIONS.md`'s own architecture already anticipates ("Firebase Crashlytics" is named explicitly as the eventual Android backend, and GitLive is the only viable way to reach it from a single `commonMain` implementation rather than writing two independent native bindings).
2. Wire Android and iOS Firebase project configuration (`google-services.json`, `GoogleService-Info.plist`, Gradle plugins, CocoaPods/Xcode build-phase changes) so the real SDK actually initializes on both platforms.
3. Swap the two platform `actual crashModule` definitions to provide `FirebaseCrashReporter` in release/production builds while **keeping `LoggerCrashReporter` fully available and wired for local/debug builds** — this is not a replacement, it is an addition of a second, environment-selected binding behind the same seam.
4. Add PII-scrubbing, a custom-key allowlist, and consent/opt-out handling specific to this being a **children's product**, since — unlike `println`, which never leaves the device — a real Crashlytics binding now transmits data to a third-party (Google/Firebase) service, which changes the privacy posture non-trivially and is the primary reason this closure needs its own dedicated security section (§9).

### 1.2 What is explicitly NOT part of this document

- The `CrashReporter` interface's method signatures (`leaveBreadcrumb`, `recordNonFatal`, `setUserId`, `setCustomKey`) — **unchanged**, byte-for-byte, so every existing call site across the entire app compiles and behaves identically from the caller's point of view.
- `core-logger`'s `RedactionPipeline`, `FieldAllowlist`, `logAppError()`, `Severity.toBreadcrumbLevel()` — unchanged. This document adds a **second, independent** scrubbing layer inside `core-crash` itself (§9.2) rather than depending on `core-logger`'s, because `core-crash` must not depend on `core-logger` (see §4 for why — it is the same circular-dependency constraint the source doc already documents).
- iOS "native crash handler with symbolication" as a distinct, second mechanism — `CORE_CRASH_INSTRUCTIONS.md` §8 names this as iOS's "Future" line, but Firebase Crashlytics's iOS SDK (which GitLive's `firebase-crashlytics` pod wraps) **is** a native fatal-crash handler with full symbolication (via dSYM upload, §15.2) — implementing the GitLive/Firebase binding on iOS satisfies this line; no separate, second native crash-hook mechanism is specced or required.
- Any backend endpoint. Crashlytics uploads go directly from the device to Google's Firebase Crashlytics backend over Firebase's own SDK-managed transport — there is no NoorHeroes backend API in this data path.

---

## 2. Scope and Requirements

### 2.1 In scope

- A new `FirebaseCrashReporter` class (`commonMain`) implementing the existing `CrashReporter` interface via GitLive's unified `Firebase.crashlytics` API — one implementation, not a per-platform `expect`/`actual` pair, because GitLive's Crashlytics module already presents a single common Kotlin API surface over both native SDKs (§3.2).
- A minimal platform `expect`/`actual` seam **only** for the one piece GitLive does not unify: Firebase *app initialization* itself, which needs an Android `Context` on Android and an explicit `FirebaseApp.configure()`-equivalent call on iOS (§3.3, §6.4).
- PII scrubbing (`CrashPiiScrubber`) applied to every string this module ever hands to Crashlytics — breadcrumb messages, custom-key values, and exception messages — regardless of whether the caller already redacted upstream (§9.2).
- A fail-closed custom-key allowlist (`CrashCustomKeyAllowlist`), mirroring `core-logger`'s `FieldAllowlist` pattern, so arbitrary caller-supplied keys can never smuggle new unreviewed metadata fields into the crash dashboard (§9.3).
- A new, small, **additive** `CrashReportingConsent` interface for collection opt-in/opt-out (§9.5) — added *alongside* `CrashReporter`, not folded into it, specifically so the existing interface's signature does not change (§2.2).
- Updated `androidMain`/`iosMain` `actual crashModule` definitions that environment-select between `LoggerCrashReporter` (debug/local) and `FirebaseCrashReporter` (release/production), both now also satisfying `CrashReportingConsent` so DI stays uniform across environments (§6.6, §12.2).
- Firebase project configuration: `google-services.json` (Android), `GoogleService-Info.plist` (iOS), Gradle plugin wiring, CocoaPods wiring, dSYM upload build phase (iOS), and ProGuard/R8 mapping-file upload (Android) — §7 and §15.
- Updating `CORE_CRASH_INSTRUCTIONS.md` §5 and §8 to describe the real implementation instead of stating it as "Future" (§13, Task 09).
- Full test plan: unit tests for scrubbing/allowlist/consent logic (fakeable, no real SDK calls), and a manual acceptance test that a deliberately forced crash appears in the real Firebase Crashlytics console (§14).

### 2.2 Out of scope — explicitly do not touch

- **The `CrashReporter` interface itself** (`leaveBreadcrumb`, `recordNonFatal`, `setUserId`, `setCustomKey`) — this is the hard constraint this entire document is written around. No new method is added to it, no existing signature changes, no default parameter changes. Every feature module, every `logAppError()` call site, and every unit test that injects `NoOpCrashReporter` today keeps compiling and behaving identically.
- **`BreadcrumbLevel`** (`core-common`) — unchanged enum, same four values (`Debug`, `Info`, `Warning`, `Error`).
- **`LoggerCrashReporter`'s and `NoOpCrashReporter`'s existing behavior** — both keep doing exactly what they do today (console output / silent no-op, respectively) for every method already on `CrashReporter`. The only change to these two files is additive: each also implements the new `CrashReportingConsent` interface with a no-op body (§6.6), purely so DI stays uniform; this changes nothing about how any existing caller observes their behavior.
- **`core-logger`'s `RedactionPipeline`, `FieldAllowlist`, `NoorHeroesLogger`, `logAppError()`** — no changes. This document's PII scrubbing is a second, independent layer inside `core-crash` (§4, §9.2), not a modification of `core-logger`'s.
- **The `core-logger` → `CrashReporter` breadcrumb-forwarding wiring** (`Severity.toBreadcrumbLevel()`, the internal call from `NoorHeroesLoggerImpl` into `crashReporter.leaveBreadcrumb()`) — unchanged code. Its *runtime effect* does change once `crashModule` starts providing `FirebaseCrashReporter` in production (breadcrumbs now genuinely reach Crashlytics instead of a `println`), which is intentional and is the whole point of this closure — see §12.1 for the exact consequence.
- **`core-analytics`** (if/when it exists) — user-behavior tracking is explicitly out of `core-crash`'s remit per `CORE_CRASH_INSTRUCTIONS.md` §1 ("What NOT to add to this module... Analytics: User behavior tracking belongs in `core-analytics`"). `FirebaseCrashReporter.setUserId()`/`setCustomKey()` exist to aid crash *diagnosis*, not to build an analytics profile — see §9.4 for the line this document draws.
- **Firebase project creation/console setup itself** — treated here as an infra prerequisite (§7.1, §16), not a deliverable of this document. If no Firebase project exists yet, that provisioning step blocks this document's Definition of Done (§17) exactly the way B-01 blocked file `16`'s DoD until Phase 4 shipped — same pattern, different blocking dependency.
- **Any other Firebase product** (Analytics, Remote Config, Cloud Messaging, Performance Monitoring) — this document adds only the `firebase-common` (required transitively by every GitLive Firebase module) and `firebase-crashlytics` GitLive artifacts. Do not add `firebase-analytics`, `firebase-messaging`, etc. as a side effect of this work; each is its own, separately-specced integration if/when needed.

---

## 3. Technical Implementation Details

### 3.1 Why GitLive, and why one common implementation instead of `expect`/`actual` per platform

`CORE_CRASH_INSTRUCTIONS.md` §8 documents the seam the project already chose for this exact purpose: `crashModule` is an `expect`/`actual` **Koin module**, with each platform's `actual` free to provide whatever concrete `CrashReporter` it wants. The naive approach would be to also make `CrashReporter`'s *implementation* `expect`/`actual` — i.e., write an `AndroidFirebaseCrashReporter` using the native Firebase Android SDK directly, and a separate `IosFirebaseCrashReporter` using Objective-C/Swift interop against the native Firebase iOS SDK. This works, but it means writing and maintaining the same PII-scrubbing, allowlist, and consent logic (§9) twice, once per platform, in two different interop styles — exactly the kind of duplication risk that, per this project's own established pattern (see the sibling file `17-core-security-credential-hashing-algorithm-verification.md` §9.4), tends to be where security-relevant gaps quietly diverge between platforms over time.

**GitLive's `firebase-kotlin-sdk`** (`dev.gitlive:firebase-crashlytics`, published under group `dev.gitlive`) solves this directly: it ships a **single `commonMain` Kotlin API** — `dev.gitlive.firebase.Firebase.crashlytics` — that internally wraps the native Android Firebase Crashlytics SDK on the Android target and the native iOS Firebase Crashlytics SDK (via Kotlin/Native cinterop over CocoaPods) on the iOS target, presenting one identical call surface (`log()`, `recordException()`, `setCustomKey()`, `setUserId()`, `setCrashlyticsCollectionEnabled()`) to Kotlin code regardless of platform. This means `FirebaseCrashReporter` — including every scrubbing, allowlist, and consent rule in §9 — is written **once**, in `commonMain`, and is impossible to have drift between platforms, because there is only one implementation.

The only piece GitLive does **not** unify into a single call is Firebase *app initialization*, because that step is inherently platform-shaped (Android needs a `Context`; iOS needs `FirebaseApp.configure()` to have run before any Firebase API is touched). That one seam stays a small `expect`/`actual` (§3.3, §6.4) — everything downstream of it is common code.

### 3.2 GitLive Crashlytics API surface this implementation depends on

Confirm the exact method signatures against the installed `dev.gitlive:firebase-crashlytics` version's own KDoc/source at implementation time (Task 01, §13) — GitLive versions this wrapper independently of the native Firebase SDKs it wraps, and minor signature changes (nullability, added default parameters) do occur across releases. The API this document is written against, and expects to still be present in any reasonably current release:

```kotlin
package dev.gitlive.firebase.crashlytics

val Firebase.crashlytics: FirebaseCrashlytics

interface FirebaseCrashlytics {
    fun log(message: String)
    fun recordException(exception: Throwable)
    fun setCustomKey(key: String, value: String)          // + Boolean/Int/Long/Double/Float overloads
    fun setUserId(userId: String)
    fun setCrashlyticsCollectionEnabled(enabled: Boolean)
    suspend fun sendUnsentReports()
    suspend fun deleteUnsentReports()
    suspend fun didCrashOnPreviousExecution(): Boolean
}
```

### 3.3 The one remaining `expect`/`actual`: Firebase app initialization

```kotlin
// commonMain — com.noorheroes.core.crash.FirebaseCrashInit.kt
internal expect fun safeInitializeFirebase()
```

- **`androidMain` actual**: Android's Firebase SDK self-initializes via a `ContentProvider` the `google-services` Gradle plugin injects into the manifest — by the time any app code (including Koin's `startKoin`) runs, `FirebaseApp.getInstance()` already exists, *provided* `google-services.json` is present and the plugin is applied (§7). The `actual` here is defensive, not load-bearing: it calls GitLive's `Firebase.initialize(context)` inside a `runCatching {}`, which is safe to call even when auto-init has already happened (idempotent), and guarantees this module never assumes auto-init succeeded without a fallback attempt.
- **`iosMain` actual**: iOS has **no** auto-init mechanism — `FirebaseApp.configure()` (or GitLive's Kotlin-side `Firebase.initialize()`, which wraps the identical native call) must run before *any* Firebase API is touched, or every subsequent call throws. This `actual` calls GitLive's no-arg `Firebase.initialize()` inside `runCatching {}`. See §6.4 for why this document also recommends configuring Firebase from native Swift (`AppDelegate`) as the primary path, with this Kotlin-side call as a defense-in-depth idempotent fallback, not the sole initialization point.

Both `actual` implementations are called once, from inside each platform's `actual crashModule` (§6.6), before `FirebaseCrashReporter` is ever constructed — never from a feature module, never via `GlobalKoinHolder`.

---

## 4. Architecture and Component Responsibilities

```
Feature / UI Layer (unchanged — injects CrashReporter exactly as documented in CORE_CRASH_INSTRUCTIONS.md)
    ↓
NoorHeroesLogger (core-logger, unchanged)
    ↓
CrashReporter Interface (core-common, UNCHANGED — the seam this entire document works behind)
    ↑ implemented by (environment-selected in Koin, §6.6)
    ├── LoggerCrashReporter   (unchanged — debug/local builds; console println)
    ├── NoOpCrashReporter     (unchanged — unit tests; silent)
    └── FirebaseCrashReporter (NEW — this document's deliverable; release/production builds)
            ↓ scrubs via (NEW, self-contained inside core-crash — does NOT depend on core-logger's RedactionPipeline)
        CrashPiiScrubber / CrashCustomKeyAllowlist / ScrubbedThrowable
            ↓ calls
        dev.gitlive.firebase.Firebase.crashlytics  (GitLive KMP wrapper, commonMain, single implementation)
            ↓ delegates internally to (GitLive-owned, not this project's code)
        [Android target: native com.google.firebase:firebase-crashlytics SDK]
        [iOS target: native FirebaseCrashlytics.framework via CocoaPods/cinterop]
            ↓ initialized once, before first use, via
        safeInitializeFirebase()  (expect/actual, §3.3 — the ONLY per-platform code this document adds)
            ↓ uploads to
        Firebase Crashlytics Console (Google Cloud, per-project — the acceptance-test target, §14.4)
```

**Why `core-crash` cannot depend on `core-logger`'s `RedactionPipeline` (carried forward, not new):** `CORE_CRASH_INSTRUCTIONS.md` §2 states the existing, load-bearing architectural decision explicitly — *"The `CrashReporter` interface is in `core-common` so that `core-logger` can use it without depending on `core-crash`, while `core-crash` implements it without needing to know about `core-logger`'s internals."* `core-logger` depends on `core-crash`'s output type (`CrashReporter`) but not the reverse; if `FirebaseCrashReporter` imported `core-logger`'s `RedactionPipeline`, that would create exactly the circular module dependency this architecture was built to avoid (`core-logger → core-crash → core-logger`). This is why §9.2 specifies a second, self-contained scrubber living inside `core-crash` rather than reusing `core-logger`'s — a small, deliberate duplication of a *stable, narrow* regex set, traded against not breaking the module graph. This mirrors `LoggerCrashReporter`'s own documented reason for using `println` instead of the standard logger ("to prevent infinite recursion with the logging pipeline") — the same "stay decoupled from `core-logger` on purpose" instinct, applied to PII safety instead of recursion safety.

**Component responsibilities introduced by this document:**

| Component | Responsibility | New or Changed? |
|---|---|---|
| `CrashReporter` (interface, `core-common`) | `leaveBreadcrumb`, `recordNonFatal`, `setUserId`, `setCustomKey` | **Unchanged** — hard requirement (§2.2). |
| `FirebaseCrashReporter` | Concrete `CrashReporter` implementation delegating to `Firebase.crashlytics`, with scrubbing/allowlisting applied on every call. | **New.** |
| `CrashPiiScrubber` | Regex-based scrubbing of emails, phone numbers, JWTs, credit-card-shaped digit runs, and NoorHeroes-specific identifier patterns from any free-text string before it reaches Crashlytics. | **New**, self-contained in `core-crash`. |
| `CrashCustomKeyAllowlist` | Fail-closed registry of custom-key names `FirebaseCrashReporter.setCustomKey()`/`recordNonFatal(context=...)` are permitted to forward unredacted-as-a-key (values are still scrubbed). | **New.** |
| `ScrubbedThrowable` | Wraps a `Throwable` for `recordException()`, preserving stack trace and class name but replacing the exception's own `message` with a scrubbed copy. | **New.** |
| `CrashReportingConsent` | New, small, additive interface (`setCollectionEnabled(Boolean)`) for opt-out handling. Implemented by all three `CrashReporter` implementations. | **New**, additive — does not touch `CrashReporter`. |
| `safeInitializeFirebase()` (`expect`/`actual`) | One-time, defensive Firebase app initialization per platform. | **New.** |
| `crashModule` (`androidMain`/`iosMain` `actual`) | Environment-selects `LoggerCrashReporter` vs `FirebaseCrashReporter`; binds both `CrashReporter` and `CrashReportingConsent`. | **Changed** — this is the actual "swap," and it is entirely inside these two files. |
| `LoggerCrashReporter`, `NoOpCrashReporter` | Existing behavior for all `CrashReporter` methods. | **Unchanged behavior**; additive `CrashReportingConsent` no-op implementation only. |
| `CORE_CRASH_INSTRUCTIONS.md` | Documents the real binding. | **Corrected** (§13, Task 09). |

---

## 5. Folder / File Structure

```
core-crash/
  src/
    commonMain/kotlin/com/noorheroes/core/crash/
      LoggerCrashReporter.kt          # existing — additive: implements CrashReportingConsent (no-op)
      NoOpCrashReporter.kt            # existing — additive: implements CrashReportingConsent (no-op)
      FirebaseCrashReporter.kt        # NEW — the real binding
      CrashReportingConsent.kt        # NEW — new, additive interface
      CrashPiiScrubber.kt             # NEW — self-contained regex scrubbing
      CrashCustomKeyAllowlist.kt      # NEW — fail-closed key registry
      ScrubbedThrowable.kt            # NEW — throwable message scrubbing wrapper
      FirebaseCrashInit.kt            # NEW — expect fun safeInitializeFirebase()
      di/
        CrashModule.kt                # existing — expect val crashModule: Module (UNCHANGED signature)
    androidMain/kotlin/com/noorheroes/core/crash/
      FirebaseCrashInit.android.kt    # NEW — actual safeInitializeFirebase()
      di/
        CrashModule.android.kt        # MODIFIED — actual crashModule now environment-selects
    iosMain/kotlin/com/noorheroes/core/crash/
      FirebaseCrashInit.ios.kt        # NEW — actual safeInitializeFirebase()
      di/
        CrashModule.ios.kt            # MODIFIED — actual crashModule now environment-selects
    commonTest/kotlin/com/noorheroes/core/crash/
      CrashPiiScrubberTest.kt         # NEW
      CrashCustomKeyAllowlistTest.kt  # NEW
      ScrubbedThrowableTest.kt        # NEW
      FirebaseCrashReporterTest.kt    # NEW — tests scrubbing/allowlist wiring via a fake FirebaseCrashlytics, not the real SDK

composeApp/
  build.gradle.kts                    # MODIFIED — apply google-services + firebase-crashlytics Gradle plugins (Android target)
  src/androidMain/
    google-services.json              # NEW — Firebase project config (Android), NOT committed with real prod values to a public repo (§7.3)
  src/iosMain/                        # (or iosApp/, per project's actual Xcode project layout — confirm at Task 02)

iosApp/                               # native Xcode project wrapper (confirm exact name/location at Task 02)
  iosApp/GoogleService-Info.plist     # NEW — Firebase project config (iOS), added via Xcode "Add Files", must be in Copy Bundle Resources
  iosApp/AppDelegate.swift            # MODIFIED — calls FirebaseApp.configure() in didFinishLaunchingWithOptions
  Podfile                             # MODIFIED — pod 'FirebaseCrashlytics' (via Kotlin CocoaPods plugin, §7.4) or direct pod entry
  [Xcode project]                     # MODIFIED — new "Run Script" build phase for dSYM upload (§15.2)

gradle/libs.versions.toml             # MODIFIED — new [versions]/[libraries]/[plugins] entries for GitLive Firebase + google-services + firebase-crashlytics plugin

NoorHeroes/core/
  CORE_CRASH_INSTRUCTIONS.md          # MODIFIED — §5 and §8 corrected (exact diff in §13, Task 09)
```

**Note on exact file locations that must be confirmed, not assumed:** the corpus provided to this task documents `core-crash`'s package structure (§3 above, quoting `CORE_CRASH_INSTRUCTIONS.md` §3 verbatim) but does not name the exact Gradle module path for the Android application target, nor the exact iOS Xcode project/workspace layout (`iosApp/` vs. a differently-named wrapper, whether an `AppDelegate.swift` already exists or whether the project uses a SwiftUI `@main App` struct without one). **Task 02 (§13) requires locating these exact paths first** — the same "confirm before you build" discipline the sibling files in this phase (`16`, `17`) already establish for this codebase.

---

## 6. APIs, Models, Interfaces, and Data Flow

### 6.1 `CrashReporter` — unchanged interface (reconstructed from source doc usage examples; confirm exact signature at Task 01)

```kotlin
// core-common — com.noorheroes.core.common.crash — UNCHANGED, shown here for reference only
interface CrashReporter {
    fun leaveBreadcrumb(level: BreadcrumbLevel, tag: String, message: String)
    fun recordNonFatal(throwable: Throwable, context: Map<String, String> = emptyMap())
    fun setUserId(userId: String?)
    fun setCustomKey(key: String, value: String)
}

enum class BreadcrumbLevel { Debug, Info, Warning, Error }
```

### 6.2 `CrashReportingConsent` — new, additive interface

```kotlin
package com.noorheroes.core.crash

/**
 * Controls whether crash/breadcrumb data is actually transmitted off-device.
 * Deliberately a SEPARATE interface from [CrashReporter] — added so a settings/privacy
 * screen can toggle collection without adding a method to the interface every existing
 * CrashReporter consumer in the app already depends on (see gap-closure §2.2).
 */
interface CrashReportingConsent {
    /** Enables or disables data collection at the SDK level. Safe to call before or after init. */
    fun setCollectionEnabled(enabled: Boolean)
}
```

### 6.3 `CrashPiiScrubber` — new, self-contained regex scrubbing

```kotlin
package com.noorheroes.core.crash

/**
 * Independent, minimal PII scrubber for core-crash. Deliberately NOT a dependency on
 * core-logger's RedactionPipeline — see gap-closure §4 for why core-crash must not
 * depend on core-logger. This is intentional, narrow, stable-surface duplication, not
 * an oversight; a future refactor MAY hoist the shared regex patterns into core-common
 * if both modules' scrubbing needs converge further, but that is not required for this
 * Definition of Done and must not be attempted as a side effect of this document.
 */
internal object CrashPiiScrubber {
    private val EMAIL = Regex("""[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}""")
    private val JWT = Regex("""eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+""")
    private val PHONE = Regex("""\+?\d[\d\-\s()]{6,14}\d""")
    private val CREDIT_CARD = Regex("""\b(?:\d[ -]?){13,19}\b""")

    fun scrub(input: String): String = input
        .replace(JWT, "[REDACTED_JWT]")
        .replace(EMAIL, "[REDACTED_EMAIL]")
        .replace(CREDIT_CARD, "[REDACTED_CARD]")
        .replace(PHONE, "[REDACTED_PHONE]")
}
```

### 6.4 `CrashCustomKeyAllowlist` — new, fail-closed key registry

```kotlin
package com.noorheroes.core.crash

/**
 * Fail-closed registry of custom-key NAMES that FirebaseCrashReporter is permitted to
 * forward to Crashlytics. Mirrors core-logger's FieldAllowlist pattern (see
 * CORE_LOGGER_INSTRUCTIONS.md §7 "FieldAllowlist"). A key not on this list is dropped
 * silently — never forwarded, never logged as an error (dropping a diagnostic key must
 * never itself become a new source of noise or a new PII leak vector).
 *
 * Adding a key requires the same security review core-logger's FieldAllowlist requires.
 * NEVER add a key whose value could plausibly hold a child's name, a parent's name,
 * an email, a raw child-lock PIN, free-text Islamic-learning-content answers, or any
 * other user-generated text. Only structural/categorical metadata belongs here.
 */
internal object CrashCustomKeyAllowlist {
    val ALLOWED: Set<String> = setOf(
        "screen",                 // current screen/route name (e.g. "settings_privacy") — not user content
        "app_version",
        "build_type",             // "debug" | "release" | "internal"
        "environment",            // "staging" | "production"
        "locale",                 // e.g. "en-US" — device locale, not user-entered
        "network_status",         // "online" | "offline" | "metered"
        "subscription_tier",      // e.g. "free" | "premium" — categorical, not identifying
        "child_profile_count",    // an integer count, never a name
        "feature_flag_snapshot",  // a short, reviewed summary string, not raw config dump
        "session_id",             // opaque ULID, not tied to real-world identity by itself
    )

    fun isAllowed(key: String): Boolean = key in ALLOWED
}
```

### 6.5 `ScrubbedThrowable` — new, exception-message scrubbing wrapper

```kotlin
package com.noorheroes.core.crash

/**
 * Wraps [original] for transmission to Crashlytics: preserves the original class name and
 * stack trace (both essential for triage) but replaces the exception's own message with a
 * scrubbed copy, since an arbitrary caught exception's message (e.g. from a third-party
 * library, or an interpolated string built elsewhere in the app) is not guaranteed to be
 * PII-free just because it was "caught," and Crashlytics.recordException() otherwise
 * transmits that raw message verbatim.
 */
internal class ScrubbedThrowable(original: Throwable) : Throwable(
    message = original.message?.let { CrashPiiScrubber.scrub(it) },
    cause = null, // never chain the original — its cause chain may itself carry unscrubbed messages
) {
    init {
        stackTrace = original.stackTrace
    }
    override val message: String? = original.message?.let { CrashPiiScrubber.scrub(it) }

    companion object {
        /** Preserves the reported class name for Crashlytics grouping, via a synthetic subclass name is not needed —
         *  Crashlytics groups primarily by stack trace + this wrapper's own class; see gap-closure §9.6 for the
         *  documented, accepted trade-off this causes and why it is acceptable. */
    }
}
```

### 6.6 `FirebaseCrashReporter` — new concrete implementation

```kotlin
package com.noorheroes.core.crash

import com.noorheroes.core.common.crash.BreadcrumbLevel
import com.noorheroes.core.common.crash.CrashReporter
import dev.gitlive.firebase.Firebase
import dev.gitlive.firebase.crashlytics.crashlytics

internal class FirebaseCrashReporter : CrashReporter, CrashReportingConsent {

    override fun leaveBreadcrumb(level: BreadcrumbLevel, tag: String, message: String) {
        runCatching {
            val scrubbedMessage = CrashPiiScrubber.scrub(message)
            Firebase.crashlytics.log("[${level.name.uppercase()}][${tag}] $scrubbedMessage")
        }
        // Swallow ALL failures — see gap-closure §10.1: the crash reporter must never crash the app.
    }

    override fun recordNonFatal(throwable: Throwable, context: Map<String, String>) {
        runCatching {
            context.forEach { (key, value) ->
                if (CrashCustomKeyAllowlist.isAllowed(key)) {
                    Firebase.crashlytics.setCustomKey(key, CrashPiiScrubber.scrub(value))
                }
                // Non-allowlisted keys are silently dropped — fail-closed, per §9.3.
            }
            Firebase.crashlytics.recordException(ScrubbedThrowable(throwable))
        }
    }

    override fun setUserId(userId: String?) {
        runCatching {
            // Contract (unchanged, existing): callers pass an opaque account/session identifier
            // (e.g. a ULID from core-common's `id` package), never a raw email/name — see
            // gap-closure §9.4 for the defense-in-depth check applied here regardless.
            val safeId = userId?.let {
                if (looksLikeDirectPii(it)) "[REJECTED_PII_USER_ID]" else it
            } ?: ""
            Firebase.crashlytics.setUserId(safeId)
        }
    }

    override fun setCustomKey(key: String, value: String) {
        runCatching {
            if (!CrashCustomKeyAllowlist.isAllowed(key)) return@runCatching
            Firebase.crashlytics.setCustomKey(key, CrashPiiScrubber.scrub(value))
        }
    }

    override fun setCollectionEnabled(enabled: Boolean) {
        runCatching { Firebase.crashlytics.setCrashlyticsCollectionEnabled(enabled) }
    }

    private fun looksLikeDirectPii(value: String): Boolean =
        value.contains("@") || value.any { it.isWhitespace() }
        // A syntactically valid opaque ID (ULID/UUID) never contains "@" or whitespace;
        // this is a cheap shape check, not a substitute for the call-site contract.
}
```

### 6.7 `FirebaseCrashInit` — `expect`/`actual` initialization seam

```kotlin
// commonMain
package com.noorheroes.core.crash

internal expect fun safeInitializeFirebase()
```

```kotlin
// androidMain
package com.noorheroes.core.crash

import dev.gitlive.firebase.Firebase
import dev.gitlive.firebase.initialize
import android.content.Context

internal lateinit var androidAppContextForFirebase: Context // set once from crashModule, see §6.8

internal actual fun safeInitializeFirebase() {
    runCatching { Firebase.initialize(androidAppContextForFirebase) }
    // Idempotent-safe even though google-services' ContentProvider has usually already
    // auto-initialized Firebase by this point — see gap-closure §3.3.
}
```

```kotlin
// iosMain
package com.noorheroes.core.crash

import dev.gitlive.firebase.Firebase
import dev.gitlive.firebase.initialize

internal actual fun safeInitializeFirebase() {
    runCatching { Firebase.initialize() }
    // Defense-in-depth only — primary init is native Swift AppDelegate.FirebaseApp.configure(),
    // §6.4/§7.4/§13 Task 04. This call is a safety net if that native call is ever missed or
    // races, not the primary initialization path.
}
```

### 6.8 `crashModule` — `androidMain` `actual` (environment-selected)

```kotlin
package com.noorheroes.core.crash.di

import com.noorheroes.core.common.crash.CrashReporter
import com.noorheroes.core.crash.CrashReportingConsent
import com.noorheroes.core.crash.FirebaseCrashReporter
import com.noorheroes.core.crash.LoggerCrashReporter
import com.noorheroes.core.crash.androidAppContextForFirebase
import com.noorheroes.core.crash.safeInitializeFirebase
import org.koin.android.ext.koin.androidContext
import org.koin.dsl.bind
import org.koin.dsl.module

actual val crashModule = module {
    single {
        androidAppContextForFirebase = androidContext()
        val isDebugBuild = BuildConfig.DEBUG // confirm this exact reference at Task 03 — see gap-closure §11.2
        if (!isDebugBuild) safeInitializeFirebase()
        if (isDebugBuild) LoggerCrashReporter() else FirebaseCrashReporter()
    } bind CrashReporter::class bind CrashReportingConsent::class
}
```

### 6.9 `crashModule` — `iosMain` `actual` (environment-selected)

```kotlin
package com.noorheroes.core.crash.di

import com.noorheroes.core.common.crash.CrashReporter
import com.noorheroes.core.crash.CrashReportingConsent
import com.noorheroes.core.crash.FirebaseCrashReporter
import com.noorheroes.core.crash.LoggerCrashReporter
import com.noorheroes.core.crash.safeInitializeFirebase
import kotlin.native.Platform
import org.koin.dsl.bind
import org.koin.dsl.module

actual val crashModule = module {
    single {
        val isDebugBuild = Platform.isDebugBinary // confirm this API is appropriate for the project's
                                                    // Kotlin/Native version at Task 03 — see gap-closure §11.2
        if (!isDebugBuild) safeInitializeFirebase()
        if (isDebugBuild) LoggerCrashReporter() else FirebaseCrashReporter()
    } bind CrashReporter::class bind CrashReportingConsent::class
}
```

### 6.10 Data flow — a non-fatal error reported in production

```
Repository catches exception
    ↓
logger.logAppError(crashReporter, error, event = "fetch_failed")   ← core-logger, UNCHANGED call site
    ↓
logAppError() decides "Reportable" → calls crashReporter.recordNonFatal(AppErrorNonFatal, fields)
    ↓
crashModule provides FirebaseCrashReporter in this (production) build   ← THIS DOCUMENT's swap
    ↓
FirebaseCrashReporter.recordNonFatal():
    ├─ context map entries filtered through CrashCustomKeyAllowlist (non-allowlisted keys dropped)
    ├─ surviving values passed through CrashPiiScrubber.scrub()
    ├─ throwable wrapped in ScrubbedThrowable (message scrubbed, stack trace preserved)
    └─ Firebase.crashlytics.setCustomKey(...) × N, then Firebase.crashlytics.recordException(...)
            ↓
        GitLive delegates to native Android/iOS Firebase Crashlytics SDK
            ↓
        Uploaded (batched, per Firebase SDK's own scheduling) to the Firebase Crashlytics Console
```

---

## 7. Dependencies and Configuration Requirements

### 7.1 Infra prerequisite — a Firebase project must already exist

This document assumes a Firebase project has been created (Firebase Console → "Add project"), with **one Android app registration and one iOS app registration** added under it, matching the project's real applicationId/bundle identifier for each of its Android and iOS build variants (at minimum: production; strongly recommended: separate Firebase "apps" — not separate projects, unless the team's environment-isolation policy requires separate projects — for staging vs. production, so a forced test crash in `§14.4` never pollutes the production dashboard). **This provisioning step is called out here as an infra prerequisite, most naturally done alongside Phase 1 (`Development_Blueprints.Phase1_Infra_Config.Infra.*`), and is not itself a deliverable of this document** — if it has not happened yet, this document's Definition of Done (§17) cannot be reached, in exactly the same "blocked on an external prerequisite" shape as file `16`'s dependency on B-01 (§1.2 of that file).

### 7.2 Version catalog additions (`gradle/libs.versions.toml`)

```toml
[versions]
gitlive-firebase = "REPLACE_WITH_LATEST_STABLE"     # confirm current stable release compatible with the
                                                      # project's Kotlin/Compose Multiplatform version at Task 01
google-services-plugin = "REPLACE_WITH_LATEST_STABLE"
firebase-crashlytics-plugin = "REPLACE_WITH_LATEST_STABLE"

[libraries]
gitlive-firebase-common = { module = "dev.gitlive:firebase-common", version.ref = "gitlive-firebase" }
gitlive-firebase-crashlytics = { module = "dev.gitlive:firebase-crashlytics", version.ref = "gitlive-firebase" }

[plugins]
google-services = { id = "com.google.gms.google-services", version.ref = "google-services-plugin" }
firebase-crashlytics-gradle = { id = "com.google.firebase.crashlytics", version.ref = "firebase-crashlytics-plugin" }
```

**Do not hardcode a version number in this document as if it were final** — GitLive's `firebase-kotlin-sdk` and Google's Gradle plugins are both actively released; Task 01 (§13) requires the implementing agent to resolve the actual current stable versions compatible with the project's existing Kotlin/AGP/Compose Multiplatform versions before filling these in.

### 7.3 `core-crash/build.gradle.kts` — new dependencies

```kotlin
kotlin {
    sourceSets {
        commonMain.dependencies {
            implementation(project(":core:core-common"))
            implementation(libs.gitlive.firebase.common)
            implementation(libs.gitlive.firebase.crashlytics)
        }
        // No new androidMain/iosMain dependency block entries required — GitLive pulls the
        // native Android Firebase Crashlytics SDK transitively for the Android target; the
        // iOS target's native dependency is declared via CocoaPods (§7.4), not a Gradle dependency block.
    }
}
```

### 7.4 Root and app-module Gradle wiring (Android)

```kotlin
// root build.gradle.kts
plugins {
    alias(libs.plugins.google.services) apply false
    alias(libs.plugins.firebase.crashlytics.gradle) apply false
}
```

```kotlin
// composeApp/build.gradle.kts (the module that produces the Android application; confirm exact module
// name at Task 02 — some KMP+CMP layouts call this `androidApp`, others build the Android target
// directly inside `composeApp`)
plugins {
    id("com.google.gms.google-services")
    id("com.google.firebase.crashlytics")
}
```

- `google-services.json` (downloaded from the Firebase Console's Android app registration, §7.1) goes in the Android application module's root (typically `composeApp/google-services.json` — the same directory as that module's `build.gradle.kts`).
- **Secrets/config hygiene:** `google-services.json` is not a credential secret in the traditional sense (it identifies the app to Firebase, it does not authorize privileged writes), but per this project's own established secrets-handling posture (`Development_Blueprints.Phase1_Infra_Config.Infra.02-secrets-management-env-example-gitleaks.md`), confirm whether the project's convention is to commit this file directly (common and generally accepted for `google-services.json` specifically, since it is not a bearer secret) or to inject it via CI from a secrets store — **do not assume**; follow whatever that Phase 1 document's established convention for platform-config files already is.

### 7.5 iOS wiring — CocoaPods and native Firebase Crashlytics

```kotlin
// core-crash/build.gradle.kts (or wherever the project's Kotlin CocoaPods plugin is already configured
// for iOS interop — confirm at Task 02 whether this belongs in core-crash or a shared iOS-interop module)
kotlin {
    cocoapods {
        version = "1.0"
        summary = "core-crash Firebase Crashlytics binding"
        homepage = "https://noorheroes.app" // confirm actual project homepage/identifier convention
        ios.deploymentTarget = "REPLACE_WITH_PROJECT_MIN_IOS_VERSION" // match the project's existing minimum
        pod("FirebaseCrashlytics") {
            version = "REPLACE_WITH_VERSION_MATCHING_GITLIVE_RELEASE" // GitLive's release notes specify the
                                                                        // native Firebase iOS SDK version each
                                                                        // GitLive release was built/tested against
        }
    }
}
```

- `GoogleService-Info.plist` (downloaded from the Firebase Console's iOS app registration, §7.1) must be added to the Xcode project via **"Add Files to..."** (not just dropped into the filesystem) so it is included in the app target's **Copy Bundle Resources** build phase — a file present on disk but not in that build phase is silently ignored at runtime, and Crashlytics fails to initialize with no obvious error (this is the single most common iOS Firebase setup mistake; call it out explicitly in the PR/review checklist).
- `pod install` must be re-run in the iOS project directory after adding the `pod("FirebaseCrashlytics")` declaration and regenerating the Podfile via the Kotlin CocoaPods plugin.

### 7.6 iOS wiring — native `AppDelegate.swift`

```swift
import FirebaseCore

@main
class AppDelegate: UIResponder, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        FirebaseApp.configure()
        return true
    }
}
```

If the project's iOS entry point is a SwiftUI `@main App` struct without an `AppDelegate` today (confirm at Task 04, §13), add one via `@UIApplicationDelegateAdaptor` rather than attempting to call `FirebaseApp.configure()` from inside SwiftUI's `App.init()` directly — `didFinishLaunchingWithOptions` is the documented, supported point in the iOS app lifecycle for Firebase configuration, and configuring too late (e.g. after the first Compose UIViewController is presented) can produce intermittent, hard-to-reproduce Crashlytics initialization failures.

---

## 8. Database/Storage Requirements

No new database tables or schema — Crashlytics is a direct-to-cloud SDK integration; nothing is persisted by this document's code beyond what the native Firebase SDKs already manage internally on-device (their own small, OS-managed local queue for unsent reports, entirely outside this project's control or storage layer). The one piece of local state this document *reads* (not owns) is the consent/opt-out flag (§9.5), which is stored via the project's existing `PreferenceManager` (`core-common`) — this document does not introduce a new storage mechanism for that flag, it only specifies the key name and default value.

---

## 9. Authentication, Authorization, Validation, and Security Considerations

### 9.1 Why this section is non-negotiable for this specific closure

`println`-based `LoggerCrashReporter` never transmits anything off-device — its worst-case failure mode is noisy Logcat/Console output during development. **A real Crashlytics binding changes that fundamentally**: every string passed to `leaveBreadcrumb`, every `context` map passed to `recordNonFatal`, every exception's `.message`, and every `setCustomKey`/`setUserId` value now leaves the device and is stored by a third party (Google/Firebase). NoorHeroes is a **children's product**; PII discipline that was merely good practice for console-only output becomes a hard product-safety and regulatory requirement (COPPA-adjacent posture — a children's app must not transmit a child's name, a child's free-text content, or any other identifying data to a third-party analytics/crash SDK without deliberate, reviewed justification) the moment the destination becomes a real external service. This is why §2.2's "do not change the interface" constraint is paired with the requirement that the *implementation* behind that interface add real scrubbing — the interface staying the same does not mean the safety bar stays the same.

### 9.2 Explicit PII-scrubbing rules — mandatory, non-negotiable

**Every string this module ever hands to `Firebase.crashlytics` passes through `CrashPiiScrubber.scrub()` first, with no exception, regardless of whether the caller already redacted the value upstream.** This is deliberate defense-in-depth: `core-logger`'s call sites already redact before forwarding to `leaveBreadcrumb` (via `RedactionPipeline`), but **direct** caller code (a feature module calling `crashReporter.leaveBreadcrumb(...)` or `.recordNonFatal(...)` without going through `core-logger`) does **not** pass through `RedactionPipeline` at all — `FirebaseCrashReporter` cannot assume the caller redacted, and must never trust caller discipline alone for data leaving the device to a third party.

Concretely:

1. **Breadcrumb messages** (`leaveBreadcrumb`'s `message` parameter) — scrubbed before being handed to `Firebase.crashlytics.log()`.
2. **`recordNonFatal`'s `context` map values** — every value scrubbed; every **key** checked against `CrashCustomKeyAllowlist` first, and dropped entirely (not merely redacted) if not allowlisted.
3. **`setCustomKey`'s `value` parameter** — scrubbed; the `key` itself checked against the same allowlist.
4. **Exception messages** — never passed to `recordException()` raw; always wrapped in `ScrubbedThrowable` (§6.5) first, which scrubs the message while preserving the stack trace and class name Crashlytics needs for grouping and triage.
5. **`setUserId`** — never accepts a raw email, name, phone number, or other direct identifier by contract (existing, unchanged call-site rule per `CORE_CRASH_INSTRUCTIONS.md` §11's "Do" list: *"Redact PII: Ensure `message` and `context` do not contain emails, names, or cleartext IDs"*); `FirebaseCrashReporter` additionally applies a cheap shape check (§6.6, `looksLikeDirectPii`) as a last-resort catch, not as the primary control — the primary control remains: **callers must only ever pass an opaque account/session identifier (e.g. a ULID), never a human-meaningful value.**

**What scrubbing explicitly cannot catch, and why the rule is call-site discipline, not just regex:** free-text content a child or parent typed — a journal entry, a chat message, an Islamic-learning-content quiz answer, a display name typed at onboarding — does not match any of `CrashPiiScrubber`'s patterns (there is no reliable regex for "this string is a child's name" or "this string is Quranic-recitation-app user content"). **The binding rule, restated as a hard "Don't" for every future call site, not just this document's own code:**

> **Never pass raw user-generated text content — names, journal/chat text, learning-content answers, or any other freeform field a child or parent typed — into any `CrashReporter` method, ever, for any reason, even for debugging.** If a bug needs that content to reproduce, capture a **structural** description instead (e.g. `"child_lock_pattern_length_mismatch"` rather than the pattern itself; `"quiz_answer_validation_failed for question_id=42"` rather than the child's typed answer text). This is the single most important rule in this document and is enforced by code review, not by any automated scrubber, because no automated scrubber can reliably detect arbitrary freeform PII with acceptable false-negative risk for a children's product.

### 9.3 The custom-key allowlist is fail-closed by design

Mirrors `core-logger`'s `FieldAllowlist` pattern exactly (`CORE_LOGGER_INSTRUCTIONS.md` §7: *"Any field key not in this list is always redacted"*) — here, a non-allowlisted key is **dropped entirely** rather than redacted-in-place, since a custom key's *name itself* is visible in the Crashlytics dashboard as a column header even if its value were somehow scrubbed, and an ad hoc key name (e.g. `"child_first_name"` added by a well-intentioned engineer trying to debug a specific ticket) is itself a signal that should never reach a third-party dashboard even as a key name. Adding a new key to `CrashCustomKeyAllowlist.ALLOWED` requires the same security review discipline `FieldAllowlist` requires.

### 9.4 Where this document draws the line against becoming analytics

`CORE_CRASH_INSTRUCTIONS.md` §1 is explicit: *"What NOT to add to this module... Analytics: User behavior tracking belongs in `core-analytics`."* `setUserId`/`setCustomKey` exist so a specific crash can be correlated back to a specific session for **triage** (e.g., "this crash only happens for users on `subscription_tier=free`"), not to build a behavioral profile. `CrashCustomKeyAllowlist` is deliberately narrow and categorical (§6.4) — no engagement metrics, no feature-usage counts beyond the small structural set already listed, no funnel/session-duration data. If a future need arises for richer behavioral context, that belongs in `core-analytics` (a distinct module, out of scope here), not as an expanding `CrashCustomKeyAllowlist`.

### 9.5 Consent / opt-out handling

- **Default posture: crash-data collection is OFF until explicitly enabled.** `FirebaseCrashReporter.setCollectionEnabled(false)` is called immediately at construction time, before any other Crashlytics call, so the SDK never transmits anything by default.
- Collection is turned on only after confirming the project's actual parental-consent/privacy-policy acceptance flag — **confirm the exact existing preference key and consent flow with the team/PRD corpus before wiring this** (do not invent a new consent mechanism if one already exists from onboarding/parental-gate work); read it via `PreferenceManager` (`core-common`) and call `crashReportingConsent.setCollectionEnabled(hasConsent)` once, at app startup, after that flag is known, and again any time the user changes it from a privacy-settings screen.
- **Regardless of the exact key name**, the *default-safe* behavior specified above (collection OFF until a confirmed consent signal turns it on) is mandatory and is not itself something the implementing agent may skip or invert, even if the exact wiring to the project's real consent flag needs a follow-up confirmation.
- This is why `CrashReportingConsent` is a **separate interface** (§6.2/§2.1) — it lets a privacy/settings screen depend on exactly this one capability without widening the `CrashReporter` interface every other call site in the app already depends on.

### 9.6 Accepted trade-off: crash grouping under `ScrubbedThrowable`'s wrapper

Wrapping every recorded exception in `ScrubbedThrowable` (§6.5) means Crashlytics's automatic issue-grouping (which partly considers the exception's declared type in its heuristic, alongside the stack trace) sees `ScrubbedThrowable` as the "top" of the transmitted throwable rather than the original exception class in some SDK-internal presentations. This is an accepted, deliberate trade-off: the stack trace (the primary grouping signal) and the original message's *safe* content are both preserved; only the wrapper class name is synthetic. If this proves to meaningfully degrade triage quality in practice once real production data accumulates (§14.4's acceptance test is the first opportunity to observe this), a future refinement could set a custom key recording the original exception's simple class name (e.g. `"original_exception_type" → "IllegalStateException"`) — not required for this Definition of Done, noted here only so a future reviewer understands this was a considered choice, not an oversight.

---

## 10. Error Handling and Edge Cases

### 10.1 The crash reporter must never crash the app

Every public method on `FirebaseCrashReporter` wraps its entire body in `runCatching { }` and **swallows every failure silently** (§6.6). This is intentional and mirrors `LoggerCrashReporter`'s own existing discipline of using `println` specifically to avoid any risk of the reporting path itself becoming a new failure source. Concrete failure modes this protects against:

- **`google-services.json`/`GoogleService-Info.plist` missing or malformed** — `Firebase.initialize()`/auto-init throws or silently produces a non-functional `FirebaseApp`; every subsequent `Firebase.crashlytics.*` call would otherwise throw. `safeInitializeFirebase()`'s own `runCatching` (§6.7) absorbs the init failure, and every `FirebaseCrashReporter` method's own `runCatching` independently absorbs any resulting call failure — **two layers**, since init failure and per-call failure are different moments a real-world misconfiguration could surface at.
- **Network entirely unavailable** — GitLive/Firebase's native SDKs already queue reports locally and retry on their own schedule; this module makes no assumption about network state and never blocks or throws on an offline device.
- **SDK not yet initialized when the first call arrives** (a race between Koin building the `CrashReporter` singleton and Firebase's own async init completing on some platform edge case) — absorbed by the same `runCatching`; the call is simply a no-op for that one invocation rather than a startup crash.
- **`Platform.isDebugBinary` (iOS) or `BuildConfig.DEBUG` (Android) unavailable/renamed in a future Kotlin/AGP upgrade** — this is a compile-time reference, not a runtime one, so a breaking rename surfaces as a build failure, not a runtime crash; still worth flagging in code review whenever either toolchain is upgraded (§11.2).

### 10.2 What is explicitly NOT swallowed

`safeInitializeFirebase()` and every `FirebaseCrashReporter` method log nothing on failure via the standard logger (to avoid the same recursion risk `LoggerCrashReporter` already avoids by using `println` instead of `NoorHeroesLogger`) — but a `runCatching` result **may** optionally be inspected via `println` in local/debug context only, never in production, purely as a development aid; this must never call back into `NoorHeroesLogger` or `CrashReporter` from inside `FirebaseCrashReporter`'s own failure path, to avoid any risk of recursive failure loops.

### 10.3 Malformed/absent `context` map entries

`recordNonFatal`'s `context: Map<String, String> = emptyMap()` default already handles the no-context case without special-casing. An empty or all-non-allowlisted `context` map simply results in zero `setCustomKey` calls before `recordException` — never an error.

---

## 11. State Management and Lifecycle Considerations

### 11.1 Breadcrumb integration with `core-logger` — unchanged code, changed runtime effect

No code changes are required in `core-logger` for this document — its existing `NoorHeroesLoggerImpl` already calls `crashReporter.leaveBreadcrumb(...)` (via `Severity.toBreadcrumbLevel()`) for every log line at or above whatever threshold that pipeline is configured for. **The behavior change this document introduces is entirely downstream of that call**: once `crashModule` starts providing `FirebaseCrashReporter` instead of `LoggerCrashReporter` in production builds, those same, already-redacted (`RedactionPipeline`-scrubbed) log-derived breadcrumbs now genuinely accumulate inside Crashlytics's per-session breadcrumb trail, visible on the dashboard alongside any eventual crash/non-fatal from that same session — this is the entire point of the "breadcrumb" concept and requires no new wiring beyond the `crashModule` swap itself (§6.8/§6.9).

### 11.2 Debug/local builds keep the existing `LoggerCrashReporter` — this is a hard requirement, not an incidental default

Per the task brief's explicit instruction, this closure **must not** replace `LoggerCrashReporter` outright — the environment-selection logic in §6.8/§6.9 is the mechanism that keeps it fully available:

- Android: `BuildConfig.DEBUG` (confirm this exact reference exists already in the project's `composeApp`/Android module at Task 03 — some projects gate this differently, e.g. a custom `BuildConfig` field or Gradle build-type name check; do not assume `BuildConfig.DEBUG` is accessible from `core-crash` without first confirming `core-crash`'s Android source set can see the application module's generated `BuildConfig`, or whether a dedicated `expect val isDebugBuild: Boolean` should instead be defined in `core-common`'s `config` package for this purpose — if such a flag already exists there for other reasons, per `CORE_COMMON_INSTRUCTIONS.md`'s `config` package description ("App-wide constants, feature flag defaults, and environment config"), reuse it instead of introducing a second one).
- iOS: `kotlin.native.Platform.isDebugBinary` — confirm this stdlib API is present and behaves as expected against the project's actual Kotlin/Native version at Task 03; if unavailable, fall back to the same `core-common` environment-config flag suggested above for Android, applied uniformly on iOS too, so both platforms key off one consistent signal rather than two different mechanisms.
- Regardless of which exact mechanism is confirmed, the **outcome** is fixed by this document: local/debug builds get `LoggerCrashReporter` (unchanged console behavior, zero data ever leaves the device), and only release/production builds get `FirebaseCrashReporter`. This also incidentally means a developer running a debug build never needs a working Firebase configuration at all to build and run the app locally — `safeInitializeFirebase()` is only invoked in the non-debug branch (§6.8/§6.9), so a missing `google-services.json` on a fresh local checkout does not block local development (confirm this is actually desired; if the team wants Firebase-in-debug-too for local dashboard testing, that is a one-line change to the branch condition, but is not this document's default recommendation).

### 11.3 Lifecycle — when initialization happens

`safeInitializeFirebase()` runs exactly once, synchronously, inside the `single { }` Koin definition block the first time `CrashReporter` (or `CrashReportingConsent`) is resolved from the Koin graph — i.e., whenever `initKoin()`'s modules are first built, which per `CORE_COMMON_INSTRUCTIONS.md` §4.1's `appScope`/`GlobalKoinHolder` context happens once, at app startup, before any feature module resolves its own dependencies. No lazy re-initialization, no per-call re-init check beyond the `runCatching` safety net (§10.1).

---

## 12. Integration Points with Existing Modules

### 12.1 `core-logger` — breadcrumb forwarding (already-built wiring, now genuinely effective)

As covered in §11.1: `core-logger`'s existing `crashReporter.leaveBreadcrumb(...)` calls, and its `logAppError()` → `recordNonFatal()` classification bridge, require **zero code changes**. The only consequence of this document landing is that those calls, in production builds, now reach a real backend instead of `println`. Any team member reviewing this closure should understand: **this document does not touch `core-logger` at all** — it only changes what sits behind the interface `core-logger` already calls into.

### 12.2 `composeApp` — Koin wiring

`composeApp`'s `initKoin()` (or platform-specific `initKoin(...)` entry points) already include `crashModule` per `CORE_CRASH_INSTRUCTIONS.md` §8 ("Used in the main Koin `initKoin` function to provide the `CrashReporter` binding"). **No change is required in `composeApp`'s module-list wiring** — `crashModule` is still included exactly as before; only its internal contents (inside `core-crash`'s own `androidMain`/`iosMain`, §6.8/§6.9) change. The one new integration point in `composeApp` is optional and additive: any privacy/settings screen that needs to let a parent toggle crash-data collection can now inject `CrashReportingConsent` (a new, separate Koin binding, §6.2) alongside its existing `CrashReporter` injections elsewhere in the app — this is new capability, not a required change to any existing screen.

### 12.3 `core-common` — no changes, one possible reuse

§11.2 flags a possible reuse of `core-common`'s existing `config` package for an `isDebugBuild`-style flag, **if** one is not already accessible the simpler way (`BuildConfig.DEBUG` on Android, `Platform.isDebugBinary` on iOS). This is a "confirm and reuse if present" note, not a mandated new addition to `core-common` — do not add a new flag to `core-common` unless Task 03 (§13) confirms the simpler platform-native mechanisms are unavailable or unreliable in this project's actual toolchain.

### 12.4 Feature modules — zero required changes

Every feature module today calls `crashReporter.leaveBreadcrumb(...)`, `.recordNonFatal(...)`, `.setUserId(...)`, `.setCustomKey(...)` via constructor-injected `CrashReporter`, per `CORE_CRASH_INSTRUCTIONS.md` §9's "Allowed" list. None of these call sites require any change — the entire point of this closure is that the interface they already depend on now has a real implementation behind it in production, transparently.

---

## 13. Development Steps in the Correct Implementation Order

**Task 01 — Confirm the exact `CrashReporter`/`BreadcrumbLevel` signatures and current `crashModule`/`LoggerCrashReporter`/`NoOpCrashReporter` source.**
Locate and read the real source files (`grep -r "interface CrashReporter" core-common/src/`, `grep -r "class LoggerCrashReporter" core-crash/src/`) — this document reconstructed the interface from usage examples in `CORE_CRASH_INSTRUCTIONS.md` (§6.1); confirm against the real file before writing `FirebaseCrashReporter`, since an implementation written against a slightly-wrong reconstructed signature will fail to compile or, worse, silently satisfy a different contract than the real one.

**Task 02 — Confirm the project's exact module/file layout for the Android application module and the iOS Xcode project.**
Determine the exact Gradle module that produces the Android APK (`composeApp` vs. a separate `androidApp`), and the exact iOS wrapper project's structure (`iosApp/` name, whether `AppDelegate.swift` exists today or the entry point is a SwiftUI `@main App` struct, and where the Kotlin CocoaPods plugin, if any, is already configured). Do not assume; §5's structure block is written from the project's stated stack ("KMP/Compose Multiplatform") but the exact paths must be confirmed against the real repository.

**Task 03 — Confirm (or introduce, per §11.2/§12.3) the debug-vs-release detection mechanism for both platforms.**
Confirm `BuildConfig.DEBUG` is reachable from `core-crash`'s `androidMain` source set, and that `kotlin.native.Platform.isDebugBinary` exists and behaves as expected in the project's actual Kotlin/Native version. Fall back to a shared `core-common` flag only if neither platform-native mechanism is confirmed usable.

**Task 04 — Provision or confirm the Firebase project and download platform config files (§7.1).**
If a Firebase project does not yet exist, this blocks the rest of this task list from reaching a fully verifiable state (Tasks 05–09 can still be written/compiled, but §14's acceptance test cannot run) — flag this to the team immediately rather than proceeding on an assumed/placeholder project. Download `google-services.json` and `GoogleService-Info.plist` from the real project's Android/iOS app registrations.

**Task 05 — Add the GitLive Firebase + Google Services + Firebase Crashlytics Gradle dependencies and plugins (§7.2–§7.4).**
Resolve real, current version numbers (do not use this document's placeholder strings verbatim). Confirm the resolved GitLive `firebase-crashlytics` release's documented compatible native Firebase iOS SDK version before pinning the CocoaPods `pod("FirebaseCrashlytics")` version (§7.5).

**Task 06 — Implement `CrashPiiScrubber`, `CrashCustomKeyAllowlist`, `ScrubbedThrowable`, `CrashReportingConsent` (§6.2–§6.5).**
Pure Kotlin, `commonMain`, no Firebase dependency — write and unit-test these in isolation first (§14.1), before touching `FirebaseCrashReporter` itself, so scrubbing/allowlist correctness is verified independent of any SDK integration risk.

**Task 07 — Implement `FirebaseCrashInit` (`expect`/`actual`) and wire the Android `AppDelegate`-equivalent / iOS `AppDelegate.swift` native init (§6.7, §7.6).**
Get Firebase initializing successfully on both platforms (verify via `Firebase.crashlytics.didCrashOnPreviousExecution()` returning without throwing, as a smoke check) before writing `FirebaseCrashReporter` itself.

**Task 08 — Implement `FirebaseCrashReporter` (§6.6) and update both `actual crashModule` definitions (§6.8, §6.9).**
Confirm both `LoggerCrashReporter` and `NoOpCrashReporter` now additionally implement `CrashReportingConsent` (a small, additive change to each, per §2.2) before wiring the `bind CrashReporter::class bind CrashReportingConsent::class` Koin definitions, since the Koin `single { }` block's return type must satisfy both bound interfaces across every branch of the environment-selection `if`.

**Task 09 — Correct `CORE_CRASH_INSTRUCTIONS.md` §5 and §8.**
Replace §8's "Future: Firebase Crashlytics" / "Future: Native iOS crash handler with symbolication" lines with the real, current binding description, and add `FirebaseCrashReporter` and `CrashReportingConsent` to §5's Implementation Classes list — mirrors the doc-correction discipline the sibling file `17` establishes at its own §9.4/§15 for the identical reason (a module's own reference documentation must not describe a resolved gap as still-open once it is closed).

**Task 10 — Run the full test suite (§14.1–§14.3), then perform the manual forced-crash acceptance test against the real Firebase Crashlytics console (§14.4).**

---

## 14. Testing Strategy and Acceptance Criteria

### 14.1 Unit tests — `CrashPiiScrubber`, `CrashCustomKeyAllowlist`, `ScrubbedThrowable`

Pure Kotlin, `commonTest`, no Firebase/SDK involvement:

- `CrashPiiScrubberTest`: assert emails, JWT-shaped strings, phone-number-shaped digit runs, and credit-card-shaped digit runs are replaced with their respective `[REDACTED_*]` markers; assert non-matching structural strings (e.g. `"screen=settings_privacy"`) pass through unchanged.
- `CrashCustomKeyAllowlistTest`: assert every key in §6.4's `ALLOWED` set returns `true`; assert an arbitrary invented key (e.g. `"child_first_name"`) returns `false`.
- `ScrubbedThrowableTest`: construct a `Throwable` with a PII-shaped message and a known stack trace; assert the resulting `ScrubbedThrowable`'s `.message` is scrubbed and its `.stackTrace` is identical (by content) to the original.

### 14.2 Unit tests — `FirebaseCrashReporter` behavior, via a fake `FirebaseCrashlytics`

Since `Firebase.crashlytics` is a real singleton wrapping a native SDK, do not attempt to unit-test `FirebaseCrashReporter` against the real SDK in `commonTest`. Instead, restructure `FirebaseCrashReporter` (or provide a thin seam) so its scrubbing/allowlist/consent **decision logic** is testable independent of the actual `Firebase.crashlytics.*` calls — e.g., extract a small internal pure function that computes "what would be sent" (the final scrubbed message string, the final allowlist-filtered custom-key map) from raw inputs, and unit-test *that* function directly; the thin wrapper around `Firebase.crashlytics.*` itself is then a one-line pass-through verified only by the manual acceptance test (§14.4), consistent with the general KMP testing principle of not unit-testing third-party SDK internals.

- Assert `recordNonFatal` with a `context` map containing both allowlisted and non-allowlisted keys results in only the allowlisted keys' scrubbed values being forwarded.
- Assert `leaveBreadcrumb` with a PII-shaped message results in a scrubbed message being forwarded.
- Assert `setUserId` with an email-shaped or whitespace-containing string is rejected (`looksLikeDirectPii` catches it) while a ULID-shaped opaque string passes through unchanged.
- Assert every public method, when the underlying `Firebase.crashlytics` call is stubbed to throw, does not propagate the exception (verifies the `runCatching` contract of §10.1).

### 14.3 Integration/smoke test — Firebase initializes without throwing

On both platforms, in a build variant with a real (even if staging-only) `google-services.json`/`GoogleService-Info.plist` present, confirm `safeInitializeFirebase()` followed by `Firebase.crashlytics.didCrashOnPreviousExecution()` completes without throwing — this is the cheapest possible signal that configuration files, Gradle plugins, and CocoaPods wiring are all correctly in place, before attempting the full forced-crash acceptance test.

### 14.4 Acceptance criteria — a deliberately forced test crash appears in the Firebase Crashlytics console

This is the binding, observable Definition-of-Done signal for this entire document (§17):

1. In a build variant that resolves to the `FirebaseCrashReporter` branch (i.e., a **release** or **internal/staging** build — not a debug build, per §11.2), add a temporary, clearly-labeled test-only trigger (e.g., a hidden developer-menu action reachable only in that non-debug-but-not-production-distributed build variant) that does:
   ```kotlin
   throw RuntimeException("NoorHeroes Crashlytics verification — forced test crash, safe to ignore")
   ```
   — a genuine **fatal** crash (not `recordNonFatal`), so the test exercises the real fatal-crash-capture path, not only the non-fatal-reporting path already covered by §14.2.
2. Let the app actually crash and terminate. **Relaunch the app once** — Crashlytics's native SDKs write the crash report to local disk at the moment of the crash but upload it on the *next* process start, per both platforms' standard Crashlytics behavior; a crash observed only via a debugger attached at the moment of the crash, or a process that is force-quit and never relaunched, does not upload.
3. Wait a few minutes (Crashlytics console processing time is not instantaneous) and confirm the crash appears in the real Firebase Crashlytics console for the correct Firebase project/app, with a non-empty, non-garbled stack trace (correct dSYM/mapping-file symbolication, §15) and the test's identifying message text visible.
4. Repeat the same forced-crash test on **both** Android and iOS independently — a pass on one platform is not evidence the other platform's native wiring (dSYM upload, CocoaPods, `AppDelegate.configure()`) is also correct; both must be independently confirmed.
5. Remove the temporary test-trigger code before this branch is considered mergeable to a shipping release configuration — it must never be reachable in a real production build users receive (the internal/staging-only build-variant gating in step 1 is the control that prevents this; confirm it actually holds before merging).
6. Confirm a **non-fatal** (`recordNonFatal`) also appears correctly on the console, exercising §6.10's data flow end-to-end, including that a custom key set beforehand (e.g. `"screen" → "settings_privacy"`) is visible attached to that non-fatal event, and that no non-allowlisted key or unscrubbed PII-shaped string appears anywhere in the reported event — this is the acceptance check for §9's scrubbing/allowlist rules actually holding in the real product, not merely in unit tests against fakes.

---

## 15. Production-Readiness Considerations

### 15.1 Android — ProGuard/R8 mapping file upload

The `com.google.firebase.crashlytics` Gradle plugin (§7.4), once applied to the Android application module, automatically uploads the ProGuard/R8 obfuscation mapping file to Firebase as part of each release build's assembly, so obfuscated stack traces de-obfuscate correctly in the console. Confirm this upload task is actually wired into the project's existing release/CI build pipeline (`Development_Blueprints.Phase1_Infra_Config.CI_CD.06-ci-pipeline-lint-test-build-stages.md`) — the plugin adds a Gradle task (`uploadCrashlyticsMappingFileRelease` or equivalently named per the plugin's current version) that must actually run as part of the release build, not be skipped by a `--offline`/cache-only CI configuration that might otherwise bypass network-dependent tasks.

### 15.2 iOS — dSYM upload

Firebase Crashlytics's iOS SDK requires uploading the build's dSYM (debug symbols) file so native stack traces symbolicate correctly. Add the standard Firebase-provided "Run Script" Xcode build phase (`${PODS_ROOT}/FirebaseCrashlytics/run`, when the pod is integrated via CocoaPods per §7.5) to the app target's build phases, positioned **after** the "Copy Bundle Resources" phase (so `GoogleService-Info.plist` is already present when the script runs) — confirm the exact script path/invocation against the version of `FirebaseCrashlytics` actually resolved (Task 05), since the script's exact CocoaPods-relative path can shift between major SDK versions. Confirm the project's iOS CI build pipeline (release/TestFlight/App Store builds) actually runs this script — a dSYM upload that only happens on a developer's local Xcode build and never in CI means every CI-built release ships with unsymbolicated production crashes.

### 15.3 Crash-free-users monitoring as a release gate (recommendation, not a hard DoD item)

Once this closure ships and a few production releases have accumulated real crash data, consider wiring the Firebase Crashlytics "crash-free users" metric into whatever release-health dashboard the project's `Development_Blueprints.Phase11_CICD_Deployment` / `Development_Blueprints.Phase12_Production_Readiness` documents already establish, so a regression in crash-free rate can gate or flag a release. This is a natural next step this document's binding enables, not a requirement of this document's own Definition of Done (§17).

### 15.4 Cost/quota awareness

Firebase Crashlytics itself is free (no usage-based billing) at the product level, but confirm the Firebase project's overall plan (Spark vs. Blaze) if any *other* Firebase product sharing the same project has usage-based costs — out of scope for this document's own implementation, but worth a one-line confirmation during Task 04 so this closure is not mistakenly blocked on an unrelated billing-plan decision.

---

## 16. Dependencies/Prerequisites

- **`core-common`** — already built; provides the unchanged `CrashReporter` interface and `BreadcrumbLevel` enum this document implements against.
- **`core-crash`'s existing abstraction layer** (`LoggerCrashReporter`, `NoOpCrashReporter`, the `crashModule` `expect`/`actual` seam) — already built; this document adds to it, does not rebuild it.
- **A Firebase project, with Android and iOS app registrations already created** — infra prerequisite, most naturally provisioned alongside Phase 1 (`Development_Blueprints.Phase1_Infra_Config.*`); **blocks this document's Definition of Done (§17) if not yet done**, in the same shape file `16`'s DoD is blocked on B-01.
- **GitLive `firebase-kotlin-sdk`** (`dev.gitlive:firebase-common`, `dev.gitlive:firebase-crashlytics`) — external, actively maintained third-party KMP wrapper; version compatibility with the project's Kotlin/Compose Multiplatform version must be confirmed at implementation time (Task 01/05), not assumed from this document.
- **Google's `google-services` and `com.google.firebase.crashlytics` Gradle plugins** (Android) and the native `FirebaseCrashlytics` CocoaPod (iOS) — external, Google-maintained.

---

## 17. Definition of Done

- [ ] `FirebaseCrashReporter`, `CrashPiiScrubber`, `CrashCustomKeyAllowlist`, `ScrubbedThrowable`, `CrashReportingConsent`, and `safeInitializeFirebase()`/its `actual`s are implemented exactly as specced (or with confirmed, documented deviations resolved during Tasks 01–03) in `core-crash`.
- [ ] `CrashReporter`'s public interface in `core-common` is provably unchanged (no diff to that file, or a diff limited to comments/KDoc only).
- [ ] Both `androidMain` and `iosMain` `actual crashModule` definitions environment-select `LoggerCrashReporter` (debug/local) vs. `FirebaseCrashReporter` (release/production), and both bind `CrashReporter` and `CrashReportingConsent`.
- [ ] `LoggerCrashReporter` and `NoOpCrashReporter` continue to behave identically for every existing `CrashReporter` method, with only an additive, no-op `CrashReportingConsent` implementation added to each.
- [ ] `google-services.json` and `GoogleService-Info.plist` are correctly wired for at least one non-production Firebase app registration (staging), and the Android/iOS Gradle/CocoaPods/Xcode configuration changes in §7 are all in place.
- [ ] All unit tests in §14.1–§14.2 pass.
- [ ] §14.3's initialization smoke test passes on both platforms.
- [ ] §14.4's forced-test-crash acceptance test is performed and confirmed on **both** Android and iOS independently, with correctly symbolicated stack traces (confirming §15.1/§15.2's mapping-file/dSYM upload actually work), and the temporary test-trigger code is removed afterward.
- [ ] §9.2's scrubbing rules and §9.3's allowlist are confirmed holding against the real forced-crash test's console output (no unscrubbed PII-shaped string, no non-allowlisted key, visible in the Firebase Crashlytics console).
- [ ] §9.5's default-off consent posture is implemented and wired to the project's real (confirmed, not invented) consent/privacy-policy flag.
- [ ] `CORE_CRASH_INSTRUCTIONS.md` §5 and §8 are corrected to describe the real, implemented binding.
- [ ] A CI release build (per §15.1/§15.2) successfully uploads the ProGuard/R8 mapping file (Android) and dSYM (iOS) as part of its normal pipeline, not only via a manual local build.

---

## 18. Assumptions or Decisions the Coding Agent Must Follow

1. **The `CrashReporter` interface must not change.** If, during Task 01, the real interface's exact signature differs from §6.1's reconstruction, implement `FirebaseCrashReporter` against the *real* signature — do not modify the interface to match this document's reconstruction.
2. **`LoggerCrashReporter` remains fully available and is the binding used for local/debug builds** — this is a hard requirement from the task brief, not a suggestion; do not remove it, do not make `FirebaseCrashReporter` the unconditional binding on any platform.
3. **`core-crash` must not gain a dependency on `core-logger`** — `CrashPiiScrubber` is deliberately self-contained and duplicates a narrow, stable regex set rather than reusing `core-logger`'s `RedactionPipeline`, to preserve the existing, documented no-circular-dependency architecture (§4).
4. **Never pass raw user-generated free text (names, chat/journal content, learning-content answers) to any `CrashReporter` method** — this is a call-site discipline rule that scrubbing cannot fully enforce automatically (§9.2); the coding agent must not introduce any new call site in the app that violates this while implementing or testing this document.
5. **The custom-key allowlist is fail-closed** — when in doubt about whether a new key should be added, do not add it; escalate for review rather than defaulting to permissive.
6. **Default crash-data collection to OFF** until a confirmed consent signal enables it (§9.5) — do not default to ON "to make testing easier"; use the manual §14.4 test flow (which explicitly enables collection for that test) instead.
7. **Do not hardcode placeholder version numbers from this document as final** — §7.2, §7.5's version strings are explicitly marked as placeholders requiring real resolution at implementation time.
8. **Confirm exact module/file paths before writing platform config-wiring code** (§13, Task 02) — this document's Android/iOS file-layout guesses are reasonable defaults for a "KMP + Compose Multiplatform" project shape but are not guaranteed to match the real repository without verification.
9. **The forced test-crash trigger (§14.4) is temporary test code and must be removed before merge to any branch that produces a real production release build.**

---

## AI Agent Development Prompt

You are implementing a **gap-closure** change to the already-built `core-crash` KMP module in the NoorHeroes project. Read `NoorHeroes/core/core-crash/CORE_CRASH_INSTRUCTIONS.md` in full first — it documents the existing, already-implemented `CrashReporter` interface (`core-common`), the `BreadcrumbLevel` enum, the existing `LoggerCrashReporter`/`NoOpCrashReporter` implementations, and the `crashModule` `expect`/`actual` Koin seam. **Do not re-implement or restructure any of that** — it already works and is in production use by every feature module in the app.

**What you are building:** a real `FirebaseCrashReporter` implementation of the existing, unchanged `CrashReporter` interface, using the GitLive Kotlin Multiplatform Firebase wrapper (`dev.gitlive:firebase-crashlytics`), wired for both Android and iOS, with PII scrubbing, a fail-closed custom-key allowlist, and default-off consent handling — because this is a children's product and, unlike the current console-only `LoggerCrashReporter`, this new implementation transmits data to a real third-party service (Firebase).

**What you must NOT change:**
- The `CrashReporter` interface's method signatures in `core-common` — zero changes.
- `LoggerCrashReporter`'s or `NoOpCrashReporter`'s existing behavior for any `CrashReporter` method — the only change permitted to either file is adding a no-op implementation of the new `CrashReportingConsent` interface.
- Anything in `core-logger` (`RedactionPipeline`, `FieldAllowlist`, `logAppError()`, the breadcrumb-forwarding call into `CrashReporter`) — this closure works entirely behind the interface `core-logger` already calls.
- `composeApp`'s Koin module list — `crashModule` is already wired in; only its internal contents inside `core-crash` change.

**Implementation order:**
1. Read the real `CrashReporter`/`BreadcrumbLevel` source and the real `LoggerCrashReporter`/`NoOpCrashReporter`/`crashModule` source — confirm this document's §6.1 reconstruction matches; if not, implement against the real signature.
2. Confirm the project's real Android application module path and iOS Xcode project structure (does an `AppDelegate.swift` already exist?).
3. Confirm the debug-vs-release detection mechanism available on each platform (`BuildConfig.DEBUG` on Android, `kotlin.native.Platform.isDebugBinary` on iOS, or an existing `core-common` config flag if neither is directly usable).
4. Confirm a Firebase project exists with Android + iOS app registrations (staging, at minimum); download `google-services.json`/`GoogleService-Info.plist`. If no Firebase project exists yet, flag this blocker immediately — it prevents reaching this document's Definition of Done.
5. Add the GitLive Firebase (`firebase-common`, `firebase-crashlytics`), `google-services`, and `com.google.firebase.crashlytics` Gradle dependencies/plugins, resolving real current version numbers.
6. Implement `CrashPiiScrubber`, `CrashCustomKeyAllowlist`, `ScrubbedThrowable`, and `CrashReportingConsent` in `commonMain` — pure Kotlin, no SDK dependency — and unit-test them first, in isolation.
7. Implement `safeInitializeFirebase()` (`expect`/`actual`) and wire native Firebase init: `google-services` auto-init on Android (defensive `Firebase.initialize(context)` call as backup), and an explicit `FirebaseApp.configure()` call in iOS's `AppDelegate.didFinishLaunchingWithOptions` (add an `AppDelegate` via `UIApplicationDelegateAdaptor` if the project's iOS entry is a bare SwiftUI `@main App` struct today) plus a defensive Kotlin-side `Firebase.initialize()` call.
8. Implement `FirebaseCrashReporter` (implements both `CrashReporter` and `CrashReportingConsent`), wrapping every method body in `runCatching { }` so a Crashlytics SDK failure can never crash the app, applying `CrashPiiScrubber`/`CrashCustomKeyAllowlist`/`ScrubbedThrowable` on every outbound value, and defaulting collection to OFF at construction.
9. Update both `androidMain`/`iosMain` `actual crashModule` definitions to environment-select `LoggerCrashReporter` vs. `FirebaseCrashReporter`, binding both `CrashReporter` and `CrashReportingConsent` via Koin.
10. Add the Android ProGuard/R8 mapping-file upload (automatic via the Crashlytics Gradle plugin — confirm it actually runs in CI) and the iOS dSYM-upload Xcode Run Script build phase; confirm both are wired into the project's actual CI release pipeline, not just a local build.
11. Correct `CORE_CRASH_INSTRUCTIONS.md` §5 and §8 to describe the real binding instead of "Future."
12. Run all unit tests (scrubber, allowlist, wrapped-throwable, `FirebaseCrashReporter` decision-logic tests against a fake, not the real SDK).
13. Perform the manual acceptance test: in a non-debug (staging/internal) build, trigger a genuine forced fatal crash via a temporary, clearly-labeled test-only trigger, relaunch the app once, and confirm the crash appears in the real Firebase Crashlytics console with a correctly symbolicated stack trace — on **both** Android and iOS independently. Also confirm a forced `recordNonFatal` call appears correctly, with an allowlisted custom key visible and no unscrubbed PII-shaped content anywhere in the event. Remove the temporary test-trigger code afterward.

**Verify before declaring this done:**
- `grep` confirms zero diff to `CrashReporter`'s interface file in `core-common` (aside from possible comment-only changes).
- Every existing call site across the app (`grep -r "crashReporter\." --include="*.kt"`) still compiles unmodified.
- A debug build never requires a valid Firebase configuration to build or run locally (the debug branch never calls `safeInitializeFirebase()` or constructs `FirebaseCrashReporter`).
- The forced-crash test's stack trace is legible (not `<compiler-generated>`/hex-only), proving mapping/dSYM upload actually worked, on both platforms independently.
- No non-allowlisted custom key and no unscrubbed PII-shaped string appears anywhere in the acceptance test's Crashlytics console output.
