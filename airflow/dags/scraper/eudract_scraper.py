import os
import logging

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger()

# Links
SEARCH_PAGE = 'https://www.clinicaltrialsregister.eu/ctr-search/search?query='

# XPaths
RESULTS = '//*[@id="tabs-1"]/div[3]'
NEXT_PAGE = '//*[@id="tabs-1"]/div[2]/a[9]'

DOWNLOAD_DIRECTORY = os.environ.get("DOWNLOAD_DIR", "")

# XXX: The study titles are clipped. I could get the full titles by downloading the full trial details, but that takes
# much longer and I deemed it unnecessary for the sake of the take home challenge.
class EudraCTScraperFactory:
    def __init__(self, chrome_options=None, driver=None):
        if driver is not None:
            self.driver = driver
        else:
            if chrome_options is None:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("window-size=1200x600")
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--no-sandbox')
            self.driver = webdriver.Remote('remote_chromedriver:4444/wd/hub', options=chrome_options)

    def wait_for_element(self, xpath, delay=15):
        WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def get_data_as_csv(self, pages=3):
        try:
            df = pd.DataFrame(columns = ["EudraCT Number", "Study Title", "Conditions", "Sponsor"])
            for page in range(1, pages + 1):
                logger.debug(f"Scraping page {page}")
                self.driver.get(f"{SEARCH_PAGE}&page={page}")
                self.wait_for_element(RESULTS)
                studies = self.driver.find_element(By.XPATH, RESULTS).find_elements(By.XPATH,".//table[@class='result']/tbody")
                for i in studies:
                    eudract_number = i.find_element(By.XPATH, './/tr[1]/td[1]').text[16:]
                    sponsor = i.find_element(By.XPATH, './/tr[2]/td').text[13:]
                    title = i.find_element(By.XPATH, './/tr[3]/td').text[12:]
                    condition = i.find_element(By.XPATH, './/tr[4]/td').text[19:]
                    row = {"EudraCT Number": eudract_number, "Study Title": title, "Conditions": condition, "Sponsor": sponsor}
                    df.loc[len(df)] = row
            logger.debug("Saving as CSV")
            df.to_csv(f"{DOWNLOAD_DIRECTORY}/eudract_studies.csv")
            # XXX: right now I am putting all the results into a Pandas DataFrame, and then writing all of it at once
            # to a csv file. In the future, if we were to incorporate significantly more results, this should be changed
            # to either incrementally add to a csv file, create a csv file in parts, or upload directly to MySQL
        finally:
            # self.quit()
            pass

    def quit(self):
        self.driver.quit()