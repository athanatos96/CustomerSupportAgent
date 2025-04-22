# app/utils/prompt_loader.py

import json
import os

def load_prompts(agent_name: str, lang: str = "en") -> dict:
    """
    Load prompt definitions for a given agent and language from a JSON file.

    Args:
        agent_name (str): The name of the agent (folder name).
        lang (str): Language code for the prompt file (default is "en").

    Returns:
        dict: A dictionary containing the loaded prompts.
    """
    path = os.path.join("app", "prompts", agent_name, f"{lang}.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)
