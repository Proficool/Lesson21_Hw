import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

@pytest.fixture()
def driver():
    """Pytest fixture to set up and tear down the WebDriver instance."""
    download_dir = "~/Downloads/"

    # Chrome options with download preferences
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    # Set up the WebDriver
    service = Service(ChromeDriverManager().install())
    config_driver = webdriver.Chrome(service=service, options=chrome_options)
    yield config_driver
    config_driver.quit()

def test_task4_2(driver):
    """Test to download a file and verify the download."""
    download_dir = "D:/TeachMeSkills"
    file_name = "file-sample_100kB.doc"

    # Set up explicit wait
    wait = WebDriverWait(driver, 20)

    # Open the website
    driver.get("https://file-examples.com/")

    # Close the cookie window
    close_cookie_window(driver)

    # Click on the Documents menu
    wait.until(EC.element_to_be_clickable((By.ID, "menu-item-27"))).click()
    handle_interstitial_ads(driver)

    print("Current URL after menu click:", driver.current_url)
    assert "index.php/sample-documents-download/" in driver.current_url, "Failed to navigate to documents page"

    # Click the first file link
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".text-right.file-link > a")))
    files = driver.find_elements(By.CSS_SELECTOR, ".text-right.file-link > a")
    files[0].click()
    handle_interstitial_ads(driver)

    print("Current URL after file click:", driver.current_url)
    assert "index.php/sample-documents-download/sample-doc-download/" in driver.current_url, "Failed to navigate to file page"

    # Click the download button
    file_sizes = driver.find_elements(By.CSS_SELECTOR, ".btn.btn-orange.btn-outline.btn-xl.page-scroll.download-button")
    file_sizes[0].click()

    # Check if the file is downloaded
    check_download(wait, download_dir, file_name)

def close_cookie_window(driver):
    """Close the cookie banner if present."""
    try:
        cookie_close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "fc-button.fc-cta-consent.fc-primary-button"))
        )
        cookie_close_button.click()
    except Exception:
        print("No cookie banner to close.")

def handle_interstitial_ads(driver):
    """Handle interstitial ads if present."""
    try:
        wait = WebDriverWait(driver, 5)
        ad_iframes = driver.find_elements(By.TAG_NAME, "iframe")

        for iframe in ad_iframes:
            driver.switch_to.frame(iframe)
            try:
                close_btn = wait.until(EC.element_to_be_clickable((By.ID, "dismiss-button")))
                close_btn.click()
                print("Interstitial ad closed.")
                driver.switch_to.default_content()
                return
            except:
                driver.switch_to.default_content()
    except Exception as e:
        print(f"Error handling interstitial ads: {e}")
    finally:
        driver.switch_to.default_content()

def check_download(wait, download_dir, file_name):
    """Wait for the file to appear in the download directory."""
    file_path = os.path.join(download_dir, file_name)
    wait.until(lambda driver: os.path.exists(file_path), "File not downloaded")
    print("Download completed!")
