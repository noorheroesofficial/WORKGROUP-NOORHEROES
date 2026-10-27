---
id: EPIC-036
title: Ramadan Mode Cross-Cutting Seasonal Module
status: planned
prd: ../../PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md
prd_sections: ["1.7", "3", "4", "5", "8", "12"]
depends_on: []
created: 2026-09-30
---

## Description
Implements the backend orchestration layer and core APIs for Ramadan Mode (Feature F.36 / Tasks B-01 to B-08). Orchestrates the 6-phase lifecycle (Pre-Ramadan Countdown, Active Ramadan, Laylatul Qadr, Eid Transition, Eid Celebration, Post-Eid Tail) based strictly on Parent Profile Region. Provides server-computed gamification suppression for Laylatul Qadr, unbypassable parent-configured fasting approach validation, idempotent journey progress and reward dispatch via A.11's shared ledger, an anti-sibling-comparison Family Aggregate, PII-safe certificate/Eid card generation, and a super_admin-gated moon-sighting Eid date override with regional push notifications.

## Stories
- STORY-036-01 — Ramadan Campaign Lifecycle & Region-Keyed Activation Window Service (B-01)
- STORY-036-02 — Hijri Calendar Authority Service & Regional Moon-Sighting Override (B-02)
- STORY-036-03 — Ramadan Mission Content Delivery API with Server-Computed Gamification Suppression (B-03)
- STORY-036-04 — Fasting Log API with Strict Parent-Configured Approach Enforcement (B-04)
- STORY-036-05 — Ramadan Journey Progress & Idempotent Reward Engine Integration (B-05)
- STORY-036-06 — Family Ramadan Aggregate API with Anti-Sibling Comparison Structural Guarantee (B-06)
- STORY-036-07 — PII-Safe Ramadan Certificate & Eid Card Generation with Parent Gate (B-07)
- STORY-036-08 — Super-Admin Moon-Sighting Eid Date Override & Regional Notification API (B-08)
- STORY-036-09 — Ramadan Mode End-to-End Contract & Seam Integration (Integration)

## Out of Scope
- Mobile client Compose UI implementation (handled in K-01 to K-08 under Android domain).
- Admin Portal Next.js frontend pages (handled in N-01 to N-06 under Admin domain).
- Public marketing landing pages for Ramadan (handled in Website domain).
- Parallel content authoring/review pipelines (strictly delegated to E.29 Content CMS).
- Parallel reward/badge economies or ledger tables (strictly delegated to A.11 Reward Service).
