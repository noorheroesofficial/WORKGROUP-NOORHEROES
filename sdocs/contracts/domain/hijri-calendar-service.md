---
id: domain.hijri-calendar-service
kind: repo
title: Hijri Calendar & Moon-Sighting Override Service Interface
status: draft
owner_story: STORY-036-02
version: 1
created: 2026-09-30
---

## Interface

```ts
export interface HijriDates {
  region: string;
  hijri_start_date: string; // ISO 8601 Date (YYYY-MM-DD)
  eid_date: string;         // ISO 8601 Date (YYYY-MM-DD)
  is_overridden: boolean;   // true if sourced from moon_sighting_overrides
  source_note: string | null;
}

export interface OverrideResult {
  override_id: string;
  region: string;
  corrected_eid_date: string;
  applied_at: string; // ISO 8601 UTC timestamp
}

export interface HijriCalendarService {
  /**
   * Resolves region-adjusted Ramadan dates.
   * Priority: Checks moon_sighting_overrides table first; falls back to algorithmic calculation.
   */
  getDates(region: string): Promise<HijriDates>;

  /**
   * Admin-only write path invoked exclusively by EidOverrideService (B-08).
   * Validates corrected date within ±3 days sanity bound and updates campaign record.
   */
  applyOverride(
    region: string,
    correctedEidDate: string,
    sourceNote: string,
    actingAdminId: string
  ): Promise<OverrideResult>;
}
```

## Error Semantics
- `getDates` raises `UnsupportedRegionException` when region string is unmapped or unknown (B-01 translates to `phase: "not_active"`).
- `applyOverride` raises `SanityBoundExceededException` when `correctedEidDate` deviates > 3 days from algorithmic target.
- `applyOverride` raises `CampaignNotFoundException` when no base campaign exists for the specified region.

## Invariants
1. **Platform Authority**: `HijriCalendarService` is the sole authoritative source of Hijri dates across all NoorHeroes services. Zero platform code or client logic performs independent date arithmetic.
2. **Sanity Bound**: Corrected date must satisfy:
   `|corrected_eid_date - algorithmic_eid_date| <= 3 days`.
3. **No Public Router**: Internal leaf service only; write method callable exclusively from `EidOverrideService` (B-08).
4. **Append-Only Audit**: All overrides record an immutable row in `moon_sighting_overrides` with admin attribution.
