from app.llm_modules.open_ai import OpenAI_Model
from app.agent.customer_support_agent import CustomerSupportAgent


MODE = "natural" # Supported mode natural/rigid (rigid is a more direct conversation, only using llms to extract information from user response)
COMPANY_NAME = "TechSavvy Inc." # Just a random company name for the prompts
LANG = "en" # Supported lang en/es 
VERBOSE = False # In order to allow debug comments to see full prompts, responses, and usefull extra info
READ_SILENCE_DURATION = 2.0 # Seconds the bot is waiting. How long to wait in seconds before stopping on silence.
READ_MAX_DURATION = 60 # Max Seconds the bot is listening to the user.
READ_SILENCE_THRESHOLD = 5 # Threshold use to define "silence". Lower values more sensitive to lower volumes

if __name__ == "__main__":



    model = OpenAI_Model()

    agent = CustomerSupportAgent(model=model, 
                                 mode=MODE, 
                                 company=COMPANY_NAME, 
                                 lang = LANG,
                                 verbose=VERBOSE,
                                 read_silence_duration = READ_SILENCE_DURATION,
                                 read_max_duration = READ_MAX_DURATION,
                                 read_silence_threshold = READ_SILENCE_THRESHOLD)
    agent.start()