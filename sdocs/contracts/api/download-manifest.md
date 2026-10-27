---
id: api.download-manifest
kind: api
title: Download Manifest Issuance API (POST /v1/downloads/manifest)
status: stable
owner_story: TASK-B01
version: 1
created: 2026-09-29
---

## Endpoint

```http
POST /v1/downloads/manifest
```

## Auth & Security

- **Auth**: Bearer token, child-mode session (`Depends(get_current_child)`).
- **Scope**: Rejects parent-mode or unauthenticated tokens with HTTP `401 Unauthorized` / `403 Forbidden`.
- **Anti-Caching Headers**:
  - `Cache-Control: private, no-store, no-cache, must-revalidate`
  - `Pragma: no-cache`
- **Security**: Signed chunk URLs are short-TTL (e.g. 900s), minting secure access to CDN/R2 media assets.

---

## 1. Request Payload

```ts
export interface DownloadManifestRequest {
  content_id: string; // Valid UUID
  content_type: "story" | "surah" | "dua" | "quiz" | "audio";
  quality?: "standard" | "high"; // Optional, defaults to "standard"
}
```

*Note: Dual-wire compatibility supports both camelCase (`contentId`, `contentType`) and snake_case.*

---

## 2. Response — 200 OK

```ts
export interface ManifestChunk {
  chunk_id: string;
  url: string;       // Signed, short-TTL CDN URL
  checksum: string;  // Format: "sha256:<hex>"
}

export interface DownloadManifestResponse {
  manifest_id: string;
  chunks: ManifestChunk[];
  expires_at: string;        // ISO 8601 timestamp
  license_expires_at: string; // ISO 8601 timestamp
}
```

---

## 3. Error Responses

| Code | HTTP Status | Description | Details Envelope |
|---|---|---|---|
| `UNAUTHENTICATED` | 401 | Missing, malformed, or invalid child token | `{ "code": "UNAUTHENTICATED", "message": "..." }` |
| `FORBIDDEN` | 403 | Parent-mode session token used | `{ "code": "FORBIDDEN", "message": "..." }` |
| `DOWNLOAD_CAP_REACHED` | 403 | Child storage cap exceeded | `{ "code": "DOWNLOAD_CAP_REACHED", "usage_bytes": 1073741824, "limit_bytes": 1073741824 }` |
| `DOWNLOADS_DISABLED_BY_PARENT` | 403 | Parental controls disabled offline downloads | `{ "code": "DOWNLOADS_DISABLED_BY_PARENT" }` |
| `ENTITLEMENT_REQUIRED` | 403 | Content requires active family subscription tier | `{ "code": "ENTITLEMENT_REQUIRED" }` |
| `CONTENT_WITHDRAWN` | 403 | Content has been unpublished / withdrawn by publisher | `{ "code": "CONTENT_WITHDRAWN" }` |
| `VALIDATION_ERROR` | 422 | Invalid UUID, unallowed quality, or missing fields | `{ "code": "VALIDATION_ERROR", "details": [...] }` |

---

## 4. Core Invariants & Guarantees

1. **Gate Evaluation Order (Blueprint B-01 §10, B-03 §10)**:
   - Parental lockout gate (`DOWNLOADS_DISABLED_BY_PARENT`) evaluated first.
   - Subscription entitlement gate (`ENTITLEMENT_REQUIRED`) evaluated second.
   - Storage cap gate (`DOWNLOAD_CAP_REACHED`) evaluated third.
2. **Zero-Row-On-Rejection Invariant (Blueprint B-01 §10)**:
   - Any rejection (cap exceeded, entitlement missing, downloads disabled) short-circuits immediately with **zero rows written** to `download_record`.
3. **Idempotent Manifest Re-issuance & Dedup (Blueprint B-01 §5 / §10, PRD Edge Case 3)**:
   - Re-requesting a manifest for already `complete` content resolves the existing `download_record` row, issuing fresh signed chunk URLs without creating a duplicate row or violating `UNIQUE(child_id, content_id)`.
4. **Resumable Downloads (Blueprint B-01 §10, PRD Edge Case 5)**:
   - If an existing record is in `in_progress` or `failed` state, the endpoint reuses `download_id` and reissues signed chunk URLs so the client can resume chunk transfer seamlessly.
5. **Outbox Metrics Emission (Blueprint B-01 §10 / B-07 §6)**:
   - Emits `DownloadManifestIssued` outbox event capturing success/rejection status, reason, content ID, and child ID.
