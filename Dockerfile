# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Update package list and install tcpdump
RUN apt-get update && apt-get install -y tcpdump iproute2 net-tools && \
    which tcpdump

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port that the Flask app will run on
EXPOSE 5000

# Grant privileges for traffic monitoring
RUN chmod u+s $(which tcpdump)

# Command to run the Flask app
CMD ["python", "webapp/app.py"]

