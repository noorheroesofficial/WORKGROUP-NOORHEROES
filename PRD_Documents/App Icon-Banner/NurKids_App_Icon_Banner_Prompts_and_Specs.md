> [!WARNING]
> **DEPRECATED / SUPERSEDED:** This file contains legacy branding ('NurKids') and is retained for historical archive purposes only. The authoritative, active brand asset specification is [NoorHeroes_App_Icon_Banner_Prompts_and_Specs.md](NoorHeroes_App_Icon_Banner_Prompts_and_Specs.md).

# NurKids — Android App Icon & Play Store Banner: Prompt Pack & Size Specification

**App:** NurKids — Islamic Learning App for Children
**Purpose:** A single reference package containing (1) ready-to-use AI image-generation prompts for the app icon and Play Store feature graphic, and (2) the complete, exact technical specification of every icon size/format Android and the Play Store actually require, so a designer or an image-generation tool can produce a fully compliant asset set in one pass.

> **Design language note:** These prompts follow the same visual system established throughout the NurKids product documentation — warm teal (#0F5E5E-ish deep teal) and gold accents, a crescent moon / lantern / star motif tied to the "Noor" (light) companion character, soft rounded shapes, no realistic human faces, calm and trustworthy rather than cartoonish-loud. The icon should be instantly recognizable at 48px and still feel intentional at 512px.

---

## 1. App Icon — Concept & Prompts

Android's modern icon system (API 26+) requires the icon as **two separate layers** — a **foreground** (the actual symbol/mark, transparent background) and a **background** (a solid or simple graphic that fills the canvas) — which the OS then composites and masks into circle/squircle/rounded-square/teardrop shapes depending on the device's launcher. You need both layers as *separate* prompts/files, not one flattened icon.

### 1.1 Foreground Layer Prompt

*(This is the symbol itself. Must be a simple, bold, single-focal-point mark — Android crops this to a shape and scales it down to 48px, so avoid fine detail, text, or anything near the edges.)*

**English:**
> "A simple, bold, flat vector app-icon mark for a children's Islamic learning app called NurKids. A single glowing crescent moon cradling a small five-pointed star, rendered as a soft rounded lantern-like shape, in warm gold (#F0B429-ish) on a transparent background. Minimalist, geometric, no fine detail, no text, no realistic human faces, no photographic elements — must read clearly as a small silhouette at 48x48 pixels. Centered with generous padding on all sides (at least 20% margin from every edge), soft subtle glow around the crescent, flat design suitable for Android adaptive icon masking, transparent PNG background."

**Arabic (RTL context note — icon itself has no directional text, included for asset-brief parity):**
> "علامة أيقونة تطبيق بسيطة وجريئة ومسطحة بأسلوب متجه لتطبيق تعليم إسلامي للأطفال يُدعى NurKids. هلال متوهج واحد يحتضن نجمة صغيرة خماسية، مُقدَّم على شكل فانوس ناعم مستدير الحواف، بلون ذهبي دافئ على خلفية شفافة. تصميم بسيط وهندسي، بدون تفاصيل دقيقة، بدون نص، بدون وجوه بشرية واقعية، بدون عناصر تصويرية — يجب أن يكون واضحًا كظل صغير عند 48×48 بكسل. متمركز مع هامش سخي من جميع الجهات (لا يقل عن 20% من كل حافة)، توهج خفيف حول الهلال، تصميم مسطح مناسب لقناع أيقونة Android التكيفية، خلفية PNG شفافة."

### 1.2 Background Layer Prompt

*(A simple fill/backdrop the foreground sits on top of. Android will crop this to the mask shape too, so keep any pattern subtle and centered.)*

**English:**
> "A simple, flat background layer for an Android adaptive app icon. A smooth radial gradient from deep warm teal (#0F5E5E) at the edges to a slightly lighter warm teal (#1B7A7A) at the center, evoking a calm night sky. Subtle, sparse small star-dot accents scattered softly near the corners only (nothing near the center, since the foreground symbol sits there). No text, no realistic imagery, perfectly flat and simple, full-bleed square canvas, no transparency."

**Arabic:**
> "طبقة خلفية بسيطة ومسطحة لأيقونة تطبيق Android التكيفية. تدرج شعاعي ناعم من فيروزي دافئ عميق عند الحواف إلى فيروزي دافئ أفتح قليلاً في المنتصف، يستحضر سماء ليلية هادئة. لمسات نجوم صغيرة ومتناثرة وخفيفة قرب الزوايا فقط (بدون أي شيء قرب المنتصف، حيث يوضع رمز الواجهة الأمامية). بدون نص، بدون صور واقعية، مسطحة وبسيطة تمامًا، لوحة مربعة كاملة بلا حواف، بدون شفافية."

### 1.3 Legacy / Combined Flat Icon Prompt

*(For older Android versions and the Play Store listing icon, which want one pre-composited square/circle image rather than two layers.)*

**English:**
> "A polished, flat, modern app icon for a children's Islamic learning app called NurKids, square canvas with rounded corners. Deep warm teal radial-gradient background evoking a calm night sky with a few soft small stars near the corners. Centered, a glowing warm-gold crescent moon cradling a small five-pointed star, styled like a gentle lantern, with a soft outer glow. Calm, trustworthy, premium children's-app aesthetic — not cartoonish, not overly playful, no realistic human faces, no text anywhere on the icon. Clean vector-flat shading, subtle soft shadow beneath the crescent for depth, generous padding from all edges."

**Arabic:**
> "أيقونة تطبيق مصقولة ومسطحة وحديثة لتطبيق تعليم إسلامي للأطفال يُدعى NurKids، بلوحة مربعة ذات زوايا مستديرة. خلفية بتدرج شعاعي فيروزي دافئ وعميق تستحضر سماء ليلية هادئة مع بضع نجوم صغيرة وناعمة قرب الزوايا. في المنتصف، هلال متوهج بذهبي دافئ يحتضن نجمة صغيرة خماسية، بأسلوب فانوس لطيف، مع توهج خارجي ناعم. طابع هادئ وموثوق وراقٍ لتطبيق أطفال — ليس كرتونيًا، وليس مفرط المرح، بدون وجوه بشرية واقعية، بدون أي نص على الأيقونة. تظليل متجه نظيف ومسطح، ظل ناعم وخفيف أسفل الهلال لإضافة العمق، هامش سخي من جميع الحواف."

---

## 2. Play Store Feature Graphic ("Banner") — Prompt

*(This is the wide banner shown at the top of your Play Store listing — text is allowed here, unlike the icon.)*

**English:**
> "A wide, horizontal Play Store feature-graphic banner for a children's Islamic learning app called NurKids, landscape orientation. Warm deep-teal night-sky gradient background with soft glowing stars, transitioning to a warm gold glow on one side. On the left third, a friendly abstract lantern/crescent-moon companion character (soft, rounded, non-human, glowing warm gold) floating gently beside a small stack of illustrated storybooks and a glowing Quran-like open-book icon. On the right two-thirds, bold, warm, rounded sans-serif text reading 'NurKids' in gold, with a smaller tagline beneath in white reading 'Islamic Learning, Made Joyful' (leave real tagline text editable/swappable). Soft particle glow throughout, calm and premium mood, no realistic human faces, no photographic elements, clean flat-illustration style suitable for a family education app."

**Arabic:**
> "لافتة عريضة أفقية لصفحة Google Play لتطبيق تعليم إسلامي للأطفال يُدعى NurKids، بتوجيه أفقي. خلفية متدرجة بسماء ليلية فيروزية دافئة وعميقة مع نجوم متوهجة ناعمة، تتحول إلى توهج ذهبي دافئ من جهة واحدة. في الثلث الأيمن، شخصية رفيق فانوس/هلال مجردة وودودة (ناعمة، مستديرة، غير بشرية، متوهجة بذهبي دافئ) تحلق بلطف بجانب كومة صغيرة من كتب القصص المصورة وأيقونة كتاب مفتوح متوهج يشبه المصحف. في الثلثين الأيسرين، نص عريض ودافئ ومستدير الخط يقول 'NurKids' بالذهبي، مع شعار فرعي أصغر أسفله باللون الأبيض يقول 'تعلم إسلامي، بفرح' (النص القابل للتبديل حسب اللغة). توهج جزيئات ناعم في كل مكان، طابع هادئ وراقٍ، بدون وجوه بشرية واقعية، بدون عناصر تصويرية، أسلوب رسم مسطح ونظيف مناسب لتطبيق تعليم عائلي."

---

## 3. Complete Android Icon Size Specification

Everything below is what Android/Play Store actually consume. Generate the **foreground** and **background** layers at the largest size (432×432 px) and let your build tooling (Android Studio's Image Asset Studio, or a script) auto-generate the smaller densities — this is strongly preferred over hand-exporting every size, since it guarantees pixel-perfect scaling and correct safe-zone alignment.

### 3.1 Adaptive Icon (Android 8.0 / API 26+) — REQUIRED, primary path

| Layer | Canvas size | Safe zone (content must stay inside) | Format |
|---|---|---|---|
| Foreground | 108×108 dp → **432×432 px** @ xxxhdpi | Inner **66×66 dp** (264×264 px) circle — the OS may crop anything outside this on some launcher masks | PNG, transparent background, or a vector drawable (`.xml`, preferred for crispness at all sizes) |
| Background | 108×108 dp → **432×432 px** @ xxxhdpi | Full bleed — no transparency, gets masked by the OS | PNG (no alpha) or vector drawable |
| Optional monochrome layer (Android 13+ themed icons) | Same as foreground | Same 66dp safe zone | PNG or vector, single-color silhouette only |

Output files needed in `res/mipmap-anydpi-v26/ic_launcher.xml` (adaptive icon XML referencing the two layers) plus the two drawables in `res/drawable/`.

### 3.2 Legacy Launcher Icon (pre-Android 8.0 fallback) — REQUIRED

Pre-composited flat square icon (use the "combined" prompt from §1.3), exported at each density:

| Density | Size (px) | Folder |
|---|---|---|
| mdpi | 48×48 | `mipmap-mdpi/ic_launcher.png` |
| hdpi | 72×72 | `mipmap-hdpi/ic_launcher.png` |
| xhdpi | 96×96 | `mipmap-xhdpi/ic_launcher.png` |
| xxhdpi | 144×144 | `mipmap-xxhdpi/ic_launcher.png` |
| xxxhdpi | 192×192 | `mipmap-xxxhdpi/ic_launcher.png` |

### 3.3 Legacy Round Icon (pre-Android 8.0, circular-launcher devices)

Same sizes as §3.2 above, pre-cropped to a circle, saved as `ic_launcher_round.png` in the same density folders.

### 3.4 Google Play Store Listing Icon — REQUIRED

| Asset | Size | Format |
|---|---|---|
| Store listing icon (App icon on Play Store) | **512×512 px** | 32-bit PNG with alpha channel, max 1MB |

### 3.5 Google Play Feature Graphic ("Banner") — REQUIRED

| Asset | Size | Format |
|---|---|---|
| Feature graphic | **1024×500 px** | PNG or JPEG, no alpha, max 15MB (keep well under — 1-2MB is typical) |

### 3.6 Notification Icon — REQUIRED for push notifications (B.17)

Android **requires** notification icons to be a **flat white/transparent silhouette only** (the OS tints it automatically) — a colored icon here will render as a solid grey/white blob, so this needs its own dedicated simple-silhouette prompt (e.g., "a simple flat white silhouette of a crescent moon and star, transparent background, no gradients, no color, no glow — pure white shape only, suitable for Android status-bar notification icon tinting").

| Density | Size (px) | Folder |
|---|---|---|
| mdpi | 24×24 | `drawable-mdpi/ic_stat_notify.png` |
| hdpi | 36×36 | `drawable-hdpi/ic_stat_notify.png` |
| xhdpi | 48×48 | `drawable-xhdpi/ic_stat_notify.png` |
| xxhdpi | 72×72 | `drawable-xxhdpi/ic_stat_notify.png` |
| xxxhdpi | 96×96 | `drawable-xxxhdpi/ic_stat_notify.png` |

### 3.7 Splash Screen Icon (Android 12+ SplashScreen API)

Uses the **same foreground drawable** as the adaptive icon by default (recommended — keep it consistent), rendered inside a system-defined circular/rounded backdrop.

| Spec | Value |
|---|---|
| Icon content area | 240×240 dp |
| Must sit inside a | 288×288 dp circular mask |
| Source | Reuse the adaptive-icon foreground vector/PNG — no separate asset strictly required, but a simplified version with slightly more internal padding renders best |

### 3.8 Play Store Promo Graphic (optional, legacy — no longer required by Play Console but still occasionally requested)

| Asset | Size | Format |
|---|---|---|
| Promo graphic | 180×120 px | PNG/JPEG |

### 3.9 TV Banner (only if NurKids ever ships an Android TV build — not currently in scope per this app's phone/tablet-only design)

| Asset | Size | Format |
|---|---|---|
| TV banner | 320×180 px | PNG/JPEG |

---

## 4. Recommended Generation Workflow

1. Generate the **foreground** (§1.1) and **background** (§1.2) layers separately at 432×432px each — these two feed Android Studio's built-in **Image Asset Studio** (`New > Image Asset > Launcher Icons (Adaptive and Legacy)`), which auto-produces every density in §3.1–§3.3 correctly, including the round variants.
2. Generate the **combined flat icon** (§1.3) at 512×512px for the Play Store listing icon (§3.4).
3. Generate the **notification silhouette** separately (§3.6) — do not reuse the colored icon; Android will render it wrong.
4. Generate the **feature graphic** (§2) at 1024×500px for the Play Store banner (§3.5).
5. Feed the same foreground vector into the Splash Screen API config (§3.7) rather than creating a new asset.

This gives you every required Android + Play Store asset from four source generations instead of hand-producing a dozen+ individual files.
