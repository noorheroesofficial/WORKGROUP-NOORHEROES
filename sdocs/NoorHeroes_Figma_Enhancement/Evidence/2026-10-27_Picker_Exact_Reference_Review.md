# Profile Picker reference correction — 2026-10-27

Updated existing Figma file MR9935oQZACMjndzGIUgq5, V2 picker 2188:7275 and its existing states. Inspected live reference 1095:296 and Add Child 1095:356; compared rendered reference and current screen.

## Applied
- Existing NH/V2/ChildProfileCard family 2232:10365 updated in place, all eight variants.
- Cards 168 × 209.5 px, radius 16; selected solid teal 2 px border from 1095:298 plus 2 px gold outer outline. Rounded 21 px Active badge and 64 px gold-ringed avatar.
- Level/star badge now content sized, centered, and baseline aligned; existing source data retained.
- Existing Add Child tiles now reference-shaped 168 × 200.13 px vertical cards: 56 px circular plus, dashed 2 px teal border, radius 16, reference background/effects. Real PRD-backed slot counts and sample plan label retained.
- Grid 350 px, 14 px gaps. All existing picker states updated; Empty retains side-by-side tiles.
- Existing NH Poppins typography, functional lock controls, background/gradient and saved content retained. Reference checkmark does not replace the functional lock control.
- Removed footer stays removed. One full-screen scroll container remains; 390 × 640 QA clone verified and removed.
- Retry feedback preserved. Add Child icon/title respect slot availability.

## Verification
64/64 actual Figma structural and reaction-graph checks passed; all 18 referenced destinations exist. Includes selection independence, PIN/pattern/biometric and verified-parent recovery, cooldowns, data/slot preservation, reference card borders/dimensions, Add Child geometry, background, footer removal and scrolling.
Screenshots: 2026-10-27_Picker_Reference.png, _Before.png, _After.png, _Empty.png.

Live browser Present playback remains unverified because browser access was previously rejected by saved permissions. Graph evaluation is not playback evidence.
Add Child and Child Home destinations remain explicitly pending per user decisions; no routes invented. No app code changed.

