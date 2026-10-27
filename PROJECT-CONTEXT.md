# NoorHeroes — Master Project Context & Cross-Platform Specification

> **Authoritative Technical & Operational Reference for AI Agents and Engineers**  
> This document provides the complete architectural, product, API, data, and implementation state of the **NoorHeroes** platform.  
> Every AI agent entering this Workgroup must read and align with this context before designing or implementing any code across Backend, Web Admin, Mobile App, or Parent Web.

---

## 1. Product Context

### 1.1 Mission & Value Proposition
NoorHeroes is an interactive Islamic educational ecosystem designed for Muslim children aged 4–18+, their families, and Islamic scholars. It bridges high-production-value digital gameplay with rigorous, verified Islamic pedagogy. The platform provides a secure, wholesome alternative to mainstream children's media platforms, completely free from unvetted user-generated content, intrusive commercial behavioral tracking, and dopamine-driven dark patterns.

### 1.2 User Personas
1. **The Child (Ages 4–18+)**:
   - **Early Explorers (Ages 4–6)**: Visual and auditory learners focused on phonetics, Arabic letter tracing, short prophet stories, gentle bedtime audio routines, and daily Sunnah habits.
   - **Curious Adventurers (Ages 6–9)**: Independent readers mastering Tajweed rules, memorizing Du'as, solving daily quizzes, earning Noor Coins, and customizing their personal hero avatar.
   - **Eager Learners (Ages 9–12)**: Intermediate learners engaging with comprehensive Surah skill trees, Islamic historical facts, multi-step quests, and seasonal Ramadan challenges.
   - **Young Scholars (Ages 12–15)**: Pre-teen learners exploring deeper theological context, prophetic biography, and practical moral leadership.
   - **Youth Leaders (Ages 15–18+)**: Advanced youth focusing on foundational Fiqh, community service projects, and mentoring younger siblings.
2. **The Parent**:
   - Manages the family account, creates and customizes child profiles, enforces bedtime sleep timers and screentime caps, views granular learning progress reports, manages subscriptions, and exercises COPPA/GDPR-K privacy rights.
3. **The Islamic Scholar & Curriculum Reviewer**:
   - Vets Islamic narratives, validates Quranic recitation accuracy, inspects AI moral summaries, reviews Du'a citations, and authorizes seasonal moon-sighting overrides for Ramadan.
4. **The Administrative Staff & Safety Operator**:
   - Super Admins, Trust & Safety Moderators, Support Agents, and Billing Ops who monitor service health, review PII unmasking requests, manage feature flags under dual-approval gates, and handle customer recovery workflows.

---

## 2. Platform Context

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

The Workgroup is partitioned into four active software repositories and one fully specified upcoming portal:

```
                                        +---------------------------------------+
                                        |         Unified Identity Layer        |
                                        |   (OAuth 2.0 / TOTP 2FA / Session)    |
                                        +-------------------+-------------------+
                                                            │
         ┌───────────────────────┬──────────────────────────┴──────────────────────────┬────────────────────────┐
         │                       │                                                     │                        │
         ▼                       ▼                                                     ▼                        ▼
+-----------------+     +-----------------+                                   +-----------------+      +-----------------+
| NoorHeroes App  |     | noorheroes-admin|                                   | Parent Web      |      |noorheroes-website|
| (Kotlin KMP)    |     | (Next.js 16)    |                                   | (Planned Next)  |      | (Next.js 15 App)|
|                 |     |                 |                                   |                 |      |                 |
| • Android & iOS |     | • Staff Portal  |                                   | • Family Acct   |      | • Public Portal |
| • Compose Multi |     | • TanStack/Zod  |                                   | • Subscriptions |      | • 4-Lang i18n   |
| • SQLDelight DB |     | • Zero Storage  |                                   | • Privacy Ctr   |      | • Habit Showcase|
+--------+--------+     +--------+--------+                                   +--------+--------+      +--------+--------+
         │                       │                                                     │                        │
         │ HTTPS / REST          │ HTTPS / REST                                        │ HTTPS / REST           │ HTTPS / REST (Public)
         │ Bearer JWT (app)      │ Bearer JWT (admin)                                  │ Bearer JWT (app)       │ Read-Only / Static
         ▼                       ▼                                                     ▼                        ▼
+------------------------------------------------------------------------------------------------------------------------+
|                                              NoorHeroes-Backend (FastAPI)                                              |
|                                                                                                                        |
| • Modular Monolith with 18 Bounded Contexts                                                                             |
| • Async SQLAlchemy 2.0 ORM + Alembic Migrations                                                                        |
| • Redis 7 (Caching, Sliding-Window Rate Limiting, Celery Broker)                                                       |
| • PostgreSQL 16 (Primary DB) with SQLite Test Suite Fallback                                                           |
| • Celery Async Workers + Transactional Outbox Event Relay                                                              |
| • Cloudflare R2 / S3 Media Ingestion & 11-Step Quarantine Pipeline                                                     |
+------------------------------------------------------------------------------------------------------------------------+
```

### 2.1 Backend Core (`NoorHeroes-Backend/`)
* **Primary Responsibility**: Authoritative source of truth for all business logic, persistent data, authentication, subscription entitlements, gamification ledgers, AI safety pipelines, and localized content delivery.
* **Technology Stack**: Python 3.12+, FastAPI, SQLAlchemy 2.0 (Async), Alembic, Pydantic v2 Settings/Schemas, PostgreSQL 16, SQLite (local test harness), Redis 7, Celery 5.3, Cloudflare R2 / S3, Sentry, OpenTelemetry.
* **Key Manuals**:
  - [`NoorHeroes-Backend/MASTER-README.md`](NoorHeroes-Backend/MASTER-README.md) (Authoritative architectural master reference)
  - [`NoorHeroes-Backend/FAST-API-INSTRUCTIONS.md`](NoorHeroes-Backend/FAST-API-INSTRUCTIONS.md) (Granular code manual covering all classes, repositories, and services)

### 2.2 Web Admin Portal (`noorheroes-admin/`)
* **Primary Responsibility**: Internal administration interface for Super Admins, Content Editors, Scholars, Support Agents, and Trust & Safety Officers.
* **Technology Stack**: Next.js 16.2.12 (App Router), React 19.2.4, TypeScript, Tailwind CSS, TanStack Query v5, Zod, Vitest, Playwright.
* **Key Invariants**: Operates strictly as a stateless REST client. Zero direct database access. Zero browser storage of access tokens (volatile memory only). 2FA elevation step-up (`X-Elevated-Token`) for sensitive operations.
* **Key Manuals**:
  - [`noorheroes-admin/MASTER-README.md`](noorheroes-admin/MASTER-README.md) (Authoritative admin portal architecture guide)
  - [`noorheroes-admin/NEXT-JS-INSTRUCTIONS.md`](noorheroes-admin/NEXT-JS-INSTRUCTIONS.md) (Component, Hook, and Repository technical guide)

### 2.3 Mobile Application (`NoorHeroes/`)
* **Primary Responsibility**: Cross-platform native mobile application for children and parents across Android and iOS devices.
* **Technology Stack**: Kotlin Multiplatform (KMP), Compose Multiplatform, SQLDelight, Ktor HTTP Client, Koin Dependency Injection, Material Design 3, Decompose/Voyager navigation.
* **Key Architecture**: Modular Clean Architecture partitioned into `:core` and `:feature`.
* **Key Manuals & Authority**:
  - [`NoorHeroes/README.md`](NoorHeroes/README.md) and the 13 core architecture manuals:
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
    are the live KMP mobile app authority.

### 2.4 Public Marketing & Discovery Web Platform (`noorheroes-website/`)
* **Primary Responsibility**: Official public web portal, interactive curriculum explorer, age-level recommendation calculator, scholar trust/safety verification showcase, and app store download gateway.
* **Technology Stack**: Next.js 15.2.0 (App Router), React 19.0.0, TypeScript 5.8, Tailwind CSS v4.1, Motion 12.23 (Framer Motion), Lucide React, Google Gen AI SDK (`@google/genai`).
* **Key Invariants**: Operates strictly as a presentation and marketing layer. Zero direct database access. 100% grounded marketing claims directly sourced from Features A.1–F.37. Strict anti-dark pattern commitment (zero urgency timers, zero fake scarcity). 4-language bidirectional i18n engine (EN, AR, UR, HI) with full RTL/LTR flipping and typography switching (DM Sans, Playfair Display, Amiri). Zero ad tracking or commercial analytics cookies.
* **Key Manuals**:
  - [`noorheroes-website/README.md`](noorheroes-website/README.md) (Public web platform architecture & quickstart)
  - [`noorheroes-website/WEBSITE-INSTRUCTIONS.md`](noorheroes-website/WEBSITE-INSTRUCTIONS.md) (Authoritative technical instruction manual & component development rules)
  - [`PRD_Documents/Website Home/NoorHeroes_website_content_spec.md`](PRD_Documents/Website%20Home/NoorHeroes_website_content_spec.md) (Content, design & build specification)

### 2.5 Parent Web Portal (Planned)
* **Primary Responsibility**: Lightweight, responsive web portal for parents who prefer desktop management of family billing, connected devices, data exports, and consent audits.
* **Current Status**: Fully specified in PRD D27, 46 screen designs in `Screens/Parent Web/`, and blueprints in `Development_Blueprints/D27_Parent_Web_Account_Portal/`. Code repository initialization pending.

---

## 3. Architecture Context & Invariants

The NoorHeroes system is built upon **eight non-negotiable architectural invariants**:

### 1. Gateway Zero-Business-Authorization Invariant
API routers act strictly as request validation and parameter-forwarding gateways. Routers must never execute business authorization queries or evaluate domain scopes directly. Domain services (`verify_child_scope`, `verify_parent_ownership`, `require_elevated_session`) independently re-verify tokens and entity ownership, guaranteeing that even if a gateway route is misconfigured or bypassed, domain invariants cannot be compromised.

### 2. Sacred Islamic Text Immutability Invariant
Sacred Quranic text (`Ayah.arabic_text_immutable`) is protected against accidental corruption, unauthorized editing, or direct SQL tampering via an active database engine trigger (`fn_prevent_ayah_text_mutation`). Direct SQL `UPDATE` queries on `arabic_text_immutable` raise a fatal database exception. Any updates must follow an immutable new version lifecycle authorized by verified scholars.

