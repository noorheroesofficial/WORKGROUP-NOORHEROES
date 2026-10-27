# B-04 — Slow-Hash Credential Storage Utility

> **Status:** Implemented & Verified  
> **Target Framework:** FastAPI (Python 3.12+)  
> **Canonical Implementation:** `src/noorheroes/common/security/credential_hasher.py`  
> **Unit & Latency Test Suite:** `tests/common/test_credential_hasher.py`  
> **CI Architectural Scan:** `tests/architecture/test_no_fast_hash_in_credential_path.py`  

## 1. Feature Context
NoorHeroes stores two credential types server-side: parent PIN and child lock pattern/PIN. This blueprint implements the single shared hashing utility that both must use, eliminating brute-force feasibility even if a hash were ever exfiltrated. No school/institutional/madarsa logic applies.

## 2. Parent Feature
F.37 — Security Architecture (Cross-Cutting).

## 3. Sub-feature
B-04 — Slow-Hash Credential Storage Utility (Backend / FastAPI).

## 4. Objective
Implement a shared credential-hashing utility using Argon2id exclusively, used by every credential-storage code path, with a dependency/import-scan test confirming no fast general-purpose hash function is used anywhere in that path, per PRD FR-10 and the §5 Backend AI Code-Generation Prompt item 4.

## 5. Business Requirements
- FR-10: "PIN and lock-pattern hashes use a slow, salted hashing algorithm (e.g., bcrypt or argon2) — never a fast general-purpose hash."
- NFR §1.8: "Slow-Hash Credential Storage: Every credential (parent PIN, child lock pattern/PIN) uses a slow, salted algorithm — never a fast general-purpose hash, eliminating brute-force feasibility even if a hash were ever exfiltrated."
- Acceptance Criterion §1.9: "Given any PIN or lock-pattern value is stored, when inspected, then it uses a slow, salted hash — never a fast general-purpose hash function."
- Security Checklist §12.9: "Slow-hash-only credential storage verified, no fast general-purpose hash anywhere."

## 6. Existing Architecture
- `identity` context (parent PIN) and whichever context owns child lock/pattern storage (confirm exact owning context — likely `identity` as well, or a child-profile-specific service; verify against the actual codebase rather than assuming) both need this utility.
- `common/utils/` (`FAST-API-INSTRUCTIONS.md` §3) is the existing home for shared, non-domain-specific utility functions — this is the natural home for the hashing utility unless a more specific `core/security.py`-adjacent location already exists for credential-related primitives (cross-check against B-01's `core/security.py` placement for consistency).

## 7. Existing Code to Reuse
None expected to exist yet in a compliant form — this blueprint's job is precisely to check whether a fast-hash implementation currently exists (e.g., a `hashlib.sha256`-based PIN check) and replace it. Search the codebase for existing PIN/pattern verification logic before writing new code; do not create a second, parallel hashing path alongside an existing one.

## 8. Files to Create
- `src/noorheroes/common/security/credential_hasher.py` — the shared Argon2id hashing utility (exact path to be reconciled with whatever `common/`/`core/` convention already governs security-adjacent shared code).
- `tests/common/test_credential_hasher.py`.
- `tests/architecture/test_no_fast_hash_in_credential_path.py`.

## 9. Files to Modify
- Every existing call site that currently hashes/verifies a parent PIN or child lock pattern/PIN — locate via search (e.g., grep for `hashlib`, `bcrypt`, or ad hoc hashing logic near PIN/pattern-related models) and migrate each to the new shared utility.

## 10. Backend Requirements
- `hash_credential(raw: str) -> str` — generates a cryptographically secure random salt, applies Argon2id with sane, documented cost parameters (memory cost, time cost, parallelism — chosen per current OWASP Argon2id guidance, tuned so hashing latency stays within acceptable request-latency bounds per §24), returns the encoded hash+salt string.
- `verify_credential(raw: str, stored_hash: str) -> bool` — verifies without ever re-deriving/comparing raw values insecurely (constant-time comparison, which Argon2id libraries provide natively).
- Both parent-PIN and child-lock-pattern/PIN storage paths call these two functions exclusively.

## 11. KMP Requirements
**Resolved (previously an open flag):** cross-checked against C.19's own PRD — `CredentialHasher`'s client-side hash is confirmed offline-comparison-only; the server-side path (this blueprint) is always authoritative when connectivity is available (C.19 §5 item 6), so no substitution risk exists. However, C.19 §1.8's NFR ("Salted, slow (Argon2id-class) hashing for PIN/pattern storage") applies to the offline-cached hash too, and `CredentialHasher`'s currently-documented SHA-256 implementation does not meet that bar. This is now tracked and being fixed under **K-01 Task 04** (migrate `CredentialHasher` to a slow, Argon2id-class algorithm) — not a change to this blueprint's own server-side utility, but noted here for cross-reference since both utilities exist to satisfy the same platform-wide FR-10 principle.

## 12. NextJS Requirements
N/A — Admin Portal authentication uses MFA/passkeys (E.28), not PIN/pattern hashing; this utility is not consumed by the Admin Portal.

## 13. API Contract
No new endpoint. This blueprint changes the internal storage mechanism behind existing PIN/pattern-setting and PIN/pattern-verification endpoints (owned by A.1/C.19/C.21); request/response shapes are unchanged.

## 14. Database Requirements
Existing `parent_pin` / `child_lock` tables (per PRD §4.1 note: "every relevant table... is already specified by its owning feature") store the hash string, never plaintext. This blueprint does not add new tables; it may require a migration if the stored hash format changes (e.g., adding an Argon2id-identifying prefix) — if an existing fast-hash value is found in production data, this requires a **credential-reset migration plan** (users must re-set their PIN; a raw value cannot be re-hashed after the fact) — flag this explicitly as a coordination point with the release plan (§15) rather than silently overwriting data.

## 15. Validation
- Reject empty/null raw credential input before hashing.
- `verify_credential` returns `False` (never raises) on a malformed stored-hash value, treated as a verification failure, not a crash.

## 16. Authentication
This utility underlies PIN/pattern-based authentication step-ups (C.19) but does not itself implement session/token issuance (that's B-01/B-02).

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Verification fails (wrong PIN/pattern) | `False` returned; caller applies `ProgressiveLockoutPolicy`-equivalent server-side lockout tracking (cross-ref C.19's lockout tiers; confirm server-side lockout state exists or whether lockout is currently client-only — do not assume, verify) |
| Malformed stored hash (data corruption) | `False` returned, logged as a data-integrity warning, never a raised exception that could crash the request |
| Hashing operation itself fails (e.g., out-of-memory under Argon2id's memory-hard cost) | 500, logged, alert if recurring (possible resource-tuning issue) |

## 19. Offline First
N/A (server-side); offline lock verification against a securely-cached salted hash is C.19's client-side design, already scoped there.

## 20. Local Data
N/A.

## 21. Localization
N/A.

## 22. RTL
N/A.

## 23. Analytics
No credential-hashing-specific event is listed in PRD §1.19; do not invent one. If lockout-related events already exist under C.19's own analytics scope, this utility should integrate with those rather than creating a parallel event.

## 24. Performance
Argon2id parameters must be tuned so a single hash/verify operation adds acceptable latency to the request path (PIN verification is a synchronous, user-facing action) while remaining computationally expensive enough to resist brute-force at scale — document the chosen parameters and the reasoning (a specific memory-cost/time-cost/parallelism tuple), not just "use Argon2id" with defaults left unexamined.

## 25. Security
- This is one of the six hard-requirement items in PRD §5's Backend AI Code-Generation Prompt.
- No fast general-purpose hash (plain SHA-256, MD5, etc.) may appear anywhere in the credential-storage code path — this must be true even in test fixtures/mocks used for anything beyond unit-testing the hasher itself, to avoid the scan test producing false negatives.
- Salt must be unique per credential (never a shared/static salt).

## 26. Library Requirements
Argon2id via the project's chosen Python Argon2 binding (e.g., `argon2-cffi`) per PRD §5's explicit stack line ("Argon2id/bcrypt for credential hashing"). Confirm which of Argon2id or bcrypt the codebase already depends on (check `pyproject.toml`/`requirements`) before adding a new dependency — reuse if already present, add `argon2-cffi` only if genuinely absent.

## 27. Testing
- **Unit:** `hash_credential` produces a different hash for the same input on repeated calls (unique salt); `verify_credential` correctly accepts/rejects.
- **Unit:** malformed stored-hash input returns `False`, does not raise.
- **Architectural (CI-blocking, mandatory):** `tests/architecture/test_no_fast_hash_in_credential_path.py` — dependency/import-scan confirming no `hashlib.sha256`/`hashlib.md5`/other fast-hash usage exists anywhere in the credential-storage code path (scope the scan to the relevant modules — parent-PIN and child-lock storage/verification files — rather than the entire repo, to avoid false positives from unrelated hashing use elsewhere, e.g., non-credential checksum use).
- **Performance:** measure and assert hash/verify latency stays within an agreed acceptable bound (document the bound).
- **Integration:** end-to-end PIN-set → PIN-verify flow through the actual API endpoint.

## 28. Documentation
Document the chosen Argon2id parameters and rationale in the utility module's docstring; document the credential-reset migration requirement if any existing fast-hash data is discovered (§14).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Audit Existing Credential-Storage Code Paths**
- Task ID: B-04-T01
- Objective: Locate every existing place a parent PIN or child lock pattern/PIN is hashed, stored, or verified.
- Why This Is Required: Cannot safely migrate to a shared utility without first knowing every call site; a missed site would leave a fast-hash gap the architectural test might not catch if scoped too narrowly.
- Existing Architecture to Follow: `identity` context and child-profile-related services.
- Existing Files to Reuse: none yet (audit only).
- Files to Create: none yet.
- Files to Modify: none yet.
- Implementation Details: search for PIN/pattern model fields, existing hash calls, any `hashlib` usage near auth/credential code.
- Business Rules: N/A.
- Validation / Error Handling / Security / Performance: N/A (audit only).
- Localization / RTL / Analytics: N/A.
- Tests: none yet.
- Documentation: audit findings feed Task 02/03.
- Dependencies: none.
- Do Not Change: nothing yet.
- Expected Result: complete list of call sites and current hashing mechanism used at each.
- Definition of Done: audit documented, no ambiguity about scope remains.

**Task 02 — Implement the Shared Argon2id Utility**
- Task ID: B-04-T02
- Objective: Build `hash_credential`/`verify_credential`.
- Why This Is Required: Core deliverable.
- Existing Architecture to Follow: `common/` or `core/security.py`-adjacent convention (reconcile with B-01's placement for consistency).
- Existing Files to Reuse: confirmed Argon2 library from Task 01's dependency check.
- Files to Create: `src/noorheroes/common/security/credential_hasher.py`.
- Files to Modify: none yet.
- Implementation Details: per §10, with tuned parameters per §24.
- Business Rules: unique salt per credential.
- Validation: as in §15.
- Error Handling: as in §18.
- Security: no fast-hash fallback path, no debug/test bypass left reachable in production code.
- Performance: measure per §24.
- Localization / RTL / Analytics: N/A.
- Tests: unit tests per §27.
- Documentation: docstring with parameter rationale.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: fully tested, reusable hashing utility.
- Definition of Done: unit + performance tests pass.

**Task 03 — Migrate All Call Sites**
- Task ID: B-04-T03
- Objective: Replace every call site found in Task 01 with the new shared utility.
- Why This Is Required: A shared utility only closes the security gap if it's actually used everywhere; a single missed call site defeats the entire guarantee.
- Existing Architecture to Follow: each call site's existing surrounding service/repository pattern.
- Existing Files to Reuse: Task 02's utility.
- Files to Create: none.
- Files to Modify: every file identified in Task 01.
- Implementation Details: swap old hashing calls for `hash_credential`/`verify_credential`; if existing stored hashes are in a fast-hash format, implement the credential-reset migration plan flagged in §14 rather than attempting an unsafe re-hash.
- Business Rules: no credential-storage code path may bypass the shared utility.
- Validation: as in §15.
- Error Handling: as in §18, integrated with existing lockout logic if present (confirm per §18, do not assume).
- Security: this task is itself the primary security fix.
- Performance: N/A beyond Task 02.
- Localization / RTL: N/A.
- Analytics: integrate with existing lockout/security events if present, per §23.
- Tests: integration tests per §27 for each migrated flow (parent-PIN set/verify, child-lock set/verify).
- Documentation: note the migration in each affected context's docs; document the credential-reset plan if data migration was required.
- Dependencies: Task 01, Task 02.
- Do Not Change: unrelated logic in the same files (lockout policy thresholds, PIN-length rules, etc. — those belong to C.19/C.21, not this blueprint).
- Expected Result: zero remaining fast-hash credential storage anywhere.
- Definition of Done: Task 04's architectural scan passes clean.

**Task 04 — Write the CI-Blocking No-Fast-Hash Architectural Test**
- Task ID: B-04-T04
- Objective: Implement `tests/architecture/test_no_fast_hash_in_credential_path.py`.
- Why This Is Required: PRD §5 explicitly requires this as a hard requirement, via "a dependency/import-scan test."
- Existing Architecture to Follow: same static-analysis approach as B-03's architectural test, for consistency.
- Existing Files to Reuse: none.
- Files to Create: `tests/architecture/test_no_fast_hash_in_credential_path.py`.
- Files to Modify: CI config to mark this test blocking.
- Implementation Details: scan the specific migrated files (Task 01's list) for `hashlib.sha256`/`md5`/other fast-hash imports/usage; fail with a clear message.
- Business Rules: zero tolerance.
- Validation: this test is the validator.
- Error Handling: clear failure message naming file/line.
- Security: non-bypassable without Security Engineering sign-off.
- Performance: fast enough for every CI run.
- Localization / RTL / Analytics: N/A.
- Tests: this task's deliverable is a test.
- Documentation: link from the utility's docstring.
- Dependencies: Task 03 (needs the migrated, clean codebase).
- Do Not Change: N/A.
- Expected Result: any future PR reintroducing a fast hash in the credential path fails CI.
- Definition of Done: test passes, wired as blocking CI gate.

## 30. Definition of Done
Shared Argon2id utility implemented and tested; every parent-PIN and child-lock-pattern/PIN call site migrated; any legacy fast-hash data handled via an explicit, documented credential-reset plan (not a silent re-hash); CI-blocking architectural test in place.

## 31. Final Verification Checklist
- [x] `hash_credential`/`verify_credential` implemented using Argon2id with documented, tuned parameters
- [x] Every existing PIN/pattern hashing call site migrated, none missed
- [x] Unique salt per credential confirmed
- [x] No fast general-purpose hash anywhere in the credential-storage path (architectural test passes)
- [x] Legacy fast-hash data (if found) handled via explicit credential-reset migration plan, not silent re-hash
- [x] Verification failure integrates correctly with existing lockout logic (confirmed, not assumed)
- [x] Performance within documented acceptable latency bound
- [x] No PostgreSQL/Redis credential changes introduced
