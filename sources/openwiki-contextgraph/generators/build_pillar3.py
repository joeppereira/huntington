"""Pillar 3 Regulatory Capital and Risk Disclosures (YE2025) for the fictional Meridian Harbor Financial Corp."""
import json
from reportlab.platypus import Spacer, PageBreak, CondPageBreak
from pdfkit_lib import *
import bankdata as B

O = json.load(open("model_outputs.json"))
CAP = B.CAPITAL
REQ = B.CAP_REQ
nm = B.BANK["name"]
sh = B.BANK["short"]
RWA = CAP["Standardized RWA"][0]

story = []
story += cover("Pillar 3 Regulatory<br/>Capital Disclosures", "Basel III Pillar 3 disclosures for the fiscal year "
               "ended December 31, 2025", "Published March 2026",
               ["Prepared under 12 CFR 217 Subpart D, Section 217.61-63 and Subpart E, Section 217.171-173"])
story += toc_page()

# 1 Intro
story.append(h1("1. Introduction and Scope"))
story += ps(
    f"This report presents the Pillar 3 disclosures of {nm} (\"{sh}\" or \"the Firm\") as of December 31, 2025. "
    "Pillar 3 complements the minimum capital requirements (Pillar 1) and the supervisory review process (Pillar 2) "
    "of the Basel III framework by requiring banks to publish information on their capital adequacy, risk "
    "exposures and risk management processes, enabling market participants to assess the Firm's capital "
    "position and risk profile.",
    "The disclosures cover the consolidated bank holding company. The Firm's principal insured depository "
    "institution, Meridian Harbor Bank, N.A., is subject to separate capital requirements and is well capitalized. "
    "There are no restrictions or impediments on the transfer of funds or regulatory capital within the Firm "
    "beyond those generally applicable to U.S. bank holding companies.",
    "The Firm is an advanced approaches banking organization and calculates risk-weighted assets under both the "
    "Standardized and Advanced approaches. The lower of each ratio under the two approaches - currently the "
    "Standardized approach - is used to assess capital adequacy (the \"Collins Floor\"). These disclosures are not "
    "required to be audited, but are subject to the Firm's disclosure controls and the review of the Disclosure "
    "Committee, and are consistent with information reported in the FR Y-9C, FFIEC 101 and FR Y-15.",
)
rows = [["Pillar 3 requirement", "Location in this report"],
        ["Scope of application", "Section 1"], ["Capital structure", "Section 3"], ["Capital adequacy", "Section 4"],
        ["Capital conservation and buffers", "Section 4.2"], ["Leverage", "Section 5"],
        ["Credit risk: general disclosures", "Section 6"], ["Counterparty credit risk", "Section 7"],
        ["Securitization", "Section 8"], ["Market risk", "Section 9"], ["Operational risk", "Section 10"],
        ["Interest rate risk in the banking book", "Section 11"], ["Liquidity (LCR and NSFR)", "Section 12"],
        ["Stress testing and capital planning", "Section 13"], ["Model risk and data governance", "Sections 14-15"]]
story.append(table(rows, [0.55, 0.45], first_col_left=True))

# 2 Governance
story.append(h1("2. Risk Management Framework and Governance"))
story += ps(
    "The Firm's risk management framework is designed to identify, measure, monitor, manage and report all "
    "material risks. The Board of Directors oversees risk through its Risk Committee, Audit Committee and "
    "Compensation Committee. The Chief Risk Officer, "
    f"{B.BANK['cro']}, reports to the Chief Executive Officer and to the Board Risk Committee, and leads an "
    "independent risk management function organized by risk stripe (credit, market, liquidity, model, "
    "operational, compliance and reputational).",
    "The Firm applies the three lines of defense model. The lines of business and Treasury/CIO are the first line "
    "and own the risks they generate. Independent Risk Management and Compliance are the second line, setting "
    "risk appetite, policies and limits, and challenging the first line. Internal Audit is the third line, "
    "providing independent assurance to the Audit Committee.",
)
story.append(h2("Risk appetite"))
story += ps(
    "The Board-approved risk appetite framework expresses the types and amount of risk the Firm is willing to "
    "take, using quantitative parameters calibrated to stressed earnings, capital and liquidity outcomes. Key "
    "parameters include: maintaining a Standardized CET1 ratio above the management target in the baseline "
    "plan and above regulatory minimums plus buffers under severe stress; maintaining liquidity sources that "
    "exceed stressed outflows over a 90-day horizon; and limiting the decline in 12-month net interest income "
    "under a 200 basis point parallel rate shock to 7% of base NII.",
)
rows = [["Risk appetite metric", "Limit / threshold", "Dec 31, 2025", "Status"],
        ["Standardized CET1 ratio (baseline)", ">= 13.0%", pct(CAP["CET1 ratio (Standardized)"][0], 2), "Within"],
        ["Minimum stressed CET1 ratio (internal severely adverse)", ">= 10.2%", "12.6%", "Within"],
        ["Supplementary leverage ratio", ">= 5.5%", pct(CAP["Supplementary leverage ratio"][0], 1), "Within"],
        ["LCR (average)", ">= 110%", f"{B.LIQUIDITY['LCR (average, Q4)'][0]*100:.0f}%", "Within"],
        ["NII decline under -200 bp shock", "<= 7.0%", pct(-O["nii"]["Down 200"]["pct"], 1), "Within"],
        ["EVE decline under +200 bp shock (% Tier 1)", "<= 15.0%", pct(-O["nii"]["Up 200"]["eve_pct"], 1), "Within"],
        ["Card net charge-off rate (annual)", "<= 4.5%", "3.42%", "Within"],
        ["Single-name wholesale exposure (% Tier 1)", "<= 10%", "4.8%", "Within"]]
