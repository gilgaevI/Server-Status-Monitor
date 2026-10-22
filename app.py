import os
import requests
from flask import Flask, jsonify
import psycopg2
import redis
from datetime import datetime

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres"),
        user=os.getenv("DB_USER", "user"),
        password=os.getenv("DB_PASSWORD", "pass"),
        dbname=os.getenv("DB_NAME", "appdb")
    )

def get_redis():
    return redis.Redis(host="redis", port=6379, decode_responses=True)

def check_site(url):
    try:
        r = requests.get(url, timeout=5)
        return "UP" if r.status_code == 200 else "DOWN"
    except:
        return "DOWN"

@app.route("/")
def index():
    r = get_redis()
    cached = r.get("statuses")

    if cached:
        return f"<h1>Status Board (Cached)</h1><pre>{cached}</pre>"

    sites = ["https://google.com", "https://github.com", "https://nonexistent.com"]
    results = {}

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS checks (
            id SERIAL PRIMARY KEY,
            url VARCHAR(255),
            status VARCHAR(10),
            checked_at TIMESTAMP
        )
    """)

    for site in sites:
        status = check_site(site)
        results[site] = status

        cur.execute(
            "INSERT INTO checks (url, status, checked_at) VALUES (%s, %s, %s)",
            (site, status, datetime.now())
        )

    conn.commit()
    cur.close()
    conn.close()
 
    r.setex("statuses", 30, str(results))

    return f"<h1>Status Board</h1><pre>{results}</pre>"

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
