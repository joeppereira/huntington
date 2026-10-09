<!-- source: raw/api_docs/MHFC_Developer_Platform_API_Reference.docx | converted by tools/convert_corpus.py -->
## API-14 Macroeconomic Scenario API

Distributes approved macroeconomic scenario sets (paths for unemployment, GDP, house prices, CRE prices, rates, spreads) and their probability weights. Scenario sets are versioned and locked after Scenario Committee approval. Migrated to the strategic data platform in 2Q26, cutting load time from six hours to under forty minutes.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-14 |
| **Version** | v1.6 |
| **Base path** | /scenarios/v1 |
| **Business domain** | Risk & Finance |
| **Owning team** | Risk Analytics Engineering |
| **Intended consumers** | Internal only: CECL, capital planning, stress testing, ALM |
| **Data classification** | Restricted - Internal |
| **OAuth scopes** | scenarios:read, scenarios:approve |
| **Rate limits** | 30 requests/minute |
| **Service-level objective** | 99.9% availability; new set published within 1 business day of approval |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **GET** | /scenario-sets | List scenario sets (e.g. MSC-2025Q4, SA-2025-INT). |
| **GET** | /scenario-sets/{setId} | Scenarios, weights and approval metadata. |
| **GET** | /scenario-sets/{setId}/paths/{variable} | Quarterly path for a variable in each scenario. |

**Example request**

GET /scenarios/v1/scenario-sets/MSC-2025Q4

**Example response (200)**

{

"setId": "MSC-2025Q4",

"approved": "2025-12-15",

"scenarios": [

{

"name": "Upside",

"weight": 0.2,

"peakUnemployment": 0.038,

"realGdp2026": 0.026,

"hpiChange": 0.045,

"creChange": 0.03

},

{

"name": "Baseline",

"weight": 0.5,

"peakUnemployment": 0.044,

"realGdp2026": 0.017,

"hpiChange": 0.022,

"creChange": -0.01

},

{

"name": "Downside",

"weight": 0.3,

"peakUnemployment": 0.068,

"realGdp2026": -0.012,

"hpiChange": -0.085,

"creChange": -0.14

}

]

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **Economics research**  **Federal Reserve supervisory scenarios**  **Scenario Committee approvals** | MDL-CR-007 CECL model (scenario weights, unemployment, HPI, CRE)  MDL-CAP-003 Capital Planning & Stress Projection Model  Credit Risk Scoring API (API-10) |

**Changelog**

* v1.6 (2026-05): strategic platform migration
* v1.5 (2025-10): internal severely adverse set
