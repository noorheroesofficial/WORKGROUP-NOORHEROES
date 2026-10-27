# Feature F35: AI Layer & Microservices Architecture — Visual & System Blueprint

## 1. Feature Identification & Reference
- **Feature ID**: Feature F.35
- **PRD Reference**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F35_AI_Layer_Microservices_Architecture.md`
- **Target Microservice**: `noorheroes-ai-gateway` (FastAPI microservice cluster)
- **Consuming Surfaces**: Mobile App (`Home`, `Stories`, `Learn`, `Duas`) and Admin Moderation Console (`E30`)

---

## 2. Microservice Topology & Visual Contract Binding
- **Core AI Pipelines**:
  1. **Recommendation Service**: Powers dynamic home feeds and continue-learning carousels on `Screens/Mobile App/Home/Home-03.png`.
  2. **Narration Service & Voice Cloning**: Synthesizes warm audio storytelling for `Screens/Mobile App/Stories/Player.png` with explicit parent consent check.
  3. **Learning Service (Non-Improvisation Strict Guard)**: Evaluates Arabic pronunciation for `Screens/Mobile App/Learn/Feedback.png` and refuses improvisation on theological rulings.
  4. **Insights Service**: Summarizes child learning patterns for `Screens/Mobile App/Child Reports/Per-Child Report-01.png`.
