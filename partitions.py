start_validators = {1: 1/20, 2:2/20, 3:2/20, 4:1/20, 5:5/20, 6:4/20, 7:2/20, 8:1/20, 9:1/20, 10:1/20}
elements = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for i in range(2000): 
    partition = generate_random_2_partition(elements)
    if len(partition[0])> 4 and len(partition[1])> 4: 
        if is_byzantine(partition, start_validators): 
            counts += 1
            print(partition)

