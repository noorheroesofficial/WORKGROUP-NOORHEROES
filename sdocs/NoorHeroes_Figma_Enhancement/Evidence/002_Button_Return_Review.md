# Continue button — return and retry revision

2026-10-13. Current [Language screen](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1166-181). This revision supersedes the separate Success states in the earlier reference review.

## Sequence

Full-width teal Continue (350×64, x20, fixed footer) → 280ms Smart Animate to centered compact capsule (180×64, x105) → continuous linear spinner and repeating clipped indeterminate beam during simulated processing → inline completion check → 550ms expansion/translation back to original size and position → Continue fades back in. At 2.8s the prototype returns to the matching selected-language frame with no additional transition, ready to repeat.

Spinner rotates two full turns over 1.65s with linear easing. Beam resets only when outside the clipped rail. Spinner/rail fade away around 1.55–1.75s; inline check appears around 1.6–2.0s and disappears by 2.2s. Expansion begins at 2.05s and completes at 2.6s; label returns by 2.65s. Text remains 19px Poppins SemiBold, with no scaling or distortion. Header, list, selected locale, colors and typography are preserved.

Removed separate Success frames: 1174:546, 1174:593, 1174:640, 1174:687. Completion is an animation phase inside the existing button, not a separate success screen. Existing Loading frames 1174:318 / 1174:375 / 1174:432 / 1174:489 remain.

This is a repeatable, timed prototype simulation. It does not observe real data-saving state or hold indefinitely for a server. Production must continue its loading loop until the actual operation resolves, then play completion/restore, or restore after failure. No real persistence, network or next-screen navigation is claimed. Screen 003 remains unimplemented per user direction.

## Error and reduced motion

Press **E** during desktop prototype loading to simulate failure. Error frames en/hi/ar/ur: 1190:2 / 1190:160 / 1190:318 / 1190:476. They restore full-width Continue, retain the selected locale, and allow retry through the same loading sequence. Ordinary UI error copy proposed for this explicit requirement: `Couldn't save your language. Please try again.` The copy is a design proposal, not an existing PRD string. No debug controls were added to the product layout.

Reduced-motion processing frames: 1189:158 / 1189:315 / 1189:472 / 1189:629. They keep the button full width, use static `Saving…` feedback (proposed status copy), and restore Continue after simulated processing without translation, spinner rotation, or animation. Selected locale is preserved.

## Verification

Attached reference GIF inspected: 150×40, 100 frames; representative start and completion frames inspected. Its add-to-cart copy/colors were not imported into NoorHeroes.

Actual native [rendered button sequence](Language_Button_Return.mp4) inspected at 0.2, 0.9, 1.85, 2.35 and 2.65s: loader moving, check appearing, width/position restoring and undistorted Continue returning. Error screenshot inspected; message clear of footer. Reaction audit confirms zero separate Success frames and zero dangling destinations. Original Frame1/Frame2 dimensions, positions and direct-child counts unchanged. Cross-frame click morph, keyboard error trigger and timeout navigation are configured and read back; interactive Present playback has not been independently exercised. Timelines alone do not certify every prototype interaction.

Changes limited to Language Selection dependencies in V2 and sdocs evidence. Source PRD, blueprints, Screens, original Figma designs and other screens preserved. Stop for user review.
