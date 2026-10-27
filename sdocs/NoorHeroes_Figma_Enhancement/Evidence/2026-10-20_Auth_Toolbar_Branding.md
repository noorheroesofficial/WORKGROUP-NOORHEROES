# Login and Registration toolbar branding

User confirmed using exact linked asset1345:1449after it was identified as the full monochrome-light wordmark, rather than the NH crescent-and-lantern monogram.

Login1355:2696and Registration1459:256now display cloned approved wordmark instances1474:389and1474:394at the right end of their350×44toolbars, with20pxscreen-edge padding and vertical centering. Artwork120×23.3668maintains1592:310source proportions and exact source tint/assets; no background paint/card/container was added behind it. Source1345:1449was unchanged.

Removed the centered symbol+wordmark from both screens. Existing122pxtransparent layout reservations remain so form geometry does not shift. Splash branding was not edited. Old Login branding nodes1355:2702/2700and Registration1459:414/416are removed; future work must use approved library sources or new toolbar instances rather than those obsolete IDs.

343Login and253Registration non-brand node snapshots retained their absolute bounds, text and prototype reactions. Both Back buttons retained exact geometry/actions. Screenshots of both final screens visually reviewed. Temporary toolbar-only geometry checks at320/360/390/420pxpassed20pxright padding, shared vertical center22pxand ample separation from44pxBack controls; temporary nodes removed. This is layout verification, not device/runtime testing.

## Change ledger

```json
+{"createdNodeIds":["1474:389","I1474:389;1304:207","I1474:389;1304:207;1300:58","I1474:389;1304:207;1300:59","I1474:389;1304:210","1474:394","I1474:394;1304:207","I1474:394;1304:207;1300:58","I1474:394;1304:207;1300:59","I1474:394;1304:210"],"mutatedNodeIds":["1383:3078","1355:2697","1459:413","1459:407"],"removedNodeIds":["1355:2702","1355:2703","1355:2700","I1355:2700;1304:207","I1355:2700;1304:207;1300:58","I1355:2700;1304:207;1300:59","I1355:2700;1304:210","1459:414","1459:415","1459:416","I1459:416;1304:207","I1459:416;1304:207;1300:58","I1459:416;1304:207;1300:59","I1459:416;1304:210"],"results":[{"root":"1355:2696","wordmark":"1474:389","source":"1345:1449","toolbar":{"x":20,"y":18,"w":350,"h":44},"wordmarkBounds":{"x":230,"y":10.316582679748535,"w":120,"h":23.36683464050293},"rightInset":20,"backgroundPaints":0,"formsAndActionsPreserved":true,"checkedNodes":343},{"root":"1459:256","wordmark":"1474:394","source":"1345:1449","toolbar":{"x":20,"y":18,"w":350,"h":44},"wordmarkBounds":{"x":230,"y":10.316582679748535,"w":120,"h":23.36683464050293},"rightInset":20,"backgroundPaints":0,"formsAndActionsPreserved":true,"checkedNodes":253}]}
```

## Width checks

```json
+{"createdNodeIds":["1474:399","1474:400","1474:401","1474:402","1474:403"],"removedNodeIds":["1474:399","1474:400","1474:401","1474:402","1474:403"],"responsiveGeometryChecks":[{"screenWidth":320,"rightPadding":20,"verticalCenter":22,"backToWordmarkGap":116},{"screenWidth":360,"rightPadding":20,"verticalCenter":22,"backToWordmarkGap":156},{"screenWidth":390,"rightPadding":20,"verticalCenter":22,"backToWordmarkGap":186},{"screenWidth":420,"rightPadding":20,"verticalCenter":22,"backToWordmarkGap":216}]}
```
