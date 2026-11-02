"""
Selenium 4 Fixtures Configuration
Objective: Provide automated WebDriver lifecycle management for headless browser testing with self-healing driver resolution.
"""
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def chrome_driver():
    """
    Session-scoped headless Chrome WebDriver fixture.
    Configures headless mode, sandboxing, and binary path discovery.
    """
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-extensions')
    options.add_argument('--ignore-certificate-errors')

    # Common Windows Chrome binary paths
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]
    for p in chrome_paths:
        if os.path.exists(p):
            options.binary_location = p
            break

    try:
        driver = webdriver.Chrome(options=options)
    except Exception as exc:
        pytest.skip(f"Chrome WebDriver could not be initialized: {exc}")

    driver.implicitly_wait(8)
    yield driver
    try:
        driver.quit()
    except Exception:
        pass
