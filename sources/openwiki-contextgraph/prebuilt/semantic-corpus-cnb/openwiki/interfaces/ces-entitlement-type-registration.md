---
type: Interface
entity_id: EP-CES-02
title: "CES Entitlement Type Registration API (EP-CES-02)"
description: Admin endpoint of the Commercial Entitlements Service (POST /ces/v2/entitlement-types) for registering new entitlement types - GA, admin-only, with InfoSec review required before a type may be made grantable by client administrators.
tags: [ces, entitlements, ep-ces-02, admin-api, infosec-review, cbo-platform]
owned_by: [openwiki/teams/cbo-platform-entitlements.md]
part_of: openwiki/systems/commercial-entitlements-service.md
status: live
status_note: admin
---

## Overview

**EP-CES-02** (`POST /ces/v2/entitlement-types`) is the admin registration
endpoint of the [Commercial Entitlements Service (CES)](../systems/commercial-entitlements-service.md).
It is GA and admin-scoped: platform teams use it to register a new entitlement
type before that type can be looked up per user through the
[CES Entitlements API (EP-CES-01)](ces-entitlements-api.md).

## Usage and constraints

| Field | Value |
|---|---|
| Method / path | `POST /ces/v2/entitlement-types` |
| Purpose | Register a new entitlement type |
| Status | GA (admin) |
| Governance | InfoSec review required for client-admin-grantable types |

Registering a type that client administrators will be able to grant themselves
(as opposed to bank-managed assignment) **requires an Information Security
review** before go-live. Existing wire entitlement types served by CES include
`WIRE_VIEW`, `WIRE_INITIATE`, `WIRE_APPROVE`, and `WIRE_RELEASE`.
