"""
Category: Black Box Testing — Positive Scenarios
Objective: Verify expected user outcomes when valid, normative inputs are provided to system endpoints.
"""
import pytest
import requests

def test_bb_pos_01_landing_page_accessible(http_session, frontend_url):
    """
    Test Case: TC-BB-POS-01
    Verify the public landing page loads with HTTP 200 and contains the CCMS brand title.
    """
    resp = http_session.get(frontend_url, timeout=5)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    assert "CCMS" in resp.text, "Landing page missing CCMS title marker"

def test_bb_pos_02_clubs_catalog_route_accessible(http_session, frontend_url):
    """
    Test Case: TC-BB-POS-02
    Verify the clubs catalog route (/clubs) is publicly accessible.
    """
    resp = http_session.get(f"{frontend_url}/clubs", timeout=5)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"

def test_bb_pos_03_auth_login_route_accessible(http_session, frontend_url):
    """
    Test Case: TC-BB-POS-03
    Verify the user authentication login page (/login) loads cleanly.
    """
    resp = http_session.get(f"{frontend_url}/login", timeout=5)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"

def test_bb_pos_04_auth_register_route_accessible(http_session, frontend_url):
    """
    Test Case: TC-BB-POS-04
    Verify user registration page (/register) is available for new student accounts.
    """
    resp = http_session.get(f"{frontend_url}/register", timeout=5)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"

def test_bb_pos_05_supabase_categories_read(http_session, supabase_url, supabase_headers):
    """
    Test Case: TC-BB-POS-05
    Verify the club categories endpoint returns HTTP 200 with active category objects.
    """
    resp = http_session.get(
        f"{supabase_url}/rest/v1/club_categories?select=id,name,description",
        headers=supabase_headers,
        timeout=10
    )
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    data = resp.json()
    assert isinstance(data, list) and len(data) > 0, "Expected non-empty list of club categories"

def test_bb_pos_06_supabase_clubs_read(http_session, supabase_url, supabase_headers):
    """
    Test Case: TC-BB-POS-06
    Verify that reading the clubs catalog returns active college clubs.
    """
    resp = http_session.get(
        f"{supabase_url}/rest/v1/clubs?select=id,name,slug,description,status&status=eq.approved",
        headers=supabase_headers,
        timeout=10
    )
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    data = resp.json()
    assert isinstance(data, list) and len(data) > 0, "Expected active clubs in catalog"

def test_bb_pos_07_frontend_static_assets_serve(http_session, frontend_url):
    """
    Test Case: TC-BB-POS-07
    Verify the frontend delivers HTML5 doctype and modern ES module script tags.
    """
    resp = http_session.get(frontend_url, timeout=5)
    assert resp.status_code == 200
    assert "<!doctype html>" in resp.text.lower()
    assert 'type="module"' in resp.text
