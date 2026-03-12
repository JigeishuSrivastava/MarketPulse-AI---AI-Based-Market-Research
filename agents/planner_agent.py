from config import client

def create_research_plan(topic):

    prompt = f"""
Create research queries for market intelligence analysis.

Topic: {topic}

Generate queries for:

Market size
CAGR forecast
Competitive landscape
Company profiles
Investment trends
Technology trends
Opportunity analysis
Strategy recommendations
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":prompt}]
    )

    queries = response.choices[0].message.content.split("\n")

    return queries