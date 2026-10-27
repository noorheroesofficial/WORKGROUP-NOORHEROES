# Screen 007 — Login readiness and copy proposal

Date: 2026-10-13. Status: user explicitly approved this proposal: “Use the proposed Login copy and layout.” Subsequently implemented; see [execution review](007_Login_Execution_Review.md). Source-audit findings below describe the evidence available before implementation.

## Scope and placement

Implement only Screen 007 and necessary states at 390 × 844 in existing file MR9935oQZACMjndzGIUgq5, page 928:2, NoorHeroes V2 Design 1128:2 → Onboarding 1270:140. Reuse the existing hierarchy; do not create another V2 section. Follow [finalized baseline](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) and [module rules](../13_INCREMENTAL_MODULE_ORGANIZATION.md). Further numbered screens require their own review.

## Verified sources and remaining gap

- [Screen prompt](../Screen_Prompts/007_Login_phone_email_Google.md), section 4: “Exact copy unavailable: execution blocked for copy-dependent design.” This remains unresolved after current inspection.
- PRD: PRD_Documents/Child App (1-12)/Feature_A1_Splash_Auth_Onboarding.md, §§1.7 FR-6/9/21/22, 1.11, 1.13, 1.14, 1.18 row 7, and 2.4 additional-screen matrix. Defines returning-parent phone/email OTP and Google authentication, Register and recovery paths, enumeration-safe errors, pending submission and connectivity requirements. No standalone Login heading or full copy specification.
- Blueprint: Development_Blueprints/A1_Splash_Auth_Onboarding/KMP/03-registration-consent-otp-verification-flow.md, §§5,10,12,17; and 04-google-sign-in-authentication-flow.md, §§5,10,12. Google cancellation returns neutrally; success uses backend-directed routing. No Apple sign-in.
- Live Figma: current Onboarding contains 15 existing objects and no Login. Mobile-wide frame-name and text searches found Registration references and Log In links, but no standalone Login screen. Registration 1095:24 is not a Login substitute.
- Screens/Verification/07_login_screen.png was visually inspected. Despite its filename, it displays “Create your account”, consent checkboxes and “Create Account”: Registration, not Login.
- Existing English strings in NoorHeroes/core/core-common/src/commonMain/composeResources/values/strings.xml provide registration-shared labels. They do not establish a complete approved Login content set.
- NoorHeroes/shared/src/commonMain/kotlin/com/noorheroes/app/navigation/OnboardingNavGraph.kt maps LoginRoute to RegistrationConsentScreen. This implementation mismatch does not override the separate Login requirement.

## Concrete copy proposal for approval

Source-backed labels retain their source spelling. Reuse on Login is proposed; these findings do not imply approval of newly authored copy.

| Role | Exact proposed text | Provenance |
|---|---|---|
| Heading | Log In | Existing Figma link 1095:201; promotion to heading proposed |
| Supporting instruction | Use your phone number or email to log in. | New copy proposal |
| Method tabs | Phone / Email | Existing registration UI |
| Phone field | Phone number | register_phone_placeholder |
| Email field | Email address | register_email_placeholder |
| Country picker title | Country code | New copy proposal |
| Country search | Search countries | New copy proposal |
| Empty country search | No countries found. | New copy proposal |
| Primary action | Send code | New copy proposal; action required by OTP flow |
| Pending label | Sending code… | New copy proposal |
| Separator | or continue with | register_or_continue_with |
| Google action | Continue with Google | register_continue_google |
| Registration link | Register | PRD §1.18 row 8; Screen 007 required role |
| Recovery link | Forgot access | PRD FR-22 |
| Invalid phone | Enter a valid phone number. | New copy proposal |
| Invalid email | Enter a valid email address. | New copy proposal |
| Offline helper | Connect to the internet to continue | K-03 §12 exact wording |
| Generic error | Something went wrong, please try again | K-03 §10 exact wording |
| Timeout | This is taking longer than expected. Please try again. | New copy proposal; timeout requirement is 10 seconds |
| Recovery action | Try again | New copy proposal |
| Expired session | Please log in again | Existing error_please_log_in_again resource |

