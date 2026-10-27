---
id: domain.fact-integrity-monitoring
kind: service
title: Content Integrity Monitoring & Disputed-Topic Bypass Canary Domain Contract
status: stable
owner_story: TASK-B18-09
version: 1
created: 2026-10-13
---

## Overview

Periodic background jobs and Celery tasks monitoring 100% theological scholar approval across published facts and verifying that the hard AI-assist drafting disable for disputed topics is never bypassed (Blueprint B-09).

## Domain Invariants

1. **P0 Content Governance Violation Detection**:
   - Hourly audit executes inverse SQL join query to detect any `fact_version` with `status='published'` lacking an associated valid, non-revoked `scholar_approval` row (`approved=true AND revoked_at IS NULL`). Emits P0 alert `P0_CONTENT_GOVERNANCE_VIOLATION`.
2. **P0 Disputed-Topic AI-Assist Bypass Detection**:
   - Daily canary samples production AI-assist calls to verify that calls on sensitive topics were properly rejected with HTTP 403 / `DISPUTED_TOPIC_AI_DRAFTING_FORBIDDEN`. Emits P0 alert `P0_DISPUTED_TOPIC_AI_ASSIST_BYPASS`.
3. **Read-Only Detection Invariant**:
   - Both jobs are strictly read-only with respect to content data. They detect and alert; they never attempt automated data mutation.
4. **Celery Beat Cadence**:
   - `fact_integrity_audit_hourly`: 3600.0s (hourly).
   - `disputed_topic_bypass_canary_daily`: 86400.0s (daily).
5. **Prometheus Telemetry Counters**:
   - Increments `content_integrity_audit_runs_total`, `content_integrity_violations_total`, `disputed_topic_bypass_canary_runs_total`, and `disputed_topic_bypass_violations_total`.

## Public Job Interfaces

```python
from src.noorheroes.modules.content.jobs.fact_integrity_audit import run_fact_integrity_audit
from src.noorheroes.modules.content.jobs.disputed_topic_bypass_canary import run_disputed_topic_bypass_canary
```