### 3. COPPA / GDPR-K Zero Voice Retention Invariant
Child voice recordings submitted for Arabic pronunciation analysis (`POST /v1/learning/recitation`) are held strictly in an in-memory `EphemeralAudioBuffer`. Once inference completes, `explicit_delete()` wipes the buffer from process memory. Raw child voice recordings are **never persisted** to disk, object storage, database tables, or application logs.

### 4. Double-Entry Gamification Ledger Invariant
Child balances (XP, Noor Coins, Points) are managed as an append-only accounting ledger in `rewards_ledger`. Balance balances are derived from or strictly verified against `SUM(amount)`. Balances can never be directly set or overwritten. Manual grants over 500 XP in the Admin Portal require Maker-Checker dual approval.

### 5. Bedtime Presentation Decoupling & Reward Parity Invariant
Audio stories completed during Bedtime Mode (`silent_completion: true`) award byte-for-byte identical XP and Noor Coins as daytime completions, creating identical `RewardLedgerEntry` accounting records. Dopamine-suppression is isolated purely to the presentation layer: the server returns `celebratory_ui_hint: false`, instructing client players to suppress fanfare chimes and confetti in favor of a calming Dua Ending card.

### 6. Zero Browser Token Storage in Admin Invariant
The Admin Web Portal strictly forbids storing access tokens in `localStorage`, `sessionStorage`, or cookies accessible to client-side JavaScript. Access tokens reside solely in volatile JavaScript runtime memory (`auth-token.api.ts`). Refresh tokens are encapsulated in backend-managed `httpOnly`, `SameSite=Strict`, `Secure` cookies.

### 7. Dual-Approval (Maker-Checker) Governance Invariant
Safety-critical configuration changes (feature flags with `safety_relevant: true`, customer PII unmasking, and high-value XP grants) require two distinct authorized administrators (Proposer $\ne$ Approver). Self-approvals are strictly rejected by the backend state machine.

### 8. Public Marketing Grounding & Calm Presentation Invariant
Every marketing statement, curriculum claim, and safety guarantee published on the public website (`noorheroes-website/`) must trace directly to documented features (A.1–F.37) in `PRD_Documents/`. Marketing sections requiring unconfirmed external facts (parent quotes, press coverage, partner logos) MUST be explicitly tagged with `[PLACEHOLDER — NEEDS INPUT]` and never fabricated. The web experience strictly enforces a calm visual aesthetic: zero urgency countdown timers, zero fake social proof counters, and 60 FPS spring animations that strictly respect `prefers-reduced-motion`.

---

## 4. Master Feature Context (37 Core Features & Website Home)

The NoorHeroes product requirements are organized into 37 distinct features across 6 domains, complemented by the public website content specification ([`PRD_Documents/Website Home/NoorHeroes_website_content_spec.md`](PRD_Documents/Website%20Home/NoorHeroes_website_content_spec.md)) serving as the public discovery layer for Features A.1–F.37:

