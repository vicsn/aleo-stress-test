#!/bin/bash

set -e

# Read the approver private key from the user
#read -p "Enter the private key with positive public account balance: " approver_private_key
# Read the approver view key from the user
#read -p "Enter the associated view key: " approver_view_key
# Read the approver addresss from the user
#read -p "Enter the associated address: " approver_address

# Set the keys of a validator, they will get public tokens for validating
val_0_private_key="APrivateKey1zkp8CZNn3yeCseEtxuVPbDCwSyhGW6yZKUYKfgXmcpoGPWH"
val_0_view_key="AViewKey1mSnpFFC8Mj4fXbK5YiWgZ3mjiV8CxA79bYNa8ymUpTrw"
val_0_address="aleo1rhgdu77hgyqd3xjj8ucu3jj9r2krwz6mnzyd80gncr5fxcwlh5rsvzp9px"

spender_tester_1_private_key="APrivateKey1zkp4aaUAYt2uuQzNXenZTTnv8jts1efQjv8XboJMU2y1NrP"
spender_tester_1_view_key="AViewKey1jGCzaWqEZQDejdsB41detVWR6qWKqaLptDjUHAirVoYv"
spender_tester_1_address="aleo1vl0zuh5lun7mgsutnnegh40dv5tz2dz00uydlkegdgmsc7tlwupqlm25l6"

# get block height before submitting transaction
block_height_before_transaction_submit=$(curl http://127.0.0.1:3030/testnet3/latest/height)

# store block height before submitting transaction in a text file called 4.txt
echo ${block_height_before_transaction_submit} > 4.txt


# query balance
#echo "querying balance of the validator 0"
#val_0_balance=$(curl -s http://127.0.0.1:3030/testnet3/program/credits.aleo/mapping/account/${val_0_address})
#echo "result: ${val_0_balance}"

# Remove only the enclosing quotes
#val_0_balance_shortened="${val_0_balance%\"}"
#val_0_balance_shortened="${val_0_balance_shortened#\"}"

#echo "shortened result: ${val_0_balance_shortened}"


# Create record
echo sending transaction
snarkos developer execute credits.aleo transfer_public_to_private ${spender_tester_1_address} 1000000000u64 --private-key ${val_0_private_key} --query "http://localhost:3030" --broadcast "http://localhost:3030/testnet3/transaction/broadcast"

echo letting record creation settle for 20 seconds...
sleep 20

echo scanning for record on the chain
records=$(snarkos developer scan -v ${spender_tester_1_view_key} --start ${block_height_before_transaction_submit} --endpoint "http://localhost:3030")
echo ${records}
first_record=$(echo $records | jq -j '.[0]')
echo "found record: " $first_record

echo done