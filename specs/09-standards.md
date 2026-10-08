# 09 — Standards: Security, Privacy, Operational

The standards the customer-facing app (`08-app-architecture.md`) must meet. These are
requirements on the *running product*, distinct from the generation pipeline's gates
(`04-validation.md`) — though several deliberately rhyme with them (the denylist, the
fail-closed posture), because the pipeline gates exist to stop violations of these
standards from ever being designed in.

Each standard is testable. "We intend to" is not a standard; every item below is
phrased so a reviewer can check it against the system and answer yes or no.

---

## A. Security standards

1. **Inherited auth only.** The app uses the Online Treasury Channel's SSO, session,
   and step-up mechanisms. It introduces no credentials, tokens, or session stores of
   its own.
2. **Entitlement enforced server-side per request.** Every BFF endpoint checks the
   caller's entitlement to the specific account/wire in the request. The frontend's
   hiding of unauthorized content is UX, never the control.
3. **Tipping-off suppression is a data-layer control.** The internal fraud/risk hold
   code is mapped to vetted client-safe copy inside the BFF (or deeper). The raw code
   has no field in any browser-bound contract, appears in no client-visible error, no
   URL, no browser-reachable log. This implements REQ-EX-01's critical security
   requirement structurally, not editorially.
4. **The write path is minimal and hardened.** Exactly one money-affecting operation
   (held-wire Confirm/Reject), with step-up auth, per-request entitlement, idempotency,
   and audit-before-ack per `08-app-architecture.md` §5. Any future write operation is
   a spec change to 08, not a quiet endpoint addition.
5. **Fail closed.** Any safety dependency (entitlements, step-up, audit) being
   unavailable makes the protected action unavailable. No degraded mode ever bypasses a
   control.
6. **Standard web hardening.** TLS everywhere, CSP on the SPA, no sensitive data in
   URLs or browser storage beyond the channel's session token, dependency and container
   scanning in CI, secrets in the bank's secret manager — never in code, config files,
   or environment committed anywhere.
7. **Share/export features are scoped artifacts.** REQ-SS-03's "share tracking status
   with the counterparty" produces a time-limited, single-wire, read-only artifact
   containing only counterparty-appropriate fields — never a session, never a link into
   the authenticated channel.

## B. Privacy standards

1. **Data minimization per contract.** Browser-bound contracts (`08` §3) carry only
   fields a view renders. No "send everything, let the frontend pick."
2. **Masking at the contract level.** Account/routing identifiers are masked in the
   payload itself; full values have no browser-bound field.
3. **No client-side analytics on payment data.** Usage analytics, if any, capture
   interaction events (view opened, filter used) — never wire amounts, counterparty
   names, account identifiers, or hold reasons. Analytics payloads are reviewable
   against this rule.
4. **Logs are privacy-safe by schema.** BFF logs reference wires by internal opaque id;
   log schemas (not log discipline) exclude amounts-with-counterparty combinations,
   full account numbers, and hold codes from anything shipped to shared log
   infrastructure. Audit events (which legitimately need detail) go to the audit store
   with its own access control, not to general logs.
5. **Retention follows the bank's record-retention schedule.** The app stores no
   client data of its own beyond cache (bounded TTL) and subscriptions (user-deletable);
   the systems of record retain per existing policy. The share-artifact (A.7) expires;
   expiry is enforced server-side.
6. **Counterparty privacy in shared views.** A shared tracking view shows the
   recipient what the recipient may see (status, expected timing) — not the
   originator's account details, fee breakdowns, or internal references.

## C. Operational standards

1. **Observability per upstream.** The BFF exposes health and per-adapter
   latency/error metrics (payments core, gpi, alerts) separately, so "the app is slow"
   is always attributable to a specific dependency in one glance.
2. **Latency budgets are alerted, not aspirational.** The p95 budgets in `08` §4 are
   encoded as SLO alerts; a sustained breach pages the owning team.
3. **Degraded states are tested states.** Every designed degradation in `08` §6 has an
   automated test that kills the mock upstream and asserts the specified UI state —
   degradation claims without tests rot.
4. **gpi call budget.** SWIFT gpi API usage is rate-limited and budgeted at the BFF
   with cache-hit-ratio monitoring; a cache regression shows up as a cost/quota alert
   before it shows up as an outage.
5. **Idempotent, incident-ready deploys.** Blue/green or rolling deploys with instant
   rollback; the mock-adapter mode doubles as the smoke-test environment on every
   deploy.
6. **Audit trail completeness is monitored.** Every Confirm/Reject must have a
   matching audit event; a reconciliation job verifies this continuously, and any
   mismatch is a severity-1 operational incident (the action path is supposed to make
   this impossible — the monitor exists to prove it stays impossible).
7. **Runtime indicators join the pipeline indicators.** `07-indicators.md` tracks the
   generation pipeline; the running app adds its own lagging set — support-inquiry
   volume on wire status (the PRD's core objective is reducing it), held-wire
   self-service resolution rate, gpi cache hit ratio, SLO attainment. Same discipline:
   security/audit incidents are never averaged into trend lines.

---

## How these standards connect back to the pipeline

The generation pipeline is the first line of defense for several of these: the
audience gate (spec 01) keeps internal tooling out of the customer surface; the
denylist gate (spec 04) keeps tipping-off language out of designed copy; the component
tree's `degraded` interaction states (spec 08 §6) mean operational honesty is designed
and reviewed, not improvised in production. When a standard here changes, check
whether a pipeline gate should change with it — the two layers drift apart otherwise.
