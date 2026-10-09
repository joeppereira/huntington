<!-- source: raw/api_docs/MHFC_Developer_Platform_API_Reference.docx | converted by tools/convert_corpus.py -->
## API-06 Card Management API

Manages debit and credit card lifecycle: issuance, activation, lock/unlock, spend controls, digital wallet provisioning and replacement. PAN data is tokenized; raw card numbers are never returned.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-06 |
| **Version** | v2.6 |
| **Base path** | /cards/v2 |
| **Business domain** | Card Services |
| **Owning team** | Card Technology |
| **Intended consumers** | Mobile app, fintech and co-brand partners |
| **Data classification** | Restricted - PCI |
| **OAuth scopes** | cards:read, cards:write, cards.controls:write |
| **Rate limits** | 800 requests/minute per client |
| **Service-level objective** | 99.97% availability; p95 latency 220 ms |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **GET** | /cards/{cardToken} | Card status, product and expiry (tokenized). |
| **POST** | /cards/{cardToken}/lock | Temporarily lock a card. |
| **PUT** | /cards/{cardToken}/controls | Set merchant-category, geography and amount controls. |
| **POST** | /cards/{cardToken}/wallet-provisioning | Provision to a digital wallet. |

**Example request**

POST /cards/v2/cards/{cardToken}/lock

Idempotency-Key: 6f1d2c3e-...

{

"controls": {

"blockedCategories": [

"GAMBLING"

],

"dailyLimit": 1500,

"allowedCountries": [

"US",

"CA"

]

}

}

**Example response (200)**

{

"cardToken": "tok\_card\_83jd",

"controlsVersion": 7,

"status": "active"

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **Card processing platform**  **Customer Identity & KYC API (API-07)** | Card authorization system  Digital wallets  Webhooks & Event Notifications API (API-18) |

**Changelog**

* v2.6 (2026-04): geography controls
* v2.5 (2025-08): co-brand partner scopes
