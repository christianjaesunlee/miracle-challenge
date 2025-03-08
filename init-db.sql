-- init-db.sql: This file is automatically executed by MySQL container
-- **only** when the database is first created (fresh volume).

-- Switch to your database
USE mydatabase;

CREATE TABLE IF NOT EXISTS us (
    study_id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(512),
    conditions VARCHAR(1024),
    sponsor VARCHAR(512),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS eu (
    study_id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(512),
    conditions VARCHAR(1024), -- the longest condition as of this writing is >11000 characters, so we'll just truncate it
    sponsor VARCHAR(512),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS combined_trials (
    study_id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(512),
    conditions VARCHAR(1024),
    sponsor VARCHAR(512),
    source VARCHAR(32),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- to keep track of the number of trials compared to -1 week
CREATE TABLE IF NOT EXISTS trial_count (
    snapshot_date TIMESTAMP,
    trial_count INT
);