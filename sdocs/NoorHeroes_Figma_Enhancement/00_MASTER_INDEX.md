# NoorHeroes — Figma enhancement documentation

**Current phase: controlled V2 design execution. Finalized Splash, Language and Intro work is tracked in the current handoff. Historical research below remains source documentation.** Prepared 13 October 2026, Asia/Kolkata. All generated files are isolated under `sdocs/NoorHeroes_Figma_Enhancement/`.

The package contains **237 independently reviewable prompts** (screens, owned overlays, and explicitly labeled state surfaces). Numbering is review order; conditional user navigation follows the source flows. Prompts with missing copy, conflicting requirements or proposed surfaces are blocked until the relevant decision is approved.

## Review documents

- [Screen 007 — implemented Login review](Evidence/007_Login_Execution_Review.md)
- [01 SOURCE AUDIT AND ACCESSIBILITY](01_SOURCE_AUDIT_AND_ACCESSIBILITY.md)
- [02 SCREEN INVENTORY AND ORDER](02_SCREEN_INVENTORY_AND_ORDER.md)
- [03 REQUIREMENT TRACEABILITY MATRIX](03_REQUIREMENT_TRACEABILITY_MATRIX.md)
- [04 EXISTING VS ENHANCED DESIGN AUDIT](04_EXISTING_VS_ENHANCED_DESIGN_AUDIT.md)
- [05 DESIGN SYSTEM AND COMPONENT GUIDELINES](05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md)
- [06 GLOBAL NAVIGATION AND PROTOTYPE ARCHITECTURE](06_GLOBAL_NAVIGATION_AND_PROTOTYPE_ARCHITECTURE.md)
- [07 MOTION AND ANIMATION GUIDELINES](07_MOTION_AND_ANIMATION_GUIDELINES.md)
- [08 ACCESSIBILITY RESPONSIVENESS AND EDGE CASES](08_ACCESSIBILITY_RESPONSIVENESS_AND_EDGE_CASES.md)
- [09 OPEN QUESTIONS AND APPROVALS](09_OPEN_QUESTIONS_AND_APPROVALS.md)
- [10 REQUIREMENT COVERAGE REGISTER](10_REQUIREMENT_COVERAGE_REGISTER.md)
- [11 CURRENT CONTROL RECONCILIATION](11_CURRENT_CONTROL_RECONCILIATION.md)
- [99 FINAL VALIDATION CHECKLIST](99_FINAL_VALIDATION_CHECKLIST.md)

## Evidence and source research

- [Figma exact-copy and structural extraction](Evidence/figma-screens.json)
- [Current mobile catalogue / exact DOM copy](Evidence/current-site-screens.json)
- [Ramadan20 mobile exact-copy previews](Evidence/current-site-ramadan.json)
- [Source manifest](Evidence/source-manifest.json)
- [Onboarding requirements records](Research/onboarding-enriched.json)
- [Child learning audit](Research/child-learning.md)
- [Supporting/seasonal audit](Research/supporting.md)
- [Parent audit](Research/parent.md)

## Screen-by-screen execution sequence

Review source/decision documents first; approve global tokens/working area; resolve each screen’s blocking copy/flow conflicts; then execute exactly one prompt, compare references and evidence, correct, and approve before the next. Start with Splash after its references and shared gates are settled. Branch screens are reviewed in their listed group; prototype routes depend on actual user state, not numeric successor.


### A1

