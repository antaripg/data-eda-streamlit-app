import streamlit as st
import pandas as pd
import io
import requests
import boto3

st.set_page_config(page_title="Smart Data Loader", layout="wide")

st.sidebar.header("📂 Data Source Selection")

# --- Data Source Choice
data_source = st.sidebar.selectbox(
    "Choose where your data is stored:",
    ["Upload CSV", "GitHub", "Google Drive", "AWS S3"]
)

df = None

# ---------------------------------------------------
# 1️⃣  File Upload
# ---------------------------------------------------
if data_source == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success(f"✅ Loaded: {uploaded_file.name}")

# ---------------------------------------------------
# 2️⃣  GitHub
# ---------------------------------------------------
elif data_source == "GitHub":
    github_url = st.sidebar.text_input("Enter GitHub CSV URL")

    if github_url:
        # Convert blob → raw if needed
        if "github.com" in github_url and "blob" in github_url:
            github_url = github_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

        st.sidebar.info(f"🔗 Using: {github_url}")

        # Optional token for private repos
        github_token = st.sidebar.text_input("GitHub Access Token (if private)", type="password")

        headers = {"Authorization": f"token {github_token}"} if github_token else {}
        try:
            r = requests.get(github_url, headers=headers)
            r.raise_for_status()
            df = pd.read_csv(io.StringIO(r.text))
            st.sidebar.success("✅ Data loaded from GitHub")
        except Exception as e:
            st.sidebar.error(f"❌ Error: {e}")

# ---------------------------------------------------
# 3️⃣  Google Drive
# ---------------------------------------------------
elif data_source == "Google Drive":
    drive_url = st.sidebar.text_input("Enter Google Drive File URL")

    if drive_url:
        try:
            # Extract file ID and create direct link
            file_id = drive_url.split("/d/")[1].split("/")[0]
            csv_url = f"https://drive.google.com/uc?id={file_id}"
            df = pd.read_csv(csv_url)
            st.sidebar.success("✅ Data loaded from Google Drive (public)")
        except Exception as e:
            st.sidebar.error(f"❌ Error: {e}")
            st.sidebar.info("If file is private, please provide service account or OAuth token (future support).")

# ---------------------------------------------------
# 4️⃣  AWS S3
# ---------------------------------------------------
elif data_source == "AWS S3":
    aws_access_key = st.sidebar.text_input("AWS Access Key ID", type="password")
    aws_secret_key = st.sidebar.text_input("AWS Secret Access Key", type="password")
    s3_bucket = st.sidebar.text_input("S3 Bucket Name")
    s3_key = st.sidebar.text_input("S3 File Path (e.g., folder/data.csv)")

    if all([aws_access_key, aws_secret_key, s3_bucket, s3_key]):
        try:
            s3 = boto3.client(
                "s3",
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key
            )
            obj = s3.get_object(Bucket=s3_bucket, Key=s3_key)
            df = pd.read_csv(io.BytesIO(obj["Body"].read()))
            st.sidebar.success("✅ Data loaded from S3")
        except Exception as e:
            st.sidebar.error(f"❌ Error: {e}")

# ---------------------------------------------------
# ✅ Show Data if Loaded
# ---------------------------------------------------
if df is not None:
    st.success("Data Loaded Successfully ✅")
    st.write(f"**Rows:** {len(df)} | **Columns:** {len(df.columns)}")
    st.dataframe(df.head())
else:
    st.info("Please select a data source and load your dataset.")
