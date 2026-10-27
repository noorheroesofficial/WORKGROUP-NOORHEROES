# Global navigation and prototype architecture

[Index](00_MASTER_INDEX.md) · [Screen owners/branches](02_SCREEN_INVENTORY_AND_ORDER.md) · [Control ledger](11_CURRENT_CONTROL_RECONCILIATION.md) · [Decisions](09_OPEN_QUESTIONS_AND_APPROVALS.md)

## Prototype and production boundary

The Figma reference layouts currently have no detected descendant reactions. Connections below are requirements/proposals to build after approval,not verified existing Figma wiring. The current site is a UI-only preview with session-resetting sample state,not a backend-connected app. Never use its sidebar Next arrow or111-entry catalogue as production navigation.

Navigate to,Back,Open/Close overlay,Change to,Scroll to and Open link are prototype actions. Variables and conditionals can simulate selected profiles,consent booleans,answers and offline scenarios; they do not enforce security,authenticate,charge,grant OS permissions or persist production records. Action availability and conditional logic depend on current Figma plan/editor capabilities; use separately named scenario starting points if advanced prototyping is unavailable. [Figma actions](https://help.figma.com/hc/en-us/articles/360040035874-Prototype-actions), [variables](https://help.figma.com/hc/en-us/articles/14506587589399-Use-variables-in-prototypes) and [conditionals](https://help.figma.com/hc/en-us/articles/15253220891799-Multiple-actions-and-conditionals).

## Routing context contract

Before connecting a transition specify actor(parent/child),selected child,authenticated session,verified parent gate and expiry,content ID/availability,invoking route,return destination and relevant current operation. A prototype may hold these as named fixture variables; production evaluates authoritative state. Never embed real PINs,OTP,child PII or access tokens in Figma variable examples.

| Entry | Preconditions / branch | Destination | Back/exit |
|---|---|---|---|
| Cold start → Splash | Unsupported version | Forced Update | Store handoff only; no back into app |
| Splash | Maintenance active | Maintenance | Retry bootstrap or exit |
| Splash | No network | Pre-auth no-connectivity / cache-permitted route | Retry; bundled intros remain available; auth still requires network |
| Splash | Unauthenticated first run | Language → four intros → Login/Registration | Intro back previous; Skip from slide1 goes auth,never content |
| Splash | Valid session,no children | Add Child | Resume draft; no child content before saved profile |
| Splash | Valid session,children | Profile Picker | Do not redo intro/login |
| Auth expired while interrupted | Refresh unavailable | Login → OTP → authoritative pending step | Restore completed onboarding step/draft without new child duplicates |
| Registration | Valid identifier + required Terms/Privacy/child-processing consents | OTP | Required full text must load; optional grants independent OFF |
| Google login | Verified new/returning family | Same downstream onboarding / picker | New family's required consent cannot be bypassed |
| OTP | Verified new family | PIN setup,or unresolved post-verify consent step | A1 FR10 conflicts with narrative/pre-captured consent; decision G-03 |
| PIN set+confirmed | Optional eligible biometric | OS enrollment simulation → Add Child | Skip/cancel retains PIN fallback |
| Add Child | Valid DOB/avatar/language/level,capacity permits,online | Add Another → family summary → primer → picker | Selection substeps return with draft; optional repeat loop; idempotent save |
| Child tile | Lock configured | Child lock → restriction check | Recovery routes parent gate; no self-reset |
| Child tile | No lock | Restriction check → Home | Cached signed policy only where permitted; cannot bypass limits offline |
| Parent tile / parent-only action | Parent not verified or verification expired | Parent Gate → pending parent destination | Cancel returns caller; child context remains private |
| Gate success | Screen-time exhausted | Calm Rest | Parent-only override route if policy permits; no child unlock loop |
| Gate success / new activity | Bedtime blocks activity | Bedtime Block | Allowed calm content route per policy; active-player graceful boundary differs from new launch |

## Authenticated child shell

Preserve existing Home,Learn,Stories,Rewards,Profile bottom navigation. Feature eligibility and content restrictions apply before a route opens. Search/bell enter contextual search/notification route. Onboarding,legal,gates,parent mode and immersive player surfaces do not automatically inherit bottom nav. Child profile switch goes through approved parent authorization and lock/restriction checks. Clear old-child UI before rendering new context.

| Journey | Forward route / branch | Return semantics |
|---|---|---|
| Home mission | Assigned content of approved type → its detail/player/practice | Home section refreshed after completion; no invented eleventh Games rail |
| Continue Learning/Watching | Stored valid content/resume point | Same source rail context and scroll; withdrawn/unavailable → safe fallback |
| Stories | Library/filter → Detail → Video/Audio/Text player → optional choice/pause quiz → approved ending | Back exits to caller; confirmation only if source specifies lost-progress consequence; persist resume |
| Story completion | Normal completion → effort/reward/moral/post-story quiz; bedtime boundary → calm ending | Child result actions preserve story return context; no forced replay or pressure loop |
| Audio bedtime | Player → timer/speed/episode overlays → calm reflection/goodnight | Dismiss sheet returns player; stop/sleep/navigation ends simulation; no loud reward burst |
| Learn | Map → placement/mode selection → Surah/Arabic/Tajweed/Quran exercise | Unlock eligibility server-sourced; contextual form and harakah exercises included even though inventory omitted them |
| Recitation | Consent + OS grant → recorder → processing → feedback | Denied/offline AI unavailable → listen-only/self-assessment; exit stops recording |
| Duas | Category → list → detail → recall question → result | Exact Arabic/transliteration/translation; favorites/download shared owner keeps Dua filter and return route |
| Habits | Checklist → dhikr/fasting/good deed/history/recovery/garden | Check-in updates visible status; offline outbox pending distinct from confirmed rewards |
| Quiz | Question type → submit → explanation → next → retry set if required → completion/result | Wrong answers do not imply incomplete journey; Review Mistakes absent if none; Retry and Continue preserve context |
| Games | Hub → configured mechanics screen → session wrapper | Wrapper returns stored caller (hub,mission,Learn); abandonment does not invent full-completion rewards |
| Rewards | Wallet → ledger detail / badges / levels / challenge / store / family goal | Resource metaphors separate; store only points; child share routes parent gate before external OS action |
| Avatar | Preview → owned equip/locked criteria/evolution | Equip returns current preview; visible unlock criteria; rollback/pending sync distinct |
| Search | Query/recent/suggestion or permitted voice → Results → content detail | Back restores query/filter; clarification/empty never connects to arbitrary content |
| Favorites/Downloads | Profile shared shell → typed saved items/download states | Preserve active tab/filter; unavailable item gives allowed explanation,not broken destination |
| Notifications/deep link | Resolve auth/profile/availability/policy → intended content | Resolve profile mismatch before content; failed/withdrawn links use defined fallback; no raw URL in child copy |
| Facts | Home fact/Browse → Fact Detail → verified fact-linked quiz | A8 owns question/result; Browse exists in preview but needs PRD-scope decision |

## Parent shell and privacy

| Entry | Destination behavior | Cancel/back/exit |
|---|---|---|
| Verified parent gate | Dashboard with selected child/date context | Exit parent mode clears verification and returns authorized child/picker route |
| Dashboard child chips | Change selected report context,not logged-in child session | Retain date filters; zero children exposes Add Child |
| Dashboard activity See All | Full Activity Timeline missing independent C22 specification | Block wiring until G-07; never route to unrelated safety history |
| Child Management | Add Child / Edit Child / disable / reenable / irreversible deletion / reorder variant | DOB edit locked; irreversible child deletion requires cited step-up and warning; request outcomes simulated |
| Reports | Per-child → skill/safety/AI insight or scoped history; monthly family aggregate | Preserve child/date range; distinguish C22 safety history from C26 redacted interaction detail |
| Controls | Screen time,quiet hours,AI permissions,content level,locks/sessions | Saves confirm authoritative outcome; failure restores prior value; prompt OS permission only where required |
| Subscription | Plan → trial/direct-upgrade disclosure → platform checkout handoff → management | Cancellation equal-access; no charges in prototype; price/renewal obtained from authoritative store/product data |
| Parent notifications | Inbox → report/ticket or validated deep link; preferences → categories/quiet hours | Safety notifications cannot be disabled if PRD forbids; no misrouting child vs parent preferences |
| Support | Center → FAQ search/article or contact form → submitted → history/detail | Rejected attachment/text validation preserves draft; safety/account-cancellation categories retained |
| Settings/Privacy | Consent log/detail/withdrawal,history/detail,language,devices,export | Optional withdrawal needs clear consequence; full legal text unchanged; parent history redacted per scope |
| Data export | Request → preparing/ready/failed/expired status → authenticated delivery handoff | Never a child route or real data export in prototype |
| Logout | Unsynced-work confirmation if relevant → signed-out login | Cancel retains session; confirmation cancels active UI/media and clears private context |
| Family deletion | Request/confirmation/status/cancellation surfaces documented as missing policy | Cross-reference to C21 is broken; destructive outcome/cancellation window remain blocked |

## Ramadan branch — seasonal,not a replacement app

Current site review order: Prep → Home → Journey → Night Recap → Mission → Story → Fasting → Qadr → Eid Countdown → Eid Home → Reward Reveal → Card Generator → Certificate → Keep Habit → Parent Settings → Parent Dashboard → Family Aggregate → Family Report → Conversion → Invite. This catalogue order is a review sequence; normal child traversal is Home/Journey → eligible tonight Mission → linked activity → Recap → Journey. Completed nights may show recap; future gates remain unavailable. Qadr is conditional for configured reflection nights; no fixed assertion of the actual night or live religious date.

Parent settings/dashboard/aggregate/report/conversion/invite always pass the parent gate. Family aggregate never compares siblings. Fasting practice is parent-configured and child non-shaming; no hidden compulsory target. Eid/certificates/cards retain approved templates and parent-gated sharing. Conversion is parent-only and terms-first; no child purchase CTA. After Eid,keep-habit offer returns the normal habit journey and archived content remains available only as specified. Backend regional configuration/approved calendar override determines eligibility,not prototype clock.

## Overlays,history and restoration

Open an overlay from its actual caller; Close overlay returns caller focus and state. Outside-tap dismissal is allowed only for non-destructive,nonmandatory overlays where the source permits it. A legal read overlay does not alter a checkbox; a timer sheet does not stop playback just because it closes. Nested overlays have an explicit close path. Figma Swap overlay does not add history; use it only when that behavior matches the intended flow. [Prototype action semantics](https://help.figma.com/hc/en-us/articles/360040035874-Prototype-actions).

Android system Back and iOS in-app Back return the same logical route,with OS differences represented as annotations. Edge-back gestures need a visible equivalent; do not invent platform-only features. Long-list scroll/filter state survives detail-return where requirements expect it. Interrupted form/quiz/player restores the last authoritative completed state; stale network/AI response cannot attach to another child's screen. Session expiry invokes authentication before sensitive action and restores a permissible draft afterward. No new content unlock is derived locally until the explicit A3 offline-unlock conflict is resolved.

## Prototype starting points and end-to-end review paths

All scenarios below are planned acceptance tests; **not executed against enhanced Figma screens yet**.

| Scenario | Path / interruption | Expected result |
|---|---|---|
| Fresh parent happy path | Language →4 intros → registration grants → OTP → PIN → Add Child → picker → Home | No content before login; correct fields and child context |
| Skip intro1 | Skip → auth | No paywall/content bypass |
| Required consent missing | Submit or Google path | Disabled/blocked until required grants are valid |
| Legal text load fails | Open required document | Retry/cached approved version; no acceptance without readable text |
| Incorrect/expired OTP | Wrong code then expiry | Inline correction; countdown server-simulated; cooldown after configured attempts |
| OTP channel failure | Delivery fail → alternate | Valid fallback only; no account enumeration |
| PIN mismatch/no hardware | Confirm mismatch → correct; biometric absent | Only confirm clears; optional hardware control hidden |
| Child DOB invalid/capacity | Out-of-range/second-child cap | Field reason or gated capacity route; no raw age entry |
| App killed after OTP/save | Resume starting point | Completed step/draft restored; no duplicate child |
| Returning valid/expired | Cold start two fixtures | Picker direct vs OTP then pending permitted destination |
| Parent/child gate failures | Incorrect+cooldown+biometric fallback | No protected UI; recovery is verified parent path |
| Restriction offline | Cached signed limit reached | Calm Rest; no offline bypass |
| Story withdrawn mid-play | Unavailable event fixture | Safe stop and correct caller return |
| Story crosses bedtime | Complete after policy boundary | Approved calm ending; no loud reward or forced quiz |
| Mic denied/no AI/offline | Surah recorder unavailable | Listen/self-assessment fallback,not hard learning block |
| Each quiz type | MCQ/order/true-false/image/audio | Correct input/accessibility; explanation and next |
| Mistakes/all-correct/deferred | Result three fixtures | Conditional review; equal actions; offline no invented scores/rewards |
| Favorites unavailable/sync fail | Heart toggle/error/deleted item | Consistent state and specified rollback/availability behavior |
| Downloads full/expired | Cap/storage/expiry | Distinct safe action; no duplicate downloads |
| Profile switch interrupted | Pending response for old child | No old-child content leaks into selected child |
| Deep link signed out/wrong child | Link → auth/picker/gate | Intended permitted destination or explicit fallback |
| Parent save offline/error | Control/settings submit | Prior value or pending state correct; no false saved claim |
| Billing canceled/payment failed | Store handoff scenarios | No prototype charge; truthful status; cancellation access |
| Safety support / export / withdrawal | Parent routes with failure | Draft preserved,proper scope,no child exposure |
| Ramadan tonight/future/Qadr | Lantern choices | Eligibility respected; list alternative; no presumed live Hijri date |
| Aggregate/conversion/share | Parent-gated seasonal routes | No sibling bars; terms first; OS share simulation after gate |
| Reduced motion/200%/RTL | Repeat core paths | Same outcomes with visible feedback,accessible wrapping and direction |

An unmatched captured control or missing policy blocks the relevant path's design sign-off. Record that block in the control/decision register rather than fabricating a destination.
