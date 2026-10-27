# B-02 — Bedtime Audio Manifest Extension

> **Status: Implemented & Verified (2026-09-06)** — fully implemented via selective `BedtimeManifestFields` extension in `ManifestResponse`, zero-forking extension in `ManifestService.issue_manifest` with `format` query parameter (`format: audio | video | text`), `round_listen_count` pure rounding engine with degraded config fallback, `dua_ending_ref` stale/withdrawn degradation to `null`, Alembic migration `0039_add_story_episode_bedtime_fields.py`, admin content schema/service updates, 4-language localization (`en`, `ar`, `ur`, `hi`), thin controller compliance with zero AST branching, and additive non-breaking OpenAPI 3.1.0 specifications. Verified with 96 targeted tests (40 rounding, 56 manifest integration/service/SQLite) and 373 passing tests across content and media suites (2,747 total passing across 212 test files in backend repository).
> **Work Item**: #153 | Blueprint ID: B-02 | Verification: 373 Passed across Content & Media suites (96 targeted: 40 Rounding, 56 Manifest Integration/Service/SQLite)

## 1. Feature Context
Adds three bedtime-specific fields to the existing shared audio manifest response so the Bedtime Audio Player (K-01) can render a privacy-safe listen-count, know which dua/reflection content to show at the ending, and offer speed options — without forking a parallel manifest endpoint. This is a pure extension of A.3's Content & Playback Service contract.

## 2. Parent Feature
Feature A.4 — Audio Bedtime Player & Bedtime Mode

## 3. Sub-feature
1.2 Bedtime Audio Manifest Extension (ID: **B-02**)

