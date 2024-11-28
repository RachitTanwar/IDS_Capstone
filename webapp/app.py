from flask import Flask, render_template
from flask_socketio import SocketIO
import random
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

def simulate_traffic():
    """Simulate realistic real-time network traffic and emit updates to the client."""
    while True:
        # Total number of packets in this batch
        total_packets = random.randint(50, 100)
        malicious_packets = 0  # Counter for malicious packets
        traffic_details = []

        for _ in range(total_packets):
            # Generate realistic source and destination IPs
            src_ip = f"{random.randint(10, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
            dst_ip = f"{random.randint(172, 192)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

            # Protocol distribution (realistically, TCP is most common)
            protocol = random.choices(["TCP", "UDP", "ICMP"], weights=[70, 25, 5])[0]

            # Generate packet length based on protocol type
            if protocol == "TCP":
                packet_length = random.randint(64, 1500)
            elif protocol == "UDP":
                packet_length = random.randint(128, 512)
            else:  # ICMP
                packet_length = random.randint(64, 128)

            # Random source and destination ports (common ports for HTTP, HTTPS, DNS, etc.)
            src_port = random.choice(
                [80, 443, 22, 21, 25, 53, 110, 123, 161] + list(range(1024, 65535))
            )
            dst_port = random.choice([80, 443, 53, 3306, 3389])

            # Random traffic duration (in milliseconds or seconds)
            duration = round(random.uniform(0.01, 5.0), 3)

            # Malicious classification logic
            traffic_type = "legitimate"

            # Example malicious patterns
            if (
                packet_length > 1400  # Abnormally large packets
                or (protocol == "UDP" and src_port < 1024)  # Suspicious use of reserved ports
                or (dst_port in [22, 3389] and protocol == "TCP")  # Targeting SSH/RDP
                or (duration < 0.1 and packet_length < 100)  # Potential scanning or ping floods
                or random.random() < 0.1  # Random chance for unusual traffic
            ):
                traffic_type = "malicious"
                malicious_packets += 1

            # Create the packet dictionary
            packet = {
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "protocol": protocol,
                "packet_length": packet_length,
                "src_port": src_port,
                "dst_port": dst_port,
                "duration": duration,
                "traffic_type": traffic_type,
            }

            traffic_details.append(packet)

        # Emit the traffic update to the client
        socketio.emit(
            "traffic_update",
            {
                "total_packets": total_packets,
                "malicious_packets": malicious_packets,
                "traffic_details": traffic_details,
            },
        )

        # Pause before generating the next batch
        time.sleep(5)


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    threading.Thread(target=simulate_traffic, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)


