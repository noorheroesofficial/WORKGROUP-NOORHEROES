# Screen 014 refinement — 2026-10-22

Scope: existing Add Child flow only. User approved the supplied seven-change request and display-age boundaries: 3–7 → 5_8, 8–9 → 8_10, 10–13 → 10_14, 14–17 → 14_18_plus. PRD remains authoritative for the 3–17 eligibility rule. Blueprint's old grid/Compose date-picker guidance is superseded by this explicit native-picker/carousel request.

Contract: existing AddChildState, ViewModel events, draft persistence and network DTOs remain. Existing API avatar IDs remain until a backend-approved mapping exists for the new portrait library. New portrait IDs in Figma are design-prototype values only and are not submitted to the API.

Work items:
1. Update existing Figma headers/logo, learning artwork, language sheet and shared age-wise portrait carousel. Remove nickname/custom-DOB sheets and dangling destinations. Keep current confirmed navigation.
2. Preserve editable nickname input and IME dismissal. Add native Android DatePickerDialog and UIKit UIDatePicker with current-value initialization and exact age bounds.
3. Add lazy center-snapping avatar UI, selected gold ring/check, stable keys and accessibility selection semantics. Accurate birthday-aware age validation, eligible selection retention/default and safe catalog behavior.
4. RED/GREEN tests for date bounds, invalid civil dates, birthday edges, library boundaries and state selection. Compile Android, inspect final Figma geometry/screenshots. Record unavailable device/iOS checks explicitly.

Constraints: Native Design cannot run arbitrary text input or platform dialogs. Code Layers are disabled; editable Figma will not pretend to provide these native interactions. Real native behavior belongs to the mobile implementation. Windows cannot run Xcode/iOS. Existing browser policy prevents live Figma Present playback.
