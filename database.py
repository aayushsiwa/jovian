from mail import send_email
from sqlalchemy import create_engine, text
import os

engine = create_engine(os.environ["DB_SECRET"])


def load_jobs():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs;"))
    column_names = result.keys()
    jobs = []
    for row in result.fetchall():
        row_dict = {column: value for column, value in zip(column_names, row)}
        jobs.append(row_dict)
    # print(jobs[0]["id"])
    return jobs


def load_job(id):
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM jobs where id={id};"))
        column_names = result.keys()
        row = result.fetchall()
        if len(row) == 0:
            return None
        else:
            job = {column: value for column, value in zip(column_names, row[0])}
            return job


def application_confirmation(jobId, data):
    # print(jobId)
    name = data["fullName"].capitalize()
    # print("load not working")
    job = load_job(jobId)
    subject = f"Recieved application for the of {job['title']} at Jovian"
    with open("./templates/mail.html", "r") as f:
        message = f.read()
        f.close()
    message = message.replace("CName", name)
    message = message.replace("JobT", job["title"])
    # print(subject, message)
    result = send_email(data["email"], subject, message)


def application(jobId, data):
    with engine.connect() as conn:
        query = text(
            "INSERT INTO applications (jobId, fullName, email, linkedIn, education, workExp, resume) VALUES (:jobId, :fullName, :email, :linkedIn, :education, :workExp, :resume)"
        )
        # print(query)
        # print("query sent")
        try:
            conn.execute(
                query,
                {
                    "jobId": jobId,
                    "fullName": data["fullName"],
                    "email": data["email"],
                    "linkedIn": data.get("linkedIn", None),
                    "education": data.get("education", None),
                    "workExp": data.get("workExp", None),
                    "resume": data.get("resume", None),
                },
            )
            conn.commit()
            # print("commit")
            jobT = load_job(jobId)
            # print(jobT['title'])
            print(application_confirmation(jobId, data))
            # print("app")
            return True  # Return True if insertion is successful
        except Exception as e:
            print(f"An error occurred: {e}")
            return False  # Return False if insertion fails


def load_applications():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM applications;"))
    column_names = result.keys()
    applications = []
    for row in result.fetchall():
        row_dict = {column: value for column, value in zip(column_names, row)}
        applications.append(row_dict)
    # print(jobs[0]["id"])
    return applications


def load_application(jobId):
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM applications where jobId={jobId};"))
        column_names = result.keys()
        row = result.fetchall()
        if len(row) == 0:
            return None
        else:
            application = {column: value for column, value in zip(column_names, row[0])}
            return application


def mail_application(jobId, email):
    with engine.connect() as conn:
        result = conn.execute(
            text(f"SELECT * FROM applications WHERE email='{email}' and jobId={jobId};")
        )
        column_names = result.keys()
        row = result.fetchall()
        if len(row) == 0:
            return None
        else:
            application = {column: value for column, value in zip(column_names, row[0])}
            application_confirmation(application)
