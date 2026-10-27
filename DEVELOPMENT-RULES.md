# NoorHeroes — Development Rules & Cross-Platform Operating Invariants

> **Mandatory Operational Rulebook for AI Coding Agents and Software Engineers**  
> Every engineer and AI agent operating in this Workgroup MUST strictly adhere to the rules in this document.  
> Violating these rules introduces architectural drift, security vulnerabilities, or broken contracts across platforms.

---

## 1. Mandatory Pre-Coding Lifecycle

Before authoring, modifying, or deleting any file or database entity, an agent **MUST complete all eight steps in order**:

```text
[Step 1] Ingest Workgroup Operating System
         ├── Read README.md (Understand authority hierarchy & repository layout)
         ├── Read PROJECT-CONTEXT.md (Understand data models, APIs & platform status)
         └── Read DEVELOPMENT-RULES.md (Review operational constraints & security rules)

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

[Step 2] Retrieve Authoritative Requirements
         ├── Read target feature PRD in PRD_Documents/ (Understand exact business rules & acceptance criteria)
         └── Read relevant feature blueprint in Development_Blueprints/

[Step 3] Inspect Screen Visual Clusters
         └── Open and inspect ALL images in target Screens/ folder collectively (Multi-Image Rule)

[Step 4] Check Discrepancy & Conflict Register
         └── Check Development_Blueprints/00_GAP_ANALYSIS_AND_CONFLICT_RESOLUTION_REGISTER.md

[Step 5] Inspect Existing Codebases
         ├── Backend: NoorHeroes-Backend/ (Inspect routers, models, services, migrations)
         ├── Web Admin: noorheroes-admin/ (Inspect features, components, hooks, schemas)
         ├── Mobile: NoorHeroes/ (Inspect core modules, features, SQLDelight queries)
         └── Public Web: noorheroes-website/ (Inspect routes, components, translations, styles)

[Step 6] Conduct Cross-Platform Impact Analysis
         └── Map dependencies across API, Database, Mobile, Web Admin, Public Web, and Security layers

[Step 7] Formulate & Validate Plan
         └── Formulate step-by-step implementation plan ensuring backward compatibility

[Step 8] Execute with Invariant Preservation
         └── Implement changes, execute test suites, and log changes in CHANGELOG/CROSS_PLATFORM_CHANGES.md
```

---

## 2. Anti-Hallucination & "Do Not Guess" Directives

1. **Information Grounding Mandate**:
   - If an endpoint, database field, enum value, or business rule is not documented in `PRD_Documents/`, `Development_Blueprints/`, or active code, **DO NOT INVENT IT**.
   - If a requirement is ambiguous or unspecified, explicitly state:
     ```text
     Unknown / Not documented
     ```
   - Consult the Workgroup Lead or open a recorded issue rather than guessing.

2. **Prohibited Inventions**:
   - **Do NOT invent API endpoints**: Endpoints must adhere to established bounded context namespaces (`/v1/identity/*`, `/v1/learning/*`, `/v1/content/*`, `/v1/admin/*`).
   - **Do NOT invent database columns or relationships**: Schema changes require documented justification and a reversible Alembic migration.
   - **Do NOT invent user roles or permissions**: Roles must belong to the verified RBAC matrix (`superadmin`, `curriculum_editor`, `content_editor`, `ai_ops`, `product_admin`, `compliance_read`, `support`, `trust_safety`).
   - **Do NOT invent UI flows**: Every screen must trace directly to a verified visual specification in `Screens/` or `PRD_Documents/Website Home/`.

---

## 3. Preservation of Existing Architecture

1. **Modular Monolith & Layer Purity (Backend)**:
   - Respect Clean Architecture layer boundaries:
     ```text
     API Router (Thin Gateway) ──> Domain Service (Business Rules & Auth) ──> Repository (Data Access) ──> ORM Model
     ```
   - **Forbidden Cross-Context Direct ORM Joins**: A service in bounded context A must never query ORM tables belonging to bounded context B via direct SQL joins. Inter-context communication must use domain service dependencies, public context interfaces, or transactional outbox events.
   - Routers must contain **zero business authorization logic** (Gateway Zero-Authorization Principle). Domain services independently re-verify permissions (`verify_child_scope`, `require_elevated_session`).

2. **Zero Direct Database Access (Web Admin)**:
   - `noorheroes-admin` is strictly a client consuming the Backend REST API (`/v1`).
   - Adding direct database ORMs (Prisma, Drizzle, TypeORM, SQLAlchemy) into the web admin codebase is **strictly prohibited**.
   - Zero browser storage of access tokens: Tokens must live exclusively in volatile JavaScript runtime memory.

3. **Core Module Boundary Invariance (Mobile KMP)**:
   - `NoorHeroes/` enforces modular Clean Architecture:
     ```text
     :app (Platform Entry) ──> :shared (Integration) ──> :feature (MVI Screens) ──> :core (Infrastructure)
     ```
   - **Live Mobile App Specifications**: [`NoorHeroes/README.md`](NoorHeroes/README.md) and the 13 core architecture manuals:
     - [`NoorHeroes/core/core-analytics/CORE_ANALYTICS_INSTRUCTIONS.md`](NoorHeroes/core/core-analytics/CORE_ANALYTICS_INSTRUCTIONS.md)
     - [`NoorHeroes/core/core-common/CORE_COMMON_INSTRUCTIONS.md`](NoorHeroes/core/core-common/CORE_COMMON_INSTRUCTIONS.md)
     - [`NoorHeroes/core/core-crash/CORE_CRASH_INSTRUCTIONS.md`](NoorHeroes/core/core-crash/CORE_CRASH_INSTRUCTIONS.md)
     - [`NoorHeroes/core/core-data/CORE_DATA_INSTRUCTIONS.md`](NoorHeroes/core/core-data/CORE_DATA_INSTRUCTIONS.md)
     - [`NoorHeroes/core/core-database/CORE_DATABASE_INSTRUCTIONS.md`](NoorHeroes/core/core-database/CORE_DATABASE_INSTRUCTIONS.md)
     - [`NoorHeroes/core/core-datastore/CORE_DATASTORE_INSTRUCTIONS.md`](NoorHeroes/core/core-datastore/CORE_DATASTORE_INSTRUCTIONS.md)
     - [`NoorHeroes/core/core-designsystem/CORE_DESIGNSYSTEM_INSTRUCTIONS.md`](NoorHeroes/core/core-designsystem/CORE_DESIGNSYSTEM_INSTRUCTIONS.md)
     - [`NoorHeroes/core/core-logger/CORE_LOGGER_INSTRUCTIONS.md`](NoorHeroes/core/core-logger/CORE_LOGGER_INSTRUCTIONS.md)
     - [`NoorHeroes/core/core-navigation/CORE_NAVIGATION_INSTRUCTIONS.md`](NoorHeroes/core/core-navigation/CORE_NAVIGATION_INSTRUCTIONS.md)
     - [`NoorHeroes/core/core-network/CORE_NETWORK_INSTRUCTIONS.md`](NoorHeroes/core/core-network/CORE_NETWORK_INSTRUCTIONS.md)
     - [`NoorHeroes/core/core-notifications/CORE_NOTIFICATIONS_INSTRUCTIONS.md`](NoorHeroes/core/core-notifications/CORE_NOTIFICATIONS_INSTRUCTIONS.md)
     - [`NoorHeroes/core/core-security/CORE_SECURITY_INSTRUCTIONS.md`](NoorHeroes/core/core-security/CORE_SECURITY_INSTRUCTIONS.md)
     - [`NoorHeroes/core/core-ui/CORE_UI_INSTRUCTIONS.md`](NoorHeroes/core/core-ui/CORE_UI_INSTRUCTIONS.md)
     are the live KMP mobile app authority. Never bypass core modules with ad-hoc platform code.

4. **Public Web Architecture & Invariants (`noorheroes-website/`)**:
   - **Hybrid RSC & Client Boundaries**: Root layouts and static routes must remain React Server Components. Client components (`'use client'`) must be scoped strictly to interactive leaves (e.g. `AppClient`, `StarDustParticles`, `Header`, `Hero`, `ScrollToButtons`, `Toast`).
   - **Zero Direct Database Access**: `noorheroes-website` operates strictly as a presentation and marketing layer. Direct database ORMs (Prisma, Drizzle, SQLAlchemy) and direct DB connections are **strictly prohibited**.
   - **Strict Multilingual Bidirectional Parity**: All layouts and components must support both LTR (`en`, `hi`) and RTL (`ar`, `ur`) directions. Dynamic typography switching (`DM Sans` / `Playfair Display` for Latin/Devanagari, `Amiri` for Arabic/Urdu) must be preserved. Directional icons and progress bars must flip dynamically.
   - **Content Grounding & Anti-Fabrication**: Every product feature, pedagogical claim, and safety guarantee must trace to `PRD_Documents/` (Features A.1–F.37). Unverified claims or testimonials must be flagged `[PLACEHOLDER — NEEDS INPUT]`.
   - **Anti-Dark Pattern & Calm Motion Discipline**: Never implement artificial countdown timers, fake stock or urgency tickers, or pre-checked checkboxes. All animations must run at 60 FPS, avoid dopamine-heavy gamification, and strictly respect `prefers-reduced-motion: reduce`.
   - **Performance & Core Web Vitals**: Maintain Lighthouse $\ge 90$, LCP $< 2.5$s, CLS $< 0.1$. Lazy-load below-the-fold sections via `next/dynamic` with suspense fallbacks.

