# K-06 — Offline Lock Verification & Secure Local Cache

## 1. Feature Context
The dual-path design underpinning K-02 and K-05: a locked child selected while offline verifies against a locally cached salted hash, then enforces the last-signed restriction/entitlement policy — no network round-trip required for the lock check itself. This sub-feature owns the secure storage layer both depend on.

## 2. Parent Feature
Feature C.19 — Parent PIN/Biometric Gate & Profile Access Control

## 3. Sub-feature
2.6 Offline Lock Verification & Secure Local Cache (ID: **K-06**)

## 4. Objective
Harden `core-data`'s existing `ChildLockRepository` cached-hash storage (currently backing A.1 K-08) to guarantee Android Keystore-backed encryption for both the cached lock hash and the last-signed restriction/policy snapshot, never plaintext, with correct reconciliation against the server when connectivity returns.

## 5. Business Requirements
- FR-15: offline lock verification uses the locally cached salted hash; offline restriction check uses the last-signed policy.
- NFR (Performance): local lock verification p95 < 200ms, fully on-device, no network dependency.
- NFR (Reliability): the four-stage pipeline behaves identically online or offline, never silently skipping a stage.
- §12.4 Mobile Security: locally-cached lock hashes stored via Android Keystore-backed encrypted storage, never plaintext.

## 6. Existing Architecture
`core-data/ChildLockRepository` (existing, referenced by A.1 K-08 as already performing "local hash verification and validating the cached entitlement snapshot is within the allowed grace period"). This sub-feature audits and hardens its storage backend specifically for the Keystore-encryption guarantee, and extends it with the last-signed restriction-policy snapshot needed by K-05.

## 7. Existing Code to Reuse
- `core-data/ChildLockRepository.verifyChildLock()` (existing — audit storage backend, do not reimplement verification logic)
- Android Keystore APIs (via whatever wrapper `core-security` already exposes — confirm before introducing a new encryption utility)

## 8. Files to Create
- `test/core-data/ChildLockCacheEncryptionTest.kt` — asserts cached hash is never stored in plaintext (inspects underlying storage, not just the repository API)
- `test/core-data/RestrictionSnapshotCacheTest.kt`

## 9. Files to Modify
- `core-data/ChildLockRepository.kt` — audit/confirm Keystore-backed encrypted storage is actually used for the cached hash (not just assumed); migrate if a weaker mechanism (e.g., plain DataStore/SharedPreferences) is currently in use
- `core-data` — add `RestrictionSnapshotCache` for K-05's last-signed policy snapshot, same encryption standard

## 10. KMP Requirements
- Cached lock hash storage must use Android Keystore-backed encryption — audit the existing K-08 implementation; if it currently uses an unencrypted or weakly-encrypted store, this is a genuine Architecture Improvement (existing→problem→proposal→impact→implementation) to correct, not a new feature.
- `RestrictionSnapshotCache` stores the most recent signed restriction/entitlement response from B-04, versioned by timestamp/signature, consumed by K-05's offline path — the client verifies the signature/version rather than trusting an arbitrary local value.
- On reconnect, reconcile: if the server's authoritative state differs materially from what was used offline (e.g., a restriction that should have blocked access), apply the server's state going forward without disrupting an already-in-progress session ungracefully.

## 11. Required API
None directly — this is a storage-layer sub-feature consumed by K-02 (lock hash) and K-05 (restriction snapshot), which call B-01 and B-04 respectively when online.

## 12. Offline First
This sub-feature **is** the offline-first mechanism for the gate. Initial local load → remote refresh on connectivity → offline read/verify → retry/sync on reconnect → cache invalidation when the parent changes a child's lock configuration (old cached hash must be invalidated, not left stale).

## 13. Local Data
Android Keystore-backed encrypted storage for: cached lock hash per child, last-signed restriction/entitlement snapshot per child. Both invalidated/refreshed on every successful online verification/activation.

## 14. Localization
N/A — storage layer only, no user-facing strings.

## 15. RTL
N/A.

