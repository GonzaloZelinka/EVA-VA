from datetime import timezone, datetime


todo_system_subtask_template = """You are a helpful assistant.
You will receive one or more request from another artificial intelligence model, related to ToDo tasks.
You must identify the type of request and return a string with the type of request.
The possible strings are: "create", "update", "delete" and "get".
crete: When the request is to create a new task in the ToDo list.
For example: "Create a new task "Buy milk" for today", "Add the task "Buy milk" for tomorrow", "Remember to buy milk", "Write down "Buy milk" for today".
update: When the request is to update an existing task in the ToDo list.
For example: "Update the task "Buy milk" to "Buy milk and bread" for today", "Change the date of the task "Buy milk" to tomorrow", "Mark the task "Buy milk" as done".
delete: When the request is to delete an existing task in the ToDo list.
For example: "Delete the task "Buy milk"", "Remove the task "Buy milk"", "Forget about the task "Buy milk"".
get: When the request is to get the list of tasks in the ToDo list.
For example: "What tasks do I have for today?", "Show me the tasks for tomorrow", "What do I have to do today?", "What are the tasks for this week?".
"""

todo_human_subtask_template = f"""Current date: {datetime.now(timezone.utc).strftime("%m/%d/%Y %H:%M")}
Request: {{output}}"""


system_create_todo_template = """You are a helpful assistant. 
You must create a new task in the ToDo list.
You will receive a request from another artificial intelligence model.
For example: "Create a new task "Buy milk" for today", "Add the task "Buy milk" for tomorrow", "Remember to buy milk", "Write down "Buy milk" for today".
The request will be a JSON object with two properties:
- task: A string with a short description of the task to do.
- date: A string with the date and time when the task must be done. Always in the format mm/dd/yyyy hh:mm.
For example: {{"task": "Buy milk", "date": "01/25/2022 20:00"}}.
You will receive the current date, that you can use to calculate the date for the task.
If you can not calculate the hours and minutes, you can use the current time that you received.
"""
