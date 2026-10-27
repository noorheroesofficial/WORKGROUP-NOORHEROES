# Dua Master Badge & Achievement Criteria Specification (Blueprint B-05)

## 1. Overview & Context

This reference specification documents the configuration recipe, criteria DSL, and integration architecture for the **Dua Master** badge and cumulative achievement progression within the NoorHeroes platform (Feature A.6 Dua Learning, Blueprint B-05).

In accordance with NoorHeroes' Clean Architecture and Modular Monolith design:
- **No Duplicate Badge Engine**: A.6 does not maintain a custom badge engine, Kafka consumer, or dedicated threshold table.
- **Generic Rewards Integration**: Badge evaluation and reward persistence are delegated entirely to the existing, generic `A11_Rewards_System` (`src/noorheroes/modules/rewards/`).
- **Synchronous In-Process Call**: On a genuine transition from `not_learned` to `learned`, `DuaService.update_progress()` directly calls `RewardService.award_points()`.
- **Automatic Badge Evaluation**: `RewardService.award_points()` automatically triggers `BadgeEngine.evaluate_all()` after appending to the immutable `reward_ledger_entries` table.

---

## 2. Verification of Contract & Field Shapes

### Task 01: `award_type` / `activity_type` Field Shape Confirmation
Inspection of `src/noorheroes/modules/rewards/models.py` (`RewardLedgerEntry`) confirms:
- The ledger categorizes entries via `activity_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)`, `reason_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)`, and `reason: Mapped[str] = mapped_column(String(255), nullable=False)`.
- These fields are string-typed (not enum-constrained in the database).
- Value `"dua_learned"` is accepted directly without requiring any database schema mutations.

### Task 02: In-Process Method Signature Verification
Inspection of `RewardService.award_points` in `src/noorheroes/modules/rewards/service.py` confirms exact parameter alignment with B-02's call site in `src/noorheroes/modules/dua/service.py`:
```python
await reward_service.award_points(
    session=session,
    child_id=child_id,
    points=10,
    xp=20,
    noor_points=10,
    reason="dua_learned",
    activity_type="dua_learned",
    reason_id=clean_content_id,
    idempotency_key=f"dua_learned:{child_id}:{clean_content_id}",
)
```

---

## 3. "Dua Master" Badge Definitions (Discrete Badges)

Discrete collectible badges unlock once a child reaches a specific threshold of learned duas.

### Badge 1: `dua_master_bronze` (5 Duas Learned)
- **Badge Code**: `dua_master_bronze`
- **Locale Key**: `badges.dua_master_bronze`
- **Description**: Awarded for memorizing and learning 5 supplications.
- **Criteria DSL**:
```json
{
  "type": "activity_count",
  "activity_type": "dua_learned",
  "condition": "gte",
  "threshold": 5
}
```

### Badge 2: `dua_master_silver` (10 Duas Learned)
- **Badge Code**: `dua_master_silver`
- **Locale Key**: `badges.dua_master_silver`
- **Description**: Awarded for memorizing and learning 10 supplications.
- **Criteria DSL**:
```json
{
  "type": "activity_count",
  "activity_type": "dua_learned",
  "condition": "gte",
  "threshold": 10
}
```

### Badge 3: `dua_master_gold` (20 Duas Learned)
- **Badge Code**: `dua_master_gold`
- **Locale Key**: `badges.dua_master_gold`
- **Description**: Awarded for memorizing and learning 20 supplications.
- **Criteria DSL**:
```json
{
  "type": "activity_count",
  "activity_type": "dua_learned",
  "condition": "gte",
  "threshold": 20
}
```

### Standard Single-Tier Badge: `dua_master`
For deployments using a single consolidated badge:
- **Badge Code**: `dua_master`
- **Locale Key**: `badges.dua_master`
- **Description**: Awarded for mastering supplications.
- **Criteria DSL**:
```json
{
  "type": "activity_count",
  "activity_type": "dua_learned",
  "condition": "gte",
  "threshold": 5
}
```

---

## 4. "Dua Master" Cumulative Achievement Definition

For continuous progress tracking (milestone tiers and percentage progress on the Child Achievements screen):

