# NoorHeroes Master Screen Mapping & System Synchronization Blueprint (Complete 562-Screen Specification)

## 1. Executive Summary & Purpose
This document serves as the **authoritative master registry and synchronization blueprint** connecting the **37 Product Requirements Documents (PRDs)**, the **711+ Development Blueprints**, and all **562 Screen Designs** across the NoorHeroes platform.

It is structured specifically for **autonomous AI coding agents** and human engineering teams to implement the application end-to-end from **UI/Visual Design → Screen Flow → API Integration → Data Handling → State Handling → Edge Cases** without ambiguity.

---

## 2. Universal Directives for AI Code Generation

### 2.1 Multi-Image Screen Cluster Rule (CRITICAL)
Many screens in the NoorHeroes design system are represented by a sequence of images (e.g., `Register-01.png` to `Register-03.png`, `04-Account & Security-01.png` to `04-Account & Security-09.png`, `28-Story Editor-01.png` to `28-Story Editor-14.png`).
> **MANDATORY INSTRUCTION FOR AI AGENTS:**
> When generating code for any screen or flow represented by multiple images, the AI agent **MUST read and inspect ALL images in that cluster collectively** before generating any code.
> The agent must **NOT** implement the screen based on a single image alone. It must synthesize all visual states (initial layout, active inputs, validation errors, open modals, step transitions, and completion states) into a single cohesive, production-ready component and ViewModel/State machine.

### 2.2 Strict Technology Stack Preservation
- **Mobile Application**: Kotlin Multiplatform (KMP), Compose Multiplatform (Desktop/Android/iOS), **Material Design 3 (M3)**, Koin (DI), Decompose / Voyager navigation, Ktor Client, SQLDelight / Room, Coil3 image loader.
- **Admin Web Portal**: Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui, TanStack Query (React Query v5), Zustand, React Hook Form + Zod, Lucide React icons.
- **Parent Web Portal**: Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui, TanStack Query, Zustand, React Hook Form + Zod.
- **Backend API Layer**: Python 3.11+, FastAPI, SQLAlchemy 2.0 (Async), Alembic, Pydantic v2 Settings/Schemas, Redis 7 (Cache, Sliding-Window Rate Limiting, Celery broker), PostgreSQL 16, Celery.

### 2.3 Comprehensive Screen State Machine Requirement
Every screen implementation must handle 5 fundamental UI states:
1. **Loading State**: Initial shimmer/skeleton loaders matching the exact visual card layout.
2. **Success / Populated State**: Full data binding with proper fluid typography, RTL layout mirroring where applicable, and responsive wrapping.
3. **Empty State**: Explicit empty state cards with themed illustrations, clear messaging, and primary call-to-action (CTA).
4. **Error State**: Non-blocking banner / toast or full-screen error with localized error message and explicit "Retry" button.
5. **Action / Mutation Loading**: Disabled buttons with embedded spinners and debounce protection against double-taps.

---

## 3. Master Screen Inventory & Platform Breakdown (562 Screens Total)

| Platform | Screen Directory | Image Count | Primary PRD Feature |
|---|---|---|---|
| **Mobile App** | `Screens/Mobile App/Avatar/` | 6 | Feature A12: Avatar System |
| **Mobile App** | `Screens/Mobile App/Bedtime Audio/` | 3 | Feature A4: Audio & Bedtime Player |
| **Mobile App** | `Screens/Mobile App/Child Management/` | 13 | Feature C21: Multi-Child Management |
| **Mobile App** | `Screens/Mobile App/Child Profile/` | 8 | Feature B16: Child Profile |
| **Mobile App** | `Screens/Mobile App/Child Reports/` | 16 | Feature C22: Per-Child Reports |
| **Mobile App** | `Screens/Mobile App/Du'as/` | 14 | Feature A6: Dua Learning |
| **Mobile App** | `Screens/Mobile App/Facts/` | 8 | Feature B18: Islamic Facts Module |
| **Mobile App** | `Screens/Mobile App/Favorites/` | 9 | Feature B14: Favorites |
| **Mobile App** | `Screens/Mobile App/Games/` | 8 | Feature A10: Games Module |
| **Mobile App** | `Screens/Mobile App/Habits/` | 6 | Feature A7: Habit Tracker |
| **Mobile App** | `Screens/Mobile App/Home/` | 15 | Feature A2: Home Dashboard & AI Personalization |
| **Mobile App** | `Screens/Mobile App/Learn/` | 11 | Feature A5: Quran/Arabic & Feature A9: Skill Tree |
| **Mobile App** | `Screens/Mobile App/Notifications/` | 14 | Feature B17: Child Notifications & Feature C25 |
| **Mobile App** | `Screens/Mobile App/Onboarding/` | 13 | Feature A1: Splash, Auth & Onboarding |
| **Mobile App** | `Screens/Mobile App/Parent Area/` | 13 | Feature C19: PIN Gate & Feature C20: Parent Dashboard |
| **Mobile App** | `Screens/Mobile App/Parental Controls/` | 21 | Feature C23: Parental Controls |
| **Mobile App** | `Screens/Mobile App/Privacy/` | 14 | Feature C26: Privacy, Consent & Account Security |
| **Mobile App** | `Screens/Mobile App/Quiz Engine/` | 13 | Feature A8: Daily Quiz Engine |
| **Mobile App** | `Screens/Mobile App/Ramadan Mode/` | 21 | Feature F36: Ramadan Mode (Mobile) |
| **Mobile App** | `Screens/Mobile App/Rewards/` | 18 | Feature A11: Rewards System |
| **Mobile App** | `Screens/Mobile App/Search/` | 5 | Feature B13: Search & Discovery |
| **Mobile App** | `Screens/Mobile App/Stories/` | 14 | Feature A3: Stories Module |
| **Mobile App** | `Screens/Mobile App/Subscription/` | 17 | Feature C24: Subscription & Billing |
| **Mobile App** | `Screens/Mobile App/Support/` | 9 | Feature C25: Notifications & Parent Support |
| **Parent Web** | `Screens/Parent Web/` | 46 | Feature D27: Parent Web Account Portal |
| **Admin Web** | `Screens/Admin Web/` (Root 01-110) | 220 | Features E28, E29, E30, E31, E32, E33, E34 |
| **Admin Web** | `Screens/Admin Web/Ramadan Mode/` | 7 | Feature F36: Ramadan Mode Admin Console |
| **TOTAL** | **All Platforms** | **562** | **37 PRD Features Completely Covered** |

---

## 4. Complete Exhaustive Screen-by-Screen Table (All 562 Exact File Paths)

