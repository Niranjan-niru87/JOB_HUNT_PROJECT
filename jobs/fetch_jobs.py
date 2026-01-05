import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv  # ✅ REQUIRED IMPORT

load_dotenv("config/secrets.env")

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

QUERIES = [
    "Software Developer Fresher Bangalore",
    "AI Engineer Fresher Bangalore",
    "Software Developer Intern Remote",
    "AI Intern Hyderabad"
]

def fetch_jobs():
    if not SERPAPI_KEY:
        raise Exception("SERPAPI_KEY NOT LOADED")

    all_jobs = []

    for query in QUERIES:
        params = {
            "engine": "google_jobs",
            "q": query,
            "hl": "en",
            "api_key": SERPAPI_KEY
        }

        res = requests.get("https://serpapi.com/search", params=params)
        data = res.json()

        for job in data.get("jobs_results", []):
            job["fetched_at"] = datetime.utcnow().isoformat()
            all_jobs.append(job)

    with open("data/jobs_raw.json", "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=2)

    print(f"[FETCH] Collected {len(all_jobs)} raw jobs")

if __name__ == "__main__":
    fetch_jobs()
