<!-- source: raw/estate/DUS-07_v2.1_Data_Use_and_Client_Confidentiality_Standard.pdf | converted by tools/convert_cnb_corpus.py -->
# DUS-07 v2.1 Data Use and Client Confidentiality Standard


<!-- page 1 -->

|  Privacy Office 

**INTERNAL - CONFIDENTIAL** 

# **Data Use & Client Confidentiality Standard (extract)** 

Purpose limitation, cross-client confidentiality and aggregation thresholds for client-facing analytics 

|**Document ID**|DUS-07|
|---|---|
|**Version / Status**|2.1 / Approved|
|**Document owner**|Rachel Goldberg, Chief Privacy Officer|
|**Approver(s)**|Data Governance Council (2026-01-08)|
|**Effective / Last reviewed**|Effective 2026-01-15|
|**Classification**|INTERNAL - CONFIDENTIAL|
|**Standard contact**|Ethan Brooks, Data Governance Lead, Commercial Bank|
|**Related documents**|POL-FCC-014; MRM-POL-02; TDIP-CAT-2026.2|

## **1. Purpose** 

This Standard governs how client data may be used, combined and disclosed, particularly in analytics shown to clients. It applies to consumer and commercial clients. Consumer data is additionally subject to the Gramm-Leach-Bliley Act privacy provisions; commercial client data is protected by contractual confidentiality (Treasury Management Services Agreement, s14). 

## **2. Classification (summary)** 

|**Class**|**Examples**|
|---|---|
|Public|Published rates, cutoff times|
|Internal|Aggregated operational metrics not attributable to a client|
|Confidential - Client|A client's own transactions, wire history, beneficiaries|
|Restricted - Client Confidential|Account-level activity in deposit systems; financial-crimes features; data about one client's accounts used for<br>risk purposes|

## **3. Purpose limitation** 

Data collected or derived for one purpose (for example fraud detection, AML monitoring, or credit) must not be used for another purpose, including product features, without Privacy Office approval and, for financial-crimes data, FCC approval. Feature tables inherit the permitted purpose of their most restrictive input. 

## **4. Cross-client confidentiality** 

Information about one client, including the behavior of a client's account as a counterparty (for example activity in a counterparty's account after it receives funds), must not be used to generate content shown to another client. This applies even if the information is presented as a pattern, a typical value or an insight, and even if the counterparty is not named. 

## **5. Aggregated cohort statistics shown to clients** 

Statistics derived from multiple clients may be displayed only when all of the following hold for the measurement window: 

1. the cohort contains at least **500 transactions** ; 

2. the cohort contains at least **20 distinct originating clients** ; 

3. no single client contributes more than **15%** of cohort volume; 

4. statistics are refreshed at least monthly; and 

5. wording and disclaimer are approved by the Disclosure Review Committee. 

Cohorts failing any condition must be suppressed (not rounded or approximated). 

## **6. Use of a client's own data** 

Crestline National Bank  |  DUS-07  v2.1  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed

<!-- page 2 -->

|  Privacy Office 

**INTERNAL - CONFIDENTIAL** 

A client's own historical transactions may be used to generate insights shown to that client (for example the typical time for that client's past wires to a given beneficiary to complete). Insights must be based on at least **5 comparable transactions** and must state the basis (count and period). 

## **7. Approvals** 

|**Activity**|**Approval**|
|---|---|
|Access to Restricted datasets|Data owner + Privacy Office (Collibra DAR; 15 business days)|
|New client-facing use of client data|Privacy Impact Assessment (~4 weeks)|
|Use of financial-crimes data outside FCC purposes|Privacy Office + FCC; generally not approved|

Crestline National Bank  |  DUS-07  v2.1  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed