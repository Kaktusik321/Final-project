import sqlite3
import random

#połączenie z bazą
conn=sqlite3.connect("patients.db")
cursor=conn.cursor()

#usunięcie tabeli jeśli istnieje
cursor.execute("DROP TABLE IF EXISTS patients")

#tworzenie tabeli
cursor.execute("""
CREATE TABLE patients (
    PatientID INTEGER   PRIMARY KEY,
    Age INTEGER,
    Sex TEXT,
    Race TEXT,
    Vitamin_D_level REAL,
    Asthma INTEGER,
    Symptoms Text,
    Allergy INTEGER
)
""")

#generowanie 1000 pacjentów
sexes = ["Female","Male"]
races = ["White","Black", "Asian", "Hispanic", "Others"]

for patient_id in range(1, 1001):
    age = random.randint(18,85)
    sex = random.choice(sexes)
    race = random.choice(races)
    vitamin_d = round(random.uniform(10,80), 2)
    asthma = 1 if random.random() < 0.25 else 0
    allergy = 1 if random.random() < 0.4 else 0

    if asthma ==1:
        symptoms = random.choice([
            "Wheezing",
            "Cough",
            "Shortness of breath"
        ])
    else:
        symptoms = "No symptoms"
    cursor.execute("""
    INSERT INTO patients
    (PatientID, Age, Sex, Race, Vitamin_D_level, Asthma, Symptoms, Allergy)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        patient_id,
        age,
        sex,
        race,
        vitamin_d,
        asthma,
        symptoms,
        allergy
    ))
conn.commit()
cursor.execute("SELECT * FROM patients LIMIT 10")
rows = cursor.fetchall()

for row in rows:
    print(row)
conn.close()


