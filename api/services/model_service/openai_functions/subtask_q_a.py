get_subtask_q_a = {
    "name": "get_subtask",
    "description": "Get the type of request",
    "parameters": {
        "type": "object",
        "properties": {
            "req_type": {
                "type": "string",
                "description": "The type of request generated for the LLM. the possible values are: math and common",
            },
        },
        "required": ["req_type"],
    },
}
