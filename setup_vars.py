MODE = "natural" # Supported mode natural/rigid (rigid is a more direct conversation, only using llms to extract information from user response)
COMPANY_NAME = "TechSavvy Inc." # Just a random company name for the prompts
AUDIO_MODE = False #False # If true conversation is done by audio call, if False conversation is done by text
LANG = "en" # Supported lang en/es 
VERBOSE = False # In order to allow debug comments to see full prompts, responses, and usefull extra info
READ_SILENCE_DURATION = 2.0 # Seconds the bot is waiting. How long to wait in seconds before stopping on silence.
READ_MAX_DURATION = 60 # Max Seconds the bot is listening to the user.
READ_SILENCE_THRESHOLD = 5 # Threshold use to define "silence". Lower values more sensitive to lower volumes