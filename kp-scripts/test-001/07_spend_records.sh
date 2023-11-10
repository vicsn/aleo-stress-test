#!/bin/bash

# Set the keys of a validator, they will get public tokens for validating
val_0_private_key="APrivateKey1zkp8CZNn3yeCseEtxuVPbDCwSyhGW6yZKUYKfgXmcpoGPWH"
val_0_view_key="AViewKey1mSnpFFC8Mj4fXbK5YiWgZ3mjiV8CxA79bYNa8ymUpTrw"
val_0_address="aleo1rhgdu77hgyqd3xjj8ucu3jj9r2krwz6mnzyd80gncr5fxcwlh5rsvzp9px"

spender_tester_1_private_key="APrivateKey1zkp4aaUAYt2uuQzNXenZTTnv8jts1efQjv8XboJMU2y1NrP"
spender_tester_1_view_key="AViewKey1jGCzaWqEZQDejdsB41detVWR6qWKqaLptDjUHAirVoYv"
spender_tester_1_address="aleo1vl0zuh5lun7mgsutnnegh40dv5tz2dz00uydlkegdgmsc7tlwupqlm25l6"

spender_tester_2a_private_key="APrivateKey1zkpAA2PHBdPDwJxo7K9qiyMykz9tenBw7Fjy5WKrytRd7jo"
spender_tester_2a_view_key="AViewKey1hi36prBGKFh4sUsZYPJSw2MjNBmry6GRb6qhEQS1eyRA"
spender_tester_2a_address="aleo1tdr35vnju3c5yqcmlyph6s9fqdcv9m0sj3ct38dq0jdmktl6evyq7r3swh"

spender_tester_2b_private_key="APrivateKey1zkpFA4UGXwc3m9GUZwcBgqnofALcnBdwaitGVd7CBjGhiNM"
spender_tester_2b_view_key="AViewKey1eNPQH8pCgEFGkUSFZpPYcq6i3Qop6cxRf76rdhq6w5HK"
spender_tester_2b_address="aleo13d2ftqpapprwdz55j7qwgmlzmw7accd0t5yhe0y9x6s9clgckcgqcr73h9"


# get block height before submitting transaction
block_height_before_record_spending_large=$(curl http://127.0.0.1:3030/testnet3/latest/height)
block_height_before_record_spending_small=$(curl http://127.0.0.1:3040/testnet3/latest/height)

# store block height before submitting transaction in a text file called 7
echo ${block_height_before_record_spending_large} > 7_large.txt
echo ${block_height_before_record_spending_small} > 7_small.txt


# read the content of 4.txt into a variable called block_height_before_record_creation
block_height_before_record_creation=$(cat 4.txt)

# Scan for the record on the larger chain
records=$(snarkos developer scan -v ${spender_tester_1_view_key} --start 0 --endpoint "http://localhost:3030")
echo ${records}
first_record=$(echo $records | jq -j '.[0]')

echo "found record on the larger chain: " $first_record

## Spend record on the larger chain
snarkos developer execute credits.aleo transfer_private "${first_record}" ${spender_tester_2a_address} 100000u64 --private-key ${spender_tester_1_private_key} --query "http://localhost:3030" --broadcast "http://localhost:3030/testnet3/transaction/broadcast"

## Spend record on the smaller chain
snarkos developer execute credits.aleo transfer_private "${first_record}" ${spender_tester_2b_address} 100000u64 --private-key ${spender_tester_1_private_key} --query "http://localhost:3040" --broadcast "http://localhost:3040/testnet3/transaction/broadcast"
#snarkos developer execute credits.aleo transfer_public ${spender_tester_2b_address} 1000000000u64 --private-key ${spender_tester_1_private_key} --query "http://localhost:3040" --broadcast "http://localhost:3040/testnet3/transaction/broadcast"

echo letting transaction settle for 10 seconds...
sleep 10



# Scan for the record on the larger chain
records=$(snarkos developer scan -v ${spender_tester_2a_view_key} --start block_height_before_record_creation --endpoint "http://localhost:3030")
echo ${records}
first_record=$(echo $records | jq -j '.[0]')

echo "found record on the larger chain: " $first_record


# Scan for the record on the smaller chain
records=$(snarkos developer scan -v ${spender_tester_2b_view_key} --start block_height_before_record_creation --endpoint "http://localhost:3040")
echo ${records}
first_record=$(echo $records | jq -j '.[0]')

echo "found record on the smaller chain: " $first_record