- 001. [Splash Screen](Screen_Prompts/001_Splash_Screen.md) — screen
- 002. [Language Selection](Screen_Prompts/002_Language_Selection.md) — screen
- 003. [Intro Slide 1 (Stories)](Screen_Prompts/003_Intro_Slide_1_Stories.md) — screen
- 004. [Intro Slide 2 (Quran/Arabic/Tajweed)](Screen_Prompts/004_Intro_Slide_2_Quran_Arabic_Tajweed.md) — screen
- 005. [Intro Slide 3 (Habits & Rewards)](Screen_Prompts/005_Intro_Slide_3_Habits_Rewards.md) — screen
- 006. [Intro Slide 4 (Parent Control)](Screen_Prompts/006_Intro_Slide_4_Parent_Control.md) — screen
- 007. [Login (phone/email + Google)](Screen_Prompts/007_Login_phone_email_Google.md) — screen
- 008. [Registration + Consent](Screen_Prompts/008_Registration_Consent.md) — screen
- 009. [Consent Detail / Full Text Modal](Screen_Prompts/009_Consent_Detail_Full_Text_Modal.md) — overlay
- 010. [OTP Verification](Screen_Prompts/010_OTP_Verification.md) — screen
- 011. [OTP Fallback Channel Offer](Screen_Prompts/011_OTP_Fallback_Channel_Offer.md) — overlay
- 012. [Parent PIN Setup](Screen_Prompts/012_Parent_PIN_Setup.md) — screen
- 013. [Biometric Enrollment Prompt](Screen_Prompts/013_Biometric_Enrollment_Prompt.md) — overlay
- 014. [Add Child](Screen_Prompts/014_Add_Child.md) — screen
- 015. [Avatar Selection](Screen_Prompts/015_Avatar_Selection.md) — overlay
- 016. [Interest Selection](Screen_Prompts/016_Interest_Selection.md) — overlay
- 017. [Learning Level Setup](Screen_Prompts/017_Learning_Level_Setup.md) — overlay
- 018. ["Add Another Child?" Prompt](Screen_Prompts/018_Add_Another_Child_Prompt.md) — overlay
- 019. [Learning Level + Interests Confirmation (family-level summary)](Screen_Prompts/019_Learning_Level_Interests_Confirmation_family_level_summary.md) — screen
- 020. [Screen Time & Notification Primer](Screen_Prompts/020_Screen_Time_Notification_Primer.md) — screen
- 021. [Personalized Path Reveal](Screen_Prompts/021_Personalized_Path_Reveal.md) — screen
- 022. [Profile Picker ("Who Is Learning")](Screen_Prompts/022_Profile_Picker_Who_Is_Learning.md) — screen
- 023. [Child Lock Screen (PIN/Pattern/Biometric)](Screen_Prompts/023_Child_Lock_Screen_PIN_Pattern_Biometric.md) — screen
- 024. [Lock Recovery (via verified Parent Profile)](Screen_Prompts/024_Lock_Recovery_via_verified_Parent_Profile.md) — screen
- 025. [First Mission Screen](Screen_Prompts/025_First_Mission_Screen.md) — screen
- 026. [Forced Update Blocking Screen](Screen_Prompts/026_Forced_Update_Blocking_Screen.md) — screen
- 027. [Recommended Update Banner/Dismissible](Screen_Prompts/027_Recommended_Update_Banner_Dismissible.md) — overlay
- 028. [Maintenance Mode Screen](Screen_Prompts/028_Maintenance_Mode_Screen.md) — screen
- 029. [No Connectivity Screen (pre-auth)](Screen_Prompts/029_No_Connectivity_Screen_pre_auth.md) — screen
- 030. [Forgot Access / Account Recovery Entry](Screen_Prompts/030_Forgot_Access_Account_Recovery_Entry.md) — screen
- 031. [Terms of Service (full document)](Screen_Prompts/031_Terms_of_Service_full_document.md) — screen
- 032. [Privacy Policy (full document)](Screen_Prompts/032_Privacy_Policy_full_document.md) — screen
- 033. [Child-Data Processing Consent (full document)](Screen_Prompts/033_Child_Data_Processing_Consent_full_document.md) — screen

### A2

- 034. [Child Home (composite screen)](Screen_Prompts/034_Child_Home_composite_screen.md) — screen
- 035. [Full-Screen Retry (no cache, no network)](Screen_Prompts/035_Full_Screen_Retry_no_cache_no_network.md) — screen

### A3

- 036. [Stories Library (Landing)](Screen_Prompts/036_Stories_Library_Landing.md) — screen
- 037. [Category Filter Panel](Screen_Prompts/037_Category_Filter_Panel.md) — overlay
- 038. [Story Detail](Screen_Prompts/038_Story_Detail.md) — screen
- 039. [Story Player — Video](Screen_Prompts/039_Story_Player_Video.md) — screen
- 040. [Story Player — Audio](Screen_Prompts/040_Story_Player_Audio.md) — screen
- 041. [Story Player — Text](Screen_Prompts/041_Story_Player_Text.md) — screen
- 042. [Interactive Choice Overlay](Screen_Prompts/042_Interactive_Choice_Overlay.md) — overlay
- 043. [Pause-and-Quiz Moment Overlay](Screen_Prompts/043_Pause_and_Quiz_Moment_Overlay.md) — overlay
- 044. [Media Unavailable / Safe-Stop Screen](Screen_Prompts/044_Media_Unavailable_Safe_Stop_Screen.md) — screen
- 045. [Completion / Reward Reveal Screen](Screen_Prompts/045_Completion_Reward_Reveal_Screen.md) — screen
- 046. [Moral Summary Card ("Noor says...")](Screen_Prompts/046_Moral_Summary_Card_Noor_says.md) — screen
- 047. [Post-Story Quiz](Screen_Prompts/047_Post_Story_Quiz.md) — screen
- 048. [Achievement/Badge Unlock Modal](Screen_Prompts/048_Achievement_Badge_Unlock_Modal.md) — overlay
- 049. [Approved Share Card Preview](Screen_Prompts/049_Approved_Share_Card_Preview.md) — screen
- 050. [Caption/Audio-Track/Quality Settings Sheet](Screen_Prompts/050_Caption_Audio_Track_Quality_Settings_Sheet.md) — overlay

### A4

