import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
import seaborn as sns

from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image,PageBreak)

conn=sqlite3.connect("patients.db")
df=pd.read_sql_query("SELECT * FROM patients", conn)
conn.close()

#statystyka
number_of_patients=len(df)
mean_vit = df['Vitamin_D_level'].mean()
median_vit = df['Vitamin_D_level'].median()
max_vit = df['Vitamin_D_level'].max()
min_vit = df['Vitamin_D_level'].min()

mean_age = df['Age'].mean()
median_age = df['Age'].median()
max_age = df['Age'].max()
min_age = df['Age'].min()

filtered_patients = df[
    (df["Vitamin_D_level"] < 30) &
    (df["Asthma"] == 1) &
    (df["Allergy"] == 1)
]
number_filtered = len(filtered_patients)

vit_a=df.groupby(['Asthma'])['Vitamin_D_level'].agg(
    ["count", "mean", "median", "max", "min"]
).reset_index()

vit_a['Asthma']=vit_a['Asthma'].map({
    0: 'No',
    1: "Yes"
})

#wykresy
fig, axes = plt.subplots(figsize=(12,8))
axes.hist(df["Vitamin_D_level"], bins=10, color="pink")
axes.set_xlabel("Vitamin D level")
axes.set_ylabel("Number of patients")
axes.set_title("Vitamin D distribution")
plt.tight_layout()
plt.savefig("report_histogram.png", dpi=300, bbox_inches="tight")
plt.close()

fig2, axes2 = plt.subplots(figsize=(12,8))
df[df['Sex']=="Female"].plot(kind="scatter",x='Age', y='Vitamin_D_level', marker="o",label="Female", ax=axes2, color="green")
df[df['Sex']=="Male"].plot(kind="scatter",x='Age', y='Vitamin_D_level', marker="x",label="Female", ax=axes2, color="yellow")

axes2.set_xlabel("Age")
axes2.set_ylabel("Vitamin D level")
axes2.set_title("Vitamin D distribution by age and sex")

plt.tight_layout()
plt.savefig("report_scatter.png", dpi=300, bbox_inches="tight")
plt.close()

df["Group"]=(
    df["Asthma"].map({0:"Asthma No", 1:"Asthma Yes"})
    +" / "
    + df["Allergy"].map({0:"Allergy No", 1:"Allergy Yes"})
)
fig3, axes3 = plt.subplots(figsize=(12,8))
sns.boxplot(data=df, x="Group", y="Vitamin_D_level", ax=axes3, color='orange')
axes3.set_xlabel("Asthma or allergy")
axes3.set_ylabel("Vitamin D level")
axes3.set_title('Distribution of vitamin D levels among asthmatic and allergic patients')
axes3.tick_params(axis="x", labelrotation=20)

plt.tight_layout()
plt.savefig("report_boxplot.png", dpi=300, bbox_inches="tight")
plt.close()

#pdf
pdf=SimpleDocTemplate("patient report.pdf", pagesize=A4, rightMargin=1.5*cm,
                      leftMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
styles = getSampleStyleSheet()
story=[]

story.append(Paragraph("Asthmatic and allergic patients report", styles["Title"]))
story.append(Spacer(1,2*cm))

story.append(Paragraph("1.Basic patient information", styles["Heading2"]))
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
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0, colors.black),
        ("TOPPADDING", (0, 0), (-1, -1), 0, colors.black),
    ])
)
story.append(table)
story.append(Spacer(1, 0.7 * cm))

story.append(
    Paragraph(
        "2. Vitamin D by asthma status",
        styles["Heading2"]
    )
)
group_table_data = [
    ["Asthma", "Count", "Mean", "Median", "Min", "Max"]
]

for _, row in vit_a.iterrows():
    group_table_data.append([
        row['Asthma'],
        int(row["count"]),
        f"{row['mean']:.2f}",
        f"{row['median']:.2f}",
        f"{row['max']:.2f}",
        f"{row['min']:.2f}"
    ])
group_table = Table(
    group_table_data,
    colWidths=[
        2 * cm,
        2 * cm,
        2 * cm,
        2 * cm,
        2 * cm,
        2 * cm
    ]
)
group_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.pink),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ])
)
story.append(group_table)
story.append(PageBreak())

story.append(
    Paragraph(
        "3. Visualizations",
        styles["Heading2"]
    )
)
story.append(
    Image(
        "report_histogram.png",
        width=16 * cm,
        height=10 * cm
    )
)

story.append(Spacer(1, 0.5 * cm))


story.append(
    Image(
        "report_scatter.png",
        width=16 * cm,
        height=10 * cm
    )
)
story.append(PageBreak())


story.append(
    Image(
        "report_boxplot.png",
        width=16 * cm,
        height=9 * cm
    )
)

pdf.build(story)
print("Report created: patient_report.pdf")























