# Phase 2 — Backend Foundation: Testing Infrastructure, Root conftest.py & Testcontainers Ephemeral Harness

**Blueprint ID:** `Development_Blueprints.Phase2_Backend_Foundation.Backend.07-testing-infrastructure-conftest-testcontainers.md`  
**Platform:** Backend (`tests/conftest.py`, `tests/factories/`, `tests/architecture/test_testing_infrastructure.py`, `tests/`)  
**Phase:** Phase 2 — Backend Foundation & Security Baseline Prerequisites  
**Global Sequence:** Seq 20  
**Closes:** Phase 2 Item 07 (`Backend.07-testing-infrastructure-conftest-testcontainers.md`) — Testing infrastructure, root `conftest.py`, Testcontainers harness (ephemeral PostgreSQL 16 & Redis 7.2 containers per test session, dynamically allocated host ports, zero port collisions, tmpfs acceleration, transaction-rollback session isolation), autouse dependency override clearing (`_reset_dependency_overrides_after_each_test`), offline Redis & rate-limiter interceptor fixtures (`_mock_redis_rate_limiter`, `_mock_redis_dependency`), server-authoritative clock testing (`FrozenClock`, `test_clock`), synchronous and asynchronous HTTP test client fixtures (`plain_client`, `client_as_parent`, `client_as_child`, `client_as_admin`, `async_client`, `authenticated_*_async_client`, `gateway_bypassed_client`), cryptographic JWT minting test helpers (`mint_parent_jwt`, `mint_child_jwt`, `mint_admin_jwt`), synthetic test data factories (`ChildProfileFactory`, `UserFactory`, `FeatureFlagFactory`, `SubscriptionPlanFactory`), and architectural invariant test coverage (`test_testing_infrastructure.py`) per `NoorHeroes_Consolidated_Execution_Blueprint.md` §3, `FAST-API-INSTRUCTIONS.md` §2/§10/§11/§15/§19/§26, and `MASTER-README.md` §5/§12.  
**Depends on:**  
- `Phase2_Backend_Foundation.Backend.01-fastapi-clean-architecture-bootstrap.md` — Modular monolith layout, core layer scaffolding, base exceptions.  
- `Phase2_Backend_Foundation.Backend.02-db-orm-config-sqlalchemy-alembic.md` — Async SQLAlchemy 2.0 engine, declarative base (`Base`), `TimestampMixin`, and `AsyncSessionLocal`.  
- `Phase2_Backend_Foundation.Backend.03-config-management-pydantic-settings.md` — Type-safe `Settings` singleton, environment tiers (`Environment`).  
- `Phase2_Backend_Foundation.Backend.04-structlog-logging-correlation-ids.md` — Structlog logging, request ID, correlation ID context.  
- `Phase2_Backend_Foundation.Backend.05-exception-handling-domain-error-hierarchy.md` — Closed domain exception hierarchy (`DomainError`).  
- `Phase2_Backend_Foundation.Backend.06-base-repository-service-layer-di.md` — Base repository/service abstractions, session contexts (`ParentSessionContext`, `ChildSessionContext`, `AdminSessionContext`), and `Depends()` DI wiring.  

**Consumed by:**  
- All 11 Bounded Contexts (`identity`, `content`, `learning`, `rewards`, `subscriptions`, `media`, `notifications`, `ai_safety`, `admin`, `localization`, `feature_flags`) for unit, integration, and security tests.  
- CI Pipeline Stage 4 (Unit Tests) and Stage 5 (Integration Tests & Architectural Invariant Gates).  
- Architectural invariant test suites (`tests/architecture/`, `tests/architectural/`).  

**Source Authority:**  
- `FAST-API-INSTRUCTIONS.md` (Zero-Missing Developer Usage Manual & Master Reference §2, §10, §15, §19, §26)  
- `MASTER-README.md` (Authoritative Unified Master Technical Reference §5, §12)  
- `NoorHeroes_Consolidated_Execution_Blueprint.md` §3 (Phase 2 Backend Foundation & Security Baseline Prerequisites Item 20)  
- `NoorHeroes_Final_Development_Prompt.md` §3, §5, §8, §10, §13  

