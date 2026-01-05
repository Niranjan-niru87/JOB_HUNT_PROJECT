import json
from resume.customizer import customize_resume, generate_cover_letter

with open("data/jobs_filtered.json") as f:
    jobs = json.load(f)

with open("data/resume.txt") as f:
    resume = f.read()

job = jobs[0]

custom_resume = customize_resume(job, resume)
cover_letter = generate_cover_letter(job, resume)

print("=== CUSTOM RESUME ===")
print(custom_resume)

print("\n=== COVER LETTER ===")
print(cover_letter)
