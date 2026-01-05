import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv("config/secrets.env")

# ✅ DEFINE CLIENT (THIS WAS MISSING)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a ruthless technical recruiter.

Rules:
- Reject roles requiring more than 1 year experience
- Reject senior/lead roles
- Score match from 0–100
- Rewrite ONLY relevant resume bullets
- Be strict. No mercy.
"""

def evaluate_job(job, resume_text):
    prompt = f"""
JOB DESCRIPTION:
{job.get('description','')}

CANDIDATE RESUME:
{resume_text}

You MUST return ONLY valid JSON.
No markdown.
No explanation.
No extra text.

JSON format:
{{
  "match_score": number,
  "decision": "APPLY or REJECT",
  "rewritten_bullets": [string],
  "reason": string
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    raw = response.choices[0].message.content.strip()

    print("=== RAW GPT OUTPUT ===")
    print(raw)

    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError("GPT did not return JSON")

    return json.loads(match.group())
