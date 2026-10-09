"""
Single source of truth for the synthetic bank used across every mock document.

Meridian Harbor Financial Corp. ("MHFC") is FICTIONAL. Its structure and disclosure
style are modeled on large U.S. universal banks (segment layout, capital and
liquidity metrics, CECL, Pillar 3), but every name and number here is invented.

All amounts are in USD millions unless a field name says otherwise.
"""

BANK = {
    "name": "Meridian Harbor Financial Corp.",
    "short": "Meridian Harbor",
    "abbr": "MHFC",
    "ticker": "MHFC (fictional)",
    "hq": "Charlotte Bay, NC (fictional)",
    "ceo": "Eleanor V. Ashcombe",
    "cfo": "Rajiv N. Castellano",
    "cro": "Dana K. Whitfield",
    "cto": "Marcus O. Lindqvist",
    "treasurer": "Helen T. Mbeki",
    "employees": 214_600,
    "branches": 4_180,
    "atms": 15_900,
    "digital_users_mm": 61.4,
    "disclaimer": (
        "SYNTHETIC DOCUMENT FOR A PROOF OF CONCEPT. Meridian Harbor Financial Corp. is a "
        "fictional institution. All names, figures and events are invented and do not "
        "describe any real company."
    ),
}

# ---------------------------------------------------------------- consolidated
# FY = fiscal year ending Dec 31.  Values: (FY2025, FY2024)
INCOME = {
    "net_interest_income": (48_620, 46_910),
    "noninterest_revenue": (37_480, 34_950),
    "total_net_revenue": (86_100, 81_860),
    "provision_for_credit_losses": (6_840, 6_120),
    "noninterest_expense": (47_260, 45_580),
    "income_before_tax": (32_000, 30_160),
    "income_tax_expense": (7_040, 6_780),
    "net_income": (24_960, 23_380),
    "preferred_dividends": (1_060, 1_080),
    "net_income_to_common": (23_900, 22_300),
    "diluted_shares_mm": (1_412, 1_448),
}
# noninterest revenue detail (FY2025, FY2024)
NONINT_DETAIL = {
    "Investment banking fees": (6_840, 5_910),
    "Principal transactions": (12_460, 11_820),
    "Lending- and deposit-related fees": (4_310, 4_120),
    "Asset management fees": (9_120, 8_340),
    "Commissions and other fees": (3_020, 2_890),
    "Investment securities losses": (-410, -620),
    "Mortgage fees and related income": (980, 1_040),
    "Card income": (1_160, 1_450),
}
# noninterest expense detail
NONINT_EXP_DETAIL = {
    "Compensation expense": (25_480, 24_310),
    "Occupancy expense": (3_210, 3_140),
    "Technology, communications and equipment": (7_960, 7_420),
    "Professional and outside services": (4_380, 4_290),
    "Marketing": (2_340, 2_210),
    "Other expense": (3_890, 4_210),
}

BALANCE = {  # year-end (2025, 2024)
    "Cash and due from banks": (18_300, 19_100),
    "Deposits with banks": (118_400, 124_600),
    "Federal funds sold and securities purchased under resale agreements": (128_500, 118_300),
    "Trading assets": (132_900, 124_200),
    "Available-for-sale securities": (112_600, 104_900),
    "Held-to-maturity securities, net": (58_300, 62_800),
    "Loans": (742_300, 718_600),
    "Allowance for loan losses": (-15_920, -15_180),
    "Accrued interest and accounts receivable": (38_700, 36_400),
    "Premises and equipment": (19_800, 19_200),
    "Goodwill, MSRs and other intangibles": (33_480, 33_920),
    "Other assets": ((1_418_560 - 18_300 - 118_400 - 128_500 - 132_900 - 112_600
                      - 58_300 - 742_300 + 15_920 - 38_700 - 19_800 - 33_480),
                     (1_362_240 - 19_100 - 124_600 - 118_300 - 124_200 - 104_900
                      - 62_800 - 718_600 + 15_180 - 36_400 - 19_200 - 33_920)),
}
TOTAL_ASSETS = (1_418_560, 1_362_240)
LIABS = {
    "Deposits": (1_012_400, 978_300),
    "Federal funds purchased and securities loaned or sold under repurchase agreements": (58_900, 54_200),
    "Short-term borrowings": (22_100, 19_800),
    "Trading liabilities": (48_300, 45_600),
    "Accounts payable and other liabilities": (61_420, 58_340),
    "Long-term debt": (86_700, 83_400),
}
EQUITY = {
    "Preferred stock": (12_500, 13_000),
    "Common stockholders' equity": (116_240, 109_600),
}
TOTAL_EQUITY = (128_740, 122_600)
# check
assert sum(v[0] for v in LIABS.values()) + TOTAL_EQUITY[0] == TOTAL_ASSETS[0], \
    sum(v[0] for v in LIABS.values()) + TOTAL_EQUITY[0]