| Module Code | Feature Name | Domain | Primary Responsibilities |
|---|---|---|---|
| **A.1** | Splash, Auth & Onboarding | Child App Core | Remote config bootstrap, OTP auth, Google OAuth, PIN creation, child profile onboarding. |
| **A.2** | Home Dashboard & AI Personalization | Child App Core | Child home feed, daily streak banner, recommended content, time-of-day theme adapts. |
| **A.3** | Stories Module | Child App Core | Episodic interactive moral stories, branching choices, heartbeats, audio/video streaming. |
| **A.4** | Audio & Bedtime Player / Bedtime Mode | Child App Core | Calming bedtime player, sleep timer ceiling, silent rewards, bedtime ritual log. |
| **A.5** | Quran & Arabic Learning | Child App Core | Phonetics, Tajweed DAG skill tree, zero-retention recitation AI, progressive hints, spaced repetition. |
| **A.6** | Dua Learning | Child App Core | Contextual Du'a catalog, audio recitation, mark-as-learned, recall quizzes, master badges. |
| **A.7** | Habit Tracker | Child App Core | Sunnah daily habits, visual progress, streak tracking, parent verification. |
| **A.8** | Daily Quiz Engine | Child App Core | 5-question daily quiz, learn-tab pool integration, timed challenges, effort XP. |
| **A.9** | Skill Tree Mastery Engine | Child App Core | Prerequisite DAG engine, weighted mastery calculation, multi-session verification. |
| **A.10** | Games Module | Child App Core | Halal mini-games reinforcing Arabic vocabulary, Islamic history, and memory puzzles. |
| **A.11** | Rewards System | Child App Core | Append-only ledger, Noor Coins wallet projection, badge library, daily missions, store. |
| **A.12** | Avatar System | Child App Core | 6-layer customizable child avatar (skin, outfit, headwear, eyes, accessory, background). |
| **B.13** | Search & Discovery | Child App Supporting | Full-text and tagged content discovery, age-filtered recommendations, trending topics. |
| **B.14** | Favorites | Child App Supporting | Optimistic favoriting of stories, duas, and audio with withdrawal-resilient state. |
| **B.15** | Offline Downloads & Sync | Child App Supporting | DRM-protected offline media manifests, download policies, opportunistic sync queue. |
| **B.16** | Child Profile | Child App Supporting | Progress aggregation, age tier badge, display locale preference, sibling switching. |
| **B.17** | Notifications (Child-Facing) | Child App Supporting | Encouraging reminder notifications, streak warnings, habit nudges (ad-free, COPPA-safe). |
| **B.18** | Islamic Facts Module | Child App Supporting | Daily bite-sized Islamic facts, Hadith reflections, and shareable family trivia cards. |
| **C.19** | Parent PIN & Biometric Gate | Parent Area In-App | High-friction parent security gate, progressive exponential lockouts, self-serve OTP recovery. |
| **C.20** | Parent Dashboard | Parent Area In-App | Central parent control room: child cards, aggregate activity, quick toggles, alerts. |
| **C.21** | Multi-Child Management | Parent Area In-App | Adding, editing, archiving child profiles; individual age calibrations; sibling PIN locks. |
| **C.22** | Per-Child Reports | Parent Area In-App | Quran mastery progress, streak consistency, screen time analytics, concept-level insights. |
| **C.23** | Parental Controls | Parent Area In-App | Daily time ceilings, bedtime windows, AI microphone toggles, content exclusions. |
| **C.24** | Subscription & Billing | Parent Area In-App | In-App Purchases (Apple IAP, Google Play Billing, Stripe), family tier entitlements. |
| **C.25** | Notifications & Parent Support | Parent Area In-App | Support ticket dispatch, weekly digest configuration, security alert management. |
| **C.26** | Privacy, Consent & Data Rights | Parent Area In-App | COPPA consent ledger, instant "Purge AI History", data export, account deletion request. |
| **D.27** | Parent Web Account Portal | Parent Web Portal | Web-based account management, active device session revocation, invoice downloads. |
| **E.28** | Admin Auth, RBAC & Ops Dashboard | Admin & Scholar | TOTP 2FA admin authentication, granular RBAC scopes, live platform health monitors. |
| **E.29** | Content CMS & Scholar Review | Admin & Scholar | Story/quiz/dua authoring, multi-lingual version history, scholar review & approval queue. |
| **E.30** | AI Moderation Console | Admin & Scholar | AI conversation transcript audit, confidence evaluation harness, blocked topic registry. |
| **E.31** | Engagement Tools Admin Suite | Admin & Scholar | Challenge builders, XP rule editor, badge criteria builder, in-app banner scheduler. |
| **E.32** | User Management & Child Safety | Admin & Scholar | Family account inspection, Maker-Checker PII unmasking queue, support case management. |
| **E.33** | Subscription & Billing Ops | Admin & Scholar | Subscription plan catalog, pricing tiers, payment reconciliation jobs, revenue reports. |
| **E.34** | Localization Management | Admin & Scholar | String table editor, translation coverage dashboard, RTL preview, locale chain rules. |
| **F.35** | AI Layer Microservices | Cross-Cutting | Pronunciation scoring, moral summary generation, conversational guardrails, blocklist filter. |
| **F.36** | Ramadan Mode | Cross-Cutting | Dynamic Hijri calculation, 2-tier scholar moon-sighting overrides, fasting habit tracker. |
| **F.37** | Security Architecture | Cross-Cutting | JWT claim schema, refresh rotation, rate limiting, slow-hash auth, 11-step quarantine upload. |

---

## 5. API Context & Conventions

### 5.1 Protocol Standards
* **Base URL**: `https://api.noorheroes.com/v1` (Local dev: `http://localhost:8000/v1`)
* **Transport**: HTTPS with TLS 1.3 enforced in production.
* **Data Wire Format**: JSON UTF-8. Requests and responses use `camelCase` wire naming with backward-compatible `snake_case` validation aliases supported in backend Pydantic models.

### 5.2 Universal Headers
| Header | Required | Format | Purpose |
|---|---|---|---|
| `Authorization` | Protected routes | `Bearer <jwt_token>` | Authenticates caller identity and claims. |
| `Idempotency-Key` | State-mutating writes | `UUIDv4` string | Prevents duplicate processing on network retries. |
| `X-App-Version` | All client calls | SemVer (e.g. `1.2.0`) | Version gating and remote configuration negotiation. |
| `X-Platform` | All client calls | `ios` \| `android` \| `web` | Telemetry, platform-specific manifests, and routing. |
| `X-Locale` | Client calls | IETF (e.g. `en-US`, `ar-SA`) | Content and error message localization. |
| `X-Device-ID` | Mobile client calls | UUID / Persistent ID | Fraud prevention and sliding-window rate limit tracking. |
| `X-Correlation-ID` | All calls | UUIDv4 | End-to-end request tracing across gateway and workers. |
| `X-Elevated-Token` | Sensitive Admin actions | JWE / Ephemeral token | Confirms fresh 2FA step-up re-authentication. |

### 5.3 Standard Error Envelope
All error responses (`4xx` and `5xx`) adhere strictly to this envelope:

```json
{
  "error": {
    "code": "SPECIFIC_ERROR_ENUM",
    "message": "Human-readable, localized error message.",
    "details": {
      "field": "Optional validation error details or diagnostic context"
    },
    "timestamp": "2026-09-12T05:00:00.000Z",
    "correlation_id": "c73a792c-80a5-4e2b-b992-5b91b9a9d701"
  }
}
```

