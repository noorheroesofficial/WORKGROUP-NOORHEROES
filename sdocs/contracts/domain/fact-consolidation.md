---
id: domain.fact-consolidation
kind: service
title: Fact Architecture Consolidation & Legacy Retirement Domain Contract
status: stable
owner_story: TASK-B18-08
version: 1
created: 2026-10-13
---

## Overview

Retires the legacy A.2 fact implementation in `modules/facts` in favor of the unified B.18 Islamic Facts engine in `modules/content`, repoints Home Section 10 feed, executes non-destructive historical data migration 0104, and manages the runtime cutover toggle (Blueprint B-08).

## Domain Invariants

1. **Sole Authoritative Owner**:
   - `FactSelectionService` (`modules/content/services/fact_selection_service.py`) is the exclusive authoritative owner of `GET /v1/facts/daily`.
2. **Defensive Occasion Gate**:
   - Preserves shared `IslamicCalendarService.resolve_occasion()` with defensive `isinstance(..., str)` checks to protect greeting occasions ("Jummah Mubarak").
3. **Legacy Service Retirement**:
   - Instantiation of legacy `FactService`, `FactRepository`, and `HomeFactHistory` in `modules/facts` emits `DeprecationWarning`.
4. **Non-Destructive Migration & Isolated Downgrade**:
   - Migration 0104 preserves `home_fact_history` intact as a rollback safety net.
   - `downgrade()` deletes only rows matching `migrated_legacy_%`, guaranteeing zero collateral damage to post-cutover organic child history.
5. **Runtime Cutover Feature Flag**:
   - Managed via `settings.b18_facts_cutover_enabled: bool = True`.

## Integration Clients

```python
# IslamicCalendarClient repointed to B.18 facts endpoint with surface parameter
from src.noorheroes.modules.home.clients.islamic_calendar_client import IslamicCalendarClient
```
