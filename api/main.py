from collections import Counter
import os

from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "")

@app.route("/api/us_count")
def get_total_us_trials():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT count(*) FROM us")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/eu_count")
def get_total_eu_trials():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT count(*) FROM eu")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/sponsor")
def get_sponsor_breakdown():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT t.sponsor, COUNT(*) AS total_count FROM combined_trials t GROUP BY t.sponsor ORDER BY t.sponsor;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/condition")
def get_condition_breakdown():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT conditions FROM combined_trials")
        rows = cursor.fetchall()
        condition_counter = Counter()
        for i in rows:
            condition_counter.update(i[0].split("|"))
        cursor.close()
        conn.close()
        return jsonify(condition_counter)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return "Hello"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
