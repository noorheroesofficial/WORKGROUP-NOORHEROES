# Profile Picker refinement — 26 October 2026

Applied in the existing Figma file MR9935oQZACMjndzGIUgq5, page 928:2, V2 1128:2, section 2188:7267. Original Default frame 2188:7275 remains the target. Source reference 1095:282 was inspected live. These changes supersede the previous picker footer, border, progress and scrolling notes; original/reference frames remain unchanged. No application code was changed.

## Applied UI

- Selected variants of NH/V2/ChildProfileCard 2232:10365 and every Add Child card now match reference Add Child 1095:356: teal #0E7C7B at 30% opacity, 2 px, dash 6/4, 16 px corners, matching stroke alignment. Unselected cards retain neutral solid borders. Selected text still distinguishes selection from authentication.
- Exact reference palette RGB is used with explicit stroke alpha because a variable-bound paint rendered at full opacity. No new palette color was invented. The final canvas shows the intended light teal border.
- Reused reference star artwork 1095:313, existing NH caption styles and gold palette colors. Zayd shows the original reference sample Level 2 • 35 Stars; Maryam shows Level 1 • 12 Stars. Both are labelled Sample. The saved profile has no authoritative earned-level/star source and displays Level — • — Stars. Saved setup values are preserved; no arbitrary rewards were assigned.
- Added configurable slot information based on PRD C24 FR-1 capacities: Free 1, Mobile Family 4, Premium Family 8. The three-child demo uses a clearly labelled sample Mobile Family plan. Empty Free has one slot; single-child Free has no slots and uses existing disabled-text colors. Available count is max minus used, clamped at zero. Slot text updates for capacities 1, 4 and 8.
- Removed the entire old Manage profiles in the Parent area / Back to setup footer. Essential toolbar Back navigation is preserved.
- Every mobile picker state now has one full-page vertical scrolling viewport. Toolbar and content scroll together; inner profile viewport scrolling was removed. Content hugs height, with 24 px bottom clearance. Empty-state Add Child and Parent cards remain side by side.
- Added No child selected scenario 2269:12112; existing selected/unlocked/locked/mixed/single/long-name/error/loading/offline scenarios remain.

## Verification

57/57 checks passed against actual Figma reaction JSON and live node properties. Coverage includes prior independent child PIN/pattern/biometric/recovery flows, caller-aware cancellation, border equality with the source Add Child card, 1/4/8 capacity arithmetic, empty/full slots, selection changes, distinct sample progress, removed footer text, one scroll container per page and bottom clearance. No missing destinations were found in the evaluated existing security flows.

A temporary 390 × 640 clone verified that the full-page viewport stretches to 640 px while 812 px of content remains scrollable through 172 px, with 24 px trailing clearance. The temporary clone was removed. Only the standard 390 × 844 designs remain.

Final canvas views inspected: Default, Free/full, No selection and Empty. PNG evidence is named 2026-10-26_Profile_Refinement_Default.png, _FullFree.png, _NoSelection.png and _Empty.png. The JSON checks file records IDs, variables, assertions and the height check.

## Explicitly deferred and unverified

The user chose to keep Add Child navigation pending after being informed that its existing form replaces the single saved prototype profile instead of appending another child. No form route was added. Child Home navigation also remains pending from the earlier explicit decision. Slot availability is displayed, but the pending Add Child card has no executable navigation, including at full capacity. Existing lock/PIN/biometric and recovery behavior remains connected.

Live Present/run-mode playback remains unverified because of the existing saved browser restriction. Reaction evaluation and screenshots are not live playback or device/backend evidence. OS safe areas, keyboard behavior, screen readers and production entitlements/authentication were not tested. All displayed paid-plan/slot information is clearly identified prototype sample data, not account billing data.
