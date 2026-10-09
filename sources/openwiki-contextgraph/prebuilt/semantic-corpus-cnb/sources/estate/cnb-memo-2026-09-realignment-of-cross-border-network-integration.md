<!-- source: raw/estate/CNB-MEMO-2026-09_Realignment_of_Cross-Border_Network_Integration.pdf | converted by tools/convert_cnb_corpus.py -->
# CNB-MEMO-2026-09 Realignment of Cross-Border Network Integration


<!-- page 1 -->

|  Office of the CIO 

**INTERNAL** 

# **Organizational Announcement: Realignment of Cross-Border Network Integration** 

From: Gregory Hall, MD - CIO Payments & Treasury Technology | To: PTT Leadership, Treasury Management Products, Payment Operations 

|**Document ID**|CNB-MEMO-2026-09|
|---|---|
|**Version / Status**|1.0 / Issued|
|**Document owner**|Office of the CIO, Payments & Treasury Technology|
|**Approver(s)**|Gregory Hall|
|**Effective / Last reviewed**|Issued 2026-09-02; effective 2026-10-01|
|**Classification**|INTERNAL|
|**Related documents**|CNB-ORG-PTT-2026-06 (to be refreshed Q4); GTSI-0112|

### Team, 

As cross-border volumes grow and Swift's ISO 20022 roadmap continues beyond the end of MT/MX coexistence, we are consolidating our cross-border network capabilities under one leader. Effective **October 1, 2026** , the following changes take effect. 

## **1. What is moving** 

|**Capability**|**From**|**To**|**Accountable leader**|
|---|---|---|---|
|Swift Alliance Gateway, gpi Connector (SYS-PNG-GPI)<br>and gpi Tracker integration|Payment Networks Engineering<br>(Raj Malhotra)|Global Transaction Services<br>Integration (Elena Vasquez)|Omar Siddiqui (EM); Hannah<br>Lindqvist (Tech Lead)|
|Swift API gateway (Microgateway), SwiftNet PKI|Payment Networks Engineering|GTSI|Hannah Lindqvist|
|service accounts||||
|International wire tracking roadmap (incl. any|Payment Networks Engineering|GTSI|Elena Vasquez; business|
|client-facing gpi capability)|||sponsor Laura Kim|

## **2. What is not moving** 

- The **Fedwire Funds Connector (SYS-PNG-FFC)** , including the net.fedwire.ack.v1 and net.fedwire.inbound.v1 topics, remains with Payment Networks Engineering under Raj Malhotra (Brian Walsh, EM). 

- Raj Malhotra additionally assumes ownership of the FedNow and RTP connectors from 2026-11-01. 

## **3. People changes** 

- Tomasz Nowak (Senior Engineer, gpi Connector) transfers to GTSI and reports to Omar Siddiqui. 

- PNE on-call remains secondary support for SYS-PNG-GPI until **2026-12-15** , when knowledge transfer (GTSI-0112) completes. 

## **4. How to engage** 

From October 1, all new requests for gpi data, Swift Tracker usage, or international wire status capabilities should be raised in Jira project **GTSI** and directed to Omar Siddiqui. Requests already logged against PNE (project PNG) will be triaged by GTSI during knowledge transfer; please do not open new PNG tickets for gpi topics. The PTT Organization & Ownership Directory (CNB-ORG-PTT-2026-06) will reflect these changes in its Q4 refresh. 

## **5. Roadmap note** 

GTSI will own the gpi Tracker Real-Time Service initiative (GTSI-0107). It is not funded for 2026; discovery is planned for 2027-Q2 subject to the 2027 portfolio review. Teams with near-term needs for gpi data should engage GTSI early so requirements can inform discovery. GTSI is also responsible for the Swift Tracker API contract renewal due 2027-01-31 (GTSI-0115). 

Thank you to Raj and the PNE team for building and running these services, and to Elena's team for taking them forward. 

### **Gregory Hall** 

Managing Director, CIO Payments & Treasury Technology 

Crestline National Bank  |  CNB-MEMO-2026-09  v1.0  |  INTERNAL  |  Uncontrolled when printed