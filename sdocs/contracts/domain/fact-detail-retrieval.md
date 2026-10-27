---
id: domain.fact-detail-retrieval
kind: service
title: Fact Detail Retrieval Domain Service Interface
status: stable
owner_story: TASK-B18-03
version: 1
created: 2026-10-11
---

## Overview

The `FactDetailService` handles comprehensive Fact Detail retrieval for the mobile child application, evaluating dynamic related-content availability and series restructuring chains (Blueprint B-03).

## Domain Invariants

1. **Dynamic Related-Content Evaluation (FR-9)**:
   - Reads target content item (Story, Episode, Dua, Surah). If withdrawn or soft-deleted, sets `related_content.available = false` rather than returning a broken reference.
2. **Canonical Restructuring Traversal (Edge Case 6)**:
   - If referenced series/episode was merged or restructured, follows canonical pointer to latest active canonical ID.
3. **Mid-Session Approval Revocation Safety**:
   - Fetches fresh published version on every request. Client views already rendered on device remain stable until next navigation.
4. **Lifecycle Exclusions**:
   - If fact is soft-withdrawn (`is_withdrawn = true`), raises `FactWithdrawnError` (HTTP 410).

## Public Interface

```python
class FactDetailService(BaseService):
    async def get_fact_detail(
        self,
        fact_id: str,
        child_ctx: ChildSessionContext,
        locale: str = "en",
    ) -> FactDetailResponse:
        ...
```
