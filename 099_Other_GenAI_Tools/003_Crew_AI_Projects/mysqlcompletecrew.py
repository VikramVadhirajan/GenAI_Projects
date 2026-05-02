from crewai_tools import NL2SQLTool
from crewai import Agent, Task, Crew, Process


# ✅ Use MySQLTool instead
mysql_tool = NL2SQLTool(
    db_uri="mysql+pymysql://root:FBG_123@127.0.0.1:3306/world_layoffs"
)

schema = """
Table: layoffs_staging2
Columns:
- company (varchar)
- industry (varchar)
- location (varchar)
- total_laid_off (int)
- percentage_laid_off (float)
- date (date)
- stage (varchar)
- country (varchar)
- funds_raised_millions (float)
"""

sql_agent = Agent(
    role="SQL Analyst",
    goal="Answer business questions using MySQL database",
    backstory=f"""
    You are an expert SQL analyst.

    Database schema:
    {schema}

    Only generate SELECT queries.
    Do NOT modify database.
    """,
    tools=[mysql_tool],
    
    verbose=False
)

task = Task(
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
### optional expected output."SQL + Result + Explanation",
crew = Crew(
    agents=[sql_agent],
    tasks=[task],
    process=Process.sequential,
    verbose=False
)

result = crew.kickoff(
    inputs={"question": "Which company has raised highest funds in Germany?"}
)

print(result)