
# run the command aws ec2 describe-instances --query 'Reservations[*].Instances[*].[PublicIpAddress]' --output text

from helper import *

import subprocess
import json
import paramiko

def get_ec2_instances():
    cmd = "aws ec2 describe-instances --filters \"Name=instance-state-name,Values=running\" --query 'Reservations[*].Instances[*].[InstanceId, PublicIpAddress]' --output json"
    output = subprocess.check_output(cmd, shell=True)
    output = json.loads(output)
    output = output[0]
    return output

ec2_instances = get_ec2_instances()
first_node = ec2_instances[0]
print(first_node)

block_height_first_node = get_block_height(first_node[1])
print(block_height_first_node)

port = 22
pem_file_path = '/Users/kp/.ssh/kp2.pem'
username = 'ubuntu'

private_key = paramiko.RSAKey.from_private_key_file(pem_file_path)

desired_partition = [[10, 9, 5, 1, 11, 8, 7, 4, 0, 3, 6, 2], [16, 23, 18, 20, 17, 15, 19, 22, 21, 13, 12, 14]]

def block_IPs4(ip_server, IP_list):
    if not IP_list:
        return

    print(f"Blocking IPs for server: {ip_server}")

    # Create an SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the server
    try:
        client.connect(hostname=ip_server, port=port, username=username, pkey=private_key)

        # Fetch existing iptables rules with numeric IP addresses
        stdin, stdout, stderr = client.exec_command("sudo iptables -L -n --line-numbers")
        existing_rules = stdout.read().decode('utf-8').strip().splitlines()

        # Parse existing rules to extract IP addresses
        existing_ips = []
        existing_ips_line_numbers = []
        for line in existing_rules:
            if 'DROP' in line and '--' in line:
                parts = line.split()
                # Adjust the index based on the iptables output format
                target = parts[4]
                if(target == "0.0.0.0/0"):
                    target = parts[5]
                #if 'INPUT' in line else parts[8]
                existing_ips.append(target)
                line_number = parts[0]
                existing_ips_line_numbers.append(int(line_number))

            if(line == ''):
                break

        new_ips_to_block = set(IP_list) - set(existing_ips)
        old_ips_to_unblock = set(existing_ips) - set(IP_list)
        old_ips_to_unblock_indices = [existing_ips.index(ip) for ip in old_ips_to_unblock]
        old_ips_to_unblock_line_numbers = [existing_ips_line_numbers[index] for index in old_ips_to_unblock_indices]
        old_ips_to_unblock_line_numbers_sorted_reversed = sorted(old_ips_to_unblock_line_numbers, reverse=True)

        # Block new IP addresses
        for ip in new_ips_to_block:
            iptables_block_in = f"sudo iptables -A INPUT -s {ip} -j DROP"
            iptables_block_out = f"sudo iptables -A OUTPUT -d {ip} -j DROP"
            iptables_drop_established_in = f"sudo iptables -I INPUT -m conntrack --ctstate ESTABLISHED -s {ip} -j DROP"
            iptables_drop_established_out = f"sudo iptables -I OUTPUT -m conntrack --ctstate ESTABLISHED -d {ip} -j DROP"
            client.exec_command(iptables_block_in)
            client.exec_command(iptables_block_out)
            client.exec_command(iptables_drop_established_in)
            client.exec_command(iptables_drop_established_out)



        # Unblock old IP addresses
        for ln in old_ips_to_unblock_line_numbers_sorted_reversed:
            iptables_unblock_in = f"sudo iptables -D INPUT {ln}"
            iptables_unblock_out = f"sudo iptables -D OUTPUT {ln}"
            client.exec_command(iptables_unblock_in)
            client.exec_command(iptables_unblock_out)

        # List iptables rules for verification
        stdin, stdout, stderr = client.exec_command("sudo iptables -L")
        print(stdout.read().decode('utf-8').strip())

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()








for i in range(2):
    print("handling group " + str(i))
    group = desired_partition[i]
    other_group = desired_partition[1-i]
    ips_to_block = [ec2_instances[node_index][1] for node_index in other_group]

    for node_index in group:
        ip_of_node = ec2_instances[node_index][1]

        #ips_to_block = ["1.2.3.4"]

        a = 0

        block_IPs4(ip_of_node, ips_to_block)

        a = 0
ip_list = [item[1] for item in ec2_instances]

server_to_change = ip_list[4]
ip_list.remove(server_to_change)


#block_IPs(server_to_change, ip_list)
#block_IPs4(server_to_change, [ip_list[0]])
#block_IPs4(server_to_change, ip_list)

a = 0

#res = assign_security_group(first_node[0], 'sg-054a03275a77a6470')
#print(res)