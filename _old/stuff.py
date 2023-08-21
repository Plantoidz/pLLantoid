            api = ChannelAPI() # Initialize the ChannelAPI here or pass it as an argument.
            load_characters_from_config(api) # Load characters
            text = wait_for_wake_word(r) # This returns the detected text
            if text:
                timestamp = str(int(time.time())) # Get a current timestamp
                for channel in api.channels.keys():
                    api.process_text_and_synthesize(channel, text, timestamp)