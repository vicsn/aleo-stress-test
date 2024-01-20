import asyncio
import aiohttp
import time
import os

# Threshold for unchanged height in seconds
unchanged_threshold = 300

async def get_block_height(session, IP):
    url = f"{IP}testnet3/latest/height"
    async with session.get(url) as response:
        return await response.text()

async def query_heights(session, ec2_instances, last_heights, last_change_time):
    tasks = [get_block_height(session, node) for node in ec2_instances]
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
    ips = ["http://127.0.0.1:3030/", "http://127.0.0.1:3031/", "http://127.0.0.1:3032/", "http://127.0.0.1:3033/", "http://127.0.0.1:3034/", "http://127.0.0.1:3035/", "http://127.0.0.1:3036/", "http://127.0.0.1:3037/", "http://127.0.0.1:3038/", "http://127.0.0.1:3039/"]
    #ips = ["http://127.0.0.1:3030/", "http://127.0.0.1:3031/", "http://127.0.0.1:3032/", "http://127.0.0.1:3033/", "http://127.0.0.1:3034/"]

    last_heights = [""] * len(ips)
    last_change_time = [time.time()] * len(ips)

    async with aiohttp.ClientSession() as session:
        while True:
            unchanged_count = await query_heights(session, ips, last_heights, last_change_time)
            os.system('cls' if os.name == 'nt' else 'clear')
            for i, height in enumerate(last_heights):
                unchanged_duration = time.time() - last_change_time[i]
                if unchanged_duration > unchanged_threshold:
                    print(f"Node {i} has height {height} - not changed for {int(unchanged_duration)} seconds")
                else:
                    print(f"Node {i} has height {height}")
            print(f"{unchanged_count} of {len(ips)} node heights have not changed for more than {unchanged_threshold} seconds")
            await asyncio.sleep(10)

asyncio.run(main())
