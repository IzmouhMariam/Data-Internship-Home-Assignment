from airflow.providers.sqlite.operators.sqlite import SqliteOperator

JOB_TABLE = """CREATE TABLE IF NOT EXISTS job (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(225),
    industry VARCHAR(225),
    description TEXT,
    employment_type VARCHAR(125),
    date_posted DATE
);"""

COMPANY_TABLE = """CREATE TABLE IF NOT EXISTS company (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER,
    name VARCHAR(225),
    link TEXT,
    FOREIGN KEY (job_id) REFERENCES job(id)
);"""

EDUCATION_TABLE = """CREATE TABLE IF NOT EXISTS education (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER,
    required_credential VARCHAR(225),
    FOREIGN KEY (job_id) REFERENCES job(id)
);"""

EXPERIENCE_TABLE = """CREATE TABLE IF NOT EXISTS experience (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER,
    months_of_experience INTEGER,
    seniority_level VARCHAR(25),
    FOREIGN KEY (job_id) REFERENCES job(id)
);"""

SALARY_TABLE = """CREATE TABLE IF NOT EXISTS salary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER,
    currency VARCHAR(3),
    min_value NUMERIC,
    max_value NUMERIC,
    unit VARCHAR(12),
    FOREIGN KEY (job_id) REFERENCES job(id)
);"""

LOCATION_TABLE = """CREATE TABLE IF NOT EXISTS location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER,
    country VARCHAR(60),
    locality VARCHAR(60),
    region VARCHAR(60),
    postal_code VARCHAR(25),
    street_address VARCHAR(225),
    latitude NUMERIC,
    longitude NUMERIC,
    FOREIGN KEY (job_id) REFERENCES job(id)
);"""

TABLES = [JOB_TABLE, COMPANY_TABLE, EDUCATION_TABLE, EXPERIENCE_TABLE, SALARY_TABLE, LOCATION_TABLE]

def create():
    tasks = []
    for table in TABLES:
        table_name = table.split("EXISTS")[1].split('(')[0].strip()
        task = SqliteOperator(
            task_id=f"create_table_{table_name}",
            sqlite_conn_id="sqlite_default",
            sql=table
        )
        tasks.append(task)
    return tasks

