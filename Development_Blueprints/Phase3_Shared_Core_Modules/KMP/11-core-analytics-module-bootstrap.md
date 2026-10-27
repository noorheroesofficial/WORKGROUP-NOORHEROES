# Phase 3 — core-analytics: Architecture & Bootstrap Blueprint

`Development_Blueprints.Phase3_Shared_Core_Modules.KMP.11-core-analytics-module-bootstrap.md`

**Module:** `core-analytics` (KMP Android & iOS)  
**Phase:** 3 — Shared/Core Modules  
**Status:** ✅ **Implemented & Verified** (Verified against `NoorHeroes/core/core-analytics/CORE_ANALYTICS_INSTRUCTIONS.md`)  
**Description:** Strongly-typed analytics event contract, multiplatform event dispatcher pipeline, and strict COPPA telemetry privacy enforcement.  
**Depends on:** Phase 0 Workspace, Phase 2 Security Baseline Prerequisites  
**Consumed by:** All Phase 4, Phase 5, Phase 6, Phase 8, and Phase 10 feature implementations  
**Source of truth:** `NoorHeroes/core/core-analytics/CORE_ANALYTICS_INSTRUCTIONS.md`; `NoorHeroes_Consolidated_Execution_Blueprint.md` §4  

---

## 1. Objective and Purpose
Deliver consistent product analytics across all features while enforcing strict child privacy guardrails.

## 2. Technical Requirements
- Events: Strongly-typed data classes extending `AnalyticsEvent` (`screen_view`, `story_completed`, `quiz_attempt`, `habit_checkin`).
- Dispatcher: Pipeline routing events to Mixpanel / Firebase Analytics abstractions.
- COPPA Compliance: Strictly forbids collecting advertising IDs, GPS coordinates, or free-form child voice inputs. All child IDs are pseudonymized hashes.

## 3. Technology Stack Preservation
- Multiplatform event contracts.

## 4. Verification and Acceptance Criteria
- [x] Event schema matches PRD Section 1.19 analytics taxonomies.
- [x] Telemetry payload validation blocks unmasked PII.

