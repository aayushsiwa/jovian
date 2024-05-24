from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_hcaptcha import hCaptcha
from database import (
    load_jobs,
    load_job,
    application,
    load_applications,
    load_application,
)
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)


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
    return render_template("error.html",error=error,code=code)


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
    app.run(host="0.0.0.0", debug=True)
