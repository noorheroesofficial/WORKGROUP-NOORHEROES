# Language Selection — current reference revision

2026-10-13. This report supersedes the earlier Screen 002 review and QA snapshots. Default frame remains [1166:181](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1166-181) in V2 1128:2.

## User decisions

- Match the attached Language.png layout, restore Continue, animate selection and processing. This latest request overrides the previously approved immediate navigation without Continue. Keep the approved four-language roster: English, Hindi, Arabic, Urdu. No additional preview locales were introduced.
- Delete exactly the named QA320, QA360, QA420, QA320-Text200 and temporary Intro handoff frames. Removed IDs: 1168:128, 1168:162, 1168:196, 1168:230, 1168:2. Absence verified. Original mobile containers and Splash QA frames remain.
- User explicitly selected **Wait for Screen 003; keep success destination pending**. Success therefore has no onward destination until Screen 003 is approved. No replacement handoff was created.

## Design

Reference hierarchy retained: globe badge → exact heading → exact supporting copy → single-column cards → fixed Continue footer. Cream #FAF7F0, teal #0E7C7B, white cards, selected neutral tint #EFF0EA, rounded 18px cards, 20px horizontal margins. Heading 25px Poppins SemiBold; language 16px; autonym 14px with native script fonts. Secondary ink #606B72 maintains readable contrast. Four languages and verified autonyms remain unchanged. English is visibly selected in the screenshot-matched default.

Cards are 350×81 at 390 viewport width. List viewport begins at y232 and ends at y722; footer begins at y736, with 14px clearance. Continue is 350×64 at x20, y752; bottom clearance 28px. The list viewport clips and scrolls independently; footer stays outside its scroll container. No status/claims/religious copy was invented.

Font-based emoji flags disappeared in server-rendered video, so they were replaced with source artwork from Google Noto Emoji `third_party/region-flags`: SVG IN/SA/PK and PNG GB. The PNG avoids unsupported SVG stroke rendering of the Union Jack. Sources: `https://github.com/googlefonts/noto-emoji/tree/main/third_party/region-flags`. Flag text/details were reused from supplied artwork, not generated. Their asset license is stored in Flag_Artwork_LICENSE.txt.

## Motion and interactions

- Default entrance: each card opacity 0→1 and vertical offset 10→0, ease-in-out, 70ms stagger, settling by approximately 690ms. Only first-entry Default plays this sequence; selecting another locale does not replay the entrance.
- Locale tap: 160ms Smart Animate between matching layers; selected border, tint and checkmark change. Selection stays on Language Selection. Already-selected locale is a no-op. Local save and profile sync are production responsibilities, not real Figma persistence.
- Continue: 280ms ease-in-out Smart Animate changes the same named button from 350px to 180px centered capsule; label fades out, spinner/progress appears. Header/cards remain in place and preserve selected locale.
- Loading: spinner rotates smoothly; a white beam traverses a clipped 120px rail. This is indeterminate simulated processing, not a real percentage or network request. Loading states disable row and button actions to prevent duplicate activation.
- After 1.65s simulated processing: 180ms transition to a success checkmark. Each locale retains its own selected context. Success awaits Screen 003 by user decision.
- Reduced-motion frames: English 1168:264; Hindi 1176:2; Arabic 1176:49; Urdu 1176:96. No entrance, movement, spinner or transition. Selection remains available; Continue shows corresponding static success without decorative processing delay.
- Normal Loading IDs: en 1174:318, hi 1174:375, ar 1174:432, ur 1174:489. Success IDs: en 1174:546, hi 1174:593, ar 1174:640, ur 1174:687.
- Screen transitions cancel the current frame's motion. First-launch Splash still points to Default. Back/restore/session state remain production rules; no unsupported state logic is claimed.

## Evidence and limits

Rendered native timelines inspected at 0.2, 0.6 and 1.2 seconds for [list entrance](Language_List_Entrance.mp4) and [loading](Language_Button_Loading.mp4). Flags, stagger, spinner rotation and moving progress beam appear in rendered output. Static screenshots inspected for default, loading and success. A final secondary-text contrast refinement was made after those recordings; only secondary text color differs from the saved motion videos.

Reaction definitions and matching button hierarchy were inspected. No reaction points to a deleted node. Click-driven Smart Animate morph and cross-frame success navigation are configured but have not been exercised in interactive Present; timeline video alone does not certify cross-frame interaction playback. Full localized interface/Intro copy and RTL verification remain pending, and no translations were invented. Old narrow/200% QA frame results describe the superseded layout; those frames were deleted as requested and are not claimed as current verification.

Original Frame1 1095:2 retains x35456/y29879/16704×10825 with 70 direct children; Frame2 1085:13003 retains x52995/y29879/15314×10825 with 35 direct children. All writes stayed in V2 and documentation evidence. Source PRD, blueprints, Screens, web/admin designs unchanged.

Stop for user review. Connect success when approved Screen 003 exists.
