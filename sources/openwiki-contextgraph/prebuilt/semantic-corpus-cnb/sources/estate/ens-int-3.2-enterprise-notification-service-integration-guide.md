<!-- source: raw/estate/ENS-INT-3.2_Enterprise_Notification_Service_Integration_Guide.pdf | converted by tools/convert_cnb_corpus.py -->
# ENS-INT-3.2 Enterprise Notification Service Integration Guide


<!-- page 1 -->

|  Payments & Treasury Technology 

**INTERNAL - CONFIDENTIAL** 

# **Enterprise Notification Service - Integration Guide & Treasury Event Catalog** 

How producers register events and templates; current Treasury (TRS) event catalog; subscription model 

|**Document ID**|ENS-INT-3.2|
|---|---|
|**Version / Status**|3.2 / Published|
|**Document owner**|Melissa Grant, EM - Enterprise Notification Service|
|**Approver(s)**|Sanjay Iyer (Director, Enterprise Notification Platform)|
|**Effective / Last reviewed**|Published 2026-07-30|
|**Classification**|INTERNAL - CONFIDENTIAL|
|**Related documents**|CBO-ARCH-WC-4.1; POL-FCC-014; ENS-1120|

## **1. Overview** 

ENS delivers transactional notifications across email, SMS, mobile push (CBO Mobile) and the CBO in-app inbox. Producers send a registered **event type** ; ENS resolves recipients from **subscriptions** , renders an approved **template** and delivers per user channel preferences. 

|**Capability**|**Value**|
|---|---|
|Throughput|300 msgs/s sustained, 1,200 msgs/s burst (Treasury domain quota: 120 msgs/s)|
|Delivery latency (p95, push/in-app)|4 s|
|SMS|Requires TCPA consent flag from CBO user profile; 160-char templates|
|Masking|Account numbers masked to last 4; no Restricted data in payloads or templates|

## **2. Onboarding a new event type** 

1. Submit ServiceNow catalog item 'ENS Event Onboarding' (owner: Paul Henderson). 

2. Define payload schema and recipient resolution (subscription filters). 

3. Draft templates per channel; submit to the Disclosure Review Committee (DRC) - bi-weekly. 

4. ENS configuration and test (~12 ENS engineering hours per event type). 

5. Producer integration testing in UAT; production enablement. 

**SLA: 6 weeks** from complete submission to production, including DRC review. Requests submitted after 2026-11-20 are scheduled after the year-end change freeze. 

## **3. Subscription model** 

Subscriptions are created per user for an **event type** with optional filters on **accountId** and amount thresholds. ENS does not support subscriptions to an individual entity (for example a specific paymentId); entity-level subscriptions are planned under **ENS-1120 (2027-H1)** . Producers may send directly to a named user for transactional events where the producer itself maintains the recipient list (pattern 'producer-resolved recipients'). 

## **4. Treasury (TRS) event catalog - wire and ACH** 

|**Event type**|**Producer**|**Trigger**|**Template (subject line)**|**Status**|
|---|---|---|---|---|
|TRS.WIRE.APPROVAL_REQUIRED|CBO|Wire awaiting approver|TPL-WIRE-APR-01 'Wire awaiting your approval'|Live|
|TRS.WIRE.RELEASED|CBO|PPH v1 status -> PROCESSED|TPL-WIRE-REL-02 'Wire completed: {amount} to<br>{beneficiary}'|Live|
|TRS.WIRE.REJECTED|CBO|PPH v1 status -> REJECTED|TPL-WIRE-REJ-01 'Wire rejected'|Live|
|TRS.WIRE.INCOMING_POSTED|CDP|Incoming wire posted to DDA|TPL-WIRE-IN-03 'Incoming wire received'|Live|

Crestline National Bank  |  ENS-INT-3.2  v3.2  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed

<!-- page 2 -->

|  Payments & Treasury Technology 

**INTERNAL - CONFIDENTIAL** 

|**Event type**|**Producer**|**Trigger**|**Template (subject line)**|**Status**|
|---|---|---|---|---|
|TRS.ACH.STATUS_CHANGED|CBO SPS|ACH lifecycle milestone|TPL-ACH-STS-01|Live (2025-11)|
|TRS.ACH.RETURN_RECEIVED|CBO SPS|ACH return|TPL-ACH-RET-01|Live (2025-11)|

No event types are registered for wire network acceptance, beneficiary credit (gpi ACCC), wire returns, gpi milestones or client action required on held wires. 

## **5. APIs** 

|**ID**|**Endpoint**|**Purpose**|
|---|---|---|
|EP-ENS-01|POST /ens/v3/notifications|Send event (registered type, approved template)|
|EP-ENS-02|POST /ens/v3/subscriptions|Create subscription (eventType + accountId filter)|
|EP-ENS-03|GET /ens/v3/event-types?domain=TRS|Catalog|

## **6. Content rules** 

- Templates for financial-crimes related states must use FCC-approved copy (see POL-FCC-014 Appendix B). 

- Status wording in templates must follow the producer's approved status terminology. 

- No links that expose transaction data outside authenticated sessions. 

Crestline National Bank  |  ENS-INT-3.2  v3.2  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed