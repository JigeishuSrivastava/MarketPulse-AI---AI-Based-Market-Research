from config import client
from memory.vector_store import retrieve_data

def analyze_market(topic, status_callback=None):
    # Data retrieval
    data = retrieve_data(topic)
    
    # 10 Professional Sections for depth
    sections = [
        "Executive Summary & Strategic Overview",
        "Market Size, Growth Drivers, and CAGR Forecast (2024-2030)",
        "Competitive Landscape: Top Players & Market Share Analysis",
        "Detailed Company Profiles & Strategic Business Moves",
        "Technological Innovations & Digital Transformation Trends",
        "Regional Analysis: Global vs Domestic Markets",
        "PESTEL Analysis (Political, Economic, Social, Tech, Environmental, Legal)",
        "Investment Landscape, Funding Trends & Mergers",
        "SWOT Analysis & Risk Assessment",
        "Strategic Recommendations & Future Roadmap"
    ]
    
    full_report = f"# STRATEGIC MARKET INTELLIGENCE REPORT: {topic.upper()}\n\n"
    
    # Generate each section iteratively
    for i, section in enumerate(sections):
        if status_callback:
            status_callback(i + 1, len(sections), section)
            
        section_prompt = f"""
        Role: Senior Market Research Strategist.
        Task: Write a deep-dive analysis for the section: "{section}".
        Topic: {topic}
        Context: {data}
        
        Guidelines:
        - Word count: ~500 words for this section.
        - Use professional tone, markdown tables, and bullet points.
        - Ensure deep analysis, not just a summary.
        - Do not conclude the entire report yet.
        """
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": section_prompt}],
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        full_report += f"\n\n{content}\n\n"
        # Page separator for the PDF logic
        full_report += "\n\n---PAGE_BREAK---\n\n"
        
    return full_report