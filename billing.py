import sqlite3
import random

# Connect to existing DB
conn = sqlite3.connect("healthcare.db")
cursor = conn.cursor()

# Create Billing Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS billing (
    bill_id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    bill_amount REAL,
    payment_mode TEXT,
    FOREIGN KEY(patient_id) REFERENCES patient(patient_id)
)
''')

# Get all patient IDs
cursor.execute("SELECT patient_id FROM patient")
patient_ids = [row[0] for row in cursor.fetchall()]

# Generate billing data
billing_data = []
for pid in patient_ids:
    amount = round(random.uniform(500.0, 20000.0), 2)  # realistic billing amount
    payment_mode = random.choice(["cash", "credit"])
    billing_data.append((pid, amount, payment_mode))

# Insert in batches
batch_size = 10000
for i in range(0, len(billing_data), batch_size):
    cursor.executemany('''
    INSERT INTO billing (patient_id, bill_amount, payment_mode)
    VALUES (?, ?, ?)
    ''', billing_data[i:i+batch_size])
    print(f"Inserted batch {i//batch_size + 1}")

# Commit & close
conn.commit()
conn.close()
print("Billing table created and populated successfully.")