# Feature B15: Offline Downloads & Sync — Visual & System Blueprint

## 1. Feature Identification & Reference
- **Feature ID**: Feature B.15
- **PRD Reference**: `PRD_Documents/Child App Supporting (13-18)/Feature_B15_Offline_Downloads_Sync.md`
- **Target Module**: `:core-database`, `:core-network` (KMP) & `sync` service (Backend)
- **Primary User Role**: Child Learner (Offline playback) & Parent (Storage manager)

---

## 2. Architectural Blueprint & Screen Overlay Specifications
- **Visual Overlays**:
  - Offline badge indicators rendered across `Screens/Mobile App/Stories/Story Detail-02.png`, `Screens/Mobile App/Home/Home-09.png`, and `Screens/Mobile App/Favorites/Favorites-05.png`.
  - In-app storage bar indicating downloaded Islamic content size (MB) and "Download for Offline" toggle.
- **Offline Sync Pipeline**: SQLDelight encrypted client-side storage, background Ktor chunked asset downloader, and opportunistic upload of offline quiz attempts and habit logs upon reconnect.
