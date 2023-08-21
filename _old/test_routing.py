import os
import re
from collections import defaultdict

def route_sound(filename, device_id, channel):
    # Dummy function to represent your route_sound method
    print(f"Routing {filename} to device {device_id} on channel {channel}")


def list_files_with_same_timestamp(directory):
    # List all files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Use regex to extract timestamp and counter from filenames
    pattern = r"(\d+)_affirmation(\d+).mp3"

    # Group files by timestamp
    timestamp_files = defaultdict(list)
    for file in files:
        match = re.match(pattern, file)
        if match:
            timestamp, counter = match.groups()
            timestamp_files[timestamp].append((int(counter), file))

    return timestamp_files


def main():
    directory = "working/affirmations"
    device_id = "1"  # Replace with your device ID
    
    timestamp_files = list_files_with_same_timestamp(directory)
    for timestamp, files in timestamp_files.items():
        # Sort the files based on counter for a deterministic order
        sorted_files = sorted(files, key=lambda x: x[0])

        for counter, filename in sorted_files:
            route_sound(os.path.join(directory, filename), device_id, counter)


if __name__ == "__main__":
    main()
