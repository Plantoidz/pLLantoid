import json


def load_characters():
    with open('../characters/character_modes_v2.json', 'r') as file:
        return json.load(file)['characters']


def display_menu(characters):
    for idx, char in enumerate(characters):
        print(f"{idx + 1}. {char['name']} - {char['description']}")


def select_character(characters):
    while True:
        try:
            choice = int(input("Choose a character (1 to {}): ".format(len(characters)))) - 1
            if 0 <= choice < len(characters):
                return characters[choice]
            else:
                print("Invalid choice. Please choose between 1 and {}.".format(len(characters)))
        except ValueError:
            print("Please enter a valid number.")

def display_main_menu():
    print("\n\n1. Check the current config")
    print("2. Change the current config")
    print("3. Exit")

def display_current_config():
    try:
        with open('../working/config_characters_v2.json', 'r') as file:
            config = json.load(file)
            for char in config['characters']:
                print(f"Name: {char['name']}, Description: {char['description']}, Default Channel: {char['default_channel']}")
    except FileNotFoundError:
        print("Config file not found. Perhaps it hasn't been created yet.")

def change_current_config():
    characters = load_characters()
    selected_characters = []

    for i in range(8):
        print(f"\nSelect character {i + 1}:")
        display_menu(characters)
        choice = select_character(characters)
        character_copy = choice.copy()  # Making a copy to avoid modifying the original
        character_copy['default_channel'] = i  # Setting default channel
        selected_characters.append(character_copy)

    config = {
        "characters": selected_characters
    }

    with open('../working/config_characters_v2.json', 'w') as file:
        json.dump(config, file, indent=4)

    print("\nConfig saved to config_characters_v2.json")

def main():
    while True:
        display_main_menu()
        choice = input("\n\nSelect an option): ")

        if choice == "1":
            display_current_config()
        elif choice == "2":
            change_current_config()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == '__main__':
    main()

