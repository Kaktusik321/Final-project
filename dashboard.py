import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from analysis import analyze_data
from plots import (plot_vit_distr, plot_age_sex, plot_vit_by)
from report import generate_report

st.title("Vitamin D analysis")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        required_columns = [
            "PatientID", "Age", "Sex", "Race",
            "Vitamin_D_level", "Asthma", "Symptoms", "Allergy"
        ]

        missing_columns = [
            col for col in required_columns if col not in df.columns
        ]

        if missing_columns:
            st.error(
                "Missing columns: " + ", ".join(missing_columns)
            )
            st.stop()

        st.success("File loaded successfully!")

        st.subheader("Patient data")


        sex=st.selectbox("Sex", ["All", "Male", "Female"])
        if sex !="All":
            df=df[df["Sex"]==sex]
        asthma=st.selectbox("Asthma", ["All", "Yes", "No"])
        allergy=st.selectbox("Allergy", ["All", "Yes", "No"])

        if asthma !="All":
            df=df[df["Asthma"]==(1 if asthma=="Yes" else 0)]
        if allergy !="All":
            df=df[df["Allergy"]==(1 if allergy=="Yes" else 0)]

        st.dataframe(df, use_container_width=True)
        st.download_button(label="Download filtred data (CSV)", data=df.to_csv(index=False).encode("utf-8-sig"), file_name="filtered_patients.csv", mime="text/csv")
        vit, symp = analyze_data(df)
        st.write("Number of patients:", len(df))
        if not df.empty:
            st.write("Mean age:", round(df["Age"].mean(), 2))
            st.write("Median age:", round(df["Age"].median(), 2))
            st.write("Minimum age:", df["Age"].min())
            st.write("Maximum age:", df["Age"].max())
            st.write("Mean vitamin D level:", round(df["Vitamin_D_level"].mean(), 2))
            st.write("Median vitamin D level:", round(df["Vitamin_D_level"].median(), 2))
            st.write("Minimum vitamin D level:", round(df["Vitamin_D_level"].min(), 2))
            st.write("Maximum vitamin D level:", round(df["Vitamin_D_level"].max(), 2))
        else:
            st.warning("No patients match the selected filters.")

        st.header("Patient subgroup analysis")
        st.subheader("Selected patients with low vitamin D (<30 ng/ml)")
        st.dataframe(vit, use_container_width=True,hide_index=True)

        st.subheader("Symptoms among selected patients with low vitamin D (<30 ng/ml)")
        st.dataframe(symp, use_container_width=True,hide_index=True)

        if not df.empty:
            st.header("Data visualization")
            st.subheader("Distribution of Vitamin D level")

            fig=plot_vit_distr(df)
            st.pyplot(fig)
            plt.close(fig)

            st.subheader("Vitamin D distribution by age and sex")
            fig=plot_age_sex(df)
            st.pyplot(fig)
            plt.close(fig)


            st.subheader("Distribution of vitamin D levels among asthmatic and allergic patients")
            fig=plot_vit_by(df)
            st.pyplot(fig)
            plt.close(fig)

            st.header("PDF report")

            pdf_data = generate_report(df)

            st.download_button(
                label="Download PDF report",
                data=pdf_data,
                file_name="patient_report.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Upload a CSV file to start the analysis.")
