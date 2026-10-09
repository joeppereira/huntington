<!-- source: raw/api_docs/MHFC_Developer_Platform_API_Reference.docx | converted by tools/convert_corpus.py -->
## API-16 Regulatory Reporting API

Provides governed regulatory capital, RWA, leverage exposure and report line items (FR Y-9C, FFIEC 101, FR Y-15), reconciled to the general ledger at legal-entity level. Golden source for Pillar 3.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-16 |
| **Version** | v1.8 |
| **Base path** | /regulatory/v1 |
| **Business domain** | Finance & Regulatory |
| **Owning team** | Finance Technology |
| **Intended consumers** | Internal only: Regulatory Reporting, Capital Management, Disclosure Committee |
| **Data classification** | Restricted - Internal |
| **OAuth scopes** | regulatory:read |
| **Rate limits** | 20 requests/minute |
| **Service-level objective** | 99.9% availability; quarter-end data locked by day 25 |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **GET** | /capital/{asOf} | CET1, Tier 1, Total capital and deductions. |
| **GET** | /rwa/{asOf}?approach=standardized | RWA by exposure type and approach. |
| **GET** | /leverage/{asOf} | Total leverage exposure components and SLR. |
| **GET** | /reports/{reportId}/{asOf} | Line items for a regulatory report schedule. |

**Example request**

GET /regulatory/v1/capital/2026-06-30

**Example response (200)**

{

"asOf": "2026-06-30",

"cet1": 101200,

"standardizedRwa": 668400,

"cet1Ratio": 0.1514,

"units": "USD millions",

"status": "locked"

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **General ledger**  **RWA calculation engines**  **FX Rates API (API-13)** | MDL-CAP-003 Capital Planning & Stress Projection Model (starting CET1, RWA)  FR Y-9C and FFIEC 101 filings  Pillar 3 Disclosures  NII model Tier 1 capital input |

**Changelog**

* v1.8 (2026-03): GL reconciliation status flag
* v1.7 (2025-09): strategic platform migration
