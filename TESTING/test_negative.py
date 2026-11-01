"""
Module: Negative Testing Suite
Test Category: 2. Negative Testing (IA3 Checklist Item 4.2)
Objective: Verify rejection of invalid inputs, incorrect credentials, and unauthorized operations.
"""
import pytest
import requests

def test_neg_01_login_invalid_password(http_session, supabase_url, supabase_headers):
    """
    Test Case ID: TC-NEG-01
    Requirement ID: FR-AUTH-02
    Objective: Verify authentication fails with 400 Bad Request when provided an incorrect password.
    """
    payload = {
        "email": "student@college.edu",
        "password": "definitely_wrong_password_987654"
    }
    resp = http_session.post(
        f"{supabase_url}/auth/v1/token?grant_type=password",
        headers=supabase_headers,
        json=payload,
        timeout=10
    )
    assert resp.status_code == 400, f"Expected 400 Bad Request for bad credentials, got {resp.status_code}"
    error_data = resp.json()
    assert "error" in error_data or "msg" in error_data or "message" in error_data
    assert "invalid_credentials" in str(error_data).lower() or "invalid login" in str(error_data).lower()

def test_neg_02_login_nonexistent_user(http_session, supabase_url, supabase_headers):
    """
    Test Case ID: TC-NEG-02
    Requirement ID: FR-AUTH-02
    Objective: Verify authentication rejects nonexistent email accounts cleanly.
    """
    payload = {
        "email": "nonexistent_ghost_user_99999@college.edu",
        "password": "SomeValidPassword123!"
    }
    resp = http_session.post(
        f"{supabase_url}/auth/v1/token?grant_type=password",
        headers=supabase_headers,
        json=payload,
        timeout=10
    )
    assert resp.status_code == 400
    assert "invalid" in resp.text.lower()

def test_neg_03_unauthorized_profile_role_update_blocked(http_session, supabase_url, supabase_headers):
    """
    Test Case ID: TC-NEG-03
    Requirement ID: FR-AUTH-04, NFR-SEC-01
    Objective: Verify an unauthenticated request cannot promote or alter any profile role.
    """
    payload = {
        "role": "admin"
    }
    resp = http_session.patch(
        f"{supabase_url}/rest/v1/profiles?email=eq.student@college.edu",
        headers=supabase_headers,
        json=payload,
        timeout=10
    )
    # RLS should either return 200 with 0 modified rows or 401/403
    if resp.status_code == 200:
        assert resp.json() == [] or len(resp.json()) == 0, "Security Violation: Unauthenticated update altered rows!"
    else:
        assert resp.status_code in [401, 403, 404]

def test_neg_04_direct_insert_attendance_unauthorized(http_session, supabase_url, supabase_headers):
    """
    Test Case ID: TC-NEG-04
    Requirement ID: FR-ATT-05, NFR-SEC-01
    Objective: Verify unauthenticated users cannot directly insert verified attendance rows.
    """
    payload = {
        "event_id": "00000000-0000-0000-0000-000000000001",
        "student_id": "00000000-0000-0000-0000-000000000002",
        "status": "present"
    }
    resp = http_session.post(
        f"{supabase_url}/rest/v1/attendance",
        headers=supabase_headers,
        json=payload,
        timeout=10
    )
    assert resp.status_code in [401, 403, 404, 409], f"RLS policy failure: Status code {resp.status_code} allowed insert"

def test_neg_05_nonexistent_club_slug_query(http_session, supabase_url, supabase_headers):
    """
    Test Case ID: TC-NEG-05
    Requirement ID: FR-CLUB-04
    Objective: Querying an invalid or nonexistent club slug returns empty set without SQL exception.
    """
    resp = http_session.get(
        f"{supabase_url}/rest/v1/clubs?slug=eq.nonexistent-club-slug-xyz123",
        headers=supabase_headers,
        timeout=10
    )
    assert resp.status_code == 200
    assert resp.json() == [], "Expected empty array for nonexistent slug"

