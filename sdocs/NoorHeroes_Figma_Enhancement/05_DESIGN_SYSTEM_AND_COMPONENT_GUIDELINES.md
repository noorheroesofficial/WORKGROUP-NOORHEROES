# Design system and reusable component specification

[Index](00_MASTER_INDEX.md) · [Motion](07_MOTION_AND_ANIMATION_GUIDELINES.md) · [Accessibility](08_ACCESSIBILITY_RESPONSIVENESS_AND_EDGE_CASES.md)

## Status and preservation

The values below are sourced from A1 §2.1 and the current mobile site's visible design system. They are specifications to reuse or reconcile,not newly created Figma variables. Frame-specific fonts may differ; preserve original assets until the font decision is approved. Never globally mutate the source library while executing one screen.

## Token ledger

| Semantic token | Light | Dark | Usage / restriction |
|---|---|---|---|
| Text/primary | `#1C2B33` | `#F4F1E8` | Body and main labels |
| Brand/primary | `#0E7C7B` | `#3FB6B4` | CTA/control emphasis; test actual foreground |
| Brand/accent | `#D4A24C` | `#E8C27A` | Progress,decorative accent; insufficient contrast for small white text in many pairings |
| Background | `#FAF7F0` | `#10181C` | Main surfaces |
| Surface | `#FFFFFF` | `#16232A` | Cards/forms |
| Border | `#E5E0D5` | `#28363D` | Separation; essential control bounds need3:1 contrast or alternate indicator |
| Text/muted | `#6B7280` | `#9AA5AA` | Secondary copy; verify pair |
| Status/success | `#2E8B57` | `#4CAF7D` | With text/icon |
| Status/error | `#C0392B` | `#E0594B` | Inline errors with explicit message |
| Status/info | `#2E86C1` | `#5AA9D6` | Information with icon/text |
| Surface/parchment | `#FDF6E3` | Unspecified | Existing site token; dark equivalent needs approval |

Spacing uses4-unit base:4,8,12,16,24,32,48,64. Mobile horizontal content padding20; internal padding12–16; grid4 columns with8 gutters at360–420. Source Home section cards use12 radius and light shadow `0 2px 8px rgba(0,0,0,0.06)`. Do not silently standardize all reference cards to one radius; component-level12/16/24 radius proposals require approval against the reference. No shadow communicates status alone.

| Text role | Size | Weight | Guidelines |
|---|---|---|---|
| Brand/hero display |28/32 |600–700 | Serif for hero/brand only |
| H1 |24 |600 | Screen title |
| H2 |20 |600 | Section titles |
| H3 |18 |600 | Card hierarchy |
| Body large |16 |400–500 | Legal/instructions/long educational copy where appropriate |
| Body |14 |400 | General text |
| Caption |12 |400–500 | Secondary metadata |
| Micro |11 |400 | Nonessential metadata only; no required safety/legal action |

Latin UI: current site Poppins; PRD permits a rounded humanist style. Display: Playfair Display for brand moments. Arabic sacred content: verified Naskh asset such as Noto Naskh Arabic; Arabic interface font is separately resolved per A1. Do not substitute a font without checking diacritics,line height,shaping and glyph coverage. No generated Arabic or religious text in assets. Line heights must fit real text at200% and long translations; exact values should be checked with the selected font rather than guessed.

## Component contracts — proposed reusable organization

