# Phase 12 — Definition of Done & GA Launch Gate

`Development_Blueprints.Phase12_Production_Readiness.CrossPlatform.01-definition-of-done-ga-gate-checklist.md`

**Module:** CrossPlatform (`backend/`, `admin-web/`, `.github/workflows/`, `infra/ci/`)
**Phase:** Phase 12 — Production Readiness & GA Gate
**Depends on:** Phases 0–11 in full — the monorepo/coding-standards/branch-policy foundation (Phase 0), infrastructure and the 13-stage CI/CD pipeline including the manual production-promotion gate (Phase 1, especially `CI_CD.09`), backend/KMP/Admin foundational infrastructure (Phases 2–3, confirmed built per `NoorHeroes_Consolidated_Execution_Blueprint.md` §0.5), every A–F feature module (Phases 4–8), the architectural-invariant suite and coverage gates (Phase 9), the incident-response runbook/pentest-disposition process/NFR load validation (Phase 10), and blue-green/canary deploy plus DR restore validation (Phase 11)
**Consumed by:** none — this is the terminal file in the roadmap. Its only "consumer" is the act of launch itself: the human/process event of removing beta-gating, flipping app-store visibility to public, and ending the marketing embargo, none of which are engineering artifacts this corpus specifies elsewhere
**Source of truth:** `NoorHeroes_Consolidated_Blueprint_v6.md` §22 ("Definition of Done," 13 items, verbatim in §1 below) and §23 ("Open Questions, Assumptions & Risks" — specifically §23.2's 10-item Assumed Requirements index, reconciled in §18 below); `NoorHeroes_Final_Development_Prompt.md` §11 ("Definition of Done (per feature, applied uniformly)," 9 clauses, verbatim in §1 below); `NoorHeroes_Consolidated_Execution_Blueprint.md` §13 (Phase 12's own entry/exit criteria) and §0.5 (current repository completion status, used for this file's dry-run in §14)
**Status:** NEW — this file does not exist in the corpus today; Phase 12 is a confirmed, total gap and the final item in the entire 722-file execution sequence

**Do not re-litigate:** every A–F feature module (37 features) already has a fully-specified PRD and Development Blueprint. Phases 0/2/3's foundational infrastructure is confirmed already built (`NoorHeroes_Consolidated_Execution_Blueprint.md` §0.5). This file does not re-verify, re-test, or re-implement any of that underlying work — it builds the **tracking and enforcement mechanism** that records whether each of the 13 + 9 Definition-of-Done items is true for each of the 37 features, whether the org-level cross-phase exit criteria are met, and whether every "Assumed Requirement" has been confirmed or re-decided — and it wires that mechanism into the existing production-promotion pipeline (`CI_CD.09`, and later Phase 11's blue-green strategy) so a GA-labeled release cannot be promoted while the gate reports red. If the gate reports red, the fix is upstream work in Phases 0–11, never a change to this file's enforcement logic.

---

## 1. Objective and Purpose

NoorHeroes is a children's Islamic-education product. Its General Availability launch is not a routine deploy — a mistake at GA (a content-moderation gap, an unconsented data flow, a broken parental control) has outsized trust and safety consequences that a normal software release does not carry. `NoorHeroes_Consolidated_Blueprint_v6.md` §22 already defines what "done" means for a feature, and its own text is explicit that the checklist "is not merely aspirational guidance" — it is meant to be **audited**. As written anywhere else in the corpus, however, it is a checklist a human could skim and rubber-stamp. This file's objective is to make that impossible: it builds a database-backed, RBAC-authorized, append-only-audited, CI-enforced gate that a GA-labeled production release physically cannot pass unless every item is recorded as signed off by an authorized role-holder, with a documented exception path for the rare item that cannot be fully verified pre-launch.

Concretely, after this file's implementation:

