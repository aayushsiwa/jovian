from flask import Flask, render_template, jsonify
from database import load_jobs

app = Flask(__name__)

jobs=load_jobs()

@app.route("/")
def hello_world():
    return render_template("home.html", jobs=jobs)


@app.route("/api/jobs")
def list_jobs():
    return jsonify(jobs)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


# starting branch v3