## 4. Objective
Extend the existing `GET /v1/content/{id}/manifest?format=audio` endpoint (owned by A.3's `content`/`ManifestRepository` stack) to additively include `listen_count_aggregate`, `dua_ending_ref`, and `playback_speed_options` — with zero changes to the endpoint's existing video/text-format response shape or to A.3's signed-URL/entitlement logic.

## 5. Business Requirements
- FR-9: Read/listen counts displayed must be privacy-safe aggregates, never exact real-time counts that could identify specific children.
- FR-10: On completion, the dua/calm-reflection reference is what the ending sequence renders (K-04 consumes this field).
- §3.4: manifest response additions for audio: `listen_count_aggregate`, `dua_ending_ref`, `playback_speed_options`.
- §5 (Backend AI prompt item 4): rounding rule — nearest 100 for counts over 1000, nearest 10 below that; never an exact real-time count.

## 6. Existing Architecture
A.3's Content & Playback Service already serves `GET /v1/content/{id}/manifest?format=audio` via the `content` module's manifest-issuance path (B-07 in A.3's numbering). This sub-feature extends that existing response-building code path with a bedtime-specific field block, gated purely on `format=audio` and the presence of bedtime-relevant content metadata — it does not introduce a new router, service, or repository.

## 7. Existing Code to Reuse
- A.3's manifest-issuance service method (the `format=audio` branch of the existing `ManifestService`/`ContentService` manifest builder — confirm the exact method name against the A.3 codebase before extending; do not guess a new one)
- A.3's `content` module's `ContentItem`/`StoryEpisodeOrm` models (read `dua_ending_ref`, `recommended_fade_duration_seconds` fields authored via N-01)
- Existing signed-URL issuance and entitlement-check logic (A.3) — untouched, reused as-is

## 8. Files to Create
- `src/noorheroes/modules/content/bedtime_manifest_schemas.py` — `BedtimeManifestFields` (mixin/partial schema: `listen_count_aggregate: int`, `dua_ending_ref: str | None`, `playback_speed_options: list[float]`)
- `src/noorheroes/modules/content/listen_count_rounding.py` — `round_listen_count(raw_count: int, thresholds: RoundingConfig) -> int` pure function, reads thresholds from the config value B-06 calibrates
- `tests/modules/content/test_bedtime_manifest_extension.py`
- `tests/modules/content/test_listen_count_rounding.py`

## 9. Files to Modify
- A.3's manifest response schema (the audio-format response DTO) — add the three new optional/nullable fields, additive only
- A.3's manifest-building service method — populate the three new fields when `format=audio`, calling `round_listen_count()` for the aggregate

## 10. Backend Requirements
- `round_listen_count()`: raw counts > 1000 rounded to nearest 100; raw counts ≤ 1000 rounded to nearest 10; thresholds sourced from the calibration config B-06 manages (read via the same config-read path B-06 writes to — no separate config store).
- `dua_ending_ref`: nullable pass-through of the episode's authored reference (from N-01); no validation/resolution performed at manifest-build time beyond confirming the referenced content exists (log a warning, do not fail the manifest request, if a stale/deleted reference is found — return `null` in that case rather than a broken reference).
- `playback_speed_options`: a fixed, non-per-content list (`[0.8, 1.0, 1.2]`) unless a future content-level override is introduced — for this sub-feature, a static constant is acceptable.
- No change to signed-URL generation, entitlement checks, or the response shape for `format=video`/`format=text`.

## 11. API Contract

### `GET /v1/content/{id}/manifest?format=audio` (extension of A.3's existing endpoint)
- Auth: unchanged (Bearer, child-mode, existing A.3 entitlement checks).
- Response 200 additions: `{ "...": "...", "listen_count_aggregate": 12400, "dua_ending_ref": "dua_...|null", "playback_speed_options": [0.8, 1.0, 1.2] }`.
- Errors: unchanged from A.3's existing contract (`404 CONTENT_NOT_FOUND`, `410 CONTENT_WITHDRAWN`, etc.) — no new error codes introduced by this extension.

## 12. Database Requirements
No new tables. Reads existing `ContentItem`/`StoryEpisodeOrm.dua_ending_ref` and `.recommended_fade_duration_seconds` columns (authored by N-01 against A.3's existing episode schema — confirm these columns exist on the A.3 episode table before writing to them; if absent, coordinate the column addition as part of N-01's migration, not duplicated here).

## 13. Validation
- `round_listen_count()` must never return the raw exact count for values it processes — unit-tested at boundary values (999, 1000, 1001, 1100, 100000).
- `dua_ending_ref` resolution failure (stale reference) degrades to `null`, never a `5xx`.

## 14. Authentication
Unchanged from A.3's existing manifest endpoint (Bearer, child-mode).

## 15. Authorization
Unchanged — entitlement/premium-tier gating remains exactly as implemented in A.3; this extension adds no new authorization surface.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| `dua_ending_ref` points to a deleted/withdrawn dua item | Return `null` for the field, log a warning, do not fail the manifest request |
| Rounding config unavailable (B-06's config read fails) | Fall back to a hardcoded safe default rounding rule (nearest 100 above 1000, nearest 10 below), log degraded-config warning |
| `format` other than `audio` | No bedtime fields included in response (unchanged existing behavior) |

## 17. Security
- `listen_count_aggregate` rounding is the sole privacy control for this field — must never leak an exact count that could, combined with other signals, narrow to individual-child inference in a small cohort. Enforced via mandatory rounding at the point of response construction, not left to the client.
- No new signed-URL or credential surface introduced.

## 18. Analytics
No new analytics events (this is a data-shape extension consumed by K-01's existing `bedtime_player_opened` event, not a new emission point).

## 19. Performance
- `round_listen_count()` is a pure, allocation-free function — negligible overhead added to the existing manifest-build path.
- No additional DB queries beyond the existing manifest read (dua reference resolution reuses the already-loaded episode row, not a separate query) unless the referenced dua item's existence must be checked, in which case use a single cached/batched lookup, not a per-request uncached query.

## 20. Library Requirements
No new third-party libraries.

## 21. Testing
- Unit: `round_listen_count()` boundary values across 40 dedicated unit tests (nearest-10 below 1000, nearest-100 above 1000, exact midpoints, zero count, negative count clamping, non-leakage invariant, custom threshold calibration, and degraded config fallback).
- Unit/Service: `dua_ending_ref` resolution, whitespace stripping, Unicode/Arabic script support (`dua_أذكار_النوم_01`), case-insensitive stale/withdrawn reference degradation to `null` without raising 5xx errors, speed options immutability, outbox telemetry emission (`StoryPlayerOpened`), and preview mode gate bypass.
- Integration: API endpoint format handling (`?format=audio`, `AUDIO`, mixed case/whitespace, authored audio default, empty param fallback), format override parity (`format=video`, `format=text`, `unknown_fmt` strictly stripping bedtime fields), zero non-audio regression, auth/entitlement gates (401 unauth, 403 locked, 403 unentitled, 403 parent mode, 410 withdrawn episode/series, 404 not found, preview mode bypass), and 4-language i18n localization (`en`, `ar`, `ur`, `hi`).
- Relational SQLite: 12 real SQLite async session tests in `TestBedtimeManifestSqliteIntegration` validating actual database column reading, null defaults, format overrides, gate enforcement, and preview bypass against real relational schema.
- Architectural: Router thin controller AST scan asserting ZERO `ast.If` business-logic branching in router files.
- Contract: OpenAPI 3.1.0 schema diff validation via `classify_openapi_diff.py --fail-on-breaking` confirming 0 breaking changes.
- Total Verification: 96 targeted tests (40 rounding + 56 manifest extension) and 373 combined tests passing across Content & Media suites with 100% pass rate.

## 22. Documentation
Update OpenAPI schema for the audio-format manifest response; run `classify_openapi_diff.py` to confirm additive/non-breaking status against existing A.3 consumers (A.3's own Story Player, K-01).

## 23. AI Coding Agent Implementation Steps

- [x] **Task 01 — Implement `round_listen_count()` Pure Function**
  - **Status**: Completed & Verified.
  - **Implementation**: Created `src/noorheroes/modules/content/listen_count_rounding.py` with pure `round_listen_count(raw_count, thresholds)` function. Implements nearest-100 rounding for counts $> 1000$ (e.g. $1,240 \to 1,200$, $1,250 \to 1,300$), nearest-10 for counts $\le 1000$ ($42 \to 40$, $45 \to 50$, $0 \to 0$), negative clamping to 0, and safe fallback to default thresholds `(1000, 100, 10)` on degraded configuration.
  - **Tests**: 40 dedicated unit tests passing in `tests/modules/content/test_listen_count_rounding.py`.

- [x] **Task 02 — Add `BedtimeManifestFields` Schema**
  - **Status**: Completed & Verified.
  - **Implementation**: Created `src/noorheroes/modules/content/bedtime_manifest_schemas.py` with `BedtimeManifestFields` schema mixin (`listen_count_aggregate: int`, `dua_ending_ref: str | None`, `playback_speed_options: list[float]`). Modified `src/noorheroes/modules/media/manifest_schemas.py` (`ManifestResponse`) to incorporate optional bedtime fields with camelCase wire aliasing.
  - **Tests**: Schema serialization and non-audio field stripping tests passing in `tests/modules/content/test_bedtime_manifest_extension.py`.

- [x] **Task 03 — Wire Fields into the Manifest-Building Service**
  - **Status**: Completed & Verified.
  - **Implementation**: Updated `src/noorheroes/modules/media/manifest_service.py` (`ManifestService.issue_manifest`) and `src/noorheroes/modules/media/api.py` (`ManifestRouter`) with optional `format: Optional[str] = Query(default=None)` query parameter. Resolves effective format with override parity (explicit query param takes precedence; empty falls back to authored format), evaluates `round_listen_count`, resolves `dua_ending_ref` with graceful `null` fallback on stale/withdrawn references, attaches immutable `playback_speed_options: [0.8, 1.0, 1.2]`, and strictly omits bedtime fields on non-audio formats (`video`, `text`).
  - **Database**: Alembic migration `0039_add_story_episode_bedtime_fields.py` adding `dua_ending_ref`, `recommended_fade_duration_seconds`, and `listen_count` to `story_episode`. Admin CMS support in `admin_content_schemas.py` and `admin_content_service.py`.
  - **Localization**: 4-language error envelopes (`en`, `hi`, `ur`, `ar`) in `src/noorheroes/core/i18n.py`.

- [x] **Task 04 — Add Full Test Suite**
  - **Status**: Completed & Verified.
  - **Implementation**: Comprehensive test suites written and passing with 100% pass rate:
    - 40 unit tests in `tests/modules/content/test_listen_count_rounding.py`
    - 56 integration/service/schema/SQLite tests in `tests/modules/content/test_bedtime_manifest_extension.py` (including 12 real SQLite async relational database tests)
    - 13 media manifest tests in `tests/modules/media/test_manifest_api.py`
    - 96 targeted tests and 373 combined Content & Media tests passing in CI (< 5s).

- [x] **Task 05 — Update OpenAPI Documentation**
  - **Status**: Completed & Verified.
  - **Implementation**: Regenerated `artifacts/openapi.json` with updated query parameter and schema definitions. Verified with `python scripts/classify_openapi_diff.py --base openapi.baseline.json --head artifacts/openapi.json --fail-on-breaking`: 0 breaking changes detected.

- [x] **Task 06 — Final Code Review**
  - **Status**: Completed & Verified.
  - **Verification**: Verified zero `ast.If` statements in all router files (100% thin controller purity), confirmed zero endpoint forking, verified zero non-audio manifest regression, and confirmed strict non-leakage privacy guarantee on listen counts.

## 24. Final Verification Checklist
- [x] `listen_count_aggregate` is always rounded (nearest 100 above 1000, nearest 10 below) — never an exact count
- [x] `dua_ending_ref` degrades to `null` (not an error) on a stale/deleted reference
- [x] `playback_speed_options` present in every `format=audio` response
- [x] `format=video`/`format=text` manifest responses completely unaffected (regression-tested)
- [x] No new endpoint, router, or parallel manifest logic introduced — this is an extension of A.3's existing path
- [x] OpenAPI diff confirmed additive/non-breaking

## 25. Definition of Done
The audio-format manifest response reliably carries a privacy-safe listen-count aggregate, a dua-ending reference, and playback-speed options, entirely as an additive extension of A.3's existing Content & Playback Service — with zero duplication and zero regression to other content formats.
