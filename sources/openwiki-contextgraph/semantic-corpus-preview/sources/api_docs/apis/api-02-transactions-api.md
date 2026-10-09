<!-- source: raw/api_docs/MHFC_Developer_Platform_API_Reference.docx | converted by tools/convert_corpus.py -->
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
