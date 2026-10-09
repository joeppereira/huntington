<!-- source: raw/estate/CNB-ORG-PTT-2026-06_PTT_Organization_System_Ownership_Engagement_Directory.pdf | converted by tools/convert_cnb_corpus.py -->
# CNB-ORG-PTT-2026-06 PTT Organization System Ownership Engagement Directory


<!-- page 1 -->

|  Payments & Treasury Technology 

**INTERNAL - CONFIDENTIAL** 

# **Payments & Treasury Technology - Organization, System Ownership & Engagement Directory** 

Who owns what across the Payments business unit, how to engage each team, and planning factors for estimation 

|**Document ID**|CNB-ORG-PTT-2026-06|
|---|---|
|**Version / Status**|2026.2 / Published (quarterly refresh)|
|**Document owner**|PTT Business Management Office (BMO)|
|**Approver(s)**|Gregory Hall, MD - CIO Payments & Treasury Technology|
|**Effective / Last reviewed**|Published 2026-06-15; next refresh 2026-12 (Q4)|
|**Classification**|INTERNAL - CONFIDENTIAL|
|**Related documents**|CBO-ARCH-WC-4.1; PPH-SYS-OVW-9.2; PNG-TDD-6.0; PRSP-HMS-3.4; ENS-INT-3.2; TDIP-CAT-2026.2|

## **1. Purpose** 

This directory is the reference for system ownership, accountable leaders and engagement routes within Payments & Treasury Technology (PTT) and its first- and second-line partners. Product and engineering teams should use it to identify owners for dependencies, to raise demand through the correct intake route, and to apply the planning factors in Section 6 when sizing cross-team work. The directory is refreshed quarterly; organizational announcements issued between refreshes take precedence. 

## **2. Leadership** 

|**Role**|**Name**|**Scope**|
|---|---|---|
|MD, CIO Payments & Treasury Technology|Gregory Hall|All PTT engineering: channels, payments hub, networks, data|
|EVP, Head of Treasury Management<br>Products|Danielle Okafor|Business owner, Treasury Management (TM) products incl. Crestline Business<br>Online|
|Director, Digital Treasury Product|Marcus Chen|Product Owner, CBO Wire Center and Payments & Transfers|
|Director, Payments Platform Product|Laura Kim|Product Owner, PRISM Payments Hub; Business Data Owner for payment<br>datasets|
|Chief Architect, Payments & Treasury|Nikhil Bose|Chair, Payments Architecture Review Board (ARB)|
|EVP, Chief BSA/AML Officer|Catherine Doyle|2nd line owner of financial-crimes policies incl. POL-FCC-014|
|Head of Model Risk Management|Jonathan Price|2nd line owner of MRM-POL-02 and model inventory|
|Chief Privacy Officer|Rachel Goldberg|Owner of DUS-07 Data Use & Client Confidentiality Standard|

## **3. Engineering team directory (as of 2026-06-15)** 

|**Team**|**Leader**|**Key contacts**|**Jira / Slack**|
|---|---|---|---|
|Digital Treasury Channels - CBO Wire<br>Center squad|Anjali Deshpande<br>(Director)|Tom Becker (EM); Lucas Ferreira (Tech Lead); Marcus<br>Chen (PO)|CBO / #cbo-wire-center|
|CBO Platform & Entitlements|Nadia Haddad (EM)|Arjun Mehta (Tech Lead: SPS, CES)|CBO (Platform) /<br>#cbo-platform|
|Payments Hub Engineering|Raymond Ortiz (Director)|Kevin O'Brien (EM); Sunita Rao (Principal Eng.); Laura Kim<br>(PO)|PPH / #pph-support|
|Payment Networks Engineering (PNE)|Raj Malhotra (Director)|Brian Walsh (EM, Fedwire); Chen Wei (TL, Fedwire);<br>Tomasz Nowak (Sr. Eng., gpi Connector)|PNG /<br>#payment-networks|
|Global Transaction Services Integration<br>(GTSI)|Elena Vasquez (Director)|Omar Siddiqui (EM); Hannah Lindqvist (TL) - CHIPS<br>connector, nostro reconciliation integration|GTSI / #gtsi-crossborder|
|Financial Crimes Technology - PRSP|Victor Petrov (Director)|Grace Mensah (EM); Daniel Kowalski (TL, Hold<br>Management Service)|FCT / #fct-prsp|

