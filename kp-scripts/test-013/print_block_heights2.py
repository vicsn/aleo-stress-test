import asyncio
import aiohttp
import json
import time
import os

# Threshold for unchanged height in seconds
unchanged_threshold = 300

async def get_ec2_instances():
    cmd = "aws ec2 describe-instances --filters \"Name=instance-state-name,Values=running\" --query 'Reservations[*].Instances[*].[InstanceId, PublicIpAddress]' --output json"
    process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    output, error = await process.communicate()
    if error:
        print("Error:", error.decode())
    output = json.loads(output.decode())
    output = output[0]
    return output

async def get_block_height(session, IP):
    url = f"http://{IP}:3033/testnet3/latest/height"
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
    ec2_instances = ec2_instances[:20]
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
