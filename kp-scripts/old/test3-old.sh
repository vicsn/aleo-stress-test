# ToDo split the network into f and 2f+1

approver_private_key="APrivateKey1zkp2FSVup2ZeHTrcXhrJrPxNppYoSnsWBAYDEe4Etg9oUDr"
approver_view_key="AViewKey1t1YKpReYpVq1A5JGb9HWE2d6Cy2MgSxypaRvuvDZeXw5"
approver_address="aleo1kpj88fn4zfvymfpse8mexpwnwjsmcwlqm9ynupj7tjnu044k8c9qg22wzs"

# Scan for the record
records=$(snarkos developer scan -v ${approver_view_key} --start 0 --endpoint "http://localhost:3030")
echo ${records}
first_record=$(echo $records | jq -j '.[0]')

echo "found record: " $first_record

## Spend record once
snarkos developer execute credits.aleo transfer_private "${first_record}" ${approver_address} 100000u64 --private-key ${approver_private_key} --query "http://localhost:3030" --broadcast "http://localhost:3030/testnet3/transaction/broadcast"

## Spend record twice on the other network
snarkos developer execute credits.aleo transfer_private "${first_record}" ${approver_address} 100000u64 --private-key ${approver_private_key} --query "http://localhost:3040" --broadcast "http://localhost:3040/testnet3/transaction/broadcast"

snarkos developer execute credits.aleo transfer_public_to_private ${approver_address} 100000u64 --private-key ${approver_private_key} --query "http://localhost:3040" --broadcast "http://localhost:3040/testnet3/transaction/broadcast"

## unbond so the little network can produce blocks

## merge the network

#snarkos developer execute token.aleo approve_public ${spender_tester_address} 1u64 --private-key ${approver_private_key} --query "http://localhost:3030" --broadcast "http://localhost:3030/testnet3/transaction/broadcast"

#snarkos developer execute token.aleo transfer_from_public ${approver_address} ${spender_tester_address} 1u64 --private-key ${spender_tester_private_key} --query "http://localhost:3030" --broadcast "http://localhost:3030/testnet3/transaction/broadcast"

