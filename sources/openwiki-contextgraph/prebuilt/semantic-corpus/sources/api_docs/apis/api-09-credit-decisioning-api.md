<!-- source: raw/api_docs/MHFC_Developer_Platform_API_Reference.docx | converted by tools/convert_corpus.py -->
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
