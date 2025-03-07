import time
import os
import logging

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger()

# Links
SEARCH_PAGE = "https://clinicaltrials.gov/search"

# XPaths
DOWNLOAD_BUTTON = '//*[@id="main-content"]/ctg-search-results-page/div[2]/section/div/div/div/ctg-search-results-list/div[1]/div/ctg-search-action-bar/div/div[1]/div[1]/ctg-download' # opens download options popup
# The following are in popup
CSV_RADIO_OPTION = '//*[@id="download"]/div/div/div/div/div[1]/section[1]/div[2]/label'
ALL_STUDIES_RADIO_OPTION = '//*[@id="download"]/div/div/div/div/div[1]/section[2]/div[2]/label'
DESELECT_ALL = '//*[@id="download"]/div/div/div/div/div[1]/section[3]/ctg-popular-fields-selector/div[1]/div/button[2]'
NCT_CHECKBOX = '//*[@id="download"]/div/div/div/div/div[1]/section[3]/ctg-popular-fields-selector/div[2]/div[1]/label'
STUDY_TITLE_CHECKBOX = '//*[@id="download"]/div/div/div/div/div[1]/section[3]/ctg-popular-fields-selector/div[2]/div[2]/label'
CONDITIONS_CHECKBOX = '//*[@id="download"]/div/div/div/div/div[1]/section[3]/ctg-popular-fields-selector/div[2]/div[8]/label'
SPONSOR_CHECKBOX = '//*[@id="download"]/div/div/div/div/div[1]/section[3]/ctg-popular-fields-selector/div[2]/div[13]/label'
CONFIRM_DOWNLOAD_BUTTON = '//*[@id="download"]/div/div/div/div/div[2]/ul/li[1]/button' # actually downloads file

DOWNLOAD_DIRECTORY = os.environ.get("DOWNLOAD_DIR", "")


def download_wait(timeout=600):
    start_time = time.time()
    dl_wait = True
    while dl_wait:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(DOWNLOAD_DIRECTORY):
            if fname.endswith('ctg-studies.csv.crdownload'): # XXX may not work if chrome increments the file name
                dl_wait = True
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Spent more than {timeout} seconds waiting for ClinicalTrials.gov download")


class ClinicalTrialsScraperFactory:
    def __init__(self, chrome_options=None, driver=None):
        if driver is not None:
            self.driver = driver
        else:
            if chrome_options is None:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("window-size=1200x600")
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--no-sandbox')
                prefs = {
                    "download.default_directory": DOWNLOAD_DIRECTORY,
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True
                }
                chrome_options.add_experimental_option("prefs", prefs)
            self.driver = webdriver.Remote('remote_chromedriver:4444/wd/hub', options=chrome_options)

    def wait_for_element(self, xpath, delay=15): # XXX: maybe EC.element_to_be_clickable is better
        WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def download_csv(self):
        try:
            actions = ActionChains(self.driver)
            self.driver.get(SEARCH_PAGE)
            self.wait_for_element(DOWNLOAD_BUTTON)
            self.driver.find_element(By.XPATH, DOWNLOAD_BUTTON).click()
            self.driver.find_element(By.XPATH, CSV_RADIO_OPTION).click()
            self.driver.find_element(By.XPATH, ALL_STUDIES_RADIO_OPTION).click()
            self.driver.find_element(By.XPATH, DESELECT_ALL).click()
            self.driver.find_element(By.XPATH, NCT_CHECKBOX).click()
            self.driver.find_element(By.XPATH, STUDY_TITLE_CHECKBOX).click()
            conditions_checkbox = self.driver.find_element(By.XPATH, CONDITIONS_CHECKBOX)
            actions.move_to_element(conditions_checkbox).perform()
            conditions_checkbox.click()
            sponsor_checkbox = self.driver.find_element(By.XPATH, SPONSOR_CHECKBOX)
            actions.move_to_element(sponsor_checkbox).perform()
            sponsor_checkbox.click()
            confirm_download_button = self.driver.find_element(By.XPATH, CONFIRM_DOWNLOAD_BUTTON)
            actions.move_to_element(confirm_download_button).perform()
            confirm_download_button.click()
            logger.debug("Commencing download")
            download_wait()
        finally:
            # self.quit()
            pass

    def quit(self):
        self.driver.quit()