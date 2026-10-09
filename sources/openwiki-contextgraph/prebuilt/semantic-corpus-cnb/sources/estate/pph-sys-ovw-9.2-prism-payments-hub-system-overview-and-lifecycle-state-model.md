<!-- source: raw/estate/PPH-SYS-OVW-9.2_PRISM_Payments_Hub_System_Overview_and_Lifecycle_State_Model.pdf | converted by tools/convert_cnb_corpus.py -->
# PPH-SYS-OVW-9.2 PRISM Payments Hub System Overview and Lifecycle State Model


<!-- page 1 -->

|  Payments & Treasury Technology 

**INTERNAL - CONFIDENTIAL** 

# **PRISM Payments Hub - System Overview & Wire Lifecycle State Model** 

Wire orchestration platform for all CNB channels and rails (Fedwire, Swift CBPR+, book transfer) 

|**Document ID**|PPH-SYS-OVW-9.2|
|---|---|
|**Version / Status**|9.2 / Approved|
|**Document owner**|Sunita Rao (Principal Engineer) / Kevin O'Brien (EM), Payments Hub Engineering|
|**Approver(s)**|Raymond Ortiz (Director); Laura Kim (Payments Platform Product)|
|**Effective / Last reviewed**|Last reviewed 2026-05-30|
|**Classification**|INTERNAL - CONFIDENTIAL|
|**Related documents**|PPH-API-CAT-2026.3; PNG-TDD-6.0; PRSP-HMS-3.4; ADR-PAY-021; ADR-PAY-023|

## **1. Overview** 

PRISM Payments Hub (PPH) is CNB's wire orchestration platform, built on the **Volaris Payment Platform 9.4** (vendor) and operated on-premises in an active-active configuration across the Columbus and Charlotte data centers. PPH receives payment instructions from all channels, validates and enriches them, coordinates screening and holds with the Payment Risk & Screening Platform (PRSP), performs funds control against the Core Deposit Platform (CDP), and routes to the Payment Network Gateway (Fedwire Funds Connector or Swift Alliance/gpi Connector). 

|**Dimension**|**Value (Q2-2026 average per business day)**|
|---|---|
|Outgoing domestic wires (Fedwire)|14,200|
|Outgoing international wires (Swift CBPR+)|2,900|
|Incoming wires (all rails)|18,500|
|Book transfers|6,300|
|Channels|CBO (~67% of outgoing), host-to-host files, Swift for Corporates (MT101/pain.001), branch, Ops desk|
|Availability target|99.95% during Fedwire operating hours|
|Vendor roadmap|Volaris 9.6 upgrade scheduled April 2027 (removes legacy v1 API adapter)|

## **2. Processing stages** 

1. **Intake** - channel submits instruction (v1 or v2 API, file, Swift). 

2. **Validation & enrichment** - format, routing (ABA/BIC), ISO 20022 mapping, structured address checks (mandatory for Swift CBPR+ and Fedwire from November 2026). 

3. **Screening** - synchronous call to PRSP (SanctionScreen + Sentinel). A hit creates an HMS hold and the payment enters HELD. 

4. **Funds control** - memo debit against CDP; insufficient funds create HRC-05 holds with auto-retry until 5:30 p.m. ET. 

5. **Release** - UETR assigned (all outbound wires since ADR-PAY-023), message built (pacs.008 / pacs.009). 

6. **Network** - sent to Fedwire Funds Connector or Swift Alliance/gpi Connector; acknowledgment updates state. 

7. **Close** - accounting close (COMPLETED); later returns (pacs.004) transition to RETURNED. 

## **3. Canonical lifecycle states (v2)** 

|**State**|**Meaning**|**Typical duration**|**v1 status shown to consumers**|
|---|---|---|---|
|RECEIVED|Instruction accepted by PPH|< 1 s|RECEIVED|
|VALIDATING|Format/routing/enrichment|1-5 s|PENDING|
|SCREENING|PRSP screening in progress|1-20 s|PENDING|
|HELD|One or more HMS holds open|minutes-days|HELD|
|REPAIR|Wire Room repair queue|minutes-hours|PENDING|

Crestline National Bank  |  PPH-SYS-OVW-9.2  v9.2  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed

<!-- page 2 -->

|  Payments & Treasury Technology 

**INTERNAL - CONFIDENTIAL** 

|**State**|**Meaning**|**Typical duration**|**v1 status shown to consumers**|
|---|---|---|---|
|FUNDS_CONTROL|Awaiting available balance|seconds-hours|PENDING|
|WAREHOUSED|Future-dated or after cutoff|until value date|PENDING|
|RELEASED|Released for transmission, UETR assigned|seconds|PROCESSED|
|SENT_TO_NETWORK|Message delivered to network gateway|seconds-minutes|PROCESSED|
|NETWORK_ACCEPTED|Network acknowledgment received (rail-specific, see 4)|-|PROCESSED|
|NETWORK_REJECTED|Network rejected (admi.002 / pacs.002 RJCT / NAK)|-|REJECTED|
|COMPLETED|Internal accounting close|end of day|PROCESSED|
|CANCELLED|Cancelled before release|-|CANCELLED|
|RETURNED|Funds returned (pacs.004) after release|hours-days|RETURNED|

### **Note on v1 status PROCESSED** 

v1 collapses RELEASED, SENT_TO_NETWORK, NETWORK_ACCEPTED and COMPLETED into a single value PROCESSED. Consumers of v1 cannot distinguish a wire that has merely been released from one acknowledged by the network. 

## **4. Rail-specific meaning of NETWORK_ACCEPTED** 

|**Rail**|**Acknowledgment source**|**Business meaning**|**Finality**|
|---|---|---|---|
|Fedwire Funds|Federal Reserve pacs.002 positive<br>acknowledgment carrying OMAD (via<br>net.fedwire.ack.v1)|Payment order accepted and settled by the<br>Federal Reserve; funds credited to the<br>receiving bank's master account|Final and irrevocable interbank settlement<br>(Regulation J / UCC Article 4A). Does not<br>confirm credit to the beneficiary's account.|
|Swift CBPR+|SwiftNet delivery acknowledgment (ACK)<br>for pacs.008|Message accepted by the Swift network for<br>delivery to the next agent|No settlement implication. Settlement<br>occurs through correspondent<br>(nostro/vostro) accounts; beneficiary credit<br>is known only from gpi ACCC (if available).|

The v2 stateHistory timestamp for NETWORK_ACCEPTED is the time PPH processed the acknowledgment, not the Federal Reserve's creation timestamp in pacs.002. The authoritative Fed timestamp and OMAD are carried on net.fedwire.ack.v1 (see PPH-2207). 

## **5. Identifiers** 

|**Identifier**|**Assigned by**|**Scope**|**Available in**|
|---|---|---|---|
|pphId|PPH|Internal payment key|v1, v2, events|
|cboRef|CBO|Channel reference|v2 identifiers.cboRef (if channel = CBO)|
|IMAD|PPH (Fedwire sender)|Fedwire input message|v1 fedRef; v2 identifiers.imad|
|OMAD|Federal Reserve|Fedwire output message (acceptance)|v2 identifiers.omad; net.fedwire.ack.v1|
|UETR|PPH at release|End-to-end tracking id (Swift gpi; carried on Fedwire<br>pacs.008)|v2 identifiers.uetr; lifecycle v2 events|
|EndToEndId|Originator / PPH|Client reference passed through|v2|

## **6. Integration with Hold Management (PRSP-HMS)** 

When screening or funds control raises a hold, HMS returns a holdId and PPH transitions the payment to HELD. Since the 2019 integration, PPH also synchronizes the HMS hold _description_ into the legacy v1 field **holdReasonDesc** for backward compatibility with the Wire Room console. The v2 API exposes only hold.isHeld and hold.holdId (ADR-PAY-021). 

## **7. Cutoffs and operating windows** 

|**Item**|**Value**|
|---|---|
|Fedwire operating day|9:00 p.m. ET (prior calendar day) to 7:00 p.m. ET|
|Fedwire third-party customer transfer cutoff|6:00 p.m. ET (later items warehoused, HRC-04)|
|CBO same-day wire cutoff (domestic)|5:30 p.m. ET|

Crestline National Bank  |  PPH-SYS-OVW-9.2  v9.2  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed

<!-- page 3 -->

|  Payments & Treasury Technology 

**INTERNAL - CONFIDENTIAL** 

|**Item**|**Value**|
|---|---|
|International cutoffs|By currency (e.g., EUR 2:00 p.m. ET, GBP 1:00 p.m. ET, MXN 3:00 p.m. ET, JPY prior day)|

## **8. Upcoming changes** 

- **November 2026** - structured/hybrid postal address enforcement for Swift CBPR+ and Fedwire; repair holds (HRC-06) expected to rise. 

- **FedNow outbound expansion** - PI 27.1 commitment. 

- **2027-03-31** - PPH v1 API sunset (PPH-2190); **April 2027** - Volaris 9.6 upgrade. 

Crestline National Bank  |  PPH-SYS-OVW-9.2  v9.2  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed