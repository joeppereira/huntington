<!-- source: raw/estate/ARB-PAY-REG-2026Q3_Payments_ARB_ADR_Register_and_Minutes.pdf | converted by tools/convert_cnb_corpus.py -->
# ARB-PAY-REG-2026Q3 Payments ARB ADR Register and Minutes


<!-- page 1 -->

**CRESTLINE NATIONAL BANK** |  Enterprise Architecture 

**INTERNAL - CONFIDENTIAL** 

# **Payments Architecture Review Board - ADR Register & Decision Minutes (extract)** 

Architecture decisions binding on channel, payments and data teams; minutes of 2026-09-08 

|**Document ID**|ARB-PAY-REG-2026Q3|
|---|---|
|**Version / Status**|2026-Q3 / Published|
|**Document owner**|Jenna Ross, ARB Secretariat|
|**Approver(s)**|Nikhil Bose, Chief Architect - Payments & Treasury (ARB Chair)|
|**Effective / Last reviewed**|Published 2026-09-12|
|**Classification**|INTERNAL - CONFIDENTIAL|
|**Related documents**|PIR-2024-07; PPH-API-CAT-2026.3; TDIP-CAT-2026.2|

## **1. ADR register (Payments)** 

|**ADR**|**Title**|**Date**|**Status**|**Applies to**|
|---|---|---|---|---|
|ADR-PAY-017|Kafka (Confluent) is the integration backbone for payment lifecycle events|2023-11-07|Accepted|All payment systems|
|ADR-PAY-019|Channel status integrations must be event-driven; no polling of PPH|2024-06-11|Accepted|All channels|
|ADR-PAY-021|Hold reason details never leave the financial-crimes trust boundary|2025-04-08|Accepted|PPH v2, channels, data|
|ADR-PAY-023|UETR is the canonical end-to-end correlation id for all outbound wires|2025-09-09|Accepted|PPH, gateways, channels,<br>TDIP|
|ADR-PAY-026|Client-facing analytical outputs are served via the TDIP Insights API|2026-05-12|Accepted|Channels, TDIP|

### **ADR-PAY-019 - Event-driven channel status** 

**Context:** INC-2024-1182 showed that channel polling of PPH v1 can degrade wire release at peak. **Decision:** Channels obtain payment status by consuming lifecycle events into a channel-owned read model (pattern: CBO Status Projection Service). Synchronous status calls are limited to user-initiated refresh with throttling. **Consequences:** new status features must budget for topic onboarding, a projection/mapping module and replay handling. 

### **ADR-PAY-021 - Hold reason confidentiality** 

**Decision:** Hold reason codes, descriptions, scores and analyst notes remain within FCT systems. PPH v2 and events expose only hold presence and holdId. Any client-facing hold explanation must be obtained from an FCT-owned, FCC-approved facade that returns disclosure tier and approved copy, not raw reasons. **Note:** legacy v1 holdReasonDesc retained until v1 sunset. 

### **ADR-PAY-023 - UETR as correlation id** 

**Decision:** PPH assigns a UETR to every outbound wire at release (including Fedwire pacs.008). Consumers needing to correlate with gpi data must store UETR from v2 APIs or lifecycle events. v1 consumers do not receive UETR. 

### **ADR-PAY-026 - Insights served via TDIP** 

**Decision:** Predictions, typical-time statistics and other analytical outputs shown to clients are computed in TDIP and served via versioned Insights API endpoints; channel BFFs must not compute analytics. Each insight requires MRM classification (model or EUA) before production. 

## **2. Minutes - ARB session 2026-09-08 (extract)** 

|**Item**|**Discussion / decision**|**Owner**|
|---|---|---|
|PPH v1 sunset|Volaris 9.6 removes the v1 adapter. Decision:**no extension beyond 2027-03-31**. Remaining|Kevin O'Brien|
||consumers must present migration plans at the 2026-11-10 ARB.||

Crestline National Bank  |  ARB-PAY-REG-2026Q3  v2026-Q3  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed

<!-- page 2 -->

**CRESTLINE NATIONAL BANK** |  Enterprise Architecture 

**INTERNAL - CONFIDENTIAL** 

|**Item**|**Discussion / decision**|**Owner**|
|---|---|---|
|gpi real-time service|GTRS (GTSI-0107) not funded for 2026. Board noted client demand; recommended GTSI engage<br>channel teams early. Interim exposure of GPI_TRACKER_SNAPSHOT directly to channels is**not**<br>**approved**; a read-only service with quota isolation would require ARB review.|Elena Vasquez|
|Status projection reuse|Board reaffirmed SPS as the reference pattern for client-facing status of any payment type.|Arjun Mehta|
|Structured address<br>enforcement|PPH and gateways on track for November 2026; expect increase in repair holds.|Raymond Ortiz|

Next sessions: 2026-11-10 and 2026-12-08. Submissions due 10 business days prior via the ARB intake form. 

Crestline National Bank  |  ARB-PAY-REG-2026Q3  v2026-Q3  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed