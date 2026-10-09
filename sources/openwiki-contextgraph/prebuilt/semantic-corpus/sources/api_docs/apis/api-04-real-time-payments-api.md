<!-- source: raw/api_docs/MHFC_Developer_Platform_API_Reference.docx | converted by tools/convert_corpus.py -->
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