## 16. Analytics
`offline_lock_verification_used` (fired by K-02 when this cache serves a verification, not owned here but instrumented via this repository's return metadata).

## 17. Performance
Local verification must resolve in-process with no I/O beyond a single encrypted-store read — target p95 < 200ms end-to-end (this sub-feature's contribution should be a small fraction of that budget).

## 18. Security
- **Never plaintext, under any circumstance** — this is the sub-feature's entire reason for existing. The audit test (§19) inspects the actual underlying storage bytes, not just the repository's public API surface, to catch any accidental plaintext fallback.
- Cache invalidation on lock-configuration change prevents a stale offline hash from continuing to validate an old, parent-revoked lock.

## 19. Testing
- Unit: cached lock hash, when inspected at the storage layer directly (not via the repository API), is never plaintext or reversibly-weak-encoded (highest-priority test, mirrors K-02's server-side equivalent).
- Unit: restriction snapshot cache correctly versions and rejects a snapshot older than the currently cached one.
- Integration: lock-configuration change by the parent invalidates the previously cached hash for that child.
- Integration: reconnect reconciliation applies server-authoritative state without disrupting an active session ungracefully.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Audit Existing `ChildLockRepository` Storage Backend**
Objective: confirm actual encryption mechanism currently in use. Files to Read: `ChildLockRepository.kt` and its storage dependencies. Definition of Done: a clear finding — either "already Keystore-backed, confirmed" or "requires migration."

**Task 02 — Migrate to Keystore-Backed Storage (If Required)**
Objective: close any gap found in Task 01. Files to Modify: `ChildLockRepository.kt`. Dependencies: Task 01. (Skip if Task 01 confirms compliance.)

**Task 03 — Implement `RestrictionSnapshotCache`**
Objective: versioned, Keystore-backed storage for K-05's last-signed policy snapshot. Files to Create: within `core-data`. Dependencies: Task 01.

**Task 04 — Add Storage-Layer Encryption Audit Test**
Objective: inspect raw storage bytes, not just the API. Files to Create: `ChildLockCacheEncryptionTest.kt`. Dependencies: Task 01/02.

**Task 05 — Implement Cache Invalidation on Lock-Configuration Change**
Objective: prevent stale offline hash from validating a revoked lock. Files to Modify: `ChildLockRepository.kt`. Dependencies: Task 01/02.

**Task 06 — Add Full Test Suite**
Objective: coverage per §19. Dependencies: Task 01–05.

## 21. Final Verification Checklist
- [x] Cached lock hash confirmed Keystore-backed via direct storage-layer inspection, not just API-level assumption
- [x] Restriction snapshot cache versioned and reconciles correctly on reconnect
- [x] Lock-configuration change invalidates the old cached hash
- [x] No plaintext credential or hash artifact found anywhere in local storage

## 22. Definition of Done
`ChildLockRepository`'s offline cache (and the new `RestrictionSnapshotCache`) are confirmed or migrated to Android Keystore-backed encrypted storage, correctly invalidate on lock-configuration change, and reconcile cleanly with server-authoritative state on reconnect.

## 23. Verification & Compliance Record
- **Implementation Status**: COMPLETED (100% compliant with C.19 FR-15 and §12.4 Mobile Security)
- **Key Invariants Verified**:
  - `ChildLockRepository` cached lock hashes stored via Android Keystore-backed AES-GCM encrypted storage.
  - Automated storage audit test proves zero plaintext credentials or hash bytes in storage.
  - `RestrictionSnapshotCache` enforces versioning and signature integrity, rejecting stale/older snapshots.
  - Lock-configuration changes by parent invalidate old cached hashes.
  - Online reconciliation on reconnect preserves session stability.
- **Unit & Security Tests**:
  - `ChildLockCacheEncryptionTest.kt`: Storage-layer inspection verifying Keystore encryption and zero plaintext leakage.
  - `RestrictionSnapshotCacheTest.kt`: Versioning and snapshot validation.
  - `ChildLockRepositoryImplTest.kt`: Offline lock verification and cache invalidation.
- **Test Execution Result**:
  - `:core:core-data:testAndroidHostTest` -> SUCCESS (100% passing)
  - `:core:core-security:testAndroidHostTest` -> SUCCESS (100% passing)
