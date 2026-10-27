# B-06 Spaced Repetition Scheduler Service Runbook

## 1. System Overview
The Spaced Repetition Scheduler is a critical pedagogical engine within Feature A.5 (Quran & Arabic Learning) that computes when mastered skills become due for refresh review and transitions them to the `Needs Refresh` state without overwhelming the learner.

- **Feature**: A.5 — Quran & Arabic Learning
- **Sub-feature**: B-06 — Spaced Repetition Scheduler Service
- **Execution Pattern**: Nightly Celery Beat background job + On-demand API endpoints
- **State Transition**: `mastered` -> `needs_refresh` via shared `mastery_state_machine.compute_next_state(is_decay_triggered=True)`

---

## 2. Pedagogical Principles & Business Rules
1. **Gentle, Encouraging Framing (FR-4)**:
   - When a skill decays into `Needs Refresh`, the UI surfaces an encouraging prompt: *"Let's review this together!"* (`SPACED_REVIEW_PROMPT_CATALOG`).
   - It is never framed as a failure, penalty, regression, or loss of progress.
2. **Daily Prompt Capping (Edge Case 6)**:
   - If multiple nodes are simultaneously due on the same day, the system caps the number of `Needs Refresh` transitions per child per day at `daily_review_prompt_cap` (default: 2).
   - Only up to the daily cap rows are marked `shown_today = True` and transitioned to `needs_refresh`.
   - Remaining due nodes stay queued (`shown_today = False`) for subsequent days without dropping or losing due status.
3. **Outage Recovery (Edge Case 12)**:
   - If the nightly scheduler experiences downtime or delay, overdue reviews (`due_date <= today`) are still correctly processed and capped on the next run without being skipped or dumped all at once.
4. **Retention Purge Policy**:
   - `spaced_review_schedules` records older than 30 days past their `due_date` are purged automatically to maintain lean database tables.
5. **Skill-Tree Cache Invalidation**:
   - Every state transition to `needs_refresh` automatically triggers cache invalidation on `SkillTreeService` (`noorheroes:learning:skill_tree:{child_id}:{track}`), guaranteeing learners see up-to-date node states on next app open.

---

## 3. Mathematical Decay Function & Configuration
The decay function computes the due date for a mastered node:
$$\text{interval\_days} = \max\left(1, \text{round}\left(\text{base\_days} \times \frac{w_{\text{recency}} \times 1.0 + w_{\text{mastery}} \times (\text{mastery\_score} / 0.85)}{w_{\text{recency}} + w_{\text{mastery}}}\right)\right)$$

### Default Parameters:
- `base_retention_days`: 14 days
- `decay_weights`:
  - `recency`: 0.4
  - `mastery_strength`: 0.6
- `daily_review_prompt_cap`: 2
- `retention_purge_days`: 30

### Boundary Guards:
- Clamps continuous mastery score between 0.0 and 1.0.
- Preserves borderline mastery rounding without double penalty.
- Defensive fallback to defaults if weights are corrupt, negative, or sum to zero.
- Daily cap enforced to be $\ge 1$.

---

## 4. Operational Execution & Scheduling

### Nightly Scheduled Celery Task
- **Celery Task**: `learning.run_spaced_repetition_scheduler`
- **Schedule**: Every 86400 seconds (24 hours, recommended run at 02:00 UTC)
- **Beat Entry**: `run_spaced_repetition_scheduler_nightly` in `src/noorheroes/core/celery_app.py`
- **Execution Pipeline**: `src/noorheroes/modules/learning/tasks.py`

### HTTP Endpoints
- **Child Due Reviews**: `GET /learning/spaced-repetition/due`
  - Auth: Child Bearer token
  - Returns capped due reviews with localized prompts (English, Hindi, Urdu, Arabic).
- **Admin Trigger / Backfill**: `POST /learning/spaced-repetition/run`
  - Body: `{"childId": "optional-uuid", "evaluationDate": "YYYY-MM-DD"}`
  - Returns execution summary with counts of evaluated, transitioned, queued, and purged records.

---

## 5. DevOps Monitoring & Alerting Runbook

### Alert 1: Scheduler Task Failure (`spaced_repetition_scheduler_task_failed`)
- **Severity**: P1 (Learning Quality Regression)
- **Impact**: Mastered nodes do not decay; spaced reinforcement prompts fail to surface, reducing retention.
- **Triage**:
  1. Check Celery worker logs for `spaced_repetition_scheduler_task_failed`.
  2. Verify database connection health and Redis lock availability.
  3. Re-run manually via `POST /learning/spaced-repetition/run` or Celery CLI:
     ```bash
     celery -A src.noorheroes.core.celery_app call learning.run_spaced_repetition_scheduler
     ```
  4. Ensure task completes idempotently without double-transitions.

### Alert 2: Partial Batch Failures (`spaced_repetition_partial_batch_failures_alert`)
- **Severity**: P2
- **Impact**: Specific children failed scheduling while others succeeded due to per-child isolation.
- **Triage**:
  1. Search logs for `child_spaced_repetition_failed` with `child_id`.
  2. Inspect state consistency in `skill_node_states` for the affected `child_id`.
  3. Execute targeted child remediation:
     ```bash
     curl -X POST https://api.noorheroes.com/learning/spaced-repetition/run \
       -H "Content-Type: application/json" \
       -d '{"childId": "<affected-child-uuid>"}'
     ```
