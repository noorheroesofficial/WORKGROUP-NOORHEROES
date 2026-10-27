# B-05 — Mastery Engine Domain Registration (`islamic_facts`)

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). Registers Islamic Facts as a participating domain in A.9's shared cross-domain spaced-repetition scheduler — this is a DATA migration exercising A.9's existing extensibility design, not new mastery-calculation application code.

## 2. Parent Feature
B.18 — Islamic Facts Module

## 3. Sub-feature
1.5 Mastery Engine Domain Registration (ID: B-05)

## 4. Objective
Register `islamic_facts` as a new `domain` value in A.9's `skill_node` domain registry via an Alembic data migration, and prove — via a fixture-based extensibility test — that the shared state-machine/scoring/scheduling pipeline works end-to-end for this domain with zero new mastery-calculation code.

## 5. Business Requirements
- FR-4: Islamic Facts is a participating domain in A.9's shared Mastery Engine's spaced-repetition scheduler, subject to the same global daily-prompt cap as Quran/Arabic/Tajweed (cross-ref A.9 FR-8/§5 item 5).
- Acceptance Criteria: when the scheduler determines a fact is due for resurfacing and the global daily cap allows it, that fact may be resurfaced, subject to the same cap shared across domains.
- Edge Case 5: revoking approval on an already-engaged fact preserves the child's historical mastery-evidence record; only future eligibility is affected.
- PRD header, "Feeds into": C.22 Parent Progress Reports — Islamic Facts mastery/engagement evidence must surface in the existing parent-facing progress reporting surface via this same domain-registration mechanism, not a separate reporting integration.

## 6. Existing Architecture
A.9's `skill_node` domain registry is explicitly designed as an extensible registry (per A.9 FR-9). Per A.9's own B-01 blueprint ("Cross-Domain Skill Graph & Domain Registry Generalization"), adding a new domain is a **data operation**: inserting registry rows referencing the new domain's content identifiers (here, `fact_id`s), not writing new state-machine, scoring, or scheduling code.

## 7. Existing Code to Reuse
- A.9's `skill_node` table and domain-registry insertion pattern (confirm exact registration mechanism from A.9's own B-01 blueprint before writing the migration — do not invent a new registration shape).
- A.9's existing "fictitious new domain" extensibility test pattern (A.9's own test suite already validates the registry is domain-agnostic) — this sub-feature's test mirrors that same pattern applied to a real domain.
- A.9's existing cross-domain spaced-repetition scheduler and global daily-prompt cap logic — entirely unmodified.

## 8. Files to Create
- `alembic/versions/xxxx_register_islamic_facts_mastery_domain.py` — data migration inserting `islamic_facts` domain registry rows, linking eligible `fact_id`s as skill nodes.
- `tests/modules/mastery/test_islamic_facts_domain_extensibility.py` — end-to-end fixture test through A.9's existing pipeline.

## 9. Files to Modify
None beyond the migration — this sub-feature must not modify any A.9 application code (state machine, scoring formula, scheduler). Any perceived need to modify A.9 code is a signal that A.9's registry is not actually domain-agnostic and should be raised as a blocking architecture issue rather than worked around here.

## 10. Backend Requirements
- Data migration inserts `skill_node` rows with `domain = 'islamic_facts'`, referencing `fact.fact_id` as the external content key, following the exact column/relationship shape A.9's registry expects (confirm against A.9's B-01 schema before writing).
- No changes to A.9's `MasteryScoreFormulaEngine`, `SkillStateMachine`, or `SpacedRepetitionScheduler` — this sub-feature succeeds only if zero such changes are required.
- Global daily-prompt cap (shared with Quran/Arabic/Tajweed) applies automatically since it is enforced at the scheduler level, domain-agnostically, per A.9's existing design.

## 11. KMP Requirements
Consumed by K-04, which renders A.9's existing generic review-prompt UI parameterized for this domain — no facts-specific resurfacing UI is built.

## 12. NextJS Requirements
N/A directly; domain registry visibility may appear in A.9's own Admin Skill Domain Registry API (A.9's N-equivalent), unmodified by this sub-feature.

## 13. API Contract
No new endpoints. Domain registration is consumed transparently by A.9's existing:
- `GET /v1/skills/state` (A.9 B-05) — now returns `islamic_facts` nodes alongside other domains.
- Cross-domain spaced-repetition scheduler (A.9 B-07) — now includes `islamic_facts` nodes in its candidate pool.
- Cross-Domain Parent Mastery Summary API (A.9 B-08, "08-cross-domain-parent-mastery-summary-api.md") — now includes `islamic_facts` evidence in its aggregate, which C.22 Parent Progress Reports consumes. No new endpoint or C.22-side code is expected; this is the same "genuine reuse" guarantee as items 1 and 2 above, extended one hop further downstream.

## 14. Database Requirements
Writes to A.9's existing `skill_node` table only (per its established schema); no new tables created by this sub-feature.

## 15. Validation
Migration must validate referential integrity: every `fact_id` referenced in the new `skill_node` rows must exist in B-01's `fact` table at migration time; orphaned references are a migration failure, not a silent skip.

## 16. Authentication
N/A — data migration, no endpoint.

