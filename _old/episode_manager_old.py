"""Load Prompt Episodes"""
from dataclasses import dataclass
import os
from typing import List

@dataclass
class Episode:
    name: str
    opening_line: str
    prompt_text: str
    closing_line: str
    agent_name: str
    user_name: str
    max_turns: int
    end_phrases: List[str]
    prompt_config: dict = None

def build_transcript(turns) -> str:
    clean_lines = []
    for turn in turns:
        text = turn["text"].strip().replace("\n", " ")
        print("appending ... " + text)
        clean_lines.append(f"{turn['speaker'].capitalize()}: {text}")
    return "\n".join(clean_lines)

def inject_transcript_into_prompt(turns, prompt_template: str) -> str:
    transcript = build_transcript(turns)
    return prompt_template.replace("{{transcript}}", transcript)

def inject_stop_tokens(user_name: str, agent_name: str, prompt_config: dict) -> dict:
    """Get prompt config for chatbot and inject stop tokens."""
    params = prompt_config.copy()
    params["stop"] = [f"{agent_name}:", f"{user_name}:"]
    return params

def load_episode(episode: dict, user_name: str, inputs: dict = None):
    """Load episode with inputs injected into prompt text."""
    episode["user_name"] = user_name
    import random

    opening_line = random.choice(episode["opening_lines"])
    closing_line = random.choice(episode["closing_lines"])

    opening_line = opening_line.replace("{{user_name}}", user_name)
    print(opening_line)
    episode["prompt_text"] = episode["prompt_text"].replace("{{user_name}}", user_name)
    episode["prompt_text"] = episode["prompt_text"].replace(
        "{{agent_name}}", episode["agent_name"]
    )

    prompt_text = episode["prompt_text"]
    if inputs is not None:
        for input_name, input_value in inputs.items():
            prompt_text = prompt_text.replace("{{" + input_name + "}}", input_value)

    prompt_config = episode.get("prompt_config", PROMPT_CONFIG.copy())
    print(prompt_config, prompt_config)
    prompt_config = inject_stop_tokens(
        user_name=user_name,
        agent_name=episode["agent_name"],
        prompt_config=prompt_config,
    )

    return Episode(
        name=episode["name"],
        opening_line=opening_line,
        closing_line=closing_line,
        prompt_text=prompt_text,
        user_name=user_name,
        agent_name=episode["agent_name"],
        prompt_config=prompt_config,
        max_turns=episode["max_turns"],
        end_phrases=episode["end_phrases"]
    )

def load_episodes(episode_names: List[str], user_name: str) -> List[Episode]:
    """Loads episodes in order."""
    return [load_episode(name, user_name) for name in episode_names]

def activate_tony(r):
    turns = []
    chat_id = "default" 

    episode = episode_manager.load_episode(EPISODES["plantony"], str("tony"))
    # speaktext(episode.opening_line)

    turns.append({"speaker": AGENT_NAME, "text": episode.opening_line})
    update_remote_chat_history(chat_id, turns)

    exit_loop = False

    with sr.Microphone() as source:
        while not exit_loop:

            if(len(turns) > episode.max_turns):
                    exit_loop = True
                    if episode.closing_line:
                        speaktext(episode.closing_line)
                        exit();

            # Begin transcribing microphone audio stream
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, 100, 10)
            time.sleep(1)
             # hmm to show Tony has understood..
            playsound(acknowledgement)
            text = ""

            try:
                # Recognize the speech input using Google Speech Recognition
                text = r.recognize_google(audio)

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                playsound(fail)

            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                playsound(problem)

            if(text):
                print("I heard: " + text)
                # speaktext(text)

                turns.append({"speaker": USER_NAME, "text": text})

                prompt = inject_transcript_into_prompt(turns, episode.prompt_text)
                print(prompt)

                # Generate the response from the GPT model
                gptmagic(turns, prompt)

def generate_unique_filename(base_path, base_filename):
    counter = 0
    full_filename = os.path.join(base_path, f"{base_filename}.mp3")

    # Check if the file exists. If it does, increment the counter until we find a unique name.
    while os.path.exists(full_filename):
        counter += 1
        full_filename = os.path.join(base_path, f"{base_filename}_{counter}.mp3")
    
    return full_filename

# def speak_text(text=None, enable=True, voice=DEFAULT_VOICE_NAME, gain = 0):
#     if enable:
#         audio_bytes = google_speech.load_or_convert_text_to_speech(
#             text=text,
#             voice_name=voice,
#             cache_dir="/tmp/audio_cache",
#             pitch=TTS_PITCH_DELTA,
#         )
#         audio_utils.play_styled_audio(audio_bytes, style=PYDUB_AUDIO_STYLE, gain=gain)
#         time.sleep(POST_SPEECH_SLEEP_TIME_SEC)

def default_prompt_config():
    return {
        "model": "gpt-4",
        "temperature": 0.5,
        "max_tokens": 128,
        "logit_bias": {
            198: -100  # prevent newline
        }
    }

# Test load episodes
if __name__ == "__main__":
    episodes = load_episodes(
        [
            "confession",
            "test_of_faith",
        ]
    )
    for episode in episodes:
        print(episode.opening_line)
        print(episode.prompt_text)
        print(episode.closing_line)
        print(episode.agent_name)
        print(episode.user_name)
        print(episode.prompt_config)
