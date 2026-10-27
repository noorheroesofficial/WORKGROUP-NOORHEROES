# Architecture Reference: Stories Module — Library & Category Discovery (K-01)

## 1. System Context & Overview
The Stories Module (`feature:stories`) is the interactive storytelling hub in the NoorHeroes child application (Feature A.3, ID: K-01). It connects child learners to scholar-approved stories through:
- 7 canonical categories: `Bedtime Stories`, `Prophet Stories`, `Islamic Shorts`, `Animated Series`, `Values & Manners`, `Ramadan & Eid`, `Downloads`.
- Filtering: age band, media format (video/audio/text), duration (short/medium/long), and downloaded-only.
- Offline-first browsing: Downloads category is 100% offline-playable and browsable from local storage; other categories provide graceful degradation from cached metadata with explicit non-dead-tap affordances.

## 2. Technical Architecture & Module Structure
Clean Architecture / MVVM layering:
```
feature:feature-stories/
├── src/commonMain/kotlin/com/noorheroes/feature/stories/
│   ├── data/
│   │   ├── local/StoryCatalogCache.kt (PreferenceManager / DataStore backed)
│   │   ├── model/StoryCatalogModels.kt (Serializable DTOs)
│   │   ├── remote/StoryCatalogApi.kt (Ktor HttpClient via core-network)
│   │   └── repository/StoryCatalogRepositoryImpl.kt
│   ├── domain/
│   │   ├── model/StoryModels.kt (Domain entities: StoryCategory, StoryItem, CategoryRail, StoryFilter)
│   │   ├── repository/StoryCatalogRepository.kt
│   │   └── usecase/GetStoriesLibraryUseCase.kt
│   ├── presentation/
│   │   ├── StoriesLibraryState.kt (Sealed MVI UI State)
│   │   ├── StoriesLibraryEvent.kt (User intents)
│   │   ├── StoriesLibraryEffect.kt (One-time UI effects)
│   │   └── StoriesLibraryViewModel.kt (Extends BaseViewModel, debounce, analytics)
│   ├── ui/
│   │   ├── StoriesLibraryScreen.kt (Scaffold, LoadStateContent, Screen layout)
│   │   ├── CategoryFilterPanel.kt (Pill chips, mirrorable scroll)
│   │   ├── StoryRailComponents.kt (Category header, horizontal LazyRow, StoryCard)
│   │   ├── StoriesOfflineComponents.kt (Offline banner, ready-to-watch rail, requires-connection list)
│   │   └── StoriesEmptyComponents.kt (No stories illustration, explore alternatives)
│   └── di/StoriesModule.kt (Koin DI module)
```

## 3. Design Standards & Token Matrix Compliance (NoorHeroes/docs/rule.md)
All UI strictly adheres to `NoorHeroes/docs/rule.md`:
1. **0 Hardcoded Colors**: All colors sourced via `NoorHeroesTheme.colors.*` (surface, background, primary, textPrimary, textSecondary, error, scrim, etc.).
2. **0 Hardcoded DP / SP**: All spacing via `NoorHeroesTheme.spacing.*`, sizes via `NoorHeroesTheme.sizes.*`, typography via `NoorHeroesTheme.typography.*`.
3. **0 Raw Shapes**: All radii via `NoorHeroesTheme.shapes.*` (`shapes.pill`, `shapes.card`, `shapes.sheetTop`, etc.).
4. **0 Raw Material 3 UI**: Canonical primitives from `core:core-ui` (`NoorCard`, `NoorChip`, `PrimaryButton`, `LoadStateContent`).
5. **100% Localization Parity**: Backed by `Res.string.*` with 4-locale parity across English (`values`), Arabic (`values-ar`), Urdu (`values-ur`), and Hindi (`values-hi`).
6. **Pure Architecture**: 0 UI / Compose imports in domain and data layers.
7. **Modularity Ceiling**: Strict `< 500 lines` per file.

## 4. Backend API Contract Integration
- **Endpoint**: `GET /v1/content`
- **Query Parameters**: `type=story`, `category`, `age_band`, `locale`, `format`, `duration`, `downloaded_only`, `free_premium`, `cursor`, `limit`.
- **Response**: `StoryCatalogPaginatedResponse` containing `items: List<StorySummaryResponse>`, `nextCursor`, `hasMore`.
- **Authentication**: Child Bearer token.

## 5. Favorites Module Architecture Reference & Contract Integration (Feature B.14)

### 5.1 System Context & Overview
The Favorites Module (`feature:favorites`, Feature B.14) provides a lightweight, universal bookmarking capability across Stories (A.3), Quran/Arabic (A.5), and Dua Learning (A.6):
- **Per-Child Isolation**: Strict, non-negotiable data boundary — favorites are never shared across siblings or families.
- **Content-Agnostic Model**: Single canonical `favorite` table (`child_id`, `content_id`, `content_type`, `created_at`).
- **Resilient Availability Resolution**: Content withdrawal/archival reflects dynamically (`available: false`) without deleting the underlying bookmark.
- **Canonical Restructuring**: Automatically follows restructured episodes to their canonical identity while preserving historical origin.

### 5.2 Backend API Contracts
- **Favorite Toggle Endpoint**:
  - `POST /v1/favorites`
  - Body: `{ content_id: string, content_type: "story"|"surah"|"dua", favorited: boolean, client_request_id?: string }`
  - Response: `FavoriteToggleResponse` (`{ favorited: boolean, content_id: string, content_type: string, available: boolean }`)
  - Semantics: Idempotent toggle; server-side accessibility re-validation on add (`favorited: true`); un-gated removal (`favorited: false`); instant cache invalidation.
- **Favorites Listing Endpoint**:
  - `GET /v1/children/{id}/favorites`
  - Query Parameters: `type` (`story|surah|dua|all`), `cursor` (opaque base64 keyset), `limit` (1..50, default: 20).
  - Authorization: Strict path `{id} == session.child_id` verification. Sibling/cross-family mismatch immediately returns `403 FORBIDDEN` (`Cannot access favorites of another child`).
  - Response Envelope: `PageResult` envelope with `items: FavoriteItemResponse[]`, `nextCursor: string|null`, `hasMore: boolean`, plus dual-wire alias `favorites`.
  - Caching: Redis 60s short TTL keyed by `(child_id, content_type, cursor, limit)` with automatic database fallback.

---

## 6. Story Player Core Playback Engine Architecture Reference (Feature A.3 / K-03)

### 6.1 System Context & Overview
The Story Player (`feature:stories` player package) is the immersive, full-screen playback container for video, audio, and text formats across Android and iOS:
- **Core Wrapper**: Built directly on `library:kmpplayer` using `KMPPlayerController`, `AudioPlayerController`, and `PlaybackSessionManager`.
- **Pure Architectural Prohibition**: Explicitly zero direct calls to platform-specific `androidx.media3` or Apple `AVPlayer` APIs.
- **Unified State Machine**: A single authoritative `PlayerState` sealed hierarchy is the sole source of truth driving both media engine playback calls and Compose UI overlay visibility.

### 6.2 Architectural Invariants
1. **Desync Prevention**: No UI element or overlay may show "Playing" controls while `KMPPlayerController` is buffering or preparing.
2. **Session Idempotency**: `client_event_id` is generated once via cryptographically secure UUID v4 upon `StoryPlayerViewModel` initialization and reused identically across all heartbeat transmissions and eventual completion calls (K-06).
3. **Throttled Heartbeats**: Heartbeats to B-03 (`POST /v1/playback/{content_id}`) are triggered exclusively by playback time accumulation (every 5–10s of actual playing time) and never fire via wall-clock while paused or buffering.
4. **Safe-Stop on Media Unavailable**: Fatal media errors or 410 withdrawals trigger immediate transition to `PlayerState.Unavailable(reason)` with a comforting, child-friendly explanation and fallback recommendation; zero technical jargon or error codes reach the child learner.
5. **Scrub-Ahead UX Clamp**: When manifest indicates `scrub_restricted = true`, forward seeking is clamped to `furthestReachedPosition + tolerance` (non-authoritative UX nicety backed by server enforcement).
6. **Resume Position Persistence**: Read and restored via `PlaybackSessionManager.getResumePosition()` on `prepare()`, and saved on session exit.
7. **Text Story Format**: Dedicated `StoryTextPlayer` Composable renders text-format stories with typography scaling and auto-reading, reporting seamlessly into the same `PlayerState` machine.

### 6.3 Visual Fidelity Mapping (`Player.png`)
- **Top Chrome**:
  - Circular Back Button (`NoorBackButton`) at top start.
  - Series Title & Episode Title (`headlineSmall` & `labelMedium`) at top center.
  - Circular Caption Toggle Button (`Icons.Default.ClosedCaption`) and Settings Gear (`Icons.Default.Settings`) at top end.
  - Celestial crescent moon motif and subtle Islamic golden corner flourishes.
- **Center Media & Interactive Seam**:
  - Fullscreen media surface (`KMPPlayer` / `AudioPlayer` / `StoryTextPlayer`).
  - Centered large circular Play/Pause button (`NoorHeroesTheme.colors.surface`, `sizes.controlLarge`).
  - Floating pill button: `"Choice moment →"` on the center-right (K-04 seam).
- **Bottom Controls & Subtitle Tray**:
  - Subtitle Banner: Rounded dark semi-transparent card (`colors.scrim.copy(alpha = 0.75f)`) with clean readable subtitle typography.
  - Scrubber: Linear progress slider with circular thumb knob, elapsed time (`2:15`) at start, total duration (`5:48`) at end.
  - Auto-hiding chrome behavior on user inactivity.

### 6.4 Design Token Compliance (`rule.md`)
- 0 raw colors (all from `NoorHeroesTheme.colors.*`).
- 0 raw dp/sp (all from `NoorHeroesTheme.spacing.*`, `sizes.*`, and typography).
- 0 raw shapes (all from `NoorHeroesTheme.shapes.*`).
- 0 raw Material 3 components (all canonical primitives from `core-ui`).
- All files strictly `< 500 lines`.
- 100% 4-locale parity across English (`values`), Arabic (`values-ar`), Hindi (`values-hi`), Urdu (`values-ur`).

## 7. Interactive Choice & Quiz Moment Overlays (Task K-04 / EPIC-004)

### 7.1 Component Architecture & Layering
In-player interactive overlays appearing at scripted timestamps defined in the signed story manifest (`interactive_script`):
- **Overlay Hierarchy**: Rendered conditionally above the media surface driven directly by `PlayerState.ChoiceActive(choicePoint)` and `PlayerState.QuizActive(quizMoment)`. Never modeled as an independent navigation route, eliminating transition latency and maintaining video surface continuity without frame drops.
- **Pure Domain Determinism**: `BranchResolver` evaluates storyline branching entirely on the client using bundled manifest segment refs. Playback branches immediately upon user tap; zero network calls block or gate playback.
- **Fire-and-Forget Outbox**: `ChoiceEventRepository` records selections to B-05 (`POST /v1/content/{id}/choice`) asynchronously. Local outbox backed by `core-datastore` queues selections offline and syncs on reconnect with UUID v4 idempotency keys.
- **Shared Quiz Delegation**: `QuizMomentOverlay` acts as a thin wrapper delegating question rendering to a shared quiz engine slot/delegate, preventing redundant quiz implementations across Features A.3 and A.8.

### 7.2 Architectural Invariants
1. **Defensive 3-Option Cap**: Hard-enforces a maximum of 3 option cards per choice point. Debug builds throw an assertion error (`require(options.size <= 3)`) failing loudly; release builds truncate via `.take(3)` and log an error without crashing.
2. **Zero Countdown Pressure**: Reflects the child-centric ethical guideline ("Take your time — there is no rush ✨"); no countdown timers or progress bars are present on choice overlays.
3. **Double-Tap Debouncing**: A tap-guard debounce window ensures rapid repeated clicks register exactly one selection, preventing race conditions or duplicate analytics.
4. **Playback Non-Blocking**: Under no circumstances does branch playback await a network round-trip. Branching continues synchronously; B-05 network synchronization is entirely decoupled.
5. **Session & Event Idempotency**: Each choice event generates a persistent UUID v4 `clientEventId` preserved across offline retries to guarantee duplicate-free server aggregation.

### 7.3 Visual Fidelity Mapping (`Choice.png`)
- **Backdrop Scrim**: Darkened semi-transparent overlay (`NoorHeroesTheme.colors.scrim.copy(alpha = 0.85f)`).
- **Header Badge**: Rounded pill badge with icon and label `"💡 What would you do?"` in `labelMedium` font.
- **Question Headline**: Prominent, high-contrast headline (`titleLarge` / `headlineSmall`) in warm white text.
- **Option Cards (Max 3)**:
  - Card 1: Emoji badge `"🔥"` + Label `"Trust in Allah and walk into the fire"`.
  - Card 2: Emoji badge `"🤲"` + Label `"Pray for rain to put out the fire"`.
  - Card 3: Emoji badge `"🏃"` + Label `"Run away and hide in the mountains"`.
  - Styling: Large rounded corners (`NoorHeroesTheme.shapes.largeCardCornerRadius`), touch ripple feedback, bold typography.
- **Footer Reassurance**: Reassuring label `"Take your time — there is no rush ✨"` in warm amber/gold typography.
- **RTL Mirroring**: Full horizontal mirroring of card order, badge placement, and text alignment for Arabic (`ar`) and Urdu (`ur`).

### 7.4 Design Token Compliance (`rule.md`)
- 0 raw colors (all sourced from `NoorHeroesTheme.colors.*`).
- 0 raw dp/sp (all sourced from `NoorHeroesTheme.spacing.*`, `sizes.*`, and typography tokens).
- 0 raw shapes (all sourced from `NoorHeroesTheme.shapes.*`).
- 0 raw Material 3 components (all canonical primitives from `core-ui`).
- All source files strictly `< 500 lines`.
- 100% 4-locale parity across English (`values`), Arabic (`values-ar`), Hindi (`values-hi`), Urdu (`values-ur`).

---

## 8. Ramadan Mode Architecture Reference (Feature F.36 / Tasks B-01 to B-08)

### 8.1 System Context & Seasonal Orchestration
Ramadan Mode (`Feature F.36`) is a cross-cutting seasonal module operating across all four NoorHeroes applications (Mobile, Backend, Admin, Website). Rather than constructing parallel backend infrastructure, it orchestrates existing, hardened platform engines:
- **Content Pipeline**: Reuses E.29's `ContentService` with `season_id` scoping for all 30 nights.
- **Reward Engine**: Reuses A.11's `RewardService`, `badges.season_id`, and the shared `reward_ledger` table.
- **Habit Tracking**: Reuses A.7's `HabitService` configuration store for per-child `fasting_approach`.
- **Notifications**: Reuses B.17's `NotificationDispatchService` for regional moon-sighting Eid date alerts.
- **Billing & Conversion**: Reuses C.24's subscription engine for the Day 28–30 soft conversion moment.
- **Audit Logging**: Reuses E.28's `AuditLogService` for all administrative overrides and campaign mutations.

### 8.2 Core Architectural & Security Invariants

1. **Server-Side-Only Region Resolution (B-01 / PRD §5 item 1 / OWASP Broken Access Control)**:
   - The campaign lifecycle phase (`pre_ramadan_countdown`, `active`, `laylatul_qadr`, `eid_transition`, `eid_celebration`, `post_eid_tail`) and current night number are resolved **exclusively** from the authenticated parent's Profile `region` field.
   - Any client-supplied `region` query/body parameter is structurally absent from the request schema and has zero effect on computation.
   - Unconfigured regions return `phase: "not_active"` with HTTP 200, never an unhandled 4xx/5xx error.

2. **Sole Hijri Calendar & Moon-Sighting Override Authority (B-02 / B-08 / FR-4)**:
   - `HijriCalendarService` is an internal leaf service (no public router) serving as the platform's sole Hijri-date authority. No mobile client or secondary service computes Hijri dates locally.
   - Date overrides are persisted in the append-only `moon_sighting_overrides` audit table, updating `ramadan_campaigns.eid_date` and setting `eid_date_overridden = true`.
   - Sanity-bound validation: Corrected Eid dates must fall within ±3 days of the algorithmic expected date, rejecting catastrophic input mistakes.

3. **Server-Computed Gamification Suppression (B-03 / FR-12 / PRD §5 item 2)**:
   - For Laylatul Qadr nights (21, 23, 25, 27, 29), the response flag `gamification_suppressed: true` is server-computed directly from `ramadan_missions.is_laylatul_qadr`.
   - Clients must never use client-side clocks or hardcoded lists to determine tonal suppression.
   - During suppression, competitive mechanics, leaderboards, and celebratory badge callouts are replaced with a calm, reflection-oriented aesthetic.