### 5.4 Keyset Pagination Contract
All high-volume listing endpoints (Stories, Quizzes, Duas, Audit Logs) implement deterministic keyset cursor pagination to guarantee $O(1)$ database execution:
* **Query Parameters**: `cursor` (opaque base64 encoded sort key), `limit` (default: 20, max: 100).
* **Response Contract**:
  ```json
  {
    "items": [...],
    "limit": 20,
    "hasMore": true,
    "nextCursor": "ZXlKaGJHY2lPaUpTVXpVeE5pSXNJbl..."
  }
  ```

---

## 6. Data Context & Entity Relationships

```text
[ ParentAccount ] 1 ──── N [ ChildProfile ]
       │                          │
       │ 1                        │ 1
       ▼                          ▼
[ ParentConsentLedger ]    [ ChildLockConfig ]
       │                          │
       │ 1                        │ 1
       ▼                          ▼
[ ParentEntitlements ]     [ SkillNodeState ] ── N:1 ── [ SkillNode ]
                                  │
                                  ├──── N ── [ LearningAttempt ]
                                  ├──── N ── [ RecitationFeedbackLog ]
                                  ├──── N ── [ DuaProgress ] ── N:1 ── [ Dua ]
                                  ├──── 1 ── [ BedtimeConfig ]
                                  └──── N ── [ RewardsLedger ]
```

### Key Tables & Schema Roles
* **Identity & Access**:
  - `parent_accounts`: Primary billing/family account (email, hashed password, phone, Google ID).
  - `child_profiles`: Child personas (family-scoped, name, birth year, avatar preset, customization JSONB).
  - `child_lock_configurations`: PIN/pattern locks with progressive lockout counters and cooldown timestamps.
  - `parent_consent_ledger`: Immutable COPPA audit trail recording specific consent grants/revocations.
* **Content & Curriculum**:
  - `ayah`: Sacred Quran verses write-protected by the `fn_prevent_ayah_text_mutation` DB trigger.
  - `skill_nodes`: Curriculum DAG nodes across `quran_reading`, `arabic_letters`, `tajweed`, `memorization`.
  - `skill_node_states`: Per-child mastery states (`locked`, `ready`, `learning`, `practicing`, `mastered`, `needs_refresh`).
  - `dua` & `dua_content_version`: Versioned, multi-locale Islamic supplications.
* **Gamification & Rewards**:
  - `rewards_ledger`: Double-entry accounting ledger recording all credit/debit events.
  - `badges` & `child_badges`: Awarded achievements with permanent stickiness guarantees.
* **Administration & Safety**:
  - `admin_accounts`: Internal staff credentials, assigned roles, and TOTP secrets.
  - `unmask_approval_queue`: Maker-Checker approval queue for viewing customer PII.
  - `feature_flags` & `feature_flag_approvals`: Runtime feature flags with dual-sign-off gates.
  - `admin_audit_records`: Immutable append-only audit trail capturing all administrative actions.

---

## 7. UI & Screen Mapping Context

The Workgroup includes **562 screen visual specifications** located in [`Screens/`](Screens):

| Platform | Screen Directory | Total Images | Module Scope |
|---|---|---|---|
| **Admin Web** | `Screens/Admin Web/` | **220** | 01-110 screen flows covering Operations, Incidents, Unmasking, Support, Content CMS, Quiz Builder, Scholar Queue, AI Moderation, Engagement, Billing, Roles, and Localization. |
| **Admin Web** | `Screens/Admin Web/Ramadan Mode/` | **7** | 01-07 Moon sighting overrides, seasonal calendar, and challenge schedules. |
| **Mobile App** | `Screens/Mobile App/` | **296** | 24 modules: Avatar (6), Bedtime Audio (3), Child Management (13), Child Profile (8), Reports (16), Duas (14), Facts (8), Favorites (9), Games (8), Habits (6), Home (15), Learn (11), Notifications (14), Onboarding (13), Parent Area (13), Parental Controls (21), Privacy (14), Quiz Engine (13), Ramadan (21), Rewards (18), Search (5), Stories (14), Subscription (17), Support (9). |
| **Parent Web** | `Screens/Parent Web/` | **46** | 01-11 screen flows: Sign In (OTP), Account Home, Security, Connected Devices, Subscriptions, Privacy, Data Export, Deletion, and Support. |
| **Public Web** | `noorheroes-website/` | **14 Sections** | Next.js 15 marketing & habit discovery platform: Hero (physics lanterns & 2D canvas starfield), WhatIs, Problems, HowItWorks, FeaturesGrid (Quran, Salah, Stories, Duas), WhyChoose, Screenshots, JourneyTimeline (Levels 1–5), Benefits, SafetyPrivacy (Scholar Board), AboutUs, Testimonials & Age Calculator, Searchable FAQ, DownloadCTA. |

---

## 8. Current Implementation Status (Exhaustive Zero-Missing-Gap Matrix)

