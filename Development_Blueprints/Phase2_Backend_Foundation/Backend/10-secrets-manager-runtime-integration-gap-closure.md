# Phase 2 — Backend Config: Secrets-Manager Runtime Integration (Gap Closure)

**Blueprint ID:** `Development_Blueprints.Phase2_Backend_Foundation.Backend.10-secrets-manager-runtime-integration-gap-closure`
**Platform:** Backend (`backend/src/noorheroes/core/`)
**Phase:** Phase 2 — Backend Foundation
**Closes:** Phase 2 Backend item 03 (Config Management) — currently 🟡 **COMPLETED (partial)**: the `pydantic-settings`-based `Settings` class is built, working, and confirmed correct for Local/CI, but has never been wired to read from a live, centralized secrets manager for Staging/Production/Dev-QA.
**Depends on:**
- `Development_Blueprints.Phase1_Infra_Config.Infra.02-secrets-management-env-example-gitleaks.md` — owns the **infrastructure** side of this gap: the GCP Secret Manager vendor decision, the `infra/secrets/manifest.yaml` registry schema, per-tier IAM bindings (provisioned by Terraform, item 04), the `.env.example` convention, and mandatory gitleaks/trufflehog scanning. That document must exist and its `manifest.yaml` contract must be stable before this document's code can be implemented against it.
- The already-built `pydantic-settings` config layer (`backend/src/noorheroes/core/settings.py`), documented in `FAST-API-INSTRUCTIONS.md` §2 ("`Settings` — Pydantic settings class managing all configuration variables. Usage: Access via `settings` singleton or `get_settings()`.") and §15's Master Reference Table row (`Settings | Core Config | core/settings.py | Validated app config settings | System-wide | settings singleton`).
**Source of truth:** `FAST-API-INSTRUCTIONS.md` (existing `Settings`/`Environment` contract); `Development_Blueprints.Phase1_Infra_Config.Infra.02-secrets-management-env-example-gitleaks.md` §3.4–§3.6, §5, §6, §9 (infra-side design of the same mechanism this document implements).
**Status:** NEW — this file does not exist in the corpus today. It is a **gap-closure / integration** document, not a from-scratch build spec.

**Do not re-litigate:** The existing `Settings` class in `core/settings.py` — its field names, field types, validation rules, `SettingsConfigDict`, the `Environment` StrEnum (`LOCAL`, `DEVELOPMENT`, `STAGING`, `PRODUCTION`), and its singleton access pattern (`settings` / `get_settings()`) — is **built and confirmed working**. This document does not redesign, rename, restructure, or re-validate any of that. It specs exactly one thing: **how the process environment that `Settings()` reads gets populated, in Staging/Production/Dev-QA, from a live secrets manager, before `Settings()` is ever constructed** — i.e., the runtime wiring the already-built config layer has never had, because the secrets-manager infrastructure it would wire to did not exist until Phase 1 Infra.02 provisions it.

---

## 1. Objective and purpose