KEY_METRICS = {  # FY2025, FY2024
    "Diluted EPS ($)": (16.93, 15.40),
    "Return on common equity": (0.211, 0.209),
    "Return on tangible common equity (ROTCE)": (0.264, 0.263),
    "Overhead (efficiency) ratio": (0.549, 0.557),
    "Book value per share ($)": (83.70, 76.80),
    "Tangible book value per share ($)": (59.60, 52.90),
    "Common shares outstanding, period end (mm)": (1_388.8, 1_427.1),
    "Dividends declared per share ($)": (4.30, 3.90),
    "Net charge-offs": (6_100, 5_420),
    "Net charge-off rate": (0.0084, 0.0077),
    "Allowance to period-end loans": (0.0214, 0.0211),
    "Headcount": (214_600, 211_900),
}

CAPITAL = {  # YE2025 (YE2024) - standardized approach binding
    "CET1 capital": (98_450, 93_120),
    "Tier 1 capital": (110_620, 105_840),
    "Total capital": (128_900, 123_400),
    "Standardized RWA": (652_800, 633_900),
    "Advanced RWA": (618_300, 604_100),
    "Total leverage exposure": (1_812_000, 1_741_000),
    "CET1 ratio (Standardized)": (0.1508, 0.1469),
    "Tier 1 ratio (Standardized)": (0.1695, 0.1670),
    "Total capital ratio (Standardized)": (0.1975, 0.1947),
    "Supplementary leverage ratio": (0.0610, 0.0608),
    "Tier 1 leverage ratio": (0.0791, 0.0790),
}
CAP_REQ = {  # regulatory CET1 requirement stack
    "minimum": 0.045,
    "stress_capital_buffer": 0.032,
    "gsib_surcharge": 0.025,
    "ccyb": 0.0,
    "management_target": 0.130,
}
LIQUIDITY = {
    "LCR (average, Q4)": (1.16, 1.13),
    "NSFR": (1.28, 1.26),
    "HQLA (average, Q4)": (286_000, 274_500),
    "Unencumbered marketable securities": (318_000, 305_000),
}

SEGMENTS = {
    # name: dict of FY2025, FY2024 tuples
    "Consumer & Community Banking": {
        "abbr": "CCB",
        "revenue": (40_800, 38_950), "nii": (31_420, 30_380),
        "provision": (5_960, 5_410), "expense": (18_880, 18_340),
        "net_income": (12_300, 11_520), "roe": (0.30, 0.29),
        "equity_allocated": (40_000, 38_500),
        "avg_loans": (412_600, 401_300), "avg_deposits": (612_000, 598_400),
        "card_nco_rate": (0.0342, 0.0318), "active_mobile_users_mm": (61.4, 57.9),
    },
    "Commercial & Investment Bank": {
        "abbr": "CIB",
        "revenue": (32_450, 30_620), "nii": (12_680, 12_140),
        "provision": (820, 690), "expense": (17_920, 17_110),
        "net_income": (10_180, 9_560), "roe": (0.18, 0.17),
        "equity_allocated": (54_000, 53_000),
        "avg_loans": (268_000, 259_400), "avg_deposits": (318_000, 302_700),
        "ib_fees": (6_840, 5_910), "markets_revenue": (17_920, 17_010),
    },
    "Asset & Wealth Management": {
        "abbr": "AWM",
        "revenue": (13_180, 12_290), "nii": (3_640, 3_550),
        "provision": (60, 20), "expense": (8_420, 7_980),
        "net_income": (3_580, 3_240), "roe": (0.32, 0.30),
        "equity_allocated": (11_000, 10_500),
        "aum_bn": (2_140, 1_910), "client_assets_bn": (3_180, 2_870),
        "avg_loans": (61_700, 57_900),
    },
    "Corporate": {
        "abbr": "CORP",
        "revenue": (-330, 0), "nii": (880, 840),
        "provision": (0, 0), "expense": (2_040, 2_150),
        "net_income": (-1_100, -940),
    },
}
assert sum(s["revenue"][0] for s in SEGMENTS.values()) == INCOME["total_net_revenue"][0]
assert sum(s["net_income"][0] for s in SEGMENTS.values()) == INCOME["net_income"][0]

