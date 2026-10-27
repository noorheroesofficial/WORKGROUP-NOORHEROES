# Open questions,conflicts and approval register

[Index](00_MASTER_INDEX.md) · [Audited feature findings](Research/child-learning.md) · [Parent findings](Research/parent.md) · [Supporting findings](Research/supporting.md)

**No decisions below are approved by their inclusion in this document.** This is a review register. Preserve the original sources. Approved resolutions must identify affected prompt numbers,the chosen source version,exact copy/behavior and permitted change. Visual enhancements do not authorize functional or religious-content changes.

## Global decisions

| ID | Exact conflict / gap | Affected surfaces / impact | Recommendation for approval | Execution gate |
|---|---|---|---|---|
| G-01 | A1 FR4/§1.18 requires Stories,Quran/Arabic/Tajweed,Habits/Rewards,Parent Control; current site's four intros are Quran,Stories,Safe & Trusted,Personalized Path; Frame1 first is Welcome and Frame2 first Stories. | Intro1–4 and auth entry; topic/sequence/content mismatch. | Retain four screens; approve requirement-aligned topics with an exact approved copy ledger. Do not simply swap headings between frames. | Intro content/order blocked. |
| G-02 | A1 §2.4 says language persists on tap,no separate confirm; site/screenshot has Continue and eight locales; mobile sources differ about Hindi/French and other locales. | First-run and profile/settings language; unsupported localization/glyph coverage risk. | Confirm mobile locale roster/autonyms and whether Continue is retained with explicit requirement exception; keep complete verified translations. | Language behavior/roster blocked. |
| G-03 | A1 FR5 requires Terms/Privacy/child-processing grants plus independent optional personalization/voice/marketing. Site shows Terms/Privacy/adult confirmation and generic optional preferences. FR10 places Consent after verification while narrative/API says pre-captured consent→PIN. | Registration,Google,OTP,legal docs; child-data timing and skipped grant risk. | Approve exact legal versions/strings and one consent capture sequence; retain all required grants before child data and identical new-user Google route. Adult confirmation cannot replace processing consent. | Auth consent/policy/copy blocked. |
| G-04 | A1 FR11 says parent chooses4–6 digits; site PIN Setup says6; local Setup says4–6; Frame2 parent gate says4. | PIN setup/reset/gate; input length and routing mismatch. | Use4–6 per requirement subject to approval of existing-design correction. Reset is separate verified flow returning Security,not Add Child. | PIN wording/mechanics blocked. |
| G-05 | Current mobile/profile/Figma/Screens contain translations,Arabic,scholar/institution claims,demonstration child names,progress and prices without authoritative provenance. | All educational/trust/report/billing surfaces. | Preserve audit strings; obtain canonical content IDs/version and scholar/legal provenance. Use existing fixtures only as marked review data. Never invent or mix translations. | Copy/claims blocked where provenance missing. |
| G-06 | Frame2 includes816-wide combined panels and very tall390-wide imports; source hierarchy does not identify a canonical approved variation among Modern/Refined alternatives. | Responsive layout,component structure and motion. | Approve per-screen visual source and enhanced working area. Borrow patterns without importing combined layout or losing mandatory sections. | Global design dependency approval. |
| G-07 | C20 Activity Timeline Preview points to missing Full Activity Timeline in C22. C25/C26 family deletion points to C21 FR8/step7 although C21 FR8 is capacity and C21 defines child deletion,not a complete family-deletion policy. | Timeline,account deletion/request/status/cancellation; broken destinations and undefined irreversible/cancellation behavior. | Keep explicit blocked surfaces in inventory; supply authoritative timeline/family-deletion policy and approved legal copy before wiring. | Those destinations blocked. |
| G-08 | Source controls include Default/Loading/Offline,FR annotations,preview credentials and unconnected demo state. | Gates,reports,games,Ramadan; implementation-looking controls could accidentally become product controls. | Retain as audit evidence; approve removal from enhanced product UI and move scenario controls outside product frames. Demo PIN strings must not be production copy. | Demo-versus-product classification. |
| G-09 | Existing designs disagree on child age range; site intro3–15,README3–12,A1 blocks below3/above17 by default while visual density lists wider bands. | DOB validation,avatar filtering,age/content labels. | Confirm mobile eligible ages and bands from authoritative feature policy; do not silently use marketing/example age claims. | Age-dependent copy/validation blocked. |
| G-10 | Proposed independent Security landing,Facts Browse and optional Path Reveal/primer detail lack fully approved exact source identities/copy; runtime APIs were not called. | Additional surfaces,system handoffs and optional navigation. | Review whether independent surfaces are needed or existing-section variants; verify actual router/OpenAPI before any client implementation. The package defines no live integration fields. | Conditional proposals/copy gaps blocked. |

