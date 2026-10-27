# NoorHeroes — Workgroup Master Documentation & Cross-Platform Governance

> **Welcome to the NoorHeroes Engineering Workgroup.**  
> This workspace is the unified repository and cross-platform operating system for the entire NoorHeroes product ecosystem.  
> It governs development across the **Backend API**, the **Web Admin & Scholar Portal**, the **Kotlin Multiplatform (Android & iOS) Mobile App**, and the **Parent Web Account Portal**.

---

## 1. Project Overview

### What is NoorHeroes?
**NoorHeroes** is an enterprise-grade, privacy-first, child-safe interactive Islamic educational platform designed for Muslim children aged 3–12, their families, and Islamic educators/scholars. The platform blends gamified storytelling, Arabic & Quranic phonetics with Tajweed coaching, daily Sunnah habits, interactive bedtime audio routines, and faith-affirming quizzes into an engaging digital world.

### Core Problem Solved
Contemporary digital media platforms expose young Muslim children to unvetted user-generated content (UGC), intrusive commercial tracking, behavioral dopamine loops, and ad tracking. NoorHeroes provides:
1. **100% Halal, Scholar-Vetted Content**: Sacred text immutability and pedagogical rigor verified by qualified Islamic scholars.
2. **COPPA / GDPR-K Privacy Hardening**: Strict zero-retention voice/microphone AI processing, ephemeral memory buffers, and granular parent consent gates.
3. **Calm, Emotionally Regulated Gamification**: An append-only double-entry rewards ledger (`rewards_ledger`) with zero disparity between daytime learning and nighttime bedtime audio routines (eliminating bedtime dopamine spikes).
4. **Comprehensive Parental Supervision**: Server-authoritative Parent PIN gates, per-child screen time/learning analytics, device session revocation, and data export/deletion rights.

### Major Workgroup Platforms & Components
* **Backend Core (`NoorHeroes-Backend/`)**: Python 3.12+ modular monolith powered by FastAPI, asynchronous SQLAlchemy 2.0, PostgreSQL 16 (with SQLite testing fallback), Redis 7 (caching, sliding-window rate limiting), Celery background workers, transactional outbox event relay, and Sentry/OpenTelemetry observability.
* **Web Admin & Scholar Portal (`noorheroes-admin/`)**: Enterprise Next.js 16 (App Router) / React 19 web application built with TypeScript, Tailwind CSS, TanStack Query, and Zod. Provides RBAC-controlled CMS authoring, scholar review queues, AI moderation transcript audits, dual-approval (Maker-Checker) queues, and platform telemetry.
* **Mobile Application (`NoorHeroes/`)**: Kotlin Multiplatform (KMP) client with Compose Multiplatform powering native Android and iOS applications with Clean Architecture, MVI presentation, SQLDelight offline persistence, Ktor networking, and Material 3 adaptive design.
* **Public Marketing Web Platform (`noorheroes-website/`)**: High-performance Next.js 15 (App Router) / React 19 web application built with Tailwind CSS v4, Motion (Framer Motion), and Lucide React. Features a 4-language bidirectional i18n engine (EN, AR, UR, HI with LTR/RTL support and font switching), 2D canvas GPU starfield parallax, physics-based swinging fanous lanterns, interactive curriculum explorer, age-level recommendation calculator, scholar trust board, and app download gateway.
* **Parent Web Account Portal (`Screens/Parent Web/` & `PRD_Documents/Parent Web Portal (27)`)**: Planned Next.js self-service web portal enabling parents to manage family subscriptions, connected devices, consent ledgers, and privacy rights.

---

## 2. ⚡ Complete Setup & Clone Guide (Step-by-Step)

The NoorHeroes ecosystem operates on a **multi-repository architecture** where the central workgroup orchestrates architecture, PRDs, blueprints, and cross-platform governance, while 4 independent repositories house the active production codebases.

### 2.1 Prerequisites Checklist

Before setting up the environment, ensure your workstation has the following installed:

| Tool / Runtime | Required Version | Purpose | Verification Command |
| :--- | :--- | :--- | :--- |
| **Git** | `2.40+` | Version control & sub-repo management | `git --version` |
| **Node.js** | `>=18.18.0` (`v20.x` LTS recommended) | Admin portal, public website, and Archify tooling | `node -v` |
| **npm** | `>=9.0.0` | Node package manager | `npm -v` |
| **Python** | `3.12.x` (or `>=3.11`) | Backend API & async services | `python --version` |
| **Docker & Docker Compose** | `24.0+` | Local PostgreSQL 16 & Redis 7 services | `docker compose version` |
| **JDK (Java Development Kit)** | `17+` | Kotlin Multiplatform & Android SDK builds | `javac -version` |
| **Android Studio** | Ladybug (2024.2+) or latest stable | Android emulator, SDK manager & Compose preview | Studio > About |
| **Xcode** *(macOS only)* | `15.0+` | iOS builds & native XCFramework compilation | `xcodebuild -version` |

---

### 2.2 Step 1: Clone the Master Workgroup

Clone the root repository first. This houses all PRDs, technical blueprints, reference screens, changelogs, and unified development tooling:

```bash
git clone https://github.com/noorheroesofficial/WORKGROUP-NOORHEROES.git
cd WORKGROUP-NOORHEROES

# Install root workgroup dependencies (Archify CLI & diagram validators)
npm install
```

---

### 2.3 Step 2: Clone All 4 Platform Repositories

The root [`.gitignore`](.gitignore) is pre-configured to keep each code repository isolated as an autonomous Git working tree. Clone all 4 repositories directly into the root `WORKGROUP-NOORHEROES/` directory:

```bash
# 1. Backend Core (FastAPI / PostgreSQL / Redis)
git clone https://github.com/noorheroesofficial/NoorHeroes-Backend.git

# 2. Web Admin Portal (Next.js 16 / React 19 / TypeScript)
git clone https://github.com/noorheroesofficial/noorheroes-admin.git

# 3. Mobile Client (Kotlin Multiplatform / Compose Multiplatform)
git clone https://github.com/noorheroesofficial/NoorHeroes.git

# 4. Public Web Platform (Next.js 15 / Tailwind CSS v4)
git clone https://github.com/noorheroesofficial/noorheroes-website.git
```

> [!TIP]
> **One-Shot Clone Snippet:**
> ```bash
> # Bash / macOS / Linux:
> for repo in NoorHeroes-Backend noorheroes-admin NoorHeroes noorheroes-website; do
>   git clone https://github.com/noorheroesofficial/$repo.git
> done
> 
> # Windows (PowerShell):
> @("NoorHeroes-Backend", "noorheroes-admin", "NoorHeroes", "noorheroes-website") | ForEach-Object {
>   git clone "https://github.com/noorheroesofficial/$_.git"
> }
> ```

---

### 2.4 Step 3: Setup & Launch Backend API (`NoorHeroes-Backend`)

The backend is a FastAPI modular monolith with 14 bounded contexts, PostgreSQL 16, and Redis 7.

```bash
cd NoorHeroes-Backend

# 1. Create and activate a Python virtual environment
# Windows (PowerShell):
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS / Linux:
python3.12 -m venv .venv
source .venv/bin/activate

# 2. Upgrade pip and install all dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env

# 4. Start local PostgreSQL (port 5432) and Redis (port 6379)
docker-compose up -d postgres redis

# 5. Apply database schema migrations
alembic upgrade head

# 6. Start the FastAPI development server
uvicorn src.noorheroes.main:app --reload --host 0.0.0.0 --port 8000
```

* **Interactive Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc API Reference**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
* **Health Check**: `GET http://localhost:8000/health`

---

### 2.5 Step 4: Setup & Launch Web Admin Portal (`noorheroes-admin`)

The admin portal provides staff RBAC, CMS authoring, dual sign-off queues, and scholar verification.

```bash
# From WORKGROUP-NOORHEROES/ (or cd ../noorheroes-admin)
cd noorheroes-admin

# 1. Install Node dependencies (lockfile compliant)
npm install --legacy-peer-deps

# 2. Configure local environment variables
cp .env.example .env.development

# 3. Launch the Next.js development server
npm run dev
```

