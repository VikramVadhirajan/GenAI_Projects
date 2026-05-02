from crewai import Agent, Task, Crew, Process
from crewai_tools import SeleniumScrapingTool
import pandas as pd
import json

# ---------------------------
# Setup
# ---------------------------
selenium_tool = SeleniumScrapingTool()

web_scraper_agent = Agent(
    role="Web Scraper",
    goal="Extract structured data from financial web pages",
    backstory="Expert in scraping tabular and structured data from dynamic websites.",
    tools=[selenium_tool],
    verbose=True,
)

# ---------------------------
# List of URLs
# ---------------------------
urls=["https://www.amazon.com/dp/B0843CPBCZ"
]

# ---------------------------
# Loop through URLs
# ---------------------------
all_data = []

for url in urls:
    print(f"\nScraping: {url}")

    task = Task(
        description=f"""
        Open the website: {url}

        Extract the following 
        -Product Name, 
        -Price Rating 
        -Number of Review 
        -ASIN Number and 
        -Dimensions of the product (if available). 
        - Discount (If Available) and 
        -Past Month Purchase. 
        Return ONLY valid JSON (no explanation):
        [
            {{
                "Product Name": "...",
                "Price": "...",
                "Star Rating": "...",
                "Review Count": "...",
                "Source URL": "{url}",
                "ASIN": "...",
                "Dimensions": "...",
                "Past Month Purchase": "...",
                "Discounted Percentage": "..."
            }}
        ]
        """,
        expected_output="Clean JSON array",
        agent=web_scraper_agent,
    )

    crew = Crew(
        agents=[web_scraper_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False,  # Keep logs clean in loop
    )

    result = crew.kickoff()

    # ---------------------------
    # Parse result safely
    # ---------------------------
    try:
        data = json.loads(result)
    except:
        try:
            data = json.loads(str(result))
        except:
            print(f"⚠️ Failed to parse JSON for {url}")
            continue

    # Append results
    all_data.extend(data)

# ---------------------------
# Convert to DataFrame
# ---------------------------
df = pd.DataFrame(all_data)

# ---------------------------
# Save to Excel
# ---------------------------
file_name = "multi_url_scraped_data.xlsx"
df.to_excel(file_name, index=False)

print(f"\n✅ Data saved to {file_name}")