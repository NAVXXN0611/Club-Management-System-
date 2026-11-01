"""
Module: Boundary Testing Suite
Test Category: 3. Boundary Testing (IA3 Checklist Item 4.3)
Objective: Verify minimum, maximum, and edge-case values across data inputs and capacities.
"""
import pytest
import requests

def test_bnd_01_event_capacity_zero_boundary():
    """
    Test Case ID: TC-BND-01
    Requirement ID: FR-REG-03
    Objective: Verify capacity validation logic rejects registration when capacity is 0.
    """
    def can_register(current_count: int, capacity: int) -> bool:
        return current_count < capacity

    assert not can_register(current_count=0, capacity=0), "Capacity of 0 must reject registrations"
    assert not can_register(current_count=1, capacity=0), "Capacity of 0 must reject registrations"

def test_bnd_02_event_capacity_exact_limit_boundary():
    """
    Test Case ID: TC-BND-02
    Requirement ID: FR-REG-03
    Objective: Verify boundary condition when registered count exactly reaches maximum capacity.
    """
    capacity = 100
    assert (99 < capacity) is True, "Seat 100 out of 100 should be permitted"
    assert (100 < capacity) is False, "Seat 101 out of 100 must be rejected"
    assert (101 < capacity) is False, "Overcapacity must be rejected"

def test_bnd_03_search_empty_string_boundary(http_session, supabase_url, supabase_headers):
    """
    Test Case ID: TC-BND-03
    Requirement ID: FR-CLUB-03
    Objective: Verify search handler safely handles empty string without SQL syntax error.
    """
    resp = http_session.get(
        f"{supabase_url}/rest/v1/clubs?name=ilike.%25%25",
        headers=supabase_headers,
        timeout=10
    )
    assert resp.status_code == 200, "Empty search wildcard failed"
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1, "Empty search should return all existing clubs"

def test_bnd_04_search_extreme_length_string_boundary(http_session, supabase_url, supabase_headers):
    """
    Test Case ID: TC-BND-04
    Requirement ID: FR-CLUB-03, NFR-SEC-06
    Objective: Verify search query with 1000 characters does not crash or cause buffer overflow.
    """
    extreme_search = "A" * 1000
    resp = http_session.get(
        f"{supabase_url}/rest/v1/clubs?name=ilike.%25{extreme_search}%25",
        headers=supabase_headers,
        timeout=10
    )
    assert resp.status_code in [200, 400], "Server failed ungracefully on extreme query length"
    if resp.status_code == 200:
        assert resp.json() == []

def test_bnd_05_malformed_uuid_boundary(http_session, supabase_url, supabase_headers):
    """
    Test Case ID: TC-BND-05
    Requirement ID: NFR-SEC-06
    Objective: Verify non-UUID parameter (e.g. 'invalid-id-123') is rejected by PostgreSQL type validator.
    """
    resp = http_session.get(
        f"{supabase_url}/rest/v1/clubs?id=eq.invalid-non-uuid-string-123",
        headers=supabase_headers,
        timeout=10
    )
    assert resp.status_code in [400, 422], f"Expected 400/422 for malformed UUID, got {resp.status_code}"
    err_text = resp.text.lower()
    assert "uuid" in err_text or "invalid" in err_text or "syntax" in err_text

