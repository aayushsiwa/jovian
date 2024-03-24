from sqlalchemy import create_engine,text
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
