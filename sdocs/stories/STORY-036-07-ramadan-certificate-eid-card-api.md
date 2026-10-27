---
id: STORY-036-07
epic: EPIC-036
kind: feature
title: PII-Safe Ramadan Certificate & Eid Card Generation with Parent Gate
status: ready
priority: P1
prd: ../../PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md
depends_on: [STORY-036-05]
produces: [api.ramadan-certificates]
consumes: [type.ramadan-models, api.ramadan-journey-progress]
created: 2026-09-30
---

## User Story
As an authenticated parent, I want to generate a personalized Ramadan completion certificate and Eid greeting card behind Parent Gate verification, so that I can celebrate and share my child's achievements with extended family without exposing private child information.

## Acceptance Criteria
- [ ] AC1: Given an authenticated parent session with an active Parent Gate step-up token, when calling `POST /v1/ramadan/certificates`, then a shareable certificate is generated and the resulting signed CDN URL is returned.
- [ ] AC2: Given an incoming certificate or Eid card request lacking valid Parent Gate elevation (`require_elevated_session`), then the endpoint returns HTTP 403 Forbidden.
- [ ] AC3: Given the certificate rendering payload assembled by `CertificateService`, when inspected before transmission to A.11's `ShareCardService`, then the payload contains zero child IDs, zero dates of birth, zero ages, and zero location coordinates (mandatory PII-exclusion test).
- [ ] AC4: Given a child with 0 completed Ramadan nights, when certificate generation is requested, then the API returns HTTP 422 Unprocessable Entity (`"Child must complete at least one night to generate a certificate"`).
- [ ] AC5: Given `POST /v1/ramadan/eid-cards`, when called with an approved card design, then an Eid celebration card is rendered via A.11's `ShareCardService` and the URL is returned.
- [ ] AC6: Given a parent requesting a certificate for a child outside their household, then the endpoint returns HTTP 403 Forbidden.
- [ ] AC7: Given successful certificate generation, then the URL and generation timestamp are persisted in `ramadan_certificates` for future re-download.

## Technical Notes
- Files in scope:
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/models/certificate.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/schemas/certificate_schema.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/repositories/certificate_repository.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/services/certificate_service.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/routers/certificate_router.py`
  - `NoorHeroes-Backend/alembic/versions/xxxx_create_ramadan_certificates_table.py`
- Architecture refs: `sdocs/architecture-ref.md` Section 8.2 (Invariant 7), 8.3, 8.4; Blueprint B-07.
- Non-functional: Zero PII leakage in generated images or metadata. Parent Gate step-up enforced. Reuse A.11's `ShareCardService` rendering pipeline.

## Test Approach
- Unit: Mandatory test asserting rendering payload contains no `child_id`, `dob`, `age`, or `location` fields.
- Integration: Test `POST /v1/ramadan/certificates` and `POST /v1/ramadan/eid-cards` requiring `require_elevated_session`; test 0-completion 422 rejection; test cross-family 403 rejection.
- E2E: Parent passes Parent Gate, generates certificate for child with 30 nights completed, and receives valid signed CDN URL.

## Out of Scope
- Native image rendering and PDF composition algorithms (delegated to A.11 `ShareCardService`).
- Social sharing and print-dialog UI integration on mobile (owned by Mobile K-07).
