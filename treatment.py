import sqlite3
import random

# Connect to existing DB
conn = sqlite3.connect("healthcare.db")
cursor = conn.cursor()

# Create Treatment Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS treatment (
    treatment_id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    medicine_name TEXT,
    dose_time TEXT,
    duration INTEGER,
    FOREIGN KEY(patient_id) REFERENCES patient(patient_id)
)
''')

# Sample medicine names
medicine_list = [
    "Paracetamol", "Ibuprofen", "Metformin", "Amlodipine", "Atorvastatin",
    "Omeprazole", "Ciprofloxacin", "Azithromycin", "Levothyroxine", "Salbutamol",
    "Dolo-650", "Insulin", "Amoxicillin", "Hydrochlorothiazide", "Prednisone"
]

dose_times = ["Morning", "Afternoon", "Evening", "Night"]

# Get all patient IDs
cursor.execute("SELECT patient_id FROM patient")
patient_ids = [row[0] for row in cursor.fetchall()]

treatments = []
for pid in patient_ids:
    meds = random.sample(medicine_list, 5)  # 5 unique medicines
    for med in meds:
        dose = random.choice(dose_times)
        duration = random.randint(3, 15)  # in days
        treatments.append((pid, med, dose, duration))

# Insert in batches
batch_size = 10000
for i in range(0, len(treatments), batch_size):
    cursor.executemany('''
    INSERT INTO treatment (patient_id, medicine_name, dose_time, duration)
    VALUES (?, ?, ?, ?)
    ''', treatments[i:i+batch_size])
    print(f"Inserted batch {i//batch_size + 1}")

# Commit & close
conn.commit()
conn.close()
print("Treatment table created and populated successfully.")