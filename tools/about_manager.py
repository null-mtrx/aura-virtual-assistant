from langchain_core.tools import tool
import json


@tool
def update_about(user_data: str):
    """This one updates preferences and data about the user (like name and other details inferred from conversation) to be stored locally."""
    data = {}
    with open("config.json", "r") as file:
        data = json.load(file)

    path_to_user_data = data["agent_dets"]["data_path"]

    with open(f"{path_to_user_data}/user.txt", "a") as file:
        file.write(user_data)


@tool
def read_about() -> str:
    """This one allows the agent to get context about the user."""
    data = {}
    with open("config.json", "r") as file:
        data = json.load(file)

    path_to_user_data = data["agent_dets"]["data_path"]

    user_data = ""
    with open(f"{path_to_user_data}/user.txt", "r") as file:
        user_data = file.read()

    return user_data
