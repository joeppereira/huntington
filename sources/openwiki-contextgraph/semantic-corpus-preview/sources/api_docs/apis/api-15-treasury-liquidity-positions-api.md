<!-- source: raw/api_docs/MHFC_Developer_Platform_API_Reference.docx | converted by tools/convert_corpus.py -->
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
