# XXX: make sure to include the limit parameter twice for this one!
limit_sponsors = """WITH sponsor_counts AS (
    SELECT
        sponsor,
        COUNT(*) AS value
    FROM combined_trials
    GROUP BY sponsor
),
ranked AS (
    SELECT
        sponsor,
        value,
        RANK() OVER (ORDER BY value DESC) AS rk
    FROM sponsor_counts
)
SELECT
  CASE 
    WHEN rk <= %s THEN sponsor
    ELSE 'Other'
  END AS name,
  SUM(value) AS value
FROM ranked
GROUP BY
  CASE 
    WHEN rk <= %s THEN sponsor
    ELSE 'Other'
  END
ORDER BY value DESC;"""

unlimited_sponsors = "SELECT sponsor as name, COUNT(*) AS value FROM combined_trials GROUP BY sponsor ORDER BY value DESC;"

compare_week = "SELECT * FROM trial_count WHERE snapshot_date >= DATE_SUB(NOW(), INTERVAL 7 DAY)"

conditions = "SELECT conditions FROM combined_trials"

us_count = "SELECT count(*) FROM us"

eu_count = "SELECT count(*) FROM eu"