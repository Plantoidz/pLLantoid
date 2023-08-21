import os
import json

def load_modes_from_file():
    with open('../modes/modes.json', 'r') as file:
        return json.load(file)

def create_mode_directory(mode_data):
    modes_directory = '../modes'
    mode = mode_data['current_mode']
    mode_directory = os.path.join(modes_directory, mode)
    
    if not os.path.exists(mode_directory):
        os.makedirs(mode_directory)
        print(f"Directory for mode {mode} created.")
    else:
        print(f"Directory for mode {mode} already exists.")

    return mode_directory

MODES = load_modes_from_file()["MODES"]  # Directly access the "MODES" key after loading

def set_mode_data(mode):
    mode_data = MODES.get(mode)
    if not mode_data:
        print(f"Invalid mode: {mode}")
        return

    with open('../working/current_mode.json', 'w') as file:
        json.dump(mode_data, file)
    print(f"Mode {mode} has been set!")

if __name__ == "__main__":
    print("Select a mode:")
    mode_names = list(MODES.keys())
    for idx, mode in enumerate(mode_names, start=1):
        description = MODES[mode]["description"]
        print(f"{idx}: {mode} - {description}")

    total_modes = len(MODES)
    selection = int(input(f"Enter the mode number (1-{total_modes}): "))

    if 1 <= selection <= total_modes:
        mode = mode_names[selection-1]  # adjust index for 0-based list
        mode_data = MODES[mode]
        mode_directory = create_mode_directory(mode_data)
        set_mode_data(mode)
        print(f"Data for mode {mode} has been set in directory {mode_directory}.")
    else:
        print("Invalid selection!")
