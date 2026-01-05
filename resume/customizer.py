import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("config/secrets.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def customize_resume(job, base_resume):
    prompt = f"""
You are an ATS-aware resume expert.

JOB DESCRIPTION:
{job.get('description','')}

BASE RESUME:
{base_resume}

Tasks:
1. Rewrite ONLY relevant bullets to match the job
2. Do NOT add fake skills
3. Keep it concise and professional
4. Output plain text only (no markdown)

Return the customized resume.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()


def generate_cover_letter(job, base_resume):
    prompt = f"""
Write a short, human, customized cover letter.

JOB DESCRIPTION:
{job.get('description','')}

CANDIDATE PROFILE:
{base_resume}

Rules:
- Max 150 words
- No clichés
- Sound like a real person
- Mention 1 relevant skill or project
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()
