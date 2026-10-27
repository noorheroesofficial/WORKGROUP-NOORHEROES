# Runtime changelog - 2026-10-22

## Added
- Shared typed Snackbar state with bounded distinct feedback, duplicate suppression, cancellation cleanup, explicit action results and lifecycle disposal.
- Approved Snackbar design tokens, bundled existing Poppins fonts with license, reusable KMP renderer and overlay.
- Five behavioral regression tests plus source audit and verification evidence.

## Changed
- Twenty active consumers now use the common host/state; ten default hosts replaced, two prior shared consumers upgraded and eight ignored feedback effects wired.
- Common clipboard receives the share preview's existing CopyLink effect before existing success copy displays.
- Legacy public Snackbar/Toast signatures remain available; persistent alerts, field validation, XP celebrations and business/API/navigation logic are preserved.

## Validation
- Core-ui19/19, onboarding295/295, stories168/168, bedtime144/144; rewards143/147, with four unchanged real-clock fixture failures documented.
- Shared Android compile and core-ui common metadata compile succeeded. Native/device accessibility and positioning checks remain unperformed.