**Status:** Implemented & Verified Baseline (Authoritative Specification)  

---

## 1. Objective and Strategic Purpose

This blueprint establishes the **production-grade testing infrastructure, global test fixtures (`conftest.py`), and ephemeral Testcontainers integration harness** for the NoorHeroes backend platform. Built on **Python 3.12+**, **pytest**, **pytest-asyncio**, **Testcontainers**, **SQLAlchemy 2.0 Async ORM**, **httpx**, and **Pydantic v2**, it guarantees reliable, leak-free, reproducible, and blazing-fast test execution across both local developer inner-loops and CI runners.

The primary architectural objectives are:

1. **Dual-Tier Test Execution Strategy**:
   - **Fast Offline Unit Tests**: Pure in-memory mock fixtures (`mock_db_session`, `_mock_redis_dependency`, `_mock_redis_rate_limiter`, `FrozenClock`, synthetic factories) allowing thousands of unit and architectural tests to execute in seconds without network connectivity or Docker daemon requirements.
   - **Zero-Shared-State Ephemeral Integration Tests (Testcontainers)**: Real PostgreSQL 16 and Redis 7.2 containers provisioned dynamically per test session on random host ports, backed by memory-backed tmpfs RAM volumes for high-speed writes and zero persistent state between runs.
2. **Strict Test Isolation & Zero Dependency Override Leakage**:
   - Enforcing an unconditional autouse fixture (`_reset_dependency_overrides_after_each_test`) that automatically invokes `app.dependency_overrides.clear()` after every test function, preventing state leakage across test cases.
3. **Transaction Rollback per Integration Test**:
   - Providing `testcontainer_db_session` which connects to the ephemeral PostgreSQL container, opens a database transaction at test start, and unconditionally rolls back upon test completion. This ensures 100% data isolation between tests with zero table recreation or migration overhead during test execution.
4. **Three-Way Authentication Client Fixtures**:
   - Standardizing synchronous (`TestClient`) and asynchronous (`httpx.AsyncClient`) HTTP client fixtures pre-wired with realistic authentication contexts:
     - Parent mode: `client_as_parent`, `authenticated_parent_async_client`
     - Child mode: `client_as_child`, `authenticated_child_async_client`
     - Admin mode: `client_as_admin`, `authenticated_admin_async_client`
     - Gateway bypass: `gateway_bypassed_client` (for domain-level authorization verification)
5. **Cryptographic JWT Minting Helpers**:
   - Providing canonical token minting functions (`mint_parent_jwt`, `mint_child_jwt`, `mint_admin_jwt`) that construct 100% valid tokens signed with the active test key, enforcing audience separation (`noorheroes-app` vs `noorheroes-admin`) and session mode consistency.
6. **Server-Authoritative Deterministic Clock Mocking**:
   - Providing `frozen_clock` and `test_clock` fixtures backed by `FrozenClock` with `advance()` capabilities, allowing tests to manipulate time deterministically for token expiration, OTP verification, daily usage limit resets, and soft-delete timestamp verification.
7. **COPPA-Compliant Synthetic Test Data Factories**:
   - Establishing modular test data factories (`ChildProfileFactory`, `UserFactory`, `FeatureFlagFactory`, `SubscriptionPlanFactory`) generating synthetic, anonymized test fixtures with sortable ULIDs and zero hardcoded production credentials.
8. **Automated Architectural Invariant Verification**:
   - Backing testing conventions with automated static analysis tests (`tests/architecture/test_testing_infrastructure.py`) verifying dependency cleanup, token schema adherence, factory model stability, and zero hardcoded fixed database ports.

---

## 2. Scope and Architectural Requirements

### 2.1 In Scope

