<!-- source: raw/estate/TDIP-CAT-2026.2_Treasury_Data_and_Insights_Platform_Data_Catalog_Extract.pdf | converted by tools/convert_cnb_corpus.py -->
# TDIP-CAT-2026.2 Treasury Data and Insights Platform Data Catalog Extract


<!-- page 1 -->

|  Treasury Data & Analytics 

**INTERNAL - CONFIDENTIAL** 

# **Treasury Data & Insights Platform - Data Catalog Extract (Payments Domain) & Insights API** 

Datasets, feature tables, classifications, ownership, freshness and the Insights serving pattern 

|**Document ID**|TDIP-CAT-2026.2|
|---|---|
|**Version / Status**|2026.2 / Published|
|**Document owner**|Carlos Mendes (EM, Treasury Data Platform); Dr. Aisha Rahman (Lead Data Scientist)|
|**Approver(s)**|Wei Zhang (Director, Treasury Data & Analytics); Ethan Brooks (Data Governance)|
|**Effective / Last reviewed**|Published 2026-09-18|
|**Classification**|INTERNAL - CONFIDENTIAL|
|**Related documents**|DUS-07; MRM-POL-02; ADR-PAY-026; PNG-TDD-6.0|

## **1. Platform overview** 

TDIP runs on Snowflake (Enterprise, US-East) with dbt transformations, a Feast feature store, Amazon SageMaker for model training and batch scoring, and the **Insights API** serving layer (precomputed results in a low-latency store). Access to datasets is governed in Collibra; Restricted datasets require Privacy Office approval (SLA 15 business days). 

## **2. Payments domain datasets** 

|**Dataset**|**Source**|**Refresh**|**History**|**Classification**|**Data owner / steward**|
|---|---|---|---|---|---|
|pay_wire_txn_hist|PPH (CDC)|Hourly|7 yrs|Confidential - Client|Laura Kim / Carlos Mendes|
|gpi_tracker_events|GPI_TRACKER_SNAPSHOT<br>(GPI-C)|Nightly 05:00 ET (hourly from<br>2026-11, TDA-2188)|Since<br>2025-03-01|Confidential - Client|Laura Kim / Carlos Mendes|
|fed_ack_events|net.fedwire.ack.v1|NOT INGESTED (TDA-2210)|-|-|-|
|dda_txn_history|Core Deposit Platform|Daily|7 yrs|Restricted - Client<br>Confidential|Mark Sullivan / Deposits Data<br>Eng.|
|client_hierarchy|CIF + CES|Daily|Current + 2 yrs|Confidential - Client|Marcus Chen / Carlos<br>Mendes|
|cbo_wire_events|CBO clickstream|Hourly|13 months|Internal|Marcus Chen|

Notes: pay_wire_txn_hist.uetr is populated for Swift wires since 2018 and for Fedwire wires since 2025-10 (ADR-PAY-023). Settlement-time analytics for domestic wires require fed_ack_events (TDA-2210, backlog). 

## **3. Feature tables** 

|**Feature table**|**Grain**|**Derived from**|**Classification / permitted purpose**|**MRM link**|
|---|---|---|---|---|
|wire_corridor_stats_daily<br>(TDA-2140)|currency x destination<br>country x day|pay_wire_txn_hist +<br>gpi_tracker_events, all<br>originating clients|Internal - built for Payment Ops dashboards. Contains<br>wire counts, distinct_originating_clients,<br>same_day_accc_rate, median_hours_to_accc. No<br>suppression flag.|None<br>(descriptive)|
|beneficiary_behavior_profile|on-us beneficiary<br>account x day|dda_txn_history +<br>pay_wire_txn_hist (incoming<br>wires to CNB accounts)|Restricted - Client Confidential. Permitted purpose: FCT<br>fraud / mule-detection features only. Includes<br>bene_median_hours_to_outflow,<br>bene_outflow_ratio_24h,<br>bene_new_counterparties_30d.|Input to<br>M-FCT-0034|
|client_wire_history_features|originating client x<br>beneficiary key|pay_wire_txn_hist +<br>gpi_tracker_events|Confidential - Client. Prototype (not productionized):<br>count, median release-to-ACCC, p90, last_seen.|Not registered|

### **3.1 Corridor statistics sample (rolling 90 days to 2026-08-31, outbound Swift)** 

|**Currency / country**|**Wires**|**Distinct originating clients**|**Largest client share**|**Same-day ACCC**|**Median hours to ACCC**|
|---|---|---|---|---|---|
|EUR / DE|31,200|1,140|4%|92%|2.1|

Crestline National Bank  |  TDIP-CAT-2026.2  v2026.2  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed

<!-- page 2 -->

|  Treasury Data & Analytics 

**INTERNAL - CONFIDENTIAL** 

|**Currency / country**|**Wires**|**Distinct originating clients**|**Largest client share**|**Same-day ACCC**|**Median hours to ACCC**|
|---|---|---|---|---|---|
|GBP / GB|18,450|860|6%|94%|1.6|
|CAD / CA|12,900|1,020|5%|90%|2.4|
|MXN / MX|2,950|88|21%|81%|4.9|
|INR / IN|1,730|64|9%|76%|6.2|
|NGN / NG|140|11|38%|52%|19.5|

## **4. Insights API** 

Client-facing analytical outputs are served by the Insights API (ADR-PAY-026). Results are computed in TDIP (batch or micro-batch), published to the serving store and exposed through versioned endpoints with entitlement checks delegated to the calling channel. 

|**ID**|**Endpoint**|**Status**|**Notes**|
|---|---|---|---|
|EP-TDIP-01|GET /tdip/insights/v1/cash-forecast/{clientId}|GA (2025-09)|Model M-TRS-0142; p95 120 ms; reference<br>implementation|
|-|Wire history / corridor insights|Not available|No endpoints exist for wire insights;<br>client_wire_history_features is a prototype|

Onboarding a new insight: (1) MRM inventory registration per MRM-POL-02, (2) data access approvals per DUS-07, (3) serving endpoint build (~13-21 pts typical), (4) DRC approval of client-facing wording and disclaimers. 

## **5. Known gaps** 

- Fed acceptance timestamps not ingested (TDA-2210). 

- gpi data is nightly until TDA-2188 completes (target 2026-11); history begins 2025-03-01. 

- No real-time (sub-minute) serving for wire data; minimum freshness is hourly. 

Crestline National Bank  |  TDIP-CAT-2026.2  v2026.2  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed