"""Shared ReportLab layout for the mock bank reports."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, Image, KeepTogether, NextPageTemplate, CondPageBreak)
from reportlab.platypus.tableofcontents import TableOfContents
import bankdata as B

NAVY = colors.HexColor("#0B2545")
TEAL = colors.HexColor("#13315C")
ACCENT = colors.HexColor("#8DA9C4")
GOLD = colors.HexColor("#B08D57")
ZEBRA = colors.HexColor("#F2F5F9")
GRID = colors.HexColor("#C9D3DF")
CHART_COLORS = ["#0B2545", "#4F7CAC", "#B08D57", "#8DA9C4", "#5E6472", "#C0A36E"]

W, H = letter
MARGIN = 0.8 * inch
CONTENT_W = W - 2 * MARGIN

ST = {
    "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=NAVY,
                         spaceBefore=4, spaceAfter=10, keepWithNext=1),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=12.5, leading=16, textColor=TEAL,
                         spaceBefore=10, spaceAfter=5, keepWithNext=1),
    "h3": ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=10.2, leading=13, textColor=NAVY,
                         spaceBefore=7, spaceAfter=3, keepWithNext=1),
    "body": ParagraphStyle("body", fontName="Times-Roman", fontSize=10.2, leading=13.6, alignment=TA_JUSTIFY,
                           spaceAfter=6),
    "bullet": ParagraphStyle("bullet", fontName="Times-Roman", fontSize=10.2, leading=13.4, leftIndent=14,
                             bulletIndent=4, spaceAfter=3, alignment=TA_LEFT),
    "caption": ParagraphStyle("caption", fontName="Helvetica-Oblique", fontSize=7.8, leading=10,
                              textColor=colors.HexColor("#555555"), spaceAfter=8),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=7.9, leading=9.6),
    "cellb": ParagraphStyle("cellb", fontName="Helvetica-Bold", fontSize=7.9, leading=9.6),
    "cellh": ParagraphStyle("cellh", fontName="Helvetica-Bold", fontSize=7.9, leading=9.6, textColor=colors.white),
    "cellr": ParagraphStyle("cellr", fontName="Helvetica", fontSize=7.9, leading=9.6, alignment=TA_RIGHT),
    "quote": ParagraphStyle("quote", fontName="Times-Italic", fontSize=11, leading=15, leftIndent=18,
                            rightIndent=18, textColor=TEAL, spaceBefore=6, spaceAfter=8),
    "callout": ParagraphStyle("callout", fontName="Helvetica", fontSize=8.6, leading=11.5, textColor=NAVY),
    "toc1": ParagraphStyle("toc1", fontName="Helvetica-Bold", fontSize=10, leading=15, leftIndent=0),
    "toc2": ParagraphStyle("toc2", fontName="Helvetica", fontSize=9, leading=12.5, leftIndent=16),
}


# ------------------------------------------------------------------ formatting
def m(x, dec=0):
    """$mm number with commas, negatives in parentheses."""
    if x is None:
        return "-"
    s = f"{abs(x):,.{dec}f}"
    return f"({s})" if x < 0 else s


def usd(x, dec=0):
    return ("-$" if x < 0 else "$") + f"{abs(x):,.{dec}f}"


def pct(x, dec=1):
    if x is None:
        return "-"
    s = f"{abs(x) * 100:.{dec}f}%"
    return f"({s})" if x < 0 else s


def chg(a, b):
    return (a - b) / abs(b) if b else 0


def bn(x, dec=1):
    return f"${x / 1000:,.{dec}f} billion"


# ------------------------------------------------------------------ document
class ReportDoc(BaseDocTemplate):
    def __init__(self, path, title, running_header, **kw):
        super().__init__(path, pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN,
                         topMargin=0.95 * inch, bottomMargin=0.85 * inch, title=title,
                         author=B.BANK["name"], subject=B.BANK["disclaimer"], **kw)
        self.running_header = running_header
        frame = Frame(MARGIN, 0.85 * inch, CONTENT_W, H - 1.8 * inch, id="f")
        self.addPageTemplates([
            PageTemplate("cover", frames=[Frame(0, 0, W, H, leftPadding=0, rightPadding=0,
                                                topPadding=0, bottomPadding=0)], onPage=self._cover_bg),
            PageTemplate("body", frames=[frame], onPage=self._decorate),
        ])

    def _cover_bg(self, c, doc):
        c.saveState()
        c.setFillColor(NAVY)
        c.rect(0, 0, W, H, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(MARGIN, H * 0.58, 1.3 * inch, 4, stroke=0, fill=1)
        c.restoreState()

    def _decorate(self, c, doc):
        c.saveState()
        c.setStrokeColor(ACCENT)
        c.setLineWidth(0.6)
        c.line(MARGIN, H - 0.68 * inch, W - MARGIN, H - 0.68 * inch)
        c.setFont("Helvetica-Bold", 7.6)
        c.setFillColor(NAVY)
        c.drawString(MARGIN, H - 0.6 * inch, B.BANK["name"].upper())
        c.setFont("Helvetica", 7.6)
        c.drawRightString(W - MARGIN, H - 0.6 * inch, self.running_header)
        c.line(MARGIN, 0.62 * inch, W - MARGIN, 0.62 * inch)
        c.setFont("Helvetica", 6.6)
        c.setFillColor(colors.HexColor("#8A1C1C"))
        c.drawString(MARGIN, 0.47 * inch, "Synthetic document - fictional institution - for proof-of-concept use only")
        c.setFillColor(NAVY)
        c.setFont("Helvetica", 7.6)
        c.drawRightString(W - MARGIN, 0.47 * inch, str(doc.page))
        c.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            sn = flowable.style.name
            if sn in ("h1", "h2"):
                text = flowable.getPlainText()
                level = 0 if sn == "h1" else 1
                key = f"k{id(flowable)}"
                self.canv.bookmarkPage(key)
                self.notify("TOCEntry", (level, text, self.page, key))
                self.canv.addOutlineEntry(text, key, level=level, closed=level > 0)


def cover(title, subtitle, date_line, extra_lines=()):
    tstyle = ParagraphStyle("ct", fontName="Helvetica-Bold", fontSize=30, leading=36, textColor=colors.white)
    sstyle = ParagraphStyle("cs", fontName="Helvetica", fontSize=14, leading=19, textColor=ACCENT)
    nstyle = ParagraphStyle("cn", fontName="Helvetica-Bold", fontSize=13, leading=17, textColor=colors.white)
    dstyle = ParagraphStyle("cd", fontName="Helvetica", fontSize=10, leading=14, textColor=colors.white)
    wstyle = ParagraphStyle("cw", fontName="Helvetica-Oblique", fontSize=8, leading=11,
                            textColor=colors.HexColor("#F3C6C6"))
    items = [Spacer(1, 1.3 * inch)]
    inner = [Paragraph(B.BANK["name"].upper(), nstyle), Spacer(1, 2.3 * inch),
             Paragraph(title, tstyle), Spacer(1, 10), Paragraph(subtitle, sstyle), Spacer(1, 22),
             Paragraph(date_line, dstyle)]
    for e in extra_lines:
        inner.append(Paragraph(e, dstyle))
    inner += [Spacer(1, 2.2 * inch), Paragraph(B.BANK["disclaimer"], wstyle)]
    t = Table([[inner]], colWidths=[W - 2 * MARGIN])
    t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), MARGIN), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    items.append(t)
    items += [NextPageTemplate("body"), PageBreak()]
    return items


def toc_page():
    toc = TableOfContents()
    toc.levelStyles = [ST["toc1"], ST["toc2"]]
    toc.dotsMinLevel = 0
    return [Paragraph("Contents", ST["h1"].clone("tocttl")), Spacer(1, 6), toc, PageBreak()]


def h1(t):
    return Paragraph(t, ST["h1"])


def h2(t):
    return Paragraph(t, ST["h2"])


def h3(t):
    return Paragraph(t, ST["h3"])


def p(t):
    return Paragraph(t, ST["body"])


def ps(*texts):
    return [p(t) for t in texts]


def bullets(items):
    return [Paragraph(i, ST["bullet"], bulletText="•") for i in items]


def caption(t):
    return Paragraph(t, ST["caption"])


def quote(t):
    return Paragraph(t, ST["quote"])


def callout(title, text):
    inner = [Paragraph(f"<b>{title}</b>", ST["callout"]), Spacer(1, 3), Paragraph(text, ST["callout"])]
    t = Table([[inner]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), ZEBRA), ("BOX", (0, 0), (-1, -1), 0.6, ACCENT),
                           ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                           ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                           ("LINEBEFORE", (0, 0), (0, -1), 3, GOLD)]))
    return KeepTogether([t, Spacer(1, 8)])


def table(rows, col_widths=None, header_rows=1, total_rows=(), first_col_left=True, title=None,
          note=None, bold_rows=(), indent_rows=()):
    """rows: list of lists of str. Numbers should be pre-formatted strings."""
    n_cols = len(rows[0])
    if col_widths is None:
        first = CONTENT_W * 0.42 if n_cols > 2 else CONTENT_W * 0.6
        rest = (CONTENT_W - first) / (n_cols - 1)
        col_widths = [first] + [rest] * (n_cols - 1)
    elif sum(col_widths) <= 1.01:
        col_widths = [w * CONTENT_W for w in col_widths]
    data = []
    total_idx = {len(rows) + t if t < 0 else t for t in total_rows}
    for i, r in enumerate(rows):
        out = []
        for j, v in enumerate(r):
            v = "" if v is None else str(v)
            if i < header_rows:
                st = ST["cellh"]
                st = st.clone("hc", alignment=TA_LEFT if j == 0 else TA_RIGHT) if first_col_left else st
            elif j == 0 and first_col_left:
                st = ST["cellb"] if (i in total_idx or i in bold_rows) else ST["cell"]
                if i in indent_rows:
                    st = st.clone("ind", leftIndent=10)
            else:
                st = ST["cellr"].clone("rb", fontName="Helvetica-Bold") if (i in total_idx or i in bold_rows) \
                    else ST["cellr"]
            out.append(Paragraph(v, st))
        data.append(out)
    t = Table(data, colWidths=col_widths, repeatRows=header_rows)
    style = [("BACKGROUND", (0, 0), (-1, header_rows - 1), NAVY),
             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
             ("TOPPADDING", (0, 0), (-1, -1), 2.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
             ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
             ("LINEBELOW", (0, -1), (-1, -1), 0.8, NAVY)]
    for i in range(header_rows, len(rows)):
        if (i - header_rows) % 2 == 1:
            style.append(("BACKGROUND", (0, i), (-1, i), ZEBRA))
    for i in total_idx:
        style.append(("LINEABOVE", (0, i), (-1, i), 0.8, NAVY))
    t.setStyle(TableStyle(style))
    items = []
    if title:
        items.append(Paragraph(f"<b>{title}</b>", ST["h3"]))
    items.append(t)
    if note:
        items.append(Spacer(1, 2))
        items.append(caption(note))
    else:
        items.append(Spacer(1, 8))
    return KeepTogether(items) if len(rows) < 28 else items


# ------------------------------------------------------------------ charts
CHART_DIR = os.path.join(os.path.dirname(__file__), "_charts")
os.makedirs(CHART_DIR, exist_ok=True)


def _style_ax(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#999999")
    ax.spines["bottom"].set_color("#999999")
    ax.tick_params(colors="#333333", labelsize=8)
    ax.yaxis.grid(True, color="#E3E8EF", linewidth=0.7)
    ax.set_axisbelow(True)


def chart_image(fig, name, width=CONTENT_W, ratio=0.42):
    path = os.path.join(CHART_DIR, f"{name}.png")
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return Image(path, width=width, height=width * ratio)


def bar_chart(name, labels, series, title, ylabel="", width=CONTENT_W, ratio=0.38, fmt="{:,.0f}", stacked=False):
    fig, ax = plt.subplots(figsize=(7.2, 7.2 * ratio))
    n = len(series)
    import numpy as np
    x = np.arange(len(labels))
    bw = 0.8 / (1 if stacked else n)
    bottom = np.zeros(len(labels))
    for k, (sname, vals) in enumerate(series.items()):
        if stacked:
            bars = ax.bar(x, vals, 0.6, bottom=bottom, label=sname, color=CHART_COLORS[k % 6])
            bottom += np.array(vals)
        else:
            bars = ax.bar(x - 0.4 + bw * (k + 0.5), vals, bw * 0.92, label=sname, color=CHART_COLORS[k % 6])
            if n <= 2 and len(labels) <= 8:
                for b_ in bars:
                    ax.annotate(fmt.format(b_.get_height()), (b_.get_x() + b_.get_width() / 2, b_.get_height()),
                                ha="center", va="bottom", fontsize=6.5, color="#333333",
                                xytext=(0, 2), textcoords="offset points")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=7.5)
    ax.set_title(title, fontsize=9.5, color="#0B2545", loc="left", fontweight="bold")
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=8)
    _style_ax(ax)
    if n > 1:
        ax.legend(fontsize=7, frameon=False, ncol=min(n, 4), loc="upper left")
    return chart_image(fig, name, width, ratio)


def line_chart(name, labels, series, title, ylabel="", width=CONTENT_W, ratio=0.36, pct_axis=False, hlines=()):
    fig, ax = plt.subplots(figsize=(7.2, 7.2 * ratio))
    for k, (sname, vals) in enumerate(series.items()):
        ax.plot(labels, vals, marker="o", markersize=3.5, linewidth=1.8, label=sname, color=CHART_COLORS[k % 6])
    for val, lab, col in hlines:
        ax.axhline(val, linestyle="--", linewidth=1, color=col)
        ax.text(len(labels) - 1, val, f" {lab}", fontsize=7, va="bottom", ha="right", color=col)
    ax.set_title(title, fontsize=9.5, color="#0B2545", loc="left", fontweight="bold")
    if pct_axis:
        from matplotlib.ticker import PercentFormatter
        ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=1))
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=8)
    ax.tick_params(axis="x", labelsize=7.5)
    _style_ax(ax)
    ax.legend(fontsize=7, frameon=False, loc="best")
    return chart_image(fig, name, width, ratio)


def donut(name, labels, vals, title, width=CONTENT_W * 0.5, ratio=0.85):
    fig, ax = plt.subplots(figsize=(3.6, 3.6 * ratio))
    ax.pie(vals, labels=None, colors=CHART_COLORS[:len(vals)], startangle=90,
           wedgeprops=dict(width=0.38, edgecolor="white"))
    ax.set_title(title, fontsize=9, color="#0B2545", fontweight="bold")
    ax.legend(labels, fontsize=6.5, frameon=False, loc="center left", bbox_to_anchor=(0.95, 0.5))
    return chart_image(fig, name, width, ratio)


def side_by_side(left, right, gap=10):
    lw = (CONTENT_W - gap) / 2
    t = Table([[left, right]], colWidths=[lw + gap / 2, lw + gap / 2])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    return t


def build(doc, story):
    flat = []
    for s in story:
        if isinstance(s, list):
            flat.extend(s)
        else:
            flat.append(s)
    doc.multiBuild(flat)
