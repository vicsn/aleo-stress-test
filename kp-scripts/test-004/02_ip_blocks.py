
# run the command aws ec2 describe-instances --query 'Reservations[*].Instances[*].[PublicIpAddress]' --output text

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

def get_block_height(IP):
    # call on IP port 3033/testnet3/latest/height
    cmd = "curl " + IP + ":3033/testnet3/latest/height"
    output = subprocess.check_output(cmd, shell=True)
    return output

block_height_first_node = get_block_height(first_node[1])
print(block_height_first_node)

port = 22
pem_file_path = '/Users/kp/.ssh/kp2.pem'
username = 'ubuntu'

private_key = paramiko.RSAKey.from_private_key_file(pem_file_path)

def block_IPs(ip_server, IP_list):
    if not IP_list:
        return
    
    print(f"Blocking IPs for server: {ip_server}")

    # Create an SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the server
    try:
        client.connect(hostname=ip_server, port=port, username=username, pkey=private_key)

        # Check if UFW is enabled
        stdin, stdout, stderr = client.exec_command("sudo ufw status")
        status_output = stdout.read().decode('utf-8').strip()

        # Enable UFW if not already enabled
        if "inactive" in status_output.lower():
            stdin, stdout, stderr = client.exec_command("echo 'y' | sudo ufw enable")
            print(stdout.read().decode('utf-8').strip())

        # Allow SSH connections
        client.exec_command("sudo ufw allow ssh")

        # Block IP addresses
        for ip in IP_list:
            deny_in_command = f"sudo ufw deny from {ip}"
            deny_out_command = f"sudo ufw deny out to {ip}"
            client.exec_command(deny_in_command)
            client.exec_command(deny_out_command)

        # Check UFW status after modifications
        stdin, stdout, stderr = client.exec_command("sudo ufw status verbose")
        print(stdout.read().decode('utf-8').strip())

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()





def block_IPs2(ip_server, IP_list):
    if not IP_list:
        return
    
    print(f"Blocking IPs for server: {ip_server}")

    # Create an SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the server
    try:
        client.connect(hostname=ip_server, port=port, username=username, pkey=private_key)

        # Block IP addresses using iptables
        for ip in IP_list:
            iptables_block_in = f"sudo iptables -A INPUT -s {ip} -j DROP"
            iptables_block_out = f"sudo iptables -A OUTPUT -d {ip} -j DROP"
            iptables_drop_established = f"sudo iptables -I INPUT -m conntrack --ctstate ESTABLISHED,RELATED -s {ip} -j DROP"
            client.exec_command(iptables_block_in)
            client.exec_command(iptables_block_out)
            client.exec_command(iptables_drop_established)


        # List iptables rules for verification
        stdin, stdout, stderr = client.exec_command("sudo iptables -L")
        print(stdout.read().decode('utf-8').strip())

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()



import re
import socket

def resolve_to_ip(domain_name):
    try:
        return socket.gethostbyname(domain_name)
    except socket.error:
        return None

def block_IPs3(ip_server, IP_list):
    if not IP_list:
        return
    
    print(f"Blocking IPs for server: {ip_server}")

    # Create an SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the server
    try:
        client.connect(hostname=ip_server, port=port, username=username, pkey=private_key)

        # Fetch existing iptables rules
        stdin, stdout, stderr = client.exec_command("sudo iptables -L")
        existing_rules = stdout.read().decode('utf-8').strip().splitlines()

        # Parse existing rules to extract IP addresses
        existing_ips = set()
        for line in existing_rules:
            if 'DROP' in line and '--' in line:
                parts = line.split()
                target = parts[3]  # The IP/domain is always at index 4 for DROP rules in this format
                if target:
                    resolved_ip = resolve_to_ip(target)
                    if resolved_ip:
                        existing_ips.add(resolved_ip)
                    else:
                        # If it's already an IP or resolution failed, add the original target
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