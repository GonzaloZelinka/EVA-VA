improved_req_fn = {
    "name": "req_improved",
    "description": "The improved request and the type of request",
    "parameters": {
        "type": "object",
        "properties": {
            "req_text": {
                "type": "string",
                "description": "The string improved and translated into English",
            },
            "req_type": {
                "type": "string",
                "enum": ["q_a", "todo", "undefined"],
                "description": "The type of request generated for the LLM",
            },
        },
        "required": ["req_text", "req_type"],
    },
}
