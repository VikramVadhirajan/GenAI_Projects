from groq import Groq


def generate_llm_summary(profile_text, api_key):
    client = Groq(api_key=api_key)

    prompt = f"""
You are a senior data analyst.

Analyze the dataset and provide:

1. Key patterns
2. Data quality issues
3. Risks
4. Recommendations

Dataset Summary:
{profile_text}

Keep it concise and structured.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content