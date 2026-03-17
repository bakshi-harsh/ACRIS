import json
import re
import spacy
import pdfplumber
from pathlib import Path

# Load spacy model
import en_core_web_sm
nlp = en_core_web_sm.load()

# Load skills database
skills_path = Path("skills.json")

with open(skills_path, "r") as f:
    SKILLS_DB = json.load(f)


def extract_text_from_pdf(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text.lower()


def extract_skills(text):

    skills_found = []

    for skill in SKILLS_DB:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            skills_found.append(skill)

    return list(set(skills_found))


def parse_resume(file_path):

    text = extract_text_from_pdf(file_path)

    print("\n=========== RESUME TEXT PREVIEW ===========")
    print(text[:1000])

    skills = extract_skills(text)

    result = {
        "skills": skills,
        "experience": "Not specified"
    }

    print("Parsed Result:", result)

    return result


def select_relevant_skills(job_role, resume_skills):

    with open("job_skills.json") as f:
        job_skill_map = json.load(f)

    # normalize role
    role = job_role.lower().replace(" ", "_")

    if role not in job_skill_map:

        print("Role not found in job_skills.json")

        return resume_skills[:6]

    required_skills = job_skill_map[role]

    filtered = []

    for skill in resume_skills:

        if skill.lower() in required_skills:
            filtered.append(skill)

    if not filtered:
        filtered = resume_skills[:6]

    return filtered