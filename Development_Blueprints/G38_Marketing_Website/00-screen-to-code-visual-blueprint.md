# Feature G.38 — Marketing Website: Screen-to-Code Visual Blueprint

> **Module:** G38_Marketing_Website (Public Marketing Surface, `www.noorheroes.com`)  
> **Source PRD:** `PRD_Documents/Website Home/NoorHeroes_website_content_spec.md`  
> **Technology Stack:** Next.js 14 App Router, TypeScript, Tailwind CSS, shadcn/ui, Framer Motion  

---

## 1. Visual Architecture & Page Sections
The marketing website is composed of 8 responsive full-width sections structured for high conversion, trust-building, and search engine discoverability:

1. **Header Navigation Shell:** Sticky frosted-glass navbar (`backdrop-blur-md bg-white/80 dark:bg-slate-900/80`), logo mark, navigation links (Features, Curriculum, Pricing, Safety, FAQ), and dynamic CTAs ("Open Parent Portal" linking to `account.noorheroes.com`, "Get Started Free").
2. **Hero Section:** High-impact value proposition ("The Islamic Learning Adventure Your Children Will Love"), dual CTAs ("Start 7-Day Free Trial", "Watch Product Demo"), social proof pill ("Trusted by 25,000+ Muslim Families worldwide"), animated multi-device mockups showcasing KMP mobile app screens.
3. **Interactive Curriculum Showcase:** Tabbed interface demonstrating the 6 core pillars:
   - Animated Stories (Prophets & Moral Values)
   - Quran & Arabic Recitation (Gamified Tajweed)
   - Dua Mastery (Touch-to-listen, Spaced repetition)
   - Daily Habit Tracker (Salah, Sunnah, Kindness)
   - Interactive Daily Quizzes & Skill Trees
   - Safe Character Avatars & Noor Coin Economy
4. **Scholarly Verification & Safety Trust Badges:** Halal content assurance seal, Certified Islamic Scholars Review Board, 100% Ad-Free guarantee, strict COPPA & GDPR-K compliance badges, zero social media integrations.
5. **Subscription Pricing Matrix:** Dynamic billing comparison table:
   - Monthly Plan ($9.99/mo, 1 child profile)
   - Annual Plan ($5.99/mo billed annually at $69.99/yr, 40% savings badge, 3 child profiles)
   - Family Lifetime / Multi-Child Pack ($14.99/mo, up to 5 child profiles, priority support)
   - Clear "All plans start with a risk-free 7-day trial" guarantee.
6. **Parent Testimonials & Community Proof:** Carousel of verified parent quotes with star ratings, child age tags, and community testimonials.
7. **Interactive FAQ Accordion:** 10 core questions addressing Islamic methodology, screen time safety, multi-device access, and trial cancellation, embedded with `FAQPage` JSON-LD schema markup.
8. **Global Footer:** Multilingual language selector (`en`, `ar`, `ur`, `hi`), app store download badges (Google Play, Apple App Store), legal links (Privacy Policy, Terms of Service, COPPA Notice), contact form link, copyright.

---

## 2. Responsive Breakpoints & Mobile Optimization
- **Mobile (< 640px):** Single-column stacked layout, collapsible sheet menu, sticky bottom "Download App" bar.
- **Tablet (640px - 1024px):** 2-column grid for features, horizontal scrolling for testimonials.
- **Desktop (> 1024px):** Full multi-column grid, interactive hover micro-animations, rich imagery.
