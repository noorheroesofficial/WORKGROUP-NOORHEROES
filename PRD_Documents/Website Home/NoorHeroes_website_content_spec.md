# NoorHeroes Marketing Website — Content, Design \& Build Specification

**Document purpose:** A complete, section-by-section specification for the NoorHeroes marketing website (noorheroes.com), grounded in the actual, previously-documented NoorHeroes product — its 37 specified features (A.1–F.37), its exact brand tokens, its trust/safety architecture, and its pricing model. This is a **content and build spec**, not final legal copy or final marketing copy — every section states clearly whether it's **\[GROUNDED]** (directly sourced from documented product facts) or **\[PLACEHOLDER — NEEDS INPUT]** (marketing content like testimonials, founding story, or press mentions that doesn't exist in the product documentation and must not be fabricated).

\---

## 0\. Sourcing Note (read first)

Per instruction, this document does not invent facts about the product. Every feature claim, safety claim, and pricing figure below is pulled from the NoorHeroes feature documentation already produced (Features A.1–F.37) and the product's design-token/brand system. Where the request asks for content that simply doesn't exist yet in any document — **Our Story** (founding narrative), **Testimonials** (real parent quotes), **Press/Media** (actual coverage), **Careers** (actual open roles), **team bios** — this spec provides the correct **structure and tone** for that section plus a clearly-marked placeholder, rather than fabricated quotes, names, or dates. Legal pages (**Privacy Policy, Terms of Use, Cookie Policy**) are scoped to *what the actual product's documented data practices require them to cover* — the final binding legal text must still be drafted/reviewed by qualified legal counsel before publishing; this spec is not that legal text.

\---

## Table of Contents

