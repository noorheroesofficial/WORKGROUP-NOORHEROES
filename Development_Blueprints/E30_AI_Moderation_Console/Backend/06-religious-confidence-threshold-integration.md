# B-06 — Religious-Category Confidence Threshold Integration

## 1. Feature Context
Parent PRD: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
Depends on: F.35 (AI Layer Microservices Architecture — **owns** the six-stage pipeline itself, including the actual Confidence Score stage implementation)
Feeds into: B-01 (queue items must carry correct `stage_flagged`/`policy_category` for religious-rulings items)

## 2. Parent Feature
E.30 — AI Moderation Console & Safety Evaluation Harness

## 3. Sub-feature
**Religious-Category Confidence Threshold Integration** (ID: B-06) — this is a **boundary-contract and verification** sub-feature, not a rebuild of the pipeline. It documents and tests the console-side dependency on F.35's Confidence Score stage correctly applying a stricter threshold to religious-rulings-category interactions, and ensures such items surface correctly in this console's queue.

## 4. Objective
Guarantee — via a documented contract and a shared test-fixture bank — that a religious-rulings-category interaction whose confidence score would pass the *general* threshold but fails the *stricter religious-specific* threshold is blocked/escalated **before** display, and lands correctly in the Moderation Console's queue with accurate `policy_category`/`stage_flagged` data, without this console silently duplicating or second-guessing pipeline logic it does not own.

## 5. Business Requirements
- FR-2: religious answers must map to approved knowledge cards; rulings/aqeedah/halal-haram/prayer/fiqh receive stricter confidence thresholds and review paths.
- §3.5: religious-category stricter-threshold enforcement is applied **at the Confidence Score pipeline stage itself**, not merely a moderation-console-side after-the-fact check.
- §12.2 (OWASP-style note): "the religious-category stricter-threshold enforcement living at the actual pipeline stage (not a bolt-on filter) is a misconfiguration-defense pattern — there's no separate, potentially-forgotten check to bypass." This sub-feature must **not** introduce such a bolt-on, duplicate check in the console — doing so would itself violate this stated design principle.
- Edge Case 2: a technically-passing-but-theologically-imprecise religious answer is escalated to the Scholar Review Board via `escalate_content_gap`, not `mark_false_positive` (owned by B-03; this sub-feature ensures the underlying data — `policy_category` — is accurate enough for that routing decision to be made correctly).

## 6. Existing Architecture
This is explicitly a **cross-module boundary** sub-feature. No new bounded context or service is created — it is a verification/contract layer sitting between F.35 (owner of the pipeline) and `ai_moderation` (B-01, this console's queue). Do not implement threshold-comparison logic inside `ai_moderation` — that would duplicate F.35's stated single point of enforcement.

## 7. Existing Code to Reuse
- B-01's `AiModerationQueueItem.stage_flagged`/`policy_category` fields — the data contract this sub-feature verifies, not modifies
- `media/safety_pipeline.py`'s fail-closed orchestration style, as the precedent for how a pipeline stage should behave under any failure/timeout/ambiguity (relevant if F.35's Confidence Score stage is implemented with a similar fail-closed contract — confirm, do not assume, since B-06 does not own that implementation)

## 8. Files to Create
- `tests/modules/ai_moderation/test_religious_threshold_queue_integration.py` — integration test owned jointly with F.35's test suite; asserts that a fixture religious-rulings-category interaction with a confidence score between the general and stricter thresholds correctly produces an `ai_moderation_queue_item` with `stage_flagged="confidence_score"` and the correct `policy_category`.
- `docs/cross-feature-contracts/e30-b06-religious-threshold-contract.md` — a short, explicit written contract (per the parent PRD's "Do not guess" instruction) stating: (1) F.35 owns threshold comparison; (2) F.35 must write a flagged queue item with accurate `policy_category` when the stricter threshold fails; (3) B-01 reads that item as-is, with no additional threshold logic.
- `tests/fixtures/religious_rulings_confidence_scenarios.py` — a fixture bank of religious-rulings-category test scenarios at varying confidence levels, for staging verification (§10 DevOps requirement), shared between F.35's and E.30's test suites.

## 9. Files to Modify
None in `ai_moderation` itself — this sub-feature is intentionally read-only/verification-only with respect to B-01's code. If F.35's implementation does not yet exist or does not yet write `policy_category` accurately, flag this as an **open cross-team dependency**, not something to silently patch around inside `ai_moderation`.

## 10. Backend Requirements

### 10.1 The Contract (Non-Negotiable Boundary)
```text
F.35 (Confidence Score stage)
    │  religious-rulings category, confidence score fails stricter threshold
    ▼
Writes ai_safety_event row (redacted) + ai_moderation_queue_item row
    with stage_flagged = "confidence_score", policy_category = "religious_ruling" (or equivalent)
    │
    ▼
B-01 (this console) reads the queue item AS-IS — no re-evaluation of confidence score,
    no second threshold check, no duplicate business rule.
```

### 10.2 Verification, Not Reimplementation
```python
# tests/modules/ai_moderation/test_religious_threshold_queue_integration.py
async def test_religious_ruling_below_strict_threshold_appears_in_queue(seeded_db, religious_rulings_fixture):
    """Given F.35's pipeline has (per its own contract) flagged a religious-rulings
    interaction that passed the general threshold but failed the stricter one,
    confirm it surfaces correctly through THIS console's read path — this test
    does NOT re-implement or re-verify the threshold comparison itself, which is
    F.35's exclusive responsibility per §3.5/§12.2."""
    queue_item = await ai_moderation_repo.get_detail_joined(religious_rulings_fixture.queue_item_id)
    assert queue_item["stage_flagged"] == "confidence_score"
    assert queue_item["policy_category"] == "religious_ruling"
```

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
None directly — N-02's rendering of `policy_category` (B-01's data) is sufficient; no religious-threshold-specific frontend logic is required beyond displaying the field accurately.

