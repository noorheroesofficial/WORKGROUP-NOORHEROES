---
id: domain.device-profile-binding
kind: domain
title: Device Profile Binding Domain Engine & Exclusivity Rules
status: stable
owner_story: TASK-B17-01
version: 1
created: 2026-10-09
---

## 1. Domain Context

Part of Feature B.17 (Notifications — Child-Facing) and Blueprint B-01. Governs how device installations, push notification tokens, and family profile targeting interact to guarantee zero cross-profile misdelivery on single-user or shared family devices.

---

## 2. Invariants & Rules

1. **One-Token-Per-Installation Reality (FR-8)**:
   - FCM tokens are scoped to app installations, not user identities or child profiles.
   - Targeting is decoupled from tokens and managed strictly through the `device_profile_bindings` domain layer.

2. **Single-Row-Per-Installation Structural Exclusivity (PRD §4.2, Blueprint B-01 §10)**:
   - `device_profile_bindings` uses `installation_id` as the primary key.
   - Profile switches perform an atomic database UPSERT (`INSERT ... ON CONFLICT (installation_id) DO UPDATE`).
   - Structural guarantee: it is impossible for an installation to have multiple active binding rows or ambiguous target states.

3. **Indivisible State Transition (Acceptance Criteria §1.9)**:
   - There is no queryable intermediate state where an installation has zero active bindings during a profile transition, nor multiple bindings.
   - Deactivation of the previous profile and activation of the incoming profile occur in the same database transaction.

4. **Family Ownership Gate (PRD §12.3, Blueprint B-01 §15, §17)**:
   - A binding to `target_child_id` is only permitted if the child profile belongs to the caller's verified `family_id` and is active (not deleted or archived).
   - Unauthorized attempts raise `TargetChildNotInFamilyError` (`403 Forbidden`).

5. **Child Session Authority Constraint (Blueprint B-01 §15)**:
   - When a request originates from an active child-mode session, the caller may only bind the device to their own authenticated `child_id`.
   - Child sessions cannot switch bindings to `parent` or to sibling profiles.

6. **Safe Default State on Logout (PRD §1.10 Edge Case 8)**:
   - On parent logout or explicit deactivation, all associated bindings have `target` set to `'none'` and `active` set to `false`.
   - An unbound device is a valid, safe system state: notifications queued for the family will not be dispatched to this installation while unbound.

7. **Transactional Outbox Event Emission (Blueprint B-01 §23)**:
   - Every successful profile binding switch atomically emits:
     - `NotificationBindingDeactivated` (for the previous target, if any was active)
     - `NotificationBindingActivated` (for the new target: `parent` or `child_id`)