1. [Brand System Recap](#1-brand-system-recap)
2. [Site Map \& Navigation](#2-site-map--navigation)
3. [Global Technical \& UX Requirements](#3-global-technical--ux-requirements)
4. [Homepage — Section-by-Section Specification](#4-homepage--section-by-section-specification)
5. [Secondary Pages](#5-secondary-pages)
6. [Legal Pages — Scope Outline](#6-legal-pages--scope-outline)
7. [Footer Specification](#7-footer-specification)
8. [Feature Completeness Cross-Check Matrix](#8-feature-completeness-cross-check-matrix)
9. [Animation \& Interaction Pattern Library](#9-animation--interaction-pattern-library)
10. [SEO Specification](#10-seo-specification)
11. [Accessibility Checklist](#11-accessibility-checklist)
12. [Recommended Tech Stack](#12-recommended-tech-stack)
13. [Content Gaps — Requires Stakeholder Input](#13-content-gaps--requires-stakeholder-input)

\---

## 1\. Brand System Recap

*(Full detail already specified in `design\_prompts.md` and `NoorHeroes\_App\_Icon\_Banner\_Prompts\_and\_Specs.md` — reuse those assets directly rather than regenerating. Recap here for build reference.)*

|Token|Hex|Web Use|
|-|-|-|
|Teal (primary)|`#0B5E4A`|Primary nav, buttons, headers|
|Teal Light|`#147A61`|Hover states|
|Teal Pale|`#E6F4F1`|Section backgrounds|
|Gold (accent)|`#C9921A`|CTAs, highlights, badges|
|Gold Light|`#E8B84B`|Gradients, glow accents|
|Gold Pale|`#FDF5E4`|Warm section backgrounds|
|Cream (base)|`#FDF8F2`|Page background|
|Cream Dark|`#F5ECD8`|Card backgrounds|
|Ink|`#1A1207`|Primary text|
|Ink Soft|`#3D2F1A`|Secondary text|
|Muted|`#7A6A54`|Tertiary text/captions|
|Border|`#D6C9B0`|Dividers|
|Purple (accent)|`#7B3FA0`|Achievement/mastery accents|
|Alert Red|`#C0392B`|Form errors only — never used decoratively|

**Typography:** Playfair Display (serif display headings — premium/elegant), DM Sans (body/UI — clean/modern), Amiri (Arabic display — for the bilingual/RTL toggle and Arabic marketing copy).

**Mascot:** Noor — the glowing lantern/crescent-moon companion character (full reference sheet spec in `design\_prompts.md` §2.1). Noor should appear throughout the site as the visual "host" — greeting visitors in the hero, guiding scroll narratives, appearing in empty/loading states of interactive demos.

**Tone of voice:** warm, calm, trustworthy, never hyperbolic or high-pressure. Avoid gamified marketing clichés ("Level up your kid's Iman!"); this is a premium, scholar-governed educational product, not a mobile-game upsell funnel. Confidence comes from specificity (real feature detail, real safety architecture) rather than superlatives.

**Dual-register discipline:** the website itself should read primarily in the **parent-mode register** (calmer, credible, premium) since parents are the actual site visitors and purchasers — with the **child-mode warmth** (Noor, playful color, glow) reserved for illustrating what the *in-app* experience looks like, kept visually distinct (e.g., inside phone-mockup frames) rather than applied to the entire site's own chrome.

\---

## 2\. Site Map \& Navigation

```
/ (Homepage)
/features                  → deep-dive feature index
/features/\[slug]           → one page per major feature pillar (Stories, Quran, Habits, Rewards...)
/safety                    → Safety \& Privacy deep-dive
/pricing                   → Plan comparison (Free / Mobile Family / Premium Family)
/how-it-works
/about                     → Mission, Vision, Story, Values, Focus Areas
/blog                      → News/blog index
/blog/\[slug]
/faq
/download                  → App store CTA landing (for paid-ad traffic)
/contact
/careers                   → placeholder
/press                     → placeholder
/partners                  → placeholder
/legal/privacy-policy
/legal/terms-of-use
/legal/cookie-policy
```

**Primary nav (desktop):** Logo | Features | Safety | Pricing | How It Works | About | Blog | \[Language: EN/AR toggle] | Download App (button, gold, sticky-visible on scroll)

**Mobile nav:** hamburger → full-screen overlay menu with the same items, Noor illustration in the overlay background at low opacity.

\---

## 3\. Global Technical \& UX Requirements

* **Responsive breakpoints:** mobile (< 640px), tablet (640–1024px), desktop (1024–1440px), wide (1440px+). Every section in §4 below must be authored mobile-first with an explicit tablet/desktop layout change noted.
* **Performance targets:** Lighthouse Performance ≥ 90, LCP < 2.5s, CLS < 0.1, total initial JS payload < 200KB gzipped (defer Lottie/heavy animation libraries, lazy-load below-the-fold sections and all app-screenshot imagery).
* **Accessibility:** WCAG 2.1 AA minimum (full checklist in §11).
* **RTL support:** the site must fully mirror layout (not just text direction) when Arabic is selected, consistent with the product's own RTL rigor documented throughout the app itself (every app-screenshot mockup shown on the site should have an EN and an AR variant, per the existing `design\_prompts.md` EN/AR prompt pairs).
* **Animation performance discipline:** every scroll-triggered/parallax animation must respect `prefers-reduced-motion` and degrade to a simple fade/no-animation for users with that OS setting enabled — this directly extends the app's own "calm, never overstimulating" design philosophy to the web.
* **No dark patterns:** consistent with the product's own anti-manipulation principles (documented throughout C.24/E.31), the website must never use countdown-timer urgency tricks, fake scarcity, or pre-checked upsell boxes in its own CTAs.

\---

## 4\. Homepage — Section-by-Section Specification

Each section below includes: **Purpose**, **Grounding**, **Copy Direction**, **Visual/Animation Treatment**, and **CTA**.

### 4.1 Hero Section

**Purpose:** Immediate clarity on what NoorHeroes is, who it's for, and an emotionally warm first impression.

**Grounding \[GROUNDED]:** NoorHeroes is an AI-powered Islamic learning app for children ages 3–15, with scholar-reviewed content, multi-child family accounts, parental controls, and gamified rewards (source: product overview, consistent across every feature document).

**Copy direction:**

* Eyebrow label: "Scholar-Reviewed. Parent-Trusted. Genuinely Loved by Kids."
* Headline (H1): "Islamic Learning, Made Joyful" — or alternate: "Where Your Child's Islamic Journey Begins"
* Subhead: "NoorHeroes brings stories, Qur'an, duas, and daily habits to life for children ages 3–15 — every piece of content scholar-reviewed, every feature built with real child-safety architecture, every moment designed to build genuine love for the deen."
* Primary CTA: "Download Free" (App Store + Google Play buttons)
* Secondary CTA: "See How It Works" (scrolls to §4.5)

**Visual/animation treatment:** Full-bleed hero with a deep-teal-to-cream gradient background, Noor floating with a gentle idle animation (subtle glow pulse, small looping float — Lottie), 2–3 floating phone mockups showing real app screens (Home, Story Player, Reward unlock) at slightly different depths for a parallax effect on mouse-move/scroll, soft particle/star accents drifting slowly. Animated counter strip beneath the fold-line showing key stats (see §4.4).

### 4.2 What Is NoorHeroes

**Purpose:** A clear, single-paragraph explanation before any feature detail.

**Grounding \[GROUNDED]:** Multi-child family accounts, AI-powered personalization bounded by a scholar-reviewed corpus, gamified habit/reward system, parent dashboard with real oversight tools.

**Copy direction:** "NoorHeroes is a complete Islamic learning ecosystem for the whole family — one app, multiple children's profiles, and a parent dashboard that actually shows you what's happening. Stories that teach character. Qur'an and Arabic learning built for real beginners. Duas your child will actually remember. Daily habits that build without shame. And an AI layer designed from the ground up to increase trust, never risk."

**Visual/animation treatment:** Split layout — left: copy; right: an animated "app anatomy" illustration showing the 5 bottom-nav areas (Home/Learn/Stories/Rewards/Profile) as glowing connected nodes that pulse in sequence on scroll-into-view.

### 4.3 What Problem We Are Solving

**Purpose:** Establish the actual need before the pitch.

**Grounding \[GROUNDED]:** The product's own risk register and design principles document real problems it was built to solve: (1) parents wanting Islamic education content but unable to verify its scholarly accuracy themselves; (2) generic kids' apps using manipulative engagement patterns (streaks-as-shame, sibling comparison, pay-to-win) that NoorHeroes explicitly architects against; (3) AI-powered apps for children carrying real safety risk that most products don't take seriously; (4) parents needing genuine oversight tools, not just a "screen time" toggle.

**Copy direction:**

> "Most Islamic content for kids is either theologically inconsistent, visually uninspiring, or trapped in formats children don't want to use. Most 'educational' apps rely on the same manipulative engagement tricks as any other mobile game — leaderboards that shame, streaks that punish a missed day, in-app purchases dressed up as progress. And most AI-powered kids' products bolt safety on as an afterthought. NoorHeroes was built to solve all three at once."

**Visual/animation treatment:** Three-card layout, each card revealing on scroll with a soft slide-up + fade, icon animates in (from the global icon library — scholar-badge icon, anti-shame streak-flame icon, AI-safety-shield icon).

### 4.4 Animated Stat Counters (embedded in Hero or as its own strip)

**Grounding \[GROUNDED — figures from documented success metrics/targets, must be updated with real live figures at launch]:**

* "X Scholar-Reviewed Stories \& Lessons" (count from actual published content library at launch)
* "4 Languages Supported" (English, Hindi, Urdu, Arabic — per Localization Management, Feature E.34)
* "100% of AI Responses Pass Safety Evaluation" (per F.35's evaluation-gate requirement)
* "0 Sibling Comparisons. Ever." (the product's structural no-sibling-comparison guarantee, A.7/A.11/C.20)

*(Note: only publish real, current, verifiable numbers at launch — do not display a placeholder number as if live.)*

**Visual/animation treatment:** Numbers count up from 0 on scroll-into-view (standard animated-counter pattern), each with a small icon accent.

### 4.5 How NoorHeroes Works

**Purpose:** A simple 4-step mental model for a first-time visitor.

**Grounding \[GROUNDED]:** Reflects the actual onboarding flow (A.1) and daily-use loop (A.2/A.7/A.11).

**Copy direction (4 steps):**

1. "Create Your Family Account" — parent signs up, sets up multi-child profiles, each with their own age-appropriate experience.
2. "Your Child Explores, Safely" — stories, Qur'an, duas, and games, all scholar-reviewed and age-gated, with AI features bounded by real safety architecture.
3. "Habits Build Naturally" — daily missions and streaks that reward consistency without ever shaming a missed day.
4. "You Stay in the Loop" — a real parent dashboard: weekly reports, screen-time controls, AI safety history, all without a single sibling-comparison chart.

**Visual/animation treatment:** Horizontal scroll-driven step-through on desktop (numbered path with Noor "walking" the path as the user scrolls), vertical stacked cards on mobile. Each step's icon animates in from the global icon library.

### 4.6 What NoorHeroes Offers — Full Feature Overview

**Purpose:** The comprehensive, accurate feature catalog the entire request is anchored on. This section must reflect **every** documented feature — see the completeness matrix in §8.

**Grounding \[GROUNDED — this section is the direct product of Features A.1–B.18]**

**Structure:** A tabbed or filterable grid organized by the app's own feature groupings:

**Learn \& Explore**

* **Stories** — animated, scholar-reviewed stories including Prophet stories (told with age-appropriate reverence, never visually depicting the Prophets), bedtime stories, Islamic-manners stories, seasonal stories, with interactive choice moments.
* **Qur'an \& Arabic Learning** — a real curriculum path from Arabic letters through Surah memorization, AI-assisted pronunciation coaching (push-to-talk only, visible recording state, zero raw-audio retention), tajweed guidance.
* **Dua Learning** — categorized duas (morning, evening, meals, travel, sleep), audio-mandatory (never text-only), source-cited.
* **Islamic Facts** — a bite-sized daily-fact module, scholar-approved.
* **Daily Quiz Engine** — adaptive, non-judgmental quizzes across every learning domain.
* **Skill Tree \& Mastery** — a genuine mastery model (Locked → Ready → Learning → Practicing → Mastered → Needs Refresh) with spaced-repetition-based review, never a raw numeric score shown to a child or parent.

**Build Habits**

* **Habit Tracker** — Salah, Qur'an reading, dhikr, good deeds, fasting practice, with streak protection (a missed day is a gentle grace window, never a punitive reset) and a Family Garden view that shows combined progress without ranking individual children.

**Play \& Grow**

* **Games Module** — every mini-game is mapped to a real learning skill; no zero-skill-value game can publish.
* **Rewards System** — Noor Heroes Points, XP, named badges, an Achievement Store, all running on an append-only, auditable ledger — no real-money purchases reachable by a child.
* **Avatar System** — customizable companion characters, unlock rules always tied to real achievements (never arbitrary or pay-to-unlock).

**Stay Organized**

* **Search \& Discovery**, **Favorites**, **Offline Downloads** (resumable, checksum-verified), **Child Profile**, **Notifications**.

**For Parents**

* **Parent Dashboard** — weekly reports, activity timeline, screen-time/healthy-usage insights.
* **Multi-Child Management** — add, edit, temporarily disable, or (self-service, fully safeguarded) permanently delete a child's profile.
* **Per-Child Reports** — trend charts, habit calendars, skill mastery grids, and an AI safety log — never a raw AI transcript, never a raw score.
* **Parental Controls** — screen-time limits (server-authoritative, cannot be bypassed by changing a device clock), bedtime windows, granular AI/voice permission controls, content age-level overrides.
* **Subscription \& Billing** — transparent trial terms, billed only through Google Play/App Store, cancel anytime.
* **Privacy, Consent \& Data Rights** — review and withdraw any consent, request a data export, manage account security.
* **Notifications \& Support** — a real support center, safety-critical alerts that can never be silently muted.

**Seasonal**

* **Ramadan Mode** — a full 30-night journey with a Lantern Progress Path, a dedicated calmer Laylatul Qadr experience, and an Eid celebration — every night of content scholar-approved at least 3 weeks before Ramadan begins, as a matter of policy.

**Visual/animation treatment:** Interactive filterable grid (Learn / Build Habits / Play \& Grow / Stay Organized / For Parents / Seasonal). Each card flips or expands on hover/tap to reveal a short description and a small looping preview animation or app-screenshot thumbnail. Category filter transitions use a smooth masonry re-flow animation.

### 4.7 Why Choose NoorHeroes

**Purpose:** Direct differentiation.

**Grounding \[GROUNDED]:** Every claim below is a documented, structural product guarantee, not a marketing exaggeration.

**Copy direction (comparison-style callouts):**

* "Scholar-reviewed, not AI-improvised" — religious-rulings questions never get an improvised model answer; they route to an approved-answer set or a scholar handoff, always cited.
* "Built to never shame" — no leaderboards ranking your children against each other, no punitive streak resets, no raw scores shown to a child.
* "Real parental control, not a toggle" — screen-time limits that survive a device-clock change, bedtime windows that respect content boundaries (never cutting off mid-word), an AI permissions panel that can only restrict, never expand, capability.
* "AI that increases trust, not risk" — a documented six-stage safety pipeline, an evaluation gate with zero tolerance for unresolved critical findings, and a platform-wide emergency kill switch.
* "Privacy by architecture" — child PII is masked by default even from our own support staff; unmasking requires a logged, justified, second-approved, time-boxed exception.

**Visual/animation treatment:** Alternating left/right "us vs. the old way" comparison rows, each animating in with a horizontal wipe reveal.

### 4.8 Our Mission

**\[PLACEHOLDER — NEEDS INPUT]** No explicit mission-statement wording exists in the product documentation. Suggested draft, grounded in documented principles, **for stakeholder approval before publishing**:

> \*Draft:\* "To help every Muslim child build a genuine, joyful relationship with their faith — through learning experiences as trustworthy as they are delightful."

### 4.9 Our Vision

**\[PLACEHOLDER — NEEDS INPUT]** Suggested draft, grounded in the platform's demonstrated ambition (multi-locale, seasonal depth, family-wide design) — **for stakeholder approval**:

> \*Draft:\* "A world where Islamic education is the most trusted, most loved part of every Muslim family's digital life."

### 4.10 Our Story

**\[PLACEHOLDER — NEEDS INPUT]** No founding narrative (founder names, founding year, origin anecdote) exists in the product documentation. **Do not publish a fabricated founding story.** Structure to fill in once provided:

* Founding year \& founders
* The specific problem that motivated the company's start
* Key early milestones (first scholar partnership, first content library, first release)

### 4.11 Our Key Focus Areas

**Grounding \[GROUNDED]:** Directly derived from the platform's documented investment areas across the 37 features.

* **Scholarly Integrity** — the full content review pipeline (draft → editorial → automated safety scan → scholar review → child-safety review → publish), with segregation of duties enforced at the database level.
* **Child Safety \& Wellbeing** — anti-shaming design, screen-time/bedtime architecture, zero-tolerance AI safety gating.
* **Family Trust** — transparent billing, genuine data rights, masked-by-default PII even from internal staff.
* **Multilingual Access** — English, Hindi, Urdu, Arabic today, with Bahasa Indonesia/Malay and Turkish schema-ready.
* **Responsible AI** — a five-service AI architecture (Recommendation, Narration, Learning, Moderation, Insights), each independently bounded and evaluation-gated before any release.

**Visual/animation treatment:** Icon-led grid, each item's icon drawn with an SVG line-draw-in animation on scroll.

### 4.12 Core Values

**Grounding \[GROUNDED]:** Derived directly from the platform's stated, structurally-enforced hard rules — these are not aspirational values but architected guarantees.

1. **Never Shame** — no sibling comparisons, no punitive streaks, no raw scores shown to a child.
2. **Never Improvise on Religion** — every religious answer is scholar-approved and cited; nothing is left to AI guesswork.
3. **Never Trade Trust for Growth** — no dark patterns, no manipulative engagement mechanics, no real-money purchases reachable by a child.
4. **Never Hide the Truth from Parents** — real reports, real AI safety logs, real data rights, with only a redacted (never raw) view protecting the child's privacy.
5. **Never Ship Unsafe AI** — zero unresolved critical findings, ever, before any AI-layer change reaches a single child.

**Visual/animation treatment:** Five vertically-stacked "pledge" cards, each with a small animated checkmark-seal icon that "stamps" in on scroll.

### 4.13 Interactive App Screenshots

**Purpose:** Let visitors actually explore the product, not just read about it.

**Grounding \[GROUNDED]:** Screenshot content should be sourced from the actual, already-specified UI (every one of the 37 feature documents includes detailed screen specifications — use those, not invented UI).

**Visual/animation treatment:** An interactive device-frame carousel/tab set: tapping a feature label (Home / Stories / Qur'an / Rewards / Parent Dashboard) swaps the phone-mockup screenshot with a smooth crossfade + subtle 3D-tilt-on-drag effect. Include a live EN/AR toggle on this component specifically, demonstrating the app's real RTL support.

### 4.14 Product Highlights

**Grounding \[GROUNDED]:** A curated "best of" pull from §4.6 — e.g., the Ramadan Lantern Progress Path, the Skill Tree mastery system, the Family Garden, the Achievement Store. Format as a horizontally-scrolling highlight reel with autoplay-on-scroll-into-view (pausable, respects reduced-motion).

### 4.15 Learning Journey

**Purpose:** Show the arc of a child's multi-year progression, not just a single session.

**Grounding \[GROUNDED]:** Directly reflects A.9's Skill Tree/Mastery Engine level progression (Seedling → Sprout → Star Seeker → Noor Guardian → Hafiz Hero) and A.7/A.11's habit-and-reward compounding design.

**Visual/animation treatment:** A long horizontal (vertical on mobile) illustrated timeline/path, Noor "traveling" along it as the user scrolls, with the five level-badge illustrations appearing at their respective milestones, each glowing progressively richer as documented in `design\_prompts.md` §13.2.

### 4.16 Parent Benefits

**Grounding \[GROUNDED]:** Pulled directly from the Parent Area feature set (C.19–C.26).

* Real weekly reports, not vague "engagement" numbers.
* Screen-time and bedtime controls that are actually enforced server-side.
* AI permissions you control per child — disable AI entirely, restrict voice interaction, or choose curated-only mode.
* Full data rights: review every consent you've given, request an export, delete an account with a transparent 7-day grace period.
* A support team that treats a billing or safety alert as something that can never be silently muted.

### 4.17 Child Benefits

**Grounding \[GROUNDED]:** Pulled from the child-facing feature set (A.1–A.12, B.13–B.18).

* Stories and characters that feel genuinely made for them, not a generic reskin.
* A companion (Noor) that celebrates effort, never compares them to a sibling.
* Learning that adapts to them — never punished for a wrong answer, never locked out of yesterday's missed habit.
* A rewards economy that feels earned, never pay-to-win.

### 4.18 Safety \& Privacy

**Purpose:** This is the single most evidence-rich section on the site — it should read like real documentation, not a vague trust badge.

**Grounding \[GROUNDED — extensively, from C.19/C.21/C.26/E.28/E.29/E.30/E.32/F.35/F.37]**

**Copy direction (structured as an expandable accordion, each backed by a real architectural fact):**

* "How we handle your child's data" — masked by default (real name, DOB, and contact are never visible to support or content staff); any exception requires a logged, justified, second-approved, time-boxed unmask.
* "How AI is kept safe" — a documented six-stage pipeline (prompt filter → restricted engine → RAG boundary → confidence scoring → output moderation → parent audit), an evaluation gate requiring zero unresolved critical findings before any release, and a platform-wide kill switch that takes effect in under 60 seconds.
* "How content is reviewed" — every piece of content passes Draft → Editorial Review → Automated Safety Scan → Scholar Review → Child-Safety Review → Publish, with segregation of duties enforced at the database level (no single person can write and approve the same content).
* "How we handle voice" — push-to-talk only, never always-listening; recording state is always visibly shown; raw audio is deleted after scoring by default.
* "How billing works" — store receipt and signed webhook are the only source of truth for your subscription status; we cannot manually activate or fabricate a subscription.
* "How deletion works" — disabling a profile is instant and fully reversible; permanent deletion is self-service with a clear warning, fully audited.

**Visual/animation treatment:** Accordion with a small architecture-diagram illustration per item (simplified versions of the flow diagrams already specified in the underlying feature docs), expanding with a smooth height-animation.

### 4.19 Testimonials

**\[PLACEHOLDER — NEEDS INPUT]** No real parent testimonials, quotes, names, ratings, or photos exist in the product documentation. **Do not publish fabricated quotes or star ratings.** Structure to fill in once real testimonials/reviews are collected (post-launch or from a beta cohort):

* Parent name, location (city/country level, never more specific), a real quote, optionally a star rating pulled from actual App Store/Play Store review data (with permission).

**Visual/animation treatment (ready for real content):** Horizontally-scrolling testimonial cards on the premium testimonial-card-background template already specified in `design\_prompts.md` §28.5.

### 4.20 FAQ

**Grounding \[GROUNDED — every answer below is a real, documented policy]**

* **"What ages is NoorHeroes for?"** — Ages 3 to 15, with age-appropriate content bands throughout.
* **"Is the religious content verified?"** — Yes. Every piece of content passes scholar review before publication; religious-rulings questions are never answered by improvised AI, only approved content or a scholar handoff.
* **"Can I add more than one child?"** — Yes, multi-child family accounts are supported, with each plan tier supporting a different number of active children.
* **"What happens if I downgrade my plan?"** — Locking never deletes progress. If your new plan supports fewer active children, you choose who stays active; the rest are disabled (not deleted) and can be re-enabled anytime your plan allows.
* **"Can I control screen time?"** — Yes, with a daily limit, a bedtime window, and a warning before the limit is reached — enforced server-side, so it can't be bypassed by changing your device's clock.
* **"Does the app use AI? Is it safe?"** — Yes, in a few bounded ways (recommendations, pronunciation coaching, parent report summaries) — all governed by a documented six-stage safety pipeline and an evaluation gate with zero tolerance for unresolved safety issues.
* **"Can I export or delete my data?"** — Yes, anytime, from Settings — export requests are tracked and visible from both the app and the web portal; account deletion is self-service with a clear warning and a 7-day grace period.
* **"How does billing work?"** — Billed only through Google Play or the App Store, never a custom payment form. Trials clearly disclose price, renewal date, and auto-renew terms before you confirm.
* **"Does NoorHeroes show ads?"** — No advertising anywhere in the child experience.
* **"Is my child's voice recording stored?"** — No — voice features are push-to-talk only, recording state is always visible, and raw audio is deleted after scoring by default.

**Visual/animation treatment:** Standard accordion, smooth expand/collapse, search box at top with instant client-side filtering.

### 4.21 Blog / News Preview

**\[PLACEHOLDER — NEEDS INPUT]** No actual blog posts exist yet. Suggested, grounded content pillars for the editorial calendar (topics genuinely supported by the product's real feature depth, not invented):

* Parenting \& Islamic education tips (drawing on the app's own scholar-reviewed content areas)
* Product updates (new content drops, Ramadan Mode launch announcements)
* Behind-the-scenes on the scholar-review process
* Child-safety and responsible-AI explainers

**Visual/animation treatment (ready for real content):** 3-card preview grid, "View All" CTA to `/blog`, cards fade/slide in on scroll.

### 4.22 Download App CTA

**Grounding \[GROUNDED]:** Google Play and App Store buttons (App Store availability should only be claimed once genuinely shipped — the underlying platform's feature documentation is Android-first; confirm iOS availability before publishing that badge).

**Copy direction:** "Start Your Family's Journey Today" — "Free to start. No credit card required for the Free Family Starter plan."

**Visual/animation treatment:** Full-width warm gradient band, Noor illustration, animated QR code (scan-to-download) for desktop visitors, store badges with a subtle hover-lift micro-interaction.

### 4.23 Connect With Us / Let's Get Social

**Grounding \[GROUNDED — as a section structure; actual handles are operational information not present in product docs]**

Platforms requested: Facebook, Instagram, LinkedIn, X/Twitter, YouTube. **\[PLACEHOLDER — NEEDS INPUT: real handle URLs]**

**Visual/animation treatment:** Icon row with hover glow/scale micro-interaction, using the global icon library's flat-icon style extended to social marks (link out only — do not embed live social feeds without a performance/privacy review, since third-party embeds often violate the site's own performance and privacy-by-architecture principles).

\---

## 5\. Secondary Pages

### 5.1 Contact Us

**Grounding \[GROUNDED — as a structure]:** Route general inquiries, support (link to in-app Support Center per B.17/C.25's real support-ticket system rather than duplicating it), press inquiries, and partnership inquiries into distinct contact paths. **\[PLACEHOLDER — NEEDS INPUT: real support email/phone/address]**

### 5.2 Careers

**\[PLACEHOLDER]** — structure: mission-aligned intro, current openings (or "no open roles right now, check back soon" honest empty state), culture/values reuse from §4.12.

### 5.3 Press/Media

**\[PLACEHOLDER]** — structure: press-kit download (logo files, screenshots — reuse `design\_prompts.md`/icon-spec assets), media contact, press mentions list (empty until real coverage exists — do not fabricate press logos or quotes).

### 5.4 Partner With Us

**\[PLACEHOLDER]** — structure: partnership categories (content/scholar partnerships, school/organization partnerships, distribution partnerships), a simple inquiry form.

\---

## 6\. Legal Pages — Scope Outline

> \*\*Important:\*\* the outlines below describe what topics each legal page must \*\*cover\*\* based on the product's actual documented data practices — they are not final legal text. Have qualified legal counsel draft/review the binding version before publishing.

### 6.1 Privacy Policy — must cover

* What data is collected at signup (parent identity via OTP; child profile: nickname, DOB for age-band, no required real name)
* The masking-by-default model and the narrow, audited unmask exception (E.32)
* AI data handling: voice processing minimization, zero raw-audio retention by default (A.5/F.35)
* Consent model: required vs. optional consents, and how to review/withdraw each (C.26)
* Data export and deletion rights, including the 7-day account-deletion grace period (C.21/C.26)
* Third-party processors (billing via Google Play/App Store, any AI model providers, any analytics providers actually in use)
* Children's-privacy-law compliance framing (COPPA and equivalent regional frameworks — legal counsel must confirm exact regulatory language)

### 6.2 Terms of Use — must cover

* Subscription terms: trial disclosure, auto-renewal, cancellation (access continues until period end), platform-billing-only purchase flow (C.24)
* Account eligibility (parent must be an adult; child profiles are not independently-authenticated accounts, C.19/F.37)
* Acceptable use, content ownership, and license terms
* Disclaimer language around religious content being provided per the platform's own scholar-review process (a framing statement, not a legal disclaimer template — counsel to finalize)

### 6.3 Cookie Policy — must cover

* Essential cookies (session/auth) vs. optional (analytics) — reflecting the site's own no-dark-patterns principle (§3), the cookie consent banner should default to declining non-essential cookies, consistent with the app's own "most privacy-preserving default" instruction pattern used throughout the underlying product's own design principles.

\---

## 7\. Footer Specification

```
Column 1 — Company              Column 2 — Resources         Column 3 — Legal
About Us                        Features                     Privacy Policy
Our Story                       Pricing                      Terms of Use
Careers                         FAQ                           Cookie Policy
Press/Media                     Blog
Partner With Us                 Safety \& Privacy
Contact Us

Column 4 — Connect
\[Facebook] \[Instagram] \[LinkedIn] \[X/Twitter] \[YouTube]
Contact: \[support email]  \[PLACEHOLDER — NEEDS INPUT]

—
\[App Store badge] \[Google Play badge]
—
© 2026 NoorHeroes Private Limited. All rights reserved.
```

Footer background: deep teal (`#0B5E4A`), text in cream/white, gold link-hover underline animation.

\---

## 8\. Feature Completeness Cross-Check Matrix

*(Direct response to the requirement: "If any feature exists in the documentation but is missing from the website, include it automatically." Every one of the 37 documented features is mapped to its website location below — nothing documented is omitted.)*

|Feature|Website Location(s)|
|-|-|
|A.1 Splash/Auth/Onboarding|§4.5 How It Works|
|A.2 Home Dashboard/AI Personalization|§4.6, §4.13|
|A.3 Stories|§4.6, §4.13, §4.17|
|A.4 Bedtime Audio Player|§4.6, §4.14|
|A.5 Qur'an/Arabic Learning|§4.6, §4.13, §4.18 (voice safety)|
|A.6 Dua Learning|§4.6|
|A.7 Habit Tracker|§4.6, §4.15, §4.16 (Family Garden)|
|A.8 Daily Quiz Engine|§4.6|
|A.9 Skill Tree/Mastery|§4.6, §4.15|
|A.10 Games Module|§4.6, §4.14|
|A.11 Rewards System|§4.6, §4.14, §4.17|
|A.12 Avatar System|§4.6, §4.17|
|B.13 Search \& Discovery|§4.6|
|B.14 Favorites|§4.6|
|B.15 Offline Downloads|§4.6|
|B.16 Child Profile|§4.6|
|B.17 Notifications (Child)|§4.6, §5.1 (Support link)|
|B.18 Islamic Facts|§4.6|
|C.19 Parent PIN Gate|§4.18|
|C.20 Parent Dashboard|§4.6, §4.16|
|C.21 Multi-Child Management|§4.6, §4.16, §4.20 (FAQ)|
|C.22 Per-Child Reports|§4.6, §4.16, §4.18|
|C.23 Parental Controls|§4.6, §4.16, §4.20 (FAQ)|
|C.24 Subscription \& Billing|§4.20 (FAQ), `/pricing`|
|C.25 Notifications \& Support|§5.1|
|C.26 Privacy/Consent/Data Rights|§4.16, §4.18, §4.20 (FAQ)|
|D.27 Parent Web Account Portal|§4.16 (referenced as the "web portal" companion)|
|E.28 Admin Auth/RBAC|(internal — not customer-facing; omitted from site by design)|
|E.29 Content CMS/Scholar Review|§4.7, §4.11, §4.12, §4.18|
|E.30 AI Moderation Console|§4.18|
|E.31 Engagement Tools Admin|(internal — omitted by design)|
|E.32 User Management/Child Safety View|§4.18|
|E.33 Subscription Management/Billing Ops|(internal — omitted by design)|
|E.34 Localization Management|§4.4 (language stat), site's own EN/AR toggle|
|F.35 AI Layer \& Microservices|§4.7, §4.18|
|F.36 Ramadan Mode|§4.6 (Seasonal), §4.14|
|F.37 Security Architecture|§4.18|

*(Internal admin-only features E.28/E.31/E.33 are intentionally not surfaced on the public marketing site — they're operator tooling, not a customer-facing capability. This is a deliberate completeness decision, not an oversight.)*

\---

## 9\. Animation \& Interaction Pattern Library

|Pattern|Where Used|Notes|
|-|-|-|
|Lottie idle-loop (Noor breathing/glowing)|Hero, empty-state moments across the site|Source from `design\_prompts.md` §2.1 character sheet|
|Scroll-triggered fade/slide-up|Every major section entry|Stagger children by 80–120ms for a natural cascade|
|Parallax depth (mouse-move + scroll)|Hero phone mockups|Max 15–20px displacement — subtle, never dizzying|
|Animated counters|§4.4 stats strip|Count up over 1.2–1.8s, ease-out|
|Horizontal scroll-driven step-through|§4.5 How It Works (desktop)|Pin section, translate content on scroll progress|
|Icon line-draw-in (SVG stroke animation)|§4.11 Focus Areas|400–600ms per icon|
|Accordion height-expand|§4.18 Safety, §4.20 FAQ|Standard ease, respect reduced-motion (instant show/hide fallback)|
|Card hover-lift + shadow-deepen|Feature grid (§4.6), testimonial cards|150ms, subtle (4–8px lift)|
|Crossfade + tilt-on-drag|§4.13 Interactive screenshots|Touch-draggable on mobile, click-tab on desktop|
|Progressive glow-richness reveal|§4.15 Learning Journey badges|Matches the in-app level-badge visual progression exactly|

All animation timing/easing should feel calm and premium — avoid bouncy/cartoonish easing curves; prefer smooth ease-in-out and ease-out curves consistent with the "calm, trustworthy, premium" brand register (§1).

\---

## 10\. SEO Specification

* **Homepage title tag:** "NoorHeroes — Islamic Learning App for Kids | Stories, Qur'an \& Duas, Scholar-Reviewed"
* **Homepage meta description:** "NoorHeroes is a scholar-reviewed Islamic learning app for children ages 3–15 — stories, Qur'an \& Arabic, duas, and habit-building, with real parental controls and privacy-first AI. Download free."
* **Structured data:** `SoftwareApplication` schema for the app itself (rating only once real store ratings exist — never fabricate `aggregateRating`), `Organization` schema, `FAQPage` schema for §4.20, `BreadcrumbList` on all secondary pages.
* **Per-page title/meta:** every page in the sitemap (§2) needs its own unique title/description — do not duplicate the homepage's meta across the site.
* **Open Graph / Twitter Card images:** use the marketing banner assets already specified in `design\_prompts.md` §28.
* **Canonical + hreflang:** implement `hreflang="en"` / `hreflang="ar"` pairs for every page once the EN/AR site toggle ships, pointing to the correct locale URL structure.
* **Sitemap.xml \& robots.txt:** standard, submit to Google Search Console/Bing Webmaster Tools at launch.

\---

## 11\. Accessibility Checklist

* \[ ] All interactive elements reachable and operable via keyboard alone
* \[ ] Focus states visible and high-contrast (do not rely on the brand's subtle-shadow-only elevation style for focus indication — use a clear focus ring)
* \[ ] Color contrast ≥ 4.5:1 for body text, ≥ 3:1 for large text/UI components (spot-check the gold-on-cream combinations specifically, since gold-on-light backgrounds is a common contrast failure point)
* \[ ] All images/illustrations have meaningful `alt` text (decorative Lottie/particle elements marked `aria-hidden`)
* \[ ] Accordion (§4.18, §4.20) uses proper `aria-expanded`/`aria-controls` semantics
* \[ ] Video/animation content includes pause controls; nothing autoplays with sound
* \[ ] Form fields (Contact, Partner, Careers) have properly associated labels and clear error messaging
* \[ ] Full site usable and legible with `prefers-reduced-motion: reduce` honored throughout (§3)
* \[ ] Language/RTL toggle correctly updates the `lang` and `dir` HTML attributes, not just visual text direction

\---

## 12\. Recommended Tech Stack

* **Framework:** Next.js (React) — SSR/SSG for SEO performance, App Router for per-locale routing (EN/AR)
* **Styling:** Tailwind CSS with the brand tokens (§1) mapped to Tailwind theme config
* **Animation:** Framer Motion for scroll-triggered/interaction animations, Lottie (via `lottie-react`) for the Noor character animations, GSAP ScrollTrigger only if Framer Motion's scroll capabilities prove insufficient for the horizontal step-through pattern (§4.5)
* **CMS for Blog/Press:** a headless CMS (e.g., Sanity, Contentful) so non-engineering staff can publish blog posts without a deploy
* **Forms:** server-side validated, spam-protected (e.g., hCaptcha) contact/partner/careers forms
* **Hosting:** Vercel or equivalent edge-CDN platform for the performance targets in §3
* **Analytics:** privacy-respecting analytics (consistent with §6.3's cookie-consent default), avoid heavy third-party trackers that would undermine the brand's own privacy-by-architecture story

\---

## 13\. Content Gaps — Requires Stakeholder Input

Consolidated list of everything in this spec that is **structurally ready but content-empty**, pending real input before launch:

1. **Our Mission / Our Vision** — exact final wording sign-off (§4.8, §4.9)
2. **Our Story** — real founding narrative: founders, year, origin story (§4.10)
3. **Testimonials** — real parent quotes/ratings, ideally sourced from actual App Store/Play Store reviews with permission (§4.19)
4. **Blog posts** — at least 3–5 launch-ready articles before the Blog Preview section goes live with real content (§4.21)
5. **Social handles** — real, live URLs for Facebook/Instagram/LinkedIn/X/YouTube (§4.23)
6. **Support contact details** — real email/phone/hours for Contact Us and the footer (§5.1, §7)
7. **Careers** — actual current openings or an honest "no roles right now" state (§5.2)
8. **Press/Media** — press kit assets and any real coverage (do not publish fabricated logos or quotes) (§5.3)
9. **Legal text finalization** — qualified legal counsel must draft/review the binding Privacy Policy, Terms of Use, and Cookie Policy text; §6 provides scope only
10. **Live content statistics** — the exact story/lesson counts and any store-rating figures in §4.4 must be pulled from real, current data at time of publish, never estimated
11. **iOS availability confirmation** — confirm actual App Store availability before publishing the Apple download badge (the underlying product documentation is Android-first)