| Feature Code | Feature / Module Name | Domain | Backend Status (`NoorHeroes-Backend`) | Admin Web Status (`noorheroes-admin`) | Mobile App Status (`NoorHeroes`) | Parent Web Status |
|---|---|---|---|---|---|---|
| **Phase 0** | Monorepo, Linting & Branching | Foundation | ✅ IMPLEMENTED | ✅ IMPLEMENTED | ✅ IMPLEMENTED | N/A |
| **Phase 1** | Infra, Secrets & CI/CD (1–10) | Foundation | ✅ IMPLEMENTED (Stages 1–10) | ✅ IMPLEMENTED | ✅ IMPLEMENTED | N/A |
| **Phase 2** | Backend Clean Architecture | Foundation | ✅ IMPLEMENTED (18 Contexts) | N/A | N/A | N/A |
| **Web.Home** | Public Marketing & Curriculum Explorer | Public Web | ✅ IMPLEMENTED (Public APIs) | N/A | N/A | N/A |
| **A.1** | Splash, Auth & Onboarding | Child App Core | ✅ IMPLEMENTED (B-01–B-09, Spec E28) | ✅ IMPLEMENTED (Auth, Onboarding Views) | ✅ IMPLEMENTED (`feature-onboarding`) | ⏳ PLANNED |
| **A.2** | Home Dashboard & AI Personalization | Child App Core | ⚠️ PARTIALLY IMPLEMENTED (B-01 Feed API & B-02 AI Recommendation & Safety Filter Implemented & Verified; 138 Tests) | ⚠️ PARTIALLY IMPLEMENTED (N-03 Explainability Viewer Backend Live) | ✅ IMPLEMENTED (`feature-home`) | N/A |
| **A.3** | Stories Module | Child App Core | ✅ IMPLEMENTED (B-01–B-15) | ⚠️ PARTIALLY IMPLEMENTED (CMS Views) | ✅ IMPLEMENTED (`feature-stories`) | N/A |
| **A.4** | Audio & Bedtime Player / Bedtime Mode | Child App Core | ✅ IMPLEMENTED (B-01–B-06) | ⚠️ PARTIALLY IMPLEMENTED (Analytics) | ⚠️ PARTIALLY IMPLEMENTED (Audio Core) | N/A |
| **A.5** | Quran & Arabic Learning | Child App Core | ✅ IMPLEMENTED (B-01–B-11) | ⚠️ PARTIALLY IMPLEMENTED (Curriculum) | ✅ IMPLEMENTED (`feature-learn`) | N/A |
| **A.6** | Dua Learning | Child App Core | ✅ IMPLEMENTED (B-01–B-11) | ⚠️ PARTIALLY IMPLEMENTED (CMS Views) | ⚠️ PARTIALLY IMPLEMENTED (Dua Views) | N/A |
| **A.7** | Habit Tracker | Child App Core | ✅ IMPLEMENTED (B-01–B-13) | ⚠️ PARTIALLY IMPLEMENTED (Templates) | ✅ IMPLEMENTED (`feature-habits`) | N/A |
| **A.8** | Daily Quiz Engine | Child App Core | ✅ IMPLEMENTED (B-01–B-08) | ⚠️ PARTIALLY IMPLEMENTED (Quiz Builder)| ⚠️ PARTIALLY IMPLEMENTED (Quiz UI) | N/A |
| **A.9** | Skill Tree Mastery Engine | Child App Core | ✅ IMPLEMENTED (B-01–B-03 Graph, Formula & State Machine) | ⚠️ PARTIALLY IMPLEMENTED (Visualizer) | ✅ IMPLEMENTED (Skill Trees) | N/A |
| **A.10** | Games Module | Child App Core | ✅ IMPLEMENTED (B-01–B-06) | ⚠️ PARTIALLY IMPLEMENTED (Catalog Ops) | ⚠️ PARTIALLY IMPLEMENTED (Mini-games) | N/A |
| **A.11** | Rewards System | Child App Core | ✅ IMPLEMENTED (B-01–B-14) | ⚠️ PARTIALLY IMPLEMENTED (XP Rules) | ✅ IMPLEMENTED (`feature-rewards`) | N/A |
| **A.12** | Avatar System | Child App Core | ✅ IMPLEMENTED (B-01–B-07) | ⚠️ PARTIALLY IMPLEMENTED (Item Catalog)| ⚠️ PARTIALLY IMPLEMENTED (Compositor)| N/A |
| **B.13** | Search & Discovery | Child App Support | ⚠️ PARTIALLY IMPLEMENTED (Indexes) | N/A | ⚠️ PARTIALLY IMPLEMENTED (Search UI) | N/A |
| **B.14** | Favorites | Child App Support | ✅ IMPLEMENTED (`DuaAccessChecker` API)| N/A | ⚠️ PARTIALLY IMPLEMENTED (Bookmark UI)| N/A |
| **B.15** | Offline Downloads & Sync | Child App Support | ✅ IMPLEMENTED (Download Manifests) | ⚠️ PARTIALLY IMPLEMENTED (Health API) | ⚠️ PARTIALLY IMPLEMENTED (Sync Queue) | N/A |
| **B.16** | Child Profile | Child App Support | ✅ IMPLEMENTED (B-01, B-02) | ✅ IMPLEMENTED (Family Management) | ✅ IMPLEMENTED (Profile Pickers) | N/A |
| **B.17** | Notifications (Child-Facing) | Child App Support | ⚠️ PARTIALLY IMPLEMENTED (Dispatch) | ⚠️ PARTIALLY IMPLEMENTED (Templates) | ⚠️ PARTIALLY IMPLEMENTED (Handlers) | N/A |
| **B.18** | Islamic Facts Module | Child App Support | ⚠️ PARTIALLY IMPLEMENTED (Models) | ⚠️ PARTIALLY IMPLEMENTED (CMS) | ⚠️ PARTIALLY IMPLEMENTED (Cards) | N/A |
| **C.19** | Parent PIN & Biometric Gate | Parent Area In-App | ✅ IMPLEMENTED (B-01–B-06) | ✅ IMPLEMENTED (Gate Health Monitor) | ✅ IMPLEMENTED (Security Core Gate) | ⏳ PLANNED |
| **C.20** | Parent Dashboard | Parent Area In-App | ✅ IMPLEMENTED (Aggregated APIs) | N/A | ✅ IMPLEMENTED (`feature-parent-dash`) | ⏳ PLANNED |
| **C.21** | Multi-Child Management | Parent Area In-App | ✅ IMPLEMENTED (Profile APIs) | ✅ IMPLEMENTED (Family Management) | ✅ IMPLEMENTED (Child Switcher) | ⏳ PLANNED |
| **C.22** | Per-Child Reports | Parent Area In-App | ✅ IMPLEMENTED (Quran Learning Report)| N/A | ⚠️ PARTIALLY IMPLEMENTED (Reports UI) | ⏳ PLANNED |
| **C.23** | Parental Controls | Parent Area In-App | ✅ IMPLEMENTED (Bedtime Config APIs) | ⚠️ PARTIALLY IMPLEMENTED (Controls) | ⚠️ PARTIALLY IMPLEMENTED (Settings) | ⏳ PLANNED |
| **C.24** | Subscription & Billing | Parent Area In-App | ⚠️ PARTIALLY IMPLEMENTED (Entitlements)| ⚠️ PARTIALLY IMPLEMENTED (Billing Ops)| ✅ IMPLEMENTED (`feature-sub`) | ⏳ PLANNED |
| **C.25** | Notifications & Parent Support | Parent Area In-App | ⚠️ PARTIALLY IMPLEMENTED (Support API)| ✅ IMPLEMENTED (Support Case Queue) | ⚠️ PARTIALLY IMPLEMENTED (Tickets) | ⏳ PLANNED |
| **C.26** | Privacy, Consent & Data Rights | Parent Area In-App | ✅ IMPLEMENTED (Consent Ledger) | ✅ IMPLEMENTED (Consent Audit Viewer) | ⚠️ PARTIALLY IMPLEMENTED (Consent UI) | ⏳ PLANNED |
| **D.27** | Parent Web Account Portal | Parent Web Portal | ⚠️ PARTIALLY IMPLEMENTED (Auth/Billing)| N/A | N/A | ⏳ PLANNED (46 Screens Designed)|
| **E.28** | Admin Auth, RBAC & Dashboard | Admin & Scholar | ✅ IMPLEMENTED (Spec E28, 2FA Auth) | ✅ IMPLEMENTED (`features/auth`, `dash`) | N/A | N/A |
| **E.29** | Content CMS & Scholar Review | Admin & Scholar | ✅ IMPLEMENTED (B-11, B-12 APIs) | ⚠️ PARTIALLY IMPLEMENTED (`features/cms`)| N/A | N/A |
| **E.30** | AI Moderation Console | Admin & Scholar | ✅ IMPLEMENTED (Safety Logging APIs) | ⚠️ PARTIALLY IMPLEMENTED (`risk-review`)| N/A | N/A |
| **E.31** | Engagement Tools Admin Suite | Admin & Scholar | ✅ IMPLEMENTED (Rewards Admin APIs) | ⚠️ PARTIALLY IMPLEMENTED (XP/Badges) | N/A | N/A |
| **E.32** | User Management & Child Safety | Admin & Scholar | ✅ IMPLEMENTED (Unmask Queue APIs) | ✅ IMPLEMENTED (`features/users`, unmask)| N/A | N/A |
| **E.33** | Subscription Billing Ops | Admin & Scholar | ⚠️ PARTIALLY IMPLEMENTED (Webhooks) | ⚠️ PARTIALLY IMPLEMENTED (Catalog) | N/A | N/A |
| **E.34** | Localization Management | Admin & Scholar | ✅ IMPLEMENTED (Strings API, Locales) | ✅ IMPLEMENTED (`features/localization`) | N/A | N/A |
| **F.35** | AI Layer Microservices | Cross-Cutting | ✅ IMPLEMENTED (Pronunciation/Moral) | ⚠️ PARTIALLY IMPLEMENTED (Harness) | ⚠️ PARTIALLY IMPLEMENTED (KMP Client)| N/A |
| **F.36** | Ramadan Mode | Cross-Cutting | ⚠️ PARTIALLY IMPLEMENTED (Calculation)| ⚠️ PARTIALLY IMPLEMENTED (Overrides) | ⚠️ PARTIALLY IMPLEMENTED (Theme) | ⏳ PLANNED |
| **F.37** | Security Architecture | Cross-Cutting | ✅ IMPLEMENTED (JWT, Rate Limit, Upload)| ✅ IMPLEMENTED (2FA Elevation Step-up)| ✅ IMPLEMENTED (`core-security`) | ⏳ PLANNED |

