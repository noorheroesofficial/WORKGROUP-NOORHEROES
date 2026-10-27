# Language button revision — 2026-10-13

Current revision supersedes earlier full-screen Loading/Success evidence.

- Four language selection screens preserved: 1166:215, 1166:250, 1166:285, 1166:320.
- Local interactive component: 1194:62. Fixed 350 x 64 footprint; compact inner button 180 x 64 centered; Continue 19 px, unchanged font and teal.
- Click: 320 ms morph to compact loading. Six matched dot phases give two continuous pulse cycles; 10 ms waits and 320 ms Smart Animate transitions. Restore uses 420 ms Smart Animate, then Idle is clickable again.
- No visible success state, message or checkmark. Existing hidden source layers remain because Figma rejected deleting those component descendants; they are invisible and disconnected.
- Error demonstration: keyboard E during processing returns to the original button for retry.
- Language cards fade in and rise 12 px, with 70 ms stagger and 320 ms easing.
- V2 Splash 1131:2 waits 4 seconds, then dissolves over 300 ms to English-selected Language 1166:215.
- Screen 003 destination remains pending as previously requested.

## Verification

Figma accepted the component reaction graph, Splash timing and entrance tracks. Resting Language and compact dot screenshots reviewed: exact copy, readable text, stable footer and centered loader. Interactive Present playback was not exercised. Prototype uses fixed mock processing timing; it does not save data or wait for a server response. Original designs and protected source directories were not modified.
