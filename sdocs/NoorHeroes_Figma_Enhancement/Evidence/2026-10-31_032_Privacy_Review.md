# Screen 032 — Privacy Policy full-document reader

Ready for review. Screen031 approved; stop before033 until user approval.

## Source and scope

Figma-only extension of the approved031 reader, using the existing Privacy draft verbatim: source sheet1513:386, document1513:401, text1513:402–415. The seven sections cover collection; purpose/use; separate optional processing; safeguards; access/correction/deletion; fictional Ayaan sample; acknowledgement. No legal clauses, dates, jurisdiction, company contacts or production-control claims added.

Retains the approved reader label: “Prototype draft · Version unapproved · Legal review required”. This is a source-grounded prototype draft, not a verified complete production policy. No approved legal version or production shared content registry is available. Blueprint/PRD require shared versioned content; copy parity is verified in this design snapshot, not a runtime content architecture.

## Nodes and reusable design

- Existing V2:1128:2; new032 section2432:15286 at y30226.
- Default2432:15287; cached-draft fixture2432:15347.
- Loading2432:15407; unavailable2432:15457.
- Reduced2432:15507; reduced loading2432:15567.
- Review-only invocation2432:15617.

Approved031 geometry/components reused:390×844 screen,366×738 cream card,338×592 inner scroll viewport, fixed draft-status footer, Poppins16/26 body, NH heading/caption styles, approved toolbar wordmark/Back assets, NH quiet/primary/loading buttons, existing palette bindings. Long document is1742px high. Static decorative stars stay behind content; no new animation pattern.

## Behavior

Review-only controls open the full-screen reader overlay. Back closes that reader only. Unavailable Retry closes before opening local Loading;1.2-second loading fixture closes before opening the local draft reader. Reduced loading retains Still spinner phase and instant transitions. All cloned action destinations were remapped into032; no links to031 state fixtures remain.

Existing Terms→Privacy agreement sheets and registration unchanged. Reading writes no consent state. Registration/Settings integration remains pending under the approved031 convention; no missing Settings screen is invented. A cached-draft fixture does not claim production legal-version validity, live cache behavior or offline eligibility.

## Verification

116/116 saved-action/layout/contrast checks passed. Includes14 exact source text blocks across default/cached/reduced readers, body wrapping/size, final-section bounds, inner-only scrolling, fixed label clearance,44px Back targets,48px actions, local overlay swaps, no consent writes/external URLs, correct title and reduced Still phase. Actual contrast:body13.60:1,version notice4.52:1.

Source snapshots before/after confirmed Terms1513:350, Privacy1513:386, Registration1459:256 and the entire approved031 section2428:14707 unchanged. Default, unavailable and review-entry screenshots inspected. Adjacent _Checks.json and _Ledger.json record saved evidence.

Live Present remains unverified: browser acquisition was denied by saved Figma permission during031 in this same session, so the blocked action was not repeated or bypassed. Real fetching, caching/version validation, device accessibility/RTL/text scaling and runtime overlay/scroll playback are unverified. Only authorized390×844 standard size designed. No code, original/reference or033 changes.
