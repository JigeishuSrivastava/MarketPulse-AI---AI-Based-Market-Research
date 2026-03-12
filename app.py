import streamlit as st
from fpdf import FPDF
from agents.planner_agent import create_research_plan
from agents.research_agent import collect_data
from agents.analyst_agent import analyze_market

# --- Professional PDF Generator ---
class MarketReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, 'InsightAI Strategic Intelligence - Confidential', 0, 1, 'R')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf(text, topic):
    pdf = MarketReportPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Cover Page
    pdf.add_page()
    pdf.set_font("Arial", 'B', 26)
    pdf.set_text_color(0, 51, 102) # Navy Blue
    pdf.ln(80)
    pdf.cell(200, 20, txt="MARKET RESEARCH REPORT", ln=True, align='C')
    pdf.ln(5)
    pdf.set_font("Arial", '', 16)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(200, 10, txt=f"Project: {topic.upper()}", ln=True, align='C')
    
    # Content Pages
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    pdf.set_text_color(0, 0, 0)
    
    sections = text.split("---PAGE_BREAK---")
    for section_text in sections:
        if section_text.strip():
            lines = section_text.split('\n')
            for line in lines:
                if line.startswith('#'):
                    pdf.set_font("Arial", 'B', 14)
                    pdf.set_text_color(0, 51, 102)
                    pdf.multi_cell(0, 10, txt=line.replace('#', '').strip())
                    pdf.set_font("Arial", '', 11)
                    pdf.set_text_color(0, 0, 0)
                else:
                    clean_line = line.encode('latin-1', 'replace').decode('latin-1')
                    pdf.multi_cell(0, 7, txt=clean_line)
            pdf.add_page()
            
    return pdf.output(dest='S').encode('latin-1')

# --- UI Config ---
st.set_page_config(page_title="InsightAI Pro", layout="wide")

# CSS for Visibility & Styling
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .report-box { 
        background-color: #ffffff !important; 
        padding: 50px; 
        border-radius: 15px; 
        border: 1px solid #d1d8e0;
        color: #1a1a1a !important; /* Force Black Text */
        line-height: 1.8;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .report-box h1, .report-box h2, .report-box h3 { color: #003366 !important; }
    .stButton>button { border-radius: 8px; height: 3.5em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Session State Initialization
if "final_report" not in st.session_state:
    st.session_state.final_report = None
if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""

st.title("MarketPulse AI - AI Based Market Research ")

topic_query = st.text_input("What market should I analyze?", placeholder="e.g. Fintech growth in MENA region")

if st.button("Generate Report"):
    if topic_query:
        # Progress Tracking
        p_bar = st.progress(0)
        status = st.empty()
        
        def update_ui(c, t, name):
            p_bar.progress(int((c/t)*100))
            status.markdown(f"**Working on Section {c}/{t}:** *{name}*")

        with st.spinner("Executing Multi-Agent Workflow..."):
            # Execute Agents
            plan = create_research_plan(topic_query)
            collect_data(plan)
            report_content = analyze_market(topic_query, status_callback=update_ui)
            
            # Save to state
            st.session_state.final_report = report_content
            st.session_state.last_topic = topic_query
            
        status.success("✅ Deep Analysis Complete!")

# Persistence Layer
if st.session_state.final_report:
    st.markdown("---")
    
    # Download Section
    col_dl, _ = st.columns([1, 4])
    with col_dl:
        pdf_data = create_pdf(st.session_state.final_report, st.session_state.last_topic)
        st.download_button(
            label="📥 Download Strategic PDF",
            data=pdf_data,
            file_name=f"InsightAI_{st.session_state.last_topic.replace(' ','_')}.pdf",
            mime="application/pdf"
        )
    
    # Professional Preview
    st.markdown(f'<div class="report-box">', unsafe_allow_html=True)
    st.markdown(st.session_state.final_report)
    st.markdown('</div>', unsafe_allow_html=True)