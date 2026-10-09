"""Q2 2026 Earnings Release and Financial Supplement for the fictional Meridian Harbor Financial Corp."""
import json
from reportlab.platypus import Spacer, PageBreak, CondPageBreak
from pdfkit_lib import *
import bankdata as B

O = json.load(open("model_outputs.json"))
Q = B.Q2
QC = B.Q2_CAPITAL
nm = B.BANK["name"]
sh = B.BANK["short"]
HDR3 = ["2Q26", "1Q26", "2Q25", "vs 1Q26", "vs 2Q25"]


def q_row(label, t, dec=0, as_pct=False, money=False):
    a, b_, c = t
    if as_pct:
        return [label, pct(a, 1), pct(b_, 1), pct(c, 1) if c is not None else "-",
                f"{(a - b_) * 10000:+.0f} bps", f"{(a - c) * 10000:+.0f} bps" if c is not None else "-"]
    f = (lambda x: f"${x:.2f}") if money else (lambda x: m(x, dec))
    return [label, f(a), f(b_), f(c), pct(chg(a, b_)), pct(chg(a, c))]


def qtable(rows, bold=(), total=()):
    return table([["(in millions, except per share and ratios)"] + HDR3] + rows,
                 [0.36, 0.128, 0.128, 0.128, 0.128, 0.128], bold_rows=bold, total_rows=total)


story = []
story += cover("Second-Quarter 2026<br/>Earnings Release", "Earnings release and financial supplement<br/>for the "
               "quarter ended June 30, 2026", "Released July 14, 2026",
               ["Investor Relations conference call: 8:30 a.m. ET, July 14, 2026"])
story += toc_page()

# ---------------------------------------------------------------- press release
story.append(h1("Earnings Release"))
eps = B.Q2_EPS
story += ps(
    f"<b>{B.BANK['hq'].split(',')[0].upper()}, July 14, 2026</b> - {nm} today reported net income for the "
    f"second quarter of 2026 of {bn(Q['net_income'][0], 2)}, or ${eps[0]:.2f} per diluted share, compared with "
    f"net income of {bn(Q['net_income'][2], 2)}, or ${eps[2]:.2f} per share, in the second quarter of 2025. "
    f"Reported revenue was {bn(Q['total_net_revenue'][0], 2)}, up {pct(chg(Q['total_net_revenue'][0], Q['total_net_revenue'][2]))} "
    "year-on-year.",
)
story.append(callout("Second-quarter highlights", "<br/>".join([
    f"• Net income {bn(Q['net_income'][0], 2)}; EPS ${eps[0]:.2f}; ROTCE 25%",
    f"• Revenue {bn(Q['total_net_revenue'][0], 2)}, up {pct(chg(Q['total_net_revenue'][0], Q['total_net_revenue'][2]))} YoY; "
    f"NII {bn(Q['net_interest_income'][0], 2)}, up {pct(chg(Q['net_interest_income'][0], Q['net_interest_income'][2]))}",
    f"• Average loans up 6% YoY; average deposits up 4% YoY",
    f"• Credit costs {bn(Q['provision_for_credit_losses'][0], 2)}: net charge-offs {bn(QC['Net charge-offs'][0], 2)}, "
    f"net reserve build ${Q['provision_for_credit_losses'][0]-QC['Net charge-offs'][0]:,} million",
    f"• Standardized CET1 ratio {pct(QC['CET1 ratio (Standardized)'][0])}; returned "
    f"{bn(QC['Common shares repurchased ($mm)'][0] + 1_600, 1)} to shareholders",
])))
story.append(quote(f"\"Our businesses performed well this quarter. Clients are active, credit is behaving as we "
                   f"expected and our balance sheet has never been stronger. We remain alert to a wide range of "
                   f"economic outcomes and continue to manage the company to be ready for all of them.\" - "
                   f"{B.BANK['ceo']}, Chairman and CEO"))
story.append(h2("Firmwide results"))
story += ps(
    f"Net interest income was {bn(Q['net_interest_income'][0], 2)}, up {pct(chg(Q['net_interest_income'][0], Q['net_interest_income'][1]))} "
    "from the prior quarter, reflecting one additional day, Card loan growth and higher deposit balances, partly "
    "offset by lower deposit margins following the 25 basis point policy rate reduction in March. Noninterest "
    f"revenue was {bn(Q['noninterest_revenue'][0], 2)}, down {pct(-chg(Q['noninterest_revenue'][0], Q['noninterest_revenue'][1]))} "
    "sequentially from a seasonally strong first quarter in Markets, and up "
    f"{pct(chg(Q['noninterest_revenue'][0], Q['noninterest_revenue'][2]))} year-on-year on higher investment banking and "
    "asset management fees.",
    f"Noninterest expense was {bn(Q['noninterest_expense'][0], 2)}, up {pct(chg(Q['noninterest_expense'][0], Q['noninterest_expense'][2]))} "
    "year-on-year, driven by compensation, including growth in front-office and technology headcount, and "
    "continued technology investment, partly offset by lower legal expense. The overhead ratio was "
    f"{pct(Q['noninterest_expense'][0]/Q['total_net_revenue'][0])}.",
    f"The provision for credit losses was {bn(Q['provision_for_credit_losses'][0], 2)}, reflecting net charge-offs of "
    f"{bn(QC['Net charge-offs'][0], 2)} and a net reserve build of ${Q['provision_for_credit_losses'][0]-QC['Net charge-offs'][0]:,} "
    "million, primarily in Card on loan growth. The allowance for loan losses was "
    f"{bn(QC['Allowance for loan losses'][0], 2)}, or {pct(QC['Allowance for loan losses'][0]/QC['Loans (period end)'][0], 2)} "
    "of period-end loans.",
)
story.append(h2("Outlook"))
story += ps(
    f"Management now expects full-year 2026 net interest income of approximately $50.5 billion, up from the "
    f"approximately {bn(O['nii']['Base']['nii'], 1)} expectation provided in January, reflecting stronger deposit "
    "balances. Adjusted noninterest expense is expected to be approximately $49.5 billion, and the Card net "
    "charge-off rate is expected to be approximately 3.6%. The outlook assumes the market-implied forward rate "
    "curve as of June 30, 2026.",
)
story.append(PageBreak())

