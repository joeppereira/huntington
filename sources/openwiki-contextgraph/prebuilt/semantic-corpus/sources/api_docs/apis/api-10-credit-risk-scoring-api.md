<!-- source: raw/api_docs/MHFC_Developer_Platform_API_Reference.docx | converted by tools/convert_corpus.py -->
## API-10 Credit Risk Scoring API

Serves pool-level and obligor-level probability of default (PD), loss given default (LGD) and exposure at default (EAD) parameters. Provides point-in-time, scenario-conditional parameters for CECL and through-the-cycle parameters for Advanced approaches capital through separate endpoints. Designated a critical data service under BCBS 239.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-10 |
| **Version** | v3.0 |
| **Base path** | /credit-risk/v3 |
| **Business domain** | Credit Risk |
| **Owning team** | Risk Analytics Engineering |
| **Intended consumers** | Internal only: CECL model (MDL-CR-007), regulatory capital calculators, portfolio monitoring |
| **Data classification** | Restricted - Risk Model Data |
| **OAuth scopes** | risk.params:read |
| **Rate limits** | 60 requests/minute; batch extracts via async jobs |
| **Service-level objective** | 99.95% availability; quarterly refresh within T+3 business days |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **GET** | /pools | List portfolio pools (e.g. Credit Card, Residential Mortgage, CRE, C&I). |
| **GET** | /pools/{poolId}/parameters?basis=pit | Point-in-time PD, LGD, remaining life and macro elasticities used by CECL. |
| **GET** | /pools/{poolId}/parameters?basis=ttc | Through-the-cycle PD/LGD with regulatory floors. |
| **POST** | /extracts | Start an asynchronous full-portfolio extract; returns jobId. |

**Example request**

GET /credit-risk/v3/pools/CARD/parameters?basis=pit&asOf=2025-12-31

**Example response (200)**

{

"poolId": "CARD",

"asOf": "2025-12-31",

"basis": "pit",

"basePdAnnual": 0.0374,

"lgd": 0.88,

"remainingLifeYears": 1.7,

"pdElasticityPerPpUnemployment": 0.165,

"modelVersion": "PD-CARD-5.2"

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **Internal ratings systems**  **Loan Servicing API (API-11)**  **Macroeconomic Scenario API (API-14)** | MDL-CR-007 CECL Lifetime Expected Credit Loss Model (CECL\_Allowance\_Model.xlsx)  Advanced approaches credit RWA  Credit Decisioning API (API-09)  Pillar 3 Section 6.3 |

**Changelog**

* v3.0 (2025-10): separate PIT/TTC endpoints; added macro elasticities used by MDL-CR-007
