from flask import Flask, render_template, jsonify
from database import load_jobs,load_job

app = Flask(__name__)

jobs=load_jobs()

@app.route("/")
def hello_world():
    return render_template("home.html", jobs=jobs)


@app.route("/api/jobs")
def list_jobs():
    return jsonify(jobs)

@app.route("/job/<id>")
def show_job(id):
    job=load_job(id)
    if not job:
        return "Not Found",404
    return render_template("jobPage.html",job=job)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


# starting branch v3
