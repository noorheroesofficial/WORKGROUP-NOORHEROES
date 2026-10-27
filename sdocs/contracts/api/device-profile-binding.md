---
id: api.device-profile-binding
kind: api
title: Device Profile Binding & Token Registration API
status: stable
owner_story: TASK-B17-01
version: 1
created: 2026-10-09
---

## Endpoints

```http
POST   /v1/devices
PATCH  /v1/devices/{id}/active-profile
DELETE /v1/devices/{id}/active-profile
```

## Auth & Security

- **Auth**: Bearer token supporting both Parent (`ParentSessionContext`) and Child (`ChildSessionContext`) sessions via `DeviceCallerContext`.
- **P0 Exclusive Targeting Guarantee (PRD FR-8, FR-9; Blueprint B-01 §4, §13)**: Firebase issues one FCM push token per app installation, not per child profile. NoorHeroes achieves per-child targeting through an exclusive active-profile binding on each installation.
- **Atomic Single-Row Transaction**: The binding switch is implemented as a single indivisible database UPSERT on `device_profile_bindings.installation_id`. At no queryable moment does an installation have zero or multiple active bindings simultaneously.
- **Family Ownership Security Gate (403)**: When switching to `target_child_id`, the backend validates server-side that the child belongs to the caller's family (`family_id`). Child sessions can only bind to their own authenticated child profile.

---

## 1. POST /v1/devices (Device Installation & Token Registration)

### 1.1 Request Payload

```json
{
  "fcm_token": "string",
  "app_version": "string",
  "locale": "string",
  "timezone": "string",
  "installation_id": "uuid (optional)"
}
```

### 1.2 Response Contract (200 OK)

```json
{
  "installation_id": "0191c0e3-9824-7ef2-9e8a-0242ac120002"
}
```

### 1.3 Errors
- `400 BAD_REQUEST`: Empty or invalid `fcm_token`, invalid `locale` or `timezone`.
- `401 UNAUTHORIZED`: Missing, invalid, or expired Bearer token.

---

## 2. PATCH /v1/devices/{id}/active-profile (Atomic Active Profile Switch)

### 2.1 Request Payload

Exactly one of `target: "parent"` OR `target_child_id: "<uuid>"` must be provided:

```json
{
  "target": "parent"
}
```
*or*
```json
{
  "target_child_id": "0191c0e3-9824-7ef2-9e8a-0242ac120003"
}
```

### 2.2 Response Contract (200 OK)

```json
{
  "bound": true,
  "target": "parent" // or "<child_uuid>"
}
```

### 2.3 Errors
- `400 BAD_REQUEST`: Both `target` and `target_child_id` provided, or neither provided.
- `401 UNAUTHORIZED`: Missing or invalid Bearer token.
- `403 FORBIDDEN`: Child profile outside caller's family, or child-mode session attempting cross-child or parent binding.
- `404 NOT_FOUND`: Device installation not found.
- `409 CONFLICT`: Concurrency transaction conflict (retryable).

---

## 3. DELETE /v1/devices/{id}/active-profile (Deactivate on Logout)

### 3.1 Response Contract (200 OK)

```json
{
  "bound": false,
  "target": "none"
}
```

### 3.2 Errors
- `401 UNAUTHORIZED`: Missing or invalid Bearer token.
- `404 NOT_FOUND`: Device installation not found.

---

## 4. Core Invariants & System Behavior

| Scenario | System Behavior |
|:---|:---|
| **First-Time App Launch** | Client calls `POST /v1/devices`, creating `PushInstallation` and activating `PushToken` (`state='active'`). |
| **Token Refresh** | Re-registration with existing FCM token refreshes installation metadata and updates token timestamps. |
| **Profile Switch (Parent to Child)** | Indivisible UPSERT sets target to `child` and `target_child_id` to selected child. Deactivation of previous target and activation of new target are atomic. |
| **Profile Switch (Child to Sibling)** | Atomic switch to new sibling ID. Emits `notification_binding_deactivated` for prior child and `notification_binding_activated` for new child. |
| **Logout** | Calls `DELETE /v1/devices/{id}/active-profile` or `deactivate_all_for_parent()`, setting `target='none'` and `active=false`. Unbound state is expected and safe. |
| **Shared Family Device** | Two devices in the same family operate independently (e.g. Tablet bound to Child A, Phone bound to Parent or Child B). |
