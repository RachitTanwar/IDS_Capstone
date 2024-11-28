import numpy as np
import pandas as pd

np.random.seed(42)

num_samples = 5000

# Generate legitimate traffic
legitimate = {
    "packet_size": np.random.randint(40, 1000, num_samples // 2),
    "duration": np.random.exponential(scale=0.5, size=num_samples // 2),
    "protocol": np.random.choice([0, 1], num_samples // 2),  # 0: TCP, 1: UDP
    "src_port": np.random.randint(1024, 65535, num_samples // 2),
    "dst_port": np.random.choice([80, 443, 53], num_samples // 2),  # HTTP, HTTPS, DNS
    "is_malicious": np.zeros(num_samples // 2)  # Legitimate
}

# Generate malicious traffic
malicious = {
    "packet_size": np.random.randint(800, 1500, num_samples // 2),  # Large packets for DDoS
    "duration": np.random.exponential(scale=3, size=num_samples // 2),  # Longer sessions
    "protocol": np.random.choice([0, 1, 2], num_samples // 2),  # Include ICMP
    "src_port": np.random.randint(1, 1024, num_samples // 2),  # Uncommon source ports
    "dst_port": np.random.choice([22, 21, 3389], num_samples // 2),  # SSH, FTP, RDP
    "is_malicious": np.ones(num_samples // 2)  # Malicious
}

# Combine and shuffle
legitimate_df = pd.DataFrame(legitimate)
malicious_df = pd.DataFrame(malicious)
df = pd.concat([legitimate_df, malicious_df]).sample(frac=1).reset_index(drop=True)

# Save the dataset
df.to_csv("realistic_network_traffic.csv", index=False)
print("Realistic dataset generated: realistic_network_traffic.csv")
