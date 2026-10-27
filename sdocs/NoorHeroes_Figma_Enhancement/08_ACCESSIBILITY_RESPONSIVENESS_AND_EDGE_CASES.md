# Accessibility,responsiveness and edge-case requirements

[Index](00_MASTER_INDEX.md) · [Component contracts](05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md)

## Acceptance measurements

Requirements from A1 §1.8/§2.1 and feature-specific sections: body contrast≥4.5:1; large text≥3:1; essential nontext control indicators≥3:1; minimum44×44 logical-unit target;200% dynamic text without truncation/overlap. A2 child tasks for the youngest band use≥56 targets where specified. Platform coordinate units must be translated correctly by implementation; Figma pixel measurements are design references,not automatic dp/pt compliance.

No color-only selected,locked,error,downloaded or completed state. Add visible labels/icons and meaningful reading order. Icon-only product controls have action-specific labels; decorative images are ignored; meaningful illustrations have concise existing/approved description. Charts and maps need equivalent text summaries and ordered lists. Audio has approved captions/transcript where the feature requires it. Never omit canonical text or its translation to make a card fit.

## Layout test grid

| Test | Expected behavior |
|---|---|
|320,360,390,420 logical widths | Single-column hierarchy; cards wrap; no horizontal clipping; grids reduce/stack as needed |
| Short viewport and landscape interruption | Primary action reachable through scroll; keyboard does not cover focused field/error/submit |
|200% text | Headers/labels wrap; body hugs height; no fixed text-height clipping; footer does not cover final section |
| Safe areas | Top status area and bottom system/home area excluded from tappable content; bottom-nav/footer clearance real,not assumed constant |
| Long Arabic/Urdu | RTL order/alignment and directional arrows; full shaping/diacritics; Arabic paragraphs never distorted or truncated |
| Mixed-script/numeral content | OTP digits retain LTR numeric-entry sequence; verified punctuation/numeral convention unchanged; timeline/chart direction intentional |
| Long localized legal/validation text | Scrollable readable body and version; error under correct field; no improvised translation |
| VoiceOver/TalkBack equivalent | Logical headings/control labels/selected status/error announcements; no gesture-only choices |
| Reduced motion | Same feedback/actions in static or≤100ms dissolve state; no compulsory loop/reveal |

Do not claim full screen-reader verification from a static Figma image. Document accessible names/roles/order; test native implementation separately when it exists. Figma prototype focus/history is a design approximation.

## State relevance and interruption rules

| Context | Required handling | Do not add indiscriminately |
|---|---|---|
| Bundled intro/static illustration | Offline display,back/skip,large-text alternative | Fake network skeleton/success/error screen |
| Auth/consent/PIN/profile save | Format/grant errors,pending,server failure,offline draft,resume,enumeration-safe response | Unverified identity success; child-data collection before legal grants |
| Content lists | Loading,cache/empty/offline,withdrawn/unavailable content,filtered no results | Empty state for a populated static legal document |
| Learning/recording | Consent denied,OS denied,hardware/no-service,offline/listen-only,interruption stop | Mic gate that blocks all learning or continues after navigation |
| Quiz/game | In-progress restore,withdrawn question,answer validation,accessible ordering,offline completion/queued evidence | Invented immediate mastery/score/reward before authoritative result |
| Player | Buffering/retry,resume,content withdrawal,sleep timer,headphone/audio interruption,bedtime boundary | Loud completion reveal in bedtime; unconditional quiz at sleep boundary |
| Favorites/downloads | Pending sync/rollback,expiry,storage/cap,wifi policy,withdrawal,cancel/retry | Generic 'no internet' where storage/cap caused failure |
| Parent reports | Date/child context,no-data,delayed/partial/stale,permission status | Fabricated percentages or sibling ranking |
| Controls/consent/device revoke | Step-up validity,save pending/error,prior value on failure,offline limitations | Prototype as security proof or real destructive operation |
| Billing | Disclosure before purchase,store handoff,cancel/pending/failed/restored state | Sample price as live offer,child purchase route,pressure countdown |
| Seasonal | Server region/Hijri override,night eligibility,missing pack,post-Eid archive,aggregate-only data | Device clock as religious authority,per-child fasting competition |

Back/cancel must preserve input and selected child unless a cited privacy rule requires clearing it. Retry uses the same logical operation/idempotency where applicable. Canceling a visual transition does not imply canceling a server operation. Returning from expired authentication reevaluates policy/permissions before restoring a permissible draft. Old-child responses never render in a new context.

## Platform differences supported by sources

Shared mobile flow/visual hierarchy remains consistent. Android OTP auto-read is optional; denied permission falls back to manual entry. OS biometrics are optional and device-supported; unavailable hardware hides enrollment and PIN remains durable fallback. Native permission prompts,system Back/iOS back gesture,keyboard,safe areas,store checkout/share and audio interruption are platform adapter behavior. Apple Login is explicitly unsupported by A1 even on iOS; do not add it as a visual convention. Purchase provider/restore policy must be reconciled with C24 and actual platform requirements before execution; no new billing logic is invented here.

## Religious content and privacy

Preserve source Arabic,Quran/translations,hadith and approved educational strings exactly. Inspect full glyphs at target font size and line height; no generated diacritics,simplification or automatic transliteration. Require original content/version/scholar provenance before publishing disputed strings or institution claims. Legal strings require approved localized version. Sample child/profile/report values remain fixtures and are not verified facts about a real family. Never include tokens,real OTP/PIN or raw private transcripts in evidence.

## Open design decisions

Locale roster,age-band conflict,optional reveal/primer detail,missing legal text,unmatched controls and broken family-deletion/timeline references remain decision-register items. A required behavior whose exact text is unavailable remains documented and blocked; it is not silently omitted or filled with generic copy.
