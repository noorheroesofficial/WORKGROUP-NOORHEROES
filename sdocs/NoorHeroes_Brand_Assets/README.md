# NoorHeroes Brand & App Assets

Prepared 15 October 2026. The supplied logo images are the visual authority for this library.

[Open the dedicated Figma page](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1299-2).

## Contents and editing

The page contains the ten requested sections, 64 reusable components and six variant sets. Logo artwork is embedded from the supplied raster originals. Template text, backgrounds, tab lines and layouts remain editable. Source artwork is retained separately in the Brand Reference section. Existing app screens were not part of this work.

The export manifest identifies each source node, background, master dimensions and scale. The PNG inventory includes Android density exports, iOS master and separate layers, logo and wordmark variants, app banners, social templates, profile images, and clean/editable-copy cover layouts. Editable-copy PNGs are previews; edit their source components in Figma before publishing.

Use the masters or the Export-Ready Assets catalog, not both, when bulk exporting: catalog instances mirror the masters and would produce duplicate files. Preserve aspect ratio when resizing identity artwork. Use the symbol instead of the full lockup at small sizes.

## Source fidelity

- Original green/gold wordmark, full lockup and crescent/lantern/NH symbol are retained as supplied; their lettering is not retyped.
- Exact teal and ivory background reference images are included. Additional editable flat-background compositions use sampled teal `#074D4D` and ivory `#FEFBF4`; these are approximations of the photographic backgrounds, not claims that a solid color reproduces their texture.
- Monochrome treatments use the original alpha silhouette with a solid fill. They are derived treatments, not new vector drawings.
- Poppins is used for editable template copy. It does not replace the lettering within the logo artwork.
- The illustrated campaign reference is retained as a reference; its alternate playful wordmark is not substituted for the identity artwork.

## Android handoff

Adaptive foreground and monochrome layers use a 432 × 432 source canvas representing 108 dp at xxxhdpi. The symbol is contained within the central safe region. Five density exports are provided at 108, 162, 216, 324 and 432 pixels. Pair a transparent foreground with the corresponding full background. Legacy icons are provided at 48, 72, 96, 144 and 192 pixels. Masked and safe-area previews are design checks.

Final Android resource wiring, launcher behavior and device testing remain integration work. The detailed source symbol loses lantern detail at small sizes; the overall crescent/NH silhouette remains the intended recognition cue. No unsupported simplified emblem has been invented.

Source: [Android adaptive icon guidance](https://developer.android.com/develop/ui/compose/system/icon_design_adaptive).

## iOS handoff

The 1024 × 1024 opaque masters have square corners. Rounded previews are for inspection only. Separate transparent foreground and opaque background artwork are supplied for downstream composition. Final Icon Composer/Xcode assembly, appearance variants and device validation have not been performed on this Windows workspace. Do not treat these PNGs as a completed `.icon` project or submitted asset catalog.

Source: [Apple Icon Composer workflow](https://developer.apple.com/documentation/Xcode/creating-your-app-icon-using-icon-composer).

## Social and cover specifications

| Use | Pixels | Status |
|---|---:|---|
| Square post / announcement | 1080 × 1080 | Working template; check destination before publishing |
| Portrait / education | 1080 × 1350 | Working template; check destination before publishing |
| Story / launch | 1080 × 1920 | Working template; check destination overlays before publishing |
| Profile | 400 × 400 | Square master; circular preview provided |
| YouTube cover | 2560 × 1440 | Central safe region used; preview across devices before upload |
| Facebook page cover | 851 × 315 | Provisional; official page was inaccessible during verification |
| LinkedIn company cover | 1512 × 256 | Based on the live help page, not stale search snippets |
| X header | 1500 × 500 | Central content kept away from crop edges |
| Website hero | 1920 × 640 | Project template; responsive implementation remains downstream |

Sources checked during preparation: [YouTube channel branding](https://support.google.com/youtube/answer/10456525), [LinkedIn page image specifications](https://www.linkedin.com/help/linkedin/answer/a563309/image-specifications-for-your-linkedin-pages-and-career-pages), [X profile image guidance](https://help.x.com/en/managing-your-account/common-issues-when-uploading-profile-photo).

Neutral placeholder copy must be replaced with approved campaign copy. No new Quranic verses, religious claims or Arabic calligraphy were created. Safe-area guides are design aids; final destination cropping and overlays still need an upload preview.

## Missing source variants and limits

No isolated NH-only or crescent-plus-NH-without-lantern artwork was supplied. These variants were withheld rather than reconstructed. The approved crescent/lantern/NH composition is used for the symbol collection.

No true vector logo source was supplied. Raster artwork remains raster inside Figma, and PNG exports do not become vector artwork through an SVG wrapper. A genuine editable vector identity package requires the original vector master.

## Quality evidence

See `evidence/final-png-audit.json` for actual exported dimensions, alpha ranges, file hashes and comparison metrics against the original crops. See `EXPORTS.md` for filenames and source links. Evidence images show the Figma library sections. Visual layout checks do not replace launcher/device or social-upload testing.
