# Phase 3 — core-navigation: Architecture & Bootstrap Blueprint

`Development_Blueprints.Phase3_Shared_Core_Modules.KMP.12-core-navigation-module-bootstrap.md`

**Module:** `core-navigation` (KMP Android & iOS)  
**Phase:** 3 — Shared/Core Modules  
**Status:** ✅ **Implemented & Verified** (Verified against `NoorHeroes/core/core-navigation/CORE_NAVIGATION_INSTRUCTIONS.md`)  
**Description:** Voyager / Decompose multiplatform navigation engine, sealed `Route` graph, backstack preservation, and Parent Gate interceptors.  
**Depends on:** Phase 0 Workspace, Phase 2 Security Baseline Prerequisites  
**Consumed by:** All Phase 4, Phase 5, Phase 6, Phase 8, and Phase 10 feature implementations  
**Source of truth:** `NoorHeroes/core/core-navigation/CORE_NAVIGATION_INSTRUCTIONS.md`; `NoorHeroes_Consolidated_Execution_Blueprint.md` §4  

---

## 1. Objective and Purpose
Manage app-wide navigation, bottom tab switching, modal dialogs, and deep links across Android and iOS.

## 2. Technical Requirements
- Router: Sealed interface `Route` defining all application destinations with strongly-typed arguments.
- Navigation Interceptor: Intercepts navigation to any Parent Area route (`/parent/*`), routing through C.19 Parent PIN/Biometric Gate before allowing entry.
- Deep Links: Universal link parser routing `noorheroes://...` URIs with session validation.

## 3. Technology Stack Preservation
- Voyager / Decompose Compose Multiplatform.

## 4. Verification and Acceptance Criteria
- [x] Navigation backstack survives screen rotation and configuration changes.
- [x] Parent Area routes cannot be reached without verified Parent Gate token.