*(Note: Public Web Platform `noorheroes-website/` is ✅ FULLY IMPLEMENTED with 14 sections, Next.js 15 App Router, React 19, Tailwind CSS v4, Motion, 4-language i18n, and dynamic SEO).*

---

## 9. Known Gaps & Discrepancy Register

The following 13 architectural discrepancies were formally resolved in [`00_GAP_ANALYSIS_AND_CONFLICT_RESOLUTION_REGISTER.md`](Development_Blueprints/00_GAP_ANALYSIS_AND_CONFLICT_RESOLUTION_REGISTER.md) and must be maintained by all agents:

1. **Auth Endpoint Paths**: Clients must call canonical `/v1/identity/auth/otp/*`, not shorthand `/v1/auth/*` (gateway provides 307 rewrite).
2. **Support Nomenclature**: Public clients display user-friendly **"Tickets"** (`ticket_number`), while Admin displays internal **"Support Cases"** (`id`, `priority`, `sla_expires_at`).
3. **Avatar Layering**: `child_profiles` table supports both `avatar_preset_id` fallback and modular `avatar_customization` JSONB (6 visual layers).
4. **Ramadan Mode Overrides**: Tiered resolution: Tier 1 (Scholar moon-sighting manual override) supersedes Tier 2 (Astronomical geolocation calculation).
5. **PII Unmasking Queue**: Zero customer PII displayed by default; requires Maker-Checker dual-approval for a 15-minute time-boxed unmask token.
6. **AI History Instant Purge**: Calling `DELETE /v1/privacy/children/{id}/ai-history` atomically purges records and returns a signed receipt.
7. **Rewards Immutability**: Rewards are append-only double-entry records. Manual grants over 500 XP require Maker-Checker dual sign-off.
8. **Subscription Entitlements**: `parent_entitlements` table decouples client UI from payment gateway specifics (Stripe, Apple IAP, Google Play).
9. **Child Lock Recovery**: No generic "forgot lock" bypass exists. Recovery strictly requires parent PIN verification (`/v1/auth/pin/verify`).
10. **Customer Support Lockout**: Support agents cannot reset parent PINs; they can only re-trigger the standard phone/email OTP verification challenge.
11. **Bedtime Reward Parity**: Daytime and bedtime completions record identical ledger XP; only celebratory fanfare UI is suppressed.
12. **Tajweed Placement Safeguards**: Foundational Tajweed nodes are never skipped in placement checks; un-verified nodes become provisional `ready` and are queued for spaced review.
13. **Recitation vs Practice Separation**: Recitations (`recitation`) are strictly routed to `/v1/learning/recitation` (zero retention); practice attempts (`quiz`, `tracing`, `matching`) use `/v1/learning/attempts` and enforce multi-session holds ($\ge 2$ days).
14. **Web Admin Contract Parity & Canonical Route Prefixes**: All administrative endpoints called by `noorheroes-admin` map to canonical backend routes: `/v1/admin/users`, `/v1/admin/content`, `/v1/localization/countries`, `/v1/localization/currencies`, `/v1/localization/languages`, `/v1/admin/config/remote-config`, `/v1/admin/onboarding/funnel`, `/v1/admin/families` (with audit trail recording and elevated delete), `/v1/admin/audit-logs`, and `/admin/v1/config/consent-version/pending` alias.

