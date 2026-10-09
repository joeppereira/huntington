<!-- source: raw/api_docs/MHFC_Developer_Platform_API_Reference.docx | converted by tools/convert_corpus.py -->
## API-05 Wire Transfer API

Initiates domestic (Fedwire) and cross-border (SWIFT MT/ISO 20022 MX) wires with FX conversion using rates from the FX Rates API. Supports payment tracking via UETR.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-05 |
| **Version** | v2.0 |
| **Base path** | /wires/v2 |
| **Business domain** | Payments |
| **Owning team** | Global Payments Technology |
| **Intended consumers** | CIB corporate and institutional clients |
| **Data classification** | Restricted - Financial Transaction |
| **OAuth scopes** | wires:write, wires:read |
| **Rate limits** | 120 requests/minute per client |
| **Service-level objective** | 99.99% availability during operating hours |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **POST** | /wires | Create a domestic or international wire. |
| **GET** | /wires/{wireId} | Status and UETR tracking events. |
| **POST** | /wires/quotes | Get an FX quote valid for 60 seconds for a cross-currency wire. |

**Example request**

POST /wires/v2/wires

Idempotency-Key: 6f1d2c3e-...

{

"debtorAccount": "DDA-9100044",

"beneficiary": {

"name": "Rhein Logistik GmbH",

"iban": "DE89\*\*\*\*3000"

},

"amount": 250000,

"currency": "EUR",

"quoteId": "Q-77e2"

}

**Example response (200)**

{

"wireId": "W-31f0",

"uetr": "e0a4...c1",

"status": "screening",

"rate": 0.9214

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **FX Rates API (API-13)**  **Sanctions screening**  **Fraud Risk Signals API (API-08)** | Fedwire  SWIFT  General ledger  Treasury Liquidity Positions API (API-15) |

**Changelog**

* v2.0 (2025-11): ISO 20022 MX migration complete
