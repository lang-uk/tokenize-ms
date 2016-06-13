TOKENIZE_TEXT_INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
    },
    "required": ["text"],
    "additionalProperties": False
}

TOKENIZE_TEXT_OUTPUT_SCHEMA = {
    "type": "array",
    "items": {
        "type": "array",
        "items": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    }
}
