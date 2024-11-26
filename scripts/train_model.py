import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

def train_model():
    # Load dataset
    data = pd.read_csv('datasets/synthetic_data.csv')
    X = data.drop('label', axis=1)
    y = data['label']

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")

    # Save model
    joblib.dump(model, 'models/ids_model.pkl')
    print("Model saved at 'models/ids_model.pkl'.")

if __name__ == "__main__":
    train_model()

