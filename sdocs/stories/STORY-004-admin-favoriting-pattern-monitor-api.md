---
id: STORY-004
epic: EPIC-014
kind: feature
title: Admin Favoriting Pattern Monitor API Endpoint
status: completed
priority: P0
prd: ../../PRD_Documents/Child App Supporting (13-18)/Feature_B14_Favorites.md
depends_on: [STORY-001, STORY-003]
produces: [api.favorites-pattern-report]
consumes: [type.favorite-models]
created: 2026-09-29
---

## User Story

As a Content / Editorial Administrator, I want to retrieve an aggregate, privacy-safe report of the most and least frequently favorited content items platform-wide, filterable by content type and date window, so that I can monitor content popularity and inform editorial planning without ever exposing individual child bookmark identities or child privacy.

## Acceptance Criteria

- [x] AC1: Given an authenticated admin session with `content_editor` scope, when `GET /admin/v1/favorites/pattern-report` is invoked without parameters, returns HTTP 200 OK with `FavoritingPatternReportResponse` containing items sorted by `favorite_count DESC` and summary metadata (`total_favorites`, `unique_content_count`).
- [x] AC2 (CI-Blocking Signature Privacy Gate): The response payload, query execution, and schemas NEVER select, serialize, or expose any `child_id`, `childId`, child names, parent tokens, or per-child breakdown under any circumstance.
- [x] AC3: Authentication & RBAC: Admin requests with `content_editor`, `admin:read`, or `*` scope succeed (200 OK). Unauthenticated requests return 401 `UNAUTHENTICATED`. Requests with insufficient scopes or non-admin tokens return 403 `FORBIDDEN`.
- [x] AC4: Canonical Route Parity: Both `/admin/v1/favorites/pattern-report` and `/v1/admin/favorites/pattern-report` are mounted and return identical responses.
- [x] AC5: Content Type Filtering: Parameter `content_type` (`story`, `surah`, `dua`, `all`) narrows aggregate results accordingly (case-insensitive, whitespace-tolerant). Unsupported types return HTTP 422 `VALIDATION_ERROR`.
- [x] AC6: Date Bounding: Parameters `date_from` and `date_to` (with `from`/`to`, `start_date`/`end_date` aliases) filter by `favorite.created_at`. If `date_from > date_to` or date string is invalid, returns HTTP 422 `VALIDATION_ERROR`.
- [x] AC7: Ordering & Limit: Parameter `order` (`desc`, `asc`) determines ranking direction. Parameter `limit` (clamped 1..100, default 50) bounds the returned page items.
- [x] AC8: Non-N+1 Title Resolution: For story content items, localized titles are batch-resolved from `story_episode` where available.
- [x] AC9: Read-Only HTTP Guards: Non-GET methods (POST, PUT, DELETE, PATCH) return HTTP 405 `Method Not Allowed` in the Universal Error Envelope.
- [x] AC10: Empty Dataset Clean Handling: Zero favorites in database returns 200 OK with `items: []`, `totalFavorites: 0`, and `uniqueContentCount: 0`.
- [x] AC11: Parameter Pollution Defense: Pydantic schemas enforce `extra='forbid'`, rejecting injected unknown or child fields with `ValidationError`.
- [x] AC12: Boundary Clamping: Min limit (`1`) and max limit (`100`) succeed; out-of-range (`0`, `101`, negative) return 422.
- [x] AC13: Order Normalization: Uppercase, mixed-case, and whitespace (`DESC`, `Asc`, `" desc "`) normalize cleanly to `desc`/`asc`.
- [x] AC14: Open Date Intervals: Single-sided date filters (`date_from` alone, `date_to` alone) and same-day bounds succeed with 200 OK.
- [x] AC15: Missing Title Resilience: Orphan or withdrawn story episodes and non-story items return `title: null` without errors.
- [x] AC16: Server Error Envelope: Unexpected database failures return HTTP 500 formatted in the Universal Error Envelope.
- [x] AC17: Deterministic Tie-Breaking: Content items with identical bookmark counts are ordered deterministically by `content_id ASC` in both DESC and ASC modes.
- [x] AC18: Pagination Truncation vs Global Totals: Setting `limit < unique_content_count` truncates `items` without corrupting global `totalFavorites` or `uniqueContentCount`.
- [x] AC19: Compound Filtering: Concurrently applying `content_type` AND `date_from` AND `date_to` evaluates SQL WHERE clauses accurately.
- [x] AC20: Negative Auth Guard: Caller sessions with `role="child"` or `role="parent"` lacking admin permissions are strictly rejected with HTTP 403 Forbidden.
- [x] AC21: Dual-Wire Compatibility: Schema supports camelCase wire serialization for Next.js and bidirectional snake_case/camelCase validation.
- [x] AC22: ISO-8601 Variants & Malformed Dates: Timestamps with `Z`, microseconds, and timezone offsets parse accurately; invalid dates return 422.
- [x] AC23: Intraday Inverted Timestamp Rejection: Intraday timestamps where `date_from > date_to` (e.g. 15:00 > 09:00) return 422 Unprocessable Entity.
- [x] AC24: Batch Multiple Story Title Mapping: Multiple story episodes in a single query map to their exact respective episode titles with zero cross-item corruption.

## Technical Notes

- Files in scope:
  - `src/noorheroes/modules/admin/favorites_report_schemas.py`
  - `src/noorheroes/modules/content/favorite_repository.py`
  - `src/noorheroes/modules/content/favorite_service.py`
  - `src/noorheroes/modules/admin/api.py`
  - `src/noorheroes/modules/admin/__init__.py`
  - `main.py`
  - `tests/modules/admin/test_favorites_pattern_report_api.py`
- Architecture references: `Development_Blueprints/B14_Favorites/Backend/04-admin-favoriting-pattern-monitor-api.md`, PRD §8/§9.

## Test Approach

- Unit, Integration, & Privacy Tests:
  - `tests/modules/admin/test_favorites_pattern_report_api.py`:
    - Strict privacy isolation tests (assert zero `child_id` / `childId` in payload or schema).
    - Aggregation accuracy tests (ranking, counts, and summaries match known database state).
    - RBAC authorization tests (content_editor, admin:read, super_admin -> 200; unauthorized scope / unauth / non-admin -> 401/403).
    - Query parameter filter tests (content_type allowlist, 422 on invalid, date ranges, 422 on from > to, limit, order asc/desc).
    - Dual-route parity tests (`/admin/v1/favorites/pattern-report` and `/v1/admin/favorites/pattern-report`).
    - Read-only HTTP 405 tests for POST/PUT/DELETE/PATCH.
