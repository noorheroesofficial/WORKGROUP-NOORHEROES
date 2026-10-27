# B-01 — Consent Log & Withdrawal API

## 1. Feature Context
Part of Feature C.26 — Privacy, Consent, Account Security & Data Rights (Settings). Gives parents a reviewable, individually-withdrawable list of every consent they gave at onboarding, without introducing a second consent-storage mechanism alongside A.1's.

## 2. Parent Feature
C.26 Privacy, Consent, Account Security & Data Rights (Settings)

## 3. Sub-feature
**B-01 — Consent Log & Withdrawal API** (`GET /v1/parent/consents`, `POST /v1/parent/consents/{id}/withdraw`)

## 4. Objective
Expose the family's consent state as a browsable, individually-withdrawable list, and implement withdrawal so that every optional-consent change is written through A.1's existing append-only `ConsentLedgerService` — never a new, parallel consent-storage path.

## 5. Business Requirements
- FR-1/FR-2: Consent log with review/withdraw actions.
- FR-3: Step-up authentication required before withdrawal.
- FR-8: Required consents (terms, privacy, child_data) cannot be withdrawn — attempting to do so routes to the account-deletion path.
- FR-9: Withdrawing `voice_ai` consent here has the identical effect as toggling AI off via C.23's AI Permissions screen — same underlying value, never two independently-tracked ones.
- Edge Case 1: re-granting a withdrawn optional consent creates a new ledger entry, never an "undelete."
- Acceptance Criteria (§1.9): every onboarding consent individually listed with current status; required-consent withdrawal attempts are redirected, not toggled.

## 6. Existing Architecture — Resolved (read before implementing)
**This sub-feature's PRD (§3.4/§4.1/§4.2) describes `consent_record` as one row per consent *type* (`consent_id, family_id, type, required, status, changed_at`) with per-type withdrawal by `id`. This does not match the actual, already-implemented schema.**

A.1 B-05 ("Consent Ledger & Privacy Preference API") already built `consent_record` as a **wide, append-only snapshot table** — one row per *change event* for the whole family, with named boolean/version columns (`terms_version`, `privacy_version`, `child_data_version`, `personalization_consent`, `voice_consent`, `marketing_consent`, `region`, `source_platform`, `recorded_at`) — not one row per consent type. The table has **no UPDATE/DELETE grant at the Postgres role level** (A.1 B-05 §12/Task 01) and the repository (`ConsentRepository`) exposes only `add_record()` / `get_latest_for_family()` — no per-row-by-id lookup exists, because there is no per-type row.

A.1 B-05 also already implemented `POST /v1/identity/family/consent`, accepting `{personalization, voice, marketing}` and internally calling `ConsentLedgerService.update_optional_consent()`, which appends a new snapshot row carrying forward unchanged fields — required-consent fields are schema-excluded from that endpoint entirely (cannot even be sent).

**Resolution — build B-01 as a read/write veneer over A.1's existing service, not a new consent-storage mechanism:**
1. `GET /v1/parent/consents` **synthesizes** a 6-item list (3 required, 3 optional) from `ConsentRepository.get_latest_for_family()`'s single latest snapshot row — each synthesized item's `id` is a stable, code-defined string (`"terms"`, `"privacy"`, `"child_data"`, `"personalization"`, `"voice_ai"`, `"marketing"`), not a database primary key. `status` derives from the relevant boolean/version field being present/true vs. withdrawn; `last_changed_at` is the snapshot row's `recorded_at` (the whole snapshot changes together, since it's append-only-per-change, not per-field — document this granularity limitation explicitly in the API description).
2. `POST /v1/parent/consents/{id}/withdraw` maps `id` → the corresponding A.1 field. For the three optional ids, it loads the latest snapshot, flips only the targeted field to withdrawn, and calls **A.1's existing `ConsentLedgerService.update_optional_consent()`** with the other two optional fields carried forward unchanged — this is a thin wrapper, not new persistence logic. For the three required ids, it immediately rejects (`422`) without calling any ledger method at all.
3. **Do not** create a new `consent_record`-shaped table, a new repository, or a new DB migration for this sub-feature — B-01 adds zero new tables.

## 7. Existing Code to Reuse
- `modules/identity/consent_service.py::ConsentLedgerService.update_optional_consent()` (A.1 B-05, Task 04) — the sole write path for optional-consent changes.
- `modules/identity/consent_repository.py::ConsentRepository.get_latest_for_family()` (A.1 B-05, Task 02) — sole read path.
- `modules/identity/consent_models.py::ConsentRecordOrm` — read-only from this sub-feature's perspective.
- `core/deps.py::get_current_parent`, `require_elevated_session`.
- `common/outbox.py::OutboxWriter`.

## 8. Files to Create
- `src/noorheroes/modules/identity/consent_log_schemas.py` — `ConsentLogEntry`, `ConsentLogResponse`, `ConsentWithdrawRequest` (empty body — `id` is a path param), `ConsentWithdrawResponse`
- `src/noorheroes/modules/identity/consent_log_service.py` — `ConsentLogService(BaseService)`: `list_consents(parent_ctx)`, `withdraw(parent_ctx, consent_id)` — a thin orchestration layer distinct from `ConsentLedgerService`, calling it rather than duplicating it
- `tests/modules/identity/test_consent_log_service.py`
- `tests/modules/identity/test_consent_log_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/identity/api.py` — add `GET /v1/parent/consents`, `POST /v1/parent/consents/{id}/withdraw`

## 10. Backend Requirements
- `ConsentLogService.list_consents()`: load latest snapshot via `ConsentRepository.get_latest_for_family()`; map to 6 `ConsentLogEntry` items with a code-defined `CONSENT_TYPE_REGISTRY` constant (id, required flag, display-name key) — cross-reference B-05's admin Consent Type Registry as the eventual source of this mapping once that admin surface exists; until then, this constant is the interim source of truth and must be kept in sync manually (flag in code comments).
- `ConsentLogService.withdraw(consent_id)`:
  1. If `consent_id` is one of `terms|privacy|child_data` → raise `RequiredConsentCannotWithdrawError` immediately, no DB call.
  2. Else, load latest snapshot, build an `update_optional_consent()` payload carrying forward the other two optional fields unchanged and setting the target field to withdrawn, call `ConsentLedgerService.update_optional_consent()`.
  3. If `consent_id == "voice_ai"`, additionally call the same shared write C.23 B-04 uses (`ChildProfile.voice_interaction_enabled` via its settings service) for every child in the family — **see §25 Security for the unresolved per-family-vs-per-child scope conflict this raises; flagged, not silently resolved.**
- Enforce step-up (`require_elevated_session`) on withdrawal only; the list endpoint requires only a standard parent session.

## 11. API Contract

### `GET /v1/parent/consents`
- **Auth:** Bearer (parent)
- **Response 200:** `{ "consents": [ { "id": "personalization", "type": "personalization", "status": "granted", "required": false, "last_changed_at": "..." }, ... ] }`

### `POST /v1/parent/consents/{id}/withdraw`
- **Auth:** Bearer + step-up
- **Response 200:** `{ "updated": true, "consent_id": "marketing", "effective_at": "..." }`
- **Error Responses:** `422 REQUIRED_CONSENT_CANNOT_WITHDRAW` (with `redirect_to: "account_deletion"`) for `terms|privacy|child_data`; `404 UNKNOWN_CONSENT_ID` for any id outside the 6-item registry.

## 12. Database Requirements
None new. Reads/writes exclusively through A.1's existing `consent_record` table via its existing repository/service.

## 13. Validation
`{id}` path parameter must be one of the 6 registry values; anything else → `404 UNKNOWN_CONSENT_ID` (not `422`, since it's not a malformed request, it's a nonexistent resource).

## 14. Authentication
`Depends(get_current_parent)`; withdrawal additionally requires `Depends(require_elevated_session)`.

## 15. Authorization
Self-family-only; `family_id` derived from the bearer token, never accepted as a parameter.

