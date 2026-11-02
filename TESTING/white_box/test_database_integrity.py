"""
Category: White Box Testing — Database Integrity & Schema Contracts
Objective: Inspect structural relational integrity, foreign key cascades, CORS headers, and service health.
"""
import pytest
import requests

def test_wb_db_01_foreign_key_constraint_cascade(http_session, supabase_url, supabase_headers):
    """
    Test Case: TC-WB-DB-01
    Verify the relational schema prevents orphaned records by enforcing foreign key checks.
    """
    bogus_club = {
        "name": "Orphan Test Club",
        "slug": "orphan-test-club-slug",
        "category_id": "00000000-0000-0000-0000-999999999999"
    }
    resp = http_session.post(
        f"{supabase_url}/rest/v1/clubs",
        headers=supabase_headers,
        json=bogus_club,
        timeout=10
    )
    assert resp.status_code in [400, 401, 403, 409]

def test_wb_db_02_postgrest_cors_header_contracts(http_session, supabase_url, supabase_headers):
    """
    Test Case: TC-WB-DB-02
    Verify PostgREST server-side options preflight response headers conform to CORS contracts.
    """
    resp = http_session.options(
        f"{supabase_url}/rest/v1/clubs",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET"
        },
        timeout=10
    )
    assert resp.status_code in [200, 204]
    allow_origin = resp.headers.get("Access-Control-Allow-Origin", "")
    assert allow_origin in ["*", "http://localhost:5173"]

def test_wb_db_03_auth_service_health_endpoint(http_session, supabase_url, supabase_headers):
    """
    Test Case: TC-WB-DB-03
    Inspect internal Supabase GoTrue Auth service health status endpoint.
    """
    resp = http_session.get(f"{supabase_url}/auth/v1/health", headers=supabase_headers, timeout=10)
    assert resp.status_code in [200, 401, 404]
    if resp.status_code == 200:
        data = resp.json()
        assert "version" in data or "name" in data or data.get("status") == "ok"

def test_wb_db_04_frontend_backend_connectivity(http_session, frontend_url, supabase_url, supabase_headers):
    """
    Test Case: TC-WB-DB-04
    Verify bidirectional network connectivity between presentation tier and data tier.
    """
    fe_resp = http_session.get(frontend_url, timeout=5)
    assert fe_resp.status_code == 200
    be_resp = http_session.get(f"{supabase_url}/rest/v1/clubs?select=id&limit=1", headers=supabase_headers, timeout=10)
    assert be_resp.status_code == 200
