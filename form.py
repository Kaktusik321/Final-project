import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def add_patient():
    age = age_entry.get()
    sex=sex_box.get()
    race=race_box.get()
    vitamin_d = vitamin_d_entry.get()
    asthma=asthma_box.get()
    allergy=allergy_box.get()
    symptoms=symptoms_box.get()

    #czy są braki danych
    if not age or not sex or not race or not vitamin_d or not asthma or not allergy or not symptoms:
        messagebox.showerror("ERROR","Please fill all fields")
        return
    #zmiana typów
    age=int(age)
    vitamin_d=float(vitamin_d)
    asthma=1 if asthma=="Yes" else 0
    allergy=1 if allergy=="Yes" else 0

    #łączenie z bazą
    conn=sqlite3.connect("patients.db")
    cursor=conn.cursor()

    #patientID
    cursor.execute("SELECT MAX(PatientID) FROM patients")
    max_patient=cursor.fetchone()[0]

    if max_patient is None:
        patient_id=1
    else:
        patient_id=max_patient+1

    #pacjent
    cursor.execute("""
    INSERT INTO patients 
    (PatientID, Age, Sex, Race, Vitamin_D_level, Asthma, Allergy, Symptoms)
    VALUES (?,?,?,?,?,?,?,?)
    """,(
        patient_id,
        age,
        sex,
        race,
        vitamin_d,
        asthma,
        allergy,
        symptoms
    ))
    conn.commit()
    conn.close()

    messagebox.showinfo("HUrra!",f"Patient {patient_id} has been added")

    #puste pola
    age_entry.delete(0,tk.END)
    vitamin_d_entry.delete(0,tk.END)

#OKNO#

window=tk.Tk()
window.title("Patients")
window.geometry("500x500")

tk.Label(window,text="Age:").pack()
age_entry=tk.Entry(window)
age_entry.pack()

tk.Label(window, text="Sex:").pack()
sex_box = ttk.Combobox(window,values=["Male","Female"], state='readonly')
sex_box.pack()

tk.Label(window, text="Race:").pack()
race_box=ttk.Combobox(window,values=["White","Black", "Asian", "Hispanic", "Others"], state='readonly')
race_box.pack()

tk.Label(window, text="Vitamin D:").pack()
vitamin_d_entry=tk.Entry(window)
vitamin_d_entry.pack()

tk.Label(window, text="Asthma:").pack()
asthma_box=ttk.Combobox(window, values=["Yes","No"], state='readonly')
asthma_box.pack()

tk.Label(window, text="Allergy:").pack()
allergy_box=ttk.Combobox(window, values=["Yes","No"], state='readonly')
allergy_box.pack()

tk.Label(window, text="Symptoms:").pack()
symptoms_box= ttk.Combobox(window, values=["Wheezing","Cough", "Shortness of breath", "No symptoms"], state='readonly')
symptoms_box.pack()

#przycisk
add_button=tk.Button(window,text="Add Patient",command=add_patient)
add_button.pack(pady=20)
window.mainloop()





