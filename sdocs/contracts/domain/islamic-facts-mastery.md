---
id: domain.islamic-facts-mastery
kind: service
title: Islamic Facts Mastery Engine Domain Registration & Extensibility Interface
status: stable
owner_story: TASK-B18-05
version: 1
created: 2026-10-12
---

## Overview

Registers `islamic_facts` as a first-class participating domain in Feature A.9's shared Mastery Engine and Spaced-Repetition Scheduler via Alembic data migration `0103_register_islamic_facts_mastery_domain.py` (Blueprint B-05).

## Domain Invariants

1. **Zero Parallel Mastery Logic Invariant**:
   - Zero custom state-machine, scoring, or scheduling calculation code introduced in content module.
   - 100% architectural reuse of Feature A.9's domain-agnostic `compute_next_state`, `compute_mastery_score`, and `SpacedRepetitionScheduler`.
2. **Global Daily Review Prompt Cap Participation (FR-4)**:
   - Islamic facts resurfacing prompts are bounded by the platform-wide daily review cap (`DEFAULT_DAILY_REVIEW_PROMPT_CAP = 2`) shared across Quran, Arabic, Tajweed, and Facts.
3. **Referential Integrity & Migration Atomicity**:
   - Migration strictly validates all registered skill nodes against active `fact.fact_id` rows; aborts with transaction rollback on dangling references.
4. **Historical Evidence Preservation on Revocation (Edge Case 5)**:
   - Revoking a fact's scholar approval stops future selection/resurfacing eligibility, but preserves child's historical mastery records and parent progress aggregates intact.

## Extensibility Verification Interface

```python
# Sourced from A.9 shared engine without modification:
from src.noorheroes.modules.mastery.state_machine import compute_next_state
from src.noorheroes.modules.mastery.scoring import compute_mastery_score
from src.noorheroes.modules.mastery.scheduler import SpacedRepetitionScheduler
```
