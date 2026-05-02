from crewai import Task
from tools import *
from agents import *

sql_task = Task(
    description="""
    Answer the user question using SQL.

    Steps:
    1. Generate SQL query
    2. Execute using MySQL tool
    3. Return:
       - SQL query
       - Result
       - Explanation

    User question: {question}
    """,
    expected_output="Only the final answer",
    agent=sql_agent
)