## 13. API Contract
No new API — this sub-feature verifies B-01's existing `GET /v1/admin/ai-moderation/{id}` contract carries accurate `policy_category`/`stage_flagged` for religious-rulings items.

## 14. Database Requirements
None new. Confirms `ai_moderation_queue_item.stage_flagged`/`policy_category`-equivalent data (via the joined `AiSafetyEvent.category`) is populated correctly by the F.35 write path.

## 15. Validation
N/A — this sub-feature validates a cross-team contract, not user input.

## 16. Authentication
N/A.

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | Handling |
|---|---|
| F.35's pipeline does not yet write `policy_category` accurately for religious items | **Open dependency — do not guess or patch around it in `ai_moderation`.** Document as a blocking cross-team item in the contract doc (§8) and raise it rather than silently working around it. |
| A religious-rulings item is flagged but its `policy_category` is missing/null | Surface as-is in the queue (B-01's existing null-handling), do not backfill or infer the category client-side. |

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
Not applicable.

## 22. RTL
Not applicable.

## 23. Analytics
`ai_religious_category_strict_threshold_applied` (§1.19, internal) — this event is fired by **F.35's** pipeline at the point of threshold enforcement, not by this console; B-06's role is to confirm (via the fixture bank) that the event and the resulting queue item are consistent with each other.

## 24. Performance
Not applicable beyond B-01's existing query performance.

## 25. Security
Misconfiguration-defense principle (§12.2): keeping threshold enforcement exclusively at the F.35 pipeline stage — and explicitly **not** duplicating it here — is itself the security property this sub-feature protects. A well-intentioned "just in case" duplicate check inside `ai_moderation` would create exactly the "separate, potentially-forgotten check" §12.2 warns against.

## 26. Library Requirements
pytest-asyncio; shared fixture module importable by both F.35's and `ai_moderation`'s test suites.

## 27. Testing
- Integration test per §10.2, confirming accurate queue-item data for a religious-rulings scenario — **does not** re-test the threshold math itself (that's F.35's test suite's job).
- Regression fixture bank (§8) covering religious-rulings scenarios at varying confidence levels, used for staging verification before any deploy touching the Confidence Score stage's threshold logic (§10 DevOps requirement) — this fixture bank is a **shared artifact**, not owned exclusively by E.30.

## 28. Documentation
`docs/cross-feature-contracts/e30-b06-religious-threshold-contract.md` is the primary deliverable of this sub-feature — a short, explicit statement of which module owns what, preventing future duplication or drift.

## 29. AI Coding Agent Implementation Steps
- **Task 01 — Write the cross-feature contract doc** (§8) explicitly, before any test code — this is the actual point of this sub-feature.
- **Task 02 — Confirm current F.35 implementation status**: does the Confidence Score stage already write accurate `policy_category` for religious items? If F.35 is not yet built, document this as a blocking dependency rather than stubbing around it silently.
- **Task 03 — Build the shared fixture bank** of religious-rulings scenarios at varying confidence levels.
- **Task 04 — Integration test** per §10.2, verifying B-01's read path against the fixture bank.
- **Task 05 — Final Code Review**: confirm no threshold-comparison logic has been added inside `ai_moderation` anywhere in this change set — grep for any new confidence-score comparison code as an explicit review step.

## 30. Definition of Done
Cross-feature contract documented; fixture bank built and shared; integration test confirms B-01's queue-item data is accurate for religious-rulings scenarios flagged by F.35, with zero duplicate threshold logic introduced inside `ai_moderation`.

## 31. Final Verification Checklist
- [ ] Cross-feature contract doc written and reviewed
- [ ] F.35's current implementation status confirmed (not assumed)
- [ ] Shared religious-rulings fixture bank built
- [ ] Integration test confirms accurate `policy_category`/`stage_flagged` data flow
- [ ] Code review confirms zero duplicate threshold-comparison logic added to `ai_moderation`
- [ ] Any blocking F.35 dependency explicitly flagged, not silently patched around
