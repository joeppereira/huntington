---
type: Policy
entity_id: SEC-STD-22
title: "Digital Channel External Sharing & Step-Up Standard (SEC-STD-22)"
description: InfoSec standard governing external sharing of client transaction data from digital channels (links or documents shared with non-users) and step-up authentication requirements; any external-sharing capability requires an InfoSec design review under this standard plus a Privacy Impact Assessment.
tags: [infosec, external-sharing, step-up, security-standard, cbo, wire-center]
aliases: [external sharing standard, step-up standard, share with recipient]
status: live
governed_pages_note: referenced by CBO Wire Center current-state architecture (CBO-ARCH-WC-4.1 §security)
described_by: [openwiki/documents/cbo-arch-wc-4.1.md]
---

# Digital Channel External Sharing & Step-Up Standard (SEC-STD-22)

InfoSec standard for CNB digital channels. Per the CBO Wire Center current-state
architecture (CBO-ARCH-WC-4.1):

- External sharing of client transaction data — links or documents shared with
  non-users — is **not supported** in CBO today; any such capability requires an
  **InfoSec design review under SEC-STD-22** and a **Privacy Impact Assessment**.
- Wire release requires **step-up authentication** (EP-AUTH-01) and client-configured
  dual approval above client thresholds; step-up requirements fall under this standard.

Relevant to any wire-tracking feature that lets a client share a tracking link with a
payment recipient (see [POL-FCC-014](pol-fcc-014.md) for the customer-communication
and disclosure side of the same feature class).
