# Final V2 Button and Loading Button library synchronization

Updated20October2026 in existing Figma file MR9935oQZACMjndzGIUgq5.

## Open the updated components

- [Button page319:2](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=319-2), original public set322:99.
- [Loading Button page327:2](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=327-2), original public set329:49.
- Source references: finalized Button section1355:2567 and loading overlays1383:3275.
- Review frames322:142 and330:8show all public states as instances. Dark examples322:158 and330:22remain available.

## Applied standard

Primary uses the exact approved multicolor teal gradient,18px corners, Poppins SemiBold14/20,4px content spacing,42% disabled opacity and88% pressed opacity. Source Large dimensions342×56are the main standard. All masters now default to342px width. Regular retains its48px height to preserve the existing size contract. Optional icon assets use18px canvases.

Secondary uses the existing theme-aware surface, foreground and border semantics; Quiet retains its lower-emphasis role. Focus retains a visible outline. Disabled has no prototype actions. Existing hover/press state destinations stay within the same Style and Size; their transitions use100ms Smart Animate.

Loading Button now shows only three centered10px dots, with7px gaps in a44×10group. Primary uses the same gradient and no stroke. Other styles use contrast-appropriate dot colors and surfaces. No button dimensions change during loading.

The old circular arc nodes were replaced inside the existing private phase component set328:2. Tone/Phase names and all10private variant IDs remain. Start initializes with visible dots. Quarter → Half → ThreeQuarter → Quarter forms a continuous wave, each step10ms delay +240ms ease-in-out Smart Animate, for a750ms cycle. Phase=Still has no reactions and shows static dots. No host submit/completion routes were added to generic Loading Button components.

## Compatibility and tokens

Public Button keeps30variants: Style Primary/Secondary/Quiet × Size Regular/Large × State Default/Hover/Pressed/Focus/Disabled. Original set, variant IDs, Label, Show icon and Icon property IDs are unchanged.

Public Loading Button keeps6Style/Size variants and its original Label property ID. That text property remains for compatibility but is visually hidden; the loader-only requirement takes precedence. Preserve the action's accessible name and expose busy status in application implementation.

New collection `NH/Button — Final V2` VariableCollectionId:1412:50contains14component-scoped variables. Gradient semantic tokens alias private raw colors copied from the approved source. Supporting surfaces/text alias existing theme-aware foundation colors. The update does not alter shared foundation values. Figma variable bindings for opacity use percentage values42/88, while node.opacity reads0.42/0.88; use the correct units when editing these variables.

No Code Connect or application-code integration was requested or implemented. Existing consumers can inherit library styling and default-size changes; no full-file application-layout regression review was performed. Finalized Login source components were re-read and passed geometry/fill/stroke/opacity preservation checks.

## Verification

[Audit results](audit.json): Button321checks and Loading Button95checks passed, **416total**. Checks include all public variants, original property IDs, source gradient matching, typography, dimensions, opacity,18px icons,42valid Button state routes, centered loader-only content,10private phase variants,750ms continuous loop graph and nonanimated Still states. No Button review label clipping was found.

Visual evidence:

- [Button light review](button-light.png)
- [Button dark review](button-dark.png)
- [Loader light review](loader-light.png)
- [Loader dark/Still review](loader-dark.png)

Saved native reactions and static rendering were verified. Live Present playback, exported motion/video, runtime accessibility and application integration remain unverified. These audits inspect Figma structure and interaction definitions; they are not production API tests.

[State manifest](figma-state.json), [Button audit source](audit-button.mjs), [Loading audit source](audit-loader.mjs).