1. **Every one of the 13 Definition-of-Done items** (`NoorHeroes_Consolidated_Blueprint_v6.md` §22, quoted verbatim in §2.1) has a recorded status for every one of the 37 shipped features (A.1–F.37), stored in a new backend bounded context, not a spreadsheet or a Markdown checklist someone can edit without a trace.
2. **Every one of the 9 per-feature process clauses** in `NoorHeroes_Final_Development_Prompt.md` §11 (quoted verbatim in §2.2) is tracked the same way, as a companion checklist to the 13 items above — the two sources define overlapping but distinct dimensions of "done" and this file reconciles rather than collapses them (§2.3).
3. **Every one of the 10 "Assumed Requirement" items** indexed in `NoorHeroes_Consolidated_Blueprint_v6.md` §23.2 has an explicit team decision recorded — either "CONFIRMED AS-IS" or "RE-DECIDED: `<new value>`" — never silently carried forward as an inferred default into a production launch (§18).
4. **A GA-labeled production promotion through `CI_CD.09`** (and, once it exists, Phase 11's blue-green/canary strategy) calls this file's gate-status API before the human-approval stage even opens, and fails the pipeline outright if the gate is not green — the same "CI/gateway layer performs zero business-authorization logic of its own" principle F37 B-03 already established for every other authorization decision in this system applies here too: the CI script only asks the backend service for a yes/no, it never re-implements the sign-off logic itself (§12).
5. **A signed-off item that regresses** after sign-off but before actual launch (a new PR touches previously-clean code, coverage drops, a new pentest finding opens) is detected automatically and flips back to a blocking state — sign-off is a claim about a specific evidence snapshot, not a permanent grant (§11).

## 2. Scope and Requirements

### 2.1 The 13-item Definition of Done — `NoorHeroes_Consolidated_Blueprint_v6.md` §22 (verbatim)

> Every feature is complete only when it includes:

| # | Item (verbatim from v6 §22) |
|---|---|
| 1 | Product acceptance criteria. |
| 2 | Child/parent/admin authorization rules. |
| 3 | Age, locale, consent, and entitlement logic. |
| 4 | Loading, empty, error, offline, and partial-sync states. |
| 5 | Accessibility and RTL behavior. |
| 6 | Analytics events and metric definitions. |
| 7 | API contract and data ownership. |
| 8 | Security and privacy review. |
| 9 | Content/scholar review, where relevant. |
| 10 | Admin/support visibility. |
| 11 | Idempotency and retry behavior. |
| 12 | Feature flag, rollback, and kill-switch plan. |
| 13 | Automated tests and operational monitoring. |

Source text confirms the exact count (13) and states this checklist "is explicitly audited across **all** shipped features" as "a launch-readiness gate — it is not merely aspirational guidance." This file is that audit made real.

### 2.2 The 9-clause per-feature Definition of Done — `NoorHeroes_Final_Development_Prompt.md` §11 (verbatim, split into enumerable clauses)

> A feature is not "done" until: it went through the §12 Development Workflow (plan and documentation approved *before* implementation started, not retrofitted afterward); it matches its owning PRD's functional/validation/error-handling rules; it has unit + integration test coverage meeting the §5 thresholds; any new API endpoint is documented in the OpenAPI schema and the Admin/mobile generated clients are regenerated; any child-facing content path has scholar + child-safety approval wired into its publish flow; any security-sensitive change has passed the relevant architectural test from §5/§9; it is instrumented with the analytics events already named in its owning PRD; it built entirely on top of the §13 foundational infrastructure rather than introducing a parallel, feature-local version of something §13 already provides; and it has been through code review against the checklist in §4.

| # | Clause (paraphrased for a table row; full text above is authoritative) | Automatable evidence source |
|---|---|---|
| a | Went through the §12 Development Workflow — plan + docs approved before implementation | PR description links to the approved plan/doc artifact; no automated signal, human-attested |
| b | Matches owning PRD's functional/validation/error-handling rules | Human-attested against the PRD; no automated signal |
| c | Unit + integration test coverage meets §5 thresholds | **Automatable** — Phase 9 `CrossPlatform.02` coverage-gate CI job result |
| d | New API endpoints documented in OpenAPI schema; Admin/mobile generated clients regenerated | **Automatable** — `openapi-sync.yml` (per `CI_CD.06`) diff-clean check |
| e | Child-facing content path has scholar + child-safety approval wired into publish flow | **Partially automatable** — E29/E30 content-publish-state API queried for "published" status implying the wired approval gate fired |
| f | Security-sensitive change passed the relevant architectural test from §5/§9 | **Automatable** — Phase 9 `CrossPlatform.01` architectural-invariant suite result |
| g | Instrumented with analytics events named in owning PRD | Human-attested against the PRD's named event list; no generic automated signal exists |
| h | Built entirely on §13 foundational infrastructure, not a parallel feature-local reimplementation | Human-attested at code review time; no automated signal |
| i | Been through code review against the §4 checklist | **Automatable** — GitHub PR approval record exists and references the §4 checklist in its template |

### 2.3 Reconciling the two lists — deliberately not collapsed into one

The two lists measure different things and this file tracks them as **two adjacent, not merged, checklists per feature**: v6 §22's 13 items describe *what a finished feature must have* (an artifact-completeness lens); Final_Development_Prompt §11's 9 clauses describe *how it must have gotten there* (a process-compliance lens). A feature could satisfy every §22 artifact and still have skipped the §12 workflow process (§11 clause a) — that is a real, distinct problem this gate must be able to surface, not paper over by only tracking one list. Where the two lists name the same underlying fact from different angles (§22 item 13 "automated tests" and §11 clause c "coverage meeting §5 thresholds"; §22 item 7 "API contract" and §11 clause d "OpenAPI schema documented") the gate's evidence-linking (§6.3) points both cells at the same underlying signal so a single piece of automatable evidence satisfies both without double data entry — but the two checklist rows themselves remain visually and structurally distinct in the tracking schema, because a future audit needs to be able to answer "was §22 satisfied" and "was §11 followed" as separate questions.

### 2.4 In scope for this file

- A new backend bounded context, `ga_readiness`, following the exact Clean-Architecture layering (`api.py` / `service.py` / `repository.py` / `models.py` / `schemas.py` / `events.py`) every other bounded context already uses per `FAST-API-INSTRUCTIONS.md` §1/§5.
- Six new PostgreSQL tables (§8) — item definitions, current-state tables for org-level items, per-feature-per-item DoD cells, Assumed Requirements confirmations, exceptions, and an append-only sign-off audit ledger.
- An RBAC-authorized, maker-checker admin API (`/v1/admin/ga-readiness/...`) and one read-only machine-to-machine endpoint CI calls (§6).
- An Admin Portal page (`admin-web/src/features/ga-readiness/`) rendering the full matrix, the org-level checklist, Assumed Requirements log, exceptions, and a single GA GATE: APPROVED / NOT APPROVED banner, RBAC-gated per §9.
- A CI script (`infra/ci/verify-ga-gate.sh`) and the specific edits to `CI_CD.09`'s `promote-and-deploy-production-*` jobs that invoke it only for GA-labeled releases (§12.1), plus the equivalent hook point documented for Phase 11's eventual blue-green/canary file (§12.2).
- A scheduled regression-detection job (§11.3) that re-checks automatable evidence and flips signed-off items back to a blocking state when their underlying evidence no longer supports the prior sign-off.
- Seed data (a migration, not application code) for the 22 org-level item definitions (13 + 9) and the 10 Assumed Requirements rows.

### 2.5 Explicitly out of scope

- Actually performing any of the 13 or 9 checklist items for any feature — that work belongs to whichever phase/module owns the underlying capability (e.g., "scholar review" is E29/E30's job; this file only records whether it happened).
- Actually running the incident-response tabletop exercise (F37 `B-08`'s job) or filing/closing penetration-test findings (F37 `B-09`'s job) — this file only reads their outcomes as evidence (§12.3) and records the org-level "has the tabletop actually run at least once" boolean the Phase 12 exit criteria in the Execution Blueprint §13 explicitly names.
- Redesigning `CI_CD.09`'s existing manual-promotion mechanism, GitHub Environment protection, or Slack notification scripts — this file adds one new pre-check step; everything else in that file is untouched.
- Building Phase 11's blue-green/canary deployment strategy itself — only documenting the identical hook point that file must add when it is authored (§12.2).
- A generic "release management" tool, changelog generator, or version-bumping mechanism — Phase 0's `Repo.03` (Conventional Commits/SemVer) already owns that; this file only consumes a release's tag/label to decide whether the gate applies (§12.1).

## 3. Technical Implementation Details

### 3.1 Why a backend bounded context, not a Markdown/YAML file in the repo

A checklist file living in the repository (a `GA_READINESS.md`, a YAML state file) can be edited by anyone with write access, in the same PR as the code it is meant to gate, with no distinct authorization check beyond ordinary code review — exactly the "someone might skim it" failure mode the task brief names. Every other cross-cutting governance mechanism this corpus already specifies — the feature-flag dual-sign-off state machine (`CI_CD.10`), E28's maker-checker for high-risk RBAC changes, F37 `B-08`'s database-role-level append-only audit-log enforcement, F37 `B-09`'s `penetration_test_findings` disposition workflow — is a **backend-service-owned, database-backed** mechanism with its own RBAC-authorized API and an Admin Portal UI that only ever *reflects* backend-decided state, never re-implements the decision logic. This file follows that established pattern exactly, for the same reason: the backend `GaReadinessService` is the **sole enforcer** of every sign-off rule, role check, and two-person requirement; the CI script, the Admin Portal UI, and every other consumer are read-only or command-issuing clients of that one service, never independent decision-makers.

### 3.2 Reuse of the CI_CD.10 dual-sign-off pattern

`CI_CD.10`'s `feature_flag_approvals` table and `FeatureFlagService`'s maker/checker enforcement is the closest existing precedent in the corpus to what this file needs, and this file's `ga_gate_signoff_events` ledger (§8.6) and `GaReadinessService` (§4) are deliberately structured the same way: a **propose** action (maker) records intent; a structurally distinct **approve** action (checker), required to come from a different authenticated admin than the proposer, is what actually flips status to `signed_off`. The GA gate raises the bar once further than `CI_CD.10` does — the checker must additionally hold the *same owning role* as the item being signed off (§9.1), not merely "any other admin," since a GA item's authority derives from domain expertise (a Security Lead cannot meaningfully co-sign a Scholar/Content item), which `CI_CD.10`'s flag-approval model does not need to enforce because any admin with flag-management permission is an acceptable second reviewer for a feature-flag rollout.

### 3.3 Two authorization surfaces, one enforcement point

Some DoD items are naturally engineering/CI artifacts (test coverage, architectural-invariant results, OpenAPI-client-regeneration cleanliness) and some are naturally business/content/legal judgments (acceptance criteria, consent logic, scholar review, admin/support visibility). Both surfaces — a GitHub PR's approvals and an Admin Portal action — ultimately write to the **same** backend API (§6), through the **same** `GaReadinessService` enforcement (§4), landing in the **same** audit ledger (§8.6). GitHub is never itself the system of record; a GitHub Action that observes a PR merged with the right CODEOWNERS approval calls the backend API on the engineering side exactly the way an Admin Portal button click calls it on the business side. This keeps "who is allowed to say an item is done" as a single, auditable, role-checked decision regardless of which surface a human used to make it.

### 3.4 Evidence linking, not blind trust

Every status-change API call accepts an `evidence_url` (a PR link, a CI run URL, a pentest-finding ID, an Admin Portal content-review record ID) and, where an automatable signal exists (§2.1/§2.2's "Automatable evidence source" column), the service independently re-fetches that signal at write time and refuses the transition if the claimed evidence does not actually support it (e.g., rejects a `signed_off` transition on the coverage-gate item if the linked CI run's own conclusion was `failure`). This prevents an authorized-but-mistaken (or malicious) sign-off from being accepted purely because the correct role clicked the correct button — the service checks the underlying fact, not just the human's role, wherever a fact is checkable.

## 4. Architecture and Component Responsibilities

```text
┌───────────────────────────────────────────────────────────────────────────────┐
│                          GaReadinessService (BaseService)                     │
│   SOLE enforcer of: role-authorization, two-person maker/checker rule,        │
│   evidence re-validation, state-machine transitions, regression detection.    │
│   Every other component below is a CONSUMER or COMMAND-ISSUER — never a       │
│   second decision-maker — mirroring F37 B-03's "zero business-authorization   │
│   logic outside the domain service" principle, applied here to governance.    │
└───────────────────────┬───────────────────┬───────────────────┬───────────────┘
                         ▼                   ▼                   ▼
              ga_readiness/api.py    Celery beat job:      Outbox → domain events
              (RBAC-gated admin      detect_regressions     ga_readiness.item_signed_off
              endpoints, §6)         (nightly + on merge     ga_readiness.item_regressed
                         │           to main, §11.3)         ga_readiness.exception_granted
        ┌────────────────┼────────────────┐                        │
        ▼                ▼                ▼                        ▼
  Admin Portal      GitHub Action     CI_CD.09 /              Slack notifier +
  `ga-readiness`    (engineering-     Phase 11 gate            GitHub issue
  feature module    side sign-off     script (READ-ONLY        reopener
  (propose/approve  on PR merge,      `gate-status` call
  UI, §9.2)          §12.1)            only, §12.1)
```

| Component | Responsibility |
|---|---|
| `backend/src/noorheroes/modules/ga_readiness/service.py` — `GaReadinessService(BaseService)` | Owns every rule in §9–§11: who may propose/approve a given item, the two-person/same-role check, evidence re-validation, the state machine, and regression detection's write path. No other component ever writes to this context's tables directly. |
| `backend/src/noorheroes/modules/ga_readiness/repository.py` | Data access only — no business rules, per the same layering every other bounded context already follows. |
| `backend/src/noorheroes/modules/ga_readiness/api.py` | Thin FastAPI router; RBAC dependency injection (`RequirePermission`) only, delegates everything else to the service. |
| `admin-web/src/features/ga-readiness/` | Renders whatever state the API returns; disables propose/approve buttons based on the current admin's own role as UX convenience only — the actual authorization check happens server-side regardless of what the UI allows the user to click, exactly as `CI_CD.10` §4 already establishes for feature-flag approvals. |
| `infra/ci/verify-ga-gate.sh` | Calls one read-only endpoint, exits non-zero on a red gate. Contains zero sign-off logic of its own. |
| `detect_regressions` Celery beat task | Re-checks automatable evidence for every `signed_off` item; calls `GaReadinessService.flag_regression()` — does not itself decide the outcome by any logic outside that service call. |
| GitHub Action `ga-readiness-signoff-sync.yml` | Observes a merged PR with a CODEOWNERS-satisfying approval for an engineering-side item (§9.1), calls the backend's propose/approve API with a scoped service token — never writes a decision the backend service itself would refuse. |

## 5. Folder/File Structure

```text
noorheroes/
├── backend/
│   ├── alembic/versions/
│   │   └── 2027_XX_XX_add_ga_readiness_context.py     # NEW — 6 tables + seed data (§8)
│   └── src/noorheroes/modules/ga_readiness/            # NEW — 13th bounded context
│       ├── __init__.py
│       ├── models.py          # SQLAlchemy models for the 6 tables (§8)
│       ├── schemas.py         # Pydantic request/response schemas (§6)
│       ├── repository.py      # GaReadinessRepository(BaseRepository)
│       ├── service.py         # GaReadinessService(BaseService) — the enforcer (§4, §9–§11)
│       ├── api.py             # /v1/admin/ga-readiness/* router (§6)
│       ├── events.py          # item_signed_off / item_regressed / exception_granted outbox events
│       └── tasks.py           # detect_regressions Celery beat task (§11.3)
├── admin-web/
│   └── src/features/ga-readiness/                      # NEW
│       ├── api/ga-readiness-client.ts                  # thin wrapper over the generated OpenAPI client
│       ├── hooks/use-ga-gate-summary.ts
│       ├── hooks/use-propose-item-status.ts
│       ├── hooks/use-approve-item-status.ts
│       ├── components/gate-status-banner.tsx           # the APPROVED / NOT APPROVED banner
│       ├── components/dod-matrix-table.tsx             # 37 × 13 feature-DoD matrix
│       ├── components/process-checklist-table.tsx      # 37 × 9 Final_Development_Prompt §11 matrix
│       ├── components/assumed-requirements-log.tsx
│       ├── components/exceptions-panel.tsx
│       └── page.tsx                                    # route: /ga-readiness (E28 RBAC-gated)
├── infra/ci/
│   └── verify-ga-gate.sh                                # NEW — the single script CI_CD.09 / Phase 11 call
└── .github/workflows/
    ├── backend.yml                                      # MODIFIED — one new pre-check step, §12.1
    ├── admin-web.yml                                    # MODIFIED — same, for admin-web's own promotion
    └── ga-readiness-signoff-sync.yml                     # NEW — engineering-side sign-off relay, §9.1
```

## 6. APIs, Models, Interfaces, and Data Flow

### 6.1 Admin API — human-facing (maker/checker)

| Method & Path | Purpose | Auth |
|---|---|---|
| `GET /v1/admin/ga-readiness/summary` | Org-level gate state, all 22 item statuses, Assumed Requirements confirmation count, exception count, overall `ga_approved: bool` | Any admin with `ga_readiness:read` |
| `GET /v1/admin/ga-readiness/items` | The 22 org-level item definitions (13 + 9) with current status, owner role, evidence | Any admin with `ga_readiness:read` |
| `POST /v1/admin/ga-readiness/items/{item_id}/propose` | Maker step — propose a status transition with `evidence_url` | Admin holding the item's `owner_role` (§9.1) |
| `POST /v1/admin/ga-readiness/items/{item_id}/approve` | Checker step — confirm a pending proposal, must be a **different** admin holding the same `owner_role` | Admin holding the item's `owner_role`, `admin_id != proposer_admin_id` |
| `GET /v1/admin/ga-readiness/features/{feature_id}/dod` | The 13-item + 9-clause matrix rows for one feature (e.g. `A3`) | Any admin with `ga_readiness:read` |
| `POST /v1/admin/ga-readiness/features/{feature_id}/dod/{item_key}/propose` | Maker step for a per-feature cell | Admin holding that item's `owner_role` |
| `POST /v1/admin/ga-readiness/features/{feature_id}/dod/{item_key}/approve` | Checker step for a per-feature cell | Same role, different admin |
| `GET /v1/admin/ga-readiness/assumed-requirements` | The 10 Assumed Requirement rows (§18) and their confirm/re-decide status | Any admin with `ga_readiness:read` |
| `POST /v1/admin/ga-readiness/assumed-requirements/{req_id}/decide` | Record CONFIRMED or RE-DECIDED with a value and rationale | Admin holding the item's `owner_role`, maker/checker as above |
| `POST /v1/admin/ga-readiness/exceptions` | Request an exception for an item that cannot be fully verified pre-launch (§10) | Admin holding the item's `owner_role` |
| `POST /v1/admin/ga-readiness/exceptions/{exception_id}/executive-approve` | Executive Sponsor sign-off, the second required approval for any exception | Admin holding `executive_sponsor` role, distinct from the requester |
| `GET /v1/admin/ga-readiness/audit-log` | Paginated, filterable view of the full append-only `ga_gate_signoff_events` ledger | Any admin with `ga_readiness:read` |

### 6.2 Machine-to-machine API — CI-facing (read-only, no sign-off capability)

```
GET /v1/admin/ga-readiness/gate-status
Authorization: Bearer <ga_gate_ci_readonly service-account token, scope=ga_readiness:gate_status_read>

200 OK
{
  "ga_approved": false,
  "checked_at": "2026-08-24T00:00:00Z",
  "org_items_signed_off": 9,
  "org_items_total": 22,
  "features_fully_done": 12,
  "features_total": 37,
  "assumed_requirements_decided": 6,
  "assumed_requirements_total": 10,
  "open_exceptions_without_executive_signoff": 1,
  "incident_response_tabletop_executed": false,
  "blocking_items": [
    {"scope": "org", "item_key": "v6_22_item_13_automated_tests_monitoring", "status": "in_review", "owner_role": "engineering_lead"},
    {"scope": "assumed_requirement", "item_key": "ar_07_rpo_rto_targets", "status": "not_decided", "owner_role": "engineering_lead"},
    {"scope": "org", "item_key": "tabletop_exercise_executed", "status": "not_started", "owner_role": "security_lead"}
  ]
}
```

This is the **only** endpoint CI ever calls (§12.1). It is intentionally read-only — the CI service-account token this file provisions (§7.2) is scoped `ga_readiness:gate_status_read` and nothing else, so even a fully compromised CI credential cannot forge a sign-off, matching the least-privilege principle `CI_CD.09` §9.2 already establishes for its own production-deploy service account.

### 6.3 Core data model (see §8 for full DDL-level detail)

```
GaGateItem            (id, source, item_number, item_text, owner_role, is_automatable, evidence_source)
GaGateItemStatus       (item_id FK, status, proposed_by, proposed_at, evidence_url,
                         approved_by, approved_at, current as-of this row)
GaGateFeatureDoD       (feature_id, item_id FK[source=v6_22 or fdp_11], status, ...same maker/checker fields)
GaGateAssumedRequirement (id, v6_section_ref, description, owner_role, decision[confirmed|re_decided|not_decided],
                          decided_value, rationale, decided_by, decided_at)
GaGateException        (id, item_id FK, feature_id nullable, justification, risk_acceptance,
                         mitigation_plan, expiry_date, requested_by, executive_approved_by, status)
GaGateSignoffEvent      (id, event_type, item_id nullable, feature_id nullable, exception_id nullable,
                          actor_admin_id, actor_role, previous_status, new_status, evidence_url,
                          git_commit_sha nullable, created_at)   — APPEND-ONLY, §8.6
```

### 6.4 Data flow summary

1. A domain owner (e.g., the Scholar/Content Lead) completes work satisfying item 9 for feature `A3` in E29/E30's content-review workflow.
2. They (or an automation reading E29/E30's publish-state API) call `POST /v1/admin/ga-readiness/features/A3/dod/v6_22_item_09/propose` with `evidence_url` pointing at the content-review record.
3. `GaReadinessService` checks role (`scholar_content_lead`), checks the item is not already `signed_off`, re-fetches the evidence URL's underlying state where automatable, writes a `GaGateFeatureDoD` row with status `in_review`, and appends a `proposed` event to `GaGateSignoffEvent`.
4. A **different** Scholar/Content Lead admin calls the `approve` endpoint; the service verifies role + distinct-admin, flips status to `signed_off`, appends an `approved` event, and emits a `ga_readiness.item_signed_off` domain event through the existing transactional outbox.
5. `GET /v1/admin/ga-readiness/summary` and `gate-status` immediately reflect the new count on their next call — no caching layer sits between the API and the current-state tables for this context, since correctness matters far more than latency for a gate an entire launch depends on.
6. Nightly (and on every merge to `main`), `detect_regressions` re-checks every `signed_off` item's automatable evidence; a mismatch calls `GaReadinessService.flag_regression()`, which flips status to `regressed`, appends a `regressed` event, and emits `ga_readiness.item_regressed` (§11.3).

## 7. Dependencies and Configuration Requirements

| Requirement | Detail |
|---|---|
| Phase 2 backend foundation | `BaseService`/`BaseRepository`, async SQLAlchemy/Alembic, structured logging, transactional outbox — all confirmed built (§0.5); this context is additive, no changes to shared infrastructure required. |
| Phase 1 `CI_CD.09` | This file's §12.1 edits are a diff against `CI_CD.09`'s existing `promote-and-deploy-production-*` jobs — that file must exist first (it is a prerequisite of Phase 12 per the roadmap, and is itself an already-specified file in this corpus). |
| Phase 9 `CrossPlatform.01`/`02` | Supplies the automatable evidence for §22 item 13 / §11 clause f (architectural-invariant suite) and §11 clause c (coverage gates) — this file's evidence-revalidation logic (§3.4) queries their CI run results by run ID. |
| F37 `B-08`/`B-09` | Supplies the automatable evidence for the org-level "incident-response tabletop executed" and "open critical pentest findings" checks (§12.3) via their own tables (`penetration_test_findings`, backup-restore-verification job history). |
| E30 `B-05` / F35 `B-05` (evaluation harness) | Supplies the automatable evidence for the org-level "AI safety evaluation harness `critical_findings_count == 0`" check (§12.3) — this file reads that value, it does not re-implement the AI safety gate. |
| Configuration — backend `.env` / Settings | `GA_GATE_CI_TOKEN_HASH` (bcrypt hash of the M2M read-only service-account token, per the existing service-account-token pattern already used for other CI-to-backend calls in this corpus), `GA_GATE_REGRESSION_CHECK_SCHEDULE` (default `0 3 * * *`, 3am daily), `GA_GATE_EXECUTIVE_SPONSOR_ADMIN_IDS` (comma-separated allowlist, §9.3). |
| Configuration — CI | `GA_GATE_API_BASE_URL`, `GA_GATE_CI_TOKEN` (GitHub Actions repository secret, `production`-environment-scoped exactly like the other production credentials `CI_CD.09` §7.2 already lists). |
| Admin Portal RBAC | E28's role table gains five new permission scopes (`ga_readiness:propose:<role>` / `ga_readiness:approve:<role>` per governance role) and one new `executive_sponsor` role/flag — an additive migration to E28's existing RBAC schema, not a redesign of it (§9.1). |

## 8. Database/Storage Requirements

All six tables live in the backend's primary PostgreSQL database, in a new `ga_readiness` schema-qualified table group, migrated via the standard Alembic expand/contract pattern already established (`CI_CD.09` §8.1).

### 8.1 `ga_gate_items` — static item definitions (seeded, effectively read-only after migration)

| Column | Type | Notes |
|---|---|---|
| `id` | `uuid` PK | |
| `source` | `enum('v6_22','fdp_11')` | Which of the two lists (§2.1/§2.2) this row belongs to |
| `item_number` | `smallint` | 1–13 for `v6_22`, 1–9 (a–i mapped to 1–9) for `fdp_11` |
| `item_key` | `text` UNIQUE | e.g. `v6_22_item_09_content_scholar_review`, `fdp_11_clause_e_scholar_child_safety_approval` |
| `item_text` | `text` | Verbatim quoted text from §2.1/§2.2 |
| `owner_role` | `enum(engineering_lead, security_lead, scholar_content_lead, legal_compliance, product)` | Assigned in §4.2 below |
| `is_automatable` | `boolean` | Whether §3.4 evidence-revalidation applies |
| `evidence_source` | `text` nullable | Which upstream system/table supplies automatable evidence, where applicable |

Seeded with exactly 22 rows (13 + 9) by the migration in §5 — never created/edited through the API; a change to the checklist itself is a new migration + a new version of this blueprint file, not a runtime admin action.

### 8.2 `ga_gate_item_status` — current org-level state, one row per item

| Column | Type | Notes |
|---|---|---|
| `item_id` | `uuid` FK → `ga_gate_items.id`, UNIQUE | One current-state row per item |
| `status` | `enum(not_started, in_review, signed_off, regressed, exception_granted)` | The state machine, §11.1 |
| `proposed_by_admin_id`, `proposed_at`, `evidence_url` | | Maker fields |
| `approved_by_admin_id`, `approved_at` | | Checker fields, nullable until approved |
| `version` | `integer` | Optimistic-concurrency guard, same pattern as `CI_CD.10`'s `feature_flag_environment_states.version` |

### 8.3 `ga_gate_feature_dod` — per-feature × per-item cells

| Column | Type | Notes |
|---|---|---|
| `id` | `uuid` PK | |
| `feature_id` | `text` | The corpus's own feature code, e.g. `A3`, `C26`, `F37` — 37 distinct values |
| `item_id` | `uuid` FK → `ga_gate_items.id` | |
| `status` | same enum as §8.2, plus `not_applicable` | Item 9 ("where relevant") legitimately does not apply to every feature — e.g. `F37` Security Architecture has no scholar-review surface; `not_applicable` requires the same maker/checker sign-off as any other status, so a feature cannot silently skip an item without a recorded, role-authorized reason |
| maker/checker/evidence/version fields | | Identical shape to §8.2 |

UNIQUE constraint on `(feature_id, item_id)` — one current-state row per cell, 37 × 22 = 814 possible rows, populated incrementally as each feature's work completes (§14 dry-run discusses the expected population curve).

### 8.4 `ga_gate_assumed_requirements` — the 10 items from v6 §23.2 (§18)

| Column | Type | Notes |
|---|---|---|
| `id` | `uuid` PK | |
| `v6_section_ref` | `text` | e.g. `§2.5`, `§14.7` |
| `description` | `text` | Verbatim from §23.2's index |
| `owner_role` | same enum as §8.1 | |
| `decision` | `enum(not_decided, confirmed, re_decided)` | |
| `decided_value` | `text` nullable | The team's actual chosen value, if `re_decided` — e.g. "RPO ≤ 30 min / RTO ≤ 2 hr" replacing the source doc's "≤ 1 hr / ≤ 4 hr" suggestion |
| `rationale`, `decided_by_admin_id`, `decided_at` | | |

Seeded with exactly 10 rows by the migration (§18 lists them).

### 8.5 `ga_gate_exceptions`

| Column | Type | Notes |
|---|---|---|
| `id` | `uuid` PK | |
| `item_id` FK, `feature_id` nullable | | Which cell this exception covers |
| `justification`, `risk_acceptance`, `mitigation_plan` | `text` | Required, non-empty (§10) |
| `expiry_date` | `date` | Forces a revisit — an exception does not silently live forever |
| `requested_by_admin_id`, `requested_at` | | |
| `executive_approved_by_admin_id`, `executive_approved_at` | nullable | Second required signature, §9.3 |
| `status` | `enum(pending_executive_approval, granted, expired, revoked)` | |

### 8.6 `ga_gate_signoff_events` — the append-only audit ledger

INSERT-only at the database-role level: the application's runtime DB role has `INSERT`/`SELECT` grants on this table and explicitly **no** `UPDATE`/`DELETE` grant, enforced the identical way F37 `B-08` already enforces append-only-ness for its own audit logs ("database-role-level append-only enforcement for audit logs") — this file reuses that exact mechanism rather than inventing a second one.

| Column | Type | Notes |
|---|---|---|
| `id` | `bigserial` PK | |
| `event_type` | `enum(proposed, approved, rejected, regressed, exception_requested, exception_granted, exception_expired)` | |
| `item_id`, `feature_id`, `exception_id` | nullable FKs | Whichever scope the event applies to |
| `actor_admin_id`, `actor_role` | | Who did it and under which authorized role |
| `previous_status`, `new_status` | | |
| `evidence_url` | nullable | |
| `git_commit_sha` | nullable | Populated when the event originates from the GitHub Action relay (§9.1) |
| `created_at` | `timestamptz`, `default now()` | Immutable, server-assigned — never client-supplied, preventing backdating |

Every write anywhere in this bounded context (§8.2–§8.5 status changes) is always paired, in the same DB transaction, with exactly one `ga_gate_signoff_events` row — the ledger is the true history; the "current state" tables in §8.2/§8.3 are a materialized projection of it, kept only for fast reads.

## 9. Authentication, Authorization, Validation, and Security Considerations

### 9.1 Owner-role assignment for the 13 v6 §22 items

| # | Item | Owner role | Rationale |
|---|---|---|---|
| 1 | Product acceptance criteria | **Product** | The PRD's author and the party best positioned to confirm the shipped feature matches acceptance criteria they defined |
| 2 | Child/parent/admin authorization rules | **Security Lead** | Authorization correctness is a security property; implemented by Engineering, attested by Security per the F37 authorization-boundary pattern already established across the corpus |
| 3 | Age, locale, consent, and entitlement logic | **Legal/Compliance** | Consent and age-gating are compliance-defined rules (COPPA/GDPR-K-equivalent obligations); locale/entitlement business rules are consulted with Product but the compliance-sensitive core of this item sits with Legal/Compliance |
| 4 | Loading, empty, error, offline, and partial-sync states | **Engineering Lead** | Pure implementation-completeness question |
| 5 | Accessibility and RTL behavior | **Product** | Accessibility/localization standards are a product-quality bar Product owns; Engineering Lead is consulted as implementer |
| 6 | Analytics events and metric definitions | **Product** | Product defines the KPI framework these events feed (`NoorHeroes_Consolidated_Blueprint_v6.md` §15) |
| 7 | API contract and data ownership | **Engineering Lead** | Architectural correctness, automatable via OpenAPI-diff evidence |
| 8 | Security and privacy review | **Security Lead** | Direct match |
| 9 | Content/scholar review, where relevant | **Scholar/Content Lead** | Direct match |
| 10 | Admin/support visibility | **Product** | Product/Ops owns whether support tooling has what it needs; Engineering Lead consulted as implementer |
| 11 | Idempotency and retry behavior | **Engineering Lead** | Pure implementation-correctness question |
| 12 | Feature flag, rollback, and kill-switch plan | **Engineering Lead**, co-signed by **Security Lead** for any item `CI_CD.10` classifies `safety_relevant=true` | Reuses `CI_CD.10`'s own dual-sign-off requirement rather than defining a second, competing one |
| 13 | Automated tests and operational monitoring | **Engineering Lead** | Automatable via Phase 9 coverage-gate + architectural-invariant CI results |

### 9.2 Owner-role assignment for the 9 Final_Development_Prompt §11 clauses

| Clause | Owner role |
|---|---|
| a — §12 workflow followed | **Engineering Lead** |
| b — matches owning PRD | **Product** |
| c — coverage thresholds met | **Engineering Lead** (automatable) |
| d — OpenAPI schema + generated clients regenerated | **Engineering Lead** (automatable) |
| e — scholar + child-safety approval wired into publish flow | **Scholar/Content Lead**, co-signed by **Security Lead** (this clause explicitly names both "scholar" and "child-safety") |
| f — passed relevant architectural test | **Security Lead** (automatable) |
| g — instrumented with named analytics events | **Product** |
| h — built on §13 foundational infra, no parallel reimplementation | **Engineering Lead** |
| i — code review passed against §4 checklist | **Engineering Lead** (automatable — PR approval record) |

### 9.3 Enforcement rules (all enforced server-side by `GaReadinessService`, never by the Admin Portal UI or a CI script)

1. **Role match required to propose or approve.** `RequirePermission` checks the acting admin's role grants against the specific item's `owner_role` (or, for co-signed items, either of the two named roles) before any write is accepted.
2. **Two-person rule.** `approved_by_admin_id` must differ from `proposed_by_admin_id` on every transition to `signed_off` — enforced as a database CHECK constraint in addition to the service-layer check, so even a service-layer bug cannot silently violate it.
3. **No self-elevation, no Super Admin blanket bypass.** A Super Admin account may hold one of the five governance roles explicitly (assigned the same way any other admin is), but holding the platform's most senior role does **not** itself satisfy any item's `owner_role` check — mirroring E28's own stated goal that "no admin (including other super admins) can silently self-elevate their own access." The only Super-Admin-specific capability this context grants is initiating the documented break-glass exception path (§10), which itself still requires the separate Executive Sponsor signature.
4. **Executive Sponsor is a distinct, narrowly-scoped role.** `GA_GATE_EXECUTIVE_SPONSOR_ADMIN_IDS` (§7) is a small, explicitly configured allowlist — not derived from any existing admin role — so the second signature on an exception is always a deliberate, named individual's decision, never inferred from generic seniority.
5. **Evidence re-validation.** Per §3.4, any `is_automatable=true` item's proposed evidence is independently re-checked server-side before the transition is accepted; a mismatch returns `422 Unprocessable Entity` with the actual observed value, never silently accepts the claim.
6. **Audit ledger writes are transactional and non-optional.** `GaReadinessService` never commits a status-table write without an accompanying `ga_gate_signoff_events` insert in the same database transaction — there is no code path that changes state without leaving a ledger entry.
7. **CI credential is read-only.** The `ga_readiness:gate_status_read` scope (§6.2, §7) grants access to exactly one endpoint and cannot write to any table in this context under any circumstance — a compromised CI secret cannot forge or bypass a sign-off.

## 10. Error Handling and Edge Cases

| Scenario | Handling |
|---|---|
| An item genuinely cannot be fully verified before launch (e.g., a 90-day production-data metric that cannot exist before 90 days of production traffic) | The item's owner requests an **exception** (`POST /exceptions`) with mandatory `justification`, `risk_acceptance`, `mitigation_plan`, and `expiry_date`. It requires the item owner's own role sign-off **and** a distinct Executive Sponsor's sign-off before `status` becomes `exception_granted` — a two-signature bar higher than ordinary sign-off, reflecting that an exception is a deliberate risk acceptance, not a routine completion. |
| An exception's `expiry_date` passes before actual GA launch | A scheduled job (paired with `detect_regressions`, §11.3) flips `status` to `expired`, which counts as blocking in `gate-status` (§6.2) exactly like `not_started` — an expired exception is not a permanent pass, it forces a fresh decision. |
| A proposer and the only other role-holder for that owner role are the same two people repeatedly (a small team where, e.g., only one Security Lead exists) | Documented operational requirement (§16): each of the five governance roles must have **at least two** distinct admin accounts before this gate can ever reach `GA_APPROVED`, since the two-person rule (§9.3) is mathematically impossible to satisfy with a single role-holder. The `gate-status` summary surfaces `"role_understaffed": ["scholar_content_lead"]` explicitly if a role has fewer than two holders, so this is caught long before it blocks a real launch. |
| A `propose` call's claimed `evidence_url` returns a 404, or the linked CI run is still in progress | Rejected with `409 Conflict` before any state changes — a proposal cannot be made against evidence that does not yet resolvably exist. |
| Two proposals for the same item/cell race each other | `version` optimistic-concurrency column (§8.2/§8.3) — the second writer's transaction fails with `409 Conflict` and must re-read current state before retrying, same pattern `CI_CD.10` §10 already documents for its own approval race. |
| `gate-status` is called while a regression-detection job is mid-run | The endpoint always reads the current-state tables as they stand at query time — a regression job runs inside its own transaction per item, so a partial run never produces an inconsistent read; at worst, a caller sees some regressions already flagged and others not yet reached in that run's iteration order, both of which are individually consistent snapshots. |
| A feature is legitimately exempt from item 9 (no content/scholar-review surface, e.g. `F37`) | Recorded as `status = not_applicable` via the normal maker/checker flow (§8.3) — never left blank, since a blank cell is indistinguishable from "forgotten" while an explicit `not_applicable` sign-off is a recorded, attributable decision. |
| The `ga_readiness` service itself is down when CI calls `gate-status` | `verify-ga-gate.sh` (§12.1) fails closed — a non-200 response or timeout is treated as gate-not-approved, never silently skipped. A gate mechanism that fails open on its own outage is not a gate. |

## 11. State Management and Lifecycle Considerations

### 11.1 Per-item / per-cell state machine

```text
not_started ──propose──> in_review ──approve──> signed_off ──(regression detected)──> regressed
                              │                       │                                    │
                              └──reject───────────────┘                                    │
                                                       └──propose (re-review)───────────────┘
     (any state) ──request exception──> exception pending ──executive approve──> exception_granted
                                                                                        │
                                                                                (expiry_date passes)
                                                                                        ▼
                                                                                    expired
```

`regressed` and `expired` both re-enter the same `in_review`-reachable flow via a fresh `propose` call — a regression is not a dead end, it is a return to "needs re-verification," identical in shape to the original path.

### 11.2 Aggregate gate state

The org-level gate itself (not any single item) moves through:

`NOT_STARTED` → `IN_PROGRESS` (any item proposed) → `ALL_ITEMS_SIGNED_OFF` (every org-level item `signed_off` or `exception_granted`, every feature's every applicable cell `signed_off`/`not_applicable`/`exception_granted`, every Assumed Requirement `decided`) → `GA_APPROVED` (a final, distinct, single Executive Sponsor action confirming the aggregate — `POST /v1/admin/ga-readiness/ga-approve`, itself logged as a `ga_gate_signoff_events` row and requiring `ALL_ITEMS_SIGNED_OFF` as a server-side precondition) → `LAUNCHED` (a manual, out-of-band marker the team sets once the actual public launch event has happened, purely for historical record — this file's gate does not and cannot control app-store visibility or marketing timing directly).

This is a computed value, not a stored column — `GaReadinessService.compute_aggregate_state()` derives it fresh from the current-state tables on every `summary`/`gate-status` call, so it can never drift out of sync with the underlying per-item truth.

### 11.3 Regression detection — what happens to a signed-off item that regresses pre-launch

The scheduled `detect_regressions` task (§7 config: default 3am daily, plus triggered on every merge to `main`) iterates every row in `ga_gate_item_status`/`ga_gate_feature_dod` currently `signed_off` where `is_automatable=true`, re-fetches the linked evidence source (a fresh coverage-gate run, the current architectural-invariant suite result, the current `penetration_test_findings` open-critical count, the current evaluation-harness `critical_findings_count`), and compares it against the value recorded at sign-off time. On a mismatch, `GaReadinessService.flag_regression(item_id/cell_id, observed_value)`:

1. Writes a `regressed` `ga_gate_signoff_events` row with the previous and newly-observed evidence values.
2. Flips the current-state row's `status` to `regressed`.
3. Emits `ga_readiness.item_regressed` through the transactional outbox.
4. A consumer of that event (a small script alongside `infra/ci/notify-slack.sh`) posts to `#deploys` and reopens (or opens, if none exists) a GitHub issue tagged `ga-gate-regression`, assigned to the item's `owner_role` team.
5. `gate-status`'s `ga_approved` immediately becomes `false` again if it had been `true` — a regression detected the night before a launch is not silently absorbed; it blocks exactly as it would have blocked the first time.

Non-automatable items (human-attested ones like §22 item 1, item 5, item 6, §11 clauses a/b/g/h) are **not** subject to automatic regression detection — there is no independent signal to re-check them against — and instead carry a `last_verified_at` timestamp surfaced in the Admin Portal; the team's own process (documented in §16, not enforced in code) is to manually re-confirm any human-attested item whose `last_verified_at` predates a significant subsequent change to that feature.

## 12. Integration Points with Existing Modules

### 12.1 `CI_CD.09` — the primary enforcement wiring

`CI_CD.09`'s `promote-and-deploy-production-backend`/`promote-and-deploy-production-admin` jobs (§3.2 of that file) gain exactly one new step, inserted immediately **before** the `environment: production` declaration so a red gate blocks the job before it even opens for human approval — a rejected gate should never cost a reviewer's attention:

```yaml
# .github/workflows/backend.yml — inside promote-and-deploy-production-backend,
# inserted before the existing `environment:` block, only when this run is GA-labeled
  jobs:
    promote-and-deploy-production-backend:
      if: >
        github.ref == 'refs/heads/main' &&
        (startsWith(github.ref_name, 'refs/tags/v') && contains(github.ref_name, '-ga') ||
         github.event.inputs.release_type == 'ga')
      steps:
        - id: verify-ga-gate
          name: Verify GA Readiness Gate (only for GA-labeled releases)
          if: contains(github.ref_name, '-ga') || github.event.inputs.release_type == 'ga'
          run: ./infra/ci/verify-ga-gate.sh
          env:
            GA_GATE_API_BASE_URL: ${{ vars.GA_GATE_API_BASE_URL }}
            GA_GATE_CI_TOKEN: ${{ secrets.GA_GATE_CI_TOKEN }}
      environment:
        name: production
        # unchanged from CI_CD.09 — the human-approval stage still exists,
        # this step only runs BEFORE it, never replaces it
```

Ordinary, non-GA-labeled production promotions (the routine continuous-delivery deploys that happen throughout Phases 4–11 as features ship) are **untouched** — the `if` condition on `verify-ga-gate` only activates for a release explicitly tagged `-ga` (e.g. `v1.0.0-ga`) or dispatched with `release_type=ga`. This file's gate is specifically the *launch* gate, not a gate on every deploy — matching the objective's framing ("final go/no-go gate for GA launch," not "gate on every commit").

`resolve-promotion-artifact.sh` (`CI_CD.09` §3.3) and `verify-ga-gate.sh` are independent, sequential pre-checks — a GA-labeled release must pass both the ordinary artifact-integrity check every promotion requires and this file's readiness gate.

### 12.2 Phase 11 blue-green/canary strategy — the same hook, documented in advance

`Phase11_CICD_Deployment.Infra.01-blue-green-canary-deployment-strategy.md` (not yet authored at the time of this file) will replace `CI_CD.09`'s single-shot cutover with a staged canary rollout, but whichever mechanism is live at the moment GA actually ships, the same rule applies: **the author of that file must insert an identical `verify-ga-gate.sh` pre-check, gated on the identical GA-tag/`release_type=ga` condition, before its own canary-promotion job's approval/traffic-shift stage begins.** This file's script and API contract (§6.2) are deliberately deployment-strategy-agnostic — nothing in `verify-ga-gate.sh` assumes single-shot-cutover vs. canary, so Phase 11's author only needs to add the one step, never re-derive the gate logic.

### 12.3 Evidence sources this file reads (never writes to)

| Upstream module | What this file reads |
|---|---|
| Phase 9 `CrossPlatform.01` (architectural-invariant suite) | Latest CI run conclusion, per invariant, for §22 item 13 / §11 clause f evidence |
| Phase 9 `CrossPlatform.02` (coverage-gate enforcement) | Latest coverage percentage per stack/scope, for §22 item 13 / §11 clause c evidence |
| Phase 10 F37 `B-08` (incident-response runbook, tested backup restores) | Whether the tabletop exercise has been executed at least once (a boolean this file surfaces directly in `gate-status` per the Execution Blueprint §13 exit criteria), and the most recent backup-restore-verification job's pass/fail |
| Phase 10 F37 `B-09` (penetration-test finding disposition) | Count of `penetration_test_findings` rows still open at `critical`/`high` severity — a non-zero count is itself a blocking `gate-status` condition independent of any single DoD item, since an open critical finding is a launch blocker regardless of which feature it traces to |
| Phase 11 `Infra.01` deploy-rollback validation (once authored) | Whether the DR restore drill has been executed against RPO/RTO targets — feeds Assumed Requirement #7 (§18) |
| F37 security baseline (`B-01`–`B-07`, Phase 2) | Confirmed built per §0.5; this file does not re-verify these, but their existence is a prerequisite the Phase 12 exit criteria assumes and this file's `blocking_items` would surface a gap if, e.g., the architectural-invariant suite (which includes B-03's/B-04's/B-06's tests) reports a failure |
| E30 `B-05` / F35 `B-05` (AI safety evaluation harness) | `critical_findings_count` for the AI layer — a non-zero count blocks `gate-status` the same way an open pentest finding does, since F35/E30's own release-gate logic already treats this as absolute regardless of what this file additionally does |
| E29/E30 content publish-state API | Automatable partial evidence for §22 item 9 / §11 clause e (scholar + child-safety approval wired into publish) |
| E28 RBAC | Source of the admin role/permission model this file's five governance roles are additively layered onto (§7, §9.1) |

## 13. Development Steps in Correct Implementation Order

1. **Confirm `CI_CD.09` exists and is deployed** — this file's §12.1 diff cannot be written against a file that does not yet exist in the repository's actual `.github/workflows/`.
2. **Write the Alembic migration** (§5, §8) — all six tables, the append-only DB-role grant restriction on `ga_gate_signoff_events` (reusing F37 `B-08`'s existing mechanism), and the seed data for the 22 `ga_gate_items` rows (§9.1/§9.2 tables) and 10 `ga_gate_assumed_requirements` rows (§18).
3. **Implement `GaReadinessService`** (§4, §9–§11) — role checks, two-person rule, evidence re-validation stubs (real evidence-source integration comes next), the state machine, `compute_aggregate_state()`.
4. **Wire evidence re-validation** against Phase 9's coverage-gate/architectural-invariant CI results and F37 `B-09`'s `penetration_test_findings` table (§3.4, §12.3) — the parts of §9.3 rule 5 that are genuinely automatable; leave the remaining evidence sources (F37 `B-08` tabletop flag, E30/F35 evaluation-harness count) as explicit follow-up items if those upstream files are not yet implemented, tracked as their own `blocking_items` entries rather than silently skipped.
5. **Implement `api.py`** (§6.1, §6.2) with RBAC dependency injection extending E28's role table (§7, §9.1).
6. **Extend E28's admin role migration** to add the five governance roles' permission scopes and the `executive_sponsor` flag (§7, §9.3).
7. **Build the Admin Portal `ga-readiness` feature module** (§5) — matrix table, banner, exceptions panel, audit-log view.
8. **Write `infra/ci/verify-ga-gate.sh`** and provision the `ga_readiness:gate_status_read`-scoped service-account token as a `production`-environment GitHub secret (§7, §9.3 rule 7).
9. **Apply the `CI_CD.09` diff** (§12.1) on a feature branch of that workflow file; confirm the `if` condition correctly no-ops on an ordinary (non-GA-tagged) promotion before testing the GA-tagged path.
10. **Implement `detect_regressions`** (§11.3) and its Slack/GitHub-issue notification consumer.
11. **Populate the seed data's owner-role assignments into the actual named individuals/GitHub-team mappings** (§16) — an operational, not code, step, but a hard prerequisite before any real sign-off can occur.
12. **Run the dry-run described in §14** against the corpus's actual current state and confirm the reported output matches the expected values there — this is the acceptance test for this file's own Definition of Done (§17).
13. **Document the exception process and the two-holder-per-role staffing requirement** in `infra/ci/README.md`, alongside `CI_CD.09`'s existing rollback/reviewer documentation (consistent placement, one operational reference doc).
14. **Leave the gate itself in `NOT_STARTED`/`IN_PROGRESS` state** — do not pre-populate sign-offs for features that have not actually been verified; the entire point of this mechanism is that its state reflects reality, discovered incrementally as Phases 4–11 genuinely complete.

## 14. Testing Strategy and Acceptance Criteria

### 14.1 Unit and integration tests (owned by this file, standard for the `ga_readiness` context)

- `GaReadinessService` unit tests: role-mismatch rejection, same-proposer-as-approver rejection, evidence-mismatch rejection, correct state-machine transitions and rejected illegal transitions (e.g. `not_started → signed_off` directly, skipping `in_review`, must fail), `compute_aggregate_state()` correctness across representative fixture combinations.
- Integration tests (Testcontainers, per the existing backend pattern): the append-only DB role genuinely cannot `UPDATE`/`DELETE` `ga_gate_signoff_events` — asserted by attempting exactly that as the runtime role and asserting a permissions-denied database error, not just an application-level check.
- `verify-ga-gate.sh` tested against a mocked `gate-status` response for both `ga_approved: true` (exit 0) and `false` (exit non-zero, with `blocking_items` printed to the job log) and against a simulated timeout/5xx (exit non-zero, fail-closed per §10).
- Admin Portal component tests: propose/approve buttons correctly disabled for an admin lacking the required role (UX layer), and a Playwright E2E test that a role-mismatched API call is rejected `403` even when attempted directly against the endpoint, bypassing the UI — proving the enforcement is server-side, not merely a hidden button.

### 14.2 Acceptance criterion — a dry run against the corpus's actual current state

Per this file's own Definition of Done (§17), the gate must be dry-run once against the project's real current status and its reported output checked against the known-correct answer, using `NoorHeroes_Consolidated_Execution_Blueprint.md` §0.5 as ground truth. Running `GET /v1/admin/ga-readiness/summary` and `gate-status` against a database seeded per §13 step 2, with zero sign-offs yet recorded (a genuinely fresh gate, since this mechanism is itself new), correctly produces:

**Org-level items (22 total: 13 + 9) — expected dry-run state: all 22 report `not_started`.** This is the *correct* answer, not a bug: the tracking mechanism has just been built, and no domain owner has recorded a sign-off through it yet, regardless of how much underlying work (e.g., the confirmed-built Phase 2/3 foundation) already exists. The gate's job is to report recorded attestations, not to infer completeness from other systems it doesn't yet integrate with — this is precisely why §13 step 11 (mapping real people to roles) and the ongoing team practice of actually using the gate are necessary follow-through, not an automatic side effect of this file merely existing.

**Feature-DoD matrix (37 × 13 = 481 possible v6-§22 cells) — expected dry-run state: 0 of 481 populated.** Correct for the same reason — no feature has yet had its work run through this specific tracking mechanism, independent of each feature's own PRD/blueprint documentation already existing in the corpus.

**Assumed Requirements (10 total) — expected dry-run state: all 10 report `not_decided`.** Correct — §18 lists the 10 items exactly as the source document leaves them (inferred defaults, not yet a team decision), and seeding the row is not the same as deciding it.

**Cross-phase evidence signals — the one place the dry run legitimately differs from "everything blank," because these read live upstream state rather than requiring a human to have used this gate at all:**

| Signal | Dry-run result (per §0.5) | Why |
|---|---|---|
| Phase 9 architectural-invariant suite CI status | **Not found / gate reports this signal unavailable** | Phase 9 is a confirmed total gap (§0.5) — no CI job exists yet to query |
| Phase 9 coverage-gate CI status | **Not found / unavailable** | Same — Phase 9 not yet built |
| F37 `B-08` tabletop-exercise-executed flag | **`false`** (explicitly, since F37 `B-08` itself, while specified, has an unconfirmed implementation status per §0.5, and the roadmap's own Phase 12 exit criteria requires the tabletop to have "actually been run once (not just documented)") | Matches the Execution Blueprint §13's explicit exit-criteria language |
| F37 `B-09` open-critical `penetration_test_findings` count | **Not found / unavailable** | Phase 10 not yet reached |
| E30/F35 evaluation-harness `critical_findings_count` | **Not found / unavailable** | Phase 8's AI layer is specified but this file cannot assume its runtime state without Phase 8 actually deployed |

**`gate-status.ga_approved`: `false`.** Correctly and unambiguously — every org-level item, every feature cell, and every Assumed Requirement is unresolved, so the aggregate state (§11.2) is `NOT_STARTED`, and `ga_approved` is only ever `true` at `GA_APPROVED`. A dry run that reported anything other than "not approved" against a project this far from Phase 12 completion would itself be evidence of a broken gate.

This dry-run output — correctly reporting a fully-red gate against a project that has real, substantial completed work (Phases 0/2/3) but has not yet run that work through this specific new tracking mechanism, and correctly distinguishing "not yet recorded" from "found and failing" for the cross-phase evidence signals — **is** this file's acceptance test, not a hypothetical.

## 15. Production-Readiness Considerations

This file's entire subject is production readiness, so the considerations below are about the readiness of the *gate itself*, not a secondary concern to some other production system:

- **The gate must not become a bottleneck that trains people to bypass it.** The two-person rule (§9.3) and the exception path (§10) are calibrated to be usable under real launch-week time pressure — an exception with a clear justification/mitigation/expiry takes one Admin Portal form submission plus one Executive Sponsor click, not a multi-week process, precisely so a genuinely-blocked-but-low-risk item does not create pressure to weaken the gate's enforcement instead.
- **The gate must survive its own infrastructure failing.** §10's fail-closed behavior on a `gate-status` outage, and the fact that `GaReadinessService` runs on the same backend infrastructure already hardened by every other Phase 2/9/10 investment (not a separate, less-tested service), means the gate does not introduce a new single point of failure beyond what the rest of the production backend already represents.
- **The gate's own audit trail must itself survive an incident.** `ga_gate_signoff_events` (§8.6) lives in the same primary database covered by F37 `B-08`'s backup-restore verification — a DR event that recovers the production database recovers the sign-off history with it, so a post-incident audit of "did we actually check X before launch" remains answerable.
- **Staffing is a real prerequisite, not a footnote.** §10's "at least two holders per governance role" requirement and §13 step 11's "map roles to actual named individuals" are called out explicitly because a gate that cannot mathematically be satisfied (a single-person role) is worse than no gate — it either blocks forever or forces someone to work around it, and either failure mode should be caught during this file's own rollout, not discovered during launch week.
- **The gate is versioned with the checklist it enforces.** If `v6_22` or `fdp_11`'s items are ever revised, that is a new migration adding/retiring `ga_gate_items` rows with a recorded `superseded_by`/`superseded_at`, never a silent edit to an existing row's `item_text` — preserving the historical accuracy of what was actually checked for a launch that already happened.

## 16. Dependencies/Prerequisites

- **Phases 0–11 must exist as specified elsewhere in this corpus** — this file cannot itself close any of their gaps; it can only report on them. Most materially: `CI_CD.09` must exist for §12.1's diff to apply against a real file; F37 `B-08`/`B-09` and Phase 9's two `CrossPlatform` files supply the automatable evidence §12.3 depends on — until they exist, `gate-status` correctly reports those specific signals as unavailable (§14.2), which is itself acceptable (a true "I don't know yet," not a false pass).
- **E28's RBAC/maker-checker infrastructure** must exist for this file's role-authorization and Admin Portal integration to have somewhere to attach (§7, §9.1) — confirmed built per §0.5.
- **Named individuals mapped to the five governance roles**, with at least two people per role (§10, §13 step 11) — an organizational prerequisite, not a code dependency, but a hard blocker on ever reaching `GA_APPROVED` regardless of how complete the code is.
- **A decision from the team on `Repo.03`'s GA-tag convention** (this file assumes `v*-ga` git tags or a `release_type=ga` workflow-dispatch input, §12.1) — if `Repo.03`'s eventual implementation uses a different tagging scheme, this file's `if` condition must be updated to match, since the tag/label is the sole signal distinguishing a GA-labeled release from routine continuous delivery.

## 17. Definition of Done (for this file specifically)

This file — the gate-tracking mechanism itself — is done when:

1. All six tables (§8) exist via a merged Alembic migration, including the append-only DB-role restriction on `ga_gate_signoff_events`, verified by the integration test in §14.1 that a genuine `UPDATE` attempt against that table is rejected at the database level.
2. `GaReadinessService` enforces every rule in §9.3 (role match, two-person rule, no-self-elevation, evidence re-validation, executive-sponsor-gated exceptions, transactional audit writes), each covered by a passing unit test named in §14.1.
3. The full admin API (§6.1) and the read-only machine API (§6.2) are implemented, documented in the OpenAPI schema, and the Admin/CI generated clients regenerated — satisfying, reflexively, this same file's own §11 clause d.
4. The Admin Portal `ga-readiness` feature module (§5) renders the org-level checklist, the 37×13 and 37×9 matrices, the Assumed Requirements log, the exceptions panel, and the approval-banner, RBAC-gated per §9.
5. `CI_CD.09`'s `promote-and-deploy-production-*` jobs carry the §12.1 diff, verified to correctly no-op on a non-GA-tagged test promotion and to correctly block (in a staging rehearsal, against a deliberately red gate) a GA-tagged one.
6. `detect_regressions` (§11.3) is deployed on its scheduled cadence and has been manually triggered once against a fixture where a previously-signed-off item's underlying evidence was deliberately altered, confirmed to correctly flip that item to `regressed` and emit the expected notification.
7. **The dry-run in §14.2 has actually been executed once against the real, current state of the repository** (not a fixture) and its output matches the expected values documented there — the task brief's own explicit requirement, and the single most important acceptance check for this file, since it proves the gate reports the true state of an in-progress project rather than an idealized one.
8. `infra/ci/README.md` documents the exception process, the two-holder-per-role staffing requirement, and how to read `gate-status`'s `blocking_items` output during an actual launch rehearsal.

## 18. Assumptions or Decisions the Coding Agent Must Follow — Reconciling v6 §23's Assumed Requirements

`NoorHeroes_Consolidated_Blueprint_v6.md` §23.2 indexes 10 items the source document left as inferred defaults rather than explicit stakeholder decisions. Per this file's own objective (`NoorHeroes_Consolidated_Execution_Blueprint.md` §13: "every 'Assumed Requirement' flagged in ... §23 has been confirmed or explicitly re-decided by the team"), **none of the 10 may be silently carried forward into a GA launch** — each is seeded as a `ga_gate_assumed_requirements` row (§8.4) that must reach `confirmed` or `re_decided` before `GA_APPROVED` is reachable (§11.2). The coding agent implementing this file must seed exactly these 10 rows, with the `owner_role` assignments below, and must not resolve any of them itself — resolving them is the team's decision this gate exists to force, not a default this file should quietly pick:

| # | Assumed Requirement (v6 §23.2) | v6 ref | Owner role for the decision |
|---|---|---|---|
| 1 | Cloudflare R2/CDN as the storage/CDN vendor (source specified only generic "private object storage" + "CDN") | §2.5 | Engineering Lead |
| 2 | Email provider for OTP fallback and transactional email (vendor unnamed in source) | §3.5 | Engineering Lead |
| 3 | Analytics/data-warehouse vendor (unnamed in source) | §3.5 | Product |
| 4 | Kubernetes deferred to the Scale phase rather than launch | §2.9 / §14.3 | Engineering Lead |
| 5 | Specific performance latency targets (home-feed p95 < 500ms, media-start p95 < 2s) | §14.1 | Engineering Lead |
| 6 | Core API availability SLO (99.9% monthly) | §14.5 | Engineering Lead, co-decided with Product (an SLO is a business commitment as much as a technical one) |
| 7 | RPO/RTO disaster-recovery targets (recommended ≤1hr / ≤4hr in source, explicitly unvalidated against real business risk tolerance per v6 §23.1) | §14.7 | Security Lead |
| 8 | Numeric testing-coverage targets (≥80% backend domain, ≥95% critical-path, 100% mobile onboarding/parent-gate UI — the same figures Phase 9's `CrossPlatform.02` enforces) | §17.4 | Engineering Lead |
| 9 | KMS/secrets-manager vendor choice (unnamed in source) | §13.3 | Security Lead |
| 10 | Directional, non-committed cost-optimization guidance (no budget figures exist in the source document) | §21 | Product |

Two further items from v6 §23.1/§23.6, not separately numbered in §23.2's index but load-bearing enough to seed as their own rows rather than leaving implicit:

| # | Item | v6 ref | Owner role |
|---|---|---|---|
| 11 | Specific numeric rate limits per endpoint/role (only the rate-limiting *mechanism* is specified in the source, not thresholds) | §3.4/§3.5 of Final_Development_Prompt; v6 §23.1 | Security Lead |
| 12 | The explicit stakeholder-approval step v6 §23.6 names for "specific third-party vendor selections (email, analytics/warehouse, secrets manager)" — tracked here as a single confirming decision that items 2/3/9 above were each actually brought to and approved by the relevant budget/procurement stakeholder, not just decided unilaterally by engineering | §23.6 | Product |

This brings the seeded total to **12 rows**, not 10 — the coding agent must not truncate to exactly 10 merely because §23.2's own index numbers 10; items 11–12 are genuine, load-bearing "Assumed Requirement"-class gaps found elsewhere in the same §23, and omitting them would leave a silent default in place, which is precisely what this file's objective forbids. Where this document's own earlier sections (§7, §12.3) refer to "the 10 Assumed Requirements," that phrasing follows §23.2's own numbering for readability; the authoritative seed count implementing this section is 12.

## 19. AI Agent Development Prompt

You are implementing `Development_Blueprints.Phase12_Production_Readiness.CrossPlatform.01-definition-of-done-ga-gate-checklist.md` for the NoorHeroes monorepo (FastAPI backend, Next.js Admin Portal, KMP mobile app — mobile is **not** touched by this file).

**What you are building:** a new backend bounded context, `ga_readiness`, that tracks and enforces sign-off on (a) the 13-item Definition of Done from `NoorHeroes_Consolidated_Blueprint_v6.md` §22, for every one of the 37 shipped features (A.1–F.37); (b) the 9-clause per-feature process checklist from `NoorHeroes_Final_Development_Prompt.md` §11; and (c) the 12 "Assumed Requirement" decisions listed in §18 above. It also builds the Admin Portal UI that reflects that state, and wires a read-only gate check into the existing production-promotion pipeline (`CI_CD.09`).

**What you are NOT building:** any of the underlying 13/9/12 items themselves. Do not write scholar-review workflows, accessibility fixes, consent logic, or test coverage to satisfy any checklist item — this file only records whether those already-specified pieces of work (owned by every other Development Blueprint in this corpus) have been done and signed off by an authorized role-holder. Do not modify any A–F feature module's own code. Do not redesign `CI_CD.09`'s production-deploy mechanism beyond the one pre-check step specified in §12.1 — everything else in that file (the `resolve-promotion-artifact.sh` flow, the migration/cutover/health-check sequence, Slack notifications) is out of scope and must be left untouched. Do not build Phase 11's blue-green/canary strategy — only leave the documented hook point (§12.2) for whoever authors that file later.

**Hard requirements, in implementation order (full detail in §13 above):**

1. Alembic migration creating exactly the six tables in §8, with `ga_gate_signoff_events` restricted at the database-role level to `INSERT`/`SELECT` only (reuse the exact mechanism F37 `B-08` already establishes for append-only audit logs — do not invent a second one), seeded with exactly 22 `ga_gate_items` rows (13 `v6_22` + 9 `fdp_11`, item text and `owner_role` exactly as tabulated in §9.1/§9.2) and exactly 12 `ga_gate_assumed_requirements` rows (exactly as tabulated in §18 — not 10, see §18's closing paragraph for why).
2. `GaReadinessService(BaseService)` as the sole enforcer of every rule in §9.3: role-match on propose/approve, two-person rule (DB CHECK constraint **and** service-layer check, not just one), evidence re-validation for `is_automatable=true` items against Phase 9's coverage-gate/architectural-invariant CI results and F37 `B-09`'s `penetration_test_findings` table (integrate what upstream files already exist; for anything not yet implemented, `gate-status` must report that signal as explicitly unavailable, never silently pass it), the state machine in §11.1, and `compute_aggregate_state()` per §11.2.
3. The admin API (§6.1) and the read-only `GET /v1/admin/ga-readiness/gate-status` machine API (§6.2), exactly matching the response shape shown there. Regenerate the OpenAPI schema and the Admin generated TypeScript client — do not hand-write a parallel client.
4. Extend E28's existing RBAC role table additively (five new governance-role permission scopes plus an `executive_sponsor` flag) — do not redesign E28's RBAC model.
5. The Admin Portal `ga-readiness` feature module (§5) — matrix tables, banner, exceptions panel, audit-log view — built on the project's existing `src/features/` conventions, TanStack Query, and `RequirePermission`/`useElevatedSession` primitives already established elsewhere in the Admin Portal. The UI must never itself decide authorization; it only reflects and disables based on what the backend API returns/rejects.
6. `infra/ci/verify-ga-gate.sh` and the exact `CI_CD.09` diff in §12.1 — gated so it only activates for a GA-tagged release (`v*-ga` tag or `release_type=ga` dispatch input) and fails closed on any non-200/timeout response, never fails open.
7. `detect_regressions` scheduled task per §11.3, with its Slack + GitHub-issue-reopen notification consumer.

**Testing instruction:** write the unit/integration/E2E tests enumerated in §14.1 — in particular, the database-level test proving `ga_gate_signoff_events` genuinely rejects `UPDATE`/`DELETE` at the DB-role level (an application-level check alone does not satisfy this), and the Playwright test proving a role-mismatched sign-off is rejected `403` when called directly against the API, bypassing the Admin Portal UI. Then, **as this file's own acceptance test**, run the dry-run described in §14.2 against the actual current state of the real repository (not a test fixture) and confirm the output matches §14.2's expected values exactly: all 22 org items `not_started`, 0 of 481 feature-DoD cells populated, all 12 Assumed Requirements `not_decided`, every cross-phase evidence signal not yet implemented in the repo reported as explicitly unavailable (never a false pass), and `gate-status.ga_approved: false`. Do not consider this file complete until that specific dry-run has actually been executed and its real output recorded — an untested claim that the dry-run "would" produce this output does not satisfy §17 item 7.
