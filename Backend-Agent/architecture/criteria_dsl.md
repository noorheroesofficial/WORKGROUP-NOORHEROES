# Badge & Achievement Criteria JSON DSL Specification

**Feature:** A.11 Rewards System (Gamified Learning Ecosystem)  
**Blueprint:** B-04 Badge & Achievement Progress Engine  
**Status:** Canonical Reference

---

## 1. Overview

The NoorHeroes Badge & Achievement Progress Engine evaluates eligibility server-side using declarative `criteria_json` structures stored on `badges` (discrete collectible unlocks) and `achievement_definitions` (cumulative milestone ladders).

Evaluation occurs in-process immediately after a ledger transaction is committed in `RewardService.award_points()`. Client applications never calculate awards directly.

---

## 2. Discrete Badge Criteria DSL (`badges.criteria_json`)

Every badge definition must provide a valid `criteria_json` object specifying the qualification rule. If a malformed or unsupported criteria object is encountered, the evaluation engine logs a structured diagnostic warning and safely skips the badge without halting or crashing the calling reward pipeline.

### Supported Criteria Types

### 2.1 `activity_count` (Threshold by Activity Type)
Unlocks when the child completes at least `threshold` activities matching `activity_type`.

```json
{
  "type": "activity_count",
  "activity_type": "quiz_pass",
  "threshold": 5,
  "description": "Pass 5 Islamic knowledge quizzes"
}
```

- `type`: `"activity_count"` (string, required)
- `activity_type`: Target activity key matching `reward_ledger_entries.activity_type` or `reason_type` (string, required)
- `threshold`: Minimum qualifying completion count (positive integer, required)

### 2.2 `reason_match` (Specific Content / Habit / Mission Completion)
Unlocks when the child completes a specific content item, quiz, or habit identified by `reason_id`.

```json
{
  "type": "reason_match",
  "reason_type": "story_complete",
  "reason_id": "prophet_yusuf_ep01",
  "threshold": 1,
  "description": "Complete Episode 1 of Prophet Yusuf story series"
}
```

- `type`: `"reason_match"` (string, required)
- `reason_type`: Classification category (string, optional)
- `reason_id`: Specific content or item identifier (string, required)
- `threshold`: Required completions (positive integer, default: 1)

### 2.3 `total_xp` (Lifetime Experience Points Threshold)
Unlocks when the child's cumulative lifetime experience points (`xp`) reaches or exceeds `threshold`.

```json
{
  "type": "total_xp",
  "threshold": 1000,
  "description": "Accumulate 1,000 lifetime XP"
}
```

- `type`: `"total_xp"` (string, required)
- `threshold`: Minimum XP required (positive integer, required)

### 2.4 `streak_days` (Consecutive Daily Activity Streak)
Unlocks when the child reaches a daily active learning streak.

```json
{
  "type": "streak_days",
  "threshold": 7,
  "description": "Maintain a 7-day learning streak"
}
```

- `type`: `"streak_days"` (string, required)
- `threshold`: Number of consecutive days (positive integer, required)

### 2.5 Seasonal Badges (`season_id` / `season_ends_at`)
Seasonal badges (e.g. Ramadan, Eid) include temporal bounding rules backing Edge Case 12.

```json
{
  "type": "activity_count",
  "activity_type": "ramadan_good_deed",
  "threshold": 10,
  "season_id": "019183ab-0000-7000-8000-000000000010",
  "season_ends_at": "2026-04-10T23:59:59Z",
  "description": "Complete 10 good deeds during Ramadan"
}
```

- **Rule 1 (Window Closure)**: When `current_time > season_ends_at`, new qualification attempts are rejected.
- **Rule 2 (Permanent Retention)**: Once awarded, seasonal badges are retained permanently in `child_badges` (stickiness guarantee).
- **Rule 3 (Retroactive Qualification)**: If an offline sync or data correction demonstrates that criteria was met before `season_ends_at`, the badge is awarded with that historical timestamp.

### 2.6 `all_of` / `any_of` (Compound Criteria)
Enables multi-factor qualification criteria across diverse activities:

```json
{
  "type": "all_of",
  "criteria": [
    { "type": "activity_count", "activity_type": "quiz_pass", "threshold": 5 },
    { "type": "activity_count", "activity_type": "story_complete", "threshold": 3 }
  ],
  "description": "Pass 5 quizzes and complete 3 stories"
}
```

- `all_of`: Unlocks only when **all** nested sub-criteria conditions are satisfied.
- `any_of`: Unlocks when **at least one** nested sub-criteria condition is satisfied.

### 2.7 Rule-Based Event Criteria (Blueprint E.31 B-05)
For admin-configured event rules based on comparison conditions:

```json
{
  "event_type": "stories_completed",
  "condition": "gte",
  "threshold": 5
}
```

- `event_type`: Activity or event classification key (e.g. `stories_completed`, `habit_streak`, `quiz_score`).
- `condition`: Comparison operator (`gte`, `gt`, `eq`, `lte`, `lt`). Defaults to `gte`.
- `threshold`: Numeric evaluation threshold (positive integer).

---

## 3. Cumulative Achievement Criteria DSL (`achievement_definitions.criteria_json`)

Achievements track progressive milestone ladders (FR-2) distinct from discrete badges.

### Multi-Level Ladder Specification

```json
{
  "type": "cumulative_activity",
  "activity_type": "story_complete",
  "levels": [
    { "level": 1, "threshold": 1, "title": "Seedling" },
    { "level": 2, "threshold": 5, "title": "Sprout" },
    { "level": 3, "threshold": 15, "title": "Young Explorer" },
    { "level": 4, "threshold": 30, "title": "Story Master" },
    { "level": 5, "threshold": 50, "title": "Hafiz Hero" }
  ]
}
```

### Calculation Rules
1. **Milestone Level (`current_level`)**: The highest level where `child_counter >= threshold`.
2. **Next Threshold (`next_threshold`)**: The threshold of `current_level + 1`. If at maximum level, `null`.
3. **Fractional Progress (`progress`)**: 
   $$\text{progress} = \frac{\text{counter} - \text{threshold}_{\text{current}}}{\text{threshold}_{\text{next}} - \text{threshold}_{\text{current}}}$$
   Clamped between `0.0` and `1.0`.
4. **Downward Stickiness**: If underlying counters are corrected downward, `current_level` never decreases (FR-3 / Edge Case 3).

---

## 4. Platform Architectural Guarantees

1. **Write-Once Fact Lockout**: `child_badges` UPDATE and DELETE grants are revoked for the database application role in PostgreSQL via migration `0021_revoke_child_badges_write_grants.py`.
2. **Deterministic Replay**: Duplicate awards are prevented by `UNIQUE(child_id, badge_id)` at the database constraint level.
3. **Audit & Push Dispatch**: Unlocks automatically trigger parent push alerts via `NotificationService` and record `BadgeUnlockedEvent` / `AchievementLevelProgressedEvent` in the transactional outbox.
