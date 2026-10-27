# Source audit and access status

Prepared 13 October 2026, Asia/Kolkata. Documentation only. [Index](00_MASTER_INDEX.md).

## Authority and scope

PRDs govern behavior, required content and business rules. Existing mobile flow is the current-experience reference subject to those requirements; Frame 1 provides the PRD-based structure; Frame 2 provides visual inspiration. Recommendations are proposals. Corresponding mobile KMP blueprints and the workgroup discrepancy register inform alignment but do not silently override a product requirement. Website/admin/parent-web designs are excluded.

All outputs reside in this new `sdocs/NoorHeroes_Figma_Enhancement/` package. Existing SAM contracts, epics, stories and `sdocs/design/noorheroes-v2/` were not overwritten. This is a design documentation intake, not a replacement PRD or a software implementation plan. The sam-plan research/validation approach was adapted to the user's requested artifact structure; no software story completion or TDD claim is made.

## Access results

| Source | Result | Evidence / limit |
|---|---|---|
| Local PRD directory | Accessible: 48 Markdown files catalogued | [Manifest](Evidence/source-manifest.json). A1–A12, B13–B18, C19–C26 and F35–F37 reviewed for mobile requirements; lists and brand sources catalogued; E28–E34, D27 and website content excluded from screen generation. |
| Mobile PRDs | Product requirements, screen inventories, important UX/click tables, Android and QA contexts extracted and audited | [Child learning](Research/child-learning.md), [parent](Research/parent.md), [supporting](Research/supporting.md), [onboarding records](Research/onboarding-enriched.json). Extraction is not proof that every infrastructure/analytics paragraph was semantically reviewed. |
| KMP / visual blueprints | Feature objectives, screen mapping and mobile constraints inspected | Exact paths linked in prompts. Generic blueprint per-screen boilerplate is distinguished from specific PRD states. Source filename ordering is not journey ordering. |
| Screens/Mobile App | Accessible; clusters inventoried | 82 representative PNGs visually inspected: onboarding13, child-learning10, parent7, supporting52. Other cluster images are candidate references, not claimed visually reviewed. No admin/web PNGs used as mobile screens. |
| Current site | Browser access succeeded; text-oriented web open failed | [Current site](https://noorheroes.figma.site/). [102 catalogue captures](Evidence/current-site-screens.json):101 direct mobile surfaces/state previews + Ramadan module entry. [20 Ramadan subpreviews](Evidence/current-site-ramadan.json). The module entry is a review shell, not an app screen. |
| Figma file | Accessible through official Figma connector | [Mobile page](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=928-2). Exact page name `📱 NH Mobile `, ID `928:2`. |
| Frame 1 | Identified and structure/text inspected | Container `1095:2`,16704×10825;70 direct children, including two standalone identity assets. 70 compact nodes extracted. |
| Frame 2 | Identified and structure/text inspected | Container `1085:13003`,15314×10825;35 direct children.34 mobile/combined reference surfaces extracted;1280-wide master design hub excluded from screen-copy extraction. |
| Figma visual comparison | Four representative renders actually viewed | Frame1 Intro1 `1095:936`, Frame2 Intro1 `1085:19139`, Frame1 Home `1096:1090`, Frame2 Home `1085:16820`. Remaining frames structurally/text inspected, not claimed fully visually validated. |
| Figma components/prototype | No component instances or descendant reactions found in104 extracted children | These are flattened imported layouts. A naming/layout/content extract is not a production-ready component library or a wired prototype. Complete fill/style bindings, all image provenance and all constraint properties remain a future focused inspection requirement. |

The large page metadata exceeded practical output limits; bounded, compact read-only node extraction succeeded. All Figma scripts only read properties and selected the page for inspection. No node was created, duplicated, moved, renamed, styled or deleted. Switching inspection page does not modify designs.

## Existing design direction verified

Current site advertises teal/gold/cream tokens, Poppins UI, Playfair Display branding and Noto Naskh Arabic. Local onboarding screenshots show cream surfaces, rounded forms, teal CTA, gold branding and restrained symbolic illustration. Figma Frame1/Frame2 renders contain richer image-led compositions, rounded surfaces and card hierarchy. These are retained as references; no new art direction is selected automatically.

The site is explicitly a session-only UI prototype. Authentication, permissions, privacy actions, support delivery, billing, media and sync are not connected; gates demonstrate navigation, not security. This warning is source evidence, not copy to put inside the real app. Site sidebar numbering includes web/admin/asset-library entries and state previews; it is not the mobile production navigation stack.

## Content verification boundary

Exact strings are captured, not independently authenticated as scholar-approved/legal-approved content. Frames include Quran references, translations, real-sounding scholar/institution claims and sample child names/statistics/prices. Their verification provenance was not supplied. Preserve source strings in the audit; do not silently publish those claims or rewrite religious content. Obtain original content IDs, version and scholar/legal approval where required.

Supported locale differences are unresolved: the site lists eight languages, screenshots show French while some mobile requirements/blueprints mention Hindi, and Frame2 offers alternate locale sets. Do not import the marketing site's locale roster as mobile authority. Each verified localized string remains verbatim; missing translations are blocked.

## Completeness and accessibility limitations

The package accounts for independently reviewable mobile inventory surfaces, shared contextual aliases, important missing exercise layouts and broken destinations. It does not claim that all existing PNG variants, every image asset, all paragraph-level PRD material or all Figma style/constraint details have received final visual review. Each unreviewed variant must be inspected collectively before that screen's implementation.

Accessibility requirements are derived from A1 §1.8/§2.1 and feature rules: contrast,44-unit targets,200% type,RTL, alternatives to gestures and restrained motion. Actual enhanced-screen accessibility cannot pass before designs exist. [Accessibility specification](08_ACCESSIBILITY_RESPONSIVENESS_AND_EDGE_CASES.md) separates document checks from future design checks.

## Refresh before execution

1. Confirm the source manifest has not changed and read the screen's exact PRD/blueprint sections.
2. Reinspect the actual target Figma node and all mapped PNG variants, rather than assuming the captured design remains current.
3. Resolve its decision-register entries and missing exact copy.
4. Approve the enhanced working area and token/component changes.
5. Execute one screen; document created IDs and test evidence; wait for approval.
