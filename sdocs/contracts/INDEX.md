# Contract Index: Stories Module

| Contract ID | Kind | Title | Owner Story | Status |
|---|---|---|---|---|
| `api.content-catalog` | api | Content Catalog Stories API (`GET /v1/content`) | STORY-002 | stable |
| `api.favorite-toggle` | api | Favorite Toggle API (`POST /v1/favorites`) | STORY-001 | stable |
| `api.favorites-listing` | api | Child Favorites Listing API (`GET /v1/children/{id}/favorites`) | STORY-003 | stable |
| `data.story-cache` | repo | Story Catalog Cache Interface | STORY-002 | stable |
| `domain.story-library` | repo | Story Library Repository & Domain Interface | STORY-003 | stable |
| `type.favorite-models` | type | Favorite Persistence Entity and DTOs | STORY-001 | stable |
| `api.story-detail` | api | Story Detail API (`GET /v1/content/{id}`) | STORY-007 | stable |
| `domain.story-detail` | repo | Story Detail Domain & Repository Interface | STORY-007 | stable |
| `api.story-manifest` | api | Signed Media Manifest API (`GET /v1/content/{id}/manifest`) | STORY-012 | draft |
| `api.playback-heartbeat` | api | Playback Heartbeat API (`POST /v1/playback/{content_id}`) | STORY-012 | draft |
| `domain.story-player` | type | Story Player State Machine & Domain Entities | STORY-013 | draft |
| `repo.story-manifest` | repo | Manifest & Playback Heartbeat Repository Interface | STORY-012 | draft |
| `api.favorites-pattern-report` | api | Admin Favoriting Pattern Report API (`GET /admin/v1/favorites/pattern-report`) | STORY-004 | stable |
| `api.choice-event` | api | Interactive Choice Event API (`POST /v1/content/{id}/choice`) | STORY-019 | draft |
| `domain.branch-resolution` | type | Deterministic Story Branch Resolution Domain Model & Engine | STORY-018 | draft |
| `repo.choice-event` | repo | Choice Event Repository & Offline Outbox Interface | STORY-019 | draft |
| `api.download-manifest` | api | Download Manifest Issuance API (`POST /v1/downloads/manifest`) | TASK-B01 | stable |
| `api.download-inventory` | api | Child Download Inventory & Removal API (`GET & DELETE /v1/children/{id}/downloads`) | TASK-B02 | stable |
| `domain.entitlement-policy-service` | repo | Entitlement & Download Policy Enforcement Service Interface | TASK-B03 | stable |
| `api.sync-batch` | api | Offline Sync Batch Ingestion API (`POST /v1/sync/batch`) | TASK-B04 | stable |
| `domain.sync-event-log` | repo | Sync Event Log & Idempotent Dedup Store Interface | TASK-B05 | stable |
| `domain.license-refresh-job` | worker | License & Entitlement Periodic Refresh Job (`downloads.refresh_download_entitlements`) | TASK-B06 | stable |
| `api.admin-downloads-health` | api | Admin Download & Sync Health Monitoring API (`GET /v1/admin/downloads/health` & `GET /v1/admin/sync/health`) | TASK-B07 | stable |
| `api.admin-default-download-caps` | api | Admin Default Download Cap Configuration API (`GET & PUT /v1/admin/downloads/default-caps`) | TASK-B08 | stable |