story.append(table(rows, [0.46, 0.18, 0.18, 0.18]))
story.append(h2("Committees"))
story += bullets([
    "<b>Firmwide Risk Committee</b> - senior management forum for firmwide risk issues; chaired by the CEO and CRO.",
    "<b>Asset and Liability Committee (ALCO)</b> - oversees liquidity, interest rate and capital risk; reviews "
    "outputs of the NII Sensitivity Model monthly.",
    "<b>Capital Governance Committee</b> - oversees the capital plan, CCAR submission and capital actions; owns "
    "outputs of the Capital Planning &amp; Stress Projection Model.",
    "<b>Allowance Committee</b> - approves scenario weights, CECL model outputs and qualitative overlays each quarter.",
    "<b>Firmwide Model Risk Committee</b> - approves Tier 1 models and model risk appetite.",
    "<b>Data and Technology Risk Committee</b> - oversees critical data elements, API change management and "
    "BCBS 239 compliance.",
])
story.append(PageBreak())

# 3 Capital structure
story.append(h1("3. Capital Structure"))
story += ps(
    "Regulatory capital consists of Common Equity Tier 1 (CET1) capital, Additional Tier 1 capital and Tier 2 "
    "capital. CET1 capital comprises common stock, related surplus, retained earnings and accumulated other "
    "comprehensive income (AOCI), less regulatory deductions and adjustments. As a Category I firm, the Firm "
    "includes AOCI related to available-for-sale securities in CET1.",
)
rows = [["Reconciliation of common equity to CET1 (in millions)", "Dec 31, 2025"]]
for k, v in B.CET1_BRIDGE:
    rows.append([k, m(v)])
rows.append(["Common Equity Tier 1 capital", m(CAP["CET1 capital"][0])])
rows += [["Add: qualifying non-cumulative perpetual preferred stock", m(12_500)],
         ["Less: Additional Tier 1 deductions", m(-330)],
         ["Tier 1 capital", m(CAP["Tier 1 capital"][0])],
         ["Add: qualifying subordinated debt", m(11_900)],
         ["Add: qualifying allowance for credit losses", m(6_380)],
         ["Total capital (Standardized)", m(CAP["Total capital"][0])]]
assert 98_450 + 12_500 - 330 == CAP["Tier 1 capital"][0]
assert CAP["Tier 1 capital"][0] + 11_900 + 6_380 == CAP["Total capital"][0]
story.append(table(rows, [0.72, 0.28], bold_rows=(8, 11, 14)))
story += ps(
    "CET1 capital increased by $5.3 billion during 2025, primarily reflecting net income of $25.0 billion, "
    "partly offset by common dividends of $6.1 billion, share repurchases of $11.0 billion, preferred dividends "
    "of $1.1 billion and other movements including AOCI. Starting capital figures used in the Capital Planning "
    "&amp; Stress Projection Model are sourced from the Regulatory Reporting API (API-16), which delivers the "
    "same governed data used to prepare these disclosures and the FR Y-9C.",
)
story.append(h2("Capital instruments"))
rows = [["Instrument", "Amount ($mm)", "Coupon", "Call date", "Regulatory treatment"],
        ["Common stock (1,388.8 million shares outstanding)", "-", "-", "-", "CET1"],
        ["Series AA non-cumulative preferred", "2,500", "5.75% fixed", "2026", "Additional Tier 1"],
        ["Series CC non-cumulative preferred", "3,000", "SOFR + 3.12%", "2027", "Additional Tier 1"],
        ["Series DD non-cumulative preferred", "4,000", "6.10% fixed-to-floating", "2029", "Additional Tier 1"],
        ["Series EE non-cumulative preferred", "3,000", "6.50% fixed reset", "2030", "Additional Tier 1"],
        ["Subordinated notes due 2033-2045", "11,900", "4.25%-6.80%", "n/a", "Tier 2 (amortizing in final 5 years)"]]
story.append(table(rows, [0.36, 0.13, 0.17, 0.11, 0.23]))
story.append(PageBreak())

# 4 Capital adequacy
story.append(h1("4. Capital Adequacy"))
story.append(h2("4.1 Risk-weighted assets"))
rows = [["Standardized RWA by exposure type (in millions)", "RWA", "% of total", "Capital requirement (8%)"]]
for k, v in B.RWA_STD:
    rows.append([k, m(v), pct(v / RWA), m(v * 0.08)])
rows.append(["Total Standardized RWA", m(RWA), "100.0%", m(RWA * 0.08)])
story.append(table(rows, [0.46, 0.18, 0.18, 0.18], total_rows=(-1,)))
rows = [["Advanced RWA by risk type (in millions)", "RWA", "% of total"]]
for k, v in B.RWA_ADV:
    rows.append([k, m(v), pct(v / CAP["Advanced RWA"][0])])
rows.append(["Total Advanced RWA", m(CAP["Advanced RWA"][0]), "100.0%"])
story.append(table(rows, [0.6, 0.2, 0.2], total_rows=(-1,)))
story.append(side_by_side(
    donut("p3_rwa_std", [k for k, _ in B.RWA_STD], [v for _, v in B.RWA_STD], "Standardized RWA mix"),
    donut("p3_rwa_adv", [k for k, _ in B.RWA_ADV], [v for _, v in B.RWA_ADV], "Advanced RWA mix")))
story += ps(
    "Standardized RWA increased by $18.9 billion in 2025, driven by loan growth in Card and C&amp;I (+$14.2 "
    "billion), higher counterparty credit risk from increased client derivative activity (+$3.1 billion) and "
    "higher market risk RWA (+$1.6 billion). Advanced RWA increased by $14.2 billion, with lower growth than "
    "Standardized because internal PD and LGD estimates for the Card portfolio, delivered by the Credit Risk "
    "Scoring API (API-10), reflect the high credit quality of new originations.",
)
story.append(PageBreak())
story.append(h2("4.1a RWA flow statement"))
rows = [["Standardized RWA movement, 2025 (in millions)", "Credit risk", "Market risk", "Total"],
        ["RWA at December 31, 2024", "581,300", "52,600", "633,900"],
        ["Loan and commitment growth", "14,200", "-", "14,200"],
        ["Changes in counterparty exposure (derivatives and SFTs)", "3,100", "-", "3,100"],
        ["Changes in asset quality and collateral", "(1,400)", "-", "(1,400)"],
        ["Securities portfolio repositioning", "1,700", "-", "1,700"],
        ["Changes in market risk positions and model updates", "-", "1,600", "1,600"],
        ["Foreign exchange movements and other", "(300)", "-", "(300)"],
        ["RWA at December 31, 2025", "598,600", "54,200", "652,800"]]
