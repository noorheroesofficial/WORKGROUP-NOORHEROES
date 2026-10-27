# K-01 — On-Device AI Logic Absence Architectural Scan

## 1. Feature Context
No new Android/KMP module is introduced by F.35 — every AI-consuming client surface (A.2's Home recommendations, A.5's coaching UI, B.13's voice search) already owns its own implementation per its respective feature document. This sub-feature is a single, cross-cutting architectural test confirming the server-authoritative AI design has no on-device escape hatch anywhere in the app.

## 2. Parent Feature
F.35 — AI Layer & Microservices Architecture

## 3. Sub-feature
2.1 On-Device AI Logic Absence Architectural Scan (ID: **K-01**)

## 4. Objective
Write one cross-cutting static-scan test over the KMP codebase confirming zero function/class name suggestive of on-device religious-answer generation, on-device content ranking, or on-device voice-cloning logic exists outside thin API-client wrapper functions.

## 5. Business Requirements
- §6.1: no new Android module is introduced; this section exists only to confirm no consuming module independently re-implements F.35's server-side guarantees on-device.
- §6.10 Testing Strategy: architectural test confirming no Android module contains a string-matching/free-text religious-answer-generation code path of its own — every religious-content interaction must route through the server-side approved-answer/scholar-handoff contract, never a client-local fallback.
- §7 Android AI Code-Generation Prompt: scan for patterns like `generateAnswer`, `localRank`, `cloneVoice` outside expected thin API-client wrapper functions, asserting NONE exist.

## 6. Existing Architecture
A shared test module (e.g., `build-logic/architecture-tests` or an equivalent convenient shared test location within the KMP project) housing cross-cutting architectural/static-analysis tests, distinct from any single `feature:*` module.

## 7. Existing Code to Reuse
- The KMP project's existing static-analysis/lint tooling (e.g., Detekt custom-rule infrastructure, if already present) — reused as the scan mechanism rather than introducing a new bespoke parser, if the project's existing tooling supports custom rule authoring.

## 8. Files to Create
- `build-logic/architecture-tests/src/test/kotlin/OnDeviceAiLogicAbsenceTest.kt` (or the equivalent path per the project's actual shared-test-module convention)
- `build-logic/architecture-tests/src/test/kotlin/OnDeviceAiLogicPatternRules.kt` — the maintained list of suspicious name patterns (`generateAnswer`, `localRank`, `cloneVoice`, and any additional patterns the team identifies as on-device-AI-escape-hatch-suggestive)

## 9. Files to Modify
None — this is an additive, standalone test with no production code changes.

## 10. KMP Requirements
- The scan walks the full KMP source tree (all `feature:*`, `core-*`, and `library:*` modules) searching function and class declarations for names matching the maintained suspicious-pattern list.
- An explicit allowlist mechanism exists for genuinely legitimate thin API-client wrapper functions whose names might otherwise superficially match a pattern (e.g., a repository method literally named `fetchGeneratedAnswer` that only calls the server API and returns its response) — allowlisted entries require a code comment justifying the exception, reviewed at allowlist-addition time, so the allowlist itself doesn't silently become the escape hatch this test is meant to prevent.
- The test fails the build if any non-allowlisted match is found.

## 11. Required API
N/A — no API surface, a static-analysis test only.

## 12. Authentication / Authorization
N/A.

## 13. Loading / Empty / Error States
N/A.

## 14. Responsive UI / Accessibility
N/A.

## 15. Localization / RTL
N/A.

## 16. Security
This test IS the security control confirming F.35's server-authoritative AI architecture has no on-device bypass — its own failure (a suspicious pattern match) is the alarm. The allowlist mechanism itself is the one component requiring ongoing discipline, since an overly permissive allowlist would defeat the test's purpose.

## 17. Testing
**Mandatory, CI-blocking:** the scan test itself — this sub-feature's entire deliverable. Additional test: the scan is proven to actually catch a deliberately-introduced violation (temporarily add a function literally named `generateAnswer` containing real logic to a throwaway branch, confirm the test fails, then revert) — a scan that can't detect a known-bad fixture provides false confidence, mirroring B-03 (F.35 Backend)'s "prove the guardrail actually catches violations" discipline.

## 18. Documentation
A comment block at the top of `OnDeviceAiLogicPatternRules.kt` explaining the rationale (server-authoritative AI architecture, zero on-device religious-answer/ranking/voice-cloning logic) and instructing future engineers to extend the pattern list rather than add allowlist exceptions when in doubt.

## 19. AI Coding Agent Implementation Steps

**Task 01 — Define the Suspicious-Pattern Rule List**
Objective: Maintained list including `generateAnswer`, `localRank`, `cloneVoice`, and any additional team-identified patterns. Files: `OnDeviceAiLogicPatternRules.kt`. Definition of Done: list reviewed and documented.

**Task 02 — Implement the Static-Scan Test**
Objective: Walks the full KMP source tree, matches declarations against the pattern list, respects the allowlist mechanism. Files: `OnDeviceAiLogicAbsenceTest.kt`. Dependencies: Task 01. Tests: this IS the test. Definition of Done: test passes against the current, clean codebase.

**Task 03 — Prove the Scan Actually Catches Violations**
Objective: Temporarily introduce a fixture violation, confirm the test fails, then revert. Dependencies: Task 02. Definition of Done: confirmed the test is not trivially passing.

**Task 04 — Register as a CI-Blocking Gate**
Objective: Ensure this test cannot be skipped/marked-ignored in the CI pipeline configuration. Dependencies: Task 02. Definition of Done: CI config confirmed non-bypassable.

**Task 05 — Document the Allowlist Discipline**
Objective: Clear rationale and review-requirement documentation for any future allowlist addition. Dependencies: Task 01. Definition of Done: doc comment present and reviewed.

**Task 06 — Final Code Review**
Objective: Confirm the pattern list is genuinely comprehensive for the three named risk categories (religious-answer generation, content ranking, voice cloning) and the allowlist contains zero unjustified entries. Definition of Done: checklist in §20 checked.

## 20. Final Verification Checklist
- [ ] Scan test is CI-blocking and non-bypassable
- [ ] Test proven to actually catch a deliberately-introduced violation, not just pass trivially
- [ ] Allowlist mechanism requires a justifying comment for every entry, reviewed at addition time
- [ ] Pattern list covers all three named risk categories (religious-answer generation, ranking, voice cloning)

## 21. Definition of Done
The KMP codebase has a continuously-verified, CI-blocking guarantee that no on-device escape hatch exists for religious-answer generation, content ranking, or voice cloning — confirming every AI-touching client surface genuinely routes through F.35's server-authoritative services.
