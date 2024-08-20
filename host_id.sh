#!/bin/bash

# Step 1: Generate host_id
random_number=$((RANDOM % 89999 + 10000))  # Generates a random number between 10000 and 99999
timestamp=$(date +%s)  # Get the current timestamp
host_id=$(echo -n "$random_number$timestamp" | sha256sum | awk '{print $1}')  # Generate a SHA-256 hash

# Step 2: Retrieve the host's IP address
host_ip=$(hostname -I | awk '{print $1}')  # Get the first IP address

# Step 3: Upload the host_id and IP address via API
api_url="https://5.104.85.58/upload"  # Replace with your actual API endpoint
curl -X POST -H "Content-Type: application/json" \
    -d "{\"host_id\": \"$host_id\", \"ip\": \"$host_ip\"}" \
    $api_url

# Step 4: Save the host_id to ~/.host_id
echo "$host_id" > ~/.host_id

# Confirm the process
echo "host_id saved to ~/.host_id and uploaded to the server."
