> [!NOTE]
> **@deprecated**: For the latest unified 4D rate limiting specifications and Redis sliding-window algorithms, please see [`NoorHeroes-Backend/MASTER-README.md`](../../NoorHeroes-Backend/MASTER-README.md#11-security-authentication--authorization-architecture).

# Multi-Dimensional Rate Limiting Architecture & Runbook (F.37 / Blueprint B-07)

## 1. Executive Summary & Security Objectives
The NoorHeroes API platform implements a **Four-Dimensional Sliding-Window Rate Limiting Engine** at the outer edge middleware layer backed by Redis sorted sets (`ZREMRANGEBYSCORE`, `ZADD`, `ZCARD`, `EXPIRE`) executing within atomic single-roundtrip `MULTI`/`EXEC` pipelines.

Per **PRD FR-15, §3.4, §3.5**, rate limiting applies independently across:
1. **Device ID** (`X-Device-ID`)
2. **Client IP** (`X-Forwarded-For` / `request.client.host`)
3. **Phone Number** (Normalized E.164 extracted from unauthenticated auth request payloads)
4. **Account / Family ID** (Bound to authenticated session state)

> [!IMPORTANT]
> **Single-Dimension Rotation Resistance**: Rate limiting is never a single-dimension check alone. An attacker rotating their IP address via a proxy pool, generating random hardware identifiers, or targeting multiple accounts remains strictly constrained by the remaining static dimensions under independent **AND semantics**.

---

## 2. Four-Dimensional Extraction & Normalization Specification

```
                         ┌────────────────────────────────────────┐
                         │           Incoming HTTP Request        │
                         └───────────────────┬────────────────────┘
                                             │
         ┌──────────────────┬────────────────┴────────────────┬──────────────────┐
         ▼                  ▼                                 ▼                  ▼
   [ Device ID ]       [ Client IP ]                   [ Phone Number ]    [ Account ID ]
  Header:             Header / Socket:                JSON Request Body:   Request State:
  - X-Device-ID       - X-Forwarded-For               - "phone"            - state.family_id
  - x-device-id         (left-most IP)                - "phoneNumber"      - state.user_id
                      - request.client.host           - "phone_number"     - state.parent_sub
                                                      - "contact"          - state.account_id
                                                      (E.164 normalized)
```

### Extraction Logic & Fallbacks
1. **Device Identifier**: Extracted from `X-Device-ID` or `x-device-id`. If omitted on public endpoints, the device check is safely bypassed while IP and Phone checks are enforced.
2. **Client IP Address**: Extracted from the left-most entry in `X-Forwarded-For` to identify the originating client behind reverse proxies (Cloudflare, AWS ALB), with fallback to `request.client.host` or `"127.0.0.1"`.
3. **Phone Number**: Safely extracted via regex from incoming JSON payloads on authentication and OTP verification endpoints (`/auth/register`, `/auth/login`, `/auth/challenge`). Automatically stripped of non-digit/non-plus characters and formatted to international E.164.
4. **Account Identifier**: Extracted from `request.state` populated by upstream authentication filters (`family_id`, `user_id`, `parent_sub`).

---

## 3. Canonical Rate Limiting Matrix (§3.4)

| Profile Key | Matched Routes | Device Limit | IP Limit | Phone Limit | Account Limit | Fail Policy (Outage) |
|---|---|---|---|---|---|---|
| `auth_register` | `POST /v1/identity/auth/register` | 5 / 3600s (5/hr) | 5 / 3600s (5/hr) | 3 / 300s (3/5min) | — | **Fail-Closed** (HTTP 503) |
| `auth_login` | `POST /v1/identity/auth/login`, `/login/json` | 10 / 3600s (10/hr) | 10 / 3600s (10/hr) | 5 / 300s (5/5min) | 10 / 3600s (10/hr) | **Fail-Closed** (HTTP 503) |
| `auth_refresh` | `POST /v1/identity/auth/refresh` | 30 / 3600s (30/hr) | 60 / 3600s (60/hr) | — | 30 / 3600s (30/hr/user) | **Fail-Closed** (HTTP 503) |
| `auth_verify_email`| `POST /v1/identity/auth/verify-email` | 10 / 3600s (10/hr) | 10 / 3600s (10/hr) | — | 10 / 3600s (10/hr) | **Fail-Closed** (HTTP 503) |
| `auth_challenge` | `POST /v1/identity/auth/challenge`, `/otp` | 5 / 60s | 20 / 60s | 3 / 300s | — | **Fail-Closed** (HTTP 503) |
| `authenticated_write` | `POST`, `PUT`, `PATCH`, `DELETE` | 60 / 60s | 120 / 60s | — | 100 / 60s | **Fail-Closed** (HTTP 503) |
| `authenticated_read` | `GET`, `HEAD`, `OPTIONS` | 120 / 60s | 300 / 60s | — | 300 / 60s | **Fail-Open** (HTTP 200 + Log) |
| `admin_write` | `/v1/admin/*` mutations | 30 / 60s | 60 / 60s | — | 50 / 60s | **Fail-Closed** (HTTP 503) |

---

## 4. Single-Roundtrip Atomic Sliding Window Algorithm

To prevent Redis connection saturation under heavy burst traffic, all active dimension keys are evaluated in a single Redis `MULTI`/`EXEC` pipeline:

```python
async def check_and_increment_multi(self, items: List[Tuple[str, int, int]]) -> RateLimitResult:
    now = time.time()
    pipe = self.redis.pipeline(transaction=True)

    for key, limit, window_seconds in items:
        window_start = now - window_seconds
        pipe.zremrangebyscore(key, "-inf", window_start) # 1. Prune expired hits
        pipe.zadd(key, {f"{now}_{secrets.token_hex(4)}": now}) # 2. Record current hit
        pipe.zcard(key)                                  # 3. Read current window count
        pipe.expire(key, window_seconds)                 # 4. Refresh Redis TTL

    results = await pipe.execute()
    # Evaluate count <= limit across all dimensions with AND semantics
```

---

## 5. Resilience & Outage Policies

When Redis is unreachable (e.g. failover, network partition, timeout):
- **Fail-Closed (`fail_policy = "closed"`)**: For authentication and data mutation routes (`auth_register`, `auth_login`, `auth_refresh`, `authenticated_write`, `admin_write`), requests are rejected with **HTTP 503 Service Unavailable** (`code: "SERVICE_UNAVAILABLE"`) to prevent unthrottled brute-force or database DDoS.
- **Fail-Open (`fail_policy = "open"`)**: For non-critical catalog reads (`authenticated_read`), requests are allowed through with structured warning logs to maintain user experience.

---

## 6. Security & Privacy Controls
1. **Zero Plaintext PII in Logs**: Phone numbers and raw authentication secrets are stripped before structured logging.
2. **Gateway Purity**: Middleware performs zero domain model queries, zero database operations, and zero domain claim authorization branching (`scopes`, `role`, `mode`).
3. **Standardized Rejection Headers**:
   - `HTTP 429 Too Many Requests`
   - `Retry-After: <seconds>` header computed as the maximum window among breached dimensions.
   - Universal localized JSON error envelope (`{"error": {"code": "RATE_LIMITED", ...}}`).

---

## 7. Operations & Troubleshooting Runbook

### Metric Observability
- Prometheus metric `HTTP_REQUESTS_TOTAL{status="429"}` tracks rate limit breaches by route.
- Prometheus metric `HTTP_REQUESTS_TOTAL{status="503"}` tracks Redis outage fail-closed responses.

### Emergency Bypass
To temporarily disable rate limiting during disaster recovery or load testing:
```bash
# Set environment variable
RATE_LIMIT_ENABLED=false
```
Or toggle dynamically via `settings.rate_limit_enabled = False`.
