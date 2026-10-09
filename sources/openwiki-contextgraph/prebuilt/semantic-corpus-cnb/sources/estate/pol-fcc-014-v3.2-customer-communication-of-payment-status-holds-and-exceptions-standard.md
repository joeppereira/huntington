<!-- source: raw/estate/POL-FCC-014_v3.2_Customer_Communication_of_Payment_Status_Holds_and_Exceptions_Standard.pdf | converted by tools/convert_cnb_corpus.py -->
# POL-FCC-014 v3.2 Customer Communication of Payment Status Holds and Exceptions Standard


<!-- page 1 -->

|  Financial Crimes Compliance 

**INTERNAL - CONFIDENTIAL** 

# **Customer Communication of Payment Status, Holds & Exceptions Standard** 

Enterprise standard governing what may and may not be communicated to clients about payment status, holds and exceptions 

|**Document ID**|POL-FCC-014|
|---|---|
|**Version / Status**|3.2 / Approved - Enterprise Policy Committee|
|**Document owner**|Catherine Doyle, EVP, Chief BSA/AML Officer; co-owner Michael Tran, SVP, OFAC/Sanctions Officer|
|**Approver(s)**|Enterprise Policy Committee (2026-02-12)|
|**Effective / Last reviewed**|Effective 2026-03-01; next review 2027-03-01|
|**Classification**|INTERNAL - CONFIDENTIAL|
|**Policy contact**|Jordan Ellis, VP, FCC Policy & Advisory|
|**Related documents**|PRSP-HMS-3.4; DUS-07; MRM-POL-02; SEC-STD-22; CTRL-PAY-018 / -031 / -040|

## **1. Purpose** 

This Standard defines how CNB communicates the status of client payments, holds and exceptions through any client-facing channel. It protects the confidentiality of suspicious activity reporting, prevents disclosure that could aid fraud or sanctions evasion, and ensures status representations are accurate and not misleading. 

## **2. Scope** 

All client-facing channels and artifacts: Crestline Business Online (web and mobile), APIs and host-to-host status files, notifications (email, SMS, push, in-app), Commercial Service Center scripts, relationship manager communications, downloadable reports and any content shared with third parties at a client's request. 

## **3. Regulatory and legal basis** 

|**Source**|**Relevance**|
|---|---|
|31 U.S.C. 5318(g)(2); 31 CFR 1020.320(e)|Confidentiality of Suspicious Activity Reports - no disclosure of a SAR or information that would<br>reveal its existence|
|31 CFR Part 501 (incl. 501.603, 501.604)|OFAC blocking and reject reporting; sanctions outcomes communicated only per Sanctions<br>Operations Procedure|
|UCC Article 4A; Regulation J (12 CFR 210, Subpart B)|Acceptance, settlement finality and completion of funds transfers|
|FFIEC 'Authentication and Access to Financial Institution<br>Services and Systems' (2021)|Risk-based authentication for high-risk actions|
|Section 5 of the FTC Act (UDAP)|Representations to clients must not be unfair or deceptive|
|CNB Fair Representation Standard (FRS-02)|Accuracy of client-facing estimates and status language|

## **4. Disclosure tiers** 

|**Tier**|**Name**|**Client may see**|**Examples**|
|---|---|---|---|
|P|Public status|Factual processing status and timing|Scheduled for next business day (after cutoff)|
|C|Client-actionable|Approved explanation and permitted client action|Possible duplicate; limit exceeded; funds pending|
|G|Generic review|Generic 'being reviewed' message only|Operations manual review|
|R|Restricted|Generic 'being reviewed' message only - identical to<br>tier G|Fraud, account takeover, sanctions, AML, legal holds|

## **5. Requirements** 

Crestline National Bank  |  POL-FCC-014  v3.2  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed

<!-- page 2 -->

|  Financial Crimes Compliance 

**INTERNAL - CONFIDENTIAL** 

### **5.1 Holds** 

1. Restricted (R) reasons, hold codes, scores, list names, match details, analyst notes or queue names must never be displayed, transmitted or implied in any client-facing channel. 

2. **Indistinguishability:** tier R and tier G holds must be presented identically - same label, icon, color, copy, actions and absence of timing information - so that a client cannot infer the nature of a review from the presentation. 

3. No estimated release time, likelihood of release or 'next steps' timing may be shown for tier G or R holds (CTRL-PAY-040). 

4. Client actions on holds are permitted only where Appendix A allows, using step-up authentication of an entitled user. 

5. Callback verification (HRC-02) cannot be satisfied by any confirmation inside the channel that initiated the payment (CTRL-PAY-018). The channel may display that a callback is pending and allow the client to request a callback. 

6. Sanctions blocks/rejects are communicated only by Sanctions Operations per procedure; channels show tier G/R presentation. 

### **5.2 Status terminology** 

|**Term**|**Permitted only when**|**Not permitted**|
|---|---|---|
|Sent / In transit|Released and transmitted to the payment network|Before network transmission|
|Delivered to beneficiary's bank<br>(domestic)|Fedwire acceptance received (pacs.002 with OMAD)|At release or transmission|
|Completed / Settled|Domestic: Fedwire acceptance received. International: gpi<br>ACCC received from the beneficiary bank|On release, transmission, Swift network ACK or<br>ACSP statuses|
|Credited to beneficiary|gpi ACCC received|Domestic Fedwire (beneficiary credit is not<br>reported); any non-ACCC status|
|Tracking unavailable beyond [bank]|Last gpi status ACSP/G001|Showing 'in transit' with estimates after G001|
|Returned + reason|Return received; ISO reason from returning bank may be<br>shown (e.g., AC04 Account closed)|Returns initiated by CNB for financial-crimes<br>reasons (show 'Returned' only)|

### **5.3 International (gpi) data** 

For the client's own payments, channels may display agent names, countries, timestamps and deducted charges reported via gpi. Where tracking ends at a non-gpi agent, the presentation must state that tracking is unavailable beyond that point. 

### **5.4 Sharing with third parties** 

Status shared with a beneficiary or other third party at the client's request is limited to: amount, currency, value date, status milestones and a reference (cboRef or UETR). It must exclude account numbers, fees, the originator's internal references and any hold information. Links must expire within 7 days, must be enabled by a client administrator, and require InfoSec (SEC-STD-22) and Privacy approval of the design. 

### **5.5 Predictive and insight statements** 

Client-facing insights (for example typical completion times or estimated delivery) must: (a) use only the requesting client's own data, or aggregated cohorts meeting DUS-07 Section 5; (b) be registered with Model Risk Management where MRM-POL-02 applies; (c) carry a DRC-approved disclaimer; (d) never be shown for payments in tier G or R hold. 

## **6. Approvals** 

New or changed client-facing status, hold or exception experiences require FCC Policy & Advisory review before build commitment and DRC approval of final copy. Exceptions require Chief BSA/AML Officer approval. 

## **Appendix A - Hold code mapping** 

|**HRC**|**Mnemonic**|**Tier**|**Copy key**|**Client action permitted**|
|---|---|---|---|---|
|HRC-01|DUP_SUSPECT|C|COPY-HOLD-DUP-01|Yes - digital attestation (confirm / cancel) with step-up auth (CTRL-PAY-031)|
|HRC-02|CALLBACK_REQUIRED|C|COPY-HOLD-CB-01|No in-channel confirmation. Client may request callback; verification only via|
|||||callback to contact on file (CTRL-PAY-018)|
|HRC-03|LIMIT_EXCEEDED|C|COPY-HOLD-LIM-01|Client admin secondary approval or RM limit request|

Crestline National Bank  |  POL-FCC-014  v3.2  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed

<!-- page 3 -->

**CRESTLINE NATIONAL BANK** |  Financial Crimes Compliance 

**INTERNAL - CONFIDENTIAL** 

|**HRC**|**Mnemonic**|**Tier**|**Copy key**|**Client action permitted**|
|---|---|---|---|---|
|HRC-04|CUTOFF_WAREHOUSED|P|COPY-STAT-WH-01|None needed (informational)|
|HRC-05|FUNDS_PENDING|C|COPY-HOLD-FUND-01|Fund account; auto-retry until 5:30 p.m. ET|
|HRC-06|REPAIR_REQUIRED|C|COPY-HOLD-RPR-01|Cancel and resubmit with corrected beneficiary data (no in-place edit)|
|HRC-07|FRAUD_MODEL_HIGH|R|COPY-HOLD-GEN-01|None|
|HRC-08|ATO_SUSPECT|R|COPY-HOLD-GEN-01|None|
|HRC-09|SANCTIONS_REVIEW|R|COPY-HOLD-GEN-01|None|
|HRC-10|AML_REVIEW|R|COPY-HOLD-GEN-01|None|
|HRC-11|LEGAL_HOLD|R|COPY-HOLD-GEN-01|None|
|HRC-12|OPS_MANUAL_REVIEW|G|COPY-HOLD-GEN-01|None|

## **Appendix B - Approved copy library (excerpt)** 

|**Copy key**|**Approved text**|
|---|---|
|COPY-HOLD-GEN-01|This wire is being reviewed. No action is needed from you at this time. For questions, contact Treasury Support.|
|COPY-HOLD-DUP-01|This wire appears similar to another recent wire. Please confirm whether you intend to send both.|
|COPY-HOLD-CB-01|We will contact an authorized person at your company to verify this wire. You can request a call back.|
|COPY-HOLD-LIM-01|This wire exceeds a limit on your account. An administrator can approve it or contact your relationship manager.|
|COPY-HOLD-FUND-01|This wire is waiting for available funds. It will be retried until 5:30 p.m. ET.|
|COPY-HOLD-RPR-01|Additional beneficiary information is required. Please cancel and resubmit this wire with complete details.|
|COPY-STAT-WH-01|This wire is scheduled for the next business day.|

## **Appendix C - Prohibited terms in client-facing copy** 

fraud; suspicious; sanctions; OFAC; watch list; screening hit; AML; compliance review; investigation; flagged; security alert; risk score; law enforcement; blocked (except Sanctions Operations correspondence). 

Crestline National Bank  |  POL-FCC-014  v3.2  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed