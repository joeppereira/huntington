// Builds the Developer Platform API Reference (.docx) from api_catalog.json
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, HeadingLevel, AlignmentType,
  WidthType, ShadingType, BorderStyle, LevelFormat, PageBreak, Header, Footer, PageNumber,
  TableOfContents,
} = require("docx");

const cat = JSON.parse(fs.readFileSync("api_catalog.json", "utf8"));
const BANK = cat.bank;
const NAVY = "0B2545";
const PAGE_W = 12240, MARGIN = 1080, CONTENT = PAGE_W - 2 * MARGIN; // 10080 DXA
const FONT = "Arial";

const border = { style: BorderStyle.SINGLE, size: 4, color: "C9D3DF" };
const borders = { top: border, bottom: border, left: border, right: border };

function p(text, opts = {}) {
  return new Paragraph({ spacing: { after: 120 }, ...opts.para,
    children: [new TextRun({ text, font: FONT, size: 20, ...opts.run })] });
}
function rich(parts, para = {}) {
  return new Paragraph({ spacing: { after: 120 }, ...para,
    children: parts.map(([t, o]) => new TextRun({ text: t, font: FONT, size: 20, ...(o || {}) })) });
}
function h(text, level) { return new Paragraph({ heading: level, children: [new TextRun({ text, font: FONT })] }); }
function bullet(text) {
  return new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 60 },
    children: [new TextRun({ text, font: FONT, size: 20 })] });
}
function code(text) {
  return text.split("\n").map((line, i, arr) => new Paragraph({
    spacing: { after: i === arr.length - 1 ? 160 : 0 },
    shading: { fill: "F2F5F9", type: ShadingType.CLEAR, color: "auto" },
    indent: { left: 200 },
    children: [new TextRun({ text: line === "" ? " " : line, font: "Courier New", size: 17 })],
  }));
}
function cell(text, width, { header = false, bold = false, fill } = {}) {
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: header ? { fill: NAVY, type: ShadingType.CLEAR, color: "auto" } : (fill ? { fill, type: ShadingType.CLEAR, color: "auto" } : undefined),
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: String(text).split("\n").map(line => new Paragraph({ children: [new TextRun({
      text: line, font: FONT, size: 17, bold: header || bold, color: header ? "FFFFFF" : "000000" })] })),
  });
}
function table(headers, rows, widths) {
  const total = widths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: total, type: WidthType.DXA }, columnWidths: widths,
    rows: [new TableRow({ tableHeader: true, children: headers.map((t, i) => cell(t, widths[i], { header: true })) }),
      ...rows.map((r, ri) => new TableRow({ children: r.map((t, i) => cell(t, widths[i], { bold: i === 0, fill: ri % 2 ? "F2F5F9" : undefined })) }))],
  });
}
function kv(rows) { return table(["Attribute", "Value"], rows, [2600, CONTENT - 2600]); }
const spacer = () => new Paragraph({ spacing: { after: 80 }, children: [] });
const fmt = (x) => typeof x === "string" ? x : JSON.stringify(x, null, 2);

const children = [];
// ---------------------------------------------------------------- title
children.push(new Paragraph({ spacing: { before: 2400, after: 200 }, children: [new TextRun({ text: BANK.name.toUpperCase(), font: FONT, size: 24, bold: true, color: NAVY })] }));
children.push(new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: "Developer Platform API Reference", font: FONT, size: 56, bold: true, color: NAVY })] }));
children.push(p("Catalog of 18 production APIs: accounts, payments, cards, identity, fraud, credit, market data, treasury and regulatory reporting", { run: { size: 26, color: "4F7CAC" } }));
children.push(p("Document version 3.6 - July 2026 - Owner: Developer Platform Engineering", { run: { size: 20 } }));
children.push(p(BANK.disclaimer, { run: { size: 18, italics: true, color: "8A1C1C" }, para: { spacing: { before: 1600 } } }));
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h("Contents", HeadingLevel.HEADING_1));
children.push(new TableOfContents("Contents", { hyperlink: true, headingStyleRange: "1-2" }));
children.push(new Paragraph({ children: [new PageBreak()] }));

// ---------------------------------------------------------------- platform overview
children.push(h("1. Platform Overview", HeadingLevel.HEADING_1));
children.push(p(`The ${BANK.short} Developer Platform exposes the Firm's banking, payments, risk and finance capabilities as versioned REST APIs. The same APIs serve three audiences: internal applications (mobile app, online banking, servicing tools), external clients and partners (corporate treasurers, fintechs, data aggregators), and internal risk and finance processes, including Tier 1 risk models and regulatory reporting.`));
children.push(p("APIs that feed Tier 1 models or regulatory disclosures are classified as critical data services under the Firm's BCBS 239 program. They carry named data owners, documented data-quality rules, enhanced change management, and registration in the model inventory, so that any breaking change automatically triggers a model change review by Model Risk Governance & Review (MRGR)."));
children.push(h("1.1 Environments", HeadingLevel.HEADING_2));
children.push(table(["Environment", "Base URL", "Purpose"], [
  ["Sandbox", "https://sandbox.api.meridianharbor.example", "Synthetic data; self-service onboarding; no SLA"],
  ["Certification", "https://cert.api.meridianharbor.example", "Pre-production testing with masked data"],
  ["Production", "https://api.meridianharbor.example", "Live traffic; SLAs apply"],
  ["Internal (risk & finance)", "https://internal.api.mhfc.example", "Restricted APIs (API-10, API-14, API-15, API-16); private network only"],
], [2200, 4200, 3680]));
children.push(spacer());
children.push(h("1.2 Authentication and authorization", HeadingLevel.HEADING_2));
children.push(p("All APIs use OAuth 2.0. Server-to-server clients use the client-credentials grant with mutual TLS (certificate-bound access tokens). Customer-facing integrations use the authorization-code grant with PKCE and customer consent. Access tokens are JWTs valid for 15 minutes. Scopes are listed per API; least-privilege scopes are enforced."));
children.push(...code("POST /oauth2/token\nContent-Type: application/x-www-form-urlencoded\n\ngrant_type=client_credentials&scope=accounts:read%20accounts.balances:read"));
children.push(h("1.3 Versioning and deprecation", HeadingLevel.HEADING_2));
children.push(p("Major versions appear in the path (for example /accounts/v3). Minor versions are additive and backward compatible. A major version is supported for at least 12 months after its successor reaches general availability; deprecation is announced via the Sunset header and the developer portal."));
children.push(h("1.4 Rate limiting, idempotency and pagination", HeadingLevel.HEADING_2));
children.push(bullet("Rate limits are applied per client and per API; responses include X-RateLimit-Limit, X-RateLimit-Remaining and Retry-After on HTTP 429."));
children.push(bullet("All POST operations that move money or create resources require an Idempotency-Key header (UUID); keys are retained for 24 hours."));
children.push(bullet("List endpoints use cursor-based pagination via limit and cursor query parameters; responses include nextCursor."));
children.push(bullet("All timestamps are ISO 8601 UTC; monetary amounts are decimal numbers in the stated currency; risk and finance APIs state units (typically USD millions) in the payload."));
children.push(h("1.5 Error format", HeadingLevel.HEADING_2));
children.push(...code(JSON.stringify({ error: { code: "insufficient_scope", message: "Token lacks scope payments:write", requestId: "req_8f2c01" } }, null, 2)));
children.push(table(["HTTP status", "Error code", "Meaning"], cat.errors, [1400, 2400, 6280]));
children.push(new Paragraph({ children: [new PageBreak()] }));

// ---------------------------------------------------------------- catalog
children.push(h("2. API Catalog Summary", HeadingLevel.HEADING_1));
children.push(table(["ID", "API", "Version", "Domain", "Owner"],
  cat.apis.map(a => [a.id, a.name, a.version, a.domain, a.owner]), [900, 3000, 900, 2600, 2680]));
children.push(new Paragraph({ children: [new PageBreak()] }));

// ---------------------------------------------------------------- each API
children.push(h("3. API Reference", HeadingLevel.HEADING_1));
cat.apis.forEach((a, idx) => {
  if (idx > 0) children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(h(`${a.id} ${a.name}`, HeadingLevel.HEADING_2));
  children.push(p(a.summary));
  children.push(kv([
    ["API ID", a.id], ["Version", a.version], ["Base path", a.base], ["Business domain", a.domain],
    ["Owning team", a.owner], ["Intended consumers", a.audience], ["Data classification", a.classification],
    ["OAuth scopes", a.scopes.join(", ")], ["Rate limits", a.rate], ["Service-level objective", a.slo],
  ]));
  children.push(spacer());
  children.push(rich([["Endpoints", { bold: true, color: NAVY, size: 22 }]]));
  children.push(table(["Method", "Path", "Description"], a.endpoints, [1000, 3800, 5280]));
  children.push(spacer());
  children.push(rich([["Example request", { bold: true, color: NAVY, size: 22 }]]));
  children.push(...code(typeof a.example_req === "string" ? a.example_req : `POST ${a.base}${a.endpoints.find(e => e[0] === "POST" || e[0] === "PUT")?.[1] || ""}\nIdempotency-Key: 6f1d2c3e-...\n\n${fmt(a.example_req)}`));
  children.push(rich([["Example response (200)", { bold: true, color: NAVY, size: 22 }]]));
  children.push(...code(fmt(a.example_resp)));
  children.push(rich([["Data lineage", { bold: true, color: NAVY, size: 22 }]]));
  children.push(table(["Upstream sources", "Downstream consumers"],
    [[a.upstream.join("\n"), a.downstream.join("\n")]], [CONTENT / 2, CONTENT / 2]));
  children.push(spacer());
  children.push(rich([["Changelog", { bold: true, color: NAVY, size: 22 }]]));
  a.changelog.forEach(c => children.push(bullet(c)));
});
children.push(new Paragraph({ children: [new PageBreak()] }));

// ---------------------------------------------------------------- appendix
children.push(h("Appendix A. API-to-Model Lineage Matrix", HeadingLevel.HEADING_1));
children.push(p("The following matrix shows which APIs are registered as upstream data feeds of the Firm's Tier 1 models. Each model is documented in the model inventory and in the corresponding Excel model workbook."));
const models = cat.models;
const rows = cat.apis.map(a => [a.id + " " + a.name, ...models.map(m => m.apis.some(x => x.startsWith(a.id + " ")) ? "Upstream feed" : "")]);
children.push(table(["API", ...models.map(m => `${m.id}\n${m.name}`)], rows, [3480, 2200, 2200, 2200]));
children.push(spacer());
children.push(h("Appendix B. Tier 1 Models Consuming Platform APIs", HeadingLevel.HEADING_1));
models.forEach(m => {
  children.push(h(`${m.id} ${m.name}`, HeadingLevel.HEADING_2));
  children.push(kv([["Workbook", m.file], ["Owner", m.owner], ["Purpose", m.purpose], ["Upstream APIs", m.apis.join("; ")],
    ["Disclosed in", m.reports.join("; ")], ["Last validation", m.last_validation]]));
  children.push(spacer());
});
children.push(h("Appendix C. Support and Incident Contacts", HeadingLevel.HEADING_1));
children.push(table(["Topic", "Channel", "Hours"], [
  ["Developer onboarding", "developer-portal / onboarding queue", "Business days 8:00-18:00 ET"],
  ["Production incidents (P1/P2)", "API operations hotline, 24x7 status page", "24x7"],
  ["Critical data services (API-10, API-11, API-12, API-14, API-15, API-16)", "Data and Technology Risk Committee escalation", "24x7 during quarter close"],
  ["Security vulnerabilities", "Responsible disclosure program", "24x7"],
], [3800, 3800, 2480]));
children.push(p(BANK.disclaimer, { run: { italics: true, size: 18, color: "8A1C1C" }, para: { spacing: { before: 400 } } }));

const doc = new Document({
  creator: BANK.name, title: "Developer Platform API Reference",
  styles: {
    default: { document: { run: { font: FONT, size: 20 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: FONT, color: NAVY }, paragraph: { spacing: { before: 240, after: 160 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: FONT, color: "13315C" }, paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 1 } },
    ],
  },
  numbering: { config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•",
    alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: PAGE_W, height: 15840 }, margin: { top: 1080, right: MARGIN, bottom: 1080, left: MARGIN } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT,
      children: [new TextRun({ text: `${BANK.short} Developer Platform - API Reference v3.6`, font: FONT, size: 16, color: "555555" })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
      new TextRun({ text: "Synthetic document - fictional institution - page ", font: FONT, size: 16, color: "8A1C1C" }),
      new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: "8A1C1C" })] })] }) },
    children,
  }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(process.argv[2], buf); console.log("ok"); });
