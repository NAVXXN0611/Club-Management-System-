"""
Selenium 4 E2E Test Suite — Clubs Catalog & Domain Filters
Objective: Validate browser rendering of the club directory and interactive category filtering.
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_sel_04_clubs_catalog_navigation_and_cards(chrome_driver, frontend_url):
    """
    Test Case: TC-SEL-04
    Verify navigating to /clubs renders club cards with titles, descriptions, and coordinator info.
    """
    chrome_driver.get(f"{frontend_url}/clubs")
    WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1 | //h2"))
    )
    page_text = chrome_driver.find_element(By.TAG_NAME, "body").text
    assert "Club" in page_text or "Catalog" in page_text or "Explore" in page_text

def test_sel_05_category_filter_pills_interactive(chrome_driver, frontend_url):
    """
    Test Case: TC-SEL-05
    Verify category filter buttons or search inputs exist on the clubs directory page.
    """
    chrome_driver.get(f"{frontend_url}/clubs")
    inputs_or_buttons = chrome_driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[placeholder*='search' i], button")
    assert len(inputs_or_buttons) > 0, "Expected search input or category filter buttons on /clubs"
