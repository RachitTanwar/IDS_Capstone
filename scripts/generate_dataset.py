import numpy as np
import pandas as pd

np.random.seed(42)
num_samples = 5000

# Generate features
features = {
    "packet_size": np.random.randint(20, 1500, num_samples),
    "duration": np.random.exponential(scale=1, size=num_samples),
    "protocol": np.random.choice([0, 1, 2], num_samples),
    "src_port": np.random.randint(1024, 65535, num_samples),
    "dst_port": np.random.randint(1, 1024, num_samples),
    "is_malicious": np.random.choice([0, 1], num_samples, p=[0.8, 0.2])
}

# Add noise to simulate malicious patterns
features["packet_size"] += features["is_malicious"] * np.random.randint(0, 500, num_samples)
features["duration"] += features["is_malicious"] * np.random.exponential(scale=2, size=num_samples)

# Save the dataset
df = pd.DataFrame(features)
df.to_csv("datasets/network_traffic.csv", index=False)
print("Dataset generated: network_traffic.csv")