4. **Parent-Controlled Fasting Approach Enforcement (B-04 / FR-9, FR-10 / PRD §5 item 3)**:
   - The parent-configured `fasting_approach` (`education_only`, `fasted_practice`, `fasted_full`) is enforced server-side as an unbypassable boundary.
   - `education_only` children are strictly forbidden from submitting `fasted_full` or `fasted_practice` (HTTP 403 Forbidden with child-safe messaging).
   - Fasting Tracker visibility is parent-permissioned per child; if disabled, API writes return HTTP 403.
   - Mid-Ramadan approach adjustments preserve prior log rows and constrain future entries only.

5. **Idempotent Journey Progress & Shared Reward Ledger (B-05 / FR-8 / PRD §5 item 4)**:
   - Night mission completion enforces `UNIQUE(child_id, mission_id)` in `ramadan_journey_progress`.
   - Repeated calls for an already-completed night return HTTP 200 with `already_completed: true` and the original reward payload (safe replay, never a duplicate grant).
   - Reward grants route strictly through A.11's shared `reward_ledger` table with `badges.season_id` scoping; zero parallel reward tables exist.
   - Retroactive completion: Missed nights remain completable retroactively without date lockouts.

6. **Structural Anti-Sibling Comparison Guarantee (B-06 / PRD §3.4 / PRD §5 item 5)**:
   - `GET /v1/ramadan/family-aggregate` response DTO structurally omits any per-child array or ranking field.
   - Multi-child families with divergent fasting approaches have progress aggregated without comparative ranking or individual completion attribution.
   - Families joining mid-season receive "not applicable" indicators for pre-join nights rather than missed counts.

7. **PII-Safe Certificate & Eid Card Generation (B-07 / FR-6 / PRD §12.6)**:
   - End-of-Ramadan certificate (`POST /v1/ramadan/certificates`) and Eid Card (`POST /v1/ramadan/eid-cards`) require Parent Gate step-up authentication (`require_elevated_session`).
   - Payload assembly strictly excludes child ID, date of birth, and geographic location before delegating rendering to A.11's `ShareCardService`.
   - Requires at least 1 completed night for certificate generation (HTTP 422 if 0 nights completed).

8. **Super-Admin Gated Moon-Sighting Eid Override & Push Notification (B-08 / FR-3 / PRD §12.5)**:
   - `POST /v1/admin/ramadan/eid-date-override` is strictly restricted to `super_admin` (`require_admin_scope("super_admin")`). Lower scopes (e.g. `content_editor`) are rejected with HTTP 403.
   - Dispatches a one-time push notification to all affected families via B.17's `NotificationDispatchService`.
   - Notification dispatch failure is logged as an alertable partial-failure without rolling back the date correction in the database.
   - Generates an immutable audit log entry in E.28's `AuditLogService`.

### 8.3 Sub-Feature Seam Mapping

| Task ID | Component / Endpoint | Consumes / Reuses | Produces / Output |
|---|---|---|---|
| **B-01** | `GET /v1/ramadan/campaign-status`<br>`GET/POST/PATCH /v1/admin/ramadan/campaigns` | A.1 Parent Profile (`region`), B-02 `HijriCalendarService` | `api.ramadan-campaign-status`<br>Phase, current night, season dates |
| **B-02** | Internal `HijriCalendarService` | External Hijri calculation library | `domain.hijri-calendar-service`<br>Algorithmic dates & moon-sighting overrides |
| **B-03** | `GET /v1/ramadan/missions/{night}` | E.29 `ContentService` (`content_versions`), B-01 Campaign | `api.ramadan-missions`<br>Mission payload + `gamification_suppressed` |
| **B-04** | `POST /v1/ramadan/fasting-logs` | A.7 `HabitService` (`fasting_approach`) | `api.ramadan-fasting-logs`<br>Validated append-only log entry |
| **B-05** | `POST /v1/ramadan/missions/{night}/complete` | A.11 `RewardService`, `reward_ledger`, B-03 Missions | `api.ramadan-journey-progress`<br>Idempotent progress & seasonal reward grant |
| **B-06** | `GET /v1/ramadan/family-aggregate` | B-04 `fasting_logs`, B-05 `ramadan_journey_progress`, A.1 Family | `api.ramadan-family-aggregate`<br>Rollup without per-child array |
| **B-07** | `POST /v1/ramadan/certificates`<br>`POST /v1/ramadan/eid-cards` | A.11 `ShareCardService`, B-05 Progress, Parent Gate | `api.ramadan-certificates`<br>PII-excluded shareable artifacts |
| **B-08** | `POST /v1/admin/ramadan/eid-date-override` | B-02 `HijriCalendarService`, B.17 Notifications, E.28 Audit | `api.admin-ramadan-eid-override`<br>Corrected campaign dates + push dispatch |

