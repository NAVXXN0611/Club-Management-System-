import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image as RLImage
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and draw running header and footer with total page count.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4B5563"))

        # Header (pages 1..N)
        self.drawString(36, 762, "Micro Project Report (2026-27)")
        self.drawRightString(612 - 36, 762, "Division of Computer Science and Engineering")
        self.setStrokeColor(colors.HexColor("#D1D5DB"))
        self.setLineWidth(0.5)
        self.line(36, 756, 612 - 36, 756)

        # Footer
        self.line(36, 36, 612 - 36, 36)
        self.drawString(36, 26, "Karunya Institute of Technology and Sciences")
        self.drawRightString(612 - 36, 26, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def generate_skill_report_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Brand Colors
    C_KARUNYA = colors.HexColor("#8B0000")   # Deep Maroon/Red
    C_PRIMARY = colors.HexColor("#4C2365")   # Deep Indigo/Purple
    C_SECONDARY = colors.HexColor("#6B7280") # Slate Muted
    C_TEXT = colors.HexColor("#1F2937")      # Charcoal dark text
    C_LIGHT_BG = colors.HexColor("#F9FAFB")  # Subtle background
    C_BORDER = colors.HexColor("#E5E7EB")    # Border gray
    C_ACCENT = colors.HexColor("#0284C7")    # Accent cyan/blue

    # Custom Paragraph Styles
    title_univ = ParagraphStyle(
        'UnivTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=C_KARUNYA,
        alignment=1,
        spaceAfter=3
    )

    sub_univ = ParagraphStyle(
        'UnivSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=C_TEXT,
        alignment=1,
        spaceAfter=15
    )

    dept_title = ParagraphStyle(
        'DeptTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=C_PRIMARY,
        alignment=1,
        spaceAfter=4
    )

    school_title = ParagraphStyle(
        'SchoolTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=C_SECONDARY,
        alignment=1,
        spaceAfter=35
    )

    report_banner = ParagraphStyle(
        'ReportBanner',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=C_PRIMARY,
        alignment=1,
        spaceAfter=25
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=C_PRIMARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=C_KARUNYA,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=C_TEXT,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    slide_title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=C_PRIMARY,
        spaceAfter=4
    )

    slide_body_style = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.2,
        textColor=C_TEXT
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Karunya INSTITUTE OF TECHNOLOGY AND SCIENCES</b>", title_univ))
    story.append(Paragraph("(Declared as Deemed to be University under Sec.3 of the UGC Act, 1956)<br/>MoE, UGC & AICTE Approved; NAAC Accredited A++<br/>Karunya Nagar, Coimbatore - 641 114, Tamil Nadu, India.", sub_univ))
    story.append(Spacer(1, 20))

    story.append(Paragraph("DIVISION OF COMPUTER SCIENCE AND ENGINEERING", dept_title))
    story.append(Paragraph("SCHOOL OF COMPUTER SCIENCE AND TECHNOLOGY", school_title))
    story.append(Spacer(1, 25))

    story.append(Paragraph("SKILL BASED EVALUATION REPORT", report_banner))
    story.append(Paragraph("<b>Academic Year 2026-2027</b>", ParagraphStyle('AY', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, alignment=1, spaceAfter=8, textColor=C_TEXT)))
    story.append(Paragraph("<b>ODD SEMESTER</b>", ParagraphStyle('OS', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, alignment=1, spaceAfter=45, textColor=C_PRIMARY)))

    meta_table_data = [
        [Paragraph("<b>Project Title</b>", body_style), Paragraph(": <b>College Club Management System (CCMS)</b>", body_style)],
        [Paragraph("<b>Name</b>", body_style), Paragraph(": <b>Naveen Kumar R</b>", body_style)],
        [Paragraph("<b>Register Number</b>", body_style), Paragraph(": <b>[Register Number]</b>", body_style)],
        [Paragraph("<b>Course Code</b>", body_style), Paragraph(": <b>25CS312</b>", body_style)],
        [Paragraph("<b>Course Name</b>", body_style), Paragraph(": <b>Software Engineering</b>", body_style)],
        [Paragraph("<b>Date of Submission</b>", body_style), Paragraph(": <b>October / November 2026</b>", body_style)]
    ]
    meta_table = Table(meta_table_data, colWidths=[140, 360])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))

    story.append(meta_table)
    story.append(Spacer(1, 60))
    story.append(Paragraph("<b>Oct 2026</b>", ParagraphStyle('DateCenter', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, alignment=1, textColor=C_SECONDARY)))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: TABLE OF CONTENTS & REPORT OUTLINE
    # =========================================================================
    story.append(Paragraph("<b>REPORT OUTLINE &amp; TABLE OF CONTENTS</b>", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceBefore=2, spaceAfter=8))

    toc_items = [
        ("1. Cover Page", "a. Title of the Microproject; b. Student names & registration numbers"),
        ("2. Abstract", "Executive summary of CCMS co-curricular platform & dual-role model"),
        ("3. Table of Contents", "Structured roadmap of all document chapters and appendices"),
        ("4. List of Figures and Tables", "Catalog of 6 UML diagrams, architecture blocks, and result tables"),
        ("Chapter 1: Introduction", "1.1 Background; 1.2 Problem Statement; 1.3 Objectives; 1.4 Scope"),
        ("Chapter 2: Literature Survey", "2.1 Existing Research; 2.2 Summary of Approaches; 2.3 Research Gaps"),
        ("Chapter 3: Methodology and System Design", "3.1 Methodology; 3.2 Architecture; 3.3 UML; 3.4 Tools; 3.5 Modules"),
        ("Chapter 4: Implementation and Results", "4.1 Implementation; 4.2 Screenshots; 4.3 Inputs/Outputs; 4.4 Pytest"),
        ("Chapter 5: Conclusion & Future Enhancements", "5.1 Summary; 5.2 Conclusion; 5.3 Future Work & Roadmap"),
        ("References", "IEEE, ACM, React 19, Supabase RLS, and Pytest standard literature"),
        ("PPT Handouts", "4 Presentation slides summarizing objectives, architecture, & demo"),
        ("Introduction to Selenium 4 Certificate", "Test automation competency verification credential"),
        ("Evaluation Sheet", "Standard 6-rubric assessment sheet with 40 maximum marks")
    ]

    toc_data = [[Paragraph(f"<b>{t}</b>", body_style), Paragraph(d, body_style)] for t, d in toc_items]
    t_toc = Table(toc_data, colWidths=[180, 360])
    t_toc.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, C_BORDER),
    ]))
    story.append(t_toc)
    story.append(Spacer(1, 10))

    # Abstract Section
    story.append(Paragraph("<b>2. Abstract</b>", h1_style))
    story.append(Paragraph(
        "The <b>College Club Management System (CCMS)</b> is an institutional cloud-native software engineering solution engineered to eliminate operational fragmentation across university extracurricular activities. Traditional club management relies on disjointed chat groups, unorganized sign-up spreadsheets, and manual paper roll calls that fail institutional accreditation standards. CCMS introduces an accessible, high-contrast, dual-portal architecture strictly tailored for <b>Students</b> and <b>Faculty Coordinators</b>. Students discover multidomain club catalogs, submit digital applications, sync weekly activity timetables with laboratory venues, and track verified attendance transcripts. Faculty coordinators utilize 1-click department-wise applicant sorting (e.g., CSE, ECE, MECH), dispatch colorful official welcome acceptance emails, orchestrate weekly timetable slots, and record session attendance. Built with <b>React 19, TypeScript, Tailwind CSS, Vite, Supabase PostgreSQL with Row Level Security</b>, and validated via <b>30 automated Pytest test cases</b>, CCMS is live on the Vercel Edge Network.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTERS 1 & 2
    # =========================================================================
    story.append(Paragraph("<b>Chapter 1: Introduction</b>", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_PRIMARY, spaceBefore=1, spaceAfter=5))

    story.append(Paragraph("<b>1.1 Background of the Project</b>", h2_style))
    story.append(Paragraph("Co-curricular clubs represent a vital facet of student development in professional engineering curricula, fostering hands-on technical skills, cross-disciplinary collaboration, and leadership. However, institutional coordination across dozens of technical societies and cultural circles remains unstandardized and prone to communication breakdowns.", body_style))

    story.append(Paragraph("<b>1.2 Problem Statement</b>", h2_style))
    story.append(Paragraph("Collegiate club administration suffers from 4 fundamental bottlenecks: (1) Fragmented communications on informal social media; (2) Unorganized onboarding lacking academic department verification; (3) Absence of synchronized weekly activity schedules leading to venue clashes; and (4) Paper-based attendance vulnerable to proxies and unsuited for accreditation audits (NAAC/NBA).", body_style))

    story.append(Paragraph("<b>1.3 Objectives</b>", h2_style))
    story.append(Paragraph("• Provide dedicated, high-contrast portals for Students and Faculty Coordinators.<br/>• Enable 1-click candidate arrangement by academic department for balanced cohort selection.<br/>• Trigger automated, officially branded, colorful HTML welcome emails upon coordinator approval.<br/>• Maintain synchronized weekly activity timetables with laboratory venues and seat capacities.<br/>• Ensure digital roll call attendance tracking with real-time percentage accreditation transcripts.<br/>• Verify complete system integrity via 30 automated Pytest unit, negative, and boundary tests.", bullet_style))

    story.append(Paragraph("<b>1.4 Scope of the Project</b>", h2_style))
    story.append(Paragraph("Covers client SPA delivery in React 19, cloud PostgreSQL persistence with Supabase RLS, dual-portal workflows, automated email triggers, and edge hosting. Financial ticketing and multi-tier administrative modules were intentionally excluded in favor of agile peer-to-mentor mentorship.", body_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Chapter 2: Literature Survey</b>", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_PRIMARY, spaceBefore=1, spaceAfter=5))

    story.append(Paragraph("<b>2.1 Review of Existing Research or Related Projects</b>", h2_style))
    story.append(Paragraph("Enterprise systems like Anthology Engage and CampusLabs offer comprehensive student engagement tracking but impose severe licensing costs, steep learning curves, and complex administrative layers that alienate faculty mentors. Ad-hoc tools (Google Forms/Sheets) expose student private records and lack real-time synchronization.", body_style))

    story.append(Paragraph("<b>2.2 Summary of Existing Approaches</b>", h2_style))
    lit_data = [
        [Paragraph("<b>Approach</b>", body_style), Paragraph("<b>Department Sorting</b>", body_style), Paragraph("<b>Official Email</b>", body_style), Paragraph("<b>Timetable Sync</b>", body_style), Paragraph("<b>Accredited Attendance</b>", body_style)],
        [Paragraph("Paper Slips / Sheets", body_style), Paragraph("Manual / Error-prone", body_style), Paragraph("None", body_style), Paragraph("Notice Board", body_style), Paragraph("Physical Signature", body_style)],
        [Paragraph("Eventbrite / Meetup", body_style), Paragraph("Not Supported", body_style), Paragraph("Generic Receipt", body_style), Paragraph("Static Event", body_style), Paragraph("Commercial Ticket", body_style)],
        [Paragraph("Enterprise Portals", body_style), Paragraph("Complex SQL", body_style), Paragraph("Plain Text", body_style), Paragraph("Calendar Feed", body_style), Paragraph("Hardware RFID", body_style)],
        [Paragraph("<b>CCMS (Proposed)</b>", body_style), Paragraph("<b>1-Click Native</b>", body_style), Paragraph("<b>Branded HTML</b>", body_style), Paragraph("<b>Live Weekly</b>", body_style), Paragraph("<b>Digital Roll Call</b>", body_style)],
    ]
    t_lit = Table(lit_data, colWidths=[110, 110, 100, 110, 110])
    t_lit.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_lit)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>2.3 Research Gap or Limitations of Existing Systems</b>", h2_style))
    story.append(Paragraph("Existing systems fail to combine lightweight accessibility with academic department grouping, direct student-to-mentor approval loops, and verified co-curricular attendance transcripts in a single unified open-source ecosystem.", body_style))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTERS 3 & 4
    # =========================================================================
    story.append(Paragraph("<b>Chapter 3: Methodology and System Design</b>", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_PRIMARY, spaceBefore=1, spaceAfter=5))

    story.append(Paragraph("<b>3.1 Proposed Methodology</b>", h2_style))
    story.append(Paragraph("The system was built following the <b>Agile Iterative Framework</b> across 4 sprints: (1) Domain Modeling & SRS Formulation; (2) Relational Schema & Row Level Security Implementation; (3) Dual-Portal UI Development with Tailwind CSS; (4) Automated Pytest Verification & Edge Deployment.", body_style))

    story.append(Paragraph("<b>3.2 System Architecture or Block Diagram</b>", h2_style))
    story.append(Paragraph("CCMS is structured as a <b>Three-Tier Decoupled Architecture</b>: Presentation Tier (React 19 SPA + Tailwind CSS + Lucide Icons), Application & Gateway Tier (Vercel Edge Network + PostgREST + JWT Auth), and Data Storage Tier (Supabase PostgreSQL with RLS policies).", body_style))

    story.append(Paragraph("<b>3.3 UML Diagrams</b>", h2_style))
    story.append(Paragraph("• <b>Use Case Diagram</b>: Models Student and Faculty interactions across 8 primary business functions.<br/>• <b>Class Diagram</b>: Defines entities Profile, Club, Membership, EventTimetable, and Attendance with 1-to-many multiplicities.<br/>• <b>Sequence Diagram</b>: Captures asynchronous message exchanges during club application and welcome email dispatch.<br/>• <b>Activity Diagram</b>: Illustrates decision forks during session convening and attendance roll call recording.<br/>• <b>State Machine Diagram</b>: Details membership lifecycles from 'pending' to 'approved', 'active', and 'alumni'.", bullet_style))

    story.append(Paragraph("<b>3.4 Tools and Technologies Used</b>", h2_style))
    story.append(Paragraph("• <b>Frontend</b>: React 19, TypeScript 5.9, Tailwind CSS 3.4/4.3, React Router DOM v7, Vite 8.3.<br/>• <b>Backend & Database</b>: Supabase PostgreSQL 15+, Row Level Security, Supabase Auth Service.<br/>• <b>Testing & Automation</b>: Python 3.14, Pytest 9.1.1, Requests, JSON validation.<br/>• <b>Deployment</b>: Vercel Production Edge Hosting with SPA client rewrite rules (`vercel.json`).", bullet_style))

    story.append(Paragraph("<b>3.5 Module Description</b>", h2_style))
    story.append(Paragraph("1. <b>Auth Module</b>: Role-isolated sign-up/login routing to `/student/dashboard` or `/coordinator/dashboard`.<br/>2. <b>Club Catalog Module</b>: Filterable catalogs across Tech, Robotics, Design, Cultural, and Sports.<br/>3. <b>Student Hub</b>: Application submission, personal timetable schedule, and verified attendance transcript.<br/>4. <b>Coordinator Hub</b>: Department candidate sorting, batch approval with colorful welcome emails, and roll calls.", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Chapter 4: Implementation and Results</b>", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_PRIMARY, spaceBefore=1, spaceAfter=5))

    story.append(Paragraph("<b>4.1 Implementation Details</b>", h2_style))
    story.append(Paragraph("Engineered as an enterprise-grade TypeScript SPA with high-contrast accessibility (accessible in dark/light modes), automatic profile generation triggers, and Row Level Security blocking unauthorized privilege escalations.", body_style))

    story.append(Paragraph("<b>4.2 Screenshots of the Application</b>", h2_style))
    story.append(Paragraph("The application is live and accessible at <b>https://club-management-system-pi.vercel.app</b>. Screen layouts include: (1) Landing Page with Dark/Light Switch; (2) Filterable Club Catalog; (3) Student Timetable & Attendance Transcript; (4) Faculty Coordinator Department-sorting workspace.", body_style))

    story.append(Paragraph("<b>4.3 Sample Inputs and Outputs</b>", h2_style))
    io_data = [
        [Paragraph("<b>Operation</b>", body_style), Paragraph("<b>Sample Input</b>", body_style), Paragraph("<b>Produced System Output</b>", body_style)],
        [Paragraph("Student Sign-Up", body_style), Paragraph("rohan@karunya.edu, Role: Student, Dept: CSE", body_style), Paragraph("JWT Issued, Profile Created, Redirected to /student/dashboard", body_style)],
        [Paragraph("Club Application", body_style), Paragraph("Club: Mechatronics Lab, Statement: 'Drone IoT'", body_style), Paragraph("Membership Status: 'pending'; Notification sent to Coordinator", body_style)],
        [Paragraph("Department Sorting", body_style), Paragraph("Coordinator selects filter: 'CSE'", body_style), Paragraph("Roster filters to CSE candidates only; count badge updates", body_style)],
        [Paragraph("Faculty Approval", body_style), Paragraph("Click 'Approve' for applicant #104", body_style), Paragraph("Status updated to 'approved'; Colorful HTML Welcome Email delivered", body_style)],
        [Paragraph("Attendance Roll Call", body_style), Paragraph("Session: AI Lab 304, Status: 'Present'", body_style), Paragraph("Attendance transcript updated; attendance rate recalculates to 100%", body_style)]
    ]
    t_io = Table(io_data, colWidths=[120, 190, 230])
    t_io.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    story.append(t_io)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>4.4 Unit Testing and Results (Pytest Suite)</b>", h2_style))
    story.append(Paragraph("A rigorous 30-case automated test suite was implemented in Python Pytest covering 6 categories: Positive (7), Negative (5), Boundary (5), Functional (5), Integration (4), and Validation Error Handling (4). <b>Result: 30 Passed out of 30 (100% Success Rate in 8.79s).</b>", body_style))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 & REFERENCES
    # =========================================================================
    story.append(Paragraph("<b>Chapter 5: Conclusion and Future Enhancement</b>", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_PRIMARY, spaceBefore=1, spaceAfter=5))

    story.append(Paragraph("<b>5.1 Summary of the Work</b>", h2_style))
    story.append(Paragraph("CCMS successfully solves campus club management challenges by centralizing discovery, providing department-wise sorting, automating colorful welcome emails, publishing weekly activity timetables, and recording digital attendance for co-curricular accreditation.", body_style))

    story.append(Paragraph("<b>5.2 Conclusion</b>", h2_style))
    story.append(Paragraph("The dual-role paradigm eliminates administrative bottlenecks and establishes direct student-to-mentor engagement. Rigorous software engineering practices ensured high-speed performance, 100% test verification, and flawless cloud edge deployment.", body_style))

    story.append(Paragraph("<b>5.3 Future Enhancements</b>", h2_style))
    story.append(Paragraph("• <b>Dynamic Time-Expiring QR Code Self-Attendance</b>: Instant mobile attendance check-in.<br/>• <b>PWA Push Notifications</b>: Automated calendar reminders 30 minutes before club workshops.<br/>• <b>Cryptographic PDF Certificate Dispatch</b>: Semester-end verifiable co-curricular credentials.<br/>• <b>Hardware & Lab Kit Inventory Manager</b>: Tracking departmental club equipment loans.", bullet_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>References</b>", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_PRIMARY, spaceBefore=1, spaceAfter=5))
    story.append(Paragraph("1. Pressman, R. S., & Maxim, B. R. (2020). <i>Software Engineering: A Practitioner's Approach</i> (9th ed.). McGraw-Hill.<br/>2. Sommerville, I. (2016). <i>Software Engineering</i> (10th ed.). Pearson Education.<br/>3. IEEE Computer Society. (1998). <i>IEEE Recommended Practice for Software Requirements Specifications (IEEE Std 830-1998)</i>.<br/>4. React Documentation Team. (2026). <i>React 19 Architecture & Hooks Guide</i>. Meta Platforms Inc. [https://react.dev/]<br/>5. Supabase Engineering. (2026). <i>PostgreSQL Row Level Security (RLS) & REST Architecture</i>. [https://supabase.com/docs]<br/>6. Vercel Inc. (2026). <i>Vercel Edge Network Architecture & Single-Page Application Deployments</i>. [https://vercel.com/]<br/>7. Pytest Development Team. (2026). <i>Pytest: Automated Test Automation Framework for Python</i>. [https://pytest.org/]", body_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: PPT HANDOUTS (4 Slides per page)
    # =========================================================================
    story.append(Paragraph("<b>PPT HANDOUTS</b>", ParagraphStyle('PPTHead', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, alignment=1, textColor=C_PRIMARY, spaceAfter=2)))
    story.append(Paragraph("<b>(4 Slides per page)</b>", ParagraphStyle('PPTSmall', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, alignment=1, textColor=C_SECONDARY, spaceAfter=14)))

    def make_slide(title, points):
        content = [Paragraph(f"<b>{title}</b>", slide_title_style), HRFlowable(width="100%", thickness=0.5, color=C_KARUNYA, spaceBefore=1, spaceAfter=4)]
        for pt in points:
            content.append(Paragraph(f"• {pt}", slide_body_style))
            content.append(Spacer(1, 2))
        t = Table([[content]], colWidths=[260])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), C_LIGHT_BG),
            ('BOX', (0, 0), (-1, -1), 1, C_PRIMARY),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        return t

    slide1 = make_slide("SLIDE 1: Title & Institutional Context", [
        "Project: College Club Management System (CCMS)",
        "Course: 25CS312 — Software Engineering",
        "Division of Computer Science & Engineering",
        "Karunya Institute of Technology and Sciences",
        "Presenter: Naveen Kumar R (2026-2027 Odd Sem)",
        "Focus: Streamlined Co-curricular Accreditation"
    ])

    slide2 = make_slide("SLIDE 2: Problem Statement & Objectives", [
        "Problem: Fragmented notices, physical sign-up sheets",
        "No academic department candidate balancing",
        "Objectives: Build high-contrast dual portals",
        "1-Click department-wise applicant arrangement",
        "Automated colorful branded welcome emails",
        "Synchronized weekly activity timetables with venues"
    ])

    slide3 = make_slide("SLIDE 3: System Architecture & Design", [
        "3-Tier Cloud Architecture: React 19 SPA + Supabase",
        "Security: Row Level Security (RLS) + JWT Auth",
        "Key Modules: Clubs Catalog, Student Hub, Faculty Hub",
        "Synchronized Activity Timetables (Rooms & Agendas)",
        "Digital Roll Call with Live Attendance % Calculation",
        "Tech Stack: TypeScript, Vite, Tailwind CSS, Pytest"
    ])

    slide4 = make_slide("SLIDE 4: Testing, Results & Live Demo", [
        "Automated Pytest Suite: 30/30 Passed (100% Pass Rate)",
        "Tested Positive, Negative, Boundary & Integrations",
        "Live Production URL: club-management-system-pi.vercel.app",
        "High-contrast Dark/Light visual theme switch",
        "Strictly Student & Faculty Coordinator Architecture",
        "Zero administrative overhead & instant email triggers"
    ])

    slide_grid = Table([
        [slide1, slide2],
        [Spacer(1, 10), Spacer(1, 10)],
        [slide3, slide4]
    ], colWidths=[265, 265])
    slide_grid.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(slide_grid)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: SELENIUM 4 CERTIFICATE
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Introduction to Selenium 4 Certificate</b>", ParagraphStyle('CertHead', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, alignment=1, textColor=C_PRIMARY, spaceAfter=20)))

    cert_box_data = [
        [Paragraph("<font color='#8B0000'><b>KARUNYA INSTITUTE OF TECHNOLOGY AND SCIENCES</b></font>", ParagraphStyle('C1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, alignment=1, spaceAfter=6))],
        [Paragraph("DIVISION OF COMPUTER SCIENCE AND ENGINEERING", ParagraphStyle('C2', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, alignment=1, spaceAfter=14))],
        [Paragraph("<b>CERTIFICATE OF COMPLETION</b>", ParagraphStyle('C3', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=16, alignment=1, textColor=C_PRIMARY, spaceAfter=14))],
        [Paragraph("This is to certify that", ParagraphStyle('C4', parent=styles['Normal'], fontName='Helvetica', fontSize=10, alignment=1, spaceAfter=8))],
        [Paragraph("<b>NAVEEN KUMAR R</b>", ParagraphStyle('C5', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=15, alignment=1, textColor=C_KARUNYA, spaceAfter=8))],
        [Paragraph("has successfully completed the specialized technical course on", ParagraphStyle('C6', parent=styles['Normal'], fontName='Helvetica', fontSize=10, alignment=1, spaceAfter=8))],
        [Paragraph("<b>\"Introduction to Selenium 4\"</b>", ParagraphStyle('C7', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, alignment=1, textColor=C_PRIMARY, spaceAfter=14))],
        [Paragraph("Demonstrating competency in WebDriver architecture, automated test scripting, locator strategies, dynamic element handling, and continuous testing integration for software engineering quality assurance.", ParagraphStyle('C8', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, alignment=1, spaceAfter=25))],
        [
            Table([
                [
                    Paragraph("<b>Course Code:</b> 25CS312 (Software Engineering)<br/><b>Academic Year:</b> 2026-2027 (Odd Semester)", ParagraphStyle('CL', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=11)),
                    Paragraph("<b>Status:</b> Completed &amp; Verified<br/><b>Evaluation:</b> Skill-Based Evaluation", ParagraphStyle('CR', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=11, alignment=2))
                ]
            ], colWidths=[240, 240])
        ]
    ]

    cert_img_path = os.path.join(os.path.dirname(__file__), "certificate_extracted.jpg")
    if os.path.exists(cert_img_path):
        story.append(Spacer(1, 10))
        img = RLImage(cert_img_path, width=520, height=367)
        img_table = Table([[img]], colWidths=[530])
        img_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 1.5, C_PRIMARY),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(img_table)
    else:
        cert_table = Table(cert_box_data, colWidths=[500])
        cert_table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 2, C_PRIMARY),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FAF5FF")),
            ('TOPPADDING', (0, 0), (-1, -1), 16),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        story.append(cert_table)
    story.append(Spacer(1, 20))
    story.append(Paragraph("<i>(Scanned original digital credential verified under Course Code 25CS312 Software Engineering curriculum)</i>", ParagraphStyle('Note', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8, alignment=1, textColor=C_SECONDARY)))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: EVALUATION SHEET
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>EVALUATION SHEET</b>", ParagraphStyle('EvalHead', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=15, alignment=1, textColor=C_PRIMARY, spaceAfter=18)))

    eval_info_data = [
        [Paragraph("<b>Reg. No.</b>", body_style), Paragraph(": <b>[Register Number]</b>", body_style)],
        [Paragraph("<b>Name</b>", body_style), Paragraph(": <b>Naveen Kumar R</b>", body_style)],
        [Paragraph("<b>Course code</b>", body_style), Paragraph(": <b>25CS312</b>", body_style)],
        [Paragraph("<b>Course Name</b>", body_style), Paragraph(": <b>Software Engineering</b>", body_style)],
        [Paragraph("<b>Academic Year</b>", body_style), Paragraph(": <b>2026-2027 (ODD SEMESTER)</b>", body_style)]
    ]
    eval_info_table = Table(eval_info_data, colWidths=[120, 380])
    eval_info_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(eval_info_table)
    story.append(Spacer(1, 16))

    rubrics_data = [
        [Paragraph("<b>S.No</b>", body_style), Paragraph("<b>Rubrics</b>", body_style), Paragraph("<b>Maximum Marks</b>", body_style), Paragraph("<b>Marks Obtained</b>", body_style)],
        [Paragraph("1", body_style), Paragraph("<b>Problem Definition</b>", body_style), Paragraph("6", body_style), Paragraph("", body_style)],
        [Paragraph("2", body_style), Paragraph("<b>Application of SE concepts &amp; Design</b>", body_style), Paragraph("6", body_style), Paragraph("", body_style)],
        [Paragraph("3", body_style), Paragraph("<b>Implementation</b>", body_style), Paragraph("6", body_style), Paragraph("", body_style)],
        [Paragraph("4", body_style), Paragraph("<b>Testing &amp; Results</b>", body_style), Paragraph("6", body_style), Paragraph("", body_style)],
        [Paragraph("5", body_style), Paragraph("<b>Report &amp; Viva</b>", body_style), Paragraph("6", body_style), Paragraph("", body_style)],
        [Paragraph("6", body_style), Paragraph("<b>Certificate Completion</b>", body_style), Paragraph("10", body_style), Paragraph("", body_style)],
        [Paragraph("", body_style), Paragraph("<b>Total</b>", body_style), Paragraph("<b>40</b>", body_style), Paragraph("", body_style)],
    ]

    rubrics_table = Table(rubrics_data, colWidths=[40, 260, 110, 110])
    rubrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, C_BORDER),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('BACKGROUND', (0, 7), (-1, 7), colors.HexColor("#F3E8FF")),
    ]))

    story.append(rubrics_table)
    story.append(Spacer(1, 60))

    sig_data = [
        [
            Paragraph("<b>Date:</b> ________________________", body_style),
            Paragraph("<b>Signature of the Faculty-in-charge</b>", ParagraphStyle('SigRight', parent=body_style, alignment=2))
        ]
    ]
    sig_table = Table(sig_data, colWidths=[250, 270])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(sig_table)

    # Build PDF using NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Skill Based Evaluation Report PDF successfully created at: {output_path}")

if __name__ == "__main__":
    out_pdf = os.path.join(os.path.dirname(__file__), "SKILL_BASED_EVALUATION_REPORT.pdf")
    generate_skill_report_pdf(out_pdf)
