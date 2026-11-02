"""
Selenium 4 Fixtures Configuration
Objective: Provide automated WebDriver lifecycle management for headless browser testing.
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def chrome_driver():
    """
    Session-scoped headless Chrome WebDriver fixture.
    Initializes Chrome in headless mode with sandboxing disabled for CI/CD compatibility.
    """
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(6)
    yield driver
    driver.quit()
