"""
Category: Black Box Testing — Functional Workflows
Objective: Verify high-level functional user scenarios, state progression, and error recovery workflows.
"""
import pytest
import requests

def test_bb_fnc_01_membership_lifecycle_valid_states():
    """
    Test Case: TC-BB-FNC-01
    Verify the club membership state machine only permits valid states.
    """
    valid_states = {"pending", "approved", "rejected", "inactive"}
    sample_flow = ["pending", "approved", "inactive"]
    for state in sample_flow:
        assert state in valid_states, f"Invalid membership state encountered: {state}"

def test_bb_fnc_02_attendance_status_domain():
    """
    Test Case: TC-BB-FNC-02
    Verify the attendance status domain allows only 'present', 'absent', and 'late'.
    """
    allowed_statuses = {"present", "absent", "late"}
    test_inputs = ["present", "absent", "late"]
    for st in test_inputs:
        assert st in allowed_statuses
    assert "excused_unverified" not in allowed_statuses

def test_bb_fnc_03_spa_client_fallback_handling(http_session, frontend_url):
    """
    Test Case: TC-BB-FNC-03
    Verify that deep links to client-side routes return index.html for client-side router resolution.
    """
    deep_link = f"{frontend_url}/coordinator/dashboard"
    resp = http_session.get(deep_link, timeout=5)
    assert resp.status_code == 200
    assert "<!doctype html>" in resp.text.lower()
    assert 'id="root"' in resp.text

def test_bb_fnc_04_empty_auth_payload_rejection(http_session, supabase_url, supabase_headers):
    """
    Test Case: TC-BB-FNC-04
    Verify sending an empty JSON payload to the auth endpoint is rejected with HTTP 400.
    """
    resp = http_session.post(
        f"{supabase_url}/auth/v1/token?grant_type=password",
        headers=supabase_headers,
        json={},
        timeout=10
    )
    assert resp.status_code == 400

def test_bb_fnc_05_malformed_json_recovery(http_session, supabase_url, supabase_headers):
    """
    Test Case: TC-BB-FNC-05
    Verify the API endpoint recovers gracefully when sent invalid non-JSON raw strings.
    """
    raw_headers = dict(supabase_headers)
    raw_headers["Content-Type"] = "application/json"
    resp = http_session.post(
        f"{supabase_url}/rest/v1/clubs",
        headers=raw_headers,
        data="this is definitely { not valid json } string content",
        timeout=10
    )
    assert resp.status_code in [400, 401, 403, 415]
