# Files

- [MDL-CAP-003 Capital Planning & Stress Projection Model](capital-planning-model.md) - Excel model (Tier 1) that rolls CET1 capital and standardized RWA forward nine quarters (Q3 2026 to Q3 2028) under a baseline plan and a severely adverse scenario, then derives the minimum stressed CET1 ratio, headroom, and an indicative stress capital buffer (SCB). Fed by API-16 (starting capital and RWA) and API-14 (scenario paths).
- [MDL-CR-007 CECL Allowance Model](cecl-allowance-model.md) - Excel model (CECL_Allowance_Model.xlsx) that turns API-10, API-11 and API-14 inputs into scenario-conditional lifetime ECL by segment, weights the three scenarios, adds a qualitative overlay and reconciles to the $15,920 million allowance reported at Dec 31, 2025 (Allowance_Summary!G12).
- [MDL-ALM-014 NII Sensitivity Model](nii-sensitivity-model.md) - Tier 1 Excel model that projects 12-month net interest income (NII) and economic value of equity (EVE) sensitivity under parallel rate shocks of +/-100 and +/-200 bp for IRRBB reporting. Documents the five sheets, key cell formulas, consumed APIs (API-11, API-12, API-15, API-16), limits, owner and validator.

# Directories

- [components](components/)