## 16. Error Handling
| Scenario | Response |
|---|---|
| Withdraw a required consent id | `422 REQUIRED_CONSENT_CANNOT_WITHDRAW`, `redirect_to: "account_deletion"` |
| Unknown consent id | `404 UNKNOWN_CONSENT_ID` |
| Missing step-up on withdraw | `403 FORBIDDEN` |
| `ConsentLedgerService` write failure | `500`, no partial state (single transaction, inherited from A.1's service) |
| No consent snapshot exists yet for family (should be impossible post-registration) | `500` with alerting — indicates a data-integrity bug in B-02/A.1's registration flow, not a valid user-facing state |

## 17. Offline First
N/A — mutating action requires connectivity; list is safe to cache client-side (K-02).

## 18. Local Data
N/A (backend).

## 19. Localization
Consent display names/full text resolved via the existing legal-content versioning system (A.1) — this endpoint returns type ids and status only, not display text; client resolves display copy locally per locale.

## 20. RTL
N/A (backend).

## 21. Analytics
Backing source for `consent_withdrawn` (with `consent_type`), `consent_regranted`, `required_consent_withdrawal_attempt_redirected` — emitted client-side (K-02) based on this endpoint's responses.

## 22. Performance
Single indexed row read (`(family_id, recorded_at DESC)`, already indexed by A.1); withdrawal is a single new-row append, low volume.

## 23. Security
- No new mutation surface on `consent_record` — B-01 never bypasses A.1's append-only/DB-role-enforced guarantee, since it calls A.1's service exclusively.
- **Unresolved scope conflict (flag for product/architecture sign-off, do not silently resolve):** FR-9 states `voice_ai` withdrawal here and C.23's AI Permissions toggle are "the same underlying settings field." But A.1's `consent_record.voice_consent` is **family-scoped** (one flag for the whole family), while C.23 B-04's `ChildProfile.voice_interaction_enabled` is **per-child**. These are not structurally the same field. §10's proposed mitigation (writing to `voice_interaction_enabled` on every child in the family whenever the family-level consent is withdrawn) is a reasonable interim reconciliation but is **not** the single-shared-value guarantee the PRD requires — a child whose parent later re-enables AI individually via C.23 would silently diverge from the family-level consent state. This must be resolved at a product/schema level (e.g., either make `voice_consent` the single source of truth and remove the per-child override, or vice versa) before this task is considered fully done; implement the interim mitigation but do not mark the FR-9 guarantee itself as met without that resolution.

## 24. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2 — no new libraries.

## 25. Testing
- Unit: `list_consents()` correctly synthesizes 6 entries from a single snapshot row.
- Unit: withdrawal of each of the 3 required ids rejected with `422` and `redirect_to` hint, and confirms zero calls made to `ConsentLedgerService`.
- Integration: withdrawal of an optional id calls `update_optional_consent()` with the other two fields unchanged (verify via a spy/mock on the A.1 service).
- Integration: re-grant after withdrawal appends a new row, prior row untouched (reuses A.1's own immutability test pattern).
- Integration: `voice_ai` withdrawal's per-child propagation to `ChildProfile.voice_interaction_enabled` — test documents the flagged scope conflict from §23 rather than silently asserting a false "always in sync" guarantee.
- Unit: unknown consent id returns `404`, not `422`.

## 26. Documentation
OpenAPI description must state plainly that this endpoint is a read/write veneer over A.1's `consent_record` table, not an independent consent store, and must explicitly flag the family-vs-per-child `voice_ai` scope question from §23 as an open item.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Define the Consent Type Registry Constant**
- **Objective:** A single code-defined mapping of the 6 consent ids to required-flag and A.1 field name.
- **Files to Create:** constant inside `consent_log_service.py` (or a small `consent_registry.py` if preferred).
- **Definition of Done:** Registry has exactly 6 entries, matching A.1's actual `consent_record` columns.

**Task 02 — Implement `ConsentLogService.list_consents()`**
- **Files to Create:** `consent_log_service.py`.
- **Dependencies:** Task 01, A.1's `ConsentRepository.get_latest_for_family()`.
- **Definition of Done:** Returns exactly 6 synthesized entries from the latest snapshot.

**Task 03 — Implement `ConsentLogService.withdraw()` for Optional Consents**
- **Implementation Details:** Load latest snapshot, carry forward unaffected optional fields, call `ConsentLedgerService.update_optional_consent()`.
- **Definition of Done:** New snapshot row appended, prior row untouched, only the targeted field changed.

**Task 04 — Implement Required-Consent Rejection Path**
- **Implementation Details:** Immediate `422` with `redirect_to`, zero DB calls.
- **Tests:** All 3 required ids covered individually.
- **Definition of Done:** No code path allows a required id to reach `ConsentLedgerService`.

**Task 05 — Implement Interim `voice_ai` Per-Child Propagation, Document the Flag**
- **Objective:** Best-effort reconciliation per §23, explicitly documented as interim.
- **Definition of Done:** Propagation works for all current children at time of withdrawal; the unresolved-divergence risk is documented in code comments and OpenAPI, not hidden.

**Task 06 — Router Wiring**
- **Files to Modify:** `api.py`.
- **Definition of Done:** Both endpoints live, step-up enforced only on withdrawal.

**Task 07 — Full Test Suite & Documentation**
- **Definition of Done:** All tests in §25 green; OpenAPI updated per §26.

## 28. Definition of Done
Consent Log list and withdrawal are fully functional as a veneer over A.1's existing append-only ledger, required-consent withdrawal is provably blocked, and the FR-9 family-vs-per-child `voice_ai` scope conflict is implemented with a documented interim mitigation and flagged for architecture sign-off rather than silently papered over.

## 29. Final Verification Checklist
- [ ] No new `consent_record`-shaped table or migration created
- [ ] `list_consents()` synthesizes exactly 6 entries from A.1's existing snapshot
- [ ] All 3 required-consent withdrawal attempts rejected with `422` + `redirect_to`, zero DB calls
- [ ] Optional withdrawal calls A.1's `update_optional_consent()`, never a new write path
- [ ] `voice_ai` family-vs-per-child scope conflict documented and flagged, not silently assumed resolved
- [ ] Step-up enforced on withdrawal, not on list
- [ ] No PostgreSQL/Redis credential changes
