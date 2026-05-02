from crewai import Agent, Task, Crew, Process
from crewai_tools import SeleniumScrapingTool
import pandas as pd
import json

# Initialize Selenium tool
selenium_tool = SeleniumScrapingTool()

# Define agent
web_scraper_agent = Agent(
    role="Web Scraper",
    goal="Extract structured dividend stock table data",
    backstory="Expert in scraping and structuring financial tabular data.",
    tools=[selenium_tool],
    verbose=True,
)

# Target URL
url = "https://dhan.co/stocks/market/dividend-stocks/"

# Task
scrape_task = Task(
    description=f"""
    Open the website: {url}

    Locate the dividend stocks table.

    Extract all rows with columns such as:
    - Company Name
    - LTP
    - Dividend Yield
    - Market Cap

    Return ONLY valid JSON (no explanation) in this format:
    [
        {{
            "Company": "...",
            "LTP": "...",
            "Dividend Yield": "...",
            "Market Cap": "..."
        }}
    ]
    """,
    expected_output="Clean JSON array of dividend stock table data.",
    agent=web_scraper_agent,
)

# Crew
crew = Crew(
    agents=[web_scraper_agent],
    tasks=[scrape_task],
    process=Process.sequential,
    verbose=True,
)

# Run
result = crew.kickoff()

# ---------------------------
# Convert result → DataFrame
# ---------------------------
try:
    # If result is string JSON
    data = json.loads(result)
except:
    # Sometimes CrewAI wraps output
    data = json.loads(str(result))

df = pd.DataFrame(data)

# ---------------------------
# Save to Excel
# ---------------------------
file_name = "dividend_stocks.xlsx"
df.to_excel(file_name, index=False)

print(f"Excel file saved as {file_name}")