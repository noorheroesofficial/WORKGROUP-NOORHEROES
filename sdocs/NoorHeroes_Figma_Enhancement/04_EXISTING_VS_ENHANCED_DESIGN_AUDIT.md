# Existing versus enhanced design audit

[Index](00_MASTER_INDEX.md) · [Traceability](03_REQUIREMENT_TRACEABILITY_MATRIX.md) · [Decisions](09_OPEN_QUESTIONS_AND_APPROVALS.md)

## Verified comparison

| Area | Existing mobile / Frame1 | Frame2 visual treatment | Enhancement proposal | Requirement boundary |
|---|---|---|---|---|
| Brand | Cream,teal,gold; rounded forms and symbolic illustrations. Frame1 Intro1 adds a family illustration and trust cards. | Image-led cinematic hero, restrained badges, stronger section framing. | Retain tokens and recognizable moon/lantern identity; improve image crop and hierarchy only. | Asset direction remains existing; no new religious imagery or verification claims. |
| Intro1 | Current mobile says Quran & Tajweed first; Frame1 says Welcome; PRD first pillar is Stories. | Stories of the Anbiya with a spotlight player-like card. | Preserve separate source copies in audit; approve topic/order/content resolution before execution. | No playable/unauthenticated content or invented claims; four screens exactly. |
| Home | Frame1 long content composition includes mission,resume,recommendation,quiz,habits,challenge,rewards,bedtime,fact. | More compact card composition with progress pairs and story hero. | Reduce redundant padding, improve section headings and card alignment while retaining required priority. | A2 FR1's ten-section order; Frame2 may omit sections and cannot replace the whole structure. |
| Forms | Current registration shows only privacy,terms,adult confirmation and two optional preferences. | Frame2 groups Guardian account information and consent in rich panels, some816-wide layouts. | Single-column mobile form with accurate required/optional consent groups. | PRD's three required/three optional grants; parent PIN4–6; never a desktop two-column transplant. |
| Quran/Dua | Learning maps, practice and Arabic/transliteration/translation/audio blocks. | Rich coach/progress surfaces and visual mode chips. | Clear content hierarchy, adequate Arabic line height, distinct listen/practice modes. | Never edit canonical text; mic requires parent consent and OS grant; offline fallback remains available. |
| Habits | Checklist,streak recovery,personal/family garden. | Larger summary cards,calm garden progression. | Improve tap status clarity and progress grouping. | No shaming; no sibling rankings; timestamps and Hijri dates are sourced,not decorative fixtures. |
| Results | Effort/strengths/next-step framing and conditional mistakes action. | More expressive mastered strengths styling. | Balanced actions, discrete mastery accent layered on same result structure. | A9 equal-weight actions; no child raw accuracy score, arbitrary XP or compulsory animation. |
| Rewards/Avatar | XP,Noor Points,badges and levels are separate; owned/locked inventory. | Rich hero/avatar staging and improved grid surfaces. | Reuse clear resource metaphors and visible unlock criteria; improve alignment. | No gacha,real-money purchase path or per-child comparison; exact server-ledger values only. |
| Parent reports | Child/date context and summary/drill-down layouts. | Dense cards and richer graphs. | Progressive disclosure with clearly labeled date ranges,stale/partial data and report status. | Do not fabricate analytics; C22 safety flags and C26 redacted history retain distinct scope. |
| Ramadan |20 mobile previews with child/parent separation; local family aggregate image includes individual bars. | Lantern path and family certificate treatments. | Retain calm seasonal motif, improve accessible path/list alternative and terms-first conversion. | Aggregate-only family reporting; server region/Hijri truth; no fasting comparison or persuasion before pricing disclosure. |

## Frame properties and limitations

The104 compact extracted references contain zero component instances and zero descendant reactions. Many screens are390 wide but much taller than mobile viewports;816-wide frames combine multiple panels. Their imported screen geometry is source evidence,not responsive behavior. Some screenshots render wider than their nominal frame due to overflowing elements. Enhance by separating viewport,content and safe-area layers,then verifying overflow; do not simply resize a long artboard and call it responsive.

Actual token bindings,asset provenance and constraints must be inspected at execution. The component system below is a proposal to organize approved dependencies; there is no evidence that every named component already exists in Figma.

## Content conflicts must remain visible

Prompt section4 contains exact current-site copy and separate Frame1 copy where mapped. That is a comparison ledger,not instructions to put both sets on one screen. The source hierarchy does not grant permission to discard required behavior or silently rewrite copy. Choose the exact approved ledger after reconciling the affected requirement. Frame2 copy is never silently promoted into product content.

Missing reference screens still receive a requirement-driven prompt with a blocking exact-copy notice. Missing destinations receive an explicit blocked specification. This preserves coverage without pretending the reference or policy already exists.

## Review evidence

For each future screen compare default and relevant alternate states against all source variants, check text character-for-character, and record the improved layout's exact frame IDs and screenshots. Reviewer should be able to distinguish source preservation,requirement-driven correction and optional visual improvement. No screen is approved just because it looks richer.
