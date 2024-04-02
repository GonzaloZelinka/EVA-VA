get_subtask_q_a = {
    "name": "get_subtask_q_a",
    "description": "Get the type of action for a Q&A request",
    "parameters": {
        "type": "object",
        "properties": {
            "req_type": {
                "type": "string",
                "enum": ["math", "common"],
                "description": "The type of request generated for the LLM",
            },
        },
        "required": ["req_type"],
    },
}

get_subtask_todo = {
    "name": "get_subtask_todo",
    "description": "Get the type of action for a todo request",
    "parameters": {
        "type": "object",
        "properties": {
            "req_type": {
                "type": "string",
                "enum": ["create", "update", "delete", "get"],
                "description": "The type of request generated for the LLM",
            },
        },
        "required": ["req_type"],
    },
}
