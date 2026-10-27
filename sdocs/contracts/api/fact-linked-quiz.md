---
id: api.fact-linked-quiz
kind: api
title: Fact-Linked Quiz Delegation API (GET /v1/quizzes/fact/{fact_id})
status: stable
owner_story: TASK-B18-04
version: 1
created: 2026-10-12
---

## Endpoint

```http
GET /v1/quizzes/fact/{fact_id}
GET /v1/content/quizzes/fact/{fact_id}
GET /v1/facts/{fact_id}/quiz
```

## Auth & Security

- **Auth**: Bearer token via authenticated child session (`ChildSessionContext` / `get_current_child`).
- **Security Invariant (Blueprint B-04 §17)**: Sibling tenancy boundary enforced; if `?child_id` query parameter is provided, it must match session child token (`403 FORBIDDEN` on mismatch).
- **FR-7 Zero Parallel Engine Invariant (Blueprint B-04 §1, §6)**: Reuses Feature A.8's Quiz Engine contracts and entities directly. Zero local scoring, retry, or evaluation logic introduced.

---

## 1. Request Parameters

### Path Parameters
- `fact_id` (string, required): Canonical UUIDv7 identifier of the target Islamic fact entity.

### Query Parameters
- `child_id` (string, optional): Verification check; if passed, must strictly match session token.

### Headers
- `X-Locale` / `Accept-Language` (string, optional): Target language override (`en`, `ar`, `ur`, `hi`). Defaults to `en`.
- `X-Client-Request-Id` / `Idempotency-Key` (string, optional): Client-supplied idempotency key for deterministic replay.

---

## 2. Response Contracts

### 2.1 Success Response — 200 OK

```ts
export interface QuizDeliveryQuestionItem {
  questionId: string;           // RFC 9562 UUIDv7 curriculum question identifier
  type: string;                 // Question format: "multiple_choice" | "sequence" | "true_false" | "image_match" | "audio_match"
  contentVersionId?: string;    // Version-locked content release identifier preventing mid-session drift (FR-13)
  prompt: string;               // Localized pedagogical question prompt text
  options: any[];               // Selectable answer choices or sequence items (correct answer strictly excluded)
  mediaUrl?: string | null;     // Optional CDN URL for accompanying audio or illustration
  mediaAltText?: string | null; // Optional accessibility description for screen readers (PRD §1.8)
}

export interface QuizDeliveryResponse {
  attemptId: string;                        // RFC 9562 UUIDv7 identifier of the created or resumed in-progress attempt
  questions: QuizDeliveryQuestionItem[];     // Ordered list of assembled questions (exactly 1 question for fact context)
  sourceMix: Record<string, number>;        // Candidate pool distribution counts ({"linked_fact": 1})
  context: string;                          // Delivery context ("islamic_facts")
  status: string;                           // Attempt lifecycle status ("in_progress")
  isResumed: boolean;                       // True if an existing in-progress attempt was resumed rather than freshly created
}
```

*Note: Dual-wire compatibility supports both camelCase (`attemptId`, `questionId`, `isResumed`, etc.) and snake_case.*

---

## 3. Error Responses

- `401 UNAUTHORIZED`: Missing, invalid, or expired child session Bearer token.
- `403 FORBIDDEN`: Sibling tenancy mismatch (`child_id` query parameter does not match session child token).
- `404 QUIZ_UNAVAILABLE`: Fact has no linked question (`linked_quiz_question_id IS NULL`), or linked question is soft-withdrawn/unpublished/missing. Client gracefully hides/removes the quiz button.
- `404 FACT_NOT_FOUND`: Specified `fact_id` does not exist in the Islamic fact catalog.
- `410 FACT_WITHDRAWN`: Specified `fact_id` entity is soft-withdrawn (`is_withdrawn = true`).
- `422 VALIDATION_ERROR`: `fact_id` path parameter is not a valid UUID string.
