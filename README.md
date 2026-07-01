# AI-Based Threat Detection System

## Project Overview

The AI-Based Threat Detection System is a cybersecurity monitoring application that uses Machine Learning to identify suspicious login activities. The system provides a real-time dashboard for monitoring user logins, detecting anomalies, generating alerts, and storing data in both CSV files and a MySQL database.

---

## Features

- User Login Authentication
- AI-Based Threat Detection using Isolation Forest
- Real-Time Threat Prediction
- Suspicious Activity Detection
- Threat Summary Dashboard
- Downloadable Threat Report (CSV)
- Automatic Alert Generation
- MySQL Database Integration
- Login Activity Storage
- Alert History Storage
- Interactive Data Visualization
- Streamlit Web Dashboard

---

## Technologies Used

- Python
- Streamlit
- Machine Learning (Isolation Forest)
- Pandas
- Scikit-learn
- Matplotlib
- MySQL
- MySQL Connector for Python

---

## Project Structure

```
AI-Based-Threat-Detection-System/
│
├── dashboard.py
├── models.py
├── db.py
├── alerts.txt
├── README.md
│
├── dataset/
│   └── logins.csv
│
└── requirements.txt
```

---

## Database

### Database Name

```
threat_detection
```

### Tables

### users
Stores user login credentials.

### logins
Stores every login activity along with prediction results.

Columns:
- username
- login_time
- failed_attempts
- ip_score
- status
- prediction

### alerts
Stores detected security alerts.

Columns:
- username
- alert_message
- alert_time

---

## Machine Learning Model

Algorithm Used:

- Isolation Forest

Input Features:

- Login Time
- Failed Login Attempts
- IP Score

Prediction Output:

- Normal
- Suspicious

---

## Dashboard Features

- Login Authentication
- View Login Dataset
- View Suspicious Users
- Threat Summary
- Failed Login Attempts Chart
- Threat Distribution Pie Chart
- Live Threat Prediction
- Download Threat Report

---

## How to Run the Project

### 1. Install Required Libraries

```bash
pip install streamlit pandas matplotlib scikit-learn mysql-connector-python
```

### 2. Create Database

```sql
CREATE DATABASE threat_detection;
```

### 3. Create Required Tables

- users
- logins
- alerts

### 4. Configure MySQL Connection

Update your `db.py` file with your MySQL username and password.

### 5. Run the Project

```bash
streamlit run dashboard.py
```

---

## Future Enhancements

- Email Alerts
- SMS Notifications
- Real-Time IP Tracking
- User Management System
- Admin Dashboard
- Deep Learning-Based Threat Detection
- Cloud Database Integration

---

## Author

**Mahesh Goud**

B.Tech (Computer Science Engineering)

AI-Based Cybersecurity Project

---