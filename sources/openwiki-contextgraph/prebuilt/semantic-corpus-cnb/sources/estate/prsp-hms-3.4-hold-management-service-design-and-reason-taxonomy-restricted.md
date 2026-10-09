<!-- source: raw/estate/PRSP-HMS-3.4_Hold_Management_Service_Design_and_Reason_Taxonomy_RESTRICTED.pdf | converted by tools/convert_cnb_corpus.py -->
# PRSP-HMS-3.4 Hold Management Service Design and Reason Taxonomy RESTRICTED


<!-- page 1 -->

|  Financial Crimes Technology 

**RESTRICTED - FINANCIAL CRIMES** 

# **Payment Risk & Screening Platform - Hold Management Service: Design & Hold Reason Taxonomy** 

Hold lifecycle, reason codes, disposition controls and data handling for payment holds 

|**Document ID**|PRSP-HMS-3.4|
|---|---|
|**Version / Status**|3.4 / Approved|
|**Document owner**|Daniel Kowalski (Tech Lead) / Grace Mensah (EM), Financial Crimes Technology|
|**Approver(s)**|Victor Petrov (Director, FCT); reviewed by Jordan Ellis (FCC Policy & Advisory)|
|**Effective / Last reviewed**|Last reviewed 2026-06-24|
|**Classification**|RESTRICTED - FINANCIAL CRIMES|
|**Related documents**|POL-FCC-014; PPH-SYS-OVW-9.2; MRM-POL-02; FCT-1893; FCT-1951; FCT-2004|

## **1. Purpose and scope** 

The Hold Management Service (HMS) is the system of record for holds placed on outbound payments by screening, fraud, funds control and operational controls. It is part of the Payment Risk & Screening Platform (PRSP) together with **Sentinel Fraud Scoring** (vendor model, MRM ID M-FCT-0021) and **SanctionScreen** (OFAC and other sanctions lists). HMS work queues are surfaced to Payment Operations and the FIU via the Investigations Workbench (IWB). 

## **2. Hold lifecycle** 

|**State**|**Description**|
|---|---|
|OPEN|Hold created; payment in PPH state HELD|
|IN_REVIEW|Assigned to analyst (Wire Room, Fraud Ops, Sanctions L1/L2, FIU)|
|ESCALATED|Escalated (e.g., Sanctions L2, FIU)|
|RELEASED|Disposition = release (maker-checker); PPH resumes processing|
|REJECTED|Disposition = reject; PPH cancels payment|
|BLOCKED|OFAC blocking; funds moved to blocked account; reported to OFAC within 10 business days (31 CFR 501.603)|
|EXPIRED|Auto-cancel after client response window (HRC-01/02/05)|

## **3. Hold reason taxonomy** 

Disclosure tiers are defined by POL-FCC-014 (P = public status, C = client-actionable, G = generic review, R = restricted). 

|**Code**|**Mnemonic**|**Description**|**Tier**|**Share of holds**|
|---|---|---|---|---|
|HRC-01|DUP_SUSPECT|Possible duplicate of a recent wire (same beneficiary/amount/date<br>window)|C|22%|
|HRC-02|CALLBACK_REQUIRED|Out-of-band callback verification for new/changed beneficiary above<br>threshold|C|18%|
|HRC-03|LIMIT_EXCEEDED|Client daily / per-transaction limit exceeded|C|9%|
|HRC-04|CUTOFF_WAREHOUSED|Received after Fedwire customer cutoff (6:00 p.m. ET) or future-dated|P|6%|
|HRC-05|FUNDS_PENDING|Insufficient available balance at funds control|C|14%|
|HRC-06|REPAIR_REQUIRED|Message repair (e.g., structured postal address, invalid routing/BIC)|C|11% (forecast ~16% after<br>Nov-2026 address<br>enforcement)|
|HRC-07|FRAUD_MODEL_HIGH|Sentinel fraud score above threshold|R|8%|
|HRC-08|ATO_SUSPECT|Session / device anomalies indicating possible account takeover|R|1%|
|HRC-09|SANCTIONS_REVIEW|SanctionScreen potential match pending L1/L2 review|R|7%|
|HRC-10|AML_REVIEW|Unusual activity review by FIU|R|2%|

Crestline National Bank  |  PRSP-HMS-3.4  v3.4  |  RESTRICTED - FINANCIAL CRIMES  |  Uncontrolled when printed

<!-- page 2 -->

|  Financial Crimes Technology 

**RESTRICTED - FINANCIAL CRIMES** 

|**Code**|**Mnemonic**|**Description**|**Tier**|**Share of holds**|
|---|---|---|---|---|
|HRC-11|LEGAL_HOLD|Legal process / law enforcement request|R|<0.5%|
|HRC-12|OPS_MANUAL_REVIEW|Large-value or exception manual review by Wire Room|G|1.5%|

Volumes: ~410 holds per business day (2.6% of outbound wires). Median time to disposition: HRC-01 47 min; HRC-02 2 h 10 min; HRC-07 1 h 35 min; HRC-09 3 h 20 min; HRC-10 1-5 business days. 

## **4. Data handling** 

- Hold **description** and **analystNotes** are classified Restricted. Descriptions are generated from rule templates and typically contain the HRC mnemonic and context, e.g., 'FRAUD_MODEL_HIGH sc=9xx L1 queue', 'SANCTIONS_REVIEW name match 0.91 L2', 'Possible duplicate of PPH260924...'. 

- The HMS-to-PPH description sync (feeding PPH v1 holdReasonDesc) predates ADR-PAY-021 and remains active for v1 backward compatibility until v1 sunset. Risk FCT-2004 is open. 

- Topic risk.hold.events.v1 is restricted to FCT and Payment Operations tooling. Channel applications are not authorized consumers. 

## **5. Interfaces** 

|**ID**|**Interface**|**Callers**|**Notes**|
|---|---|---|---|
|EP-HMS-01|GET /prsp/hms/v1/holds?paymentId=|IWB; PPH (legacy sync)|Returns hrcCode, category, description,<br>analystNotes, slaDueTs|
|EP-HMS-02|POST /prsp/hms/v1/holds/{holdId}/disposition|IWB only|Role HOLD_RELEASER; maker-checker<br>(CTRL-PAY-012)|
|EV-HMS-01|risk.hold.events.v1|FCT / Ops tooling|Restricted|

There is currently no client-facing interface. Proposal **FCT-1893** (Client-Safe Hold Status Facade, 21 pts, deprioritized 2025-Q3) would add GET /prsp/hms/v1/holds/{holdId}/client-view returning only disclosure tier, approved copy key and permitted client actions. A client attestation endpoint does not exist. 

## **6. Controls** 

|**Control**|**Requirement**|
|---|---|
|CTRL-PAY-012|Release/reject dispositions require maker-checker by users with HOLD_RELEASER role.|
|CTRL-PAY-018|Callback verification (HRC-02) must be completed by phone to a contact on file obtained independently of the payment<br>instruction or the requesting session. Confirmations received through the channel that initiated the payment do not satisfy this<br>control.|
|CTRL-PAY-031|(Updated 2026-06 following pilot FCT-1951) Duplicate-suspect holds (HRC-01) may be resolved by client attestation through a<br>digital channel, subject to step-up authentication of an entitled user. Attestation for amounts above $5,000,000 still requires Wire<br>Room release. Applies to HRC-01 only.|
|CTRL-PAY-040|No client-facing estimate of release time may be provided for holds in tiers G or R.|

## **7. Sanctions-specific handling** 

Where a payment is blocked or rejected for sanctions reasons, Sanctions Operations notifies the client in writing per the Sanctions Operations Procedure and reports to OFAC (blocked: 31 CFR 501.603; rejected: 31 CFR 501.604). Channels must not communicate screening outcomes. 

Crestline National Bank  |  PRSP-HMS-3.4  v3.4  |  RESTRICTED - FINANCIAL CRIMES  |  Uncontrolled when printed