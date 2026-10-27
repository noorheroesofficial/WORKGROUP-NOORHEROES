---
id: domain.fact-linked-quiz
kind: service
title: Fact-Linked Quiz Delegation Domain Service Interface
status: stable
owner_story: TASK-B18-04
version: 1
created: 2026-10-12
---

## Overview

The `FactQuizDelegationService` serves as a thin parameterization and delegation layer routing an Islamic Fact's single linked quiz question through Feature A.8's shared Quiz Engine (PRD FR-7 / Blueprint B-04).

## Domain Invariants

1. **FR-7 Zero Parallel Engine Invariant**:
   - Zero local scoring tables, retry mechanisms, question bank copies, or completion state machines are implemented in the `content` module.
   - Leverages shared `QuestionRepository`, `QuizAttempt`, and `QuizDeliveryResponse` from Feature A.8.
2. **Submissions Handoff**:
   - Client submits answers directly to A.8 shared endpoint `POST /v1/quizzes/attempts/{attempt_id}/responses`.
3. **Idempotent Attempt Resume**:
   - Checks existing in-progress attempts for `(child_id, "islamic_facts", fact_id)` or matching `client_request_id`.
   - Returns existing attempt with `is_resumed=True` without duplicate row creation.
4. **Mid-Session Question Drift Prevention (FR-13)**:
   - On resume, loads question from `existing_attempt.assembled_question_ids[0]` guaranteeing version-locked integrity even if admin re-links the fact record mid-session.
5. **Edge Case 3 Graceful Degradation**:
   - If `linked_quiz_question_id` is null or the referenced question is soft-withdrawn/unpublished/missing, raises `QuizUnavailableError` (HTTP 404 with code `QUIZ_UNAVAILABLE`).
6. **Answer Obfuscation (Security)**:
   - `QuizDeliveryQuestionItem` strictly omits `correct_answer` from all client payloads.

## Public Interface

```python
class FactQuizDelegationService(BaseService):
    async def get_fact_quiz(
        self,
        fact_id: str,
        child_ctx: ChildSessionContext,
        locale: Optional[str] = "en",
        client_request_id: Optional[str] = None,
    ) -> QuizDeliveryResponse:
        ...
```
