# NoorHeroes — Complete Design Asset Prompt Library (`design_prompts.md`)

**Purpose:** A single, exhaustive reference of AI image-generation prompts covering every icon, illustration, and image asset needed to build the NoorHeroes Figma file — grounded directly in the product's actual documented features, screens, brand tokens, and content-governance rules (sourced from the Consolidated Blueprint, the Enhanced Blueprint, the Feature Reference, and the 37 individually-specified feature documents produced for this project).

**How this file is organized:** Most icons and many illustrations are **shared across dozens of screens** (a back arrow, a heart/favorite icon, an empty-state illustration style). Repeating a full boilerplate prompt hundreds of times would make this file unusable. Instead:
- **§1** defines the brand foundation (exact colors, type, icon grid, illustration rules, and — critically — the religious-content guardrail) **once**.
- **§2–§4** define **reusable global libraries** (core brand assets, the full icon set, the avatar/character system) that every subsequent feature section references by name rather than re-describing.
- **§5 onward** is organized **by feature/screen** (matching the app's own A/B/C/D/E/F feature tracks), listing only what's **unique** to that screen: its specific empty states, feature illustrations, hero art, and any icon not already in the global library.
- **§27–30** cover global states, marketing, seasonal re-skins, and a master asset checklist.

Every prompt is written to be pasted directly into an AI image generator (Midjourney, DALL·E, Stable Diffusion, Adobe Firefly, etc.) and is Figma-import-ready (flat, vector-friendly, transparent background where noted).

---

## Table of Contents

1. [Brand Foundation & Content Guardrails](#1-brand-foundation--content-guardrails)
2. [Core App-Level Brand Assets](#2-core-app-level-brand-assets)
3. [Global Icon Library](#3-global-icon-library)
4. [Avatar & Character System](#4-avatar--character-system)
5. [Splash, Language & Onboarding (A.1)](#5-splash-language--onboarding-a1)
6. [Home Dashboard (A.2)](#6-home-dashboard-a2)
7. [Stories Module (A.3)](#7-stories-module-a3)
8. [Bedtime Audio Player (A.4)](#8-bedtime-audio-player-a4)
9. [Quran & Arabic Learning (A.5)](#9-quran--arabic-learning-a5)
10. [Dua Learning (A.6)](#10-dua-learning-a6)
11. [Habit Tracker (A.7)](#11-habit-tracker-a7)
12. [Daily Quiz Engine (A.8)](#12-daily-quiz-engine-a8)
13. [Skill Tree / Mastery (A.9)](#13-skill-tree--mastery-a9)
14. [Games Module (A.10)](#14-games-module-a10)
15. [Rewards System (A.11)](#15-rewards-system-a11)
16. [Avatar System (A.12)](#16-avatar-system-a12)
17. [Search (B.13)](#17-search-b13)
18. [Favorites (B.14)](#18-favorites-b14)
19. [Offline Downloads (B.15)](#19-offline-downloads-b15)
20. [Child Profile (B.16)](#20-child-profile-b16)
21. [Notifications — Child (B.17)](#21-notifications--child-b17)
22. [Islamic Facts (B.18)](#22-islamic-facts-b18)
23. [Parent Area (C.19–C.26)](#23-parent-area-c19c26)
24. [Parent Web Account Portal (D.27)](#24-parent-web-account-portal-d27)
25. [Admin & Scholar Portal (E.28–E.34)](#25-admin--scholar-portal-e28e34)
26. [Ramadan Mode (F.36)](#26-ramadan-mode-f36)
27. [Global Empty / Loading / Error / Success State Library](#27-global-empty--loading--error--success-state-library)
28. [Marketing & App Store Assets](#28-marketing--app-store-assets)
29. [Seasonal Icon Re-Skins](#29-seasonal-icon-re-skins)
30. [Master Asset Checklist](#30-master-asset-checklist)

---

## 1. Brand Foundation & Content Guardrails

### 1.1 Exact Brand Tokens (source: product design-token CSS)

| Token | Hex | Use |
|---|---|---|
| Teal (primary) | `#0B5E4A` | Primary actions, nav, headers |
| Teal Light | `#147A61` | Hover/secondary states |
| Teal Pale | `#E6F4F1` | Backgrounds, chips |
| Gold (accent) | `#C9921A` | Rewards, highlights, CTAs |
| Gold Light | `#E8B84B` | Gradients, glows |
| Gold Pale | `#FDF5E4` | Warm backgrounds |
| Cream (base bg) | `#FDF8F2` | App background |
| Cream Dark | `#F5ECD8` | Card backgrounds |
| Ink (text) | `#1A1207` | Primary text |
| Ink Soft | `#3D2F1A` | Secondary text |
| Muted | `#7A6A54` | Tertiary text |
| Border | `#D6C9B0` | Dividers, outlines |
| Purple (accent, badges) | `#7B3FA0` | Achievement/mastery accents |
| Alert Red | `#C0392B` | Errors, destructive actions |
| White | `#FFFFFF` | Cards, contrast surfaces |

**Typography for any prompt implying on-image lettering:** Playfair Display (serif, display headings — elegant/premium feel), DM Sans (sans-serif, body/UI text — clean/modern), Amiri (Arabic serif — for Arabic display text/logotype).

### 1.2 The Dual-User Design Rule (applies to every prompt below)

- **Child-mode assets:** warm, colorful, animated-feeling, soft rounded shapes, playful without being chaotic, generous glow/light effects, ages 3–12 appropriate.
- **Parent-mode assets:** calmer, denser, more premium/credible, muted accent use, data-visualization-appropriate, still warm but "grown-up."
- **Admin Portal assets:** a *third*, distinct dense professional SaaS-tool register (cool neutral greys, sharp/minimal rounding, muted blue-grey, functional over decorative) — never the child app's playful palette.
- **Never mix registers** — a parent-facing icon should never look like a child-mode sticker, and vice versa.

### 1.3 Universal Illustration Style Guardrails (apply to every prompt in this document)

- Flat or lightly-shaded flat-vector illustration style (no photorealism, no 3D-render photographic style) unless a prompt explicitly says otherwise.
- **No realistic human faces or figures anywhere in the product** — characters are abstract/rounded/non-human (the Noor companion, symbolic figures, silhouettes) consistent with the app's established character design and general child-safety/likeness policy.
- No copyrighted characters, brand marks, or real public figures.
- Material Design 3 spirit: rounded corners, clear elevation via soft shadow (not hard drop-shadow), generous whitespace, 8dp-multiple spacing implied in composition.
- SVG-friendly: clean vector shapes, limited gradient complexity, no fine photographic texture, so the output traces/exports cleanly to SVG for icons.

### 1.4 ⚠️ Critical Religious-Content Guardrail (non-negotiable — read before generating any Story/Prophet-related asset)

Islamic tradition (across the schools of thought this platform's Scholar Review Board follows) holds that the Prophets — and Prophet Muhammad ﷺ specifically — are **never visually depicted** as figures with faces/bodies. This is not a stylistic preference; it is a core content-safety rule this entire product's Scholar Review pipeline (see Feature E.29) exists to enforce.

**Every prompt in §7 (Stories) and anywhere else referencing "Prophet stories" in this file has already been written to comply** — they ask for symbolic representation (light rays, calligraphy, landscapes, architecture, animals, silhouettes-from-behind-only where a human presence is implied, or abstract glowing motifs) **instead of** a depicted Prophet figure. If you or a designer ever hand-modify one of these prompts, preserve this rule: **never** add "a depiction of [Prophet name]," "[Prophet name]'s face," or similar phrasing to any prompt in this document.

### 1.5 Standard Prompt Suffix Templates

To avoid repeating boilerplate hundreds of times, every icon/illustration prompt below should have the relevant template appended when you actually submit it to a generator:

**[ICON-TEMPLATE]** — append to any icon prompt:
> "...Flat vector icon style, single bold silhouette or two-tone fill, 24x24dp grid with 2dp internal padding, consistent 2px stroke weight if outlined style is used, transparent PNG or SVG-ready background, no gradients unless specified, Material Design 3 icon conventions, crisp at 24px and legible at 16px."

**[ILLUSTRATION-TEMPLATE]** — append to any full illustration/character/scene prompt:
> "...Flat or softly-shaded vector illustration style, warm and inviting children's-app aesthetic (or calmer parent-mode aesthetic where specified), soft rounded shapes, gentle glow/particle accents where appropriate, no realistic human faces, no copyrighted characters, high resolution (at least 2000px on the long edge), clean background suitable for Figma layering (transparent or simple flat-color backdrop as specified)."

**[HERO-BANNER-TEMPLATE]** — append to any hero/banner/marketing image prompt:
> "...Wide-format composition with clear focal hierarchy, generous negative space reserved for UI text overlay, warm and trustworthy premium-family-app mood, no realistic human faces, high resolution, web/app-store ready."

---

## 2. Core App-Level Brand Assets

> App icon and Play Store feature graphic prompts are already fully specified in the companion file `NoorHeroes_App_Icon_Banner_Prompts_and_Specs.md`. This section covers everything else at the app-identity level.

### 2.1 The Noor Companion — Master Character Sheet

*(Noor is the glowing lantern/crescent-moon mascot referenced throughout the entire product — Home greetings, story narration, reward reveals, onboarding. Generate this once as a definitive reference sheet, then reuse it as a style/character-consistency reference for every subsequent Noor appearance.)*

**Prompt:**
> "A character reference sheet for 'Noor,' a friendly mascot for a children's Islamic learning app. Noor is a soft, rounded, glowing lantern-and-crescent-moon hybrid character — no human face, no eyes drawn as human eyes, instead a warm gentle glow that conveys expression through light intensity and gentle shape shifts (glowing brighter = happy, soft dim glow = calm/sleepy). Warm gold (#E8B84B) glowing body with a soft teal (#147A61) under-glow, small soft star sparkles floating near it. Show 6 poses/expression states in a grid: (1) neutral/greeting — floating upright, gentle glow, (2) joyful/celebrating — glow brightening with small light-burst sparkles, (3) calm/bedtime — dimmed, softly closed-shape, floating low, (4) encouraging/coaching — leaning slightly forward with a soft directional glow, (5) sleepy/night-mode — very dim, curled shape, (6) proud/reward-reveal — glow radiating outward with a subtle golden halo. Consistent flat-vector style across all six, no realistic human features anywhere, transparent background, character-turnaround-sheet layout. [ILLUSTRATION-TEMPLATE]"

### 2.2 Splash Screen Graphic

**Prompt:**
> "A vertical mobile splash screen illustration for a children's Islamic learning app. Deep warm teal (#0B5E4A) background evoking a calm night sky, with a soft radial glow at the center. A gentle geometric Islamic pattern (eight-pointed star lattice, very subtle, low-opacity) frames the edges. Centered, the Noor companion character (glowing lantern/crescent-moon mascot, warm gold) floats gently with soft light rays. Small soft stars scatter across the upper portion of the composition. Generous empty space at the bottom third for a logotype and loading indicator to be added in Figma. Calm, premium, reassuring first-impression mood. [ILLUSTRATION-TEMPLATE], portrait 9:19.5 aspect ratio."

### 2.3 App Wordmark / Logotype Lockup

**Prompt:**
> "A clean wordmark logotype design for 'NoorHeroes' — the word 'Noor' in a warm gold gradient using an elegant serif display font evoking Playfair Display, paired with 'Heroes' in a softer rounded sans-serif in warm teal. A small glowing crescent-moon-and-star mark sits to the left of the wordmark, matching the app icon's symbol. Below, in a lighter weight, a small Arabic rendering 'نور هيروز' in an elegant Amiri-style Arabic serif. Horizontal lockup, transparent background, suitable for both light and dark surfaces (include a note showing both a dark-teal-on-cream version and a cream-on-teal reversed version side by side). [ILLUSTRATION-TEMPLATE]"

### 2.4 Loading Spinner / Progress Motif

**Prompt:**
> "A simple, elegant circular loading indicator design for a children's app, based on a rotating soft glow around a small crescent-moon-and-star mark at the center. Warm gold gradient ring with a soft trailing fade (for animation reference — show 4 rotation-state frames side by side), teal background dot at center. Minimal, flat, small-format (suitable for a 48x48dp loading spinner), transparent background. [ICON-TEMPLATE], circular composition."

---

## 3. Global Icon Library

*(These are the reusable, shared icons appearing across dozens of screens throughout every feature document. Each row is a complete brief — apply [ICON-TEMPLATE] to every one. Where a direction matters, an RTL-mirror variant is noted, since the app fully supports Arabic/Urdu RTL layouts.)*

### 3.1 Bottom Navigation Icons (5 tabs, each needs active + inactive state)

| Icon | Visual Description | Active State | Inactive State |
|---|---|---|---|
| Home | A simple rounded house/lantern-roof silhouette with a small glow dot inside | Filled, warm gold, subtle glow | Outlined only, muted grey-brown (#7A6A54) |
| Learn | An open book with a small crescent-moon bookmark ribbon | Filled, warm teal | Outlined, muted |
| Stories | A crescent moon cradling a small star (matches app icon motif, simplified) | Filled, warm gold | Outlined, muted |
| Rewards | A five-pointed star inside a soft rounded badge/medal outline | Filled, warm gold with tiny sparkle accent | Outlined, muted |
| Profile | A simple rounded avatar-frame silhouette (abstract, no face) with a small crescent accent | Filled, warm teal | Outlined, muted |

**Combined prompt:** "A set of 5 bottom-navigation icons for a children's Islamic learning app, each shown in both an active (filled, warm gold or teal) and inactive (thin outline, muted brown-grey) state: (1) Home — a rounded house/lantern-roof shape with a small glow dot, (2) Learn — an open book with a crescent-moon bookmark, (3) Stories — a crescent moon cradling a small star, (4) Rewards — a star inside a rounded medal outline, (5) Profile — an abstract rounded avatar-frame with a small crescent accent. Consistent line weight and corner rounding across all 10 icon states, arranged in a clean grid, transparent background. [ICON-TEMPLATE]"

### 3.2 Global Action Icon Set

**Prompt (generate as one consistent icon sheet, then export individually):**
> "A comprehensive flat vector icon set for a children's Islamic learning app's UI, all icons sharing identical line weight, corner rounding, and a warm teal/gold two-tone palette, arranged in a clean grid, transparent background. Include: back arrow (chevron-left), forward arrow, close (X), checkmark, plus/add, minus/remove, search (magnifying glass), microphone (voice input), microphone-muted, play (triangle), pause (two bars), stop, skip-forward-15s, skip-back-15s, volume-high, volume-mute, heart/favorite (outline and filled), heart-broken/unfavorite, download (arrow into tray), download-complete (checkmark in tray), download-failed (exclamation in tray), share, more-options (three dots, vertical), filter/sort (sliders), calendar, clock/time, lock (closed padlock), unlock (open padlock), fingerprint, PIN-pad/keypad, eye (show), eye-slash (hide), bell/notification, bell-muted, settings/gear, info (circled i), warning (triangle with exclamation), success-checkmark-in-circle, error-x-in-circle, star (outline and filled), flame/streak, trophy, gift-box, coin/points, badge/medal, book-open, book-closed, moon-crescent, sun, globe/language, edit-pencil, trash/delete, refresh/retry, arrow-up, arrow-down, chevron-up, chevron-down, home, camera, image/photo, audio-waveform, offline-cloud-with-slash, wifi, location-pin, family/people (abstract, non-figurative — three soft rounded blob shapes of varying size, never depicting human faces or bodies). [ICON-TEMPLATE]"

*(Note: for RTL locales, mirror the following directional icons: back arrow, forward arrow, skip-forward/skip-back, chevron-left/right — generate a mirrored variant set for Arabic/Urdu builds.)*

### 3.3 Content-Type Badge Icons (small overlay badges used across Search/Favorites/Downloads grids)

**Prompt:**
> "A set of 3 small, simple content-type indicator badges for a children's app, each a small rounded-square tag with a distinct icon: (1) Story — a small open-book icon, teal background, (2) Surah/Quran — a small crescent-and-star icon, gold background, (3) Dua — a small pair of cupped-hands icon (abstract, non-realistic), purple background. Flat, minimal, consistent 2px corner radius, transparent surrounding background. [ICON-TEMPLATE]"

---

## 4. Avatar & Character System

### 4.1 Avatar Base Library (child-selectable at onboarding, A.1/A.12)

**Prompt:**
> "A set of 6 diverse, friendly, non-human/abstract avatar base characters for a children's Islamic learning app's profile-selection screen. Each is a soft, rounded, blob-like creature (never a realistic human figure or face) with a distinct color identity and a small personality prop: (1) a warm gold star-creature with a tiny book, (2) a soft teal moon-creature with a tiny lantern, (3) a coral/warm-pink cloud-creature with tiny wings, (4) a soft green leaf-creature with a tiny watering-can, (5) a warm purple comet-creature with a tiny trailing sparkle tail, (6) a soft blue droplet-creature with a tiny umbrella. Each character shown front-facing in a simple, joyful pose, flat vector style, consistent size/proportions across all 6, transparent background, arranged in a clean grid. [ILLUSTRATION-TEMPLATE]"

### 4.2 Avatar Customization Items (A.12 — outfits, glow states, accessories)

**Prompt (outfits):**
> "A set of 4 simple, modest clothing/outfit overlay accessories designed to fit onto the rounded avatar-creature base characters from a children's Islamic app. Each is shown as a standalone flat-icon overlay (not on a character): (1) a simple soft-teal robe/cloak shape, (2) a warm gold sash/scarf shape, (3) a soft patterned vest shape with a subtle geometric Islamic pattern, (4) a cozy soft-purple wrap shape. All modest, simple, no human-body-shaped garments (they're designed to drape over a blob-creature, not a human figure), flat vector style, transparent background. [ICON-TEMPLATE]"

**Prompt (glow states):**
> "A set of 4 avatar 'glow aura' overlay effects for a children's app, each a soft radiating light-ring effect meant to surround an avatar character: (1) gentle warm gold glow, (2) soft teal shimmer, (3) sparkling star-particle aura, (4) a calm moonlight-blue soft halo. Each shown as an isolated circular glow effect on a transparent background, soft edges, no hard outlines, layerable in Figma. [ILLUSTRATION-TEMPLATE]"

**Prompt (accessories):**
> "A set of 6 small, simple avatar accessory icons for a children's Islamic app's avatar customization shop: a small soft crown/headpiece, a pair of round glasses, a small backpack, a tiny lantern to hold, a small book to hold, and a soft scarf. Flat vector style, consistent proportions, warm color palette, transparent background, arranged in a grid. [ICON-TEMPLATE]"

### 4.3 Symbolic Story Character Library (Prophets & Companions — GUARDRAIL APPLIES, see §1.4)

**Prompt (symbolic representation set, never a depicted figure):**
> "A set of 6 symbolic, non-figurative illustration motifs representing different Prophet stories for a children's Islamic app, each conveying the story's setting or theme WITHOUT depicting any human figure at all: (1) Prophet Nuh's story — a gentle wooden ark silhouette on calm gold-lit water with a soft dove shape above, (2) Prophet Yunus's story — a peaceful moonlit ocean scene with a soft glowing shape suggesting a large fish silhouette beneath the waves, (3) Prophet Ibrahim's story — a warm desert landscape at sunset with a small glowing flame motif and a simple stone structure silhouette, (4) Prophet Musa's story — a parted-sea light-beam motif with soft glowing water walls, (5) Prophet Yusuf's story — a star-filled night sky with eleven small glowing stars and one larger moon, (6) general 'Seerah/Companions' motif — a warm desert oasis scene with a simple mosque-lantern silhouette. Every scene uses landscape, light, water, animals, or architecture only — absolutely no human figures, faces, or bodies anywhere. Warm, reverent, gentle illustration mood, flat-to-softly-shaded vector style, consistent color grading across the set (warm golds and deep teals). [ILLUSTRATION-TEMPLATE]"

---

## 5. Splash, Language & Onboarding (A.1)

*(Reuses §2.2 Splash Screen and §4.1 Avatar Library. New assets below.)*

### 5.1 Language Selection Illustration

**Prompt:** "A friendly flat illustration for a language-selection screen: four small glowing speech-bubble shapes arranged in a soft arc, each containing a simple abstract script-mark suggestion (not real readable text, just gentle calligraphic squiggle shapes) in a different color (teal, gold, coral, purple), representing English, Arabic, Urdu, and Hindi without using actual language text. Warm cream background, centered composition, generous padding. [ILLUSTRATION-TEMPLATE]"

### 5.2 Consent & Child-Safety Illustration

**Prompt:** "A calm, reassuring flat illustration for a parental-consent screen. A soft glowing shield shape (rounded, warm teal, no sharp edges) with a small crescent-moon-and-star mark at its center, gently cradled by two simple abstract soft-blob 'hands' shapes (non-human, non-realistic) from below, suggesting protection and care. Warm, trustworthy, premium-parent-mode mood (calmer palette than child-mode illustrations). [ILLUSTRATION-TEMPLATE]"

### 5.3 Parent PIN Setup Illustration

**Prompt:** "A simple, reassuring flat illustration for a Parent PIN setup screen: a soft rounded padlock shape in warm teal with a small glowing keyhole shaped like a crescent moon, floating above a simple numeric keypad silhouette rendered in soft outline. Clean, calm, parent-mode premium aesthetic. [ILLUSTRATION-TEMPLATE]"

### 5.4 Interest Selection Illustration Set

**Prompt:** "A set of 5 small flat illustration cards for an onboarding interest-selection screen, each representing a content category: (1) Stories — a small glowing open storybook with soft light rays, (2) Quran — a small glowing crescent-and-star over a soft geometric pattern, (3) Duas — a pair of soft abstract cupped-hand shapes with a small glow between them, (4) Games — a small glowing puzzle-piece shape, (5) Habits — a small glowing calendar-checkmark shape. Consistent warm color palette per card, flat vector style, transparent backgrounds, arranged in a grid. [ILLUSTRATION-TEMPLATE]"

### 5.5 Learning Level Selection Illustration

**Prompt:** "A simple three-step flat illustration set representing learning levels for a children's app: (1) Beginner — a small single glowing sprout/seedling shape, (2) Intermediate — a small glowing sapling with two leaves, (3) Advanced — a small glowing full tree silhouette with a soft star at its top. Consistent warm gold-to-teal gradient progression across the three, flat vector style, transparent backgrounds. [ILLUSTRATION-TEMPLATE]"

### 5.6 Personalized Path Reveal / First Mission Hero

**Prompt:** "A celebratory, warm hero illustration for an onboarding 'your journey begins' reveal screen. The Noor companion character (from §2.1, joyful pose) floats above a softly-illuminated winding path made of small glowing stepping-stones leading into the distance, with soft golden light rays radiating from the top of the frame. Warm, hopeful, exciting-but-calm mood, generous open space at the bottom third for UI text/button overlay. [ILLUSTRATION-TEMPLATE], portrait orientation."

### 5.7 Onboarding Empty/Error States

**Prompt (OTP resend/error):** "A small, gentle flat illustration for an OTP-verification-failed state: a simple glowing envelope shape with a small soft question-mark accent, warm and non-alarming (never a harsh red error graphic), teal and gold palette. [ILLUSTRATION-TEMPLATE]"

---

## 6. Home Dashboard (A.2)

### 6.1 Noor Daily Greeting Illustration Set

**Prompt:** "A set of 4 time-of-day variants of the Noor companion character greeting the child on a home-screen widget: (1) morning — Noor glowing softly against a warm sunrise-gradient backdrop with a small sun accent, (2) midday — Noor glowing brightly against a clear warm-teal sky, (3) evening — Noor glowing warmly against a dusky purple-to-gold gradient, (4) bedtime — Noor dimmed and calm against a deep teal starry-night backdrop. Consistent character design across all 4 per §2.1, transparent character with separate background gradients. [ILLUSTRATION-TEMPLATE]"

### 6.2 "Continue Learning" Card Illustration

**Prompt:** "A small flat illustration icon for a 'continue where you left off' card: a glowing bookmark-ribbon shape draped over a small stack of abstract book/lesson shapes, warm gold accent, transparent background. [ICON-TEMPLATE]"

### 6.3 Daily Mission Widget Icon

**Prompt:** "A small flat icon for a daily-mission widget: a rounded scroll/checklist shape with a single glowing star accent in the corner, warm teal and gold, transparent background. [ICON-TEMPLATE]"

### 6.4 Empty State — First Day / No Activity Yet

**Prompt:** "A warm, encouraging flat illustration for a brand-new user's empty home-feed state. The Noor companion character floats beside a single small glowing seedling/sprout shape emerging from soft ground, with a few gentle sparkles nearby, suggesting 'your journey is just beginning' rather than emptiness. Warm cream background, generous padding for overlay text. [ILLUSTRATION-TEMPLATE]"

### 6.5 Offline State Illustration

**Prompt:** "A calm, non-alarming flat illustration for an offline-mode banner: a small soft cloud shape with a single gentle disconnect-slash accent, paired with the Noor companion in a calm/patient pose nearby, muted teal-grey palette (not alarming red), transparent background. [ILLUSTRATION-TEMPLATE]"

---

## 7. Stories Module (A.3)

> **Reminder: apply the §1.4 religious-content guardrail to every prompt in this section.**

### 7.1 Story Category Icons

**Prompt:** "A set of 6 flat category icons for a children's story library: (1) Prophet Stories — a small glowing lantern with a soft light-ray burst (symbolic, non-figurative), (2) Bedtime Stories — a small crescent moon with a soft sleepy glow, (3) Islamic Manners — a small glowing heart-in-hand-shape (abstract cupped shape, non-realistic hand), (4) Seasonal Stories — a small glowing star-and-crescent with a soft festive sparkle, (5) Animated Series — a small glowing filmstrip/play-button hybrid shape, (6) Short Stories — a small glowing single-page shape with a soft folded corner. Consistent warm palette, flat vector style, transparent backgrounds, arranged in a grid. [ICON-TEMPLATE]"

### 7.2 Story Library Cover Art Style Guide (representative set)

**Prompt:** "A set of 4 representative animated-story cover-art illustrations for a children's Islamic app's story library, each in a consistent premium Pixar-adjacent-but-2D-flat illustration style, NO human figures depicted for any Prophet-related cover (use symbolic scenery/light/architecture only per the guardrail): (1) a warm desert-oasis scene at sunset with a small mosque-lantern silhouette, (2) a calm starry night scene with a crescent moon and a soft sleeping-animal silhouette (a gentle sheep shape) for a bedtime story, (3) a cheerful daytime scene with two friendly abstract child-blob characters (non-realistic, rounded, no facial detail beyond simple glow-based expression) sharing a small gift, representing an Islamic-manners story, (4) a festive Eid-lantern-filled night scene for a seasonal story. Consistent warm gold/teal palette and soft lighting across all 4, portrait 2:3 cover-art aspect ratio. [ILLUSTRATION-TEMPLATE]"

### 7.3 Interactive Choice Overlay Icons

**Prompt:** "A pair of simple flat icons for an in-story 'choose your response' moment: two small glowing path-fork shapes, one leaning gently upward (the kind/wise choice, warm gold) and one leaning gently sideways (the alternative choice, soft muted teal — never a 'bad'-looking or scary icon, since the wrong choice should feel like a gentle learning moment, not a punishment). Transparent background. [ICON-TEMPLATE]"

### 7.4 Story Completion / Moral Summary Illustration

**Prompt:** "A warm, gentle celebratory flat illustration for a story-completion screen: the Noor companion (joyful pose) floats beside a small glowing scroll shape unrolling to reveal a simple, symbolic moral-lesson icon (e.g., a small heart-and-star combination), with soft confetti-like light-sparkle accents (never loud/flashing). Warm cream-to-gold gradient background. [ILLUSTRATION-TEMPLATE]"

### 7.5 Achievement Unlock Modal Illustration

**Prompt:** "A celebratory flat illustration for a badge/achievement unlock modal within the Stories feature: a glowing badge medallion (warm gold, with a small crescent-and-star engraving) bursts gently outward with soft light rays and small sparkle particles, the Noor companion peeking in from one side in a proud pose. Warm, joyful but calm (non-startling) mood, transparent background. [ILLUSTRATION-TEMPLATE]"

### 7.6 Offline Downloads Manager Illustration

**Prompt:** "A simple flat illustration for a story-downloads-manager empty state: a small glowing downward-arrow-into-tray icon paired with a small stack of abstract book shapes, warm teal accent, transparent background. [ICON-TEMPLATE]"

---

## 8. Bedtime Audio Player (A.4)

### 8.1 Bedtime Mode Background

**Prompt:** "A calm, dimmed, full-screen background illustration for a bedtime audio-story player. Deep muted teal-to-near-black gradient night sky, very soft scattered stars, a large soft crescent moon glowing gently in the upper third, and a subtle silhouette of a cozy rooftop/window scene along the bottom edge suggesting a child's bedroom at night. Extremely calm, low-contrast, reduced-visual-stimulation mood suitable for a pre-sleep UI. [ILLUSTRATION-TEMPLATE], portrait full-bleed."

### 8.2 Sleep Timer Icon

**Prompt:** "A simple flat icon combining a soft crescent moon shape with a small clock-hand accent, warm muted teal, transparent background, conveying 'sleep timer.' [ICON-TEMPLATE]"

### 8.3 Audio Waveform Visualizer (calm variant)

**Prompt:** "A soft, slow, gently-undulating audio waveform graphic in muted warm gold, rendered as smooth rounded bars rather than sharp spikes, suggesting calm narration rather than energetic music. Transparent background, horizontal strip composition. [ILLUSTRATION-TEMPLATE]"

---

## 9. Quran & Arabic Learning (A.5)

### 9.1 Surah Map / Curriculum Path Illustration

**Prompt:** "A gentle, warm illustrated path/map background for a Quran-learning curriculum screen: a softly winding path of small glowing nodes (each a simple circular waypoint) moving across a warm cream-and-gold landscape with subtle geometric Islamic-pattern accents in the background at low opacity. Some nodes glow (unlocked/completed), some are soft and dim (locked, not punitive-looking). [ILLUSTRATION-TEMPLATE], suitable as a scrollable vertical background."

### 9.2 Arabic Letter Learning Cards

**Prompt:** "A set of 3 representative flat illustration cards for Arabic-letter learning, each showing one large stylized Arabic letter shape in warm gold with a small matching object illustration beside it for association (e.g., a letter paired with a small glowing star, a small glowing moon, a small glowing book), soft cream card background, rounded corners. [ILLUSTRATION-TEMPLATE]"

### 9.3 Pronunciation Coaching / Microphone State Icons

**Prompt:** "A set of 4 states for a voice-recording pronunciation-practice interface: (1) idle/ready — a simple outlined microphone icon in muted teal, (2) actively listening — the same microphone filled warm gold with a soft pulsing glow ring around it, (3) processing/checking — the microphone icon with a small soft spinning-dots accent, (4) listen-only fallback (mic denied/unavailable) — a simple speaker/headphone icon replacing the microphone, muted teal. Consistent icon proportions across all 4, transparent backgrounds. [ICON-TEMPLATE]"

### 9.4 Tajweed Rule Highlight Accent

**Prompt:** "A small, soft underline/highlight accent graphic used to mark Arabic text with a specific Tajweed rule — a gentle rounded-rectangle highlight in a soft warm color (not harsh), with a tiny corner icon indicating rule type (e.g., a small elongation-arrow icon for madd rules). Flat, minimal, transparent background. [ICON-TEMPLATE]"

### 9.5 Mastery State Icons (six-state skill model, shared with A.9)

**Prompt:** "A set of 6 small flat icons representing skill-mastery states for a children's learning app: (1) Locked — a small closed padlock, muted grey, (2) Ready — a small open, glowing outline circle, soft teal, (3) Learning — a small circle filled one-quarter with warm gold, (4) Practicing — a small circle filled half with warm gold, (5) Mastered — a small circle fully filled with warm gold plus a tiny star accent, (6) Needs Refresh — a small circle mostly filled but with a soft gentle 'refresh' swirl accent overlaid (never looking like a warning or failure). Consistent circular base shape across all 6, transparent backgrounds. [ICON-TEMPLATE]"

---

## 10. Dua Learning (A.6)

### 10.1 Dua Category Icons

**Prompt:** "A set of 5 flat icons for dua categories: (1) Morning duas — a small glowing sunrise shape, (2) Evening duas — a small glowing sunset shape, (3) Mealtime duas — a small glowing simple bowl/plate shape, (4) Travel duas — a small glowing pathway/road shape, (5) Sleep duas — a small glowing crescent moon with a soft closed-eye-like curve (abstract, non-facial). Warm gold and teal palette, transparent backgrounds. [ICON-TEMPLATE]"

### 10.2 Dua Card Illustration

**Prompt:** "A warm flat card-background illustration for a dua-learning screen: a soft pair of abstract cupped-hand shapes (non-realistic, simplified rounded forms, never depicting real human hands in detail) rising gently with a small warm glow rising from between them, symbolizing supplication. Cream card background, generous padding for Arabic/transliteration text overlay. [ILLUSTRATION-TEMPLATE]"

### 10.3 Dua Learned / Recall Success Illustration

**Prompt:** "A small celebratory flat illustration for marking a dua as learned: a small glowing checkmark inside a soft heart-outline shape, with a tiny sparkle accent, warm gold, transparent background. [ICON-TEMPLATE]"

---

## 11. Habit Tracker (A.7)

### 11.1 Habit Type Icons

**Prompt:** "A set of 7 flat icons for Islamic habit types: (1) Salah — a small glowing simple mosque-dome silhouette, (2) Quran Reading — a small glowing open-book shape, (3) Daily Dua — a small glowing cupped-hands shape (abstract), (4) Good Deeds — a small glowing heart shape, (5) Fasting — a small glowing crescent-and-sun combination, (6) Dhikr — a small glowing prayer-beads loop shape (simplified circular beads, no religious text inscribed), (7) Charity/Kindness — a small glowing gift-in-hand abstract shape. Consistent warm palette, flat vector style, transparent backgrounds, arranged in a grid. [ICON-TEMPLATE]"

### 11.2 Streak Flame Icon (states)

**Prompt:** "A set of 4 states of a streak-flame icon for a children's app: (1) no streak — a small soft grey outlined flame shape, (2) active streak — a warm gold-to-orange gradient flame with a soft glow, (3) at-risk streak — the same warm flame but with a gentle pulsing soft amber ring around it (never a harsh red warning), (4) protected/grace streak — the flame with a small soft shield accent overlaid. Consistent flame silhouette across all 4, transparent backgrounds. [ICON-TEMPLATE]"

### 11.3 Habit Streak Calendar Illustration

**Prompt:** "A simple, warm flat calendar-grid background illustration for a habit-streak-history screen: a soft cream grid of rounded day-cells, some filled with a small warm gold glow dot (completed), some empty/soft outline only (not completed, never styled as a failure/red X). Clean, minimal, non-punitive visual language. [ILLUSTRATION-TEMPLATE]"

### 11.4 Family Garden Illustration (no-sibling-comparison aggregate view)

**Prompt:** "A warm, whimsical flat illustration of a small glowing garden — a few soft rounded plant/flower shapes of varying heights growing together from one shared warm-lit soil bed, each plant glowing gently, representing a family's combined habit progress without any individual labeling or ranking between the plants. Warm gold and green-teal palette, cream background. [ILLUSTRATION-TEMPLATE]"

---

## 12. Daily Quiz Engine (A.8)

### 12.1 Quiz Question-Type Icons

**Prompt:** "A set of 5 flat icons representing quiz question types: (1) multiple choice — a small stack of 3 rounded option-bubbles, (2) true/false — a small checkmark and X paired gently side by side (the X in soft muted grey, never harsh red, since wrong answers aren't shamed), (3) fill-in-the-blank — a small underline-with-cursor shape, (4) matching — two small connected-dot shapes linked by a soft curved line, (5) ordering — three small stacked horizontal bars of varying length. Warm teal/gold palette, transparent backgrounds. [ICON-TEMPLATE]"

### 12.2 Quiz Result Illustrations

**Prompt:** "A set of 2 warm, non-judgmental flat illustrations for quiz-completion states: (1) 'strengths' — the Noor companion glowing brightly beside a small stack of glowing stars, (2) 'next step suggestion' — the Noor companion in a gentle coaching pose beside a single glowing pathway-arrow pointing forward. Both illustrations avoid any 'grade' or percentage-score visual motif, emphasizing encouragement and forward progress instead. [ILLUSTRATION-TEMPLATE]"

---

## 13. Skill Tree / Mastery (A.9)

### 13.1 Skill Tree Background

**Prompt:** "A warm, organic flat illustration of a glowing skill-tree structure: a soft stylized tree silhouette in warm gold with several small glowing node-circles positioned along its branches at different heights, some nodes bright/mastered, some dim/locked, using the same six-state icon language as §9.5. Cream background, vertical scrollable composition. [ILLUSTRATION-TEMPLATE]"

### 13.2 Level Badge Icons (Noor Levels, canonical named tiers)

**Prompt:** "A set of 5 flat badge icons representing sequential mastery levels for a children's Islamic app, each a circular medallion with a distinct symbol and increasingly rich glow: (1) 'Seedling' — a small simple sprout icon, soft green-gold, gentle glow, (2) 'Sprout' — a slightly fuller two-leaf sprout icon, warm gold, (3) 'Star Seeker' — a glowing star icon, warm gold with sparkle accents, (4) 'Noor Guardian' — a glowing lantern-and-shield combination icon, richer gold-teal gradient, (5) 'Hafiz Hero' — a glowing crown-and-star combination icon, the richest gold gradient with a soft radiant halo. Progressive visual richness across the 5 tiers, consistent circular medallion base, transparent backgrounds. [ICON-TEMPLATE]"

---

## 14. Games Module (A.10)

### 14.1 Game Type Icons

**Prompt:** "A set of 4 flat icons for educational mini-game types: (1) Letter-matching game — a small glowing puzzle-piece shape with a soft Arabic-letter-like squiggle accent, (2) Word-building game — a small stack of glowing letter-block shapes, (3) Memory/matching-pairs game — two small glowing overlapping card shapes, (4) Sorting game — three small glowing basket/bucket shapes of different colors. Warm playful palette, flat vector style, transparent backgrounds. [ICON-TEMPLATE]"

### 14.2 Games Hub Hero Illustration

**Prompt:** "A cheerful, playful flat hero illustration for a games-hub landing screen: the Noor companion (joyful pose) surrounded by small floating glowing game-related shapes (a puzzle piece, a star, a small die shape without realistic pips, a small trophy), warm gold and teal palette, generous open space for a header title overlay. [ILLUSTRATION-TEMPLATE]"

---

## 15. Rewards System (A.11)

### 15.1 Named Badge Icon Set (canonical badges referenced in product documentation)

**Prompt:** "A set of 8 circular flat badge-medallion icons for a children's Islamic learning app's achievement collection, each with a distinct symbol on a warm gold or teal medallion base: (1) 'First Story' — a small glowing open-book icon, teal medallion, (2) '7-Day Streak' — a small glowing flame icon, gold medallion, (3) 'Quran Starter' — a small glowing crescent-and-page icon, purple medallion, (4) 'Dua Master' — a small glowing cupped-hands icon, teal medallion, (5) 'Quiz Champion' — a small glowing star-with-checkmark icon, gold medallion, (6) 'Salah Hero' — a small glowing mosque-dome icon, purple medallion, (7) 'Story Lover' — a small glowing stack-of-books icon, teal medallion, (8) 'Ramadan Star' — a small glowing crescent-and-lantern icon, gold medallion. Consistent medallion shape/size across all 8, subtle ribbon accent at the base of each, transparent backgrounds, arranged in a grid. [ICON-TEMPLATE]"

### 15.2 Rewards Wallet Illustration

**Prompt:** "A warm, tidy flat illustration for a rewards-wallet dashboard header: a glowing XP progress-ring shape beside a separate glowing gold-coin stack representing 'Noor Heroes Points,' with a few small sparkle accents, cream-to-gold gradient background band. [ILLUSTRATION-TEMPLATE]"

### 15.3 Noor Heroes Points Coin Icon

**Prompt:** "A simple flat icon of a single glowing gold coin with a small crescent-and-star engraving at its center, soft warm gradient, subtle rim highlight, transparent background — the app's virtual-currency icon, used throughout the rewards economy. [ICON-TEMPLATE]"

### 15.4 Weekly Challenge / Seasonal Event Card Illustrations

**Prompt:** "A set of 2 flat card-background illustrations: (1) Weekly Challenge — a small glowing checkered-flag-free 'goal flag' alternative shape (a simple glowing pennant/banner shape, avoiding a competitive racing motif) with a small progress-bar accent beneath, (2) Seasonal Event — a small glowing festive lantern cluster. Warm gold palette, cream card backgrounds, rounded corners. [ILLUSTRATION-TEMPLATE]"

### 15.5 Achievement Store Item Card Frames

**Prompt:** "A set of 2 flat item-card frame illustrations for an in-app achievement store: (1) an 'owned' item frame — a soft warm gold rounded-rectangle border with a small checkmark corner badge, (2) a 'locked, needs criteria' item frame — the same rounded-rectangle border desaturated to a soft grey silhouette style with a small lock corner badge and space beneath for unlock-criteria text. Transparent centers for item-icon insertion. [ICON-TEMPLATE]"

### 15.6 Reward Unlock Animation Keyframes

**Prompt:** "A 4-frame keyframe sequence illustration for a reward-unlock celebration animation: frame 1 — a small closed glowing box/chest shape, frame 2 — the box beginning to crack open with a soft light leak, frame 3 — warm gold light bursting outward gently with soft sparkle particles, frame 4 — the revealed reward item (a generic glowing badge shape) settling with a soft residual glow. Consistent warm gold palette across all 4 frames, transparent backgrounds, suitable for a Lottie/After-Effects-style animation reference. [ILLUSTRATION-TEMPLATE]"

---

## 16. Avatar System (A.12)

*(Base avatars and customization items already covered in §4.1/§4.2. Additional A.12-specific assets below.)*

### 16.1 Avatar Preview Stage Backdrop

**Prompt:** "A simple, elegant circular staging platform illustration for an avatar-preview screen: a soft glowing circular platform in warm cream-gold with subtle radial light rays emanating upward, designed for an avatar character to be composited on top of in Figma. Transparent background outside the circular glow. [ILLUSTRATION-TEMPLATE]"

### 16.2 Character Evolution Milestone Illustration

**Prompt:** "A gentle, magical flat illustration for a character-evolution milestone reveal: a soft abstract companion creature shown mid-transformation with a warm golden-light particle bloom radiating outward, suggesting graceful growth rather than a sudden power-up. Calm-but-joyful mood, warm gold-to-teal gradient background. [ILLUSTRATION-TEMPLATE]"

---

## 17. Search (B.13)

### 17.1 Search Empty State Illustration

**Prompt:** "A warm, friendly flat illustration for a zero-search-results state: the Noor companion holding a small glowing magnifying-glass shape, looking (via soft glow direction, not a face) toward a small empty glowing pathway, suggesting 'let's look somewhere else' rather than failure. Cream background, generous padding. [ILLUSTRATION-TEMPLATE]"

### 17.2 Voice Search Waveform Icon

**Prompt:** "A small flat icon combining a microphone shape with 3 soft radiating sound-wave arcs, warm gold, transparent background, suitable for a voice-search entry point. [ICON-TEMPLATE]"

---

## 18. Favorites (B.14)

### 18.1 Favorites Empty State Illustration

**Prompt:** "A warm, inviting flat illustration for an empty favorites list: a single soft outlined heart shape (not yet filled) with a small glowing sparkle nearby, and the Noor companion gesturing gently toward it, suggesting 'tap the heart on something you love.' Cream background. [ILLUSTRATION-TEMPLATE]"

---

## 19. Offline Downloads (B.15)

### 19.1 Download Status Icon Set

**Prompt:** "A set of 4 flat icons representing download states: (1) in-progress — a small circular progress-ring (partial fill) around a downward arrow, warm teal, (2) complete — a small downward-arrow-into-tray shape with a checkmark, warm gold, (3) failed — a small downward-arrow-into-tray shape with a soft gentle retry-swirl accent (never an alarming red X), muted amber, (4) storage-full — a small tray shape shown 'full' with a soft gentle overflow-wave accent, muted amber. Transparent backgrounds. [ICON-TEMPLATE]"

### 19.2 Storage Used Progress Bar Illustration

**Prompt:** "A simple flat horizontal progress-bar illustration for a storage-usage indicator: a soft rounded track in cream-dark, partially filled with a warm teal gradient bar, subtle rounded end caps. Transparent background, horizontal strip composition. [ICON-TEMPLATE]"

---

## 20. Child Profile (B.16)

### 20.1 Profile Stats Summary Card Icons

**Prompt:** "A set of 3 small flat icons for a profile stats-summary card: (1) XP level — a small glowing progress-ring with a number-placeholder center, (2) streak count — a small glowing flame with a number-placeholder beside it, (3) badge count — a small glowing medal shape with a number-placeholder beside it. Consistent warm gold palette, transparent backgrounds. [ICON-TEMPLATE]"

### 20.2 Switch Profile Lock Icon

**Prompt:** "A small flat icon combining a simple rounded padlock shape with a subtle 'switch/swap' arrow accent, muted teal (formal, parent-mode-adjacent tone, distinct from the playful child-mode icon set), transparent background. [ICON-TEMPLATE]"

---

## 21. Notifications — Child (B.17)

### 21.1 In-App Notification Banner Icon

**Prompt:** "A small flat icon of a glowing star inside a soft rounded notification-bell outline, warm gold, transparent background, for an in-app 'new content ready' banner. [ICON-TEMPLATE]"

### 21.2 Push Notification Small Icon (status-bar, monochrome — see also the App Icon spec doc for exact Android sizing)

**Prompt:** "A simple, pure white flat silhouette of a crescent moon cradling a small star, no gradients, no color, no glow effects — a single flat white shape only, transparent background, designed for Android status-bar notification-icon auto-tinting. [ICON-TEMPLATE]"

---

## 22. Islamic Facts (B.18)

### 22.1 Fact-of-the-Day Card Illustration

**Prompt:** "A calm, elegant flat card-background illustration for a daily Islamic-fact widget: a small glowing lightbulb-shaped motif re-imagined as a soft crescent-moon-and-spark combination (avoiding the generic lightbulb cliché while keeping the 'idea/fact' association), warm gold accent, cream card background. [ILLUSTRATION-TEMPLATE]"

### 22.2 Scholar-Approved Badge Icon

**Prompt:** "A small flat trust-badge icon: a soft rounded checkmark-in-shield shape with a tiny book accent, warm teal, transparent background, conveying 'scholar-reviewed content' — reused across Facts, Duas, and Story detail screens wherever a source-verification indicator is needed. [ICON-TEMPLATE]"

---

## 23. Parent Area (C.19–C.26)

> Parent-mode assets use the calmer, denser, more premium register per §1.2 — muted accent application, more whitespace discipline, less glow/sparkle than child-mode assets.

### 23.1 Who Is Learning — Profile Picker Tile Frames

**Prompt:** "A set of 2 flat tile-frame illustrations for a profile-selection screen: (1) a child-profile tile frame — a warm rounded-square card frame with a small lock-icon overlay corner badge (indicating a configured lock), (2) a parent-profile tile frame — a slightly more formal rounded-square card frame with a small padlock badge, styled with a subtly more muted, premium palette than the child tile. Transparent centers for avatar-image insertion. [ICON-TEMPLATE]"

### 23.2 Parent Dashboard Widget Icons

**Prompt:** "A set of 5 small flat icons for Parent Dashboard widget headers, styled in the calmer parent-mode register (muted teal/gold, minimal glow): (1) Weekly Report — a small document-with-chart-line icon, (2) Activity Timeline — a small clock-with-dots icon, (3) Screen Time — a small horizontal-bar-gauge icon, (4) Module shortcuts (Children/Reports/Settings/Subscription/Support) — five minimal line icons: a people-outline, a chart-outline, a gear-outline, a card-outline, a headset-outline. Consistent muted parent-mode palette, transparent backgrounds. [ICON-TEMPLATE]"

### 23.3 Calm Rest Screen Illustration (Screen-Time Limit)

**Prompt:** "A warm, celebratory-but-calm flat illustration for a screen-time-limit-reached rest screen: a softly glowing crescent moon and a few gentle stars over a small cozy reading-nook silhouette, the Noor companion in a calm/sleepy pose nearby. No countdown timer, no red coloring, no lock icon — the mood should read as 'time to rest' rather than 'you are blocked.' [ILLUSTRATION-TEMPLATE]"

### 23.4 Bedtime Block Screen Illustration

**Prompt:** "A calm flat illustration for a bedtime-window session-block screen: a deep teal night sky with a large soft glowing crescent moon, the Noor companion dimmed and resting, and a small 'ask a grown-up' text-link space reserved beneath. Extremely calm, low-stimulation mood. [ILLUSTRATION-TEMPLATE]"

### 23.5 Consent Log Status Icons

**Prompt:** "A pair of small flat status-pill icons for a consent-management screen: (1) 'Granted' — a small filled teal checkmark pill, (2) 'Withdrawn' — a small muted grey outline pill. Minimal, formal parent-mode styling, transparent backgrounds. [ICON-TEMPLATE]"

### 23.6 AI Interaction History / Safety Log Icons

**Prompt:** "A set of 3 small, deliberately plain and non-chat-like flat icons for an AI-safety-log list, each a simple neutral shape (never chat-bubble-shaped, to avoid resembling a conversation UI): (1) 'Allowed' — a small checkmark-in-circle, muted teal, (2) 'Blocked' — a small shield-outline icon, muted amber (never alarming red), (3) 'Redirected' — a small gentle curved-arrow icon, muted gold. Minimal, formal, transparent backgrounds. [ICON-TEMPLATE]"

### 23.7 Subscription Plan Card Illustrations

**Prompt:** "A set of 3 flat plan-tier card-header illustrations for a subscription-comparison screen: (1) Free plan — a simple soft outlined star, muted grey-gold, (2) Mobile Family plan — a filled warm gold star with a subtle glow, (3) Premium Family plan — a filled warm gold star with a richer glow and a small crown accent above it. Consistent star-based visual hierarchy communicating tier progression, transparent backgrounds. [ICON-TEMPLATE]"

### 23.8 Deletion Warning Illustration

**Prompt:** "A serious-but-calm (never alarmist) flat illustration for an account/profile deletion warning screen: a single weighty rounded-triangle warning outline (not aggressive red, a muted warm amber-brown), centered, with generous surrounding whitespace. No flashing elements, no skull/danger iconography — calm gravity, not panic. [ILLUSTRATION-TEMPLATE]"

### 23.9 Data Export / Privacy Illustration

**Prompt:** "A calm, trustworthy flat illustration for a data-export request screen: a small glowing folder/document stack shape with a soft downward-arrow accent, muted teal, formal parent-mode styling, transparent background. [ILLUSTRATION-TEMPLATE]"

---

## 24. Parent Web Account Portal (D.27)

### 24.1 Web Portal Section Icons

**Prompt:** "A set of 7 flat sidebar-navigation icons for a desktop web account-management portal, styled in a clean, minimal, professional-but-warm register (slightly more formal than the mobile parent-mode icons, suitable for a web SaaS sidebar): Account & Security (a shield-outline), Devices (a simple device-stack outline), Subscription (a card outline), Consent & Privacy (a checkmark-shield outline), Data Export (a folder-arrow outline), Account Deletion (a muted trash-outline, deliberately unalarming), Support (a headset outline). Consistent line weight, muted teal/grey palette, transparent backgrounds. [ICON-TEMPLATE]"

### 24.2 Deletion Status Countdown Illustration

**Prompt:** "A calm, serious flat illustration for a web-based account-deletion countdown page: a simple large circular countdown-ring graphic (no specific number baked in — leave for text overlay) in a muted warm amber-brown, with generous surrounding whitespace, professional web-portal aesthetic. [ILLUSTRATION-TEMPLATE]"

---

## 25. Admin & Scholar Portal (E.28–E.34)

> **Distinct visual register:** cool neutral grey-white backgrounds, sharp or minimally-rounded corners, muted blue-grey accent color (not the child app's warm teal/gold), dense information-first aesthetic. This is a professional internal tool, not a consumer product — do not reuse child-mode warmth here except where explicitly noted (e.g., a single red accent for the kill-switch severity treatment).

### 25.1 Admin Navigation Group Icons

**Prompt:** "A set of 8 flat sidebar-navigation icons for an internal admin-portal tool, dense professional SaaS aesthetic, muted blue-grey (#5B7A99-ish) line-icon style, sharp minimal corners: Operate (a simple dashboard-grid icon), Users (a people-outline icon), Content (a document-stack icon), Review (a checklist-with-magnifier icon), Engagement (a spark/star-outline icon), Commerce (a card-outline icon), Intelligence (a brain/chart-hybrid outline icon), Platform (a gear-and-globe outline icon). Consistent line weight, cool neutral palette, transparent backgrounds. [ICON-TEMPLATE]"

### 25.2 Operations Dashboard Widget Icons

**Prompt:** "A set of 8 small flat status-widget icons for an admin operations dashboard, matching the cool professional register: Active Families (people-outline), Content Completions (checkmark-document), Content Awaiting Review (clock-document), Safety Alerts (shield-alert outline, muted amber not bright red), Subscription Health (heartbeat-line-in-card), Notification Performance (bell-with-chart), AI Refusal Rate (shield-with-percentage-symbol outline), Failed Jobs (gear-with-alert outline). Consistent muted blue-grey palette with a single muted-amber accent reserved for alert-type icons, transparent backgrounds. [ICON-TEMPLATE]"

### 25.3 Review Status Pills (Content CMS / Scholar Review)

**Prompt:** "A set of 7 small flat status-pill badges for a content-review-workflow list, professional admin aesthetic: Draft (grey outline), Editorial Review (muted blue fill), Scholar Review (muted purple fill), Child-Safety Review (muted teal fill), Scheduled (muted gold outline), Published (solid muted green), Suspended (solid muted amber, never bright alarm-red — this is an internal status indicator, not a public alert). Consistent pill shape, small text-label space reserved inside each. [ICON-TEMPLATE]"

### 25.4 Segregation-of-Duties Lock Icon

**Prompt:** "A small flat icon combining a checkmark and a padlock, muted blue-grey, indicating a 'you cannot approve your own edit' disabled-state tooltip context in an admin review tool. Transparent background. [ICON-TEMPLATE]"

### 25.5 Kill Switch Severity Icon (the one deliberate red exception)

**Prompt:** "A single, deliberately high-severity flat icon for an emergency AI-feature kill-switch confirmation: a bold rounded-triangle warning outline in a clear, serious red (#C0392B), thicker stroke weight than any other admin icon in this set, reserved exclusively for this one action given its severity class. Transparent background. [ICON-TEMPLATE]"

### 25.6 Masked/Unmasked PII Field Icons

**Prompt:** "A pair of small flat icons for a PII-masking admin interface: (1) masked-field indicator — a small closed-padlock-with-dots icon, muted grey, (2) unmask-active indicator — a small open-padlock-with-timer icon, muted amber (signaling a time-boxed exception state, not a normal/safe state). Transparent backgrounds. [ICON-TEMPLATE]"

### 25.7 Reconciliation Diff / Before-After Visual

**Prompt:** "A small flat before/after comparison chip graphic for a billing-reconciliation admin log: two small rounded status-pill shapes connected by a soft curved arrow, the first in muted grey (before-state) and the second in muted green (corrected after-state). Transparent background. [ICON-TEMPLATE]"

### 25.8 Comp-Grant Visual Distinctness Badge

**Prompt:** "A small flat badge icon reading conceptually as 'not real revenue' for a billing-history timeline: a soft rounded ribbon-tag shape in a distinct muted amber color (visually separate from the blue billing-event icons used elsewhere in the same timeline), with a small gift-box accent. Transparent background. [ICON-TEMPLATE]"

### 25.9 Localization Coverage Bar Graphic

**Prompt:** "A simple flat horizontal progress-bar illustration for a translation-coverage dashboard, in the cool admin palette: a muted grey-blue track, partially filled with a gradient from muted amber (low coverage) to muted green (full coverage), with a small vertical marker line indicating the activation threshold. Transparent background, horizontal strip. [ICON-TEMPLATE]"

### 25.10 RTL Preview Split-Screen Frame

**Prompt:** "A simple flat two-panel comparison frame graphic for an RTL-preview admin tool: two identical rounded mobile-screen-shaped outline frames side by side, one labeled conceptually 'LTR' with a small left-aligned line-accent inside, the other labeled 'RTL' with a small right-aligned mirrored line-accent inside. Cool professional palette, transparent background. [ILLUSTRATION-TEMPLATE]"

---

## 26. Ramadan Mode (F.36)

*(A dedicated seasonal theme overlay applied to Home, Stories, and Rewards — distinct Standard/Laylatul-Qadr/Eid registers.)*

### 26.1 Lantern Progress Path — Node States

**Prompt:** "A set of 4 lantern-icon states for a 30-night Ramadan journey map: (1) locked/upcoming — a small dim, unlit lantern outline, muted grey-teal (not punitive-looking), (2) current/tonight — a larger, gently pulsing warm-gold lit lantern with a soft glow ring, (3) completed — a warm gold lit lantern, steady glow, (4) Laylatul Qadr special night — the completed-lantern design plus a small crescent-moon badge overlay accent. Consistent lantern silhouette across all 4, transparent backgrounds. [ICON-TEMPLATE]"

### 26.2 Ramadan Home Theme Background

**Prompt:** "A full-screen warm Ramadan theme background overlay: a deep warm teal night sky with soft scattered stars, a large gentle crescent moon in the upper portion, and a subtle winding path of small glowing lantern-dots suggested along the lower two-thirds. Warm, magical, calm mood. [ILLUSTRATION-TEMPLATE], portrait full-bleed."

### 26.3 Laylatul Qadr Calm-Mode Overlay

**Prompt:** "A deliberately quieter, slower, less saturated variant of the Ramadan theme background: the same deep teal night-sky and crescent-moon motif as §26.2 but with muted saturation, softer/slower-feeling glow, no competitive badge call-outs anywhere in the composition, extra generous negative space suggesting stillness and reflection. [ILLUSTRATION-TEMPLATE]"

### 26.4 Eid Celebration Theme Background

**Prompt:** "A bright, joyful, warm Eid-celebration theme background overlay: a warm gold-and-soft-pastel gradient sky with gentle non-startling confetti-like sparkle accents, a large glowing sun-and-crescent combination motif in the upper portion. Bright but calm celebratory mood (no loud flashing, no realistic fireworks). [ILLUSTRATION-TEMPLATE], portrait full-bleed."

### 26.5 Ramadan Badge Set

**Prompt:** "A set of 4 seasonal circular badge-medallion icons: (1) 'Ramadan Star' — a glowing star-and-crescent medallion, warm gold, (2) 'Night of Power' — a richer glowing medallion with a soft radiant halo, deep gold-purple gradient, (3) 'Ramadan Champion' (30/30 nights) — the richest medallion design with a small crown accent, (4) 'Eid Joy' — a bright warm medallion with a small sun-burst accent. Consistent medallion base shared with the §15.1 badge set, transparent backgrounds. [ICON-TEMPLATE]"

### 26.6 Fasting Tracker Icon Set

**Prompt:** "A set of 3 flat icons for parent-configured fasting approaches: (1) Full Fast — a small glowing full crescent-and-sun icon, (2) Practice Fast — the same icon at half-glow/half-opacity, (3) Education Only — a small glowing open-book icon replacing the crescent-and-sun. Warm gold palette, transparent backgrounds. [ICON-TEMPLATE]"

### 26.7 Eid Card / Certificate Frame

**Prompt:** "An ornate-but-clean flat decorative frame illustration for an end-of-Ramadan shareable certificate/Eid card: a warm gold geometric Islamic-pattern border (eight-pointed star lattice motif) surrounding a generous empty cream-colored center reserved for text/child-name/achievement insertion, with a small crescent-and-lantern accent at the top center. Premium, celebratory, shareable-card aesthetic. [ILLUSTRATION-TEMPLATE], landscape card aspect ratio (e.g., 4:3)."

---

## 27. Global Empty / Loading / Error / Success State Library

*(A consistent, reusable library referenced by every feature above — build once, reuse everywhere a generic state is needed beyond the feature-specific ones already listed.)*

### 27.1 Generic Empty State

**Prompt:** "A warm, gentle flat illustration for a generic 'nothing here yet' empty state: the Noor companion in a calm, patient pose beside a single small soft outlined placeholder-shape (a simple dashed-outline rounded rectangle), suggesting anticipation rather than absence. Cream background, generous padding for overlay text. [ILLUSTRATION-TEMPLATE]"

### 27.2 Generic Loading State

**Prompt:** "A simple, calm flat loading-state illustration: the Noor companion in a gentle 'thinking/preparing' pose (a soft rhythmic glow-pulse implied via 3 sequential frames shown side by side) beside a few small floating sparkle particles. Cream background. [ILLUSTRATION-TEMPLATE]"

### 27.3 Generic Error State (non-alarming)

**Prompt:** "A calm, reassuring flat illustration for a generic error/something-went-wrong state: the Noor companion in a gentle, understanding pose (dimmed glow, not distressed) beside a small soft outlined exclamation-mark shape in muted amber (never bright red), with a small 'try again' arrow-loop accent nearby. Warm, non-alarming, cream background. [ILLUSTRATION-TEMPLATE]"

### 27.4 Generic Success State

**Prompt:** "A warm, joyful flat illustration for a generic success/completion state: the Noor companion glowing brightly in a celebrating pose beside a large soft glowing checkmark shape, with a few gentle sparkle accents. Warm gold-to-cream gradient background. [ILLUSTRATION-TEMPLATE]"

### 27.5 No-Connectivity / Offline State

**Prompt:** "A calm flat illustration for a no-internet-connection state: a small soft cloud-with-gentle-disconnect-slash icon beside the Noor companion in a patient, unbothered pose, muted teal-grey palette (not alarming), cream background. [ILLUSTRATION-TEMPLATE]"

### 27.6 Permission-Denied State (e.g., microphone)

**Prompt:** "A calm, understanding flat illustration for a permission-denied state (e.g., microphone access): a small soft outlined microphone-with-gentle-slash icon beside the Noor companion in a reassuring pose, suggesting 'that's okay, here's another way' rather than a dead end. Warm, non-punitive mood, cream background. [ILLUSTRATION-TEMPLATE]"

---

## 28. Marketing & App Store Assets

> App icon and Play Store feature graphic are fully specified in the companion file `NoorHeroes_App_Icon_Banner_Prompts_and_Specs.md` — reference that file rather than regenerating them here. Everything below is additional marketing collateral.

### 28.1 App Store Screenshot Decorative Frames

**Prompt:** "A set of 3 decorative background-frame templates for App Store/Play Store screenshot presentation, each a warm gradient backdrop with a device-mockup silhouette placeholder in the center and generous space above/below for a short marketing headline: (1) warm teal-to-gold gradient with soft stars, (2) warm cream-to-gold gradient with a subtle geometric pattern border, (3) deep teal night-sky gradient with the Noor companion floating in a corner. Consistent brand palette across all 3, portrait phone-screenshot aspect ratio (9:19.5) with the device-mockup area left as a clean placeholder. [HERO-BANNER-TEMPLATE]"

### 28.2 Social Media Post Templates

**Prompt:** "A set of 3 square (1:1) social-media post template backgrounds for a children's Islamic app's marketing account: (1) a warm teal gradient with a centered glowing crescent-and-star motif and generous text space below, (2) a warm gold gradient with a small illustrated story-open-book motif and generous text space, (3) a soft cream background with a subtle geometric border pattern and generous text space, all leaving the center-to-lower area open for a headline/quote overlay. [HERO-BANNER-TEMPLATE], 1:1 aspect ratio."

### 28.3 Blog / Content Header Banner

**Prompt:** "A wide (16:9) blog-header banner template: a warm, calm illustrated scene combining the Noor companion, a small stack of storybooks, and a soft crescent-moon-and-star motif, arranged along the left third, with generous open cream-colored space on the right two-thirds reserved for an article headline. [HERO-BANNER-TEMPLATE], 16:9 aspect ratio."

### 28.4 Onboarding Explainer Video Thumbnail

**Prompt:** "A warm, inviting video-thumbnail illustration: the Noor companion in a welcoming pose at the center, a soft play-button triangle overlay accent, warm gold-to-teal gradient background, bold empty space reserved near the top for a short title. [HERO-BANNER-TEMPLATE], 16:9 aspect ratio."

### 28.5 Parent Testimonial Card Background

**Prompt:** "A calm, premium flat card-background template for a parent testimonial/review quote graphic: a soft cream background with a subtle warm gold quotation-mark accent in one corner and a small trust-badge (checkmark-shield) accent in another corner, generous central space reserved for quote text and a small parent-name/rating line. Parent-mode premium aesthetic (calmer than child-mode marketing assets). [HERO-BANNER-TEMPLATE]"

### 28.6 Ramadan Seasonal Marketing Banner

**Prompt:** "A wide (16:9) seasonal marketing banner for a Ramadan-campaign promotion: a warm deep-teal night-sky background with a large glowing crescent moon, a winding lantern-lit path motif along the bottom, and generous open space in the upper-left for a campaign headline. Warm, magical, premium mood. [HERO-BANNER-TEMPLATE], 16:9 aspect ratio."

---

## 29. Seasonal Icon Re-Skins

*(Beyond Ramadan's dedicated §26, the product also supports Eid, Jummah, Muharram/Islamic New Year, and Dhul Hijjah campaign moments per the Seasonal Islamic Events feature set. Generate lightweight re-skin accent variants of the core icon library for each.)*

### 29.1 Jummah (Friday) Accent Pack

**Prompt:** "A small set of 3 seasonal accent overlays for Friday/Jummah-themed missions: a small glowing green-accented mosque-dome badge, a small glowing decorative corner flourish (abstract geometric, no readable text baked in), and a small soft green ribbon-tag shape. Warm-but-cooler-green-accented variant of the core palette, transparent backgrounds. [ICON-TEMPLATE]"

### 29.2 Islamic New Year / Muharram Accent Pack

**Prompt:** "A small set of 3 seasonal accent overlays for Islamic New Year content: a small glowing hijri-calendar-page icon, a small glowing new-crescent-rising motif, and a small soft deep-purple ribbon-tag shape. Reflective, calm-toned palette variant, transparent backgrounds. [ICON-TEMPLATE]"

### 29.3 Dhul Hijjah / Eid al-Adha Accent Pack

**Prompt:** "A small set of 3 seasonal accent overlays for Dhul Hijjah content: a small glowing mountain-silhouette-with-crescent icon (symbolic of the season, never depicting pilgrims or sacred sites' interior rites literally — keep purely symbolic/landscape), a small glowing charity/kindness heart-in-hand icon, and a small soft warm-brown ribbon-tag shape. Transparent backgrounds. [ICON-TEMPLATE]"

---

## 30. Master Asset Checklist

Use this as your Figma-file build tracker — check off each group as generated and imported.

- [ ] §1 Brand tokens applied as Figma color/text styles
- [ ] §2 App icon (see companion spec file), splash screen, Noor character sheet, wordmark, loading spinner
- [ ] §3 Bottom nav icon set (10 states), global action icon set (~60 icons + RTL mirrors), content-type badges
- [ ] §4 Avatar base library (6), avatar outfits/glow/accessories, symbolic story-character motif library
- [ ] §5–§26 Per-feature illustrations, empty states, and unique icons (22 feature sections)
- [ ] §27 Global empty/loading/error/success/offline/permission-denied illustration set (6 illustrations)
- [ ] §28 Marketing collateral: App Store screenshot frames, social templates, blog header, video thumbnail, testimonial card, Ramadan marketing banner
- [ ] §29 Seasonal accent packs: Jummah, Islamic New Year, Dhul Hijjah
- [ ] Cross-check every illustration referencing "Prophet" content against §1.4's guardrail before finalizing
- [ ] Cross-check every admin-portal asset against the cool professional palette (§25) — never child-mode warmth except the single kill-switch red exception
- [ ] Generate RTL-mirrored variants for all directional icons (back/forward arrows, chevrons, skip controls)
- [ ] Export icons as SVG where the generator/tracing tool allows, for crisp Figma component use at every size
