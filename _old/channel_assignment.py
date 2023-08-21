import json
import threading
import requests

# Global channel assignments
CHANNEL_MODERATOR = [0, 1]
CHANNEL_CHARACTERS = list(range(2, 8))

class ChannelAPI:
    
    def __init__(self):
        self.channels = {}
        
        # Assigning default channels for the Moderator
        for channel in CHANNEL_MODERATOR:
            self.channels[channel] = "Moderator"
        
    def assign_character(self, channel, character_name):
        if channel in CHANNEL_MODERATOR:
            print("Channel reserved for Moderator.")
            return False
        elif channel in CHANNEL_CHARACTERS:
            self.channels[channel] = character_name
            return True
        else:
            print("Invalid channel.")
            return False
    
    def get_assigned_character(self, channel):
        return self.channels.get(channel, None)
    
    def process_text_and_synthesize(self, channel, text):
        def worker(channel, text):
            # Sending request to remote text processing API
            processed_text = self.send_to_text_processing(text)
            
            # Sending to remote audio synthesis API
            audio_data = self.send_to_audio_synthesis(processed_text)
            
            # Route the synthesized audio to the assigned channel
            self.route_to_channel(channel, audio_data)
        
        threading.Thread(target=worker, args=(channel, text)).start()
        
    def send_to_text_processing(self, text):
        # Placeholder function
        response = requests.post("https://text-processing.api.endpoint", data={"text": text})
        return response.text
    
    def send_to_audio_synthesis(self, processed_text):
        # Placeholder function
        response = requests.post("https://audio-synthesis.api.endpoint", data={"text": processed_text})
        return response.content

    def route_to_channel(self, channel, audio_data):
        # Placeholder function
        # For example, we could send this to some audio device or save to a file, etc.
        pass
    
def load_characters_from_config(api, config_file="config.json"):
    with open(config_file, "r") as file:
        config = json.load(file)
        characters = config.get("characters", [])
        
        for i, character in enumerate(characters):
            channel = CHANNEL_CHARACTERS[i]
            api.assign_character(channel, character)

api = ChannelAPI()
load_characters_from_config(api)

# Test if characters are loaded correctly
for channel in CHANNEL_CHARACTERS:
    print(f"Channel {channel} assigned to: {api.get_assigned_character(channel)}")
