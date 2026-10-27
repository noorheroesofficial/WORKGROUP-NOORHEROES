# B-07 — Signed Media Manifest & Delivery API

## 1. Feature Context
The actual access-control enforcement point for episode media: issues short-TTL signed CDN URLs only after re-validating unlock state and entitlement server-side at issuance time. Every other layer (catalog UI hints, client-cached unlock state) is advisory; this endpoint is authoritative. An unlock-bypass confirmed here is a P0 rollback trigger.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
1.7 Signed Media Manifest & Delivery API (ID: **B-07**)

## 4. Objective
Implement `GET /v1/content/{id}/manifest` inside the existing `media` module, re-validating unlock state via B-02 and entitlement via the existing `subscriptions` module at request time, then issuing a 15-minute signed CDN URL plus captions/audio-tracks/interactive-script payload.

## 5. Business Requirements
- FR-7: player supports captions, audio-track selection, quality selection.
- §3.4 API spec: server re-validates unlock state at manifest-issuance time, never trusts client-cached state.
- §12.1 Threat Analysis: unlock-bypass mitigated by server-authoritative re-validation at every manifest issuance.
- §12.9 Pre-launch checklist: penetration test — request manifest for a locked episode directly via API, confirm `403`.
- NFV: signed URL TTL 15 minutes, never a permanently public media URL; never log full signed URLs in plaintext.

## 6. Existing Architecture
Extends the existing `media` module (`MediaAsset`, `MediaRepository`, `MediaService.initiate_upload()`) with a new read/issuance path. Calls B-02's `UnlockEngine.get_unlock_state()` and the existing `subscriptions` module's `SubscriptionService.get_entitlement()` in-process before touching the CDN signing layer.