# ---------------------------------------------------------------- segment summary in release
story.append(h2("Segment results"))
rows = []
for sname in B.Q2_SEG_REV:
    rows.append(q_row(sname + " - net revenue", B.Q2_SEG_REV[sname]))
    rows.append(q_row(sname + " - net income", B.Q2_SEG_NI[sname]))
rows.append(q_row("Firmwide net income", Q["net_income"]))
story.append(qtable(rows, bold=tuple(range(2, 10, 2)), total=(-1,)))
story += ps(
    f"<b>Consumer &amp; Community Banking</b> reported net income of {bn(B.Q2_SEG_NI['Consumer & Community Banking'][0], 2)}, "
    "up 7% year-on-year, on revenue growth of 4%. Card loans grew 9% and card spend grew 7%. Deposits grew 2% "
    "sequentially. The Card net charge-off rate was 3.58%, in line with guidance.",
    f"<b>Commercial &amp; Investment Bank</b> reported net income of {bn(B.Q2_SEG_NI['Commercial & Investment Bank'][0], 2)}. "
    "Investment banking fees rose 14% year-on-year, led by equity and debt underwriting. Markets revenue was "
    "$4.6 billion, up 4% year-on-year. Payments revenue grew 8%, with real-time payment volumes up 64%.",
    f"<b>Asset &amp; Wealth Management</b> reported net income of {bn(B.Q2_SEG_NI['Asset & Wealth Management'][0], 2)}, "
    "up 10%, with record client assets of $3.31 trillion and long-term net inflows of $41 billion.",
    f"<b>Corporate</b> reported a net loss of ${-B.Q2_SEG_NI['Corporate'][0]:,} million.",
)
story.append(h2("Capital and liquidity"))
story += ps(
    f"The Standardized CET1 ratio was {pct(QC['CET1 ratio (Standardized)'][0], 1)}, flat versus the prior quarter, as "
    f"net income generation was offset by capital distributions and RWA growth of {pct(chg(*QC['Standardized RWA']))}. "
    f"The Firm repurchased ${QC['Common shares repurchased ($mm)'][0]:,} million of common stock and paid common "
    f"dividends of ${QC['Common dividend per share ($)'][0]:.2f} per share. The supplementary leverage ratio was "
    f"{pct(QC['Supplementary leverage ratio'][0])} and the average LCR was {QC['LCR (average)'][0]*100:.0f}%.",
    "The Firm received its preliminary 2026 stress capital buffer from the Federal Reserve on June 27, 2026. Based "
    "on the preliminary results, the Firm expects its SCB to remain at 3.2% from October 1, 2026.",
)
story.append(PageBreak())

# ---------------------------------------------------------------- supplement
story.append(h1("Financial Supplement"))
story.append(h2("Consolidated Financial Highlights"))
rows = [q_row("Total net revenue", Q["total_net_revenue"]), q_row("Net interest income", Q["net_interest_income"]),
        q_row("Noninterest revenue", Q["noninterest_revenue"]), q_row("Noninterest expense", Q["noninterest_expense"]),
        q_row("Provision for credit losses", Q["provision_for_credit_losses"]), q_row("Net income", Q["net_income"]),
        q_row("Diluted EPS", B.Q2_EPS, money=True),
        q_row("Average diluted shares (mm)", Q["diluted_shares_mm"]),
        q_row("Overhead ratio", tuple(Q['noninterest_expense'][k] / Q['total_net_revenue'][k] for k in range(3)), as_pct=True),
        q_row("Effective tax rate", tuple(Q['income_tax_expense'][k] / Q['income_before_tax'][k] for k in range(3)), as_pct=True)]
story.append(qtable(rows, bold=(1, 6)))
rows = [["Selected balance sheet and capital data (period end)", "2Q26", "1Q26", "Change"]]
for k in ["Total assets (period end)", "Loans (period end)", "Deposits (period end)", "Allowance for loan losses",
          "CET1 capital", "Standardized RWA"]:
    a, b_ = QC[k]
    rows.append([k, m(a), m(b_), pct(chg(a, b_))])
for k in ["CET1 ratio (Standardized)", "Supplementary leverage ratio"]:
    a, b_ = QC[k]
    rows.append([k, pct(a), pct(b_), f"{(a-b_)*10000:+.0f} bps"])
rows.append(["LCR (average)", f"{QC['LCR (average)'][0]*100:.0f}%", f"{QC['LCR (average)'][1]*100:.0f}%",
             f"{(QC['LCR (average)'][0]-QC['LCR (average)'][1])*100:+.0f} pts"])
story.append(table(rows, [0.5, 0.17, 0.17, 0.16]))
labels = ["2Q25", "3Q25", "4Q25", "1Q26", "2Q26"]
story.append(bar_chart("q2_rev_trend", labels,
                       {"Net interest income": [12_020, 12_200, 12_390, 12_310, 12_560],
                        "Noninterest revenue": [9_310, 9_120, 9_650, 10_240, 9_920]},
                       "Quarterly revenue ($mm)", stacked=True, ratio=0.32))
story.append(PageBreak())

story.append(h2("Consolidated Statements of Income"))
nint = (19_840, 19_610, 19_420)
rows = [q_row("Investment banking fees", (1_820, 1_760, 1_600)), q_row("Principal transactions", (3_180, 3_610, 3_070)),
        q_row("Lending- and deposit-related fees", (1_110, 1_090, 1_060)), q_row("Asset management fees", (2_480, 2_420, 2_250)),
        q_row("Commissions and other fees", (790, 770, 740)), q_row("Investment securities gains (losses)", (-40, -20, -90)),
        q_row("Mortgage fees and related income", (250, 240, 260)), q_row("Card income", (330, 370, 420)),
        q_row("Total noninterest revenue", Q["noninterest_revenue"]),
        q_row("Interest income", nint),
        q_row("Interest expense", tuple(nint[k] - Q["net_interest_income"][k] for k in range(3))),
        q_row("Net interest income", Q["net_interest_income"]),
        q_row("Total net revenue", Q["total_net_revenue"]),
        q_row("Provision for credit losses", Q["provision_for_credit_losses"]),
        q_row("Compensation expense", (6_540, 6_790, 6_330)), q_row("Occupancy expense", (820, 810, 800)),
        q_row("Technology, communications and equipment", (2_090, 2_040, 1_950)),
        q_row("Professional and outside services", (1_120, 1_100, 1_080)), q_row("Marketing", (610, 590, 580)),
        q_row("Other expense", (960, 1_060, 1_010)),
        q_row("Total noninterest expense", Q["noninterest_expense"]),
        q_row("Income before income tax expense", Q["income_before_tax"]),
        q_row("Income tax expense", Q["income_tax_expense"]), q_row("Net income", Q["net_income"]),
        q_row("Preferred dividends", Q["preferred_dividends"]),
        q_row("Diluted EPS", B.Q2_EPS, money=True)]
assert sum((1_820, 3_180, 1_110, 2_480, 790, -40, 250, 330)) == Q["noninterest_revenue"][0]
assert sum((1_760, 3_610, 1_090, 2_420, 770, -20, 240, 370)) == Q["noninterest_revenue"][1]
assert sum((1_600, 3_070, 1_060, 2_250, 740, -90, 260, 420)) == Q["noninterest_revenue"][2]
assert sum((6_540, 820, 2_090, 1_120, 610, 960)) == Q["noninterest_expense"][0]
assert sum((6_790, 810, 2_040, 1_100, 590, 1_060)) == Q["noninterest_expense"][1]
assert sum((6_330, 800, 1_950, 1_080, 580, 1_010)) == Q["noninterest_expense"][2]
story.append(qtable(rows, bold=(9, 12, 13, 21, 22, 24)))
story.append(PageBreak())

# ---------------------------------------------------------------- segment pages
SEGTXT = {
    "Consumer & Community Banking": (
        ["Banking &amp; Wealth Management revenue of $5.2 billion, down 2% YoY on deposit margin compression, "
         "partly offset by higher deposit balances and client investment assets.",
         "Home Lending revenue of $0.9 billion, up 5% YoY on higher production margins; originations of $11.8 billion.",
         "Card Services &amp; Auto revenue of $4.4 billion, up 11% YoY on higher Card net interest income from loan growth.",
         "Card net charge-off rate of 3.58%, compared with 3.39% in 2Q25; 30+ day delinquency rate of 2.24%.",
         "Active mobile customers of 63.0 million, up 7% YoY; 81% of new deposit accounts opened digitally."],
        [("Average loans", (421_900, 417_100, 409_800)), ("Average deposits", (628_400, 621_300, 607_900)),
         ("Card loans, period end", (145_600, 140_200, 133_700)), ("Debit and credit card sales volume", (412_300, 386_900, 385_100))]),
    "Commercial & Investment Bank": (
        ["Investment banking fees of $1.82 billion, up 14% YoY, with gains in equity and debt underwriting; "
         "wallet share of 8.1%.",
         "Markets revenue of $4.6 billion, up 4% YoY: Fixed Income Markets $2.9 billion, Equity Markets $1.7 billion.",
         "Payments revenue of $2.5 billion, up 8% YoY; real-time payments volume up 64% following the expansion of "
         "the Real-Time Payments API (API-04) to middle-market clients.",
         "Lending revenue of $0.9 billion; average loans of $279 billion, up 5% YoY.",
         "Provision for credit losses of $260 million, including office CRE net charge-offs of $90 million."],
        [("Average loans", (279_200, 274_600, 265_300)), ("Average deposits", (331_500, 326_800, 312_400)),
         ("Investment banking fees", (1_820, 1_760, 1_600)), ("Markets revenue", (4_610, 5_080, 4_430))]),
    "Asset & Wealth Management": (
        ["Asset management fees of $2.48 billion, up 10% YoY on higher average market levels and net inflows.",
         "Long-term net inflows of $41 billion and liquidity net inflows of $18 billion.",
         "Assets under management of $2.27 trillion and client assets of $3.31 trillion, both records.",
         "Pre-tax margin of 36%; ROE of 34%."],
        [("Assets under management ($bn)", (2_270, 2_210, 1_990)), ("Client assets ($bn)", (3_310, 3_240, 2_960)),
         ("Average loans", (63_800, 62_900, 59_700)), ("Average deposits", (238_100, 234_400, 226_900))]),
    "Corporate": (
        ["Net revenue of $(80) million, including investment securities losses of $40 million.",
         "Net interest income in Treasury/CIO benefited from reinvestment of maturing securities at higher yields.",
         "Expense of $480 million, primarily centrally managed technology and legal costs not allocated to segments."],
        []),
}

