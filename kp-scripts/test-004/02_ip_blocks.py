
# run the command aws ec2 describe-instances --query 'Reservations[*].Instances[*].[PublicIpAddress]' --output text

from helper import *

import subprocess
import json
import paramiko

ec2_instances = get_ec2_instances()
first_node = ec2_instances[0]
print(first_node)

block_height_first_node = get_block_height(first_node[1])
print(block_height_first_node)

port = 22
pem_file_path = '/Users/kp/.ssh/kp2.pem'
username = 'ubuntu'

private_key = paramiko.RSAKey.from_private_key_file(pem_file_path)


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
        stdin, stdout, stderr = client.exec_command("sudo iptables -L -n -v")
        existing_rules = stdout.read().decode('utf-8').strip().splitlines()

        # Parse existing rules to extract IP addresses
        existing_ips = set()
        for line in existing_rules:
            if 'DROP' in line and '--' in line:
                parts = line.split()
                # Adjust the index based on the iptables output format
                target = parts[7] if 'INPUT' in line else parts[8]
                existing_ips.add(target)

        new_ips_to_block = set(IP_list) - existing_ips
        old_ips_to_unblock = existing_ips - set(IP_list)

        # Block new IP addresses
        for ip in new_ips_to_block:
            iptables_block_in = f"sudo iptables -A INPUT -s {ip} -j DROP"
            iptables_block_out = f"sudo iptables -A OUTPUT -d {ip} -j DROP"
            client.exec_command(iptables_block_in)
            client.exec_command(iptables_block_out)

        # Unblock old IP addresses
        for ip in old_ips_to_unblock:
            iptables_unblock_in = f"sudo iptables -D INPUT -s {ip} -j DROP"
            iptables_unblock_out = f"sudo iptables -D OUTPUT -d {ip} -j DROP"
            client.exec_command(iptables_unblock_in)
            client.exec_command(iptables_unblock_out)

        # List iptables rules for verification
        stdin, stdout, stderr = client.exec_command("sudo iptables -L")
        print(stdout.read().decode('utf-8').strip())

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()










ip_list = [item[1] for item in ec2_instances]

server_to_change = ip_list[4]
ip_list.remove(server_to_change)


#block_IPs(server_to_change, ip_list)
block_IPs4(server_to_change, [ip_list[0]])
#block_IPs4(server_to_change, ip_list)

a = 0

#res = assign_security_group(first_node[0], 'sg-054a03275a77a6470')
#print(res)