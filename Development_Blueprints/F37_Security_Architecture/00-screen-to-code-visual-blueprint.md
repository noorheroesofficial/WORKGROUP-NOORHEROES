# Feature F37: Security Architecture — Visual & System Blueprint

## 1. Feature Identification & Reference
- **Feature ID**: Feature F.37
- **PRD Reference**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F37_Security_Architecture.md`
- **Target Module**: `:core-security` (KMP) & `security` layer (Backend)
- **Primary Purpose**: Zero-trust architecture, multi-dimensional rate limiting, slow-hash credential storage, and hardware keystore caching.

---

## 2. Visual Security Gates & Contract Enforcement
- **Keystore / Keychain Credential Storage**: Mobile app credentials and parent tokens cached strictly inside Android Keystore / iOS Keychain.
- **Rate-Limiting UI Handling**: Multi-dimensional rate limiters return HTTP 429 with `Retry-After` header; frontend displays localized cooldown timer without freezing UI.
- **Child-Scope Isolation**: Strict domain-service re-verification guarantees that child tokens cannot access parent dashboard APIs or other siblings' learning records.
