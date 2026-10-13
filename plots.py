import matplotlib.pyplot as plt
import seaborn as sns

#histigram - rozkład poziomu witaminy D
def plot_vit_distr(df):
    fig, ax = plt.subplots()
    ax.hist(df['Vitamin_D_level'], bins=10, color="pink")
    ax.set_xlabel('Vitamin D level')
    ax.set_ylabel('Number of patients')
    ax.set_title('Distribution of vitamin D level')
    fig.tight_layout()
    return fig

#wykres rozrzutu - wiek i płeć vs poziom witaminy
def plot_age_sex(df):
    fig, ax = plt.subplots()
    for sex, marker, color in [
        ("Female", "o", "green"),
        ("Male", "x", "yellow")
    ]:
        sex_df = df[df["Sex"] == sex]

        if not sex_df.empty:
            sex_df.plot(
                kind="scatter",
                x="Age",
                y="Vitamin_D_level",
                marker=marker,
                label=sex,
                color=color,
                ax=ax
            )
    ax.set_xlabel('Age')
    ax.set_ylabel('Vitamin D level')
    ax.set_title('Vitamin D distribution by age and sex')
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(handles, labels, loc="upper right")
    plt.tight_layout()
    return fig

#boxplot - poziom witaminy D a występowanie astmy i alergii
def plot_vit_by(df):
    df = df.copy()
    df["Group"] = (
        df["Asthma"].map({0: "Asthma No", 1: "Asthma Yes"})
        + " / "
        + df["Allergy"].map({0: "Allergy No", 1: "Allergy Yes"})
    )
    fig, ax = plt.subplots()
    sns.boxplot(x="Group",y="Vitamin_D_level",data=df, color="orange",ax=ax)
    ax.set_xlabel('Asthma or allergy')
    ax.set_ylabel('Vitamin D level')
    ax.set_title('Distribution of vitamin D levels among asthmatic and allergic patients')
    ax.tick_params(axis="x", labelrotation=20)
    fig.tight_layout()
    return fig



