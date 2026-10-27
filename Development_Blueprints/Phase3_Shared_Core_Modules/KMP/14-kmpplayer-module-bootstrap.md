# Phase 3 — kmpplayer: Architecture & Bootstrap Blueprint

`Development_Blueprints.Phase3_Shared_Core_Modules.KMP.14-kmpplayer-module-bootstrap.md`

**Module:** `kmpplayer` (KMP Android & iOS)  
**Phase:** 3 — Shared/Core Modules  
**Status:** ✅ **Implemented & Verified** (Verified against `NoorHeroes/core/kmpplayer/CORE_KMP_PLAYER_INSTRUCTIONS.md`)  
**Description:** Multiplatform media playback engine for audio stories, Quran recitations, and soundscapes (ExoPlayer Android, AVPlayer iOS) with background audio and bedtime calming fade-out.  
**Depends on:** Phase 0 Workspace, Phase 2 Security Baseline Prerequisites  
**Consumed by:** All Phase 4, Phase 5, Phase 6, Phase 8, and Phase 10 feature implementations  
**Source of truth:** `NoorHeroes/core/kmpplayer/CORE_KMP_PLAYER_INSTRUCTIONS.md`; `NoorHeroes_Consolidated_Execution_Blueprint.md` §4  

---

## 1. Objective and Purpose
Provide high-fidelity, crash-resilient audio playback supporting stories, pronunciation practice, and bedtime sleep journeys.

## 2. Technical Requirements
- Engine: Android Media3 / ExoPlayer; iOS AVQueuePlayer.
- Features: Stream caching, playback rate control (0.75x, 1.0x, 1.25x), audio focus ducking/pause on incoming calls, lock-screen media controls.
- Bedtime Mode: Sleep timer with 60-second gentle volume fade-out and silent completion signaling (A.4).

## 3. Technology Stack Preservation
- AndroidX Media3, Apple AVFoundation.

## 4. Verification and Acceptance Criteria
- [x] Background audio continues playing when screen locks.
- [x] Sleep timer fades volume smoothly to zero without pops or clicks.

