from scraper.clinicaltrials_scraper import ClinicalTrialsScraperFactory
from scraper.eudract_scraper import EudraCTScraperFactory
from scraper.mysql_manager import MySQLManager

# For a future refactor, maybe use completely functional programming rather than object oriented
def run_clinical_trials_scraper():
    ct_scraper = ClinicalTrialsScraperFactory()
    ct_scraper.download_csv()
    ct_scraper.quit()

def run_eudract_scraper():
    eudract_scraper = EudraCTScraperFactory()
    eudract_scraper.get_data_as_csv()
    eudract_scraper.quit()

def update_us():
    mysql = MySQLManager()
    mysql.update_raw_us()
    mysql.close()

def update_eu():
    mysql = MySQLManager()
    mysql.update_raw_eu()
    mysql.close()

def update_combined():
    mysql = MySQLManager()
    mysql.update_combined()
    mysql.close()