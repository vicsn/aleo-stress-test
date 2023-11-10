#!/bin/bash

# Validators weights
declare -A start_validators=(
  [1]="2/16"
  [2]="3/16"
  [3]="6/16"
  [4]="5/16"
)

# Start partition
start_partition=(1 2 3 4)

# Faults and total nodes
f=5
n=$((3*f+1))

# Check if partition is byzantine
is_byzantine() {
  local partition=("$@")
  local w1=0 w2=0

  # Calculate weight for first partition
  for p in ${partition[@]:0:2}; do
    w1=$(echo "$w1 + ${start_validators[$p]}" | bc -l)
  done

  # Calculate weight for second partition
  for p in ${partition[@]:2:2}; do
    w2=$(echo "$w2 + ${start_validators[$p]}" | bc -l)
  done

  # Check byzantine condition
  echo $(echo "$w1 > $f / $n" | bc -l) -eq 1 && echo $(echo "$w2 > $f / $n" | bc -l) -eq 1
}

# Swap elements between partitions
swap() {
  local -n p=$1
  local i=$2
  local j=$3

  local a=${p[$i]}
  local b=${p[$((j+2))]} # Offset by 2 for the second partition

  p[$i]=$b
  p[$((j+2))]=$a
}

# Move element between partitions
move() {
  local -n partition=$1
  local start=$2
  local dest=$3
  local i=$4

  if [ ${#partition[@]} -eq 0 ] || [ $i -ge 2 ]; then # Each partition has 2 elements
    return
  fi

  local a=${partition[$((start*2 + i))]} # Calculate index based on partition
  unset partition[$((start*2 + i))] # Remove from start
  partition[$((dest*2))]=$a # Add to dest
}

# Output byzantine partitions
output_byzantine_partitions() {
  local partition=("${start_partition[@]}")

  for i in {0..1}; do
    for j in {0..1}; do
      swap partition $i $j
      if is_byzantine "${partition[@]}"; then
        echo "Byzantine partition: ${partition[*]}"
      fi
      # Swap back to original for next iteration
      swap partition $i $j
    done
  done

  for i in {0..9}; do
    local start=$((i % 2))
    local dest=$(((i + 1) % 2))
    move partition $start $dest 0
    if is_byzantine "${partition[@]}"; then
      echo "Byzantine partition: ${partition[*]}"
    fi
  done
}

# Main execution
output_byzantine_partitions