- **Achievement Code**: `dua_master_track`
- **Linked Badge ID**: Optional reference to `dua_master_gold`
- **XP Value**: 100 XP per tier completion
- **Criteria DSL**:
```json
{
  "activity_type": "dua_learned",
  "levels": [
    {"level": 1, "threshold": 5},
    {"level": 2, "threshold": 10},
    {"level": 3, "threshold": 20}
  ]
}
```

---

## 5. Admin Configuration & Dry-Run Simulation Guide

Content Editors configure badges via the A11 Admin REST API or Admin CMS UI.

### Step 1: Create Badge via Admin API
```http
POST /v1/admin/rewards/badges HTTP/1.1
Host: api.noorheroes.com
Authorization: Bearer <content_editor_jwt>
Content-Type: application/json

{
  "code": "dua_master",
  "locale_key": "badges.dua_master",
  "description": "Awarded for learning 5 supplications.",
  "is_active": true,
  "criteria_json": {
    "type": "activity_count",
    "activity_type": "dua_learned",
    "condition": "gte",
    "threshold": 5
  }
}
```

### Step 2: Validate with Non-Mutating Simulate Tool
Before enabling a badge, administrators can verify criteria against a fixture history:
```http
POST /v1/admin/rewards/badges/{badge_id}/simulate HTTP/1.1
Host: api.noorheroes.com
Authorization: Bearer <content_editor_jwt>
Content-Type: application/json

{
  "fixture_activity_history": [
    {"activity_type": "dua_learned", "reason_id": "dua_01", "created_at": "2026-09-01T10:00:00Z"},
    {"activity_type": "dua_learned", "reason_id": "dua_02", "created_at": "2026-09-02T10:00:00Z"},
    {"activity_type": "dua_learned", "reason_id": "dua_03", "created_at": "2026-09-03T10:00:00Z"},
    {"activity_type": "dua_learned", "reason_id": "dua_04", "created_at": "2026-09-04T10:00:00Z"},
    {"activity_type": "dua_learned", "reason_id": "dua_05", "created_at": "2026-09-05T10:00:00Z"}
  ]
}
```
**Expected Response (200 OK)**:
```json
{
  "would_trigger": true,
  "matched_count": 5,
  "threshold": 5,
  "qualifying_timestamp": "2026-09-05T10:00:00Z"
}
```
*Note: The simulate endpoint guarantees zero persisted writes to `child_badges` or `reward_ledger_entries`.*

---

## 6. Platform Guarantees & Edge Cases

### Edge Case 2: Badge Stickiness on Un-Marking
- If a child marks 5 duas as learned and earns the `dua_master` badge, and subsequently toggles one dua back to `not_learned`, **the badge is NOT revoked**.
- The `child_badges` table is append-only with `UNIQUE(child_id, badge_id)`.
- `BadgeEngine` checks `earned_badge_ids = await repository.get_child_earned_badge_ids(child_id)`. Any already-earned badge is skipped immediately, preserving the original `earned_at` timestamp.

### Idempotency & Replay Defense
- Submissions with existing `client_request_id` or re-submissions of `status="learned"` where `was_transition=False` do not trigger `RewardService.award_points()`.
- Even under concurrent race conditions, the database unique constraint on `(child_id, idempotency_key)` in `reward_ledger_entries` guarantees exactly one ledger record.

---

## 7. Localization Keys

| Key | English (`en`) | Hindi (`hi`) | Urdu (`ur`) | Arabic (`ar`) |
|---|---|---|---|---|
| `badges.dua_master.title` | Dua Master | दुआ मास्टर | دعا ماسٹر | سيد الأدعية |
| `badges.dua_master.description` | Awarded for learning supplications and mastering their recitation. | दुआएं सीखने और उनके पाठ में महारत हासिल करने के लिए प्रदान किया गया। | دعائیں یاد کرنے اور ان کی تلاوت میں مہارت حاصل کرنے پر دیا گیا۔ | يُمنح لحفظ الأدعية وإتقان تلاوتها. |
| `rewards.reason.dua_learned` | Learned a new Dua | एक नई दुआ सीखी | ایک نئی دعا سیکھی | حفظ دعاء جديد |
