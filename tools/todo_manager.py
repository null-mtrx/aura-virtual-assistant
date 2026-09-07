from langchain_core.tools import tool
import json


@tool
def update_todo(task: str):
    """This one is used to update a todo list for the user. Just storing the task name is enough. You cannot give reminders"""
    data = {}
    with open("config.json", "r") as file:
        data = json.load(file)

    path_to_user_data = data["agent_dets"]["data_path"]

    with open(f"{path_to_user_data}/todo.txt", "a") as file:
        file.write(task + "\n")


@tool
def read_todo():
    """This one gives you the list of all the todos that are there as a list. Useful when you need to delete a todo or you need to read it"""
    data = {}
    with open("config.json", "r") as file:
        data = json.load(file)

    path_to_user_data = data["agent_dets"]["data_path"]

    tasks = []
    with open(f"{path_to_user_data}/todo.txt", "r") as file:
        tasks = file.readlines()

    return tasks


@tool
def remove_todo(index: int):
    """This one removes a given task from the todo list based on the index"""
    data = {}
    with open("config.json", "r") as file:
        data = json.load(file)

    path_to_user_data = data["agent_dets"]["data_path"]

    tasks = []
    with open(f"{path_to_user_data}/todo.txt", "r") as file:
        tasks = file.readlines()

    tasks.pop(index)

    with open(f"{path_to_user_data}/todo.txt", "w") as file:
        file.writelines(tasks)
