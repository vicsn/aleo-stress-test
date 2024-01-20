import subprocess
import time
from helper import *

def run_command(command, check_output=False):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing command: {command}\nError Output: {result.stderr}")
    if check_output and not result.stdout:
        print(f"No output returned for command: {command}")
    return result

def get_running_nodes():
    command = "ps aux | grep 'snarkos' | grep -v grep"
    process = run_command(command, check_output=True)

    running_nodes_ids = []
    running_nodes_pids = []
    for line in process.stdout.splitlines():
        if 'snarkos' in line:
            parts = line.split()
            pid = parts[1]
            node_id = parts[14]
            running_nodes_ids.append(node_id)
            running_nodes_pids.append(pid)
    
    return running_nodes_ids, running_nodes_pids

def terminate_existing_tmux_session(session_name):
    existing_sessions = run_command("tmux list-sessions")
    if session_name in existing_sessions.stdout:
        print(f"Terminating existing session '{session_name}'.")
        run_command(f"tmux kill-session -t {session_name}")

def create_tmux_session(session_name):
    terminate_existing_tmux_session(session_name)
    run_command(f"tmux new-session -d -s {session_name}")
    time.sleep(1)  # Wait for the session to be fully set up

def check_tmux_window_exists(session_name, window_name):
    check_window_command = f"tmux list-windows -t {session_name} | grep {window_name}"
    result = run_command(check_window_command)
    return result.returncode == 0

def manage_partitions(new_partitions, tmux_session="devnet", create_new_session=False):
    if create_new_session:
        print("Creating new tmux session.")
        create_tmux_session(tmux_session)

    current_nodes_ids_list, current_nodes_pids = get_running_nodes()
    current_nodes_ids = set(current_nodes_ids_list)

    nodes_to_shutdown = current_nodes_ids
    print(f"Nodes to Shutdown: {nodes_to_shutdown}")

    for node in nodes_to_shutdown:
        node_index_in_list = current_nodes_ids_list.index(node)

        port = 3030 + int(node)
        stop_url = f"http://127.0.0.1:{port}/testnet3/shutdown"
        run_command(f"curl {stop_url}")

        #run_command(f'kill {current_nodes_pids[node_index_in_list]}')

    print("Finished shutting down nodes, sleeping 5 seconds.")

    time.sleep(5)

    for i, partition in enumerate(new_partitions):
        list_of_other_partitions = new_partitions.copy()
        del list_of_other_partitions[i]

        # flatten list of partitions into a single list
        list_of_other_partitions = [item for sublist in list_of_other_partitions for item in sublist]

        partition_strings = [str(node) for node in partition]
        list_of_other_partitions_strings = [str(node) for node in list_of_other_partitions]

        nodes_to_start = partition_strings

        print(f"Nodes to Start: {nodes_to_start}")

        for j, node in enumerate(nodes_to_start):
            other_nodes = nodes_to_start.copy()
            del other_nodes[j]

            log_file = f'node_{node}.log'

            peers_string = ""
            if(j > 0):
                peer_port = 4030 + int(nodes_to_start[0])
                peers_string = f" --peers 127.0.0.1:{peer_port}"
            elif(j == 0 and len(nodes_to_start) > 1):
                peer_port = 4030 + int(nodes_to_start[1])
                peers_string = f" --peers 127.0.0.1:{peer_port}"
            elif(j == 0 and len(nodes_to_start) == 1):
                pass

            firstnodeinpartition_string = ""
            if(j == 0):
                firstnodeinpartition_string = " --firstnodeinpartition"

            nottrustedvalidators_string = ""
            if(len(list_of_other_partitions_strings) > 0):
                ips_of_nottrustedvalidators = [f"127.0.0.1:{5000 + int(node)}" for node in list_of_other_partitions_strings]
                nottrustedvalidators_string = f" --nottrustedvalidators {','.join(ips_of_nottrustedvalidators)}"
            nottrustedvalidators_string = ""

            print("nottrustedvalidators_string", nottrustedvalidators_string)

            trustedvalidators_string = ""
            if(len(other_nodes) > 0):
                ips_of_trustedvalidators = [f"127.0.0.1:{5000 + int(node)}" for node in other_nodes]
                trustedvalidators_string = f" --validators {','.join(ips_of_trustedvalidators)}"
                
            start_command = f"snarkos start --nodisplay --dev {node} --dev-num-validators {num_nodes} --validator --verbosity 0 --logfile {log_file}{peers_string}{trustedvalidators_string}{nottrustedvalidators_string}{firstnodeinpartition_string}"

            window_name = f'window{node}'
            if not check_tmux_window_exists(tmux_session, window_name):
                run_command(f"tmux new-window -t {tmux_session} -n '{window_name}'")
                time.sleep(0.5)  # Wait for window to be created
            run_command(f"tmux send-keys -t {tmux_session}:{window_name} '{start_command}' C-m")

    print("Finished starting nodes.")

initial_partitions = [[0, 1, 2, 3, 4, 5, 6, 7]]
num_nodes = len(initial_partitions[0])

# in this file, we assume equal balances of all nodes
target_node_weights = [1, 1, 1, 1, 1, 1, 1, 1]

def obtain_target_stake_balances():
    max_target_node_weight_index = target_node_weights.index(max(target_node_weights))
    max_weight = target_node_weights[max_target_node_weight_index]

    staked_balances = get_staked_balances(0)

    #address_of_node_with_max_weight = addresses[max_target_node_weight_index]

    credits_of_max_weight = staked_balances[max_target_node_weight_index]

    min_credits = min(staked_balances.values())

    for node in range(num_nodes):
        node_credits = staked_balances[node]
        if node_credits != min_credits:

            credits_to_unbond = int(staked_balances[node] - min_credits)

            unbond_credit(node, credits_to_unbond, 0)

            staked_balances = get_staked_balances(0)
            min_credits = min(staked_balances.values())
    


                
obtain_target_stake_balances()
