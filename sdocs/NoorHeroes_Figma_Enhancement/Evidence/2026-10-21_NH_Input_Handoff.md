# Login / Registration NH input verification

## Delivered

Editable Figma Login 1355:2696 and Registration 1459:256 now contain genuine NH TextField instances 1563:936 / 1563:1399. Original component 357:2 and unrelated screens preserved. Bound visual states select Empty 356:125, Filled 356:133, Focused 356:141 and Error 356:149. Input boundary remains 56 px in every state; total label/input group is 88 px normally and 116 px with error. Dynamic loading hosts follow the new field height.

Native review panels: Login 1563:946; Registration 1563:1409. Press D from the form to open the scrollable controlled review. G focuses; B blurs; V fills a fictional fixture; C clears; Q demonstrates required validation. Cases include invalid phone/email and next-response 422, 500, 503, 429, 401/403, network, timeout and successful processing. Select an outcome, then use an existing valid fixture and submit. Registration retains all required consent gates.

422 preserves values and shows inline feedback for identifier requests. Google 422 stays global. Failures use existing NH Snackbar instances 1428:220 / 1461:545. Native 429 blocks dismissal for a 15-second demonstration; the companion uses real mock Retry-After timing. Recovery restores the existing buttons and retains distinct loader styles.

## Evidence

- Native action interpreter: 32 checks passed across both forms for Empty/Focused/Filled/Error, HTTP 500/422/429/offline outcome routing, processing restoration and value preservation. This exercises variable/actions structurally; it does not prove Present playback.
- All eight state-to-component mappings checked against actual NH variant IDs.
- Default and error screenshots inspected for both forms: 56 px boundary, proper inline helper, no overlap with preferences/buttons/footer at 390×844.
- Local unit + actual mock HTTP tests: 5 groups passed. Country validation covers US, GB, India, Australia, international/shared calling codes, Unicode digits, too short/long/invalid characters and calling-code mismatch.
- Data verification: 245 unique countries, matching pinned dial codes and 245 flag assets.
- Browser checks: email error/correction/trim, country search/selection, India field error with country retained, international GB success, 500/503 Snackbar, Retry to success, Google white/dark-dot loader with Send visible/disabled, network failure, timeout, 429 disabled controls/hidden Retry and recovery, Registration consent gates and single-open-sheet sequence. Error correction/reflow checked at 320×568 with 200% text; no horizontal overflow.
- Mock HTTP integration additionally verifies 401, 403 and unrelated 422 use safe global feedback. No raw backend message is displayed.

## Boundaries

Real typing and arbitrary country-aware validation run at [local companion](http://127.0.0.1:8766/). Native Figma uses labelled controlled presets. Code Layers are disabled. Figma Present was not run due browser access restrictions. Device virtual keyboard behavior and production backend/OAuth are not verified. OTP success remains unmapped until approved.

Technical manifest: [2026-10-21_NH_Input_Verification.json](2026-10-21_NH_Input_Verification.json).

Final guard verification: [native checks](2026-10-21_NH_Input_Final_Action_Checks.json). Browser rechecked both forms after the final changes: empty/invalid identifiers disable primary submit, server-field errors block resubmission until correction, and Registration still requires the separate consent flow. Login Back is disabled only in the local companion because Intro screens are not implemented there; original Figma navigation is retained.
