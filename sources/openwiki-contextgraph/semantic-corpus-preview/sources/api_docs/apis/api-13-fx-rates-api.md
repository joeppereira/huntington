<!-- source: raw/api_docs/MHFC_Developer_Platform_API_Reference.docx | converted by tools/convert_corpus.py -->
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
