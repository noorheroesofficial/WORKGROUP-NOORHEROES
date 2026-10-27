---
id: EPIC-002
title: Story Detail & Episode Unlock Presentation
status: done
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
prd_sections: ["1.7", "1.9", "1.10", "1.11", "1.13", "1.14"]
depends_on: [EPIC-001]
created: 2026-09-29
---

## Description
Implements the pre-playback commitment screen (K-02) featuring story cover, synopsis, scholar-approval badge, episode list with per-episode lock state and specific unlock-condition text, related stories rail, real-time on-resume unlock refresh, tier-gated paywall handling via Parent PIN Gate, and 410 withdrawn-content graceful degradation.

## Stories
- STORY-006 — Add StoryDetailRoute & Deep Link
- STORY-007 — Extend StoryCatalogApi, StoryCatalogCache, and StoryCatalogRepository with getStoryDetail
- STORY-008 — Implement GetStoryDetailUseCase and StoryDetailViewModel with real-time onResume refresh
- STORY-009 — Implement StoryDetailScreen, EpisodeListItem, and ParentGatedPaywallCard Composables
- STORY-010 — Integration & End-to-End Verification of Story Detail
