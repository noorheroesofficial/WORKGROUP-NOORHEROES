---
id: domain.fact-versioning-approval
kind: service
title: Fact Content Versioning & Scholar Approval Domain Model & Invariants
status: stable
owner_story: TASK-B18-01
version: 1
created: 2026-10-11
---

## Overview

The `fact`, `fact_version`, `scholar_approval`, and `fact_seen_log` data model defines the canonical Islamic Facts content store in the `content` bounded context (PRD §4.1/§4.2, Blueprint B-01).

## Hard Architectural Invariants

1. **Query-Layer Approval Gate (Structural Invariant)**:
   - `FactVersionRepository.get_published_version(fact_id, locale, age_band)` executes a mandatory inner SQL join requiring:
     `fact_version.status = 'published' AND scholar_approval.approved = true AND scholar_approval.revoked_at IS NULL`.
   - This is the ONLY code path any sub-feature may use to resolve a "current" published fact version.
2. **Version Immutability (FR-11)**:
   - Any editorial update to text, explanation, sources, or scope notes drafts a new row in `fact_version` with `status='draft'`.
   - Published version rows are never updated in-place.
3. **Soft-Delete Rule**:
   - `fact.is_withdrawn = true` is used instead of DELETE, preserving all historical seen logs and telemetry records.
4. **Append-Only Engagement History**:
   - `fact_seen_log` is strictly append-only, indexing `(child_id, seen_at DESC)` for 30-day dedup window evaluation.

## Public Repository Interfaces

```python
class FactVersionRepository(BaseRepository[FactVersionOrm]):
    async def get_published_version(
        self,
        fact_id: str,
        locale: str,
        age_band: str,
    ) -> Optional[FactVersionOrm]:
        ...

class FactSeenLogRepository(BaseRepository[FactSeenLogOrm]):
    async def record_seen(self, child_id: str, fact_id: str) -> FactSeenLogOrm:
        ...
    async def get_recent_seen_ids(self, child_id: str, window_days: int = 30) -> Set[str]:
        ...
```
