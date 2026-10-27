# Add Child → Family Summary routing

Figma-only update,25 October2026. File MR9935oQZACMjndzGIUgq5, V2 page928:2.

- Saving frame1804:3379 now navigates to2137:6635 only in the existing successful-save branch. Error, offline, duplicate, timeout, validation and save-count actions were retained.
- Summary2137:6635 no longer forces the sample review variable mode. Nickname, DOB, language, level and five Learning Focus visibility bindings consume the current prototype mode and values.
- Empty-focus dash retains its NOT(OR(selected focus)) expression. Selected names remain visible as text; multiple selections are supported.
- Summary Back2137:6674 and Edit2137:6706 return to the normal Add Child1804:2656 instead of forcing the sample valid-draft frame.
- Review-fixture Save hit1806:3743 now uses the normal guarded save interaction, with its review variable mode explicitly carried into the flow.
- Confirm remains disabled because its Profile Picker destination is not yet supplied. No application code or backend integration changed.

Verification: evaluated actual stored Save, Saving and Summary action graphs for all32 focus combinations;32/32 passed success routing, unchanged selection values and empty-state visibility. Checked summary mode inheritance and Review-fixture Save wiring. Captured selected-focus screenshot in2026-10-25_Family_Summary_Selected_Focus.png using a temporary isolated visual fixture; removed that frame after capture. Long content uses the existing scroll viewport and fixed footer.

These are stored-graph and visual checks. Live Present playback and server-backed persistence were not tested. This update supersedes the23October audit's statements that the summary is disconnected and pinned to the review fixture.
