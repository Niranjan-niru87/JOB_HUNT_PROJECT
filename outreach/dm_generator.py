import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("config/secrets.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_dm(company, role, founder_name, your_name="Your Name"):
    prompt = f"""
You are helping a fresher reach out to a startup founder.

Rules:
- Max 4–5 lines
- No begging
- No resume dump
- No corporate tone
- Sound curious and respectful
- One specific skill or project mention

Details:
Company: {company}
Role: {role}
Founder/CTO name: {founder_name}
Candidate name: {your_name}

Write a concise LinkedIn DM.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()
