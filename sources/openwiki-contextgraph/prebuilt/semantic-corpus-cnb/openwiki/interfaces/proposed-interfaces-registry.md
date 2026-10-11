---
type: Interface
entity_id: [EP-PNG-X1, EP-HMS-X1, EP-HMS-X2, EP-TDIP-X1, EP-TDIP-X2]
title: "Proposed Interfaces Registry (do not exist yet)"
description: Registry of payment-estate interfaces that are proposed or referenced but DO NOT EXIST yet, per the estate ground truth; each lists the covering system and purpose.
tags: [registry, proposed, interfaces, gap]
status: absent
---

# Proposed Interfaces Registry (do not exist yet)

Registry of payment-estate interfaces that are proposed or referenced but DO NOT EXIST yet, per the estate ground truth; each lists the covering system and purpose.

- **EP-PNG-X1** (SYS-PNG-GPI): GET /png/gpi/v1/payments/{uetr}/tracker — Internal gpi status API. Status: DOES NOT EXIST
- **EP-HMS-X1** (SYS-PRSP-HMS): GET /prsp/hms/v1/holds/{holdId}/client-view — Client-safe hold status. Status: DOES NOT EXIST
- **EP-HMS-X2** (SYS-PRSP-HMS): POST /prsp/hms/v1/holds/{holdId}/client-attestation — Client attestation (HRC-01). Status: DOES NOT EXIST
- **EP-TDIP-X1** (SYS-TDIP): GET /tdip/insights/v1/wire-history/{clientId}?beneficiaryKey=&rail=&currency= — Client's own similar-wire history stats. Status: DOES NOT EXIST
- **EP-TDIP-X2** (SYS-TDIP): GET /tdip/insights/v1/corridor-stats?currency=&country= — Cohort completion stats w/ DUS-07 suppression. Status: DOES NOT EXIST
