# K-01 — Keystore-Backed Credential-Caching Architectural Scan

## 1. Feature Context
NoorHeroes' KMP app caches PIN/pattern-derived credential material locally for offline lock verification (C.19). This blueprint implements the architectural static-scan test that structurally guarantees that cache always uses platform Keystore-backed encrypted storage, never plaintext preferences. No school/institutional/madarsa logic applies.

## 2. Parent Feature
F.37 — Security Architecture (Cross-Cutting).

## 3. Sub-feature
K-01 — Keystore-Backed Credential-Caching Architectural Scan (KMP / Android & iOS).

## 4. Objective
Write one cross-cutting static-scan test confirming `core-security`'s locally-cached credential material (used for C.19's offline lock verification) exclusively uses Android Keystore-backed encrypted storage, per PRD §6.10/§7 (Android AI Code-Generation Prompt) and FR-10's secure-storage principle applied at the client layer. **Scope widened per confirmed cross-reference against C.19's PRD (source of truth):** also migrate `CredentialHasher` off its currently-documented SHA-256 implementation to a slow, Argon2id-class algorithm, since C.19 §1.8's NFR ("Salted, slow (Argon2id-class) hashing for PIN/pattern storage") applies to the offline-cached hash as well, not only server-side storage — see §25/Task 04.

## 5. Business Requirements
- PRD §6.4: "`:core:auth`'s token storage must never persist a refresh token in a way that survives a server-side rotation incorrectly" — related but distinct concern from this blueprint's specific PIN/pattern-cache focus.
- PRD §6.10 (Testing Strategy): "Architectural test (cross-cutting): confirm `:core:auth`'s token-storage implementation uses Android Keystore-backed encrypted storage for any locally-cached credential material... never plaintext SharedPreferences, reinforcing this document's slow-hash/secure-storage principle at the client layer."
- PRD §7 (Android AI Code-Generation Prompt, verbatim requirement): "Write ONE cross-cutting architectural test confirming `:core:auth`'s local credential-caching implementation... exclusively uses Android Keystore-backed encrypted storage -- scan for any direct `SharedPreferences.putString()` call involving a variable named/typed in a way suggestive of a PIN, pattern, or hash value, and assert none exist outside the Keystore-backed storage abstraction."

## 6. Existing Architecture
Per `CORE_SECURITY_INSTRUCTIONS.md`: the `core-security` module (package `com.noorheroes.core.security.*`) owns authentication state (`AuthState`), credential verification (`credential` package: `BiometricGate`, `CredentialHasher`), and data security (`crypto` package: `DatabaseKeyProvider`, `secureHash`, `nextSecureRandomBytes`). Its "Prohibited Patterns" section already states: "NEVER use raw `MessageDigest` or `SecureRandom` directly; always use the provided abstractions in the `crypto` package" — this blueprint extends that same discipline to local storage of credential-derived material specifically.
Per `CORE_DATASTORE_INSTRUCTIONS.md`: `core-datastore`'s own "What NOT to Add Here" section already states "❌ Sensitive Data: Use `core-security` (Keychain/EncryptedSharedPreferences)" — confirming the architectural boundary this scan enforces is already documented intent, not a new invention; this blueprint makes that intent structurally verified rather than merely written guidance.