assert 581_300+14_200+3_100-1_400+1_700-300 == 598_600
story.append(table(rows, [0.52, 0.16, 0.16, 0.16], bold_rows=(1, 8)))
story += ps(
    "Credit risk RWA growth was concentrated in retail credit risk (Card, +$9.8 billion) and wholesale lending to "
    "middle-market clients (+$4.4 billion). The improvement in asset quality and collateral primarily reflects "
    "higher eligible collateral on securities-based lending in Asset &amp; Wealth Management. Market risk RWA rose "
    "with higher stressed VaR in rates trading during the second quarter.",
)
story.append(h2("4.1b Countercyclical capital buffer - geographic distribution"))
rows = [["Jurisdiction", "Private-sector credit exposure RWA ($mm)", "CCyB rate", "Weighted contribution"],
        ["United States", "512,600", "0.00%", "0.000%"], ["United Kingdom", "18,400", "2.00%", "0.064%"],
        ["Germany", "9,800", "0.75%", "0.013%"], ["France", "8,200", "1.00%", "0.014%"],
        ["Hong Kong", "6,100", "0.50%", "0.005%"], ["Other jurisdictions", "18,700", "0.00%-1.00%", "0.012%"],
        ["Firm-specific CCyB (applied to non-U.S. exposure only; U.S. buffer is 0%)", "573,800", "", "0.108%"]]
story.append(table(rows, [0.4, 0.22, 0.16, 0.22], total_rows=(-1,),
                   note="The U.S. CCyB applicable to the Firm's Standardized and Advanced buffers is set at 0%; the "
                        "foreign-jurisdiction figures are shown for transparency and Advanced approaches computation."))
story.append(PageBreak())
story.append(h2("4.2 Capital ratios and buffers"))
rows = [["Capital ratios", "Standardized", "Advanced", "Regulatory requirement", "Well-capitalized"],
        ["CET1 ratio", pct(CAP["CET1 ratio (Standardized)"][0], 2), pct(CAP["CET1 capital"][0] / CAP["Advanced RWA"][0], 2),
         pct(REQ["minimum"] + REQ["stress_capital_buffer"] + REQ["gsib_surcharge"]), "n/a"],
        ["Tier 1 ratio", pct(CAP["Tier 1 ratio (Standardized)"][0], 2), pct(CAP["Tier 1 capital"][0] / CAP["Advanced RWA"][0], 2),
         pct(0.06 + REQ["stress_capital_buffer"] + REQ["gsib_surcharge"]), "6.0%"],
        ["Total capital ratio", pct(CAP["Total capital ratio (Standardized)"][0], 2),
         pct((CAP["Total capital"][0] - 1_900) / CAP["Advanced RWA"][0], 2),
         pct(0.08 + REQ["stress_capital_buffer"] + REQ["gsib_surcharge"]), "10.0%"]]
story.append(table(rows, [0.24, 0.17, 0.17, 0.24, 0.18]))
story += ps(
    f"The Firm's capital conservation buffer requirement under the Standardized approach equals the stress capital "
    f"buffer ({pct(REQ['stress_capital_buffer'])}) plus the G-SIB surcharge ({pct(REQ['gsib_surcharge'])}) plus the "
    "countercyclical capital buffer (currently 0%). Under the Advanced approaches, the buffer is 2.5% plus the "
    "G-SIB surcharge and countercyclical buffer. At December 31, 2025 the Firm's Standardized capital "
    f"conservation buffer was {pct(CAP['CET1 ratio (Standardized)'][0] - REQ['minimum'], 2)}, well above the "
    f"{pct(REQ['stress_capital_buffer'] + REQ['gsib_surcharge'])} required, and the Firm was not subject to any "
    "limitations on distributions or discretionary bonus payments. Eligible retained income was $23.9 billion.",
)
story.append(bar_chart("p3_stack", ["Requirement", "Mgmt target", "Actual"],
                       {"Minimum 4.5%": [0.045, 0.045, 0.045],
                        "SCB": [REQ["stress_capital_buffer"], REQ["stress_capital_buffer"], 0],
                        "G-SIB surcharge": [REQ["gsib_surcharge"], REQ["gsib_surcharge"], 0],
                        "Management buffer": [0, REQ["management_target"] - 0.102, 0],
                        "Actual CET1 above minimum": [0, 0, CAP["CET1 ratio (Standardized)"][0] - 0.045]},
                       "CET1 requirement stack vs actual (Standardized)", stacked=True, ratio=0.32))
story.append(PageBreak())

# 5 Leverage
story.append(h1("5. Leverage"))
story += ps(
    "The supplementary leverage ratio (SLR) is Tier 1 capital divided by total leverage exposure, which "
    "includes on-balance-sheet assets and certain off-balance-sheet exposures. As a G-SIB, the Firm is subject "
    "to a 3.0% minimum SLR plus a 2.0% enhanced SLR buffer, for an effective requirement of 5.0%. The Tier 1 "
    "leverage ratio (Tier 1 capital to average on-balance-sheet assets) minimum is 4.0%.",
)
rows = [["Total leverage exposure (in millions)", "Dec 31, 2025"]]
for k, v in B.LEVERAGE:
    rows.append([k, m(v)])
rows += [["Total leverage exposure", m(CAP["Total leverage exposure"][0])],
         ["Tier 1 capital", m(CAP["Tier 1 capital"][0])],
         ["Supplementary leverage ratio", pct(CAP["Supplementary leverage ratio"][0], 2)],
         ["Tier 1 leverage ratio", pct(CAP["Tier 1 leverage ratio"][0], 2)]]
story.append(table(rows, [0.72, 0.28], bold_rows=(6, 8)))

# 6 Credit risk
story.append(h1("6. Credit Risk"))
story += ps(
    "Credit risk arises from lending, lending-related commitments, derivatives, securities financing and "
    "investment securities. The Firm's credit risk management framework covers origination standards, "
    "concentration limits, ongoing monitoring, problem-loan management and reserving. Consumer credit decisions "
    "use automated scorecards delivered by the Credit Decisioning API (API-09). Wholesale credit decisions are "
    "made by credit officers with delegated authority based on internal risk ratings, which map to PD estimates "
    "produced by the Credit Risk Scoring API (API-10).",
)
story.append(h2("6.1 Credit exposure by type and geography"))
rows = [["Credit exposure (in billions)", "Loans", "Commitments", "Derivatives", "Securities", "Total"],
        ["United States", "$632.4", "$498.1", "$31.2", "$140.6", "$1,302.3"],
        ["Europe, Middle East and Africa", "$64.8", "$71.3", "$13.8", "$18.4", "$168.3"],
        ["Asia-Pacific", "$29.7", "$34.9", "$6.1", "$8.1", "$78.8"],
        ["Latin America and Canada", "$15.4", "$18.6", "$1.9", "$3.8", "$39.7"],
        ["Total", "$742.3", "$622.9", "$53.0", "$170.9", "$1,589.1"]]
story.append(table(rows, [0.3, 0.14, 0.14, 0.14, 0.14, 0.14], total_rows=(-1,)))
story.append(h2("6.2 Residual contractual maturity"))
rows = [["Exposure by maturity (in billions)", "< 1 year", "1-5 years", "> 5 years", "Total"],
        ["Consumer loans", "$92.1", "$118.6", "$235.2", "$445.9"],
        ["Wholesale loans", "$86.4", "$168.2", "$41.8", "$296.4"],
        ["Lending-related commitments", "$198.7", "$389.2", "$35.0", "$622.9"],
        ["Derivative receivables", "$19.4", "$21.2", "$12.4", "$53.0"],
        ["Total", "$396.6", "$697.2", "$324.4", "$1,418.2"]]
story.append(table(rows, [0.36, 0.16, 0.16, 0.16, 0.16], total_rows=(-1,)))
story.append(h2("6.2a Wholesale credit exposure by industry"))
rows = [["Industry (in billions)", "Loans", "Commitments", "Derivatives", "Total", "Investment grade"],
        ["Real estate", "$98.2", "$38.9", "$0.8", "$137.9", "63%"], ["Technology, media & telecom", "$31.4", "$94.7", "$5.5", "$131.6", "73%"],
        ["Consumer & retail", "$34.8", "$78.6", "$5.6", "$119.0", "61%"], ["Industrials", "$29.1", "$70.4", "$4.8", "$104.3", "66%"],
        ["Banks & finance companies", "$22.6", "$46.1", "$27.5", "$96.2", "86%"], ["Asset managers", "$18.2", "$55.4", "$14.8", "$88.4", "84%"],
        ["Healthcare", "$19.7", "$58.6", "$4.2", "$82.5", "72%"], ["Oil & gas and utilities", "$16.4", "$50.3", "$5.1", "$71.8", "68%"],
        ["Individuals and individual entities", "$46.3", "$18.2", "$2.4", "$66.9", "79%"],
        ["State and municipal governments", "$12.1", "$21.9", "$3.6", "$37.6", "94%"], ["All other", "$47.6", "$222.0", "$8.3", "$277.9", "77%"],
        ["Total wholesale", "$376.4", "$755.1", "$82.6", "$1,214.1", "74%"]]
story.append(table(rows, [0.32, 0.12, 0.15, 0.13, 0.13, 0.15], total_rows=(-1,)))
story += ps(
    "Concentration limits are set by industry, country and single name, and are monitored daily. The largest "
    "industry concentration, real estate, is dominated by multifamily lending in supply-constrained U.S. markets. "
    "Office exposure of $15.2 billion is 1.3% of total wholesale credit exposure. Exposures to banks and finance "
    "companies and to asset managers are predominantly short-dated, collateralized derivative and SFT exposures.",
)
story.append(h2("6.2b Equity exposures in the banking book"))
rows = [["Equity exposures (in millions)", "Carrying value", "RWA"],
        ["Publicly traded equity investments", "1,240", "1,860"], ["Private equity and venture investments", "2,180", "3,270"],
        ["Tax-oriented investments (affordable housing, renewable energy)", "1,180", "1,180"],
        ["Equity investments in unconsolidated funds", "390", "590"], ["Total", "4,990", "6,900"]]
story.append(table(rows, [0.6, 0.2, 0.2], total_rows=(-1,)))
story.append(PageBreak())
story.append(h2("6.3 Exposure by PD band (Advanced approaches)"))
rows = [["PD band", "Wholesale EAD ($bn)", "Avg PD", "Avg LGD", "Avg risk weight", "Retail EAD ($bn)", "Retail avg PD"],
        ["0.00% to < 0.15%", "$412.6", "0.06%", "33%", "17%", "$188.4", "0.05%"],
        ["0.15% to < 0.50%", "$231.8", "0.29%", "35%", "38%", "$121.6", "0.31%"],
        ["0.50% to < 2.50%", "$154.2", "1.18%", "37%", "71%", "$96.3", "1.24%"],
        ["2.50% to < 10.00%", "$41.7", "4.92%", "39%", "118%", "$48.1", "5.06%"],
        ["10.00% to < 100%", "$9.8", "21.4%", "41%", "191%", "$12.7", "24.8%"],
        ["100% (default)", "$4.1", "100%", "44%", "n/a", "$3.9", "100%"],
        ["Total", "$854.2", "1.21%", "35%", "45%", "$471.0", "2.09%"]]
story.append(table(rows, [0.18, 0.15, 0.1, 0.1, 0.14, 0.17, 0.16], total_rows=(-1,)))
story += ps(
    "PD, LGD and EAD parameters for Advanced approaches capital are estimated by the Firm's internal ratings "
    "systems and served to capital calculators and the CECL model through the Credit Risk Scoring API (API-10). "
    "Regulatory capital parameters are through-the-cycle estimates with regulatory floors, whereas parameters "
    "used for CECL are point-in-time estimates conditioned on macroeconomic scenarios; the API exposes both "
    "parameter sets through separate endpoints.",
)
story.append(h2("6.4 Impaired and past-due exposures; allowance"))
cl = O["cecl"]
rows = [["Portfolio segment (in millions)", "Loans", "Nonaccrual", "90+ days past due", "Allowance", "2025 NCOs"]]
na = {"Credit Card": ("-", "1,633"), "Residential Mortgage": ("2,140", "410"), "Auto": ("190", "120"),
      "Commercial Real Estate": ("1,420", "180"), "Commercial & Industrial": ("1,260", "160"),
      "Other Consumer & Wholesale": ("140", "40")}
for seg, bal, allow, lob in B.CECL_SEGMENTS:
    rows.append([seg, m(bal), na[seg][0], na[seg][1], m(allow), m(B.NCO_BY_SEGMENT[seg])])
rows.append(["Total", m(742_300), "5,150", "2,543", m(15_920), m(6_100)])
story.append(table(rows, [0.3, 0.14, 0.13, 0.15, 0.14, 0.14], total_rows=(-1,)))
story += ps(
    "The allowance is calculated under ASC 326 using the CECL Lifetime Expected Credit Loss Model (MDL-CR-007) "
    f"and includes qualitative overlays of {usd(cl['Total']['overlay'])} million approved by the Allowance Committee. "
    f"Up to 1.25% of credit RWA of the allowance (${6_380:,} million) qualifies as Tier 2 capital under the "
    "Standardized approach.",
)
story.append(h2("6.5 Credit risk mitigation"))
story += ps(
    "The Firm mitigates credit risk through collateral, guarantees, credit derivatives and netting agreements. "
    "Eligible financial collateral for Standardized RWA purposes includes cash, U.S. Treasury and agency "
    "securities, and investment-grade debt and main-index equities. At December 31, 2025, exposures covered by "
    "eligible financial collateral totaled $214 billion, by guarantees $18 billion and by single-name credit "
    "derivatives $31 billion. Collateral values are refreshed daily using prices from the Market Data API (API-12).",
)
story.append(PageBreak())

# 7 CCR
story.append(h1("7. Counterparty Credit Risk"))
story += ps(
    "Counterparty credit risk (CCR) arises from derivatives and securities financing transactions (SFTs). The "
    "Firm measures CCR exposure using the standardized approach for counterparty credit risk (SA-CCR) for "
    "Standardized RWA and the internal models methodology for Advanced RWA. Credit valuation adjustment (CVA) "
    "capital is calculated using the advanced CVA approach.",
)
rows = [["CCR exposure (in millions)", "Exposure at default", "RWA (Standardized)"],
        ["OTC derivatives - bilateral", "62,400", "24,300"], ["OTC derivatives - centrally cleared", "18,900", "1,100"],
        ["Exchange-traded derivatives", "9,700", "600"], ["Securities financing transactions", "54,200", "9,800"],
        ["Default fund contributions to CCPs", "2,400", "5,800"], ["Total", "147,600", "41,600"]]
story.append(table(rows, [0.5, 0.25, 0.25], total_rows=(-1,)))
rows = [["Derivative notional and fair value (in billions)", "Notional", "Gross positive fair value", "Net after netting & collateral"],
        ["Interest rate contracts", "$38,420", "$214.6", "$18.2"], ["Credit derivatives", "$1,410", "$11.8", "$1.7"],
        ["Foreign exchange contracts", "$9,860", "$121.3", "$14.4"], ["Equity contracts", "$2,240", "$48.9", "$6.3"],
        ["Commodity contracts", "$410", "$16.2", "$3.8"], ["Total", "$52,340", "$412.8", "$44.4"]]
story.append(table(rows, [0.4, 0.2, 0.2, 0.2], total_rows=(-1,)))
story += ps(
    "CVA RWA was $26.1 billion under the Advanced approach. Wrong-way risk is monitored at the counterparty "
    "and portfolio level. The Firm would be required to post approximately $2.1 billion of additional "
    "collateral in the event of a one-notch downgrade and $4.6 billion for a two-notch downgrade.",
)

# 8 Securitization
story.append(h1("8. Securitization"))
story += ps(
    "The Firm participates in securitization as originator (credit card master trust, residential mortgage), "
    "sponsor (client-driven asset-backed commercial paper conduits) and investor (agency and non-agency "
    "mortgage-backed securities, CLOs). Securitization exposures are risk-weighted under the simplified "
    "supervisory formula approach (SSFA) or, where applicable, the 1,250% risk weight.",
)
rows = [["Securitization exposures (in millions)", "Exposure", "RWA"],
        ["Retained interests - credit card master trust", "8,200", "1,640"],
        ["Investments in non-agency MBS and ABS", "21,400", "3,980"],
        ["Investments in CLOs (senior tranches)", "12,600", "2,520"],
        ["Liquidity facilities to sponsored conduits", "4,900", "980"],
        ["Exposures subject to 1,250% risk weight", "14", "180"], ["Total", "47,114", "9,300"]]
story.append(table(rows, [0.6, 0.2, 0.2], total_rows=(-1,)))
story.append(PageBreak())

# 9 Market risk
story.append(h1("9. Market Risk"))
story += ps(
    "Market risk capital applies to covered positions - trading assets and liabilities and certain foreign "
    "exchange and commodity positions. The Firm uses internal models approved by its regulators for VaR, "
    "stressed VaR, the incremental risk charge (IRC) and the comprehensive risk measure, and the standardized "
    "specific risk charge for certain positions. Inputs - prices, curves, volatility surfaces and correlations - "
    "are sourced from the Market Data API (API-12) and FX Rates API (API-13), which are validated independently "
    "by the Valuation Control Group.",
)
rows = [["Market risk RWA components (in millions)", "Dec 31, 2025", "Dec 31, 2024"],
        ["Regulatory VaR (10-day, 99%) x multiplier", "11,400", "11,100"],
        ["Stressed VaR (10-day, 99%) x multiplier", "21,900", "21,200"],
        ["Incremental risk charge", "7,800", "7,500"], ["Comprehensive risk measure", "1,300", "1,400"],
        ["Standardized specific risk", "11,800", "11,400"], ["Total market risk RWA", "54,200", "52,600"]]
story.append(table(rows, [0.6, 0.2, 0.2], total_rows=(-1,)))
rows = [["Regulatory VaR (10-day, 99%, in millions)", "Average", "Minimum", "Maximum", "Period end"],
        ["Interest rate", "128", "84", "192", "117"], ["Credit spread", "61", "42", "89", "58"],
        ["Equity", "52", "31", "86", "49"], ["Foreign exchange", "29", "16", "51", "27"],
        ["Commodity", "22", "12", "37", "19"], ["Diversification", "(132)", "NM", "NM", "(121)"],
        ["Total regulatory VaR", "160", "118", "231", "149"]]
story.append(table(rows, [0.4, 0.15, 0.15, 0.15, 0.15], total_rows=(-1,)))
story += ps(
    "Backtesting compares daily trading results with the prior day's 1-day 99% VaR. There were 2 backtesting "
    "exceptions at the firmwide level in the twelve months to December 31, 2025, below the threshold of five "
    "that would increase the regulatory multiplier above 3.0.",
)
story.append(line_chart("p3_var", ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                        {"1-day 95% VaR ($mm)": [48, 52, 61, 71, 55, 49, 46, 44, 47, 51, 49, 45]},
                        "Monthly average trading VaR, 2025", ratio=0.3))

# 10 Op risk
story.append(h1("10. Operational Risk"))
story += ps(
    "Operational risk capital under the Advanced approaches is calculated using a loss distribution approach that "
    "combines internal loss data, external loss data, scenario analysis and business environment and internal "
    "control factors. Operational risk RWA was $112.6 billion at December 31, 2025. Operational risk losses in "
    "2025 totaled $1.4 billion, of which 41% related to clients, products and business practices (primarily "
    "litigation), 28% to external fraud and 17% to execution, delivery and process management.",
    "Technology and cyber risk are managed within the operational risk framework. Critical client-facing and "
    "regulatory data services, including eighteen production APIs on the Developer Platform, are subject to "
    "resilience testing, change management controls and continuous monitoring of availability and latency "
    "against service-level objectives.",
)
story.append(PageBreak())

# 11 IRRBB
story.append(h1("11. Interest Rate Risk in the Banking Book"))
n = O["nii"]
story += ps(
    "IRRBB is measured using both earnings-based (NII) and value-based (EVE) metrics. The Firm's primary "
    "earnings measure is produced by the Net Interest Income Sensitivity Model (MDL-ALM-014), a Tier 1 model "
    "owned by Corporate Treasury - Asset &amp; Liability Management and validated by MRGR in September 2025.",
)
story.append(h2("Methodology and key assumptions"))
story += bullets([
    "Instantaneous, parallel shocks of +/-100 and +/-200 basis points applied to the December 31, 2025 balance "
    "sheet; static balance sheet with no growth or mix change.",
    "Repricing occurs at the midpoint of each repricing bucket: month 1.5 for 0-3 months and month 7.5 for 3-12 "
    "months; positions repricing after 12 months do not affect 12-month NII.",
    "Deposit betas: 0.45 consumer interest-bearing, 0.75 wholesale interest-bearing, 0.00 noninterest-bearing; "
    "betas held constant across shock sizes.",
    "EVE approximated using modified duration: noninterest-bearing deposits assigned a behavioral duration of "
    "3.5 years and consumer interest-bearing deposits 2.8 years.",
    "Data: balances and rates from the Treasury Liquidity Positions API (API-15); repricing profiles from the "
    "Loan Servicing API (API-11); yield curve from the Market Data API (API-12).",
])
rows = [["Scenario", "Change in 12-month NII ($mm)", "% of base NII", "Change in EVE ($mm)", "EVE % of Tier 1"]]
for k in ["Down 200", "Down 100", "Up 100", "Up 200"]:
    v = n[k]
    rows.append([k + " bps", m(v["delta"]), pct(v["pct"]), m(v["eve"]), pct(v["eve_pct"])])
story.append(table(rows, [0.2, 0.22, 0.18, 0.2, 0.2],
                   note=f"Base-case 12-month NII: ${n['Base']['nii']:,.0f} million. Source: NII_Sensitivity_Model.xlsx."))
story.append(bar_chart("p3_nii", ["-200", "-100", "+100", "+200"],
                       {"Change in NII ($mm)": [n[k]["delta"] for k in ["Down 200", "Down 100", "Up 100", "Up 200"]],
                        "Change in EVE ($mm)": [n[k]["eve"] for k in ["Down 200", "Down 100", "Up 100", "Up 200"]]},
                       "NII and EVE sensitivity by parallel shock (bps)", ratio=0.32))
story += ps(
    "<b>Known limitations.</b> The model does not capture non-parallel curve movements, basis risk, optionality in "
    "mortgage prepayments beyond the static repricing profile, or the convexity of deposit betas at very low "
    "rates. These are addressed through the quarterly dynamic simulation and supplemental scenario analysis "
    "reviewed by ALCO.",
)
story.append(PageBreak())

# 12 Liquidity
story.append(h1("12. Liquidity"))
story.append(h2("12.1 Liquidity coverage ratio"))
rows = [["Q4 2025 average (in millions)", "Unweighted", "Weighted"],
        ["High-quality liquid assets", "", m(B.LIQUIDITY["HQLA (average, Q4)"][0])],
        ["Retail funding outflows", "652,300", "40,900"], ["Unsecured wholesale funding outflows", "415,700", "168,900"],
        ["Secured wholesale funding and asset exchange outflows", "", "36,800"],
        ["Additional requirements (derivatives, commitments)", "", "122,200"], ["Other outflows", "", "13,600"],
        ["Total cash outflows", "", "382,400"], ["Secured lending inflows", "", "(74,300)"],
        ["Inflows from fully performing exposures and other", "", "(61,550)"], ["Total cash inflows", "", "(135,850)"],
        ["Total net cash outflows", "", "246,550"],
        ["Liquidity coverage ratio", "", f"{B.LIQUIDITY['LCR (average, Q4)'][0]*100:.0f}%"]]
assert 40_900 + 168_900 + 36_800 + 122_200 + 13_600 == 382_400
story.append(table(rows, [0.6, 0.2, 0.2], bold_rows=(1, 7, 10, 11, 12)))
story.append(h2("12.2 Net stable funding ratio"))
rows = [["NSFR components, Q4 2025 average (in millions)", "Weighted amount"],
        ["Available stable funding: regulatory capital and long-term debt", "214,600"],
        ["Available stable funding: retail and small business deposits", "598,400"],
        ["Available stable funding: wholesale funding and other", "269,000"],
        ["Total available stable funding (ASF)", "1,082,000"],
        ["Required stable funding: loans and securities", "671,800"],
        ["Required stable funding: HQLA, derivatives and other assets", "142,700"],
        ["Required stable funding: off-balance-sheet", "30,800"], ["Total required stable funding (RSF)", "845,300"],
        ["Net stable funding ratio", f"{B.LIQUIDITY['NSFR'][0]*100:.0f}%"]]
story.append(table(rows, [0.72, 0.28], bold_rows=(4, 8, 9)))
story += ps(
    "Liquidity positions are aggregated daily through the Treasury Liquidity Positions API (API-15), which provides "
    "legal-entity-level views of HQLA, encumbrance and contractual cash flows to the liquidity stress testing "
    "engine, the LCR and NSFR calculators and the asset-liability management models.",
)
story.append(PageBreak())

# 13 Stress testing
story.append(h1("13. Capital Planning and Stress Testing"))
c = O["capital"]
story += ps(
    "The Firm's capital planning process integrates its strategic plan, risk appetite and stress testing. The "
    "Capital Planning &amp; Stress Projection Model (MDL-CAP-003) projects CET1 capital, RWA and capital ratios over "
    "a nine-quarter horizon. The model combines pre-provision net revenue (PPNR), provisions and trading and "
    "counterparty losses produced by the enterprise stress testing program with the Firm's planned capital "
    "actions. Starting positions are sourced from the Regulatory Reporting API (API-16) and scenario variables "
    "from the Macroeconomic Scenario API (API-14).",
    "Key conventions: under stress, share repurchases are suspended and dividends are held flat at the current "
    "level; tax benefits on losses are recognized at the effective tax rate; RWA growth follows scenario-specific "
    "assumptions reflecting increased draws on commitments and higher counterparty exposure early in the scenario.",
)
rows = [["Internal severely adverse scenario (peak / trough)", "Value"],
        ["U.S. unemployment rate (peak)", "10.2%"], ["U.S. real GDP (peak-to-trough)", "-6.4%"],
        ["Equity prices (S&P 500-style index, trough)", "-41%"], ["House prices (trough)", "-28%"],
        ["Commercial real estate prices (trough)", "-35%"], ["10-year Treasury yield (trough)", "0.9%"],
        ["BBB corporate spread (peak)", "+5.4 pp"], ["Instantaneous global market shock", "Applied in first quarter"]]
story.append(table(rows, [0.72, 0.28],
                   note="Scenario paths are distributed to the CECL and capital planning models by the "
                        "Macroeconomic Scenario API (API-14), scenario set SA-2025-INT."))
story += ps(
    "Projection outputs from the model are not reproduced in this report because they are refreshed every "
    "quarter; the most recent projections are published in the Firm's quarterly earnings materials.",
)
story += ps(
    "<b>2025 supervisory stress test.</b> In the 2025 CCAR cycle, the Federal Reserve's projected minimum CET1 "
    "ratio for the Firm under the supervisory severely adverse scenario was 12.1%, resulting in a stress capital "
    f"buffer of {pct(REQ['stress_capital_buffer'])}. The Firm's own projections under the same scenario, produced "
    "with MDL-CAP-003, showed a minimum CET1 ratio of 12.6%.",
    "<b>Reverse stress testing.</b> The Firm also performs reverse stress tests to identify scenarios that would "
    "cause the CET1 ratio to fall below regulatory requirements. Scenarios examined in 2025 included a combined "
    "cyber event affecting payment systems with a simultaneous severe recession, and a sustained period of "
    "negative policy rates.",
)
story.append(PageBreak())

# 14 Model risk
story.append(h1("14. Model Risk Management and Model Inventory"))
story += ps(
    "Models used in the calculation of regulatory capital, the allowance for credit losses, liquidity metrics and "
    "interest rate risk are subject to the Firm's Model Risk Policy, aligned with SR 11-7. Models are tiered by "
    "materiality and complexity. Tier 1 models undergo annual independent validation by Model Risk Governance "
    "&amp; Review (MRGR), quarterly ongoing performance monitoring and annual attestation by model owners. Material "
    "model changes require MRGR approval and, for regulatory capital models, regulatory notification.",
    "The table below lists the Tier 1 models that most directly affect the figures in these disclosures, together "
    "with their upstream data dependencies. Each upstream API is registered as a critical data source in the model "
    "inventory; a breaking change to an API's schema or business logic automatically opens a model change review.",
)
for md in B.MODELS:
    story.append(h3(f"{md['id']} - {md['name']}"))
    rows = [["Attribute", "Detail"], ["Model file", md["file"]], ["Risk tier", md["tier"]], ["Model owner", md["owner"]],
            ["Independent validator", md["validator"]], ["Last validation / next due",
                                                         f"{md['last_validation']} / {md['next_validation']}"],
            ["Purpose", md["purpose"]], ["Upstream APIs", "; ".join(md["apis"])],
            ["Downstream disclosures", "; ".join(md["reports"])]]
    story.append(table(rows, [0.26, 0.74]))
story += ps(
    "<b>2025 validation findings.</b> MRGR's 2025 validation of MDL-CR-007 raised one medium-severity finding "
    "regarding the absence of an explicit model for unfunded commitments (remediated through an interim overlay) "
    "and one low-severity finding on documentation of the Card PD elasticity. The 2025 validation of MDL-ALM-014 "
    "raised a medium-severity finding that deposit betas are held constant across shock sizes; the compensating "
    "control is the quarterly dynamic simulation. MDL-CAP-003 was validated in February 2026 with no findings "
    "above low severity.",
)
story.append(PageBreak())

# 15 Data governance
story.append(h1("15. Risk Data Aggregation and API Data Lineage"))
story += ps(
    "The Firm complies with the BCBS 239 Principles for effective risk data aggregation and risk reporting. Risk "
    "and regulatory data flows are delivered through governed APIs on the Developer Platform, each with a named "
    "data owner, documented schema, data-quality rules and service-level objectives. The following table maps "
    "the APIs that feed regulatory and risk measures to the models and disclosures they support.",
)
lineage = [
    ("API-10 Credit Risk Scoring API", "Pool-level PD/LGD (point-in-time and TTC)", "MDL-CR-007; Advanced credit RWA", "Sections 4, 6"),
    ("API-11 Loan Servicing API", "Balances, delinquency, remaining life, repricing", "MDL-CR-007; MDL-ALM-014", "Sections 6, 11"),
    ("API-12 Market Data API", "Prices, curves, volatilities", "MDL-ALM-014; VaR; collateral valuation", "Sections 6, 9, 11"),
    ("API-13 FX Rates API", "Spot and forward FX rates", "VaR; non-USD exposure conversion", "Sections 6, 9"),
    ("API-14 Macroeconomic Scenario API", "Scenario paths and weights", "MDL-CR-007; MDL-CAP-003", "Sections 6, 13"),
    ("API-15 Treasury Liquidity Positions API", "HQLA, cash flows, balance sheet positions", "MDL-ALM-014; MDL-CAP-003; LCR/NSFR", "Sections 11, 12"),
    ("API-16 Regulatory Reporting API", "Regulatory capital, RWA, leverage exposure", "MDL-CAP-003; FR Y-9C; Pillar 3", "Sections 3, 4, 5, 13"),
    ("API-09 Credit Decisioning API", "Origination decisions and scorecard outputs", "Credit monitoring (indirect to MDL-CR-007)", "Section 6"),
    ("API-08 Fraud Risk Signals API", "Real-time fraud scores", "Operational risk loss data", "Section 10"),
]
story.append(table([["API", "Data provided", "Consuming models / calculations", "Disclosure sections"]] +
                   [list(r) for r in lineage], [0.27, 0.27, 0.28, 0.18]))
story += ps(
    "In 2025 the Firm completed the migration of the Regulatory Reporting API and the Macroeconomic Scenario API "
    "to the strategic data platform, and introduced automated reconciliation between API-16 outputs and the "
    "general ledger at the legal-entity level. Data-quality exceptions on critical data elements are reported "
    "monthly to the Data and Technology Risk Committee; no exceptions with a material impact on reported capital "
    "ratios occurred during the year.",
)
story.append(PageBreak())
story.append(h1("16. Remuneration and Risk Alignment"))
story += ps(
    "The Firm's compensation philosophy aligns pay with sustained performance and sound risk management. The "
    "Compensation &amp; Management Development Committee of the Board, composed entirely of independent directors, "
    "approves the incentive compensation pool and the compensation of the Operating Committee. The Chief Risk "
    "Officer and Chief Compliance Officer provide input on risk and control outcomes for every business and for "
    "individual material risk takers.",
    "Incentive compensation for material risk takers is subject to deferral of at least 40% (60% for the "
    "Operating Committee) over three to five years, delivered predominantly in restricted stock units. Deferred "
    "awards are subject to clawback and cancellation provisions triggered by misconduct, material financial "
    "restatement or risk-related losses. In 2025, 1.1% of eligible employees had incentive compensation reduced "
    "for risk, control or conduct issues.",
)
rows = [["2025 compensation of material risk takers ($mm)", "Operating Committee", "Other MRTs"],
        ["Number of individuals", "14", "2,310"], ["Fixed compensation", "18", "1,240"],
        ["Variable compensation - cash", "34", "1,560"], ["Variable compensation - deferred equity", "152", "1,720"],
        ["Deferred compensation outstanding (unvested)", "498", "4,860"], ["Reductions for risk / conduct (ex post)", "0", "41"]]
story.append(table(rows, [0.56, 0.22, 0.22]))
story.append(h1("Glossary"))
gl = [("Advanced approaches", "Capital rules using internal estimates of risk parameters to calculate RWA."),
      ("ASF / RSF", "Available / required stable funding in the NSFR calculation."),
      ("CVA", "Credit valuation adjustment: market value of counterparty credit risk on derivatives."),
      ("EAD", "Exposure at default."), ("IRC", "Incremental risk charge for default and migration risk in trading positions."),
      ("SA-CCR", "Standardized approach for counterparty credit risk."),
      ("SSFA", "Simplified supervisory formula approach for securitization exposures."),
      ("Stressed VaR", "VaR calibrated to a one-year period of significant financial stress."),
      ("TTC", "Through-the-cycle parameter estimates used for regulatory capital."),
      ("Collins Floor", "Requirement to use the lower of Standardized and Advanced capital ratios.")]
story.append(table([["Term", "Definition"]] + [list(x) for x in gl], [0.25, 0.75]))
story.append(p(f"<i>{B.BANK['disclaimer']}</i>"))

doc = ReportDoc("../data/reports/MHFC_2025_Pillar3_Disclosures.pdf", f"{nm} Pillar 3 Disclosures 2025",
                "Pillar 3 Regulatory Capital Disclosures - December 31, 2025")
build(doc, story)
print("ok")
