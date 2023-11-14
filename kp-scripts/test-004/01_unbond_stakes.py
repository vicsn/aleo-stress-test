from helper import *

# todo make addresses/pks a list and expand addresses and private keys from helper to 24

ec2_instances = get_ec2_instances()
first_node = ec2_instances[0]
print(first_node)

committee_first_node = get_committee(first_node[1])