## 17. Authorization
N/A.

## 18. Error Handling
Migration fails atomically (transactional) if any referenced `fact_id` does not exist — no partial domain registration.

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
N/A — domain registration is locale-agnostic; individual fact content localization is handled entirely within B-01/B-03.

## 22. RTL
N/A.

## 23. Analytics
None new; resurfacing events (`fact_spaced_repetition_resurfaced`) are emitted by K-04 client-side, using A.9's existing analytics wiring for resurfacing prompts.

## 24. Performance
No new query paths introduced beyond what A.9's existing scheduler already executes across all registered domains; negligible incremental load from the added `islamic_facts` node set.

## 25. Security
No new attack surface; inherits A.9's existing authorization model entirely.

## 26. Library Requirements
None new — pure data migration using existing Alembic/SQLAlchemy tooling.

## 27. Testing
- **Signature test:** fixture `islamic_facts` skill node flows end-to-end through A.9's existing state-machine → scoring → scheduling pipeline with zero new mastery-calculation code required — mirroring A.9's own "fictitious new domain" extensibility test pattern, but applied to this real domain.
- Verify global daily-prompt cap correctly counts `islamic_facts` resurfacing prompts alongside Quran/Arabic/Tajweed prompts (shared cap, not a per-domain cap).
- Verify migration fails cleanly on a referential-integrity violation (fixture with a dangling `fact_id`).
- Verify a fixture child's `islamic_facts` mastery evidence correctly appears in A.9's existing Cross-Domain Parent Mastery Summary API response, confirming the C.22 Parent Progress Reports integration works with zero C.22-side or summary-API-side code changes.

## 28. Documentation
Update A.9's domain-registry documentation to list `islamic_facts` as a registered domain, with a link back to this blueprint for the specific registration migration.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm A.9 Registry Schema**
Objective: Read A.9's B-01 blueprint and actual `skill_node` model to confirm exact registration shape before writing any migration.
Why Required: Rule 30 — do not guess at existing schema; inventing a shape risks breaking A.9's actual registry contract.
Dependencies: None (first task, research-only).
Expected Result: Confirmed column list and relationship shape for `skill_node` domain registration.
Definition of Done: Schema confirmed against actual A.9 codebase, not assumed from this PRD's description alone.

**Task 02 — Write Domain Registration Migration**
Objective: `xxxx_register_islamic_facts_mastery_domain.py`.
Existing Architecture to Follow: A.9's confirmed registry shape (Task 01).
Files to Create: the migration file.
Business Rules: Referential integrity to `fact.fact_id`.
Error Handling: Atomic failure on dangling reference.
Dependencies: Task 01, B-01 complete (fact table populated or migration ordered to run after seed data).
Expected Result: `islamic_facts` domain rows present in `skill_node` after migration.
Definition of Done: Migration applies/rolls back cleanly.

**Task 03 — Extensibility Test**
Objective: End-to-end fixture test through A.9's pipeline.
Files to Create: `tests/modules/mastery/test_islamic_facts_domain_extensibility.py`.
Dependencies: Task 02.
Expected Result: Fixture `islamic_facts` node scores, transitions state, and schedules spaced-repetition correctly using A.9's unmodified code.
Definition of Done: Test green; code review confirms zero A.9 application-code changes were needed.

**Task 04 — C.22 Parent Progress Reports Verification**
Objective: Confirm `islamic_facts` mastery evidence flows into A.9's existing Cross-Domain Parent Mastery Summary API with zero new code on either side.
Why Required: PRD header explicitly lists C.22 as a "Feeds into" consumer; this is the concrete verification point, otherwise the claim is untested.
Existing Architecture to Follow: A.9's B-08 Cross-Domain Parent Mastery Summary API (unmodified).
Dependencies: Task 03.
Expected Result: A fixture child's fact-engagement evidence appears correctly in the summary API's response.
Definition of Done: Verified via Task 05's test; no C.22 or A.9 B-08 code changes required.

**Task 05 — Documentation**
Dependencies: Task 04.
Definition of Done: A.9 domain-registry docs updated, noting the C.22 downstream consumption path.

## 30. Definition of Done
- `islamic_facts` domain registered via data migration only — zero A.9 application-code changes.
- Extensibility test passes, proving genuine reuse (not a parallel implementation).
- Global daily-prompt cap correctly shared across domains including `islamic_facts`.
- `islamic_facts` evidence verified surfacing correctly in A.9's Cross-Domain Parent Mastery Summary API, confirming the C.22 Parent Progress Reports integration.
- This test is a mandatory CI gate per the PRD's DevOps requirements (§10).

## 31. Final Verification Checklist
- [ ] Zero changes made to A.9's state machine, scoring engine, or scheduler code
- [ ] Migration is purely additive data, referentially valid
- [ ] Extensibility test proves end-to-end pipeline works for `islamic_facts` with no new mastery code
- [ ] Global daily cap verified shared (not per-domain) across `islamic_facts` and existing domains
- [ ] `islamic_facts` evidence verified in A.9's Cross-Domain Parent Mastery Summary API (C.22 integration)
- [ ] CI gate configured per PRD §10 DevOps requirement
- [ ] Documentation updated
