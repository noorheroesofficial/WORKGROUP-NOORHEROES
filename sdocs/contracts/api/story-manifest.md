---
id: api.story-manifest
kind: api
title: Signed Media Manifest API (GET /v1/content/{id}/manifest)
status: draft
owner_story: STORY-012
version: 1
created: 2026-09-29
---

# Contract: api.story-manifest

- **Kind**: API
- **Endpoint**: `GET /v1/content/{id}/manifest`
- **Source**: `NoorHeroes-Backend/src/noorheroes/modules/media/manifest_schemas.py` & `Development_Blueprints/A3_Stories_Module/KMP/03-story-player-core-playback-engine.md` (B-07)
- **Owner Story**: `STORY-012`
- **Status**: Draft

## Request Specification
- **Method**: `GET`
- **Path Parameter**: `id: String` (Episode content ID, e.g. `ep_01H8XVMQ2G0000000000000011`)
- **Headers**:
  - `Authorization: Bearer <child_token>` (Child session required)
  - `X-Locale: String?` (Requested locale for captions/audio default resolution, e.g. `en`, `ar`, `ur`, `hi`)

## Response Specification (200 OK)
```json
{
  "contentId": "ep_01H8XVMQ2G0000000000000011",
  "playbackUrl": "https://cdn.noorheroes.com/signed/stories/musa_ep1.mp4?exp=1725515400&sig=abcdef123456",
  "expiresAt": "2026-09-29T12:00:00Z",
  "format": "video",
  "durationSeconds": 480,
  "captions": [
    {
      "language": "en",
      "label": "English",
      "url": "https://cdn.noorheroes.com/captions/musa_ep1_en.vtt",
      "format": "vtt"
    },
    {
      "language": "ar",
      "label": "العربية",
      "url": "https://cdn.noorheroes.com/captions/musa_ep1_ar.vtt",
      "format": "vtt"
    }
  ],
  "audioTracks": [
    {
      "language": "en",
      "label": "English (Original)",
      "url": "https://cdn.noorheroes.com/audio/musa_ep1_en.m4a",
      "isDefault": true
    },
    {
      "language": "ar",
      "label": "العربية (فصحى)",
      "url": "https://cdn.noorheroes.com/audio/musa_ep1_ar.m4a",
      "isDefault": false
    }
  ],
  "qualities": ["auto", "1080p", "720p", "480p", "360p"],
  "scrubRestricted": false,
  "interactiveScript": null
}
```

## Error Specification
- `401 Unauthorized`: Missing or invalid Bearer token.
- `403 Forbidden`: Content locked or premium-tier gated.
- `404 Not Found`: Episode content ID does not exist.
- `410 Gone`: Media content withdrawn. Triggers safe stop to `PlayerState.Unavailable`.
