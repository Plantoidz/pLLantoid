import json

def load_modes_from_file():
    with open('../modes/modes_ongoing.json', 'r') as file:
        return json.load(file)

MODES = load_modes_from_file()["MODES"]  # Directly access the "MODES" key after loading

def set_mode_data(mode):
    mode_data = MODES.get(mode)
    if not mode_data:
        print(f"Invalid mode: {mode}")
        return

    with open('../working/config_ongoing.json', 'w') as file:
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
        set_mode_data(mode)
    else:
        print("Invalid selection!")
