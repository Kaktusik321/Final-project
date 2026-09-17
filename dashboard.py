import sqlite3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conn=sqlite3.connect("patients.db")
df=pd.read_sql_query("SELECT * FROM patients ORDER BY PatientID",conn)
conn.close()

st.title("Patients with asthma and allergy")

sex=st.selectbox("Sex", ["All", "Male", "Female"])
if sex !="All":
    df=df[df["Sex"]==sex]
asthma=st.selectbox("Asthma", ["All", "Yes", "No"])
allergy=st.selectbox("Allergy", ["All", "Yes", "No"])

if asthma !="All":
    df=df[df["Asthma"]==(1 if asthma=="Yes" else 0)]
if allergy !="All":
    df=df[df["Allergy"]==(1 if allergy=="Yes" else 0)]
st.write("Number of patients:", len(df))
st.write("Mean vitamin D level:", round(df["Vitamin_D_level"].mean(),2))

st.subheader("Distribution of Vitamin D level")

fig, axes = plt.subplots()
axes.hist(df["Vitamin_D_level"], bins=10, color="pink")
axes.set_xlabel("Vitamin D level")
axes.set_ylabel("Number of patients")
axes.set_title("Vitamin D distribution")
st.pyplot(fig)

st.subheader("Vitamin D distribution by age and sex")
fig2, axes2 = plt.subplots()
df[df['Sex']=="Female"].plot(kind="scatter",x='Age', y='Vitamin_D_level', marker="o",label="Female", ax=axes2, color="green")
df[df['Sex']=="Male"].plot(kind="scatter",x='Age', y='Vitamin_D_level', marker="x",label="Female", ax=axes2, color="yellow")

axes2.set_xlabel("Age")
axes2.set_ylabel("Vitamin D level")
axes2.set_title("Vitamin D distribution by age and sex")
st.pyplot(fig2)


st.subheader("Distribution of vitamin D levels among asthmatic and allergic patients")
df["Group"]=(
    df["Asthma"].map({0:"Asthma No", 1:"Asthma Yes"})
    +" / "
    + df["Allergy"].map({0:"Allergy No", 1:"Allergy Yes"})
)
fig3, axes3 = plt.subplots()
sns.boxplot(data=df, x="Group", y="Vitamin_D_level", ax=axes3, color='orange')
axes3.set_xlabel("Asthma or allergy")
axes3.set_ylabel("Vitamin D level")
axes3.set_title('Distribution of vitamin D levels among asthmatic and allergic patients')
axes3.tick_params(axis="x", labelrotation=20)
st.pyplot(fig3)


