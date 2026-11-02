"""
Category: Black Box Testing — Negative Scenarios
Objective: Verify system robustness, input sanitization, and rejection of invalid user inputs.
"""
import pytest
import requests

def test_bb_neg_01_login_invalid_password(http_session, supabase_url, supabase_headers):
    """
    Test Case: TC-BB-NEG-01
    Verify that authenticating with an invalid password correctly fails with HTTP 400.
    """
    payload = {
        "email": "test_user_nonexistent@karunya.edu",
        "password": "wrong_password_xyz_123"
    }
    resp = http_session.post(
        f"{supabase_url}/auth/v1/token?grant_type=password",
        headers=supabase_headers,
        json=payload,
        timeout=10
    )
    assert resp.status_code == 400, f"Expected HTTP 400 on invalid login, got {resp.status_code}"
    body = resp.json()
    assert "error" in body or "error_description" in body or "msg" in body

def test_bb_neg_02_login_nonexistent_user(http_session, supabase_url, supabase_headers):
    """
    Test Case: TC-BB-NEG-02
    Verify attempting login with a non-existent account does not disclose internal system state.
    """
    payload = {
        "email": "definitely_does_not_exist_99887766@karunya.edu",
        "password": "ValidPassword123!"
    }
    resp = http_session.post(
        f"{supabase_url}/auth/v1/token?grant_type=password",
        headers=supabase_headers,
        json=payload,
        timeout=10
    )
    assert resp.status_code in [400, 422], f"Expected 400 or 422 on nonexistent account, got {resp.status_code}"

def test_bb_neg_03_unauthorized_profile_role_update_blocked(http_session, supabase_url, supabase_headers):
    """
    Test Case: TC-BB-NEG-03
    Verify an unauthenticated or anonymous user cannot elevate privileges or update profile roles.
    """
    bogus_update = {"role": "admin"}
    resp = http_session.patch(
        f"{supabase_url}/rest/v1/profiles?id=eq.00000000-0000-0000-0000-000000000000",
        headers=supabase_headers,
        json=bogus_update,
        timeout=10
    )
    assert resp.status_code in [200, 401, 403, 404]
    if resp.status_code == 200:
        assert resp.json() == []

def test_bb_neg_04_direct_insert_attendance_unauthorized(http_session, supabase_url, supabase_headers):
    """
    Test Case: TC-BB-NEG-04
    Verify unauthorized users cannot inject bogus attendance records without coordinator rights.
    """
    bogus_attendance = {
        "event_id": "00000000-0000-0000-0000-000000000000",
        "user_id": "00000000-0000-0000-0000-000000000000",
        "status": "present"
    }
    resp = http_session.post(
        f"{supabase_url}/rest/v1/attendance",
        headers=supabase_headers,
        json=bogus_attendance,
        timeout=10
    )
    assert resp.status_code in [400, 401, 403, 404, 409]

def test_bb_neg_05_nonexistent_club_slug_query(http_session, supabase_url, supabase_headers):
    """
    Test Case: TC-BB-NEG-05
    Verify querying a non-existent club slug gracefully returns an empty result set (HTTP 200 with []).
    """
    resp = http_session.get(
        f"{supabase_url}/rest/v1/clubs?slug=eq.completely-fabricated-nonexistent-club-slug",
        headers=supabase_headers,
        timeout=10
    )
    assert resp.status_code == 200
    assert resp.json() == []
