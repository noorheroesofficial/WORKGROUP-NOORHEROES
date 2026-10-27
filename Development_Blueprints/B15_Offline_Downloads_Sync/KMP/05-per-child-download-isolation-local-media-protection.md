# K-05 — Per-Child Download Isolation & Local Media Protection

## 1. Feature Context
Part of Feature B.15 (Offline Downloads & Sync). The security-hardening layer beneath K-02 — guarantees one child's downloaded media is never resolvable from a sibling's session on a shared device, and that raw media is never left in a freely-extractable location.

## 2. Parent Feature
B.15 — Offline Downloads & Sync

## 3. Sub-feature
K-05 — Per-Child Download Isolation & Local Media Protection

## 4. Objective
Implement per-child storage namespacing for all downloaded media and encrypted/sandboxed local storage where the platform supports it, verified by an instrumented cross-child-access test.

## 5. Business Requirements
- FR-8: downloaded media encrypted or sandboxed locally where the platform supports it — raw, freely-extractable media files never left in an unprotected, generally-accessible device location.
- FR-12: per-child download isolation — one child's downloaded content never exposed to or accessible from a sibling's session on a shared device, consistent with the platform-wide multi-child isolation principle.
- Edge Case 6: the same content requested by two different children on a shared device → each child's download stored in a separate, isolated namespace; access control enforces isolation regardless of underlying byte-level storage sharing.
- §5 Android AI Prompt item 4: per-child storage namespacing — Child A's cache entries not resolvable from Child B's `DownloadController` instance.
- §12.4 Mobile Security: encrypted/sandboxed media storage, per-child cache namespacing.

## 6. Existing Architecture
Extends K-02's `DownloadController`/local storage layer with a per-child namespace prefix on all file paths and `DownloadEntity` queries, plus platform encryption APIs (Android Keystore-backed file encryption / iOS Data Protection) — leverages the existing `core-security` module referenced in `CORE_DATA_INSTRUCTIONS.md`'s dependency rules rather than introducing a new security primitive.

