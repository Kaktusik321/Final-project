import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conn = sqlite3.connect('patients.db')
df = pd.read_sql_query('SELECT * FROM patients',conn)
conn.close()

#histigram - rozkład poziomu witaminy D
plt.hist(df['Vitamin_D_level'], bins=10, color="pink")
plt.xlabel('Vitamin D level')
plt.ylabel('Number of patients')
plt.title('Distribution of vitamin D level')
plt.savefig("Distribution of vitamin D level.png", dpi=300, bbox_inches="tight")
plt.show()

#wykres rozrzutu - wiek vs poziom witaminy
df[df["Sex"] == "Female"].plot(
    kind="scatter",
    x="Age",
    y="Vitamin_D_level",
    marker="o",
    label="Female",
    color="green",
)

df[df["Sex"] == "Male"].plot(
    kind="scatter",
    x="Age",
    y="Vitamin_D_level",
    marker="x",
    label="Male",
    ax=plt.gca(),
    color="yellow"
)
plt.xlabel('Age')
plt.ylabel('Vitamin D level')
plt.title('Vitamin D distribution by age and sex')
plt.legend()
plt.savefig("Vitamin D distribution by age and sex.png", dpi=300, bbox_inches="tight")
plt.show()

#boxplot - poziom witaminy D a występowanie astmy i alergii
df["Group"] = (
    df["Asthma"].map({0: "Asthma No", 1: "Asthma Yes"})
    + " / "
    + df["Allergy"].map({0: "Allergy No", 1: "Allergy Yes"})
)

sns.boxplot(x="Group",y="Vitamin_D_level",data=df, color="orange")
plt.xlabel('Asthma or allergy')
plt.ylabel('Vitamin D level')
plt.title('Distribution of vitamin D levels among asthmatic and allergic patients')
plt.xticks(rotation=20)
plt.savefig("Distribution of vitamin D levels among patients.png", dpi=300, bbox_inches="tight")
plt.show()



