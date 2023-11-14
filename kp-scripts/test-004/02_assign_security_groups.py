
# run the command aws ec2 describe-instances --query 'Reservations[*].Instances[*].[PublicIpAddress]' --output text

import subprocess
import json

def get_ec2_instances():
    cmd = "aws ec2 describe-instances --filters \"Name=instance-state-name,Values=running\" --query 'Reservations[*].Instances[*].[InstanceId, PublicIpAddress]' --output json"
    output = subprocess.check_output(cmd, shell=True)
    output = json.loads(output)
    output = output[0]
    return output

ic2_instances = get_ec2_instances()
first_node = ic2_instances[0]
print(first_node)

def assign_security_group(instance_id, security_group_id):
    cmd = "aws ec2 modify-instance-attribute --instance-id " + instance_id + " --groups " + security_group_id
    output = subprocess.check_output(cmd, shell=True)
    return output

def get_block_height(IP):
    # call on IP port 3033/testnet3/latest/height
    cmd = "curl " + IP + ":3033/testnet3/latest/height"
    output = subprocess.check_output(cmd, shell=True)
    return output

block_height_first_node = get_block_height(first_node[1])
print(block_height_first_node)

#res = assign_security_group(first_node[0], 'sg-054a03275a77a6470')
#print(res)