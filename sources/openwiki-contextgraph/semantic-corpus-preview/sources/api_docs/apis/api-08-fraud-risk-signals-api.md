<!-- source: raw/api_docs/MHFC_Developer_Platform_API_Reference.docx | converted by tools/convert_corpus.py -->
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
