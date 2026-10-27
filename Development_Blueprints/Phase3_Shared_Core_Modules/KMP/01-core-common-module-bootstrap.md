# Phase 3 — core-common: Architecture & Bootstrap Blueprint

`Development_Blueprints.Phase3_Shared_Core_Modules.KMP.01-core-common-module-bootstrap.md`

**Module:** `core-common` (KMP Android & iOS)  
**Phase:** 3 — Shared/Core Modules  
**Status:** ✅ **Implemented & Verified** (Verified against `NoorHeroes/core/core-common/CORE_COMMON_INSTRUCTIONS.md`)  
**Description:** Foundational Kotlin Multiplatform primitives: `AppDispatchers` (IO, Main, Default), strongly-typed `Result<T>` monad, `AppError` domain hierarchy, `DateTimeUtil` (Hijri/Gregorian bridging), and localized string resolvers.  
**Depends on:** Phase 0 Workspace, Phase 2 Security Baseline Prerequisites  
**Consumed by:** All Phase 4, Phase 5, Phase 6, Phase 8, and Phase 10 feature implementations  
**Source of truth:** `NoorHeroes/core/core-common/CORE_COMMON_INSTRUCTIONS.md`; `NoorHeroes_Consolidated_Execution_Blueprint.md` §4  

---

## 1. Objective and Purpose
Define the foundational non-UI Kotlin Multiplatform primitives shared by all core and feature modules across Android and iOS. Eliminates platform-specific threading or error handling duplication.

## 2. Technical Requirements
- `AppDispatchers`: Coroutine dispatchers interface exposing `main`, `io`, `default`, and `unconfined` with test dispatcher substitution.
- `Result<T>`: Sealed class hierarchy (`Success`, `Failure`, `Loading`) providing functional transformations (`map`, `flatMap`, `onSuccess`, `onFailure`).
- `AppError`: Domain error sealed interface categorizing network, authentication, validation, persistence, and authorization failures with localized error messages.
- `DateTimeUtil`: UTC timestamp formatting, relative time calculation, and Hijri calendar conversion support.

## 3. Technology Stack Preservation
- Kotlin Multiplatform 2.0+, kotlinx.coroutines 1.8+, kotlinx-datetime 0.6+.

## 4. Verification and Acceptance Criteria
- [x] Coroutine dispatcher abstraction verified with zero direct `Dispatchers.IO` calls in common code.
- [x] Result monad unit tests pass across both JVM/Android and iOS Simulator targets.

