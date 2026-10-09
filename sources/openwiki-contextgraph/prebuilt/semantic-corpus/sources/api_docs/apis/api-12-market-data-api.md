<!-- source: raw/api_docs/MHFC_Developer_Platform_API_Reference.docx | converted by tools/convert_corpus.py -->
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
