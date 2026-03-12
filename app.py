import streamlit as st
from fpdf import FPDF
from agents.planner_agent import create_research_plan
from agents.research_agent import collect_data
from agents.analyst_agent import analyze_market

# --- PDF Class ---
class MarketReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, 'InsightAI Strategic Report', 0, 1, 'R')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf(text, topic):
    pdf = MarketReportPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Cover
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(0, 51, 102)
    pdf.ln(80)
    pdf.cell(200, 20, txt="MARKET INTELLIGENCE REPORT", ln=True, align='C')
    pdf.set_font("Arial", '', 14)
    pdf.cell(200, 10, txt=f"Topic: {topic.upper()}", ln=True, align='C')
    
    # Content
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    pdf.set_text_color(0, 0, 0)
    
    sections = text.split("---PAGE_BREAK---")
    for section_text in sections:
        if section_text.strip():
            for line in section_text.split('\n'):
                if line.startswith('#'):
                    pdf.set_font("Arial", 'B', 13)
                    pdf.set_text_color(0, 51, 102)
                    pdf.multi_cell(0, 10, txt=line.replace('#', '').strip())
                    pdf.set_font("Arial", '', 11)
                    pdf.set_text_color(0, 0, 0)
                else:
                    pdf.multi_cell(0, 7, txt=line.encode('latin-1', 'replace').decode('latin-1'))
            pdf.add_page()
            
    return pdf.output(dest='S').encode('latin-1')

# --- UI Setup ---
st.set_page_config(page_title="MarketPulse AI", layout="wide")

st.markdown("""
    <style>
    .report-card { 
        background-color: #ffffff !important; 
        padding: 40px; 
        border-radius: 12px; 
        border: 1px solid #d1d8e0;
        color: #1a1a1a !important;
        line-height: 1.8;
    }
    .stButton>button { background-color: #004a99; color: white; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

if "report_data" not in st.session_state:
    st.session_state.report_data = None
if "curr_topic" not in st.session_state:
    st.session_state.curr_topic = ""

st.title("📊 MarketPulse AI - Professional Insights")

topic = st.text_input("Analysis Topic", placeholder="Enter market to analyze...")

if st.button("Generate Detailed Report"):
    if topic:
        progress = st.progress(0)
        status = st.empty()
        
        def update_progress(c, t, s):
            progress.progress(int((c/t)*100))
            status.markdown(f"⏳ **Processing {c}/{t}:** {s}")

        with st.spinner("Analyzing..."):
            plan = create_research_plan(topic)
            collect_data(plan)
            report = analyze_market(topic, status_callback=update_progress)
            st.session_state.report_data = report
            st.session_state.curr_topic = topic
        status.success("Analysis Finished!")

if st.session_state.report_data:
    st.markdown("---")
    pdf_bytes = create_pdf(st.session_state.report_data, st.session_state.curr_topic)
    st.download_button("📥 Download Report", data=pdf_bytes, file_name=f"{st.session_state.curr_topic}.pdf")
    st.markdown(f'<div class="report-card">{st.session_state.report_data}</div>', unsafe_allow_html=True)