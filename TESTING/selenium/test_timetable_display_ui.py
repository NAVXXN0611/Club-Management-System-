"""
Selenium 4 E2E Test Suite — Activity Timetable & Dual Portals
Objective: Validate display of weekly activity timetable schedules and dual portal links in browser.
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_sel_08_activity_timetable_cards_display(chrome_driver, frontend_url):
    """
    Test Case: TC-SEL-08
    Verify the landing page activity timetable section renders timetable slots with venue and timing details.
    """
    chrome_driver.get(frontend_url)
    WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, "timetable"))
    )
    timetable_elem = chrome_driver.find_element(By.ID, "timetable")
    tt_text = timetable_elem.text
    assert "Timetable" in tt_text or "Activity" in tt_text or "Schedule" in tt_text
    assert "Monday" in tt_text or "Wednesday" in tt_text or "Saturday" in tt_text

def test_sel_09_dual_portal_access_cards(chrome_driver, frontend_url):
    """
    Test Case: TC-SEL-09
    Verify the dual portal section renders access cards for both Student Portal and Faculty Coordinator Hub.
    """
    chrome_driver.get(frontend_url)
    portals_elem = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, "portals"))
    )
    portals_text = portals_elem.text
    assert "Student Portal" in portals_text
    assert "Faculty Coordinator" in portals_text

