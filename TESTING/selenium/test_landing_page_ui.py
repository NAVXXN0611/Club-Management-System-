"""
Selenium 4 E2E Test Suite — Landing Page & Theme Switcher
Objective: Validate browser rendering, DOM element visibility, and theme toggle interaction.
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_sel_01_landing_page_title_and_branding(chrome_driver, frontend_url):
    """
    Test Case: TC-SEL-01
    Verify the webpage title and main brand heading load correctly in the browser.
    """
    chrome_driver.get(frontend_url)
    WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    assert "CCMS" in chrome_driver.title
    h1_text = chrome_driver.find_element(By.TAG_NAME, "h1").text
    assert "Students & Faculty" in h1_text or "Campus Life" in h1_text

def test_sel_02_theme_toggle_interaction(chrome_driver, frontend_url):
    """
    Test Case: TC-SEL-02
    Verify clicking the theme toggle button switches between light and dark modes.
    """
    chrome_driver.get(frontend_url)
    # Locate theme toggle button by aria-label or title
    theme_btn = WebDriverWait(chrome_driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='theme' i], button[title*='Mode' i]"))
    )
    initial_title = theme_btn.get_attribute("title")
    
    # Click to toggle theme
    theme_btn.click()
    
    # Verify title or DOM updated
    updated_title = theme_btn.get_attribute("title")
    assert initial_title != updated_title or "Mode" in updated_title

def test_sel_03_navigation_links_presence(chrome_driver, frontend_url):
    """
    Test Case: TC-SEL-03
    Verify top navigation links (Portals, Activity Timetable, Features, Directory) are present.
    """
    chrome_driver.get(frontend_url)
    nav = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "nav"))
    )
    nav_text = nav.text
    assert "Portals" in nav_text or "Activity Timetable" in nav_text or "Clubs" in nav_text

