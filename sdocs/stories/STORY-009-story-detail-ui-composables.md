---
id: STORY-009
epic: EPIC-002
kind: feature
title: Implement StoryDetailScreen, EpisodeListItem, and ParentGatedPaywallCard UI Composables
status: done
priority: P0
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
depends_on: [STORY-008]
produces: []
consumes: [domain.story-detail]
created: 2026-09-29
---

## User Story
As a child learner, I want to see the starry night cover art, scholar approval badge, episode list with status icons and progress indicators, and related stories matching `Story Detail-01.png` and `Story Detail-02.png`.

## Acceptance Criteria
- [x] AC1: Given `Story Detail-01.png`, renders dark teal starry gradient hero with 3D mosque, back button, heart favorite toggle, download button, synopsis, badges row, scholar-reviewed card, and "▶ Continue — Episode X" button.
- [x] AC2: Given `Story Detail-02.png`, renders episode list with green checkmark for completed, episode number and progress bar for in-progress, and lock icon with server-supplied unlock condition text for locked episodes.
- [x] AC3: TalkBack reads: "Episode [N], [locked/unlocked], [unlock_condition / duration]".
- [x] AC4: Tier-gated episodes render `ParentGatedPaywallCard` routing through `ParentPinGateModal`.
- [x] AC5: 100% Design System token compliance (`rule.md`): 0 raw colors, 0 raw dp/sp, 0 raw shapes, 0 raw M3 components, < 500 lines per file, 4-locale parity.

## Technical Notes
- Files in scope: `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/ui/detail/*`.
