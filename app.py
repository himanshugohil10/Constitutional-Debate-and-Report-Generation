import streamlit as st
import time
from utils.rag_loader import load_rag_data
from utils.llm_client import GroqClient
from utils.debate_manager import DebateManager

st.set_page_config(page_title="Constitutional Debate AI", layout="wide")

st.title("⚖️ Constitutional Argument Generator")

# Sidebar Configuration
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Groq API Key", type="password")
model_name = st.sidebar.text_input("Model Name", value="llama-3.3-70b-versatile")

# Main Input
st.header("Case Details")
case_summary = st.text_area("Enter Case Summary (Max 2 pages)", height=200)

# Session State Initialization
if "debate_history" not in st.session_state:
    st.session_state.debate_history = []
if "reports_generated" not in st.session_state:
    st.session_state.reports_generated = False
if "for_report" not in st.session_state:
    st.session_state.for_report = None
if "against_report" not in st.session_state:
    st.session_state.against_report = None

def run_debate():
    if not api_key or not case_summary:
        st.error("Please provide API Key and Case Summary.")
        return

    # Load RAG Data
    rag_data = load_rag_data()
    if "Error" in rag_data:
        st.error(rag_data)
        return
        
    st.info("RAG Data Loaded Successfully.")

    # Initialize Client & Manager
    client = GroqClient(api_key, model_name)
    manager = DebateManager(client, rag_data)

    st.session_state.debate_history = []
    current_history_text = ""
    st.session_state.reports_generated = False
    st.session_state.for_report = None
    st.session_state.against_report = None
    
    # Debate Rounds (3 per side = 6 total)
    roles = ["FOR", "AGAINST"] * 3
    
    progress_bar = st.progress(0)
    
    for i, role in enumerate(roles):
        st.subheader(f"Round {i+1}: {role} Argument")
        with st.spinner(f"Generating {role} argument..."):
            messages = manager.construct_debate_prompt(role, case_summary, current_history_text)
            response = client.generate_response(messages)
            
            st.write(response)
            st.session_state.debate_history.append({"role": role, "content": response})
            current_history_text += f"\n\n[{role}]: {response}"
            
            progress_bar.progress((i + 1) / 6)
            
    st.success("Debate Rounds Completed.")
    
    # Generate Reports
    st.header("Final Strategic Reports")
    
    with st.spinner("Generating FOR Side Report..."):
        for_messages = manager.construct_report_prompt("FOR", case_summary, current_history_text)
        for_report = client.generate_response(for_messages)
        st.session_state.for_report = for_report
        st.subheader("FOR Side Report")
        st.markdown(for_report)
        st.download_button("Download FOR Report", for_report, file_name="for_report.md")
        
    with st.spinner("Generating AGAINST Side Report..."):
        against_messages = manager.construct_report_prompt("AGAINST", case_summary, current_history_text)
        against_report = client.generate_response(against_messages)
        st.session_state.against_report = against_report
        st.subheader("AGAINST Side Report")
        st.markdown(against_report)
        st.download_button("Download AGAINST Report", against_report, file_name="against_report.md")

    st.session_state.reports_generated = True

def display_existing_results():
    if st.session_state.debate_history:
        st.info("RAG Data Loaded Successfully.") # Restoring context visually
        
    for i, item in enumerate(st.session_state.debate_history):
        role = item["role"]
        content = item["content"]
        st.subheader(f"Round {i+1}: {role} Argument")
        st.write(content)
        
    if st.session_state.debate_history:
        st.success("Debate Rounds Completed.")
        
    if st.session_state.reports_generated:
        st.header("Final Strategic Reports")
        
        if st.session_state.for_report:
            st.subheader("FOR Side Report")
            st.markdown(st.session_state.for_report)
            st.download_button("Download FOR Report", st.session_state.for_report, file_name="for_report.md")
            
        if st.session_state.against_report:
            st.subheader("AGAINST Side Report")
            st.markdown(st.session_state.against_report)
            st.download_button("Download AGAINST Report", st.session_state.against_report, file_name="against_report.md")

if st.button("Start Debate"):
    run_debate()
elif st.session_state.debate_history:
    display_existing_results()