- **Root Pytest Configuration (`tests/conftest.py`)**:
  - Global pytest hook `pytest_configure` registering custom markers (`integration`, `real_redis`, `real_rate_limiter`, `architectural`, `testcontainers`).
  - Autouse fixture `_reset_dependency_overrides_after_each_test` clearing FastAPI dependency overrides.
  - Autouse fixture `_mock_redis_rate_limiter` mocking rate-limiter tokens unless marked `@pytest.mark.real_rate_limiter`.
  - Autouse fixture `_mock_redis_dependency` intercepting Redis client instantiation unless marked `@pytest.mark.real_redis` or `@pytest.mark.integration`.
  - Database mock fixture `mock_db_session` supplying full async session interface.
  - Deterministic clock fixtures `frozen_clock` and `test_clock` overriding `get_clock`.
  - Session context stubs `fake_parent_context`, `fake_child_context`, `fake_admin_context`.
  - JWT minting helpers `mint_parent_jwt`, `mint_child_jwt`, `mint_admin_jwt`.
  - Synchronous HTTP test clients `plain_client`, `client_as_parent`, `client_as_child`, `client_as_admin`.
  - Asynchronous HTTP test clients `async_client`, `authenticated_parent_async_client`, `authenticated_child_async_client`, `authenticated_admin_async_client`, `gateway_bypassed_client`.
  - Ephemeral Testcontainers fixtures `postgres_container`, `redis_container`, `testcontainer_db_engine`, `testcontainer_db_session`, `testcontainer_redis_client` with graceful Docker availability checks.
- **Synthetic Test Data Factories (`tests/factories/`)**:
  - `ChildProfileFactory`: Generates `ChildProfile` domain and ORM models with 26-char ULIDs.
  - `UserFactory`: Generates `User` ORM entities with Argon2id hashed passwords.
  - `FeatureFlagFactory`: Generates `FeatureFlagOrm`, `FeatureFlagEnvironmentStateOrm`, and `FeatureFlagApprovalOrm` records.
  - `SubscriptionPlanFactory`: Generates `SubscriptionPlan` tier records.
  - `__init__.py`: Consolidated factory export package.
- **Architectural & Invariant Verification Suite (`tests/architecture/test_testing_infrastructure.py`)**:
  - Test suite validating clean-slate isolation, JWT minting invariants, clock determinism, factory integrity, and port independence.
- **Dependency & Tooling Configuration**:
  - `pyproject.toml` and `requirements.txt` updated with `testcontainers>=4.0.0` and custom pytest markers.

### 2.2 Explicitly Out of Scope

- **Docker Compose Local Development Stack**: Long-running local developer compose services (`infra/docker-compose.yml`) are managed by Phase 1 (`Infra.03`) and must remain completely decoupled from ephemeral Testcontainers.
- **Staging / Production Deployment Smoke Tests**: Live deployed environment probes (`tests/smoke/test_staging_health.py`) are managed by Phase 1 (`CI_CD.08`).

---

## 3. Architectural Design & Container Lifecycle

### 3.1 Dual-Tier Test Execution Model

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              NOORHEROES TEST SUITE                              │
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │
                   ┌─────────────────────┴─────────────────────┐
                   ▼                                           ▼