No educational content, religious text, legal claims, fabricated account data or translated copy is proposed. Country list values must come from existing project data; do not fabricate a supported-country list or infer a fixed country from the user's location.

## Proposed composition

Reuse finalized cream-to-pale-teal gradient, square top corners, Poppins, ink/secondary/teal colors, 20px horizontal inset and 350px content width. Top Back control: 44px target, 18px shared rounded arrow, matching Skip ink and 45% white surface. Header uses existing 20/28 heading style. Form follows in a vertical Auto Layout stack, phone/email segmented control, country selector only in Phone mode, editable-looking identifier field and one primary OTP action. Place secondary Google action after separator; Register and Forgot access remain readable with 44px targets. Do not add registration consent rows to returning Login.

Primary button: 350 × 56, 18px radius; existing 14/20 Poppins SemiBold label style. Shared 18px icons and 4px label gap. Fields use a documented local readable 16/24 text role, helpers/errors 14/20 rather than the Intro's small decorative footer copy. Reuse official Google mark from existing Figma registration assets without recoloring or replacing it with a generic Material icon. Avoid imposing Intro hero/cards on the form. New-screen layout must be visually compared against all four finalized intros.

## States and prototype contract

Phone and Email default/empty states; valid-entry demo states if approved data exists; inline invalid format; pending OTP; generic error; offline; timeout/retry; session expired. Preserve identifier draft and method on retry. Prevent duplicate submission. Pending may animate a spinner/dots without stretching the text; stop motion when leaving. No separate success screen. Show server errors without revealing whether an account exists. No password or PIN bypass.

For the prototype, input and authentication outcomes are simulations. Do not claim real OTP, Google SDK, server processing or durable persistence. If free-text input is not supported by the available Figma prototype API, document the limitation rather than silently substituting a working input claim. Do not invent test phone/email data.

Google's native account picker is OS-owned; do not draw fake account identities. Cancellation restores Login without an error. Future bootstrap-directed results remain unmapped until confirmed V2 destinations exist.

PRD requires spinner/duplicate-submit blocking and a 10-second timeout; successful OTP navigation must wait for a confirmed OTP screen, not a convenient existing frame. Pending without a confirmed success destination must not loop forever: cancellation/error-retry scenarios can be reviewed separately, and success navigation remains documented as pending.

## Connections when Login is approved and created

- Confirmed incoming: all four Intro Skip controls → Login; final Parent Shield action → Login under the established onboarding flow. Preserve existing Intro forward/back connections.
- Login Back → invoking Intro/history; preserve originating selection/history. Standalone session-expired entry must not create an unauthenticated route to protected content.
- OTP success → Screen 010 when its V2 frame exists and is confirmed.
- Register → Screen 008 when its V2 frame exists and is confirmed; do not link to original Registration.
- Forgot access → Screen 030 when its V2 frame exists and is confirmed.
- Google success → verified downstream state only when relevant V2 frames are present.
- Do not create placeholder destinations or unapproved future screens.

## Acceptance checks before handoff

- Exact copy decision recorded; source-backed versus newly approved strings distinguishable.
- Single 390 × 844 viewport; proper keyboard/scroll clearance; 44px hit targets.
- Shared gradient, typography, surfaces, icon sizes/gaps, alignment and Auto Layout verified against all four finalized intros.
- Text/controls remain readable; errors use text and not color alone.
- Applicable default/loading/error/offline/retry states checked; no fabricated authentication result.
- Reaction graph checked against existing confirmed destination IDs; report unmapped future routes.
- Motion inspected in playback if available; do not represent structural inspection as playback verification.
- Source PRD, blueprints, screenshots, originals and unrelated screens unchanged.

Decision received: user approved the proposed copy and layout. The finished Figma screen now awaits its separate visual review; approval of this proposal does not imply approval of the implementation.
