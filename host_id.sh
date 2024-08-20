#!/bin/bash

# Step 1: Check if host_id file exists
host_id_file="$HOME/.host_id"

if [ -f "$host_id_file" ]; then
    # If the file exists, read the host_id from the file
    host_id=$(cat "$host_id_file")
    echo "Existing host_id found: $host_id"
else
    # If the file does not exist, generate a new host_id
    random_number=$((RANDOM % 89999 + 10000))  # Generates a random number between 10000 and 99999
    timestamp=$(date +%s)  # Get the current timestamp
    host_id=$(echo -n "$random_number$timestamp" | sha256sum | awk '{print $1}')  # Generate a SHA-256 hash

    # Save the new host_id to the file
    echo "$host_id" > "$host_id_file"
    echo "New host_id generated and saved: $host_id"
fi

# Step 2: Retrieve the host's IP address
host_ip=$(hostname -I | awk '{print $1}')  # Get the first IP address

# Step 3: Upload the host_id and IP address via API
api_url="http://5.104.85.58:5500/upload"  # Replace with your actual API endpoint
curl -X POST -H "Content-Type: application/json" \
    -d "{\"host_id\": \"$host_id\", \"host_ip\": \"$host_ip\"}" \
    $api_url

# Confirm the process
echo "host_id saved to $host_id_file and uploaded to the server."
