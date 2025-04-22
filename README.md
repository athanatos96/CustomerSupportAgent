# Customer Support Bot - README

## Overview

This project implements a conversational AI-powered customer support bot that collects and processes order-related information. The bot can interact with customers through a natural conversation to gather details such as order number, category, description, and urgency. Additionally, it stores and organizes the conversations for future reference, while scoring customer frustration to help improve the service. The project integrates various components, such as audio input and transcription, prompt management, and conversation storage, with the flexibility to expand or adapt the system based on specific needs.

## Table of Contents

- [Setup Instructions](#setup-instructions)
- [System Architecture Overview](#system-architecture-overview)
- [Explanation of Key Design Decisions](#explanation-of-key-design-decisions)
- [Description of Potential Improvements](#description-of-potential-improvements)

---

## Setup Instructions

### Prerequisites

Before setting up the project, make sure you have the following dependencies:

- **Python 3.12+**: The project is written in Python 3.12.6, and you'll need Python installed on your system.
- **Libraries**: This project uses several external libraries that should be installed via `pip`. You can install them by running the following command:
  
```python
  pip install -r requirements.txt
```

- **Audio Input Setup**: If you want to use the voice input functionality, you need to have a microphone set up and ensure your system has the necessary drivers for audio input.

- **LLM Model**: The system requires an LLM model for audio transcription and text-to-speech conversion. This should be integrated in the `UserIO` class, specifically the `llm_model` argument. Local mode using Mistral 7B running with Ollama (Do not support TTS or STT) and Cloud mode using openAI API. This means that you will need a OPENAI_API_KEY enviroment variable, with a valid KEY. Default mode OpenAI (Since local model is small 7b performance is really low, recomended cloud)


### Installing and Running

1. **Clone the Repository**:
```bash
   git clone <repository_url>
   cd <project_directory>
```

2. **Create a virtual enviroment with python 3.12 and activate it**:
    Run the following command to create the Python virtual enviroment:
    For Windows
```bash
   python -m venv .venv
   .venv\Scripts\activate
```
    For Linux
```bash
   python -m venv .venv
   source .venv/bin/activate
```

3. **Install Dependencies**:
   Run the following command to install the required Python dependencies:
```bash
   pip install -r requirements.txt
```

4. **Run the Application**:
   After setting up the dependencies, you can run the bot by invoking the main script. If you’re running the bot with text input, it will simply await the user’s input in the terminal:
```bash
   python app/main.py
```

   If you’re using audio input, make sure the microphone is properly configured and audio mode is enabled.

---

## System Architecture Overview

The system architecture of the Customer Support Bot consists of several interconnected modules that handle different aspects of the application. Below is a high-level breakdown of the key components:

### Modules and Components

1. **User Input & Output (`UserIO`)**:
    The `UserIO` class handles all interactions with the user, including receiving text or audio input, displaying messages, and converting text to speech when audio mode is active. This is the primary interface for the bot to interact with users.
   
    - **Audio Input**: When the user opts for audio input, the system records the audio, transcribes it using an LLM model, and processes it as if it were text.
    - **Text Input**: If audio input is not required, the bot collects input via standard terminal text input.

    - **Audio Output**: When the user opts for audio output, the system calls the TTS Model and streams the audio to the user.
    - **Text Output**: If audio output is not required, the bot writes outputs via standard terminal text output.

2. **Prompt Management (`PromptLoader`)**:
    The `PromptLoader` class is responsible for loading different prompt configurations for various agents. The prompts are stored in JSON files and are loaded based on the agent name and language preferences. This makes it easy to scale the bot by adding new agents with specific prompts for different scenarios and different languages.

3. **Conversation & Data Storage (`Storage`)**:
    The `Storage` module handles saving, loading, and listing conversations in a structured format. Conversations are saved in JSON files with an order number as the key, allowing the system to track multiple sessions for a particular order.

    - **Conversation Structure**: Each conversation includes metadata such as timestamp, interaction mode (natural/rigid), conversation messages, and extracted data like the order number, category, description, and urgency.
    - **Conversation Summary**: A summary of each conversation is generated to provide a concise overview of the customer's issue.

    It can be changed to storage to Database without needing to modify the rest of the code.

4. **Audio Transcription and Text-to-Speech**:
    he bot integrates with a speech-to-text (STT) and text-to-speech (TTS) system via the LLM model. These functions allow the bot to:
    - Convert user speech to text for processing.
    - Convert the bot's text responses into audio.

5. **LLM modularity**:
    The `llm_modules` are designed so that a user can create new ones to interface with different LLM APIs or locally running models.

6. **Agent expansion**:
    The `agents` are designed so that new agents can be created for different purposes, while the corresponding prompts for the agent are handled in the prompts folder, making changing prompts trivial.

7. **Languaje expansion**:
    The `prompts` are designed so that language expansion is as easy as creating a new JSON file with the prompts in the desired language for each agent.


---

## Explanation of Key Design Decisions

### 1. **Separation of Concerns**:
   - The system is designed with modularity in mind. The `UserIO` class handles user interaction, while the `PromptLoader` class manages prompts, `Storage` handles data persistence, the `llm_modules` handles the comunication with each llm used, the `agent` handles all the different agents running, the `prompts` handles the different prompts for each agent and each languages. This separation ensures that different components can evolve independently and allows for easier maintenance and testing.
   
### 2. **Flexible User Input Handling**:
   - The bot supports both text and audio inputs, giving the user flexibility in how they interact with the system. Audio mode requires integration with an LLM model for transcription, while text mode uses standard input.
   
### 3. **Conversation Tracking**:
   - Each interaction is saved as a conversation session with key metadata like the frustration score and language. This allows for ongoing improvements in the customer support experience, enabling the system to identify issues over time and optimize responses based on historical data.
   
### 4. **Error Handling and Robustness**:
   - The code includes error handling mechanisms for situations like failed audio transcription, ensuring that the system doesn't crash unexpectedly. Additionally, the audio file is cleaned up after processing to avoid unnecessary file accumulation.

---

## Description of Potential Improvements

### 1. **Integration with External Systems**:
   - The bot could be expanded to integrate with CRM or order management systems to automatically fetch order details, reducing the need for users to manually input their order number.
   
### 2. **Dynamic Multilingual Support**:
   - Although the bot supports language flexibility, currently only two language files (`en.json`, `es.json`) are provided for prompts. To support global users, more language files can be added, and the bot can detect the user’s language preference dynamically. Even though OpenAI models are robust enough to handle input in a different language than the one selected, this can lead to undesired results or misinterpretations.
   
### 3. **Advanced dynamic Frustration Detection**:
   - Currently, frustration is scored by the LLM model at the end of the conversation. However, we can detect frustration in real time based on user behavior, sentiment analysis of text, or tone in audio input. This would allow for more automated and dynamic tracking of customer sentiment during the conversation, enabling escalation to a human agent if frustration levels become dangerously high or continue to rise.
   
### 4. **Audio Output Enhancement**:
   - Implementing more advance models like the ones supported by Eleven labs
   
### 5. **UI/UX for Interactions**:
   - While the current interface is command-line-based, a web or mobile-based frontend could be developed to make the bot more user-friendly, especially for non-technical users.

### 6. **RAG implementation**:
   - Implementing a knowledga base to give supported answers based on common customer issues

---

## Contributing

Contributions are welcome! If you'd like to improve this project, feel free to fork the repository and submit pull requests with improvements. Please ensure that any new features are well-documented and include relevant tests.

---

## License

This project is licensed under the Apahce 2.0 License. See the [LICENSE](LICENSE) file for more information.




















# SupportBot - AI-Powered Customer Support Agent

SupportBot is an AI-driven customer support agent designed to assist in gathering essential information from users in a friendly and efficient manner. The bot uses natural language processing (NLP) to extract key details such as order numbers, categories of issues (shipping, billing, product-related), descriptions, and urgency levels. It provides a smooth customer support experience by collecting, validating, and summarizing customer queries.

## Features

- **Intelligent Conversation Flow**: SupportBot asks users questions based on a predefined structure, ensuring all necessary information is collected.
- **Natural and Rigid Modes**: The bot operates in either "rigid" mode (strict question flow) or "natural" mode (more conversational and flexible).
- **Order History Integration**: The bot can retrieve past conversations related to a specific order number to provide continuity and avoid repetition.
- **Issue Validation**: SupportBot checks the validity of the information provided by the user and prompts for corrections if necessary.
- **Supervisor Validation**: The bot integrates with a supervisor agent to ensure that all extracted information meets the requirements.
- **Customizable Prompts**: You can define the prompts and messages in different languages to tailor the bot's behavior to your needs.

## Installation

To use **SupportBot**, clone this repository and install the required dependencies.

### Clone the repository:

```bash
git clone https://github.com/athanatos96/CustomerSupportAgent.git
cd supportbot
```

### Install the required packages:

```bash
pip install -r requirements.txt
```

## Configuration

1. **Model Integration**: SupportBot relies on an AI model for natural language processing tasks (e.g., GPT, BERT, or any custom NLP model). Ensure the model is properly set up and integrated before running the agent.
2. **Prompts Configuration**: The bot uses customizable prompts that can be found in the `prompts/` directory. Edit these prompts to adjust the questions and responses to match your company's needs.
3. **Order History**: To enable order history functionality, ensure that the `list_all_orders()` and `load_conversations()` functions are properly integrated with your order database or logs.

## Usage

### Starting the Agent

You can start the customer support agent in either "rigid" or "natural" mode by creating an instance of the `CustomerSupportAgent` class.

#### Example (Rigid Mode):
```python
from app.agent.customer_support_agent import CustomerSupportAgent

# Initialize the support bot in "rigid" mode
support_bot = CustomerSupportAgent(model=your_model_instance, mode="rigid", company="YourCompany")
support_bot.start()
```

#### Example (Natural Mode):
```python
from app.agent.customer_support_agent import CustomerSupportAgent

# Initialize the support bot in "natural" mode
support_bot = CustomerSupportAgent(model=your_model_instance, mode="natural", company="YourCompany")
support_bot.start()
```

### Conversation Flow

1. **Order Number**: The bot will prompt the user for an order number (e.g., `ORD12345`).
2. **Category**: The bot will ask about the issue category (shipping, billing, product).
3. **Description**: The user provides a brief explanation of the issue.
4. **Urgency**: The user specifies the urgency level (low, medium, high).
5. **Validation**: The bot checks if the provided information is correct. If something is missing or incorrect, it will prompt the user for clarification.
6. **Supervisor Review**: After gathering all required information, the bot escalates the conversation to a supervisor for validation and correction if needed.
7. **History Integration**: If the user provides an order number, the bot will check for past conversations and include relevant history in the conversation.

## Customization

You can customize the behavior of SupportBot by modifying the following:

- **Prompts**: Update the questions and instructions in the `prompts/` directory.
- **Supervisor Validation**: The bot includes a supervisor agent for validation. You can adjust its behavior and requirements as needed.
- **Mode**: Choose between "rigid" (strict question flow) and "natural" (more flexible and conversational).

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt` (such as `openai`, `requests`, etc.)
- A pre-trained language model (like GPT or any other NLP model)

## Contributing

We welcome contributions to SupportBot! If you have ideas for improvements or new features, feel free to open an issue or submit a pull request.

### Steps to contribute:


1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and test them.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-name`).
6. Create a pull request.


## License

SupportBot is open-source software licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For support or inquiries, feel free to reach out to us at [support@example.com].