# Phase 3 — core-security: CredentialHasher Algorithm Verification & Alignment (Gap Closure)

## 0. Document Metadata

| Field | Value |
|---|---|
| Phase | Phase 3 — Shared Core Modules (KMP) |
| Blueprint ID | Phase3_Shared_Core_Modules.KMP.17 |
| Surface | KMP (`core-security` module, Android + iOS actuals) |
| Status this closes | `core-security` is 🟡 **COMPLETED (partial)** — module built and in production use by A.1/C.19, but `CredentialHasher`'s hashing-algorithm choice was left undocumented-as-a-decision. This file makes it a decision. |
| Depends on | F.37 B-04 — Slow-Hash Credential Storage Utility (Backend, already implemented — `src/noorheroes/common/security/credential_hasher.py`, Argon2id); `core-security` module (already implemented, `com.noorheroes.core.security.*`) |
| Also cross-references (do not re-implement) | F.37 KMP K-01 — Keystore-Backed Credential-Caching Architectural Scan (`Development_Blueprints/F37_Security_Architecture/KMP/01-keystore-backed-credential-caching-architectural-scan.md`), which independently reaches the identical conclusion this document reaches (§1) and already scopes the fix as its own Task 04 (K-01-T04). This document does not duplicate K-01 as a blueprint; it is the Phase-3, module-scoped, execution-ready closure of the same gap, written so `core-security` can be brought to full-green without requiring K-01 to be scheduled first. See §12 for exact reconciliation. |
| Consumers of the outcome | A.1 KMP K-05 `ParentPinLocalStore` (parent's own local PIN cache — `Development_Blueprints/A1_Splash_Auth_Onboarding/KMP/05-parent-pin-biometric-enrollment-flow.md`); C.19 KMP `ChildLockRepository` / K-06 offline cache (child lock PIN/pattern cache — `Development_Blueprints/C19_Parent_PIN_Biometric_Gate/KMP/06-offline-lock-verification-secure-local-cache.md`) |
| Status of underlying code | `CredentialHasher` interface: complete, stable, do not change its contract. `CredentialHasher`'s concrete algorithm: **non-compliant, must be replaced.** Status of this document | **Verification performed, decision made, implementation fully specified below.** |

---

## 1. Objective and Purpose

`CORE_SECURITY_INSTRUCTIONS.md` §4 documents `CredentialHasher` as follows:

> ```kotlin
> val hash = hasher.hash("1234") // Salts and hashes using SHA-256
> val isValid = hasher.verify(input, hash)
> ```

Meanwhile, F.37 B-04 (backend) mandates Argon2id — a deliberately slow, memory-hard algorithm — for every parent-PIN and child-lock-pattern/PIN credential the backend stores, specifically because SHA-256 is a *fast* general-purpose hash: an attacker holding a SHA-256 digest of a 4–6 digit PIN can exhaust the entire keyspace (10,000–1,000,000 combinations) in a fraction of a second on commodity hardware, whereas Argon2id raises that cost by five-to-six orders of magnitude.

This document's job is to answer one question with certainty, not hand-wave it:

> **Does `CredentialHasher`'s use of SHA-256 sit inside a different, narrower threat model than backend credential storage (in which case it is an intentional, correct, cheaper choice) — or is it the exact same class of secret, facing a materially similar exposure risk, using the wrong algorithm by omission (in which case it is a defect that must be fixed)?**

### 1.1 The verification finding

**`CredentialHasher` is used for exactly the same class of secret the backend protects with Argon2id — a parent's own 4–6 digit PIN, and a child's lock PIN/pattern — cached locally so a subset of the platform's gate logic can function offline.** It is not used for anything else. See §3 for the full call-site trace that establishes this.

Because it hashes the *same secret class* (a low-entropy, human-chosen PIN/pattern that gates parent-mode access and content restrictions in a children's-safety product) and that hash is written to durable on-device storage that a sufficiently-motivated attacker with physical device access can, in realistic non-theoretical scenarios (§9.3), extract independent of the app's own runtime — SHA-256 is **not** an acceptable substitute for a slow hash here, regardless of the fact that the comparison itself happens locally and offline. The "different threat model" argument (Outcome A, evaluated in full below) does not hold for this specific credential once its actual usage is traced. This is a **genuine compliance gap**, not a defensible intentional distinction.

### 1.2 The two candidate outcomes, both evaluated

Per this document's brief, both outcomes are documented in full so a coding agent can execute whichever the evidence supports — but the evidence in §3 and §9 supports only one of them:

- **Outcome A — "SHA-256 is correct/intentional for local-PIN-cache-only use."** Evaluated and **rejected**. See §9.1 for the argument and why it fails against this platform's actual facts (low-entropy PIN, no hardware-enforced attempt-throttling at the point of comparison, cross-platform corpus already treats this as a required NFR without a server-only carve-out).
- **Outcome B — "It is a defect; upgrade to a slow hash."** **Confirmed.** This is the outcome this document implements. See §9.2 onward and §13 (development steps) for the full execution path.

### 1.3 Why this matters specifically for NoorHeroes

NoorHeroes is a children's-safety product. The parent PIN is the single mechanism that separates a "parent" session (able to change restrictions, disable screen-time limits, authorize purchases, view unfiltered settings) from a "child" session (deliberately restricted). A weak local cache of that PIN's hash is not a cosmetic gap — a child (or anyone with brief, unsupervised physical access to the device, which is the single most common real-world exposure scenario for a *children's* device) who can extract the cached hash and brute-force it offline gains full parent-mode access with zero further barriers. This is precisely the failure mode F.37 exists to close platform-wide, and precisely why the C.19 PRD's Non-Functional Requirements (§1.8, quoted in full in §3.3) state the slow-hash requirement without a client/server carve-out.

---

## 2. Scope and Requirements

### 2.1 In scope
- Verifying, with a documented audit trail (§3), exactly what `CredentialHasher`'s output is used for and by whom.
- Making and recording the algorithm decision (§9), including the rejected alternative and why.
- Specifying the replacement algorithm, its exact parameters, and the rationale for those parameters against the platform's `p95 < 200ms` on-device offline-verification budget (C.19 §1.8 NFR) — §8.
- Specifying the concrete Kotlin Multiplatform implementation: package layout, `expect`/`actual` split, encoded-hash format, and migration/invalidation mechanics for pre-existing SHA-256-cached values (§5, §6, §11).
- Correcting `CORE_SECURITY_INSTRUCTIONS.md` §4 and §8 (Quick Reference Table) to state the true algorithm — the current wording is itself part of what let this gap go unnoticed (§9.4).
- Full test plan and CI wiring for the new algorithm and the migration path (§14).

### 2.2 Out of scope — explicitly do not touch
- **F.37 B-04's backend Argon2id utility** (`src/noorheroes/common/security/credential_hasher.py`, `hash_credential`/`verify_credential`) — different module, different runtime, different latency budget (server request path vs. mobile CPU/battery budget), already correctly implemented. This document only *references* it as the platform's reference standard for "what slow-hashing looks like here," per §12.
- The `CredentialHasher` **interface contract** (`hash(raw: String): String` / `verify(input: String, hash: String): Boolean`) — stays stable. Every consumer (`ParentPinLocalStore`, `ChildLockRepository`) keeps compiling and calling it exactly as today; only the concrete implementation behind the interface changes.
- `ProgressiveLockoutPolicy`, PIN-length rules (4–6 digits, FR-11), and any UI/ViewModel logic in A.1 K-05 or C.19 K-02/K-06 — those own their own concerns and are unaffected by an internal algorithm swap behind a stable interface.
- The Android-Keystore/iOS-Keychain **storage** layer itself (`EncryptedSharedPreferences`/Keychain wrapping) — already correctly specified as Keystore-backed by K-01 §6/§21 and C.19 K-06 §18. This document's concern is the **algorithm** applied *before* that storage layer receives the value, not the storage layer's encryption-at-rest guarantee (which is a separate, already-sound control — see §9.3 for how the two controls compose).
- F.37 KMP K-01's other four tasks (K-01-T01/T02/T03/T05 — the Keystore-storage-location scan and the zero-biometric-template-transmission scan) — unrelated deliverables in the same source blueprint; not part of this document's Definition of Done. See §12 for the exact boundary.

### 2.3 Non-functional requirements carried forward from the source corpus
- **Latency:** local (offline) PIN/pattern verification must resolve at **p95 < 200ms, fully on-device, no network dependency** (C.19 §1.8 NFR, restated verbatim in K-06 §5 and K-01 §11). This is the binding constraint on algorithm parameter choice — see §8.
- **No regression to the offline lock-verification user experience:** a legitimate parent/child must never be locked out by this change; the only acceptable friction is **one** forced online re-verification (or fresh PIN entry) the first time the app runs post-upgrade, to repopulate the cache under the new algorithm (§11).
- **Zero tolerance for a fast general-purpose hash anywhere in the credential-cache path** post-migration — mirrors B-04's own zero-tolerance framing (§25/§27 of B-04) and K-01's identical framing (§25) applied at the client layer.

---

## 3. Technical Implementation Details — the Verification Procedure

This is the audit that produced the §1.1 finding. A coding agent picking up this document must re-run (or trust, if the corpus has not changed) steps 3.1–3.4 before writing any code, per the project's established "audit before you build" pattern (identical in spirit to B-04 Task 01 and K-01 Task 01).

### 3.1 Trace every call site of `CredentialHasher.hash()` / `.verify()`

Two, and only two, confirmed consumers exist in the corpus:

1. **`ParentPinLocalStore`** (A.1 KMP K-05, `Development_Blueprints/A1_Splash_Auth_Onboarding/KMP/05-parent-pin-biometric-enrollment-flow.md`, Task 02). This is a **new** store (confirmed by K-05 Task 02's own text: *"no such store exists today... this is a genuine, confirmed gap"*) built specifically to hold **the parent's own on-device PIN verification hash**, so `AuthState.Parent`/`isElevated(clock)` step-up checks can succeed **offline**. It wraps `CredentialHasher.hash()`/`.verify()` directly:
   - `saveLocalPinHash(hash: String)` — called only *after* the raw PIN has already been accepted by B-04 server-side (K-05 §16: *"local hash written only after server success (never before, to avoid a client/server hash mismatch on partial failure)"*).
   - `verifyLocalPin(input: String): Boolean` — called by the parent-gate re-entry flow when biometrics are unavailable/declined and the device is offline; a successful verify updates `AuthState.Parent.elevatedUntil` via `MutableAuthStateHolder`.
2. **`ChildLockRepository`** (C.19 KMP K-02/K-06, `Development_Blueprints/C19_Parent_PIN_Biometric_Gate/KMP/06-offline-lock-verification-secure-local-cache.md`). This repository caches **a child's lock PIN/pattern hash** for the identical offline-verification purpose (C.19 FR-15: *"a locked child selected while offline verifies against the locally cached salted hash... no network round-trip is required"*). K-06's own text treats "salted hash" generically without re-specifying the algorithm, which means it inherits whatever `core-security`'s `CredentialHasher`/`crypto` package provides — i.e., it is also a consumer of this same primitive, not a second, independent hashing implementation (per `CORE_SECURITY_INSTRUCTIONS.md`'s own "Prohibited Patterns": *"NEVER use raw `MessageDigest`... always use the provided abstractions"*).

**No other consumer exists.** `secureHash()` (the separate top-level `crypto` package function documented for *"PII protection in logs/analytics"*) is a distinct utility with a distinct, non-credential purpose (irreversible pseudonymization of identifiers for telemetry, where speed is actually desirable and the input is not a low-entropy secret gating access) — it is correctly out of scope for this document and **must not** be changed by this work. Do not conflate the two; `secureHash()` staying SHA-256 is correct and is not part of the gap.

### 3.2 Confirm the secret's entropy class

Both consumers hash the same shape of secret: a **4–6 digit numeric PIN** (FR-11, "PIN 4–6 digits, parent's choice; no weak/strong judgment shown") or, per C.19 FR-5, a **lock pattern** (gesture points, itself a low-entropy discrete secret — FR-5 explicitly states raw gesture points are "never logged," confirming the platform already treats pattern data as sensitive). A 4-digit PIN has 10,000 possible values; a 6-digit PIN has 1,000,000. Both are trivially exhaustible offline against a fast hash (a modern consumer GPU computes billions of SHA-256 hashes per second; the entire 6-digit keyspace is exhausted in well under a second, the 4-digit keyspace in microseconds).

### 3.3 Confirm the platform's own stated requirement is not server-scoped

C.19's PRD (`PRD_Documents/Parent Area — In-App (19-26)/Feature_C19_Parent_PIN_Biometric_Gate.md`), the **source-of-truth document for this exact feature**, states in §1.8 (Non-Functional Requirements):

> **"Security:** Salted, slow (Argon2id-class) hashing for PIN/pattern storage; biometric verification delegates entirely to the OS, with zero biometric data ever transmitted to or stored by NoorHeroes servers. This is the platform's single most security-critical feature."

and in FR-5:

> "**Pattern** compares against a salted, slow hash (raw gesture points never logged); **PIN** compares against a salted, slow hash with retry-count-enforced progressive lockout."

Neither statement carries a "server-side only" qualifier. Both are written as properties of *"PIN/pattern storage"* as a category — which the corpus confirms (§3.1) includes the client-cached copy. This is the decisive evidence: the PRD, as the feature's source of truth, already settles the question in favor of Outcome B before this document even reasons about threat models independently (§9 reasons about it anyway, for rigor, and reaches the same place).

### 3.4 Confirm no hardware-enforced throttling compensates for the fast hash

Apple's Secure Enclave and Android's StrongBox/TEE-backed keystores can, in some configurations, enforce escalating delays *at the hardware key-usage level* (e.g., a hardware-gated signing key that itself refuses rapid repeated use) — a design where a fast software hash *could* be acceptable because the attacker cannot get unthrottled guesses even with full storage extraction. `CORE_SECURITY_INSTRUCTIONS.md` does not describe `CredentialHasher`/`TokenStore`/`DatabaseKeyProvider` this way: the described design is "generate key → store via EncryptedSharedPreferences/Keychain," with the **hash comparison itself performed in ordinary application code** (`hasher.verify(input, hash)`), not gated behind a hardware-throttled key-release. Confirmed: no such compensating hardware control exists in the documented design, so §9.1's Outcome-A precondition is not met.

**Conclusion of the verification procedure: Outcome B.** The remainder of this document specifies its execution.

---

## 4. Architecture and Component Responsibilities

```
Feature Layer (A.1 ParentPinSetupScreen/ViewModel, C.19 ChildLockVerificationScreen/ViewModel)
    ↓ calls
Data Layer (ParentPinLocalStore [core-security], ChildLockRepository [core-data])
    ↓ calls (UNCHANGED interface — this is the seam this document works behind)
CredentialHasher (interface, com.noorheroes.core.security.credential)
    ↓ implemented by (THIS DOCUMENT'S DELIVERABLE)
Pbkdf2CredentialHasher (concrete class, replaces the prior SHA-256 concrete implementation)
    ↓ delegates platform-specific KDF primitive to
Pbkdf2Primitive (expect/actual, com.noorheroes.core.security.crypto)
    ↓ actual implementations
[AndroidMain: javax.crypto.SecretKeyFactory("PBKDF2WithHmacSHA256")]
[IosMain: CommonCrypto CCKeyDerivationPBKDF via cinterop]
    ↓ salt generation reuses (unchanged, already-compliant)
nextSecureRandomBytes() (com.noorheroes.core.security.crypto)
    ↓ resulting encoded hash string persisted via (unchanged, already-compliant)
EncryptedSharedPreferences / Keychain (via ParentPinLocalStore's / ChildLockRepository's existing Keystore-backed storage wrapper — K-01/K-06's territory, not re-implemented here)
```

**Component responsibilities introduced or changed by this document:**

| Component | Responsibility | New or Changed? |
|---|---|---|
| `CredentialHasher` (interface) | `hash(raw: String): String`, `verify(input: String, hash: String): Boolean` | **Unchanged** — contract stability is a hard requirement (§2.2). |
| `Pbkdf2CredentialHasher` | Concrete `CredentialHasher` implementation using PBKDF2-HMAC-SHA256 with the parameters in §8. | **New** — replaces the prior SHA-256-based concrete class. |
| `EncodedCredentialHash` | Parses/formats the versioned, self-describing hash string (`pbkdf2-sha256$<iterations>$<salt>$<derivedKey>`) so `verify()` can dispatch correctly and so a future algorithm change (e.g., to Argon2id, see §8.4) remains detectable. | **New.** |
| `CredentialHashMigration` | Detects a pre-existing hash in the legacy (SHA-256) format at cache-read time and triggers the invalidation path of §11 rather than ever comparing against it again. | **New.** |
| `Pbkdf2Primitive` (`expect`/`actual`) | Platform-native PBKDF2-HMAC-SHA256 key derivation, invoked only by `Pbkdf2CredentialHasher`. | **New.** |
| `nextSecureRandomBytes()` | Salt generation. | **Unchanged**, reused as-is (already compliant; do not reimplement). |
| `ParentPinLocalStore`, `ChildLockRepository` | Call `CredentialHasher.hash()`/`.verify()`; on a detected legacy-format hash, clear the cached entry and surface "requires online re-verification" to the caller. | **Unchanged call sites**, one new branch each for legacy-format detection (§11.2). |
| `CORE_SECURITY_INSTRUCTIONS.md` | Documents the algorithm. | **Corrected** (§4 and §8's Quick Reference Table row for `CredentialHasher`). |

---

## 5. Folder / File Structure

```
core-security/
  src/
    commonMain/kotlin/com/noorheroes/core/security/
      credential/
        CredentialHasher.kt                 # interface — UNCHANGED
        Pbkdf2CredentialHasher.kt            # NEW — concrete CredentialHasher impl
        EncodedCredentialHash.kt             # NEW — versioned hash-string encode/parse
        CredentialHashMigration.kt           # NEW — legacy-format detection + invalidation signal
        BiometricGate.kt                     # existing — untouched
      crypto/
        Pbkdf2Primitive.kt                   # NEW — expect fun pbkdf2HmacSha256(...)
        SecureRandom.kt                      # existing (nextSecureRandomBytes) — untouched, reused
        SecureHash.kt                        # existing (secureHash, PII use) — untouched, OUT OF SCOPE
        DatabaseKeyProvider.kt               # existing — untouched
      auth/
        AuthState.kt                         # existing — untouched (elevatedUntil update stays ParentPinLocalStore's job)
    androidMain/kotlin/com/noorheroes/core/security/crypto/
      Pbkdf2Primitive.android.kt             # NEW — actual, javax.crypto.SecretKeyFactory
    iosMain/kotlin/com/noorheroes/core/security/crypto/
      Pbkdf2Primitive.ios.kt                 # NEW — actual, CommonCrypto CCKeyDerivationPBKDF
    commonTest/kotlin/com/noorheroes/core/security/credential/
      Pbkdf2CredentialHasherTest.kt          # NEW
      EncodedCredentialHashTest.kt           # NEW
      CredentialHashMigrationTest.kt         # NEW
    androidUnitTest/.../crypto/
      Pbkdf2PrimitiveAndroidTest.kt          # NEW — cross-check against a known PBKDF2-HMAC-SHA256 test vector
    iosTest/.../crypto/
      Pbkdf2PrimitiveIosTest.kt              # NEW — same known test vector, confirms platform parity

NoorHeroes/core/
  CORE_SECURITY_INSTRUCTIONS.md              # MODIFIED — §4 and §8 corrected (see §15 of this document for exact diff)
```

**Note on the pre-existing concrete SHA-256 implementation's exact current filename/path:** the corpus provided to this task (`CORE_SECURITY_INSTRUCTIONS.md`) documents `CredentialHasher` only at the interface/usage level — it does not name the current concrete implementing class. **Do not assume a filename.** Task 13.1 (Development Steps, below) requires the coding agent to locate it first (`grep -r "CredentialHasher" core-security/src/`, `grep -ri "sha-256\|sha256\|MessageDigest" core-security/src/`) and confirm its exact path and current encoded-hash string format before writing `CredentialHashMigration`'s legacy-detection logic — this mirrors the audit-first pattern B-04 Task 01 and K-01 Task 01 already establish for this exact codebase.

---

## 6. APIs, Models, Interfaces, and Data Flow

### 6.1 `CredentialHasher` — unchanged interface
```kotlin
package com.noorheroes.core.security.credential

interface CredentialHasher {
    /** Salts and hashes [raw] using the platform's designated slow-hash algorithm. */
    fun hash(raw: String): String

    /** Constant-time comparison of [input] against [encoded]. Never throws on a malformed [encoded]; returns false. */
    fun verify(input: String, encoded: String): Boolean
}
```
No signature change. Every existing call site (`ParentPinLocalStore`, `ChildLockRepository`) continues to compile unmodified.

### 6.2 `EncodedCredentialHash` — new, versioned string format

```kotlin
package com.noorheroes.core.security.credential

/**
 * Self-describing encoded hash: `<algorithmTag>$<params>$<saltB64Url>$<derivedKeyB64Url>`
 *
 * Current format: `pbkdf2-sha256$<iterations>$<saltB64Url>$<derivedKeyB64Url>`
 * Example:        `pbkdf2-sha256$600000$Qk7zX2n1...==$Yt2nJ4rQ...==`
 *
 * The algorithm tag makes the format forward-compatible: a future upgrade (e.g., to
 * `argon2id$<m>$<t>$<p>$<salt>$<hash>`, see §8.4) is distinguishable from this format by
 * [algorithmTag] alone, without needing a separate migration flag anywhere else in the system.
 */
data class EncodedCredentialHash(
    val algorithmTag: String,
    val params: List<String>,
    val saltB64Url: String,
    val derivedKeyB64Url: String,
) {
    fun encode(): String = (listOf(algorithmTag) + params + listOf(saltB64Url, derivedKeyB64Url)).joinToString("$")

    companion object {
        private const val CURRENT_TAG = "pbkdf2-sha256"

        /** Returns null (never throws) if [raw] does not parse as a well-formed encoded hash of any known format. */
        fun parseOrNull(raw: String): EncodedCredentialHash? {
            val parts = raw.split("$")
            if (parts.size < 3) return null
            val tag = parts.first()
            val saltB64Url = parts[parts.size - 2]
            val derivedKeyB64Url = parts.last()
            val params = parts.subList(1, parts.size - 2)
            return EncodedCredentialHash(tag, params, saltB64Url, derivedKeyB64Url)
        }

        fun isCurrentFormat(raw: String): Boolean = parseOrNull(raw)?.algorithmTag == CURRENT_TAG
    }
}
```

### 6.3 `Pbkdf2CredentialHasher` — new concrete implementation

```kotlin
package com.noorheroes.core.security.credential

import com.noorheroes.core.security.crypto.nextSecureRandomBytes
import com.noorheroes.core.security.crypto.pbkdf2HmacSha256

private const val PBKDF2_ITERATIONS = 600_000     // see §8.2 for rationale
private const val SALT_LENGTH_BYTES = 16          // 128-bit salt
private const val DERIVED_KEY_LENGTH_BITS = 256   // 256-bit derived key

internal class Pbkdf2CredentialHasher : CredentialHasher {

    override fun hash(raw: String): String {
        require(raw.isNotEmpty()) { "Credential must not be empty" }
        val salt = nextSecureRandomBytes(SALT_LENGTH_BYTES)
        val derivedKey = pbkdf2HmacSha256(
            password = raw.toCharArray(),
            salt = salt,
            iterations = PBKDF2_ITERATIONS,
            keyLengthBits = DERIVED_KEY_LENGTH_BITS,
        )
        return EncodedCredentialHash(
            algorithmTag = "pbkdf2-sha256",
            params = listOf(PBKDF2_ITERATIONS.toString()),
            saltB64Url = salt.encodeBase64Url(),
            derivedKeyB64Url = derivedKey.encodeBase64Url(),
        ).encode()
    }

    override fun verify(input: String, encoded: String): Boolean {
        val parsed = EncodedCredentialHash.parseOrNull(encoded) ?: return false
        if (parsed.algorithmTag != "pbkdf2-sha256") return false // legacy or unknown format — never compared; see §11
        val iterations = parsed.params.firstOrNull()?.toIntOrNull() ?: return false
        val salt = parsed.saltB64Url.decodeBase64UrlOrNull() ?: return false
        val expected = parsed.derivedKeyB64Url.decodeBase64UrlOrNull() ?: return false
        val actual = pbkdf2HmacSha256(
            password = input.toCharArray(),
            salt = salt,
            iterations = iterations,
            keyLengthBits = expected.size * 8,
        )
        return constantTimeEquals(actual, expected)
    }
}
```

`constantTimeEquals` is a length-and-value constant-time byte comparison (a simple XOR-accumulate loop that never short-circuits) — this closes the same "constant-time comparison" requirement B-04 §10 states explicitly for the backend ("verifies without ever re-deriving/comparing raw values insecurely (constant-time comparison...)"); the client-side implementation must match that discipline, not compare with `ByteArray.contentEquals` (which is not guaranteed constant-time across all KMP targets) or a naive loop that returns early on first mismatch.

### 6.4 `Pbkdf2Primitive` — new `expect`/`actual`

```kotlin
// commonMain
package com.noorheroes.core.security.crypto

/** Derives a key of [keyLengthBits] bits from [password] and [salt] using PBKDF2-HMAC-SHA256. */
expect fun pbkdf2HmacSha256(password: CharArray, salt: ByteArray, iterations: Int, keyLengthBits: Int): ByteArray
```

```kotlin
// androidMain
package com.noorheroes.core.security.crypto

import javax.crypto.SecretKeyFactory
import javax.crypto.spec.PBEKeySpec

actual fun pbkdf2HmacSha256(password: CharArray, salt: ByteArray, iterations: Int, keyLengthBits: Int): ByteArray {
    val spec = PBEKeySpec(password, salt, iterations, keyLengthBits)
    val factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256")
    return try {
        factory.generateSecret(spec).encoded
    } finally {
        spec.clearPassword() // zero the raw credential's transient char[] copy held by PBEKeySpec
    }
}
```

```kotlin
// iosMain — via CommonCrypto cinterop (CCKeyDerivationPBKDF, algorithm kCCPBKDF2, prf kCCPRFHmacAlgSHA256)
package com.noorheroes.core.security.crypto

actual fun pbkdf2HmacSha256(password: CharArray, salt: ByteArray, iterations: Int, keyLengthBits: Int): ByteArray {
    // Implementation calls CCKeyDerivationPBKDF via the project's CommonCrypto cinterop definition
    // (add a `commonCrypto.def` under iosMain's cinterop config if one is not already present for
    // another core-security primitive; confirm during Task 13.2 whether Keychain access already
    // pulls in a Security.framework cinterop that can be extended, before adding a second one).
    // ... platform-native PBKDF2 derivation, keyLengthBits / 8 output bytes ...
}
```

### 6.5 Data flow — offline PIN verification (parent, post-migration)

```
Parent enters PIN in ParentPinLocalStore.verifyLocalPin(input) offline path
    ↓
CredentialHasher.verify(input, storedEncodedHash)
    ↓
EncodedCredentialHash.parseOrNull(storedEncodedHash)
    ├─ algorithmTag == "pbkdf2-sha256" → derive + constant-time compare → Boolean result
    └─ algorithmTag != "pbkdf2-sha256" (legacy SHA-256 or unparseable) → verify() returns false
            ↓
       ParentPinLocalStore detects this specific false-from-legacy-format case (§11.2)
            ↓
       Surfaces "local cache invalid — requires online re-verification" to the ViewModel
            ↓
       ViewModel routes to: online PIN re-entry (if connectivity available) → on success,
       ParentPinLocalStore.saveLocalPinHash() repopulates the cache under pbkdf2-sha256
            ↓
       AuthState.Parent.elevatedUntil updated via MutableAuthStateHolder (unchanged path)
```

---

## 7. Dependencies and Configuration Requirements

- **No new third-party dependency for the recommended (default) path.** PBKDF2-HMAC-SHA256 is available as a JDK builtin on Android (`javax.crypto.SecretKeyFactory`) and as an Apple-platform builtin on iOS (`CommonCrypto`, already part of the OS — no CocoaPods/SPM addition required, only a cinterop `.def` file if one for `CommonCrypto` does not already exist in the iOS target's `build.gradle.kts` `cinterops {}` block).
- **Gradle:** no version-catalog changes required for the default path. If the team later opts into the Argon2id stretch path (§8.4), that would add a Kotlin/JVM-and-Native Argon2id binding (e.g., an `argon2kt`-class dependency for Android/JVM plus a native Argon2id pod/SPM package for iOS) — **not part of this document's Definition of Done**; documented in §8.4 as a deferred option only.
- **iOS cinterop:** confirm during implementation (Task 13.2) whether `core-security`'s existing Keychain-access code already defines a `Security.framework` (or adjacent) cinterop block that a `CommonCrypto` interop definition can sit alongside, versus needing an entirely new `.def` file — do not assume; the exact iOS build configuration was not included in the corpus provided to this task.
- **ProGuard/R8 (Android release builds):** `javax.crypto.SecretKeyFactory` and `PBEKeySpec` are JDK platform classes and require no explicit keep rules under standard Android minification; confirm no existing custom ProGuard rule in the project incorrectly strips `javax.crypto.**` (unlikely, but a one-line audit).

---

## 8. Storage / Parameter Requirements — the Algorithm Decision in Detail

### 8.1 Recommended algorithm: PBKDF2-HMAC-SHA256, 600,000 iterations

**This document's binding recommendation, to be implemented as the default and only algorithm for this Definition of Done:** PBKDF2-HMAC-SHA256 with **600,000 iterations**, a **128-bit (16-byte) random salt unique per credential**, and a **256-bit derived key**.

### 8.2 Rationale for PBKDF2-HMAC-SHA256 over a KMP-native Argon2id binding, for this specific module

The backend (B-04) uses Argon2id, and B-04 §26/§94 states that choice follows PRD §5's explicit stack line ("Argon2id/bcrypt for credential hashing"). A KMP client-side implementation is not bound to reuse the exact same library — different runtime, different constraints — but it must meet the same **security bar** ("Argon2id-class," per C.19 §1.8, meaning: a deliberately slow, salted algorithm resistant to offline brute force at the scale a stolen/compromised device's extracted storage would expose, not literally the Argon2id function by name). Two options were weighed, per K-01 §26's own explicitly-sanctioned choice between them:

| Consideration | Argon2id (true KMP binding) | PBKDF2-HMAC-SHA256 (chosen) |
|---|---|---|
| Native dependency | Requires a native Argon2 library per platform (Android: JVM/NDK binding; iOS: Swift/C binding) — new build-toolchain surface area in a module that must stay lean and auditable. | **Zero new native dependency** — `javax.crypto` (Android) and `CommonCrypto` (iOS) are OS-builtin. |
| Memory-hardness | Yes — resists GPU/ASIC parallelization better than PBKDF2 at equivalent time cost. | No — PBKDF2 is CPU-time-hard only, not memory-hard. |
| p95 < 200ms budget on low-end hardware | Achievable, but tuning (memory cost in particular) against real low-end Android devices requires its own hardware-benchmarking pass with a new dependency in the loop. | Directly tunable via a single scalar (iteration count); well-characterized cost curve; OWASP publishes a current minimum iteration count (600,000) specifically for this construction, removing guesswork. |
| Consistency with corpus | Would exceed what K-01 §26 requires ("prefer a true Argon2id KMP binding if one exists/can be added... if no such binding is feasible without disproportionate native-toolchain overhead... PBKDF2-HMAC-SHA256 with a high iteration count... is an acceptable documented fallback"). | **Explicitly, by name, the K-01-sanctioned fallback** — chosen here because it meets the stated bar without the added native-toolchain risk in a security-critical, latency-budget-constrained module. |
| Security margin vs. current SHA-256 | N/A (not chosen) | **~600,000× more expensive per guess** than a single SHA-256 round — five-to-six orders of magnitude, which is the entire point (§9.2). |

**Decision: PBKDF2-HMAC-SHA256 at 600,000 iterations is the implemented algorithm for this Definition of Done.** It closes the actual gap (a fast, single-round hash) completely; the marginal additional resistance Argon2id's memory-hardness would add is a genuine but secondary hardening layer, not required to close the identified defect, and is documented below (§8.4) as an explicit, deferred option rather than silently dropped.

### 8.3 Why 600,000 iterations specifically

600,000 is OWASP's current published minimum iteration count for PBKDF2-HMAC-SHA256 in the OWASP Password Storage Cheat Sheet (the same reference standard B-04 §24 invokes for its own Argon2id parameter tuning — "chosen per current OWASP... guidance"). It is not an arbitrary round number picked for this document; it is the platform's existing precedent (B-04 already anchors its parameter choice to OWASP guidance) applied to the PBKDF2 construction specifically.

**This number must be benchmark-confirmed against representative low-end Android/iOS hardware before being finalized as a compile-time constant**, per C.19 §1.8's `p95 < 200ms` NFR and K-01 §29 Task 04's identical instruction ("benchmark against C.19's explicit p95 < 200ms NFR on representative low-end device hardware, not just a development machine"). §14.3 specifies this benchmark test. If 600,000 iterations does not meet the 200ms budget on the project's actual low-end reference device (confirm which device tier the project already uses for this kind of benchmark — do not assume; check existing performance-test tooling/config before picking a device), the iteration count may be tuned downward **only as far as necessary to hit the budget, and never below a documented floor** — see §8.3.1. If no iteration count within the OWASP-acceptable range hits the budget on the reference hardware, this is an escalation per §9.5 (Security Engineering sign-off required before trading security for speed), exactly mirroring K-01 §29 Task 04's own escalation clause.

#### 8.3.1 Iteration-count floor if downward tuning is required

If benchmarking forces a reduction from 600,000, the floor is **310,000 iterations** — OWASP's cited minimum for PBKDF2-HMAC-SHA256 in earlier (still-acceptable, still-current-enough) guidance revisions, and still roughly 310,000× more expensive per guess than the SHA-256 baseline this replaces. Any value below that floor requires the same Security Engineering sign-off as §8.3's escalation clause — this is not a value an implementing agent may pick unilaterally under time pressure.

### 8.4 Deferred option: Argon2id upgrade path (not part of this DoD)

`EncodedCredentialHash`'s algorithm-tag design (§6.2) exists specifically so a future move to Argon2id is a clean, additive change: add a second recognized tag (`argon2id$<memoryKiB>$<iterations>$<parallelism>$<salt>$<hash>`), teach `verify()` to dispatch on tag, and have `hash()` start writing the new tag going forward — no forced-invalidation migration would be needed for that *future* transition (unlike the SHA-256→PBKDF2 transition this document specifies in §11, which cannot avoid forced invalidation because SHA-256 was never salted-and-slow to begin with). This document does not implement that future path; it only ensures today's format doesn't foreclose it. Suggested future parameters if pursued: memory cost 19 MiB, time cost 2, parallelism 1 (OWASP's Argon2id minimum recommended settings for interactive/latency-sensitive login use cases) — recorded here only as a forward pointer, not a current requirement.

---

## 9. Authentication, Authorization, Validation, and Security Considerations

### 9.1 Outcome A in full — the rejected argument, stated fairly

For completeness (this document must not hand-wave the rejected path): the argument for SHA-256 being acceptable would run — *"this hash never leaves the device, is never transmitted, is never compared against by an attacker who can make unlimited network-speed guesses the way they could against an exposed server endpoint; the Keystore/Keychain encryption-at-rest already protects the value; therefore algorithmic slowness is redundant defense against a threat (unlimited remote guessing) that doesn't apply here."*

This argument correctly identifies that the **network-scale remote brute-force** threat model does not apply to a local cache — that much is true and is exactly why B-04's own §11 originally left this as an "open flag" rather than an obvious violation. But it fails for this platform specifically for the reasons in §9.2–§9.4, primarily because it substitutes "the value never leaves the device over the network" for "the value can never be extracted by any means" — those are not the same claim, and only the second one would actually make SHA-256 safe here.

### 9.2 Why the device-extraction threat model still requires a slow hash — brute-force resistance

The realistic exposure path for a locally-cached credential hash is not "attacker calls an API repeatedly" (irrelevant here, correctly ruled out by Outcome A's argument) — it is **offline extraction followed by unlimited, unthrottled local computation**:
- A rooted Android device or jailbroken iOS device with forensic/backup-extraction tooling (e.g., commercial mobile forensics suites, or simply `adb backup`-class tooling against a debuggable/rooted build) can, in various configurations, obtain the raw bytes an app has written to its own encrypted-preferences/Keychain store, or obtain them via an OS-level or app-level vulnerability that grants read access to the app's sandbox.
- Once those bytes are obtained, **the attacker's computation is no longer rate-limited by anything the app or OS controls** — it runs entirely on attacker-owned hardware, offline, at whatever speed that hardware allows.
- Against SHA-256, that computation exhausts a 4-digit PIN's keyspace in microseconds and a 6-digit PIN's in well under a second on a consumer GPU. Against PBKDF2-HMAC-SHA256 at 600,000 iterations, the same keyspace requires roughly 600,000× the computation — turning "instant" into "computationally expensive enough to meaningfully deter opportunistic attackers," which is precisely the standard B-04 already applies server-side and C.19 §1.8 requires platform-wide.
- This is true **regardless of whether the value ever traveled over a network** — it is a property of the secret's low entropy (4–6 digits) combined with the algorithm's speed, not a property of transmission.

### 9.3 What happens if Keychain/Keystore itself is compromised

This is the specific question this document's brief requires addressing directly: encryption-at-rest (Keystore/Keychain) and algorithmic slowness are **two independent, complementary controls**, not substitutes for each other:

- **If Keystore/Keychain holds and the app-level encrypted-preferences wrapper is never bypassed:** the stored hash bytes are never exposed to an attacker at all, and the algorithm choice is moot (both SHA-256 and PBKDF2 would be equally "safe" in this scenario, because nothing is ever extracted). This is the scenario Outcome A implicitly assumes holds always.
- **If Keystore/Keychain is bypassed or compromised** (device rooted/jailbroken post-purchase by the device's own child user — a realistic scenario specifically *because* this is a children's device that a technically curious child may attempt to root; OS-level TEE/StrongBox exploit; forensic extraction from an unlocked or previously-unlocked device; a corrupted/misconfigured backup that exposes app-sandbox contents unencrypted) — the encrypted-preferences layer's protection is gone, and **the hash's own algorithmic strength becomes the only remaining control.** In this scenario, SHA-256 provides effectively zero additional resistance (the keyspace is exhausted instantly regardless of the preceding encryption layer having failed), while PBKDF2-HMAC-SHA256 at 600,000 iterations still meaningfully raises the cost of recovering the raw PIN even after the storage layer's own protection has already failed.
- **Conclusion:** defense-in-depth requires both controls to independently hold value, not just the first one. This is exactly why this document's brief frames the recommendation as "upgrade regardless, as defense-in-depth, since it's cheap to do and removes ambiguity" — and the verification in §3–§9 confirms that framing is correct here, not merely cautious.

### 9.4 A contributing cause worth naming: the documentation itself

`CORE_SECURITY_INSTRUCTIONS.md` §4's own text — *"Salts and hashes using SHA-256"* — presented as a plain, unremarkable fact rather than a flagged decision, is part of why this gap persisted undetected. A module's own reference documentation stating a security-relevant implementation detail in a tone that reads as "this is fine" rather than "this is worth a second look" is a process failure independent of the algorithm choice itself. §15 corrects the documentation for this reason specifically, not only to reflect the new algorithm but to make future reviewers' job easier by no longer stating a defect as if it were a settled fact.

### 9.5 Escalation path if the p95 < 200ms budget cannot be met at a secure parameter level

If benchmarking (§14.3) shows no iteration count at or above the §8.3.1 floor meets the 200ms budget on the project's actual low-end reference hardware, the implementing agent must **not** silently drop below the floor to hit the number. Escalate to Security Engineering for an explicit sign-off decision (trade a documented, bounded amount of security margin for latency, or relax the latency budget, or move the verification to a background thread with a UI-level "verifying..." affordance if the constraint is UX-perceived-latency rather than a hard technical requirement) — this mirrors K-01 §29 Task 04's own identical escalation clause verbatim, and the same non-negotiable-without-sign-off framing B-04 §25 applies to its own algorithm choice.

### 9.6 Validation
- `hash(raw)` rejects empty input (`require(raw.isNotEmpty())`), mirroring B-04 §15's identical server-side rule for consistency across the platform's two hashing utilities.
- `verify(input, encoded)` **never throws** on a malformed or legacy-format `encoded` value — always returns `false` (§6.3, `parseOrNull` returning `null` short-circuits to `false`). This mirrors B-04 §15's identical contract ("`verify_credential` returns `False` (never raises) on a malformed stored-hash value") and is the same discipline this document's client-side utility must uphold independently, since a crash here would mean a corrupted local cache locks a legitimate parent out entirely rather than gracefully falling back to online verification.

---

## 10. Database/Storage Requirements

No new database tables (this is entirely on-device, encrypted-preferences/Keychain storage, not SQL). The **encoded hash string format** (`pbkdf2-sha256$<iterations>$<salt>$<derivedKey>`) is the only "schema" involved, and it is versioned via the algorithm tag (§6.2) specifically so storage never needs a companion metadata field to know which algorithm produced a given value — the string is self-describing. Both `ParentPinLocalStore` and `ChildLockRepository` continue writing this string through their existing Keystore-backed storage wrappers (`EncryptedSharedPreferences` on Android, Keychain on iOS) — this document does not change *where* the string is stored, only *what algorithm produced it*.

---

## 11. State Management and Lifecycle Considerations — the Migration Path

This is the section addressing the brief's explicit requirement: *"existing stored local-PIN hashes must be migrated/re-hashed on next successful unlock, not broken."*

### 11.1 Why an in-place lazy rehash was considered and rejected

A common password-hasher upgrade pattern (used by, e.g., Django's password hasher chain) is: on a successful verify against the *old* algorithm, immediately recompute and overwrite the stored value using the *new* algorithm, since the raw input is available in memory at that exact moment. This was considered for `CredentialHasher` and **rejected** in favor of forced cache invalidation, for two concrete reasons specific to this module:

1. **It requires `verify()` to retain live support for comparing against the legacy SHA-256 format**, meaning the fast-hash comparison code path would have to stay in the codebase and stay reachable in production for an indefinite transition period — directly working against the "zero fast-hash anywhere in the credential path" posture this whole document exists to establish, and reintroducing exactly the kind of dual-algorithm complexity that made the original gap easy to overlook (§9.4).
2. **It is inconsistent with the platform's own already-established precedent for this exact transition.** F.37 KMP K-01 §29 Task 04 — the corpus's own prior treatment of this identical migration — explicitly specifies forced invalidation ("on app update, the local cache must be invalidated/cleared, forcing a one-time fresh online verification... to repopulate the offline cache under the new algorithm") and explicitly rules out silent in-place upgrading ("existing cached hashes computed under the old SHA-256 implementation cannot be safely 'upgraded in place'"). This document aligns with that established platform decision rather than introducing a second, divergent migration strategy for what is functionally the same transition.

### 11.2 The implemented migration path

1. **On app-version upgrade** (detected via the project's existing app-version-change hook, or, if none exists yet, a stored `lastCredentialHashSchemaVersion` preference bumped alongside this release — confirm which mechanism the project already uses before inventing a new one), `ParentPinLocalStore` and `ChildLockRepository` each check their currently-cached encoded hash string via `EncodedCredentialHash.isCurrentFormat(cached)` (§6.2) **before** ever passing it to `CredentialHasher.verify()`.
2. If `isCurrentFormat` returns `false` (the value is in the legacy SHA-256 format, or any other unrecognized format), the cached entry is **deleted outright** from the Keystore-backed store — it is never passed to `verify()`, and no comparison against it, successful or not, ever occurs again.
3. The consuming ViewModel (A.1's parent-gate re-entry flow / C.19's `ChildLockVerificationScreen`) receives a distinct "local cache unavailable — online verification required" signal (a new sealed-class case on whatever result type `ParentPinLocalStore.verifyLocalPin()` / `ChildLockRepository.verifyChildLock()` already returns — extend it, do not silently fold this into the existing `false` "wrong PIN" case, since UX must be able to distinguish "you typed the wrong PIN" from "your device needs to reconnect once" and message the parent accordingly).
4. If connectivity is available, the flow falls through to the existing **online** verification path (B-04's server-side endpoint, already authoritative per C.19 §5/K-01 §25 — *"the server-side path is always authoritative when connectivity is available"*) exactly as it already does for a first-time/never-cached device. On success, `saveLocalPinHash()`/the `ChildLockRepository` equivalent repopulates the cache — now, necessarily, under the new `pbkdf2-sha256` format, since that is the only format `Pbkdf2CredentialHasher.hash()` ever produces.
5. If connectivity is **not** available at that exact moment, the user sees a clear, non-alarming "reconnect once to continue" state — **not** a lockout, not an error framed as "wrong PIN," and not a silent fallback that re-trusts the deleted legacy hash. This satisfies the brief's "must not lock a legitimate parent out, only require one online-connected re-verification" requirement, matching K-01 §29 Task 04's identical business rule verbatim.
6. This is a **one-time** event per device per this migration — once step 4 succeeds once, the device's cache is permanently on the new format and never triggers this path again (barring a future, separately-planned algorithm change, which would follow the same pattern via a new algorithm tag).

### 11.3 What must not regress during migration

- `AuthState.Parent.elevatedUntil` step-up freshness tracking (owned by `MutableAuthStateHolder`, untouched by this document) must not be spuriously reset or corrupted by a cache invalidation — invalidating the *hash cache* is not the same as invalidating an *already-elevated* session; a parent mid-session when the migration triggers should not be unexpectedly de-elevated purely because their cached PIN hash was cleared in the background.
- Biometric-unlock (`BiometricGate`) is entirely unaffected — it does not touch `CredentialHasher` at all (per `CORE_SECURITY_INSTRUCTIONS.md` §4, biometric verification is a separate OS-delegated path) — a parent who normally unlocks via FaceID/fingerprint should notice nothing different during this migration; only the PIN-fallback and offline paths are affected.

---

## 12. Integration Points with Existing Modules

### 12.1 A.1 KMP K-05 — `ParentPinLocalStore`
`ParentPinLocalStore.saveLocalPinHash()`/`.verifyLocalPin()` call `CredentialHasher.hash()`/`.verify()` exactly as before (§2.2 — interface unchanged). The one integration change required in `ParentPinLocalStore` itself: add the legacy-format-detection branch from §11.2 step 1–3 to `verifyLocalPin()`, and extend its result type to distinguish "wrong PIN" from "cache invalid, needs online re-verification" (§11.2 step 3). No change to `PinSetupViewModel`'s write path (K-05 Task 03) beyond it already correctly calling `saveLocalPinHash()` only after server success — that ordering already guarantees every *newly written* cache entry uses whatever `CredentialHasher.hash()` currently produces, i.e., automatically the new format from this document's implementation onward, with zero additional work required in K-05's own code beyond the migration branch.

### 12.2 C.19 KMP K-02/K-06 — `ChildLockRepository`
Same integration shape as §12.1: `ChildLockRepository`'s existing `verifyChildLock()` gains the same §11.2 legacy-detection branch. K-06 §9 already names `ChildLockRepository.kt` as a file this platform expects to modify for storage-hardening reasons independent of this document (K-06's own Task 01/02 audit whether Keystore-backed encryption is actually in place) — this document's change is additive to that existing planned work, not a conflicting parallel edit; if K-06 is implemented first, this document's migration branch is added on top of an already-Keystore-confirmed `ChildLockRepository`; if this document is implemented first, K-06's own storage-backend audit proceeds unaffected by the algorithm change, since the algorithm and the storage-encryption-at-rest guarantee are independent controls (§9.3).

### 12.3 F.37 B-04 (backend) — reference standard, not a dependency
This document's implementation has **no runtime dependency** on B-04's code (different language, different process, different device) — B-04 is referenced throughout this document purely as **the platform's existing precedent for what "meets the Argon2id-class bar" looks like** (parameter-tuning-against-OWASP-guidance methodology in §8.3, constant-time-comparison discipline in §6.3/§9.6, never-throws-on-malformed-input discipline in §9.6). Do not add a network call, a shared library, or any other coupling between this KMP module and the backend utility — they must remain independently deployable and independently correct, exactly as B-04 §11 itself already states ("not a change to this blueprint's own server-side utility").

### 12.4 F.37 KMP K-01 — exact reconciliation
K-01 (`Development_Blueprints/F37_Security_Architecture/KMP/01-keystore-backed-credential-caching-architectural-scan.md`) already contains, as its own Task 04 (K-01-T04), a specification of this identical migration that this document independently arrives at and is consistent with in every material respect (algorithm choice reasoning, iteration-count fallback, p95 budget, forced-invalidation migration strategy, escalation clause). **If K-01 is scheduled as a blueprint in its own right, its Task 04 and this entire document cover the same ground** — an implementing team should treat them as one piece of work, not duplicate it twice. This document exists as a standalone, Phase-3-scoped, immediately-executable closure specifically so `core-security`'s 🟡 partial status can be resolved **without** waiting on K-01's other four unrelated tasks (the Keystore-storage-location scan, T01–T03, and the separate biometric-template-transmission scan, T05) to be scheduled first. When both are eventually implemented, K-01-T04's own checklist items are satisfied by this document's execution — no separate re-implementation is needed; a future K-01 execution pass should simply confirm this document's Definition of Done (§17) as already met and check its own boxes accordingly, updating K-01's own status rather than re-doing the work.

---

## 13. Development Steps in the Correct Implementation Order

**Task 01 — Locate the current concrete `CredentialHasher` implementation and confirm its exact legacy encoded-hash format.**
Search `core-security/src/` for the class currently implementing `CredentialHasher` (`grep -r "CredentialHasher" core-security/src/`, `grep -ri "MessageDigest\|sha-256\|sha256" core-security/src/`). Record its exact package/filename and the exact string format it currently produces (needed for `CredentialHashMigration`'s legacy-detection to be precise, even though detection ultimately just needs "is this the new format or not" via §6.2's `isCurrentFormat`). Do not proceed to Task 02 with an assumed format — confirm against the real source.

**Task 02 — Confirm the iOS cinterop situation for `CommonCrypto`.**
Check whether `core-security`'s iOS target already defines a cinterop block usable for `CommonCrypto`, or whether a new `.def` file is required (§7). This affects Task 06's exact implementation but not its design.

**Task 03 — Implement `EncodedCredentialHash` (§6.2) and its unit tests.**
Pure logic, no platform dependency — implement and test first as the foundation everything else builds on.

**Task 04 — Implement `Pbkdf2Primitive` `expect`/`actual` (§6.4).**
Android actual via `javax.crypto`; iOS actual via `CommonCrypto`. Verify both against a **known PBKDF2-HMAC-SHA256 test vector** (RFC 7914 Appendix B / NIST test vectors are the standard reference — pick one with SHA-256 as the PRF specifically) on both platforms independently, confirming platform parity before building anything on top of this primitive (§14.1).

**Task 05 — Implement `Pbkdf2CredentialHasher` (§6.3), replacing the current concrete `CredentialHasher` implementation located in Task 01.**
Wire up `hash()`/`verify()` exactly as specified; reuse `nextSecureRandomBytes()` unchanged for salt generation (do not reimplement); implement `constantTimeEquals` per §6.3/§9.6. Update the module's dependency-injection wiring (wherever `CredentialHasher` is bound to its implementation — locate via the same search as Task 01) to point at `Pbkdf2CredentialHasher` instead of the legacy class. Delete the legacy concrete class's SHA-256 hashing logic entirely — do not leave it dead-code-reachable (§9.4/§11.1's "zero fast-hash anywhere" posture).

**Task 06 — Implement `CredentialHashMigration` and wire the §11.2 invalidation branch into `ParentPinLocalStore` and `ChildLockRepository`.**
Extend both call sites' result types to distinguish "wrong credential" from "cache invalid, requires online re-verification" (§11.2 step 3, §12.1, §12.2). Confirm with A.1/C.19's existing ViewModel-level error handling (`BaseViewModel` pattern, per A.1 K-05 §16's testing conventions) that this new signal routes to a distinct, non-alarming UI state, not the existing "wrong PIN" error copy.

**Task 07 — Benchmark the 600,000-iteration parameter (§8.3) against the project's actual low-end reference hardware.**
Confirm p95 < 200ms. If not met, apply §8.3.1's floor-bounded downward tuning, or escalate per §9.5 — do not silently drop below the floor.

**Task 08 — Correct `CORE_SECURITY_INSTRUCTIONS.md` (§15 of this document specifies the exact text change).**

**Task 09 — Full test suite (§14) and CI wiring.**

**Task 10 — Final review** confirming: zero remaining `MessageDigest`/SHA-256 reference anywhere in the credential-cache path (a grep-level self-check, informally mirroring B-04's CI-blocking architectural test even though writing that exact CI-blocking scan is K-01-T03's own separate deliverable, not required here — see §12.4); interface stability confirmed by a clean compile of `ParentPinLocalStore`/`ChildLockRepository` with zero changes to their `CredentialHasher` call signatures; migration path manually exercised against a device with a pre-seeded legacy-format cached hash.

---

## 14. Testing Strategy and Acceptance Criteria

### 14.1 Unit — `Pbkdf2Primitive`
- Known PBKDF2-HMAC-SHA256 test vector produces the exact expected output on **both** Android and iOS actuals (platform-parity proof — this is the single most important correctness test in this document, since a silent platform divergence here would mean a hash created on Android could never verify correctly if the cache were ever restored to an iOS device, or vice versa, on a shared-family-account scenario).

### 14.2 Unit — `EncodedCredentialHash`
- Round-trip encode/parse produces an identical value.
- `parseOrNull` returns `null` (never throws) on: empty string, a string with too few `$`-delimited segments, a string whose salt/derivedKey segments are not valid base64url.
- `isCurrentFormat` correctly distinguishes the new tag from a plausible legacy-format string and from garbage input.

### 14.3 Unit + Performance — `Pbkdf2CredentialHasher`
- `hash()` produces a different encoded string for the same input across repeated calls (unique salt confirmed) — mirrors B-04 §27's identical server-side test for consistency.
- `verify()` correctly accepts a matching input and rejects a non-matching one.
- `verify()` returns `false` (never throws) for: an empty `encoded` string, a malformed `encoded` string, a syntactically-valid-but-wrong-algorithm-tag `encoded` string (i.e., a legacy SHA-256-format value — confirming it is never accidentally compared against).
- **Performance:** measure hash/verify latency on the project's designated low-end reference device (confirm which device tier via existing performance-test tooling before running) at 600,000 iterations; assert p95 < 200ms per §8.3/C.19 §1.8. Record the actual measured p95 in the test's own output/comment for future reference, per B-04 §24's identical "document the chosen parameters and the reasoning... not just defaults left unexamined" discipline applied client-side.

### 14.4 Integration — migration path
- Seed a `ParentPinLocalStore`/`ChildLockRepository` test double's underlying storage with a hand-constructed legacy-format string (using whatever exact format Task 01 confirmed); trigger `verifyLocalPin()`/`verifyChildLock()`; assert: (a) the legacy value is never passed into any comparison, (b) the stored entry is deleted, (c) the caller receives the distinct "requires online re-verification" signal, not a plain "wrong PIN" result.
- Simulate a successful online re-verification following that signal; assert the cache is repopulated and the newly-stored value's `EncodedCredentialHash.isCurrentFormat()` is `true`.
- Simulate the "no connectivity available" branch of §11.2 step 5; assert the user-facing state is distinctly "reconnect to continue," never framed as a lockout or a wrong-PIN error.
- Regression: confirm `AuthState.Parent.elevatedUntil` is not spuriously reset by a cache-invalidation event alone (§11.3), and that biometric unlock is entirely unaffected by any of the above (§11.3).

### 14.5 Architectural / static-check (lightweight, informal — the CI-blocking version is K-01-T03's separate deliverable)
- A repo-level grep/AST self-check confirming no `MessageDigest.getInstance("SHA-256")` (or equivalent) call remains anywhere in `core-security`'s `credential` package post-migration (Task 10's final-review step, §13). Formalizing this into a permanent CI-blocking gate mirroring B-04's `test_no_fast_hash_in_credential_path.py` is explicitly K-01-T03's territory (§12.4) — this document's own test suite includes the check as a one-time verification, not a claim of owning the permanent CI gate.

### 14.6 Acceptance criteria (summary)
- [ ] `Pbkdf2Primitive` matches a known test vector on both Android and iOS.
- [ ] `Pbkdf2CredentialHasher.hash()`/`.verify()` pass all unit tests in §14.3.
- [ ] Measured p95 latency on low-end reference hardware is under 200ms at the shipped iteration count (600,000, or the §8.3.1-floor-bounded reduced value if benchmarking required it, with sign-off recorded if the floor itself was insufficient).
- [ ] Migration path (§14.4) fully passes: legacy hash never compared, cache invalidated, distinct UX signal surfaced, successful repopulation confirmed under the new format.
- [ ] `ParentPinLocalStore` and `ChildLockRepository` compile and pass their own existing test suites unmodified beyond the new migration branch (interface-stability proof).
- [ ] Zero remaining SHA-256/`MessageDigest` reference in `core-security`'s `credential` package.

---

## 15. Documentation Correction — `CORE_SECURITY_INSTRUCTIONS.md`

Replace §4's `CredentialHasher` block:

> **Before:**
> ```kotlin
> val hash = hasher.hash("1234") // Salts and hashes using SHA-256
> val isValid = hasher.verify(input, hash)
> ```
>
> **After:**
> ```kotlin
> val hash = hasher.hash("1234") // Salts and hashes using PBKDF2-HMAC-SHA256 (600,000 iterations,
>                                 // 128-bit salt, 256-bit derived key) — see
>                                 // Phase3_Shared_Core_Modules.KMP.17 for the full parameter
>                                 // rationale and the C.19 §1.8 NFR ("Argon2id-class hashing")
>                                 // this satisfies. Never SHA-256 — a fast hash was the
>                                 // module's original implementation and was a confirmed
>                                 // compliance gap, corrected here.
> val isValid = hasher.verify(input, hash)
> ```

Replace §8's Quick Reference Table row for `CredentialHasher`:

| Before | After |
|---|---|
| `CredentialHasher` \| Interface \| Salts and hashes credentials (PIN). \| Data/Domain | `CredentialHasher` \| Interface \| Salts and hashes credentials (PIN) via PBKDF2-HMAC-SHA256, 600,000 iterations — slow-hash, Argon2id-class per C.19 §1.8. \| Data/Domain |

---

## 16. Dependencies / Prerequisites

- F.37 B-04 (backend Argon2id utility) — already implemented; referenced, not depended on (§12.3).
- `core-security` module itself — already implemented (`AuthState`, `MutableAuthStateHolder`, `nextSecureRandomBytes`, `TokenStore`, `DatabaseKeyProvider` all pre-exist and are reused unchanged).
- A.1 K-05's `ParentPinLocalStore` — this document assumes it exists (per its own spec) or is being built in parallel; §12.1's integration point applies whichever way the two pieces of work are sequenced.
- C.19 K-06's `ChildLockRepository` Keystore-backed storage confirmation — independent work; §12.2 clarifies this document does not block on it, and vice versa.
- No new external library dependency for the default (PBKDF2) path (§7).

---

## 17. Definition of Done

- [ ] **Decision documented**: this document itself, plus `CORE_SECURITY_INSTRUCTIONS.md` corrected per §15, stand as the permanent record that SHA-256 was evaluated, found non-compliant, and replaced — not silently patched without explanation.
- [ ] **Slow hash implemented**: `Pbkdf2CredentialHasher` (PBKDF2-HMAC-SHA256, parameters per §8) is the sole concrete `CredentialHasher` implementation in `core-security`; the prior SHA-256 concrete class is deleted, not merely superseded-but-present.
- [ ] `CredentialHasher`'s interface contract is unchanged; `ParentPinLocalStore` and `ChildLockRepository` compile and function against the new implementation with no call-site signature changes.
- [ ] Migration path (§11) implemented and tested: any pre-existing legacy-format cached hash is invalidated, never compared against, and safely repopulated via one forced online re-verification, with a distinct, non-alarming UX signal.
- [ ] p95 < 200ms offline-verification budget met on representative low-end hardware at the shipped iteration count, with the benchmark result recorded (§14.3/§14.6).
- [ ] Zero `MessageDigest`/SHA-256 usage remains anywhere in `core-security`'s `credential` package (§14.5).
- [ ] Full test suite (§14) passing.
- [ ] `secureHash()` (PII/analytics utility) confirmed untouched — out of scope, not accidentally modified.
- [ ] F.37 B-04's backend utility confirmed untouched — out of scope, not accidentally modified.

---

## 18. Assumptions or Decisions the Coding Agent Must Follow

1. **The algorithm is PBKDF2-HMAC-SHA256 at 600,000 iterations, 128-bit salt, 256-bit derived key** (§8.1–§8.3). This is not a menu of equally-valid options — it is the specified default. A KMP-native Argon2id binding is an explicitly deferred future option (§8.4), not an alternative the implementing agent should substitute on their own initiative for this Definition of Done.
2. **The migration strategy is forced cache invalidation on version upgrade, never in-place lazy rehashing** (§11.1/§11.2) — this is a deliberate, corpus-consistent (§12.4) choice, not an oversight; do not "improve" it into a lazy-rehash pattern even though that pattern is common elsewhere in the industry.
3. **The `CredentialHasher` interface signature does not change.** Any temptation to switch `hash(raw: String)` to `hash(raw: CharArray)` for stricter memory hygiene must be resisted for this Definition of Done — it is explicitly out of scope per §2.2 and K-01 §29 Task 04's own "keep the interface contract stable" instruction. Note it as a possible future hardening item if desired, but do not implement it here.
4. **Do not touch F.37 B-04's backend utility.** This document's entire subject is client-side; the backend Argon2id utility is referenced as a standard, never as code to modify.
5. **If the 600,000-iteration parameter fails the p95 < 200ms benchmark, tune downward only to the §8.3.1 floor (310,000), and escalate to Security Engineering (§9.5) rather than going lower unilaterally or reverting to a faster, non-compliant algorithm to hit the number.**
6. **`secureHash()` stays SHA-256 and stays untouched** — it protects a different, non-credential class of data (PII pseudonymization for analytics) and changing it is both unnecessary and out of scope (§3.1).
7. **If K-01 is independently scheduled and implemented**, treat its Task 04 as satisfied by this document's execution rather than re-implementing the same migration a second time (§12.4) — coordinate, don't duplicate.

---

## 19. AI Agent Development Prompt

You are implementing a security-critical algorithm migration inside NoorHeroes' KMP `core-security` module. Read this entire document (`Phase3_Shared_Core_Modules.KMP.17-core-security-credential-hashing-algorithm-verification.md`) fully before writing any code — it contains a verification finding, a decision, and a fully-specified implementation; do not re-litigate the decision in §1–§9, execute it.

**What you are verifying and fixing:** `core-security`'s `CredentialHasher` is currently documented and implemented using SHA-256 — a fast, general-purpose hash. It is used exclusively to cache a parent's own PIN (via the new/parallel `ParentPinLocalStore`, A.1 K-05) and a child's lock PIN/pattern (via `ChildLockRepository`, C.19 K-06) for **offline** parent-gate/child-lock verification. Both are low-entropy (4–6 digit) secrets gating access in a children's-safety product. The backend's equivalent utility (F.37 B-04) correctly uses Argon2id. This document's verification (§1–§9) confirms SHA-256 here is a genuine compliance gap — not an intentional, narrower-threat-model choice — because the local cache is exposed to the identical offline-brute-force risk once device storage is ever extracted (rooted/jailbroken device, forensic tooling, backup exposure), independent of whether the value ever travels over a network. C.19's own PRD §1.8 NFR ("Salted, slow (Argon2id-class) hashing for PIN/pattern storage") already states this requirement without a server-only carve-out.

**What to implement, in order (full detail in §13):**
1. Locate the current concrete `CredentialHasher` implementation in `core-security` and its exact current encoded-hash string format (do not assume — grep and confirm).
2. Implement `EncodedCredentialHash` (§6.2), `Pbkdf2Primitive` `expect`/`actual` (§6.4, Android via `javax.crypto`, iOS via `CommonCrypto`), and `Pbkdf2CredentialHasher` (§6.3) — PBKDF2-HMAC-SHA256, 600,000 iterations, 128-bit salt, 256-bit derived key. Delete the old SHA-256 concrete class entirely.
3. Implement the forced-invalidation migration path (§11.2): on detecting a legacy-format cached hash, delete it, never compare against it, and surface a distinct "requires one online re-verification" signal to `ParentPinLocalStore`/`ChildLockRepository`'s callers — never a plain "wrong PIN" error, never a silent fallback.
4. Benchmark the 600,000-iteration parameter against the project's actual low-end reference device; confirm p95 < 200ms (C.19 §1.8 NFR). If it fails, tune down only to the 310,000-iteration floor (§8.3.1) and escalate to Security Engineering if even that doesn't meet budget — do not go lower without that sign-off, and do not silently revert to a faster algorithm.
5. Correct `CORE_SECURITY_INSTRUCTIONS.md` §4 and §8 per the exact before/after text in §15.
6. Implement the full test suite in §14 (platform-parity KDF test vector, unit tests, the performance benchmark, the migration-path integration tests, the interface-stability confirmation).

**What you must NOT change:**
- F.37 B-04's backend Argon2id utility (`src/noorheroes/common/security/credential_hasher.py`) — do not touch it, do not add any coupling between it and this KMP work. It is referenced only as a standard.
- The `CredentialHasher` interface signature (`hash(raw: String): String` / `verify(input: String, hash: String): Boolean`) — keep it exactly as-is so `ParentPinLocalStore` and `ChildLockRepository` require zero call-site changes.
- `secureHash()` (the separate `crypto` package PII/analytics hashing utility) — different purpose, correctly SHA-256, out of scope.
- `ProgressiveLockoutPolicy`, PIN-length rules, `AuthState`/`MutableAuthStateHolder`'s own elevation-tracking logic, and `BiometricGate` — all untouched, all outside this document's scope.
- F.37 KMP K-01's other four tasks (Keystore-storage-location scan, biometric-template-transmission scan) — separate deliverables in the same source blueprint; not part of this task.

**How to verify you're done (full checklist in §17):**
- A known PBKDF2-HMAC-SHA256 test vector produces identical output on both the Android and iOS actuals.
- `Pbkdf2CredentialHasher` unit tests pass: unique salt per call, correct accept/reject, never throws on malformed input.
- Measured p95 latency on low-end reference hardware is under 200ms at whatever final iteration count you ship (record the number).
- A pre-seeded legacy-format cached hash is provably never compared against, is deleted, triggers the correct distinct UX signal, and is correctly repopulated in the new format after a simulated successful online re-verification.
- `AuthState.Parent.elevatedUntil` and biometric unlock are unaffected by the migration (regression check).
- A grep across `core-security`'s `credential` package for `MessageDigest`/`sha-256`/`SHA256` returns nothing outside test fixtures explicitly testing the legacy-format-rejection path.
- `CORE_SECURITY_INSTRUCTIONS.md` reflects the corrected algorithm.
- `ParentPinLocalStore` and `ChildLockRepository` compile and pass their existing test suites unmodified beyond the new migration branch.

If, during implementation, you discover a fact that contradicts this document's verification finding (e.g., you find `CredentialHasher`'s output is actually used somewhere this document didn't account for, such as being transmitted to a server anywhere), **stop and escalate rather than proceeding** — that would change the threat model this document's decision rests on, and the decision would need to be re-verified, not silently reinterpreted.
