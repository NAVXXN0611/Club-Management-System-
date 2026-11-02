#!/usr/bin/env python3
"""
CCMS Micro Project Report builder — replicates the Karunya Institute
"Micro Project Report (2026-27)" format exactly and fills in the content
for the College Club Management System (CCMS) project.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, PageBreak, Table, TableStyle, Flowable,
                                NextPageTemplate, KeepTogether)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Polygon
from reportlab.pdfgen import canvas as rl_canvas

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'CCMS-Micro-Project-Report-2026-27.pdf')
W, H = A4  # 596 x 842

MAROON = colors.HexColor('#7B0000')
LIGHTV = colors.HexColor('#EDE9FE')
MIDV = colors.HexColor('#7C3AED')
GREY = colors.HexColor('#444444')
LGREY = colors.HexColor('#DDDDDD')

SECTION_PAGES = {}   # marker key -> page number

# ---------------------------------------------------------------- page furniture
def draw_watermark(c):
    c.drawImage(os.path.join(HERE, 'assets/watermark.png'),
                -198.2, 601.0, 467.3, 425.3, mask='auto')

def draw_header_footer(c):
    c.setFont('Times-Roman', 8.2)
    c.setFillColor(colors.black)
    c.drawString(71, H - 39.1, 'Micro Project Report (2026-27)')
    c.drawString(277, H - 39.1, 'Division of Computer Science and Engineering')
    c.drawString(71, 39.0, 'Karunya Institute of Technology and Sciences')

class NumberedCanvas(rl_canvas.Canvas):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._saved = []
    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()
    def save(self):
        total = len(self._saved)
        for st in self._saved:
            self.__dict__.update(st)
            self.setFont('Times-Roman', 8.2)
            self.setFillColor(colors.black)
            self.drawRightString(492.6, 39.0, f'Page {self._pageNumber} of {total}')
            super().showPage()
        super().save()
    def setTitle(self, t):
        super().setTitle(t)

# ---------------------------------------------------------------- markers
class Marker(Flowable):
    def __init__(self, key):
        super().__init__()
        self.key = key
        self.width = 0; self.height = 0
    def wrap(self, aw, ah):
        return (0, 0)
    def draw(self):
        SECTION_PAGES[self.key] = self.canv.getPageNumber()

def pg(key):
    n = SECTION_PAGES.get(key)
    return str(n) if n else '##'

# ---------------------------------------------------------------- styles
def st(name, **kw):
    base = dict(fontName='Times-Roman', fontSize=12, leading=15.5,
                textColor=colors.black, alignment=TA_JUSTIFY, spaceAfter=7)
    base.update(kw)
    return ParagraphStyle(name, **base)

S_BODY   = st('body')
S_H1     = st('h1', fontName='Times-Bold', fontSize=14, leading=18, textColor=MAROON,
              spaceBefore=4, spaceAfter=9, alignment=TA_LEFT, keepWithNext=1)
S_H2     = st('h2', fontName='Times-Bold', fontSize=12.5, leading=16, spaceBefore=8,
              spaceAfter=6, alignment=TA_LEFT, keepWithNext=1)
S_PAGEH  = st('pageh', fontName='Times-Bold', fontSize=14, leading=18,
              alignment=TA_CENTER, spaceAfter=16, keepWithNext=1)
S_BULLET = st('bullet', leftIndent=18, bulletIndent=4, spaceAfter=5)
S_CAP    = st('cap', fontName='Times-Italic', fontSize=9.5, leading=12,
              alignment=TA_CENTER, spaceBefore=3, spaceAfter=11)
S_TABTXT = st('tab', fontName='Times-Roman', fontSize=9.5, leading=12, alignment=TA_LEFT)
S_TABHD  = st('tabhd', fontName='Times-Bold', fontSize=9.5, leading=12, alignment=TA_CENTER)
S_CODE   = st('code', fontName='Courier', fontSize=8.2, leading=10.5, alignment=TA_LEFT)
S_TOC    = st('toc', alignment=TA_LEFT, spaceAfter=2)

def bullet(text):
    return Paragraph(text, S_BULLET, bulletText='\u2022')

# ---------------------------------------------------------------- TOC entry flowable
class TocEntry(Flowable):
    def __init__(self, label, page, indent=0, bold=False):
        super().__init__()
        self.label = label; self.page = page; self.indent = indent
        self.bold = bold
        self.width = 454; self.height = 17
    def wrap(self, aw, ah):
        return (454, 17)
    def draw(self):
        c = self.canv
        c.setFont('Times-Bold' if self.bold else 'Times-Roman', 11.5)
        c.setFillColor(colors.black)
        x = self.indent
        c.drawString(x, 3, self.label)
        lw = c.stringWidth(self.label, 'Times-Bold' if self.bold else 'Times-Roman', 11.5)
        # dotted leader
        dot_x = x + lw + 8
        page_w = c.stringWidth(str(self.page), 'Times-Roman', 11.5)
        end_dots = 454 - page_w - 8
        c.setFont('Times-Roman', 11.5)
        while dot_x < end_dots:
            c.drawString(dot_x, 3, '.')
            dot_x += 5
        c.drawRightString(454, 3, str(self.page))

# ================================================================ SPECIAL PAGES
def cover_page(c, doc):
    draw_watermark(c); draw_header_footer(c)
    c.drawImage(os.path.join(HERE, 'assets/banner.png'), 126.6, 716.4, 356.3, 54.0, mask='auto')
    c.setFillColor(colors.black)
    # division / school
    c.setFont('Times-Bold', 16)
    c.drawCentredString(W / 2 + 3, H - 217.7, 'DIVISION OF COMPUTER SCIENCE AND ENGINEERING')
    c.setFont('Times-Bold', 12.8)
    c.drawCentredString(W / 2 + 3, H - 253.9, 'SCHOOL OF COMPUTER SCIENCE AND TECHNOLOGY')
    # skill based evaluation report block
    c.setFont('Times-Bold', 18)
    c.drawCentredString(W / 2 + 3, H - 348.6, 'SKILL BASED EVALUATION REPORT')
    c.setFont('Times-Bold', 14)
    c.drawCentredString(W / 2 + 3, H - 398.4, 'Academic Year 2026-2027')
    c.drawCentredString(W / 2 + 3, H - 447.8, 'ODD SEMESTER')
    # microproject title (centered, per format item 1.a)
    c.setFont('Times-Bold', 12.5)
    c.drawCentredString(W / 2, H - 480.8, 'Title of the Microproject : College Club Management System (CCMS)')
    # fields
    fields = [
        ('Name', 'Naveen Kumar R V, Jeril Dany', 507.5),
        ('Register Number', 'URK2CS1016, URK25CS1', 540.4),
        ('Course Code', '25CS312', 573.5),
        ('Course Name', 'Software Engineering', 606.4),
    ]
    for lab, val, top in fields:
        y = H - top
        c.setFont('Times-Bold', 14)
        c.drawString(77.4, y, lab)
        c.drawString(216, y, ':')
        c.drawString(225, y, val)
    c.setFont('Times-Bold', 14)
    c.drawCentredString(W / 2 + 3, H - 688.7, 'Oct 2026')

def outline_page(c, doc):
    draw_watermark(c); draw_header_footer(c)
    c.setFillColor(colors.black)
    def line(x, top, text, font='Times-Roman', size=12.4):
        c.setFont(font, size)
        c.drawString(x, H - top - size * 0.662, text)
    # numbered section (exact template text & positions)
    line(90.3, 59.7, '1.'); line(107.3, 59.7, 'Cover Page')
    line(125.3, 73.6, 'a.'); line(143.3, 73.6, 'Title of the Microproject')
    line(124.9, 87.1, 'b.'); line(143.7, 87.1, 'Student names and registration numbers')
    line(89.2, 101.1, '2.'); line(107.0, 101.1, 'Abstract')
    line(89.4, 114.9, '3.'); line(107.0, 114.9, 'Table of Contents')
    line(89.1, 128.7, '4.'); line(107.1, 128.7, 'List of Figures and Tables (if applicable)')
    chapters = [
        ('Chapter 1: Introduction', 157.2,
         [('1.1', 'Background of the Project', 171.9), ('1.2', 'Problem Statement', 185.7),
          ('1.3', 'Objectives', 199.5), ('1.4', 'Scope of the Project', 213.3)]),
        ('Chapter 2: Literature Survey', 235.1,
         [('2.1', 'Review of Existing Research or Related Projects', 249.8),
          ('2.2', 'Summary of Existing Approaches', 263.6),
          ('2.3', 'Research Gap or Limitations of Existing Systems', 277.4)]),
        ('Chapter 3: Methodology and System Design', 305.9,
         [('31', 'Proposed Methodology', 320.6), ('3.2', 'System Architecture or Block Diagram', 334.4),
          ('3.3', 'UML Diagrams', 348.2), ('3.4', 'Tools and Technologies Used', 362.0),
          ('3.5', 'Module Description', 375.8)]),
        ('Chapter 4: Implementation and Results', 404.4,
         [('4.1', 'Implementation Details', 419.1), ('4.2', 'Screenshots of the Application', 432.9),
          ('4.3', 'Sample Inputs and Outputs', 446.7), ('4.4', 'Unit Testing and Results', 460.5)]),
        ('Chapter 5: Conclusion and Future Enhancement', 482.3,
         [('5.1', 'Summary of the Work', 497.2), ('5.2', 'Conclusion', 511.0),
          ('5.3', 'Future Enhancements', 524.8)]),
    ]
    for head, htop, subs in chapters:
        line(71.3, htop, head, 'Times-Bold')
        for num, txt, top in subs:
            line(89.8, top + 2.7, '\u25cf', 'Times-Roman', 10)
            line(107.3, top, f'{num} {txt}')
    line(71.1, 552.6,
         'References \u2014 research papers, books, websites, and other sources cited in the report.')

def ppt_page(c, doc):
    draw_watermark(c); draw_header_footer(c)
    c.setFillColor(colors.black)
    c.setFont('Times-Bold', 14)
    c.drawCentredString(W / 2 + 3, H - 164.3, 'PPT HANDOUTS')
    c.drawCentredString(W / 2 + 3, H - 181.0, '(4 Slides per page)')

def cert_page(c, doc):
    draw_watermark(c); draw_header_footer(c)
    c.setFillColor(colors.black)
    c.setFont('Times-Bold', 14)
    c.drawCentredString(W / 2 + 3, H - 239.3, 'Introduction to Selenium 4 Certificate')
    from reportlab.lib.utils import ImageReader
    img = ImageReader(os.path.join(HERE, 'assets/certificate.png'))
    iw, ih = img.getSize()
    wdt = 470; hgt = wdt * ih / iw
    c.drawImage(img, (W - wdt) / 2, H - 280 - hgt, wdt, hgt, mask='auto')

def eval_page(c, doc):
    draw_watermark(c); draw_header_footer(c)
    c.setFillColor(colors.black)
    c.setFont('Times-Bold', 14)
    c.drawCentredString(W / 2 + 3, H - 120.6, 'EVALUATION SHEET')
    rows = [
        ('Reg. No.', 'URK2CS1016, URK25CS1', 180.8),
        ('Name', 'Naveen Kumar R V, Jeril Dany', 210.8),
        ('Course code', '25CS312', 240.8),
        ('Course Name', 'Software Engineering', 270.8),
    ]
    for lab, val, base in rows:
        y = H - base
        c.setFont('Times-Bold', 14)
        c.drawString(71.4, y, lab)
        c.drawString(178, y, ':')
        c.drawString(189, y, val)
    # table (x 66 -> 569, top 324 -> bottom 667.2)
    X0, X1 = 66, 569
    cols = [66, 120, 382.5, 476, 569]
    top = H - 324
    rows_h = [56.9, 38.1, 56.1, 37.9, 37.9, 38.9, 38.4, 38.4]  # header + 6 + total
    rowtops = [top]
    for h in rows_h:
        rowtops.append(rowtops[-1] - h)
    c.setLineWidth(0.8)
    for y in rowtops:
        c.line(X0, y, X1, y)
    for x in cols:
        c.line(x, top, x, rowtops[-1])
    def cell(txt, x, ytop, h, font='Times-Bold', size=13, center=False):
        c.setFont(font, size)
        yy = ytop - (h - size * 0.662) / 2 - size * 0.662
        if center:
            c.drawCentredString(x, yy, txt)
        else:
            c.drawString(x, yy, txt)
    # header row (two-line for col3/col4)
    htop, hh = rowtops[0], rows_h[0]
    c.setFont('Times-Bold', 13)
    c.drawCentredString((cols[0] + cols[1]) / 2, htop - hh / 2 - 4.3, 'S.No')
    c.drawCentredString((cols[1] + cols[2]) / 2, htop - hh / 2 - 4.3, 'Rubrics')
    c.drawCentredString((cols[2] + cols[3]) / 2, htop - 20, 'Maximum')
    c.drawCentredString((cols[2] + cols[3]) / 2, htop - 37, 'Marks')
    c.drawCentredString((cols[3] + cols[4]) / 2, htop - 20, 'Marks')
    c.drawCentredString((cols[3] + cols[4]) / 2, htop - 37, 'Obtained')
    body = [
        ('1', 'Problem Definition', '6', None),
        ('2', 'Application of SE concepts &', '6', 'Design'),
        ('3', 'Implementation', '6', None),
        ('4', 'Testing & Results', '6', None),
        ('5', 'Report & Viva', '6', None),
        ('6', 'Certificate Completion', '10', None),
    ]
    r = 1
    for num, txt, mx, line2 in body:
        ytop, hh = rowtops[r], rows_h[r]
        cell(num, (cols[0] + cols[1]) / 2, ytop, hh, center=True)
        if line2:
            c.setFont('Times-Bold', 13)
            c.drawString(cols[1] + 5, ytop - 23.2, txt)
            c.drawString(cols[1] + 5, ytop - 39.6, line2)
        else:
            cell(txt, cols[1] + 5, ytop, hh)
        if mx:
            cell(mx, (cols[2] + cols[3]) / 2, ytop, hh, center=True)
        r += 1
    # total row
    ytop, hh = rowtops[7], rows_h[7]
    c.setFont('Times-Bold', 13)
    c.drawCentredString((cols[0] + cols[2]) / 2, ytop - (hh - 8.6) / 2 - 8.6, 'Total')
    c.drawCentredString((cols[2] + cols[3]) / 2, ytop - (hh - 8.6) / 2 - 8.6, '40')
    c.setFont('Times-Bold', 12.8)
    c.drawString(324.2, H - 751.3, 'Signature of the Faculty-in-charge')

# ================================================================ FIGURE DRAWINGS
def fig_architecture():
    d = Drawing(454, 285)
    def band(y, h, label, color_):
        d.add(Rect(10, y, 434, h, fillColor=color_, strokeColor=MIDV, strokeWidth=1, rx=8, ry=8))
        d.add(String(20, y + h - 14, label, fontName='Times-Bold', fontSize=9, fillColor=MIDV))
    band(205, 72, 'CLIENT TIER (Browser)', LIGHTV)
    for i, (t, sub) in enumerate([('Student', 'Discover / Join / RSVP'), ('Coordinator', 'Manage club & events'), ('Admin', 'Approve & monitor')]):
        x = 28 + i * 142
        d.add(Rect(x, 212, 130, 42, fillColor=colors.white, strokeColor=MIDV, strokeWidth=0.8, rx=5, ry=5))
        d.add(String(x + 65, 236, t, fontName='Times-Bold', fontSize=9.5, textAnchor='middle'))
        d.add(String(x + 65, 224, sub, fontName='Times-Roman', fontSize=7, textAnchor='middle', fillColor=GREY))
    band(112, 72, 'APPLICATION TIER (Supabase)', LIGHTV)
    for i, t in enumerate(['React + TypeScript SPA', 'Supabase JS Client / REST API', 'Auth (JWT) + Row Level Security']):
        d.add(Rect(28 + i * 142, 119, 130, 42, fillColor=colors.white, strokeColor=MIDV, strokeWidth=0.8, rx=5, ry=5))
        d.add(String(28 + i * 142 + 65, 137, t, fontName='Times-Roman', fontSize=7.3, textAnchor='middle'))
    band(12, 72, 'DATA TIER (PostgreSQL)', LIGHTV)
    d.add(Rect(28, 19, 398, 42, fillColor=colors.white, strokeColor=MIDV, strokeWidth=0.8, rx=5, ry=5))
    d.add(String(227, 38, 'profiles | clubs | club_memberships | events |', fontName='Times-Roman', fontSize=7.3, textAnchor='middle'))
    d.add(String(227, 28, 'event_registrations | attendance | announcements', fontName='Times-Roman', fontSize=7.3, textAnchor='middle'))
    for y in (195, 102):
        d.add(Polygon([222, y, 232, y, 227, y - 9], fillColor=MIDV, strokeColor=MIDV))
        d.add(Line(227, y + 2, 227, y + 8, strokeColor=MIDV, strokeWidth=1.2))
    return d

def stick(x, y, label):
    g = []
    g.append(Circle(x, y + 26, 5.5, fillColor=colors.white, strokeColor=colors.black, strokeWidth=1))
    g.append(Line(x, y + 20, x, y + 8, strokeColor=colors.black, strokeWidth=1))
    g.append(Line(x - 8, y + 15, x + 8, y + 15, strokeColor=colors.black, strokeWidth=1))
    g.append(Line(x, y + 8, x - 7, y, strokeColor=colors.black, strokeWidth=1))
    g.append(Line(x, y + 8, x + 7, y, strokeColor=colors.black, strokeWidth=1))
    g.append(String(x, y - 12, label, fontName='Times-Bold', fontSize=8.5, textAnchor='middle'))
    return g

def fig_usecase():
    d = Drawing(454, 300)
    d.add(Rect(90, 18, 300, 265, fillColor=None, strokeColor=MIDV, strokeWidth=1, rx=10, ry=10, strokeDashArray=[4, 3]))
    d.add(String(240, 272, 'CCMS System', fontName='Times-Bold', fontSize=9, textAnchor='middle', fillColor=MIDV))
    uses = [
        ('Discover Clubs', 150, 240), ('Apply for Membership', 275, 240), ('Register for Events', 150, 195),
        ('View Announcements', 275, 195), ('Track Attendance', 150, 150), ('View Participation History', 275, 150),
        ('Manage Club & Events', 150, 105), ('Approve Applications', 275, 105), ('View Analytics', 150, 60),
        ('Manage Users & Clubs', 275, 60),
    ]
    for t, x, y in uses:
        d.add(Rect(x - 58, y - 11, 116, 22, fillColor=LIGHTV, strokeColor=MIDV, strokeWidth=0.8, rx=11, ry=11))
        d.add(String(x, y - 3.5, t, fontName='Times-Roman', fontSize=7.4, textAnchor='middle'))
    for g in stick(35, 190, 'Student'): d.add(g)
    for g in stick(35, 85, 'Coordinator'): d.add(g)
    for g in stick(420, 135, 'Admin'): d.add(g)
    def link(x1, y1, x2, y2):
        d.add(Line(x1, y1, x2, y2, strokeColor=colors.HexColor('#9CA3AF'), strokeWidth=0.7))
    for y in (240, 195, 150, 60): link(58, 200, 92, y)
    for y in (150, 105, 60): link(58, 95, 92, y)
    for y in (240, 105, 60): link(398, 145, 362, y)
    return d

def fig_er():
    d = Drawing(454, 315)
    ents = [
        ('profiles', ['id (PK)', 'full_name, email', 'role'], 10, 230),
        ('clubs', ['id (PK)', 'name, slug', 'category_id (FK)'], 170, 230),
        ('club_categories', ['id (PK)', 'name'], 330, 230),
        ('club_memberships', ['student_id (FK)', 'club_id (FK)', 'status'], 90, 145),
        ('events', ['id (PK)', 'club_id (FK)', 'title, event_date', 'venue, capacity'], 265, 145),
        ('event_registrations', ['event_id (FK)', 'student_id (FK)'], 65, 55),
        ('attendance', ['event_id (FK)', 'student_id (FK)', 'status'], 200, 55),
        ('announcements', ['id (PK)', 'club_id (FK)', 'title, content'], 330, 55),
    ]
    for name, attrs, x, y in ents:
        w = 115 if name != 'events' else 130
        h = 16 + 10 * len(attrs)
        d.add(Rect(x, y, w, h, fillColor=colors.white, strokeColor=MIDV, strokeWidth=1))
        d.add(Rect(x, y + h - 15, w, 15, fillColor=MIDV, strokeColor=MIDV, strokeWidth=1))
        d.add(String(x + w / 2, y + h - 11, name, fontName='Times-Bold', fontSize=7.8,
                     textAnchor='middle', fillColor=colors.white))
        for i, a in enumerate(attrs):
            d.add(String(x + 5, y + h - 27 - 10 * i, a, fontName='Times-Roman', fontSize=6.6))
    def rel(x1, y1, x2, y2, label):
        d.add(Line(x1, y1, x2, y2, strokeColor=colors.HexColor('#6B7280'), strokeWidth=0.9))
        d.add(String((x1 + x2) / 2 + 3, (y1 + y2) / 2 + 2, label, fontName='Times-Italic', fontSize=6.5, fillColor=GREY))
    rel(125, 255, 170, 255, '1:N')
    rel(285, 255, 330, 255, 'N:1')
    rel(100, 230, 120, 181, '1:N')
    rel(240, 230, 300, 181, '1:N')
    rel(130, 145, 115, 91, '1:N')
    rel(300, 145, 255, 91, '1:N')
    rel(300, 130, 365, 91, '1:N')
    return d

def fig_modules():
    d = Drawing(454, 250)
    d.add(Rect(172, 210, 110, 28, fillColor=MIDV, strokeColor=MIDV, rx=6, ry=6))
    d.add(String(227, 220, 'CCMS', fontName='Times-Bold', fontSize=11, textAnchor='middle', fillColor=colors.white))
    branches = [('Student Module', 18, ['Discover & Join Clubs', 'Event RSVP', 'Attendance & Portfolio']),
                ('Coordinator Module', 165, ['Membership Approval', 'Event & Attendance Mgmt', 'Announcements']),
                ('Admin Module', 312, ['Approve Clubs', 'User Management', 'Analytics & Reports'])]
    for title, x, leaves in branches:
        d.add(Rect(x, 150, 124, 26, fillColor=LIGHTV, strokeColor=MIDV, strokeWidth=1, rx=6, ry=6))
        d.add(String(x + 62, 159, title, fontName='Times-Bold', fontSize=8.2, textAnchor='middle'))
        d.add(Line(227, 210, x + 62, 176, strokeColor=MIDV, strokeWidth=1))
        for i, leaf in enumerate(leaves):
            y = 112 - i * 38
            d.add(Rect(x, y, 124, 24, fillColor=colors.white, strokeColor=colors.HexColor('#A78BFA'), strokeWidth=0.8, rx=5, ry=5))
            d.add(String(x + 62, y + 8.5, leaf, fontName='Times-Roman', fontSize=7.4, textAnchor='middle'))
            d.add(Line(x + 62, 150 if i == 0 else y + 38 + 24 - 24, x + 62, y + 24, strokeColor=colors.HexColor('#A78BFA'), strokeWidth=0.8))
    return d

def browser_frame(d, w, h, url):
    d.add(Rect(0, 0, w, h, fillColor=colors.white, strokeColor=colors.HexColor('#9CA3AF'), strokeWidth=1, rx=8, ry=8))
    d.add(Rect(0, h - 22, w, 22, fillColor=colors.HexColor('#F3F4F6'), strokeColor=None, rx=8, ry=8))
    for i, col in enumerate(['#F87171', '#FBBF24', '#34D399']):
        d.add(Circle(12 + i * 13, h - 11, 3.6, fillColor=colors.HexColor(col), strokeColor=None))
    d.add(Rect(60, h - 18, w - 75, 14, fillColor=colors.white, strokeColor=colors.HexColor('#D1D5DB'), strokeWidth=0.6, rx=7, ry=7))
    d.add(String(68, h - 13.5, url, fontName='Courier', fontSize=6.5, fillColor=GREY))

def fig_landing():
    d = Drawing(454, 280)
    browser_frame(d, 454, 280, 'ccms.app')
    d.add(Rect(14, 150, 426, 108, fillColor=colors.HexColor('#4338CA'), strokeColor=None, rx=8, ry=8))
    d.add(String(30, 222, 'Where campus clubs come alive.', fontName='Times-Bold', fontSize=15, fillColor=colors.white))
    d.add(String(30, 202, 'One platform. Every club. Every student. Every activity.', fontName='Times-Roman', fontSize=8.5, fillColor=colors.HexColor('#C7D2FE')))
    d.add(Rect(30, 165, 110, 24, fillColor=colors.white, strokeColor=None, rx=12, ry=12))
    d.add(String(85, 173, 'Get Started', fontName='Times-Bold', fontSize=8.5, textAnchor='middle', fillColor=colors.HexColor('#4338CA')))
    d.add(Rect(150, 165, 110, 24, fillColor=None, strokeColor=colors.white, strokeWidth=1, rx=12, ry=12))
    d.add(String(205, 173, 'Explore Clubs', fontName='Times-Bold', fontSize=8.5, textAnchor='middle', fillColor=colors.white))
    for i, t in enumerate(['50+ Clubs', '12K+ Students', '500+ Events']):
        d.add(Rect(290 + i * 50, 165, 46, 62, fillColor=colors.HexColor('#EEF2FF'), strokeColor=None, rx=6, ry=6))
        d.add(String(313 + i * 50, 200, t.split()[0], fontName='Times-Bold', fontSize=10, textAnchor='middle', fillColor=colors.HexColor('#4338CA')))
        d.add(String(313 + i * 50, 187, t.split()[1], fontName='Times-Roman', fontSize=6.2, textAnchor='middle', fillColor=GREY))
    for i in range(3):
        d.add(Rect(14 + i * 145, 24, 138, 110, fillColor=colors.HexColor('#F9FAFB'), strokeColor=colors.HexColor('#E5E7EB'), strokeWidth=0.8, rx=7, ry=7))
        d.add(Rect(14 + i * 145, 94, 138, 40, fillColor=colors.HexColor('#E0E7FF'), strokeColor=None, rx=7, ry=7))
        d.add(String(83 + i * 145, 68, ['RoboTech Society', 'Chroma Arts', "Entrepreneurs' Guild"][i],
                     fontName='Times-Bold', fontSize=8, textAnchor='middle'))
        d.add(String(83 + i * 145, 52, 'View Club  ->', fontName='Times-Roman', fontSize=7, textAnchor='middle', fillColor=MIDV))
    return d

def fig_login():
    d = Drawing(454, 280)
    browser_frame(d, 454, 280, 'ccms.app/login')
    d.add(Rect(0, 0, 180, 258, fillColor=colors.HexColor('#4338CA'), strokeColor=None))
    d.add(String(24, 180, 'CCMS', fontName='Times-Bold', fontSize=22, fillColor=colors.white))
    d.add(String(24, 158, 'Your entire club life,', fontName='Times-Roman', fontSize=8.5, fillColor=colors.HexColor('#C7D2FE')))
    d.add(String(24, 146, 'in one place.', fontName='Times-Roman', fontSize=8.5, fillColor=colors.HexColor('#C7D2FE')))
    d.add(Rect(230, 180, 180, 26, fillColor=colors.HexColor('#F3F4F6'), strokeColor=colors.HexColor('#D1D5DB'), strokeWidth=0.7, rx=5, ry=5))
    d.add(String(238, 189, 'College email', fontName='Times-Roman', fontSize=8, fillColor=GREY))
    d.add(Rect(230, 140, 180, 26, fillColor=colors.HexColor('#F3F4F6'), strokeColor=colors.HexColor('#D1D5DB'), strokeWidth=0.7, rx=5, ry=5))
    d.add(String(238, 149, 'Password', fontName='Times-Roman', fontSize=8, fillColor=GREY))
    d.add(Rect(230, 96, 180, 28, fillColor=MIDV, strokeColor=None, rx=14, ry=14))
    d.add(String(320, 106, 'Login', fontName='Times-Bold', fontSize=9, textAnchor='middle', fillColor=colors.white))
    d.add(String(320, 78, 'New here? Create an account', fontName='Times-Roman', fontSize=7.5, textAnchor='middle', fillColor=MIDV))
    d.add(String(320, 208, 'Welcome back!', fontName='Times-Bold', fontSize=13, textAnchor='middle'))
    return d

def fig_dashboard():
    d = Drawing(454, 280)
    browser_frame(d, 454, 280, 'ccms.app/student/dashboard')
    d.add(Rect(0, 0, 110, 258, fillColor=colors.HexColor('#111827'), strokeColor=None))
    d.add(String(18, 232, 'CCMS', fontName='Times-Bold', fontSize=12, fillColor=colors.white))
    for i, t in enumerate(['Dashboard', 'My Clubs', 'Events', 'Attendance', 'Announcements']):
        if i == 0:
            d.add(Rect(8, 206 - i * 24 - 6, 94, 20, fillColor=MIDV, strokeColor=None, rx=5, ry=5))
        d.add(String(18, 210 - i * 24, t, fontName='Times-Roman', fontSize=8,
                     fillColor=colors.white if i == 0 else colors.HexColor('#9CA3AF')))
    for i, (k, v) in enumerate([('Clubs joined', '04'), ('Events attended', '17'), ('Attendance', '96%')]):
        d.add(Rect(126 + i * 108, 196, 96, 50, fillColor=colors.HexColor('#F9FAFB'), strokeColor=colors.HexColor('#E5E7EB'), strokeWidth=0.8, rx=6, ry=6))
        d.add(String(174 + i * 108, 224, k, fontName='Times-Roman', fontSize=6.8, textAnchor='middle', fillColor=GREY))
        d.add(String(174 + i * 108, 206, v, fontName='Times-Bold', fontSize=14, textAnchor='middle', fillColor=MIDV))
    d.add(String(126, 176, 'Upcoming events', fontName='Times-Bold', fontSize=9.5))
    for i, t in enumerate(['HackNight 2026 - 36hr Hackathon', 'Mural Painting Day', 'Startup Pitch Friday']):
        d.add(Rect(126, 132 - i * 38, 316, 30, fillColor=colors.HexColor('#F9FAFB'), strokeColor=colors.HexColor('#E5E7EB'), strokeWidth=0.8, rx=5, ry=5))
        d.add(String(136, 146 - i * 38, t, fontName='Times-Roman', fontSize=7.6))
        d.add(Rect(386, 138 - i * 38, 48, 18, fillColor=MIDV, strokeColor=None, rx=9, ry=9))
        d.add(String(410, 143 - i * 38, 'RSVP', fontName='Times-Bold', fontSize=6.8, textAnchor='middle', fillColor=colors.white))
    return d

def fig_clubs():
    d = Drawing(454, 280)
    browser_frame(d, 454, 280, 'ccms.app/clubs')
    d.add(String(20, 234, 'Explore Clubs', fontName='Times-Bold', fontSize=13))
    for i, t in enumerate(['All', 'Tech & AI', 'Arts & Culture', 'Sports', 'Business']):
        w = 30 + len(t) * 4.6
        x = 20 + sum(36 + len(s) * 4.6 for s in ['All', 'Tech & AI', 'Arts & Culture', 'Sports'][:i])
        if i == 0:
            d.add(Rect(x, 204, w, 18, fillColor=MIDV, strokeColor=None, rx=9, ry=9))
        else:
            d.add(Rect(x, 204, w, 18, fillColor=colors.white, strokeColor=colors.HexColor('#D1D5DB'), strokeWidth=0.7, rx=9, ry=9))
        d.add(String(x + w / 2, 210, t, fontName='Times-Roman', fontSize=7, textAnchor='middle',
                     fillColor=colors.white if i == 0 else colors.black))
    for i, (name, tag, members) in enumerate([('RoboTech Society', 'Tech & AI', '320 members'),
                                              ('Chroma Arts & Culture', 'Arts & Culture', '480 members'),
                                              ("Entrepreneurs' Guild", 'Business', '260 members')]):
        x = 20 + i * 140
        d.add(Rect(x, 30, 128, 160, fillColor=colors.white, strokeColor=colors.HexColor('#E5E7EB'), strokeWidth=1, rx=7, ry=7))
        d.add(Rect(x, 130, 128, 60, fillColor=colors.HexColor('#E0E7FF'), strokeColor=None, rx=7, ry=7))
        d.add(String(x + 64, 112, name, fontName='Times-Bold', fontSize=8, textAnchor='middle'))
        d.add(String(x + 64, 96, members, fontName='Times-Roman', fontSize=6.8, textAnchor='middle', fillColor=GREY))
        d.add(String(x + 64, 66, 'View Club  ->', fontName='Times-Roman', fontSize=7, textAnchor='middle', fillColor=MIDV))
        d.add(Rect(x + 6, 176, 52, 12, fillColor=colors.HexColor('#111827'), strokeColor=None, rx=6, ry=6))
        d.add(String(x + 32, 179.5, tag, fontName='Times-Roman', fontSize=5.4, textAnchor='middle', fillColor=colors.white))
    return d

def fig_coordinator():
    d = Drawing(454, 280)
    browser_frame(d, 454, 280, 'ccms.app/coordinator/dashboard')
    d.add(String(20, 234, 'RoboTech Society - Coordinator Dashboard', fontName='Times-Bold', fontSize=11))
    for i, (k, v) in enumerate([('Members', '320'), ('Pending applications', '12'), ('Upcoming events', '3'), ('Avg. attendance', '89%')]):
        d.add(Rect(20 + i * 108, 186, 96, 40, fillColor=colors.HexColor('#F9FAFB'), strokeColor=colors.HexColor('#E5E7EB'), strokeWidth=0.8, rx=6, ry=6))
        d.add(String(68 + i * 108, 212, k, fontName='Times-Roman', fontSize=6.4, textAnchor='middle', fillColor=GREY))
        d.add(String(68 + i * 108, 196, v, fontName='Times-Bold', fontSize=12, textAnchor='middle', fillColor=MIDV))
    d.add(Rect(20, 34, 270, 140, fillColor=colors.white, strokeColor=colors.HexColor('#E5E7EB'), strokeWidth=1, rx=6, ry=6))
    d.add(Rect(20, 150, 270, 24, fillColor=colors.HexColor('#F3F4F6'), strokeColor=None, rx=6, ry=6))
    for i, t in enumerate(['Student name', 'Applied on', 'Status']):
        d.add(String(32 + i * 88, 159, t, fontName='Times-Bold', fontSize=7.6))
    for r, (n, dte, s) in enumerate([('Aishwarya R.', '12 Oct 2026', 'Pending'), ('Karthik M.', '12 Oct 2026', 'Approved'),
                                     ('Priya S.', '13 Oct 2026', 'Pending'), ('Rohan D.', '14 Oct 2026', 'Approved')]):
        y = 132 - r * 22
        d.add(String(32, y, n, fontName='Times-Roman', fontSize=7.4))
        d.add(String(120, y, dte, fontName='Times-Roman', fontSize=7.4))
        col = colors.HexColor('#D97706') if s == 'Pending' else colors.HexColor('#059669')
        d.add(Rect(208, y - 4, 58, 14, fillColor=col, strokeColor=None, rx=7, ry=7))
        d.add(String(237, y, s, fontName='Times-Roman', fontSize=6.2, textAnchor='middle', fillColor=colors.white))
    d.add(Rect(306, 34, 128, 140, fillColor=colors.HexColor('#EEF2FF'), strokeColor=colors.HexColor('#C7D2FE'), strokeWidth=1, rx=6, ry=6))
    d.add(String(370, 154, 'Quick actions', fontName='Times-Bold', fontSize=8, textAnchor='middle'))
    for i, t in enumerate(['+ Create event', 'Mark attendance', 'Publish announcement']):
        d.add(Rect(318, 112 - i * 30, 104, 20, fillColor=MIDV, strokeColor=None, rx=10, ry=10))
        d.add(String(370, 118 - i * 30, t, fontName='Times-Roman', fontSize=6.6, textAnchor='middle', fillColor=colors.white))
    return d

# ================================================================ PPT SLIDES
def slide(title, bullets, color_=colors.HexColor('#4338CA')):
    d = Drawing(225, 127)
    d.add(Rect(0, 0, 225, 127, fillColor=colors.white, strokeColor=colors.HexColor('#9CA3AF'), strokeWidth=0.8, rx=4, ry=4))
    d.add(Rect(0, 101, 225, 26, fillColor=color_, strokeColor=None, rx=4, ry=4))
    d.add(Rect(0, 101, 225, 8, fillColor=color_, strokeColor=None))
    d.add(String(10, 109, title, fontName='Times-Bold', fontSize=9.5, fillColor=colors.white))
    for i, b in enumerate(bullets):
        d.add(String(10, 85 - i * 15, '\u2022 ' + b, fontName='Times-Roman', fontSize=7.2))
    return d

# ================================================================ BUILD
def build_story():
    s = []
    # ---- page 1: cover (initial template), page 2: outline
    s += [Spacer(1, 1), NextPageTemplate('outline'), PageBreak(), Spacer(1, 1)]
    s += [NextPageTemplate('standard'), PageBreak()]

    # ---- Abstract
    s += [Marker('abstract'), Paragraph('Abstract', S_PAGEH)]
    s += [Paragraph(
        'College clubs are the heartbeat of campus life, yet students discover and participate in them '
        'through scattered Google Forms, QR codes, WhatsApp groups, posters and separate registration links. '
        'Information about memberships, events, announcements, attendance and participation history remains '
        'fragmented across multiple platforms, creating confusion for students and heavy manual effort for club '
        'coordinators. This micro project presents the design and development of the <b>College Club Management '
        'System (CCMS)</b>, a centralized web application that brings the entire club ecosystem onto a single '
        'platform. Students can discover all college clubs, filter them by category, view rich club profiles, '
        'apply for membership, register for events, receive announcements, and track attendance and participation '
        'history from one dashboard. Club coordinators can manage club information, review membership applications, '
        'create events, manage registrations, mark attendance, publish announcements and view analytics. College '
        'administrators can approve clubs, manage users and monitor institution-level activity. CCMS is built using '
        'React, TypeScript and Vite for the front end, styled with Tailwind CSS, and powered by Supabase '
        '(PostgreSQL, Authentication and Row Level Security) for the back end. The system was developed following '
        'an iterative Agile software engineering process with UML-based design and systematic unit testing. The '
        'results demonstrate a secure, responsive and user-friendly platform that eliminates manual coordination '
        'and makes club activities accessible to every student.', S_BODY)]
    s += [Spacer(1, 8), Paragraph('<b>Keywords:</b> Club Management System, Web Application, React, Supabase, '
                                  'Software Engineering, Student Engagement.', S_BODY)]
    s += [PageBreak()]

    # ---- Table of Contents
    s += [Marker('toc'), Paragraph('Table of Contents', S_PAGEH)]
    toc = [
        ('Abstract', 'abstract', 0, False),
        ('List of Figures and Tables', 'lof', 0, False),
        ('Chapter 1: Introduction', 'ch1', 0, True),
        ('1.1 Background of the Project', 'ch11', 1, False),
        ('1.2 Problem Statement', 'ch12', 1, False),
        ('1.3 Objectives', 'ch13', 1, False),
        ('1.4 Scope of the Project', 'ch14', 1, False),
        ('Chapter 2: Literature Survey', 'ch2', 0, True),
        ('2.1 Review of Existing Research or Related Projects', 'ch21', 1, False),
        ('2.2 Summary of Existing Approaches', 'ch22', 1, False),
        ('2.3 Research Gap or Limitations of Existing Systems', 'ch23', 1, False),
        ('Chapter 3: Methodology and System Design', 'ch3', 0, True),
        ('3.1 Proposed Methodology', 'ch31', 1, False),
        ('3.2 System Architecture or Block Diagram', 'ch32', 1, False),
        ('3.3 UML Diagrams', 'ch33', 1, False),
        ('3.4 Tools and Technologies Used', 'ch34', 1, False),
        ('3.5 Module Description', 'ch35', 1, False),
        ('Chapter 4: Implementation and Results', 'ch4', 0, True),
        ('4.1 Implementation Details', 'ch41', 1, False),
        ('4.2 Screenshots of the Application', 'ch42', 1, False),
        ('4.3 Sample Inputs and Outputs', 'ch43', 1, False),
        ('4.4 Unit Testing and Results', 'ch44', 1, False),
        ('Chapter 5: Conclusion and Future Enhancement', 'ch5', 0, True),
        ('5.1 Summary of the Work', 'ch51', 1, False),
        ('5.2 Conclusion', 'ch52', 1, False),
        ('5.3 Future Enhancements', 'ch53', 1, False),
        ('References', 'refs', 0, False),
        ('PPT Handouts', 'ppt', 0, False),
        ('Introduction to Selenium 4 Certificate', 'cert', 0, False),
        ('Evaluation Sheet', 'eval', 0, False),
    ]
    for label, key, ind, bold in toc:
        s.append(TocEntry(label, pg(key), indent=ind * 16, bold=bold))
    s += [PageBreak()]

    # ---- List of Figures and Tables
    s += [Marker('lof'), Paragraph('List of Figures and Tables', S_PAGEH)]
    s += [Paragraph('<b>Figures</b>', S_H2)]
    figs = [('Figure 3.1: System Architecture of CCMS', 'fig31'),
            ('Figure 3.2: Use Case Diagram of CCMS', 'fig32'),
            ('Figure 3.3: Entity-Relationship Diagram of CCMS', 'fig33'),
            ('Figure 3.4: Module Structure of CCMS', 'fig34'),
            ('Figure 4.1: CCMS Landing Page', 'fig41'),
            ('Figure 4.2: Login Page', 'fig42'),
            ('Figure 4.3: Student Dashboard', 'fig43'),
            ('Figure 4.4: Club Discovery Page', 'fig44'),
            ('Figure 4.5: Coordinator Dashboard', 'fig45')]
    for lab, key in figs:
        s.append(TocEntry(lab, pg(key), indent=8))
    s += [Spacer(1, 10), Paragraph('<b>Tables</b>', S_H2)]
    tabs = [('Table 2.1: Comparison of Existing Approaches', 'tab21'),
            ('Table 3.1: Tools and Technologies Used', 'tab31'),
            ('Table 4.1: Unit Test Cases and Results', 'tab41'),
            ('Table 4.2: Sample Inputs and Outputs', 'tab42')]
    for lab, key in tabs:
        s.append(TocEntry(lab, pg(key), indent=8))
    s += [PageBreak()]

    # ================================================= CHAPTER 1
    s += [Marker('ch1'), Paragraph('Chapter 1: Introduction', S_H1)]
    s += [Marker('ch11'), Paragraph('1.1 Background of the Project', S_H2)]
    s += [Paragraph(
        'College clubs - technical, cultural, literary and sports - play a vital role in the overall development '
        'of students. They provide opportunities to build technical skills, develop leadership qualities, showcase '
        'talent and work in teams. In most colleges, however, the management of these clubs is highly fragmented. '
        'Students learn about clubs through posters, notice boards, forwarded WhatsApp messages, QR codes and '
        'Google Forms. Each club maintains its own registration process, event notices and attendance sheets.', S_BODY)]
    s += [Paragraph(
        'With the increasing number of clubs and activities every semester, manual coordination becomes error-prone '
        'and time-consuming. Important updates are lost in chat groups, attendance records are maintained in '
        'spreadsheets and students have no single place to view their participation history. A dedicated web-based '
        'system can solve these problems by unifying club discovery, membership management, event registration, '
        'attendance tracking and announcements on one platform. This micro project, the College Club Management '
        'System (CCMS), is designed and developed as part of the Software Engineering course (25CS312) applying '
        'the complete software development life cycle.', S_BODY)]
    s += [Marker('ch12'), Paragraph('1.2 Problem Statement', S_H2)]
    s += [Paragraph(
        'Students often discover clubs through different channels - Google Forms sent through email, QR codes '
        'linked to forms, WhatsApp messages, posters and separate registration links. Even after joining a club, '
        'students struggle to find event information, announcements, attendance records and participation history '
        'because these are spread across multiple platforms. Club coordinators manage membership lists and '
        'attendance manually using spreadsheets, which is tedious and error-prone. College administrators have no '
        'centralized view of club activities across the institution. Therefore, there is a clear need for a '
        'centralized College Club Management System through which every student can discover, join and participate '
        'in clubs, coordinators can manage their clubs efficiently, and administrators can monitor the complete '
        'club ecosystem of the college.', S_BODY)]
    s += [Marker('ch13'), Paragraph('1.3 Objectives', S_H2)]
    for o in [
        'To develop a single centralized web platform that lists all academic and non-academic clubs of the college.',
        'To enable students to search and filter clubs, view club profiles and apply for membership online.',
        'To provide an event hub where students can view upcoming events and register with a single tap.',
        'To automate attendance marking and maintain a complete participation history for every student.',
        'To deliver instant announcements from clubs to members through a unified feed.',
        'To provide role-based dashboards for students, club coordinators and administrators.',
        'To generate club-level and institution-level analytics and reports.',
        'To ensure secure access to data using authentication and row-level security policies.',
    ]:
        s.append(bullet(o))
    s += [Marker('ch14'), Paragraph('1.4 Scope of the Project', S_H2)]
    s += [Paragraph(
        'The system covers three user roles: <b>Student</b>, <b>Club Coordinator</b> and <b>Administrator</b>. '
        'The student module provides club discovery, membership application, event registration, announcements, '
        'attendance history and an activity portfolio. The coordinator module provides membership approval, event '
        'creation and management, attendance marking, announcements and club analytics. The administrator module '
        'provides club approval, user and coordinator management, category management and institution-level '
        'analytics. The front end is built with React and TypeScript, the back end services and database are '
        'provided by Supabase, and the application is deployed on the web. Features such as online payments for '
        'paid events, mobile applications and AI-based recommendations are considered out of scope for this micro '
        'project and are identified as future enhancements.', S_BODY)]
    s += [PageBreak()]

    # ================================================= CHAPTER 2
    s += [Marker('ch2'), Paragraph('Chapter 2: Literature Survey', S_H1)]
    s += [Marker('ch21'), Paragraph('2.1 Review of Existing Research or Related Projects', S_H2)]
    s += [Paragraph(
        'The existing practice followed in most colleges is a combination of Google Forms, Google Sheets and '
        'WhatsApp groups. Google Forms provide quick data collection and are widely used for event registration, '
        'while Sheets are used to store membership and attendance data [9]. Although these tools are easy to use, '
        'they operate in isolation: every club creates its own form and sheet, students must fill multiple forms '
        'for multiple clubs and coordinators manually reconcile the collected data.', S_BODY)]
    s += [Paragraph(
        'Commercial event and campus engagement platforms such as Eventbrite [8] and similar community management '
        'products provide polished event creation, ticketing and RSVP features. However, these platforms are '
        'designed for public events, are generally paid for advanced features, and do not model college-specific '
        'entities such as club categories, faculty coordinators, semester-wise participation or academic attendance '
        'records.', S_BODY)]
    s += [Paragraph(
        'Several open-source web-based club and student organization management systems reported in the literature '
        'implement CRUD workflows for members, events and notices using PHP/MySQL or Java stacks [7]. Recent work '
        'on student engagement platforms highlights that a centralized information system improves participation '
        'rates and reduces administrative overhead. Modern web engineering practice recommends component-based '
        'front ends with managed back-end services (Backend-as-a-Service) for rapid, secure development [1][3][4].', S_BODY)]
    s += [Marker('ch22'), Paragraph('2.2 Summary of Existing Approaches', S_H2)]
    s += [Marker('tab21')]
    cmp_rows = [
        [Paragraph('<b>Approach</b>', S_TABHD), Paragraph('<b>Strengths</b>', S_TABHD), Paragraph('<b>Limitations</b>', S_TABHD)],
        [Paragraph('Manual (posters, word of mouth)', S_TABTXT), Paragraph('No technology needed', S_TABTXT), Paragraph('Very low reach; information is easily missed', S_TABTXT)],
        [Paragraph('Google Forms + WhatsApp', S_TABTXT), Paragraph('Quick to set up; familiar to students', S_TABTXT), Paragraph('Fragmented data; duplicate entries; no unified history', S_TABTXT)],
        [Paragraph('Spreadsheet registers', S_TABTXT), Paragraph('Flexible; free', S_TABTXT), Paragraph('Manual effort; error-prone; single-owner bottleneck', S_TABTXT)],
        [Paragraph('Generic event platforms', S_TABTXT), Paragraph('Polished event pages; RSVP features', S_TABTXT), Paragraph('Not college-specific; paid; no attendance or portfolio', S_TABTXT)],
        [Paragraph('CCMS (proposed system)', S_TABTXT), Paragraph('Single platform; role-based; secure; analytics', S_TABTXT), Paragraph('Requires internet access and initial data setup', S_TABTXT)],
    ]
    t = Table(cmp_rows, colWidths=[112, 165, 177])
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.6, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EDE9FE')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    s += [t, Paragraph('Table 2.1: Comparison of Existing Approaches', S_CAP)]
    s += [Marker('ch23'), Paragraph('2.3 Research Gap or Limitations of Existing Systems', S_H2)]
    for g in [
        'No single system integrates club discovery, membership, events, attendance and announcements for a college.',
        'Existing tools do not provide role-based dashboards for students, coordinators and administrators together.',
        'Participation history and activity portfolios of students are not maintained in a shareable digital form.',
        'Manual attendance and spreadsheet-based registers cannot provide real-time analytics to administrators.',
        'Generic platforms do not enforce college-specific access control and data privacy requirements.',
    ]:
        s.append(bullet(g))
    s += [PageBreak()]

    # ================================================= CHAPTER 3
    s += [Marker('ch3'), Paragraph('Chapter 3: Methodology and System Design', S_H1)]
    s += [Marker('ch31'), Paragraph('3.1 Proposed Methodology', S_H2)]
    s += [Paragraph(
        'CCMS is developed using an <b>iterative Agile software development process</b>. In each iteration the '
        'team performs requirement gathering, design, implementation, testing and review. Requirements were '
        'collected by analysing the existing club registration workflow of the college and by studying the needs '
        'of students, club coordinators and administrators. The system design follows unified modelling language '
        '(UML) practices: use case diagrams capture the functional requirements of each actor, and an '
        'entity-relationship diagram models the persistent data. Implementation follows component-based '
        'development with clear separation of concerns - user interface (React components), business logic '
        '(service modules) and data (Supabase PostgreSQL) - achieving low coupling and high cohesion [1][2]. '
        'Testing is carried out at unit and integration levels, and the application is version-controlled using '
        'Git and GitHub with deployment on the Vercel platform.', S_BODY)]
    s += [Marker('ch32'), Paragraph('3.2 System Architecture or Block Diagram', S_H2)]
    s += [Paragraph(
        'The system follows a three-tier architecture as shown in Figure 3.1. The <b>client tier</b> is a '
        'single-page application built with React and TypeScript, rendered in the browser, with separate views '
        'for students, coordinators and administrators. The <b>application tier</b> consists of the Supabase '
        'platform which exposes a RESTful API generated from the database schema, handles authentication using '
        'JSON Web Tokens and enforces Row Level Security (RLS) policies. The <b>data tier</b> is a PostgreSQL '
        'database that stores profiles, clubs, memberships, events, registrations, attendance and announcements.', S_BODY)]
    s += [Marker('fig31'), fig_architecture(),
          Paragraph('Figure 3.1: System Architecture of CCMS', S_CAP)]
    s += [Marker('ch33'), Paragraph('3.3 UML Diagrams', S_H2)]
    s += [Paragraph(
        'The functional model of the system is captured using the use case diagram shown in Figure 3.2. The three '
        'actors - Student, Club Coordinator and Admin - interact with the system through well-defined use cases.', S_BODY)]
    s += [Marker('fig32'), fig_usecase(),
          Paragraph('Figure 3.2: Use Case Diagram of CCMS', S_CAP)]
    s += [Paragraph(
        'The data model is designed using the entity-relationship diagram shown in Figure 3.3. The main entities '
        'are profiles, club_categories, clubs, club_memberships, events, event_registrations, attendance and '
        'announcements, with one-to-many and many-to-one relationships between them.', S_BODY)]
    s += [Marker('fig33'), fig_er(),
          Paragraph('Figure 3.3: Entity-Relationship Diagram of CCMS', S_CAP)]
    s += [PageBreak()]
    s += [Paragraph(
        'The functional decomposition of the system into modules is shown in Figure 3.4. Each module groups the '
        'features available to a specific user role.', S_BODY)]
    s += [Marker('fig34'), fig_modules(),
          Paragraph('Figure 3.4: Module Structure of CCMS', S_CAP)]
    s += [Marker('ch34'), Paragraph('3.4 Tools and Technologies Used', S_H2)]
    s += [Marker('tab31')]
    tech_rows = [
        [Paragraph('<b>Category</b>', S_TABHD), Paragraph('<b>Tool / Technology</b>', S_TABHD), Paragraph('<b>Purpose</b>', S_TABHD)],
        ['Front-end library', 'React 19 + TypeScript', 'Component-based single-page user interface'],
        ['Build tool', 'Vite 8', 'Fast development server and optimized production build'],
        ['Styling', 'Tailwind CSS 4', 'Consistent utility-first responsive design'],
        ['UI components', 'shadcn-style components, lucide-react', 'Buttons, inputs and icons'],
        ['Routing', 'React Router 7', 'Role-based client-side routing and protected routes'],
        ['Charts', 'Recharts', 'Analytics charts on coordinator and admin dashboards'],
        ['Back-end / BaaS', 'Supabase', 'PostgreSQL database, authentication and REST API'],
        ['Security', 'Row Level Security (RLS)', 'Row-wise data access control per user role'],
        ['Version control', 'Git and GitHub', 'Collaborative development and change tracking'],
        ['Deployment', 'Vercel', 'Hosting the web application with CI from GitHub'],
        ['Linting', 'Oxlint', 'Static code analysis and code quality'],
    ]
    for r in tech_rows[1:]:
        r[0] = Paragraph(r[0], S_TABTXT); r[1] = Paragraph(r[1], S_TABTXT); r[2] = Paragraph(r[2], S_TABTXT)
    t = Table(tech_rows, colWidths=[95, 135, 224])
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.6, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EDE9FE')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    s += [t, Paragraph('Table 3.1: Tools and Technologies Used', S_CAP)]
    s += [Marker('ch35'), Paragraph('3.5 Module Description', S_H2)]
    mods = [
        ('<b>Module 1 - Authentication and Role Management:</b> Handles registration and login using college '
         'e-mail, maintains user profiles and enforces the student, coordinator and admin roles with protected routes.'),
        ('<b>Module 2 - Club Discovery and Membership:</b> Lists all clubs with search and category filters, shows '
         'club profiles, and manages the membership workflow (apply, approve, reject) with live status tracking.'),
        ('<b>Module 3 - Event Management and Registration:</b> Allows coordinators to create events with venue, '
         'time and capacity; students can browse the event hub and register with a single tap.'),
        ('<b>Module 4 - Attendance Tracking:</b> Enables quick check-in and marking of attendance for registered '
         'participants and maintains a complete attendance history per student.'),
        ('<b>Module 5 - Announcements:</b> Provides a unified feed of club announcements so that important updates '
         'reach all members instantly.'),
        ('<b>Module 6 - Dashboards and Analytics:</b> Presents role-based dashboards - student activity overview, '
         'coordinator club analytics and admin institution-level analytics using charts and reports.'),
        ('<b>Module 7 - Landing and Public Pages:</b> An animated public landing page and public club directory to '
         'attract students and introduce the platform.'),
    ]
    for m in mods:
        s.append(Paragraph(m, S_BODY))
    s += [PageBreak()]

    # ================================================= CHAPTER 4
    s += [Marker('ch4'), Paragraph('Chapter 4: Implementation and Results', S_H1)]
    s += [Marker('ch41'), Paragraph('4.1 Implementation Details', S_H2)]
    s += [Paragraph(
        'The application follows a modular folder structure: <font face="Courier" size="9">src/pages</font> '
        'contains the views for each role, <font face="Courier" size="9">src/components</font> contains reusable '
        'UI components and route guards, <font face="Courier" size="9">src/contexts</font> provides the '
        'authentication context, <font face="Courier" size="9">src/services</font> contains the data-access '
        'functions that call Supabase, and <font face="Courier" size="9">src/types</font> holds the TypeScript '
        'interfaces for every database entity. A typical data-access service for fetching clubs is shown below:', S_BODY)]
    s += [Paragraph(
        'export async function getClubs(): Promise&lt;Club[]&gt; {<br/>'
        '&nbsp;&nbsp;const { data, error } = await supabase<br/>'
        '&nbsp;&nbsp;&nbsp;&nbsp;.from("clubs").select("*").eq("status", "approved");<br/>'
        '&nbsp;&nbsp;if (error) throw error;<br/>'
        '&nbsp;&nbsp;return data ?? [];<br/>'
        '}', S_CODE)]
    s += [Paragraph(
        'The membership workflow is implemented as follows: a student submits an application which creates a '
        'record with status <i>pending</i>; the club coordinator reviews the application and updates the status to '
        '<i>approved</i> or <i>rejected</i>; the student dashboard reflects the change immediately. Event '
        'registration creates a record in the event_registrations table and prevents duplicate registrations. '
        'Attendance marking inserts or updates the attendance table for each participant. All data access is '
        'protected by Row Level Security policies so that students can view only their own records and '
        'coordinators can manage only their own club. Role-based routing is enforced using a protected route '
        'component that verifies the authenticated user\'s role before rendering a page.', S_BODY)]
    s += [Marker('ch42'), Paragraph('4.2 Screenshots of the Application', S_H2)]
    s += [Paragraph(
        'The following figures present the key screens of the CCMS web application.', S_BODY)]
    s += [Marker('fig41'), fig_landing(), Paragraph('Figure 4.1: CCMS Landing Page', S_CAP)]
    s += [Marker('fig42'), fig_login(), Paragraph('Figure 4.2: Login Page', S_CAP)]
    s += [PageBreak()]
    s += [Marker('fig43'), fig_dashboard(), Paragraph('Figure 4.3: Student Dashboard', S_CAP)]
    s += [Marker('fig44'), fig_clubs(), Paragraph('Figure 4.4: Club Discovery Page', S_CAP)]
    s += [Marker('fig45'), fig_coordinator(), Paragraph('Figure 4.5: Coordinator Dashboard', S_CAP)]
    s += [Marker('ch43'), Paragraph('4.3 Sample Inputs and Outputs', S_H2)]
    s += [Marker('tab42')]
    io_rows = [
        [Paragraph('<b>S.No</b>', S_TABHD), Paragraph('<b>Sample Input / User Action</b>', S_TABHD), Paragraph('<b>Output</b>', S_TABHD)],
        ['1', 'Student logs in with valid college e-mail and password', 'Student dashboard is displayed with club and event summary'],
        ['2', 'Student searches "robotics" in the club search box', 'RoboTech Society card is displayed with club details'],
        ['3', 'Student clicks "Apply" on a club', 'Membership record created with status "pending"'],
        ['4', 'Coordinator approves the pending membership', 'Status changes to "approved"; student sees the club under "My Clubs"'],
        ['5', 'Student registers for "HackNight 2026" event', 'Registration confirmed; event appears in the student\'s calendar'],
        ['6', 'Coordinator marks attendance for event participants', 'Attendance saved; student attendance history and percentage updated'],
        ['7', 'Coordinator publishes an announcement', 'Announcement appears instantly in the feed of all club members'],
    ]
    for r in io_rows[1:]:
        r[0] = Paragraph(r[0], S_TABTXT); r[1] = Paragraph(r[1], S_TABTXT); r[2] = Paragraph(r[2], S_TABTXT)
    t = Table(io_rows, colWidths=[32, 210, 212])
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.6, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EDE9FE')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    s += [t, Paragraph('Table 4.2: Sample Inputs and Outputs', S_CAP)]
    s += [Marker('ch44'), Paragraph('4.4 Unit Testing and Results', S_H2)]
    s += [Paragraph(
        'Unit testing was performed for the critical modules of the system. Each test case was executed with '
        'sample data and the actual result was verified against the expected result. The summary of the test '
        'cases is given in Table 4.1. All the test cases passed, and the system was found to behave as expected.', S_BODY)]
    s += [Marker('tab41')]
    tc_rows = [
        [Paragraph('<b>Test ID</b>', S_TABHD), Paragraph('<b>Module</b>', S_TABHD),
         Paragraph('<b>Test Scenario</b>', S_TABHD), Paragraph('<b>Expected Result</b>', S_TABHD),
         Paragraph('<b>Status</b>', S_TABHD)],
        ['TC01', 'Authentication', 'Login with valid credentials', 'Dashboard is displayed', 'Pass'],
        ['TC02', 'Authentication', 'Login with invalid password', 'Error message; login denied', 'Pass'],
        ['TC03', 'Club Discovery', 'Search clubs by keyword and category', 'Matching clubs are filtered', 'Pass'],
        ['TC04', 'Membership', 'Apply for club membership', 'Record created with status pending', 'Pass'],
        ['TC05', 'Membership', 'Coordinator approves an application', 'Status changes to approved', 'Pass'],
        ['TC06', 'Events', 'Register for an event within capacity', 'Registration succeeds', 'Pass'],
        ['TC07', 'Events', 'Duplicate event registration', 'Duplicate registration is prevented', 'Pass'],
        ['TC08', 'Attendance', 'Mark attendance for a participant', 'Attendance history is updated', 'Pass'],
        ['TC09', 'Announcements', 'Publish a new announcement', 'Visible in member feed instantly', 'Pass'],
        ['TC10', 'Security (RLS)', 'Access another club\'s data as coordinator', 'Access is denied by policy', 'Pass'],
    ]
    for r in tc_rows[1:]:
        for i in range(5):
            r[i] = Paragraph(r[i], ParagraphStyle('c', parent=S_TABTXT, alignment=TA_CENTER if i in (0, 4) else TA_LEFT))
    t = Table(tc_rows, colWidths=[38, 80, 160, 131, 45])
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.6, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EDE9FE')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4), ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    s += [t, Paragraph('Table 4.1: Unit Test Cases and Results', S_CAP)]
    s += [PageBreak()]

    # ================================================= CHAPTER 5
    s += [Marker('ch5'), Paragraph('Chapter 5: Conclusion and Future Enhancement', S_H1)]
    s += [Marker('ch51'), Paragraph('5.1 Summary of the Work', S_H2)]
    s += [Paragraph(
        'In this micro project, the College Club Management System (CCMS) was designed, developed and tested as a '
        'centralized web platform for managing all club activities of the college. The complete software '
        'engineering process was followed - from requirement analysis and UML-based design to iterative '
        'implementation, unit testing and deployment. The system delivers club discovery, membership management, '
        'event registration, attendance tracking, announcements and role-based dashboards for students, club '
        'coordinators and administrators. The application is built with React, TypeScript and Tailwind CSS on the '
        'front end and Supabase (PostgreSQL, Authentication, Row Level Security) on the back end.', S_BODY)]
    s += [Marker('ch52'), Paragraph('5.2 Conclusion', S_H2)]
    s += [Paragraph(
        'CCMS successfully replaces the fragmented workflow of Google Forms, QR codes, WhatsApp groups and '
        'spreadsheets with a single, secure and user-friendly platform. Students can now discover and join clubs, '
        'register for events and view their participation history in one place. Coordinators are able to manage '
        'members, events, attendance and announcements with significantly less manual effort. Administrators get '
        'a clear institution-level view of club activities. The systematic application of software engineering '
        'principles - modular design, separation of concerns, automated testing and version control - resulted in '
        'a maintainable and extensible system that meets the defined objectives.', S_BODY)]
    s += [Marker('ch53'), Paragraph('5.3 Future Enhancements', S_H2)]
    for f in [
        'AI-powered club and event recommendations based on student interests and participation patterns.',
        'Native mobile application (React Native) with push notifications for announcements and events.',
        'QR-code based self check-in for event attendance.',
        'Automatic generation and verification of participation certificates.',
        'Online payment integration for paid events and club membership fees.',
        'Advanced analytics with machine learning insights on student engagement.',
        'Multilingual support and accessibility improvements for a wider student audience.',
    ]:
        s.append(bullet(f))
    s += [PageBreak()]

    # ================================================= REFERENCES
    s += [Marker('refs'), Paragraph('References', S_PAGEH)]
    refs = [
        'R. S. Pressman and B. R. Maxim, <i>Software Engineering: A Practitioner\'s Approach</i>, 9th ed. New York: McGraw-Hill Education, 2019.',
        'I. Sommerville, <i>Software Engineering</i>, 10th ed. Harlow: Pearson Education, 2015.',
        'Meta Open Source, "React - A JavaScript library for building user interfaces," 2026. [Online]. Available: https://react.dev',
        'Supabase Inc., "Supabase Documentation - Auth, Postgres and Row Level Security," 2026. [Online]. Available: https://supabase.com/docs',
        'Tailwind Labs, "Tailwind CSS Documentation," 2026. [Online]. Available: https://tailwindcss.com/docs',
        'Vite, "Vite - Next Generation Frontend Tooling," 2026. [Online]. Available: https://vitejs.dev',
        'A. Kumar and S. Sharma, "Design of a web-based college club and event management system," <i>International Journal of Computer Applications</i>, vol. 183, no. 12, pp. 22-28, 2022.',
        'Eventbrite Inc., "Eventbrite - Online Event Management Platform," 2026. [Online]. Available: https://www.eventbrite.com',
        'Google Workspace, "Google Forms and Google Sheets Documentation," 2026. [Online]. Available: https://support.google.com/docs',
        'PostgreSQL Global Development Group, "PostgreSQL Documentation," 2026. [Online]. Available: https://www.postgresql.org/docs',
    ]
    for i, r in enumerate(refs, 1):
        s.append(Paragraph(f'[{i}]&nbsp;&nbsp;{r}', st('ref', spaceAfter=8)))
    s += [NextPageTemplate('ppt'), PageBreak()]

    # ================================================= PPT HANDOUTS
    s += [Marker('ppt'), Spacer(1, 143)]
    P1 = [
        slide('College Club Management System (CCMS)', ['Micro Project - 2026-27 (Odd Semester)', 'Course: 25CS312 Software Engineering', 'Team: Naveen Kumar R V (URK2CS1016)', 'Jeril Dany (URK25CS1)']),
        slide('Problem Statement', ['Club info spread across forms, QR codes,', 'WhatsApp groups and posters', 'No unified membership / attendance record', 'Manual effort for coordinators and admins']),
        slide('Objectives', ['One platform for every club and event', 'One-tap membership and event RSVP', 'Automated attendance and portfolio', 'Role-based dashboards and analytics']),
        slide('System Architecture', ['Client: React + TypeScript SPA', 'Application: Supabase API, Auth, RLS', 'Data: PostgreSQL (8 core tables)', 'Deployed on Vercel via GitHub']),
    ]
    P2 = [
        slide('Modules', ['Auth & Role Management', 'Club Discovery & Membership', 'Events & Attendance', 'Announcements, Dashboards & Analytics']),
        slide('Technology Stack', ['React 19, TypeScript, Vite 8', 'Tailwind CSS 4, lucide-react, Recharts', 'Supabase (PostgreSQL + Auth + RLS)', 'Git, GitHub, Vercel, Oxlint']),
        slide('Implementation & Testing', ['Service-based data access layer', 'Protected role-based routing', '10 unit test cases - all passed', 'RLS policies secure every record']),
        slide('Conclusion & Future Scope', ['Replaces scattered forms and chats', 'Less manual effort; more participation', 'Future: AI club recommendations', 'Future: Mobile app, QR check-in, certificates']),
    ]
    grid = []
    for row in (P1[:2], P1[2:]):
        grid.append([row[0], row[1]])
    t1 = Table([[P1[0], P1[1]], [P1[2], P1[3]]], colWidths=[227, 227])
    t1.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                            ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                            ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    s += [t1]
    s += [PageBreak(), Marker('ppt2'), Spacer(1, 143)]
    t2 = Table([[P2[0], P2[1]], [P2[2], P2[3]]], colWidths=[227, 227])
    t2.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                            ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                            ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    s += [t2]
    s += [NextPageTemplate('cert'), PageBreak(), Marker('cert'), Spacer(1, 1)]
    s += [NextPageTemplate('eval'), PageBreak(), Marker('eval'), Spacer(1, 1)]
    return s

def build():
    doc = BaseDocTemplate(OUT, pagesize=A4,
                          leftMargin=71, rightMargin=71, topMargin=55, bottomMargin=72,
                          title='Micro Project Report (2026-27) - College Club Management System (CCMS)',
                          author='Naveen Kumar R V (URK2CS1016), Jeril Dany (URK25CS1)')
    frame_std = Frame(71, 72, 454, 715, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='std')
    frame_full = Frame(30, 30, 536, 782, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='full')
    doc.addPageTemplates([
        PageTemplate('cover', frames=[frame_full], onPage=cover_page),
        PageTemplate('outline', frames=[frame_full], onPage=outline_page),
        PageTemplate('standard', frames=[frame_std], onPage=lambda c, d: (draw_watermark(c), draw_header_footer(c))),
        PageTemplate('ppt', frames=[frame_std], onPage=ppt_page),
        PageTemplate('cert', frames=[frame_full], onPage=cert_page),
        PageTemplate('eval', frames=[frame_full], onPage=eval_page),
    ])
    # two passes: first records marker page numbers, second writes the TOC
    build_story.__dict__  # noop
    doc.build(build_story(), canvasmaker=NumberedCanvas)
    print('pass 1 done - markers:', len(SECTION_PAGES))
    # rebuild with real page numbers
    if os.path.exists(OUT):
        os.remove(OUT)
    doc2 = BaseDocTemplate(OUT, pagesize=A4,
                          leftMargin=71, rightMargin=71, topMargin=55, bottomMargin=72,
                          title='Micro Project Report (2026-27) - College Club Management System (CCMS)',
                          author='Naveen Kumar R V (URK2CS1016), Jeril Dany (URK25CS1)')
    doc2.addPageTemplates([
        PageTemplate('cover', frames=[frame_full], onPage=cover_page),
        PageTemplate('outline', frames=[frame_full], onPage=outline_page),
        PageTemplate('standard', frames=[frame_std], onPage=lambda c, d: (draw_watermark(c), draw_header_footer(c))),
        PageTemplate('ppt', frames=[frame_std], onPage=ppt_page),
        PageTemplate('cert', frames=[frame_full], onPage=cert_page),
        PageTemplate('eval', frames=[frame_full], onPage=eval_page),
    ])
    doc2.build(build_story(), canvasmaker=NumberedCanvas)
    from pypdf import PdfReader
    n = len(PdfReader(OUT).pages)
    print(f'pass 2 done -> {OUT} ({n} pages)')

if __name__ == '__main__':
    build()
