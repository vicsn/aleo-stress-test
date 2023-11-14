from helper import *

# todo make addresses/pks a list and expand addresses and private keys from helper to 24

ec2_instances = get_ec2_instances()
first_node = ec2_instances[0]
print(first_node)

committee_first_node = get_committee(first_node[1])

print(len(addresses))
print(len(private_keys))

validator_balances = []

for i, node in enumerate(ec2_instances):
    node_ip = node[1]
    node_address = addresses[i]
    validator_balance = committee_first_node["members"][node_address][0]
    validator_balances.append(validator_balance)

min_validator_balance = min(validator_balances)
target_validator_balance_3 = min_validator_balance
target_validator_balance_2 = int(2 * min_validator_balance / 3)
target_validator_balance_1 = int(1 * min_validator_balance / 3)

validator_balances_to_unbond = []

for i in range(0, 12):
    validator_balances_to_unbond.append(validator_balances[i]-target_validator_balance_1)

for i in range(12, 23):
    validator_balances_to_unbond.append(validator_balances[i]-target_validator_balance_2)

for i in range(23, 24):
    validator_balances_to_unbond.append(validator_balances[i]-target_validator_balance_3)

do_unbond = False

if(do_unbond):
    for i, node in enumerate(ec2_instances):
        to_unbond = validator_balances_to_unbond[i]
        if(to_unbond > 0):
            print(f"Unbonding {to_unbond} from node with IP {node[1]}")
            command=f"snarkos developer execute credits.aleo unbond_public {to_unbond}u64 --private-key {private_keys[i]} --query http://{node[1]}:3033 --broadcast http://{node[1]}:3033/testnet3/transaction/broadcast"
            # execute command locally
            output = subprocess.check_output(command, shell=True)
            print(output)