---

## 10. Important Technical Decisions (ADR Summary)

* **ADR-0001 (Monorepo & Versioning)**: Trunk-based development using Conventional Commits (`feat:`, `fix:`, `chore:`) and automated SemVer release tags.
* **ADR-0002 (Admin Token Isolation)**: Zero browser storage of JWT access tokens. Tokens reside solely in volatile JavaScript memory.
* **ADR-0003 (Gateway Zero Authorization)**: FastAPI routers perform parameter validation only; domain services independently enforce authorization.
* **ADR-0004 (Slow-Hash Credential Storage)**: Passwords and PINs use Argon2id/Bcrypt; fast hashes (MD5, SHA1, SHA256) are strictly prohibited in credential verification paths.
* **ADR-0005 (Sliding-Window Rate Limiting)**: Multi-dimensional rate limiting via Redis sorted sets protecting auth and AI ingestion endpoints.
* **ADR-0006 (Sacred Text Immutability)**: PostgreSQL engine trigger `fn_prevent_ayah_text_mutation` prevents SQL mutations on Quranic text.
* **ADR-0007 (Zero Voice Retention)**: In-memory ephemeral buffers explicitly wiped post-inference; zero audio columns in persistent databases.
* **ADR-0008 (Website Next.js 15 Hybrid RSC Architecture & Multilingual RTL Engine)**: Public web platform leverages React Server Components for layout/SEO with dynamic client-side splitting for below-the-fold sections, strict CSS-first Tailwind CSS v4 styling, and complete 4-language LTR/RTL bidirectional rendering.