| # | Exact Screen Image File Path | Platform | Feature & PRD Document | Screen Description & UI State | API Endpoint(s) |
|---|---|---|---|---|---|
| 001 | `Screens/Admin Web/01-login.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 01 login | `GET /v1/admin/*, POST /v1/admin/*` |
| 002 | `Screens/Admin Web/02-Two-Factor Authentication.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 02 Two Factor Authentication | `GET /v1/admin/*, POST /v1/admin/*` |
| 003 | `Screens/Admin Web/03-Two-Factor Verification.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 03 Two Factor Verification | `GET /v1/admin/*, POST /v1/admin/*` |
| 004 | `Screens/Admin Web/04-Account Recovery.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 04 Account Recovery | `GET /v1/admin/*, POST /v1/admin/*` |
| 005 | `Screens/Admin Web/05-Operations Dashboard-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 05 Operations Dashboard 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 006 | `Screens/Admin Web/05-Operations Dashboard-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 05 Operations Dashboard 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 007 | `Screens/Admin Web/06.1-Incidents.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 06.1 Incidents | `GET /v1/admin/*, POST /v1/admin/*` |
| 008 | `Screens/Admin Web/06.2-Incidents-Media CDN — Elevated Latency.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 06.2 Incidents Media CDN — Elevated Latency | `GET /v1/admin/*, POST /v1/admin/*` |
| 009 | `Screens/Admin Web/07-Service Health.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 07 Service Health | `GET /v1/admin/*, POST /v1/admin/*` |
| 010 | `Screens/Admin Web/08-Job Failures.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 08 Job Failures | `GET /v1/admin/*, POST /v1/admin/*` |
| 011 | `Screens/Admin Web/09-User Management — Search-01.png` | Admin Web | Feature B13 (Search & Discovery) | 09 User Management — Search 01 | `GET /admin/v1/search, GET /admin/v1/search/index-health, GET /admin/v1/search/zero-result-report` |
| 012 | `Screens/Admin Web/09-User Management — Search-02.png` | Admin Web | Feature B13 (Search & Discovery) | 09 User Management — Search 02 | `GET /admin/v1/search, GET /admin/v1/search/voice-quality, GET /admin/v1/search/rejected-items` |
| 013 | `Screens/Admin Web/10-Unmask Approval Queue.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 10 Unmask Approval Queue | `GET /v1/admin/*, POST /v1/admin/*` |
| 014 | `Screens/Admin Web/100-Feature Flag Change reject.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 100 Feature Flag Change reject | `GET /v1/admin/*, POST /v1/admin/*` |
| 015 | `Screens/Admin Web/101-Audit Log.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 101 Audit Log | `GET /v1/admin/*, POST /v1/admin/*` |
| 016 | `Screens/Admin Web/102-App Configuration-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 102 App Configuration 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 017 | `Screens/Admin Web/102-App Configuration-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 102 App Configuration 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 018 | `Screens/Admin Web/103-String Table Editor-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 103 String Table Editor 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 019 | `Screens/Admin Web/103-String Table Editor-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 103 String Table Editor 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 020 | `Screens/Admin Web/103-String Table Editor-03.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 103 String Table Editor 03 | `GET /v1/admin/*, POST /v1/admin/*` |
| 021 | `Screens/Admin Web/104-String table String Detail-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 104 String table String Detail 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 022 | `Screens/Admin Web/104-String table String Detail-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 104 String table String Detail 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 023 | `Screens/Admin Web/105-Translation Coverage Dashboard-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 105 Translation Coverage Dashboard 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 024 | `Screens/Admin Web/105-Translation Coverage Dashboard-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 105 Translation Coverage Dashboard 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 025 | `Screens/Admin Web/106-RTL Preview.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 106 RTL Preview | `GET /v1/admin/*, POST /v1/admin/*` |
| 026 | `Screens/Admin Web/107-Locale Activation- Urdu (ur).png` | Admin Web | Features E28–E34 (Admin Web Portal) | 107 Locale Activation  Urdu (ur) | `GET /v1/admin/*, POST /v1/admin/*` |
| 027 | `Screens/Admin Web/108-Locale List-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 108 Locale List 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 028 | `Screens/Admin Web/108-Locale List-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 108 Locale List 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 029 | `Screens/Admin Web/109-Locale Chain Configuration.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 109 Locale Chain Configuration | `GET /v1/admin/*, POST /v1/admin/*` |
| 030 | `Screens/Admin Web/11-Unmask Request Review-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 11 Unmask Request Review 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 031 | `Screens/Admin Web/11-Unmask Request Review-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 11 Unmask Request Review 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 032 | `Screens/Admin Web/110-Coverage-Drop Alert Monitor.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 110 Coverage Drop Alert Monitor | `GET /v1/admin/*, POST /v1/admin/*` |
| 033 | `Screens/Admin Web/12-Unmask Request Review-request-reject.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 12 Unmask Request Review request reject | `GET /v1/admin/*, POST /v1/admin/*` |
| 034 | `Screens/Admin Web/13-Unmask Request Review-request-approved.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 13 Unmask Request Review request approved | `GET /v1/admin/*, POST /v1/admin/*` |
| 035 | `Screens/Admin Web/14-Operator Accounts.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 14 Operator Accounts | `GET /v1/admin/*, POST /v1/admin/*` |
| 036 | `Screens/Admin Web/15-Provision Operator Account-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 15 Provision Operator Account 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 037 | `Screens/Admin Web/15-Provision Operator Account-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 15 Provision Operator Account 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 038 | `Screens/Admin Web/15-Provision Operator Account-03.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 15 Provision Operator Account 03 | `GET /v1/admin/*, POST /v1/admin/*` |
| 039 | `Screens/Admin Web/15-Provision Operator Account-04.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 15 Provision Operator Account 04 | `GET /v1/admin/*, POST /v1/admin/*` |
| 040 | `Screens/Admin Web/16-Support Case Queue-01.png` | Admin Web | Feature C25 (Notifications & Support) | 16 Support Case Queue 01 | `GET /v1/support/tickets, POST /v1/support/tickets` |
| 041 | `Screens/Admin Web/16-Support Case Queue-02.png` | Admin Web | Feature C25 (Notifications & Support) | 16 Support Case Queue 02 | `GET /v1/support/tickets, POST /v1/support/tickets` |
| 042 | `Screens/Admin Web/17-Support Case Queue-01.png` | Admin Web | Feature C25 (Notifications & Support) | 17 Support Case Queue 01 | `GET /v1/support/tickets, POST /v1/support/tickets` |
| 043 | `Screens/Admin Web/17-Support Case Queue-02.png` | Admin Web | Feature C25 (Notifications & Support) | 17 Support Case Queue 02 | `GET /v1/support/tickets, POST /v1/support/tickets` |
| 044 | `Screens/Admin Web/17-Support Case Queue-03.png` | Admin Web | Feature C25 (Notifications & Support) | 17 Support Case Queue 03 | `GET /v1/support/tickets, POST /v1/support/tickets` |
| 045 | `Screens/Admin Web/18-View Parent Account Detail-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 18 View Parent Account Detail 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 046 | `Screens/Admin Web/18-View Parent Account Detail-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 18 View Parent Account Detail 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 047 | `Screens/Admin Web/18-View Parent Account Detail-03.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 18 View Parent Account Detail 03 | `GET /v1/admin/*, POST /v1/admin/*` |
| 048 | `Screens/Admin Web/18-View Parent Account Detail-04.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 18 View Parent Account Detail 04 | `GET /v1/admin/*, POST /v1/admin/*` |
| 049 | `Screens/Admin Web/18-View Parent Account Detail-05.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 18 View Parent Account Detail 05 | `GET /v1/admin/*, POST /v1/admin/*` |
| 050 | `Screens/Admin Web/19-Unmask Request Submission-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 19 Unmask Request Submission 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 051 | `Screens/Admin Web/19-Unmask Request Submission-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 19 Unmask Request Submission 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 052 | `Screens/Admin Web/19-Unmask Request Submission-03.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 19 Unmask Request Submission 03 | `GET /v1/admin/*, POST /v1/admin/*` |
| 053 | `Screens/Admin Web/20-Inspect Entitlements.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 20 Inspect Entitlements | `GET /v1/admin/*, POST /v1/admin/*` |
| 054 | `Screens/Admin Web/21-Edit Support-Safe Metadata-01.png` | Admin Web | Feature C25 (Notifications & Support) | 21 Edit Support Safe Metadata 01 | `GET /v1/support/tickets, POST /v1/support/tickets` |
| 055 | `Screens/Admin Web/21-Edit Support-Safe Metadata-02.png` | Admin Web | Feature C25 (Notifications & Support) | 21 Edit Support Safe Metadata 02 | `GET /v1/support/tickets, POST /v1/support/tickets` |
| 056 | `Screens/Admin Web/21-Edit Support-Safe Metadata-03.png` | Admin Web | Feature C25 (Notifications & Support) | 21 Edit Support Safe Metadata 03 | `GET /v1/support/tickets, POST /v1/support/tickets` |
| 057 | `Screens/Admin Web/22-Initiate Account Recovery-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 22 Initiate Account Recovery 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 058 | `Screens/Admin Web/22-Initiate Account Recovery-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 22 Initiate Account Recovery 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 059 | `Screens/Admin Web/23-Initiate Account Recovery-03.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 23 Initiate Account Recovery 03 | `GET /v1/admin/*, POST /v1/admin/*` |
| 060 | `Screens/Admin Web/24-Child Safety View-Full History.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 24 Child Safety View Full History | `GET /v1/admin/*, POST /v1/admin/*` |
| 061 | `Screens/Admin Web/24-Child Safety View.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 24 Child Safety View | `GET /v1/admin/*, POST /v1/admin/*` |
| 062 | `Screens/Admin Web/25-Child Safety View-Full History.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 25 Child Safety View Full History | `GET /v1/admin/*, POST /v1/admin/*` |
| 063 | `Screens/Admin Web/26-Legacy Admin Users.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 26 Legacy Admin Users | `GET /v1/admin/*, POST /v1/admin/*` |
| 064 | `Screens/Admin Web/27-Content Library.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 27 Content Library | `GET /v1/admin/*, POST /v1/admin/*` |
| 065 | `Screens/Admin Web/28-Story Editor-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 28 Story Editor 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 066 | `Screens/Admin Web/28-Story Editor-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 28 Story Editor 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 067 | `Screens/Admin Web/28-Story Editor-03.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 28 Story Editor 03 | `GET /v1/admin/*, POST /v1/admin/*` |
| 068 | `Screens/Admin Web/28-Story Editor-04.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 28 Story Editor 04 | `GET /v1/admin/*, POST /v1/admin/*` |
| 069 | `Screens/Admin Web/28-Story Editor-05.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 28 Story Editor 05 | `GET /v1/admin/*, POST /v1/admin/*` |
| 070 | `Screens/Admin Web/28-Story Editor-06.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 28 Story Editor 06 | `GET /v1/admin/*, POST /v1/admin/*` |
| 071 | `Screens/Admin Web/28-Story Editor-07.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 28 Story Editor 07 | `GET /v1/admin/*, POST /v1/admin/*` |
| 072 | `Screens/Admin Web/28-Story Editor-08.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 28 Story Editor 08 | `GET /v1/admin/*, POST /v1/admin/*` |
| 073 | `Screens/Admin Web/28-Story Editor-09.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 28 Story Editor 09 | `GET /v1/admin/*, POST /v1/admin/*` |
| 074 | `Screens/Admin Web/28-Story Editor-10.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 28 Story Editor 10 | `GET /v1/admin/*, POST /v1/admin/*` |
| 075 | `Screens/Admin Web/28-Story Editor-11.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 28 Story Editor 11 | `GET /v1/admin/*, POST /v1/admin/*` |
| 076 | `Screens/Admin Web/28-Story Editor-12.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 28 Story Editor 12 | `GET /v1/admin/*, POST /v1/admin/*` |
| 077 | `Screens/Admin Web/28-Story Editor-13.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 28 Story Editor 13 | `GET /v1/admin/*, POST /v1/admin/*` |
| 078 | `Screens/Admin Web/28-Story Editor-14.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 28 Story Editor 14 | `GET /v1/admin/*, POST /v1/admin/*` |
| 079 | `Screens/Admin Web/29-Story Editor-upload media-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 29 Story Editor upload media 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 080 | `Screens/Admin Web/29-Story Editor-upload media-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 29 Story Editor upload media 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 081 | `Screens/Admin Web/29-Story Editor-upload media-03.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 29 Story Editor upload media 03 | `GET /v1/admin/*, POST /v1/admin/*` |
| 082 | `Screens/Admin Web/29-Story Editor-upload media-04.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 29 Story Editor upload media 04 | `GET /v1/admin/*, POST /v1/admin/*` |
| 083 | `Screens/Admin Web/29-Story Editor-upload media-05.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 29 Story Editor upload media 05 | `GET /v1/admin/*, POST /v1/admin/*` |
| 084 | `Screens/Admin Web/30-Story Editor-version-history-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 30 Story Editor version history 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 085 | `Screens/Admin Web/30-Story Editor-version-history-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 30 Story Editor version history 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 086 | `Screens/Admin Web/31-Quiz Builder.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 31 Quiz Builder | `GET /v1/admin/*, POST /v1/admin/*` |
| 087 | `Screens/Admin Web/32-Question Editor-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 32 Question Editor 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 088 | `Screens/Admin Web/32-Question Editor-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 32 Question Editor 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 089 | `Screens/Admin Web/32-Question Editor-03.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 32 Question Editor 03 | `GET /v1/admin/*, POST /v1/admin/*` |
| 090 | `Screens/Admin Web/32-Question Editor-04.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 32 Question Editor 04 | `GET /v1/admin/*, POST /v1/admin/*` |
| 091 | `Screens/Admin Web/33-Quiz Preview.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 33 Quiz Preview | `GET /v1/admin/*, POST /v1/admin/*` |
| 092 | `Screens/Admin Web/34-Media Library.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 34 Media Library | `GET /v1/admin/*, POST /v1/admin/*` |
| 093 | `Screens/Admin Web/35-Quran Proposal-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 35 Quran Proposal 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 094 | `Screens/Admin Web/35-Quran Proposal-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 35 Quran Proposal 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 095 | `Screens/Admin Web/35-Quran Proposal-03.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 35 Quran Proposal 03 | `GET /v1/admin/*, POST /v1/admin/*` |
| 096 | `Screens/Admin Web/36-Quran Scholar Review.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 36 Quran Scholar Review | `GET /v1/admin/*, POST /v1/admin/*` |
| 097 | `Screens/Admin Web/37-Reward:XP Rule-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 37 Reward:XP Rule 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 098 | `Screens/Admin Web/37-Reward:XP Rule-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 37 Reward:XP Rule 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 099 | `Screens/Admin Web/38-Scholar Review Queue.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 38 Scholar Review Queue | `GET /v1/admin/*, POST /v1/admin/*` |
| 100 | `Screens/Admin Web/39-Scholar Queue-accuracy review-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 39 Scholar Queue accuracy review 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 101 | `Screens/Admin Web/39-Scholar Queue-accuracy review-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 39 Scholar Queue accuracy review 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 102 | `Screens/Admin Web/40-Scholar Queue-accuracy review-confirm review.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 40 Scholar Queue accuracy review confirm review | `GET /v1/admin/*, POST /v1/admin/*` |
| 103 | `Screens/Admin Web/41-Scholar Queue-accuracy review decision recorded.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 41 Scholar Queue accuracy review decision recorded | `GET /v1/admin/*, POST /v1/admin/*` |
| 104 | `Screens/Admin Web/42-Scholar Queue-accuracy review version history.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 42 Scholar Queue accuracy review version history | `GET /v1/admin/*, POST /v1/admin/*` |
| 105 | `Screens/Admin Web/43-Child-Safety Queue.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 43 Child Safety Queue | `GET /v1/admin/*, POST /v1/admin/*` |
| 106 | `Screens/Admin Web/44-Child-Safety queue review.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 44 Child Safety queue review | `GET /v1/admin/*, POST /v1/admin/*` |
| 107 | `Screens/Admin Web/45-Child-Safety queue review passed.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 45 Child Safety queue review passed | `GET /v1/admin/*, POST /v1/admin/*` |
| 108 | `Screens/Admin Web/46-AI Moderation Queue-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 46 AI Moderation Queue 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 109 | `Screens/Admin Web/46-AI Moderation Queue-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 46 AI Moderation Queue 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 110 | `Screens/Admin Web/47-AI Moderation Flagged Interaction-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 47 AI Moderation Flagged Interaction 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 111 | `Screens/Admin Web/47-AI Moderation Flagged Interaction-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 47 AI Moderation Flagged Interaction 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 112 | `Screens/Admin Web/47-AI Moderation Flagged Interaction-03.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 47 AI Moderation Flagged Interaction 03 | `GET /v1/admin/*, POST /v1/admin/*` |
| 113 | `Screens/Admin Web/47-AI Moderation Flagged Interaction-04.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 47 AI Moderation Flagged Interaction 04 | `GET /v1/admin/*, POST /v1/admin/*` |
| 114 | `Screens/Admin Web/47-AI Moderation Flagged Interaction-05.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 47 AI Moderation Flagged Interaction 05 | `GET /v1/admin/*, POST /v1/admin/*` |
| 115 | `Screens/Admin Web/47-AI Moderation Flagged Interaction-06.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 47 AI Moderation Flagged Interaction 06 | `GET /v1/admin/*, POST /v1/admin/*` |
| 116 | `Screens/Admin Web/47-AI Moderation Flagged Interaction-07.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 47 AI Moderation Flagged Interaction 07 | `GET /v1/admin/*, POST /v1/admin/*` |
| 117 | `Screens/Admin Web/47-AI Moderation Flagged Interaction-08.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 47 AI Moderation Flagged Interaction 08 | `GET /v1/admin/*, POST /v1/admin/*` |
| 118 | `Screens/Admin Web/48-AI Moderation Flagged Content Gap Escalation.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 48 AI Moderation Flagged Content Gap Escalation | `GET /v1/admin/*, POST /v1/admin/*` |
| 119 | `Screens/Admin Web/49-AI Moderation Content Gap escalation submit.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 49 AI Moderation Content Gap escalation submit | `GET /v1/admin/*, POST /v1/admin/*` |
| 120 | `Screens/Admin Web/50-AI Moderation flagged evaluation case .png` | Admin Web | Features E28–E34 (Admin Web Portal) | 50 AI Moderation flagged evaluation case  | `GET /v1/admin/*, POST /v1/admin/*` |
| 121 | `Screens/Admin Web/51-AI Moderation Full Transcript View-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 51 AI Moderation Full Transcript View 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 122 | `Screens/Admin Web/51-AI Moderation Full Transcript View-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 51 AI Moderation Full Transcript View 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 123 | `Screens/Admin Web/52-Editorial Review Queue.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 52 Editorial Review Queue | `GET /v1/admin/*, POST /v1/admin/*` |
| 124 | `Screens/Admin Web/53-Scholar Review Queue.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 53 Scholar Review Queue | `GET /v1/admin/*, POST /v1/admin/*` |
| 125 | `Screens/Admin Web/54-Seasonal Calendar.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 54 Seasonal Calendar | `GET /v1/admin/*, POST /v1/admin/*` |
| 126 | `Screens/Admin Web/55-Habit Templates.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 55 Habit Templates | `GET /v1/admin/*, POST /v1/admin/*` |
| 127 | `Screens/Admin Web/56-Habit Template Editor-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 56 Habit Template Editor 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 128 | `Screens/Admin Web/56-Habit Template Editor-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 56 Habit Template Editor 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 129 | `Screens/Admin Web/56-Habit Template Editor-03.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 56 Habit Template Editor 03 | `GET /v1/admin/*, POST /v1/admin/*` |
| 130 | `Screens/Admin Web/56-Habit Template Editor-04.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 56 Habit Template Editor 04 | `GET /v1/admin/*, POST /v1/admin/*` |
| 131 | `Screens/Admin Web/57-Seasonal Habit Set Builder-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 57 Seasonal Habit Set Builder 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 132 | `Screens/Admin Web/57-Seasonal Habit Set Builder-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 57 Seasonal Habit Set Builder 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 133 | `Screens/Admin Web/58-Challenge Management.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 58 Challenge Management | `GET /v1/admin/*, POST /v1/admin/*` |
| 134 | `Screens/Admin Web/59-Weekly Challenge Builder-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 59 Weekly Challenge Builder 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 135 | `Screens/Admin Web/59-Weekly Challenge Builder-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 59 Weekly Challenge Builder 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 136 | `Screens/Admin Web/59-Weekly Challenge Builder-03.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 59 Weekly Challenge Builder 03 | `GET /v1/admin/*, POST /v1/admin/*` |
| 137 | `Screens/Admin Web/59-Weekly Challenge Builder-04.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 59 Weekly Challenge Builder 04 | `GET /v1/admin/*, POST /v1/admin/*` |
| 138 | `Screens/Admin Web/60-Challenge Calendar.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 60 Challenge Calendar | `GET /v1/admin/*, POST /v1/admin/*` |
| 139 | `Screens/Admin Web/61-Reward Management — XP Rules.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 61 Reward Management — XP Rules | `GET /v1/admin/*, POST /v1/admin/*` |
| 140 | `Screens/Admin Web/62-XP Rule Editor-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 62 XP Rule Editor 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 141 | `Screens/Admin Web/62-XP Rule Editor-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 62 XP Rule Editor 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 142 | `Screens/Admin Web/63-Reward Ledger Viewer-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 63 Reward Ledger Viewer 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 143 | `Screens/Admin Web/63-Reward Ledger Viewer-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 63 Reward Ledger Viewer 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 144 | `Screens/Admin Web/64-Manual Reward Grant-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 64 Manual Reward Grant 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 145 | `Screens/Admin Web/64-Manual Reward Grant-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 64 Manual Reward Grant 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 146 | `Screens/Admin Web/64-Manual Reward Grant-03.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 64 Manual Reward Grant 03 | `GET /v1/admin/*, POST /v1/admin/*` |
| 147 | `Screens/Admin Web/64-Manual Reward Grant-04.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 64 Manual Reward Grant 04 | `GET /v1/admin/*, POST /v1/admin/*` |
| 148 | `Screens/Admin Web/65-Badge Library.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 65 Badge Library | `GET /v1/admin/*, POST /v1/admin/*` |
| 149 | `Screens/Admin Web/66-Badge Criteria Builder-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 66 Badge Criteria Builder 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 150 | `Screens/Admin Web/66-Badge Criteria Builder-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 66 Badge Criteria Builder 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 151 | `Screens/Admin Web/66-Badge Criteria Builder-03.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 66 Badge Criteria Builder 03 | `GET /v1/admin/*, POST /v1/admin/*` |
| 152 | `Screens/Admin Web/66-Badge Criteria Builder-04.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 66 Badge Criteria Builder 04 | `GET /v1/admin/*, POST /v1/admin/*` |
| 153 | `Screens/Admin Web/67-Avatar Management.png` | Admin Web | Feature A12 (Avatar System) | 67 Avatar Management | `GET /v1/avatar/inventory, PUT /v1/avatar/equipped` |
| 154 | `Screens/Admin Web/68-Avatar Item Catalog.png` | Admin Web | Feature A12 (Avatar System) | 68 Avatar Item Catalog | `GET /v1/avatar/inventory, PUT /v1/avatar/equipped` |
| 155 | `Screens/Admin Web/69-Avatar Item Editor-01.png` | Admin Web | Feature A12 (Avatar System) | 69 Avatar Item Editor 01 | `GET /v1/avatar/inventory, PUT /v1/avatar/equipped` |
| 156 | `Screens/Admin Web/69-Avatar Item Editor-02.png` | Admin Web | Feature A12 (Avatar System) | 69 Avatar Item Editor 02 | `GET /v1/avatar/inventory, PUT /v1/avatar/equipped` |
| 157 | `Screens/Admin Web/69-Avatar Item Editor-03.png` | Admin Web | Feature A12 (Avatar System) | 69 Avatar Item Editor 03 | `GET /v1/avatar/inventory, PUT /v1/avatar/equipped` |
| 158 | `Screens/Admin Web/69-Avatar Item Editor-04.png` | Admin Web | Feature A12 (Avatar System) | 69 Avatar Item Editor 04 | `GET /v1/avatar/inventory, PUT /v1/avatar/equipped` |
| 159 | `Screens/Admin Web/69-Avatar Item Editor-05.png` | Admin Web | Feature A12 (Avatar System) | 69 Avatar Item Editor 05 | `GET /v1/avatar/inventory, PUT /v1/avatar/equipped` |
| 160 | `Screens/Admin Web/69-Avatar Item Editor-06.png` | Admin Web | Feature A12 (Avatar System) | 69 Avatar Item Editor 06 | `GET /v1/avatar/inventory, PUT /v1/avatar/equipped` |
| 161 | `Screens/Admin Web/69-Avatar Item Editor-07.png` | Admin Web | Feature A12 (Avatar System) | 69 Avatar Item Editor 07 | `GET /v1/avatar/inventory, PUT /v1/avatar/equipped` |
| 162 | `Screens/Admin Web/69-Avatar Item Editor-08.png` | Admin Web | Feature A12 (Avatar System) | 69 Avatar Item Editor 08 | `GET /v1/avatar/inventory, PUT /v1/avatar/equipped` |
| 163 | `Screens/Admin Web/70-Avatar Ownership Distribution.png` | Admin Web | Feature A12 (Avatar System) | 70 Avatar Ownership Distribution | `GET /v1/avatar/inventory, PUT /v1/avatar/equipped` |
| 164 | `Screens/Admin Web/71-Notification Templates.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 71 Notification Templates | `GET /v1/admin/*, POST /v1/admin/*` |
| 165 | `Screens/Admin Web/72-Notification Template Editor-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 72 Notification Template Editor 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 166 | `Screens/Admin Web/72-Notification Template Editor-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 72 Notification Template Editor 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 167 | `Screens/Admin Web/72-Notification Template Editor-03.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 72 Notification Template Editor 03 | `GET /v1/admin/*, POST /v1/admin/*` |
| 168 | `Screens/Admin Web/72-Notification Template Editor-04.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 72 Notification Template Editor 04 | `GET /v1/admin/*, POST /v1/admin/*` |
| 169 | `Screens/Admin Web/72-Notification Template Editor-05.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 72 Notification Template Editor 05 | `GET /v1/admin/*, POST /v1/admin/*` |
| 170 | `Screens/Admin Web/72-Notification Template Editor-06.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 72 Notification Template Editor 06 | `GET /v1/admin/*, POST /v1/admin/*` |
| 171 | `Screens/Admin Web/73-Campaign Scheduler-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 73 Campaign Scheduler 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 172 | `Screens/Admin Web/73-Campaign Scheduler-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 73 Campaign Scheduler 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 173 | `Screens/Admin Web/73-Campaign Scheduler-03.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 73 Campaign Scheduler 03 | `GET /v1/admin/*, POST /v1/admin/*` |
| 174 | `Screens/Admin Web/73-Campaign Scheduler-04.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 73 Campaign Scheduler 04 | `GET /v1/admin/*, POST /v1/admin/*` |
| 175 | `Screens/Admin Web/73-Campaign Scheduler-05.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 73 Campaign Scheduler 05 | `GET /v1/admin/*, POST /v1/admin/*` |
| 176 | `Screens/Admin Web/73-Campaign Scheduler-06.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 73 Campaign Scheduler 06 | `GET /v1/admin/*, POST /v1/admin/*` |
| 177 | `Screens/Admin Web/73-Campaign Scheduler-07.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 73 Campaign Scheduler 07 | `GET /v1/admin/*, POST /v1/admin/*` |
| 178 | `Screens/Admin Web/74-Delivery Report.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 74 Delivery Report | `GET /v1/admin/*, POST /v1/admin/*` |
| 179 | `Screens/Admin Web/75-In-App Banner Management.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 75 In App Banner Management | `GET /v1/admin/*, POST /v1/admin/*` |
| 180 | `Screens/Admin Web/76-Banner Editor-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 76 Banner Editor 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 181 | `Screens/Admin Web/76-Banner Editor-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 76 Banner Editor 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 182 | `Screens/Admin Web/76-Banner Editor-03.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 76 Banner Editor 03 | `GET /v1/admin/*, POST /v1/admin/*` |
| 183 | `Screens/Admin Web/76-Banner Editor-04.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 76 Banner Editor 04 | `GET /v1/admin/*, POST /v1/admin/*` |
| 184 | `Screens/Admin Web/77-Coupon Management.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 77 Coupon Management | `GET /v1/admin/*, POST /v1/admin/*` |
| 185 | `Screens/Admin Web/78-Coupon Editor-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 78 Coupon Editor 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 186 | `Screens/Admin Web/78-Coupon Editor-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 78 Coupon Editor 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 187 | `Screens/Admin Web/78-Coupon Editor-03.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 78 Coupon Editor 03 | `GET /v1/admin/*, POST /v1/admin/*` |
| 188 | `Screens/Admin Web/78-Coupon Editor-04.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 78 Coupon Editor 04 | `GET /v1/admin/*, POST /v1/admin/*` |
| 189 | `Screens/Admin Web/79-Coupon Redemption Report.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 79 Coupon Redemption Report | `GET /v1/admin/*, POST /v1/admin/*` |
| 190 | `Screens/Admin Web/80-Plan & Pricing Catalog-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 80 Plan & Pricing Catalog 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 191 | `Screens/Admin Web/80-Plan & Pricing Catalog-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 80 Plan & Pricing Catalog 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 192 | `Screens/Admin Web/81-Edit Plan-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 81 Edit Plan 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 193 | `Screens/Admin Web/81-Edit Plan-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 81 Edit Plan 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 194 | `Screens/Admin Web/81-Edit Plan-03.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 81 Edit Plan 03 | `GET /v1/admin/*, POST /v1/admin/*` |
| 195 | `Screens/Admin Web/82-Entitlement Matrix.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 82 Entitlement Matrix | `GET /v1/admin/*, POST /v1/admin/*` |
| 196 | `Screens/Admin Web/83-Subscription Search-01.png` | Admin Web | Feature B13 (Search & Discovery) | 83 Subscription Search 01 | `GET /admin/v1/search` |
| 197 | `Screens/Admin Web/83-Subscription Search-02.png` | Admin Web | Feature B13 (Search & Discovery) | 83 Subscription Search 02 | `GET /admin/v1/search` |
| 198 | `Screens/Admin Web/84-Reconciliation Log.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 84 Reconciliation Log | `GET /v1/admin/*, POST /v1/admin/*` |
| 199 | `Screens/Admin Web/85-Reconciliation Job Health-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 85 Reconciliation Job Health 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 200 | `Screens/Admin Web/85-Reconciliation Job Health-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 85 Reconciliation Job Health 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 201 | `Screens/Admin Web/86-Revenue Report.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 86 Revenue Report | `GET /v1/admin/*, POST /v1/admin/*` |
| 202 | `Screens/Admin Web/87-Evaluation Harness.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 87 Evaluation Harness | `GET /v1/admin/*, POST /v1/admin/*` |
| 203 | `Screens/Admin Web/88-Evaluation Run run-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 88 Evaluation Run run 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 204 | `Screens/Admin Web/88-Evaluation Run run-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 88 Evaluation Run run 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 205 | `Screens/Admin Web/89-Release Gate Decision.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 89 Release Gate Decision | `GET /v1/admin/*, POST /v1/admin/*` |
| 206 | `Screens/Admin Web/90-False-Positive Feedback Log.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 90 False Positive Feedback Log | `GET /v1/admin/*, POST /v1/admin/*` |
| 207 | `Screens/Admin Web/91-Model Version & Blocked Topics Registry.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 91 Model Version & Blocked Topics Registry | `GET /v1/admin/*, POST /v1/admin/*` |
| 208 | `Screens/Admin Web/92-Model Deployed .png` | Admin Web | Features E28–E34 (Admin Web Portal) | 92 Model Deployed  | `GET /v1/admin/*, POST /v1/admin/*` |
| 209 | `Screens/Admin Web/93-Active Kill Switches-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 93 Active Kill Switches 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 210 | `Screens/Admin Web/93-Active Kill Switches-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 93 Active Kill Switches 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 211 | `Screens/Admin Web/93-Active Kill Switches-03.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 93 Active Kill Switches 03 | `GET /v1/admin/*, POST /v1/admin/*` |
| 212 | `Screens/Admin Web/94-Feature Flags.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 94 Feature Flags | `GET /v1/admin/*, POST /v1/admin/*` |
| 213 | `Screens/Admin Web/95-Roles & Permissions-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 95 Roles & Permissions 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 214 | `Screens/Admin Web/95-Roles & Permissions-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 95 Roles & Permissions 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 215 | `Screens/Admin Web/96-Permission Matrix Super Admin-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 96 Permission Matrix Super Admin 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 216 | `Screens/Admin Web/96-Permission Matrix Super Admin-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 96 Permission Matrix Super Admin 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 217 | `Screens/Admin Web/97-Maker-Checker Approval Queue-01.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 97 Maker Checker Approval Queue 01 | `GET /v1/admin/*, POST /v1/admin/*` |
| 218 | `Screens/Admin Web/97-Maker-Checker Approval Queue-02.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 97 Maker Checker Approval Queue 02 | `GET /v1/admin/*, POST /v1/admin/*` |
| 219 | `Screens/Admin Web/98-Feature Flag Change.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 98 Feature Flag Change | `GET /v1/admin/*, POST /v1/admin/*` |
| 220 | `Screens/Admin Web/99-Feature Flag Change approved.png` | Admin Web | Features E28–E34 (Admin Web Portal) | 99 Feature Flag Change approved | `GET /v1/admin/*, POST /v1/admin/*` |
| 221 | `Screens/Admin Web/Ramadan Mode/01-Campaign Manager.png` | Admin Web | Feature F36 (Ramadan Mode Admin) | 01 Campaign Manager | `GET /v1/admin/ramadan/campaign, PUT /v1/admin/ramadan/campaign` |
| 222 | `Screens/Admin Web/Ramadan Mode/02-30-Night Content .png` | Admin Web | Feature F36 (Ramadan Mode Admin) | 02 30 Night Content  | `GET /v1/admin/ramadan/campaign, PUT /v1/admin/ramadan/campaign` |
| 223 | `Screens/Admin Web/Ramadan Mode/03-Laylatul Qadr Set -01.png` | Admin Web | Feature F36 (Ramadan Mode Admin) | 03 Laylatul Qadr Set  01 | `GET /v1/admin/ramadan/campaign, PUT /v1/admin/ramadan/campaign` |
| 224 | `Screens/Admin Web/Ramadan Mode/03-Laylatul Qadr Set -02.png` | Admin Web | Feature F36 (Ramadan Mode Admin) | 03 Laylatul Qadr Set  02 | `GET /v1/admin/ramadan/campaign, PUT /v1/admin/ramadan/campaign` |
| 225 | `Screens/Admin Web/Ramadan Mode/04-Eid Package Manager.png` | Admin Web | Feature F36 (Ramadan Mode Admin) | 04 Eid Package Manager | `GET /v1/admin/ramadan/campaign, PUT /v1/admin/ramadan/campaign` |
| 226 | `Screens/Admin Web/Ramadan Mode/05-Analytics Dashboard.png` | Admin Web | Feature F36 (Ramadan Mode Admin) | 05 Analytics Dashboard | `GET /v1/admin/ramadan/campaign, PUT /v1/admin/ramadan/campaign` |
| 227 | `Screens/Admin Web/Ramadan Mode/06-Deadline Tracker.png` | Admin Web | Feature F36 (Ramadan Mode Admin) | 06 Deadline Tracker | `GET /v1/admin/ramadan/campaign, PUT /v1/admin/ramadan/campaign` |
| 228 | `Screens/Mobile App/Avatar/Avatar-01.png` | Mobile App | Feature A12 (Avatar System) | Avatar 01 | `GET /v1/avatar/inventory, PUT /v1/avatar/equipped` |
| 229 | `Screens/Mobile App/Avatar/Avatar-02.png` | Mobile App | Feature A12 (Avatar System) | Avatar 02 | `GET /v1/avatar/inventory, PUT /v1/avatar/equipped` |
| 230 | `Screens/Mobile App/Avatar/Avatar-03.png` | Mobile App | Feature A12 (Avatar System) | Avatar 03 | `GET /v1/avatar/inventory, PUT /v1/avatar/equipped` |
| 231 | `Screens/Mobile App/Avatar/Evolution.png` | Mobile App | Feature A12 (Avatar System) | Evolution | `GET /v1/avatar/inventory, PUT /v1/avatar/equipped` |
| 232 | `Screens/Mobile App/Avatar/Locked Item-01.png` | Mobile App | Feature A12 (Avatar System) | Locked Item 01 | `GET /v1/avatar/inventory, PUT /v1/avatar/equipped` |
| 233 | `Screens/Mobile App/Avatar/Locked Item-02.png` | Mobile App | Feature A12 (Avatar System) | Locked Item 02 | `GET /v1/avatar/inventory, PUT /v1/avatar/equipped` |
| 234 | `Screens/Mobile App/Bedtime Audio/Audio Player.png` | Mobile App | Feature A4 (Bedtime Audio) | Audio Player | `GET /v1/audio/bedtime/tracks` |
| 235 | `Screens/Mobile App/Bedtime Audio/Dua Card.png` | Mobile App | Feature A4 (Bedtime Audio) | Dua Card | `GET /v1/audio/bedtime/tracks` |
| 236 | `Screens/Mobile App/Bedtime Audio/Sleep Timer.png` | Mobile App | Feature A4 (Bedtime Audio) | Sleep Timer | `GET /v1/audio/bedtime/tracks` |
| 237 | `Screens/Mobile App/Child Management/Add:Edit Child-01.png` | Mobile App | Feature C21 (Multi-Child Management) | Add:Edit Child 01 | `GET /v1/identity/children, POST /v1/identity/children` |
| 238 | `Screens/Mobile App/Child Management/Add:Edit Child-02.png` | Mobile App | Feature C21 (Multi-Child Management) | Add:Edit Child 02 | `GET /v1/identity/children, POST /v1/identity/children` |
| 239 | `Screens/Mobile App/Child Management/Child Management-01.png` | Mobile App | Feature C21 (Multi-Child Management) | Child Management 01 | `GET /v1/identity/children, POST /v1/identity/children` |
| 240 | `Screens/Mobile App/Child Management/Child Management-02.png` | Mobile App | Feature C21 (Multi-Child Management) | Child Management 02 | `GET /v1/identity/children, POST /v1/identity/children` |
| 241 | `Screens/Mobile App/Child Management/Child Management-03.png` | Mobile App | Feature C21 (Multi-Child Management) | Child Management 03 | `GET /v1/identity/children, POST /v1/identity/children` |
| 242 | `Screens/Mobile App/Child Management/Child Management-04.png` | Mobile App | Feature C21 (Multi-Child Management) | Child Management 04 | `GET /v1/identity/children, POST /v1/identity/children` |
| 243 | `Screens/Mobile App/Child Management/Child Management-05.png` | Mobile App | Feature C21 (Multi-Child Management) | Child Management 05 | `GET /v1/identity/children, POST /v1/identity/children` |
| 244 | `Screens/Mobile App/Child Management/Child Management-06.png` | Mobile App | Feature C21 (Multi-Child Management) | Child Management 06 | `GET /v1/identity/children, POST /v1/identity/children` |
| 245 | `Screens/Mobile App/Child Management/Child Management-07.png` | Mobile App | Feature C21 (Multi-Child Management) | Child Management 07 | `GET /v1/identity/children, POST /v1/identity/children` |
| 246 | `Screens/Mobile App/Child Management/Delete Child Warning-01.png` | Mobile App | Feature C21 (Multi-Child Management) | Delete Child Warning 01 | `GET /v1/identity/children, POST /v1/identity/children` |
| 247 | `Screens/Mobile App/Child Management/Delete Child Warning-02.png` | Mobile App | Feature C21 (Multi-Child Management) | Delete Child Warning 02 | `GET /v1/identity/children, POST /v1/identity/children` |
| 248 | `Screens/Mobile App/Child Management/Delete Child Warning-03.png` | Mobile App | Feature C21 (Multi-Child Management) | Delete Child Warning 03 | `GET /v1/identity/children, POST /v1/identity/children` |
| 249 | `Screens/Mobile App/Child Management/Delete Child Warning-04.png` | Mobile App | Feature C21 (Multi-Child Management) | Delete Child Warning 04 | `GET /v1/identity/children, POST /v1/identity/children` |
| 250 | `Screens/Mobile App/Child Profile/Child Profile-01.png` | Mobile App | Feature B16 (Child Profile) | Child Profile 01 | `GET /v1/children/{id}/progress, PATCH /v1/children/{id}/preferences` |
| 251 | `Screens/Mobile App/Child Profile/Child Profile-02.png` | Mobile App | Feature B16 (Child Profile) | Child Profile 02 | `GET /v1/children/{id}/progress, PATCH /v1/children/{id}/preferences` |
| 252 | `Screens/Mobile App/Child Profile/Child Profile-03.png` | Mobile App | Feature B16 (Child Profile) | Child Profile 03 | `GET /v1/children/{id}/progress, PATCH /v1/children/{id}/preferences` |
| 253 | `Screens/Mobile App/Child Profile/Child Profile-04.png` | Mobile App | Feature B16 (Child Profile) | Child Profile 04 | `GET /v1/children/{id}/progress, PATCH /v1/children/{id}/preferences` |
| 254 | `Screens/Mobile App/Child Profile/Child Profile-05.png` | Mobile App | Feature B16 (Child Profile) | Child Profile 05 | `GET /v1/children/{id}/progress, PATCH /v1/children/{id}/preferences` |
| 255 | `Screens/Mobile App/Child Profile/Child Profile-06.png` | Mobile App | Feature B16 (Child Profile) | Child Profile 06 | `GET /v1/children/{id}/progress, PATCH /v1/children/{id}/preferences` |
| 256 | `Screens/Mobile App/Child Profile/Child Profile-07.png` | Mobile App | Feature B16 (Child Profile) | Child Profile 07 | `GET /v1/children/{id}/progress, PATCH /v1/children/{id}/preferences` |
| 257 | `Screens/Mobile App/Child Profile/Child Profile-08.png` | Mobile App | Feature B16 (Child Profile) | Child Profile 08 | `GET /v1/children/{id}/progress, PATCH /v1/children/{id}/preferences` |
| 258 | `Screens/Mobile App/Child Reports/Per-Child Report-01.png` | Mobile App | Feature C22 (Per-Child Reports) | Per Child Report 01 | `GET /v1/reports/children/{id}/weekly` |
| 259 | `Screens/Mobile App/Child Reports/Per-Child Report-02.png` | Mobile App | Feature C22 (Per-Child Reports) | Per Child Report 02 | `GET /v1/reports/children/{id}/weekly` |
| 260 | `Screens/Mobile App/Child Reports/Per-Child Report-03.png` | Mobile App | Feature C22 (Per-Child Reports) | Per Child Report 03 | `GET /v1/reports/children/{id}/weekly` |
| 261 | `Screens/Mobile App/Child Reports/Per-Child Report-04.png` | Mobile App | Feature C22 (Per-Child Reports) | Per Child Report 04 | `GET /v1/reports/children/{id}/weekly` |
| 262 | `Screens/Mobile App/Child Reports/Per-Child Report-05.png` | Mobile App | Feature C22 (Per-Child Reports) | Per Child Report 05 | `GET /v1/reports/children/{id}/weekly` |
| 263 | `Screens/Mobile App/Child Reports/Per-Child Report-06.png` | Mobile App | Feature C22 (Per-Child Reports) | Per Child Report 06 | `GET /v1/reports/children/{id}/weekly` |
| 264 | `Screens/Mobile App/Child Reports/Per-Child Report-07.png` | Mobile App | Feature C22 (Per-Child Reports) | Per Child Report 07 | `GET /v1/reports/children/{id}/weekly` |
| 265 | `Screens/Mobile App/Child Reports/Per-Child Report-08.png` | Mobile App | Feature C22 (Per-Child Reports) | Per Child Report 08 | `GET /v1/reports/children/{id}/weekly` |
| 266 | `Screens/Mobile App/Child Reports/Per-Child Report-09.png` | Mobile App | Feature C22 (Per-Child Reports) | Per Child Report 09 | `GET /v1/reports/children/{id}/weekly` |
| 267 | `Screens/Mobile App/Child Reports/Per-Child Report-10.png` | Mobile App | Feature C22 (Per-Child Reports) | Per Child Report 10 | `GET /v1/reports/children/{id}/weekly` |
| 268 | `Screens/Mobile App/Child Reports/Per-Child Report-11.png` | Mobile App | Feature C22 (Per-Child Reports) | Per Child Report 11 | `GET /v1/reports/children/{id}/weekly` |
| 269 | `Screens/Mobile App/Child Reports/Per-Child Report-12.png` | Mobile App | Feature C22 (Per-Child Reports) | Per Child Report 12 | `GET /v1/reports/children/{id}/weekly` |
| 270 | `Screens/Mobile App/Child Reports/Screenshot 2026-08-25 at 1.49.50 PM.png` | Mobile App | Feature C22 (Per-Child Reports) | Screenshot 2026 08 25 at 1.49.50 PM | `GET /v1/reports/children/{id}/weekly` |
| 271 | `Screens/Mobile App/Child Reports/Screenshot 2026-08-25 at 1.49.59 PM.png` | Mobile App | Feature C22 (Per-Child Reports) | Screenshot 2026 08 25 at 1.49.59 PM | `GET /v1/reports/children/{id}/weekly` |
| 272 | `Screens/Mobile App/Child Reports/Screenshot 2026-08-25 at 1.50.16 PM.png` | Mobile App | Feature C22 (Per-Child Reports) | Screenshot 2026 08 25 at 1.50.16 PM | `GET /v1/reports/children/{id}/weekly` |
| 273 | `Screens/Mobile App/Child Reports/Screenshot 2026-08-25 at 1.50.22 PM.png` | Mobile App | Feature C22 (Per-Child Reports) | Screenshot 2026 08 25 at 1.50.22 PM | `GET /v1/reports/children/{id}/weekly` |
| 274 | `Screens/Mobile App/Du'as/Dua Card-01.png` | Mobile App | Feature A6 (Dua Learning) | Dua Card 01 | `GET /v1/duas/categories, GET /v1/duas/{id}` |
| 275 | `Screens/Mobile App/Du'as/Dua Card-02.png` | Mobile App | Feature A6 (Dua Learning) | Dua Card 02 | `GET /v1/duas/categories, GET /v1/duas/{id}` |
| 276 | `Screens/Mobile App/Du'as/Dua Categories-01.png` | Mobile App | Feature A6 (Dua Learning) | Dua Categories 01 | `GET /v1/duas/categories, GET /v1/duas/{id}` |
| 277 | `Screens/Mobile App/Du'as/Dua Categories-02.png` | Mobile App | Feature A6 (Dua Learning) | Dua Categories 02 | `GET /v1/duas/categories, GET /v1/duas/{id}` |
| 278 | `Screens/Mobile App/Du'as/Dua Categories-03.png` | Mobile App | Feature A6 (Dua Learning) | Dua Categories 03 | `GET /v1/duas/categories, GET /v1/duas/{id}` |
| 279 | `Screens/Mobile App/Du'as/Dua Categories-04.png` | Mobile App | Feature A6 (Dua Learning) | Dua Categories 04 | `GET /v1/duas/categories, GET /v1/duas/{id}` |
| 280 | `Screens/Mobile App/Du'as/Dua Categories-05.png` | Mobile App | Feature A6 (Dua Learning) | Dua Categories 05 | `GET /v1/duas/categories, GET /v1/duas/{id}` |
| 281 | `Screens/Mobile App/Du'as/Dua Categories-06.png` | Mobile App | Feature A6 (Dua Learning) | Dua Categories 06 | `GET /v1/duas/categories, GET /v1/duas/{id}` |
| 282 | `Screens/Mobile App/Du'as/Dua Categories-07.png` | Mobile App | Feature A6 (Dua Learning) | Dua Categories 07 | `GET /v1/duas/categories, GET /v1/duas/{id}` |
| 283 | `Screens/Mobile App/Du'as/Dua Categories-08.png` | Mobile App | Feature A6 (Dua Learning) | Dua Categories 08 | `GET /v1/duas/categories, GET /v1/duas/{id}` |
| 284 | `Screens/Mobile App/Du'as/Dua Quiz-01.png` | Mobile App | Feature A6 (Dua Learning) | Dua Quiz 01 | `GET /v1/duas/categories, GET /v1/duas/{id}` |
| 285 | `Screens/Mobile App/Du'as/Dua Quiz-02.png` | Mobile App | Feature A6 (Dua Learning) | Dua Quiz 02 | `GET /v1/duas/categories, GET /v1/duas/{id}` |
| 286 | `Screens/Mobile App/Du'as/Dua Quiz-03.png` | Mobile App | Feature A6 (Dua Learning) | Dua Quiz 03 | `GET /v1/duas/categories, GET /v1/duas/{id}` |
| 287 | `Screens/Mobile App/Du'as/Dua Quiz-04.png` | Mobile App | Feature A6 (Dua Learning) | Dua Quiz 04 | `GET /v1/duas/categories, GET /v1/duas/{id}` |
| 288 | `Screens/Mobile App/Facts/Fact Detail-01.png` | Mobile App | Feature B18 (Islamic Facts) | Fact Detail 01 | `GET /v1/facts/of-the-day, GET /v1/facts/{id}` |
| 289 | `Screens/Mobile App/Facts/Fact Detail-02.png` | Mobile App | Feature B18 (Islamic Facts) | Fact Detail 02 | `GET /v1/facts/of-the-day, GET /v1/facts/{id}` |
| 290 | `Screens/Mobile App/Facts/Fact Detail-03.png` | Mobile App | Feature B18 (Islamic Facts) | Fact Detail 03 | `GET /v1/facts/of-the-day, GET /v1/facts/{id}` |
| 291 | `Screens/Mobile App/Facts/Fact Detail-04.png` | Mobile App | Feature B18 (Islamic Facts) | Fact Detail 04 | `GET /v1/facts/of-the-day, GET /v1/facts/{id}` |
| 292 | `Screens/Mobile App/Facts/Fact Detail-05.png` | Mobile App | Feature B18 (Islamic Facts) | Fact Detail 05 | `GET /v1/facts/of-the-day, GET /v1/facts/{id}` |
| 293 | `Screens/Mobile App/Facts/Fact Detail-06.png` | Mobile App | Feature B18 (Islamic Facts) | Fact Detail 06 | `GET /v1/facts/of-the-day, GET /v1/facts/{id}` |
| 294 | `Screens/Mobile App/Facts/Fact of the Day.png` | Mobile App | Feature B18 (Islamic Facts) | Fact of the Day | `GET /v1/facts/of-the-day, GET /v1/facts/{id}` |
| 295 | `Screens/Mobile App/Facts/Facts Browse.png` | Mobile App | Feature B18 (Islamic Facts) | Facts Browse | `GET /v1/facts/of-the-day, GET /v1/facts/{id}` |
| 296 | `Screens/Mobile App/Favorites/Favorites-01.png` | Mobile App | Feature B14 (Favorites) | Favorites 01 | `GET /v1/favorites, POST /v1/favorites` |
| 297 | `Screens/Mobile App/Favorites/Favorites-02.png` | Mobile App | Feature B14 (Favorites) | Favorites 02 | `GET /v1/favorites, POST /v1/favorites` |
| 298 | `Screens/Mobile App/Favorites/Favorites-03.png` | Mobile App | Feature B14 (Favorites) | Favorites 03 | `GET /v1/favorites, POST /v1/favorites` |
| 299 | `Screens/Mobile App/Favorites/Favorites-04.png` | Mobile App | Feature B14 (Favorites) | Favorites 04 | `GET /v1/favorites, POST /v1/favorites` |
| 300 | `Screens/Mobile App/Favorites/Favorites-05.png` | Mobile App | Feature B14 (Favorites) | Favorites 05 | `GET /v1/favorites, POST /v1/favorites` |
| 301 | `Screens/Mobile App/Favorites/Favorites-06.png` | Mobile App | Feature B14 (Favorites) | Favorites 06 | `GET /v1/favorites, POST /v1/favorites` |
| 302 | `Screens/Mobile App/Favorites/Favorites-07.png` | Mobile App | Feature B14 (Favorites) | Favorites 07 | `GET /v1/favorites, POST /v1/favorites` |
| 303 | `Screens/Mobile App/Favorites/Favorites-08.png` | Mobile App | Feature B14 (Favorites) | Favorites 08 | `GET /v1/favorites, POST /v1/favorites` |
| 304 | `Screens/Mobile App/Favorites/Favorites-09.png` | Mobile App | Feature B14 (Favorites) | Favorites 09 | `GET /v1/favorites, POST /v1/favorites` |
| 305 | `Screens/Mobile App/Games/Game Complete-01.png` | Mobile App | Feature A10 (Games Module) | Game Complete 01 | `GET /v1/games/catalog, POST /v1/games/sessions` |
| 306 | `Screens/Mobile App/Games/Game Complete-02.png` | Mobile App | Feature A10 (Games Module) | Game Complete 02 | `GET /v1/games/catalog, POST /v1/games/sessions` |
| 307 | `Screens/Mobile App/Games/Game Complete-03.png` | Mobile App | Feature A10 (Games Module) | Game Complete 03 | `GET /v1/games/catalog, POST /v1/games/sessions` |
| 308 | `Screens/Mobile App/Games/Games Hub-01.png` | Mobile App | Feature A10 (Games Module) | Games Hub 01 | `GET /v1/games/catalog, POST /v1/games/sessions` |
| 309 | `Screens/Mobile App/Games/Games Hub-02.png` | Mobile App | Feature A10 (Games Module) | Games Hub 02 | `GET /v1/games/catalog, POST /v1/games/sessions` |
| 310 | `Screens/Mobile App/Games/Games Hub-03.png` | Mobile App | Feature A10 (Games Module) | Games Hub 03 | `GET /v1/games/catalog, POST /v1/games/sessions` |
| 311 | `Screens/Mobile App/Games/Games Hub-04.png` | Mobile App | Feature A10 (Games Module) | Games Hub 04 | `GET /v1/games/catalog, POST /v1/games/sessions` |
| 312 | `Screens/Mobile App/Games/Games Hub-05.png` | Mobile App | Feature A10 (Games Module) | Games Hub 05 | `GET /v1/games/catalog, POST /v1/games/sessions` |
| 313 | `Screens/Mobile App/Habits/Habit Checklist-01.png` | Mobile App | Feature A7 (Habit Tracker) | Habit Checklist 01 | `GET /v1/habits/daily, POST /v1/habits/check` |
| 314 | `Screens/Mobile App/Habits/Habit Checklist-02.png` | Mobile App | Feature A7 (Habit Tracker) | Habit Checklist 02 | `GET /v1/habits/daily, POST /v1/habits/check` |
| 315 | `Screens/Mobile App/Habits/Noor Garden-01.png` | Mobile App | Feature A7 (Habit Tracker) | Noor Garden 01 | `GET /v1/habits/daily, POST /v1/habits/check` |
| 316 | `Screens/Mobile App/Habits/Noor Garden-02.png` | Mobile App | Feature A7 (Habit Tracker) | Noor Garden 02 | `GET /v1/habits/daily, POST /v1/habits/check` |
| 317 | `Screens/Mobile App/Habits/Streak Recovery-01.png` | Mobile App | Feature A7 (Habit Tracker) | Streak Recovery 01 | `GET /v1/habits/daily, POST /v1/habits/check` |
| 318 | `Screens/Mobile App/Habits/Streak Recovery-02.png` | Mobile App | Feature A7 (Habit Tracker) | Streak Recovery 02 | `GET /v1/habits/daily, POST /v1/habits/check` |
| 319 | `Screens/Mobile App/Home/Home-01.5.png` | Mobile App | Feature A2 (Home Dashboard) | Home 01.5 | `GET /v1/home/dashboard, GET /v1/ai/recommendations` |
| 320 | `Screens/Mobile App/Home/Home-01.png` | Mobile App | Feature A2 (Home Dashboard) | Home 01 | `GET /v1/home/dashboard, GET /v1/ai/recommendations` |
| 321 | `Screens/Mobile App/Home/Home-02.png` | Mobile App | Feature A2 (Home Dashboard) | Home 02 | `GET /v1/home/dashboard, GET /v1/ai/recommendations` |
| 322 | `Screens/Mobile App/Home/Home-03.5.png` | Mobile App | Feature A2 (Home Dashboard) | Home 03.5 | `GET /v1/home/dashboard, GET /v1/ai/recommendations` |
| 323 | `Screens/Mobile App/Home/Home-03.png` | Mobile App | Feature A2 (Home Dashboard) | Home 03 | `GET /v1/home/dashboard, GET /v1/ai/recommendations` |
| 324 | `Screens/Mobile App/Home/Home-04.png` | Mobile App | Feature A2 (Home Dashboard) | Home 04 | `GET /v1/home/dashboard, GET /v1/ai/recommendations` |
| 325 | `Screens/Mobile App/Home/Home-05.png` | Mobile App | Feature A2 (Home Dashboard) | Home 05 | `GET /v1/home/dashboard, GET /v1/ai/recommendations` |
| 326 | `Screens/Mobile App/Home/Home-06.png` | Mobile App | Feature A2 (Home Dashboard) | Home 06 | `GET /v1/home/dashboard, GET /v1/ai/recommendations` |
| 327 | `Screens/Mobile App/Home/Home-07.png` | Mobile App | Feature A2 (Home Dashboard) | Home 07 | `GET /v1/home/dashboard, GET /v1/ai/recommendations` |
| 328 | `Screens/Mobile App/Home/Home-08.png` | Mobile App | Feature A2 (Home Dashboard) | Home 08 | `GET /v1/home/dashboard, GET /v1/ai/recommendations` |
| 329 | `Screens/Mobile App/Home/Home-09.png` | Mobile App | Feature A2 (Home Dashboard) | Home 09 | `GET /v1/home/dashboard, GET /v1/ai/recommendations` |
| 330 | `Screens/Mobile App/Home/Home-10.png` | Mobile App | Feature A2 (Home Dashboard) | Home 10 | `GET /v1/home/dashboard, GET /v1/ai/recommendations` |
| 331 | `Screens/Mobile App/Home/Home-11.png` | Mobile App | Feature A2 (Home Dashboard) | Home 11 | `GET /v1/home/dashboard, GET /v1/ai/recommendations` |
| 332 | `Screens/Mobile App/Home/Home-12.png` | Mobile App | Feature A2 (Home Dashboard) | Home 12 | `GET /v1/home/dashboard, GET /v1/ai/recommendations` |
| 333 | `Screens/Mobile App/Home/Home-13.png` | Mobile App | Feature A2 (Home Dashboard) | Home 13 | `GET /v1/home/dashboard, GET /v1/ai/recommendations` |
| 334 | `Screens/Mobile App/Learn/Feedback.png` | Mobile App | Feature A5 (Quran & Arabic) | Feedback | `POST /v1/learning/attempts, POST /v1/learning/recitation` |
| 335 | `Screens/Mobile App/Learn/Skill Tree-01.png` | Mobile App | Feature A9 (Skill Tree Mastery) | Skill Tree 01 | `GET /v1/learning/paths, POST /v1/learning/placement-check` |
| 336 | `Screens/Mobile App/Learn/Skill Tree-02.png` | Mobile App | Feature A9 (Skill Tree Mastery) | Skill Tree 02 | `GET /v1/learning/paths, GET /v1/learning/placement-check/questions` |
| 337 | `Screens/Mobile App/Learn/Skill Tree-03.png` | Mobile App | Feature A9 (Skill Tree Mastery) | Skill Tree 03 | `GET /v1/learning/paths` |
| 338 | `Screens/Mobile App/Learn/Skill Tree-04.png` | Mobile App | Feature A9 (Skill Tree Mastery) | Skill Tree 04 | `GET /v1/learning/paths` |
| 339 | `Screens/Mobile App/Learn/Skill Tree-05.png` | Mobile App | Feature A9 (Skill Tree Mastery) | Skill Tree 05 | `GET /v1/learning/paths` |
| 340 | `Screens/Mobile App/Learn/Skill Tree-06.png` | Mobile App | Feature A9 (Skill Tree Mastery) | Skill Tree 06 | `GET /v1/learning/paths` |
| 341 | `Screens/Mobile App/Learn/Skill Tree-07.png` | Mobile App | Feature A9 (Skill Tree Mastery) | Skill Tree 07 | `GET /v1/learning/paths` |
| 342 | `Screens/Mobile App/Learn/Skill Tree-08.png` | Mobile App | Feature A9 (Skill Tree Mastery) | Skill Tree 08 | `GET /v1/learning/paths` |
| 343 | `Screens/Mobile App/Learn/Surah Practice-01.png` | Mobile App | Feature A5 (Quran & Arabic) | Surah Practice 01 | `POST /v1/learning/attempts, POST /v1/learning/recitation` |
| 344 | `Screens/Mobile App/Learn/Surah Practice-02.png` | Mobile App | Feature A5 (Quran & Arabic) | Surah Practice 02 | `POST /v1/learning/attempts, POST /v1/learning/recitation` |
| 345 | `Screens/Mobile App/Notifications/Deep Link Resolver.png` | Mobile App | Feature B17 (Child Notifications) | Deep Link Resolver | `GET /v1/notifications/inbox, PUT /v1/notifications/preferences` |
| 346 | `Screens/Mobile App/Notifications/Notification Preferences-01.png` | Mobile App | Feature B17 (Child Notifications) | Notification Preferences 01 | `GET /v1/notifications/inbox, PUT /v1/notifications/preferences` |
| 347 | `Screens/Mobile App/Notifications/Notification Preferences-02.png` | Mobile App | Feature B17 (Child Notifications) | Notification Preferences 02 | `GET /v1/notifications/inbox, PUT /v1/notifications/preferences` |
| 348 | `Screens/Mobile App/Notifications/Notification Preferences-03.png` | Mobile App | Feature B17 (Child Notifications) | Notification Preferences 03 | `GET /v1/notifications/inbox, PUT /v1/notifications/preferences` |
| 349 | `Screens/Mobile App/Notifications/Notification Preferences-04.png` | Mobile App | Feature B17 (Child Notifications) | Notification Preferences 04 | `GET /v1/notifications/inbox, PUT /v1/notifications/preferences` |
| 350 | `Screens/Mobile App/Notifications/Notifications Inbox-01.png` | Mobile App | Feature B17 (Child Notifications) | Notifications Inbox 01 | `GET /v1/notifications/inbox, PUT /v1/notifications/preferences` |
| 351 | `Screens/Mobile App/Notifications/Notifications Inbox-02.png` | Mobile App | Feature B17 (Child Notifications) | Notifications Inbox 02 | `GET /v1/notifications/inbox, PUT /v1/notifications/preferences` |
| 352 | `Screens/Mobile App/Notifications/Notifications Settings-01.png` | Mobile App | Feature B17 (Child Notifications) | Notifications Settings 01 | `GET /v1/notifications/inbox, PUT /v1/notifications/preferences` |
| 353 | `Screens/Mobile App/Notifications/Notifications Settings-02.png` | Mobile App | Feature B17 (Child Notifications) | Notifications Settings 02 | `GET /v1/notifications/inbox, PUT /v1/notifications/preferences` |
| 354 | `Screens/Mobile App/Notifications/Notifications Settings-03.png` | Mobile App | Feature B17 (Child Notifications) | Notifications Settings 03 | `GET /v1/notifications/inbox, PUT /v1/notifications/preferences` |
| 355 | `Screens/Mobile App/Notifications/Notifications Settings-04.png` | Mobile App | Feature B17 (Child Notifications) | Notifications Settings 04 | `GET /v1/notifications/inbox, PUT /v1/notifications/preferences` |
| 356 | `Screens/Mobile App/Notifications/Notifications Settings-05.png` | Mobile App | Feature B17 (Child Notifications) | Notifications Settings 05 | `GET /v1/notifications/inbox, PUT /v1/notifications/preferences` |
| 357 | `Screens/Mobile App/Notifications/Notifications Settings-06.png` | Mobile App | Feature B17 (Child Notifications) | Notifications Settings 06 | `GET /v1/notifications/inbox, PUT /v1/notifications/preferences` |
| 358 | `Screens/Mobile App/Notifications/Notifications Settings-07.png` | Mobile App | Feature B17 (Child Notifications) | Notifications Settings 07 | `GET /v1/notifications/inbox, PUT /v1/notifications/preferences` |
| 359 | `Screens/Mobile App/Onboarding/Add Child.png` | Mobile App | Feature A1 (Splash & Onboarding) | Add Child | `GET /v1/identity/bootstrap, POST /v1/identity/auth/otp/verify` |
| 360 | `Screens/Mobile App/Onboarding/Intro 1.png` | Mobile App | Feature A1 (Splash & Onboarding) | Intro 1 | `GET /v1/identity/bootstrap, POST /v1/identity/auth/otp/verify` |
| 361 | `Screens/Mobile App/Onboarding/Intro 2.png` | Mobile App | Feature A1 (Splash & Onboarding) | Intro 2 | `GET /v1/identity/bootstrap, POST /v1/identity/auth/otp/verify` |
| 362 | `Screens/Mobile App/Onboarding/Intro 3.png` | Mobile App | Feature A1 (Splash & Onboarding) | Intro 3 | `GET /v1/identity/bootstrap, POST /v1/identity/auth/otp/verify` |
| 363 | `Screens/Mobile App/Onboarding/Intro 4.png` | Mobile App | Feature A1 (Splash & Onboarding) | Intro 4 | `GET /v1/identity/bootstrap, POST /v1/identity/auth/otp/verify` |
| 364 | `Screens/Mobile App/Onboarding/Language.png` | Mobile App | Feature A1 (Splash & Onboarding) | Language | `GET /v1/identity/bootstrap, POST /v1/identity/auth/otp/verify` |
| 365 | `Screens/Mobile App/Onboarding/OTP.png` | Mobile App | Feature A1 (Splash & Onboarding) | OTP | `GET /v1/identity/bootstrap, POST /v1/identity/auth/otp/verify` |
| 366 | `Screens/Mobile App/Onboarding/Profiles.png` | Mobile App | Feature A1 (Splash & Onboarding) | Profiles | `GET /v1/identity/bootstrap, POST /v1/identity/auth/otp/verify` |
| 367 | `Screens/Mobile App/Onboarding/Register-01.png` | Mobile App | Feature A1 (Splash & Onboarding) | Register 01 | `GET /v1/identity/bootstrap, POST /v1/identity/auth/otp/verify` |
| 368 | `Screens/Mobile App/Onboarding/Register-02.png` | Mobile App | Feature A1 (Splash & Onboarding) | Register 02 | `GET /v1/identity/bootstrap, POST /v1/identity/auth/otp/verify` |
| 369 | `Screens/Mobile App/Onboarding/Register-03.png` | Mobile App | Feature A1 (Splash & Onboarding) | Register 03 | `GET /v1/identity/bootstrap, POST /v1/identity/auth/otp/verify` |
| 370 | `Screens/Mobile App/Onboarding/Setup.png` | Mobile App | Feature A1 (Splash & Onboarding) | Setup | `GET /v1/identity/bootstrap, POST /v1/identity/auth/otp/verify` |
| 371 | `Screens/Mobile App/Onboarding/Splash.png` | Mobile App | Feature A1 (Splash & Onboarding) | Splash | `GET /v1/identity/bootstrap, POST /v1/identity/auth/otp/verify` |
| 372 | `Screens/Mobile App/Parent Area/Parent Dashboard-01.png` | Mobile App | Feature C20 (Parent Dashboard) | Parent Dashboard 01 | `GET /v1/parent/dashboard/summary` |
| 373 | `Screens/Mobile App/Parent Area/Parent Dashboard-02.png` | Mobile App | Feature C20 (Parent Dashboard) | Parent Dashboard 02 | `GET /v1/parent/dashboard/summary` |
| 374 | `Screens/Mobile App/Parent Area/Parent Dashboard-03.png` | Mobile App | Feature C20 (Parent Dashboard) | Parent Dashboard 03 | `GET /v1/parent/dashboard/summary` |
| 375 | `Screens/Mobile App/Parent Area/Parent Dashboard-04.png` | Mobile App | Feature C20 (Parent Dashboard) | Parent Dashboard 04 | `GET /v1/parent/dashboard/summary` |
| 376 | `Screens/Mobile App/Parent Area/Parent Dashboard-05.png` | Mobile App | Feature C20 (Parent Dashboard) | Parent Dashboard 05 | `GET /v1/parent/dashboard/summary` |
| 377 | `Screens/Mobile App/Parent Area/Parent Dashboard-06.png` | Mobile App | Feature C20 (Parent Dashboard) | Parent Dashboard 06 | `GET /v1/parent/dashboard/summary` |
| 378 | `Screens/Mobile App/Parent Area/Parent Gate-01.png` | Mobile App | Feature C19 (Parent PIN Gate) | Parent Gate 01 | `POST /v1/identity/parent/pin/verify` |
| 379 | `Screens/Mobile App/Parent Area/Parent Gate-02.png` | Mobile App | Feature C19 (Parent PIN Gate) | Parent Gate 02 | `POST /v1/identity/parent/pin/verify` |
| 380 | `Screens/Mobile App/Parent Area/Profile Lock.png` | Mobile App | Feature C19 (Parent PIN Gate) | Profile Lock | `POST /v1/identity/parent/pin/verify` |
| 381 | `Screens/Mobile App/Parent Area/Who is Learning?-01.png` | Mobile App | Feature C20 (Parent Dashboard) | Who is Learning? 01 | `GET /v1/parent/dashboard/summary` |
| 382 | `Screens/Mobile App/Parent Area/Who is Learning?-02.png` | Mobile App | Feature C20 (Parent Dashboard) | Who is Learning? 02 | `GET /v1/parent/dashboard/summary` |
| 383 | `Screens/Mobile App/Parent Area/Who is Learning?-03.png` | Mobile App | Feature C20 (Parent Dashboard) | Who is Learning? 03 | `GET /v1/parent/dashboard/summary` |
| 384 | `Screens/Mobile App/Parent Area/Who is Learning?-04.png` | Mobile App | Feature C20 (Parent Dashboard) | Who is Learning? 04 | `GET /v1/parent/dashboard/summary` |
| 385 | `Screens/Mobile App/Parental Controls/AI Permissions-01.png` | Mobile App | Feature C23 (Parental Controls) | AI Permissions 01 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 386 | `Screens/Mobile App/Parental Controls/AI Permissions-02.png` | Mobile App | Feature C23 (Parental Controls) | AI Permissions 02 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 387 | `Screens/Mobile App/Parental Controls/AI Permissions-03.png` | Mobile App | Feature C23 (Parental Controls) | AI Permissions 03 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 388 | `Screens/Mobile App/Parental Controls/Bedtime Settings-01.png` | Mobile App | Feature C23 (Parental Controls) | Bedtime Settings 01 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 389 | `Screens/Mobile App/Parental Controls/Bedtime Settings-02.png` | Mobile App | Feature C23 (Parental Controls) | Bedtime Settings 02 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 390 | `Screens/Mobile App/Parental Controls/Bedtime Settings-03.png` | Mobile App | Feature C23 (Parental Controls) | Bedtime Settings 03 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 391 | `Screens/Mobile App/Parental Controls/Calm Rest Screen-01.png` | Mobile App | Feature C23 (Parental Controls) | Calm Rest Screen 01 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 392 | `Screens/Mobile App/Parental Controls/Calm Rest Screen-02.png` | Mobile App | Feature C23 (Parental Controls) | Calm Rest Screen 02 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 393 | `Screens/Mobile App/Parental Controls/Calm Rest Screen-03.png` | Mobile App | Feature C23 (Parental Controls) | Calm Rest Screen 03 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 394 | `Screens/Mobile App/Parental Controls/Child Locks & Sessions-01.png` | Mobile App | Feature C23 (Parental Controls) | Child Locks & Sessions 01 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 395 | `Screens/Mobile App/Parental Controls/Child Locks & Sessions-02.png` | Mobile App | Feature C23 (Parental Controls) | Child Locks & Sessions 02 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 396 | `Screens/Mobile App/Parental Controls/Child Locks & Sessions-03.png` | Mobile App | Feature C23 (Parental Controls) | Child Locks & Sessions 03 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 397 | `Screens/Mobile App/Parental Controls/Child Locks & Sessions-04.png` | Mobile App | Feature C23 (Parental Controls) | Child Locks & Sessions 04 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 398 | `Screens/Mobile App/Parental Controls/Content Age Level-01.png` | Mobile App | Feature C23 (Parental Controls) | Content Age Level 01 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 399 | `Screens/Mobile App/Parental Controls/Content Age Level-02.png` | Mobile App | Feature C23 (Parental Controls) | Content Age Level 02 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 400 | `Screens/Mobile App/Parental Controls/Content Age Level-03.png` | Mobile App | Feature C23 (Parental Controls) | Content Age Level 03 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 401 | `Screens/Mobile App/Parental Controls/Screen Time Settings-01.png` | Mobile App | Feature C23 (Parental Controls) | Screen Time Settings 01 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 402 | `Screens/Mobile App/Parental Controls/Screen Time Settings-02.png` | Mobile App | Feature C23 (Parental Controls) | Screen Time Settings 02 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 403 | `Screens/Mobile App/Parental Controls/Screen Time Settings-03.png` | Mobile App | Feature C23 (Parental Controls) | Screen Time Settings 03 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 404 | `Screens/Mobile App/Parental Controls/Screen Time Settings-04.png` | Mobile App | Feature C23 (Parental Controls) | Screen Time Settings 04 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 405 | `Screens/Mobile App/Parental Controls/Screen Time Settings-05.png` | Mobile App | Feature C23 (Parental Controls) | Screen Time Settings 05 | `GET /v1/controls/{child_id}, PUT /v1/controls/{child_id}` |
| 406 | `Screens/Mobile App/Privacy/AI History-01.png` | Mobile App | Feature C26 (Privacy & Consent) | AI History 01 | `GET /v1/privacy/consents, DELETE /v1/privacy/ai-history` |
| 407 | `Screens/Mobile App/Privacy/AI History-02.png` | Mobile App | Feature C26 (Privacy & Consent) | AI History 02 | `GET /v1/privacy/consents, DELETE /v1/privacy/ai-history` |
| 408 | `Screens/Mobile App/Privacy/AI History-03.png` | Mobile App | Feature C26 (Privacy & Consent) | AI History 03 | `GET /v1/privacy/consents, DELETE /v1/privacy/ai-history` |
| 409 | `Screens/Mobile App/Privacy/Consent Log-01.png` | Mobile App | Feature C26 (Privacy & Consent) | Consent Log 01 | `GET /v1/privacy/consents, DELETE /v1/privacy/ai-history` |
| 410 | `Screens/Mobile App/Privacy/Consent Log-02.png` | Mobile App | Feature C26 (Privacy & Consent) | Consent Log 02 | `GET /v1/privacy/consents, DELETE /v1/privacy/ai-history` |
| 411 | `Screens/Mobile App/Privacy/Consent Log-03.png` | Mobile App | Feature C26 (Privacy & Consent) | Consent Log 03 | `GET /v1/privacy/consents, DELETE /v1/privacy/ai-history` |
| 412 | `Screens/Mobile App/Privacy/Consent Log-04.png` | Mobile App | Feature C26 (Privacy & Consent) | Consent Log 04 | `GET /v1/privacy/consents, DELETE /v1/privacy/ai-history` |
| 413 | `Screens/Mobile App/Privacy/Consent Log-05.png` | Mobile App | Feature C26 (Privacy & Consent) | Consent Log 05 | `GET /v1/privacy/consents, DELETE /v1/privacy/ai-history` |
| 414 | `Screens/Mobile App/Privacy/Consent Log-06.png` | Mobile App | Feature C26 (Privacy & Consent) | Consent Log 06 | `GET /v1/privacy/consents, DELETE /v1/privacy/ai-history` |
| 415 | `Screens/Mobile App/Privacy/Privacy & Data-01.png` | Mobile App | Feature C26 (Privacy & Consent) | Privacy & Data 01 | `GET /v1/privacy/consents, DELETE /v1/privacy/ai-history` |
| 416 | `Screens/Mobile App/Privacy/Privacy & Data-02.png` | Mobile App | Feature C26 (Privacy & Consent) | Privacy & Data 02 | `GET /v1/privacy/consents, DELETE /v1/privacy/ai-history` |
| 417 | `Screens/Mobile App/Privacy/Privacy & Data-03.png` | Mobile App | Feature C26 (Privacy & Consent) | Privacy & Data 03 | `GET /v1/privacy/consents, DELETE /v1/privacy/ai-history` |
| 418 | `Screens/Mobile App/Privacy/Privacy & Data-04.png` | Mobile App | Feature C26 (Privacy & Consent) | Privacy & Data 04 | `GET /v1/privacy/consents, DELETE /v1/privacy/ai-history` |
| 419 | `Screens/Mobile App/Privacy/Privacy & Data-05.png` | Mobile App | Feature C26 (Privacy & Consent) | Privacy & Data 05 | `GET /v1/privacy/consents, DELETE /v1/privacy/ai-history` |
| 420 | `Screens/Mobile App/Quiz Engine/Quiz Complete-01.png` | Mobile App | Feature A8 (Daily Quiz Engine) | Quiz Complete 01 | `GET /v1/quiz/daily, POST /v1/quiz/attempts` |
| 421 | `Screens/Mobile App/Quiz Engine/Quiz Complete-02.png` | Mobile App | Feature A8 (Daily Quiz Engine) | Quiz Complete 02 | `GET /v1/quiz/daily, POST /v1/quiz/attempts` |
| 422 | `Screens/Mobile App/Quiz Engine/Quiz Question-01.png` | Mobile App | Feature A8 (Daily Quiz Engine) | Quiz Question 01 | `GET /v1/quiz/daily, POST /v1/quiz/attempts` |
| 423 | `Screens/Mobile App/Quiz Engine/Quiz Question-02.png` | Mobile App | Feature A8 (Daily Quiz Engine) | Quiz Question 02 | `GET /v1/quiz/daily, POST /v1/quiz/attempts` |
| 424 | `Screens/Mobile App/Quiz Engine/Quiz Question-03.png` | Mobile App | Feature A8 (Daily Quiz Engine) | Quiz Question 03 | `GET /v1/quiz/daily, POST /v1/quiz/attempts` |
| 425 | `Screens/Mobile App/Quiz Engine/Quiz Question-04.png` | Mobile App | Feature A8 (Daily Quiz Engine) | Quiz Question 04 | `GET /v1/quiz/daily, POST /v1/quiz/attempts` |
| 426 | `Screens/Mobile App/Quiz Engine/Quiz Result-01.png` | Mobile App | Feature A8 (Daily Quiz Engine) | Quiz Result 01 | `GET /v1/quiz/daily, POST /v1/quiz/attempts` |
| 427 | `Screens/Mobile App/Quiz Engine/Quiz Result-02.png` | Mobile App | Feature A8 (Daily Quiz Engine) | Quiz Result 02 | `GET /v1/quiz/daily, POST /v1/quiz/attempts` |
| 428 | `Screens/Mobile App/Quiz Engine/Quiz Result-03.png` | Mobile App | Feature A8 (Daily Quiz Engine) | Quiz Result 03 | `GET /v1/quiz/daily, POST /v1/quiz/attempts` |
| 429 | `Screens/Mobile App/Quiz Engine/Quiz Result-04.png` | Mobile App | Feature A8 (Daily Quiz Engine) | Quiz Result 04 | `GET /v1/quiz/daily, POST /v1/quiz/attempts` |
| 430 | `Screens/Mobile App/Quiz Engine/Quiz Result-05.png` | Mobile App | Feature A8 (Daily Quiz Engine) | Quiz Result 05 | `GET /v1/quiz/daily, POST /v1/quiz/attempts` |
| 431 | `Screens/Mobile App/Quiz Engine/Quiz Result-06.png` | Mobile App | Feature A8 (Daily Quiz Engine) | Quiz Result 06 | `GET /v1/quiz/daily, POST /v1/quiz/attempts` |
| 432 | `Screens/Mobile App/Quiz Engine/Quiz Result-07.png` | Mobile App | Feature A8 (Daily Quiz Engine) | Quiz Result 07 | `GET /v1/quiz/daily, POST /v1/quiz/attempts` |
| 433 | `Screens/Mobile App/Ramadan Mode/Eid Card Generator.png` | Mobile App | Feature F36 (Ramadan Mode Mobile) | Eid Card Generator | `GET /v1/ramadan/status, GET /v1/ramadan/missions/today` |
| 434 | `Screens/Mobile App/Ramadan Mode/Eid Countdown.png` | Mobile App | Feature F36 (Ramadan Mode Mobile) | Eid Countdown | `GET /v1/ramadan/status, GET /v1/ramadan/missions/today` |
| 435 | `Screens/Mobile App/Ramadan Mode/Eid Home.png` | Mobile App | Feature A2 (Home Dashboard) | Eid Home | `GET /v1/home/dashboard, GET /v1/ai/recommendations` |
| 436 | `Screens/Mobile App/Ramadan Mode/Eid Reward Reveal.png` | Mobile App | Feature F36 (Ramadan Mode Mobile) | Eid Reward Reveal | `GET /v1/ramadan/status, GET /v1/ramadan/missions/today` |
| 437 | `Screens/Mobile App/Ramadan Mode/Fasting Tracker-01.png` | Mobile App | Feature F36 (Ramadan Mode Mobile) | Fasting Tracker 01 | `GET /v1/ramadan/status, GET /v1/ramadan/missions/today` |
| 438 | `Screens/Mobile App/Ramadan Mode/Fasting Tracker-02.png` | Mobile App | Feature F36 (Ramadan Mode Mobile) | Fasting Tracker 02 | `GET /v1/ramadan/status, GET /v1/ramadan/missions/today` |
| 439 | `Screens/Mobile App/Ramadan Mode/Journey Map (Lanterns).png` | Mobile App | Feature F36 (Ramadan Mode Mobile) | Journey Map (Lanterns) | `GET /v1/ramadan/status, GET /v1/ramadan/missions/today` |
| 440 | `Screens/Mobile App/Ramadan Mode/Laylatul Qadr Reflection.png` | Mobile App | Feature F36 (Ramadan Mode Mobile) | Laylatul Qadr Reflection | `GET /v1/ramadan/status, GET /v1/ramadan/missions/today` |
| 441 | `Screens/Mobile App/Ramadan Mode/Mission Detail.png` | Mobile App | Feature F36 (Ramadan Mode Mobile) | Mission Detail | `GET /v1/ramadan/status, GET /v1/ramadan/missions/today` |
| 442 | `Screens/Mobile App/Ramadan Mode/Night Recap.png` | Mobile App | Feature F36 (Ramadan Mode Mobile) | Night Recap | `GET /v1/ramadan/status, GET /v1/ramadan/missions/today` |
| 443 | `Screens/Mobile App/Ramadan Mode/Parent-Family Aggregate.png` | Mobile App | Feature F36 (Ramadan Mode Mobile) | Parent Family Aggregate | `GET /v1/ramadan/status, GET /v1/ramadan/missions/today` |
| 444 | `Screens/Mobile App/Ramadan Mode/Parent-Family Member Invite.png` | Mobile App | Feature F36 (Ramadan Mode Mobile) | Parent Family Member Invite | `GET /v1/ramadan/status, GET /v1/ramadan/missions/today` |
| 445 | `Screens/Mobile App/Ramadan Mode/Parent-Family Report.png` | Mobile App | Feature F36 (Ramadan Mode Mobile) | Parent Family Report | `GET /v1/ramadan/status, GET /v1/ramadan/missions/today` |
| 446 | `Screens/Mobile App/Ramadan Mode/Parent-Family Report⑲ Conversion Card (Day 28-30).png` | Mobile App | Feature F36 (Ramadan Mode Mobile) | Parent Family Report⑲ Conversion Card (Day 28 30) | `GET /v1/ramadan/status, GET /v1/ramadan/missions/today` |
| 447 | `Screens/Mobile App/Ramadan Mode/Parent-Ramadan Dashboard.png` | Mobile App | Feature F36 (Ramadan Mode Mobile) | Parent Ramadan Dashboard | `GET /v1/ramadan/status, GET /v1/ramadan/missions/today` |
| 448 | `Screens/Mobile App/Ramadan Mode/Parent-Ramadan Settings.png` | Mobile App | Feature F36 (Ramadan Mode Mobile) | Parent Ramadan Settings | `GET /v1/ramadan/status, GET /v1/ramadan/missions/today` |
| 449 | `Screens/Mobile App/Ramadan Mode/Post-Eid Keep the Habit.png` | Mobile App | Feature F36 (Ramadan Mode Mobile) | Post Eid Keep the Habit | `GET /v1/ramadan/status, GET /v1/ramadan/missions/today` |
| 450 | `Screens/Mobile App/Ramadan Mode/Prep-Countdown.png` | Mobile App | Feature F36 (Ramadan Mode Mobile) | Prep Countdown | `GET /v1/ramadan/status, GET /v1/ramadan/missions/today` |
| 451 | `Screens/Mobile App/Ramadan Mode/Ramadan Certificate.png` | Mobile App | Feature F36 (Ramadan Mode Mobile) | Ramadan Certificate | `GET /v1/ramadan/status, GET /v1/ramadan/missions/today` |
| 452 | `Screens/Mobile App/Ramadan Mode/Ramadan Home.png` | Mobile App | Feature A2 (Home Dashboard) | Ramadan Home | `GET /v1/home/dashboard, GET /v1/ai/recommendations` |
| 453 | `Screens/Mobile App/Ramadan Mode/Story Player.png` | Mobile App | Feature F36 (Ramadan Mode Mobile) | Story Player | `GET /v1/ramadan/status, GET /v1/ramadan/missions/today` |
| 454 | `Screens/Mobile App/Rewards/Achievement Store-01.png` | Mobile App | Feature A11 (Rewards System) | Achievement Store 01 | `GET /v1/catalog-items, POST /v1/rewards/claims` |
| 455 | `Screens/Mobile App/Rewards/Achievement Store-02.png` | Mobile App | Feature A11 (Rewards System) | Achievement Store 02 | `GET /v1/catalog-items, POST /v1/rewards/claims` |
| 456 | `Screens/Mobile App/Rewards/Achievement Store-03.png` | Mobile App | Feature A11 (Rewards System) | Achievement Store 03 | `GET /v1/catalog-items, POST /v1/rewards/claims` |
| 457 | `Screens/Mobile App/Rewards/Achievement Store-04.png` | Mobile App | Feature A11 (Rewards System) | Achievement Store 04 | `GET /v1/catalog-items, POST /v1/rewards/claims` |
| 458 | `Screens/Mobile App/Rewards/Achievements-01.png` | Mobile App | Feature A11 (Rewards System) | Achievements 01 | `GET /v1/rewards/wallet, GET /v1/rewards/achievements` |
| 459 | `Screens/Mobile App/Rewards/Achievements-02.png` | Mobile App | Feature A11 (Rewards System) | Achievements 02 | `GET /v1/rewards/wallet, GET /v1/rewards/achievements` |
| 460 | `Screens/Mobile App/Rewards/Achievements-03.png` | Mobile App | Feature A11 (Rewards System) | Achievements 03 | `GET /v1/rewards/wallet, GET /v1/rewards/achievements` |
| 461 | `Screens/Mobile App/Rewards/Achievements-04.png` | Mobile App | Feature A11 (Rewards System) | Achievements 04 | `GET /v1/rewards/wallet, GET /v1/rewards/achievements` |
| 462 | `Screens/Mobile App/Rewards/Family Board.png` | Mobile App | Feature A11 (Rewards System) | Family Board | `GET /v1/rewards/wallet, GET /v1/rewards/achievements` |
| 463 | `Screens/Mobile App/Rewards/Rewards Wallet-01.png` | Mobile App | Feature A11 (Rewards System) | Rewards Wallet 01 | `GET /v1/rewards/wallet, GET /v1/rewards/achievements` |
| 464 | `Screens/Mobile App/Rewards/Rewards Wallet-02.png` | Mobile App | Feature A11 (Rewards System) | Rewards Wallet 02 | `GET /v1/rewards/wallet, GET /v1/rewards/achievements` |
| 465 | `Screens/Mobile App/Rewards/Rewards Wallet-03.png` | Mobile App | Feature A11 (Rewards System) | Rewards Wallet 03 | `GET /v1/rewards/wallet, GET /v1/rewards/achievements` |
| 466 | `Screens/Mobile App/Rewards/Rewards Wallet-04.png` | Mobile App | Feature A11 (Rewards System) | Rewards Wallet 04 | `GET /v1/rewards/wallet, GET /v1/rewards/achievements` |
| 467 | `Screens/Mobile App/Rewards/Rewards Wallet-05.png` | Mobile App | Feature A11 (Rewards System) | Rewards Wallet 05 | `GET /v1/rewards/wallet, GET /v1/rewards/achievements` |
| 468 | `Screens/Mobile App/Rewards/Rewards Wallet-06.png` | Mobile App | Feature A11 (Rewards System) | Rewards Wallet 06 | `GET /v1/rewards/wallet, GET /v1/rewards/achievements` |
| 469 | `Screens/Mobile App/Rewards/Rewards Wallet-07.png` | Mobile App | Feature A11 (Rewards System) | Rewards Wallet 07 | `GET /v1/rewards/wallet, GET /v1/rewards/achievements` |
| 470 | `Screens/Mobile App/Rewards/Rewards Wallet-08.png` | Mobile App | Feature A11 (Rewards System) | Rewards Wallet 08 | `GET /v1/rewards/wallet, GET /v1/rewards/achievements` |
| 471 | `Screens/Mobile App/Rewards/Rewards Wallet-09.png` | Mobile App | Feature A11 (Rewards System) | Rewards Wallet 09 | `GET /v1/rewards/wallet, GET /v1/rewards/achievements` |
| 472 | `Screens/Mobile App/Search/Results.png` | Mobile App | Feature B13 (Search & Discovery) | Results | `GET /v1/search` |
| 473 | `Screens/Mobile App/Search/Search-01.png` | Mobile App | Feature B13 (Search & Discovery) | Search 01 | `GET /v1/search, GET /v1/search/recent, DELETE /v1/search/recent, DELETE /v1/search/recent/{search_id}` |
| 474 | `Screens/Mobile App/Search/Search-02.png` | Mobile App | Feature B13 (Search & Discovery) | Search 02 | `GET /v1/search` |
| 475 | `Screens/Mobile App/Search/Voice Search-01.png` | Mobile App | Feature B13 (Search & Discovery) | Voice Search 01 | `POST /v1/search/voice` |
| 476 | `Screens/Mobile App/Search/Voice Search-02.png` | Mobile App | Feature B13 (Search & Discovery) | Voice Search 02 | `POST /v1/search/voice` |
| 477 | `Screens/Mobile App/Stories/Bedtime Player.png` | Mobile App | Feature A3 (Stories Module) | Bedtime Player | `GET /v1/stories, GET /v1/stories/{id}/scenes` |
| 478 | `Screens/Mobile App/Stories/Choice.png` | Mobile App | Feature A3 (Stories Module) | Choice | `GET /v1/stories, GET /v1/stories/{id}/scenes` |
| 479 | `Screens/Mobile App/Stories/Complete.png` | Mobile App | Feature A3 (Stories Module) | Complete | `GET /v1/stories, GET /v1/stories/{id}/scenes` |
| 480 | `Screens/Mobile App/Stories/Moral Card.png` | Mobile App | Feature A3 (Stories Module) | Moral Card | `GET /v1/stories, GET /v1/stories/{id}/scenes` |
| 481 | `Screens/Mobile App/Stories/Player.png` | Mobile App | Feature A3 (Stories Module) | Player | `GET /v1/stories, GET /v1/stories/{id}/scenes` |
| 482 | `Screens/Mobile App/Stories/Stories-01.png` | Mobile App | Feature A3 (Stories Module) | Stories 01 | `GET /v1/stories, GET /v1/stories/{id}/scenes` |
| 483 | `Screens/Mobile App/Stories/Stories-02.png` | Mobile App | Feature A3 (Stories Module) | Stories 02 | `GET /v1/stories, GET /v1/stories/{id}/scenes` |
| 484 | `Screens/Mobile App/Stories/Stories-03.png` | Mobile App | Feature A3 (Stories Module) | Stories 03 | `GET /v1/stories, GET /v1/stories/{id}/scenes` |
| 485 | `Screens/Mobile App/Stories/Stories-04.png` | Mobile App | Feature A3 (Stories Module) | Stories 04 | `GET /v1/stories, GET /v1/stories/{id}/scenes` |
| 486 | `Screens/Mobile App/Stories/Stories-05.png` | Mobile App | Feature A3 (Stories Module) | Stories 05 | `GET /v1/stories, GET /v1/stories/{id}/scenes` |
| 487 | `Screens/Mobile App/Stories/Stories-06.png` | Mobile App | Feature A3 (Stories Module) | Stories 06 | `GET /v1/stories, GET /v1/stories/{id}/scenes` |
| 488 | `Screens/Mobile App/Stories/Stories-07.png` | Mobile App | Feature A3 (Stories Module) | Stories 07 | `GET /v1/stories, GET /v1/stories/{id}/scenes` |
| 489 | `Screens/Mobile App/Stories/Story Detail-01.png` | Mobile App | Feature A3 (Stories Module) | Story Detail 01 | `GET /v1/stories, GET /v1/stories/{id}/scenes` |
| 490 | `Screens/Mobile App/Stories/Story Detail-02.png` | Mobile App | Feature A3 (Stories Module) | Story Detail 02 | `GET /v1/stories, GET /v1/stories/{id}/scenes` |
| 491 | `Screens/Mobile App/Subscription/Cancel Confirmation-01.png` | Mobile App | Feature C24 (Subscription & Billing) | Cancel Confirmation 01 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 492 | `Screens/Mobile App/Subscription/Cancel Confirmation-02.png` | Mobile App | Feature C24 (Subscription & Billing) | Cancel Confirmation 02 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 493 | `Screens/Mobile App/Subscription/Plan Comparison-01.png` | Mobile App | Feature C24 (Subscription & Billing) | Plan Comparison 01 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 494 | `Screens/Mobile App/Subscription/Plan Comparison-02.png` | Mobile App | Feature C24 (Subscription & Billing) | Plan Comparison 02 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 495 | `Screens/Mobile App/Subscription/Plan Comparison-03.png` | Mobile App | Feature C24 (Subscription & Billing) | Plan Comparison 03 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 496 | `Screens/Mobile App/Subscription/Plan Comparison-04.png` | Mobile App | Feature C24 (Subscription & Billing) | Plan Comparison 04 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 497 | `Screens/Mobile App/Subscription/Plan Comparison-05.png` | Mobile App | Feature C24 (Subscription & Billing) | Plan Comparison 05 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 498 | `Screens/Mobile App/Subscription/Plan Comparison-06.png` | Mobile App | Feature C24 (Subscription & Billing) | Plan Comparison 06 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 499 | `Screens/Mobile App/Subscription/Plan Comparison-07.png` | Mobile App | Feature C24 (Subscription & Billing) | Plan Comparison 07 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 500 | `Screens/Mobile App/Subscription/Plan Comparison-08.png` | Mobile App | Feature C24 (Subscription & Billing) | Plan Comparison 08 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 501 | `Screens/Mobile App/Subscription/Premium Upsell-01.png` | Mobile App | Feature C24 (Subscription & Billing) | Premium Upsell 01 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 502 | `Screens/Mobile App/Subscription/Premium Upsell-02.png` | Mobile App | Feature C24 (Subscription & Billing) | Premium Upsell 02 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 503 | `Screens/Mobile App/Subscription/Subscription Management-01.png` | Mobile App | Feature C24 (Subscription & Billing) | Subscription Management 01 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 504 | `Screens/Mobile App/Subscription/Subscription Management-02.png` | Mobile App | Feature C24 (Subscription & Billing) | Subscription Management 02 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 505 | `Screens/Mobile App/Subscription/Trial Disclosure-01.png` | Mobile App | Feature C24 (Subscription & Billing) | Trial Disclosure 01 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 506 | `Screens/Mobile App/Subscription/Trial Disclosure-02.png` | Mobile App | Feature C24 (Subscription & Billing) | Trial Disclosure 02 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 507 | `Screens/Mobile App/Subscription/Trial Disclosure-03.png` | Mobile App | Feature C24 (Subscription & Billing) | Trial Disclosure 03 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 508 | `Screens/Mobile App/Support/My Tickets.png` | Mobile App | Feature C25 (Notifications & Support) | My Tickets | `GET /v1/support/tickets, POST /v1/support/tickets` |
| 509 | `Screens/Mobile App/Support/New Ticket-01.png` | Mobile App | Feature C25 (Notifications & Support) | New Ticket 01 | `GET /v1/support/tickets, POST /v1/support/tickets` |
| 510 | `Screens/Mobile App/Support/New Ticket-02.png` | Mobile App | Feature C25 (Notifications & Support) | New Ticket 02 | `GET /v1/support/tickets, POST /v1/support/tickets` |
| 511 | `Screens/Mobile App/Support/New Ticket-03.png` | Mobile App | Feature C25 (Notifications & Support) | New Ticket 03 | `GET /v1/support/tickets, POST /v1/support/tickets` |
| 512 | `Screens/Mobile App/Support/Support Center-01.png` | Mobile App | Feature C25 (Notifications & Support) | Support Center 01 | `GET /v1/support/tickets, POST /v1/support/tickets` |
| 513 | `Screens/Mobile App/Support/Support Center-02.png` | Mobile App | Feature C25 (Notifications & Support) | Support Center 02 | `GET /v1/support/tickets, POST /v1/support/tickets` |
| 514 | `Screens/Mobile App/Support/Support Center-03.png` | Mobile App | Feature C25 (Notifications & Support) | Support Center 03 | `GET /v1/support/tickets, POST /v1/support/tickets` |
| 515 | `Screens/Mobile App/Support/Ticket Detail-01.png` | Mobile App | Feature C25 (Notifications & Support) | Ticket Detail 01 | `GET /v1/support/tickets, POST /v1/support/tickets` |
| 516 | `Screens/Mobile App/Support/Ticket Detail-02.png` | Mobile App | Feature C25 (Notifications & Support) | Ticket Detail 02 | `GET /v1/support/tickets, POST /v1/support/tickets` |
| 517 | `Screens/Parent Web/01-Sign in to your account-01.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 01 Sign in to your account 01 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 518 | `Screens/Parent Web/01-Sign in to your account-02.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 01 Sign in to your account 02 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 519 | `Screens/Parent Web/02-signin-otp-01.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 02 signin otp 01 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 520 | `Screens/Parent Web/02-signin-otp-02.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 02 signin otp 02 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 521 | `Screens/Parent Web/03-Account Home.png` | Parent Web | Feature A2 (Home Dashboard) | 03 Account Home | `GET /v1/home/dashboard, GET /v1/ai/recommendations` |
| 522 | `Screens/Parent Web/04-Account & Security-01.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 04 Account & Security 01 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 523 | `Screens/Parent Web/04-Account & Security-02.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 04 Account & Security 02 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 524 | `Screens/Parent Web/04-Account & Security-03.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 04 Account & Security 03 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 525 | `Screens/Parent Web/04-Account & Security-04.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 04 Account & Security 04 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 526 | `Screens/Parent Web/04-Account & Security-05.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 04 Account & Security 05 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 527 | `Screens/Parent Web/04-Account & Security-06.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 04 Account & Security 06 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 528 | `Screens/Parent Web/04-Account & Security-07.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 04 Account & Security 07 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 529 | `Screens/Parent Web/04-Account & Security-08.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 04 Account & Security 08 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 530 | `Screens/Parent Web/04-Account & Security-09.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 04 Account & Security 09 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 531 | `Screens/Parent Web/05-Connected Devices-01.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 05 Connected Devices 01 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 532 | `Screens/Parent Web/05-Connected Devices-02.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 05 Connected Devices 02 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 533 | `Screens/Parent Web/05-Connected Devices-03.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 05 Connected Devices 03 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 534 | `Screens/Parent Web/05-Connected Devices-04.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 05 Connected Devices 04 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 535 | `Screens/Parent Web/06-Subscription & Invoices-01.png` | Parent Web | Feature C24 (Subscription & Billing) | 06 Subscription & Invoices 01 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 536 | `Screens/Parent Web/06-Subscription & Invoices-02.png` | Parent Web | Feature C24 (Subscription & Billing) | 06 Subscription & Invoices 02 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 537 | `Screens/Parent Web/06-Subscription & Invoices-03.png` | Parent Web | Feature C24 (Subscription & Billing) | 06 Subscription & Invoices 03 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 538 | `Screens/Parent Web/06-Subscription & Invoices-04.png` | Parent Web | Feature C24 (Subscription & Billing) | 06 Subscription & Invoices 04 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 539 | `Screens/Parent Web/06-Subscription & Invoices-05.png` | Parent Web | Feature C24 (Subscription & Billing) | 06 Subscription & Invoices 05 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 540 | `Screens/Parent Web/06-Subscription & Invoices-06.png` | Parent Web | Feature C24 (Subscription & Billing) | 06 Subscription & Invoices 06 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 541 | `Screens/Parent Web/06-Subscription & Invoices-07.png` | Parent Web | Feature C24 (Subscription & Billing) | 06 Subscription & Invoices 07 | `GET /v1/billing/plans, POST /v1/billing/subscribe` |
| 542 | `Screens/Parent Web/07-Consent & Privacy-01.png` | Parent Web | Feature C26 (Privacy & Consent) | 07 Consent & Privacy 01 | `GET /v1/privacy/consents, DELETE /v1/privacy/ai-history` |
| 543 | `Screens/Parent Web/07-Consent & Privacy-02.png` | Parent Web | Feature C26 (Privacy & Consent) | 07 Consent & Privacy 02 | `GET /v1/privacy/consents, DELETE /v1/privacy/ai-history` |
| 544 | `Screens/Parent Web/07-Consent & Privacy-03.png` | Parent Web | Feature C26 (Privacy & Consent) | 07 Consent & Privacy 03 | `GET /v1/privacy/consents, DELETE /v1/privacy/ai-history` |
| 545 | `Screens/Parent Web/07-Consent & Privacy-04.png` | Parent Web | Feature C26 (Privacy & Consent) | 07 Consent & Privacy 04 | `GET /v1/privacy/consents, DELETE /v1/privacy/ai-history` |
| 546 | `Screens/Parent Web/07-Consent & Privacy-05.png` | Parent Web | Feature C26 (Privacy & Consent) | 07 Consent & Privacy 05 | `GET /v1/privacy/consents, DELETE /v1/privacy/ai-history` |
| 547 | `Screens/Parent Web/08-Data Export-01.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 08 Data Export 01 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 548 | `Screens/Parent Web/08-Data Export-02.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 08 Data Export 02 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 549 | `Screens/Parent Web/08-Data Export-03.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 08 Data Export 03 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 550 | `Screens/Parent Web/08-Data Export-04.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 08 Data Export 04 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 551 | `Screens/Parent Web/08-Data Export-05.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 08 Data Export 05 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 552 | `Screens/Parent Web/08-Data Export-06.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 08 Data Export 06 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 553 | `Screens/Parent Web/08-Data Export-07.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 08 Data Export 07 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 554 | `Screens/Parent Web/09-Account Deletion-01.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 09 Account Deletion 01 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 555 | `Screens/Parent Web/09-Account Deletion-02.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 09 Account Deletion 02 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 556 | `Screens/Parent Web/09-Account Deletion-03.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 09 Account Deletion 03 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 557 | `Screens/Parent Web/09-Account Deletion-04.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 09 Account Deletion 04 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 558 | `Screens/Parent Web/09-Account Deletion-05.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 09 Account Deletion 05 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 559 | `Screens/Parent Web/10-Account Deletion Pending-01.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 10 Account Deletion Pending 01 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 560 | `Screens/Parent Web/10-Account Deletion Pending-02.png` | Parent Web | Feature D27 (Parent Web Account Portal) | 10 Account Deletion Pending 02 | `GET /v1/parent/account, POST /v1/identity/auth/otp/verify` |
| 561 | `Screens/Parent Web/11-Support-01.png` | Parent Web | Feature C25 (Notifications & Support) | 11 Support 01 | `GET /v1/support/tickets, POST /v1/support/tickets` |
| 562 | `Screens/Parent Web/11-Support-02.png` | Parent Web | Feature C25 (Notifications & Support) | 11 Support 02 | `GET /v1/support/tickets, POST /v1/support/tickets` |

---

## 5. Summary of Future AI Implementation Workflow
When implementing any feature in the codebase:
1. **Locate the Feature Folder** in `Development_Blueprints/` (e.g., `A1_Splash_Auth_Onboarding`).
2. **Open the Feature Visual Blueprint**: `00-screen-to-code-visual-blueprint.md`.
3. **Inspect ALL Screen Images** referenced for that feature before writing code.
4. **Implement Backend APIs First**: Follow the exact schema, DTOs, and error codes documented in the `Backend/` blueprints.
5. **Implement Frontend Components & ViewModels**: Follow the 5-state UI pattern, Material 3 design tokens, and exact route configurations documented in the `KMP/` or `NextJS_Admin/` or `Parent_Web_Portal/` blueprints.
