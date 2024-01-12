import json
import os

def get_file_size(filepath):
    return os.path.getsize(filepath)

def get_nested_json_field_size(json_data, nested_keys):
    current_data = json_data
    for key in nested_keys:
        if key in current_data:
            current_data = current_data[key]
        else:
            return None
    return len(json.dumps(current_data).encode('utf-8'))

def main():
    latest_block_number = 826  # Replace this with the actual latest block number
    for block_number in range(latest_block_number, latest_block_number - 5, -1):
        filename = f"{block_number}.json"
        if not os.path.exists(filename):
            print(f"File {filename} does not exist.")
            continue

        with open(filename, 'r') as file:
            block_data = json.load(file)

        block_size = get_file_size(filename)
        print(f"\nBlock {block_number} Size: {block_size} bytes")

        subdag_size = get_nested_json_field_size(block_data, ["authority", "subdag", "subdag"])
        if subdag_size is not None:
            print(f"Size of authority/subdag/subdag: {subdag_size} bytes")
        else:
            print("authority/subdag/subdag not found in the block data.")

        election_certificate_ids_size = get_nested_json_field_size(block_data, ["authority", "subdag", "election_certificate_ids"])
        if election_certificate_ids_size is not None:
            print(f"Size of authority/subdag/election_certificate_ids: {election_certificate_ids_size} bytes")
        else:
            print("authority/subdag/election_certificate_ids not found in the block data.")

if __name__ == "__main__":
    main()
