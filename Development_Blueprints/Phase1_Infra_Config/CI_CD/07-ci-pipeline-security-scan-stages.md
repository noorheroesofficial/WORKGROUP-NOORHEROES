# Phase 1 — CI Pipeline: Non-Bypassable Security Scan Stage (Stage 8 of 13)

**Blueprint ID:** `Development_Blueprints.Phase1_Infra_Config.CI_CD.07-ci-pipeline-security-scan-stages`
**Platform:** CI/CD (repo-wide: `.github/workflows/`, with per-app jobs touching `backend/`, `admin-web/`, `mobile/`)
**Phase:** Phase 1 — Infrastructure & Configuration
**Depends on:** `Development_Blueprints.Phase1_Infra_Config.CI_CD.06-ci-pipeline-lint-test-build-stages.md` (CI stages 1–7: lint/format, static type-check, secret-scan-script wiring, unit tests, integration tests, architectural invariant tests, build artifact — this document's jobs are appended to the same per-app workflow files that item 06 creates, and consume item 06's stage-7 build output)
**Also depends on:** `Development_Blueprints.Phase1_Infra_Config.Infra.02-secrets-management-env-example-gitleaks.md` (secret scanning mechanics — gitleaks + trufflehog, `.gitleaks.toml`, `secret-scan.yml` — already fully specified there; this document does not redefine any of it)
**Consumed by:** `Development_Blueprints.Phase1_Infra_Config.CI_CD.08-ci-pipeline-deploy-staging-e2e-smoke.md` (or equivalent — stage 9 "Deploy to staging" must not run until this stage's required checks are green)
**Source of truth:** `NoorHeroes_Final_Development_Prompt.md` §6 (13-stage pipeline, stage 8: "Container/dependency scan (Trivy or Grype on the built image; `pip-audit`/`pnpm audit`/Gradle dependency check)") and §9 (Security Baseline item 7: "Wire SAST (Bandit/Semgrep), dependency scanning, container scanning, and secret scanning into CI as required, non-bypassable status checks"); `NoorHeroes_Consolidated_Blueprint_v6.md` §13.4 API Security ("SAST, dependency scanning, container scanning, and regular penetration testing as part of the CI/CD pipeline and a recurring security calendar")

**Do not re-litigate:**
- **Secret scanning** (gitleaks pre-commit hook, `.gitleaks.toml`, trufflehog, `secret-scan.yml`, the `.env.example` drift-check scripts) is fully owned and already specified by Infra item 02. This document treats `secret-scan.yml`'s two jobs (`gitleaks-scan`, `trufflehog-verified-scan`) as an existing, already-required status check pair, and only describes how *this* stage's own required checks sit alongside them in branch protection as one combined, non-bypassable security gate (§9 below). Do not create a second secret-scanning mechanism here.
- **CI stages 1–7** (lint/format, `mypy`/`tsc --noEmit`/detekt static type-check, unit tests, integration tests, architectural invariant tests, Docker/APK build) are fully owned by item 06. This document assumes `backend.yml`, `admin-web.yml`, and `mobile.yml` already exist with jobs for those stages, and only specifies the **new jobs appended to those same three workflow files** for stage 8, plus how those new jobs wire into item 06's existing `needs:` graph.
- **Bandit and detekt as day-to-day lint tools** already exist per Final_Development_Prompt §1.2 (backend code-quality stack: "Ruff/Black/mypy/**Bandit** for security linting") and §1.1 (mobile: "ktlint + detekt (custom rules for 'no gateway-layer business auth', 'no raw credential prefs')"). Those existing configurations (`backend/pyproject.toml`'s `[tool.bandit]` section, `mobile/config/detekt.yml`) are not rewritten by this document — this document's job is narrower and specific: **make Bandit's findings a required, non-bypassable CI gate** (today it may only run locally / as a non-blocking lint step under item 06's stage-2 static-analysis job — confirm this before implementing, per §18 Assumption 5), and **add Semgrep as a second, independent SAST pass** covering patterns Bandit (Python-only) and detekt (Kotlin-only, architectural-rule-focused) don't reach — namely admin-web's TypeScript/React surface, and a defense-in-depth generic pass across all three languages.
- **Container image build mechanics** (multi-stage `Dockerfile`s, `python:3.12-slim` / Next.js standalone `node:XX-alpine` runtime stages, Artifact Registry push with `<git-sha>` tags to `us-central1-docker.pkg.dev/noorheroes-{env}/noorheroes-containers/{app}:<git-sha>`) are owned by item 06 (stage 7, "Build artifact") and the registry itself is provisioned by Infra item 04's `global/state-bootstrap` Terraform module. This document only *consumes* the resulting image reference to scan it — it does not touch the Dockerfiles or the registry provisioning.

---

## 1. Objective and purpose

Make it structurally impossible for a pull request to merge into `main` — for anyone, including a repository admin — while it introduces a known-exploitable code pattern (SAST), a dependency with a disclosed Critical/High vulnerability (dependency scanning), or a container image whose base layer or installed packages carry a disclosed Critical/High vulnerability with an available fix (container scanning). Secret scanning (already specified by item 02) is the fourth pillar of the same non-bypassable gate; this document's job is to build the other three pillars and then wire all four into one enforcement story.

This is Security Baseline item 7 from Final_Development_Prompt §9, and §9's preamble is explicit that this whole section is **"prerequisite infrastructure, not a feature to schedule later."** Concretely, this document delivers:

1. **SAST** — Bandit (Python, backend) made CI-blocking, plus Semgrep (Python/TypeScript/Kotlin, all three apps) as a second, independent SAST pass, both wired as required status checks.
2. **Dependency vulnerability scanning** — `pip-audit` (backend, against the `uv`-resolved environment), `pnpm audit` (admin-web), and the OWASP Dependency-Check Gradle plugin (mobile), each with an explicit severity-threshold gate.
3. **Container image scanning** — Trivy against the backend and admin-web images pushed to Artifact Registry by item 06's stage-7 build job, gated on fixable Critical/High findings.
4. **The unified, non-bypassable gate** — every job above (and item 02's two secret-scan jobs) registered as a required GitHub branch-protection status check on `main`, with "Include administrators" enabled, so no role can merge past a failure — plus the exception/waiver process that is the *only* legitimate way past a finding that turns out to be a false positive or an accepted, time-boxed risk.

**Why this belongs to Phase 1 and not "later":** every feature branch from Phase 2 onward — including the F.37 Security Architecture branches (canonical JWT schema, refresh-token rotation, Argon2id hashing, the 11-step upload pipeline) that item 02's own document calls out — touches either credential-adjacent code, a new dependency, or a container rebuild. If this stage isn't live before Phase 2 starts, every one of those branches merges without the exact category of review its own PRD demands.

---

## 2. Scope and requirements

**In scope:**
- SAST job definitions for backend (Bandit + Semgrep), admin-web (Semgrep), and mobile (Semgrep) — appended to `backend.yml`, `admin-web.yml`, `mobile.yml` respectively.
- Dependency-scan job definitions for all three apps, each with a concrete, documented severity threshold.
- Container-scan job definitions for backend and admin-web (mobile produces an APK/AAB, not a container — no container-scan job for mobile).
- The severity-threshold policy (§9) — which findings block merge, which only warn.
- The exception/waiver registry (`.github/security-waivers.yml`), its schema, its expiry enforcement, and who may approve a waiver.
- Branch-protection wiring: the exact required-status-check names this document adds, alongside item 02's existing two, with "Include administrators" confirmed still enabled.
- A scheduled (non-PR-triggered) nightly re-scan workflow that catches a CVE disclosed *after* a dependency/image was already merged (§10, §11).
- SARIF upload wiring so every tool's findings land in GitHub's Security → Code scanning tab, giving one unified audit surface across all six scanners.

**Out of scope (owned elsewhere):**
- Secret scanning mechanics — item 02, referenced only.
- Stages 1–7 (lint, type-check, tests, build) — item 06.
- Stages 9–13 (deploy, E2E, promotion, prod deploy, post-deploy smoke) — the next CI/CD blueprint in this series; this document's only contract with it is "stage 9 must not start until this stage's required checks are green," which branch protection (§9) already enforces structurally, so no explicit hand-off code is needed.
- Penetration testing and the "recurring security calendar" named in Consolidated_Blueprint_v6 §13.4 — that is a human process (scheduled pen-test engagements), not a CI job; out of scope for a CI pipeline document.
- Runtime/production WAF, rate limiting, credential-stuffing detection (Consolidated_Blueprint_v6 §13.4's other bullets) — those are gateway/infrastructure concerns, not CI gates.
- Rewriting `[tool.bandit]` in `backend/pyproject.toml` or `mobile/config/detekt.yml` — this document invokes the existing configuration, it does not redesign it (§18 Assumption 5 covers the one exception: confirming Bandit is not already silently non-blocking).

---

## 3. Technical implementation details

### 3.1 Tool choices (final — do not substitute)

| Concern | Tool(s) chosen | Why |
|---|---|---|
| SAST — Python (backend) | **Bandit** (already a dependency per Final_Development_Prompt §1.2) | Named explicitly by §9 item 7 ("SAST (Bandit/Semgrep)"); Python-native, AST-based, zero new dependency to add — this document only changes *how* its output is consumed (CI-blocking, not just local lint). |
| SAST — all three apps, defense-in-depth + admin-web/mobile coverage | **Semgrep** (OSS CLI, Apache 2.0, self-hosted rule execution — no Semgrep AppSec Platform account, no SaaS dependency) | Also named explicitly by §9 item 7. Chosen over CodeQL for three concrete reasons: (1) CodeQL's free tier is scoped to public repositories — NoorHeroes is a private monorepo, so CodeQL requires GitHub Advanced Security, a paid add-on not mentioned anywhere in the confirmed stack; (2) Semgrep's OSS CLI runs identically in CI and on a developer's laptop with zero account/licensing step, consistent with the corpus's repeated "avoid a new vendor dependency" bias (self-hosted Unleash over LaunchDarkly, self-hosted Redis note, etc. — Final_Development_Prompt §6/§7); (3) Semgrep ships maintained rule packs for Python, TypeScript/React, and Kotlin from one CLI, letting one tool cover backend, admin-web, and mobile instead of three separate SAST products. Bandit remains primary for Python specifically because it is already in the stack and has zero false-positive-prone generic rules for Python-specific footguns (`subprocess` with `shell=True`, `pickle`/`eval`, weak-hash usage) that Semgrep's Python pack covers more shallowly. |
| SAST — Kotlin (mobile) | Semgrep only (`p/kotlin` community pack), **not** a new tool | Mobile's existing detekt custom rules already enforce the two named architectural invariants ("no gateway-layer business auth," "no raw credential prefs" — Final_Development_Prompt §1.1) as CI-blocking checks under item 06's stage-2 static-analysis job. This document does not duplicate that. Semgrep's Kotlin pack adds a second, generic security net (hardcoded IPs/URLs, insecure `TrustManager` overrides, `Random()` used for security-sensitive values) that detekt's *custom* rule set was never scoped to cover. |
| Dependency scanning — backend | **`pip-audit`** (run against the `uv`-managed environment, not a hand-maintained `requirements.txt`) | Named explicitly by §6 stage 8. Queries the PyPA Advisory Database (aggregates OSV + GHSA); works directly against an installed/resolved environment, which is exactly what `uv sync --frozen` produces from `uv.lock` — no extra export/translation step needed beyond what `uv` already does. |
| Dependency scanning — admin-web | **`pnpm audit`** | Named explicitly by §6 stage 8; admin-web already uses `pnpm` (confirmed via item 02's `.gitleaks.toml` allowlist entry for `pnpm-lock.yaml` and item 03's Dockerfile reference). `pnpm audit` queries the npm/GitHub Advisory registry and has a native `--audit-level` severity gate — no wrapper script needed for the blocking check itself. |
| Dependency scanning — mobile | **OWASP Dependency-Check Gradle plugin** (`org.owasp.dependencycheck`) | Named explicitly by §6 stage 8 ("Gradle dependency check"). Cross-references resolved Gradle dependencies (the KMP/CMP `core-*` modules' third-party artifacts) against the NVD CVE feed; has a native `failBuildOnCVSS` gate and native SARIF output. |
| Container image scanning | **Trivy** (`aquasecurity/trivy-action`) | Named first in §6 stage 8 ("Trivy or Grype"). Chosen over Grype because Trivy is a single binary that also scans OS packages, language-level dependencies baked into the image, and (as a bonus, not exercised by this document) IaC misconfiguration — one tool, one config format, one GitHub Action, native SARIF output, actively maintained with same-day CVE feed updates. Grype is a reasonable alternative with no material capability gap for this use case; Trivy is selected for its broader single-tool coverage and to keep the number of distinct scanner configurations in this already six-scanner-wide stage as low as possible. |

### 3.2 SAST vs. type-check vs. lint — do not conflate

Item 06's stage 1 (lint/format: Ruff, ESLint/Prettier, ktlint) and stage 2 (`mypy --strict`, `tsc --noEmit`, detekt) are **not** SAST. They catch style violations and type errors, not exploitable security patterns. Bandit/Semgrep are security-focused static analyzers that look for a materially different class of defect (SQL built via string concatenation, `eval()` on user input, hardcoded cryptographic material, insecure deserialization, SSRF-shaped outbound requests). Do not fold this stage's jobs into stage 1/2's existing jobs — they are new, separately-named jobs specifically so a SAST failure is unmissable in the PR UI as its own check, mirroring the precedent Final_Development_Prompt §6 stage 6 already set for architectural invariant tests ("run as an explicit, separately-named, required-status-check job so a failure here is unmissable in the PR UI, distinct from a generic 'tests failed'").

### 3.3 Severity-threshold policy (the exact blocking rule per tool)

This is the single most load-bearing decision in this document — every job's exit-code logic must implement exactly this table, no tool's default behavior is trusted as-is without an explicit flag/config setting the threshold below:

| Tool | **Blocks merge** (required check fails) | **Warns only** (annotated, non-blocking) | **Ignored** (visible in report, never gates) |
|---|---|---|---|
| Bandit | `severity=HIGH` at `confidence>=MEDIUM` | `severity=MEDIUM` | `severity=LOW` |
| Semgrep | any finding tagged `severity=ERROR` in the rule packs used (§7) | `severity=WARNING` | `severity=INFO` |
| `pip-audit` | any advisory with a CVSS base score **≥ 7.0**, OR any advisory with **no CVSS score published** (fail-closed — an unscored advisory is treated as blocking until a human triages it, never silently passed) | CVSS 4.0–6.9 | CVSS < 4.0 |
| `pnpm audit` | `--audit-level=high` (blocks `high` and `critical`, per npm/GitHub Advisory's own severity taxonomy) | `moderate` | `low` |
| OWASP Dependency-Check | `failBuildOnCVSS = 7.0` (blocks CVSS ≥ 7.0) | CVSS 4.0–6.9 | CVSS < 4.0 |
| Trivy (container) | `CRITICAL`/`HIGH` **with a fix available** (`--ignore-unfixed`) | `MEDIUM`, `LOW`, and any `CRITICAL`/`HIGH` finding with **no fix available yet** (tracked via the waiver registry with an auto-renewing "unfixed upstream" waiver type, §9 — not silently dropped) | none — Trivy's full report (all severities) is always uploaded to the SARIF/Security tab regardless of gating |

Rationale for the two deliberate deviations from "just use the tool's default":
- **`pip-audit`'s fail-closed-on-unscored rule** exists because OSV-sourced advisories (which `pip-audit` also consults) sometimes lack a CVSS vector at disclosure time, especially for very recent CVEs — silently treating "no score" as "not blocking" would create exactly the gap a scanner exists to close. A human (the security-leads waiver approver, §9) must explicitly triage an unscored finding, either waiving it or confirming its eventual score.
- **Trivy's `--ignore-unfixed`** exists because blocking merges forever on a base-OS CVE with no vendor patch yet (a routine, ongoing state for `python:3.12-slim`/`node:XX-alpine` base images) would make the gate noise, training reviewers to reach for the waiver file reflexively — which defeats its purpose. Unfixed findings are tracked (not hidden) and re-checked automatically by the nightly scan (§11) so a fix that ships later is caught promptly, without every PR paying the cost in the meantime.

### 3.4 Exception/waiver mechanism — design

A single registry file, `.github/security-waivers.yml`, following the same "canonical registry" pattern item 02 already established for `infra/secrets/manifest.yaml`:

```yaml
# .github/security-waivers.yml
version: 1
waivers:
  - id: WAIVER-2026-001
    tool: trivy                       # bandit | semgrep | pip-audit | pnpm-audit | dependency-check | trivy
    finding_id: CVE-2026-XXXXX        # CVE id, GHSA id, or the tool's own rule id (e.g. Bandit's B608)
    scope: "backend image — python:3.12-slim base layer, libssl3 package"
    justification: "No upstream Debian security patch yet (tracked at security-tracker.debian.org); not reachable via any NoorHeroes code path — confirmed via Trivy's package-listing output, no application code links against the affected library directly."
    approved_by: "@noorheroes/security-leads"   # must be a GitHub team handle with write access; see enforcement below
    created_date: "2026-08-20"
    expires_date: "2026-09-19"        # mandatory — see max-duration table below; a waiver with no expires_date is invalid config and fails the gating script's own schema check
    ticket: "SEC-142"                  # link to the tracking issue for eventual remediation
```

**Every gating script (Bandit/Semgrep/`pip-audit`/`pnpm audit`/Dependency-Check/Trivy wrapper, §7) reads this one file** and, for each finding at or above its blocking threshold, checks whether an **active** (not expired) waiver entry matches on `tool` + `finding_id` (+ `scope` substring match for container/dependency findings, since the same CVE ID can recur across many packages). A match downgrades that specific finding from blocking to a warning annotation in the job's GitHub Step Summary; a non-match leaves it blocking. An **expired** waiver is treated identically to no waiver at all (still blocks) **and** the gating script additionally emits a distinct `::warning::EXPIRED WAIVER WAIVER-2026-001 for CVE-2026-XXXXX — re-triage or renew` annotation, so an expired waiver is loud, not silently ignored.

**Maximum waiver duration by severity** (enforced by the gating script's schema validation — a waiver whose `expires_date` exceeds this window for its finding's severity is rejected as invalid config, failing the job even before the underlying finding is evaluated):

| Finding severity | Max waiver duration |
|---|---|
| Critical | 30 days |
| High | 90 days |
| Medium | 180 days |
| Trivy "unfixed upstream" waiver type | 30 days, but auto-renewable without a new approval as long as the nightly re-scan (§11) confirms the upstream fix still doesn't exist — see §11 |

**Who may approve a waiver:** only `@noorheroes/security-leads` (a GitHub team this document assumes exists or is created as part of implementation — cross-reference the Repo.03 branching-policy blueprint's CODEOWNERS pattern). Enforcement is **not** a runtime check inside the gating script (a script cannot verify who wrote a YAML file) — it is enforced the same way item 03's "blast radius" reviewer requirement is enforced: `.github/security-waivers.yml` is added as a CODEOWNERS-protected path (`/.github/security-waivers.yml @noorheroes/security-leads` appended to the existing `CODEOWNERS` file item 03 creates), so no PR that edits the waiver file can merge without a security-leads review, regardless of who opened the PR. This is the actual approval gate; the `approved_by` field inside the YAML is a human-readable audit record of *which* security-lead reviewed it, not the enforcement mechanism itself.

---

## 4. Architecture and component responsibilities

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  PULL REQUEST OPENED / PUSHED                                                 │
└──────────────────────────────────────────────────────────────────────────────┘
                │
                ├─► backend.yml (item 06 + this doc's stage-8 jobs)
                │     stage1 lint ─► stage2 typecheck ─┬─► sast-bandit ─────────┐
                │                                        ├─► sast-semgrep-backend│
                │                                        ├─► dependency-scan-backend │
                │     stage3..7 (secret-scan-script, tests, build) ─► container-scan-backend │
                │                                                              │
                │                                        all of the above ────┴─► backend-security-gate (aggregator, REQUIRED)
                │
                ├─► admin-web.yml (same shape)                                       ─► admin-web-security-gate (aggregator, REQUIRED)
                │
                ├─► mobile.yml (no container-scan — APK/AAB, not an image)            ─► mobile-security-gate (aggregator, REQUIRED)
                │
                └─► secret-scan.yml (item 02, unchanged, always-triggered)
                      gitleaks-scan (REQUIRED)        trufflehog-verified-scan (REQUIRED)

┌──────────────────────────────────────────────────────────────────────────────┐
│  BRANCH PROTECTION on `main` — required status checks (union, "Include        │
│  administrators" ON):                                                          │
│    gitleaks-scan · trufflehog-verified-scan            (item 02)              │
│    backend-security-gate · admin-web-security-gate · mobile-security-gate     │
│                                                          (this document)      │
│  → PR merge button is disabled while ANY of the five is red, for every role.  │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│  NIGHTLY SCHEDULED WORKFLOW — security-nightly-rescan.yml (this document)     │
│  Re-scans main's latest images + dependency trees against a fresh vuln DB.    │
│  New Critical/High finding on already-merged code → auto-files a GitHub Issue │
│  labeled `security-nightly`, does NOT retroactively block anything already    │
│  merged (see §10 for the full "CVE disclosed post-merge" handling).           │
└──────────────────────────────────────────────────────────────────────────────┘

Every tool's findings ──SARIF──► GitHub Security → Code scanning tab (unified audit surface, §11)
```

**Component responsibilities:**

| Component | Owns | Does NOT own |
|---|---|---|
| `backend.yml` / `admin-web.yml` / `mobile.yml` (item 06, this doc appends jobs) | The actual scan execution per app, per tool | The waiver registry's approval rule (that's CODEOWNERS, item 03) |
| `{app}-security-gate` aggregator job (new, this document) | The single required-status-check name branch protection points to per app | Individual scanner logic (delegates to the jobs it depends on) |
| `.github/security-waivers.yml` | The canonical, human-reviewed record of accepted risk, with mandatory expiry | Enforcement of *who* can edit it (that's CODEOWNERS) |
| `.github/scripts/security_gate.py` (new, shared gating helper — §7) | Parsing each tool's raw output, applying §3.3's thresholds, checking §3.4's waivers, producing the pass/fail exit code and the Step Summary annotation | The scanners themselves (Bandit/Semgrep/`pip-audit`/Dependency-Check/Trivy each run as their own CLI step; this script only triages their output) |
| `security-nightly-rescan.yml` (new, this document) | Catching a CVE disclosed after merge (§10, §11) | Blocking any already-merged commit retroactively (not possible — it files an issue instead) |
| `secret-scan.yml` (item 02, unchanged) | Secret scanning, as already specified | Everything in this document |

---

## 5. Folder/file structure

```
noorheroes/
├── .github/
│   ├── CODEOWNERS                                    # MODIFY — item 03 owns this file; this doc appends one line
│   │                                                  #   /.github/security-waivers.yml @noorheroes/security-leads
│   ├── security-waivers.yml                          # NEW — the waiver registry (§3.4)
│   ├── scripts/
│   │   ├── security_gate.py                          # NEW — shared severity+waiver triage helper, imported/invoked
│   │   │                                              #   by every stage-8 job (see §7 interface)
│   │   └── security_gate_test_fixtures/               # NEW — sample tool-output JSON/SARIF files used by
│   │       ├── bandit_sample_high.json                #   security_gate.py's own unit tests (§14)
│   │       ├── pip_audit_sample_unscored.json
│   │       └── trivy_sample_unfixed.json
│   └── workflows/
│       ├── backend.yml                                # MODIFY (item 06's file) — append sast-bandit,
│       │                                              #   sast-semgrep-backend, dependency-scan-backend,
│       │                                              #   container-scan-backend, backend-security-gate
│       ├── admin-web.yml                              # MODIFY (item 06's file) — append sast-semgrep-admin-web,
│       │                                              #   dependency-scan-admin-web, container-scan-admin-web,
│       │                                              #   admin-web-security-gate
│       ├── mobile.yml                                 # MODIFY (item 06's file) — append sast-semgrep-mobile,
│       │                                              #   dependency-scan-mobile, mobile-security-gate
│       │                                              #   (no container-scan-mobile — no container is built)
│       └── security-nightly-rescan.yml                 # NEW — scheduled re-scan, §10/§11
├── backend/
│   ├── pyproject.toml                                  # MODIFY — add `bandit[sarif]` + `pip-audit` to the dev
│   │                                                  #   dependency group only if not already present (Bandit
│   │                                                  #   itself is already listed per Final_Development_Prompt
│   │                                                  #   §1.2 — confirm before adding a duplicate entry)
│   └── .semgrepignore                                  # NEW — excludes generated code (OpenAPI client stubs,
│                                                        #   Alembic migration boilerplate) from Semgrep noise
├── admin-web/
│   └── .semgrepignore                                  # NEW — excludes `.next/`, generated API client, `node_modules/`
├── mobile/
│   ├── build.gradle.kts (or the relevant convention-plugin file)   # MODIFY — apply
│   │                                              #   `org.owasp.dependencycheck` plugin, configure
│   │                                              #   `failBuildOnCVSS = 7.0f`, SARIF output format
│   └── .semgrepignore                                  # NEW — excludes generated KMP `expect`/`actual` build
│                                                        #   output, `build/` directories
└── docs/
    └── runbooks/
        └── security-scan-triage.md                     # NEW — how to read a failed stage-8 check, when to
                                                          #   fix vs. waive, the waiver-approval flow, escalation
                                                          #   path for a scanner-service outage (§10)
```

---

## 6. APIs, models, interfaces, and data flow

This is a CI/tooling document, not a feature with HTTP endpoints — "APIs" here means the internal contracts the stage-8 jobs and `security_gate.py` rely on.

### 6.1 `security_gate.py` interface

```python
# .github/scripts/security_gate.py
def evaluate(
    tool: Literal["bandit", "semgrep", "pip-audit", "pnpm-audit", "dependency-check", "trivy"],
    findings_path: Path,          # the tool's raw JSON/SARIF output file
    waivers_path: Path = Path(".github/security-waivers.yml"),
    today: date = date.today(),
) -> GateResult:
    """
    Parses `findings_path` per `tool`'s known output shape, classifies each
    finding against §3.3's threshold table, checks each blocking finding
    against an active (non-expired) waiver in `waivers_path`.

    Returns GateResult(
        exit_code: int,               # 0 if nothing blocking remains after waivers, 1 otherwise
        blocking: list[Finding],      # findings that fail the gate
        warned: list[Finding],        # findings below the blocking threshold, or waived
        expired_waivers_hit: list[str],  # waiver ids that matched but had expired
        summary_markdown: str,        # written to $GITHUB_STEP_SUMMARY
    )
    """
```

Every stage-8 CLI step is followed by one `python .github/scripts/security_gate.py --tool <name> --findings <path>` invocation; the job's pass/fail is `security_gate.py`'s exit code, never the raw scanner's own exit code (the raw scanner is invoked in "always succeed, write full output" mode — e.g. Bandit with `--exit-zero`, Trivy with `--exit-code 0` — specifically so `security_gate.py` is the single source of truth for the threshold+waiver logic, rather than duplicating that logic once per tool's own CLI flags).

### 6.2 Data flow — a PR touching `backend/`

```
git push / PR opened
  → backend.yml triggers (path-filtered on backend/**, per item 06)
  → stage1 lint, stage2 typecheck run (item 06, unchanged)
  → in parallel with stage3-7 (item 06):
      sast-bandit:          bandit -r backend/src --format json --exit-zero -o bandit.json
                             → security_gate.py --tool bandit --findings bandit.json
                             → also: bandit -r backend/src --format sarif -o bandit.sarif (always, for the Security tab)
                             → github/codeql-action/upload-sarif@v3 uploads bandit.sarif
      sast-semgrep-backend:  semgrep scan --config=p/security-audit --config=p/owasp-top-ten --config=p/python
                               --sarif --output=semgrep-backend.sarif backend/
                             → security_gate.py --tool semgrep --findings semgrep-backend.sarif
                             → upload-sarif
      dependency-scan-backend: uv sync --frozen (installs the exact locked environment)
                             → uv run pip-audit --format json -o pip-audit.json --strict
                               (--strict still runs even if a dependency fails to resolve a hash, but the JOB's
                                pass/fail comes from security_gate.py, not pip-audit's own exit code)
                             → security_gate.py --tool pip-audit --findings pip-audit.json
  → stage7 (item 06) builds & pushes backend:<git-sha> to Artifact Registry
  → container-scan-backend (needs: build):
      trivy image --format sarif --output trivy-backend.sarif --exit-code 0
        us-central1-docker.pkg.dev/noorheroes-staging/noorheroes-containers/backend:<git-sha>
      → security_gate.py --tool trivy --findings trivy-backend.sarif
      → upload-sarif
  → backend-security-gate (needs: [sast-bandit, sast-semgrep-backend, dependency-scan-backend, container-scan-backend]):
      a trivial job whose only step is `if: contains(needs.*.result, 'failure') → exit 1`, else exit 0
  → GitHub reports backend-security-gate's status on the PR
  → branch protection (§9) blocks merge until it (and the other required checks) are green
```

### 6.3 `security-waivers.yml` ↔ `security_gate.py` matching contract

A waiver matches a finding when **all** of: `tool` equals the invoking tool, `finding_id` equals the finding's CVE/GHSA/rule-id (case-insensitive), `expires_date` is on or after `today`, and — for `trivy`/`pip-audit`/`pnpm-audit`/`dependency-check` findings only — the finding's package/image-layer name appears as a substring of the waiver's `scope` field (prevents one CVE-ID waiver silently suppressing the *same* CVE in a different, unreviewed package). `bandit`/`semgrep` findings match on `tool` + `finding_id` (the rule id, e.g. `B608`, `python.lang.security.audit.formatted-sql-query`) + the finding's file path appearing in `scope` (same anti-over-broadening rationale).

---

## 7. Dependencies and configuration requirements

### 7.1 New tool dependencies

| Tool | Version pin | Installed via |
|---|---|---|
| `bandit` | Already present per Final_Development_Prompt §1.2 — pin `bandit[sarif]` extras if the SARIF formatter isn't already bundled; confirm current pin in `backend/pyproject.toml` before touching it | `uv` dev-dependency group (existing) |
| `pip-audit` | Latest stable, pinned exactly (not floated) | `uv add --dev pip-audit` |
| `semgrep` | Latest stable, pinned exactly | CI: official `semgrep/semgrep` Docker image (`returntocorp/semgrep` legacy tag is deprecated — use `semgrep/semgrep:<pinned-tag>`) run via `docker://` step or the `semgrep/semgrep-action`, pinned to a tagged release, not `:latest` |
| `trivy` | Latest stable, pinned exactly | `aquasecurity/trivy-action`, pinned to a tagged release |
| OWASP Dependency-Check Gradle plugin | Latest stable, pinned exactly in the Gradle Version Catalog (`gradle/libs.versions.toml`, per Final_Development_Prompt §1.1's build-system row) | `id("org.owasp.dependencycheck") version "<pinned>"` in the root/convention-plugin `build.gradle.kts` |
| `pnpm audit` | No separate install — ships with the already-present `pnpm` toolchain | N/A |

All CI-side tool versions (Bandit, Semgrep, Trivy, the Dependency-Check plugin) are pinned exactly, never floated to `latest`, for the same reason item 02 pins gitleaks/trufflehog exactly: a scanner silently updating its ruleset mid-sprint must never be the reason a previously-green PR suddenly goes red with no code change — version bumps are deliberate, reviewed PRs, not something CI does implicitly on every run.

### 7.2 Semgrep rule-pack configuration per app (no `p/secrets` anywhere — that's gitleaks/trufflehog's job, running it again here would duplicate alerts for the same class of finding across two unrelated tools)

| App | Rule packs |
|---|---|
| backend | `p/security-audit`, `p/owasp-top-ten`, `p/python` |
| admin-web | `p/security-audit`, `p/owasp-top-ten`, `p/typescript`, `p/react`, `p/nextjs` |
| mobile | `p/security-audit`, `p/kotlin` |

### 7.3 `mobile` — OWASP Dependency-Check Gradle configuration (excerpt)

```kotlin
// mobile/build.gradle.kts (or the shared convention plugin, per whichever the existing mobile
// build already uses — confirm before choosing where this block lives)
dependencyCheck {
    format = "SARIF"
    outputDirectory = "$buildDir/reports/dependency-check"
    failBuildOnCVSS = 7.0f          // §3.3 — blocks Critical/High, matches the other two dependency scanners
    suppressionFile = "mobile/dependency-check-suppressions.xml"   // reserved for false-positive suppression
                                     // ONLY when a matching entry also exists in .github/security-waivers.yml —
                                     // the XML suppression file alone is not a valid waiver; both must agree,
                                     // enforced by a small check in security_gate.py's dependency-check path
    nvdApiKeyEnvironmentVariable = "NVD_API_KEY"   // NVD now rate-limits unauthenticated feed access hard enough
                                     // that CI needs an API key (free, self-service) — store as a GitHub Actions
                                     // secret, NOT a Secret-Manager-backed runtime secret (this is a CI-only key)
}
```

### 7.4 `security-nightly-rescan.yml` — concrete job spec

```yaml
name: Security Nightly Re-scan
on:
  schedule:
    - cron: "0 3 * * *"   # 03:00 UTC daily — off peak, ahead of most teams' morning standup
  workflow_dispatch: {}    # allow manual trigger, e.g. right after a public CVE disclosure

permissions:
  contents: read
  security-events: write
  issues: write

jobs:
  rescan-backend-image:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Resolve latest main image tag
        run: echo "IMAGE=us-central1-docker.pkg.dev/noorheroes-production/noorheroes-containers/backend:$(git rev-parse origin/main)" >> "$GITHUB_ENV"
      - uses: aquasecurity/trivy-action@<pinned>
        with:
          image-ref: ${{ env.IMAGE }}
          format: sarif
          output: trivy-nightly-backend.sarif
          severity: CRITICAL,HIGH
          exit-code: 0
      - name: File issue on new finding
        run: python .github/scripts/security_gate.py --tool trivy --findings trivy-nightly-backend.sarif --nightly-mode --file-issue-on-new
  # rescan-admin-web-image: same shape, admin-web image
  # rescan-backend-deps / rescan-admin-web-deps / rescan-mobile-deps: same shape, dependency scanners against
  #   main's current lockfiles, catching a CVE disclosed for an already-merged dependency version
```

`--nightly-mode --file-issue-on-new` makes `security_gate.py` diff today's findings against the previous nightly run's cached findings (stored as a workflow artifact, retained per §11) and open a GitHub Issue (via the `gh` CLI, labeled `security-nightly`, assigned to `@noorheroes/security-leads`) only for genuinely new findings — not re-alert every night on an already-tracked, already-waived one.

---

## 8. Database/storage requirements

No application database tables. Three storage-adjacent artifacts, all GitHub-native, all part of this document's audit-trail design (§11):

- **GitHub Security → Code scanning alerts** (populated via `github/codeql-action/upload-sarif` from all six SARIF-producing steps) — GitHub retains code-scanning alerts on the default branch indefinitely and on other branches for the life of the branch; this is the primary, queryable audit trail for "what did we find and when."
- **GitHub Actions workflow artifacts** (the raw JSON/SARIF output of every scan, uploaded via `actions/upload-artifact`) — default 90-day retention (confirm the repo/org's configured retention window at implementation time; extend explicitly for at least the nightly re-scan's cached-findings artifact, since the new-finding diff logic in §7.4 depends on the previous run's artifact still existing).
- **`.github/security-waivers.yml`** — git-tracked, so its own edit history (via `git log`/`git blame`) is a complete, tamper-evident audit trail of every waiver ever granted, by whom (via the PR author + CODEOWNERS-enforced approving reviewer), and when it expired or was renewed.

---

## 9. Authentication, authorization, validation, and security considerations

**This entire document is the security consideration** — the items below are the specific, concrete decisions an implementer must not soften.

### 9.1 Branch protection — exact configuration

On `main` (GitHub repository settings → Branches → branch protection rule), in addition to whatever item 02/item 03 already configured:

- **Required status checks** (exact strings, must match job names verbatim): `gitleaks-scan`, `trufflehog-verified-scan` (already required by item 02 — do not remove), plus this document's three new aggregator checks: `backend-security-gate`, `admin-web-security-gate`, `mobile-security-gate`.
- **"Require branches to be up to date before merging"** — enabled (already the case per item 02; confirm it still is).
- **"Include administrators"** — enabled. This is the literal mechanism that makes the gate non-bypassable "even for repo admins," per this document's explicit requirement. Verify this checkbox specifically during implementation (§13, §17) — it is the single setting most likely to be silently unchecked by a well-meaning admin during some unrelated repo-settings change, and its absence quietly defeats every other control in this document.
- **No other bypass path exists**: this document does not create, and implementation must not add, any workflow-level `continue-on-error: true` on a stage-8 job, any `if: github.actor == 'some-admin-username'` skip condition, or any repository/organization-level "bypass list" for these specific checks. If GitHub's branch-protection UI offers a "bypass list" or "allow specified actors to bypass required pull requests" feature, it must be left empty for these five checks.

### 9.2 Least-privilege CI credentials

- The `NVD_API_KEY` (§7.3) and any Semgrep-related token are stored as GitHub Actions repository secrets, scoped to read-only usage by the stage-8 jobs — never given write access to any external system.
- Trivy's container-scan jobs need only read (pull) access to Artifact Registry, via the same Workload Identity Federation pattern Infra item 04 already establishes for CI's `terraform plan` step (cross-reference, not re-specified here) — the stage-8 scan jobs must not be granted push/write access to the registry, since they only read the image item 06's build job already pushed.

### 9.3 SARIF upload does not leak findings publicly

`security-events: write` permission (required for `upload-sarif`) only grants the workflow run permission to write to *this* repository's own Security tab — confirm the repository's code-scanning visibility is not separately configured to be public if the repo itself is private, since a public code-scanning feed would itself be a disclosure risk (a public list of exactly which CVEs a system is currently exposed to). This is a one-time repo-settings confirmation, not new code.

### 9.4 The waiver file is the only sanctioned bypass, and it is itself gated

Repeated from §3.4 because it is the crux of "non-bypassable": the *only* way a blocking finding stops blocking merge is a reviewed, expiring entry in `.github/security-waivers.yml`, approved by `@noorheroes/security-leads` via CODEOWNERS-enforced review on the waiver-file PR itself. There is no `--force`, no admin merge override, no CI variable that disables a job. A developer who believes a finding is a false positive must get a security-lead's review on the waiver entry — the same friction, deliberately, as any other risk-acceptance decision in this codebase.

### 9.5 Cross-reference to F.37's own security posture dashboard

Every SARIF upload and every waiver entry is a direct input to the "Security Posture Dashboard" Final_Development_Prompt §8 names as an Admin Portal module (MFA compliance, pen-test finding disposition, backup-restore history, IR tabletop history) — this document does not build that dashboard (out of scope, owned by whatever blueprint implements that Admin Portal page), but its data (open waivers approaching expiry, nightly-rescan-filed issues still unresolved, per-app scan pass/fail trend) is exactly the kind of feed that dashboard is specified to surface. Flag this as a known future consumer when that dashboard's blueprint is authored.

---

## 10. Error handling and edge cases

| Scenario | Behavior |
|---|---|
| Bandit/Semgrep produce a false positive (e.g., a test fixture that looks like a hardcoded credential to Semgrep's entropy-adjacent rules, or a genuinely safe `subprocess` call Bandit flags generically) | Fixed via a `.github/security-waivers.yml` entry (§3.4), reviewed by security-leads, **not** via an inline `# nosec` (Bandit) or `# nosemgrep` (Semgrep) comment — inline suppression comments are explicitly disallowed by this document's policy (see §18 Assumption 4) because they bypass the CODEOWNERS review the waiver file enforces; a developer can silently add `# nosec` to their own PR with no second reviewer ever required to approve it. |
| A dependency-scan/container-scan finding has no available fix (transitively pinned by an upstream package, or an unpatched base-OS CVE) | For Trivy, this is §3.3's built-in "unfixed, tracked not blocked" category — no waiver needed, it's structurally non-blocking already. For `pip-audit`/`pnpm audit`/Dependency-Check findings with no available fix, a waiver **is** required (these ecosystems don't have Trivy's `--ignore-unfixed` equivalent baked into the threshold table) — file one with a `ticket` tracking eventual removal/replacement of the offending dependency. |
| The vulnerability database a scanner depends on (NVD feed, PyPA Advisory DB, npm registry, Trivy's DB) is unreachable (network outage, rate-limited, provider incident) | **Fail closed, not open** — the job fails with a clear, distinct message ("scanner DB unreachable, not the same as a clean scan") rather than silently passing. Trivy specifically caches its vulnerability DB (via `actions/cache` keyed on a daily cache-bust) so a transient outage during the DB *update* step can fall back to the last successfully cached DB, **provided that cached DB is no more than 48 hours stale** — a freshness check step (`trivy --skip-db-update`'s reported DB timestamp) fails the job outright if the cached DB exceeds 48 hours old, forcing a human to investigate rather than scanning against a dangerously stale DB indefinitely. `pip-audit`/`pnpm audit`/Dependency-Check have no equivalent local-cache fallback in this design — a DB-fetch failure for those simply fails the job; retry is a `workflow_dispatch` re-run once the outage clears, not an automatic bypass. |
| A CVE is publicly disclosed for a dependency/base image **already merged and deployed** | This is exactly what `security-nightly-rescan.yml` (§7.4) exists to catch. It does **not** retroactively fail any already-merged PR's status check (that status is historical and immutable) — it files a new GitHub Issue against the current state of `main`, tagged `security-nightly`, assigned to security-leads, who then either ship a fix PR (which goes through the normal stage-8 gate like any other change) or file a time-boxed waiver if remediation needs longer than the nightly cadence allows. |
| A developer disagrees with a security-lead's waiver denial | Out of scope for this document (an organizational/process escalation, not a CI mechanism) — document the escalation path (e.g., "appeal to the engineering lead") in `docs/runbooks/security-scan-triage.md` rather than building any CI-level override. |
| A gating script itself (`security_gate.py`) has a bug that causes a false pass | Covered by `security_gate.py`'s own unit test suite (§14) against fixture files representing every threshold boundary (exactly-7.0 CVSS, exactly-expired waiver, unscored advisory) — this is the one component in this whole document whose own correctness is load-bearing enough to need direct unit tests rather than relying on the underlying scanner's correctness alone. |
| A repo admin attempts to merge a PR with a failing `backend-security-gate`/`admin-web-security-gate`/`mobile-security-gate`/`gitleaks-scan`/`trufflehog-verified-scan` check | Blocked — §9.1's "Include administrators" setting removes this escape hatch, identical in spirit to item 02's own equivalent edge case for secret scanning. |
| Semgrep's Docker-based action fails to pull its image (registry outage, rate limit) | Same fail-closed principle as the vulnerability-DB case above — the job fails, is not silently skipped; `semgrep/semgrep`'s image is also cached via `actions/cache`/Docker layer caching to reduce how often a live pull is even needed. |

---

## 11. State management and lifecycle considerations

- **Vulnerability database freshness:** every scanner's DB is fetched fresh at the start of each job run wherever the tool supports it (Trivy's `trivy-action` auto-updates its DB by default; `pip-audit`/`pnpm audit` query live registries per-invocation; Dependency-Check's NVD data is refreshed via its own incremental-update mechanism, cached across runs via `actions/cache` keyed on a weekly cache-bust to avoid re-downloading the full multi-GB NVD dataset on every single PR run while still staying materially current). The 48-hour staleness ceiling from §10 applies specifically to Trivy's cache-fallback path; the other tools' live-query design makes an equivalent staleness concept moot (they either succeed with current data or fail closed, per §10).
- **Scan result history / audit trail lifecycle:** SARIF-based findings live in GitHub's Security tab indefinitely on `main` (§8); raw JSON artifacts live for the configured Actions artifact retention window; `.github/security-waivers.yml`'s git history is permanent. Together these three give a complete answer to "what security posture did commit X have, and what was explicitly accepted at the time" — no separate database is introduced by this document specifically to avoid a second, competing source of truth for data GitHub already retains natively.
- **Waiver lifecycle:** created (PR merged, security-leads-reviewed) → active (matched, downgrades a finding) → approaching expiry (the nightly re-scan workflow, §7.4, also checks `.github/security-waivers.yml` for any entry expiring within 7 days and includes it in that day's summary/issue, giving security-leads advance notice rather than a silent lapse) → expired (treated as absent, loudly annotated per §3.4) → either renewed (a new PR bumping `expires_date`, itself CODEOWNERS-reviewed again — expiry cannot be silently extended by editing the file without review, since *any* edit to this path re-triggers the CODEOWNERS requirement) or allowed to lapse once the underlying finding is actually fixed.
- **`{app}-security-gate` aggregator jobs are stateless per-run**, same as item 02's `secret-scan.yml` jobs — no cross-run caching is required for correctness, only as a performance optimization for the underlying scanners' own DB downloads (above).
- **Nightly-rescan's "new vs. already-known finding" diff state:** persisted as a workflow artifact (the previous run's findings JSON) rather than a database — acceptable because the only consumer is the next scheduled run of the same workflow, and workflow artifacts are exactly the right lifecycle for "state one CI run hands to the next CI run."

---

## 12. Integration points with existing modules

- **Backend Python dependencies (`uv`/`uv.lock`, per Final_Development_Prompt §1.2 and confirmed by item 03's Docker Compose file using `ghcr.io/astral-sh/uv`):** `dependency-scan-backend`'s `uv sync --frozen` step must succeed against the *existing* `backend/pyproject.toml`/`uv.lock` unchanged by this document — this document adds `pip-audit` to the dev-dependency group (§7.1) and nothing else to that file's dependency graph. Bandit's config (`[tool.bandit]` in `pyproject.toml`, if present) is read as-is; if no `[tool.bandit]` section exists yet, this document's implementation must add a minimal one (excluding `backend/tests/` from scanning, since test fixtures legitimately contain patterns like hardcoded fake tokens that would otherwise false-positive) rather than leaving Bandit to scan test code with production-code assumptions.
- **Admin-web npm/pnpm dependencies (`admin-web/package.json`, `pnpm-lock.yaml`):** `dependency-scan-admin-web`'s `pnpm audit` step requires no code change to either file — it is a read-only query against the already-installed lockfile. Semgrep's admin-web pack additionally benefits from (but does not require) the existing Zod-validated `src/lib/env.ts` and centralized `API_ENDPOINTS` registry (per NEXT-JS-INSTRUCTIONS.md) as *positive* signal that reduces false positives around "hardcoded URL"/"unvalidated input" rule classes — no change to those files.
- **KMP/CMP Gradle dependencies (`mobile/gradle/libs.versions.toml`, the 12 `core-*` modules per Final_Development_Prompt §1.1):** the OWASP Dependency-Check plugin scans whatever the Gradle Version Catalog already resolves — no change to the catalog's existing entries, only the addition of the plugin itself and its configuration block (§7.3). Because `core-security`/`core-datastore` are explicitly called out elsewhere in this corpus (item 02 §12) as modules that must never be modified by adjacent infra work, this document is equally explicit: **no code in any `core-*` or `feature/*` module is touched by this blueprint** — only the root/convention-plugin Gradle file gains the plugin declaration.
- **Container images built in CI stage 7 (item 06, pushed to Artifact Registry per item 04's `noorheroes-containers` repo):** `container-scan-backend`/`container-scan-admin-web` consume the exact image reference item 06's build job outputs (`us-central1-docker.pkg.dev/noorheroes-{env}/noorheroes-containers/{app}:<git-sha>`, confirmed format per Infra item 04 §3/§7) — implementation must read item 06's build job's actual output variable name (likely a `needs.build.outputs.image_tag`-style GitHub Actions job output) rather than reconstructing the tag independently, to guarantee the exact image that will be deployed is the exact image that was scanned (never re-derive or re-build the tag string in a way that could silently drift from what stage 7 actually pushed).
- **Secret scanning (item 02's `secret-scan.yml`):** unchanged, referenced only — this document's branch-protection configuration (§9.1) adds its three new checks *alongside* item 02's existing two, never replacing or renaming them.
- **CODEOWNERS + branch protection (Repo item 03):** this document appends exactly one new CODEOWNERS line (`/.github/security-waivers.yml @noorheroes/security-leads`, §3.4) and three new required-status-check entries (§9.1) to infrastructure item 03 already establishes — it does not redefine item 03's Conventional Commits, SemVer, or general branch-protection scaffolding.
- **Terraform IaC (item 04):** this document's only Terraform-adjacent touchpoint is read-only — the Workload Identity Federation binding item 04 already grants CI for Artifact Registry access (§9.2) must include (or be extended to include, if it doesn't already) read/pull scope, which the stage-8 container-scan jobs use; no new Terraform resource is authored by this document.

---

## 13. Development steps in the correct implementation order

1. **Confirm Bandit's current CI status** (§18 Assumption 5) — read item 06's actual `backend.yml` stage-2 job and `backend/pyproject.toml`'s `[tool.bandit]` section (if any) to establish whether Bandit already runs in CI today (and if so, blocking or not) before writing a new job that might duplicate or conflict with it.
2. **Write `.github/security-waivers.yml`** with zero entries (an empty-but-valid `waivers: []` list) and `security_gate.py`'s schema validator (§14) against it, so the file and its consumer exist and agree on shape before any real scan job depends on them.
3. **Write `.github/scripts/security_gate.py`**, including the per-tool parsers (Bandit JSON, Semgrep SARIF, `pip-audit` JSON, `pnpm audit` JSON, Dependency-Check SARIF, Trivy SARIF), the threshold table from §3.3, the waiver-matching logic from §6.3, and its own unit tests against the fixture files in `.github/scripts/security_gate_test_fixtures/` (§14) — build and test this component in isolation before wiring it into any real GitHub Actions job, since every downstream job depends on it being correct.
4. **Add `bandit`'s SARIF extra and `pip-audit`** to `backend/pyproject.toml`'s dev-dependency group; run both locally against the current `backend/src` tree and resolve every real finding (fix it, or — only if genuinely a false positive/accepted risk — add a waiver entry) so the repo starts stage 8 from a clean baseline, exactly as item 02 required for gitleaks.
5. **Append `sast-bandit`, `sast-semgrep-backend`, `dependency-scan-backend` jobs to `backend.yml`** (needs: the earliest job that produces a usable checkout — no dependency on the build job, since none of these three need the container image), each ending in a `security_gate.py` invocation and a SARIF upload.
6. **Append `container-scan-backend` job to `backend.yml`** (needs: the stage-7 build job, consuming its image-tag output per §12).
7. **Append `backend-security-gate` aggregator job** (needs: all four jobs above).
8. **Repeat steps 4–7 for `admin-web.yml`** (Semgrep + `pnpm audit` + Trivy; no separate SAST tool addition needed since admin-web has no Bandit equivalent — Semgrep is its only SAST pass) and resolve its own clean-baseline findings.
9. **Repeat steps 4–7 for `mobile.yml`**, minus any container-scan job (mobile produces no container). Add the OWASP Dependency-Check Gradle plugin (§7.3), obtain an NVD API key, store it as a GitHub Actions secret, and resolve the clean-baseline findings.
10. **Append the three new required-status-check names to `main`'s branch protection**, alongside item 02's existing two, with "Include administrators" reconfirmed enabled (§9.1) — this is a GitHub repository setting, verified manually (or via a `gh api` script, consistent with item 03's branch-protection-as-code approach) exactly as item 02's own step 15 required.
11. **Append `/.github/security-waivers.yml @noorheroes/security-leads` to `CODEOWNERS`** (item 03's file) — confirm the `@noorheroes/security-leads` GitHub team exists or create it as part of this step.
12. **Write `security-nightly-rescan.yml`** (§7.4), including the `--file-issue-on-new` diff logic, and manually trigger it once via `workflow_dispatch` to confirm it runs end-to-end (including successfully filing a test issue against a deliberately-reintroduced known-CVE fixture, then deleting that test issue).
13. **Write `docs/runbooks/security-scan-triage.md`** (§10's escalation-path note, plus a walkthrough of reading a failed check, filing a waiver PR, and the nightly-rescan issue-triage flow).
14. **Run every test in §14's table**, including the deliberately-vulnerable canary tests, end to end, before declaring this blueprint done.

---

## 14. Testing strategy and acceptance criteria

### 14.1 `security_gate.py` unit tests

| Test | Asserts |
|---|---|
| `test_bandit_high_severity_blocks` | A Bandit finding at `severity=HIGH, confidence=HIGH` → `exit_code=1` |
| `test_bandit_low_severity_does_not_block` | A `severity=LOW` finding → `exit_code=0`, appears only in `warned` |
| `test_pip_audit_unscored_advisory_blocks` | A `pip-audit` finding with no CVSS field present → `exit_code=1` (fail-closed, §3.3) |
| `test_pip_audit_medium_cvss_warns_not_blocks` | CVSS `5.4` → appears in `warned`, `exit_code=0` if it's the only finding |
| `test_trivy_unfixed_critical_does_not_block` | A Trivy `CRITICAL` finding with `FixedVersion` empty → does not block (§3.3's `--ignore-unfixed`-equivalent logic), appears in `warned` |
| `test_active_waiver_downgrades_blocking_finding` | A `HIGH` Bandit finding matching an active, non-expired waiver entry (by `tool`+`finding_id`+file-path-in-scope) → moves from `blocking` to `warned`, `exit_code=0` |
| `test_expired_waiver_does_not_downgrade` | Same as above but `expires_date` is in the past → stays `blocking`, `exit_code=1`, `expired_waivers_hit` is non-empty |
| `test_waiver_exceeding_max_duration_rejected` | A waiver entry for a `Critical`-severity finding with `expires_date` more than 30 days after `created_date` → the waiver itself is treated as invalid (§3.4), the underlying finding stays blocking |
| `test_scope_mismatch_waiver_does_not_downgrade_different_package` | A waiver for `CVE-2026-XXXXX` scoped to `package-a` does not suppress the same CVE ID found in `package-b` |

### 14.2 CI job specs (illustrative excerpt — full jobs per §6.2/§7)

```yaml
# backend.yml — new jobs appended by this document (excerpt)
  sast-bandit:
    name: sast-bandit
    runs-on: ubuntu-latest
    needs: [lint-and-format]   # item 06's stage-1 job name — confirm exact name before wiring
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --frozen --group dev
      - run: uv run bandit -r backend/src --exit-zero --format json -o bandit.json
      - run: uv run bandit -r backend/src --exit-zero --format sarif -o bandit.sarif
      - uses: github/codeql-action/upload-sarif@v3
        with: { sarif_file: bandit.sarif }
      - run: uv run python .github/scripts/security_gate.py --tool bandit --findings bandit.json

  dependency-scan-backend:
    name: dependency-scan-backend
    runs-on: ubuntu-latest
    needs: [lint-and-format]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --frozen
      - run: uv run pip-audit --format json -o pip-audit.json || true   # never trust pip-audit's own exit code
      - run: uv run python .github/scripts/security_gate.py --tool pip-audit --findings pip-audit.json

  backend-security-gate:
    name: backend-security-gate
    runs-on: ubuntu-latest
    needs: [sast-bandit, sast-semgrep-backend, dependency-scan-backend, container-scan-backend]
    if: always()
    steps:
      - run: |
          if [ "${{ contains(needs.*.result, 'failure') }}" = "true" ]; then
            echo "One or more security scans failed — see individual job logs." && exit 1
          fi
```

### 14.3 Canary tests — proving the gate actually fires (the deliberately-vulnerable-dependency requirement)

| Canary | Mechanism | Asserts |
|---|---|---|
| **SAST canary** | On a scratch branch (never merged), temporarily add a file containing `subprocess.run(user_input, shell=True)` to `backend/src`. Push, open a throwaway PR. | `sast-bandit` reports failure (Bandit's `B602`), `backend-security-gate` reports failure, PR merge button disabled. Delete the branch after. |
| **Dependency-scan canary (the required "deliberately-vulnerable test dependency")** | On a scratch branch, temporarily add a known-vulnerable, EOL package pin to `backend/pyproject.toml`'s dev group — e.g. `requests==2.6.0` (CVE-2015-2296 class of issues; confirm at implementation time a currently-disclosed, high-severity, unambiguous CVE exists for whatever exact old pin is chosen) or, for admin-web, an old `lodash` version with a known prototype-pollution CVSS ≥ 7 advisory in devDependencies. `uv sync` / `pnpm install`, push, open a throwaway PR. | `dependency-scan-backend` (or `-admin-web`) reports failure, names the exact CVE, `{app}-security-gate` fails, merge blocked. Revert the pin and delete the branch after — never leave the vulnerable pin in any long-lived branch. |
| **Container-scan canary** | On a scratch branch, temporarily change the backend Dockerfile's base image tag to a known-old, CVE-laden tag (e.g. an old patch version of `python:3.12-slim` predating a disclosed `HIGH`/`CRITICAL` fixed-in-newer-tag CVE — confirm a concrete example at implementation time). Push, let stage 7 build it, let `container-scan-backend` scan it. | `container-scan-backend` reports failure naming the CVE and the fixed version, `backend-security-gate` fails, merge blocked. Revert and delete the branch after. |
| **Waiver-bypass-does-NOT-work canary** | On the same scratch branch as the dependency-scan canary, add a waiver entry to `.github/security-waivers.yml` for the injected CVE but **do not get it reviewed by `@noorheroes/security-leads`** (self-approve as a non-security-leads account, or leave the PR unreviewed). | The waiver-file PR itself is blocked by CODEOWNERS' required review (§3.4/§9.4) — confirming the *approval* gate, not just the scanning gate, actually holds. |
| **Admin-bypass-does-NOT-work canary** | Using an account with repository admin rights, attempt to merge any of the above throwaway PRs while its check is still red. | Merge button remains disabled / merge is rejected even for the admin account — the direct verification of §9.1's "Include administrators." |

### 14.4 Acceptance criteria (all must hold before this blueprint is considered implemented)

- All nine `security_gate.py` unit tests (§14.1) pass.
- `sast-bandit`, `sast-semgrep-backend`, `sast-semgrep-admin-web`, `sast-semgrep-mobile`, `dependency-scan-backend`, `dependency-scan-admin-web`, `dependency-scan-mobile`, `container-scan-backend`, `container-scan-admin-web` all run green against the current, real repository tree (a clean baseline — any real finding surfaced during implementation is either fixed or waived with a proper, reviewed waiver entry before this is checked off).
- All five canary tests in §14.3 pass exactly as described, including the two negative canaries (waiver bypass, admin bypass) — both must demonstrably fail to bypass the gate.
- `backend-security-gate`, `admin-web-security-gate`, `mobile-security-gate`, `gitleaks-scan`, `trufflehog-verified-scan` are all listed, verbatim, in `main`'s branch-protection required-status-checks, with "Include administrators" confirmed enabled.
- `security-nightly-rescan.yml` has been manually triggered at least once via `workflow_dispatch` and completed successfully, including a successful (then deleted) test issue-filing run.
- Every SARIF-producing job's output is visible in the repository's Security → Code scanning tab after at least one real run.

---

## 15. Production-readiness considerations

- **Pipeline wall-clock cost:** six new scanners across three workflow files adds meaningful CI time. Mitigate via: (a) `sast-*`/`dependency-scan-*` jobs run in parallel with stages 2–7 rather than serially after them (§13 step 5's `needs:` choice), since none of them need the build artifact; only `container-scan-*` genuinely needs to wait for stage 7's image; (b) each scanner's own dependency/vulnerability-DB download is cached (§11) to avoid re-fetching multi-hundred-MB datasets on every PR push; (c) if pipeline duration still becomes a bottleneck at scale, consider running the *slowest* full-repo Semgrep pass only on PRs (not every push to a feature branch) while still requiring it before merge — this is a future tuning knob, not part of this document's initial scope, and must not be implemented by weakening the blocking guarantee itself.
- **NVD API rate limits:** the OWASP Dependency-Check plugin's NVD feed access degrades sharply without an API key (§7.3) — provision the free NVD API key before mobile's dependency-scan job is expected to run reliably in CI; monitor for rate-limit-related job failures distinctly from genuine "outage" failures (§10) in the early weeks after launch.
- **Waiver debt monitoring:** the nightly re-scan's 7-day expiry warning (§11) is the primary safety net against silent waiver lapses; additionally, review the full `.github/security-waivers.yml` file as a standing agenda item in whatever recurring security-calendar process Consolidated_Blueprint_v6 §13.4 already names, so waiver accumulation is visible to more than just the automated 7-day check.
- **Cost of NVD/Semgrep/Trivy as external dependencies for CI availability:** all three (and `pip-audit`/`pnpm audit`'s registries) are external services this pipeline now depends on for every merge. §10's fail-closed design means an external outage blocks all merges platform-wide until it clears — an acceptable, deliberate trade-off for a security gate (fail closed, not open) but worth stating explicitly as an operational reality the team should expect and have a documented "known external outage, here's what we do" note for in `docs/runbooks/security-scan-triage.md`.
- **Scaling to a second/third repository or a services split:** this document's design (per-app jobs, one shared `security_gate.py` gating helper, one shared `security-waivers.yml`) is written for the current single-monorepo topology. If the modular monolith is later split into independently deployed services (per Final_Development_Prompt §2.9's stated long-term direction), `security_gate.py` and the waiver-file schema are already structured to be copy-portable to a new repo with no redesign — only the workflow YAML wiring needs to be replicated per repo.

---

## 16. Dependencies/prerequisites

- **Hard dependency:** item 06 (CI stages 1–7) — this document's jobs are appended to workflow files item 06 creates and depend on job names/outputs (the lint-stage job, the build-stage image-tag output) that only exist once item 06 is implemented. This document cannot be implemented in isolation against an empty `.github/workflows/` directory.
- **Hard dependency:** item 02 (secrets management + secret scanning) — this document's branch-protection configuration is additive to item 02's; item 02 must already have established `gitleaks-scan`/`trufflehog-verified-scan` as required checks before this document adds its own three alongside them (order matters only for the manual branch-protection-configuration step, §13 step 10 — the workflow files themselves have no runtime dependency on each other).
- **Soft dependency:** Repo item 03 (CODEOWNERS + branch protection scaffolding) — this document assumes a `CODEOWNERS` file already exists to append one line to, and assumes the `gh api`-scripted branch-protection-as-code pattern item 03 establishes is the mechanism used to apply §9.1's configuration (rather than a one-off manual UI click-through, though that remains an acceptable fallback per item 03's own Definition of Done language).
- **Soft dependency:** Infra item 04 (Terraform baseline) — `container-scan-*` jobs need the Artifact Registry repo and CI's read-scoped Workload Identity Federation binding item 04 provisions; can be authored and unit-tested (§14.1) before item 04 is complete, but cannot be exercised end-to-end against a real pushed image until it is.
- **Consumed by:** the next CI/CD blueprint in this series (stages 9–13: deploy to staging, E2E, manual promotion, production deploy, post-deploy smoke) — that document's "deploy to staging" job's `needs:` graph must include this document's three aggregator gates (in addition to item 06's stage-7 build job), so a staging deploy structurally cannot happen from a commit whose security gate never passed.

---

## 17. Definition of Done

- [ ] `.github/scripts/security_gate.py` exists, implements §3.3's threshold table and §3.4/§6.3's waiver-matching logic exactly, and its full unit-test suite (§14.1) passes.
- [ ] `.github/security-waivers.yml` exists (starting empty or with only genuinely-needed, reviewed entries), and `/.github/security-waivers.yml @noorheroes/security-leads` is present in `CODEOWNERS`.
- [ ] `backend.yml` gains `sast-bandit`, `sast-semgrep-backend`, `dependency-scan-backend`, `container-scan-backend`, `backend-security-gate` — all green against the current repo tree.
- [ ] `admin-web.yml` gains `sast-semgrep-admin-web`, `dependency-scan-admin-web`, `container-scan-admin-web`, `admin-web-security-gate` — all green.
- [ ] `mobile.yml` gains `sast-semgrep-mobile`, `dependency-scan-mobile`, `mobile-security-gate` (no container-scan job) — all green.
- [ ] `security-nightly-rescan.yml` exists, has been manually triggered at least once successfully, and its new-finding issue-filing logic has been verified (then cleaned up).
- [ ] `main`'s branch protection lists all five required checks (the two from item 02 plus this document's three aggregators) verbatim, with "Include administrators" enabled — verified by the admin-bypass canary (§14.3) actually failing to bypass.
- [ ] All five canary tests in §14.3 pass exactly as specified, including both negative canaries (waiver-approval bypass, admin bypass).
- [ ] The OWASP Dependency-Check Gradle plugin is applied and configured (`failBuildOnCVSS = 7.0f`, SARIF output), and an NVD API key is provisioned as a GitHub Actions secret.
- [ ] Every SARIF-producing job's findings are visible in the repository's Security → Code scanning tab.
- [ ] `docs/runbooks/security-scan-triage.md` exists and documents: reading a failed check, filing a waiver PR, the nightly-rescan issue-triage flow, and the external-scanner-outage escalation path.
- [ ] No `# nosec`/`# nosemgrep` inline suppression comment exists anywhere in the repository that isn't paired with a corresponding, currently-active entry in `.github/security-waivers.yml` (§10, §18 Assumption 4) — a repo-wide grep confirms this before sign-off.
- [ ] No `core-security`, `core-datastore`, or any other `core-*`/`feature/*` mobile module file has been modified by this blueprint's implementation beyond the single Gradle plugin-declaration file.

---

## 18. Assumptions or decisions the coding agent must follow

1. **SAST tool choice is Bandit (Python-primary) + Semgrep (multi-language, second pass) — not CodeQL.** CodeQL's free tier requires a public repository or GitHub Advanced Security (a paid add-on not named anywhere in the confirmed stack); Semgrep's OSS CLI covers Python/TypeScript/Kotlin from one tool with zero licensing step, consistent with this corpus's repeated preference for self-hosted/OSS tooling over a new paid vendor (§3.1). Do not substitute CodeQL without an explicit, separately-documented vendor decision.
2. **Container scanner is Trivy, not Grype.** Both are reasonable; Trivy is chosen for broader single-tool coverage (OS packages + language dependencies + optional IaC scanning) and to minimize the number of distinct scanner configurations in an already six-tool-wide stage (§3.1).
3. **Trivy's blocking rule is Critical/High-with-a-fix-available only (`--ignore-unfixed`); unfixed Critical/High findings are tracked, not blocking, and re-checked nightly.** This is a deliberate trade-off to keep the gate meaningful rather than perpetually red on unpatchable base-OS CVEs (§3.3) — do not remove `--ignore-unfixed` without also building a genuinely different unfixed-finding triage flow, since removing it as-is would make the gate un-mergeable indefinitely on a routine, expected condition.
4. **Inline suppression comments (`# nosec`, `# nosemgrep`, Trivy `.trivyignore` entries, Dependency-Check suppression-XML entries used alone) are not a valid way to silence a blocking finding.** The only sanctioned path is a reviewed `.github/security-waivers.yml` entry — this is a deliberate, non-negotiable policy choice (§10) specifically because inline comments bypass the CODEOWNERS-enforced second-reviewer requirement that makes this whole gate "non-bypassable" in more than name. Where a tool's own suppression mechanism (e.g., Dependency-Check's `suppressionFile`) is technically required to make the tool itself stop flagging something operationally, that file's entry must have a matching, currently-active `.github/security-waivers.yml` entry — `security_gate.py`'s Dependency-Check parser checks for this pairing and fails the job if a suppression exists without a matching waiver.
5. **This document assumes Bandit is not yet a CI-blocking check today** (it may already run as part of item 06's stage-2 static-analysis job in a non-blocking/advisory mode, consistent with "Backend/Admin/Mobile apps are all fully implemented already" but this specific Security Baseline item explicitly *not* being built yet). Before implementing, the coding agent MUST read item 06's actual `backend.yml` and `backend/pyproject.toml`'s `[tool.bandit]` section to confirm this assumption; if Bandit already runs as a required, blocking check under a different job name, this document's `sast-bandit` job should be reconciled with (not duplicated alongside) whatever already exists, keeping the severity-threshold policy in §3.3 as the target behavior either way.
6. **The `@noorheroes/security-leads` GitHub team is assumed to not yet exist and must be created (or confirmed to already exist) as part of implementation** (§13 step 11) — this document does not define its membership; that is an organizational decision for whoever implements this blueprint to make with the actual team, informed by who already holds the equivalent role for item 03's "blast radius" CODEOWNERS groups (JWT schema, reward ledger, upload pipeline reviewers) — likely significant membership overlap, possibly the same group, but this document does not mandate they be identical.
7. **Waiver maximum durations (30/90/180 days by severity, §3.4) are this document's concrete default**, chosen to be proportionate to blast radius (shortest for Critical) while still being long enough to be practically usable (30 days is enough time to schedule a proper fix without the waiver process becoming a rubber stamp renewed every few days) — treat this table as the enforced policy unless a future, explicitly-documented decision revises it.
8. **NVD API key provisioning (§7.3) is a manual, one-time setup step** (free self-service registration at the NVD's API portal) that must happen before mobile's dependency-scan job can run reliably — this document does not automate that registration (it cannot be automated; it's a human filling out a form), only documents that it's required and where the resulting key is stored (a GitHub Actions secret, not GCP Secret Manager, since this is a CI-only credential with no runtime application use).
9. **Pipeline job parallelization (§13 step 5, §15):** SAST and dependency-scan jobs are wired to run in parallel with stages 2–7 rather than strictly after stage 7, since they have no data dependency on the build artifact — only container-scan jobs wait on the build. This is a deliberate performance decision consistent with "stage 8" being a conceptual pipeline-stage *number*, not a literal requirement that every one of its jobs execute strictly after every job numbered lower — Final_Development_Prompt §6's stage list describes logical ordering of concerns, not a mandate that GitHub Actions' `needs:` graph be a single linear chain.

---

## AI Agent Development Prompt

You are implementing **Phase 1, CI/CD item 07** of the NoorHeroes monorepo: CI pipeline stage 8 — SAST, dependency vulnerability scanning, container image scanning, all wired as required, non-bypassable status checks, sitting alongside item 02's already-existing secret-scan checks as one unified security gate.

**Stack:** FastAPI backend (`backend/`, `uv`-managed, `pyproject.toml`/`uv.lock`), Next.js 15 admin (`admin-web/`, `pnpm`-managed), Kotlin Multiplatform/Compose Multiplatform mobile (`mobile/`, Gradle Version Catalog), GitHub Actions CI (`backend.yml`, `admin-web.yml`, `mobile.yml` — already created by item 06, whose stages 1–7 you are appending to, not replacing), branch protection on `main`.

**Before writing any code:**
1. Read item 06's actual `backend.yml`, `admin-web.yml`, `mobile.yml` in full to learn the real job names your new jobs will `needs:` reference (the lint-stage job name, the build-stage job's image-tag output variable name).
2. Read `backend/pyproject.toml`'s `[tool.bandit]` section (if any) and confirm whether Bandit already runs in CI today, and in what mode (§18 Assumption 5) — reconcile rather than duplicate.
3. Read item 02's `secret-scan.yml` and its documented branch-protection required-checks list, so you add to it, never replace it.

**What to build, in this order** (full detail in §13 of this document):
1. `.github/security-waivers.yml` (empty, schema-valid) and `.github/scripts/security_gate.py` (with its full unit-test suite, §14.1) — build and test this shared component first, in isolation.
2. Add `pip-audit` and Bandit's SARIF extra to `backend/pyproject.toml`'s dev group; resolve any real findings against the current tree to a clean baseline before proceeding.
3. Append `sast-bandit`, `sast-semgrep-backend`, `dependency-scan-backend`, `container-scan-backend`, `backend-security-gate` to `backend.yml`.
4. Append `sast-semgrep-admin-web`, `dependency-scan-admin-web`, `container-scan-admin-web`, `admin-web-security-gate` to `admin-web.yml`.
5. Add the OWASP Dependency-Check Gradle plugin (`failBuildOnCVSS = 7.0f`, SARIF output) and append `sast-semgrep-mobile`, `dependency-scan-mobile`, `mobile-security-gate` to `mobile.yml` — no container-scan job for mobile.
6. Provision an NVD API key as a GitHub Actions secret for the Dependency-Check plugin.
7. Write `security-nightly-rescan.yml` (§7.4) and manually trigger it once to confirm it works end-to-end, including a test (then deleted) issue-filing run.
8. Append `/.github/security-waivers.yml @noorheroes/security-leads` to `CODEOWNERS`; create the `@noorheroes/security-leads` GitHub team if it doesn't exist.
9. Add the five new required-status-check names (`backend-security-gate`, `admin-web-security-gate`, `mobile-security-gate`, plus reconfirming item 02's existing `gitleaks-scan`, `trufflehog-verified-scan`) to `main`'s branch protection, with "Include administrators" verified enabled.
10. Write `docs/runbooks/security-scan-triage.md`.
11. Run every canary test in §14.3, including the two negative canaries proving waiver-bypass and admin-bypass both genuinely fail.

**Hard requirements — do not deviate:**
- **Do not weaken or skip the non-bypassable requirement, for any role, including repository admins.** "Include administrators" must be enabled and verified via an actual admin-account merge attempt against a deliberately-failing check (§14.3's admin-bypass canary) — do not consider this document done on the basis of the checkbox being clicked alone; prove it with the canary.
- **The only sanctioned bypass for a blocking finding is a reviewed `.github/security-waivers.yml` entry, approved via CODEOWNERS-enforced review by `@noorheroes/security-leads`.** Never implement, and never leave in place if you find one, an inline `# nosec`/`# nosemgrep` suppression comment, a `.trivyignore` entry, or a Dependency-Check suppression-XML entry without a matching, currently-active waiver-file entry (§18 Assumption 4).
- **Never add `continue-on-error: true`, an `if:`-based actor skip, or a repo/org bypass-list entry to any of the six required checks.** If you find yourself tempted to add one to make a stubborn false positive stop blocking CI during implementation, the correct fix is a waiver-file entry, not a workflow-level escape hatch.
- **Never rename or modify item 02's `gitleaks-scan`/`trufflehog-verified-scan` jobs.** This document is additive to that gate, not a replacement.
- **Never modify any `core-*` or `feature/*` module file in `mobile/`** beyond the single Gradle file that declares the Dependency-Check plugin.
- **Never float a scanner tool version to `latest`.** Pin Bandit, Semgrep, Trivy, and the Dependency-Check plugin to exact tagged releases, matching item 02's precedent for gitleaks/trufflehog.
- **Apply the exact severity thresholds in §3.3** — do not substitute a tool's own default threshold without implementing the specific deviations this document calls for (fail-closed on unscored `pip-audit` findings; `--ignore-unfixed` for Trivy).

**How to verify you're done:** walk every checkbox in this document's §17 Definition of Done, in order, confirming each is literally true against the repository state you produced. Run `security_gate.py`'s full unit-test suite and confirm all pass. Then run the full canary sequence from §14.3 end to end: inject the deliberately-vulnerable test dependency (an old, CVE-bearing package pin — confirm a currently real, high-severity CVE exists for whichever exact package/version you choose at implementation time) on a scratch branch, open a throwaway PR, and confirm (a) the relevant `dependency-scan-*` job fails, naming the CVE, (b) the app's `*-security-gate` aggregator fails, (c) the PR's merge button is disabled, and (d) a repository-admin account still cannot merge past it. Repeat the equivalent check for the SAST canary (a `subprocess(..., shell=True)`-style pattern) and the container-scan canary (an old, CVE-laden base image tag). Confirm the two negative canaries (an unreviewed waiver-file PR staying blocked; an admin's merge attempt staying blocked) both hold. Clean up every scratch branch and throwaway PR/issue created during verification before considering this blueprint complete.
