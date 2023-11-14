import aiohttp
import asyncio
import json
import os

async def send_json_file(file_path, url):
    async with aiohttp.ClientSession() as session:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            async with session.post(url, json=json_data) as response:
                if response.status == 200:
                    print(f"Successfully sent {file_path}")
                else:
                    print(f"Failed to send {file_path}, Status code: {response.status}")

async def main():
    folder = os.path.join(os.getcwd(), "kp-scripts", "test-005", "bonding_transactions")
    # set files_to_submit
    files_to_submit = []
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            files_to_submit.append(os.path.join(folder, file))
    
    a = 0
    url = "http://3.137.187.113:3033/testnet3/transaction/broadcast"

    tasks = [send_json_file(file, url) for file in files_to_submit]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
