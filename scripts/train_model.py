import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
import joblib

# Load the dataset
df = pd.read_csv("datasets/network_traffic.csv")

# Separate features and target
X = df.drop(columns=["is_malicious"])
y = df["is_malicious"]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Balance the dataset using SMOTE (Synthetic Minority Oversampling Technique)
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_balanced)
X_test_scaled = scaler.transform(X_test)

# Train the Random Forest model with regularization to avoid overfitting
model = RandomForestClassifier(
    n_estimators=50,  # Reduce the number of trees to prevent overfitting
    max_depth=10,     # Limit the depth of each tree
    random_state=42
)
model.fit(X_train_scaled, y_train_balanced)

# Evaluate the model
train_accuracy = accuracy_score(y_train_balanced, model.predict(X_train_scaled))
test_accuracy = accuracy_score(y_test, model.predict(X_test_scaled))

# Perform cross-validation
cv_scores = cross_val_score(model, X_train_scaled, y_train_balanced, cv=5, scoring="accuracy")
cv_mean_accuracy = cv_scores.mean()

# Print evaluation metrics
print(f"Training Accuracy: {train_accuracy:.2f}")
print(f"Testing Accuracy: {test_accuracy:.2f}")
print(f"Cross-Validation Accuracy: {cv_mean_accuracy:.2f}")

# Detailed classification report on test data
y_test_pred = model.predict(X_test_scaled)
print("\nClassification Report on Test Data:\n")
print(classification_report(y_test, y_test_pred))

# Save the model
joblib.dump(model, "models/ids_model.pkl")
print("Model saved as ids_model.pkl")

# Save the scaler for real-time traffic normalization
joblib.dump(scaler, "models/scaler.pkl")
print("Scaler saved as scaler.pkl")

joblib.dump(model, 'models/ids_model.joblib')