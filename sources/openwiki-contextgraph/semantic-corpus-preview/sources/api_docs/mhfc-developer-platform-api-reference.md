<!-- source: raw/api_docs/MHFC_Developer_Platform_API_Reference.docx | converted by tools/convert_corpus.py -->
**MERIDIAN HARBOR FINANCIAL CORP.**

**Developer Platform API Reference**

Catalog of 18 production APIs: accounts, payments, cards, identity, fraud, credit, market data, treasury and regulatory reporting

Document version 3.6 - July 2026 - Owner: Developer Platform Engineering

*SYNTHETIC DOCUMENT FOR A PROOF OF CONCEPT. Meridian Harbor Financial Corp. is a fictional institution. All names, figures and events are invented and do not describe any real company.*

# Contents

# 1. Platform Overview

The Meridian Harbor Developer Platform exposes the Firm's banking, payments, risk and finance capabilities as versioned REST APIs. The same APIs serve three audiences: internal applications (mobile app, online banking, servicing tools), external clients and partners (corporate treasurers, fintechs, data aggregators), and internal risk and finance processes, including Tier 1 risk models and regulatory reporting.

APIs that feed Tier 1 models or regulatory disclosures are classified as critical data services under the Firm's BCBS 239 program. They carry named data owners, documented data-quality rules, enhanced change management, and registration in the model inventory, so that any breaking change automatically triggers a model change review by Model Risk Governance & Review (MRGR).

## 1.1 Environments

| **Environment** | **Base URL** | **Purpose** |
| --- | --- | --- |
| **Sandbox** | https://sandbox.api.meridianharbor.example | Synthetic data; self-service onboarding; no SLA |
| **Certification** | https://cert.api.meridianharbor.example | Pre-production testing with masked data |
| **Production** | https://api.meridianharbor.example | Live traffic; SLAs apply |
| **Internal (risk & finance)** | https://internal.api.mhfc.example | Restricted APIs (API-10, API-14, API-15, API-16); private network only |

## 1.2 Authentication and authorization

All APIs use OAuth 2.0. Server-to-server clients use the client-credentials grant with mutual TLS (certificate-bound access tokens). Customer-facing integrations use the authorization-code grant with PKCE and customer consent. Access tokens are JWTs valid for 15 minutes. Scopes are listed per API; least-privilege scopes are enforced.

POST /oauth2/token

Content-Type: application/x-www-form-urlencoded

grant\_type=client\_credentials&scope=accounts:read%20accounts.balances:read

## 1.3 Versioning and deprecation

Major versions appear in the path (for example /accounts/v3). Minor versions are additive and backward compatible. A major version is supported for at least 12 months after its successor reaches general availability; deprecation is announced via the Sunset header and the developer portal.

## 1.4 Rate limiting, idempotency and pagination

* Rate limits are applied per client and per API; responses include X-RateLimit-Limit, X-RateLimit-Remaining and Retry-After on HTTP 429.
* All POST operations that move money or create resources require an Idempotency-Key header (UUID); keys are retained for 24 hours.
* List endpoints use cursor-based pagination via limit and cursor query parameters; responses include nextCursor.
* All timestamps are ISO 8601 UTC; monetary amounts are decimal numbers in the stated currency; risk and finance APIs state units (typically USD millions) in the payload.

## 1.5 Error format

{

"error": {

"code": "insufficient\_scope",

"message": "Token lacks scope payments:write",

"requestId": "req\_8f2c01"

}

}

| **HTTP status** | **Error code** | **Meaning** |
| --- | --- | --- |
| **400** | invalid\_request | Malformed body, missing required field or invalid parameter value. |
| **401** | unauthorized | Missing, expired or invalid OAuth 2.0 access token. |
| **403** | insufficient\_scope | Token lacks the scope required for this operation. |
| **404** | not\_found | Resource does not exist or is not visible to the caller. |
| **409** | conflict | Idempotency key reused with a different payload, or state conflict. |
| **429** | rate\_limited | Rate limit exceeded; retry after the number of seconds in Retry-After. |
| **500** | internal\_error | Unexpected server error; safe to retry idempotent requests with backoff. |
| **503** | service\_unavailable | Planned maintenance or dependency outage; see status page. |

# 2. API Catalog Summary

| **ID** | **API** | **Version** | **Domain** | **Owner** |
| --- | --- | --- | --- | --- |
| **API-01** | Accounts API | v3.4 | Retail & Commercial Banking | Digital Platforms Engineering |
| **API-02** | Transactions API | v3.1 | Retail & Commercial Banking | Digital Platforms Engineering |
| **API-03** | Payments Initiation API | v3.2 | Payments | Global Payments Technology |
| **API-04** | Real-Time Payments API | v2.3 | Payments | Global Payments Technology |
| **API-05** | Wire Transfer API | v2.0 | Payments | Global Payments Technology |
| **API-06** | Card Management API | v2.6 | Card Services | Card Technology |
| **API-07** | Customer Identity & KYC API | v1.9 | Client Onboarding | Know-Your-Customer Platform |
| **API-08** | Fraud Risk Signals API | v4.0 | Fraud & Financial Crimes | Fraud Strategy Engineering |
| **API-09** | Credit Decisioning API | v2.2 | Credit Origination | Credit Platforms Engineering |
| **API-10** | Credit Risk Scoring API | v3.0 | Credit Risk | Risk Analytics Engineering |
| **API-11** | Loan Servicing API | v2.8 | Lending Operations | Lending Platforms Engineering |
| **API-12** | Market Data API | v5.1 | Markets & Treasury | Market Data Services |
| **API-13** | FX Rates API | v2.4 | Markets & Treasury | Market Data Services |
| **API-14** | Macroeconomic Scenario API | v1.6 | Risk & Finance | Risk Analytics Engineering |
| **API-15** | Treasury Liquidity Positions API | v2.1 | Treasury | Treasury Technology |
| **API-16** | Regulatory Reporting API | v1.8 | Finance & Regulatory | Finance Technology |
| **API-17** | Statements & Documents API | v1.4 | Client Servicing | Digital Platforms Engineering |
| **API-18** | Webhooks & Event Notifications API | v1.3 | Platform | Developer Platform Engineering |

# 3. API Reference

## API-01 Accounts API

Returns deposit, card and loan account details, balances and account holders for an authenticated customer or corporate client. Source of truth for account balances displayed in the mobile app and online banking.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-01 |
| **Version** | v3.4 |
| **Base path** | /accounts/v3 |
| **Business domain** | Retail & Commercial Banking |
| **Owning team** | Digital Platforms Engineering |
| **Intended consumers** | Internal apps, corporate clients, licensed data aggregators |
| **Data classification** | Confidential - Client Data |
| **OAuth scopes** | accounts:read, accounts.balances:read, accounts.holders:read |
| **Rate limits** | 1,200 requests/minute per client; burst 200/second |
| **Service-level objective** | 99.95% monthly availability; p95 latency 180 ms |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **GET** | /accounts | List accounts the caller is entitled to view, with pagination. |
| **GET** | /accounts/{accountId} | Retrieve account details (type, status, open date, product code). |
| **GET** | /accounts/{accountId}/balances | Current, available and ledger balances, with as-of timestamp. |
| **GET** | /accounts/{accountId}/holders | Account holders and authorised signers (masked PII). |

**Example request**

GET /accounts/v3/accounts/DDA-0044718823/balances

Authorization: Bearer <token>

**Example response (200)**

{

"accountId": "DDA-0044718823",

"currency": "USD",

"asOf": "2026-06-30T23:59:59Z",

"balances": {

"current": 18452.17,

"available": 17902.17,

"ledger": 18452.17

},

"holds": 550

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **Core deposit system (DDA)**  **Card processing platform**  **Loan Servicing API (API-11)** | Mobile app and online banking  Statements & Documents API (API-17)  Data aggregators |

**Changelog**

* v3.4 (2026-03): added holds field to balances response
* v3.2 (2025-07): cursor-based pagination
* v2 sunset 2025-12-31

## API-02 Transactions API

Provides posted and pending transactions with merchant enrichment (category, merchant name, location) for deposit and card accounts, up to 24 months of history.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-02 |
| **Version** | v3.1 |
| **Base path** | /transactions/v3 |
| **Business domain** | Retail & Commercial Banking |
| **Owning team** | Digital Platforms Engineering |
| **Intended consumers** | Internal apps, corporate clients, data aggregators, Fraud Strategy |
| **Data classification** | Confidential - Client Data |
| **OAuth scopes** | transactions:read, transactions.enriched:read |
| **Rate limits** | 1,000 requests/minute per client |
| **Service-level objective** | 99.95% availability; p95 latency 250 ms |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **GET** | /accounts/{accountId}/transactions | List transactions with date range, status and amount filters. |
| **GET** | /transactions/{transactionId} | Retrieve a single transaction with enrichment. |
| **POST** | /transactions/search | Full-text and structured search across a customer's accounts. |

**Example request**

GET /transactions/v3/accounts/CARD-5501/transactions?from=2026-06-01&status=posted&limit=2

**Example response (200)**

{

"data": [

{

"transactionId": "T-8812",

"postedDate": "2026-06-02",

"amount": -42.18,

"merchant": {

"name": "Harbor Coffee Co.",

"category": "Dining"

},

"status": "posted"

}

],

"nextCursor": "eyJvZmZzZXQiOjJ9"

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **Core deposit system (DDA)**  **Card processing platform**  **Merchant enrichment service** | Mobile app  Fraud Risk Signals API (API-08) feature store  Data aggregators |

**Changelog**

* v3.1 (2026-01): added merchant.location
* v3.0 (2025-04): enrichment GA

## API-03 Payments Initiation API

Initiates ACH, book transfer and check payments individually or in bulk files, with ISO 20022 structured remittance. All payments are screened by sanctions and the Fraud Risk Signals API before release.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-03 |
| **Version** | v3.2 |
| **Base path** | /payments/v3 |
| **Business domain** | Payments |
| **Owning team** | Global Payments Technology |
| **Intended consumers** | Corporate clients, ERP connectors, internal treasury applications |
| **Data classification** | Restricted - Financial Transaction |
| **OAuth scopes** | payments:write, payments:read, payments.bulk:write |
| **Rate limits** | 300 requests/minute per client; bulk files up to 50,000 items |
| **Service-level objective** | 99.98% availability; p95 latency 400 ms |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **POST** | /payments | Create a single payment; requires Idempotency-Key header. |
| **POST** | /payment-files | Upload a bulk payment file (ISO 20022 pain.001 or CSV). |
| **GET** | /payments/{paymentId} | Retrieve status: received, screened, released, settled, returned. |
| **POST** | /payments/{paymentId}/cancel | Cancel a payment before release. |

**Example request**

POST /payments/v3/payments

Idempotency-Key: 6f1d2c3e-...

{

"debtorAccount": "DDA-7700112",

"creditor": {

"name": "Acme Supplies LLC",

"routing": "021000021",

"account": "\*\*\*\*4410"

},

"amount": {

"value": 12500,

"currency": "USD"

},

"rail": "ACH\_SAME\_DAY",

"remittance": {

"invoice": "INV-2026-0611"

}

}

**Example response (200)**

{

"paymentId": "PAY-55ab91",

"status": "received",

"fraudScore": 0.04,

"expectedSettlement": "2026-07-01"

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **Accounts API (API-01) for funds check**  **Sanctions screening**  **Fraud Risk Signals API (API-08)** | ACH operator  Webhooks & Event Notifications API (API-18)  General ledger |

**Changelog**

* v3.2 (2026-05): ISO 20022 structured remittance
* v3.1 (2025-10): same-day ACH rail

## API-04 Real-Time Payments API

Sends and receives instant, irrevocable account-to-account payments 24x7x365 over real-time payment networks, including request-for-payment messages. Volumes grew 64% year-on-year in 2Q26.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-04 |
| **Version** | v2.3 |
| **Base path** | /rtp/v2 |
| **Business domain** | Payments |
| **Owning team** | Global Payments Technology |
| **Intended consumers** | Corporate and small-business clients, consumer app (P2P) |
| **Data classification** | Restricted - Financial Transaction |
| **OAuth scopes** | rtp:send, rtp:read, rtp.rfp:write |
| **Rate limits** | 600 requests/minute per client; max $1,000,000 per payment |
| **Service-level objective** | 99.99% availability; p95 end-to-end 4 s |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **POST** | /credit-transfers | Send an instant credit transfer. |
| **POST** | /requests-for-payment | Send a request for payment to a payer. |
| **GET** | /credit-transfers/{id} | Retrieve status (accepted, rejected, pending-review). |
| **GET** | /participants/{routing} | Check whether a receiving bank is reachable on the network. |

**Example request**

POST /rtp/v2/credit-transfers

Idempotency-Key: 6f1d2c3e-...

{

"debtorAccount": "DDA-7700112",

"creditorRouting": "026009593",

"creditorAccount": "\*\*\*\*2291",

"amount": 2500,

"purpose": "SUPP"

}

**Example response (200)**

{

"id": "RTP-9a1c",

"status": "accepted",

"settledAt": "2026-06-30T14:03:11Z"

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **Accounts API (API-01)**  **Fraud Risk Signals API (API-08)**  **Customer Identity & KYC API (API-07)** | Real-time payment network  Webhooks & Event Notifications API (API-18)  Treasury Liquidity Positions API (API-15) intraday cash |

**Changelog**

* v2.3 (2026-02): request-for-payment GA
* v2.2 (2025-09): opened to middle-market clients

## API-05 Wire Transfer API

Initiates domestic (Fedwire) and cross-border (SWIFT MT/ISO 20022 MX) wires with FX conversion using rates from the FX Rates API. Supports payment tracking via UETR.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-05 |
| **Version** | v2.0 |
| **Base path** | /wires/v2 |
| **Business domain** | Payments |
| **Owning team** | Global Payments Technology |
| **Intended consumers** | CIB corporate and institutional clients |
| **Data classification** | Restricted - Financial Transaction |
| **OAuth scopes** | wires:write, wires:read |
| **Rate limits** | 120 requests/minute per client |
| **Service-level objective** | 99.99% availability during operating hours |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **POST** | /wires | Create a domestic or international wire. |
| **GET** | /wires/{wireId} | Status and UETR tracking events. |
| **POST** | /wires/quotes | Get an FX quote valid for 60 seconds for a cross-currency wire. |

**Example request**

POST /wires/v2/wires

Idempotency-Key: 6f1d2c3e-...

{

"debtorAccount": "DDA-9100044",

"beneficiary": {

"name": "Rhein Logistik GmbH",

"iban": "DE89\*\*\*\*3000"

},

"amount": 250000,

"currency": "EUR",

"quoteId": "Q-77e2"

}

**Example response (200)**

{

"wireId": "W-31f0",

"uetr": "e0a4...c1",

"status": "screening",

"rate": 0.9214

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **FX Rates API (API-13)**  **Sanctions screening**  **Fraud Risk Signals API (API-08)** | Fedwire  SWIFT  General ledger  Treasury Liquidity Positions API (API-15) |

**Changelog**

* v2.0 (2025-11): ISO 20022 MX migration complete

## API-06 Card Management API

Manages debit and credit card lifecycle: issuance, activation, lock/unlock, spend controls, digital wallet provisioning and replacement. PAN data is tokenized; raw card numbers are never returned.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-06 |
| **Version** | v2.6 |
| **Base path** | /cards/v2 |
| **Business domain** | Card Services |
| **Owning team** | Card Technology |
| **Intended consumers** | Mobile app, fintech and co-brand partners |
| **Data classification** | Restricted - PCI |
| **OAuth scopes** | cards:read, cards:write, cards.controls:write |
| **Rate limits** | 800 requests/minute per client |
| **Service-level objective** | 99.97% availability; p95 latency 220 ms |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **GET** | /cards/{cardToken} | Card status, product and expiry (tokenized). |
| **POST** | /cards/{cardToken}/lock | Temporarily lock a card. |
| **PUT** | /cards/{cardToken}/controls | Set merchant-category, geography and amount controls. |
| **POST** | /cards/{cardToken}/wallet-provisioning | Provision to a digital wallet. |

**Example request**

POST /cards/v2/cards/{cardToken}/lock

Idempotency-Key: 6f1d2c3e-...

{

"controls": {

"blockedCategories": [

"GAMBLING"

],

"dailyLimit": 1500,

"allowedCountries": [

"US",

"CA"

]

}

}

**Example response (200)**

{

"cardToken": "tok\_card\_83jd",

"controlsVersion": 7,

"status": "active"

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **Card processing platform**  **Customer Identity & KYC API (API-07)** | Card authorization system  Digital wallets  Webhooks & Event Notifications API (API-18) |

**Changelog**

* v2.6 (2026-04): geography controls
* v2.5 (2025-08): co-brand partner scopes

## API-07 Customer Identity & KYC API

Performs identity verification, customer due diligence and beneficial-ownership checks, returning a KYC status and risk rating used to gate account opening and payment limits.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-07 |
| **Version** | v1.9 |
| **Base path** | /kyc/v1 |
| **Business domain** | Client Onboarding |
| **Owning team** | Know-Your-Customer Platform |
| **Intended consumers** | Onboarding applications, Payments, Card Services |
| **Data classification** | Restricted - PII |
| **OAuth scopes** | kyc:verify, kyc:read |
| **Rate limits** | 200 requests/minute per client |
| **Service-level objective** | 99.9% availability; p95 latency 1.2 s (verification) |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **POST** | /verifications | Start an individual or entity verification. |
| **GET** | /verifications/{id} | Result: verified, review, rejected; with reason codes. |
| **GET** | /customers/{customerId}/risk-rating | Current AML risk rating (low, medium, high). |

**Example request**

POST /kyc/v1/verifications

Idempotency-Key: 6f1d2c3e-...

{

"type": "individual",

"name": "Jordan Ellis",

"dob": "1988-04-12",

"documentToken": "doc\_44ab"

}

**Example response (200)**

{

"id": "KYC-1189",

"status": "verified",

"riskRating": "low",

"checks": [

"id",

"sanctions",

"pep"

]

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **Identity verification vendors**  **Sanctions and PEP lists**  **Corporate registries** | Accounts opening  Real-Time Payments API (API-04) limits  Card Management API (API-06) |

**Changelog**

* v1.9 (2026-01): beneficial-ownership for entities

## API-08 Fraud Risk Signals API

Returns real-time fraud scores (0-1) and reason codes for card authorizations, payments and account events using gradient-boosted and graph-based models. Average decision latency under 35 ms.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-08 |
| **Version** | v4.0 |
| **Base path** | /fraud/v4 |
| **Business domain** | Fraud & Financial Crimes |
| **Owning team** | Fraud Strategy Engineering |
| **Intended consumers** | Card authorization, Payments, RTP, Wires, Credit Decisioning (internal only) |
| **Data classification** | Restricted - Internal |
| **OAuth scopes** | fraud:score |
| **Rate limits** | 50,000 requests/second aggregate; internal callers only |
| **Service-level objective** | 99.99% availability; p99 latency 60 ms |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **POST** | /scores | Score an event (authorization, payment, login, account change). |
| **POST** | /feedback | Report confirmed fraud or false positive for model retraining. |
| **GET** | /reason-codes | Reference list of reason codes. |

**Example request**

POST /fraud/v4/scores

Idempotency-Key: 6f1d2c3e-...

{

"eventType": "rtp\_send",

"amount": 2500,

"accountId": "DDA-7700112",

"deviceId": "dv-118",

"payee": "new"

}

**Example response (200)**

{

"score": 0.07,

"decision": "approve",

"reasons": [

"NEW\_PAYEE\_LOW\_RISK"

]

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **Transactions API (API-02) feature store**  **Device intelligence**  **Consortium fraud data** | Payments Initiation API (API-03)  Real-Time Payments API (API-04)  Wire Transfer API (API-05)  Credit Decisioning API (API-09)  Operational risk loss data |

**Changelog**

* v4.0 (2025-12): graph features; new reason codes

## API-09 Credit Decisioning API

Returns approve/decline/refer decisions, credit line and pricing tier for consumer and small-business credit applications, combining bureau attributes, internal behaviour scores and fraud signals. Decisions are logged for fair-lending monitoring and adverse-action notices.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-09 |
| **Version** | v2.2 |
| **Base path** | /credit-decisions/v2 |
| **Business domain** | Credit Origination |
| **Owning team** | Credit Platforms Engineering |
| **Intended consumers** | Card, Auto and small-business origination channels; point-of-sale partners (sandbox) |
| **Data classification** | Restricted - Credit |
| **OAuth scopes** | credit.decisions:write, credit.decisions:read |
| **Rate limits** | 400 requests/minute per channel |
| **Service-level objective** | 99.95% availability; p95 latency 900 ms |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **POST** | /applications | Submit an application and receive a decision. |
| **GET** | /applications/{id} | Retrieve decision, reason codes and offered terms. |
| **POST** | /applications/{id}/counteroffer | Accept a counteroffer. |

**Example request**

POST /credit-decisions/v2/applications

Idempotency-Key: 6f1d2c3e-...

{

"product": "CARD\_REWARDS",

"applicant": {

"income": 92000,

"housing": "rent"

},

"bureauConsentToken": "bc\_19"

}

**Example response (200)**

{

"id": "APP-7781",

"decision": "approve",

"creditLine": 8500,

"apr": 0.2349,

"pdBand": "0.50-2.50%",

"reasonCodes": []

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **Credit bureaus**  **Fraud Risk Signals API (API-08)**  **Credit Risk Scoring API (API-10)**  **Customer Identity & KYC API (API-07)** | Card and Auto origination systems  Loan Servicing API (API-11) on booking  Fair-lending monitoring |

**Changelog**

* v2.2 (2026-05): point-of-sale sandbox
* v2.1 (2025-09): small-business applications

## API-10 Credit Risk Scoring API

Serves pool-level and obligor-level probability of default (PD), loss given default (LGD) and exposure at default (EAD) parameters. Provides point-in-time, scenario-conditional parameters for CECL and through-the-cycle parameters for Advanced approaches capital through separate endpoints. Designated a critical data service under BCBS 239.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-10 |
| **Version** | v3.0 |
| **Base path** | /credit-risk/v3 |
| **Business domain** | Credit Risk |
| **Owning team** | Risk Analytics Engineering |
| **Intended consumers** | Internal only: CECL model (MDL-CR-007), regulatory capital calculators, portfolio monitoring |
| **Data classification** | Restricted - Risk Model Data |
| **OAuth scopes** | risk.params:read |
| **Rate limits** | 60 requests/minute; batch extracts via async jobs |
| **Service-level objective** | 99.95% availability; quarterly refresh within T+3 business days |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **GET** | /pools | List portfolio pools (e.g. Credit Card, Residential Mortgage, CRE, C&I). |
| **GET** | /pools/{poolId}/parameters?basis=pit | Point-in-time PD, LGD, remaining life and macro elasticities used by CECL. |
| **GET** | /pools/{poolId}/parameters?basis=ttc | Through-the-cycle PD/LGD with regulatory floors. |
| **POST** | /extracts | Start an asynchronous full-portfolio extract; returns jobId. |

**Example request**

GET /credit-risk/v3/pools/CARD/parameters?basis=pit&asOf=2025-12-31

**Example response (200)**

{

"poolId": "CARD",

"asOf": "2025-12-31",

"basis": "pit",

"basePdAnnual": 0.0374,

"lgd": 0.88,

"remainingLifeYears": 1.7,

"pdElasticityPerPpUnemployment": 0.165,

"modelVersion": "PD-CARD-5.2"

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **Internal ratings systems**  **Loan Servicing API (API-11)**  **Macroeconomic Scenario API (API-14)** | MDL-CR-007 CECL Lifetime Expected Credit Loss Model (CECL\_Allowance\_Model.xlsx)  Advanced approaches credit RWA  Credit Decisioning API (API-09)  Pillar 3 Section 6.3 |

**Changelog**

* v3.0 (2025-10): separate PIT/TTC endpoints; added macro elasticities used by MDL-CR-007

## API-11 Loan Servicing API

Provides loan-level balances, payment schedules, delinquency status, remaining contractual life and repricing terms for consumer and wholesale loans; supports payoff quotes and payment posting.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-11 |
| **Version** | v2.8 |
| **Base path** | /loans/v2 |
| **Business domain** | Lending Operations |
| **Owning team** | Lending Platforms Engineering |
| **Intended consumers** | Servicing applications, CECL and ALM models, customer channels |
| **Data classification** | Confidential - Client Data |
| **OAuth scopes** | loans:read, loans.payments:write, loans.portfolio:read |
| **Rate limits** | 900 requests/minute; portfolio snapshots via async extract |
| **Service-level objective** | 99.95% availability |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **GET** | /loans/{loanId} | Loan details: balance, rate, next reset date, maturity, status. |
| **GET** | /loans/{loanId}/schedule | Amortization schedule. |
| **GET** | /portfolio/snapshots/{asOf} | Month-end portfolio snapshot aggregated by segment and repricing bucket (0-3m, 3-12m, 1-5y, >5y). |
| **POST** | /loans/{loanId}/payoff-quotes | Generate a payoff quote. |

**Example request**

GET /loans/v2/portfolio/snapshots/2025-12-31?segment=COMMERCIAL\_AND\_INDUSTRIAL

**Example response (200)**

{

"segment": "Commercial & Industrial",

"balance": 172500,

"units": "USD millions",

"repricing": {

"0-3m": 0.78,

"3-12m": 0.08,

"1-5y": 0.12,

">5y": 0.02

},

"delinquency30Plus": 0.0031

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **Loan servicing systems (mortgage, auto, card, commercial)**  **Credit Decisioning API (API-09) bookings** | MDL-CR-007 CECL model (EAD, remaining life)  MDL-ALM-014 NII Sensitivity Model (repricing profile)  Credit Risk Scoring API (API-10)  Accounts API (API-01) |

**Changelog**

* v2.8 (2026-02): repricing-bucket snapshot for ALM
* v2.6 (2025-06): remaining-life field for CECL

## API-12 Market Data API

Publishes end-of-day and intraday prices, yield curves (SOFR, Treasury), credit spreads and volatility surfaces from licensed vendors and internal marks. Golden source for VaR, fair value and the policy rate used in ALM models.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-12 |
| **Version** | v5.1 |
| **Base path** | /market-data/v5 |
| **Business domain** | Markets & Treasury |
| **Owning team** | Market Data Services |
| **Intended consumers** | Trading, risk, valuation control, Treasury/CIO models |
| **Data classification** | Internal - Licensed Data |
| **OAuth scopes** | marketdata:read, marketdata.curves:read |
| **Rate limits** | 5,000 requests/minute; streaming via WebSocket |
| **Service-level objective** | 99.99% availability; EOD snapshot by 19:00 ET |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **GET** | /curves/{curveId} | Yield curve points for a date (e.g. USD-SOFR, UST). |
| **GET** | /series/{seriesId} | Time series, e.g. POLICY.FEDFUNDS.UB. |
| **GET** | /prices | Instrument prices by identifier list. |
| **GET** | /vol-surfaces/{surfaceId} | Implied volatility surface. |

**Example request**

GET /market-data/v5/series/POLICY.FEDFUNDS.UB?date=2025-12-31

**Example response (200)**

{

"seriesId": "POLICY.FEDFUNDS.UB",

"date": "2025-12-31",

"value": 0.0375,

"source": "official"

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **Licensed market data vendors**  **Internal trader marks (validated by Valuation Control)** | MDL-ALM-014 NII Sensitivity Model (policy rate, curves)  VaR engine  Fair value (Note 13)  Collateral valuation |

**Changelog**

* v5.1 (2026-03): WebSocket streaming
* v5.0 (2025-05): SOFR curve family

## API-13 FX Rates API

Provides spot, forward and end-of-day reference FX rates for 150+ currency pairs, and executable quotes for client payments.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-13 |
| **Version** | v2.4 |
| **Base path** | /fx/v2 |
| **Business domain** | Markets & Treasury |
| **Owning team** | Market Data Services |
| **Intended consumers** | Wires, card cross-border pricing, risk aggregation, finance |
| **Data classification** | Internal - Licensed Data |
| **OAuth scopes** | fx:read, fx.quotes:write |
| **Rate limits** | 3,000 requests/minute |
| **Service-level objective** | 99.99% availability; quote validity 60 s |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **GET** | /rates/spot | Spot mid rates for currency pairs. |
| **GET** | /rates/eod/{date} | End-of-day reference rates used for financial reporting. |
| **POST** | /quotes | Executable quote for a client conversion. |

**Example request**

GET /fx/v2/rates/spot?pairs=EURUSD,GBPUSD

**Example response (200)**

{

"asOf": "2026-06-30T15:00:00Z",

"rates": {

"EURUSD": 1.0853,

"GBPUSD": 1.2711

}

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **FX trading desk pricing engine**  **Licensed vendors** | Wire Transfer API (API-05)  VaR engine  Regulatory Reporting API (API-16) currency conversion |

**Changelog**

* v2.4 (2025-11): EOD reference endpoint for finance

## API-14 Macroeconomic Scenario API

Distributes approved macroeconomic scenario sets (paths for unemployment, GDP, house prices, CRE prices, rates, spreads) and their probability weights. Scenario sets are versioned and locked after Scenario Committee approval. Migrated to the strategic data platform in 2Q26, cutting load time from six hours to under forty minutes.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-14 |
| **Version** | v1.6 |
| **Base path** | /scenarios/v1 |
| **Business domain** | Risk & Finance |
| **Owning team** | Risk Analytics Engineering |
| **Intended consumers** | Internal only: CECL, capital planning, stress testing, ALM |
| **Data classification** | Restricted - Internal |
| **OAuth scopes** | scenarios:read, scenarios:approve |
| **Rate limits** | 30 requests/minute |
| **Service-level objective** | 99.9% availability; new set published within 1 business day of approval |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **GET** | /scenario-sets | List scenario sets (e.g. MSC-2025Q4, SA-2025-INT). |
| **GET** | /scenario-sets/{setId} | Scenarios, weights and approval metadata. |
| **GET** | /scenario-sets/{setId}/paths/{variable} | Quarterly path for a variable in each scenario. |

**Example request**

GET /scenarios/v1/scenario-sets/MSC-2025Q4

**Example response (200)**

{

"setId": "MSC-2025Q4",

"approved": "2025-12-15",

"scenarios": [

{

"name": "Upside",

"weight": 0.2,

"peakUnemployment": 0.038,

"realGdp2026": 0.026,

"hpiChange": 0.045,

"creChange": 0.03

},

{

"name": "Baseline",

"weight": 0.5,

"peakUnemployment": 0.044,

"realGdp2026": 0.017,

"hpiChange": 0.022,

"creChange": -0.01

},

{

"name": "Downside",

"weight": 0.3,

"peakUnemployment": 0.068,

"realGdp2026": -0.012,

"hpiChange": -0.085,

"creChange": -0.14

}

]

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **Economics research**  **Federal Reserve supervisory scenarios**  **Scenario Committee approvals** | MDL-CR-007 CECL model (scenario weights, unemployment, HPI, CRE)  MDL-CAP-003 Capital Planning & Stress Projection Model  Credit Risk Scoring API (API-10) |

**Changelog**

* v1.6 (2026-05): strategic platform migration
* v1.5 (2025-10): internal severely adverse set

## API-15 Treasury Liquidity Positions API

Aggregates intraday and end-of-day cash, collateral, HQLA and rate-sensitive balance sheet positions by legal entity, including yields and costs by product line. Feeds LCR/NSFR calculators and ALM models.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-15 |
| **Version** | v2.1 |
| **Base path** | /treasury/v2 |
| **Business domain** | Treasury |
| **Owning team** | Treasury Technology |
| **Intended consumers** | Internal only: Treasury/CIO, liquidity risk, ALM and capital models |
| **Data classification** | Restricted - Internal |
| **OAuth scopes** | treasury.positions:read, treasury.hqla:read |
| **Rate limits** | 120 requests/minute |
| **Service-level objective** | 99.95% availability; EOD positions by 21:00 ET |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **GET** | /positions/balance-sheet/{asOf} | Rate-sensitive positions with balance, yield/cost and duration by line. |
| **GET** | /hqla/{asOf} | HQLA by level and legal entity. |
| **GET** | /cash/intraday | Intraday cash position by currency and entity. |

**Example request**

GET /treasury/v2/positions/balance-sheet/2025-12-31?line=CONSUMER\_IB\_DEPOSITS

**Example response (200)**

{

"line": "Consumer interest-bearing deposits",

"balance": 402000,

"units": "USD millions",

"cost": 0.0205,

"modifiedDuration": 2.8

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **General ledger**  **Payments rails (RTP, wires)**  **Securities custody**  **Deposit systems** | MDL-ALM-014 NII Sensitivity Model (balances, yields)  MDL-CAP-003 (liquidity constraints)  LCR and NSFR calculators  Liquidity stress testing engine |

**Changelog**

* v2.1 (2026-01): duration field for EVE

## API-16 Regulatory Reporting API

Provides governed regulatory capital, RWA, leverage exposure and report line items (FR Y-9C, FFIEC 101, FR Y-15), reconciled to the general ledger at legal-entity level. Golden source for Pillar 3.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-16 |
| **Version** | v1.8 |
| **Base path** | /regulatory/v1 |
| **Business domain** | Finance & Regulatory |
| **Owning team** | Finance Technology |
| **Intended consumers** | Internal only: Regulatory Reporting, Capital Management, Disclosure Committee |
| **Data classification** | Restricted - Internal |
| **OAuth scopes** | regulatory:read |
| **Rate limits** | 20 requests/minute |
| **Service-level objective** | 99.9% availability; quarter-end data locked by day 25 |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **GET** | /capital/{asOf} | CET1, Tier 1, Total capital and deductions. |
| **GET** | /rwa/{asOf}?approach=standardized | RWA by exposure type and approach. |
| **GET** | /leverage/{asOf} | Total leverage exposure components and SLR. |
| **GET** | /reports/{reportId}/{asOf} | Line items for a regulatory report schedule. |

**Example request**

GET /regulatory/v1/capital/2026-06-30

**Example response (200)**

{

"asOf": "2026-06-30",

"cet1": 101200,

"standardizedRwa": 668400,

"cet1Ratio": 0.1514,

"units": "USD millions",

"status": "locked"

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **General ledger**  **RWA calculation engines**  **FX Rates API (API-13)** | MDL-CAP-003 Capital Planning & Stress Projection Model (starting CET1, RWA)  FR Y-9C and FFIEC 101 filings  Pillar 3 Disclosures  NII model Tier 1 capital input |

**Changelog**

* v1.8 (2026-03): GL reconciliation status flag
* v1.7 (2025-09): strategic platform migration

## API-17 Statements & Documents API

Lists and retrieves account statements, tax forms and notices as PDF, with e-delivery preferences.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-17 |
| **Version** | v1.4 |
| **Base path** | /documents/v1 |
| **Business domain** | Client Servicing |
| **Owning team** | Digital Platforms Engineering |
| **Intended consumers** | Mobile app, online banking, corporate clients |
| **Data classification** | Confidential - Client Data |
| **OAuth scopes** | documents:read, documents.preferences:write |
| **Rate limits** | 300 requests/minute |
| **Service-level objective** | 99.9% availability |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **GET** | /accounts/{accountId}/statements | List statements by period. |
| **GET** | /documents/{documentId} | Download a document (application/pdf). |
| **PUT** | /preferences | Set paperless preferences. |

**Example request**

GET /documents/v1/accounts/DDA-0044718823/statements?year=2026

**Example response (200)**

{

"data": [

{

"documentId": "STM-2026-05",

"period": "2026-05",

"type": "statement"

}

]

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **Accounts API (API-01)**  **Document archive** | Mobile app  Online banking |

**Changelog**

* v1.4 (2025-12): tax forms

## API-18 Webhooks & Event Notifications API

Lets clients subscribe to signed event notifications (payment status changes, card controls updated, statement available) delivered via HTTPS webhooks with retries and replay.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-18 |
| **Version** | v1.3 |
| **Base path** | /events/v1 |
| **Business domain** | Platform |
| **Owning team** | Developer Platform Engineering |
| **Intended consumers** | All external API consumers |
| **Data classification** | Confidential |
| **OAuth scopes** | events:subscribe, events:read |
| **Rate limits** | 100 subscription changes/hour; delivery up to 10,000 events/second |
| **Service-level objective** | 99.95% delivery within 60 s |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **POST** | /subscriptions | Create a webhook subscription for event types. |
| **GET** | /events | List recent events for replay. |
| **POST** | /subscriptions/{id}/test | Send a test event. |

**Example request**

POST /events/v1/subscriptions

Idempotency-Key: 6f1d2c3e-...

{

"url": "https://client.example/hooks",

"events": [

"payment.settled",

"payment.returned"

]

}

**Example response (200)**

{

"id": "SUB-221",

"secret": "whsec\_\*\*\*\*",

"status": "active"

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **Payments Initiation API (API-03)**  **Real-Time Payments API (API-04)**  **Card Management API (API-06)** | Client systems |

**Changelog**

* v1.3 (2026-02): replay endpoint

# Appendix A. API-to-Model Lineage Matrix

The following matrix shows which APIs are registered as upstream data feeds of the Firm's Tier 1 models. Each model is documented in the model inventory and in the corresponding Excel model workbook.

| **API** | **MDL-ALM-014**  **Net Interest Income Sensitivity Model** | **MDL-CR-007**  **CECL Lifetime Expected Credit Loss Model** | **MDL-CAP-003**  **Capital Planning & Stress Projection Model** |
| --- | --- | --- | --- |
| **API-01 Accounts API** |  |  |  |
| **API-02 Transactions API** |  |  |  |
| **API-03 Payments Initiation API** |  |  |  |
| **API-04 Real-Time Payments API** |  |  |  |
| **API-05 Wire Transfer API** |  |  |  |
| **API-06 Card Management API** |  |  |  |
| **API-07 Customer Identity & KYC API** |  |  |  |
| **API-08 Fraud Risk Signals API** |  |  |  |
| **API-09 Credit Decisioning API** |  |  |  |
| **API-10 Credit Risk Scoring API** |  | Upstream feed |  |
| **API-11 Loan Servicing API** | Upstream feed | Upstream feed |  |
| **API-12 Market Data API** | Upstream feed |  |  |
| **API-13 FX Rates API** |  |  |  |
| **API-14 Macroeconomic Scenario API** |  | Upstream feed | Upstream feed |
| **API-15 Treasury Liquidity Positions API** | Upstream feed |  | Upstream feed |
| **API-16 Regulatory Reporting API** |  |  | Upstream feed |
| **API-17 Statements & Documents API** |  |  |  |
| **API-18 Webhooks & Event Notifications API** |  |  |  |

# Appendix B. Tier 1 Models Consuming Platform APIs

## MDL-ALM-014 Net Interest Income Sensitivity Model

| **Attribute** | **Value** |
| --- | --- |
| **Workbook** | NII\_Sensitivity\_Model.xlsx |
| **Owner** | Corporate Treasury - Asset & Liability Management |
| **Purpose** | Projects 12-month net interest income under parallel rate shocks and economic value of equity (EVE) sensitivity for IRRBB reporting. |
| **Upstream APIs** | API-12 Market Data API; API-15 Treasury Liquidity Positions API; API-11 Loan Servicing API |
| **Disclosed in** | Annual Report - Market Risk Management; Pillar 3 - Interest Rate Risk in the Banking Book |
| **Last validation** | 2025-09-18 |

## MDL-CR-007 CECL Lifetime Expected Credit Loss Model

| **Attribute** | **Value** |
| --- | --- |
| **Workbook** | CECL\_Allowance\_Model.xlsx |
| **Owner** | Consumer & Wholesale Credit Risk - Allowance Methodology |
| **Purpose** | Estimates the allowance for credit losses under ASC 326 (CECL) using probability-weighted macroeconomic scenarios and PD x LGD x EAD. |
| **Upstream APIs** | API-10 Credit Risk Scoring API; API-11 Loan Servicing API; API-14 Macroeconomic Scenario API |
| **Disclosed in** | Annual Report - Allowance for Credit Losses (Note 6); Q2 2026 Earnings Supplement - Credit Trends |
| **Last validation** | 2025-11-04 |

## MDL-CAP-003 Capital Planning & Stress Projection Model

| **Attribute** | **Value** |
| --- | --- |
| **Workbook** | Capital\_Planning\_Model.xlsx |
| **Owner** | Corporate Treasury - Capital Management |
| **Purpose** | Projects CET1 capital, RWA and capital ratios over a nine-quarter horizon under baseline and severely adverse scenarios to size distributions. |
| **Upstream APIs** | API-16 Regulatory Reporting API; API-14 Macroeconomic Scenario API; API-15 Treasury Liquidity Positions API |
| **Disclosed in** | Annual Report - Capital Risk Management; Pillar 3 - Capital Planning and Stress Testing |
| **Last validation** | 2026-02-27 |

# Appendix C. Support and Incident Contacts

| **Topic** | **Channel** | **Hours** |
| --- | --- | --- |
| **Developer onboarding** | developer-portal / onboarding queue | Business days 8:00-18:00 ET |
| **Production incidents (P1/P2)** | API operations hotline, 24x7 status page | 24x7 |
| **Critical data services (API-10, API-11, API-12, API-14, API-15, API-16)** | Data and Technology Risk Committee escalation | 24x7 during quarter close |
| **Security vulnerabilities** | Responsible disclosure program | 24x7 |

*SYNTHETIC DOCUMENT FOR A PROOF OF CONCEPT. Meridian Harbor Financial Corp. is a fictional institution. All names, figures and events are invented and do not describe any real company.*