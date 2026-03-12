from config import client
from memory.vector_store import retrieve_data
import time

def analyze_market(topic, status_callback=None):
    data = retrieve_data(topic)
    
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
    
    for i, section in enumerate(sections):
        if status_callback:
            status_callback(i + 1, len(sections), section)
            
        section_prompt = f"""
        Role: Senior Market Research Strategist.
        Task: Write a detailed analysis for: "{section}" about {topic}.
        Context: {data}
        Guidelines: ~500 words, professional tone, markdown tables.
        """
        
        # Retry Logic for Rate Limits
        success = False
        retries = 0
        while not success and retries < 3:
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant", # Faster & High Limits
                    messages=[{"role": "user", "content": section_prompt}],
                    temperature=0.7
                )
                content = response.choices[0].message.content
                full_report += f"\n\n{content}\n\n"
                full_report += "\n\n---PAGE_BREAK---\n\n"
                success = True
                
                # Chota sa gap taaki limit hit na ho
                time.sleep(2) 
                
            except Exception as e:
                if "rate_limit" in str(e).lower():
                    status_callback(i + 1, len(sections), f"Waiting for API limit reset... (Attempt {retries+1})")
                    time.sleep(15) # Wait for 15 seconds
                    retries += 1
                else:
                    st.error(f"Error in {section}: {str(e)}")
                    break
        
    return full_report