┌─────────────────────────────────────┐     ┌─────────────────────────────────────┐
│       TIER 1: FAST UNIT TESTS       │     │     TIER 2: INTEGRATION TESTS       │
│     (Zero External Dependencies)    │     │   (Testcontainers Ephemeral PG/RD)  │
├─────────────────────────────────────┤     ├─────────────────────────────────────┤
│ - Runtime: < 5 seconds full suite   │     │ - Runtime: ~15-30 seconds           │
│ - Mocks: mock_db_session, mock_redis│     │ - Real PostgreSQL 16 (asyncpg)      │
│ - Clock: FrozenClock (deterministic)│     │ - Real Redis 7.2 (redis.asyncio)    │
│ - Clients: TestClient + overrides   │     │ - Dynamic random host ports         │
│ - Target: Domain logic, AST rules,  │     │ - Target: Full query execution,     │
│   schemas, validators, repositories │     │   migrations, transactions, locking │
└─────────────────────────────────────┘     └─────────────────────────────────────┘
```

### 3.2 Ephemeral Testcontainers Lifecycle

For integration tests requiring real PostgreSQL or Redis, Testcontainers manages the container lifecycle per test session:

1. **Session Startup**:
   - `postgres_container` starts `postgres:16-alpine` on an OS-assigned ephemeral host port.
   - `redis_container` starts `redis:7.2-alpine` on an OS-assigned ephemeral host port.
   - `testcontainer_db_engine` connects via `asyncpg` and runs `Base.metadata.create_all` to build the complete relational schema.
2. **Function Test Execution**:
   - `testcontainer_db_session` opens a database connection and starts a transaction.
   - The test executes real queries, updates, and optimistic lock checks against PostgreSQL.
   - At test completion, the fixture unconditionally rolls back the transaction and closes the session, resetting database state in under 5 milliseconds.
3. **Session Teardown**:
   - The database engine executes `Base.metadata.drop_all` and disposes the connection pool.
   - Containers are stopped and destroyed, leaving zero residual volumes on the host.

---

## 4. Detailed Component Implementation & Fixture Contracts

### 4.1 Global Fixtures in `tests/conftest.py`

| Fixture Name | Scope | Autouse | Return Type | Description |
|---|---|---|---|---|
| `_reset_dependency_overrides_after_each_test` | `function` | **Yes** | `None` | Unconditionally runs `app.dependency_overrides.clear()` after every test. |
| `_mock_redis_rate_limiter` | `function` | **Yes** | `AsyncMock` | Intercepts rate-limiting increment calls; bypassed with `@pytest.mark.real_rate_limiter`. |
| `_mock_redis_dependency` | `function` | **Yes** | `AsyncMock` | Intercepts Redis instantiation in `deps.py`; bypassed with `@pytest.mark.real_redis`. |
| `frozen_clock` | `function` | No | `FrozenClock` | Fixed UTC clock (`2026-08-29 12:00:00 UTC`) supporting `.advance(timedelta)`. |
| `test_clock` | `function` | No | `FrozenClock` | Injects `frozen_clock` into `app.dependency_overrides[get_clock]`. |
| `mock_db_session` | `function` | No | `AsyncMock` | Mock `AsyncSession` with commit, rollback, flush, execute, and scalar methods. |
| `fake_parent_context` | `function` | No | `ParentSessionContext` | Standard parent session claims (`fam_test_123`, `parent_user_test`). |
| `fake_child_context` | `function` | No | `ChildSessionContext` | Standard child session claims (`fam_test_123`, `child_test_456`). |
| `fake_admin_context` | `function` | No | `AdminSessionContext` | Standard admin session claims (`admin_test_789`, `super_admin`). |
| `plain_client` | `function` | No | `TestClient` | Synchronous unauthenticated FastAPI client with zero overrides. |
| `client_as_parent` | `function` | No | `TestClient` | Synchronous client pre-configured with parent auth and `mock_db_session`. |
| `client_as_child` | `function` | No | `TestClient` | Synchronous client pre-configured with child auth and `mock_db_session`. |
| `client_as_admin` | `function` | No | `TestClient` | Synchronous client pre-configured with admin auth and `mock_db_session`. |
| `async_client` | `function` | No | `AsyncClient` | Native async `httpx.AsyncClient` wired via `ASGITransport(app=app)`. |
| `authenticated_parent_async_client` | `function` | No | `AsyncClient` | Async client with `Authorization: Bearer <parent_jwt>`. |
| `authenticated_child_async_client` | `function` | No | `AsyncClient` | Async client with `Authorization: Bearer <child_jwt>`. |
| `authenticated_admin_async_client` | `function` | No | `AsyncClient` | Async client with `Authorization: Bearer <admin_jwt>`. |
| `gateway_bypassed_client` | `function` | No | `AsyncClient` | Async client with `X-Gateway-Bypass-Simulation: true`. |
| `postgres_container` | `session` | No | `PostgresContainer` | Ephemeral PostgreSQL 16 container on random host port. |
| `redis_container` | `session` | No | `RedisContainer` | Ephemeral Redis 7.2 container on random host port. |
| `testcontainer_db_engine` | `session` | No | `AsyncEngine` | Session-scoped async engine connected to PostgreSQL container. |
| `testcontainer_db_session` | `function` | No | `AsyncSession` | Transaction-rollback-isolated async database session for integration tests. |
| `testcontainer_redis_client` | `function` | No | `Redis` | Isolated async Redis client connected to ephemeral container. |

---

## 5. Security, Child Privacy & COPPA Compliance in Test Data

All test factories (`tests/factories/`) adhere strictly to the following data safety standards:

1. **Zero Real PII in Test Code**: Real child names, parent phone numbers, email addresses, and production credentials are strictly prohibited. Factories use synthetic placeholders (e.g. `user_1_abcd1234@example.com`, `nickname="Mariam"`).
2. **Deterministic Sortable ULIDs**: All primary keys and correlation IDs use standard 26-character sortable ULIDs generated via `src.noorheroes.common.utils.ids.generate_ulid()`.
3. **Argon2id Mock Hashes**: All test password fields use valid formatted Argon2id hash structures (`$argon2id$v=19$...`) to satisfy authentication format checkers without burning CPU cycles on real password hashing during test runs.

---

## 6. Step-by-Step Developer Guide

### 6.1 Writing Fast Unit Tests with `mock_db_session` and `client_as_parent`

```python
import pytest
from fastapi.testclient import TestClient

