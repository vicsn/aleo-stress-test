import json
import os

def get_file_size(filepath):
    return os.path.getsize(filepath)

def get_json_field_sizes(json_data):
    field_sizes = {}
    for key, value in json_data.items():
        field_sizes[key] = len(json.dumps(value).encode('utf-8'))
    return field_sizes

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

        field_sizes = get_json_field_sizes(block_data)
        for field, size in field_sizes.items():
            print(f"Field '{field}' Size: {size} bytes")

if __name__ == "__main__":
    main()
