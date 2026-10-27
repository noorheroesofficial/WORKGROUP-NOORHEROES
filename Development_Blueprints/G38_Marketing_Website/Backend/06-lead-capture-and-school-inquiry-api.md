# G.38 Backend 06 — Lead Capture & Institutional School Inquiry API

`Development_Blueprints.G38_Marketing_Website.Backend.06-lead-capture-and-school-inquiry-api.md`

**Module:** Marketing Backend Gateway (`noorheroes.modules.marketing`)  
**Parent Feature:** G.38 — Marketing Website  
**Sequence:** Seq 592  
**Status:** 🟡 **Pending Implementation**  
**Depends on:** Phase 2 Backend Foundation  
**Source of truth:** `PRD_Documents/Website Home/NoorHeroes_website_content_spec.md` §8  

---

## 1. Objective and Purpose
Provide secure, rate-limited public endpoints for madrasah/school bulk license inquiries, parent contact requests, and newsletter signups.

## 2. API Endpoints
- `POST /v1/marketing/inquiries`:
  - Request: `name`, `email`, `organization_type` (school, mosque, parent), `student_count`, `message`, `turnstile_token`.
  - Anti-Spam: Cloudflare Turnstile token validation and 5 requests / hour / IP rate limit.
  - Storage: Persists to `marketing_inquiries` table with outbox notification event `marketing.inquiry_received`.
- `POST /v1/marketing/newsletter`:
  - Request: `email`, `locale`, `turnstile_token`.
  - Deduplication: Idempotent upsert in `newsletter_subscribers`.

## 3. Verification and Acceptance Criteria
- [ ] Endpoints reject requests without valid CAPTCHA token with HTTP 422.
- [ ] Database migration `add_marketing_inquiries_table.py` creates tables with indexes.
- [ ] Celery worker dispatches inquiry alert email to sales/partnerships team.