Crestline National Bank  |  CNB-ORG-PTT-2026-06  v2026.2  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed

<!-- page 2 -->

|  Payments & Treasury Technology 

**INTERNAL - CONFIDENTIAL** 

|**Team**|**Leader**|**Key contacts**|**Jira / Slack**|
|---|---|---|---|
|Enterprise Notification Platform|Sanjay Iyer (Director)|Melissa Grant (EM); Paul Henderson (Onboarding)|ENS / #ens-onboarding|
|Treasury Data & Analytics (TDIP)|Wei Zhang (Director)|Carlos Mendes (EM, Data Eng.); Dr. Aisha Rahman (Lead<br>Data Scientist)|TDA / #tdip-help|

### **3.1 Partner functions (first and second line)** 

|**Function**|**Accountable**|**Contacts for product / design reviews**|
|---|---|---|
|Financial Crimes Compliance (FCC)|Catherine Doyle|Jordan Ellis (FCC Policy & Advisory); Michael Tran (OFAC); Rebecca Stone (FIU)|
|Model Risk Management (MRM)|Jonathan Price|Sophie Laurent (Validation Lead, Treasury & Ops models)|
|Payment Operations|Denise Carter|Luis Ramirez (Wire Investigations); Tanya Brooks (Wire Room)|
|Commercial Service Center|Kim Nguyen|Treasury Support scripts and training|
|Legal - Treasury & Payments|Andrew Feldman|Patricia Moore (Chair, Disclosure Review Committee)|
|Information Security - Digital Channels|Farah Ali|Design reviews (SECREV)|
|Privacy Office & Data Governance|Rachel Goldberg|Ethan Brooks (Data Governance Lead, Commercial Bank)|
|Deposits Data Ownership|Mark Sullivan|Core Deposit Platform datasets (Restricted)|

## **4. System ownership register** 

Technical owner = accountable engineering manager/lead. Business owner = accountable product or data owner. Support tier: T1 = 24x7 critical, T2 = business hours + on-call, T3 = business hours. 

|**System ID**|**System**|**Owning team**|**Technical owner**|**Business owner**|**Tier**|
|---|---|---|---|---|---|
|SYS-CBO|Crestline Business Online - Wire Center<br>module|CBO Wire Center squad|Tom Becker / Lucas Ferreira|Marcus Chen|T1|
|SYS-CBO-SPS|CBO Status Projection Service|CBO Platform|Arjun Mehta|Marcus Chen|T2|
|SYS-CES|Commercial Entitlements Service|CBO Platform|Nadia Haddad|Marcus Chen|T1|
|SYS-PPH|PRISM Payments Hub (Volaris 9.4)|Payments Hub Engineering|Kevin O'Brien / Sunita Rao|Laura Kim|T1|
|SYS-PNG-FFC|Payment Network Gateway - Fedwire Funds<br>Connector|PNE|Brian Walsh / Chen Wei|Laura Kim|T1|
|SYS-PNG-GPI|Payment Network Gateway - Swift Alliance &<br>gpi Connector|PNE|Raj Malhotra / Tomasz Nowak|Laura Kim|T1|
|SYS-PRSP-HMS|PRSP - Hold Management Service|FCT|Grace Mensah / Daniel<br>Kowalski|Rebecca Stone (FIU)|T1|
|SYS-PRSP-SEN|PRSP - Sentinel Fraud Scoring (vendor)|FCT|Grace Mensah|Fraud Strategy (FCC)|T1|
|SYS-PRSP-SSC|PRSP - SanctionScreen|FCT|Grace Mensah|Michael Tran|T1|
|SYS-ENS|Enterprise Notification Service|Enterprise Notification<br>Platform|Melissa Grant|Sanjay Iyer|T2|
|SYS-TDIP|Treasury Data & Insights Platform|TDIP|Carlos Mendes|Laura Kim (payment<br>data)|T2|
|SYS-CDP|Core Deposit Platform|Deposits Technology|(Deposits Tech)|Mark Sullivan|T1|
|SYS-IWB|Investigations Workbench|Payment Operations Tech|(Ops Tech)|Luis Ramirez|T2|

## **5. Governance forums** 

