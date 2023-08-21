if __name__ == "__main__":
    exception_count = 0

    while exception_count < MAX_RETRIES:
        try:
            # Wait for taps
            if detect_taps():
                playsound("media/beep_start.wav")
            
            r = sr.Recognizer()
            time.sleep(1)
            with sr.Microphone() as source:
                print("\n\nI'm listening...")
                audio = r.listen(source)
                timestamp = time.time()  # I've assumed this since you use `timestamp` later.
                with open(f"working/requests/{timestamp}_request.wav", "wb") as f:
                    f.write(audio.get_wav_data())

            # ... [rest of the threading and sound playback code]

            # Recognize the speech input using Google Speech Recognition
            playsound(acknowledgement)
            text = r.recognize_google(audio)
            print("\n\nI heard: " + text)

            # ... [rest of the code to save transcript]

            # If successful, break out of the loop
            break

        except sr.UnknownValueError:
            exception_count += 1
            print("Google Speech Recognition could not understand audio")
            playsound(beep_stop)

        except sr.RequestError as e:
            exception_count += 1
            print(f"Could not request results from Google Speech Recognition service; {e}")
            playsound(beep_stop)

    if exception_count >= MAX_RETRIES:
        print("Max retry limit reached. Exiting program.")
        sys.exit(1)
