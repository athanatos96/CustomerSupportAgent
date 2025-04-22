# app/utils/storage.py

import json
from datetime import datetime
from pathlib import Path
from typing import Any, List, TypedDict

DATA_DIR = Path("data/conversations")
DATA_DIR.mkdir(parents=True, exist_ok=True)

class Message(TypedDict):
    role: str
    text: str


class ExtractedData(TypedDict):
    order_number: str
    category: str
    description: str
    urgency: str

class ConversationSession(TypedDict):
    timestamp: str
    mode: str
    conversation: List[Message]
    extracted: ExtractedData
    summary: str
    lang: str

def _get_file_path(order_number: str) -> Path:
    """
    Returns the path to the JSON file corresponding to an order number.
    """
    return DATA_DIR / f"{order_number.upper()}.json"

def save_conversation(extracted: ExtractedData, convo: List[Message], summary: str, mode: str, frustration_score:int, lang: str) -> None:
    """
    Save a conversation session to the appropriate order-number-based JSON file.

    Args:
        extracted (ExtractedData): Dictionary containing extracted fields.
        convo (List[Message]): List of conversation messages.
        summary (str): Summary of the conversation.
        mode (str): Mode of interaction (e.g., "natural", "rigid").
        frustration_score (int): Customer frustration (0-10)
        lang (str): Language of the conversation
    """
    file_path = _get_file_path(extracted["order_number"])

    new_session = {
        "timestamp": datetime.now().isoformat(),
        "mode": mode,
        "conversation": convo,
        "extracted": extracted,
        "summary": summary,
        "frustration_score":frustration_score,
        "lang": lang
    }

    if file_path.exists():
        with open(file_path, "r") as f:
            sessions = json.load(f)
    else:
        sessions = []

    sessions.append(new_session)

    with open(file_path, "w") as f:
        json.dump(sessions, f, indent=2)

def load_conversations(order_number: str) -> List[ConversationSession]:
    """
    Load all saved conversation sessions for a specific order.

    Args:
        order_number (str): The order number to load conversations for.

    Returns:
        List[ConversationSession]: List of conversation sessions for the order.
    """
    file_path = _get_file_path(order_number)

    if file_path.exists():
        with open(file_path, "r") as f:
            return json.load(f)
    return []

def list_all_orders() -> List[str]:
    """
    Lists all order numbers for which conversations are stored.
    """
    return [p.stem for p in DATA_DIR.glob("*.json")]
