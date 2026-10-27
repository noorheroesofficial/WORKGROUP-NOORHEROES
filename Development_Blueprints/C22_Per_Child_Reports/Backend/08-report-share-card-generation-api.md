# Blueprint: Report Share Card Generation API

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI). Module: `src/noorheroes/modules/dashboard/`, integrating `src/noorheroes/modules/identity/` (C.19 step-up) and the reward/share-card pattern established in A.11. Delivers `POST /v1/parent/reports/{child_id}/share-card`.

## 2. Parent Feature
C.22 — Per-Child Reports.

## 3. Sub-feature
B-08 — Report Share Card Generation API.

## 4. Objective
Generate a PII-free, nickname/initial-plus-badge achievement card for WhatsApp sharing, gated by a fresh Parent PIN/biometric step-up verification, reusing A.11's hardened share-card content-safety pattern rather than reimplementing it.

## 5. Business Requirements
Source: PRD §1.7 FR-10, §1.9 Acceptance Criteria, §1.10 Edge Case #2, #7, #9, §3.4, §5 item 5.
- Share flow generates a card showing nickname/initial, badge, and no PII — generated only after Parent PIN verification (FR-10, canonical share-card contract for any report-originated sharing).
- Already-shared cards remain valid/unaffected even if the underlying badge is later revoked (Edge Case #2) — a static, point-in-time artifact.
- Export/share requested against a `content_safety_passed = false` report falls back to the last passing report (Edge Case #7).
- Export/share requested offline is blocked with a clear "needs internet" message (Edge Case #9).

## 6. Existing Architecture
Reuses A.11's established share-card content-safety pattern (cross-ref A.11 FR-12) and C.19's Parent PIN/biometric step-up mechanism — this blueprint applies both to report-originated sharing specifically, it does not redefine either.

## 7. Existing Code to Reuse
- `require_elevated_session(parent, redis)` (`core/deps.py`) — confirmed exact mechanism, identically reused by A.11 B-08 and C.23 B-03 for their own step-up-gated actions; must require a **fresh** pass, not merely "currently elevated" (per C.23 B-03's note that freshness, not just current-elevation, is the requirement).
- A.11's card-composition logic: `src/noorheroes/modules/rewards/card_generator.py` plus `modules/rewards/service.py::generate_share_card(achievement_id, child_id)` — extend the card-composition function with a report-context card type (nickname/initial + badge/achievement, same explicit-allowlist-of-fields approach A.11 already uses to structurally exclude child-identifying data) rather than building a second card-generation service.
- `require_parent_session_only` (C.20 B-01).
- `ContentSafetyValidator` fallback pattern (C.20), reused per Edge Case #7.
- `MediaService`'s existing R2 pre-signed URL / CDN signing infrastructure (A.3 B-07) — reused for the signed `card_image_url`, consistent with B-07's PDF export using the same signing mechanism.

## 8. Files to Create
- `tests/modules/dashboard/test_report_share_card_generation_api.py`
- `tests/modules/dashboard/test_report_share_card_pii_absence_structural.py`

## 9. Files to Modify
- `src/noorheroes/modules/dashboard/schemas.py` — add `ShareCardRequest`, `ShareCardResponse`
- `src/noorheroes/modules/dashboard/service.py` — add `generate_share_card(parent_ctx, child_id, step_up_token)`
- `src/noorheroes/modules/dashboard/api.py` — add `POST /v1/parent/reports/{child_id}/share-card`

## 10. Backend Requirements
- Route: `POST /v1/parent/reports/{child_id}/share-card`, gated by `require_parent_session_only` + a **mandatory fresh step-up token** (C.19), validated before any card generation begins.
- `generate_share_card()`:
  1. Validate the step-up token is present and fresh (per C.19's existing token-freshness rule); reject with `403 STEP_UP_REQUIRED` if missing/expired.
  2. Validate family-ownership on `child_id`.
  3. Resolve the report data to source the achievement/badge from, applying the content-safety fallback (Edge Case #7) exactly as B-07.
  4. Build the card payload using **only** `nickname_or_initial` and `badge_id`/`achievement_label` — reusing `modules/rewards/card_generator.py`'s explicit-allowlist card-composition function (A.11 B-08), not a new one.
  5. Render/compose the card image, upload via `MediaService`'s existing R2/CDN signing infrastructure (A.3 B-07), generate a signed short-TTL `card_image_url` + `expires_at`.
  6. The generated card is a static artifact: once created, it is never retroactively invalidated by a later badge revocation (Edge Case #2) — no live-reference lookup embedded in the card.

## 11. KMP Requirements
Consumed by K-08 (`ShareReportFlow`), which must obtain the step-up token via `ParentGateLauncher.requireParentAuth(TriggerContext.AchievementShare)` (C.19) before calling this endpoint.

## 12. NextJS Requirements
N/A.

## 13. API Contract
- **HTTP Method:** POST
- **Endpoint:** `/v1/parent/reports/{child_id}/share-card`
- **Auth:** Bearer, parent session only, **plus fresh Parent PIN/biometric step-up token** (C.19)
- **Request:** path `child_id: str`; header/body: step-up token per C.19's existing convention
- **Response 200:**
```json
{ "card_image_url": "string (signed, short-TTL)", "expires_at": "ISO-8601" }
```
- **Authentication:** Bearer parent session + step-up token
- **Authorization:** Family-ownership on `child_id`
- **Validation:** Step-up token required and fresh; `child_id` required
- **Error Responses:** `403 STEP_UP_REQUIRED` (missing/expired step-up), `403`/`404` `ChildScopeViolationError`, `401` invalid session

## 14. Database Requirements
No new tables; card is a rendered artifact in object storage, not a DB row. Sources badge/achievement data from A.11's existing reward tables.

## 15. Validation
- `child_id` required, family-owned.
- Step-up token required, must be fresh per C.19's existing freshness window.
- Card payload validated (via the field-absence test, §27) to contain no PII fields.

## 16. Authentication
Bearer parent session + fresh step-up token (two-factor requirement specific to this write action, mirroring A.11's pattern).

## 17. Authorization
Family-ownership check, additive to both the base session gate and the step-up requirement.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Missing/expired step-up token | `403 STEP_UP_REQUIRED`, card never generated |
| Cross-family `child_id` | `403`/`404` `ChildScopeViolationError` |
| Underlying report `content_safety_passed = false` | Falls back to last passing report |
| Client offline | Blocked client-side before this endpoint is called (K-08's responsibility) |

## 19. Offline First
N/A server-side by design — write action requiring a live, server-validated step-up token; offline block is a client-side (K-08) responsibility per Edge Case #9.

## 20. Local Data
N/A (backend).

## 21. Localization
`achievement_label`/badge copy pre-localized per the parent's selected locale, reusing A.11's existing localization pattern for badge names.

## 22. RTL
N/A (backend; card image RTL text rendering, if applicable, is a rendering-library concern mirroring B-07's PDF RTL note).

## 23. Analytics
`report_share_gate_opened` / `report_share_completed` fired client-side (K-08).

## 24. Performance
Card generation should complete well within the parent's expectation for a "share" action (sub-second to low-single-digit-second range); reuses A.11's existing card-rendering performance characteristics.

## 25. Security
The mandatory step-up token and the PII field-absence test are this endpoint's two highest-priority guarantees — the same tier of criticality as B-03's structural no-transcript guarantee. No `child_id`, DOB, or location field may ever appear in the card payload.

## 26. Library Requirements
No new dependencies; reuses A.11's existing image-composition library.

## 27. Testing
1. Unit test: card generated successfully with valid step-up token and valid badge/achievement.
2. Unit test: missing step-up token rejected with `403 STEP_UP_REQUIRED`, no card generated.
3. Unit test: expired step-up token rejected.
4. Unit test: cross-family `child_id` rejected.
5. Unit test: content-safety-failed report triggers fallback to last passing report.
6. **Field-absence test:** scan the generated card's underlying data payload for any field matching `/child_id|dob|location|address/i` and assert none are present.
7. Unit test: a card generated before a badge revocation remains retrievable/valid after the revocation (Edge Case #2).
8. Integration test: full parent-gate-to-card flow.

## 28. Documentation
OpenAPI docstring stating the mandatory step-up requirement and the PII-free guarantee explicitly.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Enforce Step-Up Token Requirement**
- Task ID: B08-T01
- Objective: Reject card generation without a fresh C.19 step-up token.
- Why This Is Required: FR-10's mandatory gating requirement.
- Existing Architecture to Follow: C.19's existing step-up/elevated-session dependency.
- Existing Files to Reuse: `require_elevated_session` (or platform's exact equivalent, confirmed against `core/deps.py`).
- Files to Create: none.
- Files to Modify: `api.py` (dependency wiring).
- Implementation Details: Route dependency chain includes the step-up check before any service call.
- Business Rules: FR-10.
- Validation: Token freshness per C.19's existing window.
- Error Handling: `403 STEP_UP_REQUIRED`.
- Security: This IS the primary security control for this endpoint.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Docstring.
- Dependencies: C.19's step-up mechanism must exist.
- Do Not Change: C.19's step-up token issuance logic.
- Expected Result: Requests without a valid step-up token never reach card generation.
- Definition of Done: Task 04's step-up tests pass.

**Task 02 — Implement generate_share_card Using A.11's ShareCardService**
- Task ID: B08-T02
- Objective: Compose the PII-free card payload and apply the content-safety fallback.
- Why This Is Required: Core business logic, reusing rather than duplicating A.11's pattern.
- Existing Architecture to Follow: A.11's `ShareCardService` composition function.
- Existing Files to Reuse: `ShareCardService`, `ContentSafetyValidator` fallback.
- Files to Create: none.
- Files to Modify: `service.py`.
- Implementation Details: Per §10 steps 2–6.
- Business Rules: FR-10, Edge Case #2, #7.
- Validation: Family-ownership.
- Error Handling: Per §18.
- Security: PII-field exclusion at composition time.
- Performance: N/A.
- Localization: Reuse A.11's badge-label localization.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Docstring citing FR-10.
- Dependencies: Task 01, A.11's `ShareCardService`.
- Do Not Change: A.11's underlying badge-award logic.
- Expected Result: Card generated correctly, static and revocation-unaffected.
- Definition of Done: Edge Case #2 verified.

**Task 03 — Implement Route and Signed URL Generation**
- Task ID: B08-T03
- Objective: Expose `POST /v1/parent/reports/{child_id}/share-card`.
- Why This Is Required: Public contract delivery.
- Existing Architecture to Follow: Router `Depends()` pattern; existing signed-URL storage utility.
- Existing Files to Reuse: `api.py`, storage-signing utility.
- Files to Create: none.
- Files to Modify: `api.py`.
- Implementation Details: Per §13.
- Business Rules: FR-10.
- Validation: Per §15.
- Error Handling: Per §18.
- Security: Inherits step-up gate.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: OpenAPI summary.
- Dependencies: Tasks 01–02.
- Do Not Change: N/A.
- Expected Result: Endpoint live.
- Definition of Done: Matches §13.

**Task 04 — Write Test Suite Including PII Field-Absence Test**
- Task ID: B08-T04
- Objective: Cover §27, with the field-absence test as the highest-priority guarantee alongside the step-up requirement.
- Why This Is Required: PRD §5 item 5 explicitly names this as one of the two top-priority guarantees in the entire service.
- Existing Architecture to Follow: pytest + reflection/payload-scanning pattern (mirrors A.11's existing test).
- Existing Files to Reuse: A.11's existing field-absence test utility if present.
- Files to Create: `test_report_share_card_generation_api.py`, `test_report_share_card_pii_absence_structural.py`.
- Files to Modify: none.
- Implementation Details: 8 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact responses.
- Security: All tests here are security-critical.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings citing FR-10.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green; field-absence and step-up tests are CI-blocking.

## 30. Definition of Done
`POST /v1/parent/reports/{child_id}/share-card` live, requires a fresh C.19 step-up token, produces a PII-free card verified by a field-absence test, static-artifact behavior verified, content-safety fallback verified, all tests green.

## 31. Final Verification Checklist
- [ ] Fresh Parent PIN/biometric step-up token verified as mandatory before any card generation
- [ ] Field-absence test confirms no `child_id`/`dob`/`location`/`address` in the card payload (CI-blocking)
- [ ] Already-shared cards remain valid after later badge revocation (Edge Case #2)
- [ ] Content-safety-failed-report fallback verified
- [ ] Offline block enforced client-side, documented as this endpoint's assumption
- [ ] OpenAPI docs state the step-up + PII-free guarantees explicitly
