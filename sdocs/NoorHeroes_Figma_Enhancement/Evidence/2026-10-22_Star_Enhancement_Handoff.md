# Calm star enhancement — V2 onboarding and authentication

22 October2026. Decoration-only enhancement. Current application screens, source images, text, forms, buttons, component meanings and navigation preserved. No screen removed or newly invented.

## Delivered

Added181 component instances across18 screen compositions: Splash/default and reduced-motion, four intros, Login, Registration, five OTP compositions, and five Parent PIN compositions including active confirmation. 121 additions blink and60 remain static. Reused existing **NH/Atmosphere/Calm Star1726:1206**, not a second component family. Existing approved four-point gold vector uses color token295:13.

The pre-existing component's artwork opacity was approximately0.2–0.72 percent and effectively invisible. Corrected its child artwork to18/44/72 percent for Dim/Mid/Bright and36 percent for Still, without changing shape or color. Individual screen instances vary from5–12px with restrained outer opacity; static stars remain mixed into the sky.

Reused three native rhythm loops: A holds3.7s plus2.4s fades ≈6.1s; B4.6s plus2.4s ≈7.0s; C5.2s plus2.7s ≈7.9s. Holds1.1–2.2s and smooth0.7–1.0s ease-in-out fades avoid rapid, synchronized flashing. Phase offsets and mixed starting brightness prevent uniform blinking. New stars on the dedicated reduced-motion Splash are static.

## Placement and preserved areas

Each updated root has one **Atmosphere/Enhanced Calm Stars** frame behind foreground UI. Greater density fills the broad OTP gaps; dense Registration receives fewer additions. Intro stars sit in clear space above/below the content-card stack, outside copy, hero art, page indicators, buttons and supporting text. Splash additions stay clear of the full logo/wordmark lockup and loading rail. Auth compositions protect toolbar, approved logo artwork, cards, footer links, keyboard and Snackbar bounds.

Moved102 pre-existing decorative stars that intersected protected branding/card edges/footer areas into clear sky positions. Nodes remain editable and were not deleted. Six legacy stars fully hidden under the opaque OTP keyboard are explicitly exempt from visible-collision reporting and left unchanged. The original OTP below-card star remains.

Dense language lists, country selectors, legal documents, preference sheets, processing guards and scenario-control panels were reviewed but receive no independent star layer. They lack suitable clear branded space or would duplicate the underlying sky. Biometric sheets inherit the enhanced underlying PIN background through their existing backdrop; no star goes inside the sheet, fingerprint, text, button or Snackbar. No success dialog was created.

## Coverage

| Screen/frame | Added | Blinking | Static |
|---|---:|---:|---:|
| 1131:2 | 12 | 9 | 3 |
| 1146:2 | 12 | 0 | 12 |
| 1215:34 | 8 | 6 | 2 |
| 1215:138 | 8 | 6 | 2 |
| 1215:246 | 8 | 6 | 2 |
| 1215:356 | 8 | 6 | 2 |
| 1355:2696 | 9 | 6 | 3 |
| 1459:256 | 5 | 3 | 2 |
| 1612:1277 | 16 | 12 | 4 |
| 1619:404 | 16 | 12 | 4 |
| 1619:614 | 16 | 12 | 4 |
| 1619:820 | 10 | 7 | 3 |
| 1619:1026 | 8 | 6 | 2 |
| 1650:502 | 9 | 6 | 3 |
| 1654:1134 | 9 | 6 | 3 |
| 1654:1428 | 9 | 6 | 3 |
| 1709:675 | 9 | 6 | 3 |
| 1709:947 | 9 | 6 | 3 |

## Motion and accessibility boundaries

Native After Timeout → Change To → Smart Animate component loops reuse the existing design's animation pattern. Stars write no application variables and have no click, hover or navigation actions. No blur, translation, rotation or scale animation is added. At most12 additional stars blink on a visible composition; instances share10 existing master variants rather than cloned master components.

Existing Login reduced-motion flag1389:3045 (via1726:1095 alias) and Biometric flag1670:1066 route every animated phase to the static variant at its next hold with an instant transition. All18 stop branches were evaluated. After disabling reduced motion, restart the prototype to resume loops; the static state does not poll. Figma has no automatic OS preference integration here. Local companion implementation unchanged.

## Verification

All18 screen foreground/layout/application-interaction fingerprints match before and after. Initially all original nodes matched before the intentional legacy decoration relocations; those relocations affect decoration only. Added stars fit390×844 roots and sit behind foreground. All three loops close correctly with valid component-only destinations; static state has no timeout loop. Reduced-motion branches pass.39 saved PIN/confirmation/biometric regression checks passed through stable click targets. No screen removed or target rerouted.

Final Splash, first Intro, Login, Registration, OTP and Parent PIN screenshots inspected at390×844. Files:2026-10-22_Stars_Final_1131-2.png,1215-34.png,1355-2696.png,1459-256.png,1612-1277.png and1650-502.png (same filename prefix). Earlier screenshots without Final are pre-clearance review records only.

Native Present playback, actual frame-rate performance and physical mobile-device rendering remain unverified. Timeline video export would not test these prototype component state machines, so no timeline-render claim is made. Restart the prototype to load the updated shared components and review the soft blinking.

[Verification and full node ledger](2026-10-22_Star_Enhancement_Verification.json). Existing app: [V2](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1128-2). Stop for review.

## Maintenance and rollback

Reuse Calm Star A/B/C plus Still. Keep decoration-only placement behind UI and check clear bounds for each screen rather than blanket scattering. Do not animate educational icons, text or input/button affordances as background stars. For rollback, remove only the18 newly recorded atmosphere layers, restore102 legacy positions from the from/to ledger, and restore the10 master child opacity values from the before-state ledger. No application handlers or source designs require rollback.

