Application Specification

1. Purpose of the application

The application is an interactive web dashboard developed in Python using Streamlit. It enables users to explore and analyze patient data, focusing on vitamin D levels, asthma, allergy status, age, sex, and reported symptoms.
2. Graphical User Interface 

The application interface is displayed in a web browser and consists of the following sections:

* Data filters – allow users to narrow the dataset according to selected criteria, such as sex, asthma status, and allergy status.

* Summary statistics – present basic information about the currently selected dataset.

* Data visualizations – display charts illustrating the distribution of vitamin D levels, the relationship between age, sex and vitamin D levels, and differences between patient groups.

* Report generation – allows the user to generate a PDF report containing selected statistics and visualizations.

3. Application Workflow

* The application loads  the patient dataset.

* The user selects the desired filtering criteria.

* The displayed statistics and visualizations are updated to reflect the selected data.

* The user can generate a PDF report based on the available data. The generated report can be saved by the user.
4. 
5. Data Structure

The dataset contains the following variables:

* PatientID – unique patient identifier.

* Age – patient age.

* Sex – patient sex.

* Race – patient race.

* Vitamin_D_level – measured vitamin D level.

* Asthma – asthma status.

* Symptoms – reported asthma symptoms.

* Allergy – allergy status.
5. Technologies Used

* Python – application programming language.

* Streamlit – web interface.

* pandas – data handling and analysis.

* Matplotlib / Seaborn – data visualization.

* ReportLab – PDF report generation.

6. Limitations

The results depend on the quality and completeness of the input dataset. The application is intended for data exploration and educational purposes and does not provide medical diagnoses.