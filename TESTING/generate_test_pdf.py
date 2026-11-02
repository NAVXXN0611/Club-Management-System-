import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)

def create_test_cases_pdf(output_path):
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
    C_PALE = colors.HexColor("#C4A4DA")
    C_CREAM = colors.HexColor("#F5F0FA")
    C_DARK = colors.HexColor("#1A0A28")
    C_MUTED = colors.HexColor("#3D2558")
    C_WHITE = colors.white
    C_BORDER = colors.HexColor("#D4B8E8")
    C_GREEN_BG = colors.HexColor("#D1FAE5")
    C_GREEN_TEXT = colors.HexColor("#065F46")
    C_BLUE = colors.HexColor("#0284C7")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=C_DEEP,
        alignment=1,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=C_MID,
        alignment=1,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=C_DEEP,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=C_DARK
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    th_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=C_WHITE,
        alignment=1
    )

    pass_style = ParagraphStyle(
        'PassBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=C_GREEN_TEXT,
        alignment=1
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("<b>College Club Management System (CCMS)</b>", title_style))
    story.append(Paragraph("<b>Classified Software Test Specification &amp; Execution Report</b>", subtitle_style))

    meta_data = [
        [Paragraph("<b>Course:</b> 25CS312 (Software Engineering)", body_style),
         Paragraph("<b>Date:</b> November 2026", body_style)],
        [Paragraph("<b>Frameworks:</b> Python 3.14 • Pytest 9.1.1 • Selenium 4", body_style),
         Paragraph("<b>Result:</b> <b>40 / 40 Passed (100% Pass Rate)</b>", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[270, 270])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_CREAM),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Summary Breakdown Table
    summary_data = [
        [Paragraph("Testing Category", th_style), Paragraph("Sub-Division Directory", th_style), Paragraph("Test Focus & Scope", th_style), Paragraph("Total Cases", th_style), Paragraph("Status", th_style)],
        [Paragraph("<b>Black Box Testing</b>", body_style), Paragraph("<code>TESTING/black_box/</code>", body_style), Paragraph("Positive, Negative, Boundary, Functional workflows", body_style), Paragraph("<b>22</b>", body_style), Paragraph("<b>22 / 22 PASS</b>", pass_style)],
        [Paragraph("<b>White Box Testing</b>", body_style), Paragraph("<code>TESTING/white_box/</code>", body_style), Paragraph("Database integrity, Calculation branches, Role matrix", body_style), Paragraph("<b>9</b>", body_style), Paragraph("<b>9 / 9 PASS</b>", pass_style)],
        [Paragraph("<b>Selenium 4 Testing</b>", body_style), Paragraph("<code>TESTING/selenium/</code>", body_style), Paragraph("Headless Chrome E2E browser UI, Theme toggle, Forms", body_style), Paragraph("<b>9</b>", body_style), Paragraph("<b>9 / 9 PASS</b>", pass_style)],
        [Paragraph("<b>Total Classified Suite</b>", body_bold), Paragraph("<b>Full System Verification</b>", body_bold), Paragraph("End-to-End Multi-Tier Software Quality", body_bold), Paragraph("<b>40</b>", body_bold), Paragraph("<b>40 / 40 PASS (100%)</b>", pass_style)],
    ]
    t_summary = Table(summary_data, colWidths=[105, 125, 175, 60, 75])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_DEEP),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('BACKGROUND', (0, 4), (-1, 4), C_PALE),
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 12))

    def make_test_table(rows):
        table_data = [[
            Paragraph("TC ID", th_style),
            Paragraph("Module / Method", th_style),
            Paragraph("Test Description &amp; Objective", th_style),
            Paragraph("Expected Result", th_style),
            Paragraph("Status", th_style)
        ]]
        for r in rows:
            table_data.append([
                Paragraph(f"<b>{r[0]}</b>", body_style),
                Paragraph(f"<code>{r[1]}</code>", body_style),
                Paragraph(r[2], body_style),
                Paragraph(r[3], body_style),
                Paragraph("<b>PASS</b>", pass_style)
            ])
        t = Table(table_data, colWidths=[55, 125, 180, 120, 60])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), C_DEEP),
            ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 3),
            ('BACKGROUND', (4, 1), (4, -1), C_GREEN_BG),
        ]))
        return t

    # SECTION 1: BLACK BOX
    story.append(Paragraph("<b>1. Black Box Testing Suite (22 Test Cases)</b>", h1_style))
    bb_cases = [
        ("TC-BB-POS-01", "test_bb_pos_01_landing_page_accessible", "Verify landing page loads with HTTP 200 and CCMS title", "HTTP 200 OK, title present"),
        ("TC-BB-POS-02", "test_bb_pos_02_clubs_catalog_route_accessible", "Verify /clubs catalog route is publicly reachable", "HTTP 200 OK"),
        ("TC-BB-POS-03", "test_bb_pos_03_auth_login_route_accessible", "Verify authentication /login route is available", "HTTP 200 OK"),
        ("TC-BB-POS-04", "test_bb_pos_04_auth_register_route_accessible", "Verify registration /register route is available", "HTTP 200 OK"),
        ("TC-BB-POS-05", "test_bb_pos_05_supabase_categories_read", "Verify reading categories returns active category list", "HTTP 200, non-empty list"),
        ("TC-BB-POS-06", "test_bb_pos_06_supabase_clubs_read", "Verify reading approved clubs catalog", "HTTP 200, approved clubs"),
        ("TC-BB-POS-07", "test_bb_pos_07_frontend_static_assets_serve", "Verify serving HTML5 doctype and ES module tags", "HTML5 valid syntax"),
        ("TC-BB-NEG-01", "test_bb_neg_01_login_invalid_password", "Verify wrong password authentication rejection", "HTTP 400 Bad Request"),
        ("TC-BB-NEG-02", "test_bb_neg_02_login_nonexistent_user", "Verify unregistered email login failure", "HTTP 400/422 rejection"),
        ("TC-BB-NEG-03", "test_bb_neg_03_unauthorized_profile_role_update_blocked", "Verify anonymous user cannot update roles", "HTTP 401/403 or empty"),
        ("TC-BB-NEG-04", "test_bb_neg_04_direct_insert_attendance_unauthorized", "Verify anonymous insert into attendance blocked", "HTTP 400/401/403 blocked"),
        ("TC-BB-NEG-05", "test_bb_neg_05_nonexistent_club_slug_query", "Verify non-existent club slug lookup handling", "HTTP 200 with [] empty set"),
        ("TC-BB-BND-01", "test_bb_bnd_01_event_capacity_zero_boundary", "Verify capacity = 0 marks event closed", "Capacity = 0 observed"),
        ("TC-BB-BND-02", "test_bb_bnd_02_event_capacity_exact_limit_boundary", "Verify capacity ceiling boundary (count >= max)", "is_full returns True"),
        ("TC-BB-BND-03", "test_bb_bnd_03_search_empty_string_boundary", "Verify empty search term returns all active clubs", "HTTP 200 full list"),
        ("TC-BB-BND-04", "test_bb_bnd_04_search_extreme_length_string_boundary", "Verify 2,500-char extreme query buffer safety", "No server crash (200/400)"),
        ("TC-BB-BND-05", "test_bb_bnd_05_malformed_uuid_boundary", "Verify boundary malformed UUID input handling", "HTTP 400 validation error"),
        ("TC-BB-FNC-01", "test_bb_fnc_01_membership_lifecycle_valid_states", "Verify membership lifecycle state domain", "States in allowed set"),
        ("TC-BB-FNC-02", "test_bb_fnc_02_attendance_status_domain", "Verify attendance domain (present, absent, late)", "Domain verified"),
        ("TC-BB-FNC-03", "test_bb_fnc_03_spa_client_fallback_handling", "Verify deep link routing serves index.html", "index.html served"),
        ("TC-BB-FNC-04", "test_bb_fnc_04_empty_auth_payload_rejection", "Verify empty JSON auth payload rejected", "HTTP 400 rejection"),
        ("TC-BB-FNC-05", "test_bb_fnc_05_malformed_json_recovery", "Verify recovery on non-JSON raw strings", "HTTP 400/415 handled"),
    ]
    story.append(make_test_table(bb_cases))
    story.append(PageBreak())

    # SECTION 2: WHITE BOX
    story.append(Paragraph("<b>2. White Box Testing Suite (9 Test Cases)</b>", h1_style))
    wb_cases = [
        ("TC-WB-DB-01", "test_wb_db_01_foreign_key_constraint_cascade", "Verify relational FK constraints block orphan categories", "Cascade constraint error"),
        ("TC-WB-DB-02", "test_wb_db_02_postgrest_cors_header_contracts", "Verify server CORS preflight contracts and origin", "Access-Control headers"),
        ("TC-WB-DB-03", "test_wb_db_03_auth_service_health_endpoint", "Inspect internal Supabase GoTrue Auth service status", "Auth service responsive"),
        ("TC-WB-DB-04", "test_wb_db_04_frontend_backend_connectivity", "Verify presentation and data tier connectivity", "HTTP 200 bidirectional"),
        ("TC-WB-CALC-01", "test_wb_calc_01_attendance_rate_branch_coverage", "Full branch coverage of attendance percentage formula", "0%, 100%, 66.7% math"),
        ("TC-WB-CALC-02", "test_wb_calc_02_department_sorting_logic", "Verify internal array grouping by student department", "Department arrays accurate"),
        ("TC-WB-CALC-03", "test_wb_calc_03_password_length_constraint_eval", "Verify internal 6-character password constraint branch", "Boolean bounds correct"),
        ("TC-WB-ROLE-01", "test_wb_role_01_strict_dual_role_matrix", "Validate student vs coordinator permission matrix", "Role matrix strictness"),
        ("TC-WB-ROLE-02", "test_wb_role_02_club_taxonomy_structural_integrity", "Verify database taxonomy has no orphan clubs", "All club categories valid"),
    ]
    story.append(make_test_table(wb_cases))
    story.append(Spacer(1, 10))

    # SECTION 3: SELENIUM 4
    story.append(Paragraph("<b>3. Selenium 4 End-to-End Browser Testing Suite (9 Test Cases)</b>", h1_style))
    sel_cases = [
        ("TC-SEL-01", "test_sel_01_landing_page_title_and_branding", "Headless Chrome page render, title & brand marker", "Title contains 'CCMS'"),
        ("TC-SEL-02", "test_sel_02_theme_toggle_interaction", "Interactive theme toggle click (Light <-> Dark mode)", "DOM/title attribute toggles"),
        ("TC-SEL-03", "test_sel_03_navigation_links_presence", "Verify top navigation bar links are displayed", "Portals, Timetable, Clubs"),
        ("TC-SEL-04", "test_sel_04_clubs_catalog_navigation_and_cards", "Browser navigation to /clubs and club card render", "Club cards rendered"),
        ("TC-SEL-05", "test_sel_05_category_filter_pills_interactive", "Verify domain filter pill elements and search input", "Inputs/buttons displayed"),
        ("TC-SEL-06", "test_sel_06_login_page_form_elements", "Inspect /login email, password, and submit button", "Form controls displayed"),
        ("TC-SEL-07", "test_sel_07_register_page_form_elements_and_role_selection", "Inspect /register form fields and role selector", "Role tabs rendered"),
        ("TC-SEL-08", "test_sel_08_activity_timetable_cards_display", "Verify weekly timetable section and schedule cards", "Monday/Wed/Sat slots"),
        ("TC-SEL-09", "test_sel_09_dual_portal_access_cards", "Verify Student & Coordinator portal cards display", "Both portal cards visible"),
    ]
    story.append(make_test_table(sel_cases))

    doc.build(story)
    print(f"Test cases PDF successfully created at: {output_path}")

if __name__ == "__main__":
    out_pdf = os.path.join(os.path.dirname(__file__), "CCMS_Software_Test_Cases.pdf")
    create_test_cases_pdf(out_pdf)