### 8.4 Database Schema Additions (`ramadan` context)

```sql
-- Campaign lifecycle per region
CREATE TABLE ramadan_campaigns (
    campaign_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    region VARCHAR(64) NOT NULL,
    hijri_start_date DATE NOT NULL,
    eid_date DATE NOT NULL,
    eid_date_overridden BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_ramadan_campaigns_region_year UNIQUE (region, (EXTRACT(YEAR FROM hijri_start_date)))
);
CREATE INDEX ix_ramadan_campaigns_region ON ramadan_campaigns(region);

-- Append-only moon-sighting override audit
CREATE TABLE moon_sighting_overrides (
    override_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    region VARCHAR(64) NOT NULL,
    corrected_eid_date DATE NOT NULL,
    source_note TEXT NOT NULL,
    applied_by_admin_id UUID NOT NULL,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX ix_moon_sighting_overrides_region ON moon_sighting_overrides(region);

-- 30-night mission mapping
CREATE TABLE ramadan_missions (
    mission_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL REFERENCES ramadan_campaigns(campaign_id) ON DELETE CASCADE,
    night_number INT NOT NULL,
    content_version_id UUID NOT NULL,
    is_laylatul_qadr BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT ck_ramadan_missions_night_number CHECK (night_number BETWEEN 1 AND 30),
    CONSTRAINT uq_ramadan_missions_campaign_night UNIQUE (campaign_id, night_number)
);
CREATE INDEX ix_ramadan_missions_campaign_night ON ramadan_missions(campaign_id, night_number);

-- Idempotent child journey progress
CREATE TABLE ramadan_journey_progress (
    child_id UUID NOT NULL,
    mission_id UUID NOT NULL REFERENCES ramadan_missions(mission_id) ON DELETE CASCADE,
    completed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT pk_ramadan_journey_progress PRIMARY KEY (child_id, mission_id)
);
CREATE INDEX ix_ramadan_journey_progress_child_id ON ramadan_journey_progress(child_id);

-- Append-only fasting logs
CREATE TABLE fasting_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    child_id UUID NOT NULL,
    night_number INT NOT NULL,
    status VARCHAR(32) NOT NULL,
    logged_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT ck_fasting_logs_night_number CHECK (night_number BETWEEN 1 AND 30),
    CONSTRAINT ck_fasting_logs_status CHECK (status IN ('fasted_full', 'fasted_practice', 'education_only'))
);
CREATE INDEX ix_fasting_logs_child_night ON fasting_logs(child_id, night_number);

-- Generated certificates
CREATE TABLE ramadan_certificates (
    certificate_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    child_id UUID NOT NULL,
    certificate_url TEXT NOT NULL,
    generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX ix_ramadan_certificates_child ON ramadan_certificates(child_id, generated_at DESC);
```

### 8.5 Edge Cases Matrix & Error Handling

| # | Edge Case Scenario | Expected Architectural Behavior |
|---|---|---|
| **EC-1** | Family Region changes mid-Ramadan | Window recalculates future phase against new region's campaign. Completed `ramadan_journey_progress` rows remain intact (progress is keyed to child & mission, not region). |
| **EC-2** | Child age band changes mid-Ramadan | Completed nights remain credited; remaining nights serve the new age-band content version via E.29's standard version resolution. |
| **EC-3** | Parent modifies fasting approach mid-Ramadan | Historical `fasting_logs` rows remain untouched; new submissions are validated against the newly configured approach. |
| **EC-4** | Multi-child family with divergent fasting approaches | Family Aggregate endpoint computes aggregate completion without exposing individual child arrays or rankings. |
| **EC-5** | Missed nights | Missed nights remain unlocked and completable retroactively; no lockout or shaming is applied. |
| **EC-6** | Moon-sighting dispute alters Eid date | Admin invokes `POST /v1/admin/ramadan/eid-date-override`. Campaign record updates, B.17 sends one-time push, client re-syncs on next open. |
| **EC-7** | Trial expires before Day 28 | Ramadan-specific conversion card does not render; C.24's standard subscription messaging takes precedence. |
| **EC-8** | Read-only report invite shared with non-app user | Web landing page provides graceful app-install affordance without broken links. |

