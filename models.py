import pandas as pd
from sklearn.ensemble import IsolationForest

# Load dataset
data = pd.read_csv("dataset/logins.csv")

# Select numerical features
X = data[['login_time', 'failed_attempts', 'ip_score']]

# Train Isolation Forest model
model = IsolationForest(contamination=0.2, random_state=42)

# Fit model
model.fit(X)

# Predict anomalies
data['prediction'] = model.predict(X)

# Convert predictions
data['prediction'] = data['prediction'].map({
    1: 'Normal',
    -1: 'Suspicious'
})

# Show results
print("\nThreat Detection Results:\n")
print(data)