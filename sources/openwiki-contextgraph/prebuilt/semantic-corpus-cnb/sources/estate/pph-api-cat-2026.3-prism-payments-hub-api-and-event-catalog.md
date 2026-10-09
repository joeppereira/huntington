<!-- source: raw/estate/PPH-API-CAT-2026.3_PRISM_Payments_Hub_API_and_Event_Catalog.pdf | converted by tools/convert_cnb_corpus.py -->
# PPH-API-CAT-2026.3 PRISM Payments Hub API and Event Catalog


<!-- page 1 -->

|  Payments & Treasury Technology 

**INTERNAL - CONFIDENTIAL** 

# **PRISM Payments Hub - API & Event Catalog (v1 / v2) incl. v1 Deprecation Notice** 

Consumer reference for REST APIs and Kafka topics exposed by PPH 

|**Document ID**|PPH-API-CAT-2026.3|
|---|---|
|**Version / Status**|2026.3 / Published|
|**Document owner**|Sunita Rao, Principal Engineer - PPH APIs|
|**Approver(s)**|Kevin O'Brien (EM); Raymond Ortiz (Director)|
|**Effective / Last reviewed**|Published 2026-09-10|
|**Classification**|INTERNAL - CONFIDENTIAL|
|**Related documents**|PPH-SYS-OVW-9.2; ADR-PAY-019; ADR-PAY-021; ADR-PAY-023; PPH-2190; PPH-2207|

## **1. Deprecation notice - PPH v1 APIs** 

#### **v1 sunset: 2027-03-31 (no extensions)** 

The v1 adapter is not supported on Volaris 9.6 (upgrade April 2027). ARB confirmed on 2026-09-08 that no extensions will be granted. All consumers must migrate to v2 and, for status use cases, to the pay.wire.lifecycle.v2 topic. 

|**v1 consumer**|**Owner**|**Migration status (PPH-2190)**|**Notes**|
|---|---|---|---|
|IVR wire status|Contact Center Tech|Migrated (2026-05)|-|
|Service Center CRM|CRM Engineering|In progress (target 2026-12)|-|
|cbo-wire-bff (Wire Center)|CBO Wire Center squad|Not started|Tracked as CBO-4471 (unscheduled)|
|Wire Room console|Payment Operations Tech|Migrated to IWB (2025)|-|

## **2. v1 APIs (deprecated)** 

|**ID**|**Method / path**|**Purpose**|**Limits**|
|---|---|---|---|
|EP-PPH-01|GET /pph/v1/wires/{wireRef}/status|Coarse status for one wire|20 TPS shared across all v1 consumers|
|EP-PPH-02|GET /pph/v1/wires?clientId&fromDate&toDate|List wires|Max 500 rows; no cursor|
|EP-PPH-03|POST /pph/v1/wires|Submit approved wire|-|

### **EP-PPH-01 response (excerpt)** 

```
{
```

- `"wireRef": "PPH26092400481233",` 

- `"status": "HELD",            // RECEIVED | PENDING | HELD | PROCESSED | REJECTED | CANCELLED | RETURNED` 

- `"statusTs": "2026-09-24T14:12:09-04:00",` 

- `"holdFlag": true,` 

- `"holdReasonDesc": "<string, max 255>", "fedRef": "20260924QMGFT015000123"     // IMAD; null for Swift wires }` 

|**Field**|**Description**|
|---|---|
|status|PROCESSED covers RELEASED, SENT_TO_NETWORK, NETWORK_ACCEPTED and COMPLETED (see PPH-SYS-OVW-9.2 s3).|
|holdReasonDesc|Free-text hold description synchronized from HMS (legacy, since 2019). Content is not curated for external display. Not present<br>in v2 (ADR-PAY-021).|
|fedRef|IMAD only. OMAD and UETR are not available in v1.|

## **3. v2 APIs (GA 2025-10)** 

Crestline National Bank  |  PPH-API-CAT-2026.3  v2026.3  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed

<!-- page 2 -->

|  Payments & Treasury Technology 

**INTERNAL - CONFIDENTIAL** 

|**ID**|**Method / path**|**Purpose**|**Limits / notes**|
|---|---|---|---|
|EP-PPH-04|GET /pph/v2/payments/{paymentId}|Payment detail incl. lifecycleState,<br>identifiers, network, hold, charges|150 TPS|
|EP-PPH-05|GET /pph/v2/payments?clientId&rail&state&from&to&c<br>ursor|Search|Filters by clientId (not<br>account); no beneficiary-name<br>filter (PPH-2251)|
|EP-PPH-06|GET /pph/v2/payments/{paymentId}/history|State history|Timestamps = PPH processing<br>time|
|EP-PPH-07|POST /pph/v2/payments|Submit payment|Idempotency-Key header<br>required|

### **EP-PPH-04 response (excerpt)** 

- `{` 

- `"paymentId": "PPH26092400481233",` 

- `"rail": "FEDWIRE",              // FEDWIRE | SWIFT | BOOK` 

- `"lifecycleState": "NETWORK_ACCEPTED",` 

- `"identifiers": { "cboRef": "CBW-20260924-004812", "imad": "...", "omad": "...",` 

- `"uetr": "8f0c1b52-4d1e-4b0a-9e43-2b6c1f4f7a10", "endToEndId": "INV-77812" },` 

- `"network": { "sentTs": "...", "gateway": "FFC" },` 

- `"hold": { "isHeld": false, "holdId": null },` 

- `"charges": { "chargeBearer": "SHAR", "orderingBankFee": { "amount": 30.00, "ccy": "USD" } }, "return": { "isoReason": null, "returnedTs": null } }` 

v2 does not include a settlement object. Rail-specific settlement status and the authoritative Federal Reserve acceptance timestamp are proposed in PPH-2207 (backlog, 8 pts, awaiting a product sponsor). Intermediary or beneficiary bank charges are not known to PPH. 

## **4. Kafka topics** 

|**ID**|**Topic**|**Content**|**Retention**|**Classification / onboarding**|
|---|---|---|---|---|
|EV-PPH-01|pay.wire.lifecycle.v2|WireLifecycleEvent v2.3 (Avro): paymentId, rail,|7 days|Confidential - Client. Consumer ACL|
|||fromState, toState, eventTs, identifiers,||via PPH Jira; ~3 weeks incl. schema|
|||return.isoReason||registry access|
|EV-PPH-02|pay.ach.lifecycle.v1|ACH lifecycle events|7 days|Consumed by CBO SPS (ACH Tracker)|

Hold reasons are not published on PPH topics. Return reasons (ISO pacs.004 codes, e.g., AC04, AC01, RR05) are published on pay.wire.lifecycle.v2 since 2026-08 (PPH-2266). 

## **5. Service levels** 

|**Interface**|**Availability**|**Latency (p95)**|**Support**|
|---|---|---|---|
|v1 REST|99.9%|350 ms|Best effort until sunset|
|v2 REST|99.95%|180 ms|T1|
|pay.wire.lifecycle.v2|99.95%|event lag < 2 s|T1|

## **6. Open backlog relevant to consumers** 

|**Key**|**Summary**|**Status**|
|---|---|---|
|PPH-2207|v2 settlement object (fedSettlementTs from pacs.002/OMAD; settlementStatus by rail)|Backlog - no sponsor|
|PPH-2251|v2 search: index beneficiary name|Backlog|
|PPH-2190|v1 sunset - consumer migration tracking|In progress|

Contacts: Sunita Rao (API design), Kevin O'Brien (scheduling via Payments Platform Demand Board), Laura Kim (product). 

Crestline National Bank  |  PPH-API-CAT-2026.3  v2026.3  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed