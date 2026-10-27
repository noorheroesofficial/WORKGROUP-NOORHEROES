# Phase 3 — core-database: Architecture & Bootstrap Blueprint

`Development_Blueprints.Phase3_Shared_Core_Modules.KMP.05-core-database-module-bootstrap.md`

**Module:** `core-database` (KMP Android & iOS)  
**Phase:** 3 — Shared/Core Modules  
**Status:** ✅ **Implemented & Verified** (Verified against `NoorHeroes/core/core-database/CORE_DATABASE_INSTRUCTIONS.md`)  
**Description:** Local offline relational persistence: SQLDelight / Room multiplatform database driver factories, schema migrations, foreign keys, and reactive Flow queries.  
**Depends on:** Phase 0 Workspace, Phase 2 Security Baseline Prerequisites  
**Consumed by:** All Phase 4, Phase 5, Phase 6, Phase 8, and Phase 10 feature implementations  
**Source of truth:** `NoorHeroes/core/core-database/CORE_DATABASE_INSTRUCTIONS.md`; `NoorHeroes_Consolidated_Execution_Blueprint.md` §4  

---

## 1. Objective and Purpose
Provide robust, type-safe local relational storage for offline content caching (stories, duas, quiz progress, habit checkins).

## 2. Technical Requirements
- Database Driver: `AndroidSqliteDriver` on Android, `NativeSqliteDriver` on iOS.
- Tables: `offline_stories`, `offline_duas`, `habit_checkin_cache`, `learning_progress_cache`.
- Reactive Queries: Exposes database tables as Coroutine `Flow` streams emitting on data mutation.
- Schema Migrations: Automatic forward migrations with transactional rollback safety.

## 3. Technology Stack Preservation
- SQLDelight 2.0+ / Room KMP Multiplatform.

## 4. Verification and Acceptance Criteria
- [x] Database CRUD passes on both Android and iOS runtimes.
- [x] Offline queries return cached records in zero-network conditions.

