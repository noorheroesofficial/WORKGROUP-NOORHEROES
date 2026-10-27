---
id: api.fact-detail-retrieval
kind: api
title: Islamic Fact Detail Retrieval API (GET /v1/facts/{id})
status: stable
owner_story: TASK-B18-03
version: 1
created: 2026-10-11
---

## Endpoint

```http
GET /v1/facts/{id}
GET /v1/content/facts/{id}
```

## Auth & Security

- **Auth**: Bearer token via authenticated child session (`ChildSessionContext` / `get_current_child`).
- **Dynamic Content Availability**: Live evaluation of referenced `related_content` (Story, Dua, Surah). If withdrawn or deleted, sets `related_content.available = false` preventing broken mobile navigation.
- **Canonical Restructuring Traversal**: Seamlessly resolves series/episode restructuring via canonical ID references.

---

## 1. Request Parameters

### Path Parameters

- `id` (string, required): Canonical UUIDv7 identifier of target Islamic fact entity.

### Headers

- `X-Locale` / `Accept-Language` (string, optional): Target language override (`en`, `ar`, `ur`, `hi`).

---

## 2. Response Contract — 200 OK

```ts
export interface SourceReference {
  type: string;             // "primary" | "secondary" | "hadith" | "quran"
  citation: string;         // Canonical citation reference string
  arabicText?: string | null;
  englishTranslation?: string | null;
}

export interface ScholarApprovalDetail {
  approverId: string;       // Unique identifier of authorized scholar reviewer
  version: string;          // Version code approved (e.g. "v1")
  approvedAt: string;       // ISO 8601 UTC timestamp of sign-off
}

export interface RelatedContentLink {
  contentId: string;        // UUID of referenced story, episode, surah, or dua
  contentType: string;      // "story" | "dua" | "surah" | "series"
  available: boolean;       // Live eligibility: false if item is withdrawn or deleted
  title?: string | null;    // Display title of referenced content
}

export interface FactDetailResponse {
  factId: string;                               // Canonical fact identifier
  text: string;                                 // Localized statement of the fact
  explanation: string;                          // Detailed background contextual narrative
  topic: string;                                // Registered thematic topic
  sources: SourceReference[];                   // Structured primary & secondary citations
  scholarApproval: ScholarApprovalDetail;       // Active scholar sign-off verification details
  jurisprudentialScopeNote?: string | null;     // Optional scholar scope/jurisprudence notes
  relatedContent?: RelatedContentLink | null;   // Dynamically validated related content link
  linkedQuizId?: string | null;                 // Optional UUID of linked 1-question quiz
}
```

*Note: Dual-wire serialization supports both camelCase and snake_case.*

---

## 3. Error Responses

- `401 UNAUTHORIZED`: Missing, invalid, or expired child session token.
- `404 FACT_NOT_FOUND`: Fact does not exist or no published scholar-approved version exists for requesting cohort.
- `410 FACT_WITHDRAWN`: Fact entity itself has been soft-withdrawn/archived (`is_withdrawn = true`).
- `422 VALIDATION_ERROR`: Path parameter `id` is not a valid UUID string.
