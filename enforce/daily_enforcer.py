import json
from datetime import date

from gpt.job_matcher import evaluate_job
from resume.customizer import customize_resume, generate_cover_letter
from outreach.dm_generator import generate_dm

def run_daily_enforcer():
    with open("data/jobs_filtered.json") as f:
        jobs = json.load(f)

    with open("data/resume.txt") as f:
        base_resume = f.read()

    today = date.today().isoformat()
    action_pack = {
        "date": today,
        "applications": [],
        "startup_dm": None
    }

    for job in jobs:
        evaluation = evaluate_job(job, base_resume)

        if evaluation["decision"] == "APPLY":
            custom_resume = customize_resume(job, base_resume)
            cover_letter = generate_cover_letter(job, base_resume)

            action_pack["applications"].append({
                "company": job.get("company_name"),
                "role": job.get("title"),
                "resume": custom_resume,
                "cover_letter": cover_letter
            })

        if len(action_pack["applications"]) >= 2:
            break

    if jobs:
        startup = jobs[0]
        action_pack["startup_dm"] = generate_dm(
            company=startup.get("company_name", "Startup"),
            role=startup.get("title", "Engineer"),
            founder_name="Founder",
            your_name="Niranjan"
        )

    with open(f"data/action_pack_{today}.json", "w", encoding="utf-8") as f:
        json.dump(action_pack, f, indent=2)

    print("=== DAILY ACTION PACK GENERATED ===")
    print(json.dumps(action_pack, indent=2))


if __name__ == "__main__":
    run_daily_enforcer()
