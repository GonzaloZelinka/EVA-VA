from api.config import Config
from api.services.google_firestore_service import db
from api.services.google_firestore_service.models.Todo import Todo
from datetime import datetime


def create_todo(todo_data):

    todo = Todo(**todo_data)

    db.collection("todos").add(todo.dict())

    return todo.dict()


def get_todos():
    todos = db.collection("todos").stream()
    todos_list = []
    for todo in todos:
        todo_dict = todo.to_dict()
        todo_dict["id"] = todo.id
        if "createdAt" in todo_dict and isinstance(todo_dict["createdAt"], datetime):
            todo_dict["createdAt"] = todo_dict["createdAt"].strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        if "updatedAt" in todo_dict and isinstance(todo_dict["updatedAt"], datetime):
            todo_dict["updatedAt"] = todo_dict["updatedAt"].strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        if "date" in todo_dict and isinstance(todo_dict["date"], datetime):
            todo_dict["date"] = todo_dict["date"].strftime("%Y-%m-%d %H:%M:%S")
        todos_list.append(todo_dict)
    return todos_list
