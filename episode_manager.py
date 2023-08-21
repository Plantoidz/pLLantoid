"""Load Prompt Episodes"""
from dataclasses import dataclass
import os
from typing import List

PROMPT_CONFIG = {
    "model": "gpt-4",
    "temperature": 0.5,
    "max_tokens": 128,
    "logit_bias": {
        198: -100
    },  # Prevent "\n" from being generated.
}
PROMPT_DIR = "examples/"


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
