"""
Module: Validation & Error Handling Suite
Test Category: 6. Validation and Error Handling (IA3 Checklist Item 4.6)
Objective: Verification of error messages, input restrictions, and recovery behaviour.
"""
import pytest
import requests

def test_val_01_password_length_restriction(http_session, supabase_url, supabase_headers):
    """
    Test Case ID: TC-VAL-01
    Requirement ID: FR-AUTH-01, 6.1
    Objective: Verify registration with a short password (<6 chars) produces a clear validation error.
    """
    payload = {
        "email": "test_short_pw@college.edu",
        "password": "123" # Less than 6 characters
    }
    resp = http_session.post(
        f"{supabase_url}/auth/v1/signup",
        headers=supabase_headers,
        json=payload,
        timeout=10
    )
    assert resp.status_code == 422 or resp.status_code == 400, f"Expected 400/422 validation failure, got {resp.status_code}"
    error_text = resp.text.lower()
    assert "password" in error_text and ("least" in error_text or "short" in error_text or "characters" in error_text)

def test_val_02_empty_auth_payload_rejection(http_session, supabase_url, supabase_headers):
    """
    Test Case ID: TC-VAL-02
    Requirement ID: FR-AUTH-02, NFR-USE-04
    Objective: Submitting an empty JSON payload to authentication endpoint returns descriptive error.
    """
    resp = http_session.post(
        f"{supabase_url}/auth/v1/token?grant_type=password",
        headers=supabase_headers,
        json={},
        timeout=10
    )
    assert resp.status_code == 400, f"Expected 400 Bad Request, got {resp.status_code}"

def test_val_03_malformed_json_recovery(http_session, supabase_url, supabase_headers):
    """
    Test Case ID: TC-VAL-03
    Requirement ID: NFR-REL-02
    Objective: Submitting malformed JSON is caught gracefully by the server without crashing.
    """
    headers = dict(supabase_headers)
    headers["Content-Type"] = "application/json"
    resp = http_session.post(
        f"{supabase_url}/rest/v1/clubs",
        headers=headers,
        data="{ malformed_json_without_quotes: true, ", # Invalid syntax
        timeout=10
    )
    assert resp.status_code in [400, 422], f"Expected 400/422 for malformed JSON, got {resp.status_code}"

def test_val_04_spa_client_fallback_handling(http_session, frontend_url):
    """
    Test Case ID: TC-VAL-04
    Requirement ID: NFR-USE-04
    Objective: Verify arbitrary unknown client routes e.g. /some/random/missing/route return 200 SPA fallback rather than 404 Apache/Nginx crash.
    """
    resp = http_session.get(f"{frontend_url}/some/random/missing/route", timeout=5)
    assert resp.status_code == 200, "SPA router should catch all routes and render client-side 404 or redirect"
    assert "<!doctype html>" in resp.text.lower() or "<html" in resp.text.lower()

