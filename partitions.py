start_validators = {1: 2/16, 2: 3/16, 3: 6/16, 4: 5/16}
start_partition = [[1,2], [3, 4]]
f = 5
n = 3*f + 1

def is_byzantine(partition, validators): 
    w1 = 0
    for p in partition[0]: 
        w1 += validators[p]
    w2 = 0
    for p in partition[1]: 
        w2 += validators[p]
    if w1 > f / n and w2 > f / n: 
        return False 
    return True  

def swap(p, i, j):  
    a = p[0].pop(i)
    b = p[1].pop(j)
    p[0].append(b)
    p[1].append(a)
    return [p[0], p[1]]

def move(partition, start, dest, i):
    if len(partition[start]) == 0: 
        return partition 
    if i >= len(partition[start]): 
        return partition
    a = partition[start].pop(i)
    partition[dest].append(a)
    return partition

def output_byzantine_partitions(start_partition, validators):
    partition = start_partition
    for i in range(len(partition[0])): 
        for j in range((len(partition[1]))): 
            partition = swap(partition, i, j)
            if is_byzantine(partition, validators): 
                print(partition)           
    for i in range(0, 10): 
        start = i % 2
        dest = (i + 1) % 2
        partition = move(partition, start, dest, 0)
        if is_byzantine(partition, validators): 
            print(partition)
        
       
        
for i in range(3): 
    output_byzantine_partitions(start_partition, start_validators)