SEGNARR = {
    "Consumer & Community Banking": (
        "<b>Management commentary.</b> Consumer spending remained resilient across income bands, with "
        "discretionary categories such as travel and dining growing faster than non-discretionary spend. Deposit "
        "balances grew for the third consecutive quarter as customers shifted cash back from money market funds "
        "into higher-yielding savings and CD products, which carries a lower margin than checking balances.",
        "Card loan growth reflects strong new account origination in the second half of 2025 maturing into "
        "revolving balances. These vintages are performing in line with underwriting expectations. Credit "
        "decisions for new card accounts are made through the Credit Decisioning API (API-09), and the expected "
        "lifetime losses on the resulting balances are reserved through the CECL model as the loans are booked.",
        "Branch expansion continued, with 31 new branches opened in the quarter in expansion markets in the "
        "Southeast and Mountain West. The new-branch cohort from 2023 has reached break-even.",
    ),
    "Commercial & Investment Bank": (
        "<b>Management commentary.</b> Client engagement was strong across regions. The investment banking "
        "pipeline is up year-on-year, with particularly strong activity in technology and healthcare M&amp;A. "
        "Sponsor activity improved as financing markets remained open. In Markets, Fixed Income benefited from "
        "client activity in rates and securitized products, while Equity Markets were lower than a record first "
        "quarter in derivatives.",
        "Payments remains a strategic priority. The Real-Time Payments API (API-04) and the Payments Initiation API "
        "(API-03) are now integrated with the top five ERP platforms used by middle-market clients, and 2,400 "
        "clients went live on API-based payments in the quarter. Each payment is screened by the Fraud Risk "
        "Signals API (API-08) before release.",
        "Office CRE remains the area of greatest credit attention. Criticized office loans were $3.1 billion, down "
        "from $3.6 billion at year end, and the office portfolio carries an allowance coverage of 9.8%.",
    ),
    "Asset & Wealth Management": (
        "<b>Management commentary.</b> Record client assets reflect both market appreciation and continued net "
        "new money, particularly in Global Private Bank and in active ETFs, where the Firm ranks among the top "
        "five issuers by net flows. 84% of ten-year long-term mutual fund AUM performed above the peer median.",
        "Advisor headcount increased 5% year-on-year. Lending to private bank clients, primarily securities-based "
        "lending and mortgages, grew 7% with negligible credit losses.",
        "Alternatives fundraising remained strong, with $9 billion raised across private credit, infrastructure "
        "and real estate strategies in the quarter.",
    ),
    "Corporate": (
        "<b>Management commentary.</b> Treasury/CIO continued to reinvest maturing securities into agency "
        "mortgage-backed securities and U.S. Treasuries at yields above the run-off yield, supporting Firmwide "
        "NII. The investment securities portfolio duration was approximately 3.6 years at quarter end.",
        "Treasury/CIO maintains the Firm's interest rate risk positioning within Board-approved limits, measured "
        "using the Net Interest Income Sensitivity Model (MDL-ALM-014), and manages capital distributions within "
        "the plan produced by the Capital Planning &amp; Stress Projection Model (MDL-CAP-003).",
    ),
}
for sname in B.Q2_SEG_REV:
    story.append(h2(f"Segment detail - {sname}"))
    bullets_, extra = SEGTXT[sname]
    rows = [q_row("Net revenue", B.Q2_SEG_REV[sname]), q_row("Net income", B.Q2_SEG_NI[sname])]
    rows += [q_row(k, v) for k, v in extra]
    story.append(qtable(rows, bold=(2,)))
    story += bullets(bullets_)
    story.append(Spacer(1, 6))
    story.append(bar_chart("q2_seg_" + B.SEGMENTS[sname]["abbr"], ["2Q25", "1Q26", "2Q26"],
                           {"Net revenue": [B.Q2_SEG_REV[sname][2], B.Q2_SEG_REV[sname][1], B.Q2_SEG_REV[sname][0]],
                            "Net income": [B.Q2_SEG_NI[sname][2], B.Q2_SEG_NI[sname][1], B.Q2_SEG_NI[sname][0]]},
                           f"{sname}: revenue and net income ($mm)", ratio=0.3))
    story += ps(*SEGNARR[sname])
    story.append(PageBreak())

# ---------------------------------------------------------------- credit
story.append(h2("Credit Trends"))
story += ps(
    "Credit performance remained consistent with management's expectations. Consumer credit continued to "
    "normalize gradually, led by Card, while wholesale credit was stable, with losses concentrated in office CRE. "
    "Nonperforming assets were $5.4 billion, or 0.71% of loans.",
)
ncoq = {"Credit Card": (1_270, 1_200, 1_110), "Residential Mortgage": (10, 10, 10), "Auto": (100, 110, 100),
        "Commercial Real Estate": (90, 110, 80), "Commercial & Industrial": (160, 140, 130),
        "Other Consumer & Wholesale": (20, 20, 20)}
assert sum(v[0] for v in ncoq.values()) == QC["Net charge-offs"][0]
assert sum(v[1] for v in ncoq.values()) == QC["Net charge-offs"][1]
rows = [q_row(k, v) for k, v in ncoq.items()]
rows.append(q_row("Total net charge-offs", (QC["Net charge-offs"][0], QC["Net charge-offs"][1], 1_520)))
story.append(table([["Net charge-offs by portfolio (in millions)"] + HDR3] + rows,
                   [0.36, 0.128, 0.128, 0.128, 0.128, 0.128], total_rows=(-1,)))
rows = [["Allowance for loan losses roll-forward (in millions)", "2Q26", "1Q26"],
        ["Beginning balance", m(16_110), m(15_920)],
        ["Net charge-offs", m(-QC["Net charge-offs"][0]), m(-QC["Net charge-offs"][1])],
        ["Provision for loan losses", m(1_920), m(1_780)],
        ["Ending balance", m(QC["Allowance for loan losses"][0]), m(QC["Allowance for loan losses"][1])],
        ["Allowance to period-end loans", pct(QC["Allowance for loan losses"][0] / QC["Loans (period end)"][0], 2),
         pct(QC["Allowance for loan losses"][1] / QC["Loans (period end)"][1], 2)]]
story.append(table(rows, [0.6, 0.2, 0.2], total_rows=(4,)))
story += ps(
    "The allowance is estimated using the CECL Lifetime Expected Credit Loss Model (MDL-CR-007). Scenario weights "
    "were unchanged from year end (Upside 20%, Baseline 50%, Downside 30%). The baseline scenario assumes U.S. "
    "unemployment peaking at 4.5% in the first quarter of 2027, slightly higher than the 4.4% assumed at year end. "
    "The year-end allowance by segment and the model's sensitivity to scenario weights are disclosed in Note 6 of "
    "the 2025 Annual Report.",
)
story.append(line_chart("q2_card_nco", labels, {"Card NCO rate": [0.0339, 0.0344, 0.0352, 0.0355, 0.0358],
                                                "Card 30+ delinquency": [0.0215, 0.0226, 0.0231, 0.0229, 0.0224]},
                        "Card credit metrics", pct_axis=True, ratio=0.3))
story.append(PageBreak())

