# Family Summary: complete saved data

Figma-only update on25October2026. Summary2137:6635, saving1804:3379.

The prior summary read mutable Add Child draft variables and had a fixed avatar image. Its blank canvas fields reflected empty draft defaults; the chosen avatar was not bound at all.

The existing save-success branch now copies nickname, DOB, preferred language, learning level, avatar ID, five Learning Focus choices and AI Voice Guidance into dedicated saved-profile variables before navigating to Family Summary. Summary fields bind to these saved values. An80-image stack reuses original avatar artwork, with exactly one selected image visible based on the saved avatar ID. The empty-focus dash is computed from saved focus values. Existing error/validation branches were preserved.

Standalone canvas uses the existing Aisha review fixture as its preview. It is sample data. In Present, the success action replaces this snapshot with the values entered/selected on Add Child. No backend save is performed by Figma.

Verification: inspected populated Name/DOB/Language/Level/Voice canvas screenshot2026-10-25_Family_Summary_Saved_Profile.png. Retrieved actual stored success actions and evaluated5120 combinations (80avatars ×32focus combinations ×2voice states) outside the Figma API. All5120 passed field-copy equality, exactly-one chosen avatar and correct empty-focus state; success destination is2137:6635. The initial larger in-Figma verification call lost its transport; its result was not counted as a pass. Retrieved the stored actions afterward for the passing bounded check.

Live Present playback remains unverified. Confirm remains disabled pending an approved V2 Profile Picker destination. No app/backend code was changed.
