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

    running_nodes = []
    for line in process.stdout.splitlines():
        if 'snarkos' in line:
            parts = line.split()
            pid = parts[1]
            running_nodes.append(pid)
    
    return running_nodes

def terminate_existing_tmux_session(session_name):
    existing_sessions = run_command("tmux list-sessions")
    if session_name in existing_sessions.stdout:
        print(f"Terminating existing session '{session_name}'.")
        run_command(f"tmux kill-session -t {session_name}")

def create_tmux_session(session_name):
    terminate_existing_tmux_session(session_name)
    run_command(f"tmux new-session -d -s {session_name}")
    time.sleep(1)  # Wait for the session to be fully set up

def manage_partitions(new_partitions, tmux_session="devnet"):
    create_tmux_session(tmux_session)

    current_nodes = set(get_running_nodes())
    new_nodes = set([str(node) for sublist in new_partitions for node in sublist])

    nodes_to_shutdown = current_nodes - new_nodes
    nodes_to_start = new_nodes - current_nodes

    print(f"Current Nodes: {current_nodes}")
    print(f"New Nodes: {new_nodes}")
    print(f"Nodes to Shutdown: {nodes_to_shutdown}")
    print(f"Nodes to Start: {nodes_to_start}")

    for node in nodes_to_shutdown:
        run_command(f'kill {node}')

    for node in nodes_to_start:
        log_file = f'node_{node}.log'
        total_validators = len(new_nodes)
        start_command = f"snarkos start --nodisplay --dev {node} --dev-num-validators {total_validators} --validator --verbosity 0 --logfile {log_file}"

        window_name = f'window{node}'
        run_command(f"tmux new-window -t {tmux_session} -n '{window_name}'")
        time.sleep(0.5)  # Wait for window to be created
        run_command(f"tmux send-keys -t {tmux_session}:'{window_name}' '{start_command}' C-m")

num_nodes = 8
new_partitions = [[0, 1, 2, 3, 4, 5, 6, 7]]
target_node_weights = [3, 1, 1, 1, 1, 1, 1, 1]

#manage_partitions(new_partitions)
# Sleep for 1 minute
#time.sleep(60)

def obtain_target_stake_balances():
    max_target_node_weight_index = target_node_weights.index(max(target_node_weights))
    max_weight = target_node_weights[max_target_node_weight_index]

    staked_balances = get_staked_balances(0)
    credits_of_max_weight = staked_balances[max_target_node_weight_index]

    for node in range(num_nodes):
        node_weight = target_node_weights[node]
        if node_weight != max_weight:
            target_node_credits = node_weight / max_weight * credits_of_max_weight

            credits_to_unbond = int(staked_balances[node] - target_node_credits)

            unbond_credit(node, credits_to_unbond, 0)

            staked_balances = get_staked_balances(0)
    
obtain_target_stake_balances()

a = 0