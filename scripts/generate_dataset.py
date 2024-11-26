from sklearn.datasets import make_classification
import pandas as pd

def generate_dataset():
    X, y = make_classification(
        n_samples=1000,
        n_features=10,
        n_informative=5,
        n_redundant=3,
        n_classes=2,
        random_state=42,
    )
    data = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(10)])
    data['label'] = y
    data.to_csv('datasets/synthetic_data.csv', index=False)
    print("Synthetic dataset created at 'datasets/synthetic_data.csv'.")

if __name__ == "__main__":
    generate_dataset()