## 7. Existing Code to Reuse
- `core-security` module (per `core-data`'s allowed-dependency list) — existing encryption/keystore abstractions.
- `core-database`'s `DownloadEntity` — `childId` column as the namespace key for every query (K-02 already scopes by `childId`; this blueprint hardens that scoping into a verified, non-bypassable guarantee).
- `AuthRepository.logout()`'s existing "deep clean" pattern (per `CORE_DATA_INSTRUCTIONS.md` §4) — extended to also wipe the logged-out child's namespaced media on session end where appropriate.

## 8. Files to Create
- `core-data/src/commonMain/kotlin/.../download/ChildStorageNamespace.kt` — namespace-path resolution utility.
- `core-data/src/androidMain/kotlin/.../download/AndroidMediaEncryption.kt`.
- `core-data/src/iosMain/kotlin/.../download/IosMediaProtection.kt`.
- `core-data/src/androidAndroidTest/kotlin/.../download/CrossChildAccessIsolationTest.kt` (instrumented).
- `core-data/src/commonTest/kotlin/.../download/ChildStorageNamespaceTest.kt`.

## 9. Files to Modify
- K-02's `DownloadController`/`AndroidDownloadEngine`/`IosDownloadEngine` — route all file writes through `ChildStorageNamespace.resolvePath(childId, contentId)` rather than a flat/shared storage path.
- `core-database`'s `DownloadDao` — confirm every query is `childId`-scoped (audit existing queries, add `childId` filter anywhere missing).

## 10. Backend Requirements
N/A — this is a purely local, client-side hardening layer.

## 11. KMP Requirements
- `ChildStorageNamespace.resolvePath(childId, contentId)`: deterministic, collision-free per-child subdirectory/keyspace for every downloaded file — no two children's media ever share a resolvable path, even for identical `contentId` values (Edge Case 6).
- `DownloadController` (K-02) exposes no method that can be called without a `childId` — every read/write is namespace-scoped by construction, not by convention alone.
- Encrypt media at rest where the platform supports it: Android via Keystore-backed file encryption (e.g., Jetpack Security `EncryptedFile` or equivalent), iOS via Data Protection API (`NSFileProtectionComplete` or equivalent) — applied immediately after K-02 marks a chunk validated-and-persisted.
- On child-session logout/deep-clean (`AuthRepository.logout()`), the logged-out child's namespaced download directory is handled consistently with the platform's existing session-cleanup policy (verify against `CORE_DATA_INSTRUCTIONS.md`'s existing deep-clean scope — this blueprint does not introduce a new deletion policy beyond what the existing logout flow already specifies for cached data).
- Underlying storage-layer dedup (if any content-addressable storage optimization exists) must never leak cross-child accessibility — the access-control layer (namespace resolution) is the enforced boundary regardless of any byte-level sharing beneath it.

## 12. NextJS Requirements
N/A.

## 13. API Contract
N/A — purely local.

## 14. Database Requirements
`core-database`'s `DownloadEntity` — audit and confirm `childId`-scoping on every DAO query used by K-02/K-03/K-04.

## 15. Validation
`ChildStorageNamespace.resolvePath()` rejects a null/empty `childId` at the type level (non-nullable parameter) — there is no code path that can resolve a storage path without a concrete child identity.

## 16. Authentication
N/A directly — relies on the active child-mode session already established elsewhere in the app; this module trusts the `childId` passed to it by the already-authenticated caller (K-02).

## 17. Authorization
This module **is** the authorization boundary for per-child media access — no other module bypasses it to read/write downloaded media directly.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Encryption API unavailable on a given platform/OS version | Falls back to the platform's best-available sandboxing (app-private storage), never falls back to fully unprotected shared storage |
| Namespace resolution called without a valid `childId` | Compile-time prevented (non-nullable parameter) — no runtime fallback path exists |
| Cross-child path collision attempt (theoretical) | Structurally impossible by construction of the namespace key (includes `childId` as a non-optional path segment) |

## 19. Offline First
N/A directly — this is a storage-security layer beneath the already-offline-first K-02/K-03.

## 20. Local Data
Owns the storage-path/encryption policy for all of K-02's persisted media.

## 21. Localization
N/A.

## 22. RTL
N/A.

## 23. Analytics
No dedicated analytics event — this is a security-hardening layer, not a user-facing feature surface.

## 24. Performance
Namespace-path resolution is a pure, cheap string-construction function; encryption/decryption overhead is bounded to the platform's native, hardware-accelerated implementation (Keystore/Data Protection), not a custom cipher implementation.

## 25. Security
- This blueprint's entire purpose is a security guarantee: cross-child inaccessibility and no unprotected raw media on device.
- No raw, freely-extractable media file is ever written outside the per-child encrypted/sandboxed namespace — verified in code review as a hard architectural rule, not merely tested behavior.
- Underlying OS-level file-system dedup or content-addressable storage optimizations (if any exist elsewhere in the media pipeline) are explicitly documented as not a substitute for this access-control layer.

## 26. Library Requirements
Platform security APIs: Android Jetpack Security (`EncryptedFile`) or Keystore-backed equivalent, iOS Data Protection API. No third-party crypto library — reuses `core-security`'s existing abstractions.

## 27. Testing
- **Instrumented cross-child isolation test (mandatory):** Child A downloads content; assert Child B's `DownloadController` instance on the same device cannot resolve, read, or enumerate Child A's namespaced files (§5 item 4, non-bypassable CI gate).
- Unit: `ChildStorageNamespace.resolvePath()` produces distinct, non-colliding paths for the same `contentId` across two different `childId` values (Edge Case 6).
- Unit: encryption applied to every persisted chunk; a raw, unencrypted file is never found in the app's shared/generally-accessible storage locations (verified via a filesystem-scan test in a debug build).
- Unit: fallback-to-sandboxing behavior on an environment lacking full encryption API support, confirming it never falls back further to unprotected shared storage.

## 28. Documentation
KDoc explicitly stating this module is the platform's enforced access-control boundary for downloaded media, and that no other module may read/write media files directly, bypassing it.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Implement ChildStorageNamespace**
Objective: deterministic, collision-free per-child path/key resolution.
Files to create: `ChildStorageNamespace.kt`.

**Task 02 — Implement AndroidMediaEncryption**
Files to create: `AndroidMediaEncryption.kt`.

**Task 03 — Implement IosMediaProtection**
Files to create: `IosMediaProtection.kt`.

**Task 04 — Wire Namespace + Encryption into K-02's DownloadController**
Files to modify: `DownloadController.kt`, `AndroidDownloadEngine.kt`, `IosDownloadEngine.kt`.

**Task 05 — Audit and Harden DownloadDao Queries**
Files to modify: `DownloadDao.kt` (confirm/add `childId` scoping on every query).

**Task 06 — Add Cross-Child Isolation Instrumented Test (highest priority)**
Tests: `CrossChildAccessIsolationTest.kt`.
Definition of done: CI-blocking gate.

**Task 07 — Add Namespace Collision & Filesystem-Scan Tests**
Tests: `ChildStorageNamespaceTest.kt`.

**Task 08 — Final Code Review**
Objective: confirm no module reads/writes downloaded media bypassing this namespace/encryption layer.

## 30. Definition of Done
- Cross-child isolation verified by instrumented test.
- All downloaded media encrypted/sandboxed at rest where platform-supported.
- No raw, unprotected media file found in generally-accessible storage — verified by filesystem scan.
- Every `DownloadDao` query confirmed `childId`-scoped.

## 31. Final Verification Checklist
- [ ] Cross-child media access structurally impossible — verified by instrumented test.
- [ ] No raw, unencrypted media in generally-accessible storage — verified by filesystem scan.
- [ ] Every DAO query scoped by `childId`.
- [ ] Fallback-when-encryption-unavailable never degrades to fully unprotected storage.
- [ ] No module bypasses this layer to access media directly — verified in code review.
