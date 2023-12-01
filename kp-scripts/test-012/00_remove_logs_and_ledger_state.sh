#!/bin/bash

# Check if the .logs folder exists and delete it
if [ -d ".logs" ]; then
    echo ".logs folder found. Deleting..."
    rm -rf ".logs"
else
    echo ".logs folder does not exist."
fi

# Find and delete folders starting with .ledger-
for folder in .ledger-*; do
    if [ -d "$folder" ]; then
        echo "$folder found. Deleting..."
        rm -rf "$folder"
    else
        echo "No folders starting with .ledger- found."
    fi
done

echo "Operation completed."
