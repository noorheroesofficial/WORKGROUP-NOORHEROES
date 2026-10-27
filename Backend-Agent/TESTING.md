# NoorHeroes Backend — Testing Strategy & Comprehensive Guide

> [!NOTE]
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
>
> For the latest unified developer testing instructions and static analysis commands, also refer to [`NoorHeroes-Backend/MASTER-README.md`](../NoorHeroes-Backend/MASTER-README.md#9-testing-strategy--test-execution) and [`NoorHeroes-Backend/FAST-API-INSTRUCTIONS.md`](../NoorHeroes-Backend/FAST-API-INSTRUCTIONS.md).

This document outlines the testing architecture, suites, conventions, and operational verification commands for the **NoorHeroes Backend API Service**, covering **4,900 automated test cases across 339 test files** in 14 Bounded Contexts.

---

## 1. Testing Philosophy & Invariants

NoorHeroes enforces a **Zero-Drift, Fail-Closed, Layer-Pure Testing Architecture**:
1. **Automated Architectural Invariants**: AST-based tests guarantee domain isolation, repository/service purity, dependency injection rules, and logging/settings centralization.
2. **Mandatory Non-Bypassable Secret Scanning**: Verified Gitleaks custom rules and TruffleHog CI checks prevent token or credential leakage into git history.
3. **1:1 Configuration Contract Synchronization**: Automated drift detection guarantees `.env.example` templates, environment tiers, and Pydantic `Settings` models never diverge.
4. **Child Safety & Privacy Verification**: Structured logging processors and session token validators are tested against PII leakage, scope escalation, and sibling data leakage.
5. **Idempotency & Monotonic Security**: Every mutating endpoint (purchases, completions, locks, withdrawals, unlocks) is validated for idempotency, concurrent safety, and monotonic progression.

---

## 2. Complete Test Suite Directory Structure (339 Test Files, 4,900 Tests)

```
tests/
├── conftest.py                             # Root test session fixtures, test DB, Redis & HTTP clients
├── test_bump_android_version.py            # Android version bumping script verification
├── test_bump_backend_version.py            # Backend version bumping script verification
├── admin/                                  # Administrative API verification tests (3 files)
│   ├── test_badge_admin_api.py             # Admin badge definition endpoints
│   ├── test_challenge_admin_api.py         # Admin challenge & mission scheduler
│   └── test_xp_rule_admin_api.py           # Admin XP rule configuration
├── api/v1/                                 # Top-level API router registration & assembly (2 files)
│   ├── test_api_endpoints.py               # Comprehensive endpoint routing & mount validation
│   └── test_routing.py                     # Route registration & prefix verification
├── architectural/                          # Deep architectural invariant rules (2 files)
│   ├── test_jwt_schema_singularity.py      # Assertion of single canonical JwtClaims model
│   └── test_safety_flag_dual_signoff_invariant.py # DB-level safety flag dual sign-off
├── architecture/                           # Static analysis & boundary isolation tests (24 files)
│   ├── _ast_utils.py                       # AST inspection helper utilities
│   ├── test_ast_utils.py                   # AST helper unit tests
│   ├── test_base_repository_service.py     # BaseRepository & BaseService contracts
│   ├── test_cicd_config.py                 # CI/CD and Dockerfile configuration
│   ├── test_cicd_pipeline.py               # CI stage pipeline integrity
│   ├── test_db_config.py                   # Async SQLAlchemy pool & session lifecycle
│   ├── test_domain_service_reverification_under_simulated_gateway_bypass.py # Gateway bypass safety
│   ├── test_environment_tiers.py          # 4-tier environment safety bypass guards
│   ├── test_exception_handling.py          # Standardized error envelopes & hierarchy
│   ├── test_gateway_purity.py              # Controller purity & DI tests
│   ├── test_gateway_zero_authorization.py  # Zero business authorization in gateway
│   ├── test_layering.py                    # DDD bounded context layering & forbidden imports
│   ├── test_logging_centralization.py      # Centralized logging usage across codebase
│   ├── test_no_fast_hash_in_credential_path.py # AST verification of zero fast hashes for auth
│   ├── test_observability_bootstrap.py     # Metrics, Prometheus & OpenTelemetry architectural setup
│   ├── test_production_deploy_pipeline.py  # Production rolling deployment & gate pipeline tests
│   ├── test_reward_rule_immutability.py    # AST & DB assertion of immutable reward rule versions
│   ├── test_schema_conventions.py          # Pydantic v2 extra="forbid" and camelCase rules
│   ├── test_settings_centralization.py     # Centralized Settings usage across codebase
│   ├── test_shared_utilities.py            # Shared money/clock utilities tests
│   ├── test_single_jwt_schema.py           # Verification of unified JwtClaims schema
│   ├── test_terraform_baseline.py          # Terraform IaC staging baseline & WAF tests
│   ├── test_testing_infrastructure.py      # Autouse override isolation & Testcontainers
│   └── test_transactional_outbox.py        # Outbox pattern and relay integrity tests
├── common/                                 # Shared core security and utilities tests (5 files)
│   ├── test_child_scope_verifier.py        # Child scope extraction and verification
│   ├── test_credential_hasher.py           # Argon2id password hashing
│   ├── test_semver_compare.py              # Semantic version comparison utility
│   ├── security/
│   │   └── test_encrypted_column.py        # AES-256-GCM encrypted column type tests
│   └── utils/
│       └── test_age_band_calculator.py     # Child age band classification
├── core/                                   # Core application infrastructure tests (13 files)
│   ├── test_deps.py                        # Dependency injection provider tests
│   ├── test_docker_compose_local_dev.py    # Local docker-compose configuration
│   ├── test_edge_cases_production.py       # Production edge cases & fail-safes
│   ├── test_exceptions.py                  # Core exception handler tests
│   ├── test_jwt_claims_schema.py           # JwtClaims validation & serialization
│   ├── test_languages_configuration.py     # Canonical 4-language registry & RTL support
│   ├── test_logging.py                     # Structlog logging format & keys
│   ├── test_media_types_standardization.py # Centralized media types & upload constraints
│   ├── test_middleware_stack.py            # Full HTTP middleware stack execution
│   ├── test_require_elevated_admin_session.py # Admin step-up PIN session elevation
│   ├── test_secrets_bootstrap.py           # GCP Secret Manager bootloader
│   ├── test_sentry_post_deploy_watch.py    # Sentry release health & deployment monitoring
│   └── test_settings.py                    # Typed Pydantic Settings validation
├── domain/                                 # Domain-specific logic unit tests (4 files)
│   ├── identity/
│   │   └── test_identity_child_profile.py  # Child profile domain logic & PIN step-up
│   └── localization/
│       ├── test_ai_providers.py            # Pluggable AI translation provider integration
│       ├── test_country_resolution.py      # IP & Header country resolution
│       └── test_localization_service.py    # Translation caching & validation
├── factories/                              # Synthetic test data factories (6 files)
│   ├── child_profile_factory.py            # Child profile synthetic data generator
│   ├── feature_flag_factory.py             # Feature flag synthetic data generator
│   ├── subscription_factory.py             # Subscription tier synthetic data generator
│   ├── user_factory.py                     # User & family synthetic data generator
│   └── test_factory_drift.py               # Model vs factory drift verification
├── infrastructure/                         # Infrastructure integration tests (3 files)
│   ├── test_multidimensional_rate_limiting.py # Multi-dimensional rate limit enforcement
│   ├── test_rate_limit_bypass_resistance.py   # Resistance against header spoofing
│   └── oauth/
│       └── test_google_oauth_verifier.py   # Google OAuth token verification
├── integration/                            # Cross-module integration tests (1 file)
│   └── test_preview_reward_isolation.py    # Admin preview session reward bypass isolation
├── media/                                  # Media upload pipeline tests (4 files)
│   ├── test_upload_pipeline_api.py         # 11-step media upload validation endpoints
│   ├── test_upload_pipeline_ordering.py    # Step ordering & dependency verification
│   ├── test_upload_pipeline_source_agnostic.py # Storage agnostic upload handling
│   └── test_upload_pipeline_steps.py       # Magic bytes, virus scan, and metadata validation
├── modules/                                # Bounded Context Test Suites
│   ├── access_gate/                        # Child Lock & Parental Access Gate (8 files)
│   │   ├── test_lock_api.py                # Lock, unlock, and challenge REST endpoints
│   │   ├── test_lock_repository.py         # Lock state & lockout tracking queries
│   │   ├── test_lock_service.py            # Argon2id PIN verification & lockout backoff
│   │   ├── test_recovery_api.py            # Parent PIN reset & recovery endpoints
│   │   ├── test_recovery_service.py        # Email/SMS recovery challenge flow
│   │   ├── test_session_api.py             # Child session elevation & token minting
│   │   ├── test_session_service.py         # Session expiration & device binding
│   │   └── test_sibling_isolation.py       # Strict cross-sibling profile data isolation
│   ├── admin/                              # Administration & CMS Back-Office (20 files)
│   │   ├── test_admin_deps.py              # Admin RBAC scope enforcement dependencies
│   │   ├── test_admin_service.py           # Audit logging & admin session management
│   │   ├── test_bedtime_analytics_api.py   # Bedtime configuration & ritual analytics API
│   │   ├── test_bedtime_analytics_privacy.py # Privacy boundary & PII exclusion leak detection
│   │   ├── test_compute_onboarding_rollups_task.py # Celery onboarding metrics task
│   │   ├── test_consent_audit_api.py       # COPPA/GDPR consent audit trail API
│   │   ├── test_consent_audit_service.py   # Consent ledger query service
│   │   ├── test_gate_health_api.py         # Parental gate health & telemetry endpoints
│   │   ├── test_lockout_support_api.py     # Customer support PIN lockout override API
│   │   ├── test_onboarding_analytics_api.py # Onboarding conversion funnel API
│   │   ├── test_onboarding_analytics_repository.py # Funnel metrics aggregation
│   │   ├── test_onboarding_analytics_service.py # Onboarding dropout analysis
│   │   ├── test_preview_session_api.py     # Admin content preview token endpoints
│   │   ├── test_preview_session_service.py # Ephemeral preview token minting
│   │   ├── test_remote_config_admin_api.py # Dynamic remote configuration CMS API
│   │   ├── test_remote_config_write_repository.py # Remote config audit & versioning
│   │   ├── test_remote_config_write_service.py # Remote config rollout service
│   │   ├── test_risk_review_api.py         # AI content safety flagged review API
│   │   ├── test_risk_review_service.py     # Content risk assessment service
│   │   └── test_xp_rule_admin_api.py       # Administrative XP rule editor API
│   ├── ai_safety/                          # Islamic Content Moderation & AI Safety (7 files)
│   │   ├── test_ai_safety_api.py           # Safety evaluation & moderation API
│   │   ├── test_ai_safety_service.py       # Heuristic & LLM safety checks
│   │   ├── test_moral_review_api.py        # Scholar moral review queue API
│   │   ├── test_moral_review_service.py    # Moral review approval & rejection workflow
│   │   ├── test_moral_summary_api.py       # Moral takeaway generation API
│   │   ├── test_moral_summary_chaos.py     # Downstream LLM failure & fallback chaos
│   │   └── test_moral_summary_service.py   # Confidence-gated moral summary selection
│   ├── avatars/                            # Avatar System & Content Governance (16 files)
│   │   ├── test_admin_avatar_base_library.py # Base character CRUD & onboarding toggle
│   │   ├── test_admin_avatar_base_zero_missing_scenarios.py # Base boundary & sanitization matrix
│   │   ├── test_admin_avatar_item_catalog.py # Catalog item creation, update, and retirement
│   │   ├── test_admin_avatar_zero_missing_scenarios.py # Zero-missing scenario coverage for items
│   │   ├── test_admin_catalog_100_coverage.py # Exhaustive branch and error coverage
│   │   ├── test_avatars_zero_missing_scenarios.py # Avatar system edge cases
│   │   ├── test_child_inventory_api.py     # Child inventory viewing, ownership, and equip
│   │   ├── test_equip_ownership_validation.py # Ownership validation before equip
│   │   ├── test_modesty_review_workflow.py # Approval, rejection, draft-reset, audit logs
│   │   ├── test_modesty_review_zero_missing_scenarios.py # Dual routes, RBAC, Unicode/Arabic notes, state machine conflicts
│   │   ├── test_one_equipped_per_slot.py   # Equipping unequips prior item in same slot
│   │   ├── test_retire_not_delete.py       # Retired items preserve child ownership
│   │   ├── test_review_segregation_of_duties.py # P0 self-approval/rejection forbidden
│   │   ├── test_unlock_evaluation_engine.py # Unlock criteria evaluation engine
│   │   ├── test_unlock_idempotency.py      # Idempotent unlock evaluations
│   │   └── test_unlock_rule_validation.py  # Unlock rule structure and validation
│   ├── bedtime/                            # Bedtime Mode & Sleep Timer Configuration (5 files)
│   │   ├── test_bedtime_config_api.py      # Bedtime config REST API & authorization gates
│   │   ├── test_bedtime_config_service.py  # Midnight-crossing windows & safe-defaults
│   │   ├── test_bedtime_config_sqlite_integration.py # SQLite DB dialect integration
│   │   ├── test_bedtime_ritual_status_api.py # Bedtime ritual status API, i18n & safe-defaults
│   │   └── test_bedtime_session_log_service.py # Session log service, SQLite upsert & hook isolation
│   ├── common/                             # Shared Domain Repositories & Base Interfaces (1 file)
│   │   └── test_domain_repositories.py     # Domain repository interfaces & contracts
│   ├── content/                            # Stories, Episodes & Content Catalog (21 files)
│   │   ├── test_admin_content_api.py       # Story & episode CMS editor endpoints
│   │   ├── test_admin_content_service.py   # Versioned episode draft/publish workflow
│   │   ├── test_bedtime_manifest_extension.py # Bedtime audio manifest extension & degradation
│   │   ├── test_choice_api.py              # Interactive choice recording endpoints
│   │   ├── test_choice_service.py          # Choice event deduplication & debouncing
│   │   ├── test_completion_api.py          # Story completion & reward trigger API
│   │   ├── test_completion_concurrency.py  # Concurrency safety on double completion
│   │   ├── test_completion_service.py      # Idempotent completion & XP issuance
│   │   ├── test_content_service.py         # Content catalog read service
│   │   ├── test_favorite_api.py            # Child story bookmarking & favorites API
│   │   ├── test_favorite_service.py        # Story favorite toggling & restructuring
│   │   ├── test_listen_count_rounding.py   # Privacy-safe listen count rounding utility tests
│   │   ├── test_playback_api.py            # Playback heartbeat & progress endpoints
│   │   ├── test_playback_service.py        # Monotonic position & scrub gaming detection
│   │   ├── test_silent_completion_parity.py # Silent completion reward parity & ritual logging hook
│   │   ├── test_story_catalog_api.py       # Story library & series detail API
│   │   ├── test_story_catalog_service.py   # Category, age-band, and language filters
│   │   ├── test_unlock_engine.py           # Deterministic episode unlock calculation
│   │   ├── test_withdrawal_api.py          # Emergency content withdrawal & restore API
│   │   ├── test_withdrawal_service.py      # Soft-withdrawal, reason tracking & cache invalidation
│   │   └── test_withdrawal_sqlite_integration.py # SQLite DB withdrawal integration
│   ├── feature_flags/                      # Remote Config & Dynamic Feature Flags (8 files)
│   │   ├── test_evaluation.py              # SHA-256 user bucketing & targeting evaluation
│   │   ├── test_feature_flag_admin_api.py  # Flag proposal, dual sign-off, killswitch API
│   │   ├── test_feature_flag_api.py        # Client evaluation endpoints
│   │   ├── test_feature_flag_deps.py       # Flag dependency injection providers
│   │   ├── test_feature_flag_repository.py # Flag, state, approval queries
│   │   ├── test_feature_flag_service.py    # State machine & approval workflow service
│   │   ├── test_state_machine.py           # Flag lifecycle transitions & invariants
│   │   └── test_tasks.py                   # Celery proposal auto-expiry tasks
│   ├── identity/                           # Auth, Onboarding & User Management (20 files)
│   │   ├── test_bootstrap_api.py           # App bootstrap & remote config endpoint
│   │   ├── test_bootstrap_service.py       # Client version check & bootstrap bundle
│   │   ├── test_child_preferences.py       # Child theme, language, and sound settings
│   │   ├── test_child_profile_extended.py  # Child profile avatar, age-band, and limits
│   │   ├── test_consent_api.py             # COPPA consent recording endpoints
│   │   ├── test_consent_immutability.py    # Immutability of recorded legal consent
│   │   ├── test_consent_service.py         # Consent version tracking service
│   │   ├── test_google_auth_api.py         # Google OAuth login & signup API
│   │   ├── test_google_auth_service.py     # ID token verification & user provisioning
│   │   ├── test_identity_repository.py     # User, family, and child queries
│   │   ├── test_identity_service_extended.py # Extended auth, sessions, and recovery
│   │   ├── test_otp_api.py                 # SMS/Email OTP verification API
│   │   ├── test_otp_service.py             # OTP rate limiting, hashing, and verify
│   │   ├── test_pin_api.py                 # Parent PIN setup & change endpoints
│   │   ├── test_pin_service.py             # PIN Argon2id hashing & lockout tracking
│   │   ├── test_pin_verify_api.py          # Parent PIN authentication endpoints
│   │   ├── test_pin_verify_service.py      # Step-up elevation token generation
│   │   ├── test_progress_summary_aggregation.py # Family progress rollup aggregation
│   │   ├── test_refresh_replay_rejected.py # Refresh token replay rejection in Redis
│   │   └── test_refresh_rotation.py        # Single-use refresh token rotation
│   ├── learning/                           # Educational Progress & Quiz Engine (3 files)
│   │   ├── test_learning_service.py        # Learning milestone & quiz attempt logic
│   │   ├── test_story_insights_api.py      # Parent story insights REST API
│   │   └── test_story_insights_service.py  # Completion, quiz, and moral insight rollups
│   ├── localization/                       # Multi-Language Translation System (4 files)
│   │   ├── test_localization_extended.py   # Multi-language translation resolution
│   │   ├── test_localization_repositories.py # Dynamic message translation queries
│   │   ├── test_localization_tasks.py      # Background AI translation Celery tasks
│   │   └── test_translation_cache.py       # SHA-256 translation cache & fallback
│   ├── media/                              # Media Delivery & Offline Manifests (8 files)
│   │   ├── test_download_health_api.py     # Download manifest failure telemetry API
│   │   ├── test_download_health_service.py # Time-series aggregation of download health
│   │   ├── test_download_manifest_api.py   # Offline download manifest generation API
│   │   ├── test_download_manifest_service.py # Unlock-gated download packaging
│   │   ├── test_manifest_api.py            # Stream media manifest delivery API
│   │   ├── test_manifest_service.py        # 15-min Cloudflare R2 signed stream URLs
│   │   ├── test_media_service.py           # S3/R2 storage provider abstraction
│   │   └── test_upload_pipeline.py         # End-to-end 11-step asset ingestion
│   ├── notifications/                      # Mobile Push Notifications (1 file)
│   │   └── test_notifications_service.py   # APNs/FCM payload formatting & quiet hours
│   ├── rewards/                            # Gamification, Badges & Ledger (41 files)
│   │   ├── test_achievements_api.py        # Achievement progression endpoints
│   │   ├── test_audit_access_logging.py    # Ledger audit access security logging
│   │   ├── test_award_concurrency.py       # Concurrency race safety during reward awards
│   │   ├── test_award_idempotency.py       # Idempotent XP grant deduplication
│   │   ├── test_badge_definition_crud.py   # Admin badge definition management
│   │   ├── test_badge_duplicate_code_rejected.py # Unique badge code invariant
│   │   ├── test_badge_engine.py            # Rule-based badge evaluation engine
│   │   ├── test_badge_retroactive_award.py # Retroactive badge evaluation on criteria change
│   │   ├── test_badge_simulate_no_writes.py # Simulation mode zero-mutation guarantee
│   │   ├── test_badge_stickiness.py        # Permanent badge retention across season change
│   │   ├── test_catalog_admin_crud.py      # Admin store catalog CRUD API
│   │   ├── test_catalog_deactivate_preserves_ownership.py # Deactivation preserves child inventory
│   │   ├── test_challenge_archive_lifecycle.py # Challenge archive & expiry states
│   │   ├── test_challenge_instance_reclaim.py # Expired challenge reclamation
│   │   ├── test_daily_cap_enforcement.py   # Daily XP maximum ceiling enforcement
│   │   ├── test_family_board_api.py        # Family leaderboard endpoints
│   │   ├── test_family_board_no_child_field.py # PII privacy guarantee on leaderboard
│   │   ├── test_family_board_synced_only_aggregation.py # Synced-only aggregation invariant
│   │   ├── test_ledger_append_only_permission.py # DB-level append-only ledger invariant
│   │   ├── test_ledger_audit_viewer_readonly.py # Read-only administrative ledger viewer
│   │   ├── test_mission_schedule_overlap_validation.py # Overlap validation for missions
│   │   ├── test_mission_scheduler_crud.py  # Mission scheduling & recurrence rules
│   │   ├── test_missions_endpoint.py       # Child daily mission list & claims API
│   │   ├── test_no_real_money_purchase_path.py # AST proof of zero fiat purchase paths
│   │   ├── test_purchase_atomicity.py      # Balance deduction & item grant atomicity
│   │   ├── test_purchase_idempotency.py    # Idempotent purchase key deduplication
│   │   ├── test_reconciliation_job.py      # Automated wallet ledger reconciliation
│   │   ├── test_reconciliation_log_readonly.py # Reconciliation incident audit log API
│   │   ├── test_reward_rule_admin_rbac.py  # Admin RBAC on XP reward rule changes
│   │   ├── test_reward_rule_versioning.py  # Versioned immutable reward rule engine
│   │   ├── test_rewards_api.py             # Public child rewards & balance endpoints
│   │   ├── test_rewards_openapi.py         # OpenAPI 3.1.0 schema compliance
│   │   ├── test_rewards_service.py         # Core rewards service & balance computation
│   │   ├── test_rule_version_resolution.py # Deterministic version resolution for rules
│   │   ├── test_seasonal_badge_retention.py # Seasonal badge retention policy
│   │   ├── test_share_card_elevation_gate.py # Parent PIN gate before card generation
│   │   ├── test_share_card_pii_exclusion.py # Zero-PII guarantee on shared achievement cards
│   │   ├── test_share_card_service.py      # Cryptographically signed share card generation
│   │   ├── test_wallet_authorization.py    # Strict family scoping on wallet access
│   │   ├── test_wallet_endpoint.py         # Child wallet balance REST API
│   │   └── test_wallet_projection_rebuild.py # Snapshot rebuild from raw append-only ledger
│   └── subscriptions/                      # Tier Entitlements & Billing (1 file)
│       └── test_subscriptions_service.py   # Tier entitlements & quota calculations
├── scripts/                                # Maintenance & CLI verification tests (1 file)
│   └── test_check_env_example_sync.py      # Automated .env.example synchronization test
├── security/                               # Security baseline & vulnerability scans (3 files)
│   ├── test_gitleaks_rules.py              # Custom Gitleaks regex patterns
│   ├── test_security_baseline.py           # JWT signature verification & Argon2id costs
│   └── test_security_gate.py               # Security gate enforcement & rate limiting
└── smoke/                                  # Deployment & health smoke probes (2 test files)
    ├── conftest.py                         # Smoke test fixtures & --base-url option
    ├── test_smoke_unit.py                  # Unit verification of smoke test fixtures
    └── test_staging_health.py              # Live health probes (/healthz, /readyz, /livez)
```

---

## 3. Quick Execution Commands

### Makefile Targets
```bash
# Run all 4,900 tests in the test suite
make test

# Run fast unit tests (skipping slow integration tests)
make test-fast

# Validate .env.example synchronization and tier consistency
make check-env

# Run local Gitleaks secret detection
make secret-scan

# Run commitlint and configuration drift checks
make lint
```

### Pytest Execution Options
```bash
# Run full suite with verbose output
pytest -v

# Run live staging smoke tests against deployed endpoint
pytest tests/smoke/ --base-url=https://staging.api.noorheroes.com -v

# Run with coverage report
pytest --cov=src/noorheroes --cov-report=term-missing

# Run a specific bounded context test directory
pytest tests/modules/access_gate/ -v
pytest tests/modules/content/ -v
pytest tests/modules/rewards/ -v
pytest tests/modules/identity/ -v
pytest tests/modules/media/ -v
pytest tests/modules/admin/ -v
pytest tests/modules/ai_safety/ -v
pytest tests/modules/feature_flags/ -v
pytest tests/modules/learning/ -v
pytest tests/modules/localization/ -v
pytest tests/modules/notifications/ -v
pytest tests/modules/subscriptions/ -v
pytest tests/modules/bedtime/ -v

# Run architectural invariant tests
pytest tests/architecture/ -v
pytest tests/architectural/ -v

# Run a single test file
pytest tests/modules/content/test_unlock_engine.py -v

# Run a specific test function
pytest tests/modules/rewards/test_purchase_atomicity.py::test_atomic_balance_deduction -v
```

---

## 4. Test Categories & Bounded Context Scope

### 4.1 Architectural Invariant Tests (`tests/architecture/`, `tests/architectural/`)
- **Layering & Purity**: Verifies that controllers never call repositories directly, domain services do not import `FastAPI` request objects, and no module bypasses centralized dependencies.
- **Settings & Logging**: Asserts that `os.getenv` is never called outside `src/noorheroes/core/settings.py` and `secrets_bootstrap.py`.
- **CI/CD Integrity**: Asserts `.github/workflows/secret-scan.yml` is never path-filtered and Dockerfile runs under non-root `USER noorheroes`.
- **Gateway Zero-Authorization**: Proves API gateway enforces only transport security; business authorization is exclusively performed within domain services.

### 4.2 Security Baseline & Rate Limiting (`tests/security/`, `tests/infrastructure/`)
- **Slow-Hash Credential Storage**: Asserts that all password and PIN hashing routes use Argon2id with OWASP-compliant memory and time cost parameters.
- **Multi-Dimensional Rate Limiting**: Validates sliding-window enforcement across independent dimensions (device ID, IP address, phone number, parent account).
- **Gitleaks Custom Rules**: Asserts custom regex rules fire on synthetic JWT signing keys, Cloudflare R2 access keys, and OpenAI API tokens.

### 4.3 Content & Stories Module (`tests/modules/content/`)
- **Sequential Unlock Engine**: Validates deterministic unlock progression across playback percentages, choice points, and quiz scores with zero N+1 queries.
- **Heartbeat & Playback Verification**: Asserts monotonic position progression, flagging unnatural scrub-forward gaming attempts silently without crashing client playback.
- **Idempotent Completion**: Enforces exactly-once XP granting on story completion, even under high-concurrency race conditions.
- **Emergency Content Withdrawal**: Tests instant cache invalidation, reason recording, and soft-only withdrawal (`is_withdrawn = true`), ensuring zero child data loss.
- **Bedtime Audio Manifest Extension (Blueprint B-02)**: Validates additive extension on `GET /v1/content/{id}/manifest?format=audio`, format override parity (authored audio overridden by `format=video`/`text`, authored video overridden by `format=audio`, unrecognized format stripping), case/whitespace normalization (`AUDIO`, `%20%20audio%20%20`), nearest-100/10 privacy rounding (`round_listen_count`), degraded config fallback, graceful `null` fallback on stale/withdrawn `dua_ending_ref`, whitespace stripping, full Unicode/Arabic script support (`dua_أذكار_النوم_01`), selective wire serialization strictly omitting bedtime keys on non-audio formats, immutable `[0.8, 1.0, 1.2]` speed options, preview mode gate bypass, and real in-memory SQLite integration (`TestBedtimeManifestSqliteIntegration`) asserting ORM column loading across 96 targeted tests (460 total content tests).

### 4.4 Rewards & Gamification Module (`tests/modules/rewards/`)
- **Append-Only Ledger**: Database-level test proving ledger records cannot be modified or deleted once written.
- **Wallet Projection & Rebuild**: Verifies wallet balance projections match raw ledger sums to the exact integer.
- **Strict Family Scoping**: Proves cross-family reward queries return HTTP 403 / 404 with zero PII leakage.
- **Zero Real Money Paths**: AST scan guaranteeing no fiat currency or credit card charge logic exists in child gamification flows.

### 4.5 Child Lock & Access Gate (`tests/modules/access_gate/`)
- **Progressive Lockout Backoff**: Validates exponential delay and temporary account locking upon consecutive invalid PIN entries.
- **Sibling Data Isolation**: Tests strict separation of progress, favorites, and wallet balances between sibling profiles on the same device.
- **Parent Mode Step-Up Elevation**: Proves 3-stage child session tokens cannot access parental controls or billing settings.

### 4.6 Media Delivery & Upload Ingestion (`tests/modules/media/`, `tests/media/`)
- **11-Step Upload Validation Pipeline**: Validates MIME sniffing, magic bytes verification, ClamAV virus scanning, and dimension bounds checking before S3/R2 storage persistence.
- **Time-Limited Signed URLs**: Proves streaming URLs expire after 15 minutes and download manifests expire after 24 hours.
- **Download Health Telemetry**: Aggregates offline download failures into hourly, daily, and weekly monitoring buckets.
- **Authorized Media Manifest Delivery (`GET /v1/content/{id}/manifest`)**: Validates server-authoritative sequential unlock and entitlement gating with optional `format` parameter (`audio`, `video`, `text`), 15-minute presigned Cloudflare R2 streaming URLs, and Bedtime Audio Manifest extension delivery without forking parallel manifest endpoints across 240 total media tests (198 in `tests/modules/media/`, 42 in `tests/media/`).

### 4.7 Bedtime & Sleep Timer Configuration (`tests/modules/bedtime/`)
- **Fail-Safe Safe Defaults**: Verifies that unconfigured child profiles return HTTP 200 with safe defaults (`window_start = null`), never 404 or 500.
- **Strict Parent-Only Gating**: Proves child-mode tokens are strictly rejected with HTTP 403 `BEDTIME_PARENT_ONLY` on mutating PUT requests.
- **Midnight-Crossing Window Evaluation**: Validates evaluation of overnight windows (e.g. 20:00–07:00) with boundary instant checks (20:00, 23:30, 05:00, 07:00).
- **Zero-Length & Partial Range Rejection**: Asserts equal start/end or partial time pairs are rejected with HTTP 422 `INVALID_TIME_RANGE`.
- **Sleep Timer Ceiling Bounding**: Tests 5–120 minute enforcement across Pydantic schemas, service logic, and database CHECK constraints.
- **Transactional Outbox Eventing**: Asserts single-transaction persistence of `parent_bedtime_window_configured` and `parent_sleep_timer_ceiling_configured` events.
- **Bedtime Ritual Status Tracking API (`GET /v1/children/{id}/bedtime-ritual-status`)**: Validates safe default `ritualCompleted: false` (HTTP 200, never 404/500) for unrecorded dates, server-clock date derivation, minimal privacy-safe payload (`childId`, `date`, `ritualCompleted`), parent-only authorization, localized date validation (422 `INVALID_DATE` across `en`, `hi`, `ur`, `ar`), and `parent_bedtime_ritual_status_viewed` outbox event emission across 33 tests.
- **Repository Idempotent Upsert & Sibling Isolation**: Validates atomic ON CONFLICT upsert collapsing multiple same-day completions into a single row, and strict state isolation between siblings in the same family across 13 tests.
- **Silent Completion Non-Blocking Hook Isolation**: Validates in `tests/modules/content/test_silent_completion_parity.py` that transient DB failures during `record_ritual()` are logged as warnings and never fail or block story completion or reward ledger balances.

### 4.8 Identity, Authentication & Child Profiles (`tests/modules/identity/`)
- **Parent Auth & Session Security**: Validates Argon2id PIN setup and step-up verification, OTP rate limiting, Google OAuth ID token verification, and single-use refresh token rotation with replay detection.
- **Strict Sibling Data Isolation**: Proves cross-sibling queries return HTTP 403 `CHILD_MISMATCH` or `SESSION_CHILD_MISMATCH`, preventing data leakage between children on shared family devices.
- **Child Progress & Preferences**: Tests glanceable 5-field progress rollup aggregation (`GET /v1/children/{id}/progress` with 60-second Redis caching) and atomic upsert of child display locale preferences (`PATCH /v1/children/{id}/preferences`).
- **COPPA & GDPR-K Legal Consent**: Asserts append-only immutability of parental consent records with full audit trail.

### 4.9 Islamic Content Moderation & AI Safety (`tests/modules/ai_safety/`)
- **LLM & Heuristic Safety Checks**: Enforces child-safety, Islamic orthodoxy, and toxicity screening across moral summaries and translations.
- **Scholar Moral Review Workflow**: Validates human scholar approval queues (`/v1/ai-safety/moral-summaries/review-queue`), version increments, and unapproved status rejections.
- **Confidence-Gated Fallback & Chaos**: Tests 600ms latency budget with automatic fail-closed fallback to pre-approved human takeaways upon LLM timeout or confidence scores below 0.85.

### 4.10 Educational Learning & Parent Story Insights (`tests/modules/learning/`)
- **Parent Story Insights**: Validates `GET /v1/children/{id}/story-insights` with strict family scoping, aggregation of viewing progress, quiz attempts, and scholar-validated morals, returning 200 OK empty states without 5xx degradation.
- **Educational Progression**: Asserts quiz attempt recording, milestone validation, and streak calculations with zero unearned XP rewards.

### 4.11 Multi-Language Localization System (`tests/modules/localization/`)
- **Canonical 4-Language Resolution**: Asserts translation delivery and fallback across English (`en`, LTR default), Hindi (`hi`, LTR), Urdu (`ur`, RTL), and Arabic (`ar`, RTL).
- **Dynamic Translation Caching**: Validates SHA-256 Redis translation caching, cache invalidation, and asynchronous Celery translation workers.
- **Geographic & Currency Resolution**: Tests IP/Header country resolution and local currency formatting.

### 4.12 Dynamic Feature Flags & Remote Config (`tests/modules/feature_flags/`)
- **Deterministic SHA-256 Bucketing**: Validates percentage rollout bucketing based on SHA-256 hashing of entity UUIDs.
- **Dual Sign-Off Governance**: Asserts multi-party human approval requirement on safety-relevant feature flags before production rollout.
- **Instant Killswitch & Expiry**: Verifies Celery auto-expiry tasks and instant killswitch propagation through Redis pub/sub.

### 4.13 Administration, CMS & Operational Governance (`tests/modules/admin/`, `tests/admin/`)
- **Admin RBAC Scope Gating**: Asserts role-based access control across `content_editor`, `trust_safety`, `admin:read`, and `admin:write` scopes, strictly denying child and parent tokens.
- **Operational Health Telemetry**: Tests parental gate health metrics, onboarding conversion funnel analytics, and customer support PIN lockout overrides.
- **Dynamic Remote Config CMS**: Validates proposal, audit logging, dual approval, and rollout of dynamic client configurations.
- **Bedtime Configuration Analytics API (`GET /admin/v1/bedtime/analytics` / `GET /v1/admin/bedtime/analytics`, Blueprint B-05)**: Validates 100% SQL-level aggregation (`COUNT`, `GROUP BY`, `CASE WHEN`), portable database dialect formatting (`to_char` on Postgres, `strftime` on SQLite), empty range safe fallback (`200 OK` with 5 zero-count ceiling buckets `5-15`, `16-30`, `31-45`, `46-60`, `60+`), max 365-day query ceiling enforcement (`422 INVALID_DATE_RANGE`), `extra="forbid"` structural privacy guarantee with dedicated content-based PII regex leak assertion across 34 dedicated test cases (198 total admin module tests, 0 warnings).

### 4.14 Subscriptions & Mobile Push Notifications (`tests/modules/subscriptions/`, `tests/modules/notifications/`)
- **Subscription Tier Entitlements**: Enforces entitlement gating across free, standard, and premium tiers, rejecting unentitled audio/video manifest generation with 403 `ENTITLEMENT_REQUIRED`.
- **Push Notification Management**: Validates APNs/FCM payload formatting, quiet hours enforcement, and bedtime mode push delivery suppression.

### 4.15 Avatar System & Modesty Review Governance (`tests/modules/avatars/`, Blueprint B-05)
- **Segregation of Duties (P0 / CI-Blocking)**: Enforces that the asset's original submitting admin (`submitted_by_admin_id`) can never approve or reject their own asset under any administrative role (including superadmin), returning HTTP 403 `SELF_APPROVAL_FORBIDDEN`. Validated with defense-in-depth across both HTTP router/service and repository layers.
- **Modesty Review State Machine**: Enforces valid status transitions (`pending_review` -> `published` or `rejected`), rejecting repeated or invalid transitions with HTTP 409 `INVALID_STATE_TRANSITION`.
- **Return to Draft & Resubmission**: Re-editing rejected items or base characters via PATCH endpoints automatically resets status back to `pending_review`, allowing resubmission and approval by independent reviewers.
- **Child Inventory Isolation**: Guarantees that only `published` items are ever visible or equipable in child-facing endpoints (`GET /v1/children/{id}/inventory`), completely filtering out `pending_review` and `rejected` assets.
- **Substantive Feedback & Localization**: Rejection requires non-blank `review_notes` (HTTP 422), supporting complete Arabic script (`يرجى تعديل التصميم...`), Urdu, multilingual notes, formatting, and dual-wire (`reviewNotes` / `review_notes`) serialization up to 1024 characters.
- **Immutable Audit Logging**: Every approval and rejection writes an immutable `AdminAuditLog` record capturing both submitter and reviewer admin IDs.
- **End-to-End Multi-Step Lifecycle**: Complete lifecycle coverage in `TestEndToEndReviewLifecycle` verifying creation (`pending_review`, invisible to children) -> rejection with notes -> re-edit (returns to `pending_review`) -> submitter self-approval blocked (403) -> independent approval (`published`, 200) -> child inventory reflection (`owned_items`), plus HTTP TestClient journey.
- **Dual Router Parity & Parameter Bounds**: Validates 100% route parity across `/v1/admin/avatars/review-queue` and `/admin/v1/avatars/review-queue`, complete RBAC scope matrix, case-insensitive entity types (`ITEM`, `Base`), and 1-based pagination bounds across 299 passing test cases (16 test files, 0 failures, 0 warnings).

---

## 5. CI/CD Integration & Automated Gating

All tests run automatically on every pull request and push across the GitHub Actions CI pipelines:

1. **Stage 1 (Lint & Static Analysis)**:
   - `python scripts/check_env_example_sync.py`
   - `python scripts/check_env_drift.py`
   - `ruff check`
2. **Secret Scan Pipeline (`.github/workflows/secret-scan.yml`)**:
   - `gitleaks detect --config .gitleaks.toml --verbose`
   - `trufflehog git file://. --only-verified`
3. **Stage 2 (Unit & Architectural Tests)**:
   - `pytest -v --cov=src/noorheroes` (enforcing ≥80% coverage on core domains)
4. **Stage 3 (Integration & Smoke Tests)**:
   - Ephemeral Postgres/Redis Testcontainers execution and live staging smoke probes (`/healthz`, `/readyz`).

---

## 6. Guidelines for Writing New Tests

1. **Place tests in matching subdirectories**: Mirror the `src/noorheroes/modules/<module>` tree under `tests/modules/<module>`.
2. **Use pytest fixtures**: Leverage clean environment state fixtures (`clean_env_state`) and async fixtures (`@pytest.fixture`).
3. **Maintain Purity**: Never hardcode real credentials or live external service calls in unit tests. Use mock clients or in-memory repositories.
4. **Update Sync Checks**: When adding a new field to `Settings`, immediately add the safe placeholder key to `backend/.env.example` and run `make check-env`.
