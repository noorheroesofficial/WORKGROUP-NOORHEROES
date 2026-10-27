# G.38 NextJS_Web 05 — Interactive FAQ Accordion & SEO Structured Data

`Development_Blueprints.G38_Marketing_Website.NextJS_Web.05-faq-accordion-and-seo-structured-data.md`

**Module:** Marketing Website FAQ & SEO  
**Parent Feature:** G.38 — Marketing Website  
**Sequence:** Seq 591  
**Status:** 🟡 **Pending Implementation**  
**Depends on:** 01-shell  
**Source of truth:** `PRD_Documents/Website Home/NoorHeroes_website_content_spec.md` §6, §7  

---

## 1. Objective and Purpose
Implement the expandable FAQ accordion answering top parent questions and inject JSON-LD structured data for Google Search rich snippets.

## 2. Technical Features
- `FaqAccordion`: Accessible Radix UI / shadcn accordion component with smooth height transition.
- JSON-LD Structured Data:
  - `SoftwareApplication`: App name, category, rating, operating system compatibility.
  - `FAQPage`: Auto-generates structured questions and answers for Google search SERP prominence.
  - `BreadcrumbList`: Navigation hierarchy schema.
- OpenGraph & Twitter Cards: Dynamic metadata generation using Next.js `generateMetadata()` with localized social preview images.
