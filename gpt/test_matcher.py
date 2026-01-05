print("=== TEST MATCHER STARTED ===")

import sys
import os
print("Python executable:", sys.executable)
print("Current working directory:", os.getcwd())

import json
from gpt.job_matcher import evaluate_job

print("=== IMPORT SUCCESSFUL ===")

with open("data/jobs_filtered.json") as f:
    jobs = json.load(f)

with open("data/resume.txt") as f:
    resume = f.read()

print("Jobs loaded:", len(jobs))

result = evaluate_job(jobs[0], resume)

print("=== GPT RESPONSE ===")
print(json.dumps(result, indent=2))

