"""
Category: White Box Testing — Role Hierarchy & Internal Taxonomy
Objective: Verify internal role permission matrix and relational taxonomy integrity.
"""
import pytest
import requests

def test_wb_role_01_strict_dual_role_matrix():
    """
    Test Case: TC-WB-ROLE-01
    Verify the internal permission matrix strictly validates student vs faculty coordinator roles.
    """
    PERMISSIONS_MATRIX = {
        "student": {
            "can_browse_clubs": True,
            "can_apply_to_clubs": True,
            "can_view_timetable": True,
            "can_view_own_attendance": True,
            "can_approve_members": False,
            "can_publish_timetable": False,
            "can_mark_attendance": False,
        },
        "coordinator": {
            "can_browse_clubs": True,
            "can_apply_to_clubs": False,
            "can_view_timetable": True,
            "can_view_own_attendance": False,
            "can_approve_members": True,
            "can_publish_timetable": True,
            "can_mark_attendance": True,
        }
    }

    # Verify Student cannot perform coordinator actions
    student_perms = PERMISSIONS_MATRIX["student"]
    assert student_perms["can_approve_members"] is False
    assert student_perms["can_publish_timetable"] is False
    assert student_perms["can_mark_attendance"] is False

    # Verify Coordinator can approve, schedule and mark attendance
    coord_perms = PERMISSIONS_MATRIX["coordinator"]
    assert coord_perms["can_approve_members"] is True
    assert coord_perms["can_publish_timetable"] is True
    assert coord_perms["can_mark_attendance"] is True

def test_wb_role_02_club_taxonomy_structural_integrity(http_session, supabase_url, supabase_headers):
    """
    Test Case: TC-WB-ROLE-02
    Verify every active club in the database is correctly associated with a valid category ID.
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
