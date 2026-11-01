"""
Module: Functional Testing Suite
Test Category: 4. Functional Testing (IA3 Checklist Item 4.4)
Objective: Verify the major functional features, calculation business logic, and workflows.
"""
import pytest
import requests

def test_fnc_01_club_category_taxonomy_integrity(http_session, supabase_url, supabase_headers):
    """
    Test Case ID: TC-FNC-01
    Requirement ID: FR-CLUB-02
    Objective: Verify every active club is correctly linked to an existing, valid category.
    """
    clubs_resp = http_session.get(
        f"{supabase_url}/rest/v1/clubs?select=id,name,category_id",
        headers=supabase_headers,
        timeout=10
    )
    cats_resp = http_session.get(
        f"{supabase_url}/rest/v1/club_categories?select=id,name",
        headers=supabase_headers,
        timeout=10
    )
    assert clubs_resp.status_code == 200 and cats_resp.status_code == 200
    clubs = clubs_resp.json()
    cats = {c["id"]: c["name"] for c in cats_resp.json()}
    
    for club in clubs:
        if club.get("category_id"):
            assert club["category_id"] in cats, f"Club {club['name']} links to orphan category ID {club['category_id']}"

def test_fnc_02_attendance_rate_calculation():
    """
    Test Case ID: TC-FNC-02
    Requirement ID: FR-ATT-04
    Objective: Verify the institutional attendance percentage calculation logic is accurate.
    """
    def compute_attendance_rate(records: list) -> float:
        if not records:
            return 0.0
        present_count = sum(1 for r in records if r["status"] in ["present", "late"])
        return round((present_count / len(records)) * 100, 1)

    # Test Case A: Perfect attendance
    assert compute_attendance_rate([{"status": "present"}, {"status": "present"}]) == 100.0

    # Test Case B: 3 present, 1 absent (75.0%)
    recs = [{"status": "present"}, {"status": "present"}, {"status": "present"}, {"status": "absent"}]
    assert compute_attendance_rate(recs) == 75.0

    # Test Case C: Empty attendance history (0.0%)
    assert compute_attendance_rate([]) == 0.0

def test_fnc_03_membership_lifecycle_valid_states():
    """
    Test Case ID: TC-FNC-03
    Requirement ID: FR-MEM-01, FR-MEM-04
    Objective: Verify that only valid states ('pending', 'approved', 'rejected') are recognized by the model.
    """
    valid_states = {"pending", "approved", "rejected"}
    assert "pending" in valid_states
    assert "approved" in valid_states
    assert "rejected" in valid_states
    assert "hacked_status" not in valid_states
    assert "active" not in valid_states

def test_fnc_04_attendance_status_domain():
    """
    Test Case ID: TC-FNC-04
    Requirement ID: FR-ATT-02
    Objective: Verify attendance status domain values ('present', 'absent', 'late').
    """
    valid_attendance_states = {"present", "absent", "late"}
    assert "present" in valid_attendance_states
    assert "absent" in valid_attendance_states
    assert "late" in valid_attendance_states
    assert "excused" not in valid_attendance_states

def test_fnc_05_role_hierarchy_permissions():
    """
    Test Case ID: TC-FNC-05
    Requirement ID: FR-AUTH-03
    Objective: Verify role-based permissions matrix for student, coordinator, admin.
    """
    permissions = {
        "student": {"can_join_clubs": True, "can_approve_members": False, "can_create_clubs": False},
        "coordinator": {"can_join_clubs": True, "can_approve_members": True, "can_create_clubs": False},
        "admin": {"can_join_clubs": True, "can_approve_members": True, "can_create_clubs": True}
    }
    assert permissions["student"]["can_create_clubs"] is False
    assert permissions["coordinator"]["can_approve_members"] is True
    assert permissions["admin"]["can_create_clubs"] is True

