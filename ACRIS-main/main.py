import os
import shutil
import sqlite3
from pathlib import Path

from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.middleware.sessions import SessionMiddleware

from parser import parse_resume, select_relevant_skills
from query_generator import generate_job_queries


# ---------------- APP ---------------- #
# ----------------APP----------------#
app = FastAPI()

# Session Middleware (Fix for dashboard error)
app.add_middleware(
    SessionMiddleware,
    secret_key="acris-secret-key"
)

# Static folders
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

DB_PATH = "app.db"


# ---------------- DATABASE ---------------- #

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- HOME ---------------- #

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    user = {
        "name": "Aniket",
        "email": "aniket@email.com"
    }

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user,
            "prefs": None
        }
    )


# ---------------- SUBMIT PROFILE ---------------- #

@app.post("/submit-profile")
async def submit_profile(

    request: Request,

    job_role: str = Form(...),
    experience: str = Form(...),
    expected_salary: str = Form(...),
    location: str = Form(...),
    job_type: str = Form(...),
    work_mode: str = Form(...),

    resume: UploadFile = File(None),
):

    print("\n========== PROFILE SUBMISSION ==========")

    resume_path = None

    if resume and resume.filename:

        print("Resume file received:", resume.filename)

        safe_name = resume.filename.replace(" ", "_")

        dest = UPLOAD_DIR / safe_name

        with dest.open("wb") as f:
            shutil.copyfileobj(resume.file, f)

        resume_path = str(dest)

        print("Resume saved at:", resume_path)

        # -------- RESUME PARSER -------- #

        parsed = parse_resume(resume_path)

        resume_skills = parsed["skills"]

        print("\nResume Skills:", resume_skills)

        # -------- SKILL FILTER -------- #

        filtered_skills = select_relevant_skills(job_role, resume_skills)

        print("\nFiltered Skills:", filtered_skills)

        # -------- JOB QUERY GENERATOR -------- #

        queries = generate_job_queries(job_role, filtered_skills, location)

        print("\n========== JOB SEARCH QUERIES ==========")

        for site, query in queries.items():
            print(site.upper(), ":", query)

        print("========================================\n")

    return RedirectResponse("/", status_code=303)