## 7. Existing Code to Reuse
- `core-security`'s `TokenStore` interface (secure JWT persistence, per the module's Quick Reference Table) — the Keystore-backed abstraction this scan should confirm is used.
- `core-security`'s `DatabaseKeyProvider`/`CommonDatabaseKeyProvider` pattern (EncryptedSharedPreferences/Keychain-backed) as the reference implementation pattern for what "correct" looks like.
- `CredentialHasher` interface — note per §25 below, flag (don't silently resolve) a potential inconsistency between this interface's documented SHA-256 usage and the platform's slow-hash mandate.

## 8. Files to Create
- `core-security/src/commonTest/kotlin/.../CredentialCacheStorageScanTest.kt` (or the project's actual existing test-source-set convention for cross-cutting/architectural KMP tests — confirm exact path convention before creating).
- A static-analysis script (if the scan is implemented outside pure Kotlin test code, e.g., as a Python/shell AST or regex scan over the Android source tree, consistent with how the equivalent backend architectural tests in B-03/B-04/B-06 are implemented) — place under whatever the project's existing static-analysis tooling location is.

## 9. Files to Modify
- `core-security`'s `CredentialHasher` concrete implementation (confirmed necessary, not contingent — see Task 04) — migrate from SHA-256 to a slow, Argon2id-class algorithm.
- `CORE_SECURITY_INSTRUCTIONS.md` — correct the documented algorithm.
- Any storage-location violation the scan discovers (a `SharedPreferences.putString()` call with a PIN/pattern/hash-suggestive variable outside the Keystore-backed abstraction) — contingent on scan findings, not a predetermined file list.

## 10. Backend Requirements
N/A — this is a KMP-only blueprint.

## 11. KMP Requirements
- Implement a scan (static-analysis script or a build-time/CI check) over Android-source Kotlin files that flags any direct call of `SharedPreferences.putString(...)` (or `edit { putString(...) }` Android KTX equivalent) where the key name or the variable being stored is suggestively named/typed for PIN, pattern, or hash material (heuristic keyword match: `pin`, `pattern`, `lock`, `hash`, `credential`, case-insensitive, tunable).
- Assert zero such matches exist outside the Keystore-backed storage abstraction (i.e., inside `core-security`'s own internal Keystore-wrapping implementation, such matches are expected and excluded from the scan — only *other* modules/files bypassing the abstraction are violations).
- Cover both the Android-actual implementation and confirm the iOS-actual implementation (Keychain-backed) receives equivalent scrutiny, even though the PRD's literal example is Android-`SharedPreferences`-specific — the underlying principle (never plaintext credential-derived storage) is platform-agnostic per FR-10.
- Migrate `CredentialHasher`'s hashing algorithm from SHA-256 to a slow, Argon2id-class algorithm (or documented PBKDF2-HMAC-SHA256 high-iteration fallback), per §25/§26/Task 04, meeting C.19 §1.8's p95 < 200ms offline-verification latency budget.

## 12. NextJS Requirements
N/A.

## 13. API Contract
N/A — no network contract involved; this is a purely local, on-device static-analysis concern.

## 14. Database Requirements
N/A.

## 15. Validation
The scan's heuristic must balance false negatives (missing an actual violation due to too-narrow keyword matching) against false positives (flagging legitimate, non-sensitive `SharedPreferences` usage that merely happens to contain a matched substring) — tune the keyword list against the actual codebase's naming conventions rather than a generic guess, and document any deliberately-excluded false-positive cases with a clear justification comment in the test itself.

## 16. Authentication
N/A directly — this scan verifies the *storage* of authentication-adjacent material, not authentication logic itself.

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Scan finds a violation | CI build fails with a clear message identifying the file/line and the matched pattern |
| Scan produces a false positive | Documented exclusion with justification, not a silent broadening of the heuristic that could mask real future violations |

## 19. Offline First
Directly relevant: the credential material this scan protects is specifically the cache C.19 uses for **offline** lock verification — this scan's correctness is a precondition for that offline flow being secure.

## 20. Local Data
This blueprint's entire subject matter is local, on-device data storage discipline.

## 21. Localization
N/A.

## 22. RTL
N/A.

## 23. Analytics
N/A — no runtime event; this is a build-time/CI static check.

## 24. Performance
The scan should run quickly enough to be part of every CI run without materially slowing the build (a targeted AST/regex scan over `core-security` and any module touching credential caching, not a full-repository deep scan).

## 25. Security
- This is the client-side enforcement half of FR-10's slow-hash/secure-storage principle (the server-side half is B-04).
- **Resolved (previously an open flag — now confirmed against C.19's own PRD, source of truth):** `Feature_C19_Parent_PIN_Biometric_Gate.md` FR-15 confirms the client-side cache exists specifically for **offline lock verification** ("a locked child selected while offline verifies against the locally cached salted hash... no network round-trip is required for the lock check itself") and §5 (Backend AI Code-Generation Prompt, item 6) confirms "the server-side path is always authoritative when connectivity is available" — so `CredentialHasher`'s cached hash never substitutes for server-side verification while online, which resolves the *substitution* half of the original concern.
- However, C.19 §1.8 (Non-Functional Requirements) states plainly: **"Salted, slow (Argon2id-class) hashing for PIN/pattern storage"** as a feature-wide security NFR — this statement is not scoped to "server-side only"; it governs FR-15's locally-cached hash too, since that cached value is itself PIN/pattern-derived storage sitting on a real device that can be extracted (rooted device, OS-level compromise, forensic tooling against the Keystore-backed store). `CORE_SECURITY_INSTRUCTIONS.md` §4's current documentation of `CredentialHasher.hash()` as "Salts and hashes using SHA-256" is therefore a **genuine compliance gap, not merely an open question**: SHA-256 is a fast general-purpose hash, and Keystore-backed *storage* protects the hash at rest but does not compensate for a fast *algorithm* if that storage layer is ever bypassed or extracted. This blueprint's scope is widened accordingly (see Task 06) to close this gap, not merely flag it.

## 26. Library Requirements
Storage layer: no new dependency — Android Keystore/`EncryptedSharedPreferences` and iOS Keychain are platform APIs already presumably wrapped by `core-security`'s existing `DatabaseKeyProvider`-style abstractions. Scan tooling: a lightweight existing static-analysis approach (regex/AST) consistent with whatever the KMP project's CI already uses for lint/detekt-style checks. Hashing layer (new, per Task 06): a KMP-compatible slow-hash implementation is required to replace `CredentialHasher`'s SHA-256 — prefer a true Argon2id KMP binding if one exists/can be added (e.g., an `expect`/`actual` wrapper over a native Argon2 library per platform: Android via a JVM/NDK Argon2 binding, iOS via a Swift/C Argon2 binding); if no such binding is feasible without disproportionate native-toolchain overhead for a purely-local, offline-comparison-only cache, PBKDF2-HMAC-SHA256 with a high iteration count (tuned per current OWASP guidance, e.g., ≥600,000 iterations) is an acceptable documented fallback, since both `kotlinx-crypto`-adjacent and platform-native PBKDF2 implementations are commonly available cross-platform without new native dependencies — this decision must be made explicitly and documented, not defaulted to silently.

## 27. Testing
- **Scan test (the deliverable itself):** confirms zero direct `SharedPreferences.putString()` (or equivalent) calls with PIN/pattern/hash-suggestive naming outside the Keystore-backed abstraction.
- **Negative/regression test:** deliberately introduce a violating pattern in a scratch/test fixture file and confirm the scan correctly flags it (proving the scan actually works, not just that it currently finds nothing).
- **iOS equivalent:** confirm Keychain-backed storage is used for the same credential-cache purpose on iOS (via whatever verification approach is appropriate for iOS-actual code — Swift/Obj-C static scan or a documented manual audit if automated scanning isn't yet set up for iOS sources).

## 28. Documentation
Document the scan's heuristic and rationale in the test file itself; document the flagged `CredentialHasher`/SHA-256 architectural question (§25) as a tracked follow-up item, cross-referenced from B-04's documentation.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Audit Current Credential-Caching Call Sites**
- Task ID: K-01-T01
- Objective: Locate every current local-storage call site touching PIN/pattern/hash-derived material across `core-security` and any consuming feature module (primarily C.19).
- Why This Is Required: Cannot write a meaningful scan without first understanding current usage, including confirming whether any existing violation already exists.
- Existing Architecture to Follow: `core-security`'s package structure (`auth`, `credential`, `crypto`).
- Existing Files to Reuse: none yet (audit only).
- Files to Create: none yet.
- Files to Modify: none yet.
- Implementation Details: search Android-actual and iOS-actual source sets for `SharedPreferences`/`EncryptedSharedPreferences`/Keychain usage related to credential material.
- Business Rules / Validation / Error Handling / Security / Performance: N/A (audit only).
- Localization / RTL / Analytics: N/A.
- Tests: none yet.
- Documentation: audit findings feed Task 02.
- Dependencies: none.
- Do Not Change: nothing yet.
- Expected Result: complete current-state inventory, including confirmation of whether any existing violation exists.
- Definition of Done: audit documented.

**Task 02 — Remediate Any Found Violations**
- Task ID: K-01-T02
- Objective: If Task 01 found any plaintext-preference storage of credential material, migrate it to the Keystore-backed abstraction.
- Why This Is Required: The scan (Task 03) must pass against a genuinely compliant codebase, not merely be written and left failing.
- Existing Architecture to Follow: `core-security`'s existing `DatabaseKeyProvider`/Keystore-backed pattern.
- Existing Files to Reuse: the compliant reference pattern already in `core-security`.
- Files to Create: none prescribed — depends on findings.
- Files to Modify: whichever file(s) Task 01 flagged, if any.
- Implementation Details: case-by-case migration to the Keystore-backed abstraction.
- Business Rules: no behavior regression for the consuming feature (C.19's offline lock verification must continue working identically from the user's perspective).
- Validation: N/A beyond existing.
- Error Handling: preserve existing error/fallback behavior (e.g., `BiometricResult.Unavailable` → PIN fallback, per `CORE_SECURITY_INSTRUCTIONS.md` §7).
- Security: this is the actual fix if a violation exists.
- Performance: N/A.
- Localization / RTL / Analytics: N/A.
- Tests: add/update tests for the migrated storage call.
- Documentation: note the remediation.
- Dependencies: Task 01.
- Do Not Change: unrelated `core-security`/C.19 logic.
- Expected Result: codebase is clean (or confirmed already clean).
- Definition of Done: no remaining violations per a re-run of Task 01's audit.

**Task 03 — Implement the Architectural Scan Test**
- Task ID: K-01-T03
- Objective: Write the scan per §11/§27.
- Why This Is Required: This is the actual, durable, CI-enforced deliverable per PRD §7's explicit requirement.
- Existing Architecture to Follow: whatever static-analysis tooling the KMP project's CI already uses.
- Existing Files to Reuse: none.
- Files to Create: the scan test/script per §8.
- Files to Modify: CI configuration to run this scan on every build.
- Implementation Details: per §11; heuristic keyword-based flagging of `SharedPreferences.putString()` calls, excluding the Keystore-backed abstraction's own internals.
- Business Rules: zero tolerance, matching the backend architectural tests' (B-03/B-04/B-06) pattern of CI-blocking enforcement.
- Validation: as in §15 (tune heuristic, document exclusions).
- Error Handling: clear failure message per §18.
- Security: this scan is itself a security control — should not be skippable without Security Engineering sign-off, mirroring the backend architectural tests' treatment.
- Performance: fast scan per §24.
- Localization / RTL: N/A.
- Analytics: N/A.
- Tests: the negative/regression test per §27 (deliberately-introduced violation is caught).
- Documentation: heuristic rationale documented in the test file (§28).
- Dependencies: Task 01, Task 02.
- Do Not Change: N/A.
- Expected Result: any future PR introducing plaintext credential-material storage fails CI.
- Definition of Done: scan passes against the current (clean) codebase and correctly catches a deliberately-introduced violation in the negative test.

**Task 04 — Migrate `CredentialHasher` from SHA-256 to a Slow, Argon2id-Class Algorithm**
- Task ID: K-01-T04
- Objective: Replace `CredentialHasher`'s SHA-256-based implementation with a slow, salted, Argon2id-class hash (or the documented PBKDF2-HMAC-SHA256 high-iteration fallback per §26), closing the compliance gap confirmed in §25 against C.19 §1.8's NFR.
- Why This Is Required: C.19's own PRD (source of truth) requires "Salted, slow (Argon2id-class) hashing for PIN/pattern storage" without carving out an exception for the offline-cached copy; the currently-documented SHA-256 implementation does not meet this bar, independent of the fact that the cache is offline-comparison-only.
- Existing Architecture to Follow: `core-security`'s `crypto` package conventions (`secureHash`, `nextSecureRandomBytes`) as the existing primitive-wrapping pattern to extend, not bypass.
- Existing Files to Reuse: `core-security`'s existing `CredentialHasher` interface (keep the interface contract — `hash(raw)`/`verify(input, hash)` — stable so calling code, including C.19's `LockRepository`, requires no interface-level changes).
- Files to Create: the new Argon2id (or PBKDF2 fallback) implementation module within `core-security`'s `crypto` package (exact filename per existing module convention).
- Files to Modify: `CredentialHasher`'s concrete implementation; `CORE_SECURITY_INSTRUCTIONS.md`'s own documentation (§4 API Usage Guide) to reflect the corrected algorithm, since the current doc text is itself part of what caused this gap to go unnoticed.
- Implementation Details: unique salt per credential (already required, confirm preserved); tuned cost parameters appropriate for a client-side, latency-sensitive offline lock check (C.19 §1.8 NFR: "Local lock verification must not require a network round-trip — p95 < 200ms, fully on-device" — the chosen parameters must keep verification within this budget on representative low-end Android/iOS hardware, which may mean lighter Argon2id parameters than the server-side B-04 utility uses, or the PBKDF2 fallback if Argon2id can't hit this latency budget on-device; document whichever trade-off is chosen and why).
- Business Rules: existing cached hashes computed under the old SHA-256 implementation cannot be safely "upgraded in place" (a raw PIN can't be recovered from a fast hash to re-hash slowly) — on app update, the local cache must be invalidated/cleared, forcing a one-time fresh online verification (or fresh PIN entry) to repopulate the offline cache under the new algorithm; this must not lock a legitimate parent/child out, only require one online-connected re-verification.
- Validation: N/A beyond existing `CredentialHasher` contract validation.
- Error Handling: cache-invalidation-on-migration must fail gracefully to "require online verification" rather than crash or silently accept the old fast hash.
- Security: this task is the actual fix for the gap identified in §25; must hit the p95 < 200ms budget without regressing to a fast, insecure hash to do so — if no configuration achieves both, escalate to Security Engineering per the same sign-off bar as B-04 rather than silently picking speed over security.
- Performance: benchmark against C.19's explicit p95 < 200ms NFR on representative low-end device hardware, not just a development machine.
- Localization / RTL: N/A.
- Analytics: none new; existing C.19 `offline_lock_verification_used` event (per C.19 §1.19) is unaffected by this internal algorithm change.
- Tests: unit tests for the new hash/verify implementation (unique salt, correct accept/reject); a migration test confirming an old SHA-256-cached value is correctly invalidated (never silently accepted) on first run post-update; a performance test confirming the p95 < 200ms budget is met.
- Documentation: update `CORE_SECURITY_INSTRUCTIONS.md`'s `CredentialHasher` section to state the actual algorithm and parameters, so this document itself stops being the source of the confusion this task fixes.
- Dependencies: Task 01, Task 02, Task 03 (storage-location scan should already be clean before changing the algorithm layered on top of it).
- Do Not Change: the `CredentialHasher` interface contract itself (keep `hash`/`verify` signatures stable); do not touch B-04's separate server-side utility (different module, different latency budget, coordinate but don't merge).
- Expected Result: `CredentialHasher` uses a slow, salted, Argon2id-class (or documented PBKDF2 fallback) algorithm meeting C.19's NFR, with safe migration of any pre-existing fast-hash cached values.
- Definition of Done: unit, migration, and performance tests all pass; `CORE_SECURITY_INSTRUCTIONS.md` corrected.

**Task 05 — Architectural Test: Zero Biometric-Template Transmission/Storage**
- Task ID: K-01-T05
- Objective: Add a static-scan/structural test confirming no biometric-template-shaped data ever leaves `BiometricGate`'s result type or crosses into any repository/network call — closing PRD Security Checklist §12.9's "Zero biometric-template storage verified" item, which was previously unverified by any blueprint (identified during re-scan for missing coverage).
- Why This Is Required: FR-10/C.19 §3.5 both state biometric data is never transmitted to or stored by NoorHeroes servers, and `CORE_SECURITY_INSTRUCTIONS.md`'s `BiometricResult` type (`Success`/`Unavailable`/`Error`) is structurally designed to never carry template data — but this design intent was never actually verified by a test anywhere in the F.37 blueprint set until now.
- Existing Architecture to Follow: `core-security`'s `BiometricGate`/`BiometricResult` (§4 of `CORE_SECURITY_INSTRUCTIONS.md`).
- Existing Files to Reuse: `BiometricGate` interface and its result type (read-only reference, confirm the type structurally cannot carry a template — no `ByteArray`/`String` payload field on `Success`).
- Files to Create: a static-scan test (companion to Task 03's scan) confirming (a) `BiometricResult.Success` carries no template-shaped payload field, and (b) no network/repository call site anywhere in the codebase passes a `BiometricResult`-derived value (beyond the boolean/enum outcome itself) into any API request body.
- Files to Modify: none expected unless a violation is found, in which case remediate per the same pattern as Task 02.
- Implementation Details: type-level check (does `BiometricResult.Success` have any field beyond what's needed to proceed?) plus a call-site scan (does any `AuthApiService`/network call reference biometric-derived byte/string data?).
- Business Rules: zero tolerance, matching the PRD's zero-exception framing for this rule.
- Validation: this test is the validator.
- Error Handling: clear failure message if either check fails.
- Security: this is the direct implementation of §12.9's checklist item.
- Performance: fast, targeted scan.
- Localization / RTL / Analytics: N/A.
- Tests: this task's deliverable is a test.
- Documentation: cross-reference from `CORE_SECURITY_INSTRUCTIONS.md`'s `BiometricGate` section and from F.37's own Security Checklist (§12.9) as the item this test closes out.
- Dependencies: none beyond existing `BiometricGate` code.
- Do Not Change: `BiometricGate`'s actual OS-delegation behavior (out of scope, already correct by design — this task only adds verification).
- Expected Result: structural proof that no biometric template is ever transmitted or stored anywhere in the codebase.
- Definition of Done: test passes against the current codebase; PRD §12.9's checklist item is now backed by an actual automated check, not merely a design assumption.

## 30. Definition of Done
Credential-caching call sites audited and confirmed (or remediated) to use only Keystore/Keychain-backed storage; CI-blocking scan test implemented and passing, including a negative/regression proof; `CredentialHasher` migrated from SHA-256 to a slow, Argon2id-class (or documented PBKDF2 fallback) algorithm meeting C.19's p95 < 200ms NFR, with safe cache invalidation for any pre-existing fast-hash values, and `CORE_SECURITY_INSTRUCTIONS.md` corrected to match; zero-biometric-template-storage structurally verified via an automated test (previously unverified).

## 31. Final Verification Checklist
- [ ] All current PIN/pattern/hash-material storage call sites audited
- [ ] Any found violations remediated to use Keystore/Keychain-backed abstraction
- [ ] CI-blocking scan test implemented, passing against the clean codebase
- [ ] Negative/regression test proves the scan actually catches a deliberately-introduced violation
- [ ] iOS Keychain-backed equivalent confirmed (automated or documented manual audit)
- [ ] `CredentialHasher` migrated to a slow, Argon2id-class (or documented PBKDF2-fallback) algorithm — SHA-256 no longer used anywhere in the credential-cache path
- [ ] Migration path safely invalidates any pre-existing SHA-256-cached values (forces one online re-verification, never silently accepts the old fast hash)
- [ ] p95 < 200ms offline-verification latency budget (C.19 §1.8) met with the new algorithm on representative low-end hardware
- [ ] `CORE_SECURITY_INSTRUCTIONS.md` updated to document the corrected algorithm
- [ ] Zero-biometric-template-storage structural test implemented and passing (PRD §12.9 checklist item, previously unverified)
- [ ] No behavior regression to C.19's offline lock-verification flow
