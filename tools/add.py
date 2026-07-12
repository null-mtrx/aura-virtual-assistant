from langchain_core.tools import tool


@tool
def add_nums(num1: int, num2: int):
    """Given two integers, returns their sum"""
    return num1 + num2