| Component | Inputs/content slots | Relevant variants | Interaction and accessibility |
|---|---|---|---|
| AppHeader | Title,optional back,approved context,optional search/bell | Child,parent,bedtime | Back uses caller history; icon labels; safe top inset |
| PrimaryButton | Exact label,leading icon,status reason | Default,pressed,disabled,busy |44 minimum; busy prevents duplicate action; disabled reason readable |
| TextField | Label,value,placeholder,helper,error | Empty,filled,focused,error,disabled | Persistent label; error announced; correct keyboard; draft preserved |
| ConsentRow | Exact grant text,required flag,version link,boolean | Unchecked,checked,unavailable | Independent focus,required/optional words; read link never toggles grant |
| OTPGroup |6 cells,masked recipient,server timer | Partial,verifying,error,cooldown | Paste+auto-submit; LTR digits in RTL; timer announcements throttled |
| PINGate | Parent/child context,configured input,attempt status | Input,lockout,biometric fallback | Parent PIN4–6; no plaintext evidence; recovery is verified parent route |
| ContentCard | Verified ID,title,type,art,status,progress | Available,downloaded,locked,withdrawn | Whole card detail; heart/download separate controls; no unavailable title exposure if policy hides it |
| FavoriteToggle | Content ID,state | Off,on,pending sync | Same heart metaphor; meaningful label and pressed state; optimistic rollback only as specified |
| ProgressMetric | Value,maximum,label,data freshness | Cached,current,partial | Never color-only; no fabricated statistics or percent in child accuracy results |
| QuizAnswer | Verified answer ID,text/image/audio | Unselected,selected,submitted,feedback | Choice IDs stable; ordering accessible buttons in addition to drag |
| ResultSummary | Strengths,next step,effort,optional mastery,mistake availability | Practice,all correct,mastery,offline deferred | Review mistakes conditional; retry/continue equally weighted; no raw child accuracy |
| DownloadRow | Content,size,status,expiry | Queued,downloading,paused,ready,expired | Accessible progress; cap/storage/network distinction; retry/cancel per policy |
| AvatarItem | Asset ID,ownership,criteria,equipped state | Owned,equipped,locked | Visible criteria; non-gesture rotation controls; no opaque mystery silhouette |
| HabitRow | Verified habit,label,check-in,sync state | Due,completed,pending,missed | Warm recovery; no shame or child comparisons |
| ReportCard | Child,date range,source status,verified metrics | Loading,ready,partial,delayed,no data | Numeric accuracy parent-only where required; charts have text summary |
| BottomSheet/Dialog | Title,body,approved actions,return focus | Open,closed,scrollable,destructive review | Cancel reliable; no offscreen CTA; destructive action visually clear,not pressure-framed |
| Notice | Exact message,reason,optional retry | Offline,error,maintenance,unavailable | Text+icon; retry correct service; no generic all-screen error default |
| RamadanLantern | Night ID,eligible/completed,current,special state | Ahead,tonight,complete,reflection | Ordered textual night list alternative; no color-only eligibility |

Do not combine badge,achievement level,XP and spendable Noor Points into one metric. Family displays remain aggregate-only. Source mockup switchers (Default/Loading/Offline),FR numbers and review chrome are documentation candidates,not presumed product components.

## Layout and naming

Future approved component naming: `NH/<Domain>/<Component>`; variants use `State`,`Mode`,`Role`,`Size` only where applicable. Screen names: `NH/Enhanced/<number>/<screen>/<state>`. Existing sources keep names and IDs. Component properties carry exact text/asset slots; no hidden educational or legal copy in opaque raster images.

Use auto layout for related sections; text hugs height within available width. Long lists scroll vertically; horizontal rails only where the PRD/reference defines them. Footer content clearance equals actual footer height plus safe bottom inset. Native bottom nav remains visible only inside child authenticated shell; onboarding/legal/gates do not inherit it automatically.

## Approval and migration

Approve the working-area page/section,canonical font choice,token aliases and component recipes before reusable definitions are created. A screen prompt may instantiate approved local dependencies; it may not change every source frame by updating a shared component. Record changed IDs and affected instances if a later global migration is explicitly authorized.

## Finalized V2 visual override

For all future screen execution, [12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md](12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) is the approved visual source of truth. Its exact current tokens, shared text styles, component sizes and consistency checks supersede conflicting historical visual proposals in this guide. Functional PRD requirements and verified copy are preserved.
