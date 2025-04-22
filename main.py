# main.py

from app.llm_modules.open_ai import OpenAI_Model
from app.llm_modules.ollama_mistral7b import OllamaMistral7B_Model
from app.agent.customer_support_agent import CustomerSupportAgent

from setup_vars import *

"""MODE = "natural" # Supported mode natural/rigid (rigid is a more direct conversation, only using llms to extract information from user response)
COMPANY_NAME = "TechSavvy Inc." # Just a random company name for the prompts
AUDIO_MODE = True #False # If true conversation is done by audio call, if False conversation is done by text
LANG = "en" # Supported lang en/es 
VERBOSE = False # In order to allow debug comments to see full prompts, responses, and usefull extra info
READ_SILENCE_DURATION = 2.0 # Seconds the bot is waiting. How long to wait in seconds before stopping on silence.
READ_MAX_DURATION = 60 # Max Seconds the bot is listening to the user.
READ_SILENCE_THRESHOLD = 5 # Threshold use to define "silence". Lower values more sensitive to lower volumes"""



def str_to_bool(value):
    return value.strip().lower() in ("true", "1", "yes", "y")

def display_config(config):
    print("\n🛠️ Current Configuration:")
    for key, val in config.items():
        print(f"{key} = {val}")
    print("\nType a setting name to change it (e.g., `LANG`), `confirm` to continue, or `reset` to restore defaults.")

def ask_value(name, current, type_fn=str):
    new_value = input(f"Enter new value for {name} [{current}]: ").strip()
    if new_value == "":
        return current
    try:
        return type_fn(new_value)
    except ValueError:
        print("❌ Invalid input. Keeping previous value.")
        return current


descriptions = {
    "MODE": ("Conversation mode", "Options: 'natural' (casual), 'rigid' (direct Q&A)"),
    "COMPANY_NAME": ("Company name for the conversation", "Any name, e.g., 'TechSavvy Inc.'"),
    "AUDIO_MODE": ("Enable audio input", "True = audio mode, False = text only"),
    "LANG": ("Language for conversation", "Options: 'en' = English, 'es' = Spanish"),
    "VERBOSE": ("Show debug logs", "True = show internal logs, False = silent mode"),
    "READ_SILENCE_DURATION": ("Bot wait time on silence (sec)", "e.g., 2.0"),
    "READ_MAX_DURATION": ("Max listening time per user input (sec)", "e.g., 60"),
    "READ_SILENCE_THRESHOLD": ("Volume sensitivity for silence detection", "Lower = more sensitive, e.g., 5"),
}

type_cast = {
    "MODE": str,
    "COMPANY_NAME": str,
    "AUDIO_MODE": str_to_bool,
    "LANG": str,
    "VERBOSE": str_to_bool,
    "READ_SILENCE_DURATION": float,
    "READ_MAX_DURATION": int,
    "READ_SILENCE_THRESHOLD": float,
}

if __name__ == "__main__":
    default_config = {
        "MODE": MODE,
        "COMPANY_NAME": COMPANY_NAME,
        "AUDIO_MODE": AUDIO_MODE,
        "LANG": LANG,
        "VERBOSE": VERBOSE,
        "READ_SILENCE_DURATION": READ_SILENCE_DURATION,
        "READ_MAX_DURATION": READ_MAX_DURATION,
        "READ_SILENCE_THRESHOLD": READ_SILENCE_THRESHOLD
    }

    config = default_config.copy()

    print("Welcome! You can customize the configuration before starting.")

    while True:
        display_config(config)
        choice = input("Your choice: ").strip().upper()

        if choice == "CONFIRM":
            break
        elif choice == "RESET":
            config = default_config.copy()
            print("✅ Configuration reset to defaults.")
        elif choice in config:
            desc, example = descriptions.get(choice, ("", ""))
            print(f"\n🔧 {choice} - {desc}")
            print(f"   💡 {example}")
            config[choice] = ask_value(choice, config[choice], type_cast.get(choice, str))
        else:
            print("❌ Invalid option. Please enter a valid setting name, 'confirm', or 'reset'.")



    model = OpenAI_Model()
    # Can also use the model = OllamaMistral7B_Model() Local model. (Only supports AUDIO_MODE = False)


    agent = CustomerSupportAgent(model=model,
                                 mode=config["MODE"],
                                 company=config["COMPANY_NAME"],
                                 audio_mode=config["AUDIO_MODE"],
                                 lang=config["LANG"],
                                 verbose=config["VERBOSE"],
                                 read_silence_duration=config["READ_SILENCE_DURATION"],
                                 read_max_duration=config["READ_MAX_DURATION"],
                                 read_silence_threshold=config["READ_SILENCE_THRESHOLD"])
    agent.start()
