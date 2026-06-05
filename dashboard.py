import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
from datetime import datetime

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="AI Threat Detection System",
    layout="wide"
)

# -----------------------------------
# DARK THEME CSS
# -----------------------------------

st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        color: white;
    }

    .stApp {
        background-color: #0E1117;
    }

    h1, h2, h3 {
        color: #ff4b4b;
    }

    .stButton>button {
        background-color: red;
        color: white;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------
# LOGIN SYSTEM
# -----------------------------------

USERNAME = "admin"
PASSWORD = "admin123"

st.sidebar.title("Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if username == USERNAME and password == PASSWORD:

    st.success("Login Successful")

    # -----------------------------------
    # SIDEBAR
    # -----------------------------------

    st.sidebar.title("Cybersecurity Dashboard")
    st.sidebar.write("AI Threat Monitoring System")

    # -----------------------------------
    # TITLE
    # -----------------------------------

    st.markdown(
        "<h1>AI-Driven Threat Detection System</h1>",
        unsafe_allow_html=True
    )

    # -----------------------------------
    # LOAD DATASET
    # -----------------------------------

    data = pd.read_csv("dataset/logins.csv")

    # -----------------------------------
    # MACHINE LEARNING MODEL
    # -----------------------------------

    X = data[['login_time', 'failed_attempts', 'ip_score']]

    model = IsolationForest(
        contamination=0.2,
        random_state=42
    )

    model.fit(X)

    data['prediction'] = model.predict(X)

    data['prediction'] = data['prediction'].map({
        1: 'Normal',
        -1: 'Suspicious'
    })

    # -----------------------------------
    # SHOW DATASET
    # -----------------------------------

    st.subheader("Login Activity Dataset")

    st.write(data)

    # -----------------------------------
    # SUSPICIOUS USERS
    # -----------------------------------

    st.subheader("Suspicious Users")

    suspicious_users = data[
        data['prediction'] == 'Suspicious'
    ]

    st.write(suspicious_users)

    # -----------------------------------
    # METRICS
    # -----------------------------------

    threat_count = len(suspicious_users)

    col1, col2 = st.columns(2)

    col1.metric("Total Users", len(data))
    col2.metric("Threats Detected", threat_count)

    # -----------------------------------
    # ALERTS
    # -----------------------------------

    st.subheader("Threat Summary")

    st.error(
        f"Suspicious Activities Detected: {threat_count}"
    )

    if threat_count > 0:
        st.warning("⚠️ Threat Detected!")
    else:
        st.success("✅ System Secure")

    # -----------------------------------
    # BAR CHART
    # -----------------------------------

    st.subheader("Failed Login Attempts")

    st.bar_chart(data['failed_attempts'])

    # -----------------------------------
    # PIE CHART
    # -----------------------------------

    st.subheader("Threat Distribution")

    fig, ax = plt.subplots()

    data['prediction'].value_counts().plot.pie(
        autopct='%1.1f%%',
        ax=ax
    )

    st.pyplot(fig)

    # -----------------------------------
    # DOWNLOAD REPORT
    # -----------------------------------

    csv = data.to_csv(index=False)

    st.download_button(
        label="Download Threat Report",
        data=csv,
        file_name='threat_report.csv',
        mime='text/csv',
    )

    # -----------------------------------
    # LIVE THREAT PREDICTION
    # -----------------------------------

    st.subheader("Live Threat Prediction")

    login_time = st.number_input(
        "Login Time",
        0,
        23
    )

    failed_attempts = st.number_input(
        "Failed Attempts",
        0,
        10
    )

    ip_score = st.number_input(
        "IP Score",
        0,
        10
    )

    if st.button("Predict Threat"):

        new_data = [[
            login_time,
            failed_attempts,
            ip_score
        ]]

        prediction = model.predict(new_data)

        current_time = datetime.now()

        # -----------------------------------
        # THREAT DETECTION
        # -----------------------------------

        if prediction[0] == -1:

            st.error(
                "⚠️ Suspicious Activity Detected!"
            )

            # SAVE ALERT LOG
            with open("alerts.txt", "a") as file:

                file.write(
                    f"Threat detected at {current_time}\n"
                )

        else:

            st.success("✅ Normal Activity")

# -----------------------------------
# INVALID LOGIN
# -----------------------------------

else:

    st.warning("Please Login to Access Dashboard")