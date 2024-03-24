from flask import Flask,render_template,jsonify

app=Flask(__name__)

JOBS = [
    {'id': 1,
    'title': 'Data Analyst',
    'location': 'Bengaluru, India',
    'salary': 'Rs. 100,000'},
    
    {'id': 2,
    'title': 'Software Engineer',
    'location': 'San Francisco, USA',
    'salary': '$120,000'},
    
    {'id': 3,
    'title': 'Marketing Specialist',
    'location': 'London, UK',
    'salary': '£50,000'},
    
    {'id': 4,
    'title': 'Graphic Designer',
    'location': 'Berlin, Germany',
    'salary': '€60,000'},
    
    {'id': 5,
    'title': 'Project Manager',
    'location': 'Tokyo, Japan',
    'salary': '¥8,000,000'},
]


@app.route("/")
def hello_world():
    return render_template("home.html",jobs=JOBS)

@app.route("/api/jobs")
def list_jobs():
    return jsonify(JOBS)

if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)