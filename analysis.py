import pandas as pd

def analyze_data(df):

    #filtrowanie osób wybranych z witaminą d <30 ng/ml
    vit=df[
        (df["Vitamin_D_level"]<30)
    ].copy()


    #Liczba osób z niskim poziomem witaminy D według objawów
    symp=(
        vit["Symptoms"]
        .dropna()
        .value_counts()
        .reset_index()
    )
    symp.columns = ["Symptom", "Number of patients"]
    return vit, symp
