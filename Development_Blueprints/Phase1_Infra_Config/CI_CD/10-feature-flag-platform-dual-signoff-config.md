# Phase 1 — Feature Flag Platform & Dual-Sign-Off Governance

**File ID:** `Development_Blueprints.Phase1_Infra_Config.CI_CD.10-feature-flag-platform-dual-signoff-config.md`
**Module:** CI_CD (cross-cutting: `backend/` new `feature_flags` bounded context, `admin-web/` new Feature Flags module, `mobile/` `core-common`/`core-network`/`core-datastore`)
**Phase:** Phase 1 — Infrastructure & Configuration
**Depends on:** Phase 1 item 06 (`CI_CD.06-ci-pipeline-lint-test-build-stages.md` — specifically its Stage 6 "Architectural Invariant Tests [PLACEHOLDER]" job per app; this file adds the first *real*, non-seed backend invariant test into that job's slot, per that file's own §15 hand-off design: *"`Phase9.CrossPlatform.01` adds sibling test functions to the same file/directory rather than replacing anything"* — this file is an earlier, narrower instance of exactly that pattern, scoped to the dual-sign-off invariant alone)
**Consumed by:** Every future Development Blueprint that ships a child-facing safety-relevant capability behind a flag (AI content-filtering strictness, moderation thresholds, parental-control defaults) — this file is the platform those features toggle through, not a feature itself; `Development_Blueprints.Phase9_Testing_Quality.CrossPlatform.01-architectural-invariant-test-suite.md` (adds this file's dual-sign-off invariant test to its consolidated suite rather than re-deriving it)
**Source of truth:** `NoorHeroes_Final_Development_Prompt.md` §6 ("Feature flags" bullet — LaunchDarkly/Unleash/in-house table choice, dual sign-off mandate, F.37 cross-reference), §4 (code-review checklist line requiring scholar/child-safety sign-off review per F.37), §9 (security baseline, non-bypassable CI status checks), §14 (Open Decision: "Feature-flag platform: managed (LaunchDarkly) vs. self-hosted (Unleash) vs. in-house table" — resolved by this file, see §18); `NoorHeroes_Consolidated_Blueprint_v6.md` §11.6 (nine-role RBAC table), §11.8 (Feature Flags admin-module row: schema/CRUD/validation/workflow — this file's primary functional-spec source), §11.8 App Configuration row (sibling module, same "reason note required" / "safety-relevant approval" pattern, reused here), §11.7 (audit-log/config-settings framing); `FAST-API-INSTRUCTIONS.md` §1/§2/§3/§5/§10/§11 (modular-monolith layering, `core/deps.py`, `BaseService`/`BaseRepository`/`OutboxWriter`, 12-bounded-context precedent, security declarations, layer rules); `NEXT-JS-INSTRUCTIONS.md` §5-§9 (`RequirePermission`, `useElevatedSession`/`requestElevation`, `BaseResourceClient`, `hasPermission`); `CORE_DATASTORE_INSTRUCTIONS.md` §4 (`RemoteConfigRepository`, `FeatureFlagDefaults`, `FlagSource`), §10 Scenario 1 (the 3-step "adding a new feature flag" process this file extends to 4 steps); `CORE_NETWORK_INSTRUCTIONS.md` §4 (`AuthApiService` naming precedent, `FeatureFlagProvider`/`FeatureFlag` existing facade — reconciled, not duplicated, in §12)
**Status:** NEW — this file does not exist in the corpus today. Phase 1's feature-flag platform is a confirmed, total gap: nothing under `src/noorheroes/modules/feature_flags/`, `src/features/feature-flags/`, or a wired `RemoteConfigRepositoryImpl.refresh()` exists yet.

**Do not re-litigate:** the backend's 12 existing bounded contexts, `AdminSessionContext`/`require_admin_scope`/`BaseService`/`BaseRepository`/`OutboxWriter` (all fully implemented, per `FAST-API-INSTRUCTIONS.md`); the Admin Portal's nine-role RBAC, `RequirePermission`, `useElevatedSession`/`requestElevation` 2FA step-up mechanism, `BaseResourceClient`, `DataTable`, `ConfirmationDialog` (all fully implemented, per `NEXT-JS-INSTRUCTIONS.md`); the KMP app's `core-datastore` module, `PreferenceManager`, and the *existing* `RemoteConfigRepository`/`RemoteConfigRepositoryImpl` stub with its `FeatureFlagDefaults` model and `FlagSource` enum (fully implemented as a local-reconciliation-only stub, per `CORE_DATASTORE_INSTRUCTIONS.md`). This document builds none of that. It builds the **feature-flag platform on top of it**: a new backend bounded context, a new Admin Portal module, and the network wiring that finally gives `RemoteConfigRepositoryImpl.refresh()` — documented today as *"Phase 0 Status: `refresh()` currently triggers a local state refresh; future phases will integrate the network bootstrap endpoint"* — a real endpoint to call.

---

## 1. Objective and Purpose

Give NoorHeroes a working feature-flag platform — flag storage, environment-scoped evaluation, an Admin Portal management UI, and client SDK wiring across backend/admin-web/KMP — with one non-negotiable governance rule enforced in code, not in a process document: **a flag marked `safety_relevant = true` cannot go live, or have its rollout raised above 0%, until two distinct human admin accounts have independently approved the change, and the two accounts' combined roles must include at least one Super Admin and at least one Child Safety Reviewer.** This is the "dual sign-off" rule named in `NoorHeroes_Final_Development_Prompt.md` §6 and in `NoorHeroes_Consolidated_Blueprint_v6.md` §11.8's Feature Flags row, tracing to blueprint requirement F.37.

"Safety-relevant" means, concretely, per the task brief and blueprint's own child-safety framing: AI content-filtering strictness (e.g., relaxing the moderation threshold an AI Tutor/story-generation response must clear before reaching a child), child-facing feature rollouts for any surface a child directly interacts with unsupervised, and anything touching content moderation queues or parental-control defaults (screen-time presets, age-gating thresholds, consent-adjacent toggles). A flag like `dark_mode_enabled` or `new_dashboard_layout_v2` is not safety-relevant. A flag like `ai_tutor_moderation_threshold_relaxed` or `story_content_filter_strict_mode` is. The `safety_relevant` boolean is set once, at flag-creation time, by the admin creating the flag (§9 covers who may set it and why it cannot be silently flipped later).

**What "done" looks like, concretely:** a Super Admin proposes turning `ai_moderation_relaxed_mode` on in production. The Admin Portal shows the flag's state as "Pending — 1 of 2 approvals needed." No amount of retrying, no admin-console trick, no direct database access outside a documented break-glass runbook changes that. A second, *different* person — holding the Child Safety Reviewer role — logs in, reviews the proposal's reason note, enters their own 2FA OTP for step-up elevation, and approves. Only then does the flag's `enabled` value for production actually change, and only then does `GET /v1/feature-flags/evaluate` start returning `true` for that key. An architectural CI test (§14) makes it impossible to merge a code change that lets this rule be bypassed silently, the same way `NoorHeroes_Final_Development_Prompt.md` §5 already treats JWT-schema-singularity and gateway-authorization-zero as CI-blocking, non-negotiable invariants.

## 2. Scope and Requirements

**In scope:**
- A new 13th backend bounded context, `feature_flags` (`src/noorheroes/modules/feature_flags/`), following the identical Router→Service→Repository→PostgreSQL layering every other context uses.
- Three new PostgreSQL tables: `feature_flags` (definitions), `feature_flag_environment_states` (per-environment live/pending state), `feature_flag_approvals` (append-only audit ledger).
- A public/optional-auth evaluation endpoint (`GET /v1/feature-flags/evaluate`) consumed by the KMP app and, indirectly, the backend's own in-process `FeatureFlagService.evaluate_flag()` used by other bounded contexts.
- An admin CRUD + approval-workflow API (`/v1/admin/feature-flags/...`) enforcing the dual-sign-off state machine (§11) server-side — the only place this rule is truly enforced; the Admin Portal UI reflects it, never re-implements it.
- A new Admin Portal module, `src/features/feature-flags/`, wired into the existing `DashboardShell` navigation, reusing `RequirePermission`, `useElevatedSession`/`requestElevation`, `BaseResourceClient`, `DataTable`, `ConfirmationDialog`, `StatusBadge`.
- Completing the existing `RemoteConfigRepositoryImpl.refresh()` stub in `core-datastore` to call the new evaluation endpoint via a new `core-network` `FeatureFlagApiService`, and reconciling the existing `core-network` `FeatureFlagProvider`/`FeatureFlag` facade to be backed by it (§12).
- New RBAC permission strings layered onto the existing nine-role model (no new roles — Super Admin and Child Safety Reviewer already exist and already carry exactly the scope this rule needs).
- The CI-blocking architectural invariant test proving the dual-sign-off rule cannot be bypassed (§14).

**Explicitly not built here:**
- Any *specific* safety-relevant flag's business logic (e.g., what "relaxed moderation" actually changes inside the AI Tutor pipeline) — that belongs to whichever future Development Blueprint implements that feature. This file only guarantees that *whatever* flag that feature registers as `safety_relevant = true` is dual-sign-off-gated automatically, for free, by virtue of using this platform.
- A managed third-party flag vendor integration (LaunchDarkly/Unleash SDK). §18 documents why and confirms the in-house choice.
- Real-time flag-change push to already-connected KMP clients (WebSocket-based instant propagation). Flags propagate on the existing `RemoteConfigRepository` refresh cadence (§7); this is a deliberate, documented latency trade-off (§10), not a missing feature.
- Multivariate (string/JSON payload) flag values beyond the two types this file defines (`BOOLEAN`, `PERCENTAGE_ROLLOUT`). A future `JSON_VARIANT` flag type is an additive schema extension, not built here.
- Changes to `B-01`'s existing `remote_config` singleton table/`RemoteConfigRepository` (backend, `identity` module — the bootstrap-gate config for `min_supported_version`/`maintenance_mode`/`consent_version`). That table is a different concern (deploy-gating config, singleton row) from this file's per-key flag definitions and is not touched, extended, or merged into by this work. **Naming collision warning:** the backend already has a class named `RemoteConfigRepository` in `src/noorheroes/modules/identity/remote_config_repository.py` (per B-01), and the KMP app already has a *different* class also named `RemoteConfigRepository` in `core-common`/`core-datastore` (per `CORE_DATASTORE_INSTRUCTIONS.md`). Neither is renamed or touched by this file. This file's new backend context is named `feature_flags`, not `remote_config`, specifically to avoid a third collision.

## 3. Technical Implementation Details

### 3.1 Flag lifecycle at a glance

```text
   Engineer/Super Admin registers a flag definition
   (key, type, safety_relevant, default_value)
                    │
                    ▼
   Per-environment state starts at DRAFT (enabled=false, rollout=0)
                    │
        ┌───────────┴────────────┐
        │                         │
   safety_relevant=false     safety_relevant=true
        │                         │
   propose(enabled/rollout)   propose(enabled/rollout)
        │                         │
        ▼                         ▼
      LIVE                 PENDING_APPROVAL (0/2)
   (single actor,               │
    immediate)              approve #1 (distinct admin,
                             role ∈ {Super Admin, Child
                             Safety Reviewer}, ≠ proposer)
                                  │
                                  ▼
                          PENDING_SECOND_APPROVAL (1/2)
                                  │
                             approve #2 (distinct admin,
                             ≠ proposer, ≠ first approver,
                             combined roles cover BOTH
                             Super Admin AND Child Safety
                             Reviewer)
                                  │
                                  ▼
                                LIVE
                          (enabled/rollout now real)
                                  │
                     kill-switch (disable only,
                     single Super Admin action,
                     always instant — never gated)
                                  │
                                  ▼
                          LIVE, enabled=false
                                  │
                             archive (any state)
                                  ▼
                              ARCHIVED
```

Full state machine, transition guards, and every edge case (reject, self-approval attempts, stale proposals) are specified in §11.

### 3.2 Deterministic percentage-rollout bucketing

`PERCENTAGE_ROLLOUT` flags use a stable, dependency-free hash so raising a rollout percentage only ever *adds* newly-included subjects, never reshuffles ones already in:

```python
import hashlib

def bucket_for(flag_key: str, subject_id: str) -> int:
    """Returns a stable integer in [0, 99] for (flag_key, subject_id)."""
    digest = hashlib.sha256(f"{flag_key}:{subject_id}".encode("utf-8")).hexdigest()
    return int(digest, 16) % 100

def is_in_rollout(flag_key: str, subject_id: str, rollout_percentage: int) -> bool:
    return bucket_for(flag_key, subject_id) < rollout_percentage
```

`subject_id` is `child_id` when a child session context is available, else `family_id`, else (unauthenticated evaluate calls) a client-generated `bucketing_key` query parameter — see §6's evaluate contract. No new dependency (`hashlib` is stdlib) — consistent with §18's build-vs-buy reasoning of minimizing new moving parts.

### 3.3 Environment is server-resolved, never client-supplied

The evaluation endpoint determines which environment's state to read from `Settings.ENVIRONMENT` (the existing `Environment` StrEnum — `LOCAL`/`DEVELOPMENT`/`STAGING`/`PRODUCTION` — per `FAST-API-INSTRUCTIONS.md` §2's `core/settings.py`), **never** from a client-supplied header or query parameter. A client claiming `X-Environment: development` must not be able to see an unreleased/still-pending flag value that happens to already be `LIVE` in a lower environment — each deployed backend instance only ever serves its own environment's state, full stop.

## 4. Architecture and Component Responsibilities

```text
┌────────────────────────────────────────────────────────────────────────────────┐
│                              ADMIN PORTAL (Next.js)                             │
│  src/features/feature-flags/  — FlagListPage, FlagEditorDrawer,                 │
│  ApprovalQueuePage, FlagAuditHistoryPanel                                       │
│  Guards: <RequirePermission permission="feature_flags:..."> everywhere          │
│  High-risk actions (propose/approve/reject/kill-switch on safety-relevant       │
│  flags) require useElevatedSession()/requestElevation() step-up, exactly like   │
│  the existing useDeleteFamily() high-risk pattern.                              │
└───────────────────────────────┬───────────────────────────────────────────────┘
                                 │ HTTPS, Bearer + elevatedToken where required
                                 ▼
┌────────────────────────────────────────────────────────────────────────────────┐
│                    BACKEND — new `feature_flags` bounded context                │
│  FeatureFlagAdminRouter (admin_api.py)     FeatureFlagsRouter (api.py)          │
│       │  CRUD + propose/approve/reject/         │  GET /v1/feature-flags/       │
│       │  kill-switch, Depends(get_current_admin) │  evaluate (optional auth)    │
│       ▼                                          ▼                              │
│  FeatureFlagService(BaseService)  ← the ONLY place the dual-sign-off state       │
│       │  machine (§11) is enforced. Admin UI reflects state; never re-derives it.│
│       ▼                                                                          │
│  FeatureFlagRepository / FeatureFlagEnvironmentStateRepository /                │
│  FeatureFlagApprovalRepository  (all BaseRepository[ModelT] subclasses)         │
│       ▼                                                                          │
│  PostgreSQL: feature_flags, feature_flag_environment_states,                    │
│              feature_flag_approvals                                             │
│  Redis: cache-aside per (flag_key, environment), 30s TTL, actively busted on     │
│         approve/reject/kill-switch (§10 — cache staleness on a kill switch is    │
│         a safety bug, not a performance nit-pick)                               │
└───────────────────────────────┬───────────────────────────────────────────────┘
                                 │ Other backend contexts call FeatureFlagService
                                 │ in-process (no HTTP hop) via Depends()
                                 │
                    ┌────────────┴─────────────┐
                    │  Any future safety-       │
                    │  relevant backend logic   │
                    │  (AI Tutor moderation,    │
                    │  content filter strictness)│
                    └────────────────────────────┘
                                 │
                                 │ GET /v1/feature-flags/evaluate (HTTP, optional auth)
                                 ▼
┌────────────────────────────────────────────────────────────────────────────────┐
│                         KMP APP (Android/iOS, Compose Multiplatform)             │
│  core-network: NEW FeatureFlagApiService  (Ktor, follows AuthApiService pattern) │
│       ▼                                                                          │
│  core-datastore: RemoteConfigRepositoryImpl.refresh()  — MODIFIED (was a local-  │
│  only stub; now calls FeatureFlagApiService, writes results via PreferenceManager,│
│  reconciles against FeatureFlagDefaults build-time defaults exactly as today)    │
│       ▼                                                                          │
│  core-common: RemoteConfigRepository (interface, UNCHANGED signature),           │
│  FeatureFlagDefaults (EXTENDED with new flag properties as flags are added),     │
│  PreferenceConstants (EXTENDED with new keys)                                    │
│       ▼                                                                          │
│  core-network: FeatureFlagProvider/FeatureFlag facade — RECONCILED to delegate   │
│  to RemoteConfigRepository, not a second parallel flag source (§12)              │
│       ▼                                                                          │
│  Feature modules: featureFlagProvider.isEnabled(FeatureFlag.AI_TUTOR)            │
└────────────────────────────────────────────────────────────────────────────────┘
```

**Component responsibilities:**

| Component | Responsibility |
|---|---|
| `FeatureFlagService` (backend) | Sole enforcer of the dual-sign-off state machine (§11), evaluation logic (§3.2/§6), safe-default fallback on any storage failure (§10). Every other component — Admin UI, KMP client, other backend contexts — is a *consumer* of this service's decisions, never a second decision-maker. |
| `FeatureFlagRepository` / `...EnvironmentStateRepository` / `...ApprovalRepository` | Pure data access, `BaseRepository[ModelT]` subclasses, no business rules (matches the Router/Service/Repository layer-rule table in `FAST-API-INSTRUCTIONS.md` §11). |
| `FeatureFlagsRouter` (public evaluate) | Thin HTTP boundary; zero business logic; delegates entirely to `FeatureFlagService.evaluate_all_for_context()`. |
| `FeatureFlagAdminRouter` | Thin HTTP boundary for CRUD/propose/approve/reject/kill-switch; enforces RBAC scope + elevated-session presence at the dependency level, delegates workflow logic to the service. |
| Admin Portal `feature-flags` feature module | Presents flag state and gathers the human decision (propose/approve/reject) via existing `RequirePermission`/`useElevatedSession` primitives; contains **zero** approval-count or role-pairing logic of its own — it renders whatever state the backend returns and disables buttons based on the current admin's own permissions, purely as UX, never as the actual gate. |
| `core-datastore` `RemoteConfigRepositoryImpl` | Reconciles the network-fetched flag values with build-time `FeatureFlagDefaults`, exactly as it already does for locally-set values today — this file only gives its `refresh()` a real network call to make. |
| `core-network` `FeatureFlagApiService` / `FeatureFlagProvider` | Typed client + convenience facade for feature modules; `FeatureFlagProvider` must be backed by `RemoteConfigRepository`, never a second, divergent flag-storage path (§12). |

## 5. Folder/File Structure

```text
noorheroes/
├── backend/
│   ├── src/noorheroes/modules/feature_flags/          # NEW — 13th bounded context
│   │   ├── __init__.py
│   │   ├── models.py                # FeatureFlagOrm, FeatureFlagEnvironmentStateOrm, FeatureFlagApprovalOrm
│   │   ├── schemas.py                # Create/Update/Response/Proposal/Approval DTOs (NoorHeroesBaseModel)
│   │   ├── repository.py             # FeatureFlagRepository, FeatureFlagEnvironmentStateRepository, FeatureFlagApprovalRepository
│   │   ├── evaluation.py             # FlagEvaluationContext, bucket_for()/is_in_rollout(), TargetingRuleMatcher
│   │   ├── state_machine.py          # FlagLifecycleState enum + pure transition-guard functions (unit-testable in isolation)
│   │   ├── service.py                # FeatureFlagService(BaseService)
│   │   ├── api.py                    # FeatureFlagsRouter — GET /v1/feature-flags/evaluate
│   │   └── admin_api.py              # FeatureFlagAdminRouter — /v1/admin/feature-flags/...
│   ├── alembic/versions/xxxx_add_feature_flags_tables.py   # NEW — additive-only migration
│   └── tests/
│       ├── modules/feature_flags/
│       │   ├── test_state_machine.py
│       │   ├── test_feature_flag_service.py
│       │   ├── test_feature_flag_api.py
│       │   └── test_feature_flag_admin_api.py
│       └── architectural/
│           └── test_safety_flag_dual_signoff_invariant.py   # NEW — CI-blocking (§14)
├── admin-web/
│   └── src/
│       ├── features/feature-flags/                     # NEW
│       │   ├── api/feature-flag-resource-client.ts      # extends BaseResourceClient
│       │   ├── hooks/
│       │   │   ├── use-feature-flags.ts
│       │   │   ├── use-feature-flag-detail.ts
│       │   │   ├── use-create-feature-flag.ts
│       │   │   ├── use-propose-flag-change.ts
│       │   │   ├── use-approve-flag-change.ts
│       │   │   ├── use-reject-flag-change.ts
│       │   │   ├── use-kill-switch-flag.ts
│       │   │   └── use-flag-approval-history.ts
│       │   ├── components/
│       │   │   ├── flag-list-table.tsx
│       │   │   ├── flag-editor-drawer.tsx
│       │   │   ├── flag-approval-queue.tsx
│       │   │   ├── flag-lifecycle-badge.tsx
│       │   │   ├── flag-audit-history-panel.tsx
│       │   │   └── flag-kill-switch-button.tsx
│       │   ├── types.ts
│       │   └── index.ts
│       └── app/(dashboard)/feature-flags/
│           ├── page.tsx                                  # flag list
│           ├── [flagId]/page.tsx                          # flag detail + environment states
│           └── approvals/page.tsx                         # cross-flag approval queue
└── mobile/
    ├── core/core-common/src/commonMain/kotlin/com/noorheroes/core/common/config/
    │   ├── PreferenceConstants.kt        # MODIFIED — add new flag keys as flags are registered
    │   ├── FeatureFlagDefaults.kt        # MODIFIED — add new flag properties as flags are registered
    │   └── RemoteConfigRepository.kt     # UNCHANGED interface signature
    ├── core/core-network/src/commonMain/kotlin/com/noorheroes/core/network/
    │   ├── service/FeatureFlagApiService.kt      # NEW
    │   ├── model/FeatureFlagEvaluationResponseDto.kt   # NEW
    │   └── feature/FeatureFlagProvider.kt        # MODIFIED — delegate to RemoteConfigRepository (§12)
    └── core/core-datastore/src/commonMain/kotlin/com/noorheroes/core/datastore/store/
        └── RemoteConfigRepositoryImpl.kt          # MODIFIED — refresh() now network-backed
```

## 6. APIs, Models, Interfaces, and Data Flow

### 6.1 Flag definition schema (`feature_flags` table — see §8 for full DDL-level detail)

| Field | Type | Notes |
|---|---|---|
| `flag_id` | `uuid` PK | |
| `key` | `varchar`, unique | Immutable after creation. Pattern `^[a-z][a-z0-9_]*$`, e.g. `ai_moderation_relaxed_mode`. |
| `name` | `varchar` | Human-readable label for the Admin UI. |
| `description` | `text` | What the flag does, required non-empty. |
| `flag_type` | enum `BOOLEAN` \| `PERCENTAGE_ROLLOUT` | |
| `safety_relevant` | `boolean`, not null, default `false` | **Set once at creation, immutable thereafter** — see §9 for why. |
| `default_value` | `jsonb` | The conservative/safe fallback value returned on any evaluation failure (§10). For a safety-relevant flag this must be the *restrictive* value (e.g., `{"enabled": false}` for "relax moderation," never `{"enabled": true}`). |
| `owner_admin_id` | `uuid` FK → admin | Who registered the definition. |
| `created_at` / `updated_at` / `version` | `TimestampMixin` | Standard optimistic-lock columns, per `infrastructure/db/base.py`. |
| `archived_at` | `timestamptz`, nullable | Soft-archive marker, never hard-deleted. |

### 6.2 Environment state schema (`feature_flag_environment_states` table)

| Field | Type | Notes |
|---|---|---|
| `state_id` | `uuid` PK | |
| `flag_id` | `uuid` FK → `feature_flags.flag_id` | |
| `environment` | enum (reuses existing `Environment`: `LOCAL`/`DEVELOPMENT`/`STAGING`/`PRODUCTION`) | |
| `lifecycle_state` | enum `DRAFT` \| `PENDING_APPROVAL` \| `PENDING_SECOND_APPROVAL` \| `LIVE` \| `REJECTED` \| `ARCHIVED` | §11 owns the full transition table. |
| `enabled` | `boolean` | |
| `rollout_percentage` | `int`, 0-100 | Only meaningful for `PERCENTAGE_ROLLOUT` flags; forced to `0` at creation for `BOOLEAN` flags. |
| `targeting_rules` | `jsonb` | Whitelisted keys only: `age_bands` (array of `AgeBand` enum values), `locales` (array of BCP-47 tags), `subscription_tiers` (array), `min_app_version` (semver string). Unknown keys rejected at the schema layer (Pydantic strict mode). |
| `proposed_by_admin_id` | `uuid` FK, nullable | Set on `propose`, cleared once `LIVE`/`REJECTED`. |
| `proposed_at` | `timestamptz`, nullable | |
| `first_approved_by_admin_id` | `uuid` FK, nullable | Set on the first `approve` for a safety-relevant flag. |
| `first_approved_at` | `timestamptz`, nullable | |
| `live_since` | `timestamptz`, nullable | Set the moment `lifecycle_state` transitions to `LIVE`. |
| `version` | optimistic lock | Guards the concurrent-double-approval race (§10). |
| Unique constraint | `(flag_id, environment)` | Exactly one state row per flag per environment. |

### 6.3 Approval audit ledger (`feature_flag_approvals` table)

Append-only — no `UPDATE`/`DELETE` grant for the application DB role, mirroring the pattern already established for `consent_record` (per B-01's cross-reference) and `RewardLedgerEntry` (per `FAST-API-INSTRUCTIONS.md` §5.9's append-only reward ledger).

| Field | Type | Notes |
|---|---|---|
| `approval_id` | `uuid` PK | |
| `flag_id` | `uuid` FK | |
| `environment` | enum | |
| `action` | enum `PROPOSED` \| `APPROVED` \| `REJECTED` \| `KILL_SWITCHED` \| `ARCHIVED` | |
| `actor_admin_id` | `uuid` FK | |
| `actor_role_snapshot` | `varchar` | The actor's RBAC role **at the time of the action**, captured explicitly — a role reassignment after the fact must never retroactively change what the audit trail says was true. |
| `reason_note` | `text` | Required (min 10 chars), non-empty for every action on a safety-relevant flag; optional for non-safety flags. |
| `resulting_lifecycle_state` | enum | The state the environment-state row transitioned *to* as a result of this action. |
| `created_at` | `timestamptz` | |

### 6.4 Evaluation data flow

```text
KMP client launch / periodic refresh
        │
        ▼
GET /v1/feature-flags/evaluate
   Headers: Authorization (optional), X-App-Version, X-Platform
   Query:   bucketing_key (optional, for unauthenticated percentage-rollout bucketing)
        │
        ▼
FeatureFlagsRouter.evaluate_flags()
        │  (optional-auth: reuses get_optional_parent, per B-01's precedent —
        │   never 401s just because the app launched signed-out)
        ▼
FeatureFlagService.evaluate_all_for_context(ctx: FlagEvaluationContext)
        │
        ├─ For each active (non-archived) flag definition:
        │    1. Redis cache-aside read: key `ff:{environment}:{flag_key}` (30s TTL)
        │    2. Cache miss → FeatureFlagEnvironmentStateRepository.get_state(flag_id, environment)
        │    3. lifecycle_state != LIVE  → return flag's default_value, source=BUILD_DEFAULT_FALLBACK
        │    4. lifecycle_state == LIVE, flag_type=BOOLEAN → return {enabled}, source=REMOTE
        │    5. lifecycle_state == LIVE, flag_type=PERCENTAGE_ROLLOUT →
        │         TargetingRuleMatcher checks age_band/locale/subscription_tier/min_app_version
        │         → is_in_rollout(key, subject_id, rollout_percentage) (§3.2)
        │         → return {enabled: matched_and_in_bucket}, source=REMOTE
        │    6. Any repository/Redis exception at any step → return default_value,
        │       source=BUILD_DEFAULT_FALLBACK, log a warning (never propagate a 5xx
        │       from a single flag's evaluation failure — §10)
        ▼
FlagEvaluationResponse { environment, evaluated_at, flags: { key: {value, source} } }
        │
        ▼
KMP: FeatureFlagApiService.evaluateFlags() → RemoteConfigRepositoryImpl.refresh()
     → PreferenceManager.setBoolean(...)/setString(...) per PreferenceConstants key
     → RemoteConfigRepositoryImpl.observeFlags() Flow emits updated FeatureFlagDefaults
     → featureFlagProvider.isEnabled(FeatureFlag.AI_TUTOR) now reflects the new value
```

### 6.5 Public evaluation endpoint contract

**`GET /v1/feature-flags/evaluate`**
- **Auth:** Optional, identical pattern to B-01's bootstrap endpoint — `get_optional_parent`, never raises on an expired/missing token.
- **Headers:** `X-App-Version` (required, semver), `X-Platform` (required, `android`\|`ios`).
- **Query:** `bucketing_key` (optional, opaque client-generated stable string, used only when no authenticated child/family session exists — see §10's unauthenticated-bucketing edge case).
- **Response 200:**
```json
{
  "environment": "production",
  "evaluatedAt": "2026-08-24T10:15:00Z",
  "flags": {
    "ai_tutor_enabled": { "value": true, "source": "REMOTE" },
    "ramadan_mode_enabled": { "value": false, "source": "REMOTE" },
    "ai_moderation_relaxed_mode": { "value": false, "source": "BUILD_DEFAULT_FALLBACK" }
  }
}
```
`source` is exactly the KMP `FlagSource` enum's two members (`REMOTE`, `BUILD_DEFAULT_FALLBACK`) — chosen deliberately so the response maps onto `FeatureFlagDefaults` with zero translation layer on the client.
- **Rate limit:** 120 req/min/IP (existing `RateLimitMiddleware`/`SlidingWindowRateLimiter`) — higher than bootstrap's 60/min since active sessions call this more frequently on the refresh cadence (§7).
- **Caching:** Server-side Redis 30s TTL per key (actively busted on any admin mutation, §10). Client-side, the KMP app may cache the full response for the same interval as its refresh cadence — never longer, and never independently of a `refresh()` call the app itself controls.

### 6.6 Admin API contract summary

| Method | Path | Permission | Elevated session? | Purpose |
|---|---|---|---|---|
| `GET` | `/v1/admin/feature-flags` | `feature_flags:read` | No | Paginated list, filterable by `environment`/`safety_relevant`/`lifecycle_state`. |
| `GET` | `/v1/admin/feature-flags/{flagId}` | `feature_flags:read` | No | Definition + all environment states. |
| `POST` | `/v1/admin/feature-flags` | `feature_flags:create` | No | Create a flag definition (Super Admin only — §9). |
| `DELETE` | `/v1/admin/feature-flags/{flagId}` | `feature_flags:archive` | No | Archive definition + cascade all environment states to `ARCHIVED`. Never a hard delete. |
| `PATCH` | `/v1/admin/feature-flags/{flagId}/environments/{env}/propose` | `feature_flags:propose` | **Yes**, for `safety_relevant=true` flags only | Non-safety: commits immediately to `LIVE`. Safety-relevant: opens `PENDING_APPROVAL`. |
| `POST` | `/v1/admin/feature-flags/{flagId}/environments/{env}/approve` | `feature_flags:approve` (non-safety) or `feature_flags:approve_safety` (safety-relevant) | **Yes** | Records one approval; transitions state per §11. |
| `POST` | `/v1/admin/feature-flags/{flagId}/environments/{env}/reject` | Same as approve | **Yes** | Terminates the pending proposal; requires `reason_note`. |
| `POST` | `/v1/admin/feature-flags/{flagId}/environments/{env}/kill-switch` | `feature_flags:kill_switch` | **Yes** (single-actor, no second approver) | Instantly sets `enabled=false`, `rollout_percentage=0`. |
| `GET` | `/v1/admin/feature-flags/{flagId}/approvals` | `feature_flags:read` | No | Full immutable audit history for the flag. |
| `GET` | `/v1/admin/feature-flags/approvals/pending` | `feature_flags:approve_safety` | No | Cross-flag queue: every safety-relevant proposal awaiting this admin's role. Backs the Admin Portal's `approvals` page. |

## 7. Dependencies and Configuration Requirements

**No new external vendor, no new cloud spend** — see §18's full build-vs-buy justification.

**Backend:** zero new third-party Python dependency. `hashlib` (stdlib, §3.2), existing `redis`, `sqlalchemy[asyncio]`, `alembic`, `pydantic`. New `Settings` (`core/settings.py`) fields:

| Setting | Type | Default | Purpose |
|---|---|---|---|
| `FEATURE_FLAG_CACHE_TTL_SECONDS` | `int` | `30` | Redis cache-aside TTL for evaluation reads. |
| `FEATURE_FLAG_STALE_PROPOSAL_REMINDER_HOURS` | `int` | `48` | When an unapproved safety-relevant proposal triggers a reminder (§10's deadlock mitigation). |
| `FEATURE_FLAG_STALE_PROPOSAL_EXPIRY_DAYS` | `int` | `14` | When an unapproved proposal auto-reverts to `DRAFT` (§10, §11). |

New Celery periodic task, `expire_stale_flag_proposals_task` (`src/noorheroes/modules/feature_flags/tasks.py`), following the exact periodic-task pattern already established by `retry_failed_translations_task` in the `localization` context.

**Admin-web:** zero new npm dependency. Reuses `BaseResourceClient`, `RequirePermission`, `useElevatedSession`, `DataTable`, `ConfirmationDialog`, `StatusBadge`, `useTranslation`, `useFormatters`.

**Mobile:** zero new Gradle dependency. Reuses the existing Ktor `HttpClient` (`core-network`'s `provideHttpClient`), Koin DI, Jetpack DataStore.

**Environment variables:** none of the above are secrets — all three new `Settings` fields are plain tunable integers, safe to default in code and override via the existing `.env`/typed-config mechanism (`Infra.02`) without any new secret-provisioning step.

## 8. Database/Storage Requirements

- **Migration:** one additive-only Alembic migration, `alembic/versions/xxxx_add_feature_flags_tables.py`, creating all three tables from §6.1-§6.3. No existing table is touched. No destructive change anywhere in this file.
- **Indices:** `feature_flags.key` (unique), `feature_flag_environment_states (flag_id, environment)` (unique composite, also the primary lookup path for evaluation), `feature_flag_approvals.flag_id` (non-unique, for audit-history reads), `feature_flag_approvals.actor_admin_id` (non-unique, supports the architectural invariant test's "distinct approver" query in §14).
- **Grants:** `feature_flags` and `feature_flag_environment_states` are Create/Read/Update-only for the application DB role (matches the App Configuration module's own "no delete — append-only versioned" sibling pattern in `NoorHeroes_Consolidated_Blueprint_v6.md` §11.8) — `DELETE` is never issued; "delete" at the API layer always means `archived_at`/`lifecycle_state=ARCHIVED`. `feature_flag_approvals` is Insert-only — no `UPDATE`, no `DELETE` grant at all, full stop.
- **Backup/restore:** ordinary tables under the existing managed-Postgres automated-backup + restore-drill process (`NoorHeroes_Final_Development_Prompt.md` §7). Explicitly called out here because audit tables are sometimes mistakenly treated as ephemeral/excludable from backup scope — `feature_flag_approvals` must never be excluded; it is the only durable proof the dual-sign-off rule was actually followed for a given historical change, and a child-safety incident review may need it.
- **Redis:** cache-aside only, no durable state lives in Redis for this feature — a full Redis flush degrades every evaluation to a direct (still-correct) Postgres read plus a warning log, never to a wrong or stale value beyond the 30s TTL window it would have used anyway.

## 9. Authentication, Authorization, Validation, and Security Considerations

### 9.1 RBAC permission strings (extending the existing nine-role model — no new roles)

| Permission | Super Admin | Child Safety Reviewer | Content Editor / Publisher / Scholar Reviewer / Support Agent / Billing Ops / Analyst / Localization Manager |
|---|---|---|---|
| `feature_flags:read` | ✅ | ✅ | ✅ (visibility only — informs content scheduling, e.g. "is Ramadan Mode live") |
| `feature_flags:create` | ✅ | ❌ | ❌ |
| `feature_flags:propose` | ✅ | ❌ | ❌ |
| `feature_flags:approve` (non-safety lane) | ✅ | ❌ | ❌ |
| `feature_flags:approve_safety` | ✅ | ✅ | ❌ |
| `feature_flags:archive` | ✅ | ❌ | ❌ |
| `feature_flags:kill_switch` | ✅ | ❌ | ❌ |

This mapping is deliberate, not incidental: **Child Safety Reviewer can only ever be the checker, never the initiator** — they hold `approve_safety` and nothing else in this domain, matching their existing blueprint scope ("Independent age/safety review and moderation," `NoorHeroes_Consolidated_Blueprint_v6.md` §11.6) and mirroring the same submitter≠approver segregation-of-duties pattern already implemented for the Avatar review workflow (`AvatarReviewRouter`, `FAST-API-INSTRUCTIONS.md` §5.12 — "structurally reject self-approval"). Extend the existing `AdminPermission` TypeScript union type (consumed by `hasPermission()`/`RequirePermission`, per `NEXT-JS-INSTRUCTIONS.md` §6) with these seven string literals — do not fork a parallel permission type.

### 9.2 The `safety_relevant` boolean is immutable after creation

Once a flag definition is created, `safety_relevant` can never be changed via the API (no `PATCH /v1/admin/feature-flags/{flagId}` endpoint touches this field — it is absent from `FeatureFlagUpdateRequest`'s schema entirely, a validation-layer omission, not a runtime check that could be forgotten). Rationale: allowing a Super Admin to unilaterally flip a flag from `safety_relevant=true` to `false` would be a one-step bypass of the entire dual-sign-off rule — flip it off, then toggle freely. If a flag was genuinely miscategorized at creation, the correct fix is archiving it and creating a new, correctly-categorized flag with a new key — an intentionally heavier path, and the only one that keeps the audit trail honest.

### 9.3 Elevated-session (2FA step-up) requirements

`propose` (safety-relevant only), `approve`, `reject`, and `kill-switch` all require an `elevatedToken` obtained via the existing `useElevatedSession()`/`requestElevation()` flow — identical to the existing `useDeleteFamily()` high-risk-action pattern (`NEXT-JS-INSTRUCTIONS.md` §15's full example). Backend-side, this consumes an admin-scoped elevated-session dependency in `core/deps.py`: `require_elevated_admin(admin_ctx: AdminSessionContext, redis)`, built following the exact same shape as the existing `require_elevated_session(parent, redis)` (documented for the parent app, Redis-marker-backed step-up verification) but keyed on `AdminSessionContext` instead of `ParentSessionContext`. Since the Admin Portal's `useElevatedSession`/`requestElevation()` (backed by `API_ENDPOINTS.AUTH.ELEVATE`) is already fully implemented, the corresponding backend elevate-token-issuing endpoint already exists; this file's only new backend piece is the *consuming* dependency (`require_elevated_admin`), added additively to `core/deps.py` — confirm the exact existing elevate-endpoint/dependency naming at implementation time and reuse it rather than inventing a second parallel elevation mechanism if one already exists under a different name.

Non-safety-relevant `propose` (which commits immediately to `LIVE`) does **not** require elevation — it is a single Super Admin action with immediate, reversible effect (kill-switch is always available), consistent with the blueprint's own framing of ordinary flags as "Super Admin toggles in Admin Portal" without an approval-gate qualifier.

### 9.4 Validation rules

- `key`: `^[a-z][a-z0-9_]*$`, unique, immutable, max 100 chars.
- `rollout_percentage`: integer, `0 <= n <= 100`. A `BOOLEAN`-type flag's `rollout_percentage` is forced to `0` and ignored at evaluation time (validation rejects a non-zero value on a `BOOLEAN` flag as a `422` — prevents a confusing, meaningless combination from ever being stored).
- `targeting_rules`: Pydantic strict schema — only `age_bands`/`locales`/`subscription_tiers`/`min_app_version` keys accepted, each validated against its own real enum/format (reject unknown keys entirely, per the same "Pydantic strict mode, no request body extensions" discipline B-01 §14 already established).
- `reason_note`: required, min 10 characters, on every `approve`/`reject`/`kill-switch` action against a safety-relevant flag; optional (but still logged if given) for non-safety-relevant actions. Directly mirrors the sibling App Configuration module's rule: *"Every change requires a reason note"* (`NoorHeroes_Consolidated_Blueprint_v6.md` §11.8).
- Attempting to set `rollout_percentage > 0` or `enabled = true` on any state row not currently `LIVE` is rejected at the service layer with `ValidationError` — the only way `enabled`/`rollout_percentage` become "real" is through the state machine in §11, never through a direct field-level `PATCH`.

### 9.5 Audit trail is service-layer, not gateway-layer

Every mutation (`propose`/`approve`/`reject`/`kill-switch`/`archive`) writes one row to `feature_flag_approvals` **and** calls the existing `AdminService.log_action()`/`AdminAuditRepository.log_action()` platform-wide audit path (per `FAST-API-INSTRUCTIONS.md` §5.2), inside the same request-scoped transaction. This dual-write is intentional: `feature_flag_approvals` is the workflow-driving ledger the state machine itself reads (§11); `AdminAuditLog` is the general, cross-cutting query surface already displayed on the Admin Portal's existing Audit Logs page (`NoorHeroes_Consolidated_Blueprint_v6.md` §11.7). Both are audited at the service layer, never only at the gateway, matching the blueprint's explicit invariant: *"Sensitive reads and all mutations are audited at the service layer (not just logged at the gateway, so a compromised gateway cannot suppress the audit trail)"* (§11.6).

## 10. Error Handling and Edge Cases

| Situation | Cause | Resolution |
|---|---|---|
| Flag evaluation fails (Postgres and/or Redis unreachable) | Infra outage | Return the flag's `default_value` (the conservative one — §6.1), `source=BUILD_DEFAULT_FALLBACK`, log a warning. **Never** propagate a 5xx from a single flag's failure; a partial-outage response (some flags `REMOTE`, some `BUILD_DEFAULT_FALLBACK`) is correct and expected, not an error state. |
| Flag key referenced by calling code doesn't exist in the DB | Deploy-order mismatch — code shipped before the flag was registered, or a typo | `evaluate_flag(key, caller_default)` (the in-process backend SDK signature) requires the caller to pass its own fallback; return that fallback and log a warning naming the missing key — this is a developer-facing signal, not a child-facing failure. |
| Kill switch on a live safety-relevant flag | Emergency need to disable | **Always instant, single Super Admin action, no second approver, no elevation wait beyond the OTP itself.** This is a deliberate asymmetry: turning a risky capability **off** must never be slower than turning it **on**. The dual-sign-off gate applies only to `enabled=true`/`rollout_percentage>0` transitions, never to the reverse. Rollback/kill-switch always wins the race against any in-flight approval-pending proposal — killing a `PENDING_SECOND_APPROVAL` proposal (rejecting it outright, distinct from disabling an already-`LIVE` flag) is also a single-Super-Admin action for exactly the same reason. |
| Approver attempts to approve their own proposal | `actor_admin_id == proposed_by_admin_id` | `403 SELF_APPROVAL_FORBIDDEN`. Structural, not a UI-only disabled-button convenience — enforced in `FeatureFlagService`, the same segregation-of-duties pattern as the existing Avatar review workflow. |
| Same admin attempts both required approvals | `actor_admin_id == first_approved_by_admin_id` | `403 DUPLICATE_APPROVER_FORBIDDEN`. Two *distinct* accounts, always. |
| Two approvals arrive from the correct distinct people, but neither is a Super Admin, or neither is a Child Safety Reviewer | Role-pairing rule violated (e.g., two different Super Admins approve, no Child Safety Reviewer involved) | `403 ROLE_PAIRING_REQUIREMENT_NOT_MET` on the second `approve` call — the combined role set of the two approvals must include both required roles, not merely two different people. |
| Two Child Safety Reviewers race to submit the *first* approval simultaneously | Concurrent request | Optimistic locking (`version` column on `feature_flag_environment_states`) — the second concurrent writer receives `409 OPTIMISTIC_LOCK_CONFLICT` and must re-fetch current state and retry against the now-updated row (standard `update_with_optimistic_lock` semantics, per `BaseRepository`). |
| A pending safety-relevant proposal sits unapproved for a long time — the "one approver unavailable" / deadlock scenario | Only one qualified Child Safety Reviewer exists and is on leave, or the org has too few qualifying accounts | Two-part mitigation, both operational not code-bypass: (1) `expire_stale_flag_proposals_task` (§7) sends a reminder at `FEATURE_FLAG_STALE_PROPOSAL_REMINDER_HOURS` (default 48h) via the existing structured-logging/alerting stack, and auto-reverts the proposal to `DRAFT` at `FEATURE_FLAG_STALE_PROPOSAL_EXPIRY_DAYS` (default 14 days) so nothing rots forever in a pending state — a reverted proposal can simply be re-proposed once approvers are available, no data is lost, the audit trail records the expiry as its own `feature_flag_approvals` row; (2) a Prometheus gauge `feature_flag_pending_safety_approvals_count` and `feature_flag_pending_approval_age_seconds` feed a Grafana dashboard widget ("N safety-relevant flags pending > 48h"), per §15. **This is fundamentally a roster/prerequisite issue, not a platform gap** — §16 makes "at least two distinct Super Admin accounts and at least one Child Safety Reviewer account exist and are active" an explicit prerequisite, because no code-level design can safely substitute for a second qualified human when the rule's entire point is requiring one. |
| Proposer's admin account is deactivated after proposing, before either approval lands | Admin offboarding mid-workflow | The pending proposal remains valid and approvable by any other qualified, distinct admin — a deactivated proposer does not need to be "un-proposed." If the proposer is later reactivated, the self-approval rule still applies to their account regardless of the deactivation gap. |
| Unauthenticated evaluate call for a `PERCENTAGE_ROLLOUT` flag, no child/family session | Pre-auth surface (e.g., an intro-screen experiment) | If the client supplies `bucketing_key` (§6.5), bucket against that opaque, client-generated, non-PII identifier. If no `bucketing_key` is supplied either, the flag evaluates to its `default_value` for that call — never guesses/defaults to "included," consistent with the conservative-fallback principle throughout this file. |
| Admin attempts to `PATCH .../propose` with `rollout_percentage > 0` on a `BOOLEAN`-type flag | Type/field mismatch | `422 VALIDATION_ERROR` (§9.4) — rejected before it ever reaches the state machine. |

## 11. State Management and Lifecycle Considerations

### 11.1 States

`DRAFT` → `PENDING_APPROVAL` → `PENDING_SECOND_APPROVAL` → `LIVE` → `ARCHIVED`, plus `REJECTED` as a terminal-per-proposal (not terminal-per-flag) state.

| State | Meaning | Entered via |
|---|---|---|
| `DRAFT` | Environment row exists, no proposal in flight, `enabled=false`. | Flag creation (all environments start here); also the state a `REJECTED` or expired proposal reverts to for its next attempt. |
| `PENDING_APPROVAL` | A safety-relevant proposal has been submitted; **zero** approvals recorded yet. | `propose` on a `safety_relevant=true` flag. |
| `PENDING_SECOND_APPROVAL` | Exactly one qualifying approval recorded; the *second*, distinct, correctly-role-paired approval is still required. | First `approve` on a `PENDING_APPROVAL` row. |
| `LIVE` | The proposed `enabled`/`rollout_percentage`/`targeting_rules` are now the real, evaluation-affecting values. | Second `approve` on a `PENDING_SECOND_APPROVAL` row (safety-relevant lane); or immediately on `propose` (non-safety lane, single-actor). |
| `REJECTED` | A qualifying approver explicitly rejected the proposal. | `reject`, from either `PENDING_APPROVAL` or `PENDING_SECOND_APPROVAL`. Re-proposing starts a fresh `PENDING_APPROVAL` cycle (previous audit rows are never deleted). |
| `ARCHIVED` | Flag (or this environment's state) is retired; no evaluation reads occur, `default_value`/build-default fallback always applies. | `archive`, from any state, at any time. |

### 11.2 Guard summary (enforced in `state_machine.py`, pure functions, exhaustively unit-tested per §14)

- `propose`: allowed from `DRAFT` or `REJECTED` only. Requires `feature_flags:propose`.
- `approve` (first): allowed only from `PENDING_APPROVAL`. Actor must hold `approve_safety` (safety-relevant) or `approve` (non-safety — though non-safety flags never enter this state, so this branch is dead in practice and asserted as such by the invariant test in §14). Actor ≠ `proposed_by_admin_id`.
- `approve` (second): allowed only from `PENDING_SECOND_APPROVAL`. Actor ≠ `proposed_by_admin_id`, actor ≠ `first_approved_by_admin_id`. The **union** of `{first approver's role, second approver's role}` must contain both `SUPER_ADMIN` and `CHILD_SAFETY_REVIEWER` — checked against `actor_role_snapshot` values recorded on both approval rows, not against the admin's *current* role (a role change between the two approvals must not retroactively satisfy or violate the pairing requirement).
- `reject`: allowed from `PENDING_APPROVAL` or `PENDING_SECOND_APPROVAL`. Same role-eligibility as `approve` at that stage. Requires non-empty `reason_note`.
- `kill-switch`: allowed from `LIVE` only (disabling a flag that was never live is a no-op, not an error — return the current, already-off state idempotently). Requires `feature_flags:kill_switch` (Super Admin), single actor, no second-approver check, ever.
- `archive`: allowed from any state. Terminal — no transition leaves `ARCHIVED`.

### 11.3 Rollout percentage changes on an already-`LIVE` safety-relevant flag

Raising `rollout_percentage` on a flag that is already `LIVE` (e.g., 10% → 50%) is treated as a **new proposal** against that environment's row — it re-enters `PENDING_APPROVAL` and requires a fresh two-distinct-approver cycle, because "rollout above 0%" in the source requirement (`NoorHeroes_Final_Development_Prompt.md` §6) is read here as covering *any* increase in exposure, not merely the initial 0%→nonzero transition. *Lowering* rollout (including all the way to 0%, functionally a kill-switch) is always an immediate, single-Super-Admin action, per the same asymmetry principle as §10's kill-switch row.

## 12. Integration Points with Existing Modules

- **Backend `feature_flags` context ↔ every other bounded context:** any future backend logic needing a flag value (e.g., a new AI-safety moderation-strictness check) calls `FeatureFlagService.evaluate_flag(key, context, caller_default)` **in-process** via `Depends(get_feature_flag_service)` — never an HTTP round-trip to its own process's `/v1/feature-flags/evaluate` endpoint. That public endpoint exists for external clients (KMP) only.
- **`core/deps.py`:** additive-only. New factories `get_feature_flag_service()`, and (if not already present under a different name — confirm at implementation time per §9.3) `require_elevated_admin()`. Nothing existing in this file is modified — `get_current_admin`, `require_admin_scope`, `get_optional_parent` are reused verbatim.
- **`AdminService`/`AdminAuditRepository`:** consumed, not modified, per §9.5's dual-write.
- **B-01's `remote_config` singleton table / `RemoteConfigRepository` (backend, `identity` module):** explicitly **not** touched, merged, or extended — see §2's naming-collision warning. The two systems solve different problems (deploy-gate singleton config vs. per-key feature flags) and stay fully decoupled.
- **`core-datastore`'s existing `RemoteConfigRepositoryImpl`:** the single most important KMP integration point. Its `refresh()` method — documented today as a local-state-only stub — gets a real body: call the new `FeatureFlagApiService.evaluateFlags()`, on success write each returned value via the existing `PreferenceManager` using `PreferenceConstants` keys (exactly the module's own documented "Scenario 1: Adding a new Feature Flag" 3-step process, now extended to 4 steps — see §13 step 8), on failure leave DataStore's last-known values untouched (never move the app off its last-known-good or build-default value due to a transient network failure — the *same* conservative principle as the backend's evaluation fallback in §10, applied client-side). `observeFlags()`'s `combine` block and `FeatureFlagDefaults`'s shape are otherwise unchanged.
- **`core-network`'s existing `FeatureFlagProvider`/`FeatureFlag` facade:** per `CORE_NETWORK_INSTRUCTIONS.md` §4, feature modules already call `featureFlagProvider.isEnabled(FeatureFlag.AI_TUTOR)`. Per the existing core-common/core-datastore layering (interfaces in `core-common`, implementations in `core-datastore`), `FeatureFlagProvider` must be reconciled to delegate to `RemoteConfigRepository` under the hood rather than maintaining a second, independent flag-storage path — **if at implementation time `FeatureFlagProvider` is found to have its own divergent implementation, that is a Do-Not-Diverge violation to fix as part of this work, not a design to preserve.** The `FeatureFlag` enum's members should map 1:1 onto `FeatureFlagDefaults`' properties and this file's backend `key` strings (e.g., `FeatureFlag.AI_TUTOR` ↔ `aiTutorEnabled` ↔ backend key `ai_tutor_enabled`).
- **Admin Portal `DashboardShell` navigation:** the new Feature Flags nav entry is wrapped in `<RequirePermission permission="feature_flags:read">`, following the exact existing sidebar-filtering pattern documented in `NEXT-JS-INSTRUCTIONS.md` §2's architecture diagram.
- **CI/CD (`CI_CD.06`):** the new `test_safety_flag_dual_signoff_invariant.py` (§14) is added into the backend's existing "Architectural Invariant Tests" Stage 6 job slot that `CI_CD.06` already wires up — no new CI job, no new YAML, just a new test file dropped into the directory that job already runs (`backend/tests/architectural/`), exactly matching the hand-off design `CI_CD.06` §15 documents for this purpose.

## 13. Development Steps in the Correct Implementation Order

1. Write `state_machine.py`'s pure transition-guard functions and their exhaustive unit tests **first**, before any database/HTTP code — the dual-sign-off logic is the entire point of this file and must be provably correct in isolation before anything is wired around it.
2. Author the Alembic migration for all three tables (§6.1-§6.3, §8). Confirm it runs clean on a fresh DB and does not touch any existing table.
3. Implement `FeatureFlagRepository`/`FeatureFlagEnvironmentStateRepository`/`FeatureFlagApprovalRepository` (`BaseRepository[ModelT]` subclasses) — pure data access, no business rules.
4. Implement `evaluation.py` (`bucket_for`/`is_in_rollout`/`TargetingRuleMatcher`, §3.2) with its own unit tests (deterministic-hash boundary cases, targeting-rule match/no-match).
5. Implement `FeatureFlagService` wiring the state machine (step 1) to the repositories (step 3), including the Redis cache-aside evaluation path with the conservative-fallback behavior from §10, and the dual-write audit path from §9.5.
6. Add `get_feature_flag_service()` and (if not already present) `require_elevated_admin()` to `core/deps.py`.
7. Implement `FeatureFlagsRouter` (public evaluate) and `FeatureFlagAdminRouter` (CRUD + workflow), per §6.5/§6.6. Register both under the existing router-registration convention (`api_v1_router`).
8. Extend `PreferenceConstants`/`FeatureFlagDefaults` (KMP `core-common`) for whichever concrete flags are being seeded initially (e.g., `ai_tutor_enabled`, `ramadan_mode_enabled` already exist as build defaults per `CORE_DATASTORE_INSTRUCTIONS.md` — register matching backend `feature_flags` rows for them so they become genuinely remote-controllable rather than build-default-only).
9. Implement `FeatureFlagApiService` (`core-network`) and wire `RemoteConfigRepositoryImpl.refresh()` to call it (§12). Reconcile `FeatureFlagProvider` to delegate rather than diverge.
10. Implement the Admin Portal `feature-flags` feature module (§5) — list/detail/create/propose/approve/reject/kill-switch UI, approval queue page, audit history panel. Wrap every mutation button in the correct `RequirePermission`, and wire `useElevatedSession`/`requestElevation` into propose (safety-only)/approve/reject/kill-switch exactly per §9.3.
11. Write `test_safety_flag_dual_signoff_invariant.py` (§14) and drop it into `backend/tests/architectural/`, the directory `CI_CD.06`'s Stage 6 job already runs.
12. Write the full unit/integration/API test suites (§14) for `FeatureFlagService`, both routers, and the admin-web hooks.
13. Wire `expire_stale_flag_proposals_task` (§7) as a Celery periodic task and the two Prometheus gauges (§15) into the existing Grafana observability stack.
14. Manually exercise the full happy path end-to-end at least once: create a safety-relevant flag → propose in a non-prod environment → approve as Child Safety Reviewer → approve as Super Admin → confirm `GET /v1/feature-flags/evaluate` reflects `true` → confirm a KMP debug build's `RemoteConfigRepository.observeFlags()` Flow emits the new value after a manual `refresh()` call.

## 14. Testing Strategy and Acceptance Criteria

**The headline acceptance criterion, stated exactly as the task requires:** a safety-relevant flag change is provably blocked until 2 distinct approvers sign off. Concretely, all of the following must hold:

| # | Test | File | Asserts |
|---|---|---|---|
| 1 | `test_safety_flag_cannot_go_live_with_zero_approvals` | `test_state_machine.py` | Attempting to transition `PENDING_APPROVAL` → `LIVE` directly is not a reachable transition in the guard table. |
| 2 | `test_safety_flag_cannot_go_live_with_one_approval` | `test_feature_flag_service.py` | After exactly one valid `approve` call, `lifecycle_state == PENDING_SECOND_APPROVAL`, `enabled` on the row is still `false`/unchanged, and `GET /v1/feature-flags/evaluate` still returns the flag's `default_value`. |
| 3 | `test_safety_flag_goes_live_after_two_distinct_correctly_paired_approvals` | `test_feature_flag_service.py` | Two `approve` calls from two distinct admins, one Super Admin + one Child Safety Reviewer → `lifecycle_state == LIVE`, evaluation now reflects the proposed value. |
| 4 | `test_two_approvals_from_same_role_pairing_rejected` | `test_feature_flag_service.py` | Two distinct Super Admins (no Child Safety Reviewer) → second `approve` raises `403 ROLE_PAIRING_REQUIREMENT_NOT_MET`, state stays `PENDING_SECOND_APPROVAL`. |
| 5 | `test_proposer_cannot_self_approve` | `test_feature_flag_service.py` | `403 SELF_APPROVAL_FORBIDDEN` on both the first and (hypothetically) second approval slot. |
| 6 | `test_same_approver_cannot_approve_twice` | `test_feature_flag_service.py` | `403 DUPLICATE_APPROVER_FORBIDDEN` on the second `approve` from the same account as the first. |
| 7 | `test_non_safety_flag_live_after_single_propose` | `test_feature_flag_service.py` | `safety_relevant=false` flag reaches `LIVE` immediately on `propose`, no approval calls needed. |
| 8 | `test_evaluation_returns_safe_default_on_db_outage` | `test_feature_flag_service.py` | Mocked repository raising → evaluation returns `default_value`/`BUILD_DEFAULT_FALLBACK`, no exception propagates. |
| 9 | `test_evaluation_returns_safe_default_on_redis_outage` | `test_feature_flag_service.py` | Same, with Redis client raising, Postgres still reachable — falls through to a direct DB read, still succeeds. |
| 10 | `test_kill_switch_bypasses_dual_signoff` | `test_feature_flag_service.py` | Single Super Admin call on a `LIVE` safety-relevant flag → immediately `enabled=false`, no approval rows required for this specific action. |
| 11 | `test_rollout_increase_on_live_flag_requires_fresh_dual_signoff` | `test_feature_flag_service.py` | Raising `rollout_percentage` on an already-`LIVE` safety-relevant flag re-enters `PENDING_APPROVAL`, requiring a fresh two-approver cycle (§11.3). |
| 12 | `test_stale_proposal_expires_and_reverts_to_draft` | `test_feature_flag_service.py` (or a dedicated Celery-task test) | A `PENDING_APPROVAL`/`PENDING_SECOND_APPROVAL` row older than `FEATURE_FLAG_STALE_PROPOSAL_EXPIRY_DAYS` is reverted to `DRAFT` by `expire_stale_flag_proposals_task`, with an audit row recording the expiry. |
| 13 | `test_safety_flag_dual_signoff_invariant` (**CI-blocking architectural test**) | `backend/tests/architectural/test_safety_flag_dual_signoff_invariant.py` | Scans the live database state (or a seeded fixture DB in CI): for every `feature_flags` row with `safety_relevant=true` whose current environment state is `LIVE`, its `feature_flag_approvals` audit trail contains **at least 2 rows with `action=APPROVED`, from 2 distinct `actor_admin_id` values, whose `actor_role_snapshot` values collectively include both `SUPER_ADMIN` and `CHILD_SAFETY_REVIEWER`**. This is the exact same pattern as the existing CI-blocking architectural tests named in `NoorHeroes_Final_Development_Prompt.md` §5 (JWT-schema-singularity, gateway-authorization-zero) — a required, separately-named status check, distinct from a generic "tests failed" signal, run in `CI_CD.06`'s Stage 6 job. |
| 14 | `test_kill_switch_admin_permission_enforced` | `test_feature_flag_admin_api.py` | A non-Super-Admin token (e.g., Content Editor) hitting the kill-switch endpoint gets `403`, proving `RequirePermission`'s server-side backing (never client-UI-only). |
| 15 | Admin-web: `approve` button is disabled (not hidden) when `admin.adminId === proposal.proposedByAdminId` | Component test | UX convenience only — confirms the client renders the constraint but does not claim it enforces it (backend tests 5/6 are the actual enforcement proof). |
| 16 | KMP: `RemoteConfigRepositoryImpl.refresh()` failure path | `RemoteConfigRepositoryImplTest` (mobile) | A failed `FeatureFlagApiService` call leaves previously-persisted `PreferenceManager` values untouched — `observeFlags()` does not emit a value regression to build defaults on a transient network blip. |

**Coverage gate:** `feature_flags/service.py` and `state_machine.py` must hit the existing `≥80% domain/ service-layer` backend coverage gate (`NoorHeroes_Final_Development_Prompt.md` §5) with, additionally, **100% branch coverage specifically on the approval-role-pairing and self/duplicate-approver guard logic** — this is the one piece of this file where a missed branch is a real child-safety bypass, not a generic quality gap.

**Definition of "acceptance":** all 16 checks pass in CI, check #13 is registered as a required, separately-named status check (not folded into a generic "tests" job), and a reviewer who has not seen this file can reproduce check #13's failure by manually seeding a `LIVE` safety-relevant flag with only one (or zero, or wrongly-paired) approval rows and confirming the test — and only the test — catches it.

## 15. Production-Readiness Considerations

- **Cache invalidation on mutation is not optional.** `approve` (final), `reject`, and especially `kill-switch` must actively bust the Redis cache-aside entry for `(flag_key, environment)` synchronously, in the same request, before returning success — a kill switch that only takes effect after a 30-second TTL expiry is not a kill switch for a live child-safety incident. This is stated explicitly here because it is exactly the kind of correctness requirement that "works in the happy-path demo" without a synchronous invalidation call and then quietly fails the one time it actually matters.
- **Alerting:** a `kill_switch` action taken against a safety-relevant flag in `production` pages a human (P0/P1 routing via the existing Slack/PagerDuty on-call mechanism, per `NoorHeroes_Final_Development_Prompt.md` §8's alerting table) — someone needs to know *why* it was pulled, immediately, not discover it in a weekly report. Add this trigger to the existing P0 list alongside the already-named gateway-authorization-anomaly/refresh-token-reuse/backup-restore-failure triggers.
- **Dashboard widgets:** `feature_flag_pending_safety_approvals_count` and `feature_flag_pending_approval_age_seconds` (§10) surface on the existing "Security Posture Dashboard" (`NoorHeroes_Final_Development_Prompt.md` §8's observability table) alongside MFA compliance and pen-test finding disposition — this platform's own health (are safety approvals moving, or backlogged) is itself a security-posture signal.
- **Disaster recovery:** on a full-environment Postgres restore, feature flags resume exactly from the last backed-up committed state; because evaluation always falls back to `default_value` on any read failure (§10), the restore window itself never produces an unsafe evaluation result — at worst, flags temporarily behave as if never enabled.
- **This file introduces zero deploy/infra coupling** — no new container, no new managed service, no Terraform change. The new tables live in the existing managed Postgres instance; the new cache entries live in the existing managed Redis instance.

## 16. Dependencies and Prerequisites

- Completion of Phase 1 item 06 (`CI_CD.06`) — specifically, its per-app "Architectural Invariant Tests [PLACEHOLDER]" Stage 6 job must exist for this file's `test_safety_flag_dual_signoff_invariant.py` to have a CI slot to run in.
- The Security Baseline (`NoorHeroes_Final_Development_Prompt.md` §9) must already be live — this file's admin elevation dependency (§9.3) assumes the canonical JWT claim schema, refresh-token rotation, and MFA/passkey enforcement for every admin account are already in place; it adds no new auth primitive of its own.
- **Operational prerequisite, not a code dependency:** at least two distinct, active Super Admin accounts and at least one active Child Safety Reviewer account must exist before any safety-relevant flag work begins, or the dual-sign-off rule is unsatisfiable by construction for that org roster. This is a people/process precondition this file's design assumes and §10's deadlock-mitigation row depends on — flag it explicitly to whoever provisions the first admin accounts (per §9's Security Baseline item 8, MFA-enforced from the very first admin user created).
- `B-01`'s bootstrap endpoint and `RemoteConfigRepository` (backend, `identity` context) — referenced only to establish the naming-collision boundary in §2; no functional dependency.

## 17. Definition of Done

- [ ] All three tables (§6.1-§6.3) exist via one additive-only migration; `feature_flag_approvals` has zero `UPDATE`/`DELETE` grant at the DB-role level.
- [ ] `state_machine.py`'s guard functions exist as pure, unit-testable functions with 100% branch coverage on the approval-pairing/self-approval/duplicate-approver logic (§14).
- [ ] `FeatureFlagService`, both routers, and all repository classes exist per §5, following `BaseService`/`BaseRepository`/`OutboxWriter`/`DomainError` conventions with zero deviation from the layer rules in `FAST-API-INSTRUCTIONS.md` §11.
- [ ] `GET /v1/feature-flags/evaluate` is live, documented in OpenAPI, rate-limited (120/min/IP), and never returns a 5xx due to a single flag's evaluation failure (§10).
- [ ] The full admin API (§6.6) is live, every mutating endpoint enforces the correct `RequirePermission`-equivalent server-side scope **and** elevated-session requirement per §9.3, verified by test #14.
- [ ] `test_safety_flag_dual_signoff_invariant.py` exists, passes, is registered as a required, separately-named CI status check, and is proven to actually catch a deliberately-seeded violation (§14's acceptance definition).
- [ ] All 16 tests in §14 pass in CI.
- [ ] Admin Portal `feature-flags` module is live, navigable only via `RequirePermission`-guarded nav entry, and every high-risk action routes through `useElevatedSession`/`requestElevation` exactly like the existing `useDeleteFamily` pattern.
- [ ] `RemoteConfigRepositoryImpl.refresh()` performs a real network call, reconciles results via the existing `PreferenceManager`/`FeatureFlagDefaults` mechanism, and never regresses a cached value to a build default on a transient network failure (test #16).
- [ ] `FeatureFlagProvider` (core-network) delegates to `RemoteConfigRepository` — confirmed not to maintain a second, divergent flag-storage path.
- [ ] Kill-switch alerting (§15) and the two pending-approval Prometheus gauges are wired into the existing observability stack.
- [ ] `expire_stale_flag_proposals_task` is registered as a Celery periodic task and covered by test #12.
- [ ] No change was made to `B-01`'s `remote_config` table/`RemoteConfigRepository` (identity context), any of the 12 existing bounded contexts' own tables, the existing nine RBAC roles' definitions, or any file owned by `CI_CD.06`'s workflow YAML (only a new test file was added into its already-wired directory).

## 18. Assumptions or Decisions the Coding Agent Must Follow

1. **Build vs. buy: in-house `feature_flags` table + Admin Portal UI, not a managed vendor (LaunchDarkly) or self-hosted platform (Unleash/Flagsmith).** `NoorHeroes_Final_Development_Prompt.md` §14 leaves this explicitly open; this file resolves it in-house, for four concrete reasons specific to this product's stage and this rule's shape:
   - **The dual-sign-off rule with a specific two-role pairing (Super Admin + Child Safety Reviewer) is a custom domain rule no off-the-shelf flag tool models natively.** Building it as a first-class state machine inside our own service layer means it is covered by our own architectural CI-blocking test suite (§14) the exact same way the JWT-schema/gateway-authorization/upload-pipeline invariants already are — a vendor's "approval workflow" plugin (where one exists at all) would live outside that test/audit boundary, and proving compliance for a child-safety audit against a third party's opaque workflow engine is strictly harder than proving it against our own, fully-inspectable state machine and append-only ledger.
   - **No new vendor dependency, cloud egress, or compliance surface.** Targeting rules can reference age-band data; keeping flag evaluation entirely inside infrastructure we already control (Postgres/Redis) avoids exporting any config that touches child-safety context to a third party, and avoids adding a vendor to the SOC2/compliance review surface for a startup-stage product that has not yet needed one for this purpose.
   - **Zero incremental cost** at a stage where per-seat/per-MAU vendor pricing (LaunchDarkly) is a real, avoidable line item before revenue is validated — directly consistent with this document's own general vendor-minimization stance (e.g., §7's "do not self-host Redis without a strong operational reason" cuts the *other* way, but the underlying logic — minimize new operational surface area until scale demands otherwise — is the same).
   - **The schema in §6 is intentionally close to Unleash's/Flagsmith's own concepts** (flag/key/environment/targeting-rules/percentage-rollout) specifically so a future migration to a managed tool, if traffic or team size ever justifies it, is a data-migration exercise, not a rewrite — matching this project's established "start simple, migrate when scale justifies it" pattern (e.g., Cloud Run before Kubernetes, per §7 of the source document).
2. **`GET /v1/feature-flags/evaluate` returns the full flag map on every call, not a per-key lookup endpoint.** The KMP client's refresh cadence (periodic + app-launch) makes a bulk fetch strictly simpler and cheaper than N per-key round trips, and matches the shape `RemoteConfigRepositoryImpl.observeFlags()`'s `combine` block already expects (a full `FeatureFlagDefaults` snapshot, not incremental deltas).
3. **`safety_relevant` is a boolean set once at creation, never a per-environment or per-proposal setting.** A flag is either the kind of thing that needs dual sign-off everywhere it can go live, or it isn't — allowing it to vary by environment (e.g., "safety-relevant in production but not staging") would create exactly the kind of loophole (test the risky config in staging without governance, then flip a per-environment flag before promoting) this rule exists to prevent.
4. **Kill-switch bypassing dual-sign-off is a deliberate, load-bearing design decision, not an oversight — do not "fix" it by adding a second-approver requirement to the disable path.** Re-read §10's asymmetry principle before touching this logic; a slower kill switch is a worse safety posture, not a more rigorous one.
5. **Non-safety-relevant flags never enter `PENDING_APPROVAL`/`PENDING_SECOND_APPROVAL` at all** — `propose` commits them directly to `LIVE`. Do not add an approval step for non-safety flags "for consistency"; the source requirement is explicit that dual sign-off applies only to flags affecting child-facing safety behavior, and adding unneeded friction to ordinary flags (dark mode, layout experiments) would undermine the platform's usability for the common case without any safety benefit.
6. **Do not implement a code-level "break-glass" bypass for the two-distinct-approver rule**, even for emergencies — the kill-switch path (§10, item 4 above) already covers the one emergency case that matters (turning something risky *off* fast). An emergency need to turn something risky *on* fast without a second qualified approver is not a scenario this platform should make technically possible; if it ever becomes a genuine business need, that is an explicit, deliberate, documented policy decision for a future revision of this file, not an implementation detail to improvise.
7. **`FeatureFlagProvider`'s reconciliation to `RemoteConfigRepository` (§12) takes priority over preserving whatever its current implementation happens to be**, if the two are found to diverge at implementation time. Two independent flag-storage paths on the client is a strictly worse outcome than a one-time refactor of an already-existing, apparently-thin facade.

---

## AI Agent Development Prompt

Implement the NoorHeroes feature-flag platform — backend storage/evaluation, Admin Portal management UI, and KMP client wiring — with a server-side-enforced dual-sign-off rule for safety-relevant flags, exactly as specified in this document. The backend's 12 existing bounded contexts, the Admin Portal's nine-role RBAC/`RequirePermission`/`useElevatedSession` mechanism, and the KMP app's `core-datastore`/`core-network`/`core-common` modules already exist and work — you are adding a new backend context, a new admin module, and finishing an existing client-side stub, not rebuilding any of that.

**What to build, and exactly where:**
1. Backend: new `src/noorheroes/modules/feature_flags/` bounded context — `models.py`, `schemas.py`, `repository.py`, `evaluation.py`, `state_machine.py`, `service.py`, `api.py`, `admin_api.py` — per §5's folder structure and §6's schemas/contracts. Start with `state_machine.py` and its unit tests (§13 step 1) before any database or HTTP code.
2. Backend: one additive-only Alembic migration creating `feature_flags`, `feature_flag_environment_states`, `feature_flag_approvals` per §6.1-§6.3/§8.
3. Backend: `core/deps.py` additions — `get_feature_flag_service()`, and `require_elevated_admin()` if an equivalent admin-scoped elevation dependency doesn't already exist under a different name (confirm before adding a duplicate).
4. Backend: `backend/tests/architectural/test_safety_flag_dual_signoff_invariant.py` — the CI-blocking test from §14 #13. This is the single most important file in this entire implementation; it is what makes the dual-sign-off rule provably unbypassable rather than merely documented.
5. Admin Portal: new `src/features/feature-flags/` module (API client, hooks, components) plus `src/app/(dashboard)/feature-flags/` pages, per §5. Every mutation wrapped in the correct `RequirePermission` permission string from §9.1, every high-risk action (propose-safety/approve/reject/kill-switch) routed through `useElevatedSession()`/`requestElevation()` exactly like the existing `useDeleteFamily` pattern documented in `NEXT-JS-INSTRUCTIONS.md` §15.
6. KMP: new `core-network` `FeatureFlagApiService` (Ktor, following the `AuthApiService` naming/structure pattern); modified `core-datastore` `RemoteConfigRepositoryImpl.refresh()` to call it and reconcile via the existing `PreferenceManager`; reconciled `core-network` `FeatureFlagProvider` to delegate to `RemoteConfigRepository` rather than diverge (§12).

**Conventions to follow — do not substitute:**
- Backend layering is strictly Router → Service → Repository → PostgreSQL. No database access in either router. No `session.commit()` outside the request-scoped transaction lifecycle. Every error is a `DomainError` subclass, never a naked `HTTPException`, per `FAST-API-INSTRUCTIONS.md` §11.
- The dual-sign-off rule is exactly: for `safety_relevant=true` flags, **2 distinct admin accounts**, neither equal to the proposer, whose combined `actor_role_snapshot` values across both approvals include **both** `SUPER_ADMIN` and `CHILD_SAFETY_REVIEWER`. Do not implement "any 2 approvers" without the role-pairing check — that is a materially weaker rule than the one this file specifies.
- The `safety_relevant` boolean is set once at flag creation and is never editable afterward — no `PATCH` field, no admin override, no exception.
- Kill-switch (disable only) is always a single-actor, immediate, elevation-required-but-not-second-approver-required action, on both `LIVE` flags and pending proposals. This asymmetry is intentional (§10, §18 item 4) — do not "fix" it into requiring dual sign-off to turn something off.
- Every flag evaluation failure (missing key, DB down, Redis down) returns the flag's conservative `default_value`, never a 5xx and never a guess toward "enabled." This applies identically on the backend (§10) and on the KMP client (§12 — `refresh()` failure never regresses a cached value).
- No new third-party dependency, anywhere, in any of the three apps (§7). If implementation reveals a genuine need for one, that is a decision to surface explicitly, not to make silently.

**What NOT to change:**
- Any of the 12 existing backend bounded contexts' own models/services/routers, `AdminSessionContext`/`ParentSessionContext`/`ChildSessionContext`, `require_admin_scope`, `BaseService`, `BaseRepository`, `OutboxWriter`.
- B-01's `remote_config` singleton table or its `RemoteConfigRepository` class (backend, `identity` module) — a different system with a colliding name; do not merge, extend, or rename either side to "resolve" the collision.
- The existing nine RBAC roles' definitions or scope descriptions — only new *permission strings* are added (§9.1), no new role, no change to what Child Safety Reviewer or Super Admin already mean elsewhere in the system.
- `RemoteConfigRepository`'s existing interface signature (KMP `core-common`) or `FeatureFlagDefaults`'/`FlagSource`'s existing shape — extend with new properties as flags are added, never break the existing contract other feature modules already depend on.
- `CI_CD.06`'s workflow YAML — the new architectural test is a new file dropped into an already-wired directory, not a new CI job.

**How to verify you're done (walk through all of these before considering the task complete):**
1. Run every test in §14's table; confirm all 16 pass, with special attention to #13 (seed a `LIVE` safety-relevant flag with only one approval row directly against a test DB fixture and confirm the architectural test — and only that test — flags it).
2. Manually exercise the full happy path end-to-end (§13 step 14): create a safety-relevant flag → propose in staging → approve as a Child Safety Reviewer account → approve as a Super Admin account (or vice versa — order doesn't matter) → confirm `GET /v1/feature-flags/evaluate` now returns the enabled value → confirm a KMP debug build's `RemoteConfigRepository.observeFlags()` Flow emits the update after calling `refresh()`.
3. Attempt every blocked path manually at least once and confirm the exact error code from §10's table: self-approval, duplicate-approver, wrong role pairing, non-elevated-session mutation attempt, rollout-percentage-on-boolean-flag.
4. Confirm the kill-switch path: with a flag `LIVE` and enabled, a single Super Admin action (with OTP elevation, no second approver) disables it, and `GET /v1/feature-flags/evaluate` reflects the disabled state within the same request cycle (cache actively busted, not waiting on TTL — §15's non-negotiable requirement).
5. Confirm `feature_flags:read`-only accounts (e.g., a Content Editor token) can see the flag list but every mutating endpoint returns `403`, proving server-side enforcement independent of what the Admin Portal UI happens to render.
