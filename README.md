# PLLantoid
 
## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Contributing](#contributing)
6. [License](#license)

## Introduction
Welcome to **PLLantoid** - the pinnacle of Cybernetic Embodied Synesthesia (CES). Dive deep into the fusion of human experiences and artificial intelligence. PLLantoid is a unique platform that bridges human thoughts, sensory perceptions, and artificially intelligent agents sourced directly from your subconsciousness.

## Features
- **Synthetic Subconsciousness Interface**: PLLantoid offers an interactive landscape where AI and human cognition converge.
  
- **Orchestrator Dialogue**: Pose questions or statements to the PLLantoid orchestrator. Engage in a discourse with language-capable robotic agents representing facets of your subconscious.

- **Custom Feedback Loops**: Fine-tune your experience as you explore your subconscious.

## Installation

To install and set up PLLantoid:

1. Clone the repository:
git clone https://github.com/benrito/pLLantoid


2. Navigate to the cloned directory:
cd /pLLantoid


3. Create a working directory:
mkdir pLLantoid/working


4. Create a `.env` file in the root directory and add your API keys:
echo "OPENAI_API_KEY=<your-key>" >> .env
echo "ELEVEN=<your-key>" >> .env


5. Install the required packages using pip:
pip3 install -r requirements.txt


With these steps, PLLantoid is set up and ready for use.

## Usage

1. **Character Configuration**: Use `util/config_character.py` to set the number of characters for the session. PLLantoid supports as many audio channels as your configuration allows, and will route all audio to channel 0 (left stereo) on a typical audio setup.
python3 util/config_character.py


2. **Mode & Options**: Configure conversational modes and other settings using `util/config_modes.py`.
python3 util/config_modes.py


3. Launch a PLLantoid test mode, such as chatter.py or conversation.py. The functions in embodiment.py will handle characters, audio recognition, prompt manangement, and audio synthesis routed to assigned audio channels, allowing you to converse and interact with your AI-generated characters.

4. To view or edit character profiles, navigate to:
characters/character.json

5. Engage with the robotic agents, each representing facets of your subconsciousness. Dive deep, explore, and achieve newfound self-awareness.

(Note: Ensure a conducive environment when using PLLantoid. It's designed to provide profound insights which can be intense.)

## Contributing
This project is brand new. We encourage contributions to enhance PLLantoid. Help us build out our [Contribution Guidelines](LINK_TO_CONTRIBUTING.md), add Issues for features you'd like to see, or feel free to initiate a pull request.

## License
Still figuring out which license to use.

---

Delve into the world of PLLantoid and embark on an enlightening journey within your subconscious.
