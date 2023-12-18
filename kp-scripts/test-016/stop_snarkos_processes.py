import subprocess

# Function to get all running snarkos processes
def get_snarkos_processes():
    try:
        # Running the command "ps aux | grep 'snarkos'" and capturing the output
        output = subprocess.check_output(["ps", "aux"])
        processes = output.decode('utf-8').split('\n')

        # Filtering the processes to find those that contain 'snarkos'
        snarkos_processes = [proc for proc in processes if 'snarkos' in proc]

        return snarkos_processes
    except Exception as e:
        return f"Error: {str(e)}"

# Function to kill the snarkos processes
def kill_snarkos_processes():
    snarkos_processes = get_snarkos_processes()
    if isinstance(snarkos_processes, str):
        return snarkos_processes  # Return error message if any

    killed_processes = []
    for proc in snarkos_processes:
        try:
            # Extracting the PID (process ID) which is the second element in the process details
            pid = int(proc.split()[1])
            # Killing the process
            subprocess.run(["kill", str(pid)])
            killed_processes.append(pid)
        except Exception as e:
            return f"Error killing process {pid}: {str(e)}"

    return killed_processes if killed_processes else "No snarkos processes found."

# Get and kill snarkos processes
killed_processes = kill_snarkos_processes()
killed_processes
