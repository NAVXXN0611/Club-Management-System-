import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.graphics.shapes import (
    Drawing, Rect, String, Line, Circle, Polygon, Group
)

def create_uml_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Brand Colors
    C_DEEP = colors.HexColor("#4C2365")
    C_MID = colors.HexColor("#7F5D99")
    C_LIGHT = colors.HexColor("#9E7EB5")
    C_PALE = colors.HexColor("#C4A4DA")
    C_CREAM = colors.HexColor("#F5F0FA")
    C_DARK = colors.HexColor("#1A0A28")
    C_MUTED = colors.HexColor("#3D2558")
    C_WHITE = colors.white
    C_BORDER = colors.HexColor("#D4B8E8")
    C_GREEN = colors.HexColor("#059669")
    C_RED = colors.HexColor("#DC2626")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=C_DEEP,
        alignment=1,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=C_MID,
        alignment=1,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=C_DEEP,
        spaceBefore=6,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=C_DARK,
        spaceAfter=6
    )

    cell_style = ParagraphStyle(
        'Cell_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=C_DARK
    )

    cell_bold = ParagraphStyle(
        'Cell_Bold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10.5,
        textColor=C_DARK
    )

    cell_header = ParagraphStyle(
        'Cell_Header',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=C_WHITE
    )

    meta_style = ParagraphStyle(
        'Meta_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=C_MUTED,
        alignment=1
    )

    story = []

    # ==========================================
    # PAGE 1: USE CASE DIAGRAM
    # ==========================================
    story.append(Paragraph("College Club Management System (CCMS)", title_style))
    story.append(Paragraph("IA3 Software Engineering Milestone — UML System Design Specification", subtitle_style))
    
    meta_table_data = [
        [
            Paragraph("<b>Version:</b> 1.0.0", meta_style),
            Paragraph("<b>Standard:</b> UML 2.5 / IEEE 830", meta_style),
            Paragraph("<b>Date:</b> November 2026", meta_style),
            Paragraph("<b>Target System:</b> Web / Cloud", meta_style)
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[135, 135, 135, 135])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CREAM),
        ('BOX', (0,0), (-1,-1), 1, C_PALE),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Use Case Diagram", h1_style))
    story.append(Paragraph(
        "<b>Description:</b> Illustrates system actors (Guest, Student, Coordinator, Admin), the system boundary, "
        "and interactions with the core functional use cases.", body_style
    ))

    # Drawing Use Case Diagram
    d1 = Drawing(540, 230)
    d1.add(Rect(130, 8, 280, 215, fillColor=C_CREAM, strokeColor=C_MID, strokeWidth=1.5, rx=6, ry=6))
    d1.add(String(140, 208, "System Boundary: CCMS Core Platform", fontName="Helvetica-Bold", fontSize=8.5, fillColor=C_DEEP))

    # Student Actor
    d1.add(Circle(45, 185, 9, fillColor=C_PALE, strokeColor=C_DEEP, strokeWidth=1))
    d1.add(Line(45, 176, 45, 153, strokeColor=C_DEEP, strokeWidth=1.5))
    d1.add(Line(32, 166, 58, 166, strokeColor=C_DEEP, strokeWidth=1.5))
    d1.add(Line(45, 153, 34, 135, strokeColor=C_DEEP, strokeWidth=1.5))
    d1.add(Line(45, 153, 56, 135, strokeColor=C_DEEP, strokeWidth=1.5))
    d1.add(String(27, 123, "Student", fontName="Helvetica-Bold", fontSize=8.5, fillColor=C_DEEP))

    # Guest Actor
    d1.add(Circle(45, 75, 9, fillColor=C_WHITE, strokeColor=C_MID, strokeWidth=1))
    d1.add(Line(45, 66, 45, 43, strokeColor=C_MID, strokeWidth=1.5))
    d1.add(Line(32, 56, 58, 56, strokeColor=C_MID, strokeWidth=1.5))
    d1.add(Line(45, 43, 34, 25, strokeColor=C_MID, strokeWidth=1.5))
    d1.add(Line(45, 43, 56, 25, strokeColor=C_MID, strokeWidth=1.5))
    d1.add(String(30, 13, "Guest", fontName="Helvetica-Bold", fontSize=8.5, fillColor=C_MID))

    # Coordinator Actor
    d1.add(Circle(495, 185, 9, fillColor=C_PALE, strokeColor=C_DEEP, strokeWidth=1))
    d1.add(Line(495, 176, 495, 153, strokeColor=C_DEEP, strokeWidth=1.5))
    d1.add(Line(482, 166, 508, 166, strokeColor=C_DEEP, strokeWidth=1.5))
    d1.add(Line(495, 153, 484, 135, strokeColor=C_DEEP, strokeWidth=1.5))
    d1.add(Line(495, 153, 506, 135, strokeColor=C_DEEP, strokeWidth=1.5))
    d1.add(String(468, 123, "Coordinator", fontName="Helvetica-Bold", fontSize=8.5, fillColor=C_DEEP))

    # Admin Actor
    d1.add(Circle(495, 75, 9, fillColor=colors.HexColor("#FDE68A"), strokeColor=colors.HexColor("#D97706"), strokeWidth=1))
    d1.add(Line(495, 66, 495, 43, strokeColor=colors.HexColor("#D97706"), strokeWidth=1.5))
    d1.add(Line(482, 56, 508, 56, strokeColor=colors.HexColor("#D97706"), strokeWidth=1.5))
    d1.add(Line(495, 43, 484, 25, strokeColor=colors.HexColor("#D97706"), strokeWidth=1.5))
    d1.add(Line(495, 43, 506, 25, strokeColor=colors.HexColor("#D97706"), strokeWidth=1.5))
    d1.add(String(478, 13, "Admin", fontName="Helvetica-Bold", fontSize=8.5, fillColor=colors.HexColor("#D97706")))

    # Use Case Boxes
    ucs = [
        (145, 180, 120, 20, "UC-01: Auth & Signup"),
        (145, 152, 120, 20, "UC-02: Browse Clubs"),
        (145, 124, 120, 20, "UC-03: Join Club"),
        (145, 96,  120, 20, "UC-04: RSVP Event"),
        (145, 68,  120, 20, "UC-05: Attendance View"),
        (275, 180, 125, 20, "UC-06: Review Member"),
        (275, 152, 125, 20, "UC-07: Schedule Event"),
        (275, 124, 125, 20, "UC-08: Mark Attendance"),
        (275, 96,  125, 20, "UC-09: Announcements"),
        (275, 68,  125, 20, "UC-10: Create Club"),
        (210, 40,  120, 20, "UC-11: Appoint Coord"),
    ]

    for (x, y, w, h, label) in ucs:
        d1.add(Rect(x, y, w, h, fillColor=C_WHITE, strokeColor=C_MID, strokeWidth=1, rx=7, ry=7))
        d1.add(String(x+8, y+6, label, fontName="Helvetica-Bold", fontSize=7, fillColor=C_DARK))

    # Connectors
    # Student
    d1.add(Line(60, 150, 145, 190, strokeColor=C_DEEP, strokeWidth=0.8))
    d1.add(Line(60, 150, 145, 162, strokeColor=C_DEEP, strokeWidth=0.8))
    d1.add(Line(60, 150, 145, 134, strokeColor=C_DEEP, strokeWidth=0.8))
    d1.add(Line(60, 150, 145, 106, strokeColor=C_DEEP, strokeWidth=0.8))
    d1.add(Line(60, 150, 145, 78,  strokeColor=C_DEEP, strokeWidth=0.8))

    # Guest
    d1.add(Line(60, 45, 145, 190, strokeColor=C_MID, strokeWidth=0.8))
    d1.add(Line(60, 45, 145, 162, strokeColor=C_MID, strokeWidth=0.8))

    # Coordinator
    d1.add(Line(480, 150, 400, 190, strokeColor=C_DEEP, strokeWidth=0.8))
    d1.add(Line(480, 150, 400, 162, strokeColor=C_DEEP, strokeWidth=0.8))
    d1.add(Line(480, 150, 400, 134, strokeColor=C_DEEP, strokeWidth=0.8))
    d1.add(Line(480, 150, 400, 106, strokeColor=C_DEEP, strokeWidth=0.8))

    # Admin
    d1.add(Line(480, 45, 400, 78, strokeColor=colors.HexColor("#D97706"), strokeWidth=0.8))
    d1.add(Line(480, 45, 330, 50, strokeColor=colors.HexColor("#D97706"), strokeWidth=0.8))
    d1.add(Line(480, 45, 400, 162, strokeColor=colors.HexColor("#D97706"), strokeWidth=0.8))

    story.append(d1)
    story.append(Spacer(1, 8))

    # Use Case Table with Paragraph wrapping
    uc_table_data = [
        [
            Paragraph("Actor", cell_header),
            Paragraph("Accessible Core Use Cases", cell_header),
            Paragraph("Security & System Permissions", cell_header)
        ],
        [
            Paragraph("<b>Student</b>", cell_style),
            Paragraph("UC-01 (Auth), UC-02 (Browse), UC-03 (Join), UC-04 (RSVP), UC-05 (Attendance)", cell_style),
            Paragraph("Restricted strictly to personal profile and owned club/event registrations.", cell_style)
        ],
        [
            Paragraph("<b>Coordinator</b>", cell_style),
            Paragraph("UC-06 (Review Members), UC-07 (Events), UC-08 (Attendance), UC-09 (Announcements)", cell_style),
            Paragraph("Elevated permissions scoped strictly to assigned club ID via PostgreSQL RLS.", cell_style)
        ],
        [
            Paragraph("<b>Admin</b>", cell_style),
            Paragraph("UC-10 (Create Club), UC-11 (Appoint Coordinator), UC-12 (Analytics & Audit)", cell_style),
            Paragraph("Global platform superuser; manages categories, clubs, coordinators, and roles.", cell_style)
        ]
    ]
    t1 = Table(uc_table_data, colWidths=[80, 225, 235])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_DEEP),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_CREAM]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t1)

    story.append(PageBreak())

    # ==========================================
    # PAGE 2: CLASS DIAGRAM
    # ==========================================
    story.append(Paragraph("2. Class Diagram", h1_style))
    story.append(Paragraph(
        "<b>Description:</b> Defines the structural domain model, representing entities, attributes, data types, "
        "operations, associations, and multiplicity constraints across the database and application layers.", body_style
    ))

    # Drawing Class Diagram
    d2 = Drawing(540, 310)

    # Box 1: Profile
    d2.add(Rect(15, 175, 120, 125, fillColor=C_CREAM, strokeColor=C_DEEP, strokeWidth=1, rx=3, ry=3))
    d2.add(Rect(15, 280, 120, 20, fillColor=C_DEEP, strokeColor=C_DEEP, strokeWidth=1))
    d2.add(String(50, 286, "Profile", fontName="Helvetica-Bold", fontSize=9, fillColor=C_WHITE))
    d2.add(String(20, 268, "+ UUID id [PK]", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(String(20, 256, "+ String full_name", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(String(20, 244, "+ String email", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(String(20, 232, "+ String role", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(String(20, 220, "+ String department", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(Line(15, 212, 135, 212, strokeColor=C_BORDER, strokeWidth=0.5))
    d2.add(String(20, 200, "+ updateProfile()", fontName="Helvetica-Oblique", fontSize=7, fillColor=C_DARK))
    d2.add(String(20, 188, "+ getAttendance()", fontName="Helvetica-Oblique", fontSize=7, fillColor=C_DARK))

    # Box 2: ClubCategory
    d2.add(Rect(210, 235, 120, 65, fillColor=C_CREAM, strokeColor=C_MID, strokeWidth=1, rx=3, ry=3))
    d2.add(Rect(210, 280, 120, 20, fillColor=C_MID, strokeColor=C_MID, strokeWidth=1))
    d2.add(String(235, 286, "ClubCategory", fontName="Helvetica-Bold", fontSize=9, fillColor=C_WHITE))
    d2.add(String(215, 268, "+ UUID id [PK]", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(String(215, 256, "+ String name", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(Line(210, 250, 330, 250, strokeColor=C_BORDER, strokeWidth=0.5))
    d2.add(String(215, 240, "+ getClubs()", fontName="Helvetica-Oblique", fontSize=7, fillColor=C_DARK))

    # Box 3: Club
    d2.add(Rect(405, 175, 120, 125, fillColor=C_CREAM, strokeColor=C_DEEP, strokeWidth=1, rx=3, ry=3))
    d2.add(Rect(405, 280, 120, 20, fillColor=C_DEEP, strokeColor=C_DEEP, strokeWidth=1))
    d2.add(String(450, 286, "Club", fontName="Helvetica-Bold", fontSize=9, fillColor=C_WHITE))
    d2.add(String(410, 268, "+ UUID id [PK]", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(String(410, 256, "+ String name", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(String(410, 244, "+ String slug [UQ]", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(String(410, 232, "+ UUID category_id", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(String(410, 220, "+ String contact_email", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(Line(405, 212, 525, 212, strokeColor=C_BORDER, strokeWidth=0.5))
    d2.add(String(410, 200, "+ getMembers()", fontName="Helvetica-Oblique", fontSize=7, fillColor=C_DARK))
    d2.add(String(410, 188, "+ getEvents()", fontName="Helvetica-Oblique", fontSize=7, fillColor=C_DARK))

    # Box 4: ClubMembership
    d2.add(Rect(210, 135, 120, 85, fillColor=C_CREAM, strokeColor=C_MID, strokeWidth=1, rx=3, ry=3))
    d2.add(Rect(210, 200, 120, 20, fillColor=C_MID, strokeColor=C_MID, strokeWidth=1))
    d2.add(String(225, 206, "ClubMembership", fontName="Helvetica-Bold", fontSize=8.5, fillColor=C_WHITE))
    d2.add(String(215, 188, "+ UUID club_id [FK]", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(String(215, 176, "+ UUID student_id [FK]", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(String(215, 164, "+ String status", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(Line(210, 156, 330, 156, strokeColor=C_BORDER, strokeWidth=0.5))
    d2.add(String(215, 144, "+ approve() / reject()", fontName="Helvetica-Oblique", fontSize=7, fillColor=C_DARK))

    # Box 5: Event
    d2.add(Rect(405, 15, 120, 115, fillColor=C_CREAM, strokeColor=C_DEEP, strokeWidth=1, rx=3, ry=3))
    d2.add(Rect(405, 110, 120, 20, fillColor=C_DEEP, strokeColor=C_DEEP, strokeWidth=1))
    d2.add(String(450, 116, "Event", fontName="Helvetica-Bold", fontSize=9, fillColor=C_WHITE))
    d2.add(String(410, 98, "+ UUID id [PK]", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(String(410, 86, "+ UUID club_id [FK]", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(String(410, 74, "+ String title", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(String(410, 62, "+ Date event_date", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(String(410, 50, "+ Integer capacity", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(Line(405, 42, 525, 42, strokeColor=C_BORDER, strokeWidth=0.5))
    d2.add(String(410, 30, "+ isFull() : Boolean", fontName="Helvetica-Oblique", fontSize=7, fillColor=C_DARK))
    d2.add(String(410, 20, "+ getAttendees()", fontName="Helvetica-Oblique", fontSize=7, fillColor=C_DARK))

    # Box 6: EventRegistration
    d2.add(Rect(210, 15, 120, 85, fillColor=C_CREAM, strokeColor=C_MID, strokeWidth=1, rx=3, ry=3))
    d2.add(Rect(210, 80, 120, 20, fillColor=C_MID, strokeColor=C_MID, strokeWidth=1))
    d2.add(String(220, 86, "EventRegistration", fontName="Helvetica-Bold", fontSize=8.5, fillColor=C_WHITE))
    d2.add(String(215, 68, "+ UUID event_id [FK]", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(String(215, 56, "+ UUID student_id [FK]", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(String(215, 44, "+ Date registered_at", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(Line(210, 36, 330, 36, strokeColor=C_BORDER, strokeWidth=0.5))
    d2.add(String(215, 24, "+ cancelRegistration()", fontName="Helvetica-Oblique", fontSize=7, fillColor=C_DARK))

    # Box 7: Attendance
    d2.add(Rect(15, 15, 120, 85, fillColor=C_CREAM, strokeColor=C_DEEP, strokeWidth=1, rx=3, ry=3))
    d2.add(Rect(15, 80, 120, 20, fillColor=C_DEEP, strokeColor=C_DEEP, strokeWidth=1))
    d2.add(String(45, 86, "Attendance", fontName="Helvetica-Bold", fontSize=9, fillColor=C_WHITE))
    d2.add(String(20, 68, "+ UUID event_id [FK]", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(String(20, 56, "+ UUID student_id [FK]", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(String(20, 44, "+ String status", fontName="Helvetica", fontSize=7, fillColor=C_DARK))
    d2.add(Line(15, 36, 135, 36, strokeColor=C_BORDER, strokeWidth=0.5))
    d2.add(String(20, 24, "+ updateStatus()", fontName="Helvetica-Oblique", fontSize=7, fillColor=C_DARK))

    # Relationship connectors
    # Category to Club
    d2.add(Line(330, 260, 405, 260, strokeColor=C_DEEP, strokeWidth=1))
    d2.add(String(335, 264, "1", fontName="Helvetica-Bold", fontSize=7, fillColor=C_DEEP))
    d2.add(String(390, 264, "0..*", fontName="Helvetica-Bold", fontSize=7, fillColor=C_DEEP))

    # Profile to Membership
    d2.add(Line(135, 220, 210, 190, strokeColor=C_DEEP, strokeWidth=1))
    d2.add(String(140, 218, "1", fontName="Helvetica-Bold", fontSize=7, fillColor=C_DEEP))
    d2.add(String(195, 195, "0..*", fontName="Helvetica-Bold", fontSize=7, fillColor=C_DEEP))

    # Club to Membership
    d2.add(Line(405, 220, 330, 190, strokeColor=C_DEEP, strokeWidth=1))
    d2.add(String(390, 218, "1", fontName="Helvetica-Bold", fontSize=7, fillColor=C_DEEP))
    d2.add(String(340, 195, "0..*", fontName="Helvetica-Bold", fontSize=7, fillColor=C_DEEP))

    # Club to Event (Composition)
    d2.add(Line(465, 175, 465, 130, strokeColor=C_DEEP, strokeWidth=1.2))
    d2.add(String(470, 160, "1", fontName="Helvetica-Bold", fontSize=7, fillColor=C_DEEP))
    d2.add(String(470, 135, "0..*", fontName="Helvetica-Bold", fontSize=7, fillColor=C_DEEP))

    # Event to EventRegistration
    d2.add(Line(405, 60, 330, 60, strokeColor=C_DEEP, strokeWidth=1))
    d2.add(String(390, 64, "1", fontName="Helvetica-Bold", fontSize=7, fillColor=C_DEEP))
    d2.add(String(340, 64, "0..*", fontName="Helvetica-Bold", fontSize=7, fillColor=C_DEEP))

    # EventRegistration to Attendance
    d2.add(Line(210, 60, 135, 60, strokeColor=C_DEEP, strokeWidth=1))
    d2.add(String(195, 64, "1", fontName="Helvetica-Bold", fontSize=7, fillColor=C_DEEP))
    d2.add(String(145, 64, "0..1", fontName="Helvetica-Bold", fontSize=7, fillColor=C_DEEP))

    story.append(d2)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Multiplicity & Structural Rules:</b> Each <code>Club</code> is associated with exactly 1 <code>ClubCategory</code>. "
        "A <code>Profile</code> may establish 0..* <code>ClubMembership</code> rows. An <code>Event</code> receives registrations up to its "
        "hard-coded <code>capacity</code> limit, after which subsequent insert attempts are rejected at the service layer.",
        body_style
    ))

    story.append(PageBreak())

    # ==========================================
    # PAGE 3: SEQUENCE DIAGRAM
    # ==========================================
    story.append(Paragraph("3. Sequence Diagram", h1_style))
    story.append(Paragraph(
        "<b>Scenario:</b> Complete Student Event Registration, Capacity Guard Validation, Coordinator Attendance Verification, "
        "and Dynamic Attendance Rate Calculation.", body_style
    ))

    # Drawing Sequence Diagram
    d3 = Drawing(540, 330)

    lifelines = [
        (50, "Student (S)", C_DEEP),
        (160, "React UI", C_MID),
        (280, "EventService", C_MID),
        (390, "Database (Postgres)", C_DEEP),
        (490, "Coordinator (C)", C_DARK)
    ]

    for (x, name, col) in lifelines:
        d3.add(Rect(x-40, 305, 80, 20, fillColor=col, strokeColor=col, rx=3, ry=3))
        d3.add(String(x-32, 311, name, fontName="Helvetica-Bold", fontSize=7.5, fillColor=C_WHITE))
        d3.add(Line(x, 305, x, 25, strokeColor=colors.HexColor("#CBD5E1"), strokeWidth=1, strokeDashArray=[2,2]))

    # Message 1
    d3.add(Line(50, 280, 160, 280, strokeColor=C_DARK, strokeWidth=1))
    d3.add(Polygon([155, 283, 160, 280, 155, 277], fillColor=C_DARK))
    d3.add(String(55, 284, "1. Click 'Register Event'", fontName="Helvetica", fontSize=7, fillColor=C_DARK))

    # Message 2
    d3.add(Line(160, 260, 280, 260, strokeColor=C_DARK, strokeWidth=1))
    d3.add(Polygon([275, 263, 280, 260, 275, 257], fillColor=C_DARK))
    d3.add(String(165, 264, "2. registerForEvent(evtId, uid)", fontName="Helvetica", fontSize=7, fillColor=C_DARK))

    # Message 3
    d3.add(Line(280, 240, 390, 240, strokeColor=C_DARK, strokeWidth=1))
    d3.add(Polygon([385, 243, 390, 240, 385, 237], fillColor=C_DARK))
    d3.add(String(285, 244, "3. SELECT capacity FROM events", fontName="Helvetica", fontSize=7, fillColor=C_DARK))

    # Message 4
    d3.add(Line(390, 220, 280, 220, strokeColor=C_MID, strokeWidth=0.8, strokeDashArray=[2,2]))
    d3.add(Polygon([285, 223, 280, 220, 285, 217], fillColor=C_MID))
    d3.add(String(290, 224, "4. Return max capacity (100)", fontName="Helvetica-Oblique", fontSize=7, fillColor=C_MID))

    # Alt Frame
    d3.add(Rect(145, 140, 270, 70, fillColor=None, strokeColor=C_BORDER, strokeWidth=1, strokeDashArray=[2,2]))
    d3.add(String(150, 198, "[Alt: count < capacity]", fontName="Helvetica-Bold", fontSize=7, fillColor=C_GREEN))

    # Message 5
    d3.add(Line(280, 185, 390, 185, strokeColor=C_GREEN, strokeWidth=1))
    d3.add(Polygon([385, 188, 390, 185, 385, 182], fillColor=C_GREEN))
    d3.add(String(285, 189, "5a. INSERT event_registrations", fontName="Helvetica", fontSize=7, fillColor=C_GREEN))

    # Message 6
    d3.add(Line(390, 168, 160, 168, strokeColor=C_GREEN, strokeWidth=0.8, strokeDashArray=[2,2]))
    d3.add(Polygon([165, 171, 160, 168, 165, 165], fillColor=C_GREEN))
    d3.add(String(170, 172, "6a. 201 Created & Decrement remaining seats", fontName="Helvetica-Oblique", fontSize=7, fillColor=C_GREEN))

    d3.add(String(150, 155, "[Else: count >= capacity]", fontName="Helvetica-Bold", fontSize=7, fillColor=C_RED))
    d3.add(String(170, 145, "6b. Throw Error: 'Event Capacity Reached' -> UI disables button", fontName="Helvetica-Oblique", fontSize=6.5, fillColor=C_RED))

    # Phase 2
    d3.add(Line(490, 115, 160, 115, strokeColor=C_DARK, strokeWidth=1))
    d3.add(Polygon([165, 118, 160, 115, 165, 112], fillColor=C_DARK))
    d3.add(String(250, 119, "7. Coordinator selects student -> Toggles 'Present'", fontName="Helvetica", fontSize=7, fillColor=C_DARK))

    # Message 8
    d3.add(Line(160, 95, 390, 95, strokeColor=C_DEEP, strokeWidth=1))
    d3.add(Polygon([385, 98, 390, 95, 385, 92], fillColor=C_DEEP))
    d3.add(String(180, 99, "8. UPSERT attendance (event_id, student_id, 'present')", fontName="Helvetica", fontSize=7, fillColor=C_DEEP))

    # Message 9
    d3.add(Line(390, 75, 490, 75, strokeColor=C_DEEP, strokeWidth=0.8, strokeDashArray=[2,2]))
    d3.add(Polygon([485, 78, 490, 75, 485, 72], fillColor=C_DEEP))
    d3.add(String(395, 79, "9. 200 OK (Attendance Recorded)", fontName="Helvetica-Oblique", fontSize=7, fillColor=C_DEEP))

    # Phase 3
    d3.add(Line(50, 50, 160, 50, strokeColor=C_DARK, strokeWidth=1))
    d3.add(Polygon([155, 53, 160, 50, 155, 47], fillColor=C_DARK))
    d3.add(String(55, 54, "10. Open Dashboard", fontName="Helvetica", fontSize=7, fillColor=C_DARK))

    d3.add(Line(160, 35, 390, 35, strokeColor=C_MID, strokeWidth=1))
    d3.add(Line(390, 35, 160, 35, strokeColor=C_MID, strokeWidth=0.8, strokeDashArray=[2,2]))
    d3.add(String(180, 39, "11. Fetch attendance records -> UI computes Rate: 98%", fontName="Helvetica", fontSize=7, fillColor=C_MID))

    story.append(d3)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Execution Order & Invariants:</b> Step 3 guarantees that race conditions on event caps are guarded prior to record insertion. "
        "Steps 8–9 leverage PostgreSQL <code>ON CONFLICT (event_id, student_id) DO UPDATE</code> semantics to prevent duplicate attendance logs.",
        body_style
    ))

    story.append(PageBreak())

    # ==========================================
    # PAGE 4: ACTIVITY DIAGRAM
    # ==========================================
    story.append(Paragraph("4. Activity Diagram", h1_style))
    story.append(Paragraph(
        "<b>Workflow:</b> High-level operational workflow representing end-to-end event lifecycle management, registration "
        "decision diamonds, attendance capture loop, and student transcript synchronization.", body_style
    ))

    # Drawing Activity Diagram
    d4 = Drawing(540, 330)

    # Initial Node
    d4.add(Circle(270, 315, 8, fillColor=C_DARK, strokeColor=C_DARK))
    d4.add(Line(270, 307, 270, 290, strokeColor=C_DARK, strokeWidth=1))

    # Action 1
    d4.add(Rect(190, 265, 160, 25, fillColor=C_CREAM, strokeColor=C_DEEP, strokeWidth=1, rx=6, ry=6))
    d4.add(String(205, 273, "Coordinator drafts Event Details", fontName="Helvetica-Bold", fontSize=8, fillColor=C_DEEP))
    d4.add(Line(270, 265, 270, 245, strokeColor=C_DARK, strokeWidth=1))

    # Decision 1
    d4.add(Polygon([270, 245, 295, 230, 270, 215, 245, 230], fillColor=C_WHITE, strokeColor=C_MID, strokeWidth=1))
    d4.add(String(252, 227, "Valid?", fontName="Helvetica-Bold", fontSize=7, fillColor=C_DARK))

    # Reject branch
    d4.add(Line(245, 230, 140, 230, strokeColor=C_RED, strokeWidth=1))
    d4.add(Line(140, 230, 140, 277, strokeColor=C_RED, strokeWidth=1))
    d4.add(Line(140, 277, 190, 277, strokeColor=C_RED, strokeWidth=1))
    d4.add(String(145, 235, "[No: Show Validation Errors]", fontName="Helvetica", fontSize=6.5, fillColor=C_RED))

    # Accept branch
    d4.add(Line(270, 215, 270, 195, strokeColor=C_GREEN, strokeWidth=1))
    d4.add(String(275, 203, "[Yes]", fontName="Helvetica", fontSize=7, fillColor=C_GREEN))

    # Action 2
    d4.add(Rect(190, 170, 160, 25, fillColor=C_CREAM, strokeColor=C_DEEP, strokeWidth=1, rx=6, ry=6))
    d4.add(String(198, 178, "Publish Event & Broadcast Notice", fontName="Helvetica-Bold", fontSize=8, fillColor=C_DEEP))
    d4.add(Line(270, 170, 270, 150, strokeColor=C_DARK, strokeWidth=1))

    # Action 3
    d4.add(Rect(190, 125, 160, 25, fillColor=C_CREAM, strokeColor=C_MID, strokeWidth=1, rx=6, ry=6))
    d4.add(String(205, 133, "Student Submits Registration", fontName="Helvetica-Bold", fontSize=8, fillColor=C_MID))
    d4.add(Line(270, 125, 270, 105, strokeColor=C_DARK, strokeWidth=1))

    # Decision 2
    d4.add(Polygon([270, 105, 300, 90, 270, 75, 240, 90], fillColor=C_WHITE, strokeColor=C_MID, strokeWidth=1))
    d4.add(String(248, 87, "Seats Left?", fontName="Helvetica-Bold", fontSize=7, fillColor=C_DARK))

    # Full Branch
    d4.add(Line(300, 90, 390, 90, strokeColor=C_RED, strokeWidth=1))
    d4.add(Rect(390, 75, 120, 30, fillColor=colors.HexColor("#FEE2E2"), strokeColor=C_RED, rx=4, ry=4))
    d4.add(String(400, 90, "Reject: Event Full", fontName="Helvetica-Bold", fontSize=7.5, fillColor=C_RED))
    d4.add(String(400, 80, "Prompt user to join waitlist", fontName="Helvetica", fontSize=6.5, fillColor=C_DARK))

    # Available Branch
    d4.add(Line(270, 75, 270, 55, strokeColor=C_GREEN, strokeWidth=1))
    d4.add(String(275, 63, "[Yes]", fontName="Helvetica", fontSize=7, fillColor=C_GREEN))

    # Action 4
    d4.add(Rect(190, 30, 160, 25, fillColor=C_CREAM, strokeColor=C_GREEN, strokeWidth=1, rx=6, ry=6))
    d4.add(String(198, 38, "Confirm Seat & Save Registration", fontName="Helvetica-Bold", fontSize=8, fillColor=C_GREEN))

    # Final Node
    d4.add(Line(270, 30, 270, 15, strokeColor=C_DARK, strokeWidth=1))
    d4.add(Circle(270, 8, 7, fillColor=None, strokeColor=C_DARK, strokeWidth=1))
    d4.add(Circle(270, 8, 4, fillColor=C_DARK, strokeColor=C_DARK))

    story.append(d4)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Activity Decisions & Exception Handling:</b> All coordinator form inputs are evaluated synchronously before dispatch. "
        "The capacity check branches prevent over-subscription by checking real-time database counts before committing attendance eligibility.",
        body_style
    ))

    story.append(PageBreak())

    # ==========================================
    # PAGE 5: STATE MACHINE DIAGRAM
    # ==========================================
    story.append(Paragraph("5. State Machine Diagram", h1_style))
    story.append(Paragraph(
        "<b>Entity Lifecycle:</b> Illustrates the operational states, state transitions, triggers, and terminal states for "
        "<b>Club Membership</b> and <b>Event Registration</b> entities.", body_style
    ))

    # Drawing State Machine Diagram
    d5 = Drawing(540, 220)

    # Membership Lifecycle Frame
    d5.add(Rect(15, 105, 510, 105, fillColor=C_CREAM, strokeColor=C_DEEP, strokeWidth=1, rx=6, ry=6))
    d5.add(String(25, 195, "State Machine: Club Membership Entity", fontName="Helvetica-Bold", fontSize=8.5, fillColor=C_DEEP))

    # Membership States
    d5.add(Circle(40, 155, 6, fillColor=C_DARK, strokeColor=C_DARK))
    d5.add(Line(46, 155, 80, 155, strokeColor=C_DARK, strokeWidth=1))
    d5.add(String(48, 160, "apply()", fontName="Helvetica", fontSize=6.5, fillColor=C_DARK))

    # State: Pending
    d5.add(Rect(80, 140, 80, 30, fillColor=C_WHITE, strokeColor=C_MID, strokeWidth=1, rx=5, ry=5))
    d5.add(String(95, 152, "Pending Review", fontName="Helvetica-Bold", fontSize=7.5, fillColor=C_DARK))

    # Transitions from Pending
    # To Approved
    d5.add(Line(160, 155, 230, 175, strokeColor=C_GREEN, strokeWidth=1))
    d5.add(String(165, 175, "approve()", fontName="Helvetica", fontSize=6.5, fillColor=C_GREEN))
    d5.add(Rect(230, 160, 80, 30, fillColor=colors.HexColor("#D1FAE5"), strokeColor=C_GREEN, rx=5, ry=5))
    d5.add(String(250, 172, "Approved", fontName="Helvetica-Bold", fontSize=7.5, fillColor=C_GREEN))

    # To Rejected
    d5.add(Line(160, 155, 230, 135, strokeColor=C_RED, strokeWidth=1))
    d5.add(String(165, 133, "reject()", fontName="Helvetica", fontSize=6.5, fillColor=C_RED))
    d5.add(Rect(230, 120, 80, 30, fillColor=colors.HexColor("#FEE2E2"), strokeColor=C_RED, rx=5, ry=5))
    d5.add(String(252, 132, "Rejected", fontName="Helvetica-Bold", fontSize=7.5, fillColor=C_RED))

    # Re-apply transition
    d5.add(Line(310, 135, 360, 135, strokeColor=C_MID, strokeWidth=0.8))
    d5.add(Line(360, 135, 360, 115, strokeColor=C_MID, strokeWidth=0.8))
    d5.add(Line(360, 115, 120, 115, strokeColor=C_MID, strokeWidth=0.8))
    d5.add(Line(120, 115, 120, 140, strokeColor=C_MID, strokeWidth=0.8))
    d5.add(String(200, 118, "re-apply in next academic semester", fontName="Helvetica-Oblique", fontSize=6, fillColor=C_MID))

    # End State
    d5.add(Line(310, 175, 450, 175, strokeColor=C_DARK, strokeWidth=1))
    d5.add(Circle(455, 175, 7, fillColor=None, strokeColor=C_DARK, strokeWidth=1))
    d5.add(Circle(455, 175, 4, fillColor=C_DARK, strokeColor=C_DARK))

    # Registration Lifecycle Frame
    d5.add(Rect(15, 10, 510, 85, fillColor=C_CREAM, strokeColor=C_MID, strokeWidth=1, rx=6, ry=6))
    d5.add(String(25, 80, "State Machine: Event Registration & Attendance Entity", fontName="Helvetica-Bold", fontSize=8.5, fillColor=C_MID))

    d5.add(Circle(40, 45, 6, fillColor=C_DARK, strokeColor=C_DARK))
    d5.add(Line(46, 45, 80, 45, strokeColor=C_DARK, strokeWidth=1))
    d5.add(String(50, 50, "rsvp()", fontName="Helvetica", fontSize=6.5, fillColor=C_DARK))

    d5.add(Rect(80, 30, 80, 30, fillColor=C_WHITE, strokeColor=C_MID, rx=5, ry=5))
    d5.add(String(95, 42, "Registered", fontName="Helvetica-Bold", fontSize=7.5, fillColor=C_DARK))

    d5.add(Line(160, 45, 230, 55, strokeColor=C_GREEN, strokeWidth=1))
    d5.add(String(165, 58, "mark('present')", fontName="Helvetica", fontSize=6.5, fillColor=C_GREEN))
    d5.add(Rect(230, 42, 90, 24, fillColor=colors.HexColor("#D1FAE5"), strokeColor=C_GREEN, rx=4, ry=4))
    d5.add(String(240, 50, "Attended: Present", fontName="Helvetica-Bold", fontSize=7, fillColor=C_GREEN))

    d5.add(Line(160, 45, 230, 25, strokeColor=C_RED, strokeWidth=1))
    d5.add(String(165, 23, "mark('absent')", fontName="Helvetica", fontSize=6.5, fillColor=C_RED))
    d5.add(Rect(230, 15, 90, 24, fillColor=colors.HexColor("#FEE2E2"), strokeColor=C_RED, rx=4, ry=4))
    d5.add(String(242, 23, "Attended: Absent", fontName="Helvetica-Bold", fontSize=7, fillColor=C_RED))

    # Terminal Circle
    d5.add(Line(320, 45, 450, 45, strokeColor=C_DARK, strokeWidth=1))
    d5.add(Circle(455, 45, 7, fillColor=None, strokeColor=C_DARK, strokeWidth=1))
    d5.add(Circle(455, 45, 4, fillColor=C_DARK, strokeColor=C_DARK))

    story.append(d5)
    story.append(Spacer(1, 10))

    sm_table_data = [
        [
            Paragraph("Entity", cell_header),
            Paragraph("Initial State", cell_header),
            Paragraph("Trigger Events & Guards", cell_header),
            Paragraph("Terminal / Valid States", cell_header)
        ],
        [
            Paragraph("<b>Club Membership</b>", cell_style),
            Paragraph("Unapplied", cell_style),
            Paragraph("apply() &rarr; Pending; approve() [if Coordinator] &rarr; Approved; reject() &rarr; Rejected", cell_style),
            Paragraph("Approved, Rejected, Cancelled", cell_style)
        ],
        [
            Paragraph("<b>Event Registration</b>", cell_style),
            Paragraph("Unregistered", cell_style),
            Paragraph("rsvp() [if count &lt; capacity] &rarr; Registered; cancel() &rarr; Cancelled", cell_style),
            Paragraph("Attended (Present / Late / Absent)", cell_style)
        ]
    ]
    t5 = Table(sm_table_data, colWidths=[90, 75, 225, 150])
    t5.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_DEEP),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_CREAM]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t5)

    doc.build(story)
    print(f"Successfully generated clean PDF at: {output_path}")

if __name__ == '__main__':
    out_dir = r"e:\Club Management System\docs"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "CCMS_UML_Diagrams.pdf")
    create_uml_pdf(out_file)
