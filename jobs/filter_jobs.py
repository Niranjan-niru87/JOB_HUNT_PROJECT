import json
from datetime import datetime, timedelta

print("[FILTER] Script started")  # 🔥 forced output

MAX_HOURS = 24
LOCATIONS = ["Bangalore", "Hyderabad", "Remote"]

def is_fresher_friendly(desc):
    if not desc:
        return False
    desc = desc.lower()
    bad_words = ["2+ years", "3+ years", "senior", "lead", "manager"]
    return not any(bad in desc for bad in bad_words)

def filter_jobs():
    print("[FILTER] Loading raw jobs file")

    try:
        with open("data/jobs_raw.json", encoding="utf-8") as f:
            jobs = json.load(f)
    except Exception as e:
        print("[FILTER] ERROR loading jobs_raw.json:", e)
        return

    print(f"[FILTER] Raw jobs found: {len(jobs)}")

    filtered = []

    for job in jobs:
        desc = job.get("description", "")
        location = job.get("location", "")

        if not is_fresher_friendly(desc):
            continue

        if not any(loc.lower() in location.lower() for loc in LOCATIONS):
            continue

        filtered.append(job)

        if len(filtered) >= 5:
            break

    with open("data/jobs_filtered.json", "w", encoding="utf-8") as f:
        json.dump(filtered, f, indent=2)

    print(f"[FILTER] Final jobs kept: {len(filtered)}")

if __name__ == "__main__":
    filter_jobs()