- 051. [Audio Bedtime Player (main screen)](Screen_Prompts/051_Audio_Bedtime_Player_main_screen.md) — screen
- 052. [Episode List Sheet (for multi-part audio series)](Screen_Prompts/052_Episode_List_Sheet_for_multi_part_audio_series.md) — overlay
- 053. [Sleep Timer Selector](Screen_Prompts/053_Sleep_Timer_Selector.md) — overlay
- 054. [Playback Speed Selector](Screen_Prompts/054_Playback_Speed_Selector.md) — overlay
- 055. [Goodnight Idle State](Screen_Prompts/055_Goodnight_Idle_State.md) — screen
- 056. [Dua / Calm-Reflection Ending Card](Screen_Prompts/056_Dua_Calm_Reflection_Ending_Card.md) — screen
- 057. [Media Unavailable / Safe-Stop (Bedtime-styled variant)](Screen_Prompts/057_Media_Unavailable_Safe_Stop_Bedtime_styled_variant.md) — screen

### A5

- 058. [Learn Tab Landing / Quran Learning Home (Skill Tree Map)](Screen_Prompts/058_Learn_Tab_Landing_Quran_Learning_Home_Skill_Tree_Map.md) — screen
- 059. [Placement Check (first-time)](Screen_Prompts/059_Placement_Check_first_time.md) — screen
- 060. [Mode Selector Sheet](Screen_Prompts/060_Mode_Selector_Sheet.md) — overlay
- 061. [Surah Learning](Screen_Prompts/061_Surah_Learning.md) — screen
- 062. [Recitation Recorder Overlay](Screen_Prompts/062_Recitation_Recorder_Overlay.md) — overlay
- 063. [AI Pronunciation Feedback Screen](Screen_Prompts/063_AI_Pronunciation_Feedback_Screen.md) — screen
- 064. [Listen-Only Self-Assessment Screen](Screen_Prompts/064_Listen_Only_Self_Assessment_Screen.md) — screen
- 065. [Arabic Letters — Hear & Match](Screen_Prompts/065_Arabic_Letters_Hear_Match.md) — screen
- 066. [Arabic Letters — Tracing](Screen_Prompts/066_Arabic_Letters_Tracing.md) — screen
- 067. [Arabic Letters — Word Context](Screen_Prompts/067_Arabic_Letters_Word_Context.md) — screen
- 068. [Arabic Letters — Word-Building (sound tiles)](Screen_Prompts/068_Arabic_Letters_Word_Building_sound_tiles.md) — screen
- 069. [Tajweed — Rule Introduction](Screen_Prompts/069_Tajweed_Rule_Introduction.md) — screen
- 070. [Tajweed — Listen (normal/slow)](Screen_Prompts/070_Tajweed_Listen_normal_slow.md) — screen
- 071. [Tajweed — Rule Identification Exercise](Screen_Prompts/071_Tajweed_Rule_Identification_Exercise.md) — screen
- 072. [Tajweed — Assessment](Screen_Prompts/072_Tajweed_Assessment.md) — screen
- 073. [Quran Game — Ayah Ordering](Screen_Prompts/073_Quran_Game_Ayah_Ordering.md) — screen
- 074. [Quran Game — Listen & Select Matching Ayah](Screen_Prompts/074_Quran_Game_Listen_Select_Matching_Ayah.md) — screen
- 075. [Quran Game — Missing Word](Screen_Prompts/075_Quran_Game_Missing_Word.md) — screen
- 076. [Quran Game — Surah Theme Matching](Screen_Prompts/076_Quran_Game_Surah_Theme_Matching.md) — screen
- 077. [Quran Game — Recitation Echo](Screen_Prompts/077_Quran_Game_Recitation_Echo.md) — screen
- 078. [Quran Game — Progressive Memorization Reveal](Screen_Prompts/078_Quran_Game_Progressive_Memorization_Reveal.md) — screen
- 079. [Hint Overlay (progressive hint)](Screen_Prompts/079_Hint_Overlay_progressive_hint.md) — overlay
- 080. [Mastery Badge/Node-Unlock Celebration](Screen_Prompts/080_Mastery_Badge_Node_Unlock_Celebration.md) — overlay
- 081. [Microphone Permission Rationale / One-Time Explainer](Screen_Prompts/081_Microphone_Permission_Rationale_One_Time_Explainer.md) — overlay
- 082. [Arabic Letters — Contextual Form Matching (Isolated / Initial / Medial / Final)](Screen_Prompts/082_Arabic_Letters_Contextual_Form_Matching_Isolated_Initial_Medial_Final.md) — state
- 083. [Arabic Letters — Harakah Sound Pairing](Screen_Prompts/083_Arabic_Letters_Harakah_Sound_Pairing.md) — state

### A6

