<!-- source: raw/api_docs/MHFC_Developer_Platform_API_Reference.docx | converted by tools/convert_corpus.py -->
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
