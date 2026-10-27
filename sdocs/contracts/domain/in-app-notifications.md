---
id: domain.in-app-notifications
kind: domain
title: In-App Notification Projection & Eligibility Rules
status: stable
owner_story: TASK-B17-09
version: 1
created: 2026-10-09
---

## 1. Domain Context

Part of Feature B.17 (Notifications — Child-Facing) and Blueprint B-09. Defines the read-only projection rules governing pull-based in-app notification banners displayed in child mobile apps (K-03).

---

## 2. Eligibility & Projection Invariants

1. **Policy Derivation Immutability (FR-13, Blueprint B-09 §5, §10)**:
   - In-app notifications pass through the central policy engine (B-03) at intent send time.
   - The fetch API (`InAppNotificationFetchService`) is strictly a **read-only projection** over intents already in `status='sent'`.
   - It NEVER performs independent consent, quiet-hours, frequency-budget, or fatigue-backoff re-evaluations during fetch, ensuring zero policy drift between push and in-app channels.

2. **Strict Child Horizontal Isolation (Blueprint B-09 §15, §25)**:
   - Queried intents MUST have `target_child_id == child_id` matching the authenticated child session token.
   - Sibling or cross-family notifications are strictly excluded from results, preventing accidental leakage on shared family devices.

3. **Pre-Rendered Copy Governance (Blueprint B-09 §10, §21)**:
   - Copy returned to the client is the pre-rendered, child-safe template output persisted during B-04 / delivery processing.
   - No dynamic string substitution or template recompilation happens during fetch, preserving the content-safety guarantee (no billing terms or sensitive telemetry).

4. **Time-Bounded Expiration (Blueprint B-09 §14, §24)**:
   - If an intent specifies `expires_at`, it is only eligible when `expires_at > current_utc_time`.
   - If `expires_at` is NULL, the intent is considered unexpired unless explicitly governed by client-side local dismissal (K-03).

5. **In-App Eligible Trigger Classes (Blueprint B-09 §10)**:
   - The projection filters `notification_type` against `IN_APP_ELIGIBLE_TYPES`:
     - `in_app_banner`
     - `new_content`
     - `episode_ready`
     - `sequential_unlock_ready`
     - `content_published`
     - `daily_reminder`, `daily_reminder_due`
     - `streak_risk`, `streak_at_risk`
     - `bedtime_story`, `bedtime_story_due`
     - `reward_posted`, `reward_milestone`
     - `seasonal_event`

6. **Client-Local Dismissal Independence (Blueprint B-09 §5, §20)**:
   - Dismissal state is managed locally in the client repository (`InAppNotificationRepository` / K-03).
   - The backend returns all eligible unexpired instances; the mobile client filters out items previously dismissed on that device profile.
