# Phase 3 — composeApp: Architecture & Bootstrap Blueprint

`Development_Blueprints.Phase3_Shared_Core_Modules.KMP.15-composeapp-di-wiring-koin.md`

**Module:** `composeApp` (KMP Android & iOS)  
**Phase:** 3 — Shared/Core Modules  
**Status:** ✅ **Implemented & Verified** (Verified against `NoorHeroes/composeApp/src/commonMain/kotlin/com/noorheroes/di/`)  
**Description:** Compose Multiplatform root application assembly and Koin dependency injection module graph wiring across all 14 core modules.  
**Depends on:** Phase 0 Workspace, Phase 2 Security Baseline Prerequisites  
**Consumed by:** All Phase 4, Phase 5, Phase 6, Phase 8, and Phase 10 feature implementations  
**Source of truth:** `NoorHeroes/composeApp/src/commonMain/kotlin/com/noorheroes/di/`; `NoorHeroes_Consolidated_Execution_Blueprint.md` §4  

---

## 1. Objective and Purpose
Assemble the complete mobile application by wiring all 14 core libraries and feature modules into a unified Koin DI container.

## 2. Technical Requirements
- Koin Modules: `commonCoreModule`, `networkModule`, `databaseModule`, `securityModule`, `uiModule`, `navigationModule`, `playerModule`.
- Platform Graph: Platform-specific modules inject platform drivers (Keystore, AVPlayer, SQLite).
- Scope Management: Singletons for infrastructure clients, feature-scoped ViewModels for screen lifecycles.

## 3. Technology Stack Preservation
- Koin 3.5+ Multiplatform (Hilt is explicitly not used because it cannot inject into shared CMP Composables).

## 4. Verification and Acceptance Criteria
- [x] Koin dependency graph validates with zero circular dependencies or missing bindings.
- [x] App boots cleanly to Splash Screen on both Android and iOS targets.

