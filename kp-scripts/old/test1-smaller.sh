set -e

# Read the approver private key from the user
#read -p "Enter the private key with positive public account balance: " approver_private_key
# Read the approver view key from the user
#read -p "Enter the associated view key: " approver_view_key
# Read the approver addresss from the user
#read -p "Enter the associated address: " approver_address

# Set the keys of a validator, they will get public tokens for validating
approver_private_key="APrivateKey1zkp8CZNn3yeCseEtxuVPbDCwSyhGW6yZKUYKfgXmcpoGPWH"
approver_view_key="AViewKey1mSnpFFC8Mj4fXbK5YiWgZ3mjiV8CxA79bYNa8ymUpTrw"
approver_address="aleo1rhgdu77hgyqd3xjj8ucu3jj9r2krwz6mnzyd80gncr5fxcwlh5rsvzp9px"

spender_tester_private_key="APrivateKey1zkp4aaUAYt2uuQzNXenZTTnv8jts1efQjv8XboJMU2y1NrP"
spender_tester_view_key="AViewKey1jGCzaWqEZQDejdsB41detVWR6qWKqaLptDjUHAirVoYv"
spender_tester_address="aleo1vl0zuh5lun7mgsutnnegh40dv5tz2dz00uydlkegdgmsc7tlwupqlm25l6"

spender_tester_private_key2="APrivateKey1zkpAA2PHBdPDwJxo7K9qiyMykz9tenBw7Fjy5WKrytRd7jo"
spender_tester_view_key2="AViewKey1hi36prBGKFh4sUsZYPJSw2MjNBmry6GRb6qhEQS1eyRA"
spender_tester_address2="aleo1tdr35vnju3c5yqcmlyph6s9fqdcv9m0sj3ct38dq0jdmktl6evyq7r3swh"


mkdir -p build_token
cp token.aleo build_token/main.aleo
cp token_program.json build_token/program.json

echo """

/* This is only used for testing the spec */
function mint_public:
    input r0 as address.public;
    input r1 as u64.public;
    async mint_public r0 r1 into r2;
    output r2 as token.aleo/mint_public.future;

finalize mint_public:
    input r0 as address.public;
    input r1 as u64.public;
    get.or_use account[r0] 0u64 into r2;
    add r2 r1 into r3;
    set r3 into account[r0];
""" >> build_token/main.aleo

mkdir -p build_spender_tester
cp spender_tester.aleo build_spender_tester/main.aleo
cp spender_tester_program.json build_spender_tester/program.json
mkdir -p build_spender_tester/imports
cp build_token/main.aleo build_spender_tester/imports/token.aleo

# deploy
snarkos developer deploy token.aleo --private-key ${approver_private_key} --query "http://localhost:3030" --path "build_token" --broadcast "http://localhost:3030/testnet3/transaction/broadcast" --priority-fee 0

snarkos developer deploy spender_tester.aleo --private-key ${approver_private_key} --query "http://localhost:3030" --path "build_spender_tester" --broadcast "http://localhost:3030/testnet3/transaction/broadcast" --priority-fee 0

echo letting deployments settle for a few seconds...
sleep 30

# mint tokens
snarkos developer execute token.aleo mint_public ${approver_address} 10u64 --private-key ${approver_private_key} --query "http://localhost:3030" --broadcast "http://localhost:3030/testnet3/transaction/broadcast"

# query balance
echo balance
curl http://127.0.0.1:3030/testnet3/program/credits.aleo/mapping/account/${approver_address}
curl http://127.0.0.1:3030/testnet3/program/credits.aleo/mapping/account/${spender_tester_address}

# transfer private from spender tester
#snarkos developer execute credits.aleo transfer_public_to_private ${spender_tester_address2} 100000u64 --private-key ${spender_tester_private_key} --query "http://localhost:3030" --broadcast "http://localhost:3030/testnet3/transaction/broadcast"

# Transfer to spender so they have enough to cover the fee
#snarkos developer execute credits.aleo transfer_public ${spender_tester_address} 100000u64 --private-key ${approver_private_key} --query "http://localhost:3030" --broadcast "http://localhost:3030/testnet3/transaction/broadcast"

# Transfer record to approver
snarkos developer execute credits.aleo transfer_public_to_private ${spender_tester_address} 1000000000u64 --private-key ${approver_private_key} --query "http://localhost:3030" --broadcast "http://localhost:3030/testnet3/transaction/broadcast"

echo letting record creation settle for a few seconds...
sleep 20

# Scan for the record
records=$(snarkos developer scan -v ${spender_tester_view_key} --start 0 --endpoint "http://localhost:3030")
echo ${records}
first_record=$(echo $records | jq -j '.[0]')
echo "found record: " $first_record

# get the current height
height=$(curl -s http://localhost:3030/testnet3/block/height/latest/)
