---
id: domain.daily-fact-selection
kind: service
title: Child Daily Fact Selection Domain Service Interface
status: stable
owner_story: TASK-B18-02
version: 1
created: 2026-10-11
---

## Overview

The `FactSelectionService` selects an age-band and locale-appropriate, scholar-approved, deduplicated, seasonally-weighted fact for a requesting child profile (Blueprint B-02).

## Domain Invariants

1. **Approval-Gated Selection**:
   - Only versions resolving via `FactVersionRepository.get_published_version()` are selectable.
2. **Progressive Dedup Window Relaxation (Edge Case 2)**:
   - Excludes facts seen by the child within 30 days. If the candidate pool is exhausted, relaxes progressively (30 → 14 → 7 → 0 days) before falling back to evergreen candidates.
3. **Seasonal Weighting & Fallback (Edge Case 7)**:
   - When seasonal calendar mode is active (Ramadan, Eid, Dhul Hijjah), candidates with matching seasonal topics are biased; if exhausted, falls back seamlessly to the general pool.
4. **Cross-Surface Collision Prevention (Edge Case 4)**:
   - Tracks same-day selected `fact_id` in Redis cache key so separate surfaces (`home_card` vs `resurfacing_prompt`) do not independently select the identical fact on the same day.
5. **Zero "No Fact" Invariant**:
   - Database or cache failures fall back to configured evergreen fact, guaranteeing a valid 200 response.

## Public Interface

```python
class FactSelectionService(BaseService):
    async def select_daily_fact(
        self,
        child_id: str,
        locale: str,
        age_band: str,
        surface: str = "home_card",
    ) -> DailyFactResponse:
        ...
```
