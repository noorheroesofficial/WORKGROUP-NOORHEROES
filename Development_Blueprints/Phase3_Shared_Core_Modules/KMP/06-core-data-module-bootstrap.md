# Phase 3 — core-data: Architecture & Bootstrap Blueprint

`Development_Blueprints.Phase3_Shared_Core_Modules.KMP.06-core-data-module-bootstrap.md`

**Module:** `core-data` (KMP Android & iOS)  
**Phase:** 3 — Shared/Core Modules  
**Status:** ✅ **Implemented & Verified** (Verified against `NoorHeroes/core/core-data/CORE_DATA_INSTRUCTIONS.md`)  
**Description:** Offline-first synchronization architecture: Cache-then-network repository strategy, transactional outbox queue for client mutations, and conflict resolution.  
**Depends on:** Phase 0 Workspace, Phase 2 Security Baseline Prerequisites  
**Consumed by:** All Phase 4, Phase 5, Phase 6, Phase 8, and Phase 10 feature implementations  
**Source of truth:** `NoorHeroes/core/core-data/CORE_DATA_INSTRUCTIONS.md`; `NoorHeroes_Consolidated_Execution_Blueprint.md` §4  

---

## 1. Objective and Purpose
Implement unified data repository orchestration ensuring seamless offline child play with background synchronization when connectivity returns.

## 2. Technical Requirements
- Strategy: Repositories emit locally cached data immediately from `:core:database`, fetch fresh state from `:core:network` in parallel, update local storage, and emit updated state.
- Client Outbox: Offline habit check-ins and quiz completions are written to an append-only `ClientMutationQueue` with monotonic `client_event_id` and replayed on reconnection.
- Conflict Resolution: Server-authoritative state reconciliation with optimistic client-side UI application.

## 3. Technology Stack Preservation
- Kotlin Coroutines Flow, SQLDelight, Ktor.

## 4. Verification and Acceptance Criteria
- [x] Offline mutations replay idempotently upon network reconnection.
- [x] Duplicate `client_event_id` submissions produce zero duplicated rewards.

