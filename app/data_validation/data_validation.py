# app/data_validation/data_validation.py

from typing import Tuple, Optional
from app.data_validation.mappings import CATEGORY_MAP, URGENCY_MAP

def validate_and_extract(field: str, text: str, lang: str = "en") -> Tuple[bool, Optional[str]]:
    """
    Validates and extracts a normalized (English) value from text for a specific field.

    Args:
        field (str): The field type (e.g., 'order_number', 'category', etc.)
        text (str): The input text from the user.
        lang (str): Language code ('en', 'es', etc.). Default is English.

    Returns:
        Tuple[bool, Optional[str]]: (True, value) if valid, else (False, None)
    """
    text = text.strip().lower()

    if field == "order_number":
        if text.startswith("ord") and text[3:].isdigit():
            return True, text.upper()
        return False, None

    elif field == "category":
        map_dict = CATEGORY_MAP.get(lang, {})
        value = map_dict.get(text)
        if value:
            return True, value
        return False, None

    elif field == "urgency":
        map_dict = URGENCY_MAP.get(lang, {})
        value = map_dict.get(text)
        if value:
            return True, value
        return False, None

    elif field == "description":
        if len(text) > 10:
            return True, text
        return False, None

    return False, None