def generate_job_queries(job_role, skills, location):

    skill_string = " ".join(skills[:5])

    linkedin_query = f'site:linkedin.com/jobs "{job_role}" {skill_string} {location}'
    indeed_query = f'site:indeed.com "{job_role}" {skill_string} {location}'
    naukri_query = f'site:naukri.com "{job_role}" {skill_string} {location}'

    return {
        "linkedin": linkedin_query,
        "indeed": indeed_query,
        "naukri": naukri_query
    }