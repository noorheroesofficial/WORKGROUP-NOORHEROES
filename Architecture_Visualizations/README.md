# NoorHeroes Archify Architecture Visualization System

> Authoritative guide, specifications, and operational runbook for the **Archify Architecture Visualization System** in the **WORKGROUP-NOORHEROES** monorepo.

---

## Table of Contents
1. [What is Archify?](#1-what-is-archify)
2. [Prerequisites & Installation](#2-prerequisites--installation)
3. [First Example Walkthrough: Cache-Miss Flow](#3-first-example-walkthrough-cache-miss-flow)
4. [Diagram Type Guide](#4-diagram-type-guide)
5. [JSON Intermediate Representation (IR) Authoring Guide](#5-json-intermediate-representation-ir-authoring-guide)
6. [Validation Engine & Diagnostics Guide](#6-validation-engine--diagnostics-guide)
7. [Delivery Engine & Atomic Replacement](#7-delivery-engine--atomic-replacement)
8. [Automated Visual Verification](#8-automated-visual-verification)
9. [Safe Modification & Surgical Update Workflow](#9-safe-modification--surgical-update-workflow)
10. [Source-of-Truth Hierarchy & Invariants](#10-source-of-truth-hierarchy--invariants)
11. [Production Safety & Fail-Closed Guardrails](#11-production-safety--fail-closed-guardrails)
12. [Developer CLI & NPM Scripts](#12-developer-cli--npm-scripts)
13. [Verified NoorHeroes Reference Diagrams](#13-verified-noorheroes-reference-diagrams)
14. [Multi-Role Engineering Usage](#14-multi-role-engineering-usage)
15. [Troubleshooting & Diagnostic Playbook](#15-troubleshooting--diagnostic-playbook)
16. [CI/CD Automated Architecture Auditing](#16-cicd-automated-architecture-auditing)
17. [Git Strategy & Artifact Policies](#17-git-strategy--artifact-policies)

---

## 1. What is Archify?

### 1.1 Overview & Purpose
**Archify** is an industrial-grade, zero-dependency architecture visualization compiler. It transforms human-readable, schema-validated **JSON Intermediate Representation (IR)** specifications into self-contained, standalone interactive HTML/SVG artifacts.

Within `WORKGROUP-NOORHEROES`, Archify serves as the official visual documentation layer for all 4 sub-projects:
- [`NoorHeroes/`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes): Mobile client (Kotlin Multiplatform / Compose Multiplatform)
- [`NoorHeroes-Backend/`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend): Core API, auth, phonetic scoring, and game state (FastAPI / PostgreSQL / Redis)
- [`noorheroes-admin/`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/noorheroes-admin): Scholar portal, curriculum CMS, and operations (Next.js 16 / React 19)
- [`noorheroes-website/`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/noorheroes-website): Public landing page & waitlist (Next.js / Tailwind CSS)

### 1.2 Core Problems Archify Solves
1. **Visual Rot & Drift**: Static images (PNG, JPEG, draw.io) silently rot when APIs change. Archify JSON specifications are strictly validated against composition rules in CI.
2. **Heavy External Dependencies**: Unlike Mermaid (limited layout control) or PlantUML (requires Java/Graphviz), Archify runs in pure **Node.js ECMAScript Modules (ESM)** with **zero runtime npm dependencies**.
3. **Loss of Interactive Context**: Archify outputs standalone HTML files containing embedded SVG, theme switching (Light / Dark), smooth pan/zoom, interactive stage navigation, view filtering, card accordions, and SVG export—viewable in any modern browser without a local web server.
4. **AI-Agent Ambiguity**: AI coding agents struggle with freeform vector layouts. Archify's JSON IR provides a structured, deterministically checkable contract that agents can inspect, generate, and patch with mathematical precision.

### 1.3 What Archify Does NOT Do
- It is **not** an arbitrary HTML or website builder; it generates self-contained vector diagram canvases.
- It is **not** a real-time runtime monitoring dashboard or APM tool (e.g., Datadog, Grafana).
- It is **not** a loose sketching tool; it enforces strict orthogonal routing, node clearances, and label collision checks.
- It does **not** treat generated HTML as the source of truth.

### 1.4 Source JSON vs. Generated HTML
```
┌───────────────────────────────────────┐
│  Source JSON IR (.json)               │  <-- SOURCE OF TRUTH (Human & Agent editable)
│  - Semantic nodes & boundaries        │
│  - Explicit orthogonal routing & via  │
│  - High-level narrative views & cards │
└──────────────────┬────────────────────┘
                   │  archify deliver (Validates 9 geometric & schema rules)
                   ▼
┌───────────────────────────────────────┐
│  Delivered Standalone HTML (.html)    │  <-- DERIVED ARTIFACT (View & Export only)
│  - Zero external scripts/CDNs         │
│  - Embedded SVG & CSS tokens          │
│  - Interactive canvas & camera engine │
└───────────────────────────────────────┘
```
**CRITICAL RULE**: Never edit generated `.html` files directly. Any manual change to an `.html` file will be completely overwritten upon the next build. Always modify the corresponding `.json` specification in `Architecture_Visualizations/source/`.

---

## 2. Prerequisites & Installation

### 2.1 Prerequisites
- **Node.js**: Version `18.0.0` or higher (verified with Node `v26.5.0` on Windows and Linux).
- **Package Manager**: `npm` (v9+), `pnpm`, or `yarn`.
- **Browser (for automated visual verification)**: Google Chrome, Microsoft Edge, Chromium, or Brave installed locally (only needed for `npm run archify:visual-check`).

### 2.2 Repository-Local Installation (Standard Workflow)
Archify is already bundled and integrated directly within the repository root at [`tools/archify/`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/tools/archify) and exposed via the root executable [`bin/archify.mjs`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/bin/archify.mjs).

No installation is needed to begin using it:
```bash
# Verify environment and CLI availability
node bin/archify.mjs doctor

# Or via npm
npm run archify:doctor
```
Expected output:
```text
[PASS] archify environment check:
  Node.js: v26.5.0
  Platform: win32
  Architecture Engine: tools/archify
  Status: Operational
```

### 2.3 Global Installation (Cross-Project Developer Workstation)
If you wish to use Archify across arbitrary external repositories on your machine, install it globally using `skills` or npm:
```bash
# Via skills CLI
npx skills add tt-a1i/archify -g

# Or link globally from source
git clone https://github.com/tt-a1i/archify.git
cd archify
npm link
```

### 2.4 Workspace Agent Skills
Archify is also mirrored into local agent skill directories for autonomous agent discovery:
- [`.agents/skills/archify/`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/.agents/skills/archify)
- [`.agent/skills/archify/`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/.agent/skills/archify)

---

## 3. First Example Walkthrough: Cache-Miss Flow

To understand the complete lifecycle from prompt to verified diagram, consider a standard backend scenario: **Browser -> API Gateway -> Redis -> Cache Miss -> PostgreSQL**.

### Step 1: Prompting an AI Agent
```text
Use Archify to create a sequence diagram showing a cache-miss request flow in NoorHeroes.
Show:
- Client (Mobile App)
- API Gateway (FastAPI /api/v1)
- Redis Cache (Session & Leaderboard Cache)
- Primary Database (PostgreSQL 16)
Include an initial GET, a cache query, cache miss return, database read, cache repopulation, and final 200 OK.
Enforce quality_profile: showcase.
```

### Step 2: The Generated JSON Specification
Save to `Architecture_Visualizations/examples/cache-miss-request.sequence.json`:
```json
{
  "schema_version": 1,
  "diagram_type": "sequence",
  "meta": {
    "title": "API Gateway Cache-Miss Flow",
    "output": "cache-miss-request.sequence.html",
    "viewBox": [960, 520],
    "quality_profile": "showcase"
  },
  "participants": [
    { "id": "client", "label": "Client App", "type": "frontend" },
    { "id": "api", "label": "FastAPI Gateway", "type": "backend" },
    { "id": "redis", "label": "Redis 7 Cache", "type": "database" },
    { "id": "postgres", "label": "PostgreSQL 16", "type": "database" }
  ],
  "messages": [
    { "from": "client", "to": "api", "label": "GET /api/v1/leaderboard", "variant": "emphasis" },
    { "from": "api", "to": "redis", "label": "GET leaderboard:daily" },
    { "from": "redis", "to": "api", "label": "nil (cache miss)", "variant": "dashed" },
    { "from": "api", "to": "postgres", "label": "SELECT * FROM daily_stars ORDER BY stars DESC LIMIT 50" },
    { "from": "postgres", "to": "api", "label": "50 rows returned", "variant": "dashed" },
    { "from": "api", "to": "redis", "label": "SETEX leaderboard:daily 300 <payload>" },
    { "from": "api", "to": "client", "label": "200 OK (application/json)", "variant": "emphasis" }
  ],
  "cards": [
    {
      "dot": "amber",
      "title": "Cache Invalidation & TTL",
      "items": [
        "Leaderboards have a 300-second TTL to balance database query loads against near-real-time updates.",
        "On cold starts or expired keys, queries fall back to indexed PostgreSQL read replicas."
      ]
    }
  ]
}
```

### Step 3: Validate the Specification
Before compiling to HTML, validate the specification:
```bash
node bin/archify.mjs validate sequence Architecture_Visualizations/examples/cache-miss-request.sequence.json --quality showcase --json
```
If valid, the exit code is `0` with `"ok": true`.

### Step 4: Deliver the Interactive HTML
Deliver atomically to an HTML file:
```bash
node bin/archify.mjs deliver sequence Architecture_Visualizations/examples/cache-miss-request.sequence.json Architecture_Visualizations/examples/cache-miss-request.sequence.html --quality showcase --json
```
Archify performs candidate generation, full composition verification, computes sha256 hashes, and atomically replaces the output file.

### Step 5: Open & Inspect
Open directly in any browser:
```bash
# On Windows
start Architecture_Visualizations/examples/cache-miss-request.sequence.html

# On macOS
open Architecture_Visualizations/examples/cache-miss-request.sequence.html

# On Linux
xdg-open Architecture_Visualizations/examples/cache-miss-request.sequence.html
```

---

## 4. Diagram Type Guide

Archify supports 5 purpose-built diagram types. Select the diagram type that accurately matches your engineering communication objective:

| Diagram Type | Primary Use Case | Key Geometric Model | NoorHeroes Project Canonical Example |
| :--- | :--- | :--- | :--- |
| **`architecture`** | Component topology, boundaries, physical hosting, and tiers | Boxes, boundary containers, orthogonal buses, ports, and clusters | [`source/architecture/system-core.architecture.json`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Architecture_Visualizations/source/architecture/system-core.architecture.json) |
| **`workflow`** | Business processes, sequential phases, conditional decision points, and user funnels | Ordered phases, linear and branch transitions, decision diamonds, review cards | [`source/workflow/auth-onboarding.workflow.json`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Architecture_Visualizations/source/workflow/auth-onboarding.workflow.json) |
| **`sequence`** | Inter-service protocol messaging, request-response lifecycles, and cache patterns | Lifelines, horizontal directional messages, activations, synchronous & async dashed arrows | [`source/sequence/mission-progress.sequence.json`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Architecture_Visualizations/source/sequence/mission-progress.sequence.json) |
| **`dataflow`** | Pipelines, stream processing, data governance, and privacy sanitization boundaries | Multi-stage pipeline columns, data classifications, routing via channels | [`source/dataflow/tajweed-phonetics.dataflow.json`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Architecture_Visualizations/source/dataflow/tajweed-phonetics.dataflow.json) |
| **`lifecycle`** | Finite state machines (FSM), entity statuses, ledger accounting, and order transitions | FSM states, orthogonal transitions, retry loops, terminal success/failure nodes | [`source/lifecycle/rewards-ledger.lifecycle.json`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Architecture_Visualizations/source/lifecycle/rewards-ledger.lifecycle.json) |

---

## 5. JSON Intermediate Representation (IR) Authoring Guide

Archify schemas are strictly typed and reject unknown or invented fields. All source specifications must adhere to the following schema conventions:

### 5.1 Common Top-Level Schema
```json
{
  "$schema": "../../tools/archify/schemas/architecture.schema.json",
  "schema_version": 1,
  "diagram_type": "architecture",
  "meta": {
    "title": "System Architecture Diagram",
    "output": "system.architecture.html",
    "viewBox": [1280, 720],
    "quality_profile": "showcase",
    "theme": "dark",
    "views": [
      {
        "id": "overview",
        "label": "All Components",
        "focus": ["client", "api", "database"],
        "note": "Complete request lifecycle"
      }
    ]
  },
  "nodes": [],
  "boundaries": [],
  "relationships": [],
  "cards": []
}
```

### 5.2 Node IDs & Stability Rules
- **Rule 1: Lowercase snake_case or kebab-case** (e.g. `fastapi_gateway`, `pg_primary`, `audio_buffer`).
- **Rule 2: Never change IDs across iterations**. Changing a node ID breaks historical references, diffs, views, and connecting edges.
- **Rule 3: Semantic, not positional**. Do not name a node `top_left_box`; name it `kmp_mobile_app`.

### 5.3 Allowed Node Types
Archify maps node types to distinct visual styling and color tokens:
- `"frontend"`: Client apps, mobile UI, browser portals, desktop applications.
- `"backend"`: API servers, controllers, background workers, microservices.
- `"database"`: Relational databases, KV stores, document databases.
- `"cloud"`: Ingress proxies, DNS, CDNs, load balancers, object storage.
- `"security"`: Vaults, encryption zones, quarantine areas, auth boundaries.
- `"external"`: Third-party vendor APIs, push notification services (FCM, APNS).

### 5.4 Relationships & Orthogonal Routing
Archify requires all arrows to be **strictly orthogonal** (horizontal and vertical line segments only). Diagonal or arbitrary lines will fail layout validation.

Fields available on relationships:
- `from`: Origin node ID.
- `to`: Destination node ID.
- `label`: Readable description of the payload or protocol.
- `variant`: Styling variant: `"default"`, `"emphasis"` (highlighted primary path), `"security"` (shielded), `"dashed"` (asynchronous or response).
- `fromSide`: `"top"`, `"bottom"`, `"left"`, `"right"`.
- `toSide`: `"top"`, `"bottom"`, `"left"`, `"right"`.
- `via`: Explicit array of coordinate waypoints `[[x1, y1], [x2, y2]]` to guide the route around obstacles.
- `labelAt`: Explicit `[x, y]` coordinate for the label background card.

---

## 6. Validation Engine & Diagnostics Guide

Archify's validator ensures diagrams are clean, legible, and structurally sound before they can ever be rendered.

### 6.1 Validation Command
```bash
node bin/archify.mjs validate <type> <path/to/spec.json> --quality showcase --json
```

### 6.2 The 9 Geometric Checks
Every diagram must pass all 9 geometric validation checks:
1. **`single_svg`**: Output must have exactly one root `<svg>` viewport.
2. **`finite_svg`**: No `NaN`, `undefined`, or infinite coordinate values in paths or viewBox.
3. **`orthogonal_arrows`**: Every path segment must be strictly horizontal (`y1 === y2`) or vertical (`x1 === x2`).
4. **`label_route_clearance`**: Labels must maintain at least 4px (default) or 10px (showcase) clearance from unrelated paths.
5. **`relationship_crossings`**: Intersecting relationships must cross perpendicularly at 90 degrees; collinear or T-junction crossings fail.
6. **`relationship_corridors`**: Parallel edge lines must maintain at least 12px separation; overlapping corridors fail.
7. **`container_border_runs`**: Relationship paths must not run directly on top of node or boundary container borders.
8. **`route_rhythm`**: Relationships must avoid excessive micro-segments (< 8px) or unnecessary bends (> 3 bends).
9. **`legend_clearance`**: Canvas nodes and paths must not collide with the floating navigation dock or legend overlay.

### 6.3 Diagnosing and Repairing Errors
When validation fails, Archify returns a JSON diagnostic payload detailing the exact cause and suggested coordinates:
```json
{
  "code": "composition/label-route-clearance",
  "severity": "error",
  "message": "showcase architecture label \"read/write\" is 0px from relation \"cache-feed\" segment",
  "suggestedFix": "adjust labelAt: [420, 290] or labelDy: +24"
}
```
**Repair Strategy**:
1. Inspect the reported `subject` and `segmentIndex`.
2. Apply the `suggestedFix` directly to the JSON specification.
3. Re-run `node bin/archify.mjs validate ...` until all 9 checks pass.

---

## 7. Delivery Guide & Atomic Replacement

### 7.1 What is "Delivery"?
In Archify, compilation and rendering is referred to as **delivery**. Unlike naive tools that spit out unverified HTML, Archify follows a transactional pipeline:
```
Source JSON IR
      │
      ▼
Candidate HTML Generation (Memory)
      │
      ▼
Full Composition & Layout Validation
      ├── FAIL ──> Abort transaction; log diagnostics; disk untouched
      │
      └── PASS ──> Compute SHA256 integrity hash
                         │
                         ▼
                   Atomic File Write (Replaces target .html cleanly)
```

### 7.2 Delivery Command
```bash
node bin/archify.mjs deliver <type> <source.json> <output.html> --quality showcase --json
```
Successful output:
```json
{
  "ok": true,
  "command": "deliver",
  "type": "architecture",
  "input": "Architecture_Visualizations/source/architecture/system-core.architecture.json",
  "output": "Architecture_Visualizations/generated/architecture/system-core.architecture.html",
  "specification": { "sha256": "3cb49a...", "bytes": 4820 },
  "artifact": { "sha256": "9b124a...", "bytes": 818420 },
  "validation": { "checksPassed": 9, "checkCount": 9, "errors": 0, "warnings": 0 }
}
```

### 7.3 Fail-Closed Safety
If validation fails during delivery, the destination file is **never modified or corrupted**. If a previously working diagram exists at that path, it remains intact.

---

## 8. Automated Visual Verification

### 8.1 Why Visual Check is Needed
Passing mathematical schema validation guarantees orthogonal segments and collision-free labels, but does not guarantee how a browser renders fonts, responsive viewports, or floating controls.

Archify includes a headless Chromium-based verification engine:
```bash
node bin/archify.mjs visual-check <path/to/diagram.html> --json
```

### 8.2 What Visual Check Measures
1. **Viewport Containment**: Opens the diagram in headless Chrome across 4 standard enterprise desktop viewports:
   - `1440 x 900` (MacBook Pro standard)
   - `1600 x 1000` (16:10 Laptop)
   - `1920 x 1080` (Full HD Desktop)
   - `2048 x 1320` (High-DPI Retina Workstation)
2. **Zero Viewport Overflow**: Verifies `scrollWidth === innerWidth` and `scrollHeight === innerHeight`. If any element forces a page scrollbar, the check fails.
3. **Typography Legibility**: Calculates the computed pixel size of the smallest text node. If any rendered text drops below `6px`, it fails.
4. **Dock & Stage Clearance**: Verifies that the bottom navigation dock maintains at least `10px` clearance from diagram nodes.
5. **Theme Snapshots**: Generates PNG screenshots for both Light and Dark themes alongside a contact-sheet HTML.

---

## 9. Safe Modification & Surgical Update Workflow

When updating existing architecture diagrams, **never delete and rewrite from scratch**. Follow this surgical update discipline:

```
┌──────────────────────────────────────────────┐
│ 1. Read existing JSON specification          │
└──────────────────────┬───────────────────────┘
                       │
┌──────────────────────▼───────────────────────┐
│ 2. Identify the exact node or edge to modify │
│    - Retain all existing node IDs            │
│    - Retain existing coordinate bounds       │
└──────────────────────┬───────────────────────┘
                       │
┌──────────────────────▼───────────────────────┐
│ 3. Apply minimal surgical JSON patch         │
└──────────────────────┬───────────────────────┘
                       │
┌──────────────────────▼───────────────────────┐
│ 4. Run `npm run archify:validate`            │
└──────────────────────┬───────────────────────┘
                       │
┌──────────────────────▼───────────────────────┐
│ 5. Run `npm run archify:build`               │
└──────────────────────┬───────────────────────┘
                       │
┌──────────────────────▼───────────────────────┐
│ 6. Verify with `npm run archify:visual-check`│
└──────────────────────────────────────────────┘
```

---

## 10. Source-of-Truth Hierarchy & Invariants

Within `WORKGROUP-NOORHEROES`, the following precedence hierarchy is strictly enforced:

```
1. PRD_Documents/                                (Authoritative Business Logic & Rules)
   │
2. Development_Blueprints/                       (Authoritative Technical Specifications)
   │
3. Production Source Code                        (Live Application Architecture)
   │
4. Architecture_Visualizations/source/*.json    (Archify Source Specification)
   │
5. Architecture_Visualizations/generated/*.html (Derived Visual Artifact)
```

### Invariants:
- Never edit PRDs to fit a diagram layout.
- Never invent backend routes or database schemas that do not exist in the source code.
- Never treat the `.html` file as source.

---

## 11. Production Safety & Fail-Closed Guardrails

Archify incorporates built-in guardrails against common documentation failure modes:
1. **Duplicate Node IDs**: Rejects duplicate IDs at parse time.
2. **Dangling References**: Every relationship `from` and `to` must resolve to a valid node ID.
3. **Collinear Overlaps**: Parallel relationships sharing a channel must maintain at least 12px clearance.
4. **Label Collisions**: Label cards cannot sit on top of nodes or crossing vectors.
5. **Non-Orthogonal Edges**: Slanted lines or diagonal routes are rejected.
6. **Integrity Hashing**: Sha256 content hashes are recorded for both the specification and delivered artifact.

---

## 12. Developer CLI & NPM Scripts

The root [`package.json`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/package.json) exposes developer commands for daily workflow:

```bash
# Check Node.js and Archify engine health
npm run archify:doctor

# Validate all specifications in source/ and examples/
npm run archify:validate

# Compile and atomically deliver all HTML artifacts
npm run archify:build

# Run headless browser visual verification on all generated diagrams
npm run archify:visual-check

# Run the standard workgroup test suite (includes Archify validation)
npm test
```

### Direct CLI Commands
You can also run Archify directly via `bin/archify.mjs`:
```bash
# Validate a single file
node bin/archify.mjs validate architecture Architecture_Visualizations/source/architecture/system-core.architecture.json --quality showcase

# Deliver a single file
node bin/archify.mjs deliver architecture Architecture_Visualizations/source/architecture/system-core.architecture.json Architecture_Visualizations/generated/architecture/system-core.architecture.html --quality showcase

# Visual-check a single file
node bin/archify.mjs visual-check Architecture_Visualizations/generated/architecture/system-core.architecture.html
```

---

## 13. Verified NoorHeroes Reference Diagrams

The repository includes 5 production-verified canonical diagrams modeling actual NoorHeroes systems:

### 1. System Architecture (`architecture`)
- **Source**: [`source/architecture/system-core.architecture.json`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Architecture_Visualizations/source/architecture/system-core.architecture.json)
- **Delivered**: [`generated/architecture/system-core.architecture.html`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Architecture_Visualizations/generated/architecture/system-core.architecture.html)
- **Scope**: Comprehensive topology showing KMP Mobile App, Web Admin Portal, Cloudflare Ingress, FastAPI Backend, Celery Workers, Redis 7, PostgreSQL 16 (master + read replica), and external integrations (Postmark, Google Play Billing, Cloud Storage).

### 2. Authentication & Onboarding Workflow (`workflow`)
- **Source**: [`source/workflow/auth-onboarding.workflow.json`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Architecture_Visualizations/source/workflow/auth-onboarding.workflow.json)
- **Delivered**: [`generated/workflow/auth-onboarding.workflow.html`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Architecture_Visualizations/generated/workflow/auth-onboarding.workflow.html)
- **Scope**: 6-phase COPPA/GDPR-K compliant onboarding funnel: Splash -> Language -> Parent Phone Registration -> Parental Consent -> OTP Verification -> Child Profile & Avatar Selection -> Home Dashboard.

### 3. Mission Progress API Sequence (`sequence`)
- **Source**: [`source/sequence/mission-progress.sequence.json`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Architecture_Visualizations/source/sequence/mission-progress.sequence.json)
- **Delivered**: [`generated/sequence/mission-progress.sequence.html`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Architecture_Visualizations/generated/sequence/mission-progress.sequence.html)
- **Scope**: Real-time roundtrip for submitting lesson audio scoring: Mobile Client -> Offline SQLDelight Store -> TLS Edge Ingress -> FastAPI `/missions/{id}/progress` -> Redis Streak Cache -> PostgreSQL Ledger -> Notification dispatch.

### 4. Rewards Double-Entry Ledger Lifecycle (`lifecycle`)
- **Source**: [`source/lifecycle/rewards-ledger.lifecycle.json`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Architecture_Visualizations/source/lifecycle/rewards-ledger.lifecycle.json)
- **Delivered**: [`generated/lifecycle/rewards-ledger.lifecycle.html`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Architecture_Visualizations/generated/lifecycle/rewards-ledger.lifecycle.html)
- **Scope**: FSM tracking star & badge transactions across financial-grade states: `draft` -> `pending_validation` -> `escrowed` -> `committed` (with branch to `failed` and `refunded_void`).

### 5. Audio & Tajweed Phonetics Data Flow (`dataflow`)
- **Source**: [`source/dataflow/tajweed-phonetics.dataflow.json`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Architecture_Visualizations/source/dataflow/tajweed-phonetics.dataflow.json)
- **Delivered**: [`generated/dataflow/tajweed-phonetics.dataflow.html`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Architecture_Visualizations/generated/dataflow/tajweed-phonetics.dataflow.html)
- **Scope**: 5-stage data processing pipeline: Client PCM Audio -> TLS Ingress -> Ephemeral RAM Buffer (Zero Retention) & Tajweed Phonetics Engine -> PostgreSQL 16 & Redis 7 -> Child Progress UI & Scholar Moderation Queue.

---

## 14. Multi-Role Engineering Usage

### For AI Coding Agents (SAM / Atlas / Titan / Dyna / Antigravity)
When prompted to generate or update architecture diagrams:
1. First read the relevant source code in `NoorHeroes/`, `NoorHeroes-Backend/`, or `noorheroes-admin/`.
2. Inspect [`Architecture_Visualizations/source/`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Architecture_Visualizations/source) for existing related specifications.
3. Generate valid Archify JSON adhering to the schema.
4. Execute `node bin/archify.mjs validate <type> <file.json> --quality showcase --json` to test layout math.
5. If valid, deliver via `node bin/archify.mjs deliver <type> <file.json> <output.html> --quality showcase`.
6. Run `node bin/archify.mjs visual-check <output.html> --json` to confirm zero overflow.

### For Senior Engineers & System Architects
- Use Archify JSON files during RFC and Architecture Review Boards (ARB).
- Include links to generated `.html` files in pull request descriptions.
- Review JSON diffs during code reviews just as you would review Terraform or OpenAPI schemas.

### For QA Engineers
- Inspect the `views` array in sequence and lifecycle diagrams to verify all edge cases (retries, timeouts, error branches) are accounted for in test plans.

### For DevOps & Platform Engineers
- Check container boundaries in `architecture` diagrams to verify deployment topology matches Kubernetes, Docker Compose, or AWS/GCP manifests.

---

## 15. Troubleshooting & Diagnostic Playbook

### Problem 1: `archify: command not found` or `Cannot find module`
**Remedy**:
Ensure you are running from the workspace root and using `node bin/archify.mjs` or `npm run archify:*`.
Verify Node.js version:
```bash
node -v  # Must be >= 18.0.0
```

### Problem 2: Validation Failure: `clean-flow/endpoint-side-direction`
**Cause**:
An authored `toSide` or `fromSide` enters a node horizontally when the segment direction is vertical, or vice versa.
**Remedy**:
Ensure the final segment of your `via` coordinates matches the perpendicular axis of the side:
- For `toSide: "left"`, the segment must run horizontally to the right (`x1 < x2`, `y1 === y2`).
- For `toSide: "bottom"`, the segment must run vertically upward (`y1 > y2`, `x1 === x2`).

### Problem 3: Validation Failure: `composition/label-route-clearance`
**Cause**:
A label rectangle is positioned too close (< 4px) to an intersecting or parallel vector route.
**Remedy**:
Adjust `labelAt: [x, y]` or provide `labelDx` / `labelDy` to move the label badge away from the line.

### Problem 4: Visual Check Failure: `overflowX` or `overflowY` is `true`
**Cause**:
The diagram content exceeds the viewport height on 1440x900 screens.
**Remedy**:
1. Check the `meta.viewBox` in the source JSON (e.g. reduce height from 720 to 520).
2. Reduce unnecessary vertical padding in `cards` or shorten card item descriptions.

---

## 16. CI/CD Automated Architecture Auditing

The repository includes a dedicated GitHub Actions workflow: [`.github/workflows/archify.yml`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/.github/workflows/archify.yml).

### Workflow Behavior
1. Triggers on any `push` or `pull_request` modifying `Architecture_Visualizations/**`, `bin/**`, or `scripts/**`.
2. Sets up Node.js.
3. Executes `npm run archify:validate`.
4. If any diagram specification fails schema or composition checks, the PR check turns RED and blocks merging.

---

## 17. Git Strategy & Artifact Policies

### Committed Files:
- **`Architecture_Visualizations/source/**/*.json`**: **ALWAYS COMMITTED**. This is the authoritative architecture specification.
- **`Architecture_Visualizations/generated/**/*.html`**: **COMMITTED**. Delivered HTML files are self-contained and pre-rendered so stakeholders can view diagrams immediately without needing to run Node.js locally.
- **`Architecture_Visualizations/examples/**/*.json`**: **COMMITTED**. Reference upstream specifications.

### Ignored Files:
- Temporary candidate files (`*.candidate.html`).
- Diagnostic screenshots (`*.png`) generated during local visual checks (unless explicitly archived for release notes).