5. **Architectural Deviation Protocol**:
   If an architectural modification is genuinely necessary:
   1. Document technical rationale and alternatives in an Architectural Decision Record (ADR).
   2. Identify cross-platform impacts on Backend, Mobile, Admin, Public Web, and Database.
   3. Update `PROJECT-CONTEXT.md` and relevant blueprints.
   4. Record the change in `CHANGELOG/CROSS_PLATFORM_CHANGES.md`.

---

## 4. Cross-Platform Synchronization Rules

Any change initiated on one platform must be evaluated across the entire dependency chain:

```text
Backend API / Schema / Feature Change
        │
        ├── 1. API Contract & OpenAPI Specification Update
        │
        ├── 2. Web Admin Impact (Zod schemas, TanStack Query hooks, UI tables)
        │
        ├── 3. Mobile App Impact (SQLDelight cache, Ktor DTOs, MVI State, Offline sync)
        │
        ├── 4. Parent Web Impact (Self-service portals, invoices, consent)
        │
        ├── 5. Public Web Impact (Marketing feature copy, curriculum explorer, pricing parity, app download links)
        │
        ├── 6. Automated Test Suites (FastAPI pytest, Vitest, Playwright, Gradle)
        │
        └── 7. Cross-Platform Change Log (CHANGELOG/CROSS_PLATFORM_CHANGES.md)
```

Never assume a backend change is isolated. Even additive fields can impact bandwidth on low-end mobile devices or cause deserialization errors if schema validators enforce `extra="forbid"`.

---

## 5. API Contract & Evolution Rules

1. **Path Canonicality**:
   - All clients must invoke canonical paths (e.g. `POST /v1/identity/auth/otp/verify`, not shorthand `/v1/auth/*`).
   - Legacy redirects or gateway rewrites are for backward compatibility only and must not be targeted by new code.

2. **Non-Breaking Schema Evolution**:
   - **Adding Fields**: New response fields are permitted only if optional or backward-compatible with older client versions.
   - **Removing or Renaming Fields**: Strictly prohibited without an official 6-month deprecation notice and multi-version phased migration.
   - **Pydantic Validation**: All backend incoming request schemas must use `extra="forbid"` to prevent parameter pollution, while supporting dual-wire `validation_alias` for `camelCase` and `snake_case`.

3. **Breaking Change Declaration**:
   - Any modification that alters required fields, changes HTTP status codes, modifies authentication schemes, or breaks response contracts **MUST be explicitly flagged**:
     ```text
     BREAKING CHANGE: [Description of breaking behavior and migration path]
     ```

4. **State-Mutating Write Idempotency**:
   - Every mutating request (`POST`, `PATCH`, `PUT`) altering persistent resources (purchases, completions, locks, manual grants) must require and validate an `Idempotency-Key` (UUIDv4) header.

---

## 6. Business Logic & Invariant Enforcement Rules

1. **Backend Authoritative Rule**:
   - The backend service is the sole authority for business validation, reward calculations, entitlement verification, and security authorization.
   - Client-side validation in Mobile and Web Admin provides UI feedback only and must never be treated as security enforcement.

2. **Sacred Islamic Content Safeguards**:
   - Quranic text in the database (`Ayah.arabic_text_immutable`) is protected by the PostgreSQL trigger `fn_prevent_ayah_text_mutation`. Never attempt to update Ayah text directly via SQL.
   - AI prompts, moral summaries, and recitation coaching feedback must pass through the `ReligiousJudgmentBlocklistValidator` (forbidding takfir, damnation, or sin-judgment terms across `en`, `ar`, `ur`, `hi`).

3. **COPPA / GDPR-K Privacy & Zero Voice Retention**:
   - In-memory `EphemeralAudioBuffer` must be explicitly wiped post-inference via `explicit_delete()`. Never write audio recordings to disk, S3/R2, or databases.
   - Child PII is strictly protected. Support agents view masked data by default and cannot access unmasked PII without Maker-Checker dual approval.

4. **Double-Entry Gamification Ledger**:
   - All XP, Noor Coins, and points must be recorded as ledger events in `rewards_ledger`.
   - Standard daytime completions and bedtime silent completions (`silent_completion: true`) must create byte-for-byte identical accounting records. Presentation suppression is handled solely via `celebratory_ui_hint: false`.

