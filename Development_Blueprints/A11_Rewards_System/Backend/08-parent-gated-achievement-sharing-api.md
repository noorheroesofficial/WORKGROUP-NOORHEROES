# B-08 — Parent-Gated Achievement Sharing API (User/Parent)

## 1. Feature Context
Part of Feature A.11 — Rewards System. Generates a shareable achievement card, gated behind parent verification, with a hard guarantee against exposing child PII.

## 2. Parent Feature
A.11 Rewards System — Backend (FastAPI)

## 3. Sub-feature
B-08 Parent-Gated Achievement Sharing API (User/Parent)

## 4. Objective
Implement `POST /v1/achievements/{id}/share-card`, backing FR-12.

## 5. Business Requirements
- Generating a shareable card requires Parent Profile verification (recent PIN/biometric step-up) before card generation.
- The card never includes child ID, DOB, or location (FR-12, a hard rule).
- Routes through the OS share sheet only after the gate passes (client-owned, K-05); this endpoint only produces the card asset/URL.

## 6. Existing Architecture
Extends the `rewards` bounded context. Reuses the existing elevated-session mechanism (`require_elevated_session`, `core/deps.py`) already used for other parent step-up-gated actions across the platform (per A.1).

## 7. Existing Code to Reuse
- `require_elevated_session(parent, redis)` (`core/deps.py`).
- `get_current_parent` dependency.
- Existing image-generation/rendering infrastructure if already present in the platform (confirm before introducing a new rendering library — do not add a second image-generation dependency if one already exists for another feature, e.g. Admin's share-card or story-cover generation).

## 8. Files to Create
- `src/noorheroes/modules/rewards/card_generator.py` — card composition logic (PII-exclusion enforced structurally in the data passed to the renderer).
- `tests/modules/rewards/test_share_card_pii_exclusion.py`
- `tests/modules/rewards/test_share_card_elevation_gate.py`

## 9. Files to Modify
- `src/noorheroes/modules/rewards/schemas.py` — `ShareCardResponse`.
- `src/noorheroes/modules/rewards/service.py` — `generate_share_card(achievement_id, child_id)`.
- `src/noorheroes/modules/rewards/api.py` — add route.

## 10. Backend Requirements
- Endpoint requires `require_elevated_session` before any card generation logic runs.
- Card composition function accepts only an explicit allowlist of fields (badge/achievement name, icon, celebratory copy) — structurally excludes any child-identifying field from ever reaching the renderer, rather than relying on the renderer to omit fields it received.
- `card_image_url` is a short-lived, signed URL with an `expires_at`.
- Rate-limit share-card generation per child to prevent abuse (e.g., via existing Redis rate-limit infrastructure).

## 11. KMP Requirements
Consumed by K-05 (Parent-Gated Achievement Sharing Flow).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract

**Required API**
- **HTTP Method:** POST
- **Endpoint:** `/v1/achievements/{id}/share-card`
- **Auth:** Bearer (parent session only — requires Parent Profile verification per FR-12).
- **Response 200:** `{ "card_image_url": "...", "expires_at": "..." }` — generated card contains no child ID/DOB/location.
- **Error Responses:** `401`/`403` if not elevated; `404` unknown achievement.

## 14. Database Requirements
No new persistent table required beyond existing badge/achievement records (B-04); generated card assets may be stored transiently (object storage with short TTL) rather than in PostgreSQL.

## 15. Validation
- Test: generated card payload structurally excludes PII fields — assert the renderer input object's type/schema has no `child_id`/`dob`/`location` field at all (not just that it's empty).
- Test: request without a valid elevated session is rejected before any card-generation work occurs.

## 16. Authentication
Bearer JWT, parent session.

## 17. Authorization
Requires `require_elevated_session` (recent PIN/biometric step-up), not just a valid parent token.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Missing/expired elevation | 401/403, gate must be re-passed client-side |
| Unknown `achievement_id` | 404 |
| Card-rendering failure | 5xx with retry guidance; no partial/corrupt card URL returned |

## 19. Offline First
N/A — card generation requires connectivity (matches PRD's general achievement-store-purchase-requires-connectivity precedent for security-sensitive actions).

## 20. Local Data
N/A (backend).

## 21. Localization
Card copy generated in the child's/family's active locale (EN/HI/AR/UR), including correct RTL text rendering for Arabic/Urdu card variants.

## 22. RTL
Card asset generation must correctly render RTL text where the active locale is Arabic/Urdu.

## 23. Analytics
Emit `achievement_share_gate_opened`, `achievement_share_completed` per PRD §1.19 (gate-opened fired client-side on modal open; completed fired on this endpoint's successful response).

## 24. Performance
Card generation is not on the hot reward-award path; a slightly higher latency budget is acceptable (target reasonable, e.g. p95 < 2s) given it's a deliberate, infrequent user action.

## 25. Security
PII-exclusion is enforced structurally (allowlist input to the renderer), not by post-hoc scrubbing — the primary defense against an accidental future field leak (PRD §12.6).

## 26. Library Requirements
FastAPI, existing image-generation/rendering library (reuse if present), object storage (R2, existing infra), Pydantic v2.

## 27. Testing
- Unit: PII-exclusion structural test (mandatory).
- Integration: elevation gate → card generation → signed URL response.
- Rate-limit test: excessive requests throttled.

## 28. Documentation
OpenAPI docs stating the elevation requirement and the PII-exclusion guarantee explicitly as part of the endpoint's contract.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Allowlist-Based Card Data Composition**
- Files to Create: `card_generator.py`
- Business Rules: FR-12.
- Implementation Details: explicit allowlist of fields passed to the renderer; no child-identifying field type exists in the composition function's input model.
- Tests: PII-exclusion structural test (mandatory).
- Do Not Change: never widen the allowlist to include identifying fields without explicit governance sign-off.
- Definition of Done: structural test passing.

**Task 02 — Implement `generate_share_card()` Service Method**
- Files to Modify: `service.py`
- Existing Files to Reuse: existing image-generation infra if present.
- Implementation Details: signed URL generation with `expires_at`.
- Definition of Done: correct card asset + URL produced.

**Task 03 — Implement Endpoint with Elevation Gate**
- Files to Modify: `api.py`
- Existing Files to Reuse: `require_elevated_session`.
- Authentication/Authorization: per §16/§17.
- Tests: elevation-gate rejection test (mandatory).
- Definition of Done: unelevated requests rejected before any generation work.

**Task 04 — Add Rate Limiting**
- Implementation Details: existing Redis rate-limit infra applied per child.
- Tests: excessive-request throttling test.
- Definition of Done: verified.

**Task 05 — Add Localization/RTL Support in Card Rendering**
- Implementation Details: correct text rendering per active locale.
- Tests: RTL rendering test for Arabic/Urdu.
- Definition of Done: verified across all four locales.

**Task 06 — Add Documentation & Final Review**
- Documentation: OpenAPI notes per §28.
- Do Not Change: PII-exclusion allowlist design.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Share-card endpoint live, gated behind parent elevation, structurally guaranteed PII-free, correctly localized/RTL-rendered.

## 31. Final Verification Checklist
- [x] Elevation gate enforced before any card-generation work
- [x] PII-exclusion structural test passing (no child_id/dob/location field reachable)
- [x] Signed URL with `expires_at` returned
- [x] Rate limiting verified
- [x] RTL/localization rendering verified for all four locales
- [x] OpenAPI documentation complete
