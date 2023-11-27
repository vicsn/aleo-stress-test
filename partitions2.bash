#!/bin/bash

# Declare validators with integer representation (e.g., 2/16 becomes 2)
declare -A start_validators=( [1]=2 [2]=3 [3]=6 [4]=5 )
f=5
n=$((3*f + 1))
total_weight=16 # Total weight to handle fractions

# Convert partition Python list to Bash array
start_partition=("1 2" "3 4")

is_byzantine() {
    local partition=("$@")
    w1=0
    for p in ${partition[0]}; do
        w1=$((w1 + start_validators[$p]))
    done
    w2=0
    for p in ${partition[1]}; do
        w2=$((w2 + start_validators[$p]))
    done
    if (( w1 > f*total_weight/n )) && (( w2 > f*total_weight/n )); then
        return 1 # False in Bash
    fi
    return 0 # True in Bash
}

swap() {
    local -a partition=($@)
    local -a part1=(${partition[0]})
    local -a part2=(${partition[1]})
    local a=${part1[$1]}
    local b=${part2[$2]}
    part1[$1]=$b
    part2[$2]=$a
    echo "${part1[*]} ${part2[*]}"
}

move() {
    local -a partition=($@)
    local -a part1=(${partition[0]})
    local -a part2=(${partition[1]})
    if [ ${#part1[@]} -eq 0 ]; then
        echo "${partition[*]}"
        return
    fi
    if [ $3 -ge ${#part1[@]} ]; then
        echo "${partition[*]}"
        return
    fi
    local a=${part1[$3]}
    unset part1[$3]
    part2+=($a)
    echo "${part1[*]} ${part2[*]}"
}

output_byzantine_partitions() {
    local partition=("$@")
    for i in ${!partition[0]}; do
        for j in ${!partition[1]}; do
            local new_partition=$(swap "${partition[@]}" $i $j)
            if is_byzantine $new_partition; then
                echo $new_partition
            fi
        done
    done
    for i in {0..9}; do
        start=$((i % 2))
        dest=$(((i + 1) % 2))
        local new_partition=$(move "${partition[@]}" $start $dest 0)
        if is_byzantine $new_partition; then
            echo $new_partition
        fi
    done
}

# Main loop
for i in {0..2}; do
    output_byzantine_partitions "${start_partition[@]}"
done
