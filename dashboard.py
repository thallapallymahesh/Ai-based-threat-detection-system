import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
from datetime import datetime
from db import conn, cursor

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

    data["prediction"] = model.predict(X)

    data["prediction"] = data["prediction"].map({
        1: "Normal",
        -1: "Suspicious"
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
        data["prediction"] == "Suspicious"
    ]

    st.write(suspicious_users)

    # -----------------------------------
    # METRICS
    # -----------------------------------

    threat_count = len(suspicious_users)

    cursor.execute("SELECT COUNT(*) FROM logins")
    total_mysql = cursor.fetchone()[0]

    col1, col2, col3 = st.columns(3)

    col1.metric("CSV Records", len(data))
    col2.metric("MySQL Records", total_mysql)
    col3.metric("Threats Detected", threat_count)

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
    # RECENT ALERTS FROM MYSQL
    # -----------------------------------

    st.subheader("Recent Alerts")

    cursor.execute("""
        SELECT username, alert_message, alert_time
        FROM alerts
        ORDER BY alert_time DESC
        LIMIT 5
    """)

    alerts = cursor.fetchall()

    if alerts:

        alert_df = pd.DataFrame(
            alerts,
            columns=[
                "Username",
                "Alert",
                "Time"
            ]
        )

        st.dataframe(
            alert_df,
            use_container_width=True
        )

    else:

        st.info("No Alerts Found")

        # -----------------------------------
    # BAR CHART
    # -----------------------------------

    st.subheader("Failed Login Attempts by User")

    fig, ax = plt.subplots(figsize=(10, 5))

    bars = ax.bar(
        data["username"],
        data["failed_attempts"],
        edgecolor="black",
        linewidth=1
    )

    # Show values on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            height + 0.1,
            str(int(height)),
            ha="center",
            fontsize=9,
            fontweight="bold"
        )

    ax.set_title("Failed Login Attempts", fontsize=14, fontweight="bold")
    ax.set_xlabel("Users", fontsize=11)
    ax.set_ylabel("Failed Attempts", fontsize=11)

    plt.xticks(rotation=45, ha="right")

    ax.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()

    st.pyplot(fig)


        # -----------------------------------
    # PIE CHART
    # -----------------------------------

    st.subheader("🛡️ Threat Distribution")

    fig, ax = plt.subplots(figsize=(6, 6))

    counts = data["prediction"].value_counts()

    colors = ["#2F80ED", "#EB5757"]  # Blue, Red

    wedges, texts, autotexts = ax.pie(
        counts,
        labels=counts.index,
        colors=colors,
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.62,
        textprops={
            "fontsize": 12,
            "fontweight": "bold",
            "color": "white"
        },
        wedgeprops={
            "edgecolor": "white",
            "linewidth": 2
        }
    )

    ax.set_aspect("equal")

    # Legend below the chart
    ax.legend(
        wedges,
        [f"{label} ({value:.1f}%)"
         for label, value in zip(
             counts.index,
             counts / counts.sum() * 100
         )],
        loc="lower center",
        bbox_to_anchor=(0.5, -0.08),
        ncol=2,
        fontsize=11,
        frameon=False
    )

    st.pyplot(fig)

        # DOWNLOAD REPORT
    csv = data.to_csv(index=False)

    st.download_button(
        label="Download Threat Report",
        data=csv,
        file_name="threat_report.csv",
        mime="text/csv",
    )

        # -----------------------------------
        # LIVE THREAT PREDICTION
        # -----------------------------------

st.subheader("Live Threat Prediction")

username_input = st.text_input("Username")

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

            if prediction[0] == -1:

                result = "Suspicious"

                st.error(
                    "⚠️ Suspicious Activity Detected!"
                )

                # Save alert to alerts.txt
                with open("alerts.txt", "a") as file:

                    file.write(
                        f"Threat detected at {current_time}\n"
                    )

                # Save alert to MySQL
                cursor.execute(
                    """
                    INSERT INTO alerts
                    (username, alert_message, alert_time)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        username_input,
                        "Threat Detected",
                        current_time
                    )
                )

                conn.commit()

            else:

                result = "Normal"

                st.success(
                    "✅ Normal Activity"
                )

            # -----------------------------------
            # ADD NEW RECORD
            # -----------------------------------

            if username_input == "":
                username_input = "live_user"

            new_row = pd.DataFrame({

                "username": [username_input],
                "login_time": [login_time],
                "failed_attempts": [failed_attempts],
                "ip_score": [ip_score],
                "status": ["live"],
                "prediction": [result]

            })

            data = pd.concat(
                [data, new_row],
                ignore_index=True
            )

            # -----------------------------------
            # SAVE TO MYSQL
            # -----------------------------------

            sql = """
            INSERT INTO logins
            (username, login_time, failed_attempts, ip_score, status, prediction)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                username_input,
                login_time,
                failed_attempts,
                ip_score,
                "live",
                result
            )

            cursor.execute(sql, values)
            conn.commit()

            # -----------------------------------
            # SAVE TO CSV
            # -----------------------------------

            data.to_csv(
                "dataset/logins.csv",
                index=False
            )

            st.success(
                "Record Added Successfully"
            )

            st.rerun()

# -----------------------------------
# INVALID LOGIN
# -----------------------------------

else:

    st.warning("Please Login to Access Dashboard")