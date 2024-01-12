import asyncio
import aiohttp
import json

async def get_ec2_instances():
    cmd = "aws ec2 describe-instances --filters \"Name=instance-state-name,Values=running\" --query 'Reservations[*].Instances[*].[InstanceId, PublicIpAddress]' --output json"
    process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    output, error = await process.communicate()
    if error:
        print("Error:", error.decode())
    output = json.loads(output.decode())
    if output:
        output = output[0]
    return output

async def get_latest_block_height(session, ip):
    url = f"http://{ip}:3033/testnet3/latest/height"
    async with session.get(url) as response:
        return int(await response.text())

async def get_block(session, ip, height):
    url = f"http://{ip}:3033/testnet3/block/{height}"
    async with session.get(url) as response:
        return await response.json()

async def save_block(block, height):
    with open(f"{height}.json", 'w') as file:
        json.dump(block, file)

async def main():
    ec2_instances = await get_ec2_instances()
    if not ec2_instances:
        print("No running EC2 instances found.")
        return

    node_0_ip = ec2_instances[0][1]  # Assuming the first instance is node 0

    async with aiohttp.ClientSession() as session:
        latest_height = await get_latest_block_height(session, node_0_ip)
        for height in range(latest_height, latest_height - 5, -1):
            block = await get_block(session, node_0_ip, height)
            await save_block(block, height)
            print(f"Block {height} saved.")

asyncio.run(main())
