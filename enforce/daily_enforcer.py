print("=== DAILY ENFORCER FILE LOADED ===")

import json
import os
from datetime import date
from dotenv import load_dotenv

# Load env
load_dotenv("config/secrets.env")

# Imports from your project
from gpt.job_matcher import evaluate_job
from resume.customizer import customize_resume, generate_cover_letter
from outreach.dm_generator import generate_dm
from notify.emailer import send_email


def run_daily_enforcer():
    print("=== RUN_DAILY_ENFORCER CALLED ===")

    # ---------- LOAD DATA ----------
    try:
        with open("data/jobs_filtered.json", encoding="utf-8") as f:
            jobs = json.load(f)
        print(f"[INFO] Jobs loaded: {len(jobs)}")
    except Exception as e:
        print("[ERROR] Failed to load jobs_filtered.json:", e)
        return

    try:
        with open("data/resume.txt", encoding="utf-8") as f:
            base_resume = f.read()
        print("[INFO] Resume loaded")
    except Exception as e:
        print("[ERROR] Failed to load resume.txt:", e)
        return

    # ---------- DATE ----------
    today = date.today().isoformat()
    print("[INFO] Date:", today)

    # ---------- ACTION PACK ----------
    action_pack = {
        "date": today,
        "applications": [],
        "startup_dm": None
    }

    # ---------- PROCESS JOBS ----------
    for job in jobs:
        print("[INFO] Evaluating job:", job.get("title"))

        evaluation = evaluate_job(job, base_resume)

        if evaluation.get("decision") == "APPLY":
            print("[INFO] Job accepted by GPT")

            custom_resume = customize_resume(job, base_resume)
            cover_letter = generate_cover_letter(job, base_resume)

            action_pack["applications"].append({
                "company": job.get("company_name", "Unknown Company"),
                "role": job.get("title", "Unknown Role"),
                "resume": custom_resume,
                "cover_letter": cover_letter
            })

        if len(action_pack["applications"]) >= 2:
            break

    # ---------- STARTUP DM ----------
    if jobs:
        startup = jobs[0]
        action_pack["startup_dm"] = generate_dm(
            company=startup.get("company_name", "Startup"),
            role=startup.get("title", "Engineer"),
            founder_name="Founder",
            your_name="Niranjan"
        )

    # ---------- SAVE ACTION PACK ----------
    try:
        os.makedirs("data", exist_ok=True)
        with open(f"data/action_pack_{today}.json", "w", encoding="utf-8") as f:
            json.dump(action_pack, f, indent=2)
        print("[INFO] Action pack saved")
    except Exception as e:
        print("[ERROR] Failed to save action pack:", e)
        return

    # ---------- EMAIL ----------
    EMAIL = os.getenv("ALERT_EMAIL")

    if not EMAIL:
        print("[WARNING] ALERT_EMAIL not set. Skipping email.")
        return

    subject = f"📌 Daily Job Action Pack – {today}"

    body = "Good morning Niranjan,\n\nToday's Action Pack:\n\n"

    if action_pack["applications"]:
        body += "Apply to:\n"
        for app in action_pack["applications"]:
            body += f"- {app['role']} @ {app['company']}\n"
    else:
        body += "No applications today.\n"

    body += "\nStartup Outreach:\n"
    body += (action_pack["startup_dm"] or "No DM generated") + "\n\n"

    body += "Focus today:\n"
    body += "✔ Apply to jobs\n✔ Send DM\n✔ Practice skills\n\n"
    body += "– Your Job Automation System"

    try:
        send_email(subject, body, EMAIL)
        print("[SUCCESS] Email sent")
    except Exception as e:
        print("[ERROR] Email sending failed:", e)

    print("=== DAILY ACTION PACK COMPLETE ===")


# ---------- ENTRY POINT ----------
if __name__ == "__main__":
    print("=== DAILY ENFORCER MAIN STARTED ===")
    run_daily_enforcer()
