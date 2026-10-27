# Complete intro consistency review — 2026-10-13

Scope: all four V2 intro roots1215:34,1215:138,1215:246,1215:356. Original references unchanged.

## Audit findings and resolution

Mixed legacy filled vectors, outline emoji glyphs and Material icon artwork caused perceived-weight differences. All28 visible intro icons now use reusable components from one official Material Icons Round family, keeping meaning (caption verified/audio/star/shield, footer lock/verified/lock/timer). Shared local component frame1253:34 contains30 icon components (15 meanings x18/14px). Main/caption/navigation icons18px; footer14px. Teal fill common across roles; CTA arrows white. Original artwork is reused where compatible; the legacy mixed glyph sources are superseded by rounded equivalents per user consistency instruction.

Feature cards previously used manual independent icon/title/tag/body positions. All12 now use horizontal Auto Layout with centered36px icon tile,12px icon-to-copy gap and vertical text stack. Card350x84, horizontal padding12, vertical8, list gap8. Title12/17 SemiBold, tag9/13 SemiBold, description11/16 Regular. Text stack278px wide,2px internal gap, auto height. No icon shifts when a description wraps.

All equivalent text roles use shared NH/Intro text styles. Poppins for Latin; Noto Sans Arabic for mixed Arabic category labels. Explicit pixel line heights. Heading20/28 SemiBold centered in56px shared slot; body12/18 Regular centered in36px slot. Shared copy stack uses vertical Auto Layout132px height and46px gap before cards, making card Y414 on every screen. Category/heading/body widths350.

Captions: hug horizontal Auto Layout,12px horizontal/8px vertical padding,4px icon-text gap. Footer:14px icon,2px gap,4px row padding. Caption and footer groups centered atscreenX195 on all screens. CTA text+18px arrow centered together,4px gap, consistent56px button.44px Back/Skip touch targets retained. Background alpha45% retained.

## Validation

Audited every text role/icon group in all four frames. Verified equivalent style IDs, font sizes, weights, line heights, icon-instance sizes, card geometry and caption/footer center axes from Figma read-back. Compared all four screens at identical0.85 scale using a temporary review frame; inspected icons, copy wrapping and spacing. Temporary review frame and clones removed after capture. Inspected Parent screen additionally at1x. All approved text strings compared before/after and matched. No clipping, overlapping text or inconsistent icon family visible in final reviewed set. Route reactions on controls retained. Motion playback not exercised by this layout task.