# ---------------------------------------------------------------- capital
story.append(h2("Capital and Capital Planning"))
c = O["capital"]
story += ps(
    f"CET1 capital was {bn(QC['CET1 capital'][0])} and Standardized RWA was {bn(QC['Standardized RWA'][0])}, for a "
    f"CET1 ratio of {pct(c['Starting CET1 ratio (Q2 2026)'], 2)}. The Firm's capital plan, produced with the "
    "Capital Planning &amp; Stress Projection Model (MDL-CAP-003) using June 30, 2026 starting capital, projects:",
)
story += bullets([
    f"Baseline: CET1 ratio rising to {pct(c['Ending CET1 ratio - baseline (Q3 2028)'], 2)} by 3Q28 after "
    f"{bn(c['Cumulative buybacks over horizon ($mm)'])} of share repurchases ($3.0 billion per quarter) and "
    "dividends of $1.15 per share per quarter.",
    f"Severely adverse: minimum CET1 ratio of {pct(c['Minimum CET1 ratio - severely adverse'], 2)}, a peak-to-trough "
    f"decline of {pct(c['Peak-to-trough CET1 decline (stress)'], 2)}, with buybacks suspended.",
    f"Indicative SCB of {pct(c['Indicative stress capital buffer (SCB)'], 2)} (peak-to-trough decline plus "
    f"{pct(c['Four quarters of planned dividends / starting RWA'], 2)} of dividends), consistent with the "
    "preliminary supervisory SCB of 3.2%.",
    f"Excess CET1 above the 13.0% management target of approximately {bn(c['Excess CET1 vs target at Q3 2028 ($mm)'])} "
    "by 3Q28, providing capacity for organic growth, additional distributions or acquisitions.",
])
q = ["2Q26", "3Q26", "4Q26", "1Q27", "2Q27", "3Q27", "4Q27", "1Q28", "2Q28", "3Q28"]
req = B.CAP_REQ
story.append(line_chart("q2_cet1_path", q, {"Baseline": O["Baseline_Projection_cet1"],
                                           "Severely adverse": O["Stress_Projection_cet1"]},
                        "Projected Standardized CET1 ratio", pct_axis=True, ratio=0.36,
                        hlines=[(req["management_target"], "Mgmt target 13.0%", "#B08D57"),
                                (req["minimum"] + req["stress_capital_buffer"] + req["gsib_surcharge"],
                                 "Requirement 10.2%", "#8A1C1C")]))
story.append(caption("Source: Capital_Planning_Model.xlsx (MDL-CAP-003), sheets Baseline_Projection and "
                     "Stress_Projection."))
rows = [["CET1 requirement stack", "2Q26"], ["Regulatory minimum", pct(req["minimum"])],
        ["Stress capital buffer", pct(req["stress_capital_buffer"])], ["G-SIB surcharge", pct(req["gsib_surcharge"])],
        ["Countercyclical buffer", pct(req["ccyb"])],
        ["Total CET1 requirement", pct(req["minimum"] + req["stress_capital_buffer"] + req["gsib_surcharge"])],
        ["Management target", pct(req["management_target"])]]
story.append(table(rows, [0.7, 0.3], total_rows=(5,)))
story.append(PageBreak())


# ---------------------------------------------------------------- average balance sheet
story.append(h2("Average Balance Sheet, Yields and Rates"))
story.append(p("Quarterly averages; yields and rates are annualized and presented on a taxable-equivalent basis."))
abs_rows = [["2Q26 (in millions)", "Average balance", "Interest", "Yield / rate"],
            ["Deposits with banks and fed funds sold", "251,300", "2,280", "3.64%"],
            ["Securities purchased under resale agreements", "131,800", "1,190", "3.62%"],
            ["Investment securities", "176,400", "1,770", "4.02%"],
            ["Trading assets - debt instruments", "101,900", "1,050", "4.13%"],
            ["Loans", "756,900", "13,290", "7.04%"],
            ["All other interest-earning assets", "33,700", "260", "3.10%"],
            ["Total interest-earning assets", "1,452,000", "19,840", "5.48%"],
            ["Interest-bearing deposits", "758,200", "4,690", "2.48%"],
            ["Repurchase agreements and short-term borrowings", "82,600", "790", "3.84%"],
            ["Long-term debt", "88,100", "1,060", "4.83%"],
            ["Other interest-bearing liabilities", "62,300", "740", "4.76%"],
            ["Total interest-bearing liabilities", "991,200", "7,280", "2.95%"],
            ["Net interest income / net interest yield", "", m(Q["net_interest_income"][0]), "3.47%"]]
story.append(table(abs_rows, [0.46, 0.18, 0.18, 0.18], bold_rows=(7, 12, 13)))
story += ps(
    "Loan yields declined 9 basis points sequentially, reflecting the March policy rate reduction on floating-"
    "rate C&amp;I and CRE loans, partly offset by mix shift toward Card. The cost of interest-bearing deposits fell "
    "7 basis points; the cumulative interest-bearing deposit beta since the start of the easing cycle is 49%, "
    "slightly above the 45% consumer and below the 75% wholesale betas assumed in the Net Interest Income "
    "Sensitivity Model, consistent with the product mix.",
)
story.append(h2("Loans and Deposits Detail"))
rows = [["Period-end balances (in millions)", "2Q26", "1Q26", "2Q25"],
        ["Credit card", "145,600", "140,200", "133,700"], ["Residential mortgage", "220,900", "219,800", "216,400"],
        ["Auto", "66,100", "65,400", "63,800"], ["Commercial real estate", "100,400", "99,300", "96,900"],
        ["Commercial & industrial", "177,600", "176,000", "170,100"], ["Other consumer & wholesale", "50,800", "51,200", "48,900"],
        ["Total loans", m(QC["Loans (period end)"][0]), m(QC["Loans (period end)"][1]), "729,800"],
        ["Consumer deposits", "668,900", "663,700", "652,300"], ["Wholesale deposits", "362,700", "361,100", "347,800"],
        ["Total deposits", m(QC["Deposits (period end)"][0]), m(QC["Deposits (period end)"][1]), "1,000,100"]]
assert 145_600+220_900+66_100+100_400+177_600+50_800 == QC["Loans (period end)"][0]
assert 140_200+219_800+65_400+99_300+176_000+51_200 == QC["Loans (period end)"][1]
story.append(table(rows, [0.46, 0.18, 0.18, 0.18], bold_rows=(7, 10)))
story.append(PageBreak())

story.append(h2("Consumer Credit Quality"))
rows = [["Delinquency and loss metrics", "2Q26", "1Q26", "2Q25"],
        ["Card 30+ day delinquency rate", "2.24%", "2.29%", "2.15%"], ["Card 90+ day delinquency rate", "1.14%", "1.19%", "1.09%"],
        ["Card net charge-off rate", "3.58%", "3.55%", "3.39%"],
        ["Residential mortgage 30+ day delinquency rate", "0.69%", "0.71%", "0.73%"],
        ["Residential mortgage weighted-average current LTV", "50%", "51%", "52%"],
        ["Auto 30+ day delinquency rate", "1.52%", "1.58%", "1.49%"], ["Auto net charge-off rate", "0.61%", "0.68%", "0.60%"],
        ["Consumer nonaccrual loans ($mm)", "2,410", "2,380", "2,290"]]
story.append(table(rows, [0.52, 0.16, 0.16, 0.16]))
story += ps(
    "Card delinquencies improved seasonally in the second quarter. Early-stage roll rates for the 2025 vintages "
    "are tracking the loss curves used in underwriting. Pool-level PD and LGD estimates delivered by the Credit "
    "Risk Scoring API (API-10) were refreshed in June and are reflected in the quarter-end allowance.",
)
story.append(h2("Wholesale Credit Exposure by Industry"))
rows = [["Industry (in billions)", "Credit exposure", "Investment grade %", "Criticized", "NCOs 2Q26 ($mm)"],
        ["Real estate - multifamily", "$84.1", "71%", "$1.9", "5"], ["Real estate - office", "$15.2", "38%", "$3.1", "90"],
        ["Real estate - other", "$37.8", "58%", "$1.2", "0"], ["Technology, media & telecom", "$131.6", "73%", "$2.4", "40"],
        ["Consumer & retail", "$119.0", "61%", "$3.0", "55"], ["Industrials", "$104.3", "66%", "$1.7", "20"],
        ["Healthcare", "$82.5", "72%", "$1.1", "10"], ["Banks & finance companies", "$96.2", "86%", "$0.4", "0"],
        ["Oil & gas and utilities", "$71.8", "68%", "$0.8", "5"], ["Asset managers", "$88.4", "84%", "$0.2", "0"],
        ["All other", "$383.1", "79%", "$4.6", "25"], ["Total wholesale", "$1,214.0", "74%", "$20.4", "250"]]
story.append(table(rows, [0.36, 0.16, 0.16, 0.16, 0.16], total_rows=(-1,)))
story.append(PageBreak())

story.append(h2("Liquidity Coverage Ratio Detail"))
rows = [["Average, 2Q26 (in millions)", "Unweighted", "Weighted"],
        ["High-quality liquid assets (HQLA)", "", "292,300"], ["  Level 1 (cash, central bank reserves, Treasuries)", "", "221,900"],
        ["  Level 2A and 2B", "", "70,400"], ["Retail and small business deposit outflows", "668,900", "41,800"],
        ["Unsecured wholesale funding outflows", "421,300", "171,400"], ["Secured funding and derivative outflows", "", "38,600"],
        ["Commitment and other outflows", "", "131,900"], ["Total cash outflows", "", "383,700"],
        ["Total cash inflows", "", "(129,500)"], ["Net cash outflows", "", "254,200"], ["Liquidity coverage ratio", "", "115%"]]
story.append(table(rows, [0.6, 0.2, 0.2], bold_rows=(1, 8, 10, 11)))
story += ps(
    "HQLA and cash flow projections are compiled daily from the Treasury Liquidity Positions API (API-15). The "
    "Firm also maintains significant additional liquidity in the form of unencumbered securities and borrowing "
    "capacity at the Federal Home Loan Banks and the Federal Reserve discount window, totalling approximately "
    "$560 billion of total liquidity resources at quarter end.",
)

# ---------------------------------------------------------------- NII
story.append(h2("Net Interest Income Outlook and Rate Sensitivity"))
n = O["nii"]
story += ps(
    "Net interest income sensitivity is measured with the Net Interest Income Sensitivity Model (MDL-ALM-014), "
    "which applies instantaneous parallel rate shocks to a static balance sheet. The Firm remains modestly "
    "asset-sensitive. The table below reproduces the year-end 2025 sensitivity disclosed in the Annual Report; "
    "the June 30, 2026 sensitivity was directionally similar, with a +100 bp shock increasing 12-month NII by "
    "approximately $1.4 billion.",
)
rows = [["12-month NII sensitivity (Dec 31, 2025, in millions)", "Change in NII", "% of base NII"]]
for k in ["Down 200", "Down 100", "Up 100", "Up 200"]:
    rows.append([k + " bps parallel shock", m(n[k]["delta"]), pct(n[k]["pct"])])
story.append(table(rows, [0.6, 0.2, 0.2]))
story += ps(
    "<b>Drivers of the 2026 NII outlook.</b> Relative to 2025, NII is expected to benefit from Card loan growth "
    "(approximately +$1.1 billion), reinvestment of maturing securities at higher yields (+$0.6 billion) and "
    "deposit growth (+$0.5 billion), partly offset by the effect of lower policy rates on deposit margins "
    "(-$1.0 billion) and continued migration to higher-yielding deposit products (-$0.4 billion). Deposit betas "
    "used in the model - 0.45 for consumer interest-bearing and 0.75 for wholesale interest-bearing deposits - "
    "were re-calibrated in the first quarter and remained unchanged.",
)
story.append(bar_chart("q2_nii_bridge", ["2025 actual", "Card growth", "Reinvestment", "Deposit growth",
                                         "Deposit margin", "Mix shift", "2026 outlook"],
                       {"$mm": [48_620, 1_100, 600, 500, -1_000, -400, 49_420 + 1_080]},
                       "Indicative NII bridge, 2025 to 2026 ($mm)", ratio=0.32))
story.append(caption("Bars show the 2025 starting point, individual drivers and the updated outlook of ~$50.5 "
                     "billion (includes ~$1.1 billion of other balance sheet effects not shown separately)."))
story.append(PageBreak())

# ---------------------------------------------------------------- tech update
story.append(h2("Technology and Digital Update"))
story += ps(
    "The Firm continues to modernize its technology estate and open its platform to clients. During the quarter, "
    "the Developer Platform processed an average of 4.4 billion API calls per month, up 21% year-on-year, with "
    "99.98% availability. Highlights by API family:",
)
rows = [["API", "Monthly calls 2Q26 (mm)", "YoY growth", "Availability", "Key consumers"],
        ["API-01 Accounts API", "1,140", "18%", "99.99%", "Mobile app, aggregators"],
        ["API-02 Transactions API", "1,320", "22%", "99.98%", "Mobile app, aggregators, Fraud"],
        ["API-03 Payments Initiation API", "310", "17%", "99.98%", "Corporate clients, ERP connectors"],
        ["API-04 Real-Time Payments API", "205", "64%", "99.99%", "Corporate & small business clients"],
        ["API-05 Wire Transfer API", "41", "9%", "99.99%", "CIB clients"],
        ["API-06 Card Management API", "260", "15%", "99.97%", "Mobile app, fintech partners"],
        ["API-08 Fraud Risk Signals API", "690", "24%", "99.99%", "Authorizations, RTP, wires"],
        ["API-10 Credit Risk Scoring API", "12", "6%", "99.95%", "CECL model, capital, monitoring"],
        ["API-12 Market Data API", "310", "11%", "99.99%", "Trading, NII model, fair value"],
        ["API-16 Regulatory Reporting API", "0.4", "3%", "99.90%", "Capital model, FR Y-9C, Pillar 3"]]
story.append(table(rows, [0.3, 0.16, 0.1, 0.12, 0.32]))
story += ps(
    "In May the Firm released version 3.2 of the Payments Initiation API, adding ISO 20022 structured remittance "
    "data, and launched a sandbox environment for the Credit Decisioning API for point-of-sale lending partners. "
    "The Firm also completed migration of the Macroeconomic Scenario API to the strategic data platform, reducing "
    "scenario-load time for the CECL and capital planning models from six hours to under forty minutes.",
)
story.append(PageBreak())
story.append(h2("Earnings Call Highlights - Analyst Q&amp;A"))
story.append(p("Summary of selected questions and management responses from the July 14, 2026 conference call. "
               "Responses are paraphrased for brevity."))
QA = [
    ("Deposit trends", "Can you talk about deposit pricing and how much further deposit margins can compress if the Fed cuts twice more?",
     B.BANK["cfo"], "We have assumed two more 25 basis point cuts in our outlook. Our models assume betas of about 45% on "
     "consumer interest-bearing and 75% on wholesale interest-bearing balances on the way down, and so far realized "
     "betas are tracking those assumptions. The bigger swing factor is mix: if customers keep moving from checking to "
     "savings and CDs, that costs us more than the rate cuts themselves."),
    ("NII sensitivity", "You remain asset-sensitive. Why not add more duration to protect NII in a down-rate scenario?",
     B.BANK["treasurer"], "We have been adding duration, which is why we took securities losses last year. A 200 basis "
     "point decline would reduce NII by roughly 6% on a static basis, which is inside our 7% Board limit. We would "
     "rather keep flexibility than lock in today's yields, and our dynamic simulations, which include management "
     "actions, show a smaller impact."),
    ("Card credit", "Card charge-offs are at 3.58%. Are you comfortable with the reserve, and what would change it?",
     B.BANK["cro"], "Yes. We hold a Card allowance of roughly 6% of loans, which covers almost two years of current "
     "charge-offs. The allowance is driven mainly by loan growth and by our scenario weights. If we moved entirely to "
     "the downside scenario, the Firmwide allowance would rise by over $4 billion, so the weighting matters more than "
     "small changes in the baseline."),
    ("Capital deployment", "You have over $20 billion of excess capital above your target by 2028. Why not buy back more?",
     B.BANK["cfo"], "Our capital model shows the excess building, but we are deliberately cautious. There is still "
     "uncertainty about the final capital rules, and we would rather deploy capital into client growth. We will "
     "revisit the buyback pace after the final SCB is confirmed in August."),
    ("Office CRE", "How much more pain is left in office real estate?",
     B.BANK["cro"], "Criticized office loans are down for the second quarter in a row, and our allowance coverage on "
     "office is close to 10%. We expect losses to remain elevated but manageable; office is about 2% of total loans."),
    ("Technology and APIs", "What is the payoff from the API platform beyond client products?",
     B.BANK["cto"], "The same governed APIs we sell to clients feed our risk models. For example, moving the "
     "Macroeconomic Scenario API to our strategic platform cut the scenario load for the CECL and capital models from "
     "six hours to forty minutes, which lets us run more scenarios and close the quarter faster with better controls."),
]
for topic, q, who, a in QA:
    story.append(h3(topic))
    story.append(p(f"<b>Analyst:</b> {q}"))
    story.append(p(f"<b>{who}:</b> {a}"))
story.append(PageBreak())
story.append(h2("Non-GAAP Financial Measures"))
story += ps(
    "In addition to U.S. GAAP results, management reviews results on a managed basis and uses certain non-GAAP "
    "measures, including ROTCE, tangible book value per share and adjusted expense. These measures are not a "
    "substitute for GAAP measures and may not be comparable to similarly titled measures used by other companies.",
)
rows = [["Reconciliation (in millions)", "2Q26", "1Q26", "2Q25"],
        ["Total net revenue (reported)", m(Q["total_net_revenue"][0]), m(Q["total_net_revenue"][1]), m(Q["total_net_revenue"][2])],
        ["Fully taxable-equivalent adjustment", "130", "130", "140"],
        ["Total net revenue (managed)", m(Q["total_net_revenue"][0] + 130), m(Q["total_net_revenue"][1] + 130), m(Q["total_net_revenue"][2] + 140)],
        ["Common stockholders' equity (average)", "119,300", "117,900", "111,600"],
        ["Less: goodwill and identifiable intangibles, net of DTL", "(16,300)", "(16,330)", "(16,410)"],
        ["Tangible common equity (average)", "103,000", "101,570", "95,190"],
        ["Net income applicable to common stockholders", m(Q["net_income"][0] - Q["preferred_dividends"][0]),
         m(Q["net_income"][1] - Q["preferred_dividends"][1]), m(Q["net_income"][2] - Q["preferred_dividends"][2])],
        ["ROTCE (annualized)", pct((Q["net_income"][0] - Q["preferred_dividends"][0]) * 4 / 103_000, 0),
         pct((Q["net_income"][1] - Q["preferred_dividends"][1]) * 4 / 101_570, 0),
         pct((Q["net_income"][2] - Q["preferred_dividends"][2]) * 4 / 95_190, 0)]]
story.append(table(rows, [0.46, 0.18, 0.18, 0.18], bold_rows=(3, 6, 8)))
story.append(PageBreak())
story.append(h2("Five-Quarter Trend Summary"))
rows = [["Key metrics", "2Q25", "3Q25", "4Q25", "1Q26", "2Q26"],
        ["Total net revenue ($mm)", "21,330", "21,320", "22,040", "22,550", "22,480"],
        ["Net interest income ($mm)", "12,020", "12,200", "12,390", "12,310", "12,560"],
        ["Noninterest expense ($mm)", "11,750", "11,690", "12,060", "12,390", "12,140"],
        ["Provision for credit losses ($mm)", "1,640", "1,710", "1,890", "1,780", "1,920"],
        ["Net income ($mm)", "6,120", "6,210", "6,310", "6,560", "6,540"],
        ["Diluted EPS ($)", "4.09", "4.20", "4.33", "4.48", "4.48"],
        ["ROTCE", "24%", "25%", "25%", "25%", "24%"],
        ["CET1 ratio (Standardized)", "14.9%", "15.0%", "15.1%", "15.1%", "15.1%"],
        ["Loans, period end ($bn)", "729.8", "736.0", "742.3", "751.9", "761.4"],
        ["Deposits, period end ($bn)", "1,000.1", "1,004.8", "1,012.4", "1,024.8", "1,031.6"],
        ["Allowance for loan losses ($mm)", "15,640", "15,780", "15,920", "16,110", "16,380"],
        ["Net charge-off rate", "0.84%", "0.83%", "0.85%", "0.86%", "0.88%"],
        ["Headcount", "212,800", "213,900", "214,600", "215,300", "216,100"],
        ["API calls per month (bn)", "3.6", "3.8", "4.1", "4.2", "4.4"]]
story.append(table(rows, [0.35, 0.13, 0.13, 0.13, 0.13, 0.13]))
story += ps(
    "Revenue and net income have grown steadily over the last five quarters, supported by loan and deposit "
    "growth and by the recovery in capital markets activity. The CET1 ratio has remained above 14.9% throughout "
    "while the Firm returned approximately $4.6 billion of capital per quarter. Credit costs have risen in line "
    "with Card loan growth and the gradual normalization of consumer charge-off rates.",
)
story.append(line_chart("q2_ni_trend", ["2Q25", "3Q25", "4Q25", "1Q26", "2Q26"],
                        {"Net income ($mm)": [6_120, 6_210, 6_310, 6_560, 6_540]}, "Net income trend", ratio=0.3))
story.append(PageBreak())
story.append(h2("Notes on Presentation and Glossary"))
story += bullets([
    "All amounts are in millions of U.S. dollars unless otherwise noted. Totals may not sum due to rounding.",
    "Segment results are presented on a managed basis; Corporate includes Treasury/CIO and Other Corporate.",
    "Average balances are daily averages. Period-end balances are as of the last day of the quarter.",
    "Regulatory capital ratios are estimated and subject to finalization in the Firm's FR Y-9C filing, which is "
    "prepared from data delivered by the Regulatory Reporting API (API-16).",
    "References to models (MDL-xxx) and APIs (API-xx) correspond to entries in the Firm's model inventory and "
    "Developer Platform catalog. The models are also described in the 2025 Annual Report and Pillar 3 Disclosures.",
])
gl = [("2Q26 / 1Q26 / 2Q25", "Second quarter 2026, first quarter 2026, second quarter 2025."),
      ("Adjusted expense", "Noninterest expense excluding legal expense and the FDIC special assessment."),
      ("Card NCO rate", "Annualized Card net charge-offs divided by average Card loans."),
      ("Deposit beta", "Proportion of a change in policy rates passed through to deposit rates."),
      ("Overhead ratio", "Noninterest expense divided by total net revenue."),
      ("Real-time payments", "Instant, irrevocable account-to-account payments settled 24x7."),
      ("ROTCE", "Annualized net income applicable to common stockholders divided by average tangible common equity."),
      ("SCB", "Stress capital buffer."), ("Wallet share", "Firm's share of global investment banking fees.")]
story.append(table([["Term", "Definition"]] + [list(x) for x in gl], [0.25, 0.75]))
story += ps(
    "<b>Forward-looking statements.</b> This release contains forward-looking statements, including the 2026 "
    "outlook for net interest income, expense and Card net charge-offs, and capital projections. These statements "
    "are subject to risks and uncertainties, and actual results may differ materially.",
    f"<i>{B.BANK['disclaimer']}</i>",
)

doc = ReportDoc("../data/reports/MHFC_Q2_2026_Earnings_Supplement.pdf",
                f"{nm} Q2 2026 Earnings Release and Financial Supplement", "2Q26 Earnings Release & Supplement")
build(doc, story)
print("ok")
