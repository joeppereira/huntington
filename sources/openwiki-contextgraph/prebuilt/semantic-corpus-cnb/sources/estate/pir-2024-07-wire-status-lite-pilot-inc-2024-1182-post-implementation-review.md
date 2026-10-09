<!-- source: raw/estate/PIR-2024-07_Wire_Status_Lite_Pilot_INC-2024-1182_Post-Implementation_Review.pdf | converted by tools/convert_cnb_corpus.py -->
# PIR-2024-07 Wire Status Lite Pilot INC-2024-1182 Post-Implementation Review


<!-- page 1 -->

|  Digital Treasury Channels 

**INTERNAL - CONFIDENTIAL** 

# **Post-Implementation Review: Wire Status Lite Pilot and Incident INC-2024-1182** 

Lessons from the 2024 attempt to provide near-real-time wire status in CBO 

|**Document ID**|PIR-2024-07|
|---|---|
|**Version / Status**|1.1 / Final|
|**Document owner**|Tom Becker, EM - CBO Wire Center (facilitated by Enterprise Architecture)|
|**Approver(s)**|Anjali Deshpande; Raymond Ortiz; Denise Carter|
|**Effective / Last reviewed**|2024-07-15|
|**Classification**|INTERNAL - CONFIDENTIAL|
|**Related documents**|CBO-3120; ADR-PAY-019; INC-2024-1182|

## **1. Summary** 

Wire Status Lite (CBO-3120) piloted auto-refreshing wire status for 60 clients from January to May 2024. The browser refreshed each visible wire's status from PPH v1 every 30 seconds. On **2024-05-31** (month-end) pilot traffic plus production refreshes drove ~85 TPS to the v1 status API, exhausting the PPH API thread pool and delaying wire release for 47 minutes. The pilot was terminated and the epic closed. 

## **2. Impact** 

|**Measure**|**Value**|
|---|---|
|Wires delayed|1,240|
|Wires released after the 6:00 p.m. ET Fedwire customer cutoff (value next day)|312|
|Clients compensated (interest claims)|14 clients, $41,800|
|Regulatory notification|Not required (no data exposure)|

## **3. What we learned about clients** 

- 37% of surveyed pilot users believed 'Processed' meant the beneficiary had received the funds. 

- Users most valued: knowing the wire left CNB, the Fed reference for their beneficiary, and when international wires were credited. 

- Users asked why wires were held; Treasury Support could not explain without FCC guidance. 

## **4. Root causes** 

1. Polling architecture against a shared synchronous API with no client-side backoff. 

2. No capacity test at month-end volumes. 

3. Status semantics were not validated with Compliance or Legal before exposure. 

## **5. Actions** 

|**Action**|**Owner**|**Status**|
|---|---|---|
|Rate-limit PPH v1 status API to 20 TPS shared|PPH|Done 2024-06|
|Adopt event-driven status pattern (became ADR-PAY-019)|EA|Done 2024-06|
|Build a reusable status projection service in CBO|CBO Platform|Delivered for ACH in 2025<br>(CBO-3815)|
|Validate client-facing status terminology with FCC and Legal before any future tracking<br>feature|CBO Product|Open - carry forward|

Crestline National Bank  |  PIR-2024-07  v1.1  |  INTERNAL - CONFIDENTIAL  |  Uncontrolled when printed