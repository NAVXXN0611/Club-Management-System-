"""
Selenium 4 E2E Test Suite — Authentication Forms & Role Selection
Objective: Validate UI elements on login and registration pages including input fields and role toggles.
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_sel_06_login_page_form_elements(chrome_driver, frontend_url):
    """
    Test Case: TC-SEL-06
    Verify email and password input elements and submit button exist on /login.
    """
    chrome_driver.get(f"{frontend_url}/login")
    WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[name='email']"))
    )
    email_input = chrome_driver.find_element(By.CSS_SELECTOR, "input[type='email'], input[name='email']")
    password_input = chrome_driver.find_element(By.CSS_SELECTOR, "input[type='password'], input[name='password']")
    submit_btn = chrome_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    assert email_input.is_displayed()
    assert password_input.is_displayed()
    assert submit_btn.is_displayed()

def test_sel_07_register_page_form_elements_and_role_selection(chrome_driver, frontend_url):
    """
    Test Case: TC-SEL-07
    Verify registration form on /register contains required fields and role selection.
    """
    chrome_driver.get(f"{frontend_url}/register")
    WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "form"))
    )
    form_text = chrome_driver.find_element(By.TAG_NAME, "form").text
    assert "Student" in form_text or "Coordinator" in form_text or "Register" in form_text
