Code to test partitioning attack
* Ensure you have this snarkOS version installed: https://github.com/AleoHQ/snarkOS/tree/kp/fix/stress_test_5
* Run the python file 01 - currently, it runs the entire network, stops it, and starts a partitioned network

Concept:
* Generally, implement in Python
* Function that accepts a new list of lists of node IDs (that form a partition)
    * If previous partition:
        * Check process IDs with Grep and match process ID with node IDs
        * From the previous partitions, match them with the new partitions. Obtain a list of nodes to keep running, and a list of nodes to shut down
    * Else:
        * Obtain list of nodes to start, and empty list of nodes to shut down
    * Shut down nodes
    * Start new nodes, make sure they only connect to their peers 