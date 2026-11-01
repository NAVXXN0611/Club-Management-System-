"""
Module: Integration Testing Suite
Test Category: 5. Integration Testing (IA3 Checklist Item 4.5)
Objective: Verify that interacting modules (Vite Frontend, Supabase PostgREST, Database, and Auth) work together correctly.
"""
import pytest
import requests

def test_int_01_frontend_backend_connectivity(http_session, frontend_url, supabase_url, supabase_headers):
    """
    Test Case ID: TC-INT-01
    Requirement ID: NFR-PERF-02, 5.3
    Objective: Verify bidirectional connectivity between client dev server and remote Supabase backend.
    """
    # 1. Ping Frontend
    fe_resp = http_session.get(frontend_url, timeout=5)
    assert fe_resp.status_code == 200, "Frontend is unreachable"

    # 2. Ping Backend PostgREST API
    be_resp = http_session.get(f"{supabase_url}/rest/v1/clubs?select=id&limit=1", headers=supabase_headers, timeout=10)
    assert be_resp.status_code == 200, f"Supabase PostgREST endpoint returned error: {be_resp.status_code}"

def test_int_02_postgrest_headers_and_cors(http_session, supabase_url, supabase_headers):
    """
    Test Case ID: TC-INT-02
    Requirement ID: 5.4, NFR-SEC-05
    Objective: Verify PostgREST returns required CORS headers for browser fetch requests.
    """
    resp = http_session.options(
        f"{supabase_url}/rest/v1/clubs",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET"
        },
        timeout=10
    )
    assert resp.status_code in [200, 204], "CORS preflight request rejected"
    allow_origin = resp.headers.get("Access-Control-Allow-Origin", "")
    assert allow_origin in ["*", "http://localhost:5173"], f"Invalid CORS Allow-Origin header: {allow_origin}"

def test_int_03_database_foreign_key_constraint_integrity(http_session, supabase_url, supabase_headers):
    """
    Test Case ID: TC-INT-03
    Requirement ID: 6.4, NFR-SEC-06
    Objective: Verify attempting to insert a club with a bogus nonexistent category ID is rejected by foreign key constraint.
    """
    bogus_club = {
        "name": "Invalid Test Club",
        "slug": "invalid-test-club-temp",
        "category_id": "00000000-0000-0000-0000-999999999999"
    }
    resp = http_session.post(
        f"{supabase_url}/rest/v1/clubs",
        headers=supabase_headers,
        json=bogus_club,
        timeout=10
    )
    # Must reject with 400 or 401/403/409 (foreign key or RLS violation)
    assert resp.status_code in [400, 401, 403, 409], f"Database accepted orphaned foreign key: {resp.status_code}"

def test_int_04_auth_service_health(http_session, supabase_url, supabase_headers):
    """
    Test Case ID: TC-INT-04
    Requirement ID: FR-AUTH-02, 5.3
    Objective: Verify Supabase GoTrue Auth service health endpoint is live and responding.
    """
    resp = http_session.get(
        f"{supabase_url}/auth/v1/health",
        headers=supabase_headers,
        timeout=10
    )
    assert resp.status_code == 200, f"Auth health check failed: {resp.text}"
    health_data = resp.json()
    assert health_data.get("name") == "GoTrue" or "version" in health_data or "description" in health_data
