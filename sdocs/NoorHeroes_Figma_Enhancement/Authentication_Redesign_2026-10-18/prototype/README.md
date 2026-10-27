# NoorHeroes authentication review companion

Run `node server.cjs` from this directory, then open http://127.0.0.1:8766/. The pre-existing port 8765 preview is separate; use 8766 for controlled HTTP behavior.

Active files: index.html, app-v2.js, auth-v2.css (with the preserved style.css), auth-core.cjs, server.cjs. app.js is the previous companion implementation and is no longer loaded. Do not rerun the one-time upgrade-html.py helper.

The editable Figma source remains MR9935oQZACMjndzGIUgq5, V2 Onboarding. Inputs reuse NH TextField 357:2; standard boundary height 56, padding 8/16, radius 12, Poppins 16/26. The local Snackbar matches the NH square dark surface, 12 px text and gold Retry action. Toolbar wordmark is exported from approved 1345:1449; existing supplied monogram retained.

## Review

- Choose Login or Registration in the review controls. Use fictional information only, for example parent@example.com or the US numbering-plan test fixture 2015550123.
- Country picker supports name, ISO and dial-code search, clear, empty results, selection, and keyboard arrows.
- Focus, blur, type, clear, submit invalid values, and correct them. Country and values remain in memory across recovery and Login/Registration navigation. Sensitive identifiers are not saved to localStorage; language remains persisted.
- Registration requires the existing Terms → separate Privacy sheet sequence, adult confirmation and child-data-processing consent. Optional choices start off independently. Draft legal copy is mirrored from Figma and requires review before production.
- Select a controlled HTTP outcome before submitting either button. The server really returns 200, 401, 403, 422, 429, 500 or 503. Network destroys the mock socket; timeout aborts at 3 seconds. Rate limit uses the real Retry-After header (3 seconds for review). Generic server text never appears in the UI.
- Google keeps its white surface/dark animated dots; primary Send/Create keeps its gradient/light dots. Both submissions are guarded while busy, with the other button visible and disabled.
- 422 applies inline only when the response identifies the active phone/email input. Google and unrelated-field 422 errors use Snackbar.
- Success restores the buttons. OTP is deliberately pending approval; no destination is invented.
- Registration Back returns to Login. The local companion does not contain the Intro screens, so Login Back remains disabled here; existing Figma navigation is preserved.
- Review controls support text scaling, RTL layout inspection and reduced motion. Body scrolling keeps controls reachable on short viewports; no extra Figma device-size frames were created.

## Verification

`node --test auth.test.cjs http.test.cjs` (server must be running) — five test groups pass. `node verify.mjs` — 245 countries, dial codes and flag assets pass.

The companion calls only its loopback mock endpoint /mock/auth-flow. This is not a production API endpoint, Google OAuth implementation, or account service. No production auth request is made. Figma Code Layers are disabled on this account; the local companion cannot be embedded. Native Figma scenarios are controlled variable presets, with a 15-second 429 overlay hold. Present playback remains unverified.
