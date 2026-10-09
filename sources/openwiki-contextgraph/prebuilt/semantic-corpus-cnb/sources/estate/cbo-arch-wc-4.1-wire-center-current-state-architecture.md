<!-- source: raw/estate/CBO-ARCH-WC-4.1_Wire_Center_Current-State_Architecture.pdf | converted by tools/convert_cnb_corpus.py -->
# CBO-ARCH-WC-4.1 Wire Center Current-State Architecture


<!-- page 1 -->

|  Payments & Treasury Technology 

**INTERNAL - CONFIDENTIAL** 

# **Crestline Business Online - Wire Center: Current-State Architecture** 

Existing commercial portal wire capabilities, integrations, status model and constraints 

|**Document ID**|CBO-ARCH-WC-4.1|
|---|---|
|**Version / Status**|4.1 / Approved|
|**Document owner**|Lucas Ferreira, Tech Lead - CBO Wire Center|
|**Approver(s)**|Anjali Deshpande (Director, Digital Treasury Channels Eng.); Nikhil Bose (Chief Architect)|
|**Effective / Last reviewed**|Last reviewed 2026-08-20|
|**Classification**|INTERNAL - CONFIDENTIAL|
|**Related documents**|PPH-API-CAT-2026.3; ENS-INT-3.2; ADR-PAY-019; PIR-2024-07; SEC-STD-22|

## **1. Overview** 

Crestline Business Online (CBO) is CNB's commercial digital banking portal (web and mobile) serving Treasury Management clients. The **Wire Center** module provides domestic (Fedwire) and international (Swift) wire initiation, templates, dual approval, release with step-up authentication, a wire activity list, wire detail, CSV export and confirmation PDF download. Wire Center does not currently provide milestone tracking, international (gpi) status, hold explanations or client actions on held wires. 

### **1.1 Usage (trailing 90 days to 2026-07-31)** 

|**Metric**|**Value**|
|---|---|
|Client companies with Wire Center entitlement|9,800|
|Active users (90-day)|41,000|
|Wires initiated via CBO per business day|11,600 avg (9,900 domestic / 1,700 international); month-end peak ~19,000|
|Wire Center page views per month|1.4 million|
|'Refresh status' clicks per month|310,000|
|Share of CNB outgoing wires originated in CBO|~67% (remainder: host-to-host files, Swift for Corporates, branch, Ops)|

## **2. Logical architecture** 

```
[Wire Center MFE (React 18, Aurora DS v4)]
        |  HTTPS (OAuth2 session)
[cbo-wire-bff  (Java 21 / Spring Boot 3, OpenShift)] ---> [CES  /ces/v2/users/{id}/entitlements]
        |                    |                     \---> [CBO Auth  /cbo/auth/v2/step-up]
        | REST (sync)        | REST (sync)
[PPH v1 APIs]          [ENS /ens/v3/notifications]
  /pph/v1/wires/{ref}/status   (EP-PPH-01)
  /pph/v1/wires?clientId...    (EP-PPH-02)
  POST /pph/v1/wires           (EP-PPH-03)
```

```
Not used by Wire Center today:  CBO Status Projection Service (SPS, ACH only), pay.wire.lifecycle.v2,
PPH v2 APIs, gpi data, HMS APIs, TDIP Insights API
```

### **2.1 Integration inventory** 

|**Consumer**|**Endpoint / interface**|**Purpose**|**Version**|**Notes**|
|---|---|---|---|---|
|cbo-wire-bff|POST /pph/v1/wires (EP-PPH-03)|Submit approved wire|v1|Returns pphId; stored with cboRef|
|cbo-wire-bff|GET /pph/v1/wires?clientId... (EP-PPH-02)|Activity list|v1|Max 500 rows; filters applied client-side<br>(CBO-4302)|
|cbo-wire-bff|GET /pph/v1/wires/{ref}/status (EP-PPH-01)|Wire detail status|v1|Cached 60 s; refresh throttled 1/60 s per wire|
|cbo-wire-bff|GET /ces/v2/users/{id}/entitlements<br>(EP-CES-01)|Authorization|v2|Account-level filtering of results|
|cbo-wire-bff|POST /cbo/auth/v2/step-up (EP-AUTH-01)|Step-up on release|v2|Push or OTP; reusable for other high-risk actions|

Crestline National Bank  |  CBO-ARCH-WC-4.1  v4.1  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed

<!-- page 2 -->

|  Payments & Treasury Technology 

**INTERNAL - CONFIDENTIAL** 

|**Consumer**|**Endpoint / interface**|**Purpose**|**Version**|**Notes**|
|---|---|---|---|---|
|cbo-wire-bff|POST /ens/v3/notifications (EP-ENS-01)|Wire notifications|v3|Produces TRS.WIRE.* events (Section 5)|