This is a **gap-closure task on top of already-working code**, not a rebuild. The `Settings` class already:
- Reads every configuration value from `os.environ` (via `pydantic-settings`'s `BaseSettings`, with `env_file=".env"` for local dev).
- Validates types, defaults, and constraints correctly.
- Is consumed correctly by every one of the 12 bounded contexts and by `main.py`.

What it has **never done** — because the infrastructure to do it did not exist until Phase 1 Infra.02 provisions GCP Secret Manager — is source its underlying environment variables from anything other than a local `.env` file or CI-injected GitHub Actions Secrets. In Staging and Production today, if those tiers were deployed, `Settings()` would either crash on missing required fields or (worse) silently fall back to insecure defaults, because nothing populates `os.environ` with real credential values before `Settings()` runs.

The objective of this document is narrow and precise: **implement the runtime secrets-source wiring** — a small, pluggable loading mechanism that runs once, at process boot, before `Settings()` is first constructed, and populates `os.environ` with the correct values for the current deployment tier:

- **Local / CI tiers:** behavior is unchanged — `.env` (local) or GitHub Actions Secrets (CI) already populate `os.environ` by the time `Settings()` runs today. This document formalizes that path as one named, explicit implementation of a loader interface (`EnvFileSecretsLoader`) rather than leaving it as implicit, undocumented behavior.
- **Staging / Production / Dev-QA tiers:** a new implementation of the same loader interface (`GCPSecretManagerLoader`) reads `infra/secrets/manifest.yaml` (owned by Phase 1 Infra.02) and fetches each listed secret from GCP Secret Manager, setting it into `os.environ` before `Settings()` is constructed.

Both implementations share one `SecretsSourceLoader` interface so the selection between them is a single runtime switch (`SECRETS_PROVIDER`), not a branch scattered through the codebase, and so a future third provider (e.g., AWS Secrets Manager, HashiCorp Vault) is a new class, not a rewrite.

**Explicitly not the objective:** rewriting `Settings`, renaming its fields, changing its validation behavior, or changing how any of the 12 bounded contexts consume `settings`/`get_settings()`. Every existing call site of `settings.<field>` continues to work identically once this document's code has run — because by the time `Settings()` is constructed, `os.environ` simply has more/different values in it than it did before boot, exactly the same input shape `pydantic-settings` has always consumed.

---

## 2. Scope and requirements

### 2.1 In scope

- A `SecretsSourceLoader` abstraction (Python `Protocol`) with exactly one method, and two concrete implementations: `EnvFileSecretsLoader` (Local/CI — effectively formalizes existing behavior) and `GCPSecretManagerLoader` (Dev-QA/Staging/Production — new).
- A factory function that selects the correct loader based on the `SECRETS_PROVIDER` env var (itself defined and defaulted by Phase 1 Infra.02 §3.6 as a new, additive `Settings` field: `secrets_provider: Literal["env", "gcp_secret_manager"] = "env"`).
- The single orchestration entrypoint, `load_secrets_into_environ()`, called once at the earliest point of `main.py`'s `lifespan()` startup — **before** the first construction of `Settings()`/`get_settings()`.
- A new, narrow exception type (`SecretsBootstrapError`) so a secrets-loading failure is unambiguous and distinguishable from an ordinary `pydantic` validation error.
- Redacted, structured startup logging (via the already-built `structlog` integration) proving which secrets were loaded — by **name only, never by value** — and from which provider.
- Unit and integration tests proving the app boots correctly from (a) a local `.env` file and (b) a mocked GCP Secret Manager client, and proving a missing/unreachable secret fails boot loudly rather than silently.
- Minimal, additive changes to `backend/src/noorheroes/core/settings.py` (one new field only, per Phase 1 Infra.02 §3.6/§12) and to `main.py` (one function call added at the top of `lifespan()`'s startup half).

### 2.2 Explicitly out of scope

- **Rewriting the existing `Settings` class structure.** No field is renamed, retyped, removed, or restructured. No change to `SettingsConfigDict`, to how `Settings` reads `.env`, or to the `Environment` StrEnum's values.
- **Provisioning the GCP Secret Manager resources, the GCP project, or IAM bindings themselves.** That is Terraform's job, driven by Phase 1 Infra.02's `infra/secrets/manifest.yaml`, and is explicitly out of scope for both that document and this one.
- **Defining the `.env.example` convention, gitleaks/trufflehog scanning, or `infra/secrets/manifest.yaml`'s schema.** All three are owned, defined, and already specified by Phase 1 Infra.02; this document consumes them as a fixed contract and does not re-specify them (see §7 for the exact contract this document depends on).
- **Live secret rotation without a redeploy.** See §11 — this is an explicit, justified MVP trade-off, not an oversight.
- **Admin-web's (`admin-web/src/lib/env.ts`) or mobile's (`local.properties`/`BuildConfig`) equivalent wiring.** Those are covered by Phase 1 Infra.02 §3.4's "Admin-web's variant" and are architecturally different (no central boot-time singleton to gate). This document is backend-only.
- **Choosing which of the manifest's listed secrets exist for which vendor (AI provider, email provider).** Vendor selection remains an open decision per `NoorHeroes_Final_Development_Prompt.md` §14; this document's code is vendor-agnostic — it loads whatever `infra/secrets/manifest.yaml` lists, by name, without caring what the secret is for.

---

## 3. Technical implementation details

### 3.1 The `SecretsSourceLoader` abstraction

A `typing.Protocol` (structural typing — no inheritance required, consistent with the "prefer composition" convention implied by the existing `BaseService`/`BaseRepository` generic-class style, but decoupled from ORM/service base classes since this runs before any of that infrastructure exists) with exactly one method:

```python
# backend/src/noorheroes/core/secrets_bootstrap.py

from typing import Protocol

class SecretsSourceLoader(Protocol):
    """
    A pluggable strategy for populating os.environ with the secret
    values a given deployment tier needs, before Settings() is
    constructed. Implementations must be idempotent (safe to call
    exactly once per process boot; never called twice in normal
    operation, but must not corrupt state if it somehow were) and
    must never log a secret value, only secret *names*.
    """

    def load(self) -> "LoadedSecretsReport":
        """
        Populates os.environ in place for every secret this loader
        is responsible for. Returns a LoadedSecretsReport describing
        what was loaded (names + counts only) for structured logging.
        Raises SecretsBootstrapError on any failure that should abort
        application startup (see §10).
        """
        ...
```

`LoadedSecretsReport` is a small, frozen dataclass — not a Pydantic model, since it never crosses a network boundary and needs no validation, only to be a safe, loggable value:

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class LoadedSecretsReport:
    provider: str                    # "env" | "gcp_secret_manager"
    secret_names_loaded: tuple[str, ...] = field(default_factory=tuple)
    secret_count: int = 0
    source_detail: str = ""          # e.g. "backend/.env" or "gcp_project=noorheroes-prod-123"
```

### 3.2 `EnvFileSecretsLoader` — Local/CI tier

```python
class EnvFileSecretsLoader:
    """
    Local/CI implementation. This is a formalization of existing,
    already-working behavior, not new logic: python-dotenv (already
    wired by the existing Settings/main.py bootstrap per
    FAST-API-INSTRUCTIONS.md) has already populated os.environ from
    backend/.env (local) or from GitHub Actions Secrets injected into
    the job's env: block (CI) by the time this loader's .load() runs.
    This loader performs NO file I/O of its own — it only reports
    what is already present, so structured startup logging is
    consistent across all providers (§3.5, §12).
    """

    def __init__(self, expected_secret_names: tuple[str, ...]) -> None:
        self._expected_secret_names = expected_secret_names

    def load(self) -> LoadedSecretsReport:
        present = tuple(
            name for name in self._expected_secret_names
            if os.environ.get(name)
        )
        return LoadedSecretsReport(
            provider="env",
            secret_names_loaded=present,
            secret_count=len(present),
            source_detail="process environment (.env / CI secrets)",
        )
```

Note this loader **never raises** on a missing secret — for Local/CI, a missing required field is caught by `Settings()`'s own Pydantic validation immediately afterward (existing, unchanged behavior, per Phase 1 Infra.02 §10's edge-case table), which already produces a clear, actionable error. Duplicating that check here would be redundant validation logic outside `Settings`'s ownership — exactly the kind of scope creep §2.2 rules out.

### 3.3 `GCPSecretManagerLoader` — Dev-QA/Staging/Production tier

```python
import yaml
from google.cloud import secretmanager
from google.api_core.exceptions import GoogleAPIError, NotFound

class GCPSecretManagerLoader:
    """
    Dev-QA/Staging/Production implementation. Reads
    infra/secrets/manifest.yaml (contract owned by Phase 1 Infra.02
    §6), filters entries whose `environments` list includes the
    current tier, and fetches each from GCP Secret Manager's
    `versions/latest`, setting os.environ[entry.env_var].
    """

    def __init__(
        self,
        environment: "Environment",
        gcp_project_id: str,
        manifest_path: Path,
        client: secretmanager.SecretManagerServiceClient | None = None,
    ) -> None:
        self._environment = environment
        self._gcp_project_id = gcp_project_id
        self._manifest_path = manifest_path
        # Injected for testability (§14) — production code path
        # constructs the real client when None.
        self._client = client or secretmanager.SecretManagerServiceClient()

    def load(self) -> LoadedSecretsReport:
        manifest = self._parse_manifest()
        tier_key = self._environment.value.lower()  # "staging" | "production" | "devqa"
        entries = [e for e in manifest if tier_key in e["environments"]]

        loaded_names: list[str] = []
        for entry in entries:
            secret_id = entry["id"]
            env_var = entry["env_var"]
            resource_name = (
                f"projects/{self._gcp_project_id}/secrets/"
                f"noorheroes-{tier_key}-{secret_id}/versions/latest"
            )
            try:
                response = self._client.access_secret_version(name=resource_name)
            except NotFound as exc:
                raise SecretsBootstrapError(
                    f"Secret '{secret_id}' (env var {env_var}) not found in "
                    f"GCP Secret Manager for tier '{tier_key}' at "
                    f"'{resource_name}'. Confirm Terraform (Phase 1 Infra.04) "
                    f"has provisioned it and the manifest entry is correct."
                ) from exc
            except GoogleAPIError as exc:
                raise SecretsBootstrapError(
                    f"GCP Secret Manager unreachable or access denied while "
                    f"fetching '{secret_id}' for tier '{tier_key}': {exc}"
                ) from exc

            os.environ[env_var] = response.payload.data.decode("utf-8")
            loaded_names.append(env_var)

        return LoadedSecretsReport(
            provider="gcp_secret_manager",
            secret_names_loaded=tuple(loaded_names),
            secret_count=len(loaded_names),
            source_detail=f"gcp_project={self._gcp_project_id}, tier={tier_key}",
        )

    def _parse_manifest(self) -> list[dict]:
        if not self._manifest_path.exists():
            raise SecretsBootstrapError(
                f"Secrets manifest not found at '{self._manifest_path}'. "
                f"This file is owned by Phase 1 Infra.02 and must be present "
                f"in the deployed container image."
            )
        try:
            raw = yaml.safe_load(self._manifest_path.read_text())
        except yaml.YAMLError as exc:
            raise SecretsBootstrapError(
                f"Secrets manifest at '{self._manifest_path}' is not valid YAML: {exc}"
            ) from exc
        return raw.get("secrets", [])
```

This is a direct implementation of the mechanism Phase 1 Infra.02 §3.4 already designed (`load_secrets_into_environ`, manifest-driven, `versions/latest`, fail-closed) — this document's contribution is turning that design into the concrete, pluggable, testable module with an explicit interface, a dedicated exception type, and a loader that a unit test can substitute a fake `SecretManagerServiceClient` into without any network access (§14).

### 3.4 Factory — selecting the loader

```python
def get_secrets_loader(
    *,
    secrets_provider: str,
    environment: "Environment",
    gcp_project_id: str | None,
    expected_secret_names: tuple[str, ...],
    manifest_path: Path,
) -> SecretsSourceLoader:
    if secrets_provider == "env":
        return EnvFileSecretsLoader(expected_secret_names=expected_secret_names)
    if secrets_provider == "gcp_secret_manager":
        if not gcp_project_id:
            raise SecretsBootstrapError(
                "SECRETS_PROVIDER=gcp_secret_manager requires GCP_PROJECT_ID "
                "to be set (it is read directly from os.environ, not from "
                "Settings, since it is needed before Settings() can be "
                "constructed)."
            )
        return GCPSecretManagerLoader(
            environment=environment,
            gcp_project_id=gcp_project_id,
            manifest_path=manifest_path,
        )
    raise SecretsBootstrapError(
        f"Unknown SECRETS_PROVIDER '{secrets_provider}'. Expected 'env' or "
        f"'gcp_secret_manager'."
    )
```

### 3.5 Orchestration entrypoint

```python
import structlog

logger = structlog.get_logger(__name__)

_DEFAULT_MANIFEST_PATH = Path(__file__).resolve().parents[4] / "infra" / "secrets" / "manifest.yaml"

def load_secrets_into_environ(*, manifest_path: Path = _DEFAULT_MANIFEST_PATH) -> LoadedSecretsReport:
    """
    The single entrypoint called once, at the very start of
    lifespan()'s startup half, before Settings()/get_settings() is
    first constructed anywhere in the process. Reads SECRETS_PROVIDER,
    ENVIRONMENT, and GCP_PROJECT_ID directly from os.environ (not from
    a Settings instance — none exists yet), selects and runs the
    appropriate loader, logs a redacted summary, and returns the
    report. Raises SecretsBootstrapError on any failure, which the
    caller (main.py) does not catch — an uncaught exception here
    aborts ASGI startup, which is the intended fail-closed behavior.
    """
    secrets_provider = os.environ.get("SECRETS_PROVIDER", "env")
    environment = Environment(os.environ.get("ENVIRONMENT", "local"))
    gcp_project_id = os.environ.get("GCP_PROJECT_ID")

    loader = get_secrets_loader(
        secrets_provider=secrets_provider,
        environment=environment,
        gcp_project_id=gcp_project_id,
        expected_secret_names=_CREDENTIAL_ENV_VAR_NAMES,
        manifest_path=manifest_path,
    )

    report = loader.load()

    logger.info(
        "secrets_bootstrap.completed",
        provider=report.provider,
        environment=environment.value,
        secret_count=report.secret_count,
        secret_names=list(report.secret_names_loaded),  # names only — never values
        source_detail=report.source_detail,
    )
    return report
```

`_CREDENTIAL_ENV_VAR_NAMES` is the fixed tuple of credential-bearing variable names from `backend/.env.example`'s `# CREDENTIAL`-tagged lines (Phase 1 Infra.02 §7.2) — e.g. `("JWT_SIGNING_KEY", "DATABASE_URL", "R2_SECRET_ACCESS_KEY", "R2_ACCESS_KEY_ID", "OPENAI_API_KEY", ...)`. Keep this tuple and `.env.example`'s `# CREDENTIAL` tags in sync manually until/unless a future blueprint automates it; it is used only for `EnvFileSecretsLoader`'s informational report, never for validation (§3.2).

### 3.6 Why a `Protocol`, not an ABC

`typing.Protocol` is chosen over `abc.ABC` deliberately: it lets `EnvFileSecretsLoader` and `GCPSecretManagerLoader` be plain classes with no shared base class or import-time coupling, keeps the test doubles in §14 trivial (any object with a `.load() -> LoadedSecretsReport` method satisfies the type, including a lambda-backed stub), and matches the codebase's existing preference for structural typing at integration boundaries (mirrors how `AIProvider` implementations are selected via `AIProviderFactory.get_provider()` per FAST-API-INSTRUCTIONS.md §4 — this document's `get_secrets_loader()` is the same factory pattern applied to a second, unrelated pluggable-provider boundary).

---

## 4. Architecture and component responsibilities

```
┌───────────────────────────────────────────────────────────────────────┐
│  main.py :: lifespan(app)  — startup half, FIRST LINE                 │
│                                                                         │
│      load_secrets_into_environ()                                      │
│               │                                                        │
│               ▼                                                        │
│      get_secrets_loader(SECRETS_PROVIDER, ENVIRONMENT, ...)            │
│               │                                                        │
│      ┌────────┴─────────┐                                              │
│      ▼                  ▼                                              │
│  EnvFileSecretsLoader   GCPSecretManagerLoader                         │
│  (env == "env")         (env == "gcp_secret_manager")                  │
│      │                  │                                              │
│      │            reads infra/secrets/manifest.yaml                   │
│      │                  │                                              │
│      │            calls GCP Secret Manager                             │
│      │            (google-cloud-secret-manager SDK)                    │
│      │                  │                                              │
│      └────────┬─────────┘                                              │
│               ▼                                                        │
│      os.environ[...] populated (both paths converge on the same       │
│      side effect: real values sitting in the process environment)     │
│               │                                                        │
│               ▼                                                        │
│      structlog: "secrets_bootstrap.completed" (names + counts only)   │
│               │                                                        │
│               ▼                                                        │
│      Settings() / get_settings() constructed for the FIRST time       │
│      — reads os.environ exactly as it already does today, UNCHANGED   │
│               │                                                        │
│               ▼                                                        │
│      init_telemetry(), rest of lifespan() startup — UNCHANGED         │
└───────────────────────────────────────────────────────────────────────┘
```

| Component | Owns | Does NOT own |
|---|---|---|
| `SecretsSourceLoader` (Protocol) | The one-method interface every provider implementation satisfies | Any concrete fetching logic |
| `EnvFileSecretsLoader` | Reporting what's already in `os.environ` for Local/CI | File-loading `.env` itself (that remains `python-dotenv`'s existing, unchanged job) |
| `GCPSecretManagerLoader` | Fetching manifest-listed secrets from GCP Secret Manager into `os.environ` | Provisioning the GCP secrets, IAM bindings, or the manifest file's schema (Phase 1 Infra.02 / Terraform item 04) |
| `get_secrets_loader()` | Runtime provider selection (the one branch point in the whole system) | Anything about *what* a provider does once selected |
| `load_secrets_into_environ()` | Orchestration, structured logging, the single call site `main.py` invokes | Constructing `Settings` (unchanged — `core/settings.py`'s job) |
| `SecretsBootstrapError` | Signaling a fatal, boot-aborting secrets failure distinctly from a Pydantic validation error | Retry logic (none — see §10) |
| `core/settings.py` (existing, unmodified except §12) | Interpreting `os.environ` into a validated `Settings` instance | Knowing or caring where `os.environ`'s values came from |

---

## 5. Folder/file structure

```
backend/
├── src/noorheroes/
│   ├── core/
│   │   ├── settings.py                 # MODIFY — add `secrets_provider` field ONLY (§12); zero other changes
│   │   ├── secrets_bootstrap.py        # NEW — SecretsSourceLoader Protocol, EnvFileSecretsLoader,
│   │   │                                #        GCPSecretManagerLoader, get_secrets_loader(),
│   │   │                                #        load_secrets_into_environ(), SecretsBootstrapError,
│   │   │                                #        LoadedSecretsReport (this document's entire deliverable)
│   │   └── exceptions.py               # MODIFY — add SecretsBootstrapError export if the codebase
│   │                                     #        convention centralizes exception exports here; otherwise
│   │                                     #        define it directly in secrets_bootstrap.py (confirm
│   │                                     #        the existing convention before choosing — see §18)
│   └── main.py                          # MODIFY — one call added: load_secrets_into_environ() as the
│                                          #        first statement inside lifespan()'s startup half
└── tests/
    └── core/
        └── test_secrets_bootstrap.py    # NEW — unit + integration tests (§14)
```

No files outside `backend/` are created or modified by this document. `infra/secrets/manifest.yaml` is read by this document's code but is neither created nor owned here — it is Phase 1 Infra.02's deliverable, consumed as a read-only contract.

---

## 6. APIs, models, interfaces, and data flow

This is a boot-time internal integration, not an HTTP-facing feature — there are no new endpoints. The "interfaces" are the Python contracts in §3, and the "data flow" is:

**Local/CI boot:**
`main.py` process starts → `python-dotenv` loads `backend/.env` (unchanged, existing behavior) → `lifespan()` startup begins → `load_secrets_into_environ()` → `SECRETS_PROVIDER` read from `os.environ` (defaults to `"env"`) → `EnvFileSecretsLoader.load()` → reports what's present, mutates nothing → `structlog` logs `secrets_bootstrap.completed` (`provider="env"`) → `Settings()` constructed, reading `os.environ` exactly as before → rest of `lifespan()` proceeds unchanged.

**Staging/Production/Dev-QA boot:**
Container starts (zero secret values baked into the image) → `lifespan()` startup begins → `load_secrets_into_environ()` → `SECRETS_PROVIDER=gcp_secret_manager` (set by Cloud Run's deploy-time env var config, per Phase 1 Infra.02 §3.6, owned by Terraform/item 04 or the deploy workflow/item 08) → `GCPSecretManagerLoader.load()` → parses `infra/secrets/manifest.yaml` → filters to current tier → for each entry, `SecretManagerServiceClient.access_secret_version(...)` → `os.environ[env_var] = value` → `structlog` logs `secrets_bootstrap.completed` (`provider="gcp_secret_manager"`, secret **names** only) → `Settings()` constructed, now reading a fully-populated `os.environ` → rest of `lifespan()` proceeds unchanged.

**Failure data flow (either tier):** any exception inside `load_secrets_into_environ()` is a `SecretsBootstrapError`, uncaught by `main.py`, which propagates out of `lifespan()`'s startup generator — FastAPI/Uvicorn treats this as a failed ASGI lifespan startup and the process exits non-zero before binding to a port. Cloud Run's health check then reports the revision unhealthy and does not route traffic to it (§10).

---

## 7. Dependencies and configuration requirements

### 7.1 The contract this document depends on (owned by Phase 1 Infra.02 — do not redefine here)

- `infra/secrets/manifest.yaml`'s schema: `version`, `secrets[]` with `id`, `env_var`, `environments[]`, `owner`, `rotation_cadence_days`, `description` (Phase 1 Infra.02 §6).
- GCP Secret Manager resource naming: `noorheroes-{env}-{secret-id}` (Phase 1 Infra.02 §3.4, §6).
- The `secrets_provider: Literal["env", "gcp_secret_manager"] = "env"` field on `Settings` (Phase 1 Infra.02 §3.6, §12) — this document's code reads the **raw env var** `SECRETS_PROVIDER` directly (not `settings.secrets_provider`) precisely because no `Settings` instance exists yet at the point this code must run; the field's existence on `Settings` afterward is for the rest of the app (e.g., a `/readyz` diagnostic, §9) to introspect which provider was active, not for this module's own bootstrap logic to depend on.
- `GCP_PROJECT_ID` env var, present only when `SECRETS_PROVIDER=gcp_secret_manager` (Phase 1 Infra.02 §7.2).

### 7.2 New Python dependencies (backend/pyproject.toml)

| Package | Scope | Reason |
|---|---|---|
| `google-cloud-secret-manager` | Main dependency (needed at runtime in Staging/Production/Dev-QA, not just dev) | `GCPSecretManagerLoader`'s SDK client — already listed as a dependency by Phase 1 Infra.02 §7.1; this document is the consumer that actually imports and uses it |
| `PyYAML` | Main dependency, only if not already present transitively | Manifest parsing in `GCPSecretManagerLoader._parse_manifest()` |
| `structlog` | Already a dependency (existing `StructuredLoggingMiddleware` per FAST-API-INSTRUCTIONS.md §4) | Redacted startup logging (§3.5, §12) — no new dependency, new usage only |

No new dependency is introduced solely for `EnvFileSecretsLoader` — it uses only `os` (stdlib).

### 7.3 Configuration this document reads (all already defined by `.env.example` per Phase 1 Infra.02 §7.2 — reproduced here only as the exact set this module's code touches)

```
SECRETS_PROVIDER=env                # env | gcp_secret_manager — the switch (§3.4)
ENVIRONMENT=local                   # local | development | staging | production
GCP_PROJECT_ID=                     # required only when SECRETS_PROVIDER=gcp_secret_manager
```

---

## 8. Database/storage requirements

None. This document introduces no database tables, no migrations, and no new persistent storage. `infra/secrets/manifest.yaml` is a git-tracked, plaintext, name-only YAML file (no secret values) read at boot; GCP Secret Manager itself is the only "storage" involved, and it is provisioned and owned entirely by Phase 1 Infra.02 / Terraform (item 04), not by this document.

---

## 9. Authentication, authorization, validation, and security considerations

- **No secret value is ever logged.** `load_secrets_into_environ()`'s structured log line (`secrets_bootstrap.completed`) carries `secret_names` (a list of env var *names*, e.g. `["JWT_SIGNING_KEY", "DATABASE_URL"]`) and `secret_count`, never `secret_values`. This is enforced by construction — `LoadedSecretsReport` has no field that could ever hold a value, only names/counts/provider strings — so there is no `structlog` processor a future change could accidentally misconfigure into leaking a value; the data simply never reaches the logger in the first place. Code review for any change to this module must reject any diff that adds a value-bearing field to `LoadedSecretsReport` or passes a raw secret string to `logger.info(...)`.
- **No secret is ever committed.** `secrets_bootstrap.py` itself contains zero literal secret values, by design — it contains only code that reads names from a manifest and fetches values from a live service at runtime. This module is, itself, exactly the kind of file gitleaks (Phase 1 Infra.02 §3.1) scans on every commit; because it structurally cannot contain a real credential (it only ever handles `os.environ` mutations and SDK calls), it should never trigger a finding — if a future edit to this file ever does trigger a gitleaks finding, that is a strong signal the edit introduced a hardcoded value that does not belong here.
- **IAM / service-account scoping is Phase 1 Infra.02's responsibility, not re-specified here** — but this module's design assumes and depends on it: `GCPSecretManagerLoader` performs no IAM logic itself; it relies entirely on the ambient credentials of the Cloud Run service account it runs under (Application Default Credentials, resolved automatically by `SecretManagerServiceClient()`'s default constructor — no service-account key file is ever read or embedded by this code). If that service account lacks `roles/secretmanager.secretAccessor` on a given secret, `access_secret_version` raises a `PermissionDenied` (a subtype of `GoogleAPIError`), which this module wraps into `SecretsBootstrapError` exactly like a `NotFound` (§3.3) — from this module's perspective, "doesn't exist" and "exists but I can't read it" are both fatal, fail-closed conditions, and the distinction is diagnosed from the wrapped exception's original type/message in the log, not handled differently by the loader.
- **Least-privilege boundary respected, not re-implemented:** this module fetches exactly the secrets listed for the *current* tier in the manifest (`tier_key in entry["environments"]`) — it does not, and structurally cannot, fetch a secret belonging to a different tier, because the resource name it constructs (`noorheroes-{tier_key}-{secret_id}`) is derived from the running process's own `ENVIRONMENT` value, not from any user input or request-scoped data. There is no code path in this module reachable from an HTTP request.
- **`SECRETS_PROVIDER` and `GCP_PROJECT_ID` are themselves non-secret** (Phase 1 Infra.02 §3.6 explicitly documents them as such in `.env.example`) — they identify *how* to fetch secrets, not a credential themselves, and are safe to log, safe to set as plain Cloud Run environment variables (not Cloud Run secret references), and safe to appear in `secrets_bootstrap.completed`'s log line.
- **Fail-closed, not fail-open, on every error path** — see §10. There is no "continue with an empty/default value" branch anywhere in `GCPSecretManagerLoader`; every exception either propagates as `SecretsBootstrapError` or the loader has fully succeeded.

---

## 10. Error handling and edge cases

| Scenario | Behavior | Why |
|---|---|---|
| GCP Secret Manager unreachable at boot (network partition, transient outage) | `GoogleAPIError` caught, wrapped into `SecretsBootstrapError`, propagates uncaught out of `lifespan()` — process fails to start | Never serve traffic with an unpopulated `os.environ`; Cloud Run's health check marks the revision unhealthy and does not cut traffic over from the previous good revision |
| A manifest entry names a secret that doesn't exist yet in GCP Secret Manager for the current tier | `NotFound` caught, wrapped into `SecretsBootstrapError` naming the specific `secret_id` and `resource_name` | A precise, actionable error (not a generic crash) — points directly at Terraform/item 04 as the fix, per the message text in §3.3 |
| Service account lacks IAM permission on a specific secret | `PermissionDenied` (a `GoogleAPIError` subtype) — same wrapped-and-abort path as unreachable | Indistinguishable from "doesn't exist" by design (§9) — both are fatal, both need a human to fix infra before the app can boot |
| `infra/secrets/manifest.yaml` missing from the deployed image | `SecretsBootstrapError` raised explicitly by `_parse_manifest()` before any GCP call is attempted | Fails fast on a packaging/build mistake rather than silently loading zero secrets and letting `Settings()` fail later with a less specific error |
| `infra/secrets/manifest.yaml` present but malformed YAML | `yaml.YAMLError` caught, wrapped into `SecretsBootstrapError` with the parse error included | Same fail-fast rationale |
| A required secret is present in the manifest for the tier but `Settings()` still fails validation afterward (e.g., the fetched value doesn't satisfy a Pydantic constraint — wrong format, empty string) | `Settings()` raises its own, existing, unchanged `pydantic.ValidationError` — this module does not attempt to validate secret *content*, only to ensure the *env var is set* | Preserves the existing, working separation of concerns: `secrets_bootstrap.py` is about *presence and source*, `Settings` is about *shape and validity* — exactly the boundary §1 and §2.2 establish |
| Secret rotated in GCP Secret Manager while the app is already running | **No effect on the running process** — `versions/latest` was resolved once, at that process's boot, and cached implicitly in `os.environ`/`Settings()`'s already-constructed instance for the process's lifetime | See §11 for the full state-management rationale; a rotation takes effect only on the next boot/redeploy, which is a stated, justified MVP trade-off, not a bug |
| `SECRETS_PROVIDER` set to an unrecognized value (typo, e.g. `"gcp"` instead of `"gcp_secret_manager"`) | `get_secrets_loader()` raises `SecretsBootstrapError` immediately, before any network call | Fails at the cheapest possible point — a config typo should never manifest as a mysterious downstream GCP client error |
| `SECRETS_PROVIDER=gcp_secret_manager` but `GCP_PROJECT_ID` unset | `get_secrets_loader()` raises `SecretsBootstrapError` immediately (§3.4) | Same fail-fast rationale — this is a deploy-config mistake, not a runtime condition to tolerate |
| Local developer accidentally sets `SECRETS_PROVIDER=gcp_secret_manager` in their local `.env` | `GCPSecretManagerLoader` attempts a real GCP call using the developer's own `gcloud` Application Default Credentials (if any) — if they lack access, it fails loudly with `SecretsBootstrapError`, which is the correct behavior (no silent fallback to `env` mode) rather than a confusing partial success | `.env.example`'s default (`SECRETS_PROVIDER=env`) is the documented, correct local value (Phase 1 Infra.02 §7.2); this is a documentation/onboarding concern, not something this module should special-case around |

---

## 11. State management and lifecycle considerations

**Decision: secrets are loaded exactly once, at boot — not hot-reloadable. This document does not implement live rotation.**

Justification:
1. **Consistency with `Settings`'s existing lifecycle.** `Settings`/`get_settings()` is already a boot-time-constructed singleton (per FAST-API-INSTRUCTIONS.md §2, accessed as `settings` — implying a module-level instance, or via a cached `get_settings()`). Making the *secrets feeding into it* hot-reloadable while `Settings` itself is a fixed singleton would be incoherent — a rotated secret would sit in `os.environ` with no mechanism to re-flow into the already-constructed, presumably-cached `Settings` instance without also solving `Settings`'s own reconstruction, which is out of this document's scope (§2.2 — "not a redesign of pydantic-settings").
2. **Matches the deployment model.** Cloud Run (the compute target per Phase 1 Infra.02 §3.4) already performs rolling redeploys on every new revision. A rotated secret naturally reaches all replicas on the *next* deploy — which, per the secret-rotation runbook Phase 1 Infra.02 §15/§10 establishes, is the intended, documented mechanism: rotate the secret in GCP Secret Manager, then trigger a redeploy (even a no-op revision bump) to pick it up. This document's `load_secrets_into_environ()` runs identically on that redeploy — no special "rotation mode" is needed, because every boot already re-fetches `versions/latest` fresh.
3. **Avoids a much larger, unscoped problem.** True hot-reload would require: a background polling/watch mechanism (GCP Secret Manager has no native push-notification-on-rotation for a general SDK client without wiring Pub/Sub separately), a thread-safe way to swap `Settings`'s field values under concurrent request handling (some fields, like `database_url` or `jwt_signing_key`, are unsafe to change under a live connection pool/active token verification without a coordinated drain), and a decision about partial-rotation windows (old JWTs signed with the previous key must still verify during a rollover). All of that is a distinct, much larger feature — explicitly flagged as future work, not silently punted.
4. **Fail-closed at boot is a stronger guarantee than best-effort hot-reload for this system's risk profile.** A children's-safety-focused product (per the project's overall PRD emphasis on child protection and content safety) benefits more from "the app refuses to start with wrong/missing credentials" than from "the app keeps running on a stale credential it silently never refreshed" — hot-reload without careful design risks exactly that silent-staleness failure mode.

This is stated explicitly so a future coding agent does not attempt to add polling/hot-reload as an unrequested enhancement: if live rotation becomes a requirement, it is a new, separately-scoped blueprint, not an extension folded into this one.

---

## 12. Integration points with existing modules

- **`core/settings.py` (`Settings` class, already built) — the primary integration point.** This document's code runs, completes, and returns *before* `Settings()`/`get_settings()` is constructed anywhere in the process. By the time `Settings` reads `os.environ`, it is indistinguishable from `os.environ` having been populated by a `.env` file directly — `Settings`'s own field-reading, validation, and defaulting logic requires **zero changes** beyond the one additive field Phase 1 Infra.02 §3.6/§12 already specifies (`secrets_provider: Literal["env", "gcp_secret_manager"] = "env"`), added purely so the rest of the running app can introspect which provider was active (e.g., surfaced on an internal diagnostics endpoint or in a structured log context processor), not because `Settings` itself needs to *act* on it — the acting already happened in `secrets_bootstrap.py`, earlier in the boot sequence.
- **`main.py`'s `lifespan()` (already built).** Exactly one line is added, as the first statement of the startup half, ahead of `init_telemetry()`:
  ```python
  async def lifespan(app: FastAPI):
      # --- startup ---
      load_secrets_into_environ()   # NEW — must run before get_settings()/Settings() is
                                     # first touched anywhere below, including transitively
                                     # via init_telemetry() or any module-level import that
                                     # triggers Settings() construction.
      init_telemetry()
      ...
      yield
      # --- shutdown --- (unchanged)
  ```
  **Confirm before implementing:** if any module-level code (an import-time `settings = Settings()` at the top of another module imported before `lifespan()` runs) already constructs `Settings()` eagerly at import time rather than lazily inside `lifespan()`, `load_secrets_into_environ()` must instead be called at the top of `main.py`'s module body, before that import — or such an eager import must be identified and deferred. This is called out explicitly because it is the one way this integration could silently fail to take effect in Staging/Production despite being "wired": Python's own module-execution order determines this, not this document's code. Locate every `Settings()`/`get_settings()` call site (`grep -rn "Settings()\|get_settings()" backend/src/`) before writing the integration line, and confirm the earliest one is reached only after `load_secrets_into_environ()` has run.
- **`structlog` (already built, `StructuredLoggingMiddleware` per FAST-API-INSTRUCTIONS.md §4).** `secrets_bootstrap.py` uses the same `structlog.get_logger(__name__)` pattern already established elsewhere in the codebase — no new logging configuration, processors, or sinks are introduced. The one new log event, `secrets_bootstrap.completed`, follows whatever redaction/PII-processor chain the existing `structlog` configuration already applies globally (Phase 1 Infra.02 §9's "Redaction cross-check" flags this same processor chain as the place a `JWT_SIGNING_KEY`/`R2_SECRET_ACCESS_KEY`-shaped value should also be caught if it ever reached a log call by accident elsewhere — this module's own log call structurally never passes such a value, per §9 above, so it does not depend on that redaction processor for its own safety, only benefits from it as defense in depth).
- **`core/exceptions.py` (already built, existing `DomainError` hierarchy).** `SecretsBootstrapError` is **not** a `DomainError` subclass — `DomainError` and its subclasses (`NotFoundError`, `ValidationError`, etc., per FAST-API-INSTRUCTIONS.md §2) are explicitly HTTP-response-mapped exceptions raised inside request-handling code (services/repositories) and translated to HTTP status codes by existing exception-handler middleware. `SecretsBootstrapError` is raised during process boot, before any HTTP request-handling infrastructure exists, and must never be caught by an HTTP exception handler — it should propagate all the way to process exit. Define it as a plain `Exception` subclass local to `secrets_bootstrap.py` (or in `core/exceptions.py` alongside the others **only** if the existing file's docstring/module comment establishes it as a general "all core exceptions live here" convention rather than specifically "all HTTP-mapped domain exceptions live here" — confirm this against the actual file content before deciding placement, per §18).
- **Phase 1 Infra.02's `infra/secrets/manifest.yaml` and `.gitleaks.toml`.** This document's code is a *consumer* of the manifest (read-only, §7.1) and is itself *subject to* the gitleaks scan Phase 1 Infra.02 establishes (§9 above) — no special exemption or allowlist entry is needed or should be added for `secrets_bootstrap.py`, `test_secrets_bootstrap.py`, or this document itself.
- **Terraform / Phase 1 Infra.04 (not yet built).** No direct code integration — this document's `GCPSecretManagerLoader` will fail with a clear `SecretsBootstrapError` (§10) if item 04 has not yet provisioned the secrets it expects, which is the correct, informative failure mode rather than a silent no-op.

---

## 13. Development steps in the correct implementation order

1. **Confirm the exact existing contract before writing any code:**
   - Read `backend/src/noorheroes/core/settings.py` in full. Note the exact `Settings` field names/types already present, the `Environment` StrEnum's exact member names, whether `Settings` is a plain class instantiated once at module scope (`settings = Settings()`) or built lazily via a `@lru_cache()`-decorated `get_settings()`, and whether `SettingsConfigDict(env_file=".env")` (or equivalent) is already configured.
   - `grep -rn "Settings()\|get_settings()" backend/src/` to find every call site and confirm none of them run at import time before `lifespan()` (§12).
   - Read `infra/secrets/manifest.yaml` (once Phase 1 Infra.02 has produced it) to confirm its exact schema matches §7.1's assumed shape.
2. **Add the `secrets_provider` field to `Settings`** (Phase 1 Infra.02 §3.6/§12) — the single additive change: `secrets_provider: Literal["env", "gcp_secret_manager"] = "env"`. Run the existing test suite to confirm zero regressions from this one-field addition.
3. **Add `google-cloud-secret-manager` and `PyYAML` (if missing) to `backend/pyproject.toml`.** Lock/sync dependencies (`uv sync` or the project's existing dependency-management command).
4. **Write `backend/src/noorheroes/core/secrets_bootstrap.py`** implementing, in this order (each independently testable before moving to the next): `LoadedSecretsReport` → `SecretsBootstrapError` → `SecretsSourceLoader` Protocol → `EnvFileSecretsLoader` → `GCPSecretManagerLoader` → `get_secrets_loader()` → `load_secrets_into_environ()`.
5. **Write `backend/tests/core/test_secrets_bootstrap.py`** (§14) alongside step 4, not after — each class/function above should have its test(s) written before moving to the next, per the project's implied TDD-friendly structure (small, isolated units).
6. **Wire the single call into `main.py`'s `lifespan()`** (§12), placed and verified per the confirmation done in step 1.
7. **Local verification:** run the backend locally with `SECRETS_PROVIDER=env` (the `.env.example` default) — confirm the app boots identically to before this change, and confirm the new `secrets_bootstrap.completed` log line appears with `provider="env"`.
8. **Mocked-Staging verification:** using the test double from §14's integration test, or manually with a local GCP service-account key against a real Dev-QA GCP project (once Phase 1 Infra.04's Terraform has provisioned at least one real secret there), set `SECRETS_PROVIDER=gcp_secret_manager` and `GCP_PROJECT_ID` locally and confirm a real `access_secret_version` round-trip succeeds and the corresponding `Settings` field reads the fetched value correctly.
9. **Negative-path verification:** deliberately misconfigure (wrong `GCP_PROJECT_ID`, or point at a tier with no provisioned secrets) and confirm the process fails to boot with a clear `SecretsBootstrapError` message, not a hang or a silent partial start.
10. **Update `backend/.env.example`'s comment block (if not already covering this)** to note that `SECRETS_PROVIDER`/`GCP_PROJECT_ID` are read directly by `secrets_bootstrap.py` before `Settings` exists — a one-line comment addition, not a new file (the file itself is owned by Phase 1 Infra.02; coordinate rather than duplicate).
11. **Run the full existing backend test suite** to confirm no regression anywhere else in the 12 bounded contexts — this change should be invisible to every module that isn't `main.py`, `settings.py`, or the new test file.

---

## 14. Testing strategy and acceptance criteria

### 14.1 Unit tests — `EnvFileSecretsLoader`

```python
def test_env_file_loader_reports_present_secrets(monkeypatch):
    monkeypatch.setenv("JWT_SIGNING_KEY", "test-value-not-a-real-secret")
    monkeypatch.delenv("DATABASE_URL", raising=False)

    loader = EnvFileSecretsLoader(expected_secret_names=("JWT_SIGNING_KEY", "DATABASE_URL"))
    report = loader.load()

    assert report.provider == "env"
    assert "JWT_SIGNING_KEY" in report.secret_names_loaded
    assert "DATABASE_URL" not in report.secret_names_loaded
    assert report.secret_count == 1
```

### 14.2 Unit tests — `GCPSecretManagerLoader` (mocked SDK client, no network)

```python
class _FakeSecretManagerClient:
    def __init__(self, values: dict[str, str], missing: set[str] = frozenset()):
        self._values = values
        self._missing = missing

    def access_secret_version(self, name: str):
        secret_id = name.split("/secrets/noorheroes-staging-")[1].split("/versions")[0]
        if secret_id in self._missing:
            raise NotFound(f"secret {secret_id} not found")
        payload = types.SimpleNamespace(data=self._values[secret_id].encode("utf-8"))
        return types.SimpleNamespace(payload=payload)


def test_gcp_loader_sets_environ_from_manifest(tmp_path, monkeypatch):
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(yaml.dump({
        "version": 1,
        "secrets": [
            {"id": "jwt-signing-key", "env_var": "JWT_SIGNING_KEY",
             "environments": ["staging", "production"], "owner": "backend-platform",
             "rotation_cadence_days": 90, "description": "test"},
        ],
    }))
    fake_client = _FakeSecretManagerClient(values={"jwt-signing-key": "fetched-secret-value"})
    loader = GCPSecretManagerLoader(
        environment=Environment.STAGING,
        gcp_project_id="noorheroes-staging-123",
        manifest_path=manifest,
        client=fake_client,
    )

    report = loader.load()

    assert os.environ["JWT_SIGNING_KEY"] == "fetched-secret-value"
    assert report.secret_count == 1
    assert report.provider == "gcp_secret_manager"


def test_gcp_loader_raises_on_missing_secret(tmp_path):
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(yaml.dump({
        "version": 1,
        "secrets": [
            {"id": "jwt-signing-key", "env_var": "JWT_SIGNING_KEY",
             "environments": ["staging"], "owner": "backend-platform",
             "rotation_cadence_days": 90, "description": "test"},
        ],
    }))
    fake_client = _FakeSecretManagerClient(values={}, missing={"jwt-signing-key"})
    loader = GCPSecretManagerLoader(
        environment=Environment.STAGING,
        gcp_project_id="noorheroes-staging-123",
        manifest_path=manifest,
        client=fake_client,
    )

    with pytest.raises(SecretsBootstrapError, match="jwt-signing-key"):
        loader.load()
```

### 14.3 Integration test — full boot from local `.env` (Acceptance Criterion A)

```python
def test_app_boots_from_local_env_file(monkeypatch, tmp_path):
    """
    Proves the app boots correctly end-to-end using the local .env
    tier — SECRETS_PROVIDER unset (defaults to "env"), all required
    Settings fields sourced from process env vars exactly as today.
    """
    monkeypatch.setenv("ENVIRONMENT", "local")
    monkeypatch.delenv("SECRETS_PROVIDER", raising=False)  # exercise the default
    monkeypatch.setenv("JWT_SIGNING_KEY", "local-test-signing-key")
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://test:test@localhost/test")
    # ... remaining required fields per the real Settings class

    report = load_secrets_into_environ()

    assert report.provider == "env"
    settings = Settings()  # must not raise
    assert settings.jwt_signing_key == "local-test-signing-key"
```

### 14.4 Integration test — full boot from a mocked secrets manager (Acceptance Criterion B)

```python
def test_app_boots_from_mocked_gcp_secret_manager(monkeypatch, tmp_path):
    """
    Proves the app boots correctly end-to-end using the
    gcp_secret_manager tier, with a fake SDK client standing in for
    GCP — no real network call, no real GCP project required for this
    test to run in CI.
    """
    monkeypatch.setenv("ENVIRONMENT", "staging")
    monkeypatch.setenv("SECRETS_PROVIDER", "gcp_secret_manager")
    monkeypatch.setenv("GCP_PROJECT_ID", "noorheroes-staging-test")

    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(yaml.dump({
        "version": 1,
        "secrets": [
            {"id": "jwt-signing-key", "env_var": "JWT_SIGNING_KEY",
             "environments": ["staging"], "owner": "backend-platform",
             "rotation_cadence_days": 90, "description": "test"},
            {"id": "database-url", "env_var": "DATABASE_URL",
             "environments": ["staging"], "owner": "backend-platform",
             "rotation_cadence_days": 180, "description": "test"},
        ],
    }))
    fake_client = _FakeSecretManagerClient(values={
        "jwt-signing-key": "gcp-fetched-signing-key",
        "database-url": "postgresql+asyncpg://staging:pw@staging-host/noorheroes",
    })

    # Dependency-injected: load_secrets_into_environ accepts an
    # optional loader override for exactly this kind of test, OR the
    # test monkeypatches GCPSecretManagerLoader's client construction
    # — pick one pattern and use it consistently; DI is preferable.
    loader = GCPSecretManagerLoader(
        environment=Environment.STAGING,
        gcp_project_id="noorheroes-staging-test",
        manifest_path=manifest,
        client=fake_client,
    )
    report = loader.load()

    assert report.provider == "gcp_secret_manager"
    settings = Settings()  # must not raise; reads the now-populated os.environ
    assert settings.jwt_signing_key == "gcp-fetched-signing-key"
```

### 14.5 Security/redaction test

```python
def test_secrets_bootstrap_never_logs_secret_values(monkeypatch, caplog):
    monkeypatch.setenv("ENVIRONMENT", "local")
    monkeypatch.setenv("JWT_SIGNING_KEY", "super-secret-value-must-never-appear-in-logs")

    load_secrets_into_environ()

    log_text = caplog.text
    assert "super-secret-value-must-never-appear-in-logs" not in log_text
    assert "JWT_SIGNING_KEY" in log_text  # the NAME is expected to appear
```

### 14.6 Acceptance criteria (summary)

- [ ] **A.** A test proves the app boots correctly (constructs `Settings()` without error) sourcing all config from a local `.env`-equivalent process environment, with `SECRETS_PROVIDER` at its default (`"env"`).
- [ ] **B.** A test proves the app boots correctly sourcing all config from a mocked GCP Secret Manager client (no real network/GCP project dependency in CI), with `SECRETS_PROVIDER=gcp_secret_manager`.
- [ ] **C.** A test proves an unreachable/erroring GCP Secret Manager client causes `SecretsBootstrapError`, not a silent fallback or an ambiguous crash.
- [ ] **D.** A test proves a manifest entry with no corresponding secret raises `SecretsBootstrapError` naming the specific missing secret.
- [ ] **E.** A test proves no secret value ever appears in a captured log line, only secret names.
- [ ] **F.** The full existing backend test suite passes unchanged after this integration — zero regressions in any of the 12 bounded contexts.
- [ ] **G.** `backend/.env.example`'s existing drift-check (`check_env_example_sync.py`, Phase 1 Infra.02 §3.3) still passes after the one-field `Settings` addition.

---

## 15. Production-readiness considerations

- **Crash-and-restart-loop is the intended failure mode, not a bug to smooth over.** If Staging/Production secrets are misconfigured, the correct operational signal is a red/unhealthy Cloud Run revision with a clear `SecretsBootstrapError` message in the boot logs — not a degraded-but-running app. On-call runbooks should treat "revision fails health check immediately after deploy" plus a `secrets_bootstrap`-tagged log line as a specific, fast-diagnosis category, distinct from a generic crash.
- **Cold-start latency:** `GCPSecretManagerLoader.load()` adds one network round-trip per manifest entry to Cloud Run cold-start time. For a manifest with a handful of entries (§6's example lists four), this is on the order of tens to low hundreds of milliseconds total — acceptable for Cloud Run's boot budget, but if the manifest grows large, consider (as a documented future optimization, not required at MVP) batching via `access_secret_version` calls issued concurrently (`asyncio.gather` equivalent, or the sync client's thread-pool) rather than sequentially, since Cloud Run's own scale-to-zero cold-start cost already dominates.
- **Observability:** the `secrets_bootstrap.completed` structured log event (§3.5) should be surfaced in whatever log-based alerting Staging/Production already has (Phase 1 Infra.02's Observability item, `05-observability-stack-bootstrap.md`) as a simple "did this fire within N seconds of container start" liveness signal — its *absence* on a revision that otherwise looks like it started is itself a diagnostic clue (e.g., the process crashed before even reaching this log line, versus crashing after it).
- **Dev-QA is treated identically to Staging/Production for this module's purposes** (per Phase 1 Infra.02 §3.5's tier table) — there is no special-cased "Dev-QA is more lenient" branch anywhere in `secrets_bootstrap.py`; the only per-tier variation is which manifest entries match `tier_key in entry["environments"]`.
- **No secret ever appears in a build artifact.** Confirm as part of any CI/CD pipeline work (item 06/08) that the container build step for `backend/` never sets a `SECRETS_PROVIDER=gcp_secret_manager`-triggering call during the *build* (only at *runtime*, post-deploy) — this module's code only runs inside `lifespan()`, which never executes during `docker build`, so this is structurally already satisfied, but worth a one-line note in the Dockerfile's comments per Phase 1 Infra.02's "zero secret values baked into the image" guarantee (§3.4 point 4).

---

## 16. Dependencies/prerequisites

- `Development_Blueprints.Phase1_Infra_Config.Infra.02-secrets-management-env-example-gitleaks.md` fully authored and its `infra/secrets/manifest.yaml` schema stable (this document's `GCPSecretManagerLoader` is written against that exact schema — §7.1).
- The already-built `backend/src/noorheroes/core/settings.py` and `Environment` StrEnum (confirmed working per FAST-API-INSTRUCTIONS.md).
- `google-cloud-secret-manager` and `PyYAML` added to `backend/pyproject.toml` (§7.2).
- For the *real* (non-mocked) Staging/Production verification step (§13 step 8) only — not required for the unit/integration test suite itself (§14), which is fully mockable: Phase 1 Infra.04's Terraform must have provisioned at least the GCP project, one `google_secret_manager_secret` resource, and the relevant `roles/secretmanager.secretAccessor` IAM binding for a real end-to-end smoke test to be possible. This document's code, tests, and CI can all be completed and merged before that infra exists — only the final live-environment smoke test is blocked on it.

---

## 17. Definition of Done

- [ ] `backend/src/noorheroes/core/secrets_bootstrap.py` exists, implementing `LoadedSecretsReport`, `SecretsBootstrapError`, `SecretsSourceLoader`, `EnvFileSecretsLoader`, `GCPSecretManagerLoader`, `get_secrets_loader()`, `load_secrets_into_environ()` exactly as specified in §3.
- [ ] `backend/src/noorheroes/core/settings.py` has exactly one new field (`secrets_provider`) added; no existing field renamed, retyped, or removed; a diff review confirms this.
- [ ] `backend/src/noorheroes/main.py` calls `load_secrets_into_environ()` as the first statement of `lifespan()`'s startup half, confirmed (via the §12/§13-step-1 grep) to run before any `Settings()`/`get_settings()` construction anywhere in the process.
- [ ] All tests in §14 exist and pass, including both Acceptance Criteria A and B (boots from local `.env` AND from a mocked secrets manager).
- [ ] The full pre-existing backend test suite passes with zero regressions.
- [ ] No secret value appears in any log output, confirmed by §14.5's test.
- [ ] `backend/.env.example`'s drift-check (owned by Phase 1 Infra.02) still passes after the one-field `Settings` addition.
- [ ] Code review confirms `SecretsBootstrapError` is not a `DomainError` subclass and is never caught by HTTP-layer exception handling.
- [ ] This document's scope boundary is respected: no PR implementing this document touches `.gitleaks.toml`, `.pre-commit-config.yaml`, `infra/secrets/manifest.yaml`'s schema, or any file under `admin-web/`/`mobile/` (all owned by Phase 1 Infra.02 or other documents).

---

## 18. Assumptions or decisions the coding agent must follow

1. **The existing `Settings` class's field names, field types, and the `Environment` StrEnum's member names are fixed and must not change.** This document assumes `Environment.LOCAL`, `Environment.DEVELOPMENT`, `Environment.STAGING`, `Environment.PRODUCTION` exist exactly as named per FAST-API-INSTRUCTIONS.md §2 — if the real `settings.py` differs in casing or naming, adapt this document's code to match the real names; do not rename the real enum/class to match this document's examples.
2. **`GCP_PROJECT_ID` and `SECRETS_PROVIDER` are read directly from `os.environ`, never from a `Settings` instance**, because no `Settings` instance exists at the point they're needed (§7.1). This is intentional, not an inconsistency with "use `Settings` everywhere" — it is the one necessarily-bootstrapped exception, and should be commented as such in the code.
3. **GCP Secret Manager is the assumed vendor**, per Phase 1 Infra.02 §3.4's explicit default decision. If the infra team later confirms a different vendor (AWS Secrets Manager, HashiCorp Vault), only `GCPSecretManagerLoader` is replaced with a new class satisfying the same `SecretsSourceLoader` protocol and `get_secrets_loader()`'s branch is extended — `Settings`, `EnvFileSecretsLoader`, `load_secrets_into_environ()`'s signature, and every call site remain untouched. This is the entire reason the Protocol-based pluggable design exists (§3.6) rather than hardcoding GCP calls directly into `main.py`.
4. **Dev-QA is treated as a `GCPSecretManagerLoader`-backed tier**, identically to Staging/Production, per Phase 1 Infra.02 §3.5 — do not add a third loader implementation or a special case for Dev-QA.
5. **No hot-reload / live rotation is implemented.** This is a deliberate MVP decision with its rationale documented in §11 — do not add polling, file-watching, or a Pub/Sub-triggered refresh as an unrequested enhancement.
6. **`SecretsBootstrapError` placement (`core/exceptions.py` vs. local to `secrets_bootstrap.py`) is decided by inspecting the real `core/exceptions.py`'s existing convention** (§12) — if it is documented/organized specifically as "HTTP-mapped `DomainError` subclasses," define `SecretsBootstrapError` locally in `secrets_bootstrap.py` instead of adding it there. Do not make `SecretsBootstrapError` a `DomainError` subclass regardless of placement — it must never be HTTP-response-mapped, since it can only ever occur before any HTTP request-handling exists.
7. **The `_CREDENTIAL_ENV_VAR_NAMES` tuple (§3.5)** used by `EnvFileSecretsLoader`'s reporting is maintained by hand, kept in sync with `.env.example`'s `# CREDENTIAL`-tagged lines (Phase 1 Infra.02 §7.2) — this is informational/logging-only and never gates `Settings()` construction (that remains Pydantic's own validation, unchanged), so a temporarily-stale list is a cosmetic logging gap, not a correctness bug.
8. **This document's tests must not require real network access or a real GCP project to run in CI.** Every test in §14 either uses `monkeypatch` for env vars or a fake/stub SDK client (§14.2's `_FakeSecretManagerClient`) — the only real-GCP verification step is §13's step 8, an explicit manual/pre-production smoke-test step, not part of the automated test suite gating merges.

---

## AI Agent Development Prompt

You are implementing a narrow, well-scoped **gap-closure integration**, not a redesign. Read this entire document first, then follow it exactly.

**Context:** NoorHeroes's backend (`backend/src/noorheroes/`) already has a fully working, `pydantic-settings`-based `Settings` class in `core/settings.py`, with an `Environment` StrEnum (`LOCAL`, `DEVELOPMENT`, `STAGING`, `PRODUCTION`) and existing `settings`/`get_settings()` access patterns. It works correctly today for Local/CI, reading `os.environ`/a local `.env` file. **You must not touch this class's existing field names, field types, validation logic, or access pattern.** Your job is to build the missing piece: a mechanism that populates `os.environ` from GCP Secret Manager, at boot, before `Settings()` is ever constructed, for Staging/Production/Dev-QA tiers — while leaving Local/CI behavior completely unchanged.

**Before writing any code:**
1. Open and read the real `backend/src/noorheroes/core/settings.py` in full. Confirm the exact `Environment` enum member names and the exact `Settings` construction pattern (module-level singleton vs. `@lru_cache()`-decorated factory).
2. Run `grep -rn "Settings()\|get_settings()" backend/src/` and confirm no call site constructs `Settings` at import time before `main.py`'s `lifespan()` startup runs. If one does, note it — you will need to place your new bootstrap call before that import instead of inside `lifespan()`.
3. Open `infra/secrets/manifest.yaml` if it already exists in the repo (produced by the sibling document `Development_Blueprints.Phase1_Infra_Config.Infra.02-secrets-management-env-example-gitleaks.md`) and confirm its schema matches §7.1 above. If the file doesn't exist yet, implement against the schema exactly as documented in §6/§7.1 of this file — it is a stable, already-authored contract even if the physical file hasn't been created by another workstream yet.

**What to build, in order (full detail in §3–§5, §13):**
1. Add exactly one new field to `Settings`: `secrets_provider: Literal["env", "gcp_secret_manager"] = "env"`. Nothing else in `settings.py` changes.
2. Add `google-cloud-secret-manager` and `PyYAML` (if not already present) to `backend/pyproject.toml`.
3. Create `backend/src/noorheroes/core/secrets_bootstrap.py` containing: `LoadedSecretsReport` (frozen dataclass), `SecretsBootstrapError` (plain exception — placement decided per §18 point 6), `SecretsSourceLoader` (a `typing.Protocol` with one method, `load() -> LoadedSecretsReport`), `EnvFileSecretsLoader` (Local/CI — reports what's already in `os.environ`, does no fetching), `GCPSecretManagerLoader` (Staging/Production/Dev-QA — parses `infra/secrets/manifest.yaml`, fetches each tier-matching entry from GCP Secret Manager via `access_secret_version`, sets `os.environ[env_var]`, fails closed with `SecretsBootstrapError` on any error), `get_secrets_loader(...)` (factory selecting the loader by `SECRETS_PROVIDER`), and `load_secrets_into_environ()` (the single orchestration entrypoint that reads `SECRETS_PROVIDER`/`ENVIRONMENT`/`GCP_PROJECT_ID` directly from `os.environ`, runs the selected loader, logs a redacted `structlog` summary — secret **names** and counts only, never values — and returns the report).
4. Add exactly one call, `load_secrets_into_environ()`, as the first statement of `main.py`'s `lifespan()` startup half — placed and verified per step 2 above.
5. Write `backend/tests/core/test_secrets_bootstrap.py` covering every case in §14: `EnvFileSecretsLoader` unit tests, `GCPSecretManagerLoader` unit tests using a fake/stub SDK client (no real network), a full-boot integration test from a local-`.env`-style environment (Acceptance Criterion A), a full-boot integration test from a mocked GCP Secret Manager (Acceptance Criterion B), a missing-secret failure test, an unreachable-Secret-Manager failure test, and a test proving no secret value ever appears in captured log output.

**What you must NOT do:**
- Do not rename, retype, or remove any existing `Settings` field.
- Do not change the `Environment` enum's member names or values.
- Do not change how any of the 12 bounded contexts (`modules/identity/`, `modules/content/`, etc.) or any existing service/repository consumes `settings`/`get_settings()` — this integration must be invisible to them.
- Do not implement live secret rotation / hot-reload / polling — secrets load once, at boot, by design (§11). If you find yourself adding a background task, a watcher, or a cache-invalidation mechanism for this, stop — it is out of scope.
- Do not log, print, or otherwise surface any secret's actual value anywhere, including in exception messages (`SecretsBootstrapError` messages must name the secret **id**/**env var name**, never its fetched value).
- Do not create, modify, or duplicate `.gitleaks.toml`, `.pre-commit-config.yaml`, `infra/secrets/manifest.yaml`'s schema, or any `admin-web/`/`mobile/` file — all owned by the Phase 1 Infra.02 document.
- Do not add a new HTTP endpoint, router, or `DomainError` subclass for this — it is a boot-time-only concern.

**How to verify you're done (§14.6, §17):**
- Run the full existing backend test suite — zero regressions.
- Run your new `test_secrets_bootstrap.py` — every case in §14 passes, with no real network or GCP credentials required.
- Manually boot the app locally with `SECRETS_PROVIDER` unset (defaulting to `env`) and confirm it starts exactly as it did before your change, with a new `secrets_bootstrap.completed` log line showing `provider="env"`.
- Manually run your mocked-GCP integration test (or a local script exercising `GCPSecretManagerLoader` against the fake client) and confirm `Settings()` correctly reflects a value that came from the fake secrets-manager fetch, not from any `.env` file.
- Grep your own diff for any literal secret value, and confirm `git diff` contains none — this file and its tests must contain zero real credentials, only fakes/placeholders like `"test-value-not-a-real-secret"`.
- Confirm `backend/.env.example`'s drift-check still passes after your one-field `Settings` addition (run `backend/scripts/check_env_example_sync.py` if it already exists in the repo).
