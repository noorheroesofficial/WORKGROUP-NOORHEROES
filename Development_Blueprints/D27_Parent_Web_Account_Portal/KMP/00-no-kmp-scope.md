# K — No KMP Scope (Explicit Exclusion)

## 1. Feature Context
Feature D.27 — Parent Web Account Portal (`account.noorheroes.com`).

## 2. Parent Feature
D.27 Parent Web Account Portal

## 3. Sub-feature
**No KMP sub-feature exists for this document.** This file is a documented decision record, not an implementation blueprint.

## 4. Objective
Record, explicitly and permanently, that Feature D.27 introduces zero changes to the KMP (Android/iOS) codebase — so that no future maintainer mistakenly assumes a missing KMP blueprint file for D.27 is an oversight.

## 5. Business Requirements
- PRD D.27 header: **"Feeds into:** Nothing downstream in the mobile app (this is a terminal, narrow-scope web surface); cross-references the Mobile App for every action explicitly out of its scope."
- PRD §Scope note: "Its single most important architectural property is what it does not do... this document introduces no parallel backend logic, only a second, narrower client surface against the same APIs" — the same principle extends to the KMP client: D.27 is a second surface against existing APIs, never a third client requiring its own KMP work.

## 6. Existing Architecture
The Mobile App's existing screens and modules that D.27 cross-references — Parent Dashboard (C.20), Parent PIN/Biometric Gate (C.19), Multi-Child Management (C.21), Subscription & Billing (C.24), Notifications & Support (C.25), Privacy/Consent/Account Security/Data Rights (C.26) — are read, cited, and reused by D.27's backend and web-frontend blueprints exactly as already specified in their own KMP blueprint sets. None of those existing KMP files require modification as a consequence of D.27. No new KMP module, screen, repository, use case, or ViewModel is introduced.

## 7. Existing Code to Reuse
Not applicable — no KMP code is touched.

## 8. Files to Create
None.

## 9. Files to Modify
None.

## 10. Backend Requirements
Not applicable to this record (see Backend section B-01 through B-04).

## 11. KMP Requirements
None. Zero KMP development tasks exist for Feature D.27.

## 12. NextJS Requirements
Not applicable to this record (see NextJS_Admin and Parent_Web_Portal sections).

## 13. API Contract
Not applicable.

## 14. Database Requirements
Not applicable.

## 15. Validation
Not applicable.

## 16. Authentication
Not applicable.

## 17. Authorization
Not applicable.

## 18. Error Handling
Not applicable.

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
Not applicable.

## 22. RTL
Not applicable.

## 23. Analytics
Not applicable.

## 24. Performance
Not applicable.

## 25. Security
Not applicable.

## 26. Library Requirements
Not applicable.

## 27. Testing
Not applicable — there is no KMP code to test as a consequence of this feature.

## 28. Documentation
This file itself is the documentation of the exclusion decision. If any future D.27 revision proposes KMP work, it must first justify why the "terminal, narrow-scope web surface" architectural property no longer holds, and this file should be updated (not silently superseded) to reflect that change.

## 29. AI Coding Agent Implementation Steps

**Task 01 — No Action Required**
- **Objective:** Confirm, before starting any D.27 implementation work, that no KMP repository, module, or screen should be touched.
- **Definition of Done:** This confirmation is on record via this file; an AI coding agent executing any other D.27 sub-feature (B-01–B-04, N-01–N-10) should treat any apparent need to modify KMP code as a signal to stop and re-confirm scope with the team, not proceed.

## 30. Definition of Done
The absence of KMP work for D.27 is explicit, on record, and citable — equivalent in rigor to a positive implementation blueprint, per the project's "do not guess, do not omit" documentation standard.

## 31. Final Verification Checklist
- [ ] No KMP files created or modified anywhere in this feature's implementation
- [ ] Any apparent need for KMP changes during D.27 implementation is escalated for scope re-confirmation, not silently implemented
