# Screen inventory and controlled review order

Numbers follow the documented feature/journey review sequence. Alternate branches, overlays and system states are labeled; they are not mandatory steps in a single linear path. Source inventory tables frequently use filename order, which is not user encounter order. The global navigation document controls routing.

## A1

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 001 | [Splash Screen](Screen_Prompts/001_Splash_Screen.md) | screen | App cold start | Bootstrap routing decision |
| 002 | [Language Selection](Screen_Prompts/002_Language_Selection.md) | screen | First launch only (re-accessible from Settings post-auth) | Intro Slides |
| 003 | [Intro Slide 1 (Stories)](Screen_Prompts/003_Intro_Slide_1_Stories.md) | screen | Language Selection | Slide 2 / Skip → Login |
| 004 | [Intro Slide 2 (Quran/Arabic/Tajweed)](Screen_Prompts/004_Intro_Slide_2_Quran_Arabic_Tajweed.md) | screen | Slide 1 | Slide 3 / Skip → Login |
| 005 | [Intro Slide 3 (Habits & Rewards)](Screen_Prompts/005_Intro_Slide_3_Habits_Rewards.md) | screen | Slide 2 | Slide 4 / Skip → Login |
| 006 | [Intro Slide 4 (Parent Control)](Screen_Prompts/006_Intro_Slide_4_Parent_Control.md) | screen | Slide 3 | Login/Registration |
| 007 | [Login (phone/email + Google)](Screen_Prompts/007_Login_phone_email_Google.md) | screen | Intro, session expiry, logout, switch account | OTP Verification, Registration |
| 008 | [Registration + Consent](Screen_Prompts/008_Registration_Consent.md) | screen | Intro, Login "Register" link | OTP Verification |
| 009 | [Consent Detail / Full Text Modal](Screen_Prompts/009_Consent_Detail_Full_Text_Modal.md) | overlay | Registration "read full text" links | Back to Registration |
| 010 | [OTP Verification](Screen_Prompts/010_OTP_Verification.md) | screen | Login, Registration, Forgot Access | Profile Picker / Parent PIN Setup |
| 011 | [OTP Fallback Channel Offer](Screen_Prompts/011_OTP_Fallback_Channel_Offer.md) | overlay | OTP delivery failure | OTP Verification (new channel) |
| 012 | [Parent PIN Setup](Screen_Prompts/012_Parent_PIN_Setup.md) | screen | First-time post-OTP; Settings → Security (reset) | Biometric Enrollment / Add Child |
| 013 | [Biometric Enrollment Prompt](Screen_Prompts/013_Biometric_Enrollment_Prompt.md) | overlay | Parent PIN Setup | Add Child |
| 014 | [Add Child](Screen_Prompts/014_Add_Child.md) | screen | Parent PIN Setup, bootstrap (session, no children), "Add Child" tile | "Add another?" / Learning Level Confirm |
| 015 | [Avatar Selection](Screen_Prompts/015_Avatar_Selection.md) | overlay | Add Child | Add Child (continued) |
| 016 | [Interest Selection](Screen_Prompts/016_Interest_Selection.md) | overlay | Add Child | Add Child (continued) |
| 017 | [Learning Level Setup](Screen_Prompts/017_Learning_Level_Setup.md) | overlay | Add Child | Add Child (continued) / Learning Level Confirm |
| 018 | ["Add Another Child?" Prompt](Screen_Prompts/018_Add_Another_Child_Prompt.md) | overlay | After Add Child save | Add Child (loop) / Learning Level Confirm |
| 019 | [Learning Level + Interests Confirmation (family-level summary)](Screen_Prompts/019_Learning_Level_Interests_Confirmation_family_level_summary.md) | screen | After all children added | Screen Time / Notification Primer |
| 020 | [Screen Time & Notification Primer](Screen_Prompts/020_Screen_Time_Notification_Primer.md) | screen | Learning level confirm | Profile Picker |
| 021 | [Personalized Path Reveal](Screen_Prompts/021_Personalized_Path_Reveal.md) | screen | Screen Time primer (per child, optional delight screen) | Profile Picker |
| 022 | [Profile Picker ("Who Is Learning")](Screen_Prompts/022_Profile_Picker_Who_Is_Learning.md) | screen | Bootstrap (returning), end of onboarding | Child Lock Screen / Parent PIN Gate / Add Child |
| 023 | [Child Lock Screen (PIN/Pattern/Biometric)](Screen_Prompts/023_Child_Lock_Screen_PIN_Pattern_Biometric.md) | screen | Profile Picker (child tile, if lock configured) | Child Home / Lock Recovery |
| 024 | [Lock Recovery (via verified Parent Profile)](Screen_Prompts/024_Lock_Recovery_via_verified_Parent_Profile.md) | screen | Child Lock Screen "forgot lock" | Parent PIN Gate → Child Lock reset |
| 025 | [First Mission Screen](Screen_Prompts/025_First_Mission_Screen.md) | screen | Child Home, first entry only | Child Home (mission content) |
| 026 | [Forced Update Blocking Screen](Screen_Prompts/026_Forced_Update_Blocking_Screen.md) | screen | Bootstrap (version below minimum) | App store / exit |
| 027 | [Recommended Update Banner/Dismissible](Screen_Prompts/027_Recommended_Update_Banner_Dismissible.md) | overlay | Bootstrap (version below recommended) | Dismiss → continues flow |
| 028 | [Maintenance Mode Screen](Screen_Prompts/028_Maintenance_Mode_Screen.md) | screen | Bootstrap (maintenance flag) | Retry / exit |
| 029 | [No Connectivity Screen (pre-auth)](Screen_Prompts/029_No_Connectivity_Screen_pre_auth.md) | screen | Splash/bootstrap with no network | Retry |
| 030 | [Forgot Access / Account Recovery Entry](Screen_Prompts/030_Forgot_Access_Account_Recovery_Entry.md) | screen | Login screen | OTP Verification (recovery mode) |
| 031 | [Terms of Service (full document)](Screen_Prompts/031_Terms_of_Service_full_document.md) | screen | Registration, Settings | Back |
| 032 | [Privacy Policy (full document)](Screen_Prompts/032_Privacy_Policy_full_document.md) | screen | Registration, Settings | Back |
| 033 | [Child-Data Processing Consent (full document)](Screen_Prompts/033_Child_Data_Processing_Consent_full_document.md) | screen | Registration | Back |
## A2

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 034 | [Child Home (composite screen)](Screen_Prompts/034_Child_Home_composite_screen.md) | screen | Profile Picker, app resume, bottom nav "Home" tab | All feature tabs, Search, Notifications |
| 035 | [Full-Screen Retry (no cache, no network)](Screen_Prompts/035_Full_Screen_Retry_no_cache_no_network.md) | screen | Home, true cold-start offline | Retry → Home |
## A3

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 036 | [Stories Library (Landing)](Screen_Prompts/036_Stories_Library_Landing.md) | screen | Bottom nav "Stories" tab, Home, Search results | Story Detail |
| 037 | [Category Filter Panel](Screen_Prompts/037_Category_Filter_Panel.md) | overlay | Library filter icon | Library (filtered) |
| 038 | [Story Detail](Screen_Prompts/038_Story_Detail.md) | screen | Library, Search, Home "Continue", Favorites | Story Player, Episode list items |
| 039 | [Story Player — Video](Screen_Prompts/039_Story_Player_Video.md) | screen | Story Detail, Continue Watching | Completion flow / Back to Detail |
| 040 | [Story Player — Audio](Screen_Prompts/040_Story_Player_Audio.md) | screen | Story Detail, Continue Listening, Bedtime Corner | Completion flow / Back to Detail |
| 041 | [Story Player — Text](Screen_Prompts/041_Story_Player_Text.md) | screen | Story Detail (text-format stories) | Completion flow / Back to Detail |
| 042 | [Interactive Choice Overlay](Screen_Prompts/042_Interactive_Choice_Overlay.md) | overlay | Mid-playback, scripted choice points | Resumes playback with branch |
| 043 | [Pause-and-Quiz Moment Overlay](Screen_Prompts/043_Pause_and_Quiz_Moment_Overlay.md) | overlay | Mid-playback, scripted quiz points | Resumes playback |
| 044 | [Media Unavailable / Safe-Stop Screen](Screen_Prompts/044_Media_Unavailable_Safe_Stop_Screen.md) | screen | Mid-playback withdrawal event | Recommended alternative card |
| 045 | [Completion / Reward Reveal Screen](Screen_Prompts/045_Completion_Reward_Reveal_Screen.md) | screen | End of playback, threshold reached | Moral Summary |
| 046 | [Moral Summary Card ("Noor says...")](Screen_Prompts/046_Moral_Summary_Card_Noor_says.md) | screen | Post-completion | Post-story Quiz or Next Learning |
| 047 | [Post-Story Quiz](Screen_Prompts/047_Post_Story_Quiz.md) | screen | Moral Summary | Next Learning suggestion |
| 048 | [Achievement/Badge Unlock Modal](Screen_Prompts/048_Achievement_Badge_Unlock_Modal.md) | overlay | Completion flow, if a badge threshold is crossed | Dismiss → returns to flow |
| 049 | [Approved Share Card Preview](Screen_Prompts/049_Approved_Share_Card_Preview.md) | screen | Parent gate success | Send/cancel |
| 050 | [Caption/Audio-Track/Quality Settings Sheet](Screen_Prompts/050_Caption_Audio_Track_Quality_Settings_Sheet.md) | overlay | Player settings icon | Resumes playback with new settings |
## A4

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 051 | [Audio Bedtime Player (main screen)](Screen_Prompts/051_Audio_Bedtime_Player_main_screen.md) | screen | Home Bedtime Corner, Stories Library "Bedtime Stories" category, Calm Mode toggle, Continue Listening (Home) | Dua ending card, Next Episode, Back to Library |
| 052 | [Episode List Sheet (for multi-part audio series)](Screen_Prompts/052_Episode_List_Sheet_for_multi_part_audio_series.md) | overlay | "Episodes" control in player | Selecting an episode → Player (new content) |
| 053 | [Sleep Timer Selector](Screen_Prompts/053_Sleep_Timer_Selector.md) | overlay | Sleep Timer icon | Player (timer active) |
| 054 | [Playback Speed Selector](Screen_Prompts/054_Playback_Speed_Selector.md) | overlay | Speed icon | Player (speed applied) |
| 055 | [Goodnight Idle State](Screen_Prompts/055_Goodnight_Idle_State.md) | screen | Sleep timer auto-pause, or manual pause-and-leave | Resume playback / Exit player |
| 056 | [Dua / Calm-Reflection Ending Card](Screen_Prompts/056_Dua_Calm_Reflection_Ending_Card.md) | screen | Completion threshold reached during Bedtime Mode | Next Episode offer / Back to Library |
| 057 | [Media Unavailable / Safe-Stop (Bedtime-styled variant)](Screen_Prompts/057_Media_Unavailable_Safe_Stop_Bedtime_styled_variant.md) | screen | Mid-playback withdrawal | Recommended alternative / dua fallback |
## A5

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 058 | [Learn Tab Landing / Quran Learning Home (Skill Tree Map)](Screen_Prompts/058_Learn_Tab_Landing_Quran_Learning_Home_Skill_Tree_Map.md) | screen | Bottom nav "Learn" tab, Home "Continue Learning" | Surah Learning, Arabic Letters, Tajweed, Quran Game modes |
| 059 | [Placement Check (first-time)](Screen_Prompts/059_Placement_Check_first_time.md) | screen | Quran Learning Home, first visit | Skill Tree (pre-populated states) |
| 060 | [Mode Selector Sheet](Screen_Prompts/060_Mode_Selector_Sheet.md) | overlay | Quran Learning Home | Specific game mode screen |
| 061 | [Surah Learning](Screen_Prompts/061_Surah_Learning.md) | screen | Skill Tree node tap | Recitation Recorder, Dua Learning (A.6), back to Skill Tree |
| 062 | [Recitation Recorder Overlay](Screen_Prompts/062_Recitation_Recorder_Overlay.md) | overlay | "Record" action | Feedback screen / Listen-only fallback |
| 063 | [AI Pronunciation Feedback Screen](Screen_Prompts/063_AI_Pronunciation_Feedback_Screen.md) | screen | Recorder submission | Mark-practiced action, Retry |
| 064 | [Listen-Only Self-Assessment Screen](Screen_Prompts/064_Listen_Only_Self_Assessment_Screen.md) | screen | Mic disabled/denied path | Mark-practiced action |
| 065 | [Arabic Letters — Hear & Match](Screen_Prompts/065_Arabic_Letters_Hear_Match.md) | screen | Skill Tree (letter node) | Tracing screen |
| 066 | [Arabic Letters — Tracing](Screen_Prompts/066_Arabic_Letters_Tracing.md) | screen | Hear & Match | Word-context screen |
| 067 | [Arabic Letters — Word Context](Screen_Prompts/067_Arabic_Letters_Word_Context.md) | screen | Tracing | Skill Tree (progress update) |
| 068 | [Arabic Letters — Word-Building (sound tiles)](Screen_Prompts/068_Arabic_Letters_Word_Building_sound_tiles.md) | screen | Mode Selector | Skill Tree |
| 069 | [Tajweed — Rule Introduction](Screen_Prompts/069_Tajweed_Rule_Introduction.md) | screen | Skill Tree (Tajweed node) | Listen step |
| 070 | [Tajweed — Listen (normal/slow)](Screen_Prompts/070_Tajweed_Listen_normal_slow.md) | screen | Rule Introduction | Identification step |
| 071 | [Tajweed — Rule Identification Exercise](Screen_Prompts/071_Tajweed_Rule_Identification_Exercise.md) | screen | Listen step | Optional Record / Assessment |
| 072 | [Tajweed — Assessment](Screen_Prompts/072_Tajweed_Assessment.md) | screen | Identification (or Record) | Skill Tree (progress update) |
| 073 | [Quran Game — Ayah Ordering](Screen_Prompts/073_Quran_Game_Ayah_Ordering.md) | screen | Mode Selector | Skill Tree |
| 074 | [Quran Game — Listen & Select Matching Ayah](Screen_Prompts/074_Quran_Game_Listen_Select_Matching_Ayah.md) | screen | Mode Selector | Skill Tree |
| 075 | [Quran Game — Missing Word](Screen_Prompts/075_Quran_Game_Missing_Word.md) | screen | Mode Selector | Skill Tree |
| 076 | [Quran Game — Surah Theme Matching](Screen_Prompts/076_Quran_Game_Surah_Theme_Matching.md) | screen | Mode Selector | Skill Tree |
| 077 | [Quran Game — Recitation Echo](Screen_Prompts/077_Quran_Game_Recitation_Echo.md) | screen | Mode Selector | AI Feedback / Listen-only fallback |
| 078 | [Quran Game — Progressive Memorization Reveal](Screen_Prompts/078_Quran_Game_Progressive_Memorization_Reveal.md) | screen | Mode Selector | Skill Tree |
| 079 | [Hint Overlay (progressive hint)](Screen_Prompts/079_Hint_Overlay_progressive_hint.md) | overlay | "Hint" control | Resumes exercise |
| 080 | [Mastery Badge/Node-Unlock Celebration](Screen_Prompts/080_Mastery_Badge_Node_Unlock_Celebration.md) | overlay | Skill Tree, threshold crossed | Dismiss → Skill Tree |
| 081 | [Microphone Permission Rationale / One-Time Explainer](Screen_Prompts/081_Microphone_Permission_Rationale_One_Time_Explainer.md) | overlay | First recording attempt | Dismiss → proceeds per permission outcome |
| 082 | [Arabic Letters — Contextual Form Matching (Isolated / Initial / Medial / Final)](Screen_Prompts/082_Arabic_Letters_Contextual_Form_Matching_Isolated_Initial_Medial_Final.md) | state | A5-08 Hear & Match or A5-10 Word Context selected by content metadata | Same owning Arabic exercise flow; no new top-level route |
| 083 | [Arabic Letters — Harakah Sound Pairing](Screen_Prompts/083_Arabic_Letters_Harakah_Sound_Pairing.md) | state | A5-08 Hear & Match selected by content metadata | Same owning Arabic exercise flow; no new top-level route |
## A6

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 084 | [Dua Learning Landing (Category List)](Screen_Prompts/084_Dua_Learning_Landing_Category_List.md) | screen | Learn Tab, Search | Category Dua List |
| 085 | [Category Dua List](Screen_Prompts/085_Category_Dua_List.md) | screen | Dua Learning Landing | Dua Card Detail |
| 086 | [Dua Card Detail (Arabic/Transliteration/Translation/Audio)](Screen_Prompts/086_Dua_Card_Detail_Arabic_Transliteration_Translation_Audio.md) | screen | Category List, Search, Favorites, Habit Tracker deep link | Recall Quiz, back to list |
| 087 | [Recall Quiz Question Screen](Screen_Prompts/087_Recall_Quiz_Question_Screen.md) | screen | Recall Quiz Entry Prompt | Next question / Result |
| 088 | [Recall Quiz Result / Pass Screen](Screen_Prompts/088_Recall_Quiz_Result_Pass_Screen.md) | screen | Final question answered correctly | Dua Master badge progress / back to list |
| 089 | [Dua Master Badge Progress Celebration (milestone)](Screen_Prompts/089_Dua_Master_Badge_Progress_Celebration_milestone.md) | overlay | Crossing a badge threshold | Dismiss → Achievements (A.11) |
| 090 | [Habit Tracker Reminder Suggestion Prompt](Screen_Prompts/090_Habit_Tracker_Reminder_Suggestion_Prompt.md) | overlay | Dua marked Learned | Habit Tracker (A.7) setup, or dismiss |
## A7

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 091 | [Habit Builder — Today's Checklist](Screen_Prompts/091_Habit_Builder_Today_s_Checklist.md) | screen | Home habit widget, bottom-nav/Learn-adjacent entry, deep links | Streak Calendar, Noor Garden, individual habit detail interactions |
| 092 | [Dhikr Counter Screen](Screen_Prompts/092_Dhikr_Counter_Screen.md) | screen | Today's Checklist (dhikr habit tap) | Today's Checklist (progress updated) |
| 093 | [Good Deed Logging — Category Selector](Screen_Prompts/093_Good_Deed_Logging_Category_Selector.md) | overlay | Today's Checklist (good deed habit tap) | Optional Note entry / direct check-in |
| 094 | [Good Deed Optional Note Entry](Screen_Prompts/094_Good_Deed_Optional_Note_Entry.md) | screen | Category Selector | Check-in confirmation |
| 095 | [Streak Calendar / History View](Screen_Prompts/095_Streak_Calendar_History_View.md) | screen | Today's Checklist "view streak history" | Today's Checklist |
| 096 | [Recovery Mission Screen](Screen_Prompts/096_Recovery_Mission_Screen.md) | screen | Streak State Detail (Broken → Recovery) | Today's Checklist (streak restored to Active) |
| 097 | [Streak State Detail — AtRisk / Protected / Broken / Recovery](Screen_Prompts/097_Streak_State_Detail_AtRisk_Protected_Broken_Recovery.md) | overlay | Checklist gentle streak banner / Calendar selected streak state | Recovery Mission / Smaller-target suggestion / dismiss to caller |
| 098 | [Mercy-Toned Smaller-Target Suggestion Prompt](Screen_Prompts/098_Mercy_Toned_Smaller_Target_Suggestion_Prompt.md) | overlay | Missed-habit pattern detected | Accept (adjusts target) / Dismiss |
| 099 | [Noor Garden — Personal View](Screen_Prompts/099_Noor_Garden_Personal_View.md) | screen | Today's Checklist "Open Noor Garden" | Family Garden (if applicable), Avatar (A.9) |
| 100 | [Noor Garden — Family View](Screen_Prompts/100_Noor_Garden_Family_View.md) | screen | Personal Garden entry point | Personal Garden |
| 101 | [Family Streak Milestone Celebration](Screen_Prompts/101_Family_Streak_Milestone_Celebration.md) | overlay | Family threshold crossed | Dismiss → Family Garden |
## A8

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 102 | [Quiz Question Screen — Multiple Choice](Screen_Prompts/102_Quiz_Question_Screen_Multiple_Choice.md) | screen | Quiz Entry Card | Per-Answer Explanation |
| 103 | [Quiz Question Screen — Sequence/Ordering](Screen_Prompts/103_Quiz_Question_Screen_Sequence_Ordering.md) | screen | Quiz Entry Card | Per-Answer Explanation |
| 104 | [Quiz Question Screen — True/False](Screen_Prompts/104_Quiz_Question_Screen_True_False.md) | screen | Quiz Entry Card | Per-Answer Explanation |
| 105 | [Quiz Question Screen — Image Match](Screen_Prompts/105_Quiz_Question_Screen_Image_Match.md) | screen | Quiz Entry Card | Per-Answer Explanation |
| 106 | [Quiz Question Screen — Audio Match](Screen_Prompts/106_Quiz_Question_Screen_Audio_Match.md) | screen | Quiz Entry Card | Per-Answer Explanation |
| 107 | [Per-Answer Explanation Overlay](Screen_Prompts/107_Per_Answer_Explanation_Overlay.md) | overlay | Every question, after submission | Next question / Retry Set / Completion |
| 108 | [Retry Set Entry Screen](Screen_Prompts/108_Retry_Set_Entry_Screen.md) | screen | End of main question set, if any incorrect | Retry Question Screens |
| 109 | [Quiz Completion / Effort XP Reveal](Screen_Prompts/109_Quiz_Completion_Effort_XP_Reveal.md) | screen | End of main set (no misses) or end of retry round | Skill Mastery update (background), Parent report availability |
## A9

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 110 | [Quiz Completion Result Screen (shared, generic)](Screen_Prompts/110_Quiz_Completion_Result_Screen_shared_generic.md) | screen | End of any quiz/practice attempt (any domain, any A.8 `QuizContext`) | Review Mistakes / Try Again / Continue |
| 111 | [Review Mistakes Screen](Screen_Prompts/111_Review_Mistakes_Screen.md) | screen | Quiz Completion Result "Review Mistakes" | Back to Result / Continue |
| 112 | [Offline Completion — Saved / Results Deferred](Screen_Prompts/112_Offline_Completion_Saved_Results_Deferred.md) | screen | Offline quiz completion before validated server result | Originating context; deferred real Quiz Completion Result after connectivity and sync |
## A10

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 113 | [Games Hub (tile grid landing)](Screen_Prompts/113_Games_Hub_tile_grid_landing.md) | screen | Home "Trending Games" rail, Rewards screen, dedicated nav entry (if present) | Individual game session |
| 114 | [Game-Specific Play Screen (per game, mechanics detailed in A.5 for Quran/Arabic games; new mini-games follow the same wrapper)](Screen_Prompts/114_Game_Specific_Play_Screen_per_game_mechanics_detailed_in_A_5_for_Quran_Arabic_games_new_mini_games_follow_the_same_wrapper.md) | screen | Game Session Loading | Session Completion |
| 115 | [Session Completion Screen (generic wrapper, reuses A.9's "strengths + next step" framing where applicable)](Screen_Prompts/115_Session_Completion_Screen_generic_wrapper_reuses_A_9_s_strengths_next_step_framing_where_applicable.md) | screen | End of any game session | Replay / Return to launching screen |
## A11

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 116 | [Rewards Hub / Wallet (landing)](Screen_Prompts/116_Rewards_Hub_Wallet_landing.md) | screen | Bottom nav "Rewards" tab, Home Milestones widget, completion-screen "View Rewards" link | Achievements, Challenges, Achievement Store, Avatar |
| 117 | [Transaction Detail (single ledger entry)](Screen_Prompts/117_Transaction_Detail_single_ledger_entry.md) | screen | Transaction History | Back |
| 118 | [Achievements Screen (badge grid + cumulative level progress)](Screen_Prompts/118_Achievements_Screen_badge_grid_cumulative_level_progress.md) | screen | Rewards Wallet, Profile | Badge Detail, Achievement Level Detail |
| 119 | [Badge Detail / Criteria View](Screen_Prompts/119_Badge_Detail_Criteria_View.md) | screen | Achievements grid | Back, or relevant activity |
| 120 | [Achievement Level Detail](Screen_Prompts/120_Achievement_Level_Detail.md) | screen | Achievements screen | Back |
| 121 | [Shareable Achievement Card Preview](Screen_Prompts/121_Shareable_Achievement_Card_Preview.md) | screen | Achievements/Badge Detail "Share" action | Parent Gate → OS Share Sheet, or cancel |
| 122 | [Weekly Challenge Detail](Screen_Prompts/122_Weekly_Challenge_Detail.md) | screen | Weekly Challenge Card | Relevant activity that advances it, Claim action |
| 123 | [Seasonal Event Screen](Screen_Prompts/123_Seasonal_Event_Screen.md) | screen | Seasonal Event Banner | Seasonal-specific missions/challenges |
| 124 | [Archived Challenge View](Screen_Prompts/124_Archived_Challenge_View.md) | screen | Challenges screen, expired challenge tap | Back |
| 125 | [Achievement Store (catalog browse)](Screen_Prompts/125_Achievement_Store_catalog_browse.md) | screen | Rewards Hub, Avatar screen "Shop" entry | Item Detail |
| 126 | [Achievement Store — Item Detail](Screen_Prompts/126_Achievement_Store_Item_Detail.md) | screen | Achievement Store grid | Purchase Confirmation |
| 127 | [Purchase Confirmation / Insufficient-Points Shortfall Screen](Screen_Prompts/127_Purchase_Confirmation_Insufficient_Points_Shortfall_Screen.md) | screen | Item Detail "Buy" | Success → Avatar Inventory; Shortfall → earn-suggestions |
| 128 | [Family Board (private, multi-child families)](Screen_Prompts/128_Family_Board_private_multi_child_families.md) | screen | Rewards Hub, Home (if surfaced) | Family Goal Detail |
| 129 | [Family Goal Detail](Screen_Prompts/129_Family_Goal_Detail.md) | screen | Family Board | Back |
| 130 | [Family Achievement Unlock Celebration](Screen_Prompts/130_Family_Achievement_Unlock_Celebration.md) | overlay | Family Board, threshold crossed | Dismiss → Family Board |
| 131 | [Badge Unlock Modal](Screen_Prompts/131_Badge_Unlock_Modal.md) | overlay | Any activity completion crossing a badge threshold | Dismiss → Achievements |
## A12

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 132 | [Avatar Screen (3D preview + owned grid + locked teasers)](Screen_Prompts/132_Avatar_Screen_3D_preview_owned_grid_locked_teasers.md) | screen | Rewards Hub (A.11), Profile tab avatar thumbnail | Item Detail, Locked Item Detail, relevant unlocking feature |
| 133 | [Item Detail (owned) — Equip/Unequip](Screen_Prompts/133_Item_Detail_owned_Equip_Unequip.md) | overlay | Owned-Items Grid | Avatar Screen (preview updated) |
| 134 | [Locked Item Detail — Unlock Criteria View](Screen_Prompts/134_Locked_Item_Detail_Unlock_Criteria_View.md) | overlay | Locked-Item Teaser | "Go to activity" deep link, or dismiss |
| 135 | [Character Evolution Milestone Reveal](Screen_Prompts/135_Character_Evolution_Milestone_Reveal.md) | overlay | Noor companion/avatar crossing an evolution threshold | Dismiss → returns to current screen (e.g., Home) |
## B13

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 136 | [Search](Screen_Prompts/136_Search.md) | screen | Contextual entry in source narrative | Any tab search icon → landing; recent/suggested query → Results; x removes one query, Clear all clears active child history; back restores invoking tab; mic explicit tap plus parent consent and OS permission → Listening. Suggestions must be moderated and age-eligible. |
| 137 | [Voice Search — Listening](Screen_Prompts/137_Voice_Search_Listening.md) | state | Contextual entry in source narrative | Explicit mic tap only; cancel/interruption discards partial audio → Search; completion → Processing; denied permission → text-only Search. Simulation control is prototype annotation pending approval. |
| 138 | [Voice Search — Processing](Screen_Prompts/138_Voice_Search_Processing.md) | state | Contextual entry in source narrative | Processing complete → Results; low-confidence → clarification; cancel → Search; no partial/garbled search. Raw audio not training data. |
| 139 | [Voice Search — Clarification](Screen_Prompts/139_Voice_Search_Clarification.md) | overlay | Contextual entry in source narrative | Low confidence asks retry or approved simplified clarification; retry → Listening, cancel → Search. No raw transcription leakage. |
| 140 | [Search Results](Screen_Prompts/140_Search_Results.md) | screen | Contextual entry in source narrative | Type chips All/Stories/Surahs/Duas requery; story → A3 Story Detail, surah → A5 Surah Learning, dua → A6 Dua Learning; close query clears input; mic → voice. Eligibility is authoritative server filtering, never adjustable beyond safe eligibility. |
| 141 | [Search Empty State](Screen_Prompts/141_Search_Empty_State.md) | state | Contextual entry in source narrative | Zero eligible results → friendly safe approved suggestion; edit query/retry → Search Results; back → invoking Search. Approved suggestion chips may rerun an age-safe query; no result-card links exist until new results return. Offline downloaded-index-empty is distinct from online no-match. |
| 142 | [Parent Area Search](Screen_Prompts/142_Parent_Area_Search.md) | screen | Contextual entry in source narrative | Gated Parent Dashboard → parent family reports/story activity/habits search; report → C22, story activity → A3 activity view, habit → A7 detail. Parent-session only; no child/admin search leakage. |
## B14

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 143 | [Favorites](Screen_Prompts/143_Favorites.md) | screen | Contextual entry in source narrative | Profile Favorites & Downloads → shared Saved shell Favorites; Downloads tab → B15; filter by content type; item → A3/A5/A6 detail; heart removes optimistically idempotently; withdrawn item cannot open; back → Profile. Save only eligible/unlocked/entitled content. All data active-child scoped. |
## B15

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 144 | [Downloads](Screen_Prompts/144_Downloads.md) | screen | Contextual entry in source narrative | Profile → Saved Downloads; completed item → owning offline player if license valid; retry resumable chunks and revalidate entitlement/cap; remove deletes only active child media; Clear All → confirmation; favorite tab independently scoped; content progress/history/favorites persist. Offline outbox causal sync/dedupe, reward exactly once. |
| 145 | [Clear All Downloads Confirmation](Screen_Prompts/145_Clear_All_Downloads_Confirmation.md) | overlay | Contextual entry in source narrative | Clear all → confirm/cancel; confirm removes active-child downloaded media only; cancel retains list and storage; no removal of favorites or progress. |
| 146 | [Parent Download Cap and Policy](Screen_Prompts/146_Parent_Download_Cap_and_Policy.md) | screen | Contextual entry in source narrative | Parent Controls → own child cap configuration; save policy; subsequent attempts over cap show supportive cap-reached state. Standard parent session and own-family constraints. |
## B16

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 147 | [Child Profile](Screen_Prompts/147_Child_Profile.md) | screen | Contextual entry in source narrative | Tab5 → active child profile; avatar → A12; Favorites & Downloads → shared Saved; language → Choose Language; Switch Profile ALWAYS parent gate then Who Is Learning then selected child lock or parent session; cancel/failure preserves child; successful switch clears child UI before rendering new identity. Stats display-only unless approved progress route. Disabled session → picker; cold start resolve session not saved screen identity. |
| 148 | [Choose Language](Screen_Prompts/148_Choose_Language.md) | overlay | Contextual entry in source narrative | Single selected display locale applies instantly app-wide; cancel dismisses untouched; offline apply locally and sync on reconnect per PRD. Content eligibility locale unaffected. |
| 149 | [Switch Profile Parent Permission](Screen_Prompts/149_Switch_Profile_Parent_Permission.md) | overlay | Contextual entry in source narrative | Shared C19 gate: 4 PIN boxes numeric keypad/backspace; always new gate child→parent no grace bypass; success→picker; failure/cancel→same child; repeated failure inherits lockout. OS biometric alternative per C19. |
## B17

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 150 | [Deep Link Resolver](Screen_Prompts/150_Deep_Link_Resolver.md) | state | Contextual entry in source narrative | OS push→resolve session/child/content/parent gate; offline→reconnect retry; required auth→shared gate/picker; unavailable→safe alternative/Home. Bedtime→A4; streak→A7; content→A3/A5/A6; reward→A11. No gate bypass or sibling disclosure. |
## B18

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 151 | [Islamic Fact Detail](Screen_Prompts/151_Islamic_Fact_Detail.md) | screen | Contextual entry in source narrative | Home fact/spaced repetition → Detail; approval information expands inline; eligible related story/surah/dua→owner detail; linked quiz → shared A8 parameterized fact quiz; stale linkage omitted; withdrawn fact friendly unavailable; offline cached content; unavailable undownloaded quiz needs internet; Home omits card if zero eligible facts. Only approved published versions. |
| 152 | [Islamic Facts Browse](Screen_Prompts/152_Islamic_Facts_Browse.md) | screen | Contextual entry in source narrative | Observed topic-filtered browse list→Fact Detail; back→entry. Existing mobile source addition beyond PRD primary Home card/detail flow; preserve only after source reconciliation. |
## C19

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 153 | [Parent Profile PIN/Biometric Gate](Screen_Prompts/153_Parent_Profile_PIN_Biometric_Gate.md) | screen | Who Is Learning "Parent Profile" tile, "Switch Profile" from Child Mode, any override-requiring action | Parent Dashboard / the specific override action |
| 154 | [Restriction Screen](Screen_Prompts/154_Restriction_Screen.md) | screen | Check Restrictions stage failure | Parent override gate, or blocked with explanation |
| 155 | [Calm Locked State (screen-time limit reached)](Screen_Prompts/155_Calm_Locked_State_screen_time_limit_reached.md) | screen | Screen-time budget exhausted mid-session | Parent override gate |
| 156 | [Bedtime Block Screen](Screen_Prompts/156_Bedtime_Block_Screen.md) | screen | Attempted session start during bedtime window | Parent override gate |
## C20

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 157 | [Parent Dashboard (landing)](Screen_Prompts/157_Parent_Dashboard_landing.md) | screen | C.19 gate success (Parent Profile or Switch Profile) | Child Management, Per-Child Reports, Screen Time/AI Controls, Subscription, Notifications/Support |
## C21

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 158 | [Child Management (List)](Screen_Prompts/158_Child_Management_List.md) | screen | Parent Dashboard module shortcut | Add/Edit Child, Per-Child Report, Child Locks & Sessions (C.23) |
| 159 | [Add Child (Parent Management)](Screen_Prompts/159_Add_Child_Parent_Management.md) | screen | Child Management Add Child / Who Is Learning Add Child after fresh Parent Gate | Child Management List (new child added) |
| 160 | [Edit Child (Parent Management)](Screen_Prompts/160_Edit_Child_Parent_Management.md) | screen | Child Management per-child Edit after fresh Parent Gate | Child Management List (selected child updated) |
| 161 | [Disable Confirmation (step-up gated)](Screen_Prompts/161_Disable_Confirmation_step_up_gated.md) | overlay | "Disable" action | Child Management List (now disabled) |
| 162 | [Re-Enable Confirmation (step-up gated)](Screen_Prompts/162_Re_Enable_Confirmation_step_up_gated.md) | overlay | "Enable" action | Child Management List, or capacity-blocked state |
| 163 | [Permanent Deletion — Step 2: Irreversible-Data Warning](Screen_Prompts/163_Permanent_Deletion_Step_2_Irreversible_Data_Warning.md) | screen | Step-Up Gate success | Confirm / Cancel |
| 164 | [Trial-Cancellation Forced-Selection Screen](Screen_Prompts/164_Trial_Cancellation_Forced_Selection_Screen.md) | screen | Plan downgrade event | Child Management List (others now disabled) |
## C22

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 165 | [Per-Child Report (full view)](Screen_Prompts/165_Per_Child_Report_full_view.md) | screen | Parent Dashboard, Child Management | AI Interaction History, Screen Time & Bedtime Settings (C.23), Skill Detail |
| 166 | [Skill Detail Drill-down](Screen_Prompts/166_Skill_Detail_Drill_down.md) | screen | Skill Mastery Grid | Back to Per-Child Report |
| 167 | [AI Interaction History (full screen)](Screen_Prompts/167_AI_Interaction_History_full_screen.md) | screen | Per-Child Report "AI interaction log" link | Concerning-interaction → AI Controls (C.23) |
| 168 | [Safety Report (on-demand, full screen)](Screen_Prompts/168_Safety_Report_on_demand_full_screen.md) | screen | Per-Child Report / Parent Dashboard | Back to Per-Child Report |
| 169 | [Monthly Family Report (cross-child, aggregate-only)](Screen_Prompts/169_Monthly_Family_Report_cross_child_aggregate_only.md) | screen | Parent Dashboard / Per-Child Report cross-link | Back |
| 170 | [AI Insight Report (premium)](Screen_Prompts/170_AI_Insight_Report_premium.md) | screen | Per-Child Report | Locked/Upsell state if non-premium (C.24) |
| 171 | [Achievement Share Card Preview (PII-free)](Screen_Prompts/171_Achievement_Share_Card_Preview_PII_free.md) | screen | Parent Gate success | OS Share Sheet |
| 172 | [Full Activity Timeline](Screen_Prompts/172_Full_Activity_Timeline.md) | screen | Parent Dashboard activity See All | Parent Dashboard / Per-Child Report |
## C23

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 173 | [Controls Landing (Screen Time / Quiet Hours / AI Permissions / Content Age Level entry list)](Screen_Prompts/173_Controls_Landing_Screen_Time_Quiet_Hours_AI_Permissions_Content_Age_Level_entry_list.md) | screen | Parent Dashboard module shortcut grid | Each sub-control screen |
| 174 | [Screen Time Settings (per child)](Screen_Prompts/174_Screen_Time_Settings_per_child.md) | screen | Controls Landing | Saves, returns to Controls Landing |
| 175 | [Quiet Hours / Bedtime Settings (per child)](Screen_Prompts/175_Quiet_Hours_Bedtime_Settings_per_child.md) | screen | Controls Landing | Saves, returns to Controls Landing |
| 176 | [AI Permissions Settings (per child)](Screen_Prompts/176_AI_Permissions_Settings_per_child.md) | screen | Controls Landing | Saves, returns to Controls Landing |
| 177 | [Content Age Level Settings (per child)](Screen_Prompts/177_Content_Age_Level_Settings_per_child.md) | screen | Controls Landing | Saves, returns to Controls Landing |
| 178 | [Child Locks & Sessions (per child)](Screen_Prompts/178_Child_Locks_Sessions_per_child.md) | screen | Child Management List, Controls Landing | Set Lock sub-screen, Device Revocation |
| 179 | [Set Lock Type (Pattern/PIN/Biometric/None)](Screen_Prompts/179_Set_Lock_Type_Pattern_PIN_Biometric_None.md) | screen | Child Locks & Sessions | Child Locks & Sessions (saved) |
| 180 | [Device Revocation Confirmation](Screen_Prompts/180_Device_Revocation_Confirmation.md) | overlay | Active Device List "Revoke" | Active Device List (device removed) |
| 181 | [Content Age Level — Override Confirmation](Screen_Prompts/181_Content_Age_Level_Override_Confirmation.md) | overlay | Content Age Level Settings, save action | Content Age Level Settings (saved) |
## C24

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 182 | [Subscription & Billing (landing)](Screen_Prompts/182_Subscription_Billing_landing.md) | screen | Parent Dashboard module shortcut, paywall upsell, Settings | Plan Comparison, Invoice History, Cancel Flow, Google Play billing sheet (external) |
| 183 | [Plan Comparison](Screen_Prompts/183_Plan_Comparison.md) | screen | Subscription landing | Trial Disclosure / Direct Upgrade Disclosure |
| 184 | [Trial Disclosure Screen (length, price, renewal date, auto-renew)](Screen_Prompts/184_Trial_Disclosure_Screen_length_price_renewal_date_auto_renew.md) | screen | Plan Comparison "Start Trial" | Platform Purchase Flow (external) |
| 185 | [Direct Upgrade Disclosure Screen](Screen_Prompts/185_Direct_Upgrade_Disclosure_Screen.md) | screen | Plan Comparison "Upgrade" | Platform Purchase Flow (external) |
| 186 | [Invoice History](Screen_Prompts/186_Invoice_History.md) | screen | Subscription landing | Invoice Detail |
| 187 | [Invoice Detail](Screen_Prompts/187_Invoice_Detail.md) | screen | Invoice History | Back |
| 188 | [Cancel Flow — Confirmation](Screen_Prompts/188_Cancel_Flow_Confirmation.md) | screen | Subscription landing "Cancel" | Subscription landing (status updated to Canceled, access continues) |
| 189 | [Retry Failed Payment](Screen_Prompts/189_Retry_Failed_Payment.md) | screen | PastDue state notification/banner | Platform Purchase Flow (external) |
| 190 | [Free-Plan Second-Child Upgrade Prompt (parent-mode only)](Screen_Prompts/190_Free_Plan_Second_Child_Upgrade_Prompt_parent_mode_only.md) | overlay | Add Child attempt beyond Free-plan capacity | Subscription landing |
## C25

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 191 | [Notifications (Parent) Inbox](Screen_Prompts/191_Notifications_Parent_Inbox.md) | screen | Parent Dashboard bell icon, push notification tap | Related deep-linked screen, Notification Preferences |
| 192 | [Notification Preferences — Category Toggles](Screen_Prompts/192_Notification_Preferences_Category_Toggles.md) | screen | Notifications Inbox, Settings | Saves, returns |
| 193 | [Notification Preferences — Quiet Hours](Screen_Prompts/193_Notification_Preferences_Quiet_Hours.md) | screen | Notification Preferences | Saves, returns |
| 194 | [Support Center (landing)](Screen_Prompts/194_Support_Center_landing.md) | screen | Parent Dashboard, Settings, Privacy & Support | FAQ Search, Contact Support Form, Ticket History |
| 195 | [FAQ Search](Screen_Prompts/195_FAQ_Search.md) | screen | Support Center | FAQ Article Detail, "Contact Support" fallback |
| 196 | [FAQ Article Detail](Screen_Prompts/196_FAQ_Article_Detail.md) | screen | FAQ Search results | Back, "Was this helpful?" → Contact Support if not |
| 197 | [Contact Support Form](Screen_Prompts/197_Contact_Support_Form.md) | screen | Support Center, FAQ fallback | Ticket Submitted Confirmation |
| 198 | [Ticket Submitted Confirmation](Screen_Prompts/198_Ticket_Submitted_Confirmation.md) | screen | Contact Support Form submit | Ticket History |
| 199 | [Ticket History List](Screen_Prompts/199_Ticket_History_List.md) | screen | Support Center | Ticket Detail |
| 200 | [Ticket Detail / Status View](Screen_Prompts/200_Ticket_Detail_Status_View.md) | screen | Ticket History | Back, add a follow-up message |
## C26

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 201 | [Settings (landing)](Screen_Prompts/201_Settings_landing.md) | screen | Parent Dashboard | Security, Consent Log, AI Interaction History, Language, Privacy & Support |
| 202 | [Privacy & Support (landing, may be a sub-section of Settings)](Screen_Prompts/202_Privacy_Support_landing_may_be_a_sub_section_of_Settings.md) | screen | Settings, Parent Dashboard | Consent Log, AI Interaction History, Data Export, Account Deletion entry |
| 203 | [Parent PIN Reset (Account Security)](Screen_Prompts/203_Parent_PIN_Reset_Account_Security.md) | screen | Settings/Security Reset PIN → OTP account reverification through A1; sensitive reset uses shared fresh C19 gate where current PIN available | Security/Settings after new PIN confirmation; cancel → Security |
| 204 | [Security — Device List](Screen_Prompts/204_Security_Device_List.md) | screen | Settings → Security | Device Revocation Confirmation |
| 205 | [Device Revocation Confirmation](Screen_Prompts/205_Device_Revocation_Confirmation.md) | overlay | Device List | Device List (device removed) |
| 206 | [Consent Log](Screen_Prompts/206_Consent_Log.md) | screen | Privacy & Support | Consent Detail / Withdraw Confirmation |
| 207 | [Consent Detail (full text + status)](Screen_Prompts/207_Consent_Detail_full_text_status.md) | screen | Consent Log | Withdraw Confirmation (if optional) |
| 208 | [Withdraw Optional Consent — Confirmation](Screen_Prompts/208_Withdraw_Optional_Consent_Confirmation.md) | overlay | Consent Detail | Consent Log (updated) |
| 209 | [AI Interaction History](Screen_Prompts/209_AI_Interaction_History.md) | screen | Privacy & Support, Per-Child Report (C.22) cross-link | AI Interaction Detail |
| 210 | [AI Interaction Detail (redacted)](Screen_Prompts/210_AI_Interaction_Detail_redacted.md) | screen | AI Interaction History | Back |
| 211 | [Language Picker](Screen_Prompts/211_Language_Picker.md) | screen | Settings | Settings (applied immediately) |
| 212 | [Data Export Request](Screen_Prompts/212_Data_Export_Request.md) | screen | Privacy & Support | Export Status Tracking |
| 213 | [Export Status Tracking (preparing/ready)](Screen_Prompts/213_Export_Status_Tracking_preparing_ready.md) | screen | Data Export Request | Download/view export, or continues polling |
| 214 | [Logout Confirmation (unsynced downloads present)](Screen_Prompts/214_Logout_Confirmation_unsynced_downloads_present.md) | overlay | Settings "Logout" | Logged out, or canceled |
| 215 | [Security (PIN and Device Management landing)](Screen_Prompts/215_Security_PIN_and_Device_Management_landing.md) | screen | Conditional approved Settings Security destination only | Parent PIN Reset / Device List / return Settings |
| 216 | [Account Deletion Request and Confirmation](Screen_Prompts/216_Account_Deletion_Request_and_Confirmation.md) | screen | Privacy & Support → Delete Account | Pending deletion status or invoking Privacy |
| 217 | [Pending Account Deletion and Cancellation](Screen_Prompts/217_Pending_Account_Deletion_and_Cancellation.md) | screen | Confirmed deletion request / returning authenticated family | Privacy & Support or signed-out completion |
## F36

| Review # | Surface | Type | Entry / branch | Exit / result |
|---|---|---|---|---|
| 218 | [Ramadan Prep / Countdown](Screen_Prompts/218_Ramadan_Prep_Countdown.md) | screen | Contextual entry in source narrative | 14 days before server region-adjusted start; parent prep action→gated parent Ramadan Settings/checklist; countdown values dynamic; child must not configure family settings. |
| 219 | [Ramadan Home](Screen_Prompts/219_Ramadan_Home.md) | screen | Contextual entry in source narrative | A2 Home seasonal variant: journey→Map; tonight→Mission; dua→A6; rewards→A11; Family requires gate→parent Ramadan Dashboard. |
| 220 | [Ramadan Journey Map](Screen_Prompts/220_Ramadan_Journey_Map.md) | screen | Contextual entry in source narrative | 30 lantern nodes; tonight/missed→Mission; complete→Recap; Qadr nights21/23/25/27/29→Reflection; future unavailable; new join prior nights not applicable, missed still completable. |
| 221 | [Night Recap](Screen_Prompts/221_Night_Recap.md) | screen | Contextual entry in source narrative | Completed mission→Recap→Map; actual reward value owner A11; Qadr recap suppress gamification. |
| 222 | [Ramadan Mission Detail](Screen_Prompts/222_Ramadan_Mission_Detail.md) | screen | Contextual entry in source narrative | Story→seasonal Player using A3/A4; dua→A6; fasting only parent-enabled allowed approach→Log; back→Map; task completion feeds existing reward engine, no parallel XP. |
| 223 | [Ramadan Story Player](Screen_Prompts/223_Ramadan_Story_Player.md) | screen | Contextual entry in source narrative | Shared A3/A4 player with seasonal context; playback controls preserve owner behavior; completion returns Mission and persists progress; interruption restores furthest valid position. |
| 224 | [Fasting Tracker](Screen_Prompts/224_Fasting_Tracker.md) | screen | Contextual entry in source narrative | Child log only permitted parent approach; practice partial log, full fast allowed full log, education-only no log; changes preserve prior nights; parent radio controls belong Settings not child. |
| 225 | [Laylatul Qadr Reflection](Screen_Prompts/225_Laylatul_Qadr_Reflection.md) | screen | Contextual entry in source narrative | Qadr nights21/23/25/27/29 calm reflection→calm Recap; approved content only; suppress competitive badges/leaderboard/reward call-outs; normal rewards internal no distracting UI. |
| 226 | [Eid Countdown](Screen_Prompts/226_Eid_Countdown.md) | screen | Contextual entry in source narrative | Last2days region-adjusted→Eid preview; server override next-open resync, one-time notification; no hardcoded device-locale calendar. |
| 227 | [Eid Home](Screen_Prompts/227_Eid_Home.md) | screen | Contextual entry in source narrative | Eid3days seasonal Home; reward→Reveal; card→Generator; certificate→Certificate; family report/share→Parent Gate then parent/report/share owner. |
| 228 | [Eid Reward Reveal](Screen_Prompts/228_Eid_Reward_Reveal.md) | screen | Contextual entry in source narrative | Tap reveals existing season-scoped badge/reward once; proceed Card/Home; no generated rewards or duplicate ledger posts. |
| 229 | [Eid Card Generator](Screen_Prompts/229_Eid_Card_Generator.md) | screen | Contextual entry in source narrative | Design→message→parent gate generation/sharing; no child name/DOB/location in artifact; cancel returns editor; share OS simulation only in Figma. |
| 230 | [Ramadan Complete Certificate](Screen_Prompts/230_Ramadan_Complete_Certificate.md) | screen | Contextual entry in source narrative | Eid Home/Map→certificate; generation/share/print parent-gated per FR6; PII excluded; only true completion claims and campaign dates. |
| 231 | [Post-Eid Keep the Habit](Screen_Prompts/231_Post_Eid_Keep_the_Habit.md) | screen | Contextual entry in source narrative | 14day tail→A7 Habit Builder; optional selections; no guilt pressure; gratitude journaling needs existing A7 requirement, not new product. |
| 232 | [Parent Ramadan Settings](Screen_Prompts/232_Parent_Ramadan_Settings.md) | screen | Contextual entry in source narrative | Gated parent Family Overview→per-child approach full/practice/education and separate visibility toggle/reminders/invite; future nights only; hidden for young by default; failed save keeps saved state. |
| 233 | [Parent Ramadan Dashboard](Screen_Prompts/233_Parent_Ramadan_Dashboard.md) | screen | Contextual entry in source narrative | Conditional tab within C20 only active window; family→Aggregate; report→Report; own child detail individually via C22, no comparisons. |
| 234 | [Family Ramadan Aggregate](Screen_Prompts/234_Family_Ramadan_Aggregate.md) | screen | Contextual entry in source narrative | Parent dashboard→aggregate-only totals; child detail separate authorized entry, never per-child array/comparative bars in aggregate. |
| 235 | [Family Ramadan Report](Screen_Prompts/235_Family_Ramadan_Report.md) | screen | Contextual entry in source narrative | Dashboard/post-Eid→printable aggregate-only report; print/share parent gate; invite→read-only link; no sibling comparison or identifying child breakdown exported. |
| 236 | [Conversion Moment Card](Screen_Prompts/236_Conversion_Moment_Card.md) | component | Contextual entry in source narrative | Embedded dismissible component only day28–30 AND active trial; terms before seasonal persuasion; CTA→C24 existing gated purchase; absent lapsed/converted; never blocking modal. |
| 237 | [Family Member Invite](Screen_Prompts/237_Family_Member_Invite.md) | screen | Contextual entry in source narrative | Parent Settings/Report→generate own-family read-only link; copy/share with parent gate; recipient without app graceful install/account prompt; expiry/auth access contract unverified. |

## Shared surfaces and contextual aliases

These are mapped to an owning prompt, preserving caller context and return path rather than generating conflicting duplicate screens.

| Source context | Owner prompt |
|---|---|
| A3 / Favorites List | [143](Screen_Prompts/143_Favorites.md) |
| A3 / Downloads Manager (Stories scope) | [144](Screen_Prompts/144_Downloads.md) |
| A5 / Daily Quiz (Learn-tab instance) | [102](Screen_Prompts/102_Quiz_Question_Screen_Multiple_Choice.md) |
| A5 / Quiz Per-Answer Explanation Overlay | [107](Screen_Prompts/107_Per_Answer_Explanation_Overlay.md) |
| A5 / Quiz Retry Set (mistakes) | [108](Screen_Prompts/108_Retry_Set_Entry_Screen.md) |
| A5 / Quiz Results / Effort XP Reveal | [110](Screen_Prompts/110_Quiz_Completion_Result_Screen_shared_generic.md) |
| A5 / Islamic Fact Detail (Learn-tab linked) | [151](Screen_Prompts/151_Islamic_Fact_Detail.md) |
| A6 / Favorites List (Dua-filtered view, shared component with A.3) | [143](Screen_Prompts/143_Favorites.md) |
| A6 / Search Results (Dua-scoped) | [140](Screen_Prompts/140_Search_Results.md) |
| A6 / Downloads Manager (Dua scope, shared with A.16) | [144](Screen_Prompts/144_Downloads.md) |
| A7 / Fasting Tracker (Ramadan/practice) | [224](Screen_Prompts/224_Fasting_Tracker.md) |
| A8 / Hint Overlay (cross-cutting, shared with A.5) | [079](Screen_Prompts/079_Hint_Overlay_progressive_hint.md) |
| B17 / In-App Notification Banner | [034](Screen_Prompts/034_Child_Home_composite_screen.md) |
| C19 / Who Is Learning (Profile Picker) | [022](Screen_Prompts/022_Profile_Picker_Who_Is_Learning.md) |
| C19 / Profile Lock Verification (Pattern/PIN/Fingerprint) | [023](Screen_Prompts/023_Child_Lock_Screen_PIN_Pattern_Biometric.md) |
| C23 / Calm Rest Screen (limit reached) | [155](Screen_Prompts/155_Calm_Locked_State_screen_time_limit_reached.md) |
| C23 / Bedtime Block Screen (new session attempt during bedtime) | [156](Screen_Prompts/156_Bedtime_Block_Screen.md) |
