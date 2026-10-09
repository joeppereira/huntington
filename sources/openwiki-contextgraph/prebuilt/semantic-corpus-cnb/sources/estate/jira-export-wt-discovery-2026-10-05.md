<!-- source: raw/estate/Jira_Export_WT-discovery_2026-10-05.pdf | converted by tools/convert_cnb_corpus.py -->
# Jira Export WT-discovery 2026-10-05


<!-- page 1 -->

|  Jira Cloud - cnb.atlassian.net 

**INTERNAL - CONFIDENTIAL** 

# **Jira Export - Wire Center & Dependency Team Backlog** 

Saved filter 'WT-discovery': projects CBO, PPH, PNG, GTSI, FCT, ENS, TDA - wire-related items updated since 2024-01-01 

|**Document ID**|JIRA-EXP-2026-10-05|
|---|---|
|**Version / Status**|export / Snapshot|
|**Document owner**|Exported by Marcus Chen (Product Owner, CBO Wire Center)|
|**Approver(s)**|n/a|
|**Effective / Last reviewed**|Exported 2026-10-05 08:14 ET|
|**Classification**|INTERNAL - CONFIDENTIAL|
|**Related documents**|CBO-ARCH-WC-4.1; PPH-API-CAT-2026.3; PRSP-HMS-3.4|

## **1. Issue list** 

|**Key**|**Type**|**Summary**|**Status**|**Sprint / target**|**Pts**<br>**Assignee / owner**|**Labels**|**Links**|**Updated**|
|---|---|---|---|---|---|---|---|---|
|**CBO-3120**|Epic|Wire Status Lite pilot - auto-refreshing wire status|Closed (Won't Do)|2024-Q2|55<br>Tom Becker|wire-center; pilot|is caused by INC-2024-1182;<br>documented in PIR-2024-07|2024-07-19|
|**CBO-3790**|Epic|ACH Payment Tracker (timeline + status notifications)|Done|R25.4 (2025-11)|89<br>Marcus Chen|ach; tracker|relates to CBO-3802, CBO-3815;<br>ENS event<br>TRS.ACH.STATUS_CHANGED|2025-11-21|
|**CBO-3802**|Story|Aurora DS: reusable <cbo-journey-timeline> component|Done|R25.3|13<br>Lucas Ferreira|design-system;<br>reusable|child of CBO-3790|2025-09-12|
|**CBO-3815**|Story|Status Projection Service (SPS) - ACH lifecycle consumer|Done|R25.3|21<br>Arjun Mehta|platform; kafka|child of CBO-3790; implements<br>ADR-PAY-019|2025-10-03|
|**CBO-4302**|Story|Wire activity list - filters by rail, status, date range|Done|R26.3|8<br>Jason Park|wire-center|-|2026-06-12|
|**CBO-4355**|Story|Wire detail - display Fed reference (IMAD)|Done|R26.4|3<br>Jason Park|wire-center|-|2026-07-17|
|**CBO-4388**|Story|Show hold reason tooltip on 'Pending Review' wires|In Progress|Sprint 26.20 (ends<br>2026-10-16)|5<br>Jason Park|wire-center;<br>ux-quickwin|requested via TSC feedback (call<br>deflection)|2026-10-02|
|**CBO-4402**|Story|Map PPH v1 status PROCESSED to client label 'Completed'|Done|R26.1 (2026-02)|2<br>Jason Park|wire-center; labels|-|2026-02-06|
|**CBO-4419**|Bug|Client complaint: wire showed 'Completed' then<br>returned/rejected|Open|Backlog|Tom Becker|wire-center;<br>complaint|relates to CMP-2026-1189|2026-09-29|
|**CBO-4471**|Epic|Migrate Wire Center from PPH v1 to PPH v2 APIs|Backlog<br>(unscheduled)|Must complete before<br>2027-03-31 v1 sunset|34<br>Tom Becker|wire-center;<br>tech-debt|blocks nothing; depends on CES<br>account-filter mapping<br>(CBO-4473); tracked in PPH-2190|2026-08-30|
|**CBO-4473**|Story|CES: account-filter mapping for PPH v2 search (clientId +<br>entitled accounts)|Backlog|-|8<br>Arjun Mehta|platform;<br>entitlements|blocks CBO-4471|2026-08-30|
|**CBO-4480**|Spike|International wire status visibility (gpi) for clients|To Do|Backlog|3<br>Lucas Ferreira|wire-center; gpi|-|2026-05-14|
|**CBO-4495**|Story|Incoming wire notification - include remitter name|Backlog|-|5<br>Jason Park|wire-center; ens|-|2026-07-02|
|**CBO-4522**|Story|Wire Center WCAG 2.1 AA remediation|In Progress|Sprint 26.20|8<br>Mei Tanaka|a11y|-|2026-10-01|

Crestline National Bank  |  JIRA-EXP-2026-10-05  vexport  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed

<!-- page 2 -->

|  Jira Cloud - cnb.atlassian.net 

**INTERNAL - CONFIDENTIAL** 

|**Key**|**Type**|**Summary**|**Status**|**Sprint / target**|**Pts**<br>**Assignee / owner**|**Labels**|**Links**|**Updated**|
|---|---|---|---|---|---|---|---|---|
|**PPH-2190**|Epic|PPH v1 API sunset - consumer migration tracking|In Progress|Sunset 2027-03-31|Kevin O'Brien|api-lifecycle|consumers: IVR (migrated), CRM<br>(in progress), cbo-wire-bff (NOT<br>started)|2026-09-22|
|**PPH-2207**|Story|v2: add rail-specific settlement object (fedSettlementTs<br>from pacs.002/OMAD; settlementStatus)|Backlog (no sponsor)|-|8<br>Sunita Rao|api-v2|consumes net.fedwire.ack.v1|2026-04-11|
|**PPH-2251**|Story|v2 search: index beneficiary name (contains / prefix)|Backlog|-|13<br>Sunita Rao|api-v2;<br>performance|-|2026-06-03|
|**PPH-2266**|Story|Publish ISO return reason (pacs.004) on<br>pay.wire.lifecycle.v2|Done|2026-08|5<br>Sunita Rao|events|-|2026-08-21|
|**PNG-1544**|Story|Increase gpi Tracker batch frequency 4h -> 2h|Won't Do|-|5<br>Raj Malhotra|gpi|quota; superseded by GTSI-0107|2026-03-03|
|**GTSI-0107**|Initiative|gpi Tracker Real-Time Service (GTRS) - change-feed based<br>internal API|Planned|Discovery 2027-Q2;<br>build 2027-Q3/Q4|Elena Vasquez|gpi; roadmap|-|2026-09-15|
|**GTSI-0112**|Epic|Knowledge transfer: gpi Connector & Swift API gateway<br>from PNE to GTSI|In Progress|Target 2026-12-15|Omar Siddiqui|re-org|per CNB-MEMO-2026-09|2026-09-30|
|**GTSI-0115**|Story|Swift gpi Tracker API contract renewal (quota 250k<br>calls/month; renewal 2027-01-31)|To Do|-|Omar Siddiqui|vendor|-|2026-09-30|
|**FCT-1893**|Story|Client-Safe Hold Status Facade (GET<br>/holds/{id}/client-view)|Backlog (deprioritized<br>2025-Q3)|-|21<br>Daniel Kowalski|hms; channels|-|2025-08-19|
|**FCT-1951**|Epic|Duplicate-suspect client attestation pilot (via Service<br>Center phone)|Done|2026-04|18<br>Grace Mensah|hms; pilot|updated CTRL-PAY-031|2026-06-10|
|**FCT-2004**|Risk|PPH v1 holdReasonDesc exposes HMS free-text to channel<br>consumers|Open|-|Daniel Kowalski|security-review;<br>data-leakage|identified in FCT security review<br>2026-05|2026-05-27|
|**ENS-1120**|Initiative|Entity-level subscriptions (subscribe to a specific<br>paymentId / caseId)|Planned|2027-H1|Melissa Grant|subscriptions|-|2026-07-30|
|**TDA-2140**|Story|Feature table wire_corridor_stats_daily (currency/country<br>completion stats)|Done|2026-05|8<br>Dr. Aisha Rahman|features|used by Ops dashboards|2026-05-22|
|**TDA-2188**|Story|gpi_tracker_events: move load from nightly to hourly|In Progress|Target 2026-11|5<br>Carlos Mendes|gpi; latency|-|2026-09-25|
|**TDA-2210**|Story|Ingest net.fedwire.ack.v1 (Fed acceptance / OMAD) into<br>TDIP|Backlog|-|8<br>Carlos Mendes|fedwire|needs Kafka ACL from PNE|2026-04-18|

## **2. Issue details (selected)** 

### **CBO-4388 - Show hold reason tooltip on 'Pending Review' wires** 

**Type:** Story **Status:** In Progress **Target:** Sprint 26.20 (ends 2026-10-16) **Points:** 5 **Assignee/owner:** Jason Park **Links:** requested via TSC feedback (call deflection) 

**Description:** Populate tooltip from PPH v1 field holdReasonDesc so clients understand why a wire is pending. AC: tooltip text = holdReasonDesc (truncate at 120 chars); fallback 'Under review'. 

_Comment 2026-09-30 - Mei Tanaka:_ UAT sample tooltips: 'Possible duplicate of PPH260924...'; 'CALLBACK REQ - new bene acct'; 'FRAUD_MODEL_HIGH sc=9xx L1 queue'; 'SANCTIONS_REVIEW name match 0.91 L2'. Long text truncated at 120 chars - AC met. 

_Comment 2026-10-01 - Jason Park:_ Merged to release/26.21. Feature flag WC_HOLD_TOOLTIP default ON for R26.21 (prod 2026-10-22). 

_Comment 2026-10-02 - Kim Nguyen:_ Great - this should reduce 'why is my wire pending' calls. 

### **CBO-4402 - Map PPH v1 status PROCESSED to client label 'Completed'** 

Crestline National Bank  |  JIRA-EXP-2026-10-05  vexport  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed

<!-- page 3 -->

|  Jira Cloud - cnb.atlassian.net 

**INTERNAL - CONFIDENTIAL** 

**Type:** Story **Status:** Done **Target:** R26.1 (2026-02) **Points:** 2 **Assignee/owner:** Jason Park **Links:** - 

**Description:** Replace legacy label 'Processed' with 'Completed' per client feedback that 'Processed' was unclear. 

_Comment 2026-02-04 - Marcus Chen:_ Clients find 'Processed' confusing; 'Completed' tested better in a 6-client survey. 

### **CBO-4419 - Client complaint: wire showed 'Completed' then returned/rejected** 

**Type:** Bug **Status:** Open **Target:** Backlog **Points:** - **Assignee/owner:** Tom Becker **Links:** relates to CMP-2026-1189 

**Description:** International wire showed 'Completed' at release; beneficiary bank rejected (RJCT AC04) next day. Client shipped goods. Root cause TBD. 

_Comment 2026-09-29 - Kim Nguyen:_ Linked complaint CMP-2026-1189 (Halvorsen Industrial Supply). EUR 412,600 wire shown 'Completed' on 2026-09-16 10:42 ET; beneficiary bank rejected 2026-09-17 (RJCT AC04). Funds returned 2026-09-21. Client released goods on 09-16. 

### **CBO-4471 - Migrate Wire Center from PPH v1 to PPH v2 APIs** 

**Type:** Epic **Status:** Backlog (unscheduled) **Target:** Must complete before 2027-03-31 v1 sunset **Points:** 34 **Assignee/owner:** Tom Becker **Links:** blocks nothing; depends on CES account-filter mapping (CBO-4473); tracked in PPH-2190 

**Description:** Replace /pph/v1 calls in cbo-wire-bff with /pph/v2. Est. 34 pts. Not yet prioritized against feature work. 

_Comment 2026-08-30 - Tom Becker:_ Sizing 34 pts assumes reuse of existing list/detail UI; excludes any new tracking features. Needs CBO-4473 first. Not yet in PI 26.4 or PI 27.1 draft. 

### **CBO-4480 - International wire status visibility (gpi) for clients** 

**Type:** Spike **Status:** To Do **Target:** Backlog **Points:** 3 **Assignee/owner:** Lucas Ferreira **Links:** - 

**Description:** gpi status today only visible to Ops in IWB. Contact: Payment Networks Engineering (Raj Malhotra) for API options. 

_Comment 2026-05-14 - Lucas Ferreira:_ gpi status lives only in Ops IWB. Will reach out to Raj Malhotra (PNE) about an API. 

### **CBO-3815 - Status Projection Service (SPS) - ACH lifecycle consumer** 

**Type:** Story **Status:** Done **Target:** R25.3 **Points:** 21 **Assignee/owner:** Arjun Mehta **Links:** child of CBO-3790; implements ADR-PAY-019 

**Description:** Kafka consumer -> Postgres read model -> /cbo/sps/v1 API. Designed to add new payment types via config + mapping module. 

_Comment 2025-10-03 - Arjun Mehta:_ SPS is payment-type agnostic: add a topic subscription + mapping module per type. Wire would need ACL on pay.wire.lifecycle.v2 and a mapping from v2 lifecycleState to client milestones. 

### **PPH-2207 - v2: add rail-specific settlement object (fedSettlementTs from pacs.002/OMAD; settlementStatus)** 

**Type:** Story **Status:** Backlog (no sponsor) **Target:** - **Points:** 8 **Assignee/owner:** Sunita Rao **Links:** consumes net.fedwire.ack.v1 

**Description:** v2 stateHistory NETWORK_ACCEPTED timestamp is PPH processing time, not Fed receipt time. Add settlement{status, fedSettlementTs, omad}. Needs product sponsor. _Comment 2026-04-11 - Sunita Rao:_ Without this, consumers can only approximate Fed settlement time from stateHistory (PPH processing time). Needs a product sponsor to enter Demand Board. _Comment 2026-06-20 - Laura Kim:_ No consuming product identified yet - parking. 

### **PPH-2190 - PPH v1 API sunset - consumer migration tracking** 

**Type:** Epic **Status:** In Progress **Target:** Sunset 2027-03-31 **Points:** - **Assignee/owner:** Kevin O'Brien **Links:** consumers: IVR (migrated), CRM (in progress), cbo-wire-bff (NOT started) **Description:** v1 adapter is not supported on Volaris 9.6 (upgrade April 2027). No extensions (ARB 2026-09-08). 

_Comment 2026-09-22 - Kevin O'Brien:_ Reminder sent to CBO Wire Center (3rd). ARB 2026-09-08: no extension beyond 2027-03-31. 

### **FCT-1893 - Client-Safe Hold Status Facade (GET /holds/{id}/client-view)** 

**Type:** Story **Status:** Backlog (deprioritized 2025-Q3) **Target:** - **Points:** 21 **Assignee/owner:** Daniel Kowalski **Links:** - 

Crestline National Bank  |  JIRA-EXP-2026-10-05  vexport  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed

<!-- page 4 -->

|  Jira Cloud - cnb.atlassian.net 

**INTERNAL - CONFIDENTIAL** 

**Description:** Return disclosure tier + approved copy key per POL-FCC-014 Appendix A; never return HRC or analyst notes. 

_Comment 2025-08-19 - Grace Mensah:_ Deprioritized - no channel consumer committed. Revisit when a client-facing hold experience is funded. 

### **FCT-1951 - Duplicate-suspect client attestation pilot (via Service Center phone)** 

**Type:** Epic **Status:** Done **Target:** 2026-04 **Points:** 18 **Assignee/owner:** Grace Mensah **Links:** updated CTRL-PAY-031 **Description:** 82% of HRC-01 holds resolved within 30 min with client confirmation. FCT Risk approved digital attestation for HRC-01 only, subject to step-up auth. 

_Comment 2026-06-10 - Grace Mensah:_ CTRL-PAY-031 updated. Digital attestation allowed for HRC-01 only, with step-up auth; amounts > $5M still need Wire Room release. No digital path exists yet. 

### **FCT-2004 - PPH v1 holdReasonDesc exposes HMS free-text to channel consumers** 

**Type:** Risk **Status:** Open **Target:** - **Points:** - **Assignee/owner:** Daniel Kowalski **Links:** identified in FCT security review 2026-05 **Description:** v1 holdReasonDesc is populated from HMS hold description (may include HRC and analyst notes). Consumers must not display. Remediation: remove in v1 or block at gateway. _Comment 2026-05-27 - Daniel Kowalski:_ Raised to PPH (Sunita Rao) and CBO (Tom Becker). Remediation options: stop sync, or redact at API gateway. Pending decision; v1 sunset may make this moot. 

### **GTSI-0107 - gpi Tracker Real-Time Service (GTRS) - change-feed based internal API** 

**Type:** Initiative **Status:** Planned **Target:** Discovery 2027-Q2; build 2027-Q3/Q4 **Points:** - **Assignee/owner:** Elena Vasquez **Links:** - 

**Description:** Internal REST + event API over Swift gpi Tracker change feed. Not funded for 2026. 

_Comment 2026-09-15 - Elena Vasquez:_ Will scope after KT. Interested in early channel requirements to shape discovery. 

### **TDA-2210 - Ingest net.fedwire.ack.v1 (Fed acceptance / OMAD) into TDIP** 

**Type:** Story **Status:** Backlog **Target:** - **Points:** 8 **Assignee/owner:** Carlos Mendes **Links:** needs Kafka ACL from PNE **Description:** Required for settlement-time analytics on domestic wires. Not scheduled. 

_Comment 2026-04-18 - Carlos Mendes:_ Blocked on Kafka ACL from PNE for net.fedwire.ack.v1. No business sponsor yet. 

## **3. Linked records outside Jira** 

|**Record**|**System**|**Summary**|**Status**|
|---|---|---|---|
|CMP-2026-1189|Complaints (Pega)|Client relied on 'Completed' status for international wire later rejected (AC04); requests clarity on what 'Completed'<br>means|Open - Regulatory complaint review pending|
|INC-2024-1182|ServiceNow|PPH v1 thread-pool exhaustion caused by Wire Status Lite polling (month-end)|Closed - see PIR-2024-07|

Crestline National Bank  |  JIRA-EXP-2026-10-05  vexport  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed