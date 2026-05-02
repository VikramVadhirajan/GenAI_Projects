from crewai_tools import NL2SQLTool
from crewai import Agent, Task, Crew, Process
from agents import *
from tasks import *
from tools import *

crew = Crew(
    agents=[sql_agent],
    tasks=[sql_task],
    process=Process.sequential,
    verbose=False
)

result = crew.kickoff(
    inputs={"question": "Which company has raised highest funds in Germany?"}
)

print(result)