from collections import Counter
import os

import sql_queries

from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app) # XXX

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "")

@app.route("/api/us_count")
def get_total_us_trials():
    """Returns the number of trials from ClinicalTrials.gov (int)"""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql_queries.us_count)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return str(rows[0]["count(*)"])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/eu_count")
def get_total_eu_trials():
    """Returns the number of trials from EudraCT (currently just first 3 pages of results) (int)"""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql_queries.eu_count)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return str(rows[0]["count(*)"])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/sponsor")
def get_sponsor_breakdown():
    """
    Returns each sponsor and the number of times it appears in the clinical trials.
    If the parameter `limit` is provided, then it will return the {limit} most common
    sponsors and their number of appearances, as well as `Other` with the count of all the rest.

    format: [{name: "sponsor1", value: "500"}, {name: "sponsor2", value: "400"}, ...]
    """
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        limit = request.args.get('limit', default=-1, type=int)
        cursor = conn.cursor(dictionary=True)
        if limit < 0:
            cursor.execute(sql_queries.unlimited_sponsors)
        else:
            cursor.execute(sql_queries.limit_sponsors, (limit,limit))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/compare_week")
def get_compare_week():
    """
    Returns the number of trials for each time the pipeline was run in the past week, and their dates
    format: [{"snapshot_date":"Sat, 08 Mar 2025 03:20:22 GMT","trial_count":529487}, ...]
    """
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql_queries.compare_week)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/condition")
def get_condition_breakdown():
    """
    Returns conditions and their prevalence in the clinical trials
    format: [{"name":"Other","value":339396},{"name":"Cancer","value":89186}, ...]
    """
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql_queries.conditions)
        rows = cursor.fetchall()
        condition_counter = Counter()
        for i in rows:
            condition_counter.update([classify_condition(i["conditions"])])
        cursor.close()
        conn.close()
        return jsonify([{"name":i, "value":condition_counter[i]} for i in condition_counter])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# These classifications are not perfect, perhaps a future version could use a language model to actually analyze the
# conditions
def classify_condition(condition: str):
    """given a condition, classify it as one of the commonly seen conditions or 'other'"""
    condition = condition.lower()
    if check_match(condition, ["cancer", "leukemia", "lymphoma", "sarcoma", "carcinoma", "myeloma", "melanoma", "tumor"]):
        return "Cancer"
    if check_match(condition, ["diabetes", "sugar", "glucose", "a1c"]):
        return "Diabetes"
    if check_match(condition, ["injury", "trauma", "sprain", "fracture", "tear", "torn", "burn", "wound"]):
        return "Injury"
    if check_match(condition, ["depression", "anxiety", "mental illness", "psycholog", "behavior", "emotion", "ptsd"]):
        return "Mental Illness"
    if check_match(condition, ["pain", "fibromyalgia"]):
        return "Pain"
    if check_match(condition, ["dementia", "alzheimer's", "parkinson's", "neurodegenerative"]):
        return "Neurodegenerative"
    if "stroke" in condition:
        return "Stroke"
    if check_match(condition, ["heart", "cardiac", "cardio", "coronary"]):
        return ("Heart")
    return "Other"

def check_match(superstring: str, substrings: list):
    for i in substrings:
        if i in superstring:
            return True
    return False

@app.route("/")
def index():
    return "Hello"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
