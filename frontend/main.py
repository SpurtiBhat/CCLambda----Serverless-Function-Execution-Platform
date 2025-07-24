import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CCLambda", layout="centered")

API_URL = "http://localhost:8000"  # Backend running locally

# Session state for token
if "token" not in st.session_state:
    st.session_state.token = None

# Utility: Auth headers
def get_auth_headers():
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}

# -------------------------------
# Sidebar - Login
# -------------------------------
st.sidebar.title("🔐 Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
if st.sidebar.button("Login"):
    res = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
    if res.status_code == 200:
        st.session_state.token = res.json()["access_token"]
        st.sidebar.success("Login successful!")
    else:
        st.sidebar.error("Invalid credentials.")
st.sidebar.write("Token:", st.session_state.token)

# -------------------------------
# Tabs UI
# -------------------------------
tab1, tab2, tab3 = st.tabs(["📤 Upload Function", "⚡ Execute & Deploy", "📊 Monitor"])

# -------------------------------
# Tab 1: Upload via file
# -------------------------------
with tab1:
    st.header("📁 Upload and Deploy a Function")

    with st.form("upload_form"):
        name = st.text_input("Function Name")
        language = st.selectbox("Language", ["python", "javascript"])
        timeout = st.number_input("Timeout (seconds)", min_value=1, value=5)
        file = st.file_uploader("Upload function file", type=["py", "js"])
        submit = st.form_submit_button("Deploy")

        if submit and file:
            files = {'file': file}
            data = {"function_name": name, "language": language, "timeout": str(timeout)}

            res = requests.post(f"{API_URL}/deploy", data=data, files=files, headers=get_auth_headers())
            res_json = res.json()
            if res.status_code == 200 and "message" in res_json:
                st.success(res_json["message"])
            else:
                st.error(res_json.get("detail", "Deployment failed."))

# -------------------------------
# Tab 2: Paste Code & Execute
# -------------------------------
with tab2:
    st.header("🧪 Paste Code & Deploy")

    code = st.text_area("Paste Python code:")
    runtime = "docker"

    if st.button("Deploy via Text"):
        response = requests.post(f"{API_URL}/functions/", json={
            "name": "MyFunc",
            "code": code,
            "language": "python",
            "timeout": 3,
            "virtualization_type": runtime
        }, headers=get_auth_headers())
        if response.status_code == 200:
            st.success("Function deployed successfully.")
        else:
            st.error("Failed to deploy function.")

    st.subheader("⚡ Execute Deployed Function")
    res = requests.get(f"{API_URL}/functions/", headers=get_auth_headers())
    if res.status_code == 200:
        funcs = res.json()

        if funcs:
            selected_func = st.selectbox("Select Function", funcs, format_func=lambda f: f["name"])
            exec_platform = st.selectbox("Select Runtime for Execution", ["docker", "gvisor"], key="runtime_select")

            if st.button("Run Selected Function"):
                result = requests.post(
                    f"{API_URL}/run/{selected_func['id']}",
                    json={"runtime": exec_platform},
                    headers=get_auth_headers()
                )
                if result.status_code == 200:
                    st.code(result.json().get("output", "No output."))
                else:
                    st.error(result.json().get("detail", "Error running function."))
        else:
            st.info("No functions available.")
    else:
        st.error("Could not fetch functions.")

# -------------------------------
# Tab 3: Monitoring Dashboard
# -------------------------------
with tab3:
    st.header("📊 Function Monitoring Dashboard")

    res = requests.get(f"{API_URL}/monitor/summary", headers=get_auth_headers())
    if res.status_code == 200:
        data = res.json()
        
        if data:
            df = pd.DataFrame([
                {"Metric": "Total Functions", "Value": data["total_functions"]},
                {"Metric": "Languages", "Value": ", ".join(data["languages"])}
            ])
            st.dataframe(df)

            st.markdown("📌 *Detailed monitoring charts will appear once metrics per function are collected.*")
            st.markdown("📌 *Average execution time is in seconds.*")
        else:
            st.info("No metrics to display yet.")
    else:
        st.error("Failed to fetch monitoring data.")
