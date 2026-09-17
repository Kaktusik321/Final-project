import sqlite3
from tracemalloc import Statistic

import pandas as pd

#połączenie z bazą
conn=sqlite3.connect("patients.db")

#wczytywanie danych do Pandas
df=pd.read_sql_query("SELECT * FROM patients",conn)

#filtrowanie osób z witaminą d <30 ng/ml,astmą i alergią
vit_aa=df[
    (df["Vitamin_D_level"]<30) &
    (df["Asthma"]==1) &
    (df['Allergy']==1)
]
vit_aa.to_csv("vit_aa.csv",index=False)

#wiek osób z niskim poziomem witaminy D, asthmą i alergią
age_stat=pd.DataFrame({
    "Statistic": ['Mean', 'Median', 'Minimum', 'Maximum'],
    'Age': [
        df["Age"].mean(),
        df["Age"].median(),
        df["Age"].min(),
        df["Age"].max()
    ]
})
age_stat.to_csv("age_stat.csv",index=False)

#porównanie poziomu witaminy d między grupami astmy
vit_a = df.groupby("Asthma")["Vitamin_D_level"].agg(
    ['count', 'mean', 'median', 'min', 'max']
).reset_index()
vit_a["Asthma"]=vit_a["Asthma"].map({0: "No", 1:"Yes"})
vit_a.to_csv("vit_a.csv",index=False)
