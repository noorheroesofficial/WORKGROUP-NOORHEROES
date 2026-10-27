# Phase 10 — Load & Performance Testing SLO Validation Blueprint

`Development_Blueprints.Phase10_Security_Performance.Backend.01-load-performance-testing-slo-validation.md`

**Module:** Performance & Scalability Hardening (`tests/performance/` and k6 test suites)  
**Phase:** 10 — Security & Performance Hardening  
**Sequence:** Seq 735  
**Status:** 🟡 **Pending Load Suite Execution**  
**Depends on:** Phase 9 Testing & Quality Hardening, Phase 1 Infra Staging Environment  
**Consumed by:** Phase 12 Production Readiness & GA Gate Checklist  
**Source of truth:** `NoorHeroes_Consolidated_Execution_Blueprint.md` §11; `FAST-API-INSTRUCTIONS.md` §14  

---

## 1. Objective and Purpose
Validate platform Non-Functional Requirements (NFRs) and Service Level Objectives (SLOs) under realistic and peak stress conditions prior to General Availability (GA). Proves that the FastAPI backend, PostgreSQL 16 connection pooling, Redis caching, and KMP client synchronization meet latency and concurrency targets without data degradation.

---

## 2. NFR Targets & Service Level Objectives (SLOs)

| Endpoint Category | Traffic Mix | p50 Latency | p95 Latency | p99 Latency | Max Error Rate |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Cached Reads** (`GET /v1/identity/bootstrap`, Content Lists) | 50% | < 30ms | < 80ms | < 150ms | < 0.01% |
| **Database Reads** (Child Progress, Habit Status, Reports) | 30% | < 60ms | < 150ms | < 300ms | < 0.05% |
| **Mutations / Ledger Writes** (Check-in, Quiz Submit, Rewards) | 15% | < 120ms | < 350ms | < 600ms | < 0.05% |
| **Admin Operations** (CMS Search, Moderation Queue) | 5% | < 100ms | < 250ms | < 500ms | < 0.10% |

### 2.2 Concurrency & Stress Capacity Targets
- **Sustained Baseline:** 2,500 concurrent active family sessions.
- **Peak Ramadan / Daily Surge:** 10,000 concurrent active family sessions (simulating Maghrib/Iftar and Bedtime spikes).
- **Stress Breaking Point:** System must gracefully shed load via HTTP 429 without dropping database transactions or corrupting ledger states up to 25,000 concurrent sessions.

---

## 3. Test Suite Implementation

### 3.1 Tooling & Architecture
- **Engine:** `k6` distributed runner deployed in staging cluster via Kubernetes job / Docker container.
- **Harness Scripts:**
  - `tests/performance/scenarios/browse_and_read.js`: Simulates child reading stories, browsing Quran surahs, checking daily habits.
  - `tests/performance/scenarios/quiz_and_reward.js`: Simulates high-frequency quiz submissions and double-entry reward ledger writes with unique client idempotency keys.
  - `tests/performance/scenarios/ramadan_surge.js`: Simulates 10k users hitting campaign status and countdown simultaneously.

### 3.2 Key Verification Invariants
1. **Connection Pool Stability:** PostgreSQL `max_connections` (100) and SQLAlchemy async pool (`pool_size=20`, `max_overflow=10`) must not experience starvation or pool exhaustion timeouts (`TimeoutError`).
2. **Redis Memory & Rate Limit Atomicity:** Sliding-window rate limiter keys must expire cleanly with TTLs; Redis memory usage must stay bounded under sustained stress.
3. **Outbox Relay Throughput:** Celery outbox relay worker must drain transactional outbox events at > 500 events/second without lagging behind write volume.

---

## 4. Verification and Acceptance Criteria
- [ ] Sustained load test runs for 60 minutes with 2,500 VUs: 0 connection pool errors, 0 dropped ledger entries.
- [ ] 10k VU spike test achieves p95 read latency < 150ms and write latency < 600ms.
- [ ] Multi-dimensional rate limiter triggers HTTP 429 accurately when quotas are exceeded without affecting legitimate concurrent families.
- [ ] Automated performance report generated and archived in `docs/performance/load-test-report-staging.md`.
