from flask import Flask, render_template
from flask_socketio import SocketIO
import random
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

def simulate_traffic():
    """Simulate real-time network traffic and emit updates to the client."""
    while True:
        total_packets = random.randint(50, 100)
        malicious_packets = random.randint(0, total_packets // 3)
        traffic_details = [
            {
                "src_ip": f"192.168.1.{random.randint(1, 255)}",
                "dst_ip": f"10.0.0.{random.randint(1, 255)}",
                "protocol": random.choice(["TCP", "UDP", "ICMP"]),
                "packet_length": random.randint(64, 1500),
                "traffic_type": "malicious" if random.random() < 0.3 else "legitimate",
            }
            for _ in range(total_packets)
        ]
        socketio.emit("traffic_update", {
            "total_packets": total_packets,
            "malicious_packets": malicious_packets,
            "traffic_details": traffic_details,
        })
        time.sleep(5)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    threading.Thread(target=simulate_traffic, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

