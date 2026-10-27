# G.38 NextJS_Web 01 — Marketing Website Application Shell & Design System

`Development_Blueprints.G38_Marketing_Website.NextJS_Web.01-marketing-website-shell-and-design-system.md`

**Module:** Marketing Website Shell (`apps/marketing-web/`)  
**Parent Feature:** G.38 — Marketing Website  
**Sequence:** Seq 587  
**Status:** 🟡 **Pending Implementation**  
**Depends on:** Phase 0 Workspace Foundation, Phase 1 CI/CD  
**Source of truth:** `PRD_Documents/Website Home/NoorHeroes_website_content_spec.md` §1  

---

## 1. Objective and Purpose
Scaffold the standalone Next.js 14 App Router project for the public marketing website, establishing the design token system, responsive navbar, mobile drawer, and shared footer.

## 2. Technical Stack & Design Tokens
- Framework: Next.js 14 (Static Site Generation + Incremental Static Regeneration).
- Styling: Tailwind CSS, CSS Variables for Islamic color tokens:
  - `--primary`: `#0F5E5E` (Deep Teal)
  - `--accent`: `#F0B429` (Warm Amber Gold)
  - `--background`: `#FCFCFA` (Subtle Warm Cream)
  - `--foreground`: `#1A202C`
- Fonts: `next/font/google` loading Inter (body), Outfit (headings), and Amiri (Arabic typography).

## 3. Implementation Tasks
1. Initialize `apps/marketing-web` with TypeScript strict mode and Tailwind CSS.
2. Build `NavigationHeader` with sticky glassmorphism styling and mobile drawer navigation.
3. Build `Footer` with legal disclaimers, language picker, and App Store badges.
4. Add dark mode toggle support using `next-themes`.
