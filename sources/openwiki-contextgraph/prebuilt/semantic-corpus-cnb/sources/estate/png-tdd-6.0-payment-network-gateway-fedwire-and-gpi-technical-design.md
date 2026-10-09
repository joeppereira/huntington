<!-- source: raw/estate/PNG-TDD-6.0_Payment_Network_Gateway_Fedwire_and_gpi_Technical_Design.pdf | converted by tools/convert_cnb_corpus.py -->
# PNG-TDD-6.0 Payment Network Gateway Fedwire and gpi Technical Design


<!-- page 1 -->

|  Payments & Treasury Technology 

**INTERNAL - CONFIDENTIAL** 

# **Payment Network Gateway - Fedwire Funds Connector & Swift gpi Integration: Technical Design** 

Network connectivity, ISO 20022 message handling, acknowledgments and gpi Tracker integration 

|**Document ID**|PNG-TDD-6.0|
|---|---|
|**Version / Status**|6.0 (+ Addendum A) / Approved|
|**Document owner**|Payment Networks Engineering - Raj Malhotra (Director); Chen Wei (Fedwire); Tomasz Nowak (gpi)|
|**Approver(s)**|Raj Malhotra; Nikhil Bose (ARB)|
|**Effective / Last reviewed**|v6.0 2025-11-14; Addendum A 2026-03-03|
|**Classification**|INTERNAL - CONFIDENTIAL|
|**Related documents**|PPH-SYS-OVW-9.2; PPH-API-CAT-2026.3; PNG-1544|

## **1. Scope and ownership** 

This design covers both modules of the Payment Network Gateway, owned and operated by **Payment Networks Engineering (PNE)** : the **Fedwire Funds Connector (FFC)** and the **Swift Alliance & gpi Connector (GPI-C)** . Support: PNE on-call (T1), #payment-networks. gpi Tracker questions: Tomasz Nowak. 

## **2. Fedwire Funds Connector (SYS-PNG-FFC)** 

### **2.1 Connectivity and formats** 

- FedLine Direct (dual MQ channels, primary Columbus / contingency Charlotte). 

- ISO 20022 since the Federal Reserve's single-day implementation on **2025-07-14** (legacy FAIM retired). 

- Outbound: pacs.008 (customer transfer), pacs.009 (FI transfer), pacs.004 (return), camt.056 (return request), camt.110 (investigation). 

- Inbound: pacs.008 / pacs.009 / pacs.004 (published to net.fedwire.inbound.v1), pacs.002 positive and negative acknowledgments, admi.002 technical/business errors. 

### **2.2 Acknowledgment handling** 

For each accepted value message the Federal Reserve returns a **pacs.002** containing the OMAD and a creation timestamp. FFC publishes these to **net.fedwire.ack.v1** (EV-PNG-01). Errors (admi.002) are published with the IMAD reference. Acceptance by the Fedwire Funds Service constitutes final settlement between the sending and receiving banks under Regulation J. The Federal Reserve does not report credit to the beneficiary's account at the receiving bank. 

|**Metric (Q3-2025)**|**Value**|
|---|---|
|Median Fed acknowledgment latency (send to pacs.002)|4.2 s|
|Median PPH RELEASED to Fed acceptance (incl. queueing)|6 min|
|Fed technical/business rejects (admi.002 / negative pacs.002)|0.07% of messages|

### **2.3 Topic access** 

|**Topic**|**Producer**|**Authorized consumers**|**ACL owner**|
|---|---|---|---|
|net.fedwire.ack.v1|FFC|PPH|PNE|
|net.fedwire.inbound.v1|FFC|PPH|PNE|

## **3. Swift Alliance & gpi Connector (SYS-PNG-GPI)** 

### **3.1 Messaging** 

Crestline National Bank  |  PNG-TDD-6.0  v6.0 (+ Addendum A)  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed

<!-- page 2 -->

|  Payments & Treasury Technology 

**INTERNAL - CONFIDENTIAL** 

- Swift CBPR+ ISO 20022 pacs.008 mandatory for customer credit transfers from **2025-11-22** (end of MT/MX coexistence); MT103 contingency conversion is not used by CNB. 

- UETR assigned by PPH at release (UUID v4) and carried in pacs.008; GPI-C maps Swift ACK/NAK to PPH. 

- Exceptions & investigations moving to camt.110/camt.111 (Swift timeline November 2026). 

### **3.2 gpi Tracker integration (current)** 

GPI-C retrieves gpi Tracker updates via the Swift API through the Swift Microgateway using SwiftNet PKI credentials bound to the GPI-C service account. Integration is **batch** : every 4 hours (00:00, 04:00, 08:00, 12:00, 16:00, 20:00 ET) GPI-C requests changed payment transactions for outbound UETRs from the last 30 days and upserts results into the Oracle table **GPI_TRACKER_SNAPSHOT** . 

|**Column**|**Description**|
|---|---|
|UETR|Tracking id (join key to PPH v2 identifiers.uetr)|
|LAST_STATUS / LAST_REASON|ACSP/ACCC/RJCT and G000-G004 or ISO reject reason|
|ROUTE_JSON|Ordered agents (BIC, name, country, received/forwarded timestamps)|
|DEDUCTED_CHARGES_JSON|Charges deducted per agent (amount, currency) when reported|
|CONFIRMED_AMOUNT / CREDIT_TS|Amount and timestamp reported with ACCC|
|SNAPSHOT_TS|Time GPI-C captured the update|

Consumers: Payment Operations' Investigations Workbench (IWB) and the TDIP nightly load (gpi_tracker_events). **There is no internal API** for gpi status. The snapshot table must not be exposed directly to channels; a client-facing capability requires a dedicated service with its own SLA, entitlement checks and quota management. 

### **3.3 Tracker API quota** 

The Swift Tracker API contract permits **250,000 calls per month** (renewal 2027-01-31). Current usage is ~61% (batch pulls plus Ops ad-hoc lookups). Per-payment lookups from client channels were estimated at ~1.9 million calls/month (2,900 outbound international wires per day with repeated client views) and would exceed the contract by ~7x. Any real-time design must use a change-feed with internal fan-out rather than per-payment calls. 

### **3.4 gpi statuses handled** 

|**Status / reason**|**Meaning**|**Tracking implication**|
|---|---|---|
|ACSP / G000|Forwarded to next gpi agent|Further updates expected|
|ACSP / G001|Forwarded to a non-gpi agent|No further updates will follow - tracking ends at the last<br>gpi agent|
|ACSP / G002|Credit may not be confirmed same day|Update expected|
|ACSP / G003|Pending - awaiting documents from creditor|Update expected|
|ACSP / G004|Pending - awaiting cover funds|Update expected|
|ACCC|Credited to beneficiary account|Terminal; credit timestamp and confirmed amount<br>available|
|RJCT + reason (e.g., AC01, AC04,<br>RR05)|Rejected by an agent|Terminal; return expected via pacs.004|

### **3.5 Observed outcomes (outbound, Q3-2025)** 

|**Outcome**|**Share**|
|---|---|
|Final status ACCC (beneficiary credited)|88%|
|Last status ACSP/G001 (tracking ended at non-gpi agent)|8%|
|Pending > 24 h (G002/G003/G004)|2.5%|
|RJCT|1.5%|
|Median release-to-ACCC (all corridors)|2 h 41 min|
|Wires with at least one intermediary deduction reported (SHAR/CRED)|34%|

Crestline National Bank  |  PNG-TDD-6.0  v6.0 (+ Addendum A)  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed

<!-- page 3 -->

|  Payments & Treasury Technology 

**INTERNAL - CONFIDENTIAL** 

## **4. Operations** 

- Change windows: Saturday 22:00-02:00 ET. 

- Monitoring: Splunk dashboards PNG-FFC-*, PNG-GPI-*. 

- Business continuity: FedLine Advantage contingency; Swift Alliance Lite2 standby. 

## **Addendum A (2026-03-03) - PNG-1544 decision** 

The request to increase gpi batch frequency from 4 hours to 2 hours (PNG-1544) was declined: projected Tracker API usage would exceed the contracted quota. A change-feed based internal service is recommended as a future initiative. 

Crestline National Bank  |  PNG-TDD-6.0  v6.0 (+ Addendum A)  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed