import sqlite3
import random

# Connect to existing DB
conn = sqlite3.connect("healthcare.db")
cursor = conn.cursor()

# Create Diagnosis Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS diagnosis (
    diagnosis_id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    diagnosis_name TEXT,
    FOREIGN KEY(patient_id) REFERENCES patient(patient_id)
)
''')

# Sample diagnosis types
diagnosis_types = [
    "Diabetes", "Hypertension", "Asthma", "COVID-19", "Arthritis",
    "Migraine", "Anxiety", "Heart Disease", "Thyroid", "Flu",
    "PCOS", "Kidney Stones", "Ulcer", "Pneumonia", "Back Pain"
]

# Get all patient IDs
cursor.execute("SELECT patient_id FROM patient")
patient_ids = [row[0] for row in cursor.fetchall()]

diagnosis_records = []
for pid in patient_ids:
    diagnoses = random.sample(diagnosis_types, 2)  # 2 unique diagnoses
    for diagnosis in diagnoses:
        diagnosis_records.append((pid, diagnosis))

# Insert diagnoses in batches
batch_size = 10000
for i in range(0, len(diagnosis_records), batch_size):
    cursor.executemany('''
    INSERT INTO diagnosis (patient_id, diagnosis_name)
    VALUES (?, ?)
    ''', diagnosis_records[i:i+batch_size])
    print(f"Inserted batch {i//batch_size + 1}")

# Commit & close
conn.commit()
conn.close()
print("Diagnosis table created and populated successfully.")