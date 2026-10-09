<!-- source: raw/api_docs/MHFC_Developer_Platform_API_Reference.docx | converted by tools/convert_corpus.py -->
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
