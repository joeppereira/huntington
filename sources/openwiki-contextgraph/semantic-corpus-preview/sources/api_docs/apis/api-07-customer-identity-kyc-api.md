<!-- source: raw/api_docs/MHFC_Developer_Platform_API_Reference.docx | converted by tools/convert_corpus.py -->
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