# ---------------------------------------------------------------- credit / CECL
# CECL portfolio segments at YE2025 - consumed by CECL_Allowance_Model.xlsx
CECL_SEGMENTS = [
    # name, balance, reported allowance, owning LOB, scoring API pool
    ("Credit Card", 138_400, 8_640, "CCB"),
    ("Residential Mortgage", 218_600, 820, "CCB"),
    ("Auto", 64_900, 690, "CCB"),
    ("Commercial Real Estate", 98_200, 2_470, "CIB"),
    ("Commercial & Industrial", 172_500, 2_760, "CIB"),
    ("Other Consumer & Wholesale", 49_700, 540, "AWM/CCB"),
]
assert sum(s[1] for s in CECL_SEGMENTS) == BALANCE["Loans"][0]
assert sum(s[2] for s in CECL_SEGMENTS) == -BALANCE["Allowance for loan losses"][0]

NCO_BY_SEGMENT = {  # FY2025 net charge-offs, $mm
    "Credit Card": 4_620, "Residential Mortgage": 40, "Auto": 410,
    "Commercial Real Estate": 380, "Commercial & Industrial": 560,
    "Other Consumer & Wholesale": 90,
}
assert sum(NCO_BY_SEGMENT.values()) == KEY_METRICS["Net charge-offs"][0]

MACRO_SCENARIOS = {
    # weight, unemployment peak, real GDP 2026, HPI change, CRE price change
    "Upside": (0.20, 0.038, 0.026, 0.045, 0.030),
    "Baseline": (0.50, 0.044, 0.017, 0.022, -0.010),
    "Downside": (0.30, 0.068, -0.012, -0.085, -0.140),
}

# ---------------------------------------------------------------- quarterly
# Q2 2026 earnings (Q2 2026, Q1 2026, Q2 2025)
Q2 = {
    "net_interest_income": (12_560, 12_310, 12_020),
    "noninterest_revenue": (9_920, 10_240, 9_310),
    "total_net_revenue": (22_480, 22_550, 21_330),
    "provision_for_credit_losses": (1_920, 1_780, 1_640),
    "noninterest_expense": (12_140, 12_390, 11_750),
    "income_before_tax": (8_420, 8_380, 7_940),
    "income_tax_expense": (1_880, 1_820, 1_820),
    "net_income": (6_540, 6_560, 6_120),
    "preferred_dividends": (260, 260, 270),
    "diluted_shares_mm": (1_402, 1_407, 1_431),
}
Q2_EPS = (4.48, 4.48, 4.09)
Q2_SEG_NI = {  # Q2 26, Q1 26, Q2 25
    "Consumer & Community Banking": (3_210, 3_150, 3_010),
    "Commercial & Investment Bank": (2_740, 2_890, 2_510),
    "Asset & Wealth Management": (960, 910, 870),
    "Corporate": (-370, -390, -270),
}
assert sum(v[0] for v in Q2_SEG_NI.values()) == Q2["net_income"][0]
assert sum(v[1] for v in Q2_SEG_NI.values()) == Q2["net_income"][1]
assert sum(v[2] for v in Q2_SEG_NI.values()) == Q2["net_income"][2]
Q2_SEG_REV = {
    "Consumer & Community Banking": (10_520, 10_310, 10_090),
    "Commercial & Investment Bank": (8_480, 8_870, 8_110),
    "Asset & Wealth Management": (3_560, 3_440, 3_220),
    "Corporate": (-80, -70, -90),
}
assert sum(v[0] for v in Q2_SEG_REV.values()) == Q2["total_net_revenue"][0]
assert sum(v[1] for v in Q2_SEG_REV.values()) == Q2["total_net_revenue"][1]
assert sum(v[2] for v in Q2_SEG_REV.values()) == Q2["total_net_revenue"][2]

Q2_CAPITAL = {  # Q2 2026 (Q1 2026)
    "CET1 capital": (101_200, 100_100),
    "Standardized RWA": (668_400, 661_000),
    "CET1 ratio (Standardized)": (0.1514, 0.1514),
    "Supplementary leverage ratio": (0.0608, 0.0611),
    "LCR (average)": (1.15, 1.17),
    "Loans (period end)": (761_400, 751_900),
    "Deposits (period end)": (1_031_600, 1_024_800),
    "Total assets (period end)": (1_452_900, 1_441_300),
    "Allowance for loan losses": (16_380, 16_110),
    "Net charge-offs": (1_650, 1_590),
    "Common shares repurchased ($mm)": (3_000, 3_000),
    "Common dividend per share ($)": (1.15, 1.15),
}

# ---------------------------------------------------------------- models & APIs
MODELS = [
    {
        "id": "MDL-ALM-014", "name": "Net Interest Income Sensitivity Model",
        "file": "NII_Sensitivity_Model.xlsx", "tier": "Tier 1 (High)",
        "owner": "Corporate Treasury - Asset & Liability Management",
        "validator": "Model Risk Governance & Review (MRGR)",
        "last_validation": "2025-09-18", "next_validation": "2026-09-30",
        "purpose": "Projects 12-month net interest income under parallel rate shocks and "
                   "economic value of equity (EVE) sensitivity for IRRBB reporting.",
        "apis": ["API-12 Market Data API", "API-15 Treasury Liquidity Positions API",
                 "API-11 Loan Servicing API"],
        "reports": ["Annual Report - Market Risk Management",
                    "Pillar 3 - Interest Rate Risk in the Banking Book"],
    },
    {
        "id": "MDL-CR-007", "name": "CECL Lifetime Expected Credit Loss Model",
        "file": "CECL_Allowance_Model.xlsx", "tier": "Tier 1 (High)",
        "owner": "Consumer & Wholesale Credit Risk - Allowance Methodology",
        "validator": "Model Risk Governance & Review (MRGR)",
        "last_validation": "2025-11-04", "next_validation": "2026-11-30",
        "purpose": "Estimates the allowance for credit losses under ASC 326 (CECL) using "
                   "probability-weighted macroeconomic scenarios and PD x LGD x EAD.",
        "apis": ["API-10 Credit Risk Scoring API", "API-11 Loan Servicing API",
                 "API-14 Macroeconomic Scenario API"],
        "reports": ["Annual Report - Allowance for Credit Losses (Note 6)",
                    "Q2 2026 Earnings Supplement - Credit Trends"],
    },
    {
        "id": "MDL-CAP-003", "name": "Capital Planning & Stress Projection Model",
        "file": "Capital_Planning_Model.xlsx", "tier": "Tier 1 (High)",
        "owner": "Corporate Treasury - Capital Management",
        "validator": "Model Risk Governance & Review (MRGR)",
        "last_validation": "2026-02-27", "next_validation": "2027-02-28",
        "purpose": "Projects CET1 capital, RWA and capital ratios over a nine-quarter horizon "
                   "under baseline and severely adverse scenarios to size distributions.",
        "apis": ["API-16 Regulatory Reporting API", "API-14 Macroeconomic Scenario API",
                 "API-15 Treasury Liquidity Positions API"],
        "reports": ["Annual Report - Capital Risk Management",
                    "Pillar 3 - Capital Planning and Stress Testing"],
    },
]

APIS = [  # id, name, domain, owner, consumers (models/reports)
    ("API-01", "Accounts API", "Retail & Commercial Banking", "Digital Platforms Engineering"),
    ("API-02", "Transactions API", "Retail & Commercial Banking", "Digital Platforms Engineering"),
    ("API-03", "Payments Initiation API", "Payments", "Global Payments Technology"),
    ("API-04", "Real-Time Payments API", "Payments", "Global Payments Technology"),
    ("API-05", "Wire Transfer API", "Payments", "Global Payments Technology"),
    ("API-06", "Card Management API", "Card Services", "Card Technology"),
    ("API-07", "Customer Identity & KYC API", "Client Onboarding", "Know-Your-Customer Platform"),
    ("API-08", "Fraud Risk Signals API", "Fraud & Financial Crimes", "Fraud Strategy Engineering"),
    ("API-09", "Credit Decisioning API", "Credit Origination", "Credit Platforms Engineering"),
    ("API-10", "Credit Risk Scoring API", "Credit Risk", "Risk Analytics Engineering"),
    ("API-11", "Loan Servicing API", "Lending Operations", "Lending Platforms Engineering"),
    ("API-12", "Market Data API", "Markets & Treasury", "Market Data Services"),
    ("API-13", "FX Rates API", "Markets & Treasury", "Market Data Services"),
    ("API-14", "Macroeconomic Scenario API", "Risk & Finance", "Risk Analytics Engineering"),
    ("API-15", "Treasury Liquidity Positions API", "Treasury", "Treasury Technology"),
    ("API-16", "Regulatory Reporting API", "Finance & Regulatory", "Finance Technology"),
    ("API-17", "Statements & Documents API", "Client Servicing", "Digital Platforms Engineering"),
    ("API-18", "Webhooks & Event Notifications API", "Platform", "Developer Platform Engineering"),
]

# Q2 allowance roll-forward check: YE 15,920 - Q1 NCO 1,590 + Q1 provision 1,780 = 16,110
assert 15_920 - 1_590 + 1_780 == Q2_CAPITAL["Allowance for loan losses"][1]
assert 16_110 - 1_650 + 1_920 == Q2_CAPITAL["Allowance for loan losses"][0]

# Pillar 3 capital composition (YE2025)
CET1_BRIDGE = [
    ("Common stockholders' equity", 116_240),
    ("Less: goodwill, net of associated deferred tax liabilities", -14_210),
    ("Less: other intangible assets, net of associated DTLs", -2_150),
    ("Add: cash flow hedge losses in AOCI (reversed)", 3_420),
    ("Less: deferred tax assets from net operating loss and tax credit carryforwards", -1_380),
    ("Less: defined benefit pension fund net assets", -1_240),
    ("Less: other CET1 deductions and adjustments", -2_230),
]
assert sum(v for _, v in CET1_BRIDGE) == CAPITAL["CET1 capital"][0]
RWA_STD = [("Wholesale credit risk", 312_400), ("Retail credit risk", 196_800),
           ("Counterparty credit risk (derivatives and SFTs)", 41_600), ("Securitization exposures", 9_300),
           ("Equity exposures", 6_900), ("Other assets", 31_600), ("Market risk", 54_200)]
assert sum(v for _, v in RWA_STD) == CAPITAL["Standardized RWA"][0]
RWA_ADV = [("Credit risk (incl. CCR and CVA)", 451_500), ("Market risk", 54_200), ("Operational risk", 112_600)]
assert sum(v for _, v in RWA_ADV) == CAPITAL["Advanced RWA"][0]
LEVERAGE = [("On-balance-sheet assets", 1_418_560), ("Less: Tier 1 capital deductions and other adjustments", -19_000),
            ("Derivative exposures (replacement cost + PFE)", 98_600), ("Securities financing transaction exposures", 142_500),
            ("Off-balance-sheet exposures (after credit conversion factors)", 171_340)]
assert sum(v for _, v in LEVERAGE) == CAPITAL["Total leverage exposure"][0]
