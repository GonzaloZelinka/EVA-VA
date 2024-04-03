get_create_todo = {
    "name": "get_create_todo",
    "description": "Get the task created, extract/convert the task with specified date and time from the request",
    "parameters": {
        "type": "object",
        "properties": {
            "task": {
                "type": "string",
                "description": "The task to create, should be a short description of the task to do",
            },
            "date": {
                "type": "string",
                "format": "date-time",
            },
        },
        "required": ["task", "date"],
    },
}
