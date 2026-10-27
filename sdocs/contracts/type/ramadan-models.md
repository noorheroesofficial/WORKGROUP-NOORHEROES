---
id: type.ramadan-models
kind: type
title: Ramadan Domain Entities and Persistence Models
status: draft
owner_story: STORY-036-01
version: 1
created: 2026-09-30
---

## Shape

```ts
export interface RamadanCampaignEntity {
  campaign_id: string; // UUID v4 PK
  region: string;      // Region code
  hijri_start_date: string; // YYYY-MM-DD
  eid_date: string;         // YYYY-MM-DD
  eid_date_overridden: boolean;
  created_at: string;
  updated_at: string;
}

export interface MoonSightingOverrideEntity {
  override_id: string; // UUID v4 PK
  region: string;
  corrected_eid_date: string; // YYYY-MM-DD
  source_note: string;
  applied_by_admin_id: string;
  applied_at: string;
}

export interface RamadanMissionEntity {
  mission_id: string; // UUID v4 PK
  campaign_id: string; // FK to ramadan_campaigns
  night_number: number; // 1..30
  content_version_id: string; // FK to E.29 content_versions
  is_laylatul_qadr: boolean;
  created_at: string;
}

export interface RamadanJourneyProgressEntity {
  child_id: string;   // FK to child profile
  mission_id: string; // FK to ramadan_missions
  completed_at: string;
}

export interface FastingLogEntity {
  log_id: string; // UUID v4 PK
  child_id: string;
  night_number: number; // 1..30
  status: 'fasted_full' | 'fasted_practice' | 'education_only';
  logged_at: string;
}

export interface RamadanCertificateEntity {
  certificate_id: string; // UUID v4 PK
  child_id: string;
  certificate_url: string;
  generated_at: string;
}
```

## Invariants
1. `night_number` is strictly constrained: `1 <= night_number <= 30`.
2. `(child_id, mission_id)` in `RamadanJourneyProgressEntity` forms a composite primary key guaranteeing uniqueness.
3. `RamadanMissionEntity.is_laylatul_qadr` is true if and only if `night_number` in `[21, 23, 25, 27, 29]`.
4. `FastingLogEntity` is append-only (no soft deletion or in-place overwrite).
5. `RamadanCertificateEntity` retains zero child date-of-birth, national identity, or geographical coordinates.
