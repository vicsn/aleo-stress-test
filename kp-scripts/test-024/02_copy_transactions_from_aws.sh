#!/bin/bash

# Directory to store remote logs
LOCAL_LOG_DIR="aws-transactions"

# Create the local log directory if it does not exist
mkdir -p "$LOCAL_LOG_DIR"

# Read IP addresses from ip_addresses.txt
IP_ADDRESSES=()
while IFS= read -r line; do
    IP_ADDRESSES+=("$line")
done < ip_addresses.txt

echo "Copying logs from ${#IP_ADDRESSES[@]} AWS EC2 instances."

# Define a function to copy logs from a node
copy_logs() {
  local IP_ADDRESS=$1
  local LOG_INDEX=$2
  local LOCAL_LOG_DIR=$3

  # Updated path to the log file on the remote server
  REMOTE_LOG_FILE="/root/aleo-stress-test/kp-scripts/test-024/program_deployments/all_deployments.txt"

  # Copy the log file directly using scp
  # Note: Using 'sudo' to access the root's file, ensure 'ubuntu' user has the necessary sudo permissions
  ssh -o StrictHostKeyChecking=no "ubuntu@$IP_ADDRESS" "sudo cat $REMOTE_LOG_FILE" > "$LOCAL_LOG_DIR/program_original-$LOG_INDEX.txt"

  # Check the exit status of the SCP command
  if [ $? -eq 0 ]; then
    echo "program_original.txt from $IP_ADDRESS copied successfully to program_original-$LOG_INDEX.txt."
  else
    echo "Failed to copy program_original.txt from $IP_ADDRESS."
  fi
}

# Loop through IPs and copy logs in parallel
for INDEX in "${!IP_ADDRESSES[@]}"; do
  copy_logs "${IP_ADDRESSES[$INDEX]}" "$INDEX" "$LOCAL_LOG_DIR" &
done

# Wait for all background jobs to finish
wait
