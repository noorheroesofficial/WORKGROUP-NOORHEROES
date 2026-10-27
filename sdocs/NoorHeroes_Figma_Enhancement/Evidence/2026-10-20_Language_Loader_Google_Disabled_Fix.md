# Language loader and Google processing fix

## Root cause and repair

Language processing1259:140 contained legacy WIDTH350→180 and TRANSLATION_X0→85 tracks on host1259:141. Those tracks conflicted with the newly nested350px shared loader and clipped its dots. Removed both tracks, retaining350×64 host bounds. Shared loader1428:7739 now matches working Login's Start327:7→Quarter327:9→Half327:11→ThreeQuarter327:13→Quarter cycle. Reparented static reduced-motion fallback1428:7745 from the page into1259:141 at0,0. Existing1.95second completion to first Intro1215:34 is preserved.

Google click1355:2734 and Google Retry branch on I1428:220;1420:20 now keep Idle=true while Can submit=false, Cannot submit=true and Processing=true. Thus Send code stays visible disabled while Google loader is shown. OTP submission still hides idle Send code and replaces it with its own loader. Cancellation/completion/error restoration is unchanged.

16 targeted geometry/graph/state checks passed. Repaired button resting render inspected. Live Present playback remains unverified; do not describe graph tests or static screenshots as runtime animation evidence.

Previous integration audit's Google pending expectation (!Idle) is superseded by this task's explicit visible-disabled requirement.

## Saved audit

```json
+{"status":"PASS","count":16,"checks":["No legacy width/translation tracks","Full-width stable loading container","Static fallback correctly nested","Matches working Login Start variant","Reduced motion Still variant","All dots inside unclipped bounds","Loop 327:7 to 327:9","Loop 327:9 to 327:11","Loop 327:11 to 327:13","Loop 327:13 to 327:9","Language completes into first Intro","Google opens correct loader","Send code remains visible disabled during Google","Google duplicate click blocked","Google Retry retains disabled Send code","OTP still replaces Send code with loader"],"limits":"Saved graph and geometry validated; live Present playback unverified"}
```
