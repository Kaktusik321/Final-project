import matplotlib.pyplot as plt
import seaborn as sns
import io
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image,PageBreak)

def generate_report(df):
    df = df.copy()

#statystyka
    number_of_patients=len(df)
    mean_age = df['Age'].mean()
    median_age = df['Age'].median()
    max_age = df['Age'].max()
    min_age = df['Age'].min()
    mean_vit = df['Vitamin_D_level'].mean()
    median_vit = df['Vitamin_D_level'].median()
    max_vit = df['Vitamin_D_level'].max()
    min_vit = df['Vitamin_D_level'].min()

    filtered_patients = df[
        (df["Vitamin_D_level"] < 30)
    ]
    number_filtered = len(filtered_patients)
    symp = (
        filtered_patients["Symptoms"]
        .dropna()
        .value_counts()
        .reset_index()
    )
    symp.columns = ["Symptom", "Number of patients"]

#wykresy
    histogram_buffer= io.BytesIO()
    fig, axes = plt.subplots(figsize=(12,8))
    axes.hist(df["Vitamin_D_level"], bins=10, color="pink")
    axes.set_xlabel("Vitamin D level")
    axes.set_ylabel("Number of patients")
    axes.set_title("Vitamin D distribution")
    fig.tight_layout()
    fig.savefig(histogram_buffer, format="png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    histogram_buffer.seek(0)

    scatter_buffer = io.BytesIO()
    fig2, axes2 = plt.subplots(figsize=(12,8))
    for sex_value, marker, color in [
        ("Female", "o", "green"),
        ("Male", "x", "yellow")
    ]:
        sex_df = df[df["Sex"] == sex_value]

        if not sex_df.empty:
            axes2.scatter(
                sex_df["Age"],
                sex_df["Vitamin_D_level"],
                marker=marker,
                color=color,
                label=sex_value
            )

    axes2.set_xlabel("Age")
    axes2.set_ylabel("Vitamin D level")
    axes2.set_title("Vitamin D distribution by age and sex")

    handles, labels = axes2.get_legend_handles_labels()
    if handles:
        axes2.legend(handles, labels, loc="upper right")

    fig2.tight_layout()
    fig2.savefig(scatter_buffer, format="png", dpi=300, bbox_inches="tight")
    plt.close(fig2)
    scatter_buffer.seek(0)

    boxplot_buffer = io.BytesIO()
    df_plot = df.copy()
    df_plot["Group"]=(
        df["Asthma"].map({0:"Asthma No", 1:"Asthma Yes"})
        +" / "
        + df["Allergy"].map({0:"Allergy No", 1:"Allergy Yes"})
    )
    fig3, axes3 = plt.subplots(figsize=(12,8))
    sns.boxplot(data=df_plot, x="Group", y="Vitamin_D_level", ax=axes3, color='orange')
    axes3.set_xlabel("Asthma or allergy")
    axes3.set_ylabel("Vitamin D level")
    axes3.set_title('Distribution of vitamin D levels among asthmatic and allergic patients')
    axes3.tick_params(axis="x", labelrotation=20)

    fig3.tight_layout()
    fig3.savefig(boxplot_buffer, format="png", dpi=300, bbox_inches="tight")
    plt.close(fig3)
    boxplot_buffer.seek(0)


#pdf
    pdf_buffer = io.BytesIO()
    pdf=SimpleDocTemplate(pdf_buffer, pagesize=A4, rightMargin=1.5*cm,
                          leftMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
    styles = getSampleStyleSheet()
    story=[]

    story.append(Paragraph("Asthmatic and allergic patients report", styles["Title"]))
    story.append(Spacer(1,2*cm))

    story.append(Paragraph("1.Basic information about selected patients", styles["Heading2"]))
    basic=[
        ['Measure', 'Value'],
        ['Number of patients', str(number_of_patients)],
        ['Mean age', f'{mean_age:.2f}'],
        ['Median age', f'{median_age:.2f}'],
        ['Max age', f'{max_age:.2f}'],
        ['Min age', f'{min_age:.2f}'],
        ['Mean vitamin D level', f'{mean_vit:.2f}'],
        ['Median vitamin D level', f'{median_vit:.2f}'],
        ['Max vitamin D level', f'{max_vit:.2f}'],
        ['Min vitamin D level', f'{min_vit:.2f}'],
    ]

    table = Table(basic, colWidths=[10*cm, 5*cm])
    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.pink),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN",(1, 0), (1, -1), "CENTER" ),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE" ),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
        ])
    )
    story.append(table)
    story.append(Spacer(1, 0.5 * cm))


    story.append(
        Paragraph(
            "2. Patient subgroup analysis",
            styles["Heading2"]
        )
    )
    story.append(
        Paragraph(
            "Selected patients with vitamin D below 30 ng/ml",
            styles["Heading3"]
        )
    )
    story.append(Spacer(1, 0.2 * cm))
    story.append(
        Paragraph(
            f"Number of patients in this subgroup: {number_filtered}",
            styles["BodyText"]
        )
    )
    story.append(Spacer(1, 0.3 * cm))

    subgroup_columns = [
        "PatientID", "Age", "Sex", "Vitamin_D_level", "Asthma", "Allergy"
    ]

    subgroup_data = [
        ["Patient ID", "Age", "Sex", "Vitamin D", "Asthma", "Allergy"]
    ]

    for _, row in filtered_patients[subgroup_columns].iterrows():
        subgroup_data.append([
            str(row["PatientID"]),
            str(row["Age"]),
            str(row["Sex"]),
            f'{row["Vitamin_D_level"]:.2f}',
            str(row["Asthma"]),
            str(row["Allergy"])
        ])

    subgroup_table = Table(
        subgroup_data,
        colWidths=[3 * cm, 1.5 * cm, 2 * cm, 3 * cm, 2 * cm, 2 * cm],
        repeatRows=1
    )
    subgroup_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.pink),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5)
    ]))

    story.append(subgroup_table)
    story.append(Spacer(1, 0.5 * cm))

    story.append(
        Paragraph(
            "Symptoms among selected patients with low vitamin D (<30 ng/ml)",
            styles["Heading3"]
        )
    )

    symp_table_data = [["Symptom", "Number of patients"]]

    for _, row in symp.iterrows():
        symp_table_data.append([
            str(row["Symptom"]),
            str(row["Number of patients"])
        ])

    symp_table = Table(symp_table_data, colWidths=[7 * cm, 5 * cm])
    symp_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.pink),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6)
    ]))

    story.append(symp_table)
    story.append(PageBreak())

    story.append(
        Paragraph(
            "3. Visualizations",
            styles["Heading2"]
        )
    )
    story.append(
        Image(histogram_buffer, width=16 * cm, height=10 * cm)
    )
    story.append(Spacer(1, 0.5 * cm))
    story.append(
        Image(scatter_buffer,width=16 * cm, height=10 * cm)
    )
    story.append(PageBreak())
    story.append(
        Image(boxplot_buffer, width=16 * cm, height=10 * cm
        )
    )
    story.append(Spacer(1, 0.5 * cm))
    story.append(
        Paragraph("4. Summary and conclusions", styles["Heading2"])
    )

    summary = (
        f"The selected dataset contains {number_of_patients} patients. "
        f"The mean age is {mean_age:.2f} years and the median age is "
        f"{median_age:.2f} years. The mean vitamin D level is "
        f"{mean_vit:.2f} ng/ml and the median is {median_vit:.2f} ng/ml. "
        f"{number_filtered} patients have vitamin D levels below 30 ng/ml."
    )

    story.append(Paragraph(summary, styles["BodyText"]))
    story.append(Spacer(1, 0.3 * cm))

    story.append(
        Paragraph(
            "These results describe the selected dataset. "
            "They do not establish a causal relationship between vitamin D "
            "levels and asthma or allergy.",
            styles["BodyText"]
        )
    )

    pdf.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()























