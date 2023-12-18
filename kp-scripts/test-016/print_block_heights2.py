import asyncio
import aiohttp
import json
import time
import os

num_nodes = 8

# Threshold for unchanged height in seconds
unchanged_threshold = 300

async def get_ec2_instances():
    output = []
    for i in range(0, num_nodes):
        output.append(["", "127.0.0.1:"+str(3030+i)])
    return output

async def get_block_height(session, IP):
    url = f"http://{IP}/testnet3/latest/height"
    async with session.get(url) as response:
        return await response.text()

async def query_heights(session, ec2_instances, last_heights, last_change_time):
    tasks = [get_block_height(session, node[1]) for node in ec2_instances]
    heights = await asyncio.gather(*tasks)
    unchanged_count = 0

    for i, (height, last_height, last_change) in enumerate(zip(heights, last_heights, last_change_time)):
        if height == last_height:
            unchanged_duration = time.time() - last_change
            if unchanged_duration > unchanged_threshold:
                print(f"Node {i} has height {height} - not changed for {int(unchanged_duration)} seconds")
                unchanged_count += 1
            else:
                print(f"Node {i} has height {height}")
        else:
            last_heights[i] = height
            last_change_time[i] = time.time()
            print(f"Node {i} has height {height}")

    return unchanged_count

async def main():
    ec2_instances = await get_ec2_instances()
    ec2_instances = ec2_instances[:num_nodes]
    last_heights = [""] * len(ec2_instances)
    last_change_time = [time.time()] * len(ec2_instances)

    async with aiohttp.ClientSession() as session:
        while True:
            unchanged_count = await query_heights(session, ec2_instances, last_heights, last_change_time)
            os.system('cls' if os.name == 'nt' else 'clear')
            for i, height in enumerate(last_heights):
                unchanged_duration = time.time() - last_change_time[i]
                if unchanged_duration > unchanged_threshold:
                    print(f"Node {i} has height {height} - not changed for {int(unchanged_duration)} seconds")
                else:
                    print(f"Node {i} has height {height}")
            print(f"{unchanged_count} of {len(ec2_instances)} node heights have not changed for more than {unchanged_threshold} seconds")
            await asyncio.sleep(10)

asyncio.run(main())
