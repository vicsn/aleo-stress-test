#!/bin/bash

# Directory to store remote logs
LOCAL_LOG_DIR="remote-logs"

# Create the local log directory if it does not exist
mkdir -p "$LOCAL_LOG_DIR"

# Determine the number of AWS EC2 instances by checking ~/.ssh/config
NODE_ID=0
while [ -n "$(grep "aws-n${NODE_ID}" ~/.ssh/config)" ]; do
    NODE_ID=$((NODE_ID + 1))
done

# Read the number of AWS EC2 instances to query from the user
read -p "Enter the number of AWS EC2 instances to query (default: $NODE_ID): " NUM_INSTANCES
NUM_INSTANCES="${NUM_INSTANCES:-$NODE_ID}"

echo "Copying logs from $NUM_INSTANCES AWS EC2 instances."

# Define a function to copy logs from a node
copy_logs() {
  local NODE_ID=$1
  local LOCAL_LOG_DIR=$2

  # The remote log directory
  REMOTE_LOG_DIR="/root/snarkOS/.logs"
  REMOTE_ARCHIVE="/tmp/log_archive_$NODE_ID.tar.gz"

  # SSH into the node, use sudo to create an archive of the log directory, then copy it
  ssh -o StrictHostKeyChecking=no "aws-n$NODE_ID" "sudo tar -czf $REMOTE_ARCHIVE -C $(dirname $REMOTE_LOG_DIR) $(basename $REMOTE_LOG_DIR)"
  scp -o StrictHostKeyChecking=no "aws-n$NODE_ID:$REMOTE_ARCHIVE" "$LOCAL_LOG_DIR/log_archive_$NODE_ID.tar.gz"
  ssh -o StrictHostKeyChecking=no "aws-n$NODE_ID" "sudo rm $REMOTE_ARCHIVE"

  # Extract the archive in a specific subdirectory
  mkdir -p "$LOCAL_LOG_DIR/log$NODE_ID"
  tar -xzf "$LOCAL_LOG_DIR/log_archive_$NODE_ID.tar.gz" -C "$LOCAL_LOG_DIR/log$NODE_ID"
  rm "$LOCAL_LOG_DIR/log_archive_$NODE_ID.tar.gz"

  # Check the exit status of the SCP command
  if [ $? -eq 0 ]; then
    echo "Logs from aws-n$NODE_ID copied successfully."
  else
    echo "Failed to copy logs from aws-n$NODE_ID."
  fi
}

# Loop through aws-n nodes and copy logs in parallel
for NODE_ID in $(seq 0 $((NUM_INSTANCES - 1))); do
  copy_logs $NODE_ID $LOCAL_LOG_DIR &
done

# Wait for all background jobs to finish
wait
