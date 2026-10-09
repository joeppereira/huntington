<!-- source: raw/api_docs/MHFC_Developer_Platform_API_Reference.docx | converted by tools/convert_corpus.py -->
## API-17 Statements & Documents API

Lists and retrieves account statements, tax forms and notices as PDF, with e-delivery preferences.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-17 |
| **Version** | v1.4 |
| **Base path** | /documents/v1 |
| **Business domain** | Client Servicing |
| **Owning team** | Digital Platforms Engineering |
| **Intended consumers** | Mobile app, online banking, corporate clients |
| **Data classification** | Confidential - Client Data |
| **OAuth scopes** | documents:read, documents.preferences:write |
| **Rate limits** | 300 requests/minute |
| **Service-level objective** | 99.9% availability |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **GET** | /accounts/{accountId}/statements | List statements by period. |
| **GET** | /documents/{documentId} | Download a document (application/pdf). |
| **PUT** | /preferences | Set paperless preferences. |

**Example request**

GET /documents/v1/accounts/DDA-0044718823/statements?year=2026

**Example response (200)**

{

"data": [

{

"documentId": "STM-2026-05",

"period": "2026-05",

"type": "statement"

}

]

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **Accounts API (API-01)**  **Document archive** | Mobile app  Online banking |

**Changelog**

* v1.4 (2025-12): tax forms
