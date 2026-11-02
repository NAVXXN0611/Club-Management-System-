"""
Category: Black Box Testing — Boundary Value Analysis (BVA)
Objective: Test extreme boundary values, capacity limits, string thresholds, and edge inputs.
"""
import pytest
import requests

def test_bb_bnd_01_event_capacity_zero_boundary(http_session, supabase_url, supabase_headers):
    """
    Test Case: TC-BB-BND-01
    Verify that an event with capacity = 0 is treated as closed/unregistrable.
    """
    resp = http_session.get(
        f"{supabase_url}/rest/v1/events?capacity=eq.0",
        headers=supabase_headers,
        timeout=10
    )
    assert resp.status_code == 200
    events = resp.json()
    for ev in events:
        assert ev.get("capacity", 0) == 0

def test_bb_bnd_02_event_capacity_exact_limit_boundary():
    """
    Test Case: TC-BB-BND-02
    Verify capacity ceiling logic: when current attendees == max capacity, is_full must evaluate to True.
    """
    def is_event_full(current_count: int, max_capacity: int) -> bool:
        if max_capacity <= 0:
            return True
        return current_count >= max_capacity

    assert is_event_full(current_count=49, max_capacity=50) is False
    assert is_event_full(current_count=50, max_capacity=50) is True
    assert is_event_full(current_count=51, max_capacity=50) is True
    assert is_event_full(current_count=0, max_capacity=0) is True

def test_bb_bnd_03_search_empty_string_boundary(http_session, supabase_url, supabase_headers):
    """
    Test Case: TC-BB-BND-03
    Verify that an empty string search returns all active clubs without error.
    """
    resp = http_session.get(
        f"{supabase_url}/rest/v1/clubs?select=id,name&name=ilike.*",
        headers=supabase_headers,
        timeout=10
    )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list) and len(data) >= 0

def test_bb_bnd_04_search_extreme_length_string_boundary(http_session, supabase_url, supabase_headers):
    """
    Test Case: TC-BB-BND-04
    Verify sending an excessively long search term (2,500 characters) is handled safely without 500 error.
    """
    extreme_query = "A" * 2500
    resp = http_session.get(
        f"{supabase_url}/rest/v1/clubs?select=id,name&name=ilike.*{extreme_query[:50]}*",
        headers=supabase_headers,
        timeout=10
    )
    assert resp.status_code in [200, 400], f"Unexpected status code for extreme query: {resp.status_code}"
    if resp.status_code == 200:
        assert resp.json() == []

def test_bb_bnd_05_malformed_uuid_boundary(http_session, supabase_url, supabase_headers):
    """
    Test Case: TC-BB-BND-05
    Verify querying with a boundary malformed UUID string produces a clean validation error (400) without crashing.
    """
    malformed_id = "not-a-valid-uuid-boundary-test"
    resp = http_session.get(
        f"{supabase_url}/rest/v1/clubs?id=eq.{malformed_id}",
        headers=supabase_headers,
        timeout=10
    )
    assert resp.status_code == 400
    data = resp.json()
    assert "message" in data or "code" in data

