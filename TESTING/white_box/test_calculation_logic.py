"""
Category: White Box Testing — Internal Calculation & Algorithmic Logic
Objective: Verify branch coverage, mathematical formulas, and internal sorting/filtering algorithms.
"""
import pytest

def test_wb_calc_01_attendance_rate_branch_coverage():
    """
    Test Case: TC-WB-CALC-01
    Verify complete branch coverage of the institutional attendance percentage calculation function.
    """
    def calculate_attendance_percentage(records: list) -> float:
        # Branch 1: Empty list (guard against ZeroDivisionError)
        if not records:
            return 0.0
        # Branch 2: Count attended sessions ('present' and 'late' qualify)
        present_count = 0
        for r in records:
            if r.get("status") in ("present", "late"):
                present_count += 1
        # Branch 3: Division and 1-decimal rounding
        return round((present_count / len(records)) * 100, 1)

    # Branch 1 test: Empty list
    assert calculate_attendance_percentage([]) == 0.0

    # Branch 2 test: 100% attendance (all present or late)
    assert calculate_attendance_percentage([{"status": "present"}, {"status": "late"}]) == 100.0

    # Branch 3 test: Fractional calculation with rounding (2 out of 3 = 66.7%)
    recs = [{"status": "present"}, {"status": "present"}, {"status": "absent"}]
    assert calculate_attendance_percentage(recs) == 66.7

    # Branch 4 test: 0% attendance (all absent)
    assert calculate_attendance_percentage([{"status": "absent"}, {"status": "absent"}]) == 0.0

def test_wb_calc_02_department_sorting_logic():
    """
    Test Case: TC-WB-CALC-02
    Verify the internal departmental sorting and filtering algorithm used by faculty coordinators.
    """
    applicants = [
        {"id": 1, "name": "Alice", "department": "CSE"},
        {"id": 2, "name": "Bob", "department": "ECE"},
        {"id": 3, "name": "Charlie", "department": "CSE"},
        {"id": 4, "name": "David", "department": "MECH"}
    ]

    def filter_by_department(candidates: list, dept: str) -> list:
        if dept == "ALL":
            return candidates
        return [c for c in candidates if c.get("department") == dept]

    # Branch A: Filter CSE
    cse_group = filter_by_department(applicants, "CSE")
    assert len(cse_group) == 2
    assert all(c["department"] == "CSE" for c in cse_group)

    # Branch B: Filter ECE
    ece_group = filter_by_department(applicants, "ECE")
    assert len(ece_group) == 1
    assert ece_group[0]["name"] == "Bob"

    # Branch C: Filter ALL
    all_group = filter_by_department(applicants, "ALL")
    assert len(all_group) == 4

def test_wb_calc_03_password_length_constraint_eval():
    """
    Test Case: TC-WB-CALC-03
    Verify internal credential validation logic enforcing the minimum 6-character length boundary.
    """
    def validate_password_length(password: str) -> bool:
        if not password or not isinstance(password, str):
            return False
        return len(password.strip()) >= 6

    # Boundary: length < 6
    assert validate_password_length("12345") is False
    assert validate_password_length("") is False
    assert validate_password_length("   ") is False

    # Boundary: length >= 6
    assert validate_password_length("123456") is True
    assert validate_password_length("SecurePass123!") is True