## 7. Existing Code to Reuse
- `modules/media/service.py::MediaService` (extend, do not fork)
- `modules/content/unlock_engine.py::UnlockEngine` (B-02)
- `modules/subscriptions/service.py::SubscriptionService.get_entitlement()`
- `core/deps.py::get_current_child`
- `infrastructure/` CDN signing integration (referenced by existing `MediaService.initiate_upload()`'s R2 pre-signed URL pattern — reuse the same signing infrastructure for playback delivery, not a new integration)

## 8. Files to Create
- `src/noorheroes/modules/media/manifest_schemas.py` — `ManifestResponse`
- `src/noorheroes/modules/media/manifest_service.py` — `ManifestService(BaseService)`
- `tests/modules/media/test_manifest_service.py`
- `tests/modules/media/test_manifest_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/media/api.py::MediaRouter` — add `GET /v1/content/{id}/manifest`

## 10. Backend Requirements
- `ManifestService.issue_manifest(child_id, episode_id)`: calls `UnlockEngine.get_unlock_state()` — if `locked`, return `403 EPISODE_LOCKED` immediately, no CDN call made. Calls `SubscriptionService.get_entitlement()` — if the series is tier-gated and the family lacks entitlement, return `403 ENTITLEMENT_REQUIRED`.
- On pass: issues a signed URL with 15-minute TTL via the existing CDN signing infrastructure, single-use-preferred where the CDN supports it; assembles `captions`, `audio_tracks`, `interactive_script` (choice-point data for offline branch mirroring) into the response.
- Logging: log only `content_id` and a hash of the signed URL — never the full signed URL in plaintext application logs.
- This endpoint is never cached (always-live check) — explicitly bypasses any Redis/CDN response caching applied to B-01's catalog reads.

## 11. API Contract

### `GET /v1/content/{id}/manifest`
- Auth: Bearer (child-mode) + entitlement + unlock-state check (server re-validates at issuance time). Response 200: `{ "playback_url": "https://cdn.../signed?exp=...", "expires_at": "...", "captions": [...], "audio_tracks": [...], "interactive_script": {...} }`. Errors: `403 EPISODE_LOCKED` (race-condition guard), `403 ENTITLEMENT_REQUIRED`. Security: signed URL TTL 15 minutes, single-use-preferred, never permanently public.

## 12. Database Requirements
- No new tables — reads `story_episode` (B-01), `episode_unlock_state` (B-02), existing subscription/entitlement tables.

## 13. Validation
- Episode existence and non-withdrawn status checked before unlock/entitlement evaluation (a withdrawn episode returns the same `410` semantics as B-01's detail read, not a `403`).

## 14. Authentication
Bearer child-mode session via `get_current_child`.

## 15. Authorization
Server-side unlock-state + entitlement re-validation is the authorization mechanism itself — no separate RBAC layer beyond authenticated child session.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Episode locked (stale client UI) | `403 EPISODE_LOCKED` — no CDN call made, no leakage of media URL |
| Series tier-gated, family lacks entitlement | `403 ENTITLEMENT_REQUIRED` |
| Episode withdrawn | `410 CONTENT_WITHDRAWN` (same semantics as B-01) |
| CDN signing-key/service failure | `503`, failover within 5s per PRD NFR if a secondary signing path exists, else clear retry error |
| Unlock Engine internal error | Fail-closed per B-02's contract — treated as locked, `403` |
| Anomalous concurrent-session use of the same signed URL | Not hard-blocked; logged as a fraud signal for monitoring (per PRD §12.1) |

## 17. Security
- Server-authoritative re-validation at every single call — the core mitigation for unlock-bypass and the subject of the mandatory penetration test.
- Signed URLs never logged in plaintext (content_id + hash only).
- 15-minute TTL, single-use-preferred; no permanently public media URL under any circumstance.
- Monitoring hook for anomalous concurrent signed-URL usage (credential/URL-sharing fraud signal).

## 18. Analytics
Emit via `OutboxWriter`: `story_player_opened` (fired by the client on successful manifest fetch, correlated server-side via request logging).

## 19. Performance
- Unlock-state and entitlement checks must both be fast, indexed reads (B-02's `get_unlock_state()` is already a single indexed query) — this endpoint sits on the player's cold-start critical path (PRD target: p95 < 1.5s cached manifest, < 2s video start-to-first-frame on 3G-equivalent throttling).
- No response caching of any kind (correctness requirement, not just a performance choice).

## 20. Library Requirements
No new libraries — reuses existing CDN signing infrastructure from `MediaService`.

## 21. Testing
- Unit: locked-episode rejection, entitlement rejection, withdrawn-episode `410` precedence over `403`.
- Integration: **mandatory penetration test** — direct manifest request for a locked episode (bypassing UI), confirm `403 EPISODE_LOCKED` (per PRD §12.9).
- Integration: signed URL TTL and non-public-access verified against the CDN configuration in a staging environment.

## 22. Documentation
Update OpenAPI schema; document the CDN signing-key configuration by env var name only (never values) per the PRD backend AI-prompt's explicit requirement.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Implement `ManifestResponse` Schema**
Objective: Define the response shape (`playback_url`, `expires_at`, `captions`, `audio_tracks`, `interactive_script`). Follow: existing Pydantic v2 conventions in `modules/media`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `ManifestService.issue_manifest()` Unlock + Entitlement Gate**
Objective: Sequential unlock-check → entitlement-check → CDN-signing chain, short-circuiting on the first failure with no CDN call made. Dependencies: B-02's `UnlockEngine`, existing `SubscriptionService`. Business Rules: withdrawn precedence over locked; unlock-engine error fails closed. Tests: all §16 scenarios. Definition of Done: tests pass.

**Task 03 — Wire CDN Signed-URL Issuance**
Objective: Reuse existing CDN signing infrastructure (the same pattern as `MediaService.initiate_upload()`'s R2 pre-signed flow) for playback URL issuance with a 15-minute TTL. Security: log only content_id + URL hash, never the full URL. Tests: TTL correctness, no-plaintext-logging assertion (scan logs in test for the raw signed URL string, assert absent). Definition of Done: logging assertion passes.

**Task 04 — Add Router Endpoint**
Objective: Wire `GET /v1/content/{id}/manifest` into `MediaRouter`. Tests: covered by Task 06. Definition of Done: endpoint live, documented, never cached.

**Task 05 — Implement Mandatory Penetration Test**
Objective: Direct manifest request for a locked episode (bypassing UI assumptions), confirm `403 EPISODE_LOCKED` (PRD §12.9 pre-launch requirement). Definition of Done: test passes and is registered as a required CI/pre-launch check.

**Task 06 — Add Remaining Unit & Integration Tests**
Objective: Full coverage per §21. Definition of Done: all green in CI.

**Task 07 — Update OpenAPI Documentation**
Objective: Regenerate/diff-classify; document CDN signing-key env var names only. Definition of Done: non-breaking diff confirmed, no secret values present anywhere in docs.

**Task 08 — Final Code Review**
Objective: Confirm zero code path issues a signed URL without a fresh unlock+entitlement check; confirm no plaintext URL logging anywhere. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] Unlock state re-validated server-side on every single manifest request (no client-trust path exists)
- [ ] Entitlement re-validated server-side on every single manifest request
- [ ] Direct manifest request for a locked episode returns `403 EPISODE_LOCKED` (penetration test passing)
- [ ] Signed URL TTL is exactly 15 minutes; never a permanently public URL
- [ ] Full signed URLs never appear in plaintext logs (only content_id + hash)
- [ ] Withdrawn-content precedence (`410`) correctly takes priority over lock/entitlement checks
- [ ] This endpoint is never response-cached
- [ ] Anomalous concurrent signed-URL usage is monitored (not silently ignored)
- [ ] No PostgreSQL/Redis credentials modified

## 25. Definition of Done
Media access is gated exclusively through a server-authoritative, freshly-revalidated, short-TTL signed-URL issuance path with zero client-trust shortcuts — closing the loop that B-02's Unlock Engine opens and satisfying the PRD's zero-tolerance unlock-bypass guarantee.
