import os
import logging
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# -----------------------------
# Create folders for logs/screenshots
# -----------------------------
if not os.path.exists("logs"):
    os.makedirs("logs")

if not os.path.exists("screenshots"):
    os.makedirs("screenshots")


# -----------------------------
# Logging Configuration
# -----------------------------
log_file = f"logs/test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# -----------------------------
# Pytest Fixture (Setup + Teardown)
# -----------------------------
@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login")
    yield driver
    driver.quit()


# -----------------------------
# Screenshot Helper
# -----------------------------
def take_screenshot(driver, name):
    file_path = f"screenshots/{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    driver.save_screenshot(file_path)
    logging.info(f"Screenshot saved: {file_path}")


# -----------------------------
# Main Test Case
# -----------------------------
def test_full_banking_flow(driver):

    wait = WebDriverWait(driver, 15)

    try:
        logging.info("Starting Test Case")

        # ---------------- Manager Login ----------------
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[text()='Bank Manager Login']"))
        ).click()
        logging.info("Clicked Bank Manager Login")

        # ---------------- Add Customer ----------------
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@ng-click='addCust()']"))
        ).click()

        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//input[@ng-model='fName']"))
        ).send_keys("John")

        driver.find_element(By.XPATH, "//input[@ng-model='lName']").send_keys("Doe")
        driver.find_element(By.XPATH, "//input[@ng-model='postCd']").send_keys("12345")
        driver.find_element(By.XPATH, "//button[text()='Add Customer']").click()

        alert = wait.until(EC.alert_is_present())
        logging.info(f"Add Customer Alert: {alert.text}")
        alert.accept()

        # ---------------- Open Account ----------------
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@ng-click='openAccount()']"))
        ).click()

        Select(wait.until(EC.visibility_of_element_located(
            (By.ID, "userSelect"))
        )).select_by_visible_text("John Doe")

        Select(driver.find_element(By.ID, "currency")) \
            .select_by_visible_text("Dollar")

        driver.find_element(By.XPATH, "//button[text()='Process']").click()

        alert = wait.until(EC.alert_is_present())
        logging.info(f"Open Account Alert: {alert.text}")
        alert.accept()

        # ---------------- Go Home ----------------
        driver.find_element(By.XPATH, "//button[text()='Home']").click()

        # ---------------- Customer Login ----------------
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[text()='Customer Login']"))
        ).click()

        Select(wait.until(EC.visibility_of_element_located(
            (By.ID, "userSelect"))
        )).select_by_visible_text("John Doe")

        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        logging.info("Customer Login Successful")

        # ---------------- Deposit ----------------
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@ng-click='deposit()']"))
        ).click()

        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//input[@ng-model='amount']"))
        ).send_keys("1000")

        driver.find_element(By.XPATH, "//button[text()='Deposit']").click()
        logging.info("Deposited 1000")

        # ---------------- Withdraw ----------------
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@ng-click='withdrawl()']"))
        ).click()

        # wait for amount field, clear any previous value then enter amount
        amt_field = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//input[@ng-model='amount']"))
        )
        amt_field.clear()
        amt_field.send_keys("200")

        # make sure the withdraw button is present/clickable before clicking
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[text()='Withdraw']"))
        ).click()
        logging.info("Withdrawn 200")

        # ---------------- Validate Balance ----------------
        # wait for balance element to be present then read its value
        bal_elem = wait.until(EC.presence_of_element_located(
            (By.XPATH, "(//strong)[2]")
        ))

        balance = bal_elem.text.strip()
        logging.info(f"Final Balance fetched: '{balance}'")
        # convert to integer if possible and compare
        try:
            numeric = int(balance)
        except ValueError:
            pytest.fail(f"Balance value is not numeric: {balance}")

        assert numeric == 800, f"Expected balance 800 but got {numeric}"
        logging.info("Balance Validated Successfully")

    except Exception as e:
        logging.error(f"Test Failed: {str(e)}")
        take_screenshot(driver, "failure")
        raise