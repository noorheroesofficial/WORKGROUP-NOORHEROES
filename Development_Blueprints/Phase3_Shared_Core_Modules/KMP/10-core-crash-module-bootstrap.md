# Phase 3 — core-crash: Architecture & Bootstrap Blueprint

`Development_Blueprints.Phase3_Shared_Core_Modules.KMP.10-core-crash-module-bootstrap.md`

**Module:** `core-crash` (KMP Android & iOS)  
**Phase:** 3 — Shared/Core Modules  
**Status:** ✅ **Implemented & Verified** (Verified against `NoorHeroes/core/core-crash/CORE_CRASH_INSTRUCTIONS.md`)  
**Description:** Multiplatform crash reporting abstraction (`CrashReporter`), GitLive Crashlytics bindings, and breadcrumb event tracking.  
**Depends on:** Phase 0 Workspace, Phase 2 Security Baseline Prerequisites  
**Consumed by:** All Phase 4, Phase 5, Phase 6, Phase 8, and Phase 10 feature implementations  
**Source of truth:** `NoorHeroes/core/core-crash/CORE_CRASH_INSTRUCTIONS.md`; `NoorHeroes_Consolidated_Execution_Blueprint.md` §4  

---

## 1. Objective and Purpose
Track client application stability and capture stack traces without leaking sensitive user data.

## 2. Technical Requirements
- Abstraction: `CrashReporter` interface exposing `recordException()`, `logBreadcrumb()`, `setCustomKey()`.
- Binding: Production binding wraps Firebase Crashlytics via GitLive wrapper; development binding routes to `:core:logger`.
- Sanitization: Automatically scrubs PII from breadcrumb keys and exception messages.

## 3. Technology Stack Preservation
- GitLive Firebase Crashlytics KMP.

## 4. Verification and Acceptance Criteria
- [x] Unhandled exceptions log breadcrumbs leading up to the crash event.
- [x] Crashlytics reports contain zero child real names or contacts.

