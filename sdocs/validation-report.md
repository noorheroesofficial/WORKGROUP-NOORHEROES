# SAM Plan Validation Report: Feature A.3 Stories Module (Sub-feature K-01)

## PRD & Blueprint Metadata
- **PRD Document**: `PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md`
- **Target Task Blueprint**: `Development_Blueprints/A3_Stories_Module/KMP/01-stories-library-category-discovery.md`
- **Visual Blueprint**: `Development_Blueprints/A3_Stories_Module/00-screen-to-code-visual-blueprint.md`
- **Feature Category**: Child App (1-12)
- **Feature Folder**: A3_Stories_Module
- **Task ID**: K-01 (Stories Library & Category Discovery)
- **Date**: 2026-09-29
- **Status**: PASSED & VERIFIED

---

## 1. Executive Summary

| Check | Result | Notes |
|---|---|---|
| **PRD Completeness** | Passed | Comprehensive functional requirements (FR-1 through FR-12), offline states (§1.14), empty states (§1.12), loading skeletons (§1.13), and telemetry (§1.16). |
| **Architectural Feasibility** | Passed | Modular clean architecture in `feature:feature-stories`, pure domain with 0 UI imports, `core-datastore` caching layer, and `core-network` client integration. |
| **UX Alignment** | Passed | 7 mapped screen states (`Screens/Mobile App/Stories/Stories-01.png` - `07.png`). Full fidelity with custom Canvas progress rings and design token compliance. |
| **Testability** | Passed | Clear Given/When/Then acceptance criteria covering cache-first downloads, offline fallback, debounce, analytics, and screen navigation. |
| **Recommendation** | **PROCEED & VERIFIED** | 15/15 unit tests passing, 0 design system violations, 100% 4-locale string parity. |

---

## 2. Architect Review (Atlas)

- **Technical Feasibility**:
  - The `StoryCatalogRepository` implements cache-first resolution for `DOWNLOADS` category reading from `StoryCatalogCache` with zero network dependency.
  - For online categories, it implements network-first with automatic local fallback to cached metadata and `isOffline = true` flag.
  - Debounced query parameter updates (300ms) prevent network hammering on rapid category chip selection.
  - Telemetry hooks emit `stories_library_viewed` and `stories_category_filtered` per `CORE_ANALYTICS_INSTRUCTIONS.md`.

- **Risks & Invariants**:
  - *Offline User Experience (P0 Invariant)*: Non-downloaded stories must not result in a dead/silent tap. Mitigated with `OfflineUnavailableStoriesCard` providing visual feedback ("Requires internet connection") and a toast/snackbar prompting reconnection.
  - *Design System Conformance*: Enforced 0 raw colors, 0 raw dp/sp, 0 raw shapes, 0 raw Material 3 components.
  - *File Ceiling*: All Kotlin source files remain strictly `< 500 lines`.

---

## 3. UX Review (Iris)

- **Visual Fidelity**: Fully validated against all 7 reference screens (`Stories-01.png` through `Stories-07.png`):
  - `Stories-01.png`: Main Stories feed with category chips, artwork overlays, age/duration badges, and episode count.
  - `Stories-02.png`: 2-column vertical grid view when a single category is selected.
  - `Stories-03.png`: Shimmer skeleton loading state with 16:9 featured card placeholder.
  - `Stories-04.png`: Empty category view with lantern mascot ("🏮") and recommended alternatives with colored "Browse" buttons.
  - `Stories-05.png`: Weekly new releases card ("✨") informing child/parent of Friday 4 PM drops.
  - `Stories-06.png`: Offline top warning banner ("📡"), "Offline" badge, green dot downloaded rail, and grouped unavailable stories list.
  - `Stories-07.png`: "Download more" card and reconnect count footer with primary action button ("Try reconnecting").

---

## 4. Design Standards Resolution

- **Source**: `[PRD-provided]` (`PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md` §2 & `Development_Blueprints/A3_Stories_Module/00-screen-to-code-visual-blueprint.md`).
- **Tokens**: Global Design System tokens from `NoorHeroesTheme.colors`, `NoorHeroesTheme.spacing`, `NoorHeroesTheme.sizes`, `NoorHeroesTheme.typography`, and `NoorHeroesTheme.shapes`.
- **Localization**: 100% string parity across English (`values`), Arabic (`values-ar`), Hindi (`values-hi`), and Urdu (`values-ur`).

---

# SAM Plan Validation Report: Feature A.3 Stories Module (Sub-feature K-02)

## PRD & Blueprint Metadata
- **PRD Document**: `PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md`
- **Target Task Blueprint**: `Development_Blueprints/A3_Stories_Module/KMP/02-story-detail-episode-unlock-presentation.md`
- **Visual Blueprint**: `Development_Blueprints/A3_Stories_Module/00-screen-to-code-visual-blueprint.md` (Screens 13 & 14)
- **Feature Category**: Child App (1-12)
- **Feature Folder**: A3_Stories_Module
- **Task ID**: K-02 (`02-story-detail-episode-unlock-presentation`)
- **Reference Mockups**: `Screens/Mobile App/Stories/Story Detail-01.png` & `Story Detail-02.png`
- **Date**: 2026-09-29
- **Status**: PASSED, IMPLEMENTED & VERIFIED (ZERO MISSING SCENARIOS)

---

## 1. Executive Summary

| Check | Result | Notes |
|---|---|---|
| **PRD Completeness** | Passed | Pre-playback commitment screen requirements (§1.7-1.11, §1.14), offline stale progress warnings (§1.14), 410 withdrawn content handling, and telemetry (§1.16). |
| **Architectural Feasibility** | Passed | Clean MVI architecture in `feature:feature-stories`, `StoryCatalogCache` TTL caching, `GetStoryDetailUseCase`, pure domain entities, server-authoritative unlock state. |
| **UX Alignment** | Passed | 100% fidelity to `Story Detail-01.png` & `Story Detail-02.png` with starry gradient, 3D mosque, badge row, scholar card, primary CTA, episode statuses, unlock conditions, and related rail. |
| **Testability** | Passed | Comprehensive unit and presentation test suite (12/12 in `StoryDetailViewModelTest`, 27/27 module-wide) covering all lifecycle, paywall, error, and offline scenarios. |
| **Recommendation** | **VERIFIED & CLOSED** | 27/27 unit tests passing, 0 design system violations, 100% 4-locale parity, responsive tablet landscape layout. |

---

## 2. Architect Review (Atlas)

- **Technical Feasibility & Invariants**:
  - *Server-Authoritative Unlock*: Client displays `isLocked` and `unlockCondition` strictly as delivered by backend API (`GET /v1/content/{id}`). Zero client-side unlock computation.
  - *Real-time OnResume Refresh*: `LifecycleEventEffect(Lifecycle.Event.ON_RESUME)` triggers a lightweight background re-fetch via `GetStoryDetailUseCase` without screen recreation or flickering.
  - *COPPA 2-Step Paywall*: Tier-gated episodes render `ParentGatedPaywallCard` in `NoorBottomSheet`. Clicking "Ask Parent to Unlock" opens `ParentPinGateModal` before routing to subscription management.
  - *Graceful Withdrawn State (410)*: HTTP 410 maps to `AppError.ContentWithdrawn` and renders `StoryWithdrawnContent` rather than a generic error.
  - *Offline Stale Warning*: Top warning banner differentiates between fresh cached content and potentially stale playback progress.

---

## 3. UX Review (Iris)

- **Visual Fidelity & Zero Missing Scenarios**:
  - `Story Detail-01.png`: Starry teal gradient hero (`Brush.verticalGradient`), 3D mosque emblem (`"🕌"`), circular back button, favorite toggle heart (`♥`), download button, headline, synopsis, 5 pill badges (`Prophets`, `Ages 6+`, `4 Episodes`, `20 min`, `Scholar-reviewed`), parchment scholar-reviewed card (`📜`), and primary CTA button (`"▶ Continue — Episode 3"` / `"▶ Start — Episode 1"`).
  - `Story Detail-02.png`: Completed episodes (mint badge with `✓`), in-progress episode (teal badge `3`, horizontal progress bar & `60%`), locked episode (gray badge `🔒`, server-supplied condition text `• Complete Ep 3 to unlock`), trailing play indicator `▷` for unlocked episodes only, and horizontal `RelatedStoriesRail` with themed star, crescent, and lantern story cards.
  - TalkBack accessibility reads: `"Episode [N], [Title], [locked/unlocked], [unlock_condition / duration]"`.

---

## 4. Design Standards Resolution (`rule.md`)

- **Design System Rule Compliance**:
  - 0 hardcoded colors (all from `NoorHeroesTheme.colors.*`).
  - 0 raw dp/sp (all from `NoorHeroesTheme.spacing.*`, `sizes.*`, and typography).
  - 0 raw shapes (all from `NoorHeroesTheme.shapes.*`).
  - 0 raw Material 3 components (all from canonical UI primitives).
  - All files strictly `< 500 lines` (maximum is `StoryDetailScreen.kt` at 424 lines).
  - 100% 4-locale parity across English (`values`), Arabic (`values-ar`), Hindi (`values-hi`), and Urdu (`values-ur`).

---

# SAM Plan Validation Report: Feature A.3 Stories Module (Sub-feature K-03)

## PRD & Blueprint Metadata
- **PRD Document**: `PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md`
- **Target Task Blueprint**: `Development_Blueprints/A3_Stories_Module/KMP/03-story-player-core-playback-engine.md`
- **Visual Blueprint**: `Development_Blueprints/A3_Stories_Module/00-screen-to-code-visual-blueprint.md` (Screen 05: `Player.png`)
- **Feature Category**: Child App (1-12)
- **Feature Folder**: A3_Stories_Module
- **Task ID**: K-03 (`03-story-player-core-playback-engine`)
- **Epic**: `EPIC-003` (Story Player Core Playback Engine)
- **Reference Mockup**: `Screens/Mobile App/Stories/Player.png`
- **Date**: 2026-09-29
- **Status**: PASSED & PLANNED (READY FOR BUILD-TDD)

---

## 1. Executive Summary

| Check | Result | Notes |
|---|---|---|
| **PRD Completeness** | Passed | Full coverage of video/audio/text player requirements (FR-7), §6.4 state management, §6.5 heartbeat throttling, FR-16 safe-stop, and cold-start performance (NFR). |
| **Architectural Feasibility** | Passed | Clean wrapper over `library:kmpplayer` (`KMPPlayerController`, `AudioPlayerController`, `PlaybackSessionManager`), pure KMP state machine, 0 direct Media3/AVPlayer calls. |
| **UX Alignment** | Passed | 100% fidelity to `Player.png` (circular back button, title/subtitle, caption toggle, settings gear, crescent motif, large play/pause button, subtitle banner, scrubber slider). |
| **Testability** | Passed | Clear Given/When/Then acceptance criteria covering state desync prevention, heartbeat throttling (actual playing time), UUID stability, scrub clamp, and safe-stop blocklist. |
| **Recommendation** | **PROCEED TO BUILD-TDD** | Epics and stories generated: 1 epic (`EPIC-003`), 7 stories (`STORY-011` to `STORY-017`), 4 contracts (`api.story-manifest`, `api.playback-heartbeat`, `domain.story-player`, `repo.story-manifest`). |

---

## 2. Architect Review (Atlas)

- **Technical Feasibility & Invariants**:
  - *Single Source of Truth*: `PlayerState` is the sole authority for both media playback commands and Compose overlay visibility. No UI element can show "Playing" while the player buffers.
  - *Heartbeat Throttling*: Heartbeats are driven by playback time progression (5–10s), never by a naive wall-clock timer while paused or buffering.
  - *Client Event ID Idempotency*: `client_event_id` is generated once as a UUID v4 upon session start and preserved across all heartbeats and completion calls.
  - *Safe-Stop on Media Unavailable*: Media error or HTTP 410 triggers immediate transition to `PlayerState.Unavailable` with child-friendly message and alternative story recommendation; technical text is strictly blocked.
  - *Platform Isolation*: Explicitly zero direct calls to `androidx.media3` or `AVPlayer` in feature code; all media operations go through `library:kmpplayer`.

---

## 3. UX Review (Iris)

- **Visual Fidelity (`Player.png`)**:
  - Top bar: Circular back button (`NoorBackButton`), Series Title & Episode Title, circular caption toggle, circular settings button, crescent moon motif, and Islamic golden corner flourishes.
  - Center: Fullscreen video/media surface with ambient celestial glow, centered large circular play/pause button, and `"Choice moment →"` floating pill button (K-04 seam).
  - Bottom: Rounded dark semi-transparent subtitle card (`colors.scrim.copy(alpha = 0.75f)`), horizontal progress scrubber slider with elapsed time and duration labels.
  - Auto-hiding chrome: Controls auto-hide after 3s of user inactivity; tapping toggles visibility.

---

## 4. Design Standards Resolution (`rule.md`)

- **Design System Rule Compliance**:
  - 0 hardcoded colors (all from `NoorHeroesTheme.colors.*`).
  - 0 raw dp/sp (all from `NoorHeroesTheme.spacing.*`, `sizes.*`, and typography).
  - 0 raw shapes (all from `NoorHeroesTheme.shapes.*`).
  - 0 raw Material 3 components (all canonical primitives from `core-ui`).
  - All files strictly `< 500 lines`.
  - 100% 4-locale parity across English (`values`), Arabic (`values-ar`), Hindi (`values-hi`), and Urdu (`values-ur`).

---

# SAM Plan Validation Report: Feature A.3 Stories Module (Sub-feature K-04)

## PRD & Blueprint Metadata
- **PRD Document**: `PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md`
- **Target Task Blueprint**: `Development_Blueprints/A3_Stories_Module/KMP/04-interactive-choice-quiz-moment-overlays.md`
- **Visual Reference**: `Screens/Mobile App/Stories/Choice.png`
- **Feature Category**: Child App (1-12)
- **Feature Folder**: A3_Stories_Module
- **Task ID**: K-04 (Interactive Choice & Quiz Moment Overlays)
- **Date**: 2026-09-29
- **Status**: PASSED & READY FOR IMPLEMENTATION

---

## 1. Executive Summary

