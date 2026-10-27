---
id: api.ramadan-certificates
kind: api
title: Ramadan Certificate & Eid Card Generation API (POST /v1/ramadan/certificates & POST /v1/ramadan/eid-cards)
status: draft
owner_story: STORY-036-07
version: 1
created: 2026-09-30
---

## Endpoints

```http
POST /v1/ramadan/certificates
POST /v1/ramadan/eid-cards
```

## Description
Generates printable, shareable completion certificates and celebratory Eid greeting cards. Operates strictly behind Parent Gate step-up authentication and guarantees complete exclusion of child PII (no child ID, date of birth, or geographic location). Delegates rendering to A.11's `ShareCardService`.

## Auth & Security
- **Auth**: Bearer parent token via `Depends(get_current_parent)`.
- **Step-Up Authentication**: Requires valid elevated Parent Gate session (`Depends(require_elevated_session)`).
- **PII-Exclusion Guarantee**:
  - Generated image artifacts and metadata exclude: `child_id`, `family_id`, date of birth, age, and geographic location.
  - Artifact displays only the child's configured first display name, completion milestone (e.g. "Completed 30 Nights of Ramadan"), and season year.

## 1. Certificate Request & Response

### Request
```ts
export interface RamadanCertificateRequest {
  child_id: string; // UUID v4 belonging to authenticated parent's household
  theme?: 'classic_gold' | 'starlit_night' | 'emerald_lantern';
  locale?: 'en' | 'ar' | 'ur' | 'hi';
}
```

### Response — 201 Created / 200 OK
```ts
export interface RamadanCertificateResponse {
  certificate_id: string;
  child_display_name: string; // Sanitized display name only
  certificate_url: string;    // Signed CDN URL for rendered artifact (PNG/PDF)
  nights_completed: number;   // 1..30
  season_title: string;       // e.g. "Ramadan 1448 / 2027"
  generated_at: string;       // ISO 8601 UTC timestamp
  share_preview_url: string;  // Watermarked/preview URL
}
```

## 2. Eid Card Request & Response

### Request
```ts
export interface EidCardRequest {
  child_id: string;
  card_design: 'crescent_joy' | 'lantern_glow' | 'celebration_confetti';
  greeting_text?: string; // Optional parent custom blessing (sanitized, max 100 chars)
  locale?: 'en' | 'ar' | 'ur' | 'hi';
}
```

### Response — 201 Created / 200 OK
```ts
export interface EidCardResponse {
  card_id: string;
  card_url: string;          // Signed CDN URL for rendered card (PNG/WebP)
  greeting_text: string;
  season_title: string;      // e.g. "Eid Al-Fitr 1448"
  generated_at: string;      // ISO 8601 UTC timestamp
}
```

## Errors
- `401 UNAUTHORIZED`: Missing or invalid parent token.
- `403 FORBIDDEN`:
  - Missing or expired Parent Gate elevated step-up session (`require_elevated_session`).
  - Requesting child does not belong to parent's household.
- `422 UNPROCESSABLE_ENTITY`:
  - Child has 0 completed nights (certificate requires at least 1 completed night).
- `502 BAD_GATEWAY`: Downstream rendering failure in A.11 `ShareCardService`.

## Invariants
1. Both endpoints strictly require Parent Gate step-up authentication.
2. Zero child PI (ID, DOB, location) is transmitted to the rendering pipeline or included in the final media file.
3. Renders reuse A.11's existing `ShareCardService`; zero parallel rendering infrastructure is built.
