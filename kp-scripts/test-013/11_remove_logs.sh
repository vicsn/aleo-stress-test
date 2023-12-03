#!/bin/bash

# Determine the number of AWS EC2 instances by checking ~/.ssh/config
NODE_ID=0
while [ -n "$(grep "aws-n${NODE_ID}" ~/.ssh/config)" ]; do
    NODE_ID=$((NODE_ID + 1))
done

# Read the number of AWS EC2 instances to clean logs from the user
read -p "Enter the number of AWS EC2 instances to clean logs (default: $NODE_ID): " NUM_INSTANCES
NUM_INSTANCES="${NUM_INSTANCES:-$NODE_ID}"

echo "Removing .logs directory from $NUM_INSTANCES AWS EC2 instances."

# Define a function to remove the .logs directory from a node
remove_logs() {
  local NODE_ID=$1

  # The remote log directory
  REMOTE_LOG_DIR="/root/snarkOS/.logs"

  # SSH into the node and remove the entire log directory
  ssh -o StrictHostKeyChecking=no "aws-n$NODE_ID" "sudo rm -rf $REMOTE_LOG_DIR"

  # Check the exit status of the SSH command
  if [ $? -eq 0 ]; then
    echo "Logs directory on aws-n$NODE_ID removed successfully."
  else
    echo "Failed to remove logs directory on aws-n$NODE_ID."
  fi
}

# Loop through aws-n nodes and remove logs
for NODE_ID in $(seq 0 $((NUM_INSTANCES - 1))); do
  remove_logs $NODE_ID &
done

# Wait for all background jobs to finish
wait