## Feature-specific conflict ledger

The full source-specific findings and recommendations are retained verbatim in:

- [Child-learning CL-01–CL-12](Research/child-learning.md): daily mission3 vs4,reward accuracy/effort ambiguity,equal result action weight,misnumbered shared features,Home Games entry,first mission copy,Dua badge dismissal,offline episode unlocks,Arabic mechanics and bedtime boundary.
- [Parent audit](Research/parent.md): free-tier capacity,age versus immutable DOB,deletion confirmation friction,missing safety/account-cancellation support categories,C22/C26 history scope,broken account-deletion reference and missing full activity timeline.
- [Supporting/seasonal audit](Research/supporting.md): locale roster,offline profile behavior,Search count mismatch,fact-linked question count,profile switch authorization,Ramadan aggregate-only versus individual bars,fasting role split,terms-first conversion and religious verification.

| Concrete source difference | Impact | Resolution recommendation |
|---|---|---|
| A2 FR4/A11 FR10 daily missions3; Rewards Wallet-01 says3 of4 done | Incorrect child task/reward count | Requirement-driven3-mission fixture/layout only after approval; original screenshot remains unchanged. |
| C24 FR1 Free permits1 active child; Plan Comparison-01 saysup to2 and limited AI questions5/day | Wrong entitlement and upsell trigger | Approve correcting enhanced plan content to authoritative live product/PRD data; no live price fabricated. |
| Add_Edit Child-01 uses Age/Enter age; A1/C21 require DOB-derived age and immutable edit DOB | Missing required field/business rule | Separate Add and Edit prompts; Add usesDOB,Edit shows locked DOB/support correction route. |
| Child deletion screenshot typed AISHA/only warning; C21 sober,equal cancel/delete,no artificial delay | Added friction/dark-pattern tone | Confirm whether typed-name is required policy; do not invent second gate or preserve coercive wording uncritically. |
| Frame1 Dua Card and site differ: translation “after causing us to die” versus “after having taken it from us”; transliteration aḥyānā/ahyānā and ba'da/baʿda; learned/button states differ | Sacred-content/source-state mismatch | Select one coherent canonically verified text version and its intended learned state; never blend or paraphrase. |
| Source Parent Gate contains “Preview gate only · PIN5678” | Demo credential and security claim could enter production copy | Keep audit-only; remove from enhanced app after G-08 decision; recover parent PIN through A1 OTP,not a dead-end support hint. |
| Family Aggregate PNG warns aggregate-only but includes Sara/Yusuf bars; F36/KMP excludes per-child arrays | Sibling comparison/privacy conflict | Approve cooperative aggregate treatment; no per-child ranking or fasting bars. |
| Fasting preview includes approach selector on child screen | Parent/child boundary ambiguity | Keep configuration parent-gated; child logs only permitted activity with non-shaming copy. |
| Ramadan conversion persuasion precedes terms; F36 FR13 says terms-first | Billing disclosure order mismatch | Approve terms/price/renewal/cancel before any benefit persuasion; parent-only checkout handoff. |
| Game/quiz/photo placeholders contain unverified educational strings or scholar claims | Factual/religious fidelity risk | Resolve actual content/version and asset provenance; do not fill gaps with new examples. |

## Per-screen approval record

For each prompt record: source versions checked;exact content selected;functional conflict decisions;visual reference selected;working area;required components;platform/safe-area behavior;motion approval;state coverage;unmatched controls resolved;review screenshots and created IDs. Decision status is **Open / Approved with exact resolution / Rejected / Deferred**. An approval applies to the identified screen and dependencies,not to unrelated frames or the next prompt.

## Proposed review order

1. Source scope and G-01–G-10; religious/legal/locale/age/entitlement conflicts first.
2. Shared tokens/components/working area and navigation/motion specification.
3. Approve Splash prompt and its references; execute only after separate authorization.
4. Review each next independent screen/state within its group; corrections and user approval before advancement.
5. Validate end-to-end branches after constituent screens are approved.

The current task stops at documentation handover. No Figma write authorization is inferred from this package.

## CL-13 — Dua text and learned state conflict

The hosted Dua translation contains “after having taken it from us”; Frame 1 contains “after causing us to die”. Transliteration glyphs also differ (ahyānā/aḥyānā and baʿda/ba'da), and learned-state indicators differ. These are conflicting source strings, not editorial alternatives. Approve one verified content-registry version with religious review provenance and define the learned-state source. Block Dua text replacement and learned-state wiring until resolved; preserve both sources in the prompt audit.
