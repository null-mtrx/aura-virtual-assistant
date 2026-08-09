from langchain_core.tools import tool

import datetime
import os
import subprocess


@tool
def perform_math_operations(operation_str: str) -> int:
    """Provided a mathematical expression in a string using basic BODMAS operations, it evaluates the string"""
    solution = eval(operation_str)
    return solution


@tool
def get_date() -> str:
    """This tool allows you to get the current date (day/month/year)"""
    date_now = datetime.datetime.now().strftime("%d/%m/%y")
    return date_now


@tool
def get_time() -> str:
    """This tool gives you the current time (Hour: Minute)"""
    date_now = datetime.datetime.now().strftime("%H:%M")
    return date_now


@tool
def execute_low_priority_commands(command: str) -> str:
    """This tool allows you to execute low priority commands on the shell"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result
