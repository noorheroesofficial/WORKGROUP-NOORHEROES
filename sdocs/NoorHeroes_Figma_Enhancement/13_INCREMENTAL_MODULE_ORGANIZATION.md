# Incremental Figma module organization

User-approved organization,13 October2026.

## Current hierarchy

- Existing mobile page928:2 (original references remain here unchanged).
- Main section1128:2: **NoorHeroes V2 Design**.
- Nested section1270:140: **Onboarding**.
- All15 current onboarding frames/dependencies moved into Onboarding: Splash and retained QA/reduced-motion variants, four Language states, four Intro slides, icon-component library and required Language Processing overlay.

Naming: `NH/V2/<Module>/<screen number>/<Screen_Name>/<State>`; local dependencies `NH/V2/<Module>/Components/...` and `NH/V2/<Module>/Prototype/...`. Existing root/frame IDs preserved. Language states consistently numbered002. Keep row/read order Splash -> Language -> Intro1..4; alternate states are grouped with their owning screen, not numbered as new journey steps.

## Mandatory rules for every future screen

1. Read the relevant PRD and blueprint and determine the real feature/module owner. Use those sources to select the section name. Names suggested conversationally (Home, Vehicle, Safety, Care, Profile) are examples, not permission to invent modules absent from NoorHeroes requirements.
2. Locate NoorHeroes V2 Design1128:2 on the existing mobile page. Reuse its Onboarding1270:140 for all remaining A1 Splash/Auth/Onboarding screens.
3. Create a module section only when authorized design work on that module begins. Never pre-create empty future sections. Reuse an existing matching section rather than creating a duplicate.
4. Put screens and their local prototype/component dependencies inside the owning module. Do not mix child/parent/admin/web surfaces or move original reference designs into the enhanced section.
5. Maintain logical user-journey ordering, state ownership and consistent names. Preserve nodeIDs whenever reorganizing existing work.
6. Read12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md and apply the approved visual standards. Requirements still govern purpose/content and existing confirmed destinations govern connections.
7. Before completion, check module placement, ordering, names, contents and reaction destinations. Organizational work must not alter source designs, copy, geometry or navigation. Report new section/nodeIDs and update the handoff.

## Verification of this organization

One module section created; no future sections created. Existing originals1095:2 and1085:13003 retained their bounds and child counts. All25 existing connected-control reaction definitions compared before/after and unchanged. All15 V2 objects accounted for inside Onboarding. No frames deleted; no styling changed. This was structural validation, not fresh prototype playback.
