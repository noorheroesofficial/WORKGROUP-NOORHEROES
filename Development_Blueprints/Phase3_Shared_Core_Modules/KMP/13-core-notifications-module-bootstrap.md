# Phase 3 — core-notifications: Architecture & Bootstrap Blueprint

`Development_Blueprints.Phase3_Shared_Core_Modules.KMP.13-core-notifications-module-bootstrap.md`

**Module:** `core-notifications` (KMP Android & iOS)  
**Phase:** 3 — Shared/Core Modules  
**Status:** ✅ **Implemented & Verified** (Verified against `NoorHeroes/core/core-notifications/CORE_NOTIFICATIONS_INSTRUCTIONS.md`)  
**Description:** Local notification scheduling engine, FCM / APNs token registration, and notification permission state handling.  
**Depends on:** Phase 0 Workspace, Phase 2 Security Baseline Prerequisites  
**Consumed by:** All Phase 4, Phase 5, Phase 6, Phase 8, and Phase 10 feature implementations  
**Source of truth:** `NoorHeroes/core/core-notifications/CORE_NOTIFICATIONS_INSTRUCTIONS.md`; `NoorHeroes_Consolidated_Execution_Blueprint.md` §4  

---

## 1. Objective and Purpose
Deliver timely, localized notifications (habit reminders, bedtime alerts, prayer times, Ramadan countdowns) across Android and iOS.

## 2. Technical Requirements
- Local Scheduling: `LocalNotificationScheduler` managing exact alarms (Android `AlarmManager`) and iOS `UNNotificationRequest`.
- Push Registration: FCM token registration on Android; APNs device token registration on iOS.
- Quiet Hours: Respects parent-configured quiet hours and bedtime mode suppression rules.

## 3. Technology Stack Preservation
- Android NotificationManager, iOS UserNotifications Framework.

## 4. Verification and Acceptance Criteria
- [x] Notifications trigger at scheduled local times.
- [x] Quiet hours prevent notification delivery during sleep periods.

