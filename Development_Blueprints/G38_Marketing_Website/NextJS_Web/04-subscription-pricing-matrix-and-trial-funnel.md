# G.38 NextJS_Web 04 — Subscription Pricing Matrix & Trial Funnel

`Development_Blueprints.G38_Marketing_Website.NextJS_Web.04-subscription-pricing-matrix-and-trial-funnel.md`

**Module:** Marketing Website Pricing Table  
**Parent Feature:** G.38 — Marketing Website  
**Sequence:** Seq 590  
**Status:** 🟡 **Pending Implementation**  
**Depends on:** 01-shell, C.24 Subscription Backend (`GET /v1/billing/plans`)  
**Source of truth:** `PRD_Documents/Website Home/NoorHeroes_website_content_spec.md` §5  

---

## 1. Objective and Purpose
Present transparent, dynamic subscription plan pricing with monthly/annual toggle, savings highlights, and seamless checkout handoff.

## 2. Technical Specifications
- Pricing Plans:
  - Monthly: $9.99/month, 1 child profile.
  - Annual: $5.99/month ($69.99 billed annually), 40% discount highlight, 3 child profiles (Most Popular badge).
  - Family Tier: $14.99/month, up to 5 child profiles.
- Currency Localizer: Detects visitor country and displays localized pricing in USD, GBP, EUR, CAD, AUD, SAR, AED, and INR.
- Action: "Start 7-Day Free Trial" redirects to Parent Web Account Portal registration with pre-selected plan.
