# K-01 — Shared Mastery Engine Core Module

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). This is the foundational `:core:mastery-engine` KMP module — the shared Android/iOS layer every domain feature module (A.5's `:feature:learn`, and future domains) consumes for mastery data access, mirroring the `:core:quiz-engine` pattern already established for Feature A.8.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
K-01 — Shared Mastery Engine Core Module (Shared Core Module)

## 4. Objective
Stand up `:core:mastery-engine` with `MasteryRepository`, score-free DTOs, Hilt DI wiring, Retrofit networking against B-04/B-05/B-06, and Room caching — the dependency every other KMP sub-feature in this feature (K-02 through K-06) and every domain consumer builds on.

## 5. Business Requirements
- FR-3: no raw numeric mastery/confidence field anywhere client-side, enforced structurally in the DTOs themselves (Android AI Prompt item 2).
- NFR-Extensibility: consumed by `:feature:learn` today, designed for future domain modules to adopt without new engine work.
- Architecture requirement (A.9 PRD §6.1): module mirrors `:core:quiz-engine`'s established pattern.

## 6. Existing Architecture
NoorHeroes KMP app: Kotlin, Jetpack Compose, MVVM, Clean Architecture (data/domain/presentation layers), Hilt DI, Retrofit+OkHttp networking, Room local database, Navigation-Compose. `:core:quiz-engine` (built for A.8) is the direct architectural precedent this module mirrors. Reference `CORE_NETWORK_INSTRUCTIONS.md`, `CORE_DATABASE_INSTRUCTIONS.md`, `CORE_DATA_INSTRUCTIONS.md`, `CORE_DESIGNSYSTEM_INSTRUCTIONS.md` for the established conventions this module must follow.

## 7. Existing Code to Reuse
- `:core:network`'s Retrofit/OkHttp client setup and auth-header interceptor (child-session Bearer token attachment) — do not build a parallel network client.
- `:core:database`'s Room setup conventions (DAO patterns, migration strategy).
- `:core:quiz-engine`'s module structure as the direct template (Gradle module setup, DI module registration, package layout) — mirror it rather than inventing a new layout.
- `:core:design-system` (dependency, not modified here).

## 8. Files to Create
- `core/mastery-engine/build.gradle.kts` — module definition, dependencies on `:core:design-system`, `:core:network`, `:core:database`.
- `core/mastery-engine/src/commonMain/kotlin/.../data/MasteryApi.kt` — Retrofit interface (`getResult`, `getSkillStates`, `postReviewDue`).
- `core/mastery-engine/src/commonMain/kotlin/.../data/MasteryRepository.kt` — interface.
- `core/mastery-engine/src/commonMain/kotlin/.../data/MasteryRepositoryImpl.kt` — implementation (remote + Room cache).
- `core/mastery-engine/src/commonMain/kotlin/.../data/dto/SkillStateDto.kt` — `skill_node_id`, `state`, `domain` — **no score field declared**.
- `core/mastery-engine/src/commonMain/kotlin/.../data/dto/QuizResultDto.kt` — `strengths`, `next_step`, `has_mistakes`, `mistake_question_ids`.
- `core/mastery-engine/src/commonMain/kotlin/.../data/db/SkillNodeStateEntity.kt` — Room entity for cached skill states.
- `core/mastery-engine/src/commonMain/kotlin/.../data/db/MasteryDao.kt`
- `core/mastery-engine/src/commonMain/kotlin/.../di/MasteryEngineModule.kt` — Hilt module.
- `core/mastery-engine/src/commonTest/kotlin/.../data/MasteryRepositoryTest.kt`
- `core/mastery-engine/src/commonTest/kotlin/.../dto/DtoReflectionNoScoreFieldTest.kt`

## 9. Files to Modify
- `settings.gradle.kts` — register the new `:core:mastery-engine` module.
- `:feature:learn/build.gradle.kts` — add dependency on `:core:mastery-engine` (replacing any direct-to-network mastery calls A.5 may have made before this module existed).

## 10. Backend Requirements
N/A (this is the KMP client sub-feature; backend endpoints B-04/B-05/B-06 already specified).

## 11. KMP Requirements
- **`MasteryApi`:** Retrofit interface with suspend functions mapping to `GET /v1/mastery/result/{attemptId}`, `GET /v1/mastery/skills`, `POST /v1/mastery/review-due`.
- **`MasteryRepository`:** `getResult(attemptId): QuizResultDto`, `getSkillStates(domain): List<SkillStateDto>`, `getReviewDue(childId): List<DueSkillDto>` — remote-first with Room-cached fallback for `getSkillStates` (offline-first per A.9 PRD §6.7), remote-only (no cache) for `getResult` (server-computed feedback, requires connectivity per K-04's design).
- **DTOs:** `SkillStateDto` and any other public data class in this module must contain NO field of numeric type named matching `/score|confidence/i` — enforced by a reflection-based unit test (Android AI Prompt item 2).
- **Room caching:** `SkillNodeStateEntity`/`MasteryDao` cache the last-synced `skill_node_state` per child/skill for offline display (K-04 consumes this).
- **Hilt DI:** `MasteryEngineModule` provides `MasteryApi`, `MasteryRepository`, `MasteryDao` bindings, following `:core:quiz-engine`'s existing DI module structure.

## 12. NextJS Requirements
N/A.

## 13. API Contract
Consumes B-04 (`POST /v1/mastery/evidence` — server-side only, not called from this module), B-05 (`GET /v1/mastery/skills`), B-06 (`GET /v1/mastery/result/{attempt_id}`), B-07 (`POST /v1/mastery/review-due`) exactly as specified in those blueprints — this module must not invent additional fields beyond those response contracts.

## 14. Database Requirements
Room: `skill_node_state` cache table (child-scoped, `skill_node_id`, `state`, `domain`, `synced_at`) — local mirror of B-05's response shape, no score field locally either.

## 15. Validation
DTO parsing via Retrofit's Moshi/kotlinx.serialization converter (whichever the platform standard is per `CORE_NETWORK_INSTRUCTIONS.md`); malformed responses surface as a typed `MasteryApiException`, not a raw parse crash.

## 16. Authentication
Reuses `:core:network`'s existing Bearer-token attachment interceptor (child-session scope) — no new auth logic in this module.

## 17. Authorization
N/A at this layer (server enforces family/session scoping per B-04/B-05/B-06).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Network failure on `getSkillStates` | Fall back to Room-cached last-synced state, surface a "may be outdated" signal to the ViewModel layer (consumed by K-03's renderer) |
| Network failure on `getResult` | Propagate as a typed error to K-02's ViewModel — no cache fallback (this data requires a live server computation) |
| Malformed/unexpected API response shape | Typed `MasteryApiException`, logged via `:core:logger`, does not crash the app |

## 19. Offline First
`getSkillStates` is offline-capable via Room cache (remote-first, cache-fallback). `getResult` is NOT offline-capable by design (server-computed) — K-04 owns the offline-completion interim-state handling around this constraint.

## 20. Local Data
Room `SkillNodeStateEntity` mirrors B-05's response shape exactly (no score field locally, consistent with the server-side guarantee — defense in depth, not just convenience).

## 21. Localization
N/A directly in this module (raw state enums/domain keys only; human-readable label mapping and localization happen in K-03's renderer and K-02's screen).

## 22. RTL
N/A (data layer, no UI in this module).

## 23. Analytics
N/A directly (K-05 owns the shared analytics interface; this module exposes data K-05's callers consume).

## 24. Performance
Room queries indexed on `(childId, domain)` equivalent to the server's `(child_id, state)` index; Retrofit calls use the shared OkHttp client's connection pooling (no new client instantiation per call).

## 25. Security
No new sensitive data handling; mastery-progress metadata only, no raw content/voice data (consistent with A.9 PRD §12.4).

## 26. Library Requirements
Hilt, Retrofit+OkHttp, Room — all already standard in the KMP stack per `CORE_NETWORK_INSTRUCTIONS.md`/`CORE_DATABASE_INSTRUCTIONS.md`. No new libraries introduced.

## 27. Testing
- Unit: `MasteryRepositoryImpl` remote/cache-fallback branching logic.
- **DTO reflection test (mandatory):** enumerate every public data class in `:core:mastery-engine`, assert none contains a numeric field matching `/score|confidence/i` (Android AI Prompt item 2).
- Unit: DTO parsing against representative B-04/B-05/B-06 response fixtures.

## 28. Documentation
Module README documenting the `:core:quiz-engine`-mirrored structure and the explicit "no score field" design constraint for future contributors.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Scaffold :core:mastery-engine Module**
- Task ID: K-01-T01
- Objective: Gradle module skeleton mirroring `:core:quiz-engine`.
- Why This Is Required: Foundational — nothing else in K-02 through K-06 can proceed without this module existing.
- Existing Architecture to Follow: `:core:quiz-engine`'s exact module structure (package layout, `build.gradle.kts` shape).
- Existing Files to Reuse: `:core:quiz-engine/build.gradle.kts` as the direct template.
- Files to Create: `core/mastery-engine/build.gradle.kts`.
- Files to Modify: `settings.gradle.kts`.
- Implementation Details: Dependencies on `:core:design-system`, `:core:network`, `:core:database`; no dependency on any `:feature:*` module (core modules must not depend on feature modules — layering rule).
- Business Rules: N/A. Validation: N/A. Error Handling: N/A. Security: N/A. Performance: N/A.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: Module compiles cleanly.
- Documentation: Module README stub.
- Dependencies: None.
- Do Not Change: `:core:quiz-engine` itself (reference only).
- Expected Result: Empty but correctly-wired Gradle module.
- Definition of Done: Module builds; registered in `settings.gradle.kts`.

**Task 02 — Implement DTOs with Reflection-Enforced No-Score-Field Guarantee**
- Task ID: K-01-T02
- Objective: Score-free public data classes.
- Why This Is Required: FR-3's client-side enforcement layer, mirroring the backend's structural guarantee (B-05).
- Existing Architecture to Follow: Existing DTO conventions in `:core:quiz-engine`.
- Existing Files to Reuse: N/A.
- Files to Create: `dto/SkillStateDto.kt`, `dto/QuizResultDto.kt`, `dto/DtoReflectionNoScoreFieldTest.kt`.
- Files to Modify: None.
- Implementation Details: Reflection test walks every public data class in the module's `dto` package, fails if any numeric-typed field name matches `/score|confidence/i`.
- Business Rules: This test must automatically cover future DTOs added to this package without manual test updates (package-scan-based, not a hardcoded class list).
- Validation: N/A. Error Handling: N/A. Security: this IS the control. Performance: N/A.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: This task IS the test.
- Documentation: Comment explaining the intentional omission.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: DTOs matching B-04/B-05/B-06 response shapes, score-free.
- Definition of Done: Reflection test green, marked mandatory in CI.

**Task 03 — Implement MasteryApi (Retrofit) + MasteryRepository**
- Task ID: K-01-T03
- Objective: Networking + repository abstraction.
- Why This Is Required: The data-access layer every ViewModel in K-02/K-06 depends on.
- Existing Architecture to Follow: `:core:network`'s shared OkHttp/Retrofit client pattern.
- Existing Files to Reuse: `:core:network`'s auth interceptor.
- Files to Create: `data/MasteryApi.kt`, `data/MasteryRepository.kt`, `data/MasteryRepositoryImpl.kt`.
- Files to Modify: None.
- Implementation Details: Suspend-function Retrofit interface; repository implements remote-first/cache-fallback for `getSkillStates`, remote-only for `getResult`.
- Business Rules: Per §18 error-handling table.
- Validation: DTO parsing via standard converter.
- Error Handling: Typed `MasteryApiException`.
- Security: Reuses existing auth interceptor.
- Performance: Shared connection pool.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: `MasteryRepositoryTest.kt` covering fallback branching.
- Documentation: KDoc on public repository methods.
- Dependencies: Task 01, Task 02.
- Do Not Change: `:core:network`'s client configuration.
- Expected Result: Working repository layer.
- Definition of Done: Unit tests green including cache-fallback path.

**Task 04 — Implement Room Cache Layer**
- Task ID: K-01-T04
- Objective: `SkillNodeStateEntity`/`MasteryDao` for offline-capable skill-state reads.
- Why This Is Required: Backs K-04's offline behavior and general offline-first UX for skill-tree viewing.
- Existing Architecture to Follow: `:core:database`'s existing Room DAO/entity conventions.
- Existing Files to Reuse: `:core:database`'s base DAO patterns.
- Files to Create: `data/db/SkillNodeStateEntity.kt`, `data/db/MasteryDao.kt`.
- Files to Modify: `:core:database`'s Room database class (register the new entity/DAO), following existing migration-registration convention.
- Implementation Details: Entity mirrors `SkillStateDto` shape (no score field), indexed on `(childId, domain)`.
- Business Rules: N/A. Validation: N/A. Error Handling: N/A. Security: N/A. Performance: Indexed queries.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: DAO CRUD unit tests.
- Documentation: KDoc.
- Dependencies: Task 02.
- Do Not Change: Existing Room database migration history (append a new migration, don't edit a shipped one).
- Expected Result: Working local cache.
- Definition of Done: DAO tests green; migration applies cleanly.

**Task 05 — Wire Hilt DI Module**
- Task ID: K-01-T05
- Objective: `MasteryEngineModule` providing all bindings.
- Why This Is Required: Every consumer (K-02–K-06, `:feature:learn`) needs DI-injectable access.
- Existing Architecture to Follow: `:core:quiz-engine`'s Hilt module structure.
- Existing Files to Reuse: N/A.
- Files to Create: `di/MasteryEngineModule.kt`.
- Files to Modify: None.
- Implementation Details: `@Provides`/`@Binds` for `MasteryApi`, `MasteryRepository`, `MasteryDao`.
- Business Rules: N/A. Validation: N/A. Error Handling: N/A. Security: N/A. Performance: N/A.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: DI graph compiles/resolves in a smoke test.
- Documentation: KDoc.
- Dependencies: Tasks 01-04.
- Do Not Change: N/A.
- Expected Result: Fully injectable module.
- Definition of Done: App compiles with `:feature:learn` consuming the new module via DI.

## 30. Definition of Done
`:core:mastery-engine` module live, mirroring `:core:quiz-engine`'s structure, providing score-free DTOs (reflection-tested), a remote-first/cache-fallback repository, Room caching, and full Hilt DI wiring — ready for K-02 through K-06 and `:feature:learn` to consume.

## 31. Final Verification Checklist
- [ ] Module builds and is registered in `settings.gradle.kts`
- [ ] DTO reflection test passing (no score/confidence field anywhere)
- [ ] `MasteryRepository` remote-first/cache-fallback behavior verified for `getSkillStates`
- [ ] `getResult` correctly has no offline fallback (by design)
- [ ] Room cache entity/DAO working, indexed correctly
- [ ] Hilt DI graph resolves cleanly
- [ ] No dependency from this core module back onto any `:feature:*` module
- [ ] `:feature:learn` successfully migrated to consume this module