- 084. [Dua Learning Landing (Category List)](Screen_Prompts/084_Dua_Learning_Landing_Category_List.md) — screen
- 085. [Category Dua List](Screen_Prompts/085_Category_Dua_List.md) — screen
- 086. [Dua Card Detail (Arabic/Transliteration/Translation/Audio)](Screen_Prompts/086_Dua_Card_Detail_Arabic_Transliteration_Translation_Audio.md) — screen
- 087. [Recall Quiz Question Screen](Screen_Prompts/087_Recall_Quiz_Question_Screen.md) — screen
- 088. [Recall Quiz Result / Pass Screen](Screen_Prompts/088_Recall_Quiz_Result_Pass_Screen.md) — screen
- 089. [Dua Master Badge Progress Celebration (milestone)](Screen_Prompts/089_Dua_Master_Badge_Progress_Celebration_milestone.md) — overlay
- 090. [Habit Tracker Reminder Suggestion Prompt](Screen_Prompts/090_Habit_Tracker_Reminder_Suggestion_Prompt.md) — overlay

### A7

- 091. [Habit Builder — Today's Checklist](Screen_Prompts/091_Habit_Builder_Today_s_Checklist.md) — screen
- 092. [Dhikr Counter Screen](Screen_Prompts/092_Dhikr_Counter_Screen.md) — screen
- 093. [Good Deed Logging — Category Selector](Screen_Prompts/093_Good_Deed_Logging_Category_Selector.md) — overlay
- 094. [Good Deed Optional Note Entry](Screen_Prompts/094_Good_Deed_Optional_Note_Entry.md) — screen
- 095. [Streak Calendar / History View](Screen_Prompts/095_Streak_Calendar_History_View.md) — screen
- 096. [Recovery Mission Screen](Screen_Prompts/096_Recovery_Mission_Screen.md) — screen
- 097. [Streak State Detail — AtRisk / Protected / Broken / Recovery](Screen_Prompts/097_Streak_State_Detail_AtRisk_Protected_Broken_Recovery.md) — overlay
- 098. [Mercy-Toned Smaller-Target Suggestion Prompt](Screen_Prompts/098_Mercy_Toned_Smaller_Target_Suggestion_Prompt.md) — overlay
- 099. [Noor Garden — Personal View](Screen_Prompts/099_Noor_Garden_Personal_View.md) — screen
- 100. [Noor Garden — Family View](Screen_Prompts/100_Noor_Garden_Family_View.md) — screen
- 101. [Family Streak Milestone Celebration](Screen_Prompts/101_Family_Streak_Milestone_Celebration.md) — overlay

### A8

- 102. [Quiz Question Screen — Multiple Choice](Screen_Prompts/102_Quiz_Question_Screen_Multiple_Choice.md) — screen
- 103. [Quiz Question Screen — Sequence/Ordering](Screen_Prompts/103_Quiz_Question_Screen_Sequence_Ordering.md) — screen
- 104. [Quiz Question Screen — True/False](Screen_Prompts/104_Quiz_Question_Screen_True_False.md) — screen
- 105. [Quiz Question Screen — Image Match](Screen_Prompts/105_Quiz_Question_Screen_Image_Match.md) — screen
- 106. [Quiz Question Screen — Audio Match](Screen_Prompts/106_Quiz_Question_Screen_Audio_Match.md) — screen
- 107. [Per-Answer Explanation Overlay](Screen_Prompts/107_Per_Answer_Explanation_Overlay.md) — overlay
- 108. [Retry Set Entry Screen](Screen_Prompts/108_Retry_Set_Entry_Screen.md) — screen
- 109. [Quiz Completion / Effort XP Reveal](Screen_Prompts/109_Quiz_Completion_Effort_XP_Reveal.md) — screen

### A9

- 110. [Quiz Completion Result Screen (shared, generic)](Screen_Prompts/110_Quiz_Completion_Result_Screen_shared_generic.md) — screen
- 111. [Review Mistakes Screen](Screen_Prompts/111_Review_Mistakes_Screen.md) — screen
- 112. [Offline Completion — Saved / Results Deferred](Screen_Prompts/112_Offline_Completion_Saved_Results_Deferred.md) — screen

### A10

- 113. [Games Hub (tile grid landing)](Screen_Prompts/113_Games_Hub_tile_grid_landing.md) — screen
- 114. [Game-Specific Play Screen (per game, mechanics detailed in A.5 for Quran/Arabic games; new mini-games follow the same wrapper)](Screen_Prompts/114_Game_Specific_Play_Screen_per_game_mechanics_detailed_in_A_5_for_Quran_Arabic_games_new_mini_games_follow_the_same_wrapper.md) — screen
- 115. [Session Completion Screen (generic wrapper, reuses A.9's "strengths + next step" framing where applicable)](Screen_Prompts/115_Session_Completion_Screen_generic_wrapper_reuses_A_9_s_strengths_next_step_framing_where_applicable.md) — screen

### A11

- 116. [Rewards Hub / Wallet (landing)](Screen_Prompts/116_Rewards_Hub_Wallet_landing.md) — screen
- 117. [Transaction Detail (single ledger entry)](Screen_Prompts/117_Transaction_Detail_single_ledger_entry.md) — screen
- 118. [Achievements Screen (badge grid + cumulative level progress)](Screen_Prompts/118_Achievements_Screen_badge_grid_cumulative_level_progress.md) — screen
- 119. [Badge Detail / Criteria View](Screen_Prompts/119_Badge_Detail_Criteria_View.md) — screen
- 120. [Achievement Level Detail](Screen_Prompts/120_Achievement_Level_Detail.md) — screen
- 121. [Shareable Achievement Card Preview](Screen_Prompts/121_Shareable_Achievement_Card_Preview.md) — screen
- 122. [Weekly Challenge Detail](Screen_Prompts/122_Weekly_Challenge_Detail.md) — screen
- 123. [Seasonal Event Screen](Screen_Prompts/123_Seasonal_Event_Screen.md) — screen
- 124. [Archived Challenge View](Screen_Prompts/124_Archived_Challenge_View.md) — screen
- 125. [Achievement Store (catalog browse)](Screen_Prompts/125_Achievement_Store_catalog_browse.md) — screen
- 126. [Achievement Store — Item Detail](Screen_Prompts/126_Achievement_Store_Item_Detail.md) — screen
- 127. [Purchase Confirmation / Insufficient-Points Shortfall Screen](Screen_Prompts/127_Purchase_Confirmation_Insufficient_Points_Shortfall_Screen.md) — screen
- 128. [Family Board (private, multi-child families)](Screen_Prompts/128_Family_Board_private_multi_child_families.md) — screen
- 129. [Family Goal Detail](Screen_Prompts/129_Family_Goal_Detail.md) — screen
- 130. [Family Achievement Unlock Celebration](Screen_Prompts/130_Family_Achievement_Unlock_Celebration.md) — overlay
- 131. [Badge Unlock Modal](Screen_Prompts/131_Badge_Unlock_Modal.md) — overlay

### A12

- 132. [Avatar Screen (3D preview + owned grid + locked teasers)](Screen_Prompts/132_Avatar_Screen_3D_preview_owned_grid_locked_teasers.md) — screen
- 133. [Item Detail (owned) — Equip/Unequip](Screen_Prompts/133_Item_Detail_owned_Equip_Unequip.md) — overlay
- 134. [Locked Item Detail — Unlock Criteria View](Screen_Prompts/134_Locked_Item_Detail_Unlock_Criteria_View.md) — overlay
- 135. [Character Evolution Milestone Reveal](Screen_Prompts/135_Character_Evolution_Milestone_Reveal.md) — overlay

### B13

- 136. [Search](Screen_Prompts/136_Search.md) — screen
- 137. [Voice Search — Listening](Screen_Prompts/137_Voice_Search_Listening.md) — state
- 138. [Voice Search — Processing](Screen_Prompts/138_Voice_Search_Processing.md) — state
- 139. [Voice Search — Clarification](Screen_Prompts/139_Voice_Search_Clarification.md) — overlay
- 140. [Search Results](Screen_Prompts/140_Search_Results.md) — screen
- 141. [Search Empty State](Screen_Prompts/141_Search_Empty_State.md) — state
- 142. [Parent Area Search](Screen_Prompts/142_Parent_Area_Search.md) — screen

### B14

- 143. [Favorites](Screen_Prompts/143_Favorites.md) — screen

### B15

- 144. [Downloads](Screen_Prompts/144_Downloads.md) — screen
- 145. [Clear All Downloads Confirmation](Screen_Prompts/145_Clear_All_Downloads_Confirmation.md) — overlay
- 146. [Parent Download Cap and Policy](Screen_Prompts/146_Parent_Download_Cap_and_Policy.md) — screen

### B16

- 147. [Child Profile](Screen_Prompts/147_Child_Profile.md) — screen
- 148. [Choose Language](Screen_Prompts/148_Choose_Language.md) — overlay
- 149. [Switch Profile Parent Permission](Screen_Prompts/149_Switch_Profile_Parent_Permission.md) — overlay

### B17

- 150. [Deep Link Resolver](Screen_Prompts/150_Deep_Link_Resolver.md) — state

### B18

- 151. [Islamic Fact Detail](Screen_Prompts/151_Islamic_Fact_Detail.md) — screen
- 152. [Islamic Facts Browse](Screen_Prompts/152_Islamic_Facts_Browse.md) — screen

### C19

- 153. [Parent Profile PIN/Biometric Gate](Screen_Prompts/153_Parent_Profile_PIN_Biometric_Gate.md) — screen
- 154. [Restriction Screen](Screen_Prompts/154_Restriction_Screen.md) — screen
- 155. [Calm Locked State (screen-time limit reached)](Screen_Prompts/155_Calm_Locked_State_screen_time_limit_reached.md) — screen
- 156. [Bedtime Block Screen](Screen_Prompts/156_Bedtime_Block_Screen.md) — screen

### C20

- 157. [Parent Dashboard (landing)](Screen_Prompts/157_Parent_Dashboard_landing.md) — screen

### C21

- 158. [Child Management (List)](Screen_Prompts/158_Child_Management_List.md) — screen
- 159. [Add Child (Parent Management)](Screen_Prompts/159_Add_Child_Parent_Management.md) — screen
- 160. [Edit Child (Parent Management)](Screen_Prompts/160_Edit_Child_Parent_Management.md) — screen
- 161. [Disable Confirmation (step-up gated)](Screen_Prompts/161_Disable_Confirmation_step_up_gated.md) — overlay
- 162. [Re-Enable Confirmation (step-up gated)](Screen_Prompts/162_Re_Enable_Confirmation_step_up_gated.md) — overlay
- 163. [Permanent Deletion — Step 2: Irreversible-Data Warning](Screen_Prompts/163_Permanent_Deletion_Step_2_Irreversible_Data_Warning.md) — screen
- 164. [Trial-Cancellation Forced-Selection Screen](Screen_Prompts/164_Trial_Cancellation_Forced_Selection_Screen.md) — screen

### C22

- 165. [Per-Child Report (full view)](Screen_Prompts/165_Per_Child_Report_full_view.md) — screen
- 166. [Skill Detail Drill-down](Screen_Prompts/166_Skill_Detail_Drill_down.md) — screen
- 167. [AI Interaction History (full screen)](Screen_Prompts/167_AI_Interaction_History_full_screen.md) — screen
- 168. [Safety Report (on-demand, full screen)](Screen_Prompts/168_Safety_Report_on_demand_full_screen.md) — screen
- 169. [Monthly Family Report (cross-child, aggregate-only)](Screen_Prompts/169_Monthly_Family_Report_cross_child_aggregate_only.md) — screen
- 170. [AI Insight Report (premium)](Screen_Prompts/170_AI_Insight_Report_premium.md) — screen
- 171. [Achievement Share Card Preview (PII-free)](Screen_Prompts/171_Achievement_Share_Card_Preview_PII_free.md) — screen
- 172. [Full Activity Timeline](Screen_Prompts/172_Full_Activity_Timeline.md) — screen

### C23

- 173. [Controls Landing (Screen Time / Quiet Hours / AI Permissions / Content Age Level entry list)](Screen_Prompts/173_Controls_Landing_Screen_Time_Quiet_Hours_AI_Permissions_Content_Age_Level_entry_list.md) — screen
- 174. [Screen Time Settings (per child)](Screen_Prompts/174_Screen_Time_Settings_per_child.md) — screen
- 175. [Quiet Hours / Bedtime Settings (per child)](Screen_Prompts/175_Quiet_Hours_Bedtime_Settings_per_child.md) — screen
- 176. [AI Permissions Settings (per child)](Screen_Prompts/176_AI_Permissions_Settings_per_child.md) — screen
- 177. [Content Age Level Settings (per child)](Screen_Prompts/177_Content_Age_Level_Settings_per_child.md) — screen
- 178. [Child Locks & Sessions (per child)](Screen_Prompts/178_Child_Locks_Sessions_per_child.md) — screen
- 179. [Set Lock Type (Pattern/PIN/Biometric/None)](Screen_Prompts/179_Set_Lock_Type_Pattern_PIN_Biometric_None.md) — screen
- 180. [Device Revocation Confirmation](Screen_Prompts/180_Device_Revocation_Confirmation.md) — overlay
- 181. [Content Age Level — Override Confirmation](Screen_Prompts/181_Content_Age_Level_Override_Confirmation.md) — overlay

### C24

- 182. [Subscription & Billing (landing)](Screen_Prompts/182_Subscription_Billing_landing.md) — screen
- 183. [Plan Comparison](Screen_Prompts/183_Plan_Comparison.md) — screen
- 184. [Trial Disclosure Screen (length, price, renewal date, auto-renew)](Screen_Prompts/184_Trial_Disclosure_Screen_length_price_renewal_date_auto_renew.md) — screen
- 185. [Direct Upgrade Disclosure Screen](Screen_Prompts/185_Direct_Upgrade_Disclosure_Screen.md) — screen
- 186. [Invoice History](Screen_Prompts/186_Invoice_History.md) — screen
- 187. [Invoice Detail](Screen_Prompts/187_Invoice_Detail.md) — screen
- 188. [Cancel Flow — Confirmation](Screen_Prompts/188_Cancel_Flow_Confirmation.md) — screen
- 189. [Retry Failed Payment](Screen_Prompts/189_Retry_Failed_Payment.md) — screen
- 190. [Free-Plan Second-Child Upgrade Prompt (parent-mode only)](Screen_Prompts/190_Free_Plan_Second_Child_Upgrade_Prompt_parent_mode_only.md) — overlay

### C25

- 191. [Notifications (Parent) Inbox](Screen_Prompts/191_Notifications_Parent_Inbox.md) — screen
- 192. [Notification Preferences — Category Toggles](Screen_Prompts/192_Notification_Preferences_Category_Toggles.md) — screen
- 193. [Notification Preferences — Quiet Hours](Screen_Prompts/193_Notification_Preferences_Quiet_Hours.md) — screen
- 194. [Support Center (landing)](Screen_Prompts/194_Support_Center_landing.md) — screen
- 195. [FAQ Search](Screen_Prompts/195_FAQ_Search.md) — screen
- 196. [FAQ Article Detail](Screen_Prompts/196_FAQ_Article_Detail.md) — screen
- 197. [Contact Support Form](Screen_Prompts/197_Contact_Support_Form.md) — screen
- 198. [Ticket Submitted Confirmation](Screen_Prompts/198_Ticket_Submitted_Confirmation.md) — screen
- 199. [Ticket History List](Screen_Prompts/199_Ticket_History_List.md) — screen
- 200. [Ticket Detail / Status View](Screen_Prompts/200_Ticket_Detail_Status_View.md) — screen

### C26

- 201. [Settings (landing)](Screen_Prompts/201_Settings_landing.md) — screen
- 202. [Privacy & Support (landing, may be a sub-section of Settings)](Screen_Prompts/202_Privacy_Support_landing_may_be_a_sub_section_of_Settings.md) — screen
- 203. [Parent PIN Reset (Account Security)](Screen_Prompts/203_Parent_PIN_Reset_Account_Security.md) — screen
- 204. [Security — Device List](Screen_Prompts/204_Security_Device_List.md) — screen
- 205. [Device Revocation Confirmation](Screen_Prompts/205_Device_Revocation_Confirmation.md) — overlay
- 206. [Consent Log](Screen_Prompts/206_Consent_Log.md) — screen
- 207. [Consent Detail (full text + status)](Screen_Prompts/207_Consent_Detail_full_text_status.md) — screen
- 208. [Withdraw Optional Consent — Confirmation](Screen_Prompts/208_Withdraw_Optional_Consent_Confirmation.md) — overlay
- 209. [AI Interaction History](Screen_Prompts/209_AI_Interaction_History.md) — screen
- 210. [AI Interaction Detail (redacted)](Screen_Prompts/210_AI_Interaction_Detail_redacted.md) — screen
- 211. [Language Picker](Screen_Prompts/211_Language_Picker.md) — screen
- 212. [Data Export Request](Screen_Prompts/212_Data_Export_Request.md) — screen
- 213. [Export Status Tracking (preparing/ready)](Screen_Prompts/213_Export_Status_Tracking_preparing_ready.md) — screen
- 214. [Logout Confirmation (unsynced downloads present)](Screen_Prompts/214_Logout_Confirmation_unsynced_downloads_present.md) — overlay
- 215. [Security (PIN and Device Management landing)](Screen_Prompts/215_Security_PIN_and_Device_Management_landing.md) — screen
- 216. [Account Deletion Request and Confirmation](Screen_Prompts/216_Account_Deletion_Request_and_Confirmation.md) — screen
- 217. [Pending Account Deletion and Cancellation](Screen_Prompts/217_Pending_Account_Deletion_and_Cancellation.md) — screen

### F36

- 218. [Ramadan Prep / Countdown](Screen_Prompts/218_Ramadan_Prep_Countdown.md) — screen
- 219. [Ramadan Home](Screen_Prompts/219_Ramadan_Home.md) — screen
- 220. [Ramadan Journey Map](Screen_Prompts/220_Ramadan_Journey_Map.md) — screen
- 221. [Night Recap](Screen_Prompts/221_Night_Recap.md) — screen
- 222. [Ramadan Mission Detail](Screen_Prompts/222_Ramadan_Mission_Detail.md) — screen
- 223. [Ramadan Story Player](Screen_Prompts/223_Ramadan_Story_Player.md) — screen
- 224. [Fasting Tracker](Screen_Prompts/224_Fasting_Tracker.md) — screen
- 225. [Laylatul Qadr Reflection](Screen_Prompts/225_Laylatul_Qadr_Reflection.md) — screen
- 226. [Eid Countdown](Screen_Prompts/226_Eid_Countdown.md) — screen
- 227. [Eid Home](Screen_Prompts/227_Eid_Home.md) — screen
- 228. [Eid Reward Reveal](Screen_Prompts/228_Eid_Reward_Reveal.md) — screen
- 229. [Eid Card Generator](Screen_Prompts/229_Eid_Card_Generator.md) — screen
- 230. [Ramadan Complete Certificate](Screen_Prompts/230_Ramadan_Complete_Certificate.md) — screen
- 231. [Post-Eid Keep the Habit](Screen_Prompts/231_Post_Eid_Keep_the_Habit.md) — screen
- 232. [Parent Ramadan Settings](Screen_Prompts/232_Parent_Ramadan_Settings.md) — screen
- 233. [Parent Ramadan Dashboard](Screen_Prompts/233_Parent_Ramadan_Dashboard.md) — screen
- 234. [Family Ramadan Aggregate](Screen_Prompts/234_Family_Ramadan_Aggregate.md) — screen
- 235. [Family Ramadan Report](Screen_Prompts/235_Family_Ramadan_Report.md) — screen
- 236. [Conversion Moment Card](Screen_Prompts/236_Conversion_Moment_Card.md) — component
- 237. [Family Member Invite](Screen_Prompts/237_Family_Member_Invite.md) — screen

## Current execution review — Screen 002

[Language Selection review and node links](Evidence/002_Language_Selection_Review.md) · [Structural QA](Evidence/002_Language_Selection_QA.json). User approved four blueprint locales and immediate selection without Continue. Built in existing V2; screen review required before Screen 003. Localized interface/Intro copy and full RTL checks remain pending.


## Latest Screen 002 reference revision

[Current design and animation review](Evidence/002_Reference_Revision.md). The five requested QA/handoff frames are deleted. Continue now transforms into simulated processing and success. Success destination explicitly awaits Screen 003. Earlier Screen 002 review/QA records are historical.


## Current button revision

[Button return/retry review](Evidence/002_Button_Return_Review.md). Separate Success frames removed; completion now plays inline, then restores Continue. Rendered motion and reaction audit recorded.

## Mandatory visual baseline for every new screen

- [Finalized V2 reusable design prompt](12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md)
- [Current context and next-screen handoff](CURRENT_CONTEXT_AND_NEXT_SCREEN.md)

- [Incremental Figma module organization](13_INCREMENTAL_MODULE_ORGANIZATION.md) — required for all future screen work.
# Screen 010 implementation review — 21 October 2026

[OTP handoff and Figma links](Evidence/2026-10-21_010_OTP_Handoff.md) · [Verification](Evidence/2026-10-21_010_Verification.json). Implemented at390×844 using approved authentication styling. Awaiting user review; future success/fallback destinations remain unmapped. Screen009 rollback and approved screens through Registration preserved.

## Screen 012 implementation review — 21 October 2026

[Parent PIN Setup handoff](Evidence/2026-10-21_012_PIN_Handoff.md) · [Verification](Evidence/2026-10-21_012_Verification.json). Implemented at390×844 in existing V2 Onboarding; awaiting review. PIN equality/network are controlled prototype fixtures. Screen011 remains rolled back; future013/014 destinations are unmapped.

## Screen 013 implementation review — 21 October 2026

[Biometric enrollment handoff](Evidence/2026-10-21_013_Handoff.md) · [Verification](Evidence/2026-10-21_013_Verification.json). Approved copy implemented in existing V2 Onboarding bottom-sheet format; awaiting review. Connected from successful eligible PIN save; Add Child014 remains unmapped. Earlier013-uncreated notes are historical.

## Latest connected authentication flow repair — 21 October 2026

[OTP → PIN → Biometric navigation handoff](Evidence/2026-10-21_010_012_013_Navigation_Handoff.md) · [Verification](Evidence/2026-10-21_010_012_013_Navigation_Repair.json). Start the named new-parent flow at Registration1459:256. Corrected consent-context handoff, back/re-verification and misleading flow starts; existing designs unchanged.

## Latest OTP/PIN revision — 22 October 2026

[Single-entry PIN handoff](Evidence/2026-10-22_Single_Entry_PIN_Handoff.md) · [Verification](Evidence/2026-10-22_Single_Entry_PIN_Verification.json). OTP success → one PIN entry → save → Biometric directly. No confirmation or success dialog. Approved stars restored below OTP cards;33 action checks pass.

## Latest PIN navigation — 22 October2026

[Two-screen PIN handoff](Evidence/2026-10-22_Two_Screen_PIN_Handoff.md) · [Verification](Evidence/2026-10-22_Two_Screen_PIN_Verification.json). Latest user decision: Continue opens preserved Confirm PIN; Save PIN opens Biometrics after successful processing. All screens retained.

## Calm star enhancement —22 October2026

[18-screen enhancement handoff](Evidence/2026-10-22_Star_Enhancement_Handoff.md) · [Verification](Evidence/2026-10-22_Star_Enhancement_Verification.json). Reused staggered blinking stars above/below cards; foreground content and app navigation preserved. Awaiting review.


## Screen014 execution —22 October2026

Add Child now designed in V2 Onboarding: section1804:2599/main1804:2656. User-approved screenshot copy + PRD fields/3–17 range. See Evidence/014_Add_Child_Handoff.md,014_Final_Nodes.json and014_Verification.json.64 native stored-action checks and39 upstream checks pass; Present remains blocked, and name/date/catalog/API/persistence are controlled fixtures. Future018/019 stay unmapped. Stop for014 review before015. This supersedes older014-uncreated notes without changing historical evidence.
