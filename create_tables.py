import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize
fake = Faker()
conn = sqlite3.connect("healthcare.db")
cursor = conn.cursor()

# Step 1: Create hospital table
cursor.execute('''
CREATE TABLE IF NOT EXISTS hospital (
    hospital_id INTEGER PRIMARY KEY,
    hospital_name TEXT
)
''')

hospital_names = [f"{fake.company()} Hospital" for _ in range(5)]
cursor.executemany("INSERT INTO hospital (hospital_name) VALUES (?)", [(name,) for name in hospital_names])

# Step 2: Create patient table
cursor.execute('''
CREATE TABLE IF NOT EXISTS patient (
    patient_id INTEGER PRIMARY KEY,
    hospital_id INTEGER,
    patient_name TEXT,
    dob DATE,
    admission_datetime DATETIME,
    discharge_datetime DATETIME,
    FOREIGN KEY(hospital_id) REFERENCES hospital(hospital_id)
)
''')

def generate_patient(hospital_id):
    name = fake.name()
    dob = fake.date_of_birth(minimum_age=1, maximum_age=90)
    admission_date = fake.date_time_between(start_date="-1y", end_date="now")
    discharge_date = admission_date + timedelta(days=random.randint(1, 20))
    return (hospital_id, name, dob, admission_date, discharge_date)

# Generate 100,000 patients
patients = []
for _ in range(100_000):
    hosp_id = random.randint(1, 5)
    patients.append(generate_patient(hosp_id))

# Insert in batches for performance
batch_size = 5000
for i in range(0, len(patients), batch_size):
    cursor.executemany('''
    INSERT INTO patient (hospital_id, patient_name, dob, admission_datetime, discharge_datetime)
    VALUES (?, ?, ?, ?, ?)
    ''', patients[i:i+batch_size])
    print(f"Inserted batch {i//batch_size + 1}")

# Commit & close
conn.commit()
conn.close()
print("Hospital and patient tables created successfully.")