|**Forum**|**Cadence**|**Submission lead time**|**Notes**|
|---|---|---|---|
|Payments Architecture Review Board<br>(ARB)|Monthly, 2nd Tuesday|10 business days|Required for new client-facing integrations to payment<br>systems. Upcoming: 2026-11-10, 2026-12-08|
|Payments Platform Demand Board|Monthly|Request by prior<br>month-end|Prioritizes PPH roadmap; next session 2026-10-21|
|FCT Change Advisory|Bi-weekly|5 business days|FCC sign-off required for hold/screening changes; year-end<br>freeze Dec-15 to Jan-05|

Crestline National Bank  |  CNB-ORG-PTT-2026-06  v2026.2  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed

<!-- page 3 -->

|  Payments & Treasury Technology 

**INTERNAL - CONFIDENTIAL** 

|**Forum**|**Cadence**|**Submission lead time**|**Notes**|
|---|---|---|---|
|Disclosure Review Committee (DRC)|Bi-weekly, Thursday|5 business days|Approves client-facing copy, disclaimers and notification<br>templates|
|MRM Model Inventory & Validation|Continuous (Archer)|Register before<br>development|Tier 2 validation 10-14 weeks plus queue|
|Privacy Impact Assessment (PIA)|Continuous (OneTrust)|~4 weeks|Required for new uses of client data in client-facing features|

## **6. Engagement routes and planning factors** 

Use these factors for first-pass sizing of cross-team dependencies. Hours are engineering hours unless stated; factors are calibrated from the last four program increments (PIs). 

|**Team**|**Planning factor**|**Intake route / lead time**|**Capacity note (PI 27.1)**|
|---|---|---|---|
|CBO Wire Center squad|1 story point ~ 6.5 hrs; velocity ~42<br>pts/sprint|Jira CBO; PO prioritization|Q4-2026 ~85% committed|
|CBO Platform & Entitlements|1 pt ~ 6.5 hrs; ~30 pts/sprint|Jira CBO (Platform); 2-week triage|~70% committed|
|Payments Hub Engineering|1 pt ~ 8 hrs (vendor platform + regression)|Payments Platform Demand Board; 6-8<br>weeks to schedule|~90% committed (Nov-2026<br>address enforcement; FedNow<br>outbound)|
|Payment Networks Engineering|1 pt ~ 8 hrs|Jira PNG; change windows Sat 22:00-02:00<br>ET|~80% committed|
|GTSI|1 pt ~ 7 hrs|Jira GTSI; quarterly roadmap intake|~75% committed|
|Financial Crimes Technology|1 pt ~ 8 hrs + 20% independent compliance<br>testing|FCT Change Advisory + FCC sign-off|~80% committed|
|Enterprise Notification Platform|~12 ENS hrs per new event type|ServiceNow 'ENS Event Onboarding'; SLA 6<br>weeks|Per-entity subscriptions 2027-H1|
|TDIP|1 pt ~ 6 hrs|Jira TDA; Collibra DAR (Restricted: +15<br>business days)|~75% committed|
|Model Risk Management|EUA registration ~16 hrs; Tier 2 validation<br>160-240 validator hrs|Archer; Tier 2 10-14 weeks + queue|Queue ~6 weeks (Q4-2026)|
|FCC Policy & Advisory|~10 business days per review|FCC Advisory intake|-|
|Information Security (SECREV)|Design review ~24-40 hrs|SLA 3 weeks|-|
|Payment Operations|~40 hrs per new client-facing workflow<br>(SOPs)|Ops Readiness Review 4 weeks pre go-live|-|
|Commercial Service Center|~24 hrs scripts/training|Readiness checklist 3 weeks pre go-live|-|

## **7. Program increment calendar** 

|**PI**|**Dates**|**Planning event**|
|---|---|---|
|PI 26.4|2026-09-07 to 2026-11-27|Complete|
|PI 27.1|2026-12-01 to 2027-03-05|PI planning 2026-11-17 / 18 (dependency asks due 2026-11-06)|
|PI 27.2|2027-03-15 to 2027-06-11|PI planning 2027-03-02 / 03|

## **8. Escalation** 

Dependency conflicts that cannot be resolved between engineering managers escalate to the respective Directors, then to the PTT Leadership Team (weekly, Mondays). Compliance or policy interpretation questions route to FCC Policy & Advisory (Jordan Ellis) or the Privacy Office (Ethan Brooks) and are not decided by engineering teams. 

Crestline National Bank  |  CNB-ORG-PTT-2026-06  v2026.2  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed