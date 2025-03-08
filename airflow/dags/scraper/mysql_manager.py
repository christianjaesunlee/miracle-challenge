import csv
import os
import time
import logging

import mysql.connector

logger = logging.getLogger()

class MySQLManager:
    def __init__(self):
        # Retrieve DB connection info from environment variables
        db_host = os.environ.get("DB_HOST", "localhost")
        db_user = os.environ.get("DB_USER", "root")
        db_password = os.environ.get("DB_PASSWORD", "")
        db_name = os.environ.get("DB_NAME", "")
        self.download_dir = os.environ.get("DOWNLOAD_DIR", "")

        # Wait a bit to ensure DB is ready (optional safeguard if DB initialization is slow)
        time.sleep(5)

        # Connect to the MySQL database
        try:
            self.conn = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name
            )
            logger.debug("Connected to MySQL")
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def close(self):
        self.cursor.close()
        self.conn.close()

    def update_raw_table(self, file, table):
        with open(f'{self.download_dir}/{file}') as csv_file:
            csv_file_reader = csv.reader(csv_file)
            csv_file_reader.__next__()
            for row in csv_file_reader:
                sql = f'REPLACE INTO {table} (study_id, name, conditions, sponsor) VALUES (%s, %s, %s, %s)'
                self.cursor.execute(sql, (row[0], row[1][:512], row[2][:1024], row[3][:512]))
        self.conn.commit()

    def update_raw_us(self):
        logger.info("Updating us table")
        self.update_raw_table("ctg-studies.csv", "us") # XXX: maybe use constants

    def update_raw_eu(self):
        logger.info("Updating eu table")
        self.update_raw_table("eudract_studies.csv", "eu")

    def update_combined(self):
        logger.info("Updating combined table")
        self.cursor.execute(
            "REPLACE INTO combined_trials (study_id, name, conditions, sponsor, source) "
            "SELECT study_id, name, conditions, sponsor, 'us' "
            "FROM us "
            "UNION ALL "
            "SELECT study_id, name, conditions, sponsor, 'eu' "
            "FROM eu;"
        )
        logger.info("Updating trial count table")
        self.cursor.execute("INSERT INTO trial_count (snapshot_date, trial_count) SELECT NOW(), COUNT(*) FROM combined_trials")
        self.conn.commit()