# NoorHeroes Gap Analysis & Conflict Resolution Register

> ### 🏛️ Canonical Cross-Platform Authority Specifications
> - **Live Backend & API Specifications**: [`NoorHeroes-Backend/MASTER-README.md`](../NoorHeroes-Backend/MASTER-README.md) and [`FAST-API-INSTRUCTIONS.md`](../NoorHeroes-Backend/FAST-API-INSTRUCTIONS.md) are the live backend authority. ([`NoorHeroes_Consolidated_Execution_Blueprint.md`](../NoorHeroes_Consolidated_Execution_Blueprint.md) is retained for historical global sequence roadmap context).
> - **Live Admin Portal Specifications**: [`noorheroes-admin/MASTER-README.md`](../noorheroes-admin/MASTER-README.md) and [`NEXT-JS-INSTRUCTIONS.md`](../noorheroes-admin/NEXT-JS-INSTRUCTIONS.md) are the live web admin authority.
> - **Live Mobile App Specifications**: [`NoorHeroes/README.md`](../NoorHeroes/README.md) and the 13 core architecture manuals:
>   - [`NoorHeroes/core/core-analytics/CORE_ANALYTICS_INSTRUCTIONS.md`](../NoorHeroes/core/core-analytics/CORE_ANALYTICS_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-common/CORE_COMMON_INSTRUCTIONS.md`](../NoorHeroes/core/core-common/CORE_COMMON_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-crash/CORE_CRASH_INSTRUCTIONS.md`](../NoorHeroes/core/core-crash/CORE_CRASH_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-data/CORE_DATA_INSTRUCTIONS.md`](../NoorHeroes/core/core-data/CORE_DATA_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-database/CORE_DATABASE_INSTRUCTIONS.md`](../NoorHeroes/core/core-database/CORE_DATABASE_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-datastore/CORE_DATASTORE_INSTRUCTIONS.md`](../NoorHeroes/core/core-datastore/CORE_DATASTORE_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-designsystem/CORE_DESIGNSYSTEM_INSTRUCTIONS.md`](../NoorHeroes/core/core-designsystem/CORE_DESIGNSYSTEM_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-logger/CORE_LOGGER_INSTRUCTIONS.md`](../NoorHeroes/core/core-logger/CORE_LOGGER_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-navigation/CORE_NAVIGATION_INSTRUCTIONS.md`](../NoorHeroes/core/core-navigation/CORE_NAVIGATION_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-network/CORE_NETWORK_INSTRUCTIONS.md`](../NoorHeroes/core/core-network/CORE_NETWORK_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-notifications/CORE_NOTIFICATIONS_INSTRUCTIONS.md`](../NoorHeroes/core/core-notifications/CORE_NOTIFICATIONS_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-security/CORE_SECURITY_INSTRUCTIONS.md`](../NoorHeroes/core/core-security/CORE_SECURITY_INSTRUCTIONS.md)
>   - [`NoorHeroes/core/core-ui/CORE_UI_INSTRUCTIONS.md`](../NoorHeroes/core/core-ui/CORE_UI_INSTRUCTIONS.md)
>   are the live KMP mobile app authority.

## 1. Purpose & Authority
This register documents all identified architectural discrepancies, contract variances, missing backend endpoints, data field gaps, and UX edge cases across:
- **Product Requirement Documents (PRDs)** (`PRD_Documents/`)
- **Development Blueprints** (`Development_Blueprints/`)
- **Screen Visual Designs** (`Screens/`)
- **Consolidated Execution Blueprint** (`NoorHeroes_Consolidated_Execution_Blueprint.md`)

It provides **authoritative, backward-compatible resolutions** to guarantee that future AI coding agents and engineering teams implement a 100% synchronized, error-free system without conflicting assumptions.

---

## 2. Master Discrepancy & Resolution Register

### Gap 01: Authentication Endpoint Paths (PRD vs Backend Router)
- **Source A (PRDs)**: PRD A1 and D27 reference legacy shorthand endpoints `POST /v1/auth/otp/request` and `POST /v1/auth/otp/verify`.
- **Source B (Backend Architecture)**: Clean Architecture / FastAPI modular design mounts all identity endpoints under the `identity` router at `POST /v1/identity/auth/otp/request` and `POST /v1/identity/auth/otp/verify`.
- **Impact**: Frontend clients calling shorthand paths would receive 404 Not Found.
- **Authoritative Resolution**: 
  - All clients (KMP Mobile, Next.js Parent Web, Next.js Admin) **MUST call the canonical backend path**: `/v1/identity/auth/otp/request` and `/v1/identity/auth/otp/verify`.
  - For backward compatibility during migration, FastAPI gateway configures a non-breaking 307 Temporary Redirect / URL rewrite from legacy `/v1/auth/*` to `/v1/identity/auth/*`.

---

### Gap 02: Support Tickets vs. Admin Support Cases
- **Source A (Mobile/Parent PRDs B17, C25, D27)**: Refers to user-submitted issues as "Support Tickets" with user-facing ticket IDs (e.g. `TICK-10492`).
- **Source B (Admin PRD E32 & Screens 16, 17)**: Uses "Support Cases" with operator assignment, SLA timers, escalation tiers, and PII masking.
- **Authoritative Resolution**:
  - The domain model explicitly unifies this under a single database entity `support_cases` in PostgreSQL.
  - In the **Parent/Child Mobile & Parent Web UI**, the concept is rendered with user-friendly label **"Ticket"** and public identifier `ticket_number` (e.g. `TICK-8472`).
  - In the **Admin Portal UI**, the concept is rendered as **"Support Case"** with internal UUID `id`, `ticket_number`, `priority`, `sla_expires_at`, `assigned_operator_id`, and `unmask_status`.

---

### Gap 03: Avatar Asset IDs vs. Custom Accessory Compositions
- **Source A (PRD A12)**: Describes simple avatar selection by preset avatar ID (e.g. `avatar_01`).
- **Source B (Screens: Mobile App/Avatar & Admin Web 67-70)**: Shows a modular customization engine with separate layers: `skin_tone`, `eyes`, `outfit`, `headwear`, `accessory`, and `background`.
- **Authoritative Resolution**:
  - The `child_profiles` database table supports both:
    1. `avatar_preset_id` (Nullable String, default preset fallback).
    2. `avatar_customization` (JSONB column storing the modular layer IDs: `{"skin":"st_02", "headwear":"hw_hijab_teal", "outfit":"of_robe_blue", "accessory":"acc_book"}`).
  - Mobile App Compose UI renders using the modular composite layer engine, ensuring full fidelity with `Screens/Mobile App/Avatar/Avatar-01.png` to `06.png`.

---

### Gap 04: Ramadan Mode Activation & Hijri Calculation Overrides
- **Source A (PRD F36)**: Mentions automated Hijri astronomical calculation based on geolocation.
- **Source B (Screens: Admin Web/Ramadan Mode/01-06 & Screens 54, 60)**: Shows manual scholar moon-sighting override controls and regional calendar adjustment offsets (-1, 0, +1 days).
- **Authoritative Resolution**:
  - The backend `HijriCalendarService` operates with **Tiered Resolution**:
    1. **Tier 1 (Authoritative Override)**: Admin/Scholar explicit Moon Sighting Override stored in Redis / Postgres with active date range and region scope.
    2. **Tier 2 (Umm al-Qura / Geolocation Algorithmic Calculation)**: Default fallback when no manual override is published.
  - Mobile app fetches active Ramadan campaign config during `GET /v1/identity/bootstrap` and `GET /v1/ramadan/status`, caching locally for 1 hour with instant push invalidation on override publication.

---

### Gap 05: Dual-Operator PII Unmasking Workflow
- **Source A (Admin PRD E32)**: Mentions support agents viewing customer details.
- **Source B (Screens: Admin Web 09-13, 18-25)**: Explicitly enforces a strict **Maker-Checker / Dual-Approval Unmasking Queue** where Operator A submits a formal justification to unmask PII (phone/email/real name), and Operator B (Supervisor / Data Protection Officer) must approve before a 15-minute time-boxed unmask token is granted.
- **Authoritative Resolution**:
  - The backend enforces strict zero-PII by default for all customer view endpoints.
  - When unmasking is needed, `POST /v1/admin/users/{id}/unmask-requests` is submitted creating an entry in `unmask_approval_queue` (`Screens/Admin Web/10-Unmask Approval Queue.png`).
  - Approval by a distinct authorized operator triggers an audit log and returns an encrypted, ephemeral JWE unmask token valid for exactly 15 minutes.

---

### Gap 06: Child Voice & AI Interaction Consent and Purge
- **Source A (PRDs A2, C26, F35)**: Mentions voice cloning and AI conversation features.
- **Source B (Screens: Mobile App/Privacy/AI History-01 to 03, Consent Log-01 to 06)**: Demonstrates strict COPPA/GDPR-K compliance with per-child consent toggles, immutable consent audit trails, and an explicit "Purge All AI History" instant action.
- **Authoritative Resolution**:
  - All AI conversational interactions and voice syntheses require active parent consent recorded in `parent_consent_ledger`.
  - Calling `DELETE /v1/privacy/children/{child_id}/ai-history` performs an atomic purge from Postgres, Redis session cache, and vector embeddings, returning a signed purge receipt displayed in `Screens/Mobile App/Privacy/AI History-03.png`.

---

### Gap 07: Gamification XP & Rewards Ledger Immutability
- **Source A (PRD A11)**: Describes awarding XP and Noor Coins for quizzes, stories, and daily habits.
- **Source B (Screens: Admin Web 61-64, Mobile App/Rewards 01-09)**: Shows detailed transaction ledger, balance verification, and manual reward grants requiring supervisory approval.
- **Authoritative Resolution**:
  - Rewards are implemented as an **Append-Only Double-Entry Ledger** (`rewards_ledger` table) with `entry_type` (EARN, SPEND, EXPIRE, MANUAL_GRANT, REFUND).
  - Child balance is a materialized cache verified against `SUM(amount)`.
  - Manual grants in Admin Web (`Screens/Admin Web/64-Manual Reward Grant-01.png`) > 500 XP require Maker-Checker dual sign-off.

---

### Gap 08: Subscription Webhook & Entitlement Synchronization
- **Source A (PRDs C24, E33, D27)**: Describes App Store, Google Play, and Stripe subscriptions.
- **Source B (Screens: Admin Web 84, 85 & Mobile Subscription 01-17)**: Shows real-time reconciliation jobs, billing event health, and graceful grace-period handling.
- **Authoritative Resolution**:
  - Unified webhook ingestion engine at `POST /v1/billing/webhooks/{provider}` handles Stripe, Apple App Store Server Notifications v2, and Google Play Real-Time Developer Notifications.
  - `parent_entitlements` table acts as the unified source of truth for feature access, decoupling frontend clients from specific payment gateway identifiers.

### Gap 09: Child Lock Verification vs. Parent Profile Lock Recovery Boundary (Feature C.19)
- **Source A (PRD C.19 §1.7 FR-5, FR-6, FR-12)**: Details per-child lock verification, progressive lockout, and parent-verified recovery.
- **Source B (Development Blueprints B-01 & B-02)**: Separates server-authoritative lock verification (`POST /v1/children/{id}/lock/verify`) from the compound-authenticated recovery path (`POST /v1/children/{id}/lock/recover`).
- **Authoritative Resolution**:
  - `POST /v1/children/{id}/lock/verify` is the primary verification endpoint enforcing progressive exponential lockout (30s, 60s, 300s, 900s) and zero biometric data storage. Mid-cooldown requests are server-rejected with HTTP 423 `LOCKED_RETRY_COOLDOWN` without evaluating credentials.
  - If a child forgets their lock or gets locked out, recovery is **only** reachable via `POST /v1/children/{id}/lock/recover` after completing the Parent Gate (`POST /v1/auth/pin/verify`). There is strictly **no generic "forgot lock" bypass** anywhere in the system.

---

### Gap 10: Customer Support Parent Lockout Recovery Boundary (Feature C.19 / Blueprint B-05)
- **Source A (PRD C.19 §8 Admin Requirements & Support Tool)**: Mentions support agents assisting locked-out parents who have forgotten their Parent PIN or exhausted verification attempts.
- **Source B (Development Blueprint B-05)**: Establishes `POST /v1/admin/support/parents/{id}/recovery/initiate` behind the dedicated `support` RBAC scope.
- **Authoritative Resolution**:
  - Customer support agents are **strictly prohibited** from viewing, resetting, or overriding a Parent PIN directly.
  - The endpoint strictly re-triggers the parent's standard A.1 phone/email OTP challenge flow to their registered contact, identical to the parent's own self-serve recovery flow.
  - Every single invocation (success, 404 parent not found, or 502 upstream dispatch failure) immutably persists an `AdminAuditRecord` with `severity: high` and emits domain events via the transactional outbox.

### Gap 11: Bedtime Silent Completion UX Suppression vs. Gamification Ledger Parity (Feature A.4 / Blueprint B-03 / PRD FR-10)
- **Source A (PRD A.4 §1.7 FR-10 & §3.3)**: Specifies that audio story completion during Bedtime Mode must record rewards quietly in the background without dopamine-spiking celebratory fanfare, audio chimes, or confetti popups.
- **Source B (Rewards Architecture / Blueprint B-03 §10)**: Strict accounting rules forbid any divergence between standard daytime rewards and bedtime rewards to guarantee child fairness and prevent ledger discrepancies.
- **Authoritative Resolution**:
  - The backend completion endpoint `POST /v1/content/{id}/complete` accepts an optional `silent_completion: bool = False` parameter.
  - **Zero Ledger Divergence**: `RewardService.award_points()` receives byte-for-byte identical parameters (`points`, `xp`, `noor_points`, `reason`, `activity_type`, `idempotency_key`), creating identical `RewardLedgerEntry` accounting rows in PostgreSQL.
  - **Presentation Hint Isolation**: Suppression of celebratory UI is completely isolated to the response field `celebratory_ui_hint: bool` (`False` when `silent_completion=True`, `True` otherwise), directing the mobile client to navigate directly to the calming Dua Ending Card (Screen K-10).
  - **Analytics Outbox**: Genuine first-time silent completions emit `content.bedtime_reward_recorded_silently` into the transactional outbox for telemetry without affecting the reward ledger.

---

### Gap 12: Foundational Tajweed Placement vs. Advanced Quran Progress Gating (Feature A.5 / Blueprint B-02 / PRD §1.10 Edge Case 9)
- **Source A (PRD A.5 §1.10 Edge Case 9)**: When a placement check places a child past Surah-tree nodes that have un-verified Tajweed prerequisites, the system must either mark them provisionally `Ready` or schedule them for near-term review — foundational Tajweed prerequisites must never be silently skipped based on placement check alone.
- **Source B (Development Blueprint B-02 §10)**: Specifies `POST /v1/learning/placement-check` scoring against a content-driven question bank with atomic session flushing and Redis cache eviction.
- **Authoritative Resolution**:
  - Un-verified Tajweed prerequisites are **never silently skipped**. If a child tests past a Surah node requiring Tajweed, the prerequisite Tajweed node is marked provisional `ready` in `provisional_states` and an entry is scheduled in `spaced_review_schedules` with `due_date = today` (UTC). Directly verified Tajweed nodes are marked `mastered`.
  - **Duplicate Placement Submission**: Rejects repeated submissions with HTTP 409 Conflict (`PlacementCheckAlreadyCompletedError`), returning previously evaluated recommendations in error `details`.
  - **Admin Re-Check Override**: An administrator may toggle `set_recheck_allowed(child_id, is_recheck_allowed=True)`, allowing a single re-evaluation that resets the flag back to `False`.
  - **Diagnostic Question Bank Retrieval**: `GET /v1/learning/placement-check/questions` (and direct alias `/v1/placement-check/questions`) serves 6 calibrated diagnostic questions with localized prompts and options across English, Hindi, Urdu, and Arabic.

---

### Gap 13: Non-Recitation Practice vs. Recitation Audio Pipeline Separation & Multi-Session Mastery (Feature A.5 / Blueprint B-03 / PRD FR-7, FR-18)
- **Source A (PRD A.5 §1.7 FR-7, FR-10, FR-11, FR-18)**: Requires multi-session demonstration ($\ge 2$ distinct calendar dates) before awarding mastery; hints must not visibly penalize the child; recitation attempts must follow strict zero-retention voice privacy rules.
- **Source B (Development Blueprint B-03 §10)**: Non-recitation practice endpoint `POST /v1/learning/attempts` processes `quiz`, `tracing`, and `matching` attempts.
- **Authoritative Resolution**:
  - **Strict Recitation Guard**: Attempt type `recitation` is explicitly rejected on `/v1/learning/attempts` with HTTP 400 Bad Request (`RECITATION_ATTEMPT_TYPE_NOT_ALLOWED`), directing clients to Blueprint B-04 (`POST /v1/learning/recitation`).
  - **FR-7 Multi-Session Hold**: A node cannot transition from `practicing` to `mastered` in a single session. Correct demonstrations must span $\ge 2$ distinct calendar dates (`get_distinct_correct_session_dates`). Single-session repeated correct demonstrations are held in `practicing`.
  - **FR-18 Non-Penalizing Hints**: Hint count scales down the positive mastery increment (`delta > 0`), ensuring hints never create a visible penalty deduction on correct attempts.
  - **Replay Idempotency & Race Recovery**: Submissions with duplicate `client_event_id` return the original evaluation (`is_idempotent_replay: true`) without double-mutating mastery. Concurrency collisions catch `IntegrityError` and recover existing records cleanly.

---

### Gap 14: Search Operations Monitoring Telemetry, Per-Child Privacy Invariants & Content-Safety Filter Isolation (Feature B.13 / Blueprint B-07 / PRD §8, §10)
- **Source A (PRD B.13 §8 Admin Requirements & §10 DevOps)**: Specifies editorial and AI operations monitors for Search Index Health (sync lag, rejected items), Zero-Result Query Report, and Voice Search Confidence/Quality trends over time. Requires zero per-child privacy leaks and content safety filtering of all search terms surfaced to operators (Edge Case 3).
- **Source B (Development Blueprint B-07 §10, §14, §17, §25)**: Defines four read-only monitoring endpoints with distinct RBAC scopes, strict database schema privacy enforcement, and sanitized query aggregation.
- **Authoritative Resolution**:
  - **Structural Privacy Invariant**: Table `voice_search_confidence_log` has exactly 4 columns (`id`, `confidence_score`, `clarification_needed`, `created_at`). It is structurally incapable of persisting `child_id`, transcript text, or audio blobs, verified via schema introspection unit tests.
  - **Zero-Result Aggregate Privacy & Moderation**: Endpoint `GET /admin/v1/search/zero-result-report` aggregates strictly via `GROUP BY query_text, COUNT(*)` where `coalesce(result_count, 0) == 0`. It never groups by or returns `child_id`. All query strings pass through heuristic bad-word filters and `AISafetyService` moderation prior to aggregate exposure. Unsafe or inappropriate queries are completely omitted from operator reports.
  - **Distinct RBAC Scopes**: Rather than a generic "admin" role check, endpoints enforce distinct least-privilege scopes:
    - `/admin/v1/search/index-health` & `/admin/v1/search/rejected-items`: `content_editor`, `product_admin`, `admin:read`, `*`
    - `/admin/v1/search/zero-result-report`: `content_editor`, `admin:read`, `*` (forbidden to `ai_ops` and `product_admin` without editor scope)
    - `/admin/v1/search/voice-quality`: `ai_ops`, `product_admin`, `admin:read`, `*` (forbidden to `content_editor` alone)
  - **Date Range Constraints**: `from`/`to` parameters are validated as ISO-8601 or `YYYY-MM-DD`, enforce `from <= to`, and are bounded to a maximum span of 90 days (`422 Unprocessable Entity` on violation).

---

## 3. Backward Compatibility Safeguards & Invariants
1. **Schema Evolution**: All database schema changes MUST use nullable columns or provide backward-compatible column defaults.
2. **DTO Compatibility**: No API response fields may be removed or renamed without a formal API version deprecation cycle (minimum 6 months).
3. **Graceful Offline Degradation**: All Mobile App features must implement local SQLDelight caching and optimistic UI updates for core child experiences (Quran, Stories, Duas, Habits).



