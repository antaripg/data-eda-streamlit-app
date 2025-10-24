import numpy as np
import pandas as pd
import streamlit as st
#from pandas_profiling import ProfileReport
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

# Web App Title
st.markdown('''
# **The EDA App**

This is the **EDA App** created in Streamlit using the **pandas-profiling** library.

**Credit:** App built in `Python` + `Streamlit` by [Chanin Nantasenamat](https://medium.com/@chanin.nantasenamat) (aka [Data Professor](http://youtube.com/dataprofessor))

''')
st.markdown("[Example CSV input file](https://raw.githubusercontent.com/dataprofessor/data/master/delaney_solubility_with_descriptors.csv)")
st.markdown("---")
if "pr" not in st.session_state:
    st.session_state["pr"] = None
if "uploaded" not in st.session_state:
    st.session_state["uploaded"] = False
if "uploaded_file_name" not in st.session_state:
    st.session_state["uploadedfile_name"] = None

# Upload CSV data
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
    if uploaded_file:
        st.session_state["uploaded_file_name"] = uploaded_file.name

@st.cache_data
def profile_report_gen(df, explorative=True):
    pr = ProfileReport(df, explorative=explorative)
    return pr

@st.cache_data
def load_csv():
    csv = pd.read_csv(uploaded_file, nrows=5000)
    return csv
    
# Pandas Profiling Report
if uploaded_file is not None:
    st.session_state["uploaded"] = True
    df = load_csv()
    if st.sidebar.button("Generate Data Report", 
    disabled=not st.session_state["uploaded"], width="stretch"):
        pr = profile_report_gen(df, explorative=True)
        st.session_state["pr"] = pr

    st.header('**Input DataFrame**')
    st.write(df)
    st.write('---')
    if st.session_state["pr"]:
        st.header('**Pandas Profiling Report**')
        st_profile_report(st.session_state["pr"])
    # Create HTML report in-memory
    if st.session_state["pr"]:
        html_report = st.session_state["pr"].to_html()
        # Download as HTML
        st.sidebar.download_button(
            label="📥 Download HTML Report",
            data=html_report,
            file_name=st.session_state["uploaded_file_name"].split(".")[0]+"_data_report.html",
            disabled = not st.session_state["uploaded"],
            mime="text/html"
        )
else:
    st.warning('Awaiting for CSV file to be uploaded. Download the example csv and upload or use your own csv')



