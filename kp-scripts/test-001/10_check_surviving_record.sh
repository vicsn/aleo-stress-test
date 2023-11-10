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


block_height_before_record_spending_large=$(cat 7_large.txt)
block_height_before_record_spending_small=$(cat 7_small.txt)


# Scan for the record on the larger chain
records=$(snarkos developer scan -v ${spender_tester_2a_view_key} --start block_height_before_record_spending_large --endpoint "http://localhost:3030")
echo ${records}
first_record=$(echo $records | jq -j '.[0]')

echo "found record on the larger chain: " $first_record


# Scan for the record on the node of the old smaller chain
records=$(snarkos developer scan -v ${spender_tester_2b_view_key} --start block_height_before_record_spending_small --endpoint "http://localhost:3040")
echo ${records}
first_record=$(echo $records | jq -j '.[0]')

echo "found record on the smaller chain: " $first_record