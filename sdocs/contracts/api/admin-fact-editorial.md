---
id: api.admin-fact-editorial
kind: api
title: Admin Fact Editorial & Scholar-Approval Workflow API
status: stable
owner_story: TASK-B18-06
version: 1
created: 2026-10-12
---

## Endpoints

```http
POST   /v1/admin/facts                                (Role: content_editor)
PUT    /v1/admin/facts/{id}/versions                  (Role: content_editor)
GET    /v1/admin/facts                                (Role: content_editor)
GET    /v1/admin/facts/{id}                           (Role: content_editor)
DELETE /v1/admin/facts/{id}                           (Role: content_editor)
POST   /v1/admin/facts/versions/{id}/approve          (Role: scholar_reviewer)
POST   /v1/admin/facts/versions/{id}/reject           (Role: scholar_reviewer)
POST   /v1/admin/facts/versions/{id}/revoke           (Role: scholar_reviewer)
PATCH  /v1/admin/topics/{id}/disputed-flag            (Role: trust_safety, scholar_lead)
GET    /v1/admin/topics                               (Role: content_editor, scholar_reviewer, ...)
POST   /v1/admin/facts/ai-draft                       (Role: content_editor)
POST   /v1/admin/facts/ai-assist                      (Role: content_editor)
```

## Auth & Security

- **RBAC Enforcement**: Fine-grained role gating via `require_admin_role()`.
- **Version Immutability (FR-11)**: Content edits create a new draft version; published versions are never mutated in place.
- **Edge Case 8 Review Notes Mandate**: Approvals without genuine reviewer notes are rejected with `422 Unprocessable Entity`.
- **FR-3 Server-Side Hard Gate**: AI drafting assist strictly rejects calls on sensitive topics with `403 Forbidden` (`DISPUTED_TOPIC_AI_DRAFTING_FORBIDDEN`), regardless of client UI state.
- **Audit Logging**: All mutations write to immutable audit log (`high_sensitivity=true` on revocations and topic flag toggles).

---

## 1. Selected Schemas

```ts
export interface FactCreateRequest {
  topic: string;
  locale: string;
  ageBand: string;
  text: string;
  explanation: string;
  sources: SourceReference[];
  jurisprudentialScopeNote?: string | null;
  linkedQuizQuestionId?: string | null;
  relatedContentId?: string | null;
  relatedContentType?: string | null;
}

export interface FactApproveRequest {
  reviewerNotes: string;      // Strictly required (non-empty)
}

export interface FactRevokeRequest {
  reason: string;             // Strictly required (non-empty)
}

export interface DisputedFlagUpdateRequest {
  isJurisprudentiallySensitive: boolean;
}

export interface AIAssistDraftRequest {
  topic: string;
  prompt: string;
  locale?: string;
  ageBand?: string;
}
```

---

## 2. Key Error Codes

- `401 UNAUTHORIZED`: Missing/invalid admin session Bearer token.
- `403 FORBIDDEN`: Insufficient administrative role or server-side disputed topic bypass rejection (`DISPUTED_TOPIC_AI_DRAFTING_FORBIDDEN`).
- `404 NOT_FOUND`: Fact, version, or topic entity does not exist.
- `422 UNPROCESSABLE_ENTITY`: Schema validation error, missing approval review notes, or missing revocation reason.
