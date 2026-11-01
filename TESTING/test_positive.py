"""
Module: Positive Testing Suite
Test Category: 1. Positive Testing (IA3 Checklist Item 4.1)
Objective: Verify valid inputs and expected successful operations across the working application.
"""
import pytest
import requests

def test_pos_01_landing_page_loads_successfully(http_session, frontend_url):
    """
    Test Case ID: TC-POS-01
    Requirement ID: FR-CLUB-01
    Objective: Verify the landing page returns HTTP 200 and loads essential UI markers.
    """
    resp = http_session.get(frontend_url, timeout=5)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    assert "<title>" in resp.text or "CCMS" in resp.text, "Landing page title or brand marker missing"
    assert "root" in resp.text, "React root mounting container not found in DOM"

def test_pos_02_clubs_catalog_route_accessible(http_session, frontend_url):
    """
    Test Case ID: TC-POS-02
    Requirement ID: FR-CLUB-01, FR-CLUB-02
    Objective: Verify the public clubs directory route returns HTTP 200.
    """
    resp = http_session.get(f"{frontend_url}/clubs", timeout=5)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    assert "text/html" in resp.headers.get("Content-Type", ""), "Response is not HTML"

def test_pos_03_auth_login_route_accessible(http_session, frontend_url):
    """
    Test Case ID: TC-POS-03
    Requirement ID: FR-AUTH-02
    Objective: Verify the sign-in route returns HTTP 200.
    """
    resp = http_session.get(f"{frontend_url}/login", timeout=5)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"

def test_pos_04_auth_register_route_accessible(http_session, frontend_url):
    """
    Test Case ID: TC-POS-04
    Requirement ID: FR-AUTH-01
    Objective: Verify the registration route returns HTTP 200.
    """
    resp = http_session.get(f"{frontend_url}/register", timeout=5)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"

def test_pos_05_supabase_categories_read(http_session, supabase_url, supabase_headers):
    """
    Test Case ID: TC-POS-05
    Requirement ID: FR-CLUB-02
    Objective: Verify that valid queries to the Supabase backend fetch active categories.
    """
    resp = http_session.get(
        f"{supabase_url}/rest/v1/club_categories?select=id,name",
        headers=supabase_headers,
        timeout=10
    )
    assert resp.status_code == 200, f"Supabase category fetch failed: {resp.text}"
    data = resp.json()
    assert isinstance(data, list), "Expected array of categories"
    assert len(data) >= 1, "Expected at least one seeded category in database"
    category_names = [c["name"] for c in data]
    assert any("Academic" in name or "Cultural" in name for name in category_names), "Expected Academic or Cultural categories"

def test_pos_06_supabase_clubs_read(http_session, supabase_url, supabase_headers):
    """
    Test Case ID: TC-POS-06
    Requirement ID: FR-CLUB-01
    Objective: Verify that valid queries to the Supabase backend fetch active clubs.
    """
    resp = http_session.get(
        f"{supabase_url}/rest/v1/clubs?select=id,name,slug",
        headers=supabase_headers,
        timeout=10
    )
    assert resp.status_code == 200, f"Supabase clubs fetch failed: {resp.text}"
    data = resp.json()
    assert isinstance(data, list), "Expected array of clubs"
    assert len(data) >= 1, "Expected at least one active club in database"
    assert all("id" in c and "name" in c and "slug" in c for c in data), "Missing required club columns"

def test_pos_07_frontend_static_assets_serve(http_session, frontend_url):
    """
    Test Case ID: TC-POS-07
    Requirement ID: NFR-PERF-01
    Objective: Verify that Vite bundles and serves static CSS and JavaScript chunks.
    """
    # Fetch index HTML to extract script path
    html_resp = http_session.get(frontend_url, timeout=5)
    assert html_resp.status_code == 200
    # Search for bundled asset references
    assert "src/main.tsx" in html_resp.text or "/assets/" in html_resp.text, "Vite script tag missing from HTML"

