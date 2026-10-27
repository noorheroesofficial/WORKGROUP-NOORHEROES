# B-06 — AI-Flow Distributed Tracing Instrumentation

## 1. Feature Context
Dedicated observability for the AI layer's request paths — given these flows involve the most cross-service-module hops in the platform and the highest cost of a silent failure, every AI-flow request produces a correlated trace spanning each internal service hop it passes through.

## 2. Parent Feature
F.35 — AI Layer & Microservices Architecture

## 3. Sub-feature
1.6 AI-Flow Distributed Tracing Instrumentation (ID: **B-06**)

## 4. Objective
Instrument all five logical AI services (Recommendation, Narration, Learning, Moderation, Insights) with correlated distributed tracing spans, tagged specifically for AI-flow identification.

## 5. Business Requirements
- FR-12: distributed tracing specifically required for AI flows, given they involve the most cross-service hops and the highest cost of a silent failure.
- §5 Backend AI prompt item 5: a fixture AI-flow request produces a correlated trace spanning each internal service-module hop it passes through.
- §10 DevOps: distributed tracing specifically instrumented for AI-flow request paths.

## 6. Existing Architecture
`app/shared/tracing/ai_flow_tracer.py`, integrating with the platform's existing distributed-tracing infrastructure (OpenTelemetry or equivalent, confirmed against the platform's established observability stack).

## 7. Existing Code to Reuse
- The platform's existing tracing/observability middleware (extended with AI-flow-specific span tagging, not a parallel tracing system)

## 8. Files to Create
- `app/shared/tracing/ai_flow_tracer.py` — a decorator/context-manager applying a consistent `ai.flow_id`/`ai.service_name` span-tagging convention
- `app/ai/middleware/ai_tracing_middleware.py`

## 9. Files to Modify
- `app/ai/services/recommendation_service.py`, `narration_service.py`, `learning_service.py`, `insights_service.py` (B-01–B-04) — wrap each service's entry method with the `ai_flow_tracer` decorator
- E.30's Moderation Service entry point — same decorator applied (additive instrumentation only, no logic change)

## 10. Backend Requirements
- `ai_flow_tracer`: a decorator that, when applied to a service's public entry method, creates or continues a trace span tagged `ai.service_name` (`recommendation`/`narration`/`learning`/`moderation`/`insights`) and `ai.flow_id` (a correlation ID generated at the originating consumer-facing request and propagated through every internal hop).
- Every one of the five services' entry points carries this instrumentation — no AI service call path is untraced.
- Trace propagation survives internal-module-to-internal-module calls within the monolith (e.g., Recommendation Service calling into the Citation/Safety Verifier, which calls into E.30's six-stage pipeline) — the same `ai.flow_id` appears on every span in that chain.

## 11. Required API / API Contract
No new public endpoint — this is cross-cutting middleware/decorator instrumentation applied to the five existing services' internal entry points (B-01–B-04, plus E.30's Moderation Service).

## 12. Database Requirements
None — traces are exported to the platform's existing tracing backend (not a new database table).

## 13. Validation
N/A (instrumentation, not a request-validated endpoint).

## 14. Authentication
N/A.

## 15. Authorization
N/A.

## 16. Error Handling
A tracing-export failure must never block or fail the underlying AI-service call itself (tracing is best-effort observability, not a hard dependency of the request path) — confirmed by a fault-injection test.

## 17. Security
N/A directly — this sub-feature strengthens operational visibility rather than a data-protection guarantee, though correlated tracing does support faster incident diagnosis for any of the other sub-features' safety-relevant failures.

## 18. Analytics
N/A — this feeds the platform's tracing/observability system, distinct from the analytics event bus (§1.19's events remain separately emitted).

## 19. Performance
Tracing overhead kept minimal (span creation/propagation only, no synchronous export blocking the request path — exports are async/batched per the platform's existing tracing infrastructure conventions).

## 20. Library Requirements
The platform's existing distributed-tracing library (e.g., OpenTelemetry Python SDK, confirmed against current infrastructure). No new tracing framework introduced.

## 21. Testing
Unit: `ai_flow_tracer` decorator correctly tags spans with `ai.service_name`/`ai.flow_id`. Integration: **mandatory** — a fixture AI-flow request (e.g., a Recommendation Service call that internally invokes the Citation/Safety Verifier and E.30's pipeline) produces a single correlated trace with the same `ai.flow_id` present on every span across all internal hops; fault-injection test confirming a tracing-export failure does not block or fail the underlying service call.

## 22. Documentation
Docstring on `ai_flow_tracer` explaining the tagging convention and its cross-service-hop correlation guarantee.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Implement `ai_flow_tracer` Decorator**
Objective: Span creation/continuation with `ai.service_name`/`ai.flow_id` tagging. Files: `tracing/ai_flow_tracer.py`. Tests: unit tests for tag correctness. Definition of Done: tests pass.

**Task 02 — Implement `ai_tracing_middleware`**
Objective: Correlation-ID generation/propagation at the originating request boundary. Files: `middleware/ai_tracing_middleware.py`. Dependencies: Task 01. Tests: propagation test. Definition of Done: test passes.

**Task 03 — Apply Instrumentation to All Five AI Services**
Objective: Decorator applied to Recommendation/Narration/Learning/Insights (B-01–B-04) and E.30's Moderation Service entry points, additive only. Dependencies: Task 01, Task 02, B-01–B-04. Tests: **mandatory** — correlated-trace-across-all-hops fixture test. Definition of Done: test passes.

**Task 04 — Implement Fault-Injection Resilience**
Objective: Tracing-export failure never blocks the underlying request. Dependencies: Task 03. Tests: **mandatory** — fault-injection test. Definition of Done: test passes.

**Task 05 — Add Full Test Suite**
Objective: Complete coverage per §21, both mandatory tests included. Definition of Done: all green in CI.

**Task 06 — Final Code Review**
Objective: Confirm all five AI services carry instrumentation with zero untraced entry point, and confirm tracing failures are genuinely non-blocking. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] All five AI services' entry points carry `ai_flow_tracer` instrumentation
- [ ] A single `ai.flow_id` correlates every span across a multi-hop AI-flow request — mandatory test passing
- [ ] Tracing-export failure never blocks the underlying service call — mandatory fault-injection test passing
- [ ] Tracing overhead does not synchronously block the request path

## 25. Definition of Done
Every AI-flow request across the platform's five logical AI services produces a correlated, cross-hop distributed trace, giving engineering the observability this deliberately cross-service-heavy layer requires without adding any hard dependency risk to the request path itself.
