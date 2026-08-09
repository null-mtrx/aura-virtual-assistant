from langchain_core.tools import tool


@tool
def perform_math_operations(operation_str: str) -> int:
    """Provided a mathematical expression in a string using basic BODMAS operations, it evaluates the string"""
    solution = eval(operation_str)
    return solution
