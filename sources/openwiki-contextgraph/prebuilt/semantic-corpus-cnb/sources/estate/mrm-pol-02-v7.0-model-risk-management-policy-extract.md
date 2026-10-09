<!-- source: raw/estate/MRM-POL-02_v7.0_Model_Risk_Management_Policy_Extract.pdf | converted by tools/convert_cnb_corpus.py -->
# MRM-POL-02 v7.0 Model Risk Management Policy Extract


<!-- page 1 -->

|  Model Risk Management 

**INTERNAL - CONFIDENTIAL** 

# **Model Risk Management Policy (extract)** 

Model definition, tiering, validation and use limitations - aligned to the April 2026 interagency guidance 

|**Document ID**|MRM-POL-02|
|---|---|
|**Version / Status**|7.0 / Approved - Board Risk Committee|
|**Document owner**|Jonathan Price, Head of Model Risk Management|
|**Approver(s)**|Board Risk Committee (2026-06-18)|
|**Effective / Last reviewed**|Effective 2026-07-01|
|**Classification**|INTERNAL - CONFIDENTIAL|
|**Regulatory alignment**|Revised interagency Guidance on Model Risk Management issued 2026-04-17 (Federal Reserve SR 26-2; OCC Bulletin<br>2026-13; FDIC FIL-15-2026), which rescinded SR 11-7 / OCC 2011-12|
|**Related documents**|POL-FCC-014; DUS-07; ADR-PAY-026; TDIP-CAT-2026.2|

## **1. Changes in version 7.0** 

Version 7.0 re-baselines the policy following the April 17, 2026 interagency guidance that replaced SR 11-7. Key changes: a model definition that requires complexity; a formal End-User Analytic (EUA) category for simple calculations; risk-based tiering emphasizing model purpose and exposure; and a dedicated section on vendor models. 

## **2. Definitions** 

|**Term**||**Definition**||
|---|---|---|---|
|Model||A quantitative method applying statistical, economic, fin<br>complexity to produce estimates or predictions used in|ancial or machine-learning techniques of meaningful<br>decisions or communicated to clients.|
|End-User A|nalytic (EUA)|Simple descriptive calculations (counts, medians, percen<br>estimation. Registered in Archer with business-owner at|tages over historical data) with no forward-looking<br>testation; no independent validation.|
|Customer-f|acing estimate|Any forward-looking value shown to a client (e.g., expec|ted delivery time, probability of completion).|
|**3. Tier**<br>**Tier**|**ing**<br>**Criteria**||**Validation before use**|
|Tier 1|Regulatory, capital,|financial-crimes detection, or high financial exposure|Full independent validation; annual review|
|Tier 2|Customer-facing es|timates; models influencing client decisions or treatment|Independent validation; 10-14 weeks typical; 160-240<br>validator hours|
|Tier 3|Internal operationa|l models with limited exposure|Targeted validation; 6-9 weeks|
|EUA|Descriptive only||Registration + attestation (~2 weeks)|

**Customer-facing estimates are Tier 2 at minimum** and may not be shown to clients before validation is complete and use conditions (disclaimers, monitoring thresholds) are approved. 

## **4. Use limitations** 

- Models and their inputs may be used only for registered purposes. Outputs of financial-crimes models (Tier 1) - including Sentinel fraud scores (M-FCT-0021) and beneficiary mule-risk features (M-FCT-0034) - may not be used for product, marketing or client-facing purposes. 

- Vendor models: where developers cannot provide sufficient information, compensating controls and outcome monitoring are required. 

## **5. Inventory extract (Treasury & Payments)** 

Crestline National Bank  |  MRM-POL-02  v7.0  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed

<!-- page 2 -->

|  Model Risk Management 

**INTERNAL - CONFIDENTIAL** 

|**Model ID**|**Name**|**Tier**|**Owner**|**Status**|
|---|---|---|---|---|
|M-FCT-0021|Sentinel payment fraud score (vendor)|1|Victor Petrov|Validated 2025-12|
|M-FCT-0034|Beneficiary mule-risk features|1|Victor Petrov|Validated 2026-02|
|M-TRS-0142|Treasury Insights cash forecast|3 (re-tiering to 2 under v7.0|Wei Zhang|Validated 2025-09 (9|
|||review)||weeks)|
|EUA-TRS-0007|Ops corridor completion dashboard|EUA|Denise Carter|Registered 2026-05|

## **6. Capacity notice (Q4-2026)** 

The Tier 2 validation queue is approximately **6 weeks** before work starts. Submissions should include development documentation, data lineage and proposed monitoring. Contact: Sophie Laurent (Validation Lead, Treasury & Operations models). 

Crestline National Bank  |  MRM-POL-02  v7.0  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed