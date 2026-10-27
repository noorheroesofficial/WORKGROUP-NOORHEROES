---
id: domain.admin-fact-engagement-monitoring
kind: service
title: Admin Fact Engagement Monitoring Domain Service Interface
status: stable
owner_story: TASK-B18-07
version: 1
created: 2026-10-13
---

## Overview

The `FactEngagementService` provides read-only analytical aggregation of view and quiz-engagement conversion rates per fact and per topic, sourcing from telemetry event queues and seen logs (Blueprint B-07).

## Domain Invariants

1. **Read-Only Purity**:
   - Zero mutation of operational catalog records or telemetry event tables.
2. **Formula Metrics**:
   - `view_rate = views_count / impressions_count` (clamped to 1.00 max).
   - `quiz_engagement_rate = quiz_starts_count / views_count` (clamped to 1.00 max).
3. **Resilient Short-TTL Caching**:
   - Redis caching with 300s TTL; graceful fallback to direct database calculation on Redis connection errors or corrupt JSON.
4. **Boundary Validation**:
   - Strictly enforces `date_from <= date_to` (HTTP 422 `INVALID_DATE_RANGE`) and max page size <= 100.

## Public Interface

```python
class FactEngagementService(BaseService):
    async def get_engagement_report(
        self,
        topic: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> FactEngagementMonitoringResponse:
        ...
```
