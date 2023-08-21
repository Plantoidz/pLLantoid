import os
import json
import random

def load_modes_from_file():
    with open('../modes/modes_single_v2.json', 'r') as file:
        return json.load(file)

MODES = load_modes_from_file()["MODES"]

def set_mode_data(mode):
    mode_data = MODES.get(mode)
    if not mode_data:
        print(f"Invalid mode: {mode}")
        return mode_data  # Return the mode data if valid, else None

def write_to_random_file(mode):
    with open('working/random.json', 'w') as file:
        json.dump({"random_mode": mode}, file)
    print(f"Randomly selected mode {mode} has been saved to random.json.")

if __name__ == "__main__":
    mode_names = list(MODES.keys())
    mode = random.choice(mode_names)

    mode_data = set_mode_data(mode)  # get mode data

    # Check if mode_data is not None (i.e., the mode was valid)
    if mode_data:
        write_to_random_file(mode)
        # If create_mode_directory function exists and you want to use it, uncomment the following lines
        # mode_directory = create_mode_directory(mode_data)
        # print(f"Data for mode {mode} has been set in directory {mode_directory}.")
