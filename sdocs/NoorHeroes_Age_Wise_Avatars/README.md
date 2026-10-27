# NoorHeroes V2 — Age-Wise Avatar Library

Created 22 October 2026 with Canva image generation.

[Open the complete Figma section](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1847-3309).

## Delivery

80 additional original avatars, with 20 separate 1264 × 1264 PNGs per age group. Each group contains ten female and ten male character presentations. Files are in four folders under `assets/`. See [ASSET-INDEX.md](ASSET-INDEX.md) for all 80 Canva originals and individual Figma node links.

| Group | Count | Figma frame | Canva originals |
|---|---:|---|---|
| Ages 5–8 | 20 | [Avatar Library — Ages 5–8](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1847-3310) | [Ages 5–8](https://www.canva.com/folder/FAHYtoS01rE) |
| Ages 8–10 | 20 | [Avatar Library — Ages 8–10](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1847-3381) | [Ages 8–10](https://www.canva.com/folder/FAHYtkhLWw0) |
| Ages 10–14 | 20 | [Avatar Library — Ages 10–14](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1847-3452) | [Ages 10–14](https://www.canva.com/folder/FAHYtmNIwh4) |
| Ages 14–18+ | 20 | [Avatar Library — Ages 14–18+](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1847-3523) | [Ages 14–18+](https://www.canva.com/folder/FAHYto5Vpa8) |

The four frames sit inside a new section below the existing NoorHeroes V2 Design area on the NH Mobile page. Every avatar has its own selectable image node, sequential label and 1264 px PNG export preset. Auto Layout maintains five columns and four rows with 120 px previews.

## Visual direction and review

The existing NoorHeroes avatar collection and the earlier attached references supplied the soft 3D rendering direction. Two completed Canva avatars from the existing collection were used as style references. New prompts explicitly varied facial structure, complexion, hair, headwear, clothing, accessories and expression, with age-specific proportions.

Ages 5–8 use rounder faces and larger expressive eyes; ages 8–10 use more developed schoolchild proportions; ages 10–14 use longer youthful faces, smaller eye-to-face ratios and adolescent shoulders; ages 14–18+ use refined facial structure and more mature teen/young-adult styling. The older group includes intended ages from 14 into the early twenties. These are artistic age categories, not verified ages or strict automated account-routing rules.

All 80 outputs were reviewed individually through the original-resolution contact sheets for age appearance, face clarity, framing, anatomy, style consistency, unwanted text and duplicate characters. The four sheets are in `evidence/contact-*.png`. Final Figma renders provide a second layout review. No unsuitable image was included solely to meet the count.

The original 20-avatar collection is retained separately. Exact file hashes for this new collection are distinct from one another and from that prior set. Existing page-frame geometry and the previous library are checked against the live baseline in the Figma audit.

## Files and integration metadata

- `avatar-metadata.json`: 80 populated reusable records with stable IDs, portrayed ages, alt text, Canva provenance, file dimensions/hashes/storage keys, Figma mappings and review status.
- `avatar-metadata.schema.json`: JSON Schema for the metadata structure.
- `EXPORT-AND-STORAGE.md`: exact export, naming, size, storage and revision requirements.
- `generation-plan.json`: generation prompts and intended character variations.
- `evidence/`: original-image audits, contact sheets, Figma audit and final render evidence.

The delivered originals have opaque ivory backgrounds and square corners. The app can apply circular clipping. The Figma previews have a 16 px corner radius; use the packaged masters when square corners are needed.

Canva gave the original downloads .jpg filenames while their decoded contents were PNG. File extensions were normalized without resizing, recompression or changes to the downloaded bytes. The 200 px connector thumbnails were used only for progress review; all delivered and imported source images are 1264 × 1264 originals.

Agent review is recorded separately from user approval, which remains pending. The illustrations are raster images; individual facial features are not editable vector shapes. Cloud storage deployment and application integration have not been performed.

