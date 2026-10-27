---
id: domain.admin-fact-editorial-workflow
kind: service
title: Admin Fact Editorial & Scholar Approval Workflow Domain Service Interface
status: stable
owner_story: TASK-B18-06
version: 1
created: 2026-10-12
---

## Overview

The `AdminFactService` manages editorial CRUD, scholar sign-off transitions, topic sensitivity flags, and the hard server-side disable for AI drafting on sensitive topics (Blueprint B-06).

## Domain Invariants

1. **Role Separation Matrix**:
   - `content_editor`: Create facts, draft new versions, edit drafts, list/filter, soft-withdraw.
   - `scholar_reviewer`: Approve (publishes version), reject (returns to draft), revoke (archives and immediately excludes).
   - `trust_safety` / `scholar_lead`: Toggle topic `is_jurisprudentially_sensitive` flag.
2. **Server-Side Disputed-Topic AI-Assist Hard Gate (FR-3 / §12.5)**:
   - When generating AI draft, checks `topic.is_jurisprudentially_sensitive`.
   - If true, raises `DisputedTopicAIBypassForbiddenError` (HTTP 403 `DISPUTED_TOPIC_AI_DRAFTING_FORBIDDEN`), completely blocking direct API bypasses.
3. **Edge Case 8 Review Notes Mandate**:
   - Scholar approval requires non-empty reviewer notes; rejects with HTTP 422 if empty/whitespace.
4. **Audit Logging**:
   - Every mutation records an immutable `AdminAuditRecord` (`high_sensitivity=True` on revocations and topic flag toggles).

## Public Interface

```python
class AdminFactService(BaseService):
    async def create_fact(self, admin_id: str, request: FactCreateRequest) -> Tuple[FactOrm, FactVersionOrm]:
        ...
    async def approve_version(self, admin_id: str, version_id: str, request: FactApproveRequest) -> Tuple[FactVersionOrm, ScholarApprovalOrm]:
        ...
    async def reject_version(self, admin_id: str, version_id: str, request: FactRejectRequest) -> FactVersionOrm:
        ...
    async def revoke_approval(self, admin_id: str, version_id: str, request: FactRevokeRequest) -> Tuple[FactVersionOrm, datetime]:
        ...
    async def update_disputed_flag(self, admin_id: str, topic_id_or_slug: str, is_sensitive: bool) -> TopicOrm:
        ...
    async def generate_ai_draft(self, admin_id: str, request: AIAssistDraftRequest) -> AIAssistDraftResponse:
        ...
```
