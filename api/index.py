from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_hcaptcha import hCaptcha
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)


def send_email(receiver_email, subject, message):
    try:
        smtp_server = "smtp-mail.outlook.com"
        smtp_port = 587
        smtp_username = os.environ["SMTP_USER"]
        smtp_password = os.environ["SMTP_PASS"]
        msg = MIMEMultipart()
        sender_mail = os.environ["MAIL_FROM"]
        msg["From"] = os.environ["MAIL_FROM"]
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "html"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_mail, receiver_email, msg.as_string())
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")
        return False
    finally:
        server.quit()  # Ensure to close the SMTP connection


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
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM jobs WHERE id={id};"))
            column_names = result.keys()
            row = result.fetchone()
            if row is None:
                return None
            else:
                job = {column: value for column, value in zip(column_names, row)}
                return job
    except Exception as e:
        print(f"An error occurred while loading job: {e}")
        return None


def application_confirmation(jobId, data):
    # print(jobId)
    name = data["fullName"].capitalize()
    # print("load not working")
    job = load_job(jobId)
    subject = f"Recieved application for the of {job['title']} at Jovian"
    template_path = os.path.join(os.path.dirname(__file__), "templates", "mail.html")
    with open(template_path, "r") as f:
        message = f.read()
    message = message.replace("CName", name)
    message = message.replace("JobT", job["title"])
    # print(subject, message)
    result = send_email(data["email"], subject, message)


def application(jobId, data):
    try:
        with engine.connect() as conn:
            query = text(
                "INSERT INTO applications (jobId, fullName, email, linkedIn, education, workExp, resume) VALUES (:jobId, :fullName, :email, :linkedIn, :education, :workExp, :resume)"
            )
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
            application_confirmation(jobId, data)
            return True
    except Exception as e:
        print(f"An error occurred while processing application: {e}")
        return False


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
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT * FROM applications where jobId={jobId};")
            )
            column_names = result.keys()
            row = result.fetchall()
            if len(row) == 0:
                return None
            else:
                application = {
                    column: value for column, value in zip(column_names, row[0])
                }
                return application
    except Exception as e:
        print(f"An error occurred while loading application: {e}")
        return None


app = Flask(__name__)

app.config["HCAPTCHA_SITE_KEY"] = os.environ["CAPTCHA_SITEKEY"]
app.config["HCAPTCHA_SECRET_KEY"] = os.environ["CAPTCHA_SECRET"]
hcaptcha = hCaptcha(app)

jobs = load_jobs()


@app.errorhandler(404)
def not_found_error(error):
    code = str(error).split(" ")[0]
    return render_template("error.html", error=error, code=code)


@app.errorhandler(500)
def internal_server_error(error):
    code = str(error).split(" ")[0]
    return render_template("error.html", error=error, code=code)


@app.errorhandler(400)
def bad_request_error(error):
    code = str(error).split(" ")[0]
    return render_template("error.html", error=error, code=code)


@app.errorhandler(405)
def method_not_allowed(error):
    code = str(error).split(" ")[0]
    return render_template("error.html", error=error, code=code)


@app.route("/")
def hello_world():
    return render_template("home.html", jobs=jobs)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path), "favicon.ico")


@app.route("/api/jobs")
def list_jobs():
    return jsonify(jobs)


@app.route("/api/jobs/<id>")
def list_job(id):
    job = load_job(id)
    return jsonify(job)


@app.route("/api/applications")
def list_applications():
    return load_applications()


@app.route("/api/applications/<jobId>")
def list_application(jobId):
    application = load_application(jobId)
    return jsonify(application)


@app.route("/job/<id>")
def show_job(id):
    job = load_job(id)
    if not job:
        return not_found_error("404 : Job Not Found")
    return render_template(
        "jobPage.html", job=job, captcha_sitekey=os.environ["CAPTCHA_SITEKEY"]
    )


@app.route("/job/<id>/apply", methods=["post"])
def apply_to(id):
    job = load_job(id)
    data = request.form
    if request.method != "POST":
        return "This route only allows GET requests"
    if not hcaptcha.verify():
        return bad_request_error("400 hCaptcha verification failed")
    application(id, data)
    return render_template("applicationSub.html", job=job, application=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
