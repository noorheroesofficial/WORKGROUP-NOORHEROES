# Motion and animation specification

[Index](00_MASTER_INDEX.md) · [Navigation](06_GLOBAL_NAVIGATION_AND_PROTOTYPE_ARCHITECTURE.md)

Motion serves continuity,selection and status. Avoid stimulus-heavy reward loops,flashes,random surprise reveals,parallax and automatic section reveals that conceal content. Each prompt supplies its own trigger/start/end/timing/interruption/reduced-motion/Figma table. Durations below are sourced where identified and otherwise explicit proposals requiring review.

| Pattern | Trigger and start/end | Timing/easing | Interrupt/reverse/leave | Reduced motion | Figma implementation |
|---|---|---|---|---|---|
| Screen transition | Approved action → next route | A1 slide+fade250–300ms ease-in-out; package proposal uses250ms dissolve unless direction is helpful | Back reverses route; leave cancels pending visual state; no input wait | Instant or≤100ms dissolve | Navigate to; Dissolve/Move in appropriate to screen; never animate backend validation |
| Splash logo | First visible launch → settled logo | A1≤1200ms gentle fade/scale; proposal400ms .98→1 | End immediately on route decision; bootstrap slow uses connecting state after2.5s cap | Static logo/loading label | Two matching states; Smart Animate if appropriate; After delay is visual timing only |
| Press feedback | Press/release → rest/pressed | A1 scale.96,100ms | Reverse on release/cancel; disabled no activation | Border/color change | While pressing → Change to; click separately executes approved destination |
| Selection | Tap option → labeled selected state | Proposal120–160ms ease-out | Reversible; no disappearance of choice labels | Instant check+label | Change to variant or variable state; don't assume variable update itself animates |
| Sheet/dialog | Open →visible; close →caller | Proposal200ms ease-out/160ms ease-in | Cancel/leave closes; restore focus; no mandatory dwell | Instant open/close | Open/Close overlay with supported Dissolve/Move in/out; not Smart Animate overlay |
| Expanded card | Tap expand →larger matching layout | Proposal200ms ease-out | Collapse reverses; long content accessible immediately | Instant height change | Matching component states + Change to/Smart Animate; scroll position verified |
| Loading | Actual pending operation →ready/error | Use minimal spinner; skeleton only if list/content body requires it | Stop on completion/error/leave; never perpetual decorative loading | Static labeled pending skeleton | Scenario variants; After delay may simulate response but is not a real timer/network call |
| Validation error | Failed input →text+icon/outline | Proposal120ms color/dissolve; optional shake omitted by default | Correction clears only relevant error; no repetitive shake | Same message/outline static | Variant with exact approved message; error feedback never motion-only |
| Success | Confirmed simulated outcome →check/status | A1 OTP≤500ms; proposal400ms | Actions enabled immediately; no repeated reward on resume | Static check/status | Matching success state; Navigate to correct branch after optional feedback |
| Reward/evolution | Confirmed milestone →subtle bloom/accent | Existing site≤2s; proposal400–700ms once | Skip/leave cancels; reversible viewing does not regrant reward | Static earned/mastery label | Matching layers/states; no gacha or random reveal |
| Voice/recording | Consent+OS grant+start →listening indicator | Proposal600ms calm pulse | Stop on cancel/background/permission loss/leave; no continued mic implication | Static Recording label | Idle/Recording variants; audio capture not implemented by Figma |
| Bedtime/Qadr | Authorized mode→calm theme | Proposal150ms dissolve; no celebration/shimmer loop | Preserve playback/calm context; stop on leave | Static dim theme | Separate calm scenario/state; no audio autoplay or bright overlay |

## Capability limits verified

Smart Animate compares matching layers and property differences; it is not a physical shared-element transition system or automatic navigation-history engine. Matching names/hierarchy must be checked and image/text changes may require dissolve. **Smart Animate is not supported for overlay actions**; use the supported overlay animation options. [Official Smart Animate reference](https://help.figma.com/hc/en-us/articles/360039818874-Smart-animate-layers-between-frames).

Set variable and Conditional actions support simulated state decisions. Keep selected answer/profile flags separate from real service outcomes; use alternate starting points for expired/offline/denied states. Do not claim that setting a variable provides production persistence or automatically animates a property change. [Official variables](https://help.figma.com/hc/en-us/articles/14506587589399-Use-variables-in-prototypes) and [conditionals](https://help.figma.com/hc/en-us/articles/15253220891799-Multiple-actions-and-conditionals).

Reduced motion is a separately reviewable prototype mode/start point,not an asserted automatic response to device accessibility settings. Production maps OS settings through the application's actual platform code. Hardware haptics,biometric dialogs,background audio and screen-reader focus require production verification beyond a Figma interaction.

## Performance/accessibility review

Prefer opacity/transform on a small number of layers; no full-screen continuous blur/particle rendering. No flashes or strobes. Avoid countdown announcements every second; announce relevant availability changes. Animate an illustration only after content and provenance approval,with a static alternative. Essential taps remain available during visual transitions; multiple fast taps do not duplicate operation/reward. Return from interruption restores logical state without replaying entrance reward animation.

For each future screen record actual durations,easing,delay(or none),interrupt/cancel behavior,destination and reduced-motion comparison. Test slow-device simulation and rapid navigation; a visually smooth prototype is not production performance evidence.