* **Admin Portal URL**: [http://localhost:3000](http://localhost:3000)
* **Test Suite**: `npm run test` (Vitest) | `npm run test:e2e` (Playwright)

---

### 2.6 Step 5: Setup & Launch Public Web Platform (`noorheroes-website`)

The public website is the multilingual marketing, curriculum discovery, and PWA download gateway.

```bash
# From WORKGROUP-NOORHEROES/ (or cd ../noorheroes-website)
cd noorheroes-website

# 1. Install Node dependencies
npm install

# 2. Configure local environment variables (optional)
cp .env.example .env.local

# 3. Launch on port 3001 (to prevent conflict with Admin on 3000)
npm run dev -- -p 3001
```

* **Public Web URL**: [http://localhost:3001](http://localhost:3001) *(or [http://localhost:3000](http://localhost:3000) if admin is not running)*
* **Build Check**: `npm run build`

---

### 2.7 Step 6: Build & Test Mobile Application (`NoorHeroes`)

The mobile client is built with Kotlin Multiplatform (KMP) and Compose Multiplatform for Android & iOS.

```bash
# From WORKGROUP-NOORHEROES/ (or cd ../NoorHeroes)
cd NoorHeroes

# 1. Build Android Debug APK
./gradlew :androidApp:assembleDebug

# 2. Run all unit and KMP common tests
./gradlew allTests

# 3. (macOS only) Compile shared iOS XCFramework
./gradlew :shared:assembleXCFramework
```

> [!NOTE]
> For active mobile UI development, open `NoorHeroes/` in **Android Studio Ladybug+**, allow Gradle sync to complete, and run the `:androidApp` target on an Android Emulator (API 34+ recommended).

---

### 2.8 Local Service & Port Allocation Matrix

When running the entire NoorHeroes stack locally on your workstation:

| Service / Platform | Directory | Default Port | Local URL / Endpoint | Purpose |
| :--- | :--- | :---: | :--- | :--- |
| **FastAPI Backend** | `NoorHeroes-Backend/` | `8000` | [http://localhost:8000/docs](http://localhost:8000/docs) | REST API, OpenAPI docs & auth services |
| **Web Admin Portal** | `noorheroes-admin/` | `3000` | [http://localhost:3000](http://localhost:3000) | CMS, scholar review & moderation |
| **Public Website** | `noorheroes-website/` | `3001` | [http://localhost:3001](http://localhost:3001) | Marketing, curriculum & i18n platform |
| **PostgreSQL Database** | Docker | `5432` | `localhost:5432/noorheroes_db` | Primary relational database |
| **Redis Cache** | Docker | `6379` | `localhost:6379/0` | Token blacklist, rate limiter & cache |
| **Mobile App (Android)** | `NoorHeroes/` | - | Android Emulator / Physical Device | Child app & in-app parent dashboard |
| **Mobile App (iOS)** | `NoorHeroes/` | - | iOS Simulator (macOS Xcode) | Child app & in-app parent dashboard |

---

## 3. Workgroup Directory Architecture

```text
WORKGROUP-NOORHEROES/
│
├── README.md                                          # Master Workgroup Entry Point (This Document)
├── PROJECT-CONTEXT.md                                 # Primary Context, System Architecture & Status Reference
├── DEVELOPMENT-RULES.md                               # Strict Operational Invariants & Agent Rulebook
├── NoorHeroes_Consolidated_Execution_Blueprint.md     # Cross-Platform Historical Execution Order & Roadmap
│
├── CHANGELOG/
│   └── CROSS_PLATFORM_CHANGES.md                      # Synchronized Cross-Platform Contract Change Ledger
│
├── PRD_Documents/                                     # Authoritative Product Requirements (37 Features)
│   ├── Admin & Scholar Portal (28-34)/                # Features E28 through E34
│   ├── Child App (1-12)/                              # Features A1 through A12
│   ├── Child App Supporting (13-18)/                  # Features B13 through B18
│   ├── Cross-Cutting System Features (35-37)/         # Features F35 through F37
│   ├── Parent Area In-App (19-26)/                    # Features C19 through C26
│   ├── Parent Web Portal (27)/                        # Feature D27
│   ├── Website Home/                                  # Public website content spec (NoorHeroes_website_content_spec.md)
│   └── App Icon-Banner/                               # Visual brand identity & design prompts
│
├── Development_Blueprints/                            # Per-Feature Technical Implementation Blueprints
│   ├── 00_GAP_ANALYSIS_AND_CONFLICT_RESOLUTION_REGISTER.md # Authoritative Dispute & Discrepancy Resolutions
│   ├── 00_MASTER_SCREEN_MAPPING_AND_SYSTEM_SYNCHRONIZATION.md # 562-Screen Mapping to API & UI States
│   ├── A1_Splash_Auth_Onboarding/ ... F37_Security/   # 37 Feature Module Blueprints (Backend, KMP, Admin)
│   └── Phase0_Repo ... Phase12_Production/            # Repository Foundation & DevOps Phase Blueprints
│
├── Screens/                                           # 562 Visual Screen Specifications & UI States
│   ├── Admin Web/                                     # 220 Admin Screens (01-110) + 7 Ramadan Mode Screens
│   ├── Mobile App/                                    # 296 Mobile Screens across 24 Feature Modules
│   └── Parent Web/                                    # 46 Parent Web Portal Screens (01-11)
│
├── NoorHeroes-Backend/                                # Live Backend Codebase (FastAPI Modular Monolith)
│   ├── MASTER-README.md                               # Authoritative Live Backend Architecture Manual
│   ├── FAST-API-INSTRUCTIONS.md                       # Comprehensive 14-Context Codebase Usage Manual
│   ├── src/noorheroes/                                # Core, Common, Infra, and 14 Bounded Contexts
│   └── tests/                                         # 4,900 Passing Tests (Unit, Service, API, Invariants)
│
├── noorheroes-admin/                                  # Live Web Admin Codebase (Next.js 16 App Router)
│   ├── MASTER-README.md                               # Authoritative Live Admin Portal Architecture Manual
│   ├── NEXT-JS-INSTRUCTIONS.md                        # Component, Hook & Feature Module Technical Guide
│   ├── src/                                           # App Router, Edge Proxy, Shared, and 17 Features
│   └── tests/ & e2e/                                  # Vitest unit tests and Playwright test suites
│
├── noorheroes-website/                                # Live Public Web Codebase (Next.js 15 App Router)
│   ├── README.md                                      # Public Web Platform Overview & Quickstart
│   ├── WEBSITE-INSTRUCTIONS.md                        # Authoritative Technical Manual & Component Rules
│   ├── app/                                           # App Router, Layout, Loading, SEO (Sitemap & Robots)
│   ├── components/                                    # Modular Component Library (Layout, Sections, UI)
│   ├── data/translations/                             # 4-Language Localization Dictionaries (EN, AR, UR, HI)
│   ├── types/                                         # Strict TypeScript Contracts & Translation Schema
│   └── public/                                        # Optimized Media Assets, Icons & PWA Manifest
│
├── NoorHeroes/                                        # Live Mobile Codebase (Kotlin Multiplatform)
│   ├── README.md                                      # Authoritative KMP Architecture & Build Guide
│   ├── core/                                          # 13 Shared Core KMP Modules & Architecture Manuals
│   │   ├── core-analytics/CORE_ANALYTICS_INSTRUCTIONS.md
│   │   ├── core-common/CORE_COMMON_INSTRUCTIONS.md
│   │   ├── core-crash/CORE_CRASH_INSTRUCTIONS.md
│   │   ├── core-data/CORE_DATA_INSTRUCTIONS.md
│   │   ├── core-database/CORE_DATABASE_INSTRUCTIONS.md
│   │   ├── core-datastore/CORE_DATASTORE_INSTRUCTIONS.md
│   │   ├── core-designsystem/CORE_DESIGNSYSTEM_INSTRUCTIONS.md
│   │   ├── core-logger/CORE_LOGGER_INSTRUCTIONS.md
│   │   ├── core-navigation/CORE_NAVIGATION_INSTRUCTIONS.md
│   │   ├── core-network/CORE_NETWORK_INSTRUCTIONS.md
│   │   ├── core-notifications/CORE_NOTIFICATIONS_INSTRUCTIONS.md
│   │   ├── core-security/CORE_SECURITY_INSTRUCTIONS.md
│   │   └── core-ui/CORE_UI_INSTRUCTIONS.md
│   └── feature/                                       # 8 Implemented KMP Compose Feature Modules
│
├── Admin-Agent/                                       # Supporting Admin Agent Knowledge & Runbooks
│   ├── API_DOCUMENTATION.md                           # 230 API Operations Extracted from Live OpenAPI 3.1.0
│   ├── feature-flags-and-testing-guide.md             # Dual Sign-off & Safety Flag Architecture Guide
│   ├── adr/                                           # Architectural Decision Records (Admin Portal)
│   └── runbooks/                                      # Operational Runbooks (Secret Rotation, etc.)
│
└── Backend-Agent/                                     # Supporting Backend Agent Knowledge & Runbooks
    ├── TESTING.md                                     # Backend Test Philosophy (4,900 Tests across 339 Files)
    ├── architecture/                                  # Criteria DSL, Gateway Defense, Rate Limiting Specs
    ├── dua/                                           # Event Contracts & Master Badge Criteria Specs
    ├── adr/                                           # Architectural Decision Records (Backend)
    └── runbooks/                                      # Deployment, Rollback, Reconciliation & Security Runbooks
```

---

## 4. Hierarchy of Authority Matrix

When working across multiple documentation sources and code repositories, all engineering teams and AI coding agents **MUST strictly adhere to the following hierarchy of truth**:

> ### 🏛️ Canonical Cross-Platform Authority Specifications
> - **Live Backend & API Specifications**: [`NoorHeroes-Backend/MASTER-README.md`](NoorHeroes-Backend/MASTER-README.md) and [`FAST-API-INSTRUCTIONS.md`](NoorHeroes-Backend/FAST-API-INSTRUCTIONS.md) are the live backend authority. ([`NoorHeroes_Consolidated_Execution_Blueprint.md`](NoorHeroes_Consolidated_Execution_Blueprint.md) is retained for historical global sequence roadmap context).
> - **Live Admin Portal Specifications**: [`noorheroes-admin/MASTER-README.md`](noorheroes-admin/MASTER-README.md) and [`NEXT-JS-INSTRUCTIONS.md`](noorheroes-admin/NEXT-JS-INSTRUCTIONS.md) are the live web admin authority.
> - **Live Mobile App Specifications**: [`NoorHeroes/README.md`](NoorHeroes/README.md) and the 13 core architecture manuals:
>   - [`NoorHeroes/core/core-analytics/CORE_ANALYTICS_INSTRUCTIONS.md`](NoorHeroes/core/core-analytics/CORE_ANALYTICS_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-common/CORE_COMMON_INSTRUCTIONS.md`](NoorHeroes/core/core-common/CORE_COMMON_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-crash/CORE_CRASH_INSTRUCTIONS.md`](NoorHeroes/core/core-crash/CORE_CRASH_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-data/CORE_DATA_INSTRUCTIONS.md`](NoorHeroes/core/core-data/CORE_DATA_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-database/CORE_DATABASE_INSTRUCTIONS.md`](NoorHeroes/core/core-database/CORE_DATABASE_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-datastore/CORE_DATASTORE_INSTRUCTIONS.md`](NoorHeroes/core/core-datastore/CORE_DATASTORE_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-designsystem/CORE_DESIGNSYSTEM_INSTRUCTIONS.md`](NoorHeroes/core/core-designsystem/CORE_DESIGNSYSTEM_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-logger/CORE_LOGGER_INSTRUCTIONS.md`](NoorHeroes/core/core-logger/CORE_LOGGER_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-navigation/CORE_NAVIGATION_INSTRUCTIONS.md`](NoorHeroes/core/core-navigation/CORE_NAVIGATION_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-network/CORE_NETWORK_INSTRUCTIONS.md`](NoorHeroes/core/core-network/CORE_NETWORK_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-notifications/CORE_NOTIFICATIONS_INSTRUCTIONS.md`](NoorHeroes/core/core-notifications/CORE_NOTIFICATIONS_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-security/CORE_SECURITY_INSTRUCTIONS.md`](NoorHeroes/core/core-security/CORE_SECURITY_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-ui/CORE_UI_INSTRUCTIONS.md`](NoorHeroes/core/core-ui/CORE_UI_INSTRUCTIONS.md)
>   are the live KMP mobile app authority.
> - **Live Public Web Platform Specifications**: [`noorheroes-website/README.md`](noorheroes-website/README.md) and [`noorheroes-website/WEBSITE-INSTRUCTIONS.md`](noorheroes-website/WEBSITE-INSTRUCTIONS.md) are the live public website authority.

| Domain / Question | Primary Source of Truth | Secondary Reference | Prohibited Action |
|---|---|---|---|
| **Product Vision, Business Rules & Acceptance Criteria** | [`PRD_Documents/`](PRD_Documents) (37 Features) | [`Development_Blueprints/`](Development_Blueprints) | Do NOT alter business logic or invent features not in PRDs. |
| **Visual Design, UI Components & Screen States** | [`Screens/`](Screens) (562 Screens) | `00-screen-to-code-visual-blueprint.md` files | Do NOT modify, move, or rename images in `Screens/`. |
| **Architectural Discrepancies & Contract Conflicts** | [`00_GAP_ANALYSIS_AND_CONFLICT_RESOLUTION_REGISTER.md`](Development_Blueprints/00_GAP_ANALYSIS_AND_CONFLICT_RESOLUTION_REGISTER.md) | Workgroup Lead / PRD Author | Do NOT make silent assumptions on conflicting requirements. |
| **Live Backend Implementation & API Contracts** | [`NoorHeroes-Backend/MASTER-README.md`](NoorHeroes-Backend/MASTER-README.md) & [`FAST-API-INSTRUCTIONS.md`](NoorHeroes-Backend/FAST-API-INSTRUCTIONS.md) | `NoorHeroes_Consolidated_Execution_Blueprint.md` (historical roadmap context), `NoorHeroes-Backend/artifacts/openapi.json` | Do NOT bypass domain service authorization in API routers. |
| **Live Web Admin Implementation & RBAC** | [`noorheroes-admin/MASTER-README.md`](noorheroes-admin/MASTER-README.md) & [`NEXT-JS-INSTRUCTIONS.md`](noorheroes-admin/NEXT-JS-INSTRUCTIONS.md) | `Admin-Agent/API_DOCUMENTATION.md` | Do NOT store access tokens in `localStorage` or query DB directly. |
| **Live Mobile App Implementation & KMP Architecture** | [`NoorHeroes/README.md`](NoorHeroes/README.md) and the 13 core architecture manuals: [`NoorHeroes/core/*/CORE_*_INSTRUCTIONS.md`](NoorHeroes/core) | `Development_Blueprints/*/KMP/` | Do NOT write platform-specific code outside designated wrappers. |
| **Live Public Web Platform Implementation** | [`noorheroes-website/README.md`](noorheroes-website/README.md) & [`noorheroes-website/WEBSITE-INSTRUCTIONS.md`](noorheroes-website/WEBSITE-INSTRUCTIONS.md) | [`PRD_Documents/Website Home/NoorHeroes_website_content_spec.md`](PRD_Documents/Website%20Home/NoorHeroes_website_content_spec.md) | Do NOT fabricate marketing quotes or connect directly to persistent databases. |
| **Build Sequence & Cross-Platform Roadmap** | [`NoorHeroes_Consolidated_Execution_Blueprint.md`](NoorHeroes_Consolidated_Execution_Blueprint.md) | Phase 0–12 Foundation Blueprints | Retained for cross-platform sequencing & historical context. |
| **Cross-Platform Change Logging** | [`CHANGELOG/CROSS_PLATFORM_CHANGES.md`](CHANGELOG/CROSS_PLATFORM_CHANGES.md) | Local module git commits | Never introduce breaking cross-platform changes unrecorded. |

---

## 5. Platform Overview

### 4.1 Backend (`NoorHeroes-Backend`)
* **Technology**: Python 3.12+, FastAPI, SQLAlchemy 2.0 (Async), Alembic, PostgreSQL 16, SQLite (CI test engine), Redis 7, Celery 5.3, Cloudflare R2 / S3.
* **Architecture**: Clean Architecture Modular Monolith with 14 Bounded Contexts:
  `identity`, `access_gate`, `bedtime`, `dua`, `content`, `learning`, `rewards`, `subscriptions`, `admin`, `ai_safety`, `feature_flags`, `localization`, `media`, `notifications`.
* **Key Invariants**:
  - Gateway Zero-Business-Authorization: Routers perform zero business authorization; domain services independently re-verify session scope (`verify_child_scope`).
  - Sacred Content Protection: Database engine trigger `fn_prevent_ayah_text_mutation` write-protects Quranic text against direct SQL mutation.
  - Zero Voice Retention: In-memory `EphemeralAudioBuffer` explicitly wipes audio bytes post-inference; zero DB voice columns.
  - Double-Entry Gamification: All XP, Noor Coins, and points are recorded via `rewards_ledger`.
* **Testing**: 4,900 automated tests passing across 339 test modules with 100% pass rate in CI.

### 4.2 Web Admin Portal (`noorheroes-admin`)
* **Technology**: Next.js 16.2.12 App Router, React 19.2.4, TypeScript, Tailwind CSS, TanStack Query v5, Zod, Vitest, Playwright.
* **Architecture**: Zero-database frontend proxy architecture. Consumes backend REST API `/v1`.
* **Key Invariants**:
  - Zero Browser Access-Token Storage: Access tokens reside strictly in volatile memory; refresh tokens in `httpOnly`, `SameSite=Strict` cookies.
  - 2FA Step-Up Elevation: High-risk mutations require fresh TOTP re-authentication (`X-Elevated-Token`).
  - Maker-Checker Dual Sign-off: Safety-critical feature flag changes and PII unmasking require 2 distinct admin approvals.
  - Backend-Driven Localization: UI strings, RTL layout direction, and date formats are resolved dynamically from backend localization payloads.

### 4.3 Mobile Application (`NoorHeroes`)
* **Technology**: Kotlin Multiplatform (KMP), Compose Multiplatform (Android & iOS), SQLDelight, Ktor Client, Koin, Material Design 3.
* **Architecture**: Clean Architecture (`App -> Shared -> Feature -> Core`) with MVI state machines.
* **Key Invariants**:
  - 13 Isolated Core Modules: Governed by their respective `CORE_*_INSTRUCTIONS.md` architectural manuals.
  - Offline-First Sync Queue: Mutating actions queue locally in SQLDelight and synchronize with backend using idempotent replays.
  - Presentation Hint Decoupling: UI honors server-supplied hints (e.g. `celebratory_ui_hint: false` during Bedtime Mode).

### 4.4 Public Marketing & Discovery Web Platform (`noorheroes-website`)
* **Technology**: Next.js 15.2.0 App Router, React 19.0.0, TypeScript 5.8, Tailwind CSS v4.1, Motion 12.23, Lucide React, Google Gen AI SDK (`@google/genai`).
* **Architecture**: Hybrid React Server Components with dynamic code splitting (`next/dynamic`) for interactive sections, 2D HTML5 Canvas particle physics, and CSS-first `@theme` design tokens.
* **Key Invariants**:
  - Grounded Marketing Claims: Every product feature, pedagogical claim, and safety guarantee traces directly to Features A.1–F.37; unconfirmed items are explicitly flagged `[PLACEHOLDER — NEEDS INPUT]`.
  - Zero Direct Database Access: Presentation and static generation layer with zero database connections or server-side ORMs.
  - Multilingual LTR/RTL Parity: Full bidirectional support across English, Arabic, Urdu, and Hindi with dynamic font pairing (`DM Sans`, `Playfair Display`, `Amiri`).
  - Calm Motion & Anti-Dark Patterns: Strictly no fake urgency timers, countdown tickers, or manipulative dark patterns; full `prefers-reduced-motion` compliance.
  - COPPA/GDPR-K Aligned Privacy: Zero commercial advertising tracking pixels, zero persistent tracking cookies.

### 4.5 Parent Web Portal (Planned)
* **Technology**: Next.js App Router (TypeScript, Tailwind CSS, TanStack Query).
* **Scope**: 46 visual screens (`Screens/Parent Web/`) covering Account & Security, Connected Devices, Subscriptions & Invoices, Consent & Privacy, Data Export, and Account Deletion.
* **Status**: Fully specified in PRD D27 and Development Blueprints; repository initialization pending.

---

## 6. Universal AI Agent Workflow

Future AI agents joining this Workgroup must strictly follow this 10-step lifecycle:

```text
[Step 1: Ingest Workgroup Operating System]
    ├── Read README.md (Hierarchy of authority & platform layout)
    ├── Read PROJECT-CONTEXT.md (System models, APIs, and current implementation status)
    └── Read DEVELOPMENT-RULES.md (Operational constraints, security rules & invariants)
                   │
                   ▼
[Step 2: Retrieve Authoritative Requirements]
    ├── Locate target feature in PRD_Documents/ (Understand business rules & acceptance criteria)
    └── Review relevant blueprint in Development_Blueprints/
                   │
                   ▼
[Step 3: Inspect Visual Assets & Screen Clusters]
    ├── Inspect all images in target Screens/ folder collectively (Multi-Image Screen Cluster Rule)
    └── Identify all 5 UI states: Loading, Success/Populated, Empty, Error with retry, Action Mutation
                   │
                   ▼
[Step 4: Cross-Reference Conflict Register]
    └── Check Development_Blueprints/00_GAP_ANALYSIS_AND_CONFLICT_RESOLUTION_REGISTER.md
                   │
                   ▼
[Step 5: Inspect Existing Codebases]
    ├── Backend: NoorHeroes-Backend/ (Check routes, schemas, models, services)
    ├── Web Admin: noorheroes-admin/ (Check components, hooks, api layer)
    ├── Mobile: NoorHeroes/ (Check core modules, KMP features, SQLDelight queries)
    └── Public Web: noorheroes-website/ (Check routes, components, translations, styles)
                   │
                   ▼
[Step 6: Perform Cross-Platform Impact Analysis]
    └── Evaluate impact on API contracts, Mobile app, Web Admin, Public Web, DB migrations & Auth
                   │
                   ▼
[Step 7: Propose Technical Implementation Plan]
    └── Identify changes, file paths, test commands, and open design questions
                   │
                   ▼
[Step 8: Implement with Architectural Purity]
    ├── Follow DDD bounded contexts & Clean Architecture
    ├── Never invent endpoints, database columns, or unvetted business rules
    └── Strictly enforce non-bypassable security invariants
                   │
                   ▼
[Step 9: Validate & Execute Test Suites]
    ├── Run automated test suites (Pytest, Vitest, Playwright, Gradle)
    └── Verify architectural invariant and lint gates
                   │
                   ▼
[Step 10: Synchronize Cross-Platform Changelog]
    └── Record any contract modifications in CHANGELOG/CROSS_PLATFORM_CHANGES.md
```

---

## 7. Important Governance References

Before making any modifications in this Workgroup, consult the core governance files:
* 📄 [`PROJECT-CONTEXT.md`](PROJECT-CONTEXT.md) — Comprehensive technical, product, API, and implementation context.
* 🛡 [`DEVELOPMENT-RULES.md`](DEVELOPMENT-RULES.md) — Mandatory operational constraints, security rules, and invariants.
* 📝 [`CHANGELOG/CROSS_PLATFORM_CHANGES.md`](CHANGELOG/CROSS_PLATFORM_CHANGES.md) — Ledger of all cross-platform and contract changes.

---

## 8. Current Project Status (Verified Evidence Baseline)

| Component | Repository / Path | Architecture / Framework | Implemented Status | Verification Evidence |
|---|---|---|---|---|
| **Backend Core** | `NoorHeroes-Backend/` | FastAPI / Async SQLAlchemy 2.0 / PostgreSQL | **Phases 0–6 Implemented** (A1, C19, B16, A11, A3, A4, A5, A6, A7, A8, A9 B01–B05, F37) | 4,900 tests passing across 339 test files; 0 schema drift; full Alembic migrations. |
| **Web Admin Portal** | `noorheroes-admin/` | Next.js 16 App Router / React 19 / TypeScript | **Foundation & 17 Features Implemented** (Auth, 2FA, Users, CMS, Flags, Risk, etc.) | Complete Vitest test suite; edge proxy middleware active; zero token browser storage. |
| **Mobile Application** | `NoorHeroes/` | Kotlin Multiplatform / Compose Multiplatform | **Foundation & 8 Features Implemented** (Onboarding, Home, Learn, Stories, Habits, Rewards, Subscription, Parent Dashboard) | 13 Core instruction manuals active; SQLDelight persistence; MVI state machines. |
| **Public Web Platform** | `noorheroes-website/` | Next.js 15 App Router / React 19 / Tailwind v4 | **Implemented (14 Sections, i18n, PWA)** | Full 4-language LTR/RTL engine active; dynamic SEO, sitemap & robots configured; 0 database dependencies. |
| **Parent Web Portal** | `Screens/Parent Web/` | Next.js App Router (Target) | **Planned / Fully Specified** | 46 UI screens designed; PRD D27 completed; codebase initialization pending. |
| **Historical Roadmap** | `NoorHeroes_Consolidated_Execution_Blueprint.md` | 13-Phase Monorepo Roadmap | **Retained as Roadmap Reference** | 711+ blueprints cross-mapped to 562 screens and 37 PRDs. |