## **3. Status model and client-facing labels** 

Wire Center derives the displayed status from PPH v1 status values. Statuses prior to submission (Draft, Pending Approval, Approved) are CBO-owned. The label **'Completed'** replaced 'Processed' in R26.1 (CBO-4402) following client feedback that 'Processed' was unclear. 

|**PPH v1 status**|**CBO label**|**Visual**|**Since**|
|---|---|---|---|
|(CBO) DRAFT / PENDING_APPROVAL / APPROVED|Draft / Pending Approval / Approved|grey|R21|
|RECEIVED|Submitted|blue|R21|
|PENDING|In Process|blue|R21|
|HELD|Pending Review|amber|R22|
|PROCESSED|Completed|green check|R26.1 (was 'Processed')|
|REJECTED|Rejected|red|R21|
|CANCELLED|Cancelled|grey|R21|
|RETURNED|Returned|red|R23|

Hold reasons are not displayed today; held wires show 'Pending Review' with the standard text 'This wire is being reviewed.' 

## **4. Identifiers stored by Wire Center** 

|**Identifier**|**Example**|**Source**|**Stored in CBO?**|
|---|---|---|---|
|cboRef|CBW-20260924-004812|CBO|Yes (primary key)|
|pphId|PPH26092400481233|PPH v1 POST response|Yes|
|IMAD (Fedwire input reference)|20260924QMGFT015000123|PPH v1 fedRef|Displayed only (CBO-4355); not<br>persisted|
|OMAD (Fed output reference)|-|Not available in v1|No|
|UETR (end-to-end tracking id)|-|Not available in v1|No|

## **5. Notifications produced by Wire Center** 

|**Event type**|**Trigger**|**Template**|**Channels**|
|---|---|---|---|
|TRS.WIRE.APPROVAL_REQUIRED|Wire awaiting approver|TPL-WIRE-APR-01|email, push, in-app|
|TRS.WIRE.RELEASED|PPH v1 status transitions to PROCESSED|TPL-WIRE-REL-02|email, push, in-app, SMS (opt-in)|
|TRS.WIRE.REJECTED|PPH v1 status REJECTED|TPL-WIRE-REJ-01|email, push, in-app|

## **6. Security and entitlements** 

- Entitlement types in use: WIRE_VIEW, WIRE_INITIATE, WIRE_APPROVE, WIRE_RELEASE, WIRE_TEMPLATE_ADMIN (CES). 

- Release requires step-up authentication (EP-AUTH-01) and client-configured dual approval above client thresholds. 

- External sharing of client transaction data (links or documents shared with non-users) is not supported; any such capability requires an InfoSec design review under SEC-STD-22 (Digital Channel External Sharing & Step-Up Standard) and a Privacy Impact Assessment. 

- Search results are filtered to the user's entitled accounts in the BFF. 

## **7. Constraints and known limitations** 

1. **No status polling.** Per ADR-PAY-019 (following INC-2024-1182), Wire Center must not poll PPH for status; only user-initiated refresh is permitted (throttled 1 per 60 s per wire). New status capabilities must be event-driven. 

Crestline National Bank  |  CBO-ARCH-WC-4.1  v4.1  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed

<!-- page 3 -->

|  Payments & Treasury Technology 

**INTERNAL - CONFIDENTIAL** 

2. **PPH v1 sunset 2027-03-31.** Migration to v2 is tracked as CBO-4471 (34 pts, unscheduled) and depends on CBO-4473 (CES account-filter mapping). 

3. **No international tracking.** gpi status is visible only to Payment Operations in the Investigations Workbench (spike CBO-4480). 

4. **Activity list limits.** v1 list returns max 500 rows without cursor; no beneficiary-name search server-side. 

5. **Status Projection Service** (SPS, CBO-3815) is configured for ACH only; wire support requires a new mapping module and a consumer ACL on pay.wire.lifecycle.v2. 

## **8. Reusable assets** 

|**Asset**|**Origin**|**Reuse notes**|
|---|---|---|
|<cbo-journey-timeline> component (Aurora|CBO-3802 (ACH Payment|Rail-agnostic milestone timeline incl. terminal/error styling|
|DS v4)|Tracker)||
|Status Projection Service (SPS)|CBO-3815|Kafka consumer -> Postgres read model -> /cbo/sps/v1; add payment<br>types by config + mapping module|
|Step-up authentication|CBO Auth v2|Already used for wire release; reusable for other high-risk client actions|
|ENS producer library|cbo-commons 3.x|Templated sends with masking helpers|

Crestline National Bank  |  CBO-ARCH-WC-4.1  v4.1  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed