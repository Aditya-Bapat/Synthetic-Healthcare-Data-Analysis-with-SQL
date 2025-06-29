select count(*) from patient
select count(*) from hospital

SELECT hospital_id, COUNT(*) AS total_patients
FROM patient
GROUP BY hospital_id;

SELECT * FROM hospital LIMIT 5;
SELECT * FROM patient LIMIT 5;

SELECT p.patient_id, p.patient_name, p.dob, h.hospital_name
FROM patient p
JOIN hospital h ON p.hospital_id = h.hospital_id
LIMIT 5;

SELECT * FROM diagnosis LIMIT 10;

SELECT * FROM treatment LIMIT 10;

SELECT * FROM billing LIMIT 10;

-- Query 
-- 
-- 1) Average Patients Per Month, Week, Year

-- Monthly
SELECT h.hospital_name, 
       strftime('%Y-%m', p.admission_datetime) AS month,
       COUNT(p.patient_id) AS monthly_admissions
FROM patient p
JOIN hospital h ON p.hospital_id = h.hospital_id
GROUP BY h.hospital_id, month;

-- Weekly
SELECT h.hospital_name, 
       strftime('%Y-%W', p.admission_datetime) AS week,
       COUNT(p.patient_id) AS weekly_admissions
FROM patient p
JOIN hospital h ON p.hospital_id = h.hospital_id
GROUP BY h.hospital_id, week;

-- Yearly
SELECT h.hospital_name, 
       strftime('%Y', p.admission_datetime) AS year,
       COUNT(p.patient_id) AS yearly_admissions
FROM patient p
JOIN hospital h ON p.hospital_id = h.hospital_id
GROUP BY h.hospital_id, year;

-- 2) Hospital occupancy on a daily, weekly, monthly, and yearly basis 

-- Daily occupancy
SELECT strftime('%Y-%m-%d', admission_datetime) AS day,
       COUNT(*) AS daily_admissions
FROM patient
GROUP BY day;

-- Weekly occupancy
SELECT strftime('%Y-%W', admission_datetime) AS week,
       COUNT(*) AS weekly_admissions
FROM patient
GROUP BY week;

-- Monthly occupancy
SELECT strftime('%Y-%m', admission_datetime) AS month,
       COUNT(*) AS monthly_admissions
FROM patient
GROUP BY month;

-- Yearly occupancy
SELECT strftime('%Y', admission_datetime) AS year,
       COUNT(*) AS yearly_admissions
FROM patient
GROUP BY year;

-- 3) Age-wise categorization of patients 

SELECT 
  CASE 
    WHEN (strftime('%Y', 'now') - strftime('%Y', dob)) <= 12 THEN 'Child'
    WHEN (strftime('%Y', 'now') - strftime('%Y', dob)) BETWEEN 13 AND 59 THEN 'Adult'
    ELSE 'Senior'
  END AS age_group,
  COUNT(*) AS total_patients
FROM patient
GROUP BY age_group;

-- 4) Most consumed medicine 

SELECT medicine_name, COUNT(*) AS total_prescribed
FROM treatment
GROUP BY medicine_name
ORDER BY total_prescribed DESC
LIMIT 1;

-- 5) Most consumed medicine by diagnosis 

SELECT d.diagnosis_name, t.medicine_name
FROM diagnosis d
JOIN treatment t ON d.patient_id = t.patient_id
LIMIT 10;

SELECT t.medicine_name, COUNT(*) AS usage_count
FROM diagnosis d
JOIN treatment t ON d.patient_id = t.patient_id
WHERE d.diagnosis_name = 'Pneumonia'
GROUP BY t.medicine_name
ORDER BY usage_count DESC
LIMIT 1;

SELECT d.diagnosis_name,
       (
         SELECT t.medicine_name
         FROM treatment t
         JOIN diagnosis d2 ON d2.patient_id = t.patient_id
         WHERE d2.diagnosis_name = d.diagnosis_name
         GROUP BY t.medicine_name
         ORDER BY COUNT(*) DESC
         LIMIT 1
       ) AS top_medicine
FROM diagnosis d
GROUP BY d.diagnosis_name
ORDER BY d.diagnosis_name;


-- 6) Average Days of Hospitalization

SELECT 
  ROUND(AVG(julianday(discharge_datetime) - julianday(admission_datetime)), 2) 
  AS average_days_hospitalized
FROM patient;

-- 7)Monthly and yearly income, with a cash/credit split 

-- Monthly
SELECT 
  strftime('%Y-%m', p.admission_datetime) AS month,
  b.payment_mode,
  ROUND(SUM(b.bill_amount), 2) AS total_income
FROM billing b
JOIN patient p ON b.patient_id = p.patient_id
GROUP BY month, b.payment_mode
ORDER BY month;

-- Yearly
SELECT 
  strftime('%Y', p.admission_datetime) AS year,
  b.payment_mode,
  ROUND(SUM(b.bill_amount), 2) AS total_income
FROM billing b
JOIN patient p ON b.patient_id = p.patient_id
GROUP BY year, b.payment_mode
ORDER BY year;

