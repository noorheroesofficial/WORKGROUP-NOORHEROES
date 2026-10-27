# SAM + NoorHeroes Engineering Guide & Reference Manual

> **Comprehensive operational guide with concrete, multi-platform examples** for executing AI-driven engineering with **SAM (Smart Agent Manager)** inside the **WORKGROUP-NOORHEROES** workspace alongside Google Antigravity.

---

## ⚡ Quick Command Index & Immediate Cheat Sheet

Type these exact slash commands or prompts into the Antigravity chat window:

| Command | Category | Best Used For | Instant Copy-Paste Example |
| :--- | :--- | :--- | :--- |
| `/sam-plan` | Workflow | Decompose a PRD into epics & stories in `sdocs/` | `/sam-plan PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md` |
| `/sam-build-tdd` | Workflow | Build a story via RED-GREEN-REFACTOR TDD | `/sam-build-tdd sdocs/stories/STORY-001-record-reward-event.md` |
| `/sam-plan-n-build` | Workflow | Full autonomous PRD-to-code pipeline | `/sam-plan-n-build PRD_Documents/Child App Supporting (13-18)/Feature_B18_Islamic_Facts_Module.md` |
| `/sam-extend` | Workflow | Add endpoints/features without rewriting done work | `/sam-extend sdocs/addenda/ADDENDUM-001-dua-analytics.md` |
| `/sam-quick-prd` | Workflow | Fast draft PRD with explicit assumptions | `/sam-quick-prd "WebSocket connection health monitor for Backend"` |
| `/sam-scope` | Workflow | Full interactive requirements discovery | `/sam-scope "Voice recognition for Arabic tajweed recitation"` |
| `/sam-orchestrator` | Persona | Pipeline status, resume, and gatekeeping | `/sam-orchestrator "Report status of all stories in sdocs/stories/"` |
| `/sam-atlas` | Persona | Architecture, DB schemas, API seams | `/sam-atlas "Design PostgreSQL schema for reward_ledger in NoorHeroes-Backend"` |
| `/sam-titan` | Persona | Write failing tests (RED phase) | `/sam-titan "Write failing pytest tests for /api/v1/rewards/events"` |
| `/sam-dyna` | Persona | Implement minimal passing code (GREEN phase) | `/sam-dyna "Implement minimal FastAPI router for /api/v1/rewards/events"` |
| `/sam-argus` | Persona | Code review & refactoring (REFACTOR phase) | `/sam-argus "Review NoorHeroes-Backend rewards service for clean architecture"` |
| `/sam-sentinel` | Persona | Security audit, BOLA/IDOR, secrets | `/sam-sentinel "Scan rewards claim endpoint for IDOR vulnerabilities"` |
| `/sam-cosmo` | Persona | CSS, design tokens & responsive UI | `/sam-cosmo "Review noorheroes-admin RewardCard.tsx for Tailwind tokens"` |
| `/sam-aria` | Persona | WCAG 2.1 AA accessibility & keyboard nav | `/sam-aria "Audit noorheroes-admin ParentPinModal.tsx for focus traps"` |
| `/sam-iris` | Persona | UX flows, state transitions, modals | `/sam-iris "Review rewards claim celebration modal flow"` |
| `/sam-quill` | Persona | Requirements & acceptance criteria | `/sam-quill "Clarify streak-freeze rules in Feature_A11_Rewards_System.md"` |
| `/sam-sage` | Persona | API documentation & ADR generation | `/sam-sage "Generate OpenAPI runbook for Rewards V1 in Backend-Agent/"` |
| `/sam-lens` | Persona | Capture visual proof & test logs | `/sam-lens "Record test logs for STORY-001 into sdocs/evidence/STORY-001/"` |
| `/sam-upkeep` | Persona | Dependency audits & CVE checks | `/sam-upkeep "Audit Python dependencies in NoorHeroes-Backend/.venv"` |

---

## 📑 Table of Contents
1. [Architecture & Execution Hierarchy](#1-architecture--execution-hierarchy)
   - [Workgroup Rule Architecture & Deduplication](#workgroup-rule-architecture--deduplication)
2. [Multi-Project Boundaries](#2-multi-project-boundaries)
3. [Available SAM Commands & Skills Reference (With Concrete Examples)](#3-available-sam-commands--skills-reference-with-concrete-examples)
   - [A. All 6 Workflow Commands with Multi-Platform Examples](#a-workflow-commands)
   - [B. All 13 Specialized Agent Personas with Concrete Invocations](#b-specialized-agent-personas-reference-with-invocations)
4. [End-to-End Walkthrough: Feature A.11 Rewards System](#4-end-to-end-walkthrough-feature-a11-rewards-system)
5. [Technology-Specific Code Patterns & Guidelines](#5-technology-specific-code-patterns--guidelines)
   - [A. Python / FastAPI (Backend)](#a-python--fastapi-noorheroes-backend)
   - [B. Kotlin Multiplatform / CMP (Mobile)](#b-kotlin-multiplatform--cmp-noorheroes)
   - [C. Next.js 16 / React 19 (Web Admin)](#c-web-admin-portal-noorheroes-admin)
   - [D. Next.js 15 / Tailwind v4 (Public Website)](#d-public-website-noorheroes-website)
6. [Review Gates & Verification Examples (Security, CSS, Accessibility)](#6-review-gates--verification-examples)
7. [Artifact Organization in sdocs/](#7-artifact-organization-in-sdocs)
8. [Common Troubleshooting & Error Recovery](#8-common-troubleshooting--error-recovery)
9. [Common Commands Cheat Sheet & Real Scenarios (Recipe Book)](#9-common-commands-cheat-sheet--real-scenarios-recipe-book)

---

## 1. Architecture & Execution Hierarchy

SAM operates strictly as an **autonomous engineering execution engine**. It translates authoritative requirements and blueprints into concrete contracts, epics, stories, and tested code through a disciplined TDD workflow.

```text
Authoritative PRD (PRD_Documents/)
               ↓
Authoritative Blueprint (Development_Blueprints/)
               ↓
Reference Visuals (Screens/)
               ↓
Live Architectural Rules (DEVELOPMENT-RULES.md & Tech Manuals)
               ↓
SAM Planning (/sam-plan)
               ↓
Contracts & Stories (sdocs/contracts/, sdocs/stories/)
               ↓
TDD Implementation (/sam-build-tdd)
  ├── RED: Titan writes failing test
  ├── GREEN: Dyna implements minimal solution
  └── REFACTOR: Argus & Sentinel review code & security
               ↓
Verification & Evidence (sdocs/evidence/)
```

### Precedence Table

| Priority | Source | Role | Can SAM Modify? |
| :--- | :--- | :--- | :--- |
| **1 (Highest)** | `PRD_Documents/` | Authoritative product requirements & business logic | ❌ **STRICTLY READ-ONLY** |
| **2** | `Development_Blueprints/` | Authoritative module boundaries & implementation sequence | ❌ **STRICTLY READ-ONLY** |
| **3** | `Screens/` | UI design references & visual truth | ❌ **STRICTLY READ-ONLY** |
| **4** | `NoorHeroes_Consolidated_Execution_Blueprint.md` | Global project roadmap & sequence index | ❌ **STRICTLY READ-ONLY** |
| **5** | `DEVELOPMENT-RULES.md` & `PROJECT-CONTEXT.md` | Workgroup operating invariants & live architecture context | ❌ **READ-ONLY** |
| **6** | Architecture Manuals (`MASTER-README.md`, etc.) | Stack-specific guidelines for Backend, KMP, Admin, Web | ❌ **READ-ONLY** |
| **7** | `Admin-Agent/` & `Backend-Agent/` | Domain ADRs, operational runbooks, and event contracts | ❌ **PRESERVED** |
| **8 (Lowest)** | SAM Execution Artifacts (`sdocs/`) | Generated epics, stories, contracts, logs, test evidence | ✅ **SAM MANAGED** |

### Workgroup Rule Architecture & Deduplication
- **Authoritative Rule File**: [`AGENTS.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/AGENTS.md) at the workspace root is the single source of truth for agent behavior and execution invariants across all projects.
- **Antigravity Rule Ingestion**: Antigravity automatically discovers and enforces [`AGENTS.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/AGENTS.md) across all subdirectories and subagent sessions.
- **Deduplication Audit**: Redundant duplicate rule files (such as `.agent/rules/noorheroes-sam-governance.md`) have been audited and removed to ensure clean, single-point governance and prevent duplicate rule token overhead.

---

## 2. Multi-Project Boundaries

WORKGROUP-NOORHEROES contains 4 independent codebases. Never cross boundaries or mix build tools:

| Project | Location | Technology Stack | Test Framework | Live Authority Doc |
| :--- | :--- | :--- | :--- | :--- |
| **Mobile App** | [`NoorHeroes/`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes) | Kotlin Multiplatform (KMP), Compose Multiplatform (CMP), SQLDelight, Ktor | Kotlin Test / Kermit | [`NoorHeroes/README.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes/README.md) + 13 `core/` manuals |
| **Backend API** | [`NoorHeroes-Backend/`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend) | Python, FastAPI, PostgreSQL, SQLAlchemy, Alembic, Redis | pytest | [`NoorHeroes-Backend/MASTER-README.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/MASTER-README.md) & [`FAST-API-INSTRUCTIONS.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/FAST-API-INSTRUCTIONS.md) |
| **Web Admin** | [`noorheroes-admin/`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/noorheroes-admin) | Next.js 16, React 19, TypeScript, Tailwind CSS | Vitest & Playwright | [`noorheroes-admin/MASTER-README.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/noorheroes-admin/MASTER-README.md) & [`NEXT-JS-INSTRUCTIONS.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/noorheroes-admin/NEXT-JS-INSTRUCTIONS.md) |
| **Public Website** | [`noorheroes-website/`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/noorheroes-website) | Next.js 15, React 19, TypeScript, Tailwind CSS v4, Motion | Next test / Vitest | [`noorheroes-website/README.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/noorheroes-website/README.md) & [`WEBSITE-INSTRUCTIONS.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/noorheroes-website/WEBSITE-INSTRUCTIONS.md) |

---

## 3. Available SAM Commands & Skills Reference (With Concrete Examples)

All 19 skills are installed and natively discoverable in Antigravity. Below are detailed usage instructions, syntax, and real NoorHeroes examples for every skill.

### A. Workflow Commands

#### 1. `/sam-plan <prd-path> [--force]`
Decomposes an existing authoritative PRD into system contracts, epics, and implementation stories inside `sdocs/`. Does NOT write production code.

- **Syntax**: `/sam-plan <path-to-prd> [--force]`
- **Flag `--force`**: Overwrites existing `sdocs/epics/`, `sdocs/stories/`, and `sdocs/contracts/` if re-planning.

**Concrete Real-World Examples:**
```bash
# Example 1: Planning Feature A.11 (Rewards System) - Core Economy
/sam-plan PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md

# Example 2: Planning Feature A.6 (Dua Learning) - Audio & Gamification
/sam-plan PRD_Documents/Child App (1-12)/Feature_A6_Dua_Learning.md

# Example 3: Planning Feature C.23 (Parental Controls) - PIN & Time Limits
/sam-plan PRD_Documents/Parent Area In-App (19-26)/Feature_C23_Parental_Controls.md

# Example 4: Planning Feature E.28 (Admin Auth & RBAC) - Security & Permissions
/sam-plan PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC.md

# Example 5: Re-planning with overwrite flag
/sam-plan PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md --force
```

---

#### 2. `/sam-build-tdd <story-path>`
Executes the strict TDD implementation cycle (RED → GREEN → REFACTOR) for a single story file. Enforces quality, security, and styling gates.

- **Syntax**: `/sam-build-tdd <path-to-story-file>`
- **Prerequisite**: Story must exist with `status: ready` (or `status: blocked` when retrying).

**Concrete Real-World Examples:**
```bash
# Example 1: Implementing a Backend Python/FastAPI Story
/sam-build-tdd sdocs/stories/STORY-001-record-reward-event.md

# Example 2: Implementing a Mobile KMP / SQLDelight Story
/sam-build-tdd sdocs/stories/STORY-002-cache-offline-rewards.md

# Example 3: Implementing a Web Admin React 19 / Vitest Story
/sam-build-tdd sdocs/stories/STORY-003-xp-rule-editor-form.md

# Example 4: Implementing an Integration Seam Story
/sam-build-tdd sdocs/stories/STORY-004-rewards-integration.md
```

---

#### 3. `/sam-plan-n-build <prd-path> [--force]`
Composes the entire pipeline: validates PRD, decomposes into epics and stories, iteratively runs TDD for every story until all are `done`, and produces technical documentation.

- **Syntax**: `/sam-plan-n-build <path-to-prd> [--force]`

**Concrete Real-World Examples:**
```bash
# Example 1: Autonomous implementation of Islamic Facts Module (Feature B.18)
/sam-plan-n-build PRD_Documents/Child App Supporting (13-18)/Feature_B18_Islamic_Facts_Module.md

# Example 2: Autonomous implementation of Ramadan Seasonal Mode (Feature F.36)
/sam-plan-n-build PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Seasonal_Experience.md
```

---

#### 4. `/sam-extend <addendum-path>`
Plans additive features, new fields, or new API routes on top of an existing application without modifying already completed stories or erasing existing `sdocs/`.

- **Syntax**: `/sam-extend <path-to-addendum-markdown>`

**Concrete Real-World Examples:**
```bash
# Example 1: Adding Spaced Repetition Analytics to Dua Learning
/sam-extend sdocs/addenda/ADDENDUM-001-dua-spaced-repetition-analytics.md

# Example 2: Adding Multi-Child Screen Time Aggregation to Parent Reports
/sam-extend sdocs/addenda/ADDENDUM-002-parent-screen-time-aggregation.md
```

---

#### 5. `/sam-quick-prd "<concept-or-prompt>"`
Quickly drafts a valid PRD in one pass with explicit reviewable assumptions. Use this **only** for new internal tools or unspecced utility tasks where no PRD exists in `PRD_Documents/`.

- **Syntax**: `/sam-quick-prd "<prompt-or-notes>"`

**Concrete Real-World Examples:**
```bash
# Example 1: Internal Developer Diagnostics Utility
/sam-quick-prd "Create an internal WebSocket connection health diagnostic endpoint and CLI tool for NoorHeroes-Backend"

# Example 2: Database Migration Integrity Checker
/sam-quick-prd "Create an automated database migration checksum verification script for CI pipeline"
```

---

#### 6. `/sam-scope "<concept-or-prompt>"`
Performs full requirements discovery interview with Iris (UX) and Atlas (Architecture) to produce an authoritative PRD.

- **Syntax**: `/sam-scope "<idea-or-brief>"`

**Concrete Real-World Examples:**
```bash
# Example: Scoping a future Tajweed Audio AI Grading microservice
/sam-scope "Real-time AI audio analysis microservice for validating child Arabic tajweed recitation"
```

---

### B. Specialized Agent Personas Reference (With Invocations)

You can invoke individual SAM agents directly for ad-hoc reviews, architectural guidance, failing tests, or security audits.

#### 1. `/sam-orchestrator` (SAM Master)
- **Role**: Coordinates workflows, tracks story statuses, and reports pipeline health.
- **Example Usage**:
  ```bash
  /sam-orchestrator "Report the progress and status of all stories in sdocs/stories/"
  /sam-orchestrator "Resume execution of EPIC-001 from the first story with status: ready"
  ```

#### 2. `/sam-atlas` (System Architect)
- **Role**: Validates technical design, derives contract seams, and verifies architecture boundaries.
- **Example Usage**:
  ```bash
  # Example 1: Database indexing and concurrency design
  /sam-atlas "Design PostgreSQL index and table partitioning strategy for reward_ledger table in NoorHeroes-Backend"
  
  # Example 2: KMP clean architecture seam design
  /sam-atlas "Verify dependency injection and repository interfaces between core-database and feature-rewards in NoorHeroes"
  ```

#### 3. `/sam-titan` (Test Architect - RED Phase)
- **Role**: Authors comprehensive failing tests before any production code is written.
- **Example Usage**:
  ```bash
  # Example 1: FastAPI Pytest Async tests
  /sam-titan "Write failing pytest integration tests for /api/v1/rewards/claim with child authentication and idempotency"
  
  # Example 2: Next.js Vitest unit tests
  /sam-titan "Write failing Vitest component tests for XpRuleEditor.tsx testing validation errors on negative XP input"
  
  # Example 3: KMP Kotlin Multiplatform tests
  /sam-titan "Write failing Kotlin commonTest unit tests for RewardsStateMachine handling ClaimRewardIntent"
  ```

#### 4. `/sam-dyna` (Core Developer - GREEN Phase)
- **Role**: Implements the minimal, correct code required to turn failing tests green.
- **Example Usage**:
  ```bash
  # Example 1: Python/FastAPI implementation
  /sam-dyna "Implement the RewardsService.record_event method in NoorHeroes-Backend to pass tests/modules/rewards/test_ledger.py"
  
  # Example 2: Next.js React 19 implementation
  /sam-dyna "Implement XpRuleForm component with React Hook Form and Zod to pass tests/features/rewards/xp-rule-form.test.tsx"
  ```

#### 5. `/sam-argus` (Code Reviewer - REFACTOR Phase)
- **Role**: Reviews green code for architectural integrity, clean abstractions, naming, and dead code.
- **Example Usage**:
  ```bash
  /sam-argus "Review NoorHeroes-Backend/src/noorheroes/modules/rewards/service.py for clean architecture and PEP 8 conformity"
  /sam-argus "Review NoorHeroes/feature/feature-rewards for strict MVI state separation and Kermit logging"
  ```

#### 6. `/sam-sentinel` (Security Reviewer)
- **Role**: Audits code for OWASP Top 10, IDOR/BOLA, SQL injection, authentication flaws, and exposed credentials.
- **Example Usage**:
  ```bash
  # Example 1: Audit an API router for IDOR / authorization bypass
  /sam-sentinel "Audit /api/v1/rewards/wallet/{child_id} in NoorHeroes-Backend to verify parent-child family ownership check"
  
  # Example 2: Scan for secret leaks
  /sam-sentinel "Scan recent changes in NoorHeroes-Backend and noorheroes-admin for accidental hardcoded secrets or API tokens"
  ```

#### 7. `/sam-cosmo` (CSS & Styling Reviewer)
- **Role**: Ensures web components strictly conform to design tokens, Tailwind scale, and mobile responsiveness.
- **Example Usage**:
  ```bash
  /sam-cosmo "Review noorheroes-admin/src/features/rewards/components/RewardCard.tsx for Tailwind spacing scale and design tokens"
  /sam-cosmo "Verify mobile responsive layout for noorheroes-website/src/app/page.tsx across sm, md, and lg viewports"
  ```

#### 8. `/sam-aria` (Accessibility Reviewer)
- **Role**: Audits components for WCAG 2.1 AA compliance, keyboard navigation, contrast, and ARIA attributes.
- **Example Usage**:
  ```bash
  /sam-aria "Audit noorheroes-admin/src/features/auth/components/ParentPinModal.tsx for focus traps and screen reader labels"
  /sam-aria "Verify color contrast and tap target sizes on NoorHeroes KMP Compose buttons in RewardsWalletScreen.kt"
  ```

#### 9. `/sam-iris` (UX Designer)
- **Role**: Designs and validates user experience flows, modal states, loading skeletons, and celebration micro-interactions.
- **Example Usage**:
  ```bash
  /sam-iris "Review user interaction flow and empty states for the Rewards Wallet screen against Screens/Child App/Rewards/"
  /sam-iris "Design celebration micro-animation state transitions when a child unlocks an Eid Mubarak badge"
  ```

#### 10. `/sam-quill` (Product Manager)
- **Role**: Refines acceptance criteria, edge-case definitions, and business logic clarity.
- **Example Usage**:
  ```bash
  /sam-quill "Clarify streak-freeze business rules in Feature_A11_Rewards_System.md when a child is traveling across time zones"
  ```

#### 11. `/sam-sage` (Technical Writer)
- **Role**: Authors OpenAPI documentation, architecture decision records (ADRs), and integration runbooks.
- **Example Usage**:
  ```bash
  /sam-sage "Generate OpenAPI endpoint documentation and error catalog for the Rewards V1 API in Backend-Agent/runbooks/"
  ```

#### 12. `/sam-lens` (Evidence & Demo Recorder)
- **Role**: Validates test logs, CLI command outputs, and UI evidence into `sdocs/evidence/`.
- **Example Usage**:
  ```bash
  /sam-lens "Record test execution logs and coverage report for STORY-001 into sdocs/evidence/STORY-001/"
  ```

#### 13. `/sam-upkeep` (Maintenance & Upkeep Specialist)
- **Role**: Inspects package vulnerabilities, outdated lockfiles, and deprecation notices.
- **Example Usage**:
  ```bash
  /sam-upkeep "Audit Python dependencies in NoorHeroes-Backend/.venv and identify any CVEs"
  /sam-upkeep "Check npm dependency updates for noorheroes-admin and noorheroes-website"
  ```

---

## 4. End-to-End Walkthrough: Feature A.11 Rewards System

This concrete walkthrough demonstrates how a feature transitions through SAM from PRD to production-ready code.

### Step 1: Planning Phase (`/sam-plan`)

**User executes in chat:**
```bash
/sam-plan PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md
```

**What SAM does automatically:**
1. Ingests [`Feature_A11_Rewards_System.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Child%20App%20%281-12%29/Feature_A11_Rewards_System.md).
2. Cross-references [`Development_Blueprints/A11_Rewards_System/`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A11_Rewards_System).
3. Inspects UI references in [`Screens/Child App/Rewards/`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Child%20App/Rewards) and [`Screens/Admin Web/`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Admin%20Web).
4. Produces the canonical `sdocs/` structure:
   - `sdocs/architecture-ref.md`
   - `sdocs/contracts/rewards/ledger-event.md`
   - `sdocs/epics/EPIC-001-rewards-core.md`
   - `sdocs/stories/STORY-001-record-reward-event.md`
   - `sdocs/stories/STORY-002-get-rewards-wallet.md`

---

### Step 2: Generated Contract Example (`sdocs/contracts/`)

File: `sdocs/contracts/rewards/ledger-event.md`
```yaml
---
id: rewards.ledger-event
kind: type
title: Append-Only Reward Ledger Event Contract
status: stable
owner_story: STORY-001
version: 1
created: 2026-09-27
---

# Contract: rewards.ledger-event

## Data Schema (Pydantic / TypeScript Aligned)

```python
class RewardType(str, Enum):
    XP = "xp"
    POINTS = "points"
    BADGE = "badge"

class RewardLedgerEntry(BaseModel):
    id: UUID
    child_id: UUID
    reward_type: RewardType
    amount: int = Field(ge=0, description="Earned value, always non-negative")
    source_activity: str = Field(description="e.g. stories, dua, quiz")
    idempotency_key: str = Field(description="Unique key to prevent duplicate awards")
    created_at: datetime
```
```

---

### Step 3: Generated Story Example (`sdocs/stories/`)

File: `sdocs/stories/STORY-001-record-reward-event.md`
```yaml
---
id: STORY-001
epic: EPIC-001
kind: feature
title: Append-only reward event recording with idempotency
status: ready
priority: P0
prd: ../../PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md
depends_on: []
produces: [rewards.ledger-event]
consumes: []
created: 2026-09-27
---

# STORY-001: Append-only reward event recording with idempotency

## Context
Every learning activity emits reward events (XP and Noor Points). The ledger must be append-only and strictly idempotent to prevent duplicate reward grants.

## Acceptance Criteria
- [ ] AC-1: Emitting a reward event inserts a row into `reward_ledger` table with non-negative amount.
- [ ] AC-2: Submitting an identical `idempotency_key` returns the existing record without creating a duplicate row (HTTP 200).
- [ ] AC-3: Update and Delete operations on `reward_ledger` are strictly forbidden at database and ORM level.
```

---

### Step 4: TDD Implementation Phase (`/sam-build-tdd`)

**User executes in chat:**
```bash
/sam-build-tdd sdocs/stories/STORY-001-record-reward-event.md
```

#### Phase A: RED (Titan writes failing test)
Titan creates [`tests/modules/rewards/test_ledger_idempotency.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/tests/modules/rewards/test_ledger_idempotency.py):
```python
import pytest
from uuid import uuid4
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_duplicate_reward_event_is_idempotent(async_client: AsyncClient, auth_headers: dict):
    payload = {
        "child_id": str(uuid4()),
        "reward_type": "xp",
        "amount": 50,
        "source_activity": "quiz_daily",
        "idempotency_key": "daily_quiz_2026_09_27_child_123"
    }
    
    # First call: Created
    resp1 = await async_client.post("/api/v1/rewards/events", json=payload, headers=auth_headers)
    assert resp1.status_code == 201
    
    # Second call with same idempotency key: Returns existing without duplicate
    resp2 = await async_client.post("/api/v1/rewards/events", json=payload, headers=auth_headers)
    assert resp2.status_code == 200
    assert resp2.json()["id"] == resp1.json()["id"]
```
*Titan executes pytest: Test FAILS (router does not exist yet) → Gate RED Passed.*

#### Phase B: GREEN (Dyna writes minimal implementation)
Dyna implements the endpoint in [`src/noorheroes/modules/rewards/router.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/rewards/router.py) and service layer:
```python
@router.post("/events", status_code=status.HTTP_201_CREATED, response_model=RewardLedgerResponse)
async def record_reward_event(
    payload: RewardEventCreate,
    service: RewardsService = Depends(get_rewards_service),
    response: Response = None
):
    entry, is_new = await service.record_event_idempotent(payload)
    if not is_new:
        response.status_code = status.HTTP_200_OK
    return entry
```
*Dyna runs pytest: Test PASSES (2 passed) → Gate GREEN Passed.*

#### Phase C: REFACTOR (Argus + Sentinel Review)
1. **Argus (Code Review)**: Verifies domain boundaries, typing, and docstrings.
2. **Sentinel (Security Review)**: Confirms child ownership verification: child belongs to authenticated parent family account (prevents IDOR).
3. **Story State Transition**: SAM updates story frontmatter:
   ```yaml
   status: done
   ```
4. **Evidence Recorded**: Test execution logs and output saved to `sdocs/evidence/STORY-001/test_run.log`.

---

## 5. Technology-Specific Code Patterns & Guidelines

### A. Python / FastAPI (`NoorHeroes-Backend/`)
Adhere to [`FAST-API-INSTRUCTIONS.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/FAST-API-INSTRUCTIONS.md):
- **Routers**: Thin controllers handling HTTP status codes and dependency injection only.
- **Services**: Pure business logic, async database transactions.
- **Repositories**: Encapsulated SQLAlchemy 2.0 select/insert operations.
- **Testing**: Pytest with `AsyncClient`, factories, and SQLite/PostgreSQL test fixtures.

```python
# Example: Safe Dependency Injection & Error Handling
@router.get("/wallet/{child_id}", response_model=RewardWalletResponse)
async def get_wallet(
    child_id: UUID,
    current_user: User = Depends(get_current_active_user),
    service: RewardsService = Depends(get_rewards_service)
):
    await service.verify_child_access(parent_id=current_user.id, child_id=child_id)
    return await service.get_child_wallet(child_id)
```

---

### B. Kotlin Multiplatform / CMP (`NoorHeroes/`)
Adhere to [`NoorHeroes/README.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes/README.md) and the 13 `core/` manuals:
- **Architecture**: MVI (Model-View-Intent) pattern with immutable state.
- **Logging**: Use Kermit via `core-logger` (never raw `println`).
- **Database**: Use SQLDelight queries defined in `.sq` files.
- **Network**: Ktor Client via `core-network`.

```kotlin
// Example: MVI ViewModel Pattern
class RewardsViewModel(
    private val rewardsRepository: RewardsRepository,
    private val logger: KermitLogger
) : ViewModel() {
    private val _uiState = MutableStateFlow<RewardsUiState>(RewardsUiState.Loading)
    val uiState: StateFlow<RewardsUiState> = _uiState.asStateFlow()

    fun onIntent(intent: RewardsIntent) {
        when (intent) {
            is RewardsIntent.LoadWallet -> loadWallet(intent.childId)
            is RewardsIntent.ClaimMilestone -> claimMilestone(intent.milestoneId)
        }
    }
}
```

---

### C. Web Admin Portal (`noorheroes-admin/`)
Adhere to [`NEXT-JS-INSTRUCTIONS.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/noorheroes-admin/NEXT-JS-INSTRUCTIONS.md):
- **Framework**: Next.js App Router with React 19.
- **Data Fetching**: `@tanstack/react-query` with centralized API client.
- **Forms**: `react-hook-form` + `@hookform/resolvers/zod`.
- **Validation**: Strict Zod schemas matching backend OpenAPI contracts.

```typescript
// Example: React Query Hook with Error Boundary Support
export function useRewardLedger(childId: string) {
  return useQuery({
    queryKey: ['rewards', 'ledger', childId],
    queryFn: () => apiClient.get<RewardLedgerEntry[]>(`/api/v1/admin/rewards/ledger/${childId}`),
    staleTime: 60 * 1000,
  });
}
```

---

### D. Public Website (`noorheroes-website/`)
Adhere to [`WEBSITE-INSTRUCTIONS.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/noorheroes-website/WEBSITE-INSTRUCTIONS.md):
- **Framework**: Next.js with React 19 and Tailwind CSS v4.
- **Animations**: `motion` (Framer Motion).
- **SEO**: Semantic metadata exports, OpenGraph tags, structured JSON-LD.

---

## 6. Review Gates & Verification Examples

### Sentinel Security Gate (`/sam-sentinel`)
Sentinel performs static analysis and checks for vulnerabilities:
```markdown
# Sentinel Gate Checklist
- [x] No plaintext credentials or hardcoded API keys
- [x] Input parameters sanitized / validated via Pydantic or Zod
- [x] Broken Object-Level Authorization (BOLA/IDOR) protected via parent-child ownership check
- [x] Rate limiting applied on public-facing and authentication endpoints
- [x] Database queries use parameterized queries (ORM) to prevent SQL injection
```

### Cosmo CSS Review Gate (`/sam-cosmo`)
Cosmo checks UI implementations against design tokens:
- No ad-hoc colors (e.g. `bg-[#ff0033]`) — must use theme tokens like `bg-primary`, `bg-emerald-500`.
- Consistent spacing scale (`p-4`, `gap-6`) conforming to Tailwind guidelines.
- Mobile-first responsive breakpoints (`sm:`, `md:`, `lg:`).

### Aria Accessibility Gate (`/sam-aria`)
Aria audits web and mobile interfaces:
- Correct ARIA roles on interactive elements (`role="button"`, `aria-expanded`).
- Sufficient color contrast (minimum 4.5:1 for normal text).
- Full keyboard navigability without focus traps in modal dialogs.
- Screen reader accessibility for child-friendly icons and badges.

---

## 7. Artifact Organization in `sdocs/`

All SAM-generated files are strictly kept inside `sdocs/`:

```text
sdocs/
├── architecture-ref.md             # Resolved technical architecture and seam decisions
├── validation-report.md            # PRD intake and assumption validation results
├── contracts/                      # Code-shaped typed contracts between stories
│   ├── INDEX.md                    # Registry of all contracts
│   └── rewards/
│       ├── ledger-event.md         # rewards.ledger-event
│       └── wallet-balance.md       # rewards.wallet-balance
├── epics/                          # High-level epic groupings
│   ├── EPIC-001-rewards-ledger.md
│   └── EPIC-002-xp-rules-engine.md
├── stories/                        # Executable TDD units
│   ├── STORY-001-record-reward-event.md
│   ├── STORY-002-evaluate-xp-rules.md
│   └── STORY-003-integration-rewards.md
└── evidence/                       # Test logs, verification reports, UI proofs
    ├── STORY-001/
    │   ├── pytest_output.log
    │   └── schema_validation.log
    └── STORY-002/
        └── test_execution.log
```

---

## 8. Common Troubleshooting & Error Recovery

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| **Story blocked on retry exhaustion** | Titan tests failed 3 times or implementation cannot pass tests | Inspect `sdocs/evidence/<STORY_ID>/failure.log`, refine prompt/code manually, or run `/sam-argus` to diagnose |
| **Contract drift / mismatch** | Client-side story implements fields not present in FastAPI OpenAPI schema | Inspect live schema in `NoorHeroes-Backend/` router before coding; never invent client-side fields |
| **Attempted modification of PRD** | Agent attempts to rewrite file in `PRD_Documents/` | Blocked by governance rule. Generate supplementary details inside `sdocs/` instead |
| **Accidental secret detected** | A `.env` or API token is staged or present in diff | Remove immediately. Sentinel will block any commit or story completion containing secrets |

---

## 9. Common Commands Cheat Sheet & Real Scenarios (Recipe Book)

Here is a practical, copy-pasteable cookbook of the 12 most common everyday workflows in NoorHeroes.

### Recipe 1: Plan a New Feature from an Existing PRD
**Scenario:** You need to decompose Feature A.6 (Dua Learning) into contracts, epics, and stories.
```bash
/sam-plan PRD_Documents/Child App (1-12)/Feature_A6_Dua_Learning.md
```
*Expected Outcome:* Generates `sdocs/architecture-ref.md`, `sdocs/contracts/dua/`, `sdocs/epics/`, and `sdocs/stories/`.

---

### Recipe 2: Plan Feature A.11 Rewards System
**Scenario:** Decomposing the gamified economy and reward ledger into actionable TDD stories.
```bash
/sam-plan PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md
```
*Expected Outcome:* Produces `sdocs/contracts/rewards/ledger-event.md`, `sdocs/epics/EPIC-001-rewards-core.md`, and initial stories ready for TDD.

---

### Recipe 3: Implement a Single Backend API Story via TDD
**Scenario:** You have story `STORY-005-dua-spaced-repetition.md` ready and want to implement it in FastAPI.
```bash
/sam-build-tdd sdocs/stories/STORY-005-dua-spaced-repetition.md
```
*Expected Outcome:* Titan writes failing pytest tests in `NoorHeroes-Backend/tests/`, Dyna implements routers/services in `src/noorheroes/`, Argus refactors, Sentinel audits security, and updates status to `done`.

---

### Recipe 4: Implement a Mobile Screen Story in KMP / CMP
**Scenario:** You want to implement the child Dua playback audio screen in Compose Multiplatform.
```bash
/sam-build-tdd sdocs/stories/STORY-008-dua-player-screen.md
```
*Expected Outcome:* Titan writes Compose Multiplatform unit tests, Dyna implements the ViewModel and `@Composable` UI adhering to `CORE_UI_INSTRUCTIONS.md`, and Cosmo checks layout tokens.

---

### Recipe 5: Implement an Admin Web Dashboard Screen Story
**Scenario:** You want to build the Scholar Content Approval table in Next.js Admin.
```bash
/sam-build-tdd sdocs/stories/STORY-012-admin-dua-moderation-table.md
```
*Expected Outcome:* Titan writes Vitest component tests, Dyna builds the table with React Query and Hook Form, Aria validates keyboard accessibility, and Cosmo validates Tailwind CSS classes.

---

### Recipe 6: Implement a Public Website Landing Page Story
**Scenario:** You want to implement the Parent Web Portal feature highlight section on the public website.
```bash
/sam-build-tdd sdocs/stories/STORY-018-website-parent-portal-section.md
```
*Expected Outcome:* Dyna authors the responsive component using Tailwind CSS v4 and Motion, ensuring SEO metadata and OpenGraph compatibility.

---

### Recipe 7: Add a New Feature or Endpoint to an Already Completed Feature
**Scenario:** Feature A.11 is already live, but you need to add an endpoint for calculating Ramadan 2x multipliers.
1. Create `sdocs/addenda/ADDENDUM-003-ramadan-multiplier.md`.
2. Run:
```bash
/sam-extend sdocs/addenda/ADDENDUM-003-ramadan-multiplier.md
```
*Expected Outcome:* Evolve contracts in `sdocs/contracts/rewards/` and append new stories `STORY-015-...` without modifying completed stories.

---

### Recipe 8: Full Autonomous PRD-to-Code Pipeline
**Scenario:** You want to autonomously plan and build an isolated supporting module like Islamic Facts (Feature B.18).
```bash
/sam-plan-n-build PRD_Documents/Child App Supporting (13-18)/Feature_B18_Islamic_Facts_Module.md
```
*Expected Outcome:* Sequentially plans, designs contracts, generates stories, and executes TDD for every story until all are marked `done`.

---

### Recipe 9: Perform a Pre-Release Security Audit
**Scenario:** You are preparing a release candidate for the Family Area and want Sentinel to audit for BOLA/IDOR and secret exposure.
```bash
/sam-sentinel "Perform a comprehensive security audit on all endpoints under /api/v1/family and /api/v1/parent in NoorHeroes-Backend"
```
*Expected Outcome:* Generates a vulnerability audit report in `sdocs/evidence/security-audit-family.md`.

---

### Recipe 10: Audit Accessibility and Keyboard Navigation on Web Admin
**Scenario:** Ensuring the Parent Web Portal and Admin CMS meet WCAG 2.1 AA standards.
```bash
/sam-aria "Audit noorheroes-admin/src/features/family-management for keyboard navigation, tab stops, and aria-labels"
```
*Expected Outcome:* Identifies missing ARIA attributes, color contrast issues, and tab order errors with code-fix recommendations.

---

### Recipe 11: Review Code Quality and Adherence to Invariants
**Scenario:** After implementing a complex database transaction in rewards or wallet.
```bash
/sam-argus "Review NoorHeroes-Backend/src/noorheroes/modules/rewards/repository.py for adherence to append-only immutability invariant"
```
*Expected Outcome:* Confirms zero `UPDATE` or `DELETE` statements on financial/reward tables and verifies SQLAlchemy 2.0 async conventions.

---

### Recipe 12: Inspect Story Statuses Across the Whole Pipeline
**Scenario:** Check which stories are ready, in-progress, done, or blocked.
```bash
/sam-orchestrator "List all stories in sdocs/stories/ grouped by status and epic"
```
*Expected Outcome:* Tabular breakdown of the entire implementation progress.
