---
id: domain.notification-intent-service
kind: domain
title: Notification Trigger Catalog & Intent Creation Engine
status: stable
owner_story: TASK-B17-02
version: 1
created: 2026-10-09
---

## 1. Domain Context

Part of Feature B.17 (Notifications — Child-Facing) and Blueprint B-02. Defines the intake, scheduled evaluation, validation, deduplication, and lifecycle management for pending notification intents before policy evaluation.

---

## 2. Six Approved Trigger Classes (FR-1, FR-12)

The service accepts and classifies intents exclusively across 6 authorized child-facing trigger categories:

1. **Approved Learning Reminder (`daily_reminder` / `daily_reminder_due`)**:
   - Triggered when a child's daily learning goal is unmet by a configured threshold hour.
2. **Bedtime Story (`bedtime_story` / `bedtime_story_due`)**:
   - Triggered 30 minutes before configured bedtime. Must safely handle midnight-crossing windows (e.g. 23:45 to 00:30).
3. **Streak at Risk (`streak_risk` / `streak_at_risk`)**:
   - Triggered on late-day inactivity when an active streak is in danger of being broken.
4. **New Content Published (`content_published` / `new_content`)**:
   - Triggered when newly published story or learning content matches the child's age band and locale eligibility.
5. **Reward & Milestone (`reward_posted` / `reward_milestone`)**:
   - Triggered by notify-worthy Reward Service ledger entries celebrating milestones.
6. **Seasonal Calendar Event (`seasonal_event`)**:
   - Triggered by Islamic calendar schedules (e.g. Ramadan, Eid, Jummah, Laylat al-Qadr) targeting families and children.

---

## 3. Invariants & Rules

1. **Idempotent Deduplication (Blueprint B-02 §10, §15)**:
   - Evaluates a composite deduplication key: `(target_child_id, notification_type, trigger_window)`.
   - Prevents duplicate intent records from being created if domain events are replayed or scheduled jobs overlap within the same trigger window.

2. **Mandatory Content-Safety Filter at Intent Ingestion (PRD §3.5, Blueprint B-02 §10)**:
   - Every incoming event payload is pre-validated against child-safe content rules.
   - Any payload containing forbidden commercial, billing, or telemetry terms (`subscription`, `pricing`, `renew`, `paywall`, `credit card`, `checkout`, `engagement score`, etc.) is immediately rejected and dead-lettered.

3. **Midnight-Crossing Bedtime Computation (Edge Case 3, Blueprint B-02 §10)**:
   - The 30-minute pre-bedtime trigger window computes the target hour and minute modulo 24 hours.
   - Correctly handles bedtime schedules that span midnight without wrapping errors or date drift.

4. **Early Cancellation on Stale Domain Condition (Edge Case 7, Blueprint B-02 §10)**:
   - When an underlying condition resolves prior to send (e.g. child completes daily goal, or streak risk is resolved), the intent status transitions from `pending` to `canceled`.
   - Canceled intents are permanently suppressed and never forwarded to the Policy Engine or Delivery Adapter.

5. **In-App Notification Intent Parity (FR-13)**:
   - In-app notification triggers (`in_app_banner`, `episode_ready`) follow identical intent schemas and deduplication logic, ensuring unified governance.

6. **Dead-Letter Queue Resilience (Blueprint B-02 §18)**:
   - Unrecognized event types or malformed payloads with missing required attributes are logged and routed to a dead-letter queue, ensuring zero silent message drops while keeping the consumer running.
