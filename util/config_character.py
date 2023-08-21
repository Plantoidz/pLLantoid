import json

#TODO: enable checking current configuration
def load_characters():
    with open('../characters/characters.json', 'r') as file:
        return json.load(file)['characters']

def display_menu(all_characters):
    for i, character in enumerate(all_characters, start=1):
        print(f"{i}. {character['name']}")

def select_character(all_characters):
    index = int(input("Enter the number for the character: ")) - 1
    if 0 <= index < len(all_characters):
        return all_characters[index]
    else:
        print("Invalid choice!")
        return select_character(all_characters)

def change_current_config():
    # TODO: enable number of channels selection
    # Step 1: Load all characters
    all_characters = load_characters()

    # Step 2: Ask user how many characters they want to select
    num_of_characters = int(input("How many characters do you want to select? "))
    while num_of_characters <= 0 or num_of_characters > len(all_characters):
        print("Invalid number. Please enter a number between 1 and the total number of characters.")
        num_of_characters = int(input("How many characters do you want to select? "))

    # Step 3: Let user select characters based on the provided number and modify their default_channel
    selected_characters = []
    selected_characters_map = {}

    for i in range(num_of_characters):
        print(f"\nSelect character {i + 1}:")
        display_menu(all_characters)
        choice = select_character(all_characters)
        selected_characters.append(choice)
        selected_characters_map[choice['name']] = i  # Mapping name to the default channel

    # Modify only the default_channel of the selected characters.
    for character in selected_characters:
        if character['name'] in selected_characters_map:
            character['default_channel'] = selected_characters_map[character['name']]

    config = {
        "characters": selected_characters
    }

    with open('../working/current_characters.json', 'w') as file:
        json.dump(config, file, indent=4)

    print(f"\nConfig saved to current_characters.json with the {num_of_characters} selected characters only.")

if __name__ == "__main__":
    change_current_config()
