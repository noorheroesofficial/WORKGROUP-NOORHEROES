# Phase 0 — Monorepo Scaffold & Workspace Structure Verification

`Development_Blueprints.Phase0_Project_Repo_Foundation.Repo.01-monorepo-scaffold-workspace-structure.md`

**Module:** Repo (cross-cutting workspace root)  
**Phase:** 0 — Project & Repository Foundation  
**Status:** ✅ **Implemented & Verified**  
**Depends on:** None (Root Scaffolding)  
**Consumed by:** All subsequent phases (Phase 0 items 02–03, Phase 1 Infrastructure, Phase 2 Backend Foundation, Phase 3 Shared Core Modules, Phase 4–8 Feature Implementations)  
**Source of truth:** `NoorHeroes_Consolidated_Execution_Blueprint.md` §1; `MASTER-README.md`; `.workgroup-root.json`  

---

## 1. Objective and Purpose

Establish and formally verify the canonical multi-platform monorepo workspace structure for NoorHeroes. The workspace integrates three discrete application domains and supporting documentation into a unified development tree:
1. **`NoorHeroes/`** — Kotlin Multiplatform (KMP) mobile application targeting Android (API 26+) and iOS (16.0+), powered by Compose Multiplatform (CMP) and Material Design 3 (M3).
2. **`NoorHeroes-Backend/`** — Asynchronous Python 3.11+ / FastAPI Clean Architecture backend services, SQLAlchemy 2.0 async ORM, Alembic migrations, PostgreSQL 16, and Redis 7.
3. **`noorheroes-admin/`** — Next.js 14 App Router administration and scholar review portal, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query v5, and Zustand.
4. **`Development_Blueprints/` & `PRD_Documents/`** — Authoritative technical specifications, API contracts, domain models, and product requirement documents.
5. **`Screens/`** — Authoritative repository of 562 visual screen designs mapped 1:1 to application components.

---

## 2. Monorepo Directory Layout

```text
WORKGROUP-NOORHEROES/
├── .workgroup-root.json              # Monorepo workspace metadata and environment configuration
├── DEVELOPMENT-RULES.md             # Non-negotiable cross-cutting engineering rules and invariants
├── FAST-API-INSTRUCTIONS.md         # Production-ready FastAPI architecture manual and endpoint register
├── MASTER-README.md                 # System overview, service inventory, and run instructions
├── PROJECT-CONTEXT.md               # High-level architecture context and technology stack decisions
├── NoorHeroes/                      # KMP Mobile Client Application
│   ├── build.gradle.kts             # Root Gradle build configuration
│   ├── settings.gradle.kts          # Module include tree
│   ├── composeApp/                  # Application composition, Koin DI graph, platform main entry points
│   └── core/                        # 14 shared modular libraries
│       ├── core-analytics/          # Analytics event contracts and dispatcher abstraction
│       ├── core-common/             # Shared utilities, Result monad, Dispatchers
│       ├── core-crash/              # Crash reporting abstraction and Crashlytics binding
│       ├── core-data/               # Data layer abstractions, offline sync engines
│       ├── core-database/           # SQLDelight / Room local offline cache
│       ├── core-datastore/          # Encrypted key-value store, Remote Config cache
│       ├── core-designsystem/       # M3 theme, colors, typography, shapes, icons
│       ├── core-logger/             # Kermit structured multiplatform logger
│       ├── core-navigation/         # Voyager / Decompose navigation backstack and type-safe routes
│       ├── core-network/            # Ktor Client, HTTP client engine, auth token interceptors
│       ├── core-notifications/      # Local notification scheduler, FCM / APNs registration
│       ├── core-security/           # Android Keystore / iOS Keychain token storage, credential hasher
│       ├── core-ui/                 # Shared UI components, state machines, shimmer loaders
│       └── kmpplayer/               # Media playback engine for audio stories and recitations
├── NoorHeroes-Backend/              # FastAPI Backend Microservices & API Gateway
│   ├── pyproject.toml               # Poetry dependency management and tool configuration
│   ├── alembic/                     # Reversible database migration scripts
│   ├── src/noorheroes/              # Domain bounded contexts
│   │   ├── core/                    # Security, logging, exceptions, settings, database session
│   │   └── modules/                 # Clean Architecture modules (identity, access_gate, rewards, etc.)
│   └── tests/                       # Unit, integration, architecture, and Testcontainers test suites
├── noorheroes-admin/                # Next.js 14 Web Administration & Scholar Portal
│   ├── package.json                 # Node dependencies and build scripts
│   ├── tsconfig.json                # TypeScript strict configuration
│   ├── src/                         # Next.js App Router application source
│   │   ├── app/                     # Role-scoped routes and layouts
│   │   ├── components/              # shadcn/ui components and feature widgets
│   │   ├── features/                # Bounded feature logic, queries, and mutations
│   │   └── shared/                  # API client, Zustand stores, constants, and utilities
├── PRD_Documents/                   # 37 Feature PRDs, Website Specs, and Asset Prompt Packs
├── Development_Blueprints/          # Detailed technical blueprints per feature and foundation phase
└── Screens/                         # 562 Screen visual designs across Mobile, Admin Web, and Parent Web
```

---

## 3. Workspace Invariants & Boundary Rules

1. **Clean Separation of Concerns:**
   - Client code in `NoorHeroes/` never depends on backend source code directly; communication is strictly over HTTP/WebSocket via the generated OpenAPI contract.
   - Admin code in `noorheroes-admin/` communicates via the admin API router (`/v1/admin/*`) under strict RBAC gating.
   - The Parent Web Portal communicates via allowlisted public endpoints under CORS allowlisting (`account.noorheroes.com`).
2. **Contract-First Development:**
   - Any API change must update the Pydantic schemas in `NoorHeroes-Backend/`, generate the OpenAPI schema, and propagate to frontend TypeScript clients and Ktor models.
3. **Multiplatform Isolation:**
   - Shared business logic, state handling, and domain repositories live in `NoorHeroes/core/` and `composeApp/commonMain`. Platform-specific code (`androidMain`, `iosMain`) is strictly limited to hardware-level integration (Keystore, Audio HAL, Biometrics, Push tokens).

---

## 4. Verification and Acceptance Criteria

- [x] Monorepo directory structure confirmed present and organized according to Clean Architecture boundaries.
- [x] Root configuration files (`.workgroup-root.json`, `DEVELOPMENT-RULES.md`, `MASTER-README.md`) verified.
- [x] All 14 KMP core modules configured and compiling in `NoorHeroes/settings.gradle.kts`.
- [x] Backend FastAPI application structure verified in `NoorHeroes-Backend/src/noorheroes/`.
- [x] Admin Web structure verified in `noorheroes-admin/src/app/`.
