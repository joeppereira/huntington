"""2025 Annual Report (Form 10-K style) for the fictional Meridian Harbor Financial Corp."""
import json
from reportlab.platypus import Spacer, PageBreak, CondPageBreak
from pdfkit_lib import *
import bankdata as B

O = json.load(open("model_outputs.json"))
I = B.INCOME
SEG = B.SEGMENTS
CAP = B.CAPITAL
nm = B.BANK["name"]
sh = B.BANK["short"]


def yoy_row(label, t, dec=0, as_pct=False):
    a, b = t
    if as_pct:
        return [label, pct(a, 1), pct(b, 1), f"{(a - b) * 10000:+.0f} bps"]
    return [label, m(a, dec), m(b, dec), pct(chg(a, b))]


story = []
story += cover("2025 Annual Report", "Annual Report on Form 10-K style disclosure<br/>for the fiscal year ended "
               "December 31, 2025", "Published February 2026",
               [f"Headquarters: {B.BANK['hq']}"])
story += toc_page()

# ================================================================ 1. Letter
story.append(h1("Letter to Shareholders"))
story += ps(
    "Dear Fellow Shareholders,",
    f"2025 was a year in which {sh} demonstrated the value of a balanced, diversified franchise. We generated "
    f"record revenue of {bn(I['total_net_revenue'][0])}, up {pct(chg(*I['total_net_revenue']))} from the prior "
    f"year, and net income of {bn(I['net_income'][0])}, or ${B.KEY_METRICS['Diluted EPS ($)'][0]:.2f} per diluted "
    f"share. Our return on tangible common equity was {pct(B.KEY_METRICS['Return on tangible common equity (ROTCE)'][0])}, "
    "comfortably above our through-the-cycle target of 17%, even as we continued to invest heavily in technology, "
    "branches, bankers and controls.",
    "The operating environment was more complicated than the headline results suggest. Policy rates began to "
    "decline in the second half of the year, compressing deposit spreads in our consumer franchise, while credit "
    "card charge-offs continued to normalize toward pre-pandemic levels. At the same time, capital markets "
    "activity recovered meaningfully: investment banking fees rose "
    f"{pct(chg(*SEG['Commercial & Investment Bank']['ib_fees']))} and Markets revenue reached a record "
    f"{bn(SEG['Commercial & Investment Bank']['markets_revenue'][0])}. Diversification is not a slogan for us. "
    "It is the reason we can keep investing through every part of the cycle.",
    "We ended the year with a Common Equity Tier 1 (CET1) ratio of "
    f"{pct(CAP['CET1 ratio (Standardized)'][0])}, well above our regulatory requirement of "
    f"{pct(B.CAP_REQ['minimum'] + B.CAP_REQ['stress_capital_buffer'] + B.CAP_REQ['gsib_surcharge'])} and our "
    f"management target of {pct(B.CAP_REQ['management_target'])}. That strength allowed us to return "
    "$17.1 billion to shareholders through dividends and share repurchases while still growing loans by "
    f"{pct(chg(*B.BALANCE['Loans']))} and deposits by {pct(chg(*B.LIABS['Deposits']))}. "
    "Our fortress balance sheet remains our first line of defense, and we will continue to hold more capital "
    "and liquidity than we strictly need.",
)
story.append(quote("\"We run the company to be resilient in a severe recession and to keep serving clients "
                   "when others pull back. Strong capital is what lets us be there for them.\""))
story += ps(
    "<b>Consumer &amp; Community Banking.</b> Our consumer franchise added 1.9 million net new checking accounts "
    f"and now serves {B.BANK['digital_users_mm']} million active digital users. We opened 112 new branches in "
    "expansion markets and closed 64 lower-traffic locations, continuing a deliberate shift toward advice-led "
    "branches supported by a digital-first servicing model. Card spend grew 8% and card loans grew 9%, with "
    "charge-offs in line with the guidance we provided at our Investor Day.",
    "<b>Commercial &amp; Investment Bank.</b> In January 2025 we combined our corporate and investment banking "
    "business with our commercial banking business to create a single Commercial &amp; Investment Bank. The "
    "combination gives middle-market clients direct access to our global product set, from payments and "
    "treasury services to capital markets. Global Payments revenue grew 7%, helped by real-time payments "
    "volume, which more than doubled after we opened our Real-Time Payments API to corporate clients.",
    "<b>Asset &amp; Wealth Management.</b> Client assets reached "
    f"${SEG['Asset & Wealth Management']['client_assets_bn'][0]/1000:.2f} trillion and assets under management "
    f"reached ${SEG['Asset & Wealth Management']['aum_bn'][0]/1000:.2f} trillion, driven by record long-term net "
    "inflows of $148 billion and higher market levels. Our wealth advisor headcount grew 6%.",
    "<b>Technology and data.</b> We spent $16.8 billion on technology in 2025, roughly half of it on new "
    "capabilities. Our Developer Platform now exposes eighteen production APIs covering accounts, payments, "
    "cards, credit, market data and regulatory reporting. These APIs are not only products for clients; they are "
    "also the governed data feeds for our most important risk models, including the models that set our "
    "allowance for credit losses, measure interest rate risk and project capital under stress. Building one set "
    "of well-controlled data pipes for both clients and regulators is one of the most important things we did "
    "this year.",
    "<b>Risk and controls.</b> We are realistic about what could go wrong. Geopolitical tension, sticky inflation, "
    "elevated asset prices and the rapid adoption of artificial intelligence all carry risks we take seriously. "
    "We continued to strengthen our model risk management, cyber defenses and third-party oversight, and we "
    "remain focused on operational resilience in our critical payment systems.",
    "Finally, I want to thank our 214,600 employees. Everything in this report is the result of their work, "
    "their judgment and their care for clients and communities.",
    f"Sincerely,<br/><b>{B.BANK['ceo']}</b><br/>Chairman and Chief Executive Officer",
)
story.append(PageBreak())

# ================================================================ 2. Highlights
story.append(h1("Financial Highlights"))
story.append(p("Selected consolidated financial data for the years ended December 31 (in millions, except per-share "
               "data and ratios)."))
rows = [["", "2025", "2024", "Change"]]
for k, lab in [("total_net_revenue", "Total net revenue"), ("net_interest_income", "Net interest income"),
               ("noninterest_revenue", "Noninterest revenue"), ("noninterest_expense", "Noninterest expense"),
               ("provision_for_credit_losses", "Provision for credit losses"), ("net_income", "Net income"),
               ("net_income_to_common", "Net income applicable to common stockholders")]:
    rows.append(yoy_row(lab, I[k]))
for k in ["Diluted EPS ($)", "Book value per share ($)", "Tangible book value per share ($)",
          "Dividends declared per share ($)"]:
    a, b = B.KEY_METRICS[k]
    rows.append([k.replace(" ($)", ""), f"${a:.2f}", f"${b:.2f}", pct(chg(a, b))])
for k in ["Return on common equity", "Return on tangible common equity (ROTCE)", "Overhead (efficiency) ratio"]:
    rows.append(yoy_row(k, B.KEY_METRICS[k], as_pct=True))
rows.append(yoy_row("CET1 ratio (Standardized)", CAP["CET1 ratio (Standardized)"], as_pct=True))
rows.append(yoy_row("Supplementary leverage ratio", CAP["Supplementary leverage ratio"], as_pct=True))
rows.append(["Total assets (period end)", m(B.TOTAL_ASSETS[0]), m(B.TOTAL_ASSETS[1]), pct(chg(*B.TOTAL_ASSETS))])
rows.append(yoy_row("Loans (period end)", B.BALANCE["Loans"]))
rows.append(yoy_row("Deposits (period end)", B.LIABS["Deposits"]))
rows.append(["Headcount", f"{B.KEY_METRICS['Headcount'][0]:,}", f"{B.KEY_METRICS['Headcount'][1]:,}",
             pct(chg(*B.KEY_METRICS['Headcount']))])
story.append(table(rows, [0.46, 0.18, 0.18, 0.18]))
story.append(bar_chart("ar_rev_seg", ["2024", "2025"],
                       {s: [SEG[s]["revenue"][1], SEG[s]["revenue"][0]] for s in list(SEG)[:3]},
                       "Net revenue by reportable segment ($mm)", ratio=0.33))
story.append(caption("Corporate segment excluded from chart (2025 net revenue: $(330) million)."))
story.append(PageBreak())

# ================================================================ 3. MD&A overview
story.append(h1("Management's Discussion and Analysis"))
story.append(h2("Executive Overview"))
story += ps(
    f"This Management's Discussion and Analysis (MD&amp;A) describes the financial condition and results of "
    f"operations of {nm} and its subsidiaries (collectively, \"{sh}\", \"the Firm\", \"we\") for 2025 compared with "
    "2024. It should be read with the Consolidated Financial Statements and Notes beginning on page "
    "\"Consolidated Financial Statements\" of this report. Certain amounts are presented on a managed basis, "
    "which adjusts revenue for the tax-equivalent impact of tax-exempt income; reconciliations appear in the "
    "earnings supplement.",
    f"{sh} is a financial holding company with operations in 31 countries. We organize our activities into three "
    "reportable business segments - Consumer &amp; Community Banking (CCB), Commercial &amp; Investment Bank "
    "(CIB) and Asset &amp; Wealth Management (AWM) - plus a Corporate segment that includes Treasury and the Chief "
    "Investment Office (Treasury/CIO), which manages the Firm's liquidity, investment securities portfolio and "
    "structural interest rate risk.",
)
story.append(h3("2025 at a glance"))
story += bullets([
    f"Net income of {bn(I['net_income'][0])}, up {pct(chg(*I['net_income']))}; diluted EPS of "
    f"${B.KEY_METRICS['Diluted EPS ($)'][0]:.2f}, up {pct(chg(*B.KEY_METRICS['Diluted EPS ($)']))}.",
    f"Net interest income of {bn(I['net_interest_income'][0])}, up {pct(chg(*I['net_interest_income']))}, driven by "
    "higher average loan and deposit balances partly offset by deposit margin compression late in the year.",
    f"Noninterest revenue of {bn(I['noninterest_revenue'][0])}, up {pct(chg(*I['noninterest_revenue']))}, on "
    "stronger investment banking fees, Markets revenue and asset management fees.",
    f"Provision for credit losses of {bn(I['provision_for_credit_losses'][0])}, including net charge-offs of "
    f"{bn(B.KEY_METRICS['Net charge-offs'][0])} and a net reserve build of $740 million, primarily in Card.",
    f"Noninterest expense of {bn(I['noninterest_expense'][0])}, up {pct(chg(*I['noninterest_expense']))}, reflecting "
    "compensation, technology investment and marketing; the overhead ratio improved to "
    f"{pct(B.KEY_METRICS['Overhead (efficiency) ratio'][0])}.",
    f"CET1 ratio of {pct(CAP['CET1 ratio (Standardized)'][0])} (Standardized), up "
    f"{(CAP['CET1 ratio (Standardized)'][0]-CAP['CET1 ratio (Standardized)'][1])*10000:.0f} bps; average LCR of "
    f"{B.LIQUIDITY['LCR (average, Q4)'][0]*100:.0f}% in the fourth quarter.",
])
story.append(h3("2026 outlook"))
story += ps(
    f"Management currently expects 2026 net interest income of approximately {bn(O['nii']['Base']['nii'], 1)}, "
    "assuming the forward rate curve as of year-end 2025 (two further 25 basis point policy rate reductions in "
    "2026) and modest loan growth. This expectation is consistent with the base-case output of the Firm's Net "
    "Interest Income Sensitivity Model (MDL-ALM-014) described under Market Risk Management. Adjusted noninterest "
    "expense is expected to be approximately $49.5 billion. We expect the full-year Card net charge-off rate to be "
    "approximately 3.6%.",
    "These expectations are forward-looking statements, subject to the risks and uncertainties described under "
    "Forward-Looking Statements and Risk Factors, and actual results may differ materially.",
)

# ================================================================ consolidated results
story.append(h2("Consolidated Results of Operations"))
story.append(h3("Net revenue"))
story += ps(
    f"Total net revenue was {bn(I['total_net_revenue'][0])}, an increase of "
    f"{bn(I['total_net_revenue'][0]-I['total_net_revenue'][1])} from 2024. Net interest income rose to "
    f"{bn(I['net_interest_income'][0])}, as growth in Card loans and wholesale deposits more than offset the "
    "impact of lower policy rates in the fourth quarter. The Firm's net interest yield on a managed basis was "
    "2.71%, down 4 basis points, reflecting a higher proportion of lower-yielding liquid assets.",
    "Noninterest revenue increased across most categories. Principal transactions revenue, which reflects Markets "
    "client activity, rose on higher volumes in Fixed Income and Equity Markets. Asset management fees increased "
    "with higher average market levels and strong net inflows. Investment securities losses of $410 million "
    "reflect repositioning of the available-for-sale portfolio within Treasury/CIO to extend duration ahead of "
    "expected rate cuts.",
)
rows = [["Noninterest revenue (in millions)", "2025", "2024", "Change"]]
for k, v in B.NONINT_DETAIL.items():
    rows.append(yoy_row(k, v))
rows.append(yoy_row("Total noninterest revenue", I["noninterest_revenue"]))
story.append(table(rows, [0.46, 0.18, 0.18, 0.18], total_rows=(-1,)))
story.append(h3("Provision for credit losses"))
story += ps(
    f"The provision for credit losses was {bn(I['provision_for_credit_losses'][0])}, compared with "
    f"{bn(I['provision_for_credit_losses'][1])} in 2024. The provision comprised net charge-offs of "
    f"{bn(B.KEY_METRICS['Net charge-offs'][0])} and a net addition to the allowance for credit losses of $740 "
    "million. The reserve build was driven by loan growth in Card and a modest increase in the weight placed on "
    "the downside macroeconomic scenario, partly offset by improved commercial real estate (CRE) valuations in "
    "the multifamily segment. See Credit Risk Management and Note 6 for further detail.",
)
story.append(h3("Noninterest expense"))
rows = [["Noninterest expense (in millions)", "2025", "2024", "Change"]]
for k, v in B.NONINT_EXP_DETAIL.items():
    rows.append(yoy_row(k, v))
rows.append(yoy_row("Total noninterest expense", I["noninterest_expense"]))
story.append(table(rows, [0.46, 0.18, 0.18, 0.18], total_rows=(-1,)))
story += ps(
    "Compensation expense increased 4.8%, reflecting higher revenue-related compensation in CIB and AWM and "
    "growth in bankers, advisors and technologists. Technology, communications and equipment expense rose 7.3% "
    "as we migrated additional applications to public and private cloud, expanded the Developer Platform and "
    "retired 1,140 legacy applications. Other expense declined due to lower legal expense and a lower FDIC "
    "special assessment.",
    f"Income tax expense was {bn(I['income_tax_expense'][0])}, an effective tax rate of "
    f"{pct(I['income_tax_expense'][0]/I['income_before_tax'][0])} compared with "
    f"{pct(I['income_tax_expense'][1]/I['income_before_tax'][1])} in 2024, reflecting changes in the "
    "geographic mix of income and lower benefits from tax-oriented investments.",
)
story.append(PageBreak())

# ================================================================ segments
story.append(h1("Business Segment Results"))
story += ps(
    "The Firm's segment results are presented on a managed basis. Capital is allocated to each segment based on "
    "its standalone risk profile, including regulatory capital requirements under the Standardized approach, "
    "the stress capital buffer and the G-SIB surcharge. Segment return on equity (ROE) is net income less "
    "preferred dividends allocated, divided by average allocated equity.",
)
rows = [["Segment results (in millions)", "Net revenue 2025", "Net revenue 2024", "Net income 2025",
         "Net income 2024", "ROE 2025"]]
for sname, s in SEG.items():
    rows.append([sname, m(s["revenue"][0]), m(s["revenue"][1]), m(s["net_income"][0]), m(s["net_income"][1]),
                 pct(s["roe"][0], 0) if "roe" in s else "NM"])
rows.append(["Total Firm", m(I["total_net_revenue"][0]), m(I["total_net_revenue"][1]), m(I["net_income"][0]),
             m(I["net_income"][1]), pct(B.KEY_METRICS["Return on common equity"][0], 0)])
story.append(table(rows, [0.32, 0.136, 0.136, 0.136, 0.136, 0.136], total_rows=(-1,)))


def seg_table(s, extra):
    rows = [["(in millions, except ratios)", "2025", "2024", "Change"]]
    rows.append(yoy_row("Net revenue", s["revenue"]))
    rows.append(yoy_row("  of which: net interest income", s["nii"]))
    rows.append(yoy_row("Provision for credit losses", s["provision"]))
    rows.append(yoy_row("Noninterest expense", s["expense"]))
    rows.append(yoy_row("Net income", s["net_income"]))
    if "equity_allocated" in s:
        rows.append(yoy_row("Average equity allocated", s["equity_allocated"]))
        rows.append(yoy_row("Return on equity", s["roe"], as_pct=True))
    rows += extra
    return table(rows, [0.46, 0.18, 0.18, 0.18], bold_rows=(5,))


ccb = SEG["Consumer & Community Banking"]
story.append(h2("Consumer & Community Banking"))
story += ps(
    "CCB offers deposit, investment and lending products, payments and services to consumers and small "
    "businesses through Banking &amp; Wealth Management, Home Lending, Card Services and Auto. The segment "
    f"serves 74 million customers through {B.BANK['branches']:,} branches, {B.BANK['atms']:,} ATMs and digital "
    "channels.",
    f"Net income was {bn(ccb['net_income'][0])}, up {pct(chg(*ccb['net_income']))}. Net revenue increased "
    f"{pct(chg(*ccb['revenue']))} to {bn(ccb['revenue'][0])}, driven by higher Card net interest income on loan "
    "growth and higher card spend, partly offset by deposit margin compression. Average deposits grew "
    f"{pct(chg(*ccb['avg_deposits']))} to {bn(ccb['avg_deposits'][0])} as customers moved balances back from "
    "money market funds late in the year.",
    f"The provision for credit losses was {bn(ccb['provision'][0])}, reflecting Card net charge-offs of $4.6 "
    f"billion and a reserve build of $600 million. The Card net charge-off rate was {pct(ccb['card_nco_rate'][0], 2)} "
    f"compared with {pct(ccb['card_nco_rate'][1], 2)} in 2024, consistent with continued normalization of "
    "consumer credit. Home Lending credit remained very strong, with net charge-offs of only $40 million.",
)
story.append(seg_table(ccb, [
    yoy_row("Average loans", ccb["avg_loans"]), yoy_row("Average deposits", ccb["avg_deposits"]),
    yoy_row("Card net charge-off rate", ccb["card_nco_rate"], as_pct=True),
    ["Active mobile users (millions)", f"{ccb['active_mobile_users_mm'][0]:.1f}",
     f"{ccb['active_mobile_users_mm'][1]:.1f}", pct(chg(*ccb['active_mobile_users_mm']))],
]))
story += ps(
    "<b>Digital and payments.</b> Active mobile users grew 6% to 61.4 million. Customers initiated 4.1 billion "
    "Zelle-style person-to-person and real-time payments, and 79% of deposit account openings were completed "
    "digitally. Account and transaction data shown in our consumer apps is served through the Accounts API and "
    "Transactions API, which are also offered to aggregators under our data-access agreements.",
)

cib = SEG["Commercial & Investment Bank"]
story.append(CondPageBreak(3.5 * 72))
story.append(h2("Commercial & Investment Bank"))
story += ps(
    "CIB provides investment banking, markets, securities services, global payments and lending to corporations, "
    "institutional investors, financial institutions, middle-market companies, real estate investors and "
    "government entities. In 2025 we completed the integration of the former Commercial Banking segment into CIB.",
    f"Net income was {bn(cib['net_income'][0])}, up {pct(chg(*cib['net_income']))}, on net revenue of "
    f"{bn(cib['revenue'][0])}. Investment banking fees rose {pct(chg(*cib['ib_fees']))} to {bn(cib['ib_fees'][0])}, "
    "led by debt underwriting and a recovery in advisory activity. Markets revenue was a record "
    f"{bn(cib['markets_revenue'][0])}, up {pct(chg(*cib['markets_revenue']))}, with strength in rates, securitized "
    "products and equity derivatives. Global Payments revenue was $9.6 billion, up 7%, on higher deposit "
    "balances and fee growth from real-time payments and cross-border wires.",
    f"The provision for credit losses was {m(cib['provision'][0])} million, including net charge-offs concentrated in "
    "office CRE and a small number of C&amp;I names in the consumer discretionary sector. Average loans grew "
    f"{pct(chg(*cib['avg_loans']))}.",
)
story.append(seg_table(cib, [
    yoy_row("Investment banking fees", cib["ib_fees"]), yoy_row("Markets revenue", cib["markets_revenue"]),
    yoy_row("Average loans", cib["avg_loans"]), yoy_row("Average deposits", cib["avg_deposits"]),
]))

awm = SEG["Asset & Wealth Management"]
story.append(CondPageBreak(3.5 * 72))
story.append(h2("Asset & Wealth Management"))
story += ps(
    "AWM offers investment and wealth management solutions to institutions, retail investors and high-net-worth "
    "individuals across equities, fixed income, alternatives, multi-asset and liquidity strategies, as well as "
    "lending, banking and trust services through Global Private Bank.",
    f"Net income was {bn(awm['net_income'][0])}, up {pct(chg(*awm['net_income']))}, on net revenue of "
    f"{bn(awm['revenue'][0])}. Management fees grew on higher average market levels and record long-term net "
    f"inflows. Assets under management were ${awm['aum_bn'][0]:,} billion and client assets were "
    f"${awm['client_assets_bn'][0]:,} billion at year end. Pre-tax margin was 36%.",
)
story.append(seg_table(awm, [
    ["Assets under management ($bn)", f"{awm['aum_bn'][0]:,}", f"{awm['aum_bn'][1]:,}", pct(chg(*awm['aum_bn']))],
    ["Client assets ($bn)", f"{awm['client_assets_bn'][0]:,}", f"{awm['client_assets_bn'][1]:,}",
     pct(chg(*awm['client_assets_bn']))],
    yoy_row("Average loans", awm["avg_loans"]),
]))
corp = SEG["Corporate"]
story.append(h2("Corporate"))
story += ps(
    "The Corporate segment consists of Treasury/CIO and Other Corporate, which includes centrally managed "
    "functions and expense not allocated to the business segments. Treasury/CIO manages the Firm's liquidity, "
    "funding, capital and structural interest rate and foreign exchange risks, and the investment securities "
    "portfolio. It is the owner of the Net Interest Income Sensitivity Model and the Capital Planning &amp; Stress "
    "Projection Model.",
    f"Corporate reported a net loss of {usd(corp['net_income'][0])} million compared with "
    f"{usd(corp['net_income'][1])} million in 2024. Net revenue of {usd(corp['revenue'][0])} million included "
    "$410 million of investment securities losses from portfolio repositioning, partly offset by higher net "
    "interest income on the investment portfolio.",
)
story.append(PageBreak())

# ================================================================ balance sheet
story.append(h1("Balance Sheet Analysis"))
story += ps(
    f"Total assets were {bn(B.TOTAL_ASSETS[0])} at December 31, 2025, up {pct(chg(*B.TOTAL_ASSETS))}. The increase "
    "reflected loan growth, higher securities purchased under resale agreements in CIB and higher investment "
    "securities, partly offset by lower deposits with banks as Treasury/CIO deployed excess cash into "
    "high-quality securities.",
    f"Loans grew {pct(chg(*B.BALANCE['Loans']))} to {bn(B.BALANCE['Loans'][0])}, driven by Card, CRE multifamily "
    f"and C&amp;I lending to middle-market clients. Deposits grew {pct(chg(*B.LIABS['Deposits']))} to "
    f"{bn(B.LIABS['Deposits'][0])}, with growth in wholesale operating deposits and consumer savings. The "
    f"loan-to-deposit ratio was {B.BALANCE['Loans'][0]/B.LIABS['Deposits'][0]*100:.0f}%.",
)
rows = [["Selected balance sheet data (in millions)", "Dec 31, 2025", "Dec 31, 2024", "Change"]]
for k in ["Cash and due from banks", "Deposits with banks",
          "Federal funds sold and securities purchased under resale agreements", "Trading assets",
          "Available-for-sale securities", "Held-to-maturity securities, net", "Loans", "Allowance for loan losses"]:
    rows.append(yoy_row(k, B.BALANCE[k]))
rows.append(["Total assets", m(B.TOTAL_ASSETS[0]), m(B.TOTAL_ASSETS[1]), pct(chg(*B.TOTAL_ASSETS))])
for k in ["Deposits", "Long-term debt", "Short-term borrowings"]:
    rows.append(yoy_row(k, B.LIABS[k]))
rows.append(yoy_row("Total stockholders' equity", B.TOTAL_EQUITY))
story.append(table(rows, [0.5, 0.17, 0.17, 0.16], bold_rows=(9, 13)))
story.append(bar_chart("ar_loans_mix", [s[0].replace("Commercial & Industrial", "C&I").replace(
    "Commercial Real Estate", "CRE").replace("Other Consumer & Wholesale", "Other").replace(
    "Residential Mortgage", "Resi mortgage") for s in B.CECL_SEGMENTS],
    {"Loans, Dec 31 2025 ($mm)": [s[1] for s in B.CECL_SEGMENTS]}, "Loan portfolio by segment", ratio=0.32))
story.append(PageBreak())

# ================================================================ capital
story.append(h1("Capital Risk Management"))
story += ps(
    "Capital risk is the risk that the Firm has insufficient capital to support its business activities and "
    "associated risks during normal economic environments and under stressed conditions. The Firm's capital "
    "management objectives are to hold capital sufficient to cover all material risks, remain \"well "
    "capitalized\" under applicable regulations, maintain debt ratings that support our franchise, and retain "
    "flexibility to take advantage of future opportunities.",
    "The Board of Directors approves the Firm's Capital Policy and risk appetite. The Capital Governance "
    "Committee, chaired by the Chief Financial Officer, oversees capital planning, the Comprehensive Capital "
    "Analysis and Review (CCAR) submission and contingency capital planning. Capital projections are produced "
    "using the <b>Capital Planning &amp; Stress Projection Model (MDL-CAP-003)</b>, owned by Corporate Treasury - "
    "Capital Management, which projects CET1 capital, risk-weighted assets and capital ratios over a nine-quarter "
    "horizon under baseline and severely adverse scenarios. Starting capital and RWA are sourced from the Firm's "
    "Regulatory Reporting API (API-16), and scenario variables from the Macroeconomic Scenario API (API-14).",
)
rows = [["Regulatory capital (in millions, except ratios)", "Dec 31, 2025", "Dec 31, 2024", "Change"]]
for k in ["CET1 capital", "Tier 1 capital", "Total capital", "Standardized RWA", "Advanced RWA",
          "Total leverage exposure"]:
    rows.append(yoy_row(k, CAP[k]))
for k in ["CET1 ratio (Standardized)", "Tier 1 ratio (Standardized)", "Total capital ratio (Standardized)",
          "Tier 1 leverage ratio", "Supplementary leverage ratio"]:
    rows.append(yoy_row(k, CAP[k], as_pct=True))
story.append(table(rows, [0.5, 0.17, 0.17, 0.16]))
req = B.CAP_REQ
story.append(h3("Capital requirements"))
story += ps(
    f"The Firm's Standardized CET1 requirement is {pct(req['minimum'] + req['stress_capital_buffer'] + req['gsib_surcharge'])}, "
    f"comprising the {pct(req['minimum'])} regulatory minimum, a stress capital buffer (SCB) of "
    f"{pct(req['stress_capital_buffer'])} effective October 1, 2025, and a G-SIB surcharge of "
    f"{pct(req['gsib_surcharge'])}. The countercyclical capital buffer is currently set at zero. Management "
    f"targets a CET1 ratio of approximately {pct(req['management_target'])}, providing a buffer above the "
    "requirement for macroeconomic uncertainty and pending regulatory changes, including the proposed revisions "
    "to the U.S. capital framework.",
)
story.append(h3("Capital planning and stress testing"))
story += ps(
    "The Firm participates annually in the Federal Reserve's CCAR process and runs its own internally developed "
    "severely adverse scenario at least semi-annually. In the 2025 supervisory stress test, the Firm's projected "
    "peak-to-trough CET1 decline plus four quarters of planned dividends resulted in a stress capital buffer of "
    f"{pct(req['stress_capital_buffer'])}, effective October 1, 2025 through September 30, 2026.",
    "The Capital Planning &amp; Stress Projection Model is re-run each quarter with updated starting capital, "
    "RWA and scenario paths. The model projects: (1) the baseline CET1 path after planned dividends and share "
    "repurchases; (2) the severely adverse CET1 path assuming buybacks are suspended and dividends held flat; and "
    "(3) an indicative SCB equal to the peak-to-trough decline plus four quarters of planned dividends as a "
    "percentage of starting RWA, floored at 2.5%. The most recent projection, based on June 30, 2026 starting "
    "capital, is presented in the Firm's Q2 2026 Earnings Release and Financial Supplement.",
)
story.append(h3("Capital actions"))
story += ps(
    "In 2025 the Firm declared common dividends of $4.30 per share ($6.1 billion) and repurchased $11.0 billion of "
    "common stock (38.3 million shares). In June 2025 the Board authorized a new $30 billion common share "
    "repurchase program effective through 2028. The amount and timing of repurchases depend on capital position, "
    "market conditions, regulatory considerations and alternative uses of capital.",
)
story.append(PageBreak())

# ================================================================ liquidity
story.append(h1("Liquidity Risk Management"))
story += ps(
    "Liquidity risk is the risk that the Firm will be unable to meet its contractual and contingent financial "
    "obligations as they arise, or that it does not have the appropriate amount, composition and tenor of "
    "funding and liquidity to support its assets and liabilities. Treasury/CIO is responsible for liquidity risk "
    "management, with independent oversight by the Liquidity Risk Oversight function within the Chief Risk "
    "Office.",
    "Liquidity positions across all legal entities are aggregated daily through the <b>Treasury Liquidity "
    "Positions API (API-15)</b>, which publishes intraday cash, collateral and high-quality liquid asset (HQLA) "
    "positions to the liquidity stress testing engine and to the Firm's asset-liability management models. The "
    "same feed supplies balance sheet positions to the Net Interest Income Sensitivity Model.",
)
rows = [["Liquidity metrics", "2025", "2024"]]
L = B.LIQUIDITY
rows += [["Liquidity coverage ratio (average, Q4)", f"{L['LCR (average, Q4)'][0]*100:.0f}%", f"{L['LCR (average, Q4)'][1]*100:.0f}%"],
         ["Net stable funding ratio", f"{L['NSFR'][0]*100:.0f}%", f"{L['NSFR'][1]*100:.0f}%"],
         ["HQLA, average Q4 (in millions)", m(L["HQLA (average, Q4)"][0]), m(L["HQLA (average, Q4)"][1])],
         ["Unencumbered marketable securities (in millions)", m(L["Unencumbered marketable securities"][0]),
          m(L["Unencumbered marketable securities"][1])],
         ["Loan-to-deposit ratio", f"{B.BALANCE['Loans'][0]/B.LIABS['Deposits'][0]*100:.0f}%",
          f"{B.BALANCE['Loans'][1]/B.LIABS['Deposits'][1]*100:.0f}%"]]
story.append(table(rows, [0.6, 0.2, 0.2]))
story += ps(
    "The Firm's primary source of funding is its deposit base, which is diversified by client type, product and "
    "geography. Approximately 66% of deposits are from consumer and small-business clients, and an estimated 58% "
    "of total deposits are insured or fully collateralized. Wholesale operating deposits arising from payments, "
    "custody and cash-management relationships provide a stable source of funding. Long-term debt outstanding "
    f"was {bn(B.LIABS['Long-term debt'][0])}, with a weighted-average remaining maturity of 6.8 years.",
    "The Firm's internal liquidity stress tests assume a 90-day idiosyncratic and market-wide stress, including "
    "the loss of unsecured wholesale funding, accelerated deposit outflows, collateral calls from a three-notch "
    "downgrade, and draws on committed facilities. At December 31, 2025, the Firm's liquidity sources exceeded "
    "stressed outflows in every material legal entity.",
    "Credit ratings: Moody's Aa2 (long-term deposits, bank), S&amp;P A+ (holding company senior unsecured), Fitch AA- "
    "(holding company). All outlooks were stable at year end. (Ratings shown are fictional.)",
)

# ================================================================ credit risk
story.append(h1("Credit Risk Management"))
story += ps(
    "Credit risk is the risk associated with the default or change in credit profile of a client, counterparty "
    "or customer. The Firm provides credit to consumers through mortgages, auto loans and credit cards, and to "
    "businesses through loans, lending-related commitments and derivatives. Credit risk is managed by the "
    "independent Chief Risk Office and the lines of business within a Board-approved risk appetite framework.",
    "Credit decisions for consumer products are made using automated scorecards exposed through the <b>Credit "
    "Decisioning API (API-09)</b>, which combines bureau data, internal behavior scores and fraud signals from the "
    "Fraud Risk Signals API (API-08). Portfolio-level probability of default (PD) and loss given default (LGD) "
    "estimates are produced by the <b>Credit Risk Scoring API (API-10)</b>, which serves pool-level parameters to "
    "the CECL model, regulatory capital calculations and portfolio monitoring dashboards.",
)
rows = [["Loan portfolio (in millions)", "Loans", "% of total", "Net charge-offs", "NCO rate", "Allowance",
         "Allowance / loans"]]
for seg, bal, allow, lob in B.CECL_SEGMENTS:
    nco = B.NCO_BY_SEGMENT[seg]
    rows.append([seg, m(bal), pct(bal / B.BALANCE["Loans"][0]), m(nco), pct(nco / bal, 2), m(allow), pct(allow / bal, 2)])
rows.append(["Total", m(B.BALANCE["Loans"][0]), "100.0%", m(B.KEY_METRICS["Net charge-offs"][0]),
             pct(B.KEY_METRICS["Net charge-offs"][0] / B.BALANCE["Loans"][0], 2), m(15_920),
             pct(15_920 / B.BALANCE["Loans"][0], 2)])
story.append(table(rows, [0.28, 0.12, 0.1, 0.13, 0.1, 0.12, 0.15], total_rows=(-1,)))
story.append(h2("Consumer credit portfolio"))
story += ps(
    f"The consumer portfolio, including Card, Residential Mortgage, Auto and other consumer loans, totaled "
    f"{bn(138_400 + 218_600 + 64_900 + 24_000)}. Card 30+ day delinquency was 2.31% at year end, up 12 basis points; "
    "90+ day delinquency was 1.18%. Residential mortgage credit remained excellent, with a weighted-average "
    "current loan-to-value ratio of 51% and FICO of 768. Auto delinquencies were stable.",
)
story.append(h2("Wholesale credit portfolio"))
story += ps(
    "Wholesale exposure, including loans, lending-related commitments and derivative receivables, was $1.21 "
    "trillion, of which 74% was investment grade. CRE loans of $98.2 billion are concentrated in multifamily "
    "(61%), with office representing 9% of CRE loans. Criticized office exposure declined in the second half as "
    "borrowers refinanced or paid down loans. Within C&amp;I, the largest industry exposures are technology, "
    "media &amp; telecom (11%), consumer &amp; retail (10%), industrials (9%) and healthcare (7%).",
)
story.append(h2("Allowance for Credit Losses"))
cl = O["cecl"]
story += ps(
    "The allowance for credit losses represents management's estimate of expected credit losses over the "
    "remaining expected life of the Firm's loans, in accordance with ASC 326 (Current Expected Credit Losses, or "
    "CECL). The allowance is estimated using the <b>CECL Lifetime Expected Credit Loss Model (MDL-CR-007)</b>, "
    "owned by Consumer &amp; Wholesale Credit Risk - Allowance Methodology and independently validated by Model "
    "Risk Governance &amp; Review in November 2025.",
    "The model estimates lifetime expected loss for each portfolio segment as exposure at default multiplied by "
    "lifetime probability of default and loss given default under each of three macroeconomic scenarios "
    "supplied by the Macroeconomic Scenario API (API-14). Scenario-conditional estimates are weighted by the "
    "probabilities approved by the Firm's Scenario Committee. Loan balances and remaining lives are sourced from "
    "the Loan Servicing API (API-11). Management then applies qualitative adjustments for risks not fully "
    "captured by the models.",
)
rows = [["Scenario (as of Dec 31, 2025)", "Weight", "Peak unemployment", "Real GDP 2026", "House prices",
         "CRE prices"]]
for n, v in B.MACRO_SCENARIOS.items():
    rows.append([n, pct(v[0], 0), pct(v[1]), pct(v[2]), pct(v[3]), pct(v[4])])
story.append(table(rows, [0.25, 0.13, 0.17, 0.15, 0.15, 0.15]))
rows = [["Allowance by segment (in millions)", "Modeled", "Qualitative overlay", "Total allowance", "Coverage"]]
for seg, v in cl.items():
    rows.append([seg, m(v["modeled"]), m(v["overlay"]), m(v["total"]), pct(v["coverage"], 2)])
story.append(table(rows, [0.36, 0.16, 0.16, 0.16, 0.16], total_rows=(-1,),
                   note="Source: CECL_Allowance_Model.xlsx, sheet Allowance_Summary."))
sens = O["cecl_sens"]
story += ps(
    "<b>Sensitivity.</b> The allowance is sensitive to scenario weights. If the Firm had applied a 100% weight to "
    f"the downside scenario, the allowance would have been approximately {bn(sens['100% Downside']['allowance'])}, "
    f"or {bn(sens['100% Downside']['delta'])} higher than reported. A 100% weight on the baseline scenario would "
    f"have reduced the allowance by approximately {bn(-sens['100% Baseline']['delta'])}. These sensitivities hold "
    "the qualitative overlay constant and do not represent management's expectation of losses.",
)
story.append(PageBreak())

# ================================================================ market risk
story.append(h1("Market Risk Management"))
story += ps(
    "Market risk is the risk associated with the effect of changes in market factors, such as interest and "
    "foreign exchange rates, equity and commodity prices, credit spreads or implied volatilities, on the value "
    "of assets and liabilities held for both the short and long term. Market Risk Management, part of the "
    "independent risk function, sets limits, monitors exposures and reports to the Board Risk Committee.",
    "Trading positions are valued daily using prices, curves and volatility surfaces published by the "
    "<b>Market Data API (API-12)</b> and foreign exchange rates from the <b>FX Rates API (API-13)</b>. Both feeds "
    "are designated critical data elements under the Firm's BCBS 239 program.",
)
rows = [["Average 95% 1-day VaR (in millions)", "2025", "2024", "Min 2025", "Max 2025"],
        ["Fixed income", "38", "41", "27", "55"], ["Foreign exchange", "9", "8", "5", "16"],
        ["Equities", "15", "13", "9", "24"], ["Commodities and other", "7", "8", "4", "12"],
        ["Credit portfolio and other", "12", "14", "8", "19"],
        ["Diversification benefit", "(31)", "(33)", "NM", "NM"], ["Total VaR", "50", "51", "37", "71"]]
story.append(table(rows, [0.4, 0.15, 0.15, 0.15, 0.15], total_rows=(-1,),
                   note="VaR is calculated using historical simulation over a one-year look-back. There were 3 "
                        "backtesting exceptions in 2025, within the expected range."))
story.append(h2("Structural interest rate risk (IRRBB)"))
n = O["nii"]
story += ps(
    "Structural interest rate risk arises from the Firm's traditional banking activities, including the "
    "extension of loans and credit facilities, the taking of deposits and the issuance of debt. Treasury/CIO "
    "manages this risk through the investment securities portfolio and interest rate derivatives, within limits "
    "approved by the Board Risk Committee.",
    "The Firm measures earnings-at-risk using the <b>Net Interest Income Sensitivity Model (MDL-ALM-014)</b>, "
    "owned by Corporate Treasury - Asset &amp; Liability Management. The model applies instantaneous parallel "
    "shocks to the year-end balance sheet and measures the change in net interest income over the following "
    "twelve months. Each position reprices for the portion of the horizon remaining after its repricing date, and "
    "deposit rates move by the shock multiplied by a product-specific deposit beta (0.45 for consumer "
    "interest-bearing deposits, 0.75 for wholesale interest-bearing deposits). Balances and rates are sourced "
    "from the Treasury Liquidity Positions API (API-15), loan repricing profiles from the Loan Servicing API "
    "(API-11) and the yield curve from the Market Data API (API-12).",
)
rows = [["12-month NII sensitivity (in millions)", "Shock", "Projected NII", "Change in NII", "% change",
         "Change in EVE (% Tier 1)"]]
for k in ["Down 200", "Down 100", "Base", "Up 100", "Up 200"]:
    v = n[k]
    rows.append([k, f"{v['shock']:+d} bps" if v['shock'] else "0 bps", m(v["nii"]), m(v["delta"]), pct(v["pct"], 1),
                 pct(v["eve_pct"], 1)])
story.append(table(rows, [0.28, 0.12, 0.15, 0.15, 0.12, 0.18],
                   note="Source: NII_Sensitivity_Model.xlsx, sheet Summary. Static balance sheet; parallel shocks."))
story += ps(
    f"At December 31, 2025, the Firm was asset-sensitive: a +100 basis point parallel shock would increase "
    f"projected NII by approximately {bn(n['Up 100']['delta'])} ({pct(n['Up 100']['pct'])}), while a -200 basis point "
    f"shock would reduce it by {bn(-n['Down 200']['delta'])} ({pct(n['Down 200']['pct'])}), within the Board limit "
    "of a 7.0% decline. The economic value of equity (EVE) declines modestly in rising-rate scenarios because "
    "the duration of fixed-rate mortgages and investment securities exceeds that of the Firm's modeled deposit "
    "liabilities. The results do not reflect management actions, changes in balance sheet mix or non-parallel "
    "curve movements, which are captured in the quarterly dynamic simulation.",
)
story.append(PageBreak())

# ================================================================ model risk & tech
story.append(h1("Model Risk Management"))
story += ps(
    "Model risk is the potential for adverse consequences from decisions based on incorrect or misused model "
    "outputs. The Firm uses models for many purposes, including valuing exposures, measuring risk, estimating "
    "credit losses, determining capital and making business decisions. Model risk is governed by the Model Risk "
    "Policy, which aligns with supervisory guidance SR 11-7, and overseen by the Model Risk Governance &amp; "
    "Review (MRGR) function, which reports to the Chief Risk Officer.",
    "Each model is assigned a risk tier based on materiality and complexity. Tier 1 models require annual "
    "independent validation, documented ongoing performance monitoring, and approval by the Firmwide Model Risk "
    "Committee before use. Each model's upstream data feeds are registered in the model inventory; changes to an "
    "upstream API's schema or business logic trigger a model change review. The Firm's inventory includes "
    "approximately 2,900 models, of which the following three Tier 1 models directly drive amounts and metrics "
    "disclosed in this report:",
)
rows = [["Model ID", "Model", "Owner", "Upstream APIs", "Last validated"]]
for md in B.MODELS:
    rows.append([md["id"], md["name"], md["owner"], ", ".join(a.split(" ")[0] for a in md["apis"]),
                 md["last_validation"]])
story.append(table(rows, [0.13, 0.25, 0.3, 0.18, 0.14]))
story += bullets([f"<b>{md['id']} - {md['name']}:</b> {md['purpose']} Disclosed in: {'; '.join(md['reports'])}."
                  for md in B.MODELS])
story.append(h1("Operational, Technology and Cybersecurity Risk"))
story += ps(
    "Operational risk is the risk of an adverse outcome resulting from inadequate or failed internal processes "
    "or systems, human factors or external events, including cybersecurity, technology, third-party, fraud and "
    "conduct risks. The Firm's Operational Risk Management Framework establishes risk and control self-assessments, "
    "key risk indicators, scenario analysis and loss data collection across all lines of business.",
    f"<b>Technology and the Developer Platform.</b> Under the oversight of Chief Technology Officer {B.BANK['cto']}, the "
    "Firm operates a single Developer Platform that exposes eighteen production APIs to internal applications, "
    "clients and approved third parties. APIs are versioned, authenticated using OAuth 2.0 with mutual TLS for "
    "server-to-server traffic, rate-limited and monitored against published service-level objectives. In 2025 "
    "the platform handled an average of 4.0 billion calls per month with 99.97% availability. APIs that feed "
    "Tier 1 models or regulatory reports - the Credit Risk Scoring, Loan Servicing, Market Data, Macroeconomic "
    "Scenario, Treasury Liquidity Positions and Regulatory Reporting APIs - are classified as critical data "
    "services with enhanced change management and data-quality controls.",
    "<b>Cybersecurity.</b> The Firm spends more than $1 billion annually on cybersecurity and employs over 3,500 "
    "cybersecurity professionals. Controls include continuous vulnerability management, zero-trust network "
    "segmentation, phishing-resistant multifactor authentication and 24x7 global security operations. The Firm "
    "experienced no material cybersecurity incidents in 2025.",
    "<b>Fraud.</b> Real-time fraud scoring through the Fraud Risk Signals API (API-08) is applied to every card "
    "authorization, real-time payment and wire. Fraud losses as a percentage of card sales declined to 7.9 basis "
    "points.",
    "<b>Operational resilience.</b> Critical services - including payments clearing, card authorization and "
    "client access to deposits - are mapped end to end, with impact tolerances tested at least annually through "
    "severe-but-plausible scenarios.",
)
story.append(PageBreak())

# ================================================================ financial statements
story.append(h1("Consolidated Financial Statements"))
story.append(h2("Consolidated Statements of Income"))
rows = [["Year ended December 31 (in millions, except per share)", "2025", "2024"]]
rows += [["Revenue", "", ""]]
for k, v in B.NONINT_DETAIL.items():
    rows.append([k, m(v[0]), m(v[1])])
rows.append(["Total noninterest revenue", m(I["noninterest_revenue"][0]), m(I["noninterest_revenue"][1])])
nii_gross = (79_340, 77_120)
rows += [["Interest income", m(nii_gross[0]), m(nii_gross[1])],
         ["Interest expense", m(nii_gross[0] - I["net_interest_income"][0]), m(nii_gross[1] - I["net_interest_income"][1])],
         ["Net interest income", m(I["net_interest_income"][0]), m(I["net_interest_income"][1])],
         ["Total net revenue", m(I["total_net_revenue"][0]), m(I["total_net_revenue"][1])],
         ["Provision for credit losses", m(I["provision_for_credit_losses"][0]), m(I["provision_for_credit_losses"][1])]]
for k, v in B.NONINT_EXP_DETAIL.items():
    rows.append([k, m(v[0]), m(v[1])])
rows += [["Total noninterest expense", m(I["noninterest_expense"][0]), m(I["noninterest_expense"][1])],
         ["Income before income tax expense", m(I["income_before_tax"][0]), m(I["income_before_tax"][1])],
         ["Income tax expense", m(I["income_tax_expense"][0]), m(I["income_tax_expense"][1])],
         ["Net income", m(I["net_income"][0]), m(I["net_income"][1])],
         ["Net income applicable to common stockholders", m(I["net_income_to_common"][0]), m(I["net_income_to_common"][1])],
         ["Average diluted shares (millions)", m(I["diluted_shares_mm"][0]), m(I["diluted_shares_mm"][1])],
         ["Diluted earnings per share ($)", f"{B.KEY_METRICS['Diluted EPS ($)'][0]:.2f}", f"{B.KEY_METRICS['Diluted EPS ($)'][1]:.2f}"]]
bold = [i for i, r in enumerate(rows) if r[0].startswith(("Total", "Net income", "Income before", "Revenue", "Diluted"))]
story.append(table(rows, [0.62, 0.19, 0.19], bold_rows=bold))
story.append(PageBreak())
story.append(h2("Consolidated Balance Sheets"))
rows = [["December 31 (in millions)", "2025", "2024"], ["Assets", "", ""]]
for k, v in B.BALANCE.items():
    rows.append([k, m(v[0]), m(v[1])])
rows.append(["Total assets", m(B.TOTAL_ASSETS[0]), m(B.TOTAL_ASSETS[1])])
rows.append(["Liabilities", "", ""])
for k, v in B.LIABS.items():
    rows.append([k, m(v[0]), m(v[1])])
tl = (sum(v[0] for v in B.LIABS.values()), sum(v[1] for v in B.LIABS.values()))
rows.append(["Total liabilities", m(tl[0]), m(tl[1])])
rows.append(["Stockholders' equity", "", ""])
for k, v in B.EQUITY.items():
    rows.append([k, m(v[0]), m(v[1])])
rows.append(["Total stockholders' equity", m(B.TOTAL_EQUITY[0]), m(B.TOTAL_EQUITY[1])])
rows.append(["Total liabilities and stockholders' equity", m(tl[0] + B.TOTAL_EQUITY[0]), m(tl[1] + B.TOTAL_EQUITY[1])])
bold = [i for i, r in enumerate(rows) if r[0].startswith(("Total", "Assets", "Liabilities", "Stockholders"))]
story.append(table(rows, [0.62, 0.19, 0.19], bold_rows=bold))
story.append(h2("Consolidated Statements of Cash Flows (condensed)"))
rows = [["Year ended December 31 (in millions)", "2025", "2024"],
        ["Net income", m(I["net_income"][0]), m(I["net_income"][1])],
        ["Provision for credit losses", m(I["provision_for_credit_losses"][0]), m(I["provision_for_credit_losses"][1])],
        ["Depreciation and amortization", "8,140", "7,720"],
        ["Net change in trading assets and liabilities", "(10,000)", "(14,350)"],
        ["Other operating adjustments", "3,920", "(2,180)"],
        ["Net cash provided by operating activities", "33,860", "20,690"],
        ["Net change in loans", "(30,540)", "(26,410)"],
        ["Net purchases of investment securities", "(3,200)", "(9,850)"],
        ["Net change in resale agreements and other", "(13,900)", "(6,300)"],
        ["Net cash used in investing activities", "(47,640)", "(42,560)"],
        ["Net change in deposits", "34,100", "29,800"],
        ["Net change in borrowings and long-term debt", "8,400", "6,100"],
        ["Common dividends and share repurchases", "(17,100)", "(15,900)"],
        ["Preferred dividends and redemptions", "(1,560)", "(1,080)"],
        ["Net cash provided by financing activities", "23,840", "18,920"],
        ["Net change in cash and deposits with banks", "10,060", "(2,950)"]]
story.append(table(rows, [0.62, 0.19, 0.19], bold_rows=(6, 10, 15, 16)))
story.append(caption("Condensed presentation for illustrative purposes; cash and deposits with banks also reflect "
                     "foreign exchange and restricted cash movements not shown."))
story.append(PageBreak())

# ================================================================ notes
story.append(h1("Notes to Consolidated Financial Statements"))
story.append(h2("Note 1 - Basis of Presentation"))
story += ps(
    f"{nm} is a financial holding company incorporated under Delaware law. The Consolidated Financial Statements "
    "are prepared in accordance with U.S. generally accepted accounting principles (U.S. GAAP). The preparation "
    "of financial statements requires management to make estimates and assumptions, the most significant of "
    "which relate to the allowance for credit losses, fair value measurements, goodwill impairment, legal "
    "reserves and income taxes. Actual results could differ from those estimates.",
)
story.append(h2("Note 2 - Significant Accounting Policies"))
story += ps(
    "<b>Loans.</b> Loans held for investment are measured at amortized cost. Interest income is recognized using "
    "the effective interest method. Consumer loans are generally placed on nonaccrual status when 90 days past "
    "due (except credit cards, which accrue until charged off at 180 days); wholesale loans are placed on "
    "nonaccrual when full payment of principal or interest is not expected.",
    "<b>Allowance for credit losses.</b> The allowance is measured on a collective (pool) basis where loans share "
    "similar risk characteristics, using the CECL model described in Credit Risk Management, and on an "
    "individual basis for collateral-dependent and restructured wholesale loans. The reasonable and supportable "
    "forecast period is two years, after which loss rates revert to historical averages over 12 months.",
    "<b>Fair value.</b> Fair value is the price that would be received to sell an asset or paid to transfer a "
    "liability in an orderly transaction between market participants. The Firm classifies fair value "
    "measurements within a three-level hierarchy based on the observability of inputs. Level 1 and Level 2 "
    "inputs are sourced primarily through the Market Data API.",
)
story.append(h2("Note 5 - Loans"))
rows = [["Loans by segment (in millions)", "Dec 31, 2025", "Nonaccrual", "30+ days past due", "Credit quality indicator"]]
info = {"Credit Card": ("-", "3,197", "FICO >= 660: 84%"), "Residential Mortgage": ("2,140", "1,530", "Current LTV < 80%: 96%"),
        "Auto": ("190", "1,010", "FICO >= 660: 81%"), "Commercial Real Estate": ("1,420", "610", "Investment grade: 62%"),
        "Commercial & Industrial": ("1,260", "540", "Investment grade: 69%"), "Other Consumer & Wholesale": ("140", "210", "Secured: 88%")}
for seg, bal, allow, lob in B.CECL_SEGMENTS:
    a, b_, c_ = info[seg]
    rows.append([seg, m(bal), a, b_, c_])
rows.append(["Total loans", m(B.BALANCE["Loans"][0]), "5,150", "7,097", ""])
story.append(table(rows, [0.28, 0.15, 0.13, 0.17, 0.27], total_rows=(-1,)))
story.append(h2("Note 6 - Allowance for Credit Losses"))
story.append(p("The following table presents the roll-forward of the allowance for loan losses for 2025 by portfolio "
               "segment. The year-end balance is produced by the CECL Lifetime Expected Credit Loss Model (MDL-CR-007) "
               "plus approved qualitative adjustments."))
start = {"Credit Card": 8_040, "Residential Mortgage": 860, "Auto": 670, "Commercial Real Estate": 2_510,
         "Commercial & Industrial": 2_610, "Other Consumer & Wholesale": 490}
assert sum(start.values()) == 15_180
rows = [["2025 (in millions)", "Beginning balance", "Net charge-offs", "Provision", "Ending balance"]]
tp = 0
for seg, bal, allow, lob in B.CECL_SEGMENTS:
    nco = B.NCO_BY_SEGMENT[seg]
    prov = allow - start[seg] + nco
    tp += prov
    rows.append([seg, m(start[seg]), m(-nco), m(prov), m(allow)])
rows.append(["Total", m(15_180), m(-B.KEY_METRICS["Net charge-offs"][0]), m(tp), m(15_920)])
story.append(table(rows, [0.32, 0.17, 0.17, 0.17, 0.17], total_rows=(-1,),
                   note=f"Provision for loan losses of ${tp:,} million; the remaining "
                        f"${I['provision_for_credit_losses'][0]-tp:,} million of the total provision for credit losses "
                        "relates to lending-related commitments and investment securities."))
story.append(h2("Note 9 - Deposits"))
rows = [["Deposits (in millions)", "Dec 31, 2025", "Dec 31, 2024"],
        ["Noninterest-bearing (U.S.)", "272,000", "268,900"], ["Interest-bearing - consumer savings and checking", "402,000", "381,600"],
        ["Interest-bearing - wholesale and time deposits (U.S.)", "236,600", "229,300"],
        ["Non-U.S. offices", "101,800", "98,500"], ["Total deposits", m(B.LIABS["Deposits"][0]), m(B.LIABS["Deposits"][1])]]
story.append(table(rows, [0.6, 0.2, 0.2], total_rows=(-1,)))
story.append(h2("Note 11 - Long-Term Debt"))
rows = [["Long-term debt by maturity (in millions)", "Under 1 year", "1-5 years", "After 5 years", "Total"],
        ["Senior debt - parent", "6,100", "24,800", "27,900", "58,800"],
        ["Subordinated debt", "-", "3,100", "8,800", "11,900"],
        ["Bank-level senior notes and FHLB advances", "4,200", "9,400", "2,400", "16,000"],
        ["Total long-term debt", "10,300", "37,300", "39,100", m(B.LIABS["Long-term debt"][0])]]
story.append(table(rows, [0.4, 0.15, 0.15, 0.15, 0.15], total_rows=(-1,)))
story.append(h2("Note 13 - Fair Value Measurement"))
rows = [["Assets at fair value (in millions)", "Level 1", "Level 2", "Level 3", "Total"],
        ["Trading assets", "61,400", "68,300", "3,200", "132,900"],
        ["Available-for-sale securities", "48,900", "62,800", "900", "112,600"],
        ["Derivative receivables (net)", "1,100", "41,600", "1,700", "44,400"],
        ["Mortgage servicing rights", "-", "-", "6,820", "6,820"]]
story.append(table(rows, [0.4, 0.15, 0.15, 0.15, 0.15]))
story.append(h2("Note 18 - Regulatory Capital"))
story += ps(
    "The Federal Reserve establishes capital requirements for the Firm, including well-capitalized standards. "
    "The Firm's binding ratio is the Standardized CET1 ratio. At December 31, 2025 and 2024, the Firm and its "
    "principal insured bank subsidiary, Meridian Harbor Bank, N.A., were well capitalized and met all capital "
    "requirements to which each was subject. The composition of CET1 capital is disclosed in the Firm's Pillar 3 "
    "Regulatory Capital Disclosures.",
)
story.append(PageBreak())

# ================================================================ glossary & FLS
story.append(h1("Glossary of Terms"))
gl = [("ALM", "Asset-liability management: managing the mismatch between assets and liabilities in rates, liquidity and currency."),
      ("Allowance for credit losses", "Reserve for expected lifetime credit losses on loans and commitments under CECL (ASC 326)."),
      ("API", "Application programming interface; the Firm's Developer Platform exposes 18 production APIs (API-01 to API-18)."),
      ("CCAR", "Comprehensive Capital Analysis and Review; the Federal Reserve's annual stress test and capital plan review."),
      ("CECL", "Current Expected Credit Losses accounting standard requiring lifetime expected loss estimates at origination."),
      ("CET1", "Common Equity Tier 1 capital: common equity less regulatory deductions; the highest-quality regulatory capital."),
      ("EVE", "Economic value of equity: present value of assets less present value of liabilities; used to measure IRRBB."),
      ("G-SIB surcharge", "Additional CET1 buffer applied to global systemically important banks."),
      ("HQLA", "High-quality liquid assets eligible for the liquidity coverage ratio."),
      ("IRRBB", "Interest rate risk in the banking book."),
      ("LCR", "Liquidity coverage ratio: HQLA divided by net cash outflows over a 30-day stress period."),
      ("LGD", "Loss given default: expected loss as a percentage of exposure if a borrower defaults."),
      ("Managed basis", "Non-GAAP presentation adjusting revenue for the tax-equivalent impact of tax-exempt income."),
      ("MRGR", "Model Risk Governance & Review, the independent model validation function."),
      ("NCO", "Net charge-offs: gross charge-offs less recoveries."),
      ("NII", "Net interest income: interest income less interest expense."),
      ("NSFR", "Net stable funding ratio: available stable funding divided by required stable funding."),
      ("PD", "Probability of default over a given horizon."),
      ("ROTCE", "Return on tangible common equity: net income applicable to common divided by average tangible common equity."),
      ("RWA", "Risk-weighted assets: exposures weighted by riskiness under the Standardized or Advanced approaches."),
      ("SCB", "Stress capital buffer: CET1 buffer derived from the peak-to-trough decline in the supervisory stress test plus four quarters of dividends."),
      ("SLR", "Supplementary leverage ratio: Tier 1 capital divided by total leverage exposure."),
      ("VaR", "Value-at-risk: statistical estimate of potential one-day loss in trading positions at a given confidence level.")]
story.append(table([["Term", "Definition"]] + [[a, b_] for a, b_ in gl], [0.22, 0.78]))
story.append(h1("Forward-Looking Statements"))
story += ps(
    "This report contains forward-looking statements within the meaning of the Private Securities Litigation "
    "Reform Act of 1995. These statements are based on the current beliefs and expectations of management and "
    "are subject to significant risks and uncertainties, including: economic and market conditions; changes in "
    "interest rates and deposit behavior; credit performance of consumer and wholesale borrowers; the "
    "effectiveness of the Firm's models, including those used to estimate the allowance for credit losses, "
    "interest rate risk and capital; changes in laws and regulations; cybersecurity and technology failures; "
    "and the other factors described under Risk Factors. The Firm does not undertake to update any "
    "forward-looking statement.",
    f"<i>{B.BANK['disclaimer']}</i>",
)

doc = ReportDoc("../data/reports/MHFC_2025_Annual_Report.pdf", f"{nm} 2025 Annual Report", "2025 Annual Report")
build(doc, story)
print("ok")
