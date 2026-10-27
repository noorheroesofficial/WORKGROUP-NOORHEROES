# Phase 3 — core-designsystem: Architecture & Bootstrap Blueprint

`Development_Blueprints.Phase3_Shared_Core_Modules.KMP.02-core-designsystem-module-bootstrap.md`

**Module:** `core-designsystem` (KMP Android & iOS)  
**Phase:** 3 — Shared/Core Modules  
**Status:** ✅ **Implemented & Verified** (Verified against `NoorHeroes/core/core-designsystem/CORE_DESIGNSYSTEM_INSTRUCTIONS.md`)  
**Description:** Material Design 3 (M3) Compose Multiplatform design system: Color palettes (Islamic teal, warm gold), dynamic dark/light themes, typography scales (Inter, Outfit, Amiri Arabic), shapes, and icon tokens.  
**Depends on:** Phase 0 Workspace, Phase 2 Security Baseline Prerequisites  
**Consumed by:** All Phase 4, Phase 5, Phase 6, Phase 8, and Phase 10 feature implementations  
**Source of truth:** `NoorHeroes/core/core-designsystem/CORE_DESIGNSYSTEM_INSTRUCTIONS.md`; `NoorHeroes_Consolidated_Execution_Blueprint.md` §4  

---

## 1. Objective and Purpose
Establish the single authoritative visual design language for the NoorHeroes mobile application across Android and iOS, enforcing the visual system defined in PRDs and 562 visual screen designs.

## 2. Technical Requirements
- Colors: Deep Teal (`#0F5E5E`), Warm Gold (`#F0B429`), Soft Cream (`#FDFBF7`), Coral Alert (`#E05D5D`), Midnight Navy (`#0A192F` dark theme).
- Typography: Inter for clean UI copy, Outfit for friendly child-facing headers, Amiri for reverent Arabic script rendering.
- Shapes: Soft rounded corners (`RoundedCornerShape(16.dp)` standard, `24.dp` for hero cards, pill shapes for interactive chips).
- Theme: `NoorTheme` composable providing `LocalNoorColors`, `LocalNoorTypography`, and `LocalNoorShapes`.

## 3. Technology Stack Preservation
- Compose Multiplatform 1.6+, Material Design 3 (M3).

## 4. Verification and Acceptance Criteria
- [x] Theme previews render consistently in Light and Dark modes.
- [x] RTL layout direction switches Arabic fonts and mirrors directional iconography automatically.