| `api.ramadan-campaign-status` | api | Ramadan Campaign Status API (`GET /v1/ramadan/campaign-status`) | STORY-036-01 | draft |
| `type.ramadan-models` | type | Ramadan Domain Entities and Persistence Models | STORY-036-01 | draft |
| `domain.hijri-calendar-service` | repo | Hijri Calendar & Moon-Sighting Override Service Interface | STORY-036-02 | draft |
| `api.ramadan-missions` | api | Ramadan Mission Content Delivery API (`GET /v1/ramadan/missions/{night}`) | STORY-036-03 | draft |
| `api.ramadan-fasting-logs` | api | Fasting Log API (`POST /v1/ramadan/fasting-logs`) | STORY-036-04 | draft |
| `api.ramadan-journey-progress` | api | Ramadan Journey Progress & Reward Completion API (`POST /v1/ramadan/missions/{night}/complete`) | STORY-036-05 | draft |
| `api.ramadan-family-aggregate` | api | Family Ramadan Aggregate API (`GET /v1/ramadan/family-aggregate`) | STORY-036-06 | draft |
| `api.ramadan-certificates` | api | Ramadan Certificate & Eid Card Generation API (`POST /v1/ramadan/certificates` & `POST /v1/ramadan/eid-cards`) | STORY-036-07 | draft |
| `api.admin-ramadan-eid-override` | api | Admin Eid Date Override & Notification API (`POST /v1/admin/ramadan/eid-date-override`) | STORY-036-08 | draft |
| `api.device-profile-binding` | api | Device Profile Binding & Token Registration API (`/v1/devices`) | TASK-B17-01 | stable |
| `domain.device-profile-binding` | service | Device Profile Binding Domain Engine & Exclusivity Rules | TASK-B17-01 | stable |
| `domain.notification-intent-service` | service | Notification Trigger Catalog & Intent Creation Engine | TASK-B17-02 | stable |
| `domain.notification-policy-engine` | service | Notification Policy Engine Send-Time Evaluation Rules | TASK-B17-03 | stable |
| `api.admin-notification-templates` | api | Admin Notification Copy Template Governance API (`/v1/admin/notifications/templates`) | TASK-B17-04 | stable |
| `domain.child-safe-template-governance` | service | Child-Safe Template Governance & Multi-Locale Rendering Domain Service | TASK-B17-04 | stable |
| `domain.delivery-adapter` | service | Delivery Adapter & Push Token Lifecycle Interface | TASK-B17-05 | stable |
| `api.deep-link-resolution` | api | Notification Deep Link Resolution API (`GET /v1/notifications/resolve`) | TASK-B17-06 | stable |
| `domain.deep-link-resolution` | service | Notification Deep Link Resolution Domain Service Interface | TASK-B17-06 | stable |
| `api.admin-notification-campaigns` | api | Admin Notification Campaign & Segment API (`/v1/admin/notifications/campaigns`) | TASK-B17-07 | stable |
| `domain.admin-notification-campaigns` | service | Notification Campaign & Segment Management Domain Service | TASK-B17-07 | stable |
| `api.admin-notification-reports` | api | Admin Notification Delivery, Engagement & Binding Health Reporting API (`/v1/admin/notifications/reports`) | TASK-B17-08 | stable |
| `domain.admin-notification-reports` | service | Notification Reporting & Binding Health Monitoring Domain Service | TASK-B17-08 | stable |
| `api.in-app-notifications` | api | In-App Notification Fetch API (`GET /v1/notifications/in-app`) | TASK-B17-09 | stable |
| `domain.in-app-notifications` | service | In-App Notification Projection & Eligibility Domain Service | TASK-B17-09 | stable |
| `domain.fact-versioning-approval` | service | Fact Content Versioning & Scholar Approval Domain Model & Invariants | TASK-B18-01 | stable |
| `api.daily-fact-selection` | api | Child Fact-of-the-Day Selection API (`GET /v1/facts/daily`) | TASK-B18-02 | stable |
| `domain.daily-fact-selection` | service | Child Daily Fact Selection Domain Service Interface | TASK-B18-02 | stable |
| `api.fact-detail-retrieval` | api | Islamic Fact Detail Retrieval API (`GET /v1/facts/{id}`) | TASK-B18-03 | stable |
| `domain.fact-detail-retrieval` | service | Fact Detail Retrieval Domain Service Interface | TASK-B18-03 | stable |
| `api.fact-linked-quiz` | api | Fact-Linked Quiz Delegation API (`GET /v1/quizzes/fact/{fact_id}`) | TASK-B18-04 | stable |
| `domain.fact-linked-quiz` | service | Fact-Linked Quiz Delegation Domain Service Interface | TASK-B18-04 | stable |
| `domain.islamic-facts-mastery` | service | Islamic Facts Mastery Engine Domain Registration & Extensibility Interface | TASK-B18-05 | stable |
| `api.admin-fact-editorial` | api | Admin Fact Editorial & Scholar-Approval Workflow API | TASK-B18-06 | stable |
| `domain.admin-fact-editorial-workflow` | service | Admin Fact Editorial & Scholar Approval Workflow Domain Service Interface | TASK-B18-06 | stable |
| `api.admin-fact-engagement` | api | Admin Fact Engagement Monitoring API (`GET /v1/admin/facts/engagement`) | TASK-B18-07 | stable |
| `domain.admin-fact-engagement-monitoring` | service | Admin Fact Engagement Monitoring Domain Service Interface | TASK-B18-07 | stable |
| `domain.fact-consolidation` | service | Fact Architecture Consolidation & Legacy Retirement Domain Contract | TASK-B18-08 | stable |
| `domain.fact-integrity-monitoring` | service | Content Integrity Monitoring & Disputed-Topic Bypass Canary Domain Contract | TASK-B18-09 | stable |



