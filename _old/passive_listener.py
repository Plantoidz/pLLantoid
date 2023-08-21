def passive_listener():
   
    load_api_keys()
    max_device_id, max_channels = get_device_with_max_channels()  
    get_mode_data()
    announce_session()
    print(f"\n\n{reasoning_prompt1}")
    # Initialize the recognizer
    r = sr.Recognizer()

    # Set the microphone as the source
    time.sleep(1)  # wait for 1 second
    
    api = ChannelAPI() # Initialize the ChannelAPI here or pass it as an argument.
    load_characters_from_config(api) # Load characters

    """Run continuously, restarting on error."""
    while True:
        try:
            text = wait_for_wake_word(r) # This returns the detected text
            if text:
                timestamp = str(int(time.time())) # Get a current timestamp
                for channel in api.channels.keys():
                    api.process_text_and_synthesize(channel, text, timestamp)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
        time.sleep(1)