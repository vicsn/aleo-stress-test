import subprocess
import time

def start_node(node_id, peer_port=None):
    command = [
        "snarkos", "start", "--nodisplay", "--dev", str(node_id), 
        "--dev-num-validators", "4", "--validator", "--verbosity", "0"
    ]
    # Set the peer port only if it's provided and not for nodes 0 and 4
    if peer_port and node_id not in [0, 4]:
        command.append("--peers")
        command.append(f"127.0.0.1:{peer_port}")
    log_file = f"node_{node_id}.log"
    with open(log_file, "w") as log:
        subprocess.Popen(command, stdout=log, stderr=log)

# Start first network
for i in range(4):
    peer_port = 4030 + i - 1 if i > 0 else None
    start_node(i, peer_port)

# Wait for 5 minutes
time.sleep(30000000)

# Start second network
for i in range(4, 8):
    peer_port = 4030 + i - 1 if i > 4 else None
    start_node(i, peer_port)
