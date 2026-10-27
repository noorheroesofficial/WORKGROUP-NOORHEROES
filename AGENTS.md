# NoorHeroes + SAM Engineering Governance & Execution Rules

> Authoritative operational rules for SAM agents (Atlas, Titan, Dyna, Argus, Sentinel, Quill, etc.) and AI coding agents operating within WORKGROUP-NOORHEROES.

## 1. Source-of-Truth Hierarchy & Precedence
SAM operates strictly as an **engineering execution layer**, never as the authoritative requirements source. All planning and coding must observe this precedence:
1. `PRD_Documents/` — Authoritative product requirements & business logic
2. `Development_Blueprints/` — Authoritative implementation blueprints & flow specifications
3. `NoorHeroes_Consolidated_Execution_Blueprint.md` — Consolidated execution roadmap
4. `DEVELOPMENT-RULES.md` & `PROJECT-CONTEXT.md` — Workgroup operating invariants & live architecture context
5. **Project Architecture Manuals**:
   - Backend: [`NoorHeroes-Backend/MASTER-README.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/MASTER-README.md) & [`FAST-API-INSTRUCTIONS.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/FAST-API-INSTRUCTIONS.md)
   - Mobile: [`NoorHeroes/README.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes/README.md) & 13 core manuals in `NoorHeroes/core/`
   - Admin: [`noorheroes-admin/MASTER-README.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/noorheroes-admin/MASTER-README.md) & [`NEXT-JS-INSTRUCTIONS.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/noorheroes-admin/NEXT-JS-INSTRUCTIONS.md)
   - Public Web: [`noorheroes-website/README.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/noorheroes-website/README.md) & [`WEBSITE-INSTRUCTIONS.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/noorheroes-website/WEBSITE-INSTRUCTIONS.md)
6. **Project Domain Agents**: `Admin-Agent/` and `Backend-Agent/` (domain-specific runbooks, ADRs, contracts)
7. **SAM Generic Workflows**: SAM planning, contracts, stories, TDD pipeline

## 2. Protected Directories (Strictly Read-Only)
Never modify, generate, reformat, move, or delete files inside:
- `PRD_Documents/`
- `Development_Blueprints/`
- `Screens/`

## 3. Autonomous Multi-Project Boundaries
WORKGROUP-NOORHEROES contains 4 independent codebases/repositories:
- `NoorHeroes/`: Mobile app (Kotlin Multiplatform / Compose Multiplatform / Android & iOS)
- `NoorHeroes-Backend/`: Backend API & DB (Python / FastAPI / PostgreSQL / Redis)
- `noorheroes-admin/`: Internal Admin Portal (Next.js / TypeScript / React 19)
- `noorheroes-website/`: Public Website (Next.js / TypeScript / Tailwind CSS)

Do not cross boundaries improperly or merge architectures. Respect each project's isolated package managers, test runners, and build systems.

## 4. SAM Artifact Isolation
All SAM-generated artifacts (plans, contracts, epics, stories, test reports, evidence) MUST reside strictly in:
- `sdocs/` (e.g. `sdocs/contracts/`, `sdocs/epics/`, `sdocs/stories/`, `sdocs/evidence/`)
Never output SAM-generated files into `PRD_Documents/`, `Development_Blueprints/`, or `Screens/`.

## 5. Pre-Implementation Workflow
Before authoring any code:
1. **PRD Intake**: Consume the relevant feature PRD from `PRD_Documents/`. Do NOT generate a replacement PRD.
2. **Blueprint Alignment**: Read the corresponding Blueprint in `Development_Blueprints/`.
3. **Screen Reference**: Inspect reference screens in `Screens/` (visual guidance; compare implementation evidence against them).
4. **SAM Planning**: Run `/sam-plan <prd-path>` to decompose into contracts and stories within `sdocs/`.
5. **API Contract Verification**: Inspect live FastAPI OpenAPI schemas/routers before implementing client-side API integrations. Never invent fields.

## 6. Implementation & Verification
1. **TDD Discipline**: Follow SAM's strict RED (failing test) → GREEN (minimal implementation) → REFACTOR cycle via `/sam-build-tdd`.
2. **Security & Secrets**: Never expose credentials, API keys, or `.env` files into Git, `sdocs/`, or agent outputs. Run Sentinel security checks.
3. **Evidence & Quality**: Capture test logs and UI evidence into `sdocs/evidence/`. Verify cross-platform contracts before closing stories.
