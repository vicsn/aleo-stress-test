#!/bin/bash

# Read the total number of validators from the user or use a default value of 4
read -p "Enter the total number of validators (default: 20), this will start n-4 nodes: " total_validators
total_validators=${total_validators:-20}

# Create a timestamp-based directory for log files
log_dir=".logs"
mkdir -p "$log_dir"

# Create a new tmux session named "devnet"
tmux new-session -d -s "devnet" -n "window0"

# Generate validator indices from 0 to (total_validators - 1)
validator_indices=($(seq 4 $((total_validators - 1))))

# Loop through the list of validator indices and create a new window for each
for validator_index in "${validator_indices[@]}"; do
  # Generate a unique and incrementing log file name based on the validator index
  log_file="$log_dir/validator-$validator_index.log"

  # Create a new window with a unique name
  tmux new-window -t "devnet:$validator_index" -n "window$validator_index"

  # Send the command to start the validator to the new window and capture output to the log file
  tmux send-keys -t "devnet:window$validator_index" "snarkos start --nodisplay --dev $validator_index --dev-num-validators 4 --validator --verbosity 0 --logfile $log_file" C-m
done

# Attach to the tmux session to view and interact with the windows
tmux attach-session -t "devnet"