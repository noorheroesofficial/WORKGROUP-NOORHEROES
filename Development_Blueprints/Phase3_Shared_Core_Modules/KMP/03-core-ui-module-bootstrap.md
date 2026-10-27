# Phase 3 — core-ui: Architecture & Bootstrap Blueprint

`Development_Blueprints.Phase3_Shared_Core_Modules.KMP.03-core-ui-module-bootstrap.md`

**Module:** `core-ui` (KMP Android & iOS)  
**Phase:** 3 — Shared/Core Modules  
**Status:** ✅ **Implemented & Verified** (Verified against `NoorHeroes/core/core-ui/CORE_UI_INSTRUCTIONS.md`)  
**Description:** Reusable Compose Multiplatform UI components, skeleton/shimmer loaders, and 5-state screen container state machines (`Loading`, `Content`, `Empty`, `Error`, `Offline`).  
**Depends on:** Phase 0 Workspace, Phase 2 Security Baseline Prerequisites  
**Consumed by:** All Phase 4, Phase 5, Phase 6, Phase 8, and Phase 10 feature implementations  
**Source of truth:** `NoorHeroes/core/core-ui/CORE_UI_INSTRUCTIONS.md`; `NoorHeroes_Consolidated_Execution_Blueprint.md` §4  

---

## 1. Objective and Purpose
Provide standardized UI building blocks implementing the universal screen state machine directive across all 562 screen designs.

## 2. Technical Requirements
- Components: `NoorButton` (Primary, Secondary, Ghost, Icon), `NoorCard`, `NoorTextField`, `NoorTopAppBar`, `NoorBottomSheet`.
- State Machine: `StateContainer<T>` composable handling loading shimmer, empty illustrations, retryable error banners, and offline cached indicators.
- Accessibility: Minimum 48x48dp touch targets, content descriptions on all graphical elements, high-contrast support.

## 3. Technology Stack Preservation
- Compose Multiplatform, Coil3 for asynchronous image loading.

## 4. Verification and Acceptance Criteria
- [x] All 5 fundamental states verified with interactive preview tests.
- [x] Accessibility audit confirms zero missing content descriptions.

