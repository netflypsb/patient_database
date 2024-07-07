import streamlit as st
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import os

# Function to load data from the local CSV file
def load_data():
    df = pd.read_csv('patient_data.csv')
    df['Date of Birth'] = pd.to_datetime(df['Date of Birth'], format='%Y-%m-%d', errors='coerce')
    df['Visit Date'] = pd.to_datetime(df['Visit Date'], errors='coerce')
    df['Age'] = df['Date of Birth'].apply(lambda dob: (dt.datetime.now() - dob).days // 365)
    return df

# Function to save data to the local CSV file
def save_data(df):
    df.to_csv('patient_data.csv', index=False)
    st.write("Data saved successfully.")

# Load data from the CSV file
df = load_data()

# Sidebar: Select or create patient
action = st.sidebar.selectbox("Action", ["Select Patient", "Create New Patient"])

if action == "Select Patient":
    patient_id = st.sidebar.selectbox("Patient ID", df['Patient ID'].unique())

    # Display patient data
    patient_data = df[df['Patient ID'] == patient_id]
    if not patient_data.empty:
        st.header("General Information")
        st.write(f"**Patient ID:** {patient_id}")
        st.write(f"**Name:** {patient_data.iloc[0]['Patient Name']}")
        st.write(f"**Date of Birth:** {patient_data.iloc[0]['Date of Birth'].strftime('%Y-%m-%d')}")
        st.write(f"**Age:** {patient_data.iloc[0]['Age']}")
        st.write(f"**Gender:** {patient_data.iloc[0]['Gender']}")
        st.write(f"**Medical History:** {patient_data.iloc[0]['Medical History']}")
        st.write(f"**Allergies:** {patient_data.iloc[0]['Allergies']}")

        # Graphs of medical data
        st.header("Medical Data Over Time")
        fig, ax = plt.subplots(2, 2, figsize=(12, 8))
        ax[0, 0].plot(patient_data['Visit Date'], patient_data['Systolic BP'])
        ax[0, 0].set_title("Systolic Blood Pressure")
        ax[0, 1].plot(patient_data['Visit Date'], patient_data['Glucose'])
        ax[0, 1].set_title("Glucose")
        ax[1, 0].plot(patient_data['Visit Date'], patient_data['Cholesterol'])
        ax[1, 0].set_title("Cholesterol")
        ax[1, 1].plot(patient_data['Visit Date'], patient_data['Hemoglobin'])
        ax[1, 1].set_title("Hemoglobin")
        st.pyplot(fig)

        # Current visit input
        st.header("Current Visit")
        with st.form("current_visit_form"):
            new_visit_date = st.date_input("Visit Date", dt.date.today())
            complaint = st.text_area("Complaint")
            physical_exam = st.text_area("Physical Examination")
            systolic_bp = st.number_input("Systolic Blood Pressure", min_value=0)
            diastolic_bp = st.number_input("Diastolic Blood Pressure", min_value=0)
            temperature = st.number_input("Temperature", min_value=0.0, format="%.1f")
            glucose = st.number_input("Glucose", min_value=0)
            cholesterol = st.number_input("Cholesterol", min_value=0)
            hemoglobin = st.number_input("Hemoglobin", min_value=0)
            other_notes = st.text_area("Other Notes")
            submitted = st.form_submit_button("Add Entry")
            if submitted:
                new_entry = {
                    "Patient ID": patient_id,
                    "Patient Name": patient_data.iloc[0]['Patient Name'],
                    "Date of Birth": patient_data.iloc[0]['Date of Birth'],
                    "Age": patient_data.iloc[0]['Age'],
                    "Gender": patient_data.iloc[0]['Gender'],
                    "Medical History": patient_data.iloc[0]['Medical History'],
                    "Allergies": patient_data.iloc[0]['Allergies'],
                    "Visit Date": pd.to_datetime(new_visit_date).strftime('%Y-%m-%d'),
                    "Complaint": complaint,
                    "Physical Examination": physical_exam,
                    "Systolic BP": systolic_bp,
                    "Diastolic BP": diastolic_bp,
                    "Temperature": temperature,
                    "Glucose": glucose,
                    "Cholesterol": cholesterol,
                    "Hemoglobin": hemoglobin,
                    "Other Notes": other_notes,
                }
                df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
                st.write("New entry added to DataFrame.")

                # Save the updated data to CSV
                save_data(df)
                st.success("New visit entry added successfully!")

                # Reload data
                df = load_data()
                patient_data = df[df['Patient ID'] == patient_id]

        # Dropdown menu of previous visits
        st.header("Previous Visits")
        visit_date = st.selectbox("Select Visit Date", patient_data['Visit Date'].dt.strftime('%Y-%m-%d').unique())
        visit_data = patient_data[patient_data['Visit Date'] == pd.to_datetime(visit_date)]
        if not visit_data.empty:
            st.write(f"**Complaint:** {visit_data.iloc[0]['Complaint']}")
            st.write(f"**Physical Examination:** {visit_data.iloc[0]['Physical Examination']}")
            st.write(f"**Systolic BP:** {visit_data.iloc[0]['Systolic BP']}")
            st.write(f"**Diastolic BP:** {visit_data.iloc[0]['Diastolic BP']}")
            st.write(f"**Temperature:** {visit_data.iloc[0]['Temperature']}")
            st.write(f"**Glucose:** {visit_data.iloc[0]['Glucose']}")
            st.write(f"**Cholesterol:** {visit_data.iloc[0]['Cholesterol']}")
            st.write(f"**Hemoglobin:** {visit_data.iloc[0]['Hemoglobin']}")
            st.write(f"**Other Notes:** {visit_data.iloc[0]['Other Notes']}")
        else:
            st.write("No visit data available for the selected date.")
    else:
        st.write("No patient data available.")

elif action == "Create New Patient":
    st.header("Create New Patient Account")
    with st.form("new_patient_form"):
        new_patient_id = st.text_input("Patient ID")
        new_patient_name = st.text_input("Patient Name")
        new_dob = st.date_input("Date of Birth")
        new_age = (dt.datetime.now() - pd.to_datetime(new_dob)).days // 365
        new_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        new_med_history = st.text_area("Medical History")
        new_allergies = st.text_area("Allergies")
        new_submitted = st.form_submit_button("Add New Patient")
        if new_submitted:
            new_patient = {
                "Patient ID": new_patient_id,
                "Patient Name": new_patient_name,
                "Date of Birth": pd.to_datetime(new_dob).strftime('%Y-%m-%d'),
                "Age": new_age,
                "Gender": new_gender,
                "Medical History": new_med_history,
                "Allergies": new_allergies,
                "Visit Date": None,
                "Complaint": None,
                "Physical Examination": None,
                "Systolic BP": None,
                "Diastolic BP": None,
                "Temperature": None,
                "Glucose": None,
                "Cholesterol": None,
                "Hemoglobin": None,
                "Other Notes": None,
            }
            df = pd.concat([df, pd.DataFrame([new_patient])], ignore_index=True)
            st.write("New patient added to DataFrame.")

            # Save the updated data to CSV
            save_data(df)
            st.success("New patient account created successfully!")
