---
id: domain.notification-policy-engine
kind: domain
title: Notification Policy Engine Send-Time Evaluation Rules
status: stable
owner_story: TASK-B17-03
version: 1
created: 2026-10-09
---

## 1. Domain Context

Part of Feature B.17 (Notifications — Child-Facing) and Blueprint B-03. Implements the central principle of the child notification architecture: **every policy, consent, quiet-hours, fatigue, and binding check is evaluated strictly at actual send time against live system state, never relying on a stale intent-creation snapshot**.

---

## 2. Six-Stage Send-Time Evaluation Sequence (Blueprint B-03 §10)

For every `pending` notification intent claimed by the delivery worker, the `PolicyEngine` executes the following checks in strict order:

```
[Claim Intent (status='processing')]
               │
               ▼
   [Stage 1: Consent & Category Opt-In] ────(Opted Out)────► [Suppressed: consent]
               │ (Passed)
               ▼
   [Stage 2: Quiet Hours & Bedtime] ───────(In Window)─────► [Suppressed: quiet_hours]
               │ (Passed)
               ▼
   [Stage 3: Frequency Budget & Fatigue] ──(Cap Exceeded)──► [Suppressed: frequency_cap]
               │ (Passed)
               ▼
   [Stage 4: Age Band & Locale Match] ─────(Ineligible)────► [Suppressed: age_ineligible / locale_mismatch]
               │ (Passed)
               ▼
   [Stage 5: Live Active Binding Gate] ────(Not Active)────► [Suppressed: binding_inactive]
               │ (Passed)
               ▼
   [Stage 6: Stale Condition Re-Check] ────(Resolved)──────► [Suppressed: stale_condition]
               │ (Passed)
               ▼
   [Hand off to B-04 Template Rendering & B-05 Delivery]
```

---

## 3. Policy Invariants & Rules

1. **Mandatory Live Re-Evaluation (PRD §3.5, §5 preamble)**:
   - Evaluates current `screen_time_policies`, live Redis fatigue/frequency counters, current child profile age, and live `device_profile_bindings`.
   - Never trusts snapshots taken when the intent was created hours or minutes prior.

2. **Stage 1 — Consent & Parental Controls (FR-3)**:
   - Checks per-child notification preferences. If the parent disabled reminders or specific notification categories for this child, suppresses immediately.

3. **Stage 2 — Quiet Hours & Bedtime Protection (FR-3, FR-10, Edge Case 6)**:
   - Compares the current local time in the child's timezone against the parent-configured quiet hours and bedtime windows.
   - Accurately handles midnight-crossing quiet windows (e.g. 21:00 to 07:00).
   - If the parent changed quiet-hours config after intent creation, the new configuration is respected at send time.

4. **Stage 3 — Frequency Caps & Progressive Fatigue Backoff (FR-4, FR-11)**:
   - Redis-backed sliding-window counters enforce maximum notifications per child per day and week.
   - Tracks consecutive non-open events per category. If non-opens reach threshold, exponentially backs off the send interval until child re-engagement occurs.

5. **Stage 4 — Birthday Rollover & Locale Compatibility (Edge Case 11)**:
   - Re-computes child's exact age at delivery attempt. If a child aged out of the content's age band on their birthday between intent creation and send, suppresses delivery.
   - Validates child's current device locale against the content's supported languages.

6. **Stage 5 — Live Active Binding Re-Check (P0 Invariant, Edge Case 1)**:
   - Inspects `device_profile_bindings` on the target installation.
   - Delivery is permitted ONLY if the installation's active binding currently matches `target_child_id`.
   - If the device was switched to a sibling profile, switched to parent mode, or logged out, delivery is suppressed (`binding_inactive`), preventing cross-profile leakage.

7. **Stage 6 — Final Stale Condition Resolution (Edge Case 7)**:
   - Re-queries the domain condition (e.g. daily goal progress or streak status).
   - If the task was completed in the interim, suppresses with `stale_condition`.

8. **Fail-Safe Defense In Depth (Blueprint B-03 §10, §18)**:
   - If Redis (frequency counters) or PostgreSQL (binding/quiet-hours) encounters an unexpected outage during policy evaluation, the engine **fails safe** by suppressing the delivery.
   - The engine NEVER fails open to dispatch unpoliced notifications to a child.