5. **Dual-Sign-Off (Maker-Checker) Rules**:
   - Actions classified as `safety_relevant: true` (modifying child safety flags, PII unmasking, or manual XP grants > 500) require two distinct administrators.
   - Self-approval is structurally prohibited.

---

## 7. Screen & UI Implementation Rules

1. **Multi-Image Screen Cluster Rule (CRITICAL)**:
   - When a screen or user flow is represented by multiple screenshots in `Screens/` (e.g. `28-Story Editor-01.png` to `14.png`, `04-Account & Security-01.png` to `09.png`):
     > **MANDATORY**: Agents MUST inspect ALL images in that cluster collectively before writing code.
     > Never implement a screen based on a single image. Synthesize initial layout, active inputs, validation states, modals, and edge cases into a single cohesive component and ViewModel.

2. **Universal 5 UI States Requirement**:
   Every frontend and mobile screen must implement five distinct UI states:
   1. **Loading State**: Shimmer or skeleton loaders matching the exact card/table layout.
   2. **Success / Populated State**: Full data binding with responsive wrapping and fluid typography.
   3. **Empty State**: Custom themed illustration, explanatory message, and primary CTA.
   4. **Error State**: Non-blocking toast or full-screen card with localized message and "Retry" action.
   5. **Action Mutation Loading**: Disabled buttons with embedded spinners and debounce protection.

3. **Backend-Driven Localization**:
   - UI strings must be resolved from backend localization payloads or string tables.
   - RTL layout mirroring must be supported and previewed for Arabic and Urdu.

---

## 8. Cross-Platform Change Logging

Every meaningful change affecting cross-platform contracts must be appended to [`CHANGELOG/CROSS_PLATFORM_CHANGES.md`](CHANGELOG/CROSS_PLATFORM_CHANGES.md).

### Trigger Criteria for Changelog Entries:
* Modifying, adding, or deprecating an API endpoint or DTO schema.
* Adding or modifying database tables, columns, or Alembic migrations.
* Modifying authentication, session, or RBAC permission scopes.
* Altering shared business rules, calculation algorithms, or gamification ledger rules.
* Modifying cross-context domain events dispatched through the transactional outbox.

---

## 9. Universal Cross-Platform Portability & Dynamic Root Resolution Invariants

To guarantee that `WORKGROUP-NOORHEROES` remains 100% portable when copied or moved to any computer, user account, drive letter, or filesystem across **Windows**, **Linux**, and **macOS**:

1. **Zero Hardcoded Machine Paths**:
   - Never embed absolute machine paths (e.g. `C:\Users\...`, `/Users/...`, `/home/...`, `file:///...`) in source code, scripts, documentation, or configuration.
   - Never assume a specific drive letter or home directory.

2. **Immutable Root Marker (`.workgroup-root`)**:
   - The directory containing `.workgroup-root` and `.workgroup-root.json` is the canonical architectural root of the workgroup.
   - All tools and runtime utilities dynamically ascend the directory tree from `__file__` / `import.meta.url` / `PSScriptRoot` / `BASH_SOURCE[0]` to locate this marker.
   - An optional `WORKGROUP_ROOT` environment variable can override root discovery when explicitly provided by container or CI environments.

3. **Standardized Native Path Resolution Utilities**:
   - **Python**: Use `noorheroes.core.workgroup` (or `tools/workgroup_path.py`) with `pathlib.Path`.
     ```python
     from noorheroes.core.workgroup import get_workgroup_root, resolve_workgroup_path
     spec_file = resolve_workgroup_path("PRD_Documents", "Feature_A1.md")
     ```
   - **Node.js / TypeScript**: Use `src/lib/workgroup-path.ts` or `tools/workgroup-path.mjs` with `node:path`.
     ```typescript
     import { getWorkgroupRoot, resolveWorkgroupPath } from '@/lib/workgroup-path';
     const backendDir = resolveWorkgroupPath('NoorHeroes-Backend');
     ```
   - **Shell / Automation**: Use `tools/workgroup-root.sh` (Linux/macOS) and `tools/workgroup-root.ps1` (Windows/PowerShell).

4. **Portable Markdown Documentation Links**:
   - All markdown links must use standard POSIX relative paths (`../`, `./`, or `path/to/file.md`).
   - Never use root-relative links with leading slashes (`/NoorHeroes/...`), which resolve to Windows drive roots (`C:\NoorHeroes\...`) and break in offline viewers.
   - Never use `file:///` URLs with machine-specific paths.