def test_get_child_profile_as_parent(client_as_parent: TestClient, mock_db_session):
    # Set up mock query result
    mock_db_session.execute.return_value.scalar_one_or_none.return_value = {
        "id": "01J6A1B2C3D4E5F6G7H8J9K0L1",
        "nickname": "Zayd",
    }
    
    response = client_as_parent.get("/api/v1/identity/children/01J6A1B2C3D4E5F6G7H8J9K0L1")
    assert response.status_code == 200
```

### 6.2 Writing Integration Tests with Testcontainers

```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.noorheroes.modules.identity.models import User

@pytest.mark.integration
@pytest.mark.asyncio
async def test_user_persistence_in_real_postgres(testcontainer_db_session: AsyncSession):
    user = User(
        email="real_pg_user@example.com",
        hashed_password="pw",
        role="parent",
        is_active=True,
    )
    testcontainer_db_session.add(user)
    await testcontainer_db_session.flush()
    
    assert user.id is not None
    # Transaction is automatically rolled back after this test completes
```

### 6.3 Testing Time-Dependent Features with `FrozenClock`

```python
from datetime import timedelta
from src.noorheroes.common.utils.clock import FrozenClock

def test_daily_streak_rollover(test_clock: FrozenClock):
    assert test_clock.now().hour == 12
    
    # Fast forward 24 hours
    test_clock.advance(timedelta(days=1))
    assert test_clock.now().day == 30
```

---

## 7. Master Reference Table for Test Markers & CLI Commands

### 7.1 Pytest Markers

| Marker | Purpose | When to Use |
|---|---|---|
| `@pytest.mark.asyncio` | Enables async test execution via `pytest-asyncio`. | On every async test function (`async def test_*`). |
| `@pytest.mark.integration` | Marks test as an integration test requiring Testcontainers or external resources. | On tests using `testcontainer_db_session` or live network stacks. |
| `@pytest.mark.real_redis` | Bypasses `_mock_redis_dependency` autouse mock. | On Redis integration tests using `testcontainer_redis_client`. |
| `@pytest.mark.real_rate_limiter` | Bypasses `_mock_redis_rate_limiter` autouse mock. | On rate-limiter algorithm and sliding window tests. |
| `@pytest.mark.architectural` | Marks architectural AST and structure invariant tests. | On all tests under `tests/architecture/` and `tests/architectural/`. |

### 7.2 Execution CLI Commands

```bash
# Run all fast unit tests (offline, instant execution)
pytest -m "not integration" -v

# Run full test suite including Testcontainers integration tests
pytest -v

# Run architectural invariant checks only
pytest tests/architecture/ tests/architectural/ -v

# Run with test coverage reporting
pytest --cov=src/noorheroes --cov-report=term-missing
```
