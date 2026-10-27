# Parent PIN live-click target repair

22 October2026. User reported that live Continue did not open Confirm PIN despite stored-action tests passing.

## Investigation

PIN Continue1650:831 and Save PIN1709:749 were instance-level ON_CLICK targets on a shared button family. Its masters change Default→Hover on MOUSE_ENTER and Default/Hover→Pressed on MOUSE_DOWN, then Pressed→Hover on MOUSE_UP. Keypad digit master494:18 similarly changes to494:24 on ON_PRESS. Previous action-only tests did not exercise this pointer-driven target replacement. The observed component event conflict is the likely live failure mechanism; native Present reproduction remains unavailable and unverified.

## Repair

Moved application click reactions onto29 stable transparent Frame hit areas, above the existing24 PIN controls and5 biometric buttons. Each hit area has identical bounds and is above its original source. The presentation components, text, variant bindings and disabled/loading appearance remain intact, while the app click target no longer changes when a component variant changes. Source instance local click reactions are cleared to prevent duplicate submissions. Existing guards still enforce readiness, active screen and busy/saved state.

Mappings are in [the verification ledger](2026-10-22_PIN_Stable_Click_Repair.json). Important actions:

- Continue source1650:831 → stable target1718:803 → Confirm PIN1709:675.
- Save PIN source1709:749 → stable target1718:811 → processing1650:844 → Biometric1670:1069.
- Both PIN keypads and Delete controls have matching stable hit areas.
- Biometric Enable/Skip/Cancel/Error-retry button instances use stable targets too; existing Snackbar frames already have stable actions.

No screen was removed. All eight390×844 PIN screens remain. Keyboard actions remain on their original screen roots. No new feature, copy, server call, real PIN storage or biometric implementation was introduced.

## Verification

39 stored-action checks passed using the new hit targets. All29 targets are Frames with matching source bounds, top z-order relative to the source, local click handlers and no duplicate local source click. The confirmation screenshot is byte-identical to the previous screenshot, confirming no rendered design change. Screens remain preserved. Present playback is not verified, so this does not prove native pointer playback end to end.

Restart the prototype after loading the updated file, then test **enter4–6 digits → Continue → Confirm PIN → Save PIN → Biometric Enrollment**. Existing D review controls can reset session fixtures when needed. PIN matching remains a controlled count-based fixture, not secure digit comparison. Add Child remains uncreated/unmapped.

[Verification](2026-10-22_PIN_Stable_Click_Repair.json) · [Action test](2026-10-22_PIN_Stable_Click_Test.js) · [Unchanged confirmation image](2026-10-22_PIN_Stable_Click_Targets.png).

Future prototype corrections must test actual hit-layer ownership and inherited press/hover interactions, not only evaluate application ON_CLICK action arrays.

