# Screen014 — content and source reconciliation

Approved by user: screenshot's “Add a child”, subtitle, nickname/DOB/avatar fields, learning-level descriptions; add PRD-required preferred language and an Optional preferences sheet using existing app copy. Standard390×844, V2→Onboarding only, primary48px.

Source hierarchy: Feature_A1 PRD FR13–17 and edge cases10/11; KMP K06/K07; existing screenshot; live reference1095:390 and1085:21358 for assets only; finalized Login1355:2696 and PIN1650:502 for visual style. No raw age selector. Original references remain unchanged.

Existing app strings: NICKNAME, DATE OF BIRTH, CHOOSE AVATAR, Enter birthdate to see age-appropriate avatars, LEARNING LEVEL, Beginner / Just starting out, Intermediate / Knows the basics, Advanced / Ready to grow further, Save & Continue, Learning Interests, Daily Goal (minutes), AI Voice Guidance, Enable interactive AI voice for activities (default off), Duplicate Nickname, Confirm Name, Change Details, Existing Profile, New Profile. Existing network/API messages are reused through NH/Snackbar.

Additional copy approved by the user on22 October2026:

- PRD defaults block below3 and above17, while current runtime says3–18. Approved UI error: “Choose a birthdate for a child aged 3–17.” PRD wins; no production code change in this design task.
- Capacity: “Your plan’s child limit has been reached.”
- Saved feedback: “Child profile saved.” Next destination stays unmapped until Screen018 is approved.
- Accessibility preference labels: “Large text” and “High contrast”.

Final standalone portrait sources1085:21471/21480/21490 depict Tariq/Maryam/Noor. Rejected1095:452/462/468 because some contain embedded thumbnail mockups. The final portraits remain visual reference samples, not a verified age-tagged avatar catalog; prototype results are controlled review fixtures. The production catalog uses different themed companion assets and requires separate reconciliation; never imply a verified semantic mapping from those IDs to these pictures.

Figma native Design cannot provide unrestricted secure text entry, device storage, server-authoritative DOB/age filtering, true idempotency, API delivery or OS biometric grants. Use explicitly documented controlled prototype fixtures. Browser access to figma.com remains denied by saved policy; do not claim live Present verification. Code Layers are unavailable for this account; no duplicate Make file is authorized.

Confirmed inbound routes: successful PIN with biometric unavailable, biometric Skip, biometric success. Cancelled biometric system prompt returns to offer; no bypass. Back from the form preserves draft and returns to invoking confirmed context. Future Avatar015/Interests016/Learning017/AddAnother018/summary019 destinations must not be guessed or built beyond014 without approval.
