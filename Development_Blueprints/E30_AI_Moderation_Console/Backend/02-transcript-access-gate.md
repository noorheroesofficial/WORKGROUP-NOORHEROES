# B-02 — Transcript Access Gate

## 1. Feature Context
Parent PRD: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
Depends on: B-01 (queue item + `ai_safety_event` join), E.28 (Admin Auth/RBAC, shared audit log)
Feeds into: N-02 (Full Transcript View screen)

## 2. Parent Feature
E.30 — AI Moderation Console & Safety Evaluation Harness

## 3. Sub-feature
**Transcript Access Gate** (ID: B-02) — the elevated-permission, fully-audited path to raw (unredacted) prompt/output content. This is this entire feature's single highest-priority guarantee (§12.3): "the single most important guarantee in this entire service."

## 4. Objective
Provide the platform's **sole sanctioned exception** to write-time redaction (§12.6) — but only behind an elevated permission distinct from general queue access, with every access attempt, granted or rejected, permanently and immediately logged.

## 5. Business Requirements
- FR-5: Access to transcripts is role-limited and fully audited — a hard rule; not every admin role with general AI-moderation visibility automatically gets transcript-level access.
- §3.4: `403 INSUFFICIENT_TRANSCRIPT_PRIVILEGE` for insufficient privilege, **and this rejection itself is logged** — every call, successful or not, writes an audit entry.
- Edge Case 6 (§1.10): a transcript-access request by an admin with general queue visibility but not the elevated permission → rejected at the service layer, with the rejection itself logged.
- §4.2: `transcript_access_log` is append-only — every access attempt, granted or rejected, is permanently recorded.

## 6. Existing Architecture
Extends the `ai_moderation` context created in B-01. Reuses `AdminSessionContext`/`require_admin_scope` from `core/deps.py` for the elevated check, and writes to E.28's shared audit log **in addition to** this module's own append-only table (§4.3 — intentional redundancy given severity class).

