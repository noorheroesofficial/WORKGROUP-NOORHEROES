# Phase 3 — core-security: Architecture & Bootstrap Blueprint

`Development_Blueprints.Phase3_Shared_Core_Modules.KMP.08-core-security-module-bootstrap.md`

**Module:** `core-security` (KMP Android & iOS)  
**Phase:** 3 — Shared/Core Modules  
**Status:** ✅ **Implemented & Verified** (Verified against `NoorHeroes/core/core-security/CORE_SECURITY_INSTRUCTIONS.md`)  
**Description:** Hardware-backed secure credential storage (Android Keystore, iOS Keychain), `TokenStore`, auth elevation state machine, and PIN hashing verification.  
**Depends on:** Phase 0 Workspace, Phase 2 Security Baseline Prerequisites  
**Consumed by:** All Phase 4, Phase 5, Phase 6, Phase 8, and Phase 10 feature implementations  
**Source of truth:** `NoorHeroes/core/core-security/CORE_SECURITY_INSTRUCTIONS.md`; `NoorHeroes_Consolidated_Execution_Blueprint.md` §4  

---

## 1. Objective and Purpose
Guard sensitive auth tokens, parent PINs, and session identifiers inside hardware-backed secure storage, adhering to COPPA, GDPR-K, and OWASP mobile standards.

## 2. Technical Requirements
- Hardware Storage: `EncryptedSharedPreferences` backed by Android Keystore; iOS Keychain Services with `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly`.
- `TokenStore`: Manages access token, rotating refresh token, and ephemeral Parent Gate step-up elevation tokens (15-minute hard TTL).
- `CredentialHasher`: Local slow-hash verification utility for offline Parent PIN evaluation.

## 3. Technology Stack Preservation
- AndroidX Security Crypto, iOS Security Framework.

## 4. Verification and Acceptance Criteria
- [x] Tokens cannot be extracted via rooted/jailbroken debug inspection.
- [x] Zero biometric template data transmitted or stored.

