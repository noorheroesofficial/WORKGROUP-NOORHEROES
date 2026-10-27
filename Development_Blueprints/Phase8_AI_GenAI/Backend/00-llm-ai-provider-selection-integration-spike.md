# Phase 8 — LLM / AI Provider Selection & Integration Spike Blueprint

`Development_Blueprints.Phase8_AI_GenAI.Backend.00-llm-ai-provider-selection-integration-spike.md`

**Module:** AI / GenAI Foundation Layer (`noorheroes.modules.ai_safety` and external AI gateways)  
**Phase:** 8 — AI/GenAI Layer & Ramadan Seasonal Mode  
**Sequence:** Seq 699  
**Status:** 🟡 **Pending Spike Execution**  
**Depends on:** Phase 2 Backend Foundation & Security Baseline  
**Consumed by:** Feature F.35 AI Microservices (`Backend.01-recommendation-service.md` through `06-ai-flow-distributed-tracing.md`)  
**Source of truth:** `NoorHeroes_Consolidated_Execution_Blueprint.md` §9; `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F35_AI_Layer_Microservices_Architecture.md` §1.7  

---

## 1. Objective and Purpose
Resolve the open architectural decision regarding external LLM / Generative AI providers for the NoorHeroes platform. This spike evaluates candidates against strict Islamic content boundaries, child safety latency thresholds, token economics, and data privacy requirements before F.35 AI services are wired to production models.

---

## 2. Evaluation Criteria & Benchmark Gates

### 2.1 Provider Candidates
1. **Anthropic Claude 3.5 Sonnet:** Renowned for superior instruction-following, nuanced boundary refusals, and low hallucination rates.
2. **OpenAI GPT-4o / GPT-4o-mini:** Fast time-to-first-token (TTFT), multimodal capabilities, cost-effective mini tier for classification.
3. **Google Gemini 1.5 Flash / Pro:** Exceptional multilingual support (Arabic, Urdu, Hindi), generous context window, competitive pricing.
4. **Self-Hosted vLLM (Llama-3-8B-Instruct fine-tuned):** Zero third-party data transmission, full on-premise governance, predictable hosting cost.

### 2.2 Non-Negotiable Pass/Fail Invariants
- **Islamic Rulings Guardrail (FR-3):** The model must never improvise religious rulings, halal/haram judgments, or fiqh rulings. It must strictly adhere to closed Islamic knowledge card citations or trigger scholar handoff.
- **Child Voice Privacy (FR-10):** Zero child voice recording used for model training; any voice narration features must verify explicit parent voice-cloning consent (`voice_cloning` consent type).
- **Latency SLOs:**
  - Recommendation ranking (F35 B-01): p95 < 400ms.
  - Interactive learning adaptation (F35 B-03): p95 < 800ms.
  - Narration text generation (F35 B-02): p95 < 1,500ms.
- **Cost Target:** Blended cost < $0.005 per daily active family session across all AI touchpoints.

---

## 3. Spike Implementation Steps

1. **Step 1: Test Dataset Calibration**
   - Assemble 200 standardized evaluation prompts spanning:
     - 50 Islamic theological questions (Aqeedah, Salah, Fasting).
     - 50 general child curiosity questions (Science, Nature, History).
     - 50 adversarial / jailbreak attempts (prompt injection, PII solicitation).
     - 50 multilingual queries across English, Arabic, Urdu, and Hindi.
2. **Step 2: Automated Benchmark Harness**
   - Stand up a test harness measuring: accuracy against scholar-approved reference cards, refusal correctness rate, latency distribution (p50, p90, p99), and token cost.
3. **Step 3: Gateway Adapter Interface Definition**
   - Implement the unified Python interface `LlmProviderGateway` in `src/noorheroes/modules/ai_safety/gateway.py` supporting:
     - `generate_completion(prompt, schema, temperature, timeout) -> LlmResponse`
     - `generate_embeddings(text) -> List[float]`
     - Streaming response support with mid-stream safety tripwires.
4. **Step 4: Circuit Breaker & Fallback Strategy**
   - Wire resilience middleware: if Primary Provider error rate > 5% or latency > 2s, automatically route to Secondary Provider or fall back to pre-rendered static knowledge cards.

---

## 4. Verification and Acceptance Criteria
- [ ] Evaluation harness executes all 200 test cases against each provider.
- [ ] Refusal correctness on out-of-bounds/ruling topics is 100%.
- [ ] Cost model proves sustainability at 50,000 MAU.
- [ ] Architectural Decision Record (ADR) committed to `docs/architecture/adr-008-llm-provider.md`.
