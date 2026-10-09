<!-- source: raw/api_docs/MHFC_Developer_Platform_API_Reference.docx | converted by tools/convert_corpus.py -->
## API-18 Webhooks & Event Notifications API

Lets clients subscribe to signed event notifications (payment status changes, card controls updated, statement available) delivered via HTTPS webhooks with retries and replay.

| **Attribute** | **Value** |
| --- | --- |
| **API ID** | API-18 |
| **Version** | v1.3 |
| **Base path** | /events/v1 |
| **Business domain** | Platform |
| **Owning team** | Developer Platform Engineering |
| **Intended consumers** | All external API consumers |
| **Data classification** | Confidential |
| **OAuth scopes** | events:subscribe, events:read |
| **Rate limits** | 100 subscription changes/hour; delivery up to 10,000 events/second |
| **Service-level objective** | 99.95% delivery within 60 s |

**Endpoints**

| **Method** | **Path** | **Description** |
| --- | --- | --- |
| **POST** | /subscriptions | Create a webhook subscription for event types. |
| **GET** | /events | List recent events for replay. |
| **POST** | /subscriptions/{id}/test | Send a test event. |

**Example request**

POST /events/v1/subscriptions

Idempotency-Key: 6f1d2c3e-...

{

"url": "https://client.example/hooks",

"events": [

"payment.settled",

"payment.returned"

]

}

**Example response (200)**

{

"id": "SUB-221",

"secret": "whsec\_\*\*\*\*",

"status": "active"

}

**Data lineage**

| **Upstream sources** | **Downstream consumers** |
| --- | --- |
| **Payments Initiation API (API-03)**  **Real-Time Payments API (API-04)**  **Card Management API (API-06)** | Client systems |

**Changelog**

* v1.3 (2026-02): replay endpoint