## 7. Existing Code to Reuse
- `require_admin_scope()` factory (`core/deps.py`) — used here with a **new, distinct** scope string, not reused from B-01's general read scope
- `AuthorizationError` subclassing pattern from `core/exceptions.py::SegregationOfDutiesViolationError` — the direct precedent for a new `InsufficientTranscriptPrivilegeError`
- `BaseRepository`, `common/base_service.py`
- `AiModerationRepository`/`AiModerationQueueService` from B-01 (queue item lookup)
- `noorheroes/modules/ai_safety/models.py::AiSafetyEvent` — this is the **only** module in the codebase permitted to select its raw-content-adjacent fields beyond the redacted ones (note: the current `AiSafetyEvent` schema per `ai_safety/models.py` stores only bounded/redacted `input_redacted`/`output_redacted` — if a true raw-content store exists elsewhere in the AI pipeline (F.35), this service must be pointed at that actual raw store; do not invent a raw-content column on `AiSafetyEvent` itself, since its own docstring states no column here is shaped to hold raw transcripts. Flag this as an open integration point with F.35 to confirm before implementation — do not guess the raw store's location.)

## 8. Files to Create
- `src/noorheroes/modules/ai_moderation/transcript_access_models.py` → `TranscriptAccessLog` ORM model
- `src/noorheroes/modules/ai_moderation/transcript_access_schemas.py` → `TranscriptAccessResponse`
- `src/noorheroes/modules/ai_moderation/transcript_access_service.py` → `TranscriptAccessGateService(BaseService)`
- `alembic/versions/xxxx_add_transcript_access_log.py`
- `tests/modules/ai_moderation/test_transcript_access_gate.py`

## 9. Files to Modify
- `src/noorheroes/modules/ai_moderation/api.py` → add `POST /{id}/transcript-access-request`
- `src/noorheroes/core/exceptions.py` → add `InsufficientTranscriptPrivilegeError(AuthorizationError)`

## 10. Backend Requirements

### 10.1 Model
```python
class TranscriptAccessLog(Base):
    __tablename__ = "transcript_access_log"
    __table_args__ = (Index("ix_transcript_access_requester_time", "requested_by", "requested_at"),)
    # append-only: no update/delete path is ever exposed on this model

    log_id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_ulid)
    queue_item_id: Mapped[str] = mapped_column(String, ForeignKey("ai_moderation_queue_item.queue_item_id"))
    requested_by: Mapped[str] = mapped_column(String, ForeignKey("admin_account.admin_id"))
    granted: Mapped[bool] = mapped_column(Boolean, nullable=False)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
```

### 10.2 Endpoint
| Method | Path | Auth | Purpose |
|---|---|---|---|
| POST | `/v1/admin/ai-moderation/{id}/transcript-access-request` | Elevated `ai-moderation:transcript-access` scope | Returns raw transcript if authorized |

### 10.3 Service Logic — Audit-Before-Response (the critical path)
```python
class TranscriptAccessGateService(BaseService):
    def __init__(self, log_repo: TranscriptAccessLogRepository, queue_repo: AiModerationRepository):
        self.log_repo = log_repo
        self.queue_repo = queue_repo

    async def request_access(self, queue_item_id: str, admin_ctx: AdminSessionContext) -> dict:
        has_elevated_scope = "ai-moderation:transcript-access" in admin_ctx.scopes or "super_admin" in admin_ctx.scopes
        # --- AUDIT WRITE HAPPENS REGARDLESS OF OUTCOME, BEFORE RAISING/RETURNING ---
        await self.log_repo.add(TranscriptAccessLog(
            queue_item_id=queue_item_id,
            requested_by=admin_ctx.admin_id,
            granted=has_elevated_scope,
        ))
        if not has_elevated_scope:
            raise InsufficientTranscriptPrivilegeError(
                "This action requires the elevated transcript-access permission.",
                queue_item_id=queue_item_id,
            )
        raw = await self.queue_repo.get_raw_transcript_for_item(queue_item_id)  # F.35 raw-store integration point
        if raw is None:
            raise NotFoundError(f"AI moderation queue item {queue_item_id} not found")
        return {"raw_prompt": raw["raw_prompt"], "raw_output": raw["raw_output"]}
```
> The `TranscriptAccessLog` insert must occur **before** the `InsufficientTranscriptPrivilegeError` is raised — never in an `except`/finally afterthought — so a mid-request crash after the check but before logging cannot produce an unaudited rejection. Within the same DB transaction as the request itself (`get_db_session`'s commit/rollback boundary), the audit row and the outcome are atomic.

### 10.4 New Exception
```python
class InsufficientTranscriptPrivilegeError(AuthorizationError):
    """Raised when an admin has general ai-moderation:read access but lacks
    the elevated ai-moderation:transcript-access scope. See B-02."""
    error_code = "INSUFFICIENT_TRANSCRIPT_PRIVILEGE"
```

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
Consumed by N-02's Transcript-Access Elevated Permission Gate modal and Full Transcript View.

## 13. API Contract

### `POST /v1/admin/ai-moderation/{id}/transcript-access-request`
- **Auth:** Elevated `ai-moderation:transcript-access` scope, distinct from general `ai-moderation:read`
- **Response 200:** `{ "raw_prompt": "...", "raw_output": "..." }`
- **Response 403:** `{ "error_code": "INSUFFICIENT_TRANSCRIPT_PRIVILEGE", "message": "..." }` — **and a `TranscriptAccessLog` row with `granted=false` is written regardless**
- **Response 404:** unknown `{id}`

## 14. Database Requirements
- `transcript_access_log`: FK `queue_item_id`, `requested_by`; append-only (no `UPDATE`/`DELETE` code path exposed anywhere in this module); index `(requested_by, requested_at DESC)` per §4.2.
- This table's completeness is a compliance-grade guarantee (§12.8) — retained at the platform's highest safety-audit durability tier (§10 DevOps).

## 15. Validation
- `queue_item_id` must reference an existing `ai_moderation_queue_item`.

## 16. Authentication
`Depends(get_current_admin)`.

## 17. Authorization
`require_admin_scope("ai-moderation:transcript-access")` — **not** the same scope as B-01's `ai-moderation:read`. An admin can have one without the other; `super_admin` implicitly satisfies both per the existing `require_admin_scope` bypass convention.

## 18. Error Handling
| Scenario | Response | Audit Behavior |
|---|---|---|
| Elevated scope present | `200` with raw content | `granted=true` logged |
| Elevated scope absent | `403 INSUFFICIENT_TRANSCRIPT_PRIVILEGE` | `granted=false` logged — **not silently dropped** |
| Unknown `{id}` | `404 NOT_FOUND` | No log row (item doesn't exist to reference) — confirm this against the FK constraint; if the FK requires a valid `queue_item_id`, the not-found check must precede the log write |
| Two moderators request access to the same item | Both succeed/log independently | Each gets its own log row |

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
Response is raw operator-facing content; no localization applied server-side.

## 22. RTL
Not applicable to backend.

## 23. Analytics
`ai_moderation_transcript_access_requested`, `ai_moderation_transcript_access_granted`, `ai_moderation_transcript_access_rejected` (§1.19 — the rejection event is explicitly called out as an "internal/security signal").

## 24. Performance
Single-row insert + single-row read; no pagination or heavy joins involved. Latency is not the concern here — correctness of the audit-before-response ordering is.

## 25. Security
- **This is the module's defining risk** (§12.1): unauthorized raw-transcript access. Mitigated entirely by this sub-feature's elevated-scope-plus-mandatory-audit design.
- A spike in `ai_moderation_transcript_access_rejected` events is a potential probing/insider-risk signal and should alert (§10 DevOps).
- The raw-content read path (`get_raw_transcript_for_item`) must not be callable from anywhere else in the codebase outside this service — confirm no other module imports it.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Alembic, Pydantic v2, pytest-asyncio.

## 27. Testing
- **Signature test 1 (CI-blocking, backend AI code-gen prompt item 2a):** a `child_safety_reviewer` **without** the elevated scope is rejected with `403 INSUFFICIENT_TRANSCRIPT_PRIVILEGE`.
- **Signature test 2 (CI-blocking, item 2b):** that same rejection **creates a `TranscriptAccessLog` row with `granted=false`** — the rejection is audited, not silently dropped. This is treated as one of the two highest-priority guarantees in the entire E.30 service (alongside B-04's kill-switch tests).
- Unit: successful grant path returns raw content and logs `granted=true`.
- Unit: two concurrent requests from different admins both succeed/log independently.
- Integration test against E.28's shared audit log confirming the dual-write (§4.3).

## 28. Documentation
Export OpenAPI; explicitly document that this is the platform's sole sanctioned exception to write-time redaction and that every call is audited regardless of outcome — this is the feature's core trust claim.

## 29. AI Coding Agent Implementation Steps
- **Task 01 — Model & Migration**: `TranscriptAccessLog`, append-only, indexed per §14.
- **Task 02 — New exception**: `InsufficientTranscriptPrivilegeError` in `core/exceptions.py`.
- **Task 03 — Confirm F.35 raw-store integration point**: identify (not guess) where raw prompt/output actually lives upstream before wiring `get_raw_transcript_for_item()`.
- **Task 04 — Service**: `TranscriptAccessGateService.request_access()` with audit-before-raise ordering per §10.3.
- **Task 05 — Router**: `POST` endpoint with elevated-scope enforcement.
- **Task 06 — Signature tests**: both CI-blocking tests from §27.
- **Task 07 — Dual-audit integration test** against E.28's shared log.
- **Task 08 — Documentation**: OpenAPI export with the sanctioned-exception claim documented.
- **Task 09 — Final Code Review**: confirm the audit-log insert cannot be skipped on any code path (including exception-raising paths), and that no other module can read raw transcript content.

## 30. Definition of Done
Elevated-scope enforcement and audit-on-every-call (both success and rejection) verified by independent CI-blocking tests; raw-content read path proven unreachable from any other module.

## 31. Final Verification Checklist
- [ ] `transcript_access_log` table created, append-only, correctly indexed
- [ ] `InsufficientTranscriptPrivilegeError` added and mapped to `403 INSUFFICIENT_TRANSCRIPT_PRIVILEGE`
- [ ] Rejected access attempts are logged (`granted=false`) — tested
- [ ] Granted access attempts are logged (`granted=true`) — tested
- [ ] F.35 raw-store integration point confirmed, not guessed
- [ ] Dual-write to E.28's shared audit log verified
- [ ] `ai_moderation_transcript_access_rejected` wired as a monitored security signal
- [ ] Tests green in CI, both signature tests non-bypassable
