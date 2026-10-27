# NH authentication input upgrade

Scope: editable V2 Login and Registration, plus the existing local review companion. No production app/backend changes. User explicitly approved the companion because Code Layers are disabled.

Requirements: Feature_A1_Splash_Auth_Onboarding.md and A1 registration/consent blueprint; supplied NH TextField 357:2 and boundary 356:127. Retain consent gates, country selection, distinct Send code / Google loaders, and unapproved OTP exit pending.

Implementation story: reuse NH variants and tokens in Figma; controlled presets demonstrate native states. Local HTML inputs implement focus, blur, validation and correction. libphonenumber-js/max validates country numbering plans; validator.js checks trimmed email. A loopback-only mock HTTP endpoint returns the backend's error envelope shape, without calling production services. Field 422 errors stay inline; generic failures use NH Snackbar. Guard duplicate submissions and preserve drafts.

Verification: RED unit tests for country rules, email, safe error mapping and HTTP outcomes; GREEN implementation; browser tests for both forms, correction, country persistence, real mock HTTP status, loader behavior, consent gates, retry/cooldown, keyboard and narrow viewport. Inspect Figma component variants, geometry and routes. Present playback remains separately unverified.
