# Contract: api.story-detail

- **Kind**: API
- **Endpoint**: `GET /v1/content/{id}`
- **Source**: `NoorHeroes-Backend/src/noorheroes/modules/content/api.py:1236`
- **Owner Story**: `STORY-007`
- **Status**: Stable

## Request Specification
- **Method**: `GET`
- **Path Parameter**: `id: String` (Story series identifier, e.g. `ser_01H8XVMQ2G000`)
- **Headers**:
  - `Authorization: Bearer <child_token>` (Child session strictly required)
  - `X-Locale: String?` (Optional requested locale, e.g. `en`, `ar`, `ur`, `hi`)

## Response Specification (200 OK)
```json
{
  "id": "ser_01H8XVMQ2G000",
  "seriesId": "ser_01H8XVMQ2G000",
  "title": "Prophet Ibrahim (AS)",
  "synopsis": "The inspiring story of Ibrahim — the Friend of Allah...",
  "description": "Full editorial narrative description...",
  "category": "Prophet Stories",
  "ageBands": ["6 to 9"],
  "coverUrl": "https://cdn.noorheroes.com/covers/ibrahim.jpg",
  "scholarApprovalStatus": "approved",
  "scholarApprovalTags": ["verified_seerah", "azhar_certified"],
  "sourceReferences": ["Surah Al-Anbiya 21:51-71"],
  "episodes": [
    {
      "id": "ep_001",
      "episodeNumber": 1,
      "title": "The Great Test",
      "durationSeconds": 360,
      "unlockState": "unlocked",
      "unlockCondition": null,
      "scholarApprovalStatus": "approved",
      "completed": true,
      "progressSeconds": 360
    },
    {
      "id": "ep_002",
      "episodeNumber": 2,
      "title": "Into the Fire",
      "durationSeconds": 420,
      "unlockState": "unlocked",
      "unlockCondition": null,
      "scholarApprovalStatus": "approved",
      "completed": true,
      "progressSeconds": 420
    },
    {
      "id": "ep_003",
      "episodeNumber": 3,
      "title": "The Land of Canaan",
      "durationSeconds": 300,
      "unlockState": "unlocked",
      "unlockCondition": null,
      "scholarApprovalStatus": "approved",
      "completed": false,
      "progressSeconds": 180
    },
    {
      "id": "ep_004",
      "episodeNumber": 4,
      "title": "The Ultimate Sacrifice",
      "durationSeconds": 480,
      "unlockState": "locked",
      "unlockCondition": "Complete Episode 3 to unlock",
      "scholarApprovalStatus": "approved",
      "completed": false,
      "progressSeconds": 0
    }
  ],
  "relatedStories": ["ser_002", "ser_003"],
  "totalDurationSeconds": 1560,
  "isBedtimeEligible": false,
  "freeOrPremium": "free"
}
```

## Error Specification
- `401 Unauthorized`: Missing or invalid Bearer token.
- `403 Forbidden`: Parent session token presented (child mode required).
- `404 Not Found`: Story ID does not exist.
- `410 Gone`: Withdrawn content. Client must render "This story is no longer available" rather than a generic error.
