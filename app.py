import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Data Analysis App", layout="wide")  # nicer layout

st.title("Data Analysis App 📊")

# File uploader with help text
uploaded_file = st.file_uploader(
    "Upload your CSV or Excel file",
    type=['csv', 'xlsx', 'xls'],
    help="Supported: .csv, .xlsx, .xls"
)

if uploaded_file is not None:
    try:
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        
        if file_ext == '.csv':
            df = pd.read_csv(uploaded_file)
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload CSV or Excel.")
            st.stop()

        st.subheader("Data Preview")
        st.dataframe(df.head(10))  # better than st.write() for tables

        if st.checkbox("Show Summary Statistics", value=True):
            st.subheader("Summary Statistics")
            st.dataframe(df.describe())

        # Download section
        st.subheader("Export Results")
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download processed data as CSV",
            data=csv_data,
            file_name="processed_data.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.info("Common fixes: ensure file is not corrupted, and try re-uploading.")