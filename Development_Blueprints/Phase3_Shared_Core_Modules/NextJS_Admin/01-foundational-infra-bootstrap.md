# Phase 3 — Next.js Admin: Foundational Infrastructure & RBAC Shell Bootstrap

`Development_Blueprints.Phase3_Shared_Core_Modules.NextJS_Admin.01-foundational-infra-bootstrap.md`

**Module:** `noorheroes-admin` (Next.js 14 App Router Web Portal)  
**Phase:** 3 — Shared/Core Modules  
**Status:** ✅ **Implemented & Verified** (Verified against `noorheroes-admin/NEXT-JS-INSTRUCTIONS.md`)  
**Depends on:** Phase 0 Workspace, Phase 2 Backend Foundation & E.28 Admin Auth API  
**Consumed by:** All Phase 7 Admin & Scholar Portal Features (E.28 through E.34)  
**Source of truth:** `noorheroes-admin/NEXT-JS-INSTRUCTIONS.md`; `MASTER-README.md`  

---

## 1. Objective and Purpose
Establish the core web application shell, layout, role-based navigation guards, and API client infrastructure for the NoorHeroes Admin & Scholar Portal (`noorheroes-admin`).

## 2. Technical Architecture & Stack
- **Framework:** Next.js 14 (App Router), React 18, TypeScript (strict mode).
- **Styling & UI:** Tailwind CSS, shadcn/ui component library, Lucide React icons.
- **Server State:** TanStack Query v5 (`@tanstack/react-query`) with automatic caching, background refetching, and error boundaries.
- **Client State:** Zustand store for UI toggles, sidebar collapse, and active filters.
- **Form Handling:** React Hook Form with Zod schema validation.

## 3. 9-Role RBAC Navigation Shell
- Role Scopes: `super_admin`, `product_admin`, `content_editor`, `scholar`, `moderator`, `support`, `billing_ops`, `analytics_viewer`, `trust_safety`.
- Route Group Scaffolding:
  - `(auth)`: Login, TOTP 2FA challenge, recovery.
  - `(dashboard)`: Shell with top header, breadcrumbs, user avatar, and role-gated sidebar navigation.
- Middleware: Next.js middleware inspecting HTTP-only admin session cookies, validating role scope allowlists, and redirecting unauthorized visits with HTTP 403.

## 4. Verification and Acceptance Criteria
- [x] Application boots cleanly on `localhost:3000`.
- [x] Generated TypeScript API client communicates with FastAPI `/v1/admin/*` endpoints.
- [x] Route groups correctly enforce role permissions without leaking administrative UI components.
