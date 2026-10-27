# NoorHeroes age-wise avatar export and storage contract

This is an asset handoff contract. It does not create an API, database table, cloud bucket, application route or production integration.

## Required master files

| Property | Exact requirement |
|---|---|
| Collection | `noorheroes-v2-age-wise` |
| Groups | `5_8`, `8_10`, `10_14`, `14_18_plus` |
| Count | At least 20 individual images per group |
| Filenames | `avatar_{groupKey}_{twoDigitIndex}.png` |
| Master dimensions | 1264 × 1264 pixels; aspect ratio 1:1 |
| Format | Valid decoded PNG; MIME `image/png` |
| Background | Opaque warm ivory; square full image |
| Maximum file size | 10,485,760 bytes per master |
| Integrity | SHA-256 of the exact delivered bytes |
| Local path | `assets/{groupKey}/{filename}` |
| Proposed object-storage key | `avatars/v2/age-wise/{groupKey}/{filename}` |
| Figma preview | 120 × 120 px; individually selectable image fill |
| Figma preview corners | 16 px radius, applied by the preview node |
| Figma PNG export preset | Width 1264 px; use the packaged master for full square corners |

The original downloads are retained byte-for-byte. Canva may name a download with `.jpg` even when the file contains PNG bytes; identify the format by decoding it, then normalize the filename to `.png`. Do not enlarge the connector's 200 px thumbnails and call them originals.

No rounded corners are baked into the packaged masters. The consuming application should apply its own circular or rounded clipping. Keep the head centered and retain the square master for future crops. If new compressed derivatives are required later, generate them from these originals and record separate dimensions, byte counts, MIME types and hashes.

Preserve source color data and embedded profiles when present. Do not claim a particular embedded profile when a PNG is untagged. Do not recolor or recompress a master in place. A replacement illustration requires a new revision and a new content hash; preserve the earlier file and metadata for traceability.

## Reusable metadata

`avatar-metadata.schema.json` defines the reusable manifest structure. `avatar-metadata.json` is the populated deliverable. Each avatar records:

- Stable ID, age-group key, intended portrayed age and character presentation.
- Display label and descriptive alternative text.
- Canva provider, media ID and original image link.
- Master path, proposed storage key, decoded format, dimensions, bytes and SHA-256.
- Figma file, frame, image node, link and preview dimensions.
- Agent review checks and a separate user-approval status.

The four user-specified ranges overlap at ages 8, 10 and 14. They are visual collection categories. Do not infer an automatic account-age routing rule from these labels. `portrayedAge` records the generation brief's intended age, not a verified age of a real person. The final `14_18_plus` category remains open-ended for future young-adult entries; this batch targets older teens and young adults rather than middle-aged characters.

`review.status = agent-reviewed` means the artwork passed the agent's visual review. It is separate from `review.userApproval`, which remains `pending` for the user's review. Do not publish the collection merely because a metadata record exists.

## Validation before storage or integration

Decode every file and verify dimensions, MIME, PNG signature and size. Confirm that all IDs, paths and storage keys are unique. Match each file hash to the manifest. Require at least 20 entries per group. Validate the manifest against the schema and verify its Figma links refer to the correct group frames.

Cloud storage provisioning, access permissions, CDN configuration and application integration remain separate work. The storage keys above are exact proposed keys, not claims that files have been deployed to a cloud service.
