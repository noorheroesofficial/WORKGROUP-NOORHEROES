# Phase 3 — core-network: Architecture & Bootstrap Blueprint

`Development_Blueprints.Phase3_Shared_Core_Modules.KMP.04-core-network-module-bootstrap.md`

**Module:** `core-network` (KMP Android & iOS)  
**Phase:** 3 — Shared/Core Modules  
**Status:** ✅ **Implemented & Verified** (Verified against `NoorHeroes/core/core-network/CORE_NETWORK_INSTRUCTIONS.md`)  
**Description:** Ktor HTTP Client engine (CIO/Darwin), canonical JWT Bearer auth plugin, automatic refresh-token rotation, exponential backoff retry, and distributed tracing correlation ID propagation.  
**Depends on:** Phase 0 Workspace, Phase 2 Security Baseline Prerequisites  
**Consumed by:** All Phase 4, Phase 5, Phase 6, Phase 8, and Phase 10 feature implementations  
**Source of truth:** `NoorHeroes/core/core-network/CORE_NETWORK_INSTRUCTIONS.md`; `NoorHeroes_Consolidated_Execution_Blueprint.md` §4  

---

## 1. Objective and Purpose
Deliver resilient, authenticated, and observable network communication between mobile clients and the FastAPI backend gateway.

## 2. Technical Requirements
- Ktor Client configured with Darwin engine (iOS) and OkHttp/CIO engine (Android).
- Content Negotiation: `kotlinx.serialization.json` with camelCase/snake_case dual support.
- Auth Plugin: Intercepts outgoing requests to inject `Authorization: Bearer <token>`, handles HTTP 401 with atomic refresh rotation via `RefreshTokenService`, denylisting replayed tokens.
- Telemetry: Generates and attaches `X-Correlation-ID` and `X-Device-ID` headers to every request.

## 3. Technology Stack Preservation
- Ktor 2.3+, kotlinx.serialization.

## 4. Verification and Acceptance Criteria
- [x] 401 unauthorized triggers seamless refresh token rotation and retries original request.
- [x] Correlation IDs match between client Ktor logs and backend structlog traces.

