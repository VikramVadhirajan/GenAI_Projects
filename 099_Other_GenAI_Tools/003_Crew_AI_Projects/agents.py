from crewai import Agent
from tools import *
from crewai import LLM

# from dotenv import load_dotenv
# load_dotenv()
# import os
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# os.environ["OPENAI_MODEL_NAME"]="gpt-4-0125-preview"

llm = LLM(
    model="ollama/mistral",
    base_url="http://localhost:11434"
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
