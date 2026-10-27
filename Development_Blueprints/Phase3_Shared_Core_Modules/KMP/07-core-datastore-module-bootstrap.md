# Phase 3 — core-datastore: Architecture & Bootstrap Blueprint

`Development_Blueprints.Phase3_Shared_Core_Modules.KMP.07-core-datastore-module-bootstrap.md`

**Module:** `core-datastore` (KMP Android & iOS)  
**Phase:** 3 — Shared/Core Modules  
**Status:** ✅ **Implemented & Verified** (Verified against `NoorHeroes/core/core-datastore/CORE_DATASTORE_INSTRUCTIONS.md`)  
**Description:** Key-value preferences store, encryption layer, Remote Config caching, and dynamic feature flag evaluation.  
**Depends on:** Phase 0 Workspace, Phase 2 Security Baseline Prerequisites  
**Consumed by:** All Phase 4, Phase 5, Phase 6, Phase 8, and Phase 10 feature implementations  
**Source of truth:** `NoorHeroes/core/core-datastore/CORE_DATASTORE_INSTRUCTIONS.md`; `NoorHeroes_Consolidated_Execution_Blueprint.md` §4  

---

## 1. Objective and Purpose
Provide fast, reactive key-value storage for app settings, selected language, onboarding completion flags, and cached remote feature configurations.

## 2. Technical Requirements
- Storage: Multiplatform `DataStore` / `MultiplatformSettings`.
- Remote Config: `RemoteConfigRepository` managing feature flags, maintenance mode banners, and minimum semver version enforcement.
- Reactive: Exposes preferences via `StateFlow` for immediate Composable recomposition on toggle.

## 3. Technology Stack Preservation
- AndroidX DataStore / Multiplatform Settings 1.1+.

## 4. Verification and Acceptance Criteria
- [x] Preferences persist across app process death and cold restart.
- [x] Feature flag evaluation defaults safely to conservative child-safe values when offline.

