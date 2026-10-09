<!-- source: raw/api_docs/MHFC_Developer_Platform_API_Reference.docx | converted by tools/convert_corpus.py -->
## API-03 Payments Initiation API

Initiates ACH, book transfer and check payments individually or in bulk files, with ISO 20022 structured remittance. All payments are screened by sanctions and the Fraud Risk Signals API before release.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-03 |
| **Version** | v3.2 |
| **Base path** | /payments/v3 |
| **Business domain** | Payments |
| **Owning team** | Global Payments Technology |
| **Intended consumers** | Corporate clients, ERP connectors, internal treasury applications |
| **Data classification** | Restricted - Financial Transaction |
| **OAuth scopes** | payments:write, payments:read, payments.bulk:write |
| **Rate limits** | 300 requests/minute per client; bulk files up to 50,000 items |
| **Service-level objective** | 99.98% availability; p95 latency 400 ms |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **POST** | /payments | Create a single payment; requires Idempotency-Key header. |
| **POST** | /payment-files | Upload a bulk payment file (ISO 20022 pain.001 or CSV). |
| **GET** | /payments/{paymentId} | Retrieve status: received, screened, released, settled, returned. |
| **POST** | /payments/{paymentId}/cancel | Cancel a payment before release. |

**Example request**

POST /payments/v3/payments

Idempotency-Key: 6f1d2c3e-...

{

"debtorAccount": "DDA-7700112",

"creditor": {

"name": "Acme Supplies LLC",

"routing": "021000021",

"account": "\*\*\*\*4410"

},

"amount": {

"value": 12500,

"currency": "USD"

},

"rail": "ACH\_SAME\_DAY",

"remittance": {

"invoice": "INV-2026-0611"

}

}

**Example response (200)**

{

"paymentId": "PAY-55ab91",

"status": "received",

"fraudScore": 0.04,

"expectedSettlement": "2026-07-01"

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **Accounts API (API-01) for funds check**  **Sanctions screening**  **Fraud Risk Signals API (API-08)** | ACH operator  Webhooks & Event Notifications API (API-18)  General ledger |

**Changelog**

* v3.2 (2026-05): ISO 20022 structured remittance
* v3.1 (2025-10): same-day ACH rail