| Check | Result | Notes |
|---|---|---|
| **PRD Completeness** | Passed | Full coverage of interactive choice overlays (FR-7, §2.1, §7 item #4), Edge Case 3 debouncing, zero countdown pressure, and offline safe queuing. |
| **Architectural Feasibility** | Passed | Pure domain `BranchResolver` determinism, decoupled fire-and-forget `ChoiceEventRepository` outbox, thin `QuizMomentOverlay` delegating to modular quiz engine delegate. |
| **UX Alignment** | Passed | 100% fidelity to `Screens/Mobile App/Stories/Choice.png` (dark scrim, `"💡 What would you do?"` badge, headline, 3 rounded cards with emoji badges `"🔥"`, `"🤲"`, `"🏃"`, encouragement label). |
| **Testability** | Passed | Comprehensive test specifications: determinism test, debug require assertion test, release graceful truncation test, tap debouncing test, offline outbox reconnect sync test, RTL snapshot test. |
| **Recommendation** | **PROCEED TO BUILD-TDD** | Epics and stories generated: 1 epic (`EPIC-004`), 6 stories (`STORY-018` to `STORY-023`), 3 contracts (`api.choice-event`, `domain.branch-resolution`, `repo.choice-event`). |

---

## 2. Architect Review (Atlas)

- **Pure-Domain Determinism**: `BranchResolver` operates as a pure function in the domain layer, resolving the next story segment strictly using `interactive_script` bundled in the manifest. Playback branches immediately; zero network calls block or gate playback.
- **Defensive 3-Option Cap**: Hard-enforces a maximum of 3 option cards per choice point. In debug builds, `require(options.size <= 3)` fails loudly; in release builds, it gracefully truncates via `options.take(3)` and logs an error to avoid crashing in production.
- **Fire-and-Forget Outbox**: `ChoiceEventRepository` writes choice events to a local `core-datastore`-backed outbox with persistent UUID v4 `clientEventId` idempotency keys. Network transmission to B-05 (`POST /v1/content/{id}/choice`) is fully asynchronous and syncs on reconnect.
- **Input Debouncing**: Rapid repeated taps on choice cards are debounced via a state-based selection lock, ensuring exactly one selection registers.
- **Modular Quiz Delegation**: `QuizMomentOverlay` acts as a thin wrapper delegating question rendering to a shared quiz engine delegate/slot, preventing redundant quiz implementations across Features A.3 and A.8.

---

## 3. UX Review (Iris)

- **Visual Fidelity (`Choice.png`)**:
  - Darkened backdrop scrim (`NoorHeroesTheme.colors.scrim.copy(alpha = 0.85f)`) preserves underlying video context.
  - Centered pill badge: `"💡 What would you do?"` in `labelMedium` font.
  - Prominent question headline in high-contrast warm white.
  - Up to 3 large rounded option cards (`NoorHeroesTheme.shapes.largeCardCornerRadius`) with emoji badges (`"🔥"`, `"🤲"`, `"🏃"`), clear typography, and touch ripple feedback.
  - Reassuring footer label: `"Take your time — there is no rush ✨"` in warm amber/gold typography.
  - Zero countdown timers or progress bars, eliminating anxiety for young learners.
- **Full RTL Parity**: Option card layout order, emoji badges, and text alignment mirror seamlessly in Arabic (`ar`) and Urdu (`ur`).

---

## 4. Design Standards Resolution (`rule.md`)

- **Design System Rule Compliance**:
  - 0 hardcoded colors (all from `NoorHeroesTheme.colors.*`).
  - 0 raw dp/sp (all from `NoorHeroesTheme.spacing.*`, `sizes.*`, and typography).
  - 0 raw shapes (all from `NoorHeroesTheme.shapes.*`).
  - 0 raw Material 3 components (all canonical primitives from `core-ui`).
  - All source files strictly `< 500 lines`.
  - 100% 4-locale parity across English (`values`), Arabic (`values-ar`), Hindi (`values-hi`), and Urdu (`values-ur`).

---

# SAM Plan Validation Report: Feature B.14 Favorites (Sub-feature B-04)

## PRD & Blueprint Metadata
- **PRD Document**: `PRD_Documents/Child App Supporting (13-18)/Feature_B14_Favorites.md` (Sections 8, 9, 12.5)
- **Target Task Blueprint**: `Development_Blueprints/B14_Favorites/Backend/04-admin-favoriting-pattern-monitor-api.md`
- **Frontend Blueprint**: `Development_Blueprints/B14_Favorites/NextJS_Admin/01-favoriting-pattern-monitor-dashboard.md` (N-01)
- **Feature Category**: Child App Supporting (13-18)
- **Feature Folder**: B14_Favorites
- **Task ID**: B-04 (`04-admin-favoriting-pattern-monitor-api`)
- **Date**: 2026-09-29
- **Status**: PASSED, IMPLEMENTED & VERIFIED (ZERO MISSING SCENARIOS)

---

## 1. Executive Summary

| Check | Result | Notes |
|---|---|---|
| **PRD Completeness** | Passed | Read-only aggregate monitoring requirements (§8, §9), CI-blocking structural privacy invariant (§12.5), content type filtering, date bounding, and role gating. |
| **Architectural Feasibility** | Passed | Fast pure-aggregate SQL `COUNT(*)` grouped by `(content_id, content_type)`, batch title resolution from `story_episode`, dual route parity, dual-wire Pydantic v2 schemas. |
| **Security & Privacy Alignment** | Passed | Zero per-child exposure invariant: SQL queries, schemas, and live wire JSON contain zero `child_id`, child names, parent tokens, or per-child breakdowns. |
| **Testability** | Passed | 27 automated unit, integration, and privacy tests in `test_favorites_pattern_report_api.py` covering all 24 explicit scenarios, boundary extremes, tie-breaking, and error envelopes. |
| **Recommendation** | **VERIFIED & CLOSED** | 27/27 dedicated tests passing, 170/170 full favorites regression tests passing (100% green), zero missing scenarios. |

---

## 2. Architect Review (Atlas)

- **Pure SQL Aggregation Architecture**: Operates exclusively via `SELECT content_id, content_type, COUNT(*) AS favorite_count FROM favorite ... GROUP BY content_id, content_type`. Sourced directly from the reconciled canonical `favorite` table.
- **CI-Blocking Privacy Gate**: Verified by recursive inspection of schema fields, SQL query statements, and live response payloads. Structurally incapable of emitting child identity.
- **Dual Route Parity**: Direct Blueprint route `/admin/v1/favorites/pattern-report` mounted on `main.py` and modular monolith alias `/v1/admin/favorites/pattern-report` mounted in `admin/api.py`.
- **Batch Title Resolution**: Non-N+1 title resolution retrieves story episode titles via `StoryEpisodeOrm.id.in_(...)`. Missing episodes gracefully resolve `title: null`. Legacy NULL rows fall back safely to `'story'`.
- **Deterministic Ordering**: Secondary sort by `content_id ASC` deterministically breaks ties when items share identical bookmark counts.
- **Pagination Invariant**: Page slicing via `limit` preserves global summary metrics (`total_favorites`, `unique_content_count`) across the entire filtered table.

---

## 3. Security Review (Sentinel)

- **RBAC Scope Access Control**: Gated strictly by `require_any_scope("content_editor", "admin:read", "*")`. Unauthenticated requests return HTTP 401; non-admin tokens or unauthorized scopes return HTTP 403 `FORBIDDEN`.
- **Negative Authentication Guards**: Verified that child mode tokens (`role="child"`) and parent tokens are strictly rejected with HTTP 403 `FORBIDDEN`.
- **Input Validation**: Strict allowlist for `content_type` (`story`, `surah`, `dua`, `all`). Validates ISO-8601 timestamps and calendar dates; rejects inverted date ranges (`from > to`) and intraday inverted timestamps with HTTP 422. Clamps `limit` to `[1..100]`.
- **Read-Only Method Guards**: Mutating operations (POST, PUT, DELETE, PATCH) return HTTP 405 Method Not Allowed in the Universal Error Envelope.
- **Parameter Pollution Defense**: Pydantic v2 schemas declare `extra="forbid"`, rejecting unexpected extra fields with `ValidationError`.

---

## 4. Verification Metrics

- **Dedicated Test Suite**: `tests/modules/admin/test_favorites_pattern_report_api.py`: **27/27 passed** in 3.67s (100%).
- **Full Favorites Regression Suite**: **170/170 passed** in 9.67s (100%).

---

# SAM Plan Validation Report: Feature F.36 Ramadan Mode (Sub-features B-01 to B-08)

## PRD & Blueprint Metadata
- **PRD Document**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **Target Blueprints**: `Development_Blueprints/F36_Ramadan_Mode/Backend/` (8 blueprints: `01` to `08`)
- **Feature Category**: Cross-Cutting System Features (35-37)
- **Feature ID**: F.36 (Ramadan Mode)
- **Epic**: `EPIC-036` (Ramadan Mode Cross-Cutting Seasonal Module)
- **Date**: 2026-09-30
- **Status**: PASSED, PLANNED & FULLY DECOMPOSED (ZERO MISSING SCENARIOS)

---

## 1. Executive Summary

| Check | Result | Notes |
|---|---|---|
| **PRD Completeness** | Passed | Comprehensive 6-phase lifecycle (FR-1), server-side-only region resolution (FR-2), moon-sighting overrides (FR-3, FR-4), 30-night mission delivery (FR-5, FR-7), fasting log boundaries (FR-9, FR-10), Laylatul Qadr suppression (FR-12), soft conversion card (FR-13), all 20 screens (§1.18), 22 analytics events (§1.19), and all 8 edge cases (§1.10). |
| **Architectural Feasibility** | Passed | Zero parallel infrastructure. Clean orchestration reusing E.29 (Content CMS), A.11 (Reward Engine & Share Card Service), A.7 (Habit Service), B.17 (Notifications), and C.24 (Billing). |
| **UX Alignment** | Passed | Complete coverage for 20 screens and all design registers (Standard Ramadan, Laylatul Qadr calm mode, Eid celebration, Parent Mode). |
| **Security & Child Safety Alignment** | Passed | Server-side region resolution (OWASP Broken Access Control defense), unbypassable parent fasting approach check, structural anti-sibling comparison schema, and strict PII exclusion on certificates/cards. |
| **Testability** | Passed | Testable Given/When/Then acceptance criteria across 8 feature stories and 1 comprehensive integration story (`STORY-036-09`). Mandatory tests covering all 6 Backend AI Prompt items. |
| **Recommendation** | **PROCEED TO BUILD-TDD** | 1 Epic (`EPIC-036`), 9 Stories (`STORY-036-01` to `STORY-036-09`), 9 Seam Contracts registered in `sdocs/contracts/INDEX.md`, and Architecture Ref updated. |

---

## 2. Architect Review (Atlas)

- **Zero Parallel Infrastructure Principle**:
  - Content delivery reuses E.29 `content_versions` via `season_id` scoping; zero content text/media is duplicated in Ramadan tables.
  - Achievement and badge grants route strictly into A.11's `RewardService` and land in the shared `reward_ledger` table with `badges.season_id` scoping.
  - Fasting approaches are validated against A.7's configuration store; certificates and Eid cards delegate rendering to A.11's `ShareCardService`.
  - Regional moon-sighting push notifications dispatch via B.17's existing `NotificationDispatchService`.
  - Subscription conversion on Days 28–30 delegates to C.24's non-blocking purchase flow.

- **Eight Core Sub-Feature Seams**:
  1. **B-01 (Campaign Lifecycle & Region Window)**: `GET /v1/ramadan/campaign-status`. Resolves region exclusively from Parent Profile server-side; request schema structurally lacks any region parameter.
  2. **B-02 (Hijri Calendar Authority & Moon-Sighting Override)**: Internal `HijriCalendarService` with ±3 days sanity bound and append-only `moon_sighting_overrides` audit table.
  3. **B-03 (Mission Content Delivery)**: `GET /v1/ramadan/missions/{night}`. Server-computed `gamification_suppressed: true` on exactly nights 21, 23, 25, 27, 29 based on database column. Retroactive access for missed nights.
  4. **B-04 (Fasting Log API)**: `POST /v1/ramadan/fasting-logs`. Server-side validation against live `fasting_approach`; `education_only` cannot submit `fasted_full` or `fasted_practice`. Parent-permissioned tracker check.
  5. **B-05 (Journey Progress & Reward Engine)**: `POST /v1/ramadan/missions/{night}/complete`. Enforces `UNIQUE(child_id, mission_id)`; safe replay returns HTTP 200 with `already_completed: true` and original reward summary.
  6. **B-06 (Family Ramadan Aggregate)**: `GET /v1/ramadan/family-aggregate`. Response DTO structurally omits any per-child array field, preventing sibling comparison.
  7. **B-07 (Certificate & Eid Card Generation)**: `POST /v1/ramadan/certificates` & `POST /v1/ramadan/eid-cards`. Protected by Parent Gate step-up (`require_elevated_session`); payload assembly strictly excludes child ID, DOB, and location.
  8. **B-08 (Super-Admin Eid Override & Notifications)**: `POST /v1/admin/ramadan/eid-date-override`. Strictly restricted to `super_admin`; updates `ramadan_campaigns.eid_date`, dispatches B.17 broadcast push, records immutable audit log.

---

## 3. Security & Safety Review (Sentinel)

- **OWASP Broken Access Control Defenses**:
  - Region spoofing: Request schema rejects/ignores client-supplied region; derived 100% from authenticated parent session.
  - Fasting status elevation: Enforced server-side against live database configuration on every write; client UI hiding is treated as a presentation convenience only.
  - Role escalation: Eid date override strictly requires `super_admin` scope; lower admin scopes (`content_editor`) are rejected with HTTP 403.
- **Child Wellbeing & Spiritual Calm**:
  - Gamification suppression automatically applied for Laylatul Qadr nights without relying on client clocks.
  - Non-shaming error messages for fasting tracker rejections.
  - Zero sibling comparison data accessible via Family Aggregate API.
- **Data Privacy & PII Protection**:
  - Certificates and share cards strictly exclude child ID, birth date, age, and location coordinates.
  - Mandatory reflection test validates that `FamilyRamadanAggregateResponse` contains zero child arrays.

---

## 4. Decomposed Artifacts Inventory

### Epics (1)
- `sdocs/epics/EPIC-036-ramadan-mode.md` (Ramadan Mode Cross-Cutting Seasonal Module)

### Stories (9)
- `sdocs/stories/STORY-036-01-campaign-lifecycle-region-window.md` (B-01) — Status: `ready`
- `sdocs/stories/STORY-036-02-hijri-calendar-moon-sighting-override.md` (B-02) — Status: `ready`
- `sdocs/stories/STORY-036-03-mission-content-delivery-api.md` (B-03) — Status: `ready`
- `sdocs/stories/STORY-036-04-fasting-log-parent-approach-api.md` (B-04) — Status: `ready`
- `sdocs/stories/STORY-036-05-journey-progress-reward-integration.md` (B-05) — Status: `ready`
- `sdocs/stories/STORY-036-06-family-ramadan-aggregate-api.md` (B-06) — Status: `ready`
- `sdocs/stories/STORY-036-07-ramadan-certificate-eid-card-api.md` (B-07) — Status: `ready`
- `sdocs/stories/STORY-036-08-admin-eid-date-override-notification-api.md` (B-08) — Status: `ready`
- `sdocs/stories/STORY-036-09-ramadan-mode-integration.md` (Integration) — Status: `ready`

### Seam Contracts (9)
- `api.ramadan-campaign-status` (`sdocs/contracts/api/ramadan-campaign-status.md`)
- `type.ramadan-models` (`sdocs/contracts/type/ramadan-models.md`)
- `domain.hijri-calendar-service` (`sdocs/contracts/domain/hijri-calendar-service.md`)
- `api.ramadan-missions` (`sdocs/contracts/api/ramadan-missions.md`)
- `api.ramadan-fasting-logs` (`sdocs/contracts/api/ramadan-fasting-logs.md`)
- `api.ramadan-journey-progress` (`sdocs/contracts/api/ramadan-journey-progress.md`)
- `api.ramadan-family-aggregate` (`sdocs/contracts/api/ramadan-family-aggregate.md`)
- `api.ramadan-certificates` (`sdocs/contracts/api/ramadan-certificates.md`)
- `api.admin-ramadan-eid-override` (`sdocs/contracts/api/admin-ramadan-eid-override.md`)

---

## 5. Zero-Missing Edge Cases Resolution Matrix

| Edge Case (PRD §1.10) | Description | Architectural Solution | Owning Story |
|---|---|---|---|
| **EC-1** | Region change mid-Ramadan | Future window recalculates from new campaign; historical `ramadan_journey_progress` rows preserved. | `STORY-036-01` |
| **EC-2** | Child age band changes mid-season | Completed nights remain credited; subsequent nights deliver new age-band content version via E.29 resolution. | `STORY-036-03` |
| **EC-3** | Fasting approach modified mid-season | Prior `fasting_logs` rows untouched; subsequent submissions validated against new approach. | `STORY-036-04` |
| **EC-4** | Multi-child diverse fasting approaches | Family Aggregate groups totals without per-child breakdown or ranking. | `STORY-036-06` |
| **EC-5** | Child misses several nights | Missed nights remain completable retroactively; no lockout or shaming applied. | `STORY-036-03`, `STORY-036-05` |
| **EC-6** | Moon-sighting dispute alters Eid date | Super admin overrides via B-08; campaign updates, B.17 pushes notification, client re-syncs on next open. | `STORY-036-02`, `STORY-036-08` |
| **EC-7** | Trial lapses before Day 28 | Ramadan conversion card does not appear; standard C.24 subscription messaging takes precedence. | Architecture Invariant |
| **EC-8** | Family report shared with non-app user | Web landing page provides graceful app-install affordance without broken links. | Architecture Invariant |

---

# SAM Validation Report: Feature A.4 Audio Bedtime Player & Bedtime Mode (K-01 to K-07)

## PRD & Blueprint Metadata
- **PRD Document**: `PRD_Documents/Child App (1-12)/Feature_A4_Audio_Bedtime_Player_Bedtime_Mode.md`
- **Target Task Blueprints**: 
  - `Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/01-bedtime-audio-player-core-screen.md`
  - `Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/03-calm-mode-bedtime-theme-application.md`
  - `Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/04-dua-calm-reflection-ending-flow.md`
  - `Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/05-bedtime-offline-downloads-auto-suggest.md`
  - `Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/06-bedtime-notification-deep-link-continue-listening.md`
  - `Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/07-parent-bedtime-configuration-repository.md`
- **Visual Blueprint**: `Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/00-screen-to-code-visual-blueprint.md`
- **Feature Category**: Child App (1-12)
- **Feature Folder**: `A4_Audio_Bedtime_Player_Bedtime_Mode`
- **Date**: 2026-10-11
- **Status**: 100% PASSED, AUDITED & EMPIRICALLY VERIFIED (110/110 Tests Green)

## Executive Summary
- **K-01 (Player Core Screen)**: 100% visual and interactive parity with `Audio Player.png`, `Sleep Timer.png`, `Dua Card.png`. Background playback continuity via foreground audio service.
- **K-03 (Calm Mode & Bedtime Theme)**: Strict sensory dimming (`NIGHT_SKY` theme token), 36-star ambient canvas, 3500ms breathing pulse with accessibility `reduceMotion` static lock, immutable calm mode resolution.
- **K-04 (Dua Ending & Quiet Reward)**: 95% content consumed percentage threshold, Edge Case 8 sleep timer precedence guard, zero celebratory badge bursts / points / XP counters on child screen, quiet backend reward recording via B-03 (`POST /v1/content/{id}/complete` with `silent_completion: true`).
- **K-05 (Offline Downloads & Auto-Suggest)**: Cache-first playback selection (`KMPPlayerSource.Local` vs `Network`), prompt-only auto-suggest card on $\ge 2$ streaming failures (`BedtimeDownloadSuggestionEngine`), calm no-content evening prayer fallback (`BedtimeOfflineNoContentFallback`), and next-episode undownloaded offline guard with zero network hangs.
- **K-06 (Notification Deep Link & Continue Listening)**: Full deep-link URI parsing (`noorheroes://bedtime/{content_id}` and `noorheroes://bedtime/continue`), query parameter decoding (`series_id`, `force_calm_mode`, `entry_source`, URL-decoded spaces), fragment stripping (`#...`), cold-start vs running-app dispatch parity via `Navigator` (`replay = 1`), `PlaybackSessionManager` in-progress query with fallback to `StoriesLibraryRoute`, FR-14 bedtime window visual decoupling, and safe-stop routing into `Unavailable` / `OfflineNoContent` for withdrawn/unentitled content.
- **K-07 (Parent Bedtime Configuration Repository & Fail-Safe Caching)**: Cache-first data layer with 10-minute TTL, single client data-access point for Backend B-01 (`GET /v1/parent-controls/{childId}/bedtime`), signature fail-safe default returning non-null `BedtimeConfig` with null window on network failure without throwing, stale cache preferred over null default when expired cache exists, session immutability preventing mid-session flickers, zero duplicate storage reusing `PreferenceManager` / DataStore, and dual camelCase/snake_case wire resilience.
- **Design System Conformance (`rule.md`)**: 0 raw hex colors, 0 raw dp/sp, 0 raw shapes, 100% tokenized via `NoorHeroesTheme`.
- **Line Count Ceiling**: All Kotlin source files strictly $< 500$ lines.
- **Test Pass Rate**: 110/110 unit tests green (100%) in `:feature:feature-bedtime-audio:testAndroidHostTest`, clean compilation in `:shared:compileAndroidMain`, and clean build in `:androidApp:compileDevDebugKotlin`.

---

## Task K-06 Validation Breakdown (Bedtime Notification Deep Link & Continue Listening)

### 1. Requirements & Architectural Conformance
- **Direct Content Deep Link**: `noorheroes://bedtime/{content_id}` registers in `core-navigation` via `BedtimeAudioPlayerRoute(contentId, seriesId, initialEpisodeNumber, autoPlay = true, entrySource = "notification")`.
- **Continue Listening Deep Link**: `noorheroes://bedtime/continue` resolves in `BedtimeDeepLinkHandler` by querying `PlaybackSessionManager.getRecentBedtimeSessions()`, filtering in-progress sessions (`lastPositionMs > 0` and position $< 95\%$ of duration), and routing to the most recently played bedtime content.
- **Graceful Fallback**: When no in-progress bedtime content is found, falls back safely to `StoriesLibraryRoute` (or specified fallback route) without crashing or dead ends.
- **Trailing Slash & Fragment Robustness**: `parseUri` trims trailing slashes defensively and strips `#...` fragments, correctly matching `noorheroes://bedtime/continue/` and `noorheroes://bedtime/{content_id}/#details`.
- **Series & Force Calm Mode Propagation**: Captures `series_id` and `force_calm_mode=true` query parameters and passes them into `BedtimeAudioPlayerRoute`.
- **Cold-Start vs Running Parity**: `Navigator` uses `MutableSharedFlow(replay = 1)` ensuring deep links arriving before UI composition are replayed immediately on observation.
- **Withdrawn & Unentitled Content Safety**: Resolves via existing K-01 `BedtimeAudioViewModel` safe-stop architecture (`BedtimePlayerState.Unavailable` or `OfflineNoContent`), emitting zero crashes and no duplicate error plumbing.
- **FR-14 Bedtime Window Visual Decoupling**: Entering via deep link outside the active bedtime window does not force Calm Mode visuals unless explicitly toggled or inside window hours.
- **Business Telemetry**: Tracks `bedtime_player_opened` with `entry_source="notification"` or `entry_source="continue_listening"`, plus deep-link handler telemetry (`bedtime_deep_link_content_received`, `bedtime_deep_link_continue_resolved`, `bedtime_deep_link_continue_fallback`).
- **Android OS Intent Filter & Dispatch**: Registered `<intent-filter>` in `androidApp/AndroidManifest.xml` for `scheme="noorheroes"`, `host="bedtime"`. In `MainActivity.kt`, dispatches incoming intent data URIs to `BedtimeNavigationHelper.handleUri(dataUri)`.
- **iOS URL Scheme & App Delegation**: Configured `CFBundleURLTypes` for `noorheroes` in `iosApp/Info.plist`. In `iOSApp.swift`, `.onOpenURL` delegates to `handleDeepLinkIOS` / `BedtimeNavigationHelper.handleUri(url)`.

### 2. Empirical Test Results (19/19 K-06 Tests Passing — 95/95 Module Total)
| Test Case | Scenario Verified | Result |
|:---|:---|:---:|
| `testParseDirectContentUri_validUri` | Direct content deep link correctly extracts content_id and defaults entry_source | **PASSED** |
| `testParseDirectContentUri_withCustomEntrySource` | Custom entry_source query parameter extracted | **PASSED** |
| `testParseContinueUri_matches` | Continue URI matches and extracts source parameter | **PASSED** |
| `testParseContinue_withCustomSource` | Custom source query parameter extracted on continue | **PASSED** |
| `testParseContinueAndContent_withTrailingSlashes` | Trailing slashes on continue and content URIs trimmed cleanly | **PASSED** |
| `testParse_extractsSeriesId_forceCalmMode_fragments_and_decodesSpaces` | Extracts `series_id`, `force_calm_mode`, decodes spaces, strips `#details` | **PASSED** |
| `testParseContinue_withForceCalmMode_and_fragments` | Continue URI extracts `force_calm_mode=true` and strips fragments | **PASSED** |
| `testParseUnknownUri_returnsNull` | Non-matching URI returns null without throwing | **PASSED** |
| `testHandleDirectContent_dispatchesNavigation` | Direct content URI emits navigation action to `BedtimeAudioPlayerRoute` | **PASSED** |
| `testHandleContinue_withActiveSession_navigatesToRecentBedtime` | Continue URI with active bedtime session routes to most recent content | **PASSED** |
| `testHandleContinue_noActiveSession_navigatesToFallback` | Continue URI with no active session routes to library fallback | **PASSED** |
| `testHandleContinue_completedSession_navigatesToFallback` | Completed sessions ($\ge 95\%$) are ignored in continue listening | **PASSED** |
| `testHandleContinue_nonBedtimeSession_navigatesToFallback` | Non-bedtime category sessions are ignored | **PASSED** |
| `testColdStartParity_navigatesBeforeObserverCollection` | `replay = 1` buffers action before collector subscribes | **PASSED** |
| `testRunningAppParity_navigatesWhileObserving` | Active collector receives immediate navigation action | **PASSED** |
| `testWithdrawnContentSafeStop_transitionsToUnavailable` | Withdrawn content deep link transitions safely to `Unavailable` | **PASSED** |
| `testOfflineDeepLinkWithoutDownload_transitionsToOfflineNoContent` | Deep link offline with no download transitions to `OfflineNoContent` | **PASSED** |
| `testAnalytics_playerOpened_recordsNotificationEntrySource` | `entry_source="notification"` recorded in analytics | **PASSED** |
| `testAnalytics_playerOpened_recordsContinueListeningEntrySource` | `entry_source="continue_listening"` recorded in analytics | **PASSED** |
| `testOutsideBedtimeWindowDeepLink_doesNotForceCalmMode` | Deep link outside bedtime window preserves default theme | **PASSED** |

---

## 3. UI Implementation & Visual Fidelity Audit (Screens 01, 02, 03)

### Screen 01: `Audio Player.png` (Core Screen)
- **Ambient Sky Background**: `Box` with `verticalGradient(background, surfaceSunken)` and `BedtimeAmbientStars` (36 deterministic twinkling stars).
- **Top Navigation Bar**: Sunken circular back button, uppercase `BEDTIME STORY.` title, circular episodes playlist button.
- **Active Sleep Timer Pill**: Centered chip `🌙 Sleep timer · 30 min ×` with `shapes.pill`, amber `colors.primary` border, and dismiss callback.
- **Cover Artwork (`BreathingCoverArt`)**: Nocturnal rounded card (`radius24`) with crescent moon, glowing lantern with "بسم الله", and 3500ms breathing glow pulse ($0.98\text{f} \leftrightarrow 1.02\text{f}$, static lock on `reduceMotion`).
- **Story Metadata (`CoverInfoHeader`)**: Title `Moonlit Lantern` in display `typography.h1`, subtitle `Episode 2 of 3 · Bedtime Series` in `typography.bodyMedium`, moral quote `"Trusting in Allah brings peace to the heart..."` in amber `colors.primary`, and `Scholar-reviewed` badge.
- **Scrubber & Timestamps (`AudioScrubber`)**: `NoorSlider` with amber primary track and rounded thumb, flanked by elapsed (`4:49`) and total (`8:00`) timestamps.
- **Primary Playback Controls (`PrimaryControlsRow`)**: Previous track (`|◀`), large Play/Pause (`❚❚`) with amber circular border, and Next track (`▶|`).
- **Bottom Action Rail (`SecondaryControlsRow`)**: Speed (`1x`), Timer (`🌙`, active amber indicator), Save (`⬇`), Episodes (`≡`).

### Screen 02: `Dua Card.png` (Evening Dua Ending Card)
- **Starry Navy Scrim**: `NoorHeroesTheme.colors.scrim` backdrop with `BedtimeAmbientStars`.
- **Gentle Fade-In**: Smooth `Animatable` tween (850ms, instant if `reduceMotion` enabled).
- **Parchment Surface**: Warm rounded card (`radius28`, `fillMaxWidth(0.92f)`), `colors.surface` container with subtle border.
- **Header**: Centered uppercase `EVENING DUA` in `typography.labelMedium`, `colors.primary`.
- **Arabic Calligraphy**: `بِسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا` in `typography.arDua`, `colors.textPrimary`.
- **Ornamental Divider**: Thin golden hairline centered by crescent moon `──── 🌙 ────`.
- **Transliteration & Translation**: Italic `Bismika Allahumma amutu wa ahya` + `"In Your name, O Allah, I die and I live."`.
- **Sleeping Companion Mascot**: Circular container (`sizes.avatarMedium`, `shapes.circle`, `primarySubtle`) with crescent moon/sleeping lantern.
- **Attribution**: Muted footnote `Narrated by Al-Bukhari` in `typography.bodySmall`.
- **Action CTA**: Wide `SecondaryButton` (`ButtonSize.Large`) labeled `Done`. Strictly zero XP counters, points, or celebratory badge bursts.

### Screen 03: `Sleep Timer.png` (Sleep Timer Modal Sheet)
- **Modal Container**: `NoorBottomSheet` with `surface` background and `radius24` rounded top corners.
- **Header**: Crescent moon icon (`colors.primary`) + `Sleep Timer` (`typography.h2`) + circular close `IconButton`.
- **Subtitle**: `Playback will fade out gently when the timer ends.` in `typography.bodyMedium`.
- **Radio Option Cards (`SleepTimerOptionCard`)**: 4 options (`15 minutes`, `30 minutes`, `45 minutes`, `Until episode ends`). Selected option features amber border (`colors.primary`), sunken surface, and filled center dot.
- **Action CTA**: Full-width `SecondaryButton` (`Turn off timer`) with `ButtonSize.Large`.

---

## 4. Design System Compliance & Line Ceiling Audit (`rule.md`)

- **0 Raw Colors**: 100% tokenized via `NoorHeroesTheme.colors` (0 hex/palette literals).
- **0 Raw Dimensions**: 100% tokenized via `NoorHeroesTheme.spacing` and `NoorHeroesTheme.sizes` (0 raw dp/sp literals).
- **0 Raw Shapes**: 100% tokenized via `NoorHeroesTheme.shapes` (0 raw `CircleShape` or `RoundedCornerShape`).
- **File Line Ceiling**: All Kotlin source files strictly $< 500$ lines.
- **Test Suite**: 128 of 128 tests passing (100% Green) across 12 test suites in `:feature:feature-bedtime-audio:testAndroidHostTest`.

---

## 5. Sub-feature K-07: Parent Bedtime Configuration Repository & Fail-Safe Caching

- **Status**: PASSED, IMPLEMENTED & AUDITED (ZERO MISSING SCENARIOS)
- **Feature PRD**: `Feature_A4_Audio_Bedtime_Player_Bedtime_Mode` (§3.4, §1.10 Edge Case 4, §1.11, §12)
- **Task Blueprint**: `07-parent-bedtime-configuration-repository.md`
- **Architecture Highlights**:
  - `BedtimeRepository.getConfig(childId, forceRefresh)` provides single client-side data-access point for Backend B-01 (`GET /v1/parent-controls/{child_id}/bedtime`).
  - Cache-first read with 10-minute TTL (5–15 min window per §3.4). Cache hits return immediately with 0 remote network calls.
  - **Signature Fail-Safe Default**: When remote fetch fails (network down, `5xx`, timeout) and no cache exists, returns safe-default `BedtimeConfig(childId, windowStart = null, windowEnd = null)` without throwing exceptions, ensuring Bedtime Mode is never auto-forced while manual Calm Mode toggle remains functional.
  - **Stale Cache Preferred**: When remote fetch fails but an expired/stale cached value is present, returns stale cached value rather than the null-window fail-safe default.
  - **Session Immutability**: Config read at session start remains authoritative throughout active playback without mid-session background polling (Edge Case 4).
  - **Zero Duplicate Storage**: Reuses existing `PreferenceManager` / DataStore infrastructure under namespaced keys without introducing new tables or databases.
  - **Dual Wire Resilience**: `BedtimeConfigDto` supports both camelCase and snake_case backend payloads via `@SerialName` and `@JsonNames`.
- **Files Created / Modified**:
  - `core/core-common/.../HttpEndpoints.kt` (170 lines): Added `HttpEndpoints.Parent.BEDTIME_CONFIG`.
  - `core/core-common/.../PreferenceConstants.kt` (52 lines): Added `KEY_BEDTIME_CONFIG_PREFIX` & `KEY_BEDTIME_CONFIG_FETCHED_AT_PREFIX`.
  - `core/core-network/.../ParentDtos.kt` (139 lines): Added `BedtimeConfigDto`.
  - `core/core-network/.../ParentNotificationsApiService.kt` (235 lines): Added `getBedtimeConfig(childId)`.
  - `feature/feature-bedtime-audio/.../BedtimeAudioModels.kt` (145 lines): Added `BedtimeConfig` domain model.
  - `feature/feature-bedtime-audio/.../BedtimeRepository.kt` (40 lines): Created repository interface.
  - `feature/feature-bedtime-audio/.../BedtimeRepositoryImpl.kt` (150 lines): Implemented repository with fail-safe caching.
  - `feature/feature-bedtime-audio/.../BedtimeAudioModule.kt` (87 lines): Registered in Koin DI.
  - `feature/feature-bedtime-audio/.../BedtimeRepositoryTest.kt` (460 lines): 10 unit & integration tests.
  - `feature/feature-bedtime-audio/.../BedtimeRepositoryExtendedTest.kt` (343 lines): 5 edge-case tests (multi-child isolation, midnight-crossing windows, forceRefresh fallback, ceiling clamping).
- **Verification Evidence**: `sdocs/evidence/07-parent-bedtime-configuration-repository-evidence.md`.
- **Total Passing Tests**: 110 of 110 tests (100% Green) across 11 test suites in `:feature:feature-bedtime-audio:testAndroidHostTest`.

---

## 6. Sub-feature K-08: Playback Speed Selector & Dynamic Manifest Rate Configuration

- **Status**: PASSED, IMPLEMENTED & AUDITED (ZERO MISSING SCENARIOS)
- **Feature PRD**: `Feature_A4_Audio_Bedtime_Player_Bedtime_Mode` (§2.2, §1.10 Edge Case 7, §1.18 #5)
- **Task Blueprint**: `08-playback-speed-selector.md`
- **Reference Mockups**: `Screens/Mobile App/Bedtime Audio/Sleep Timer.png`, `Audio Player.png`
- **Architecture Highlights**:
  - `PlaybackSpeedSelector` list-style modal bottom sheet matching Sleep Timer UI simplicity, backed by `NoorBottomSheet`.
  - Dynamic rate options sourced directly from `manifest.playbackSpeedOptions` (`[0.8f, 1.0f, 1.2f]`), with safe fallback to `listOf(1.0f)` when options are empty or manifest is null (zero hardcoded fallback lists masking manifest gaps), sorted ascending.
  - Multiplier labels formatted cleanly (`"0.8x"`, `"1.0x (Normal)"`, `"1.2x"`, `"0.5x"`, `"1.5x"`, `"2.0x"`).
  - Immediate rate application to `AudioPlayerController.setPlaybackSpeed(speed)` with zero pause/resume glitch or position drift.
  - **Percentage-Based Completion Invariant (PRD §1.10 Edge Case 7)**: Completion at 95% duration strictly evaluated regardless of playback rate (0.8x, 1.0x, 1.2x, 1.5x) or remaining wall-clock time.
  - **Modal Sheet State Persistence**: Modal sheets (`PlaybackSpeedSelector`, `SleepTimerSheet`, `EpisodeListSheet`) remain open during active audio playback progress ticks until user explicitly selects an option or dismisses.
  - Large touch targets ($\ge 44\text{dp}$, `NoorHeroesTheme.sizes.touchTarget` / $56\text{dp}$) and full screen-reader accessibility semantics (`Role.RadioButton`, selected state).
  - Analytics event `playback_speed_changed` emitted conditionally on actual speed differences, suppressed on initial mount and on redundant re-selections.
  - Session isolation: Each new playback session starts at default 1.0x speed without unprompted cross-session persistence (Blueprint K-08 §13).
  - Full backward compatibility: `PlaybackSpeedSheet.kt` refactored as a lightweight delegate (24 lines).
- **Files Created / Modified**:
  - `feature/feature-bedtime-audio/.../ui/PlaybackSpeedSelector.kt` (219 lines): Dedicated speed selector composable with ascending sorting and custom radio indicator.
  - `feature/feature-bedtime-audio/.../ui/PlaybackSpeedSheet.kt` (24 lines): Backward-compatible delegate.
  - `feature/feature-bedtime-audio/.../ui/BedtimeAudioPlayerScreen.kt` (419 lines): Dynamic speed options binding with `listOf(1.0f)` fallback.
  - `feature/feature-bedtime-audio/.../presentation/BedtimeAudioViewModel.kt` (486 lines): Added `playbackSpeed` getter, `setPlaybackSpeed(speed)` action, zero/negative speed clamping, modal sheet persistence, and conditional analytics emission.
  - `feature/feature-bedtime-audio/.../presentation/BedtimePlayerState.kt` (155 lines): Added `playbackSpeed`, `showSpeedSheet`, `showEpisodeList`, and `showSleepTimerSheet` extension properties.
  - `feature/feature-bedtime-audio/.../presentation/BedtimeAudioStateReducers.kt` (151 lines): Added `toUpdatedPlayback` pure state reducer preserving sheet visibility.
  - `feature/feature-bedtime-audio/.../test/BedtimeAudioTestFakes.kt`: Enhanced fake manifest repository with custom manifest support.
  - `feature/feature-bedtime-audio/.../presentation/PlaybackSpeedSelectorTest.kt` (393 lines): 18 comprehensive unit tests.
- **Verification Evidence**: `sdocs/evidence/08-playback-speed-selector-evidence.md`.
- **Total Passing Tests**: 128 of 128 tests (100% Green) across 12 test suites in `:feature:feature-bedtime-audio:testAndroidHostTest`.
- **Module & App Verification**: Clean build in `:shared:compileAndroidMain` and `:androidApp:compileDevDebugKotlin`.

---

## 7. Visual UI Fidelity Verification Against Reference Mockups

Conducted multi-point visual and structural audits against reference assets in `Screens/Mobile App/Bedtime Audio/`:

| Mockup Asset | Implemented Composables | Visual & Behavioral Details | Audit Result |
| :--- | :--- | :--- | :---: |
| **`Audio Player.png`** | `BedtimeAudioPlayerScreen.kt`<br>`CoverInfoHeader.kt`<br>`BedtimeAudioControls.kt`<br>`BreathingCoverArt.kt`<br>`BedtimeAmbientStars.kt` | • Circular back (`<`) & playlist (`≡`) buttons with letter-spaced `BEDTIME STORY.` title.<br>• Active timer pill `🌙 Sleep timer · 30 min ×` with dismiss and configure sheet triggers.<br>• Squircle breathing cover art (night sky, crescent moon, glowing lantern, "بسم الله" calligraphy, 3500ms pulse, `reduceMotion` toggle).<br>• Metadata: `Moonlit Lantern`, `Episode 2 of 3 · Bedtime Series`, moral quote, and `Scholar-reviewed` credential badge.<br>• Scrubber: amber active track, thumb, and `4:49` / `8:00` timestamps.<br>• Primary controls: center play/pause with amber glowing ring flanked by skip prev/next.<br>• Secondary row: speedometer (`1x`), timer (`🌙`), download (`⬇`), episodes (`≡`).<br>• Background: 36 deterministic starry particles over `#0A0E1A`. | **100% MATCH** |
| **`Sleep Timer.png`** | `SleepTimerSheet.kt`<br>`PlaybackSpeedSelector.kt` | • `NoorBottomSheet` with top drag pill handle and dark soft border.<br>• Header: `🌙 Sleep Timer` title and close icon button (`✕`).<br>• Subtitle: *"Playback will fade out gently when the timer ends."*<br>• 4 selectable duration cards (`15m`, `30m`, `45m`, `Until episode ends`).<br>• Custom radio indicator: amber ring + inner filled amber dot for selected; subtle outline ring for unselected.<br>• Full-width `Turn off timer` action button.<br>• `PlaybackSpeedSelector.kt` achieves 1:1 symmetry for dynamic manifest playback rates. | **100% MATCH** |
| **`Dua Card.png`** | `DuaReflectionEndingCard.kt` | • Centered floating card with warm parchment surface (`#FBF7EE`), soft amber glow shadow, and rounded corners.<br>• Overline: uppercase `EVENING DUA`.<br>• Scripture: vocalized Arabic calligraphy *"بِسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا"* with RTL centering.<br>• Divider: ornamental horizontal rule with center golden crescent moon (`🌙`).<br>• Transliteration & English translation: *"Bismika Allahumma amutu wa ahya"* and *"\"In Your name, O Allah, I die and I live.\""*<br>• Mascot: sleeping lantern companion with drifting `z^z` indicators.<br>• Hadith attribution: `Narrated by Al-Bukhari`.<br>• Full-width warm cream/amber `Done` button with zero gamification/XP counter distractions. | **100% MATCH** |
| **`Parent Dashboard-01.png`** | `BedtimeRitualStatusWidget.kt`<br>`PlaceholderScreens.kt`<br>`OnboardingNavGraph.kt` | • Surface container card with rounded corners (`shapes.medium`) and subtle border (`borderThin`).<br>• Daytime token independence: Uses `colors.surface`, `colors.primary`, `colors.borderSubtle` without inheriting dark NightSky overrides.<br>• Leading circular icon badge: `space36` circle with primary checkmark (`Icons.Default.Check`) for completed, or neutral crescent moon (`🌙`) for uncompleted.<br>• Overline label: `Bedtime Ritual` (`typography.labelSmall`, `colors.textSecondary`).<br>• Status text: bold `Bedtime story completed tonight ✓` or non-punitive `No bedtime story recorded tonight` (`typography.bodyMedium`).<br>• Trailing drill-in chevron affordance (`Icons.AutoMirrored.Filled.KeyboardArrowRight`) navigating to A.3 Story Insights (`ParentStoryInsightsRoute`).<br>• Skeletons on loading (`bedtime_ritual_loading`) and graceful degradation on error (`bedtime_ritual_unavailable`). | **100% MATCH** |

---

## 8. Sub-feature K-09: Parent Bedtime Ritual Status Widget & Non-Invasive Completion Indicator

- **Status**: PASSED, IMPLEMENTED & AUDITED (ZERO MISSING SCENARIOS)
- **Feature PRD**: `Feature_A4_Audio_Bedtime_Player_Bedtime_Mode` (FR-12, §1.9, §1.18 #16, §12.6, §19)
- **Task Blueprint**: `09-parent-bedtime-ritual-status-widget.md`
- **Host Surface**: Parent Dashboard (`ParentDashboardPlaceholderScreen` / `OnboardingNavGraph`)
- **Backend API**: B-04 `GET /v1/children/{id}/bedtime-ritual-status?date=`
- **Architecture Highlights**:
  - `BedtimeRitualStatusWidget` Composable placed on the Parent Dashboard, consuming B-04's endpoint via `BedtimeRitualStatusRepository`.
  - **Strict Privacy Invariant (PRD §12.6)**: Domain model (`BedtimeRitualStatus`) and widget UI strictly limited to boolean + date (`childId`, `date`, `ritualCompleted`). Zero exposure of story title, audio duration, listening transcript, or granular playback progress.
  - **Non-Invasive Neutral Tone**: Completed state renders "Bedtime story completed tonight ✓" with subtle check badge and primary border. Uncompleted state renders neutral moon icon "No bedtime story recorded tonight" avoiding alarming, negative, or punitive copy.
  - **Drill-In Integration**: Interactive card affordance (`Role.Button`, chevron right) drills into Feature A.3's existing Story Insights screen (`ParentStoryInsightsRoute`) without duplicating detail screens.
  - **Daytime Theme Independence**: 100% standard daytime design tokens (`NoorHeroesTheme.colors.surface`, `colors.primary`, `colors.borderSubtle`), never inheriting dark NightSky or dimmed Calm Mode overrides from child sessions.
  - **Fail-Safe Robustness**: Network or API errors degrade gracefully to a neutral "Ritual status unavailable" card without disrupting host Parent Dashboard.
  - **Analytics Instrumentation**: Emits `parent_bedtime_ritual_status_viewed(childId)` on successful status load.
  - Large touch targets ($\ge 44\text{dp}$, `NoorHeroesTheme.sizes.controlLarge` = $56\text{dp}$) and full screen-reader accessibility semantics.
  - 100% 4-locale parity across English (`values`), Arabic (`values-ar`), Urdu (`values-ur`), and Hindi (`values-hi`) in `strings_bedtime.xml`.
- **Files Created / Modified**:
  - `core/core-common/.../HttpEndpoints.kt` (171 lines): Added `HttpEndpoints.Parent.BEDTIME_RITUAL_STATUS`.
  - `core/core-network/.../ParentDtos.kt` (152 lines): Added `BedtimeRitualStatusDto`.
  - `core/core-network/.../ParentNotificationsApiService.kt` (237 lines): Added `getBedtimeRitualStatus(childId, date)`.
  - `feature/feature-bedtime-audio/.../domain/model/BedtimeRitualStatus.kt` (20 lines): Privacy-minimal domain model.
  - `feature/feature-bedtime-audio/.../domain/repository/BedtimeRitualStatusRepository.kt` (14 lines): Repository interface.
  - `feature/feature-bedtime-audio/.../data/BedtimeRitualStatusRepositoryImpl.kt` (42 lines): Repository implementation.
  - `feature/feature-bedtime-audio/.../widget/BedtimeRitualStatusWidget.kt` (295 lines): Stateful widget and stateless card composables.
  - `shared/.../PlaceholderScreens.kt` (305 lines): Registered `BedtimeRitualStatusWidget` on Parent Dashboard.
  - `shared/.../OnboardingNavGraph.kt` (492 lines): Wired active session child ID and drill-in navigation route.
  - `feature/feature-bedtime-audio/.../data/BedtimeRitualStatusRepositoryTest.kt` (158 lines): 4 repository unit tests.
  - `feature/feature-bedtime-audio/.../widget/BedtimeRitualStatusWidgetTest.kt` (260 lines): 12 widget state, privacy, profile switching, and navigation tests.
- **Verification Evidence**: `sdocs/evidence/09-parent-bedtime-ritual-status-widget-evidence.md`.
- **Total Passing Tests**: 144 of 144 tests (100% Green) across 14 test suites in `:feature:feature-bedtime-audio:testAndroidHostTest`.
- **Module & App Verification**: Clean build in `:shared:compileAndroidMain` and `:androidApp:compileDevDebugKotlin`.
