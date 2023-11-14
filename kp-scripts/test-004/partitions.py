
# This program will generate Byzantine partitions 

import random
import math  

f = 12
total_stake = 3*f + 1
num_byzantine_nodes = f
num_honest_nodes = f # there are f number of honest nodes BUT they have 2*f + 1 of the total stake 
num_nodes = 2*f 
stake_byzantine_nodes = f 
stake_honest_nodes = 2*f+1 

def assign_stake_to_partition(num_byzantine_nodes, num_honest_nodes, f): 
    
    # Every byzantine node has stake 1, every honest node has stake 2 (except for last with stake 3). 
    vals_to_stake = {} 
    for i in range(num_byzantine_nodes): 
        vals_to_stake[i] = 1 
    for i in range(num_byzantine_nodes, num_nodes): 
        vals_to_stake[i] = 2
    vals_to_stake[-1] = 3 
    
    return vals_to_stake 

def is_byzantine(f, partition, vals_to_stake): 
    w1 = 0
    for p in partition[0]: 
        w1 += vals_to_stake[p]
    w2 = 0
    for p in partition[1]: 
        w2 += vals_to_stake[p]
    if w1 > f and w2 > f: 
        return False 
    return True 

def weight(partition, subset): 
    w = 0 
    for p in partition[subset]: 
        w += p 
    return w  


def move(partition, start, dest, i):
    if len(partition[start]) == 0: 
        return partition 
    if i >= len(partition[start]): 
        return partition
    a = partition[start].pop(i)
    partition[dest].append(a)
    return partition

# Start partition looks like (V1, V2) , (V3, V4)
def gen_byzantine_partition(start_partition): 
    
    V1 = num_byzantine_nodes // 2 
    V2 = num_byzantine_nodes // 2 
    V3 = num_honest_nodes // 2 
    V4 = num_honest_nodes // 2 
    partition = start_partition.copy()
    
    # Partition will look like (V1,V2,V3), (V4)
    # move V3 
    for i in range(V3): 
        r = random.randint(0, len(partition[1])-1)
        partition = move(partition, 1, 0, r)

    if is_byzantine(f, partition, vals_to_stake): 
        print('Round 1: ', partition)
    
    
    #Partition will look like (V1), (V3, V4, V2)
    #move V2 
    for i in range(V2): 
        found = False 
        r = random.randint(0, len(partition[0]) - 1)
        while not found: 
            if vals_to_stake[partition[0][r]] == 1: 
                partition = move(partition, 0, 1, r)
                found = True 
            r = random.randint(0, len(partition[0]) - 1)
    if is_byzantine(f, partition, vals_to_stake): 
        print('Round 2: ', partition)
    
    #move V3 
    for i in range(V3): 
        found = False 
        r = random.randint(0, len(partition[0]) - 1)
        while not found: 
            if vals_to_stake[partition[0][r]] == 2 or vals_to_stake[partition[0][r]] == 3: 
                partition = move(partition, 0, 1, r)
                found = True 

            r = random.randint(0, len(partition[0]) - 1)
    if is_byzantine(f, partition, vals_to_stake): 
        print('Round 3: ', partition)

    # Partition will look like (V1, V2), (V3, V4)
    # move V1 
    for i in range(V1): 
        found = False 
        r = random.randint(0, len(partition[1]) - 1)
        while not found: 
            if vals_to_stake[partition[1][r]] == 1:
                partition = move(partition, 1, 0, r)
                found = True 
            r = random.randint(0, len(partition[1]) - 1)
    if is_byzantine(f, partition, vals_to_stake): 
        print('Round 4: ', partition)
    
    
    return partition 


vals_to_stake = assign_stake_to_partition(num_byzantine_nodes, num_honest_nodes, f)
start_partition = [[i for i in range(num_byzantine_nodes)]]
start_partition.append([i for i in range(num_byzantine_nodes, num_nodes)])  

partition = start_partition.copy()
for i in range(20): 
    print('Round 0 ', partition)
    partition = gen_byzantine_partition(partition) 
    print('')
    